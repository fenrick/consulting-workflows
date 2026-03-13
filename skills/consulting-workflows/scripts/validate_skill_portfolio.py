#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_HEADINGS = {
    "input-evidence-cataloger": [
        "## Core outcome",
        "## Required outputs",
        "## Quality gate",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "brief-storyline-architect": [
        "## Core outcome",
        "## Required outputs",
        "## Quality gate",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "report-storyboard-builder": [
        "## Core outcome",
        "## Required outputs",
        "## Quality gate",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "presentation-storyboard-builder": [
        "## Core outcome",
        "## Required outputs",
        "## Quality gate",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "consulting-workflow-orchestrator": [
        "## Pipeline order",
        "## Orchestration outputs",
        "## Stage gate contract",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "evidence-consistency-auditor": [
        "## Core outcome",
        "## Required outputs",
        "## Quality gate",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "workshop-writeup-composer": [
        "## Core outcome",
        "## Required outputs",
        "## Quality gate",
        "## Working materials discipline",
        "## Back-iteration loop",
        "## Do not",
    ],
    "document-writer": [
        "## Working materials discipline",
    ],
}


def fail(msg: str) -> None:
    print(f"[validate_skill_portfolio] {msg}", file=sys.stderr)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill_files = sorted(root.glob("**/SKILL.md"))
    if not skill_files:
        fail("No SKILL.md files found under consulting-workflows.")
        return 1

    errors: list[str] = []
    for file_path in skill_files:
        text = file_path.read_text(encoding="utf-8")
        skill_name = None
        for line in text.splitlines():
            if line.startswith("name: "):
                skill_name = line.split("name: ", 1)[1].strip()
                break
        if not skill_name:
            errors.append(f"{file_path}: missing `name:` in frontmatter")
            continue

        expected = REQUIRED_HEADINGS.get(skill_name, [])
        for heading in expected:
            if heading not in text:
                errors.append(f"{file_path}: missing heading `{heading}`")

        if skill_name in REQUIRED_HEADINGS and "quality-standard.md" not in text:
            errors.append(
                f"{file_path}: missing reference to shared quality standard"
            )

    if errors:
        for err in errors:
            fail(err)
        return 1

    print("[validate_skill_portfolio] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
