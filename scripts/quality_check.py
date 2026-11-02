#!/usr/bin/env python3
"""Run bounded quality evidence on explicitly named files; never grants approval."""
import argparse
from collections.abc import Mapping
import hashlib
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import time

SUPPORTED = {'.py', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.java', '.go', '.rs', '.clj', '.cljc', '.cljs'}


class QualityError(Exception):
    pass


def read_edn(path):
    try:
        import edn_format
    except ImportError as error:
        raise QualityError('Use the installed toolkit Python: edn-format is required') from error

    def normalize(value):
        if isinstance(value, Mapping):
            return {str(k).lstrip(':'): normalize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)) or type(value).__name__ == 'ImmutableList':
            return [normalize(v) for v in value]
        return value
    try:
        result = normalize(edn_format.loads(path.read_text()))
    except Exception as error:
        raise QualityError(f'Cannot parse quality report: {path.name}') from error
    if not isinstance(result, dict):
        raise QualityError(f'Unexpected quality report shape: {path.name}')
    return result


def execute(command, root, deadline, log):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise QualityError('Quality-check budget exhausted')
    with log.open('w') as output:
        process = subprocess.Popen(command, cwd=root, stdout=output, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            return process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as error:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            raise QualityError('Quality-check budget exhausted; process group stopped') from error


def assess(crap, duplicates, mutations=None):
    gaps, findings = [], []
    entries = crap.get('entries', [])
    if not entries:
        gaps.append('No analyzed functions')
    if any(e.get('coverage') is None or e.get('crap') is None for e in entries):
        gaps.append('Missing coverage or CRAP measurement')
    if any(e.get('coverage', 0) == 0 for e in entries):
        gaps.append('One or more analyzed functions have zero reported coverage')
    if any(e.get('crap') is not None and e['crap'] >= 10 for e in entries):
        findings.append('CRAP score at or above 10 requires scoped review')
    if duplicates.get('candidates'):
        findings.append('Duplicate candidates require semantic review')
    if mutations is not None:
        forms = [form for report in mutations for form in report.get('forms', [])]
        if sum(f.get('killed', 0) + f.get('survived', 0) for f in forms) == 0:
            gaps.append('No executed mutants')
        if any(f.get('uncovered', 0) for f in forms):
            gaps.append('Uncovered mutation sites')
        if any(f.get('survived', 0) for f in forms):
            findings.append('Surviving mutants require test-effectiveness review')
        findings.append('Interpret mutation logs: a killed mutant can include timeout or compile failure')
    return {'evidence_gaps': gaps, 'review_items': findings,
            'state': 'evidence-gap' if gaps else ('review-required' if findings else 'checks-complete'),
            'independent_review': 'not established by this command'}


def run(args):
    root = args.repo.resolve()
    paths = []
    for name in args.paths:
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.suffix not in SUPPORTED:
            raise QualityError(f'Unsupported, absent or outside-scope file: {name}')
        paths.append(path)
    if not args.test_command.strip() or args.seconds <= 0 or args.workers < 1:
        raise QualityError('Test command and positive time/worker limits are required')
    if args.profile != 'quick-mvp' and (not args.coverage_command or not args.coverage_report):
        raise QualityError('Standard/rigorous checks require an explicit coverage command and report path')
    report_dir = root / '.quality-evidence' / str(time.time_ns())
    report_dir.mkdir(parents=True)
    start_ns = time.time_ns()
    deadline = time.monotonic() + args.seconds
    digest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    report = {'candidate_files': digest, 'profile': args.profile, 'logs': str(report_dir)}
    try:
        if execute(shlex.split(args.test_command), root, deadline, report_dir / 'baseline.log'):
            raise QualityError('Baseline tests failed; quality interpretation blocked')
        if args.profile == 'quick-mvp':
            report.update(state='checks-complete', independent_review='not established by this command')
        else:
            relative = [str(p.relative_to(root)) for p in paths]
            command = [str(args.bin / 'crapper'), '--coverage-command', args.coverage_command, *relative]
            if execute(command, root, deadline, report_dir / 'crapper.log'):
                raise QualityError('Complexity/coverage command failed')
            coverage = (root / args.coverage_report).resolve()
            if not coverage.is_relative_to(root) or not coverage.is_file() or coverage.stat().st_mtime_ns < start_ns:
                raise QualityError('Expected fresh project coverage report is absent')
            if execute([str(args.bin / 'dryer'), '--threshold', '0.8', *relative], root, deadline, report_dir / 'dryer.log'):
                raise QualityError('Duplication analysis failed')
            snapshots = []
            for name in ('crap.edn', 'dry.edn'):
                path = root / '.metrics' / name
                if not path.exists() or path.stat().st_mtime_ns < start_ns:
                    raise QualityError(f'Fresh {name} is absent')
                snapshots.append(read_edn(path))
            mutations = None
            if args.profile == 'rigorous':
                mutation_start = time.time_ns()
                code = execute([str(args.bin / 'mutator'), '--mutate-all', '--use-existing-coverage',
                                '--test-command', args.test_command, '--max-workers', str(args.workers),
                                *relative], root, deadline, report_dir / 'mutator.log')
                if code not in (0, 3):
                    raise QualityError(f'Mutation command failed or baseline invalid (exit {code})')
                mutations = [read_edn(p) for p in (root / '.metrics/mutate').glob('*.edn')
                             if p.stat().st_mtime_ns >= mutation_start]
            report.update(assess(*snapshots, mutations))
        if any(hashlib.sha256(p.read_bytes()).hexdigest() != digest[str(p.relative_to(root))] for p in paths):
            raise QualityError('Candidate changed during checks; results cannot certify the original candidate')
    except (QualityError, OSError, ValueError) as error:
        report.update(state='blocked', reason=str(error))
    (report_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 2 if report['state'] in ('blocked', 'evidence-gap') else (1 if report['state'] == 'review-required' else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--bin', type=Path, default=Path(sys.executable).parent)
    parser.add_argument('--profile', choices=['quick-mvp', 'standard', 'rigorous'], default='standard')
    parser.add_argument('--test-command', required=True)
    parser.add_argument('--coverage-command')
    parser.add_argument('--coverage-report')
    parser.add_argument('--seconds', type=int, default=300)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('paths', nargs='+')
    return run(parser.parse_args())


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (QualityError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
