"""Exercise packaging and filesystem safety without contacting Multica."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import zipfile


sys.dont_write_bytecode = True
SCRIPT = Path(__file__).with_name("prepare.py")
spec = importlib.util.spec_from_file_location("prepare", SCRIPT)
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        for folder in ("agents", "squads", "skills"):
            shutil.copytree(prepare.ROOT / folder, self.root / folder)

    def run_prepare(self):
        with contextlib.redirect_stdout(io.StringIO()):
            prepare.prepare(self.root)

    def outputs(self):
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in sorted((self.root / "build").rglob("*")) if path.is_file()
        }

    def test_complete_deterministic_archives_and_inventory(self):
        self.run_prepare()
        first = self.outputs()
        manifest = json.loads((self.root / "build/multica/bundle.json").read_text())
        self.assertEqual(set(manifest["skills"]), set(prepare.SKILLS))
        self.assertEqual(len(manifest["files"]), len(prepare.ROLES) + len(prepare.SQUADS) + 1)
        self.assertEqual(set(manifest["squads"]), set(prepare.SQUADS))
        for name, metadata in manifest["skills"].items():
            archive_path = self.root / "build/multica" / metadata["archive"]
            self.assertEqual(hashlib.sha256(archive_path.read_bytes()).hexdigest(), metadata["sha256"])
            source = self.root / "skills" / name
            expected = {
                path.relative_to(source).as_posix(): path.read_bytes()
                for path in source.rglob("*") if path.is_file()
            }
            with zipfile.ZipFile(archive_path) as archive:
                self.assertIn("SKILL.md", archive.namelist())
                self.assertEqual(set(archive.namelist()), set(expected))
                self.assertEqual(set(metadata["files"]), set(expected))
                for path, content in expected.items():
                    self.assertEqual(archive.read(path), content)
                    self.assertEqual(metadata["files"][path]["sha256"], hashlib.sha256(content).hexdigest())
        # Source mtime changes must not alter archive bytes or inventory.
        for path in (self.root / "skills").rglob("*.md"):
            path.touch()
        self.run_prepare()
        self.assertEqual(first, self.outputs())

    def test_cli_from_another_working_directory(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        shutil.copy2(SCRIPT, scripts / "prepare.py")
        shutil.copy2(SCRIPT.with_name("catalog.py"), scripts / "catalog.py")
        result = subprocess.run(
            [sys.executable, "-B", str(scripts / "prepare.py")],
            cwd=self.temporary.name, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "build/multica/skills/review-paper.zip").is_file())
        self.assertFalse((Path(self.temporary.name) / "build").exists())

    def test_generated_prompts_separate_agent_contract_from_squad_policies(self):
        self.run_prepare()
        common = (self.root / "agents/common.md").read_text().strip()
        for role in prepare.ROLES:
            generated = (self.root / "build/multica/agents" / f"{role}.md").read_text()
            self.assertEqual(generated, common + "\n\n" + (self.root / "agents" / f"{role}.md").read_text().strip() + "\n")
            self.assertNotRegex(generated, r'\b(?:G|U|FR|BR|AC|KPI|OP|RISK|ADR|FINDING)-')
            self.assertNotIn("two unsuccessful", generated.lower())
            self.assertNotIn("repair counter", generated.lower())
            self.assertNotIn("event-driven loop", generated.lower())
        for profile in prepare.SQUADS:
            squad_common = (self.root / prepare.SQUAD_POLICY_COMMON[profile]).read_text().strip()
            generated = (self.root / "build/multica/squads" / f"{profile}.md").read_text()
            self.assertEqual(generated, squad_common + "\n\n" + (self.root / "squads" / f"{profile}.md").read_text().strip() + "\n")
        self.assertEqual(
            (self.root / "build/multica/squad.md").read_text(),
            (self.root / "build/multica/squads/research-engineering.md").read_text(),
        )

    def test_missing_squad_source_does_not_refresh_outputs(self):
        self.run_prepare()
        before = self.outputs()
        (self.root / "squads/open-research.md").unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_prepare()
        self.assertEqual(before, self.outputs())

    def test_skill_resource_links_survive_standalone_import(self):
        for name in prepare.SKILLS:
            skill = self.root / "skills" / name
            for source in skill.rglob("*.md"):
                for raw in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', source.read_text()):
                    link = urlsplit(raw.split(' "')[0].strip("<>"))
                    if link.scheme or not link.path:
                        continue
                    target = (source.parent / unquote(link.path)).resolve()
                    with self.subTest(skill=name, source=source.name, link=raw):
                        self.assertIn(skill, target.parents, "resource link escapes imported skill")
                        self.assertTrue(target.is_file(), "linked resource is missing")

    def test_missing_source_does_not_create_or_refresh_outputs(self):
        missing = self.root / "skills/deliver-slice/SKILL.md"
        original = missing.read_bytes()
        missing.unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_prepare()
        self.assertFalse((self.root / "build").exists())
        missing.write_bytes(original)
        self.run_prepare()
        before = self.outputs()
        (self.root / "agents/lead.md").write_text("A changed profile")
        missing.unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_prepare()
        self.assertEqual(before, self.outputs())

    def test_empty_entrypoint_fails_before_writing(self):
        (self.root / "skills/analyze-data/SKILL.md").write_text("  \n")
        with self.assertRaisesRegex(ValueError, "Source is empty"):
            self.run_prepare()
        self.assertFalse((self.root / "build").exists())

    def test_symlink_sources_are_rejected(self):
        targets = ("agents/common.md", "skills/review-paper", "skills/analyze-data/assets/analysis-ledger.md")
        for relative in targets:
            with self.subTest(relative=relative):
                source = self.root / relative
                backup = source.with_name(source.name + "-saved")
                source.rename(backup)
                source.symlink_to(backup, target_is_directory=backup.is_dir())
                try:
                    with self.assertRaisesRegex(ValueError, "Refusing symlink"):
                        self.run_prepare()
                    self.assertFalse((self.root / "build").exists())
                finally:
                    source.unlink()
                    backup.rename(source)

    def test_symlink_outputs_are_rejected_without_external_changes(self):
        self.run_prepare()
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        sentinel = outside / "sentinel"
        sentinel.write_text("unchanged")
        targets = ("build/multica/skills", "build/multica/agents/lead.md", "build/multica/bundle.json")
        for relative in targets:
            with self.subTest(relative=relative):
                output = self.root / relative
                backup = output.with_name(output.name + "-saved")
                output.rename(backup)
                output.symlink_to(outside if backup.is_dir() else sentinel, target_is_directory=backup.is_dir())
                try:
                    with self.assertRaisesRegex(ValueError, "Refusing symlink"):
                        self.run_prepare()
                    self.assertEqual(sentinel.read_text(), "unchanged")
                    self.assertEqual(list(outside.iterdir()), [sentinel])
                finally:
                    output.unlink()
                    backup.rename(output)

    def test_unexpected_private_or_generated_files_are_rejected(self):
        for relative in (".env", "assets/token.txt", "references/__pycache__/cached.pyc"):
            with self.subTest(relative=relative):
                path = self.root / "skills/frame-problem" / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("must not be packaged")
                try:
                    with self.assertRaisesRegex(ValueError, "Unexpected skill"):
                        self.run_prepare()
                    self.assertFalse((self.root / "build").exists())
                finally:
                    path.unlink()
                    if path.parent.name == "__pycache__":
                        path.parent.rmdir()

    def test_absolute_paths_and_traversal_are_rejected(self):
        for relative in ("../outside", "skills/../../outside", "/tmp/outside", r"references/..\outside.md"):
            with self.subTest(relative=relative):
                with self.assertRaisesRegex(ValueError, "outside the repository"):
                    prepare.checked_path(self.root, relative)


if __name__ == "__main__":
    unittest.main()
