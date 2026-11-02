#!/usr/bin/env python3
"""One entry point for pinned host tools, native skills and Multica configuration."""
import argparse
import copy
import fcntl
import json
import os
from pathlib import Path
import shutil
import sys
import time
import tomllib

import bootstrap_tools
import install_multica
from catalog import SPECS, SQUADS, SKILLS

ROOT = Path(__file__).resolve().parents[1]


def config(path):
    data = tomllib.loads(path.read_text())
    multica = data.get('multica', {})
    host = data.get('host', {})
    profiles = multica.get('squad_profiles', list(SQUADS))
    if not profiles or not isinstance(profiles, list) or set(profiles) - set(SQUADS) or len(profiles) != len(set(profiles)):
        raise ValueError('squad_profiles must name unique known squad profiles')
    overrides = data.get('runtime_map', {})
    if set(overrides) - set(SPECS):
        raise ValueError('runtime_map contains an unknown role')
    root = Path(host.get('tool_root', '.multica/tools')).expanduser()
    if not root.is_absolute():
        root = ROOT / root
    research = host.get('research', True)
    environment = bootstrap_tools.target(root, research)
    ids = {overrides.get(role, multica.get('runtime_id', '')) for role in SPECS}
    research_context = ('The research pack is enabled: PDF libraries include pypdf, pdfplumber and pypdfium2; '
                        'numerical/plotting libraries include NumPy and Matplotlib.' if research else
                        'The research pack is disabled; this setup does not provision PDF or numerical/plotting libraries.')
    context = (f'Runtime tools provisioned for this configured host: `{environment / "venv/bin"}`. '
               f'Use `{environment / "venv/bin/python"}` for the toolkit and '
               f'`{ROOT / "scripts/quality_check.py"}` for bounded quality evidence. '
               'Use explicit project test/coverage commands and the correct project environment. '
               'Host installation is not proof of managed-run capability; report inaccessible paths or tools. '
               + research_context)
    args = argparse.Namespace(workspace_id=multica.get('workspace_id', ''), runtime_id=multica.get('runtime_id', ''),
                              profile=multica.get('profile'), squad_name=None, squad_profile=profiles[0],
                              update_existing=multica.get('update_existing', False), reuse_existing=False,
                              overwrite_skills=False, apply=False, runtime_map=overrides,
                              runtime_context={runtime: context for runtime in ids})
    return data, args, profiles, root, research


def files(path):
    result = {}
    for p in path.rglob('*'):
        if p.is_symlink():
            raise ValueError(f'Refusing symlink in native skill: {p}')
        if p.is_file():
            result[p.relative_to(path).as_posix()] = p.read_bytes()
    return result


def native_plan(data):
    plan = []
    for value in data.get('native', {}).get('skill_directories', []):
        base = Path(value).expanduser().absolute()
        for parent in (base, *base.parents):
            if parent.is_symlink():
                raise ValueError(f'Refusing symlink native skill destination: {parent}')
        for name in SKILLS:
            source, target = ROOT / 'skills' / name, base / name
            if target.exists() and not target.is_dir():
                raise ValueError(f'Native skill target is not a directory: {target}')
            action = 'create' if not target.exists() else ('reuse' if files(source) == files(target) else 'replace')
            if action == 'replace' and not data['multica'].get('update_existing', False):
                raise ValueError(f'Native skill differs: {target}; explicit update_existing is required')
            plan.append((source, target, action))
    return plan


def verify_workspace(args, profiles):
    """Read back every shared role/skill and selected squad without mutation."""
    manifest = install_multica.prepare_bundle()
    skill_items = install_multica.collection(install_multica.cli(args, ['skill', 'list']), 'skills')
    skills = install_multica.matching_objects(skill_items, SKILLS, 'Skill')
    ids = {}
    for name in SKILLS:
        if name not in skills:
            raise ValueError(f'Missing skill: {name}')
        ids[name] = install_multica.id_value(skills[name])
        install_multica.verify_skill(args, name, ids[name], manifest)
    agent_items = install_multica.collection(install_multica.cli(args, ['agent', 'list', '--include-archived']), 'agents')
    agents = install_multica.matching_objects(agent_items, [v[0] for v in SPECS.values()], 'Agent')
    role_ids = {}
    for role, (name, _, _) in SPECS.items():
        if name.casefold() not in agents:
            raise ValueError(f'Missing role: {name}')
        role_ids[role] = install_multica.id_value(agents[name.casefold()])
        install_multica.verify_agent(args, role, role_ids[role], ids, check_description=True)
    squad_items = install_multica.collection(install_multica.cli(args, ['squad', 'list']), 'squads')
    squads = install_multica.matching_objects(squad_items, [SQUADS[p]['name'] for p in profiles], 'Squad')
    for profile in profiles:
        name = SQUADS[profile]['name']
        if name.casefold() not in squads:
            raise ValueError(f'Missing squad: {name}')
        squad_id = install_multica.id_value(squads[name.casefold()])
        detail = install_multica.object_response(install_multica.cli(args, ['squad', 'get', squad_id]), 'squad')
        expected = (install_multica.BUNDLE / 'squads' / (profile + '.md')).read_text()
        if detail.get('instructions') != expected or detail.get('leader_id') != role_ids['lead']:
            raise ValueError(f'Squad configuration differs: {name}')
        members = install_multica.collection(install_multica.cli(args, ['squad', 'member', 'list', squad_id]), 'members')
        actual = [m['member_id'] for m in members if m.get('member_type') == 'agent' and m.get('member_id') != role_ids['lead']]
        wanted = {role_ids[role] for role in SQUADS[profile]['members']}
        if set(actual) != wanted or len(actual) != len(wanted):
            raise ValueError(f'Squad membership differs: {name}')


def snapshot_managed(args, profiles, destination):
    """Keep only fields needed to inspect/recover managed configuration changes."""
    snapshot = {'workspace': args.workspace_id, 'agents': [], 'skills': [], 'squads': []}
    targets = {'agent': {value[0].casefold() for value in SPECS.values()},
               'skill': {name.casefold() for name in SKILLS},
               'squad': {SQUADS[p]['name'].casefold() for p in profiles}}
    for kind, names in targets.items():
        items = install_multica.collection(install_multica.cli(args, [kind, 'list']), kind + 's')
        for item in items:
            if item.get('name', '').casefold() not in names:
                continue
            command = [kind, 'get', str(item['id'])] + (['--with-content'] if kind == 'skill' else [])
            detail = install_multica.object_response(install_multica.cli(args, command), kind)
            fields = {'agent': ('id', 'name', 'description', 'instructions', 'runtime_id'),
                      'skill': ('id', 'name', 'content', 'files'),
                      'squad': ('id', 'name', 'instructions', 'leader_id')}[kind]
            saved = {key: detail[key] for key in fields if key in detail}
            if kind == 'agent':
                saved['skills'] = install_multica.cli(args, ['agent', 'skills', 'list', str(item['id'])])
            elif kind == 'squad':
                saved['members'] = install_multica.cli(args, ['squad', 'member', 'list', str(item['id'])])
            snapshot[kind + 's'].append(saved)
    with open(destination, 'x', opener=lambda path, flags: os.open(path, flags, 0o600)) as output:
        json.dump(snapshot, output, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--plan', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--doctor', action='store_true')
    parser.add_argument('--host-only', action='store_true', help='Provision/check only this host, without contacting Multica')
    options = parser.parse_args()
    data, args, profiles, tool_root, research = config(options.config)
    native = native_plan(data)
    if not options.host_only:
        if not args.workspace_id or not args.runtime_id or 'REPLACE' in args.workspace_id + args.runtime_id:
            raise ValueError('Fill in the new workspace and runtime IDs in the configuration')
        required = {install_multica.runtime_for(args, role) for role in SPECS}
        if not required <= set(data.get('host', {}).get('local_runtime_ids', [])):
            raise ValueError('Every selected runtime must be explicitly declared local to this host; bootstrap other hosts there')
    if options.doctor:
        report = bootstrap_tools.doctor(bootstrap_tools.target(tool_root, research))
        for source, destination, _ in native:
            if not destination.is_dir() or files(source) != files(destination):
                raise ValueError(f'Native skill missing or changed: {destination}')
        if not options.host_only:
            verify_workspace(args, profiles)
            report['workspace'] = 'configuration-read-back-passed'
        print(json.dumps(report, indent=2)); return
    # Preview every selected workspace target before host or remote installation.
    if not options.host_only:
        for profile in profiles:
            args.squad_profile = profile
            args.squad_name = None
            install_multica.main(args)
    print(json.dumps({'tools': str(bootstrap_tools.target(tool_root, research)), 'research_pack': research,
                      'native_skills': [{'target': str(p), 'action': a} for _, p, a in native],
                      'squads': profiles, 'apply': options.apply}, indent=2))
    if not options.apply:
        print('Plan only; no tools, native skills or Multica objects installed.'); return
    state_dir = ROOT / '.multica/setup'
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / 'apply.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        journal = state_dir / f'{time.time_ns()}.json'
        state = {'workspace': args.workspace_id, 'steps': [], 'state': 'in-progress'}

        def record(step):
            state['steps'].append(step)
            journal.write_text(json.dumps(state, indent=2) + '\n')
        try:
            if args.update_existing and not options.host_only:
                snapshot = journal.with_suffix('.before.json')
                snapshot_managed(args, profiles, snapshot)
                record({'before_configuration': str(snapshot)})
            report = bootstrap_tools.install(tool_root, research)
            record({'host': report})
            for source, destination, action in native:
                if action == 'reuse':
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                if action == 'replace':
                    backup = state_dir / 'native-backups' / str(time.time_ns()) / destination.name
                    backup.parent.mkdir(parents=True)
                    shutil.move(str(destination), str(backup))
                    record({'native_backup': str(backup)})
                shutil.copytree(source, destination)
                record({'native_skill': str(destination)})
            if not options.host_only:
                for index, profile in enumerate(profiles):
                    item = copy.copy(args)
                    item.squad_name = None
                    item.squad_profile = profile
                    item.apply = True
                    item.reuse_existing = bool(index and not item.update_existing)
                    install_multica.main(item)
                    record({'squad': profile, 'state': 'configuration-read-back-passed'})
                verify_workspace(args, profiles)
            state['state'] = 'configured'
            record({'managed_run_verified': False, 'next': 'Seed parked pilot issues and explicitly launch one case'})
            print(f'Setup configured. Journal: {journal}. Managed-run behavior still needs the pilot.')
        except Exception:
            state['state'] = 'partial-failure'
            record({'next': 'Inspect actual objects and retry with update_existing=true; no automatic rollback'})
            raise


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, bootstrap_tools.BootstrapError, install_multica.InstallError) as error:
        raise SystemExit(str(error))
