"""Stateful offline ticket tests; no live workspace or agent runs."""
import contextlib
import copy
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import pilot_issues as pilot
from catalog import SQUADS
from pilot_cases import CASES


class FakeClient:
    workspace = 'workspace-test'

    def __init__(self):
        self.issues = []
        self.calls = []
        self.runs = []
        self.fail_assign = False
        self.lost_create_response = False
        self.squads = [dict(id='squad-' + str(i), name=v['name']) for i, v in enumerate(SQUADS.values())]

    def call(self, *args):
        self.calls.append(args)
        if args[:2] == ('project', 'get'):
            return {'id': args[2], 'workspace_id': self.workspace}
        if args[:2] == ('squad', 'list'):
            return copy.deepcopy(self.squads)
        if args[:2] == ('issue', 'search'):
            return copy.deepcopy(self.issues)
        if args[:2] == ('issue', 'create'):
            value = lambda key: args[args.index(key) + 1]
            issue = dict(id='issue-' + str(len(self.issues) + 1), title=value('--title'),
                         # The live CLI/server removes the final file newline.
                         description=(pilot.ROOT / value('--description-file')).read_text().rstrip('\n'),
                         project_id=value('--project'), workspace_id=self.workspace,
                         status=value('--status'), assignee_id=None, assignee_type=None)
            self.issues.append(issue)
            if self.lost_create_response:
                self.lost_create_response = False
                raise pilot.PilotError('Simulated lost response after successful creation')
            return copy.deepcopy(issue)
        if args[:2] == ('issue', 'get'):
            return copy.deepcopy(next(i for i in self.issues if i['id'] == args[2]))
        if args[:2] == ('issue', 'assign'):
            if self.fail_assign:
                raise pilot.PilotError('Simulated assignment failure')
            assert args[-1] == '--no-start'
            issue = next(i for i in self.issues if i['id'] == args[2])
            issue['assignee_id'] = args[4]
            issue['assignee_type'] = 'squad'
            return copy.deepcopy(issue)
        if args[:2] == ('issue', 'runs'):
            return self.runs
        if args[:2] == ('issue', 'status'):
            issue = next(i for i in self.issues if i['id'] == args[2])
            issue['status'] = args[3]
            return copy.deepcopy(issue)
        raise AssertionError(args)


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.addCleanup(patch.stopall)
        patch.object(pilot, 'ROOT', self.root).start()
        self.client = FakeClient()

    def seed(self, apply=False, cases=CASES):
        with contextlib.redirect_stdout(io.StringIO()):
            return pilot.seed(self.client, 'fresh-v5', 'project-test', Path('/runtime/pilots'), cases, apply)

    def test_preview_makes_no_remote_writes(self):
        self.seed()
        self.assertFalse(self.client.issues)
        self.assertFalse(any(c[:2] in [('issue', 'create'), ('issue', 'assign')] for c in self.client.calls))

    def test_seed_nine_cases_all_backlog_no_start(self):
        self.seed(True)
        self.assertEqual(len(self.client.issues), 9)
        self.assertTrue(all(i['status'] == 'backlog' and i['assignee_id'] for i in self.client.issues))
        creates = [c for c in self.client.calls if c[:2] == ('issue', 'create')]
        self.assertTrue(all('--assignee-id' not in c and '--allow-duplicate' not in c for c in creates))
        self.assertFalse(any(c[:2] == ('issue', 'status') for c in self.client.calls))
        for case, issue in zip(CASES, self.client.issues):
            self.assertNotIn(case['expected'], issue['description'])

    def test_repeat_preserves_closed_and_active_issues(self):
        self.seed(True)
        self.client.issues[0]['status'] = 'done'
        self.client.issues[1]['status'] = 'in_progress'
        before = copy.deepcopy(self.client.issues)
        self.client.calls.clear()
        self.seed(True)
        self.assertEqual(self.client.issues, before)
        self.assertFalse(any(c[:2] in [('issue', 'assign'), ('issue', 'create'), ('issue', 'status')] for c in self.client.calls))

    def test_trimmed_newlines_allow_seed_repeat_and_launch_but_text_changes_do_not(self):
        self.seed(True)
        before = copy.deepcopy(self.client.issues)
        self.assertFalse(any(i['description'].endswith('\n') for i in before))
        self.seed(True)
        self.assertEqual(self.client.issues, before)
        pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path('/runtime/pilots'))
        self.assertTrue(pilot.descriptions_match('first\r\nsecond', 'first\nsecond\n'))
        self.assertFalse(pilot.descriptions_match('first second', 'first\nsecond\n'))
        self.assertFalse(pilot.descriptions_match('first changed\nsecond', 'first\nsecond\n'))

    def test_wrong_assignment_type_blocks_seed_and_launch_before_writes(self):
        self.seed(True)
        self.client.issues[3]['assignee_type'] = 'agent'
        self.client.calls.clear()
        with self.assertRaisesRegex(pilot.PilotError, 'not assigned to a squad'):
            self.seed(True)
        with self.assertRaisesRegex(pilot.PilotError, 'ownership'):
            pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path('/runtime/pilots'))
        self.assertFalse(any(c[:2] in [('issue', 'assign'), ('issue', 'create'), ('issue', 'status')] for c in self.client.calls))

    def test_lost_create_response_recovers_without_duplicate(self):
        self.client.lost_create_response = True
        with self.assertRaises(pilot.PilotError):
            self.seed(True)
        self.assertEqual(len(self.client.issues), 1)
        self.seed(True)
        self.assertEqual(len(self.client.issues), 9)

    def test_assignment_failure_can_resume(self):
        self.client.fail_assign = True
        with self.assertRaises(pilot.PilotError):
            self.seed(True)
        self.client.fail_assign = False
        self.seed(True)
        self.assertEqual(len(self.client.issues), 9)

    def test_all_squad_targets_validated_before_writes(self):
        self.client.squads.pop()
        with self.assertRaises(pilot.PilotError):
            self.seed(True)
        self.assertFalse(self.client.issues)

    def test_duplicate_identity_blocks_batch(self):
        self.seed(True)
        self.client.issues.append({**self.client.issues[0], 'id': 'duplicate'})
        with self.assertRaisesRegex(pilot.PilotError, 'Duplicate'):
            self.seed(True)

    def test_wrong_project_or_owner_or_description_blocks(self):
        self.seed(True)
        baseline = copy.deepcopy(self.client.issues)
        for key, value in [('project_id', 'other'), ('assignee_id', 'other'), ('description', self.client.issues[0]['description'] + ' changed')]:
            self.client.issues = copy.deepcopy(baseline)
            self.client.issues[0][key] = value
            with self.subTest(key=key), self.assertRaises(pilot.PilotError):
                self.seed(True)

    def test_launch_only_one_case_and_refuse_repeat(self):
        self.seed(True)
        pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', False, Path('/runtime/pilots'))
        self.assertTrue(all(i['status'] == 'backlog' for i in self.client.issues))
        pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path('/runtime/pilots'))
        self.assertEqual(sum(i['status'] == 'todo' for i in self.client.issues), 1)
        with self.assertRaises(pilot.PilotError):
            pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path('/runtime/pilots'))

    def test_launch_refuses_prior_run_history(self):
        self.seed(True)
        self.client.runs = [{'id': 'old-run'}]
        with self.assertRaises(pilot.PilotError):
            pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path('/runtime/pilots'))

    def test_launch_refuses_changed_owner_description_or_directory(self):
        self.seed(True)
        baseline = copy.deepcopy(self.client.issues)
        for key, value, directory in [('assignee_id', 'other', '/runtime/pilots'),
                                      ('description', baseline[3]['description'] + ' changed', '/runtime/pilots'),
                                      ('status', 'backlog', '/different/runtime')]:
            self.client.issues = copy.deepcopy(baseline)
            self.client.issues[3][key] = value
            self.client.calls.clear()
            with self.subTest(key=key), self.assertRaises(pilot.PilotError):
                pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path(directory))
            self.assertFalse(any(c[:2] == ('issue', 'status') for c in self.client.calls))

    def test_custom_squad_name_used_for_seed_and_launch(self):
        name = SQUADS['software-delivery']['name']
        next(s for s in self.client.squads if s['name'] == name)['name'] = 'Custom Delivery'
        names = {'software-delivery': 'Custom Delivery'}
        with contextlib.redirect_stdout(io.StringIO()):
            pilot.seed(self.client, 'fresh-v5', 'project-test', Path('/runtime/pilots'), [CASES[3]], True, names)
        pilot.launch(self.client, 'fresh-v5', 'project-test', 'P04', True, Path('/runtime/pilots'), names)
        self.assertEqual(self.client.issues[0]['status'], 'todo')

    def test_fixtures_never_reset_previous_work(self):
        destination = pilot.init_fixtures(self.root, 'fresh-v5')
        fixture = destination / 'P04/size_filter.py'
        fixture.write_text('user work')
        with self.assertRaises(pilot.PilotError):
            pilot.init_fixtures(self.root, 'fresh-v5')
        self.assertEqual(fixture.read_text(), 'user work')

    def test_boundary_fixtures_have_a_green_baseline_but_miss_the_contract(self):
        destination = pilot.init_fixtures(self.root, 'fixture-integrity')
        for case, test_file in [('P04', 'test_size_filter.py'), ('P09', 'weak_tests.py')]:
            directory = destination / case
            result = subprocess.run([sys.executable, '-B', test_file], cwd=directory,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            subject = runpy.run_path(str(directory / 'size_filter.py'))['within_limit']
            # The authored defect is deliberate: the pilot must expose this gap.
            self.assertNotEqual(subject([0, 512, 1024], 1024), [0, 512, 1024])
            self.assertEqual(subject([0, 512, 2048], 1024), [0, 512])

    def test_truncated_results_are_not_absence(self):
        with self.assertRaises(pilot.PilotError):
            pilot.collection({'issues': [], 'has_more': True}, 'issues')


if __name__ == '__main__':
    unittest.main()
