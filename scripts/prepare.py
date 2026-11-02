#!/usr/bin/env python3
"""Prepare local Multica instructions and complete skill archives; no network calls."""

import hashlib
import io
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
from catalog import ROLES, SQUADS, SKILLS

SQUAD_POLICY_COMMON = {
    profile: ("squads/research-common.md" if profile == "open-research" else "squads/common.md")
    for profile in SQUADS
}
RESOURCE_DIRS = {"references", "assets", "templates"}


def checked_path(root, relative):
    """Reject traversal and symlinks before reading sources or writing outputs."""
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts or "\\" in str(relative):
        raise ValueError(f"Refusing path outside the repository: {relative}")
    current = root
    for part in (None, *relative.parts):
        if part is not None:
            current = current / part
        if current.is_symlink():
            raise ValueError(f"Refusing symlink: {current}")
    return current


def read_text(root, relative):
    content = checked_path(root, relative).read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Source is empty: {relative}")
    return content


def skill_files(root, name):
    base = checked_path(root, f"skills/{name}")
    # All current resources are Markdown. Fail on unexpected content rather than
    # silently omitting resources or shipping caches, credentials, or local files.
    read_text(root, f"skills/{name}/SKILL.md")
    files = {}

    def visit(directory):
        for path in sorted(directory.iterdir()):
            checked_path(root, path.relative_to(root))
            relative = path.relative_to(base)
            if path.is_dir():
                if relative.parts[0] not in RESOURCE_DIRS or any(
                    part.startswith(".") or part == "__pycache__" for part in relative.parts
                ):
                    raise ValueError(f"Unexpected skill directory: {path.relative_to(root)}")
                visit(path)
            elif path.is_file() and (
                relative == Path("SKILL.md")
                or len(relative.parts) > 1
                and relative.parts[0] in RESOURCE_DIRS
                and path.suffix == ".md"
                and not any(part.startswith(".") for part in relative.parts)
            ):
                files[relative.as_posix()] = path.read_bytes()
            else:
                raise ValueError(f"Unexpected skill resource: {path.relative_to(root)}")

    visit(base)
    return dict(sorted(files.items()))


def make_archive(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, content)
    return buffer.getvalue()


def digest(content):
    return hashlib.sha256(content).hexdigest()


def prepare(root=ROOT):
    root = Path(root)
    # Prepare every byte before creating output directories. Missing, empty, or
    # unsafe sources must not leave a partly refreshed bundle.
    common = read_text(root, "agents/common.md")
    prompts = {}
    for role in ROLES:
        body = read_text(root, f"agents/{role}.md")
        prompts[f"agents/{role}.md"] = common + "\n\n" + body + "\n"
    for profile in SQUADS:
        squad_common = read_text(root, SQUAD_POLICY_COMMON[profile])
        prompts[f"squads/{profile}.md"] = (
            squad_common + "\n\n" + read_text(root, f"squads/{profile}.md") + "\n"
        )
    # Preserve the original default path for existing manual installation steps.
    prompts["squad.md"] = prompts["squads/research-engineering.md"]
    outputs = {name: content.encode("utf-8") for name, content in prompts.items()}
    manifest = {
        "format": "local-instruction-bundle-v3",
        "description": "Local file inventory; not a Multica import schema.",
        "squads": {
            profile: {**metadata, "instructions": f"squads/{profile}.md", "leader": "lead"}
            for profile, metadata in SQUADS.items()
        },
        "files": {
            name: {"sha256": digest(outputs[name]), "words": len(content.split())}
            for name, content in prompts.items()
        },
        "skills": {},
    }
    for name in SKILLS:
        files = skill_files(root, name)
        archive_name = f"skills/{name}.zip"
        outputs[archive_name] = make_archive(files)
        manifest["skills"][name] = {
            "archive": archive_name,
            "sha256": digest(outputs[archive_name]),
            "entrypoint": "SKILL.md",
            "files": {
                path: {"sha256": digest(content), "bytes": len(content)}
                for path, content in files.items()
            },
        }
    outputs["bundle.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")

    destination = checked_path(root, "build/multica")
    for name in outputs:
        output = checked_path(root, Path("build/multica") / name)
        if output.exists() and not output.is_file():
            raise ValueError(f"Output is not a regular file: {output}")
        for parent in output.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Output parent is not a directory: {parent}")

    for name, content in outputs.items():
        output = destination / name
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(content)
    print(f"Prepared {len(ROLES)} reusable agent instructions, {len(SQUADS)} squad policies, and {len(SKILLS)} complete skill archives.")
    print("Outputs: build/multica/. The manifest is a local inventory, not a Multica import schema.")
    print("No live agents, skills, squads, or issues were changed.")


if __name__ == "__main__":
    try:
        prepare()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Preparation failed: {error}") from error
