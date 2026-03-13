#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a distributable archive for the skill pack."
    )
    parser.add_argument(
        "--output",
        default="dist/consulting-workflows",
        help="Archive path without extension (default: dist/consulting-workflows)",
    )
    parser.add_argument(
        "--include-repo-meta",
        action="store_true",
        help="Include repository-level docs/scripts in archive (default packages skill folders only).",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output_base = root / args.output
    output_base.parent.mkdir(parents=True, exist_ok=True)

    temp_root = root / ".tmp-package"
    if temp_root.exists():
        shutil.rmtree(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)

    package_root = temp_root / "consulting-workflows"
    package_root.mkdir(parents=True, exist_ok=True)

    skills_dir = root / "skills"
    if not skills_dir.exists():
        raise SystemExit("Missing required path for packaging: skills/")
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir():
            shutil.copytree(skill_dir, package_root / skill_dir.name)

    if args.include_repo_meta:
        include_paths = (
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "scripts",
            "tests",
        )
        for rel in include_paths:
            src = root / rel
            if not src.exists():
                continue
            dst = package_root / rel
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    archive_path = shutil.make_archive(str(output_base), "zip", root_dir=temp_root, base_dir=package_root.name)
    shutil.rmtree(temp_root)
    print(f"[package_skill_pack] created: {archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
