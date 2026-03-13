# Contributing

## Scope

This repository is a skill pack. Changes should improve output quality, portability, and deterministic behavior across supported runtimes.

## Required checks

Before opening a PR:

```bash
python3 scripts/validate_skill_portfolio.py
python3 scripts/run_portfolio_tests.py
./scripts/run_security_scans.sh
```

## Change standards

- Keep skill contracts explicit: required outputs, quality gate, working-material discipline, back-iteration loop.
- Keep references path-stable inside each skill (`references/quality-standard.md`, `references/workflow.md`).
- Do not add runtime-specific behavior that bypasses markdown-first workflows.
- Do not remove required tracking artifacts from `document-writer`:
  - `tracking/document-brief.md`
  - `tracking/source-register.md`
  - `tracking/review-notebook.md`
  - `tracking/findings-workbook.md`
  - `tracking/open-questions.md`

## Versioning

- Use semantic versioning tags (`vMAJOR.MINOR.PATCH`).
- Update `CHANGELOG.md` in the same PR as the change.
- For breaking contract changes, increment MAJOR.

## PR expectations

- Include a short statement of what changed and why.
- Include command output from required checks.
