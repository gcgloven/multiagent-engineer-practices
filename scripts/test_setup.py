"""Unified setup checks with a fake CLI and mocked host provisioning."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import setup
from test_install_multica import FAKE


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        checkout = self.folder / 'checkout'
        shutil.copytree(setup.ROOT / 'skills', checkout / 'skills')
        self.addCleanup(patch.stopall)
        patch.object(setup, 'ROOT', checkout).start()
        self.config_file = self.folder / 'setup.toml'
        self.config_file.write_text('[multica]\nworkspace_id="workspace-1"\nruntime_id="runtime-1"\n'
                                    'squad_profiles=["software-delivery","open-research"]\nupdate_existing=true\n'
                                    '[host]\nlocal_runtime_ids=["runtime-1"]\nresearch=false\n'
                                    f'tool_root="{self.folder / "tools"}"\n')
        fake = self.folder / 'multica'
        fake.write_text(FAKE); fake.chmod(0o755)
        self.db = self.folder / 'db.json'
        patch.dict(os.environ, {'PATH': str(self.folder) + os.pathsep + os.environ['PATH'], 'FAKE_DB': str(self.db)}).start()

    def invoke(self, *args):
        with patch.object(sys, 'argv', ['setup.py', '--config', str(self.config_file), *args]), contextlib.redirect_stdout(io.StringIO()):
            setup.main()

    def test_plan_never_provisions_or_writes_remote_objects(self):
        with patch.object(setup.bootstrap_tools, 'install') as install:
            self.invoke('--plan')
            install.assert_not_called()
        self.assertEqual(json.loads(self.db.read_text())['writes'], 0)

    def test_apply_then_doctor_and_idempotent_refresh(self):
        with patch.object(setup.bootstrap_tools, 'install', return_value={'state': 'host-checked'}):
            self.invoke('--apply')
            before = json.loads(self.db.read_text())
            self.assertEqual((len(before['agents']), len(before['skills']), len(before['squads'])), (9, 11, 2))
            self.invoke('--apply')
            self.assertEqual(json.loads(self.db.read_text()), before)
        with patch.object(setup.bootstrap_tools, 'doctor', return_value={'state': 'host-checked'}):
            self.invoke('--doctor')
        self.assertEqual(json.loads(self.db.read_text()), before)

    def test_host_failure_prevents_workspace_mutation(self):
        with patch.object(setup.bootstrap_tools, 'install', side_effect=setup.bootstrap_tools.BootstrapError('offline')):
            with self.assertRaises(setup.bootstrap_tools.BootstrapError):
                self.invoke('--apply')
        self.assertEqual(json.loads(self.db.read_text())['writes'], 0)

    def test_unmapped_remote_runtime_is_rejected(self):
        self.config_file.write_text(self.config_file.read_text().replace('local_runtime_ids=["runtime-1"]', 'local_runtime_ids=[]'))
        with self.assertRaisesRegex(ValueError, 'declared local'):
            self.invoke('--plan')
        self.assertFalse(self.db.exists())

    def test_native_collision_requires_explicit_update(self):
        base = self.folder / 'skills'
        (base / 'ub-coding').mkdir(parents=True)
        (base / 'ub-coding/SKILL.md').write_text('custom')
        with self.assertRaisesRegex(ValueError, 'differs'):
            setup.native_plan({'native': {'skill_directories': [str(base)]}, 'multica': {'update_existing': False}})

    def test_native_update_keeps_backup_outside_discovery_directory(self):
        base = self.folder / 'native-skills'
        (base / 'ub-coding').mkdir(parents=True)
        (base / 'ub-coding/SKILL.md').write_text('custom instruction')
        self.config_file.write_text(self.config_file.read_text() + f'\n[native]\nskill_directories=["{base}"]\n')
        backup_root = setup.ROOT / '.multica/setup/native-backups'
        before = set(backup_root.glob('*/ub-coding/SKILL.md'))
        with patch.object(setup.bootstrap_tools, 'install', return_value={'state': 'host-checked'}):
            self.invoke('--host-only', '--apply')
        backups = set(backup_root.glob('*/ub-coding/SKILL.md')) - before
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups.pop().read_text(), 'custom instruction')
        self.assertEqual(len(list(base.iterdir())), 11)
        self.assertIn('name: ub-coding', (base / 'ub-coding/SKILL.md').read_text())


if __name__ == '__main__':
    unittest.main()
