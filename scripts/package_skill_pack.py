#!/usr/bin/env python3
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


REPO_META_PATHS = (
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "scripts",
    "tests",
)

SKIP_SUFFIXES = {".pyc", ".pyo", ".zip"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create distributable zip archives for the skill collection and each skill."
    )
    parser.add_argument(
        "--output",
        default="dist/consulting-workflows",
        help="Collection archive path without extension (default: dist/consulting-workflows).",
    )
    parser.add_argument(
        "--version",
        default="",
        help="Optional version string. When set, archives are named with -v<version>.",
    )
    parser.add_argument(
        "--include-repo-meta",
        action="store_true",
        help="Include repository-level docs/scripts in the collection archive.",
    )
    return parser.parse_args()


def iter_skill_dirs(skills_dir: Path) -> list[Path]:
    return sorted(path for path in skills_dir.iterdir() if path.is_dir())


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if "__pycache__" in rel.parts:
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        if any(part.startswith(".") for part in rel.parts):
            continue
        files.append(path)
    return files


def add_tree(archive: zipfile.ZipFile, source_root: Path, archive_root: Path) -> None:
    for path in iter_files(source_root):
        archive.write(path, archive_root / path.relative_to(source_root))


def add_path(archive: zipfile.ZipFile, source_path: Path, archive_path: Path) -> None:
    if source_path.is_dir():
        add_tree(archive, source_path, archive_path)
        return
    archive.write(source_path, archive_path)


def build_archive(output_path: Path, members: list[tuple[Path, Path]]) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source_path, archive_path in members:
            add_path(archive, source_path, archive_path)
    return output_path


def version_suffix(version: str) -> str:
    return f"-v{version}" if version else ""


def resolve_output_base(root: Path, output_arg: str) -> Path:
    output_base = Path(output_arg)
    if output_base.suffix == ".zip":
        output_base = output_base.with_suffix("")
    if not output_base.is_absolute():
        output_base = root / output_base
    return output_base


def main() -> int:
    args = parse_args()

    root = Path(__file__).resolve().parents[1]
    skills_dir = root / "skills"
    if not skills_dir.exists():
        raise SystemExit("Missing required path for packaging: skills/")

    skill_dirs = iter_skill_dirs(skills_dir)
    if not skill_dirs:
        raise SystemExit("No skill folders found under skills/")

    output_base = resolve_output_base(root, args.output)
    output_dir = output_base.parent
    collection_name = output_base.name
    suffix = version_suffix(args.version.strip())

    created: list[Path] = []

    collection_members: list[tuple[Path, Path]] = []
    for skill_dir in skill_dirs:
        collection_members.append(
            (skill_dir, Path(collection_name) / skill_dir.name)
        )
    if args.include_repo_meta:
        for rel in REPO_META_PATHS:
            src = root / rel
            if src.exists():
                collection_members.append((src, Path(collection_name) / rel))

    collection_archive = build_archive(
        output_dir / f"{collection_name}{suffix}.zip",
        collection_members,
    )
    created.append(collection_archive)

    for skill_dir in skill_dirs:
        archive = build_archive(
            output_dir / f"{skill_dir.name}{suffix}.zip",
            [(skill_dir, Path(skill_dir.name))],
        )
        created.append(archive)

    for archive in created:
        print(f"[package_skill_pack] created: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
