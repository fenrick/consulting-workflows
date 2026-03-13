#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


TRACKING_FILES = {
    "document-brief-template.md": "document-brief.md",
    "source-register-template.md": "source-register.md",
    "section-status-template.md": "section-status.md",
    "decision-log-template.md": "decision-log.md",
    "open-questions-template.md": "open-questions.md",
    "editorial-pass-template.md": "editorial-pass.md",
    "release-check-template.md": "release-check.md",
    "review-notebook-template.md": "review-notebook.md",
    "findings-workbook-template.md": "findings-workbook.md",
}


def parse_args() -> argparse.Namespace:
    project_root = Path.cwd()
    parser = argparse.ArgumentParser(
        description="Scaffold the working document files for a new document stream."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=project_root,
        help="Target project root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing scaffolded files.",
    )
    return parser.parse_args()


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_template(source: Path, dest: Path, force: bool) -> None:
    if dest.exists() and not force:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    skill_root = Path(__file__).resolve().parent.parent
    assets_dir = skill_root / "assets"
    tracking_templates_dir = assets_dir / "tracking-templates"

    copy_template(
        assets_dir / "title-block-template.md",
        project_root / "report-body" / "title-block.md",
        args.force,
    )
    write_file(
        project_root / "report-body" / "01 - Executive Summary.md",
        "# Executive Summary\n\n",
        args.force,
    )
    write_file(
        project_root / "report-body" / "02 - Introduction.md",
        "# Introduction\n\n## Purpose\n\n## Scope\n\n## Method\n\n## What This Document Is and Is Not\n\n",
        args.force,
    )
    (project_root / "full").mkdir(parents=True, exist_ok=True)

    for source_name, dest_name in TRACKING_FILES.items():
        copy_template(
            tracking_templates_dir / source_name,
            project_root / "tracking" / dest_name,
            args.force,
        )

    print(project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
