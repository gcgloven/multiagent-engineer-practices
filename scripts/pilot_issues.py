#!/usr/bin/env python3
"""Preview/seed parked Multica pilot issues; launch exactly one case explicitly."""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from catalog import SQUADS
from pilot_cases import CASES, FIXTURES

ROOT = Path(__file__).resolve().parents[1]


class PilotError(Exception):
    pass


def collection(value, key):
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return value
    if isinstance(value, dict):
        if value.get('has_more') or value.get('next_cursor'):
            raise PilotError('Incomplete result; refusing to assume a ticket or squad is absent')
        for candidate in (key, 'items', 'data', 'results'):
            if candidate in value:
                return collection(value[candidate], key)
    raise PilotError(f'Unexpected {key} response')


def obj(value):
    if isinstance(value, dict):
        if value.get('id'):
            return value
        for key in ('issue', 'project', 'data', 'result'):
            if key in value:
                return obj(value[key])
    raise PilotError('Response has no object identity')


class Client:
    def __init__(self, workspace, profile=None):
        self.workspace = workspace
        self.prefix = ['multica'] + (['--profile', profile] if profile else []) + ['--workspace-id', workspace]
        result = subprocess.run(['multica', 'version'], capture_output=True, text=True, timeout=15)
        version = re.search(r'\bmultica\s+(\d+)\.(\d+)\.(\d+)', result.stdout)
        if result.returncode or not version or tuple(map(int, version.groups())) < (0, 7, 1):
            raise PilotError('Multica CLI 0.7.1 or newer is required')

    def call(self, *command):
        try:
            response = subprocess.run(self.prefix + list(command) + ['--output', 'json'],
                                      cwd=ROOT, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise PilotError(f'CLI outcome uncertain for {" ".join(command[:2])}; inspect before retrying') from error
        if response.returncode:
            raise PilotError(f'CLI {" ".join(command[:2])} failed ({response.returncode}); output withheld to avoid exposing secrets')
        try:
            return json.loads(response.stdout)
        except ValueError as error:
            raise PilotError('CLI response was not JSON; reconcile the workspace before retrying') from error


def marker(batch, case):
    return f'multica-pilot:{batch}:{case["id"]}'


def description(batch, case, workdir):
    return (f'{case["request"]}\n\nWorking directory in the agent runtime: '
            f'`{workdir / batch / case["id"]}`. Use only this case directory for new files. '
            'If it is unavailable, report the access gap before implementation.\n\n'
            f'Pilot identity: `{marker(batch, case)}`\n')


def descriptions_match(actual, expected):
    """Multica trims the file's final newline; retain all meaningful text checks."""
    return (isinstance(actual, str)
            and actual.replace('\r\n', '\n').rstrip('\n')
            == expected.replace('\r\n', '\n').rstrip('\n'))


def init_fixtures(workdir, batch):
    destination = workdir / batch
    if destination.exists():
        raise PilotError(f'Fixture directory already exists; refusing to reset prior work: {destination}')
    destination.mkdir(parents=True)
    for case in CASES:
        path = destination / case['id']
        path.mkdir()
        for name, content in FIXTURES.get(case['id'], {}).items():
            (path / name).write_text(content, encoding='utf-8')
    (destination / 'README.md').write_text('Disposable pilot inputs. Each case owns its directory. Do not reset these files during an active test.\n')
    return destination


def find_existing(client, batch, project):
    items = collection(client.call('issue', 'search', batch,
                                   '--include-closed', '--limit', '100'), 'issues')
    if len(items) >= 100:
        raise PilotError('Pilot search may be truncated; use a narrower/new batch after inspecting existing tickets')
    found = {}
    for item in items:
        issue = obj(client.call('issue', 'get', str(item['id'])))
        for case in CASES:
            token = f'`{marker(batch, case)}`'
            if token not in issue.get('description', ''):
                if issue.get('title', '').startswith(f'[PILOT {batch} {case["id"]}]'):
                    raise PilotError('Pilot title exists but its identity marker is missing; inspect before retrying')
                continue
            if issue.get('project_id') != project or issue.get('workspace_id', client.workspace) != client.workspace:
                raise PilotError('This batch already exists in another project/workspace; choose a new batch identifier')
            if case['id'] in found:
                raise PilotError(f'Duplicate pilot identity: {case["id"]}; resolve it manually')
            found[case['id']] = issue
    return found


def seed(client, batch, project, workdir, cases, apply=False, squad_names=None):
    project_obj = obj(client.call('project', 'get', project))
    if project_obj['id'] != project or project_obj.get('workspace_id', client.workspace) != client.workspace:
        raise PilotError('Project does not belong to the selected workspace')
    squads = collection(client.call('squad', 'list'), 'squads')
    targets = {}
    for case in cases:
        name = (squad_names or {}).get(case['squad'], SQUADS[case['squad']]['name'])
        matches = [s for s in squads if s.get('name') == name]
        if len(matches) != 1:
            raise PilotError(f'Expected exactly one squad named {name}; install/configure it before seeding')
        targets[case['id']] = str(matches[0]['id'])
    existing = find_existing(client, batch, project)
    # Validate all selected existing objects before any mutation.
    for case in cases:
        item = existing.get(case['id'])
        if item and item.get('assignee_id') not in (None, '', targets[case['id']]):
            raise PilotError(f'{case["id"]} has a different owner; refusing to reassign it')
        if item and item.get('assignee_id') and item.get('assignee_type') != 'squad':
            raise PilotError(f'{case["id"]} is not assigned to a squad; inspect before retrying')
        if item and not descriptions_match(item.get('description'), description(batch, case, workdir)):
            raise PilotError(f'{case["id"]} description or runtime directory changed; inspect it or use a new batch')
        if item and not item.get('assignee_id') and item.get('status') != 'backlog':
            raise PilotError('Unassigned existing case is no longer backlog; refusing to change ownership')
    report = []
    for case in cases:
        item = existing.get(case['id'])
        action = 'reuse' if item else 'create backlog'
        if apply:
            if item is None:
                body_dir = ROOT / '.multica/pilot-descriptions' / batch
                body_dir.mkdir(parents=True, exist_ok=True)
                body = body_dir / (case['id'] + '.md')
                body.write_text(description(batch, case, workdir), encoding='utf-8')
                item = obj(client.call('issue', 'create', '--title', f'[PILOT {batch} {case["id"]}] {case["title"]}',
                                       '--description-file', str(body.relative_to(ROOT)), '--project', project,
                                       '--status', 'backlog'))
                item = obj(client.call('issue', 'get', str(item['id'])))
                if (item.get('status') != 'backlog' or item.get('project_id') != project
                        or not descriptions_match(item.get('description'), description(batch, case, workdir))):
                    raise PilotError('Created issue read-back differs; inspect before retrying')
            if not item.get('assignee_id'):
                if item.get('status') != 'backlog':
                    raise PilotError('Unassigned existing case is no longer backlog; refusing to change ownership')
                client.call('issue', 'assign', str(item['id']), '--to-id', targets[case['id']], '--no-start')
                item = obj(client.call('issue', 'get', str(item['id'])))
                if (item.get('assignee_id') != targets[case['id']] or item.get('assignee_type') != 'squad'
                        or item.get('status') != 'backlog'):
                    raise PilotError('Ownership/status read-back differs; inspect before retrying')
        report.append({'case': case['id'], 'action': action, 'issue_id': item['id'] if item else None,
                       'identifier': item.get('identifier') if item else None,
                       'status': item.get('status') if item else None,
                       'assignee_type': item.get('assignee_type') if item else None,
                       'squad_id': targets[case['id']], 'expected': case['expected']})
        print(f'{case["id"]}: {action}; issue={item["id"] if item else "not created"}', flush=True)
    return report


def launch(client, batch, project, case_id, apply, workdir, squad_names=None):
    found = find_existing(client, batch, project)
    if case_id not in found:
        raise PilotError('Case has not been seeded')
    issue = found[case_id]
    if issue.get('status') != 'backlog' or not issue.get('assignee_id'):
        raise PilotError('Launch requires an assigned backlog issue; it will not rerun an active/completed case')
    case = next(c for c in CASES if c['id'] == case_id)
    name = (squad_names or {}).get(case['squad'], SQUADS[case['squad']]['name'])
    squads = collection(client.call('squad', 'list'), 'squads')
    matches = [s for s in squads if s.get('name') == name]
    if (len(matches) != 1 or str(matches[0]['id']) != issue['assignee_id']
            or issue.get('assignee_type') != 'squad'):
        raise PilotError('Case ownership no longer matches the configured squad; inspect before launching')
    if not descriptions_match(issue.get('description'), description(batch, case, workdir)):
        raise PilotError('Case description or runtime directory changed; inspect before launching')
    runs = collection(client.call('issue', 'runs', str(issue['id'])), 'runs')
    if runs:
        raise PilotError('Case already has run history; use a new batch for a clean retest')
    if apply:
        client.call('issue', 'status', str(issue['id']), 'todo')
        state = obj(client.call('issue', 'get', str(issue['id'])))
        if state.get('status') == 'backlog':
            raise PilotError('Launch outcome uncertain; inspect runs before retrying')
    return {'case': case_id, 'issue_id': issue['id'], 'action': 'launch requested' if apply else 'would launch'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-id')
    parser.add_argument('--project-id')
    parser.add_argument('--profile')
    parser.add_argument('--batch', default='pilot-v2')
    parser.add_argument('--workdir', type=Path)
    parser.add_argument('--cases', default=','.join(c['id'] for c in CASES))
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--init-fixtures', action='store_true')
    parser.add_argument('--launch', choices=[c['id'] for c in CASES])
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--squad-map', type=Path, help='JSON map of profile keys to exact custom squad names')
    args = parser.parse_args()
    if args.list:
        print(json.dumps(CASES, indent=2)); return
    if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]{0,47}', args.batch):
        raise PilotError('Batch must be a short letter-led identifier using letters, digits, _ or -')
    if args.init_fixtures:
        if not args.workdir or not args.workdir.is_absolute() or args.launch or args.apply:
            raise PilotError('--init-fixtures requires an absolute --workdir and cannot launch/apply tickets')
        print(init_fixtures(args.workdir, args.batch)); return
    if not args.workspace_id or not args.project_id:
        raise PilotError('Explicit --workspace-id and --project-id are required')
    if not args.workdir or not args.workdir.is_absolute():
        raise PilotError('Supply the absolute --workdir as seen by the worker runtime')
    selected = args.cases.split(',')
    if set(selected) - {c['id'] for c in CASES} or len(set(selected)) != len(selected):
        raise PilotError('Unknown or repeated case ID')
    names = json.loads(args.squad_map.read_text()) if args.squad_map else None
    if names is not None and (not isinstance(names, dict) or set(names) - set(SQUADS)
                              or any(not isinstance(v, str) or not v.strip() for v in names.values())):
        raise PilotError('Squad map must map known profile keys to nonempty squad names')
    client = Client(args.workspace_id, args.profile)
    key = hashlib.sha256(f'{args.profile}:{args.workspace_id}:{args.project_id}:{args.batch}'.encode()).hexdigest()[:20]
    state_dir = ROOT / '.multica/pilot-state'
    state_dir.mkdir(parents=True, exist_ok=True)
    # This lock prevents concurrent invocations on this checkout only.
    with (state_dir / f'{key}.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise PilotError('Another local invocation is handling this batch') from error
        if args.launch:
            report = launch(client, args.batch, args.project_id, args.launch, args.apply, args.workdir, names)
        else:
            report = seed(client, args.batch, args.project_id, args.workdir,
                          [c for c in CASES if c['id'] in selected], args.apply, names)
        (state_dir / f'{key}.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2))
        if not args.apply:
            print('Preview only: no Multica changes. Add --apply to perform the displayed action.')


if __name__ == '__main__':
    try:
        main()
    except (PilotError, OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error))
