#!/usr/bin/env python3
"""Preview or install this kit using an already authenticated Multica CLI.

Select a squad workflow while keeping specialists reusable. Existing agents and
skills can be reused after compatibility checks, or explicitly updated in place.
Failed writes are not automatically rolled back; inspect partial objects before retrying.
"""
import argparse
import copy
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import prepare

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'build' / 'multica'
from catalog import SPECS
SKILLS = prepare.SKILLS


class InstallError(Exception):
    pass


def cli(args, command):
    cmd = ['multica']
    if args.profile:
        cmd += ['--profile', args.profile]
    cmd += ['--workspace-id', args.workspace_id] + command + ['--output', 'json']
    try:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise InstallError(f"Cannot run Multica CLI for {' '.join(command[:2])}: {type(error).__name__}") from error
    if result.returncode:
        # CLI errors can contain account details or provider secrets. Do not print them.
        raise InstallError(f"Multica command {' '.join(command[:2])} failed (exit {result.returncode}); inspect it separately with the CLI if needed")
    try:
        return json.loads(result.stdout)
    except ValueError as error:
        raise InstallError(f"Unexpected non-JSON response from {' '.join(command[:2])}") from error


def object_response(value, kind):
    if isinstance(value, dict):
        if isinstance(value.get('id'), (str, int)) and str(value['id']):
            return value
        for key in (kind, 'data', 'result'):
            if key in value:
                try:
                    return object_response(value[key], kind)
                except InstallError:
                    pass
    raise InstallError(f'Unrecognized {kind} response: missing object ID')


def collection(value, kind):
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return value
    if isinstance(value, dict):
        # Refuse paginated or ambiguous responses rather than assuming absence.
        if value.get('next_cursor') or value.get('nextCursor') or value.get('has_more') or value.get('hasMore'):
            raise InstallError(f'Cannot safely inspect paginated {kind} list')
        matches = [value[k] for k in (kind, 'items', 'data', 'results') if k in value]
        if len(matches) == 1:
            return collection(matches[0], kind)
    raise InstallError(f'Unrecognized {kind} list response; cannot verify workspace state')


def named(items, label):
    if any(not isinstance(item.get('name'), str) or not item.get('name') for item in items):
        raise InstallError(f'{label} list contains an item without a name; cannot check collisions')
    return {item['name'].casefold() for item in items}


def matching_objects(items, wanted, label):
    """Index only planned names, refusing ambiguous case-insensitive matches."""
    named(items, label)
    wanted = {name.casefold() for name in wanted}
    matches = {}
    for item in items:
        key = item['name'].casefold()
        if key not in wanted:
            continue
        if key in matches:
            raise InstallError(f'Ambiguous existing {label.lower()} name: {item["name"]}')
        matches[key] = item
    return matches


def id_value(item):
    value = item.get('id')
    if not isinstance(value, (str, int)) or not str(value):
        raise InstallError('Expected a nonempty object ID in CLI response')
    return str(value)


def prepare_bundle():
    # Rebuild from current checked sources, so stale archives cannot be installed.
    prepare.prepare(ROOT)
    manifest = json.loads((BUNDLE / 'bundle.json').read_text(encoding='utf-8'))
    return manifest


def verify_skill(args, name, skill_id, manifest):
    info = object_response(cli(args, ['skill', 'get', skill_id, '--with-content']), 'skill')
    if id_value(info) != skill_id or info.get('name') != name or not isinstance(info.get('content'), str) or not isinstance(info.get('files'), list):
        raise InstallError(f'Cannot verify skill {name}: content or file list absent')
    with zipfile.ZipFile(BUNDLE / manifest['skills'][name]['archive']) as archive:
        contents = {p: archive.read(p).decode('utf-8') for p in archive.namelist()}
    files = {}
    for item in info['files']:
        if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not isinstance(item.get('content'), str):
            raise InstallError(f'Cannot verify skill {name}: unexpected file format')
        if item['path'] in files:
            raise InstallError(f'Cannot verify skill {name}: duplicate file paths')
        files[item['path']] = item['content']
    if info['content'] != contents.pop('SKILL.md') or files != contents:
        raise InstallError(f'Skill {name} contents differ from the local archive')


def ids_from_bindings(items):
    ids = set()
    for item in items:
        # Different CLI versions can return a skill itself or a binding.
        value = item.get('skill_id', item.get('id'))
        if not isinstance(value, (str, int)) or not str(value):
            raise InstallError('Cannot identify an attached skill in read-back')
        ids.add(str(value))
    return ids


def verify_agent(args, stem, agent_id, skill_ids, allow_additional=False, check_description=False):
    label, skills, description = SPECS[stem]
    prompt = prompt_for(args, stem)
    details = object_response(cli(args, ['agent', 'get', agent_id]), 'agent')
    if (id_value(details) != agent_id or details.get('name') != label or details.get('instructions') != prompt
            or str(details.get('runtime_id', '')) != runtime_for(args, stem)):
        raise InstallError(f'Cannot verify name, instructions and runtime for {label}; refresh incompatible agents explicitly before reuse')
    if check_description and details.get('description') != description:
        raise InstallError(f'Cannot verify description for {label}')
    if details.get('archived') or details.get('is_archived') or details.get('archived_at'):
        raise InstallError(f'Cannot reuse archived agent {label}')
    if any(skill not in skill_ids for skill in skills):
        raise InstallError(f'Cannot reuse {label}: a required skill is missing from the workspace')
    actual = ids_from_bindings(collection(cli(args, ['agent', 'skills', 'list', agent_id]), 'skills'))
    required = {skill_ids[skill] for skill in skills}
    if not (required <= actual if allow_additional else required == actual):
        raise InstallError(f'Unexpected skill bindings for {label}')
    return actual


def prompt_for(args, role):
    base = (BUNDLE / 'agents' / (role + '.md')).read_text(encoding='utf-8')
    context = getattr(args, 'runtime_context', {}).get(runtime_for(args, role), '')
    return base + ('\n' + context + '\n' if context else '')


def runtime_for(args, role):
    return getattr(args, 'runtime_map', {}).get(role, args.runtime_id)


def main(args):
    profile = prepare.SQUADS[args.squad_profile]
    if args.squad_name is None:
        args.squad_name = profile['name']
    if not args.workspace_id.strip() or not args.runtime_id.strip() or not args.squad_name.strip():
        raise InstallError('Workspace ID, runtime ID, and squad name must be nonempty')
    if args.reuse_existing and args.overwrite_skills:
        raise InstallError('--reuse-existing and --overwrite-skills cannot be combined; inspect and update existing skills separately')
    if args.update_existing and args.reuse_existing:
        raise InstallError('--update-existing and --reuse-existing cannot be combined')
    try:
        version = subprocess.run(['multica', 'version'], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise InstallError('Cannot run multica version') from error
    match = re.search(r'\bmultica\s+(\d+)\.(\d+)\.(\d+)', version.stdout)
    if version.returncode or not match or tuple(map(int, match.groups())) < (0, 7, 1):
        raise InstallError('Multica CLI 0.7.1 or newer is required')
    manifest = prepare_bundle()
    runtimes = collection(cli(args, ['runtime', 'list']), 'runtimes')
    requested = {runtime_for(args, role) for role in SPECS}
    if not requested <= {id_value(item) for item in runtimes}:
        raise InstallError('Runtime ID not found in the selected workspace')
    existing_agents = matching_objects(
        collection(cli(args, ['agent', 'list', '--include-archived']), 'agents'),
        [label for label, _, _ in SPECS.values()], 'Agent',
    )
    existing_squads = matching_objects(collection(cli(args, ['squad', 'list']), 'squads'), [args.squad_name], 'Squad')
    skill_items = collection(cli(args, ['skill', 'list']), 'skills')
    existing_skills = matching_objects(skill_items, SKILLS, 'Skill')
    collisions = [f'agent: {label}' for label, _, _ in SPECS.values()
                  if label.casefold() in existing_agents and not args.reuse_existing and not args.update_existing]
    if args.squad_name.casefold() in existing_squads and not args.update_existing:
        collisions.append('squad: ' + args.squad_name)
    collisions += [f'skill: {name}' for name in SKILLS if name.casefold() in existing_skills
                   and not args.overwrite_skills and not args.reuse_existing and not args.update_existing]
    if collisions:
        raise InstallError('Existing names found; no workspace changes made: ' + ', '.join(collisions))
    overwrite_targets = {}
    reuse_skills = {}
    for name in SKILLS:
        item = existing_skills.get(name.casefold())
        if item is not None:
            if item['name'] != name:
                raise InstallError(f'Existing skill name differs in case: {item["name"]}; cannot safely use {name}')
            if args.reuse_existing:
                reuse_skills[name] = id_value(item)
                verify_skill(args, name, reuse_skills[name], manifest)
            else:
                overwrite_targets[name] = id_value(item)
    # Reuse byte-identical skill archives during an explicit refresh.
    if args.update_existing:
        for name, skill_id in list(overwrite_targets.items()):
            try:
                verify_skill(args, name, skill_id, manifest)
            except InstallError as error:
                if str(error) != f'Skill {name} contents differ from the local archive':
                    raise
            else:
                reuse_skills[name] = skill_id
                del overwrite_targets[name]
    reuse_agents = {}
    unchanged_agents = set()
    original_bindings = {}
    if args.reuse_existing or args.update_existing:
        for stem, (label, _, _) in SPECS.items():
            item = existing_agents.get(label.casefold())
            if item is None:
                continue
            if item['name'] != label:
                raise InstallError(f'Existing agent name differs in case: {item["name"]}; cannot safely reuse {label}')
            reuse_agents[stem] = id_value(item)
            if args.reuse_existing:
                original_bindings[stem] = verify_agent(args, stem, reuse_agents[stem], reuse_skills, allow_additional=True)
            else:
                detail = object_response(cli(args, ['agent', 'get', reuse_agents[stem]]), 'agent')
                if id_value(detail) != reuse_agents[stem] or detail.get('name') != label:
                    raise InstallError(f'Cannot confirm identity of existing agent {label}')
                if detail.get('archived') or detail.get('is_archived') or detail.get('archived_at'):
                    raise InstallError(f'Cannot update archived agent {label}')
                original_bindings[stem] = ids_from_bindings(collection(cli(args, ['agent', 'skills', 'list', reuse_agents[stem]]), 'skills'))
                prompt = prompt_for(args, stem)
                required = {reuse_skills[name] for name in SPECS[stem][1] if name in reuse_skills}
                if (detail.get('instructions') == prompt and detail.get('description') == SPECS[stem][2]
                        and str(detail.get('runtime_id', '')) == runtime_for(args, stem)
                        and all(name in reuse_skills for name in SPECS[stem][1])
                        and original_bindings[stem] == required):
                    unchanged_agents.add(stem)
        if len(set(reuse_agents.values())) != len(reuse_agents):
            raise InstallError('Different agent names resolved to the same ID; cannot safely reuse')
    squad_id = None
    current_members = []
    if args.update_existing and args.squad_name.casefold() in existing_squads:
        item = existing_squads[args.squad_name.casefold()]
        if item['name'] != args.squad_name:
            raise InstallError(f'Existing squad name differs in case: {item["name"]}; cannot safely update {args.squad_name}')
        squad_id = id_value(item)
        squad_detail = object_response(cli(args, ['squad', 'get', squad_id]), 'squad')
        if id_value(squad_detail) != squad_id or squad_detail.get('name') != args.squad_name:
            raise InstallError(f'Cannot confirm identity of existing squad {args.squad_name}')
        current_members = collection(cli(args, ['squad', 'member', 'list', squad_id]), 'members')
        agent_ids = []
        human_ids = []
        for member in current_members:
            if member.get('member_type') not in ('agent', 'member'):
                raise InstallError('Cannot safely update squad with unknown member type')
            member_id = member.get('member_id')
            if not isinstance(member_id, (str, int)) or not str(member_id):
                raise InstallError('Cannot safely identify squad member')
            if member['member_type'] == 'agent':
                agent_ids.append(str(member_id))
            else:
                if not isinstance(member.get('role'), str):
                    raise InstallError('Cannot safely verify existing human squad member role')
                human_ids.append(str(member_id))
        if len(set(agent_ids)) != len(agent_ids):
            raise InstallError('Cannot safely update squad with duplicate agent members')
        if len(set(human_ids)) != len(human_ids):
            raise InstallError('Cannot safely update squad with duplicate human members')
    print(f'Profile: {args.profile or "CLI default"}\nWorkspace: {args.workspace_id}\nRuntime: {args.runtime_id}\nSquad: {args.squad_name}\nSquad workflow: {args.squad_profile}')
    print('Verify the effective server and account separately with multica config show and multica auth status.')
    print('Agents: ' + ', '.join(x[0] for x in SPECS.values()))
    print('Skills: ' + ', '.join(SKILLS))
    print('Squad members: Lead, ' + ', '.join(
        SPECS[stem][0] + (' (optional dispatch)' if stem in profile.get('optional_members', ()) else '')
        for stem in profile['members']
    ))
    if args.reuse_existing and (reuse_agents or reuse_skills):
        print('Reuse verified agents: ' + (', '.join(SPECS[stem][0] for stem in reuse_agents) or 'none'))
        print('Reuse verified skills: ' + (', '.join(reuse_skills) or 'none'))
    if overwrite_targets:
        print('Existing skills to overwrite (shared bindings may be affected): ' +
              ', '.join(f'{name} ({skill_id})' for name, skill_id in overwrite_targets.items()))
    if args.update_existing:
        print('Update existing objects in place; shared agents and skills may affect other squads.')
        print('Agent name, description, instructions, runtime and skill bindings will be updated; other agent settings are preserved.')
        for stem, agent_id in reuse_agents.items():
            print(f'  Update agent {SPECS[stem][0]} ({agent_id}); current skill IDs: {", ".join(sorted(original_bindings[stem])) or "none"}; desired skills: {", ".join(SPECS[stem][1])}')
        if squad_id:
            desired_ids = {reuse_agents[stem] for stem in ('lead', *profile['members']) if stem in reuse_agents}
            removed = [str(m['member_id']) for m in current_members if m['member_type'] == 'agent' and str(m['member_id']) not in desired_ids]
            print(f'  Update squad {args.squad_name} ({squad_id}): leader, instructions and agent roster/roles; human members and other squad settings are preserved.')
            print('  Current squad agents: ' + (', '.join(f'{m["member_id"]} ({m.get("role", "unknown role")})' for m in current_members if m['member_type'] == 'agent') or 'none'))
            print('  Squad agent IDs to remove: ' + (', '.join(removed) or 'none'))
    for label, skills, _ in SPECS.values():
        print(f'  {label}: {", ".join(skills)}')
    if not args.apply:
        print('Preview only: no Multica workspace changes. Add --apply to install.')
        return
    print('Installing; completed objects are listed below for recovery if interrupted.', flush=True)
    skill_ids = dict(reuse_skills)
    for name in SKILLS:
        if name in reuse_skills:
            continue
        strategy = 'overwrite' if name in overwrite_targets else 'fail'
        obj = object_response(cli(args, ['skill', 'import', '--file', str(BUNDLE / 'skills' / (name + '.zip')), '--on-conflict', strategy]), 'skill')
        skill_ids[name] = id_value(obj)
        print(f'{"Overwrote" if name in overwrite_targets else "Created"} skill {name}: {skill_ids[name]}', flush=True)
        if name in overwrite_targets and skill_ids[name] != overwrite_targets[name]:
            raise InstallError(f'Overwritten skill {name} returned a different ID; inspect existing bindings')
        verify_skill(args, name, skill_ids[name], manifest)
    agents = dict(reuse_agents)
    for stem, (label, skills, description) in SPECS.items():
        prompt = prompt_for(args, stem)
        if stem in reuse_agents:
            if args.update_existing and stem not in unchanged_agents:
                agent_id = agents[stem]
                cli(args, ['agent', 'update', agent_id, '--name', label, '--runtime-id', runtime_for(args, stem), '--description', description, '--instructions', prompt])
                print(f'Updated agent {label}: {agent_id}', flush=True)
                cli(args, ['agent', 'skills', 'set', agent_id, '--skill-ids', ','.join(skill_ids[s] for s in skills)])
                verify_agent(args, stem, agent_id, skill_ids, check_description=True)
            continue
        obj = object_response(cli(args, ['agent', 'create', '--name', label, '--runtime-id', runtime_for(args, stem), '--description', description, '--instructions', prompt]), 'agent')
        agent_id = agents[stem] = id_value(obj)
        print(f'Created agent {label}: {agent_id}', flush=True)
        cli(args, ['agent', 'skills', 'add', agent_id, '--skill-ids', ','.join(skill_ids[s] for s in skills)])
        verify_agent(args, stem, agent_id, skill_ids)
    # Check reused objects again before attaching them; never edit their bindings.
    for name, skill_id in reuse_skills.items():
        verify_skill(args, name, skill_id, manifest)
    if args.reuse_existing:
        for stem, agent_id in reuse_agents.items():
            if verify_agent(args, stem, agent_id, skill_ids, allow_additional=True) != original_bindings[stem]:
                raise InstallError(f'Skill bindings changed during installation for {SPECS[stem][0]}')
    updating_squad = squad_id is not None
    if not updating_squad:
        squad = object_response(cli(args, ['squad', 'create', '--name', args.squad_name, '--leader', agents['lead']]), 'squad')
        squad_id = id_value(squad)
        print(f'Created squad {args.squad_name}: {squad_id}', flush=True)
    instructions = (BUNDLE / manifest['squads'][args.squad_profile]['instructions']).read_text(encoding='utf-8')
    update_command = ['squad', 'update', squad_id, '--instructions', instructions]
    if updating_squad:
        update_command += ['--name', args.squad_name, '--leader', agents['lead']]
    if not updating_squad or any(squad_detail.get(key) != value for key, value in (('instructions', instructions), ('name', args.squad_name), ('leader_id', agents['lead']))):
        cli(args, update_command)
    if updating_squad:
        # The leader may appear in the member list; preserve it if present.
        selected_ids = {agents[stem] for stem in ('lead', *profile['members'])}
        for member in current_members:
            member_id = str(member['member_id'])
            if member['member_type'] == 'agent' and member_id not in selected_ids:
                cli(args, ['squad', 'member', 'remove', squad_id, '--member-id', member_id, '--type', 'agent'])
    for stem in profile['members']:
        role = SPECS[stem][2]
        existing = next((m for m in current_members if m.get('member_type') == 'agent' and str(m.get('member_id', '')) == agents[stem]), None)
        if existing is None:
            cli(args, ['squad', 'member', 'add', squad_id, '--member-id', agents[stem], '--type', 'agent', '--role', role])
        elif existing.get('role') != role:
            cli(args, ['squad', 'member', 'set-role', squad_id, '--member-id', agents[stem], '--member-type', 'agent', '--role', role])
    detail = object_response(cli(args, ['squad', 'get', squad_id]), 'squad')
    if (id_value(detail) != squad_id or detail.get('name') != args.squad_name or detail.get('instructions') != instructions
            or str(detail.get('leader_id', '')) != agents['lead']):
        raise InstallError('Cannot verify squad identity, name, instructions and leader')
    members = collection(cli(args, ['squad', 'member', 'list', squad_id]), 'members')
    agent_members = [m for m in members if m.get('member_type') == 'agent']
    for stem in profile['members']:
        role = SPECS[stem][2]
        matches = [m for m in agent_members if str(m.get('member_id', '')) == agents[stem]]
        if len(matches) != 1 or matches[0].get('role') != role:
            raise InstallError(f'Squad member or role read-back failed for {stem}')
    selected_ids = {agents[stem] for stem in ('lead', *profile['members'])}
    if any(str(m.get('member_id', '')) not in selected_ids for m in agent_members):
        raise InstallError('Unexpected squad agent in read-back')
    if updating_squad:
        before_humans = {(str(m['member_id']), m['role']) for m in current_members if m['member_type'] == 'member'}
        after_humans = [(str(m.get('member_id', '')), m.get('role')) for m in members if m.get('member_type') == 'member']
        if any(not member_id or not isinstance(role, str) for member_id, role in after_humans):
            raise InstallError('Cannot verify human squad members or their roles')
        if len(after_humans) != len(before_humans) or set(after_humans) != before_humans:
            raise InstallError('Human squad members or their roles changed during installation')
    print('Installation read-back passed. Test an actual pilot task before relying on agent behavior.')


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-id', required=True, help='Explicit target workspace ID')
    parser.add_argument('--runtime-id', required=True, help='Runtime ID for all reusable agents')
    parser.add_argument('--profile', help='Configured Multica CLI profile')
    parser.add_argument('--squad-profile', choices=(*prepare.SQUADS, 'all'), default='research-engineering', help='Workflow policy and squad membership')
    parser.add_argument('--squad-name', '--name-prefix', dest='squad_name', help='Squad display name (default depends on profile; --name-prefix is a compatibility alias)')
    parser.add_argument('--apply', action='store_true', help='Create objects after read-only preflight (default is preview)')
    parser.add_argument('--overwrite-skills', action='store_true', help='Allow existing matching skills to be overwritten during --apply')
    parser.add_argument('--reuse-existing', action='store_true', help='Reuse exactly compatible existing agents and skills; preserve additional agent skill bindings')
    parser.add_argument('--update-existing', action='store_true', help='Update matching agents, skills and squad in place, replacing managed skill bindings and squad agent roster')
    return parser.parse_args()


def run(args):
    if args.squad_profile != 'all':
        return main(args)
    if args.squad_name:
        raise InstallError('--squad-name cannot be combined with all profiles')
    # Resolve all target conflicts before the first remote write.
    planned = []
    for profile in prepare.SQUADS:
        item = copy.copy(args)
        item.squad_profile = profile
        item.apply = False
        main(item)
        planned.append(item)
    if args.apply:
        for index, item in enumerate(planned):
            item.apply = True
            if index and not args.update_existing:
                item.reuse_existing = True
                item.overwrite_skills = False
            main(item)


if __name__ == '__main__':
    try:
        run(parse_args())
    except (InstallError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print(f'Installation stopped: {error}', file=sys.stderr)
        print('If --apply was used, inspect the target workspace by all planned names before retrying: an interrupted write may have succeeded without returning an ID. Overwritten skills and other changes are not automatically rolled back.', file=sys.stderr)
        raise SystemExit(1) from error
