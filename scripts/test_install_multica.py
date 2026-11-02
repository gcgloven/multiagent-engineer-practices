#!/usr/bin/env python3
"""Offline installer tests against a stateful fake Multica CLI, not a live server."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'install_multica.py'
FAKE = r'''#!/usr/bin/env python3
import json,os,pathlib,sys,zipfile
p=pathlib.Path(os.environ['FAKE_DB'])
d=json.loads(p.read_text()) if p.exists() else {'skills':[], 'agents':[], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}
a=sys.argv[1:]
if a == ['version']: print('multica 0.7.1'); sys.exit(0)
if a[:1] == ['--profile']: a=a[2:]
if a[:1] != ['--workspace-id'] or a[1] != 'workspace-1': sys.exit(8)
a=a[2:]
def val(flag): return a[a.index(flag)+1]
def created(kind, obj):
 number=max([int(x['id'].split('-')[-1]) for x in d[kind+'s'] if x['id'].startswith(kind+'-') and x['id'].split('-')[-1].isdigit()]+[0])+1
 obj['id']=kind+'-'+str(number); d[kind+'s'].append(obj); return obj
write = any(a[:2]==x for x in [['skill','import'],['agent','create'],['agent','update'],['squad','create'],['squad','update']]) or a[:3] in [['agent','skills','add'],['agent','skills','set'],['squad','member','add'],['squad','member','remove'],['squad','member','set-role']]
if write:
 d['writes']+=1
 if os.getenv('FAIL_AT') == str(d['writes']): p.write_text(json.dumps(d)); sys.exit(7)
if a[:2] == ['runtime','list']: out=d['runtimes']
elif a[:2] in [['skill','list'],['agent','list'],['squad','list']]: out=d[a[0]+'s']
elif a[:2] == ['skill','import']:
 with zipfile.ZipFile(val('--file')) as z:
  files={x:z.read(x).decode() for x in z.namelist()}
 name=pathlib.Path(val('--file')).stem
 existing=next((x for x in d['skills'] if x['name'].casefold()==name.casefold()), None)
 strategy=val('--on-conflict')
 if existing:
  if strategy != 'overwrite': sys.exit(9)
  existing.update({'name':name,'content':files.pop('SKILL.md'),'files':[{'path':k,'content':v} for k,v in files.items()]})
  out=existing
 else:
  if strategy != 'fail': sys.exit(9)
  out=created('skill', {'name':name,'content':files.pop('SKILL.md'),'files':[{'path':k,'content':v} for k,v in files.items()]})
elif a[:2] == ['skill','get']: out=next(x for x in d['skills'] if x['id']==a[2])
elif a[:2] == ['agent','create']: out=created('agent',{'name':val('--name'),'runtime_id':val('--runtime-id'),'description':val('--description'),'instructions':val('--instructions'),'skills':[]})
elif a[:2] == ['agent','get']: out=next(x for x in d['agents'] if x['id']==a[2])
elif a[:2] == ['agent','update']:
 out=next(x for x in d['agents'] if x['id']==a[2])
 for flag,key in [('--name','name'),('--runtime-id','runtime_id'),('--description','description'),('--instructions','instructions')]:
  if flag in a: out[key]=val(flag)
elif a[:3] == ['agent','skills','add']:
 out=next(x for x in d['agents'] if x['id']==a[3]); out['skills']=list(dict.fromkeys(out['skills']+val('--skill-ids').split(',')))
elif a[:3] == ['agent','skills','set']:
 out=next(x for x in d['agents'] if x['id']==a[3]); out['skills']=val('--skill-ids').split(',')
elif a[:3] == ['agent','skills','list']:
 out=[{'id':x} for x in next(x for x in d['agents'] if x['id']==a[3])['skills']]
elif a[:2] == ['squad','create']: out=created('squad',{'name':val('--name'),'leader_id':val('--leader'),'members':[]})
elif a[:2] == ['squad','update']:
 out=next(x for x in d['squads'] if x['id']==a[2])
 for flag,key in [('--name','name'),('--leader','leader_id'),('--instructions','instructions')]:
  if flag in a: out[key]=val(flag)
elif a[:3] == ['squad','member','add']:
 out=next(x for x in d['squads'] if x['id']==a[3]); out['members'].append({'member_id':val('--member-id'),'member_type':'agent','role':val('--role')})
elif a[:3] == ['squad','member','remove']:
 out=next(x for x in d['squads'] if x['id']==a[3]); out['members']=[m for m in out['members'] if not (m['member_id']==val('--member-id') and m['member_type']==val('--type'))]
elif a[:3] == ['squad','member','set-role']:
 out=next(x for x in d['squads'] if x['id']==a[3]); next(m for m in out['members'] if m['member_id']==val('--member-id') and m['member_type']==val('--member-type'))['role']=val('--role')
elif a[:3] == ['squad','member','list']: out=next(x for x in d['squads'] if x['id']==a[3])['members']
elif a[:2] == ['squad','get']: out=next(x for x in d['squads'] if x['id']==a[2])
else: sys.exit(6)
if os.getenv('MALFORMED_LIST') and a[:2] == ['skill','list']: out={'next_cursor':'next','skills':out}
if os.getenv('TAMPER_SKILL') and a[:2] == ['skill','get']: out={**out,'content':'wrong'}
if os.getenv('TAMPER_AGENT') and a[:2] == ['agent','get'] and d['writes'] > int(os.getenv('TAMPER_AFTER', '0')): out={**out,'description':'wrong'}
if os.getenv('TAMPER_SQUAD') and a[:2] == ['squad','get'] and d['writes'] > int(os.getenv('TAMPER_AFTER', '0')): out={**out,'leader_id':'wrong'}
if os.getenv('TAMPER_HUMAN') and a[:3] == ['squad','member','list'] and d['writes'] > int(os.getenv('TAMPER_AFTER', '0')):
 if os.getenv('TAMPER_HUMAN') == 'remove': out=[m for m in out if m['member_type'] != 'member']
 else: out=[{**m,'role':'changed'} if m['member_type'] == 'member' else m for m in out]
p.write_text(json.dumps(d))
print(json.dumps(out))
'''


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        fake = self.folder / 'multica'
        fake.write_text(FAKE, encoding='utf-8')
        fake.chmod(0o755)
        self.db = self.folder / 'db.json'
        self.env = {**os.environ, 'PATH': str(self.folder) + os.pathsep + os.environ['PATH'], 'FAKE_DB': str(self.db)}

    def run_installer(self, *args, **env):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), '--workspace-id', 'workspace-1', '--runtime-id', 'runtime-1', *args], cwd=ROOT, env={**self.env, **env}, text=True, capture_output=True)

    def state(self):
        return json.loads(self.db.read_text())

    def test_preview_is_read_only(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Preview only', result.stdout)
        self.assertIn('Agents: Lead, Scout, Paper Reviewer, Analyst, Systems Engineer, Software Engineer, Test & Code Review Engineer, Verifier, Product Manager', result.stdout)
        self.assertIn('Product Manager (optional dispatch)', result.stdout)
        self.assertEqual(self.state()['writes'], 0)

    def test_install_and_readback(self):
        result = self.run_installer('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('read-back passed', result.stdout)
        db = self.state()
        self.assertEqual((len(db['skills']), len(db['agents']), len(db['squads'])), (12, 9, 1))
        self.assertEqual([agent['name'] for agent in db['agents']], ['Lead', 'Scout', 'Paper Reviewer', 'Analyst', 'Systems Engineer', 'Software Engineer', 'Test & Code Review Engineer', 'Verifier', 'Product Manager'])
        self.assertEqual(len(db['squads'][0]['members']), 8)
        self.assertEqual(len(db['agents'][0]['skills']), 1)
        self.assertTrue(all(s['content'] for s in db['skills']))

    def test_second_squad_reuses_pool_and_preserves_additional_bindings(self):
        first = self.run_installer('--apply')
        self.assertEqual(first.returncode, 0, first.stderr)
        initial = self.state()
        engineer = next(a for a in initial['agents'] if a['name'] == 'Software Engineer')
        engineer['skills'].append('custom-method')
        self.db.write_text(json.dumps(initial))
        preview = self.run_installer('--squad-profile', 'software-delivery', '--reuse-existing')
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(self.state(), initial)
        result = self.run_installer('--squad-profile', 'software-delivery', '--reuse-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        final = self.state()
        self.assertEqual(final['agents'], initial['agents'])
        self.assertEqual(final['skills'], initial['skills'])
        self.assertEqual(len(final['squads']), 2)
        squad = final['squads'][1]
        self.assertEqual(squad['name'], 'Software Delivery Squad')
        ids = {a['name']: a['id'] for a in final['agents']}
        self.assertEqual(squad['leader_id'], ids['Lead'])
        self.assertEqual({m['member_id'] for m in squad['members']}, {ids['Software Engineer'], ids['Test & Code Review Engineer'], ids['Systems Engineer'], ids['Verifier'], ids['Product Manager']})
        self.assertEqual(squad['instructions'], (ROOT / 'build/multica/squads/software-delivery.md').read_text())

    def test_selected_squad_profiles_use_correct_members(self):
        expected = {
            'open-research': {'Scout', 'Paper Reviewer', 'Analyst', 'Verifier'},
            'analytics-engineering': {'Analyst', 'Software Engineer', 'Test & Code Review Engineer', 'Verifier', 'Systems Engineer'},
            'engineering-design': {'Product Manager', 'Systems Engineer', 'Verifier', 'Software Engineer', 'Test & Code Review Engineer'},
        }
        first = self.run_installer('--apply')
        self.assertEqual(first.returncode, 0, first.stderr)
        for profile, names in expected.items():
            with self.subTest(profile=profile):
                result = self.run_installer('--squad-profile', profile, '--reuse-existing', '--apply')
                self.assertEqual(result.returncode, 0, result.stderr)
                db = self.state()
                ids = {a['name']: a['id'] for a in db['agents']}
                squad = db['squads'][-1]
                self.assertEqual({m['member_id'] for m in squad['members']}, {ids[n] for n in names})
                self.assertEqual(squad['instructions'], (ROOT / f'build/multica/squads/{profile}.md').read_text())
                self.assertEqual((len(db['agents']), len(db['skills'])), (9, 12))
                if profile == 'engineering-design':
                    self.assertEqual(squad['name'], 'Engineering Design Squad')
                    self.assertIn('Product Manager (optional dispatch)', result.stdout)

    def test_incompatible_reused_objects_stop_before_writes(self):
        first = self.run_installer('--apply')
        self.assertEqual(first.returncode, 0, first.stderr)
        baseline = self.state()
        for defect in ('prompt', 'runtime', 'skill-content', 'binding', 'ambiguous-agent', 'ambiguous-skill'):
            with self.subTest(defect=defect):
                db = json.loads(json.dumps(baseline))
                if defect == 'prompt':
                    db['agents'][0]['instructions'] = 'previous shared vocabulary and loop'
                elif defect == 'runtime':
                    db['agents'][0]['runtime_id'] = 'other-runtime'
                elif defect == 'skill-content':
                    db['skills'][0]['content'] = 'customized skill'
                elif defect == 'binding':
                    db['agents'][0]['skills'] = []
                elif defect == 'ambiguous-agent':
                    db['agents'].append({**db['agents'][0], 'id': 'duplicate-agent'})
                else:
                    db['skills'].append({**db['skills'][0], 'id': 'duplicate-skill'})
                self.db.write_text(json.dumps(db))
                result = self.run_installer('--squad-profile', 'software-delivery', '--reuse-existing', '--apply')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.state(), db)

    def test_reuse_still_rejects_existing_target_squad(self):
        first = self.run_installer('--apply')
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.state()
        result = self.run_installer('--reuse-existing', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('squad: Engineering Practice Squad', result.stderr)
        self.assertEqual(self.state(), before)

    def test_reuse_and_overwrite_cannot_be_combined(self):
        result = self.run_installer('--reuse-existing', '--overwrite-skills', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('cannot be combined', result.stderr)
        self.assertFalse(self.db.exists())

    def stale_installation(self):
        result = self.run_installer('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        db = self.state()
        for agent in db['agents']:
            agent.update(instructions='old prompt', description='old description', runtime_id='old-runtime', skills=['custom-skill'])
        for skill in db['skills']:
            skill['content'] = 'old skill'
        squad = db['squads'][0]
        squad['instructions'] = 'old squad policy'
        squad['leader_id'] = 'old-leader'
        squad['members'] = [
            {'member_id': db['agents'][1]['id'], 'member_type': 'agent', 'role': 'old role'},
            {'member_id': 'extra-agent', 'member_type': 'agent', 'role': 'old role'},
            {'member_id': 'human-1', 'member_type': 'member', 'role': 'observer'},
        ]
        self.db.write_text(json.dumps(db))
        return db

    def test_update_existing_preview_and_apply_reconcile_in_place(self):
        before = self.stale_installation()
        preview = self.run_installer('--update-existing')
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn('preview', preview.stdout.lower())
        self.assertEqual(self.state(), before)

        result = self.run_installer('--update-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('read-back passed', result.stdout)
        after = self.state()
        for kind in ('skills', 'agents', 'squads'):
            self.assertEqual([x['id'] for x in after[kind]], [x['id'] for x in before[kind]])
        skills = {s['name']: s['id'] for s in after['skills']}
        from catalog import SPECS
        desired = {label: set(methods) for label, methods, _ in SPECS.values()}
        for agent in after['agents']:
            self.assertEqual(agent['runtime_id'], 'runtime-1')
            self.assertNotEqual(agent['instructions'], 'old prompt')
            self.assertNotEqual(agent['description'], 'old description')
            self.assertEqual(set(agent['skills']), {skills[name] for name in desired[agent['name']]})
        self.assertTrue(all(skill['content'] != 'old skill' for skill in after['skills']))
        ids = {a['name']: a['id'] for a in after['agents']}
        squad = after['squads'][0]
        self.assertEqual(squad['leader_id'], ids['Lead'])
        self.assertEqual(squad['instructions'], (ROOT / 'build/multica/squads/research-engineering.md').read_text())
        members = squad['members']
        self.assertEqual({m['member_id'] for m in members if m['member_type'] == 'agent'},
                         {ids[name] for name in ('Scout', 'Paper Reviewer', 'Analyst', 'Systems Engineer', 'Software Engineer', 'Test & Code Review Engineer', 'Verifier', 'Product Manager')})
        self.assertNotEqual(next(m['role'] for m in members if m['member_id'] == ids['Scout']), 'old role')
        self.assertIn({'member_id': 'human-1', 'member_type': 'member', 'role': 'observer'}, members)

    def test_update_handles_partial_install_and_can_run_again(self):
        before = self.stale_installation()
        before['skills'] = [before['skills'][0]]
        before['agents'] = [before['agents'][0]]
        before['squads'] = []
        self.db.write_text(json.dumps(before))
        result = self.run_installer('--update-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        first = self.state()
        self.assertEqual((len(first['skills']), len(first['agents']), len(first['squads'])), (12, 9, 1))
        self.assertEqual(first['skills'][0]['id'], before['skills'][0]['id'])
        self.assertEqual(first['agents'][0]['id'], before['agents'][0]['id'])
        result = self.run_installer('--update-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        second = self.state()
        for kind in ('skills', 'agents', 'squads'):
            self.assertEqual(first[kind], second[kind])

    def test_update_expands_partial_pool_without_replacing_existing_ids(self):
        result = self.run_installer('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        current = self.state()
        legacy = json.loads(json.dumps(current))
        pm_id = next(a['id'] for a in legacy['agents'] if a['name'] == 'Product Manager')
        new_skill_ids = {s['id'] for s in legacy['skills'] if s['name'] in ('explain-work', 'design-solution')}
        legacy['agents'] = [a for a in legacy['agents'] if a['id'] != pm_id]
        legacy['skills'] = [s for s in legacy['skills'] if s['id'] not in new_skill_ids]
        for agent in legacy['agents']:
            agent['skills'] = [skill_id for skill_id in agent['skills'] if skill_id not in new_skill_ids]
        legacy['squads'][0]['members'] = [m for m in legacy['squads'][0]['members'] if m['member_id'] != pm_id]
        self.assertEqual((len(legacy['agents']), len(legacy['skills'])), (8, 10))

        # Reuse cannot silently change an older prompt or add its new bindings.
        for defect in ('old-prompt', 'missing-new-bindings'):
            with self.subTest(defect=defect):
                before = json.loads(json.dumps(legacy))
                if defect == 'old-prompt':
                    next(a for a in before['agents'] if a['name'] == 'Software Engineer')['instructions'] = 'old engineer prompt'
                self.db.write_text(json.dumps(before))
                result = self.run_installer('--squad-profile', 'engineering-design', '--reuse-existing', '--apply')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.state(), before)

        self.db.write_text(json.dumps(legacy))
        preview = self.run_installer('--update-existing')
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(self.state(), legacy)
        result = self.run_installer('--update-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        after = self.state()
        self.assertEqual((len(after['agents']), len(after['skills']), len(after['squads'])), (9, 12, 1))
        for kind in ('agents', 'skills', 'squads'):
            old_ids = {item['name']: item['id'] for item in legacy[kind]}
            new_ids = {item['name']: item['id'] for item in after[kind]}
            self.assertTrue(all(new_ids[name] == object_id for name, object_id in old_ids.items()))
        skills = {s['name']: s['id'] for s in after['skills']}
        agents = {a['name']: a for a in after['agents']}
        self.assertEqual(set(agents['Product Manager']['skills']), {skills['frame-problem'], skills['explain-work']})
        for role in ('Systems Engineer', 'Verifier'):
            self.assertIn(skills['design-solution'], agents[role]['skills'])
        self.assertIn(agents['Product Manager']['id'], {m['member_id'] for m in after['squads'][0]['members']})

    def test_update_preserves_existing_lead_membership(self):
        before = self.stale_installation()
        lead_id = before['agents'][0]['id']
        lead_member = {'member_id': lead_id, 'member_type': 'agent', 'role': 'existing lead role'}
        before['squads'][0]['members'].append(lead_member)
        self.db.write_text(json.dumps(before))
        result = self.run_installer('--update-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        members = self.state()['squads'][0]['members']
        self.assertEqual([m for m in members if m['member_id'] == lead_id], [lead_member])

    def test_update_detects_human_member_changes_during_readback(self):
        before = self.stale_installation()
        for change in ('remove', 'role'):
            with self.subTest(change=change):
                self.db.write_text(json.dumps(before))
                result = self.run_installer('--update-existing', '--apply',
                                            TAMPER_AFTER=str(before['writes']), TAMPER_HUMAN=change)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('read-back passed', result.stdout)

    def test_update_preflight_rejects_ambiguous_or_archived_targets(self):
        before = self.stale_installation()
        for defect in ('agent', 'skill', 'squad', 'archived-agent'):
            with self.subTest(defect=defect):
                db = json.loads(json.dumps(before))
                if defect == 'archived-agent':
                    db['agents'][0]['archived'] = True
                else:
                    collection = db[defect + 's']
                    collection.append({**collection[0], 'id': 'duplicate'})
                self.db.write_text(json.dumps(db))
                result = self.run_installer('--update-existing', '--apply')
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.state(), db)

    def test_update_fails_on_bad_agent_or_squad_readback(self):
        before = self.stale_installation()
        for tamper in ('TAMPER_AGENT', 'TAMPER_SQUAD'):
            with self.subTest(tamper=tamper):
                self.db.write_text(json.dumps(before))
                result = self.run_installer('--update-existing', '--apply',
                                            TAMPER_AFTER=str(before['writes']), **{tamper: '1'})
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('read-back passed', result.stdout)

    def test_update_failed_write_stops_without_retry(self):
        before = self.stale_installation()
        result = self.run_installer('--update-existing', '--apply', FAIL_AT=str(before['writes'] + 2))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()['writes'], before['writes'] + 2)
        self.assertNotIn('read-back passed', result.stdout)

    def test_existing_names_abort_before_writes(self):
        self.db.write_text(json.dumps({'skills':[{'id':'existing','name':'review-paper'}], 'agents':[], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('skill: review-paper', result.stderr)
        self.assertEqual(self.state()['writes'], 0)

    def test_overwrite_preview_is_read_only(self):
        existing = {'id': 'existing', 'name': 'review-paper', 'content': 'old', 'files': []}
        self.db.write_text(json.dumps({'skills':[existing], 'agents':[], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--overwrite-skills')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('overwrite', result.stdout.lower())
        self.assertIn('review-paper', result.stdout)
        self.assertEqual(self.state()['skills'], [existing])
        self.assertEqual(self.state()['writes'], 0)

    def test_overwrite_existing_skill_and_create_missing_skills(self):
        existing = {'id': 'existing', 'name': 'review-paper', 'content': 'old', 'files': [{'path': 'obsolete.txt', 'content': 'old'}]}
        self.db.write_text(json.dumps({'skills':[existing], 'agents':[], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--overwrite-skills', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('read-back passed', result.stdout)
        db = self.state()
        self.assertEqual((len(db['skills']), len(db['agents']), len(db['squads'])), (12, 9, 1))
        skill = next(x for x in db['skills'] if x['name'] == 'review-paper')
        self.assertEqual(skill['id'], 'existing')
        self.assertNotEqual(skill['content'], 'old')
        self.assertNotIn('obsolete.txt', [f['path'] for f in skill['files']])
        reviewer = next(x for x in db['agents'] if x['name'] == 'Paper Reviewer')
        self.assertIn('existing', reviewer['skills'])

    def test_ambiguous_skill_names_abort_before_overwrite(self):
        self.db.write_text(json.dumps({'skills':[{'id':'one','name':'review-paper'}, {'id':'two','name':'REVIEW-PAPER'}], 'agents':[], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--overwrite-skills', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()['writes'], 0)

    def test_agent_collision_aborts_before_skill_overwrite(self):
        self.db.write_text(json.dumps({'skills':[{'id':'existing','name':'review-paper','content':'old','files':[]}], 'agents':[{'id':'agent','name':'Software Engineer'}], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--overwrite-skills', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('agent: Software Engineer', result.stderr)
        self.assertEqual(self.state()['writes'], 0)
        self.assertEqual(self.state()['skills'][0]['content'], 'old')

    def test_failed_overwrite_readback_stops_before_creating_agents(self):
        self.db.write_text(json.dumps({'skills':[{'id':'existing','name':'frame-problem','content':'old','files':[]}], 'agents':[], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--overwrite-skills', '--apply', TAMPER_SKILL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('contents differ', result.stderr)
        self.assertEqual(len(self.state()['skills']), 1)
        self.assertEqual(len(self.state()['agents']), 0)

    def test_partial_failure_never_retries_or_overwrites(self):
        result = self.run_installer('--apply', FAIL_AT='3')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(self.state()['skills']), 2)
        again = self.run_installer('--apply')
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual(len(self.state()['skills']), 2)
        self.assertEqual(self.state()['writes'], 3)

    def test_agent_name_collision_aborts_even_with_custom_squad_name(self):
        self.db.write_text(json.dumps({'skills':[], 'agents':[{'id':'existing','name':'Software Engineer'}], 'squads':[], 'runtimes':[{'id':'runtime-1','name':'Local'}], 'writes':0}))
        result = self.run_installer('--apply', '--squad-name', 'Another Squad')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('agent: Software Engineer', result.stderr)
        self.assertEqual(self.state()['writes'], 0)

    def test_all_profiles_share_pool_and_repeat_update_has_no_writes(self):
        first = self.run_installer('--squad-profile', 'all', '--apply')
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.state()
        self.assertEqual((len(before['agents']), len(before['skills']), len(before['squads'])), (9, 12, 5))
        again = self.run_installer('--squad-profile', 'all', '--update-existing', '--apply')
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.state(), before)

    def test_legacy_engineer_identity_is_not_repurposed(self):
        legacy = {'id': 'legacy-engineer', 'name': 'Engineer', 'instructions': 'old', 'skills': [], 'runtime_id': 'runtime-1'}
        self.db.write_text(json.dumps({'skills': [], 'agents': [legacy], 'squads': [],
                                      'runtimes': [{'id': 'runtime-1'}], 'writes': 0}))
        result = self.run_installer('--update-existing', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(next(a for a in self.state()['agents'] if a['id'] == 'legacy-engineer'), legacy)
        self.assertEqual(len(self.state()['agents']), 10)

    def test_runtime_must_exist(self):
        self.db.write_text(json.dumps({'skills':[], 'agents':[], 'squads':[], 'runtimes':[], 'writes':0}))
        result = self.run_installer('--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()['writes'], 0)

    def test_paginated_preflight_fails_closed(self):
        result = self.run_installer('--apply', MALFORMED_LIST='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('paginated', result.stderr)
        self.assertEqual(self.state()['writes'], 0)

    def test_incorrect_import_content_stops_install(self):
        result = self.run_installer('--apply', TAMPER_SKILL='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('contents differ', result.stderr)
        self.assertEqual(len(self.state()['skills']), 1)
        self.assertEqual(len(self.state()['agents']), 0)


if __name__ == '__main__':
    unittest.main()
