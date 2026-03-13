# Consulting Workflows Skills

Reusable cross-tool skills for consulting-grade evidence intake, storyline design, storyboard production, workshop write-ups, and document assembly.

This pack is designed for local-skill workflows and can be distributed through standard skill-pack channels such as [skills.sh](https://skills.sh).
Skill folder shape is aligned to the [Agent Skills specification](https://agentskills.io/specification): each skill is self-contained.

## Repository layout

- `skills/`: installable skills (`SKILL.md` + supporting assets/scripts)
- `scripts/`: portfolio validation and test harness scripts
- `tests/`: fixtures used by the end-to-end checks

## Included skills

- `consulting-workflow-orchestrator`
- `input-evidence-cataloger`
- `evidence-consistency-auditor`
- `brief-storyline-architect`
- `report-storyboard-builder`
- `presentation-storyboard-builder`
- `workshop-writeup-composer`
- `document-writer`

## Quality checks

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_skill_portfolio.py
python3 scripts/run_portfolio_tests.py
```

## Security scans

Run locally:

```bash
./scripts/run_security_scans.sh
```

Required local tools:

- `gitleaks`
- `pip-audit`
- `semgrep`

Example install on macOS:

```bash
brew install gitleaks semgrep pip-audit
```

These scans do not require an LLM API key.

## Packaging

Build a distributable archive:

```bash
python3 scripts/package_skill_pack.py
```

Default output:

- `dist/consulting-workflows.zip`
- archive contains skill folders only (no parent docs required by host runtimes)

## Install matrix

- Codex-style runtimes:
  - copy unpacked skill folders under your configured skills home (for example `$CODEX_HOME/skills`)
- Claude-style local skills:
  - copy unpacked skill folders into the runtime's local skills directory
- Generic local runners:
  - keep repo layout intact (`skills/`, `references/`, `scripts/`, `tests/`) and run quality checks before use

## Versioning

- Semantic version tags: `vMAJOR.MINOR.PATCH`
- See [`CHANGELOG.md`](CHANGELOG.md)
- Tagging a release (`git tag vX.Y.Z && git push origin vX.Y.Z`) triggers the release workflow and publishes `dist/consulting-workflows.zip`.
