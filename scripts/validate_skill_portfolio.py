#!/usr/bin/env python3
from __future__ import annotations

import sys
import re
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

REQUIRED_REFERENCE_FILES = {
    "workflow.md",
    "quality-standard.md",
    "validation-checklist.md",
    "term-sheet.md",
    "repo-map.md",
    "tracking-readme.md",
}

REFERENCE_REQUIRED_HEADINGS = {
    "workflow.md": [
        "## Purpose",
        "## Working files",
        "## Back-iteration loop",
        "## Handoff and closure",
    ],
    "quality-standard.md": [
        "## Purpose",
        "## Core standard",
        "## Authoring standard",
        "## Tracking standard",
        "## Handoff standard",
    ],
    "validation-checklist.md": [
        "## Purpose",
        "## How to use this checklist",
    ],
    "term-sheet.md": [
        "## Purpose",
        "## Core terms",
        "## Usage rules",
        "## Drift-control rules",
    ],
    "repo-map.md": [
        "## Purpose",
        "## Main files",
        "## Typical flow",
        "## Handoff note",
    ],
    "tracking-readme.md": [
        "## Purpose",
        "## Template roles",
        "## Working rule",
    ],
}

MAX_SKILL_LINES = 220
MAX_SKILL_TOKENS_APPROX = 3500


def fail(msg: str) -> None:
    print(f"[validate_skill_portfolio] {msg}", file=sys.stderr)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def approx_token_count(text: str) -> int:
    # lightweight approximation suitable for linting budgets
    return max(1, len(text) // 4)


def parse_backticked_paths(text: str) -> list[str]:
    candidates = re.findall(r"`([^`]+)`", text)
    paths: list[str] = []
    for candidate in candidates:
        if "/" in candidate or candidate.endswith(".txt") or candidate.endswith(".md"):
            paths.append(candidate.strip())
    return paths


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        fail("No SKILL.md files found under skills/.")
        return 1

    errors: list[str] = []
    for file_path in skill_files:
        text = file_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        skill_name = frontmatter.get("name")
        if not skill_name:
            errors.append(f"{file_path}: missing `name:` in frontmatter")
            continue

        description = frontmatter.get("description", "")
        if not description:
            errors.append(f"{file_path}: missing `description:` in frontmatter")
        elif len(description) > 1024:
            errors.append(f"{file_path}: `description` exceeds 1024 characters")

        if file_path.parent.name != skill_name:
            errors.append(
                f"{file_path}: frontmatter `name` must match folder name (`{file_path.parent.name}`)"
            )

        if not re.fullmatch(r"[a-z0-9-]+", skill_name):
            errors.append(f"{file_path}: invalid skill name format `{skill_name}`")

        line_count = len(text.splitlines())
        if line_count > MAX_SKILL_LINES:
            errors.append(f"{file_path}: exceeds {MAX_SKILL_LINES} line limit ({line_count})")
        token_count = approx_token_count(text)
        if token_count > MAX_SKILL_TOKENS_APPROX:
            errors.append(
                f"{file_path}: exceeds ~{MAX_SKILL_TOKENS_APPROX} token budget ({token_count} approx)"
            )

        expected = REQUIRED_HEADINGS.get(skill_name, [])
        for heading in expected:
            if heading not in text:
                errors.append(f"{file_path}: missing heading `{heading}`")

        if skill_name in REQUIRED_HEADINGS and "quality-standard.md" not in text:
            errors.append(
                f"{file_path}: missing reference to shared quality standard"
            )

        # progressive disclosure hygiene: references to local files should resolve.
        for referenced in parse_backticked_paths(text):
            if referenced.startswith(("tracking/", "inputs/", "report-body/", "full/")):
                continue
            if referenced.startswith("http://") or referenced.startswith("https://"):
                continue
            resolved = file_path.parent / referenced.rstrip("/")
            if referenced.endswith("/"):
                if not resolved.exists() or not resolved.is_dir():
                    errors.append(f"{file_path}: referenced directory missing `{referenced}`")
                continue
            if referenced.startswith(("assets/", "scripts/", "references/", "agents/")) or referenced == "requirements.txt":
                if not resolved.exists():
                    errors.append(f"{file_path}: referenced file missing `{referenced}`")

        # if a skill ships python scripts, it must declare requirements.txt.
        scripts_dir = file_path.parent / "scripts"
        if scripts_dir.exists() and list(scripts_dir.glob("*.py")):
            req_file = file_path.parent / "requirements.txt"
            if not req_file.exists():
                errors.append(f"{file_path.parent}: missing requirements.txt for python scripts")

        references_dir = file_path.parent / "references"
        missing_reference_files = sorted(
            ref for ref in REQUIRED_REFERENCE_FILES if not (references_dir / ref).exists()
        )
        for ref in missing_reference_files:
            errors.append(f"{file_path.parent}: missing references/{ref}")
        for ref_name, headings in REFERENCE_REQUIRED_HEADINGS.items():
            ref_path = references_dir / ref_name
            if not ref_path.exists():
                continue
            ref_text = ref_path.read_text(encoding="utf-8")
            for heading in headings:
                if heading not in ref_text:
                    errors.append(f"{ref_path}: missing heading `{heading}`")

        # validate optional openai adapter metadata if present.
        openai_yaml = file_path.parent / "agents" / "openai.yaml"
        if openai_yaml.exists():
            yaml_text = openai_yaml.read_text(encoding="utf-8")
            for required_key in (
                "interface:",
                "display_name:",
                "short_description:",
                "default_prompt:",
            ):
                if required_key not in yaml_text:
                    errors.append(f"{openai_yaml}: missing `{required_key}`")

    if errors:
        for err in errors:
            fail(err)
        return 1

    print("[validate_skill_portfolio] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
