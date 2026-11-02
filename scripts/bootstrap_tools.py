#!/usr/bin/env python3
"""Install pinned quality tools on this host; never calls Multica or starts agents."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'toolkits.lock.json'
REQUIREMENTS = ROOT / 'requirements-quality.lock'


class BootstrapError(Exception):
    pass


def run(command, cwd=None, timeout=300):
    try:
        result = subprocess.run([str(x) for x in command], cwd=cwd, text=True,
                                capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise BootstrapError(f'{Path(str(command[0])).name} failed: {type(error).__name__}') from error
    if result.returncode:
        raise BootstrapError(f'{Path(str(command[0])).name} failed (exit {result.returncode}); command output withheld to avoid exposing environment secrets')
    return result.stdout.strip()


def lock_bytes(research=False):
    return LOCK.read_bytes() + REQUIREMENTS.read_bytes() + ((ROOT / 'requirements-research.lock').read_bytes() if research else b'')


def target(root, research=False):
    digest = hashlib.sha256(lock_bytes(research)
                            + f'{sys.version_info[:2]}:{sys.platform}'.encode()).hexdigest()[:16]
    return Path(root).expanduser().absolute() / digest


def doctor(directory):
    directory = Path(directory)
    marker = directory / 'installation.json'
    python = directory / 'venv/bin/python'
    if not marker.is_file() or not python.is_file():
        raise BootstrapError(f'Quality environment is not installed: {directory}')
    info = json.loads(marker.read_text())
    expected = hashlib.sha256(lock_bytes(info.get('research', False))).hexdigest()
    if info.get('fixture_checks') != 'passed':
        raise BootstrapError('Toolkit fixture checks have not passed')
    if info.get('lock_sha256') != expected:
        raise BootstrapError('Installed environment does not match the current toolkit lock')
    run([python, '-c', 'import crapper, dryer, mutator, edn_format; import mutator.crapper_link; mutator.crapper_link.ensure_crapper()'])
    run([python, '-m', 'pip', 'check'])
    requirement_files = [REQUIREMENTS] + ([ROOT / 'requirements-research.lock'] if info.get('research') else [])
    versions = {}
    for requirement_file in requirement_files:
        for line in requirement_file.read_text().splitlines():
            if line.strip() and not line.startswith('#'):
                name, version = line.split('==', 1)
                versions[name] = version
    actual = json.loads(run([python, '-c', 'import importlib.metadata as m,json; '
                              + f'names={list(versions)!r}; print(json.dumps({{n:m.version(n) for n in names}}))']))
    if actual != versions:
        raise BootstrapError('Installed dependency versions differ from the lock')
    for relative, digest in info.get('parser_files', {}).items():
        path = directory / 'cache' / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise BootstrapError('Installed parser cache changed or is incomplete')
    if not info.get('parser_files'):
        raise BootstrapError('No provisioned parser cache recorded')
    if info.get('research'):
        run([python, '-c', 'import numpy, matplotlib, pdfplumber, pypdf, pypdfium2'])
    for name in json.loads(LOCK.read_text())['tools']:
        run([directory / 'venv/bin' / name, '--help'])
    return {'state': 'host-checked', 'environment': str(directory),
            'bin': str(directory / 'venv/bin'), 'lock_sha256': expected,
            'research': info.get('research', False), 'managed_run_verified': False}


def install(root, research=False):
    if sys.version_info < (3, 11) or sys.platform != 'linux':
        raise BootstrapError('This bootstrap supports Linux with Python 3.11+; use a tested platform adapter elsewhere')
    if research and sys.version_info < (3, 12):
        raise BootstrapError('The research dependency lock requires Python 3.12+; validated on Linux Python 3.12')
    destination = target(root, research)
    for part in (destination, *destination.parents):
        if part.is_symlink():
            raise BootstrapError(f'Refusing symlink in installation path: {part}')
    if destination.exists():
        return doctor(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Build at its final path: virtualenv console scripts embed absolute paths.
    destination.mkdir()
    try:
        venv.EnvBuilder(with_pip=True).create(destination / 'venv')
        python = destination / 'venv/bin/python'
        run([python, '-m', 'pip', 'install', '--disable-pip-version-check', '--no-cache-dir',
             '--no-deps', '-r', REQUIREMENTS], timeout=600)
        if research:
            run([python, '-m', 'pip', 'install', '--no-deps', '--no-cache-dir', '-r', ROOT / 'requirements-research.lock'], timeout=600)
        site = Path(run([python, '-c', 'import sysconfig; print(sysconfig.get_paths()["purelib"])']))
        cache = destination / 'cache'
        cache.mkdir()
        (site / 'multica_tool_environment.py').write_text(
            'import os\nfrom tree_sitter_language_pack import configure\n'
            + f'configure({{"cache_dir": {str(cache / "parsers")!r}}})\n'
            + f'os.environ.setdefault("MPLCONFIGDIR", {str(cache / "matplotlib")!r})\n')
        (site / 'multica_tool_environment.pth').write_text('import multica_tool_environment\n')
        languages = ['python', 'javascript', 'typescript', 'tsx', 'java', 'go', 'rust']
        run([python, '-c', 'from tree_sitter_language_pack import download, get_parser; '
             + f'names={languages!r}; download(names); [get_parser(n) for n in names]'], timeout=300)
        tools = json.loads(LOCK.read_text())['tools']
        sources = destination / 'sources'
        sources.mkdir()
        for name, item in tools.items():
            path = sources / name
            run(['git', 'init', '-q', path])
            run(['git', '-C', path, 'remote', 'add', 'origin', item['repository']])
            run(['git', '-C', path, 'fetch', '--depth', '1', 'origin', item['commit']])
            run(['git', '-C', path, 'checkout', '--detach', '-q', item['commit']])
            if run(['git', '-C', path, 'rev-parse', 'HEAD']) != item['commit']:
                raise BootstrapError(f'Unexpected revision for {name}')
            run([python, '-m', 'pip', 'install', '--no-deps', '--no-build-isolation', path])
        marker = {'lock_sha256': hashlib.sha256(lock_bytes(research)).hexdigest(), 'research': research,
                  'tools': tools, 'python': sys.version.split()[0], 'parsers': languages,
                  'parser_files': {str(p.relative_to(cache)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (cache / 'parsers').rglob('*') if p.is_file()}}
        run([python, ROOT / 'scripts/test_toolkit_smoke.py', '--bin', destination / 'venv/bin'], timeout=180)
        marker['fixture_checks'] = 'passed'
        (destination / 'installation.json').write_text(json.dumps(marker, indent=2) + '\n')
        result = doctor(destination)
        result['fixture_checks'] = 'passed'
        return result
    except Exception as error:
        raise BootstrapError(f'Installation incomplete at {destination}. Inspect that directory before removing it and retrying. {error}') from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--research', action='store_true', help='Also install pinned PDF and numerical/plotting libraries')
    parser.add_argument('--root', type=Path, default=ROOT / '.multica/tools')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--doctor', action='store_true')
    args = parser.parse_args()
    if args.apply:
        result = install(args.root, args.research)
    elif args.doctor:
        result = doctor(target(args.root, args.research))
    else:
        result = {'state': 'planned', 'destination': str(target(args.root, args.research)),
                  'tools': json.loads(LOCK.read_text())['tools'], 'writes': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (BootstrapError, OSError, ValueError) as error:
        raise SystemExit(str(error))
