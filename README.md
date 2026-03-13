<p align="center">
  <img src=".github/assets/consulting-workflows-mark.svg" alt="Consulting Workflows mark" width="96">
</p>

<h1 align="center">Consulting Workflows</h1>

<p align="center">
  Cross-tool agent skills for evidence intake, storyline design, storyboard production, workshop write-ups, and document assembly.
</p>

<p align="center">
  <a href="https://github.com/fenrick/consulting-workflows/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/fenrick/consulting-workflows?display_name=tag&sort=semver"></a>
  <a href="https://github.com/fenrick/consulting-workflows/actions/workflows/ci.yml"><img alt="Quality checks" src="https://img.shields.io/github/actions/workflow/status/fenrick/consulting-workflows/ci.yml?branch=main&label=quality"></a>
  <a href="https://github.com/fenrick/consulting-workflows/actions/workflows/security-scan.yml"><img alt="Security scans" src="https://img.shields.io/github/actions/workflow/status/fenrick/consulting-workflows/security-scan.yml?branch=main&label=security"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/fenrick/consulting-workflows"></a>
  <a href="https://agentskills.io/specification"><img alt="Agent Skills specification" src="https://img.shields.io/badge/spec-agentskills.io-0b7285"></a>
</p>

`consulting-workflows` is a distribution repository for self-contained skills that can be used across Codex, Claude Code, and other runtimes that consume local skill folders or packaged skill archives. The pack is aligned to the [Agent Skills specification](https://agentskills.io/specification) and is designed for consulting-grade work rather than generic prompt snippets.

## What This Repo Contains

| Skill | Purpose |
| --- | --- |
| `consulting-workflow-orchestrator` | Runs a structured multi-skill workflow from intake through final deliverable. |
| `input-evidence-cataloger` | Catalogs source material, maps document sets, and records factual observations from inputs. |
| `evidence-consistency-auditor` | Checks claims, gaps, contradictions, and evidence traceability across working materials. |
| `brief-storyline-architect` | Turns a brief and evidence base into a consulting-style storyline and narrative structure. |
| `report-storyboard-builder` | Converts a storyline into a written-report skeleton and section file plan. |
| `presentation-storyboard-builder` | Converts a storyline into a presentation-ready slide sequence and narrative spine. |
| `workshop-writeup-composer` | Produces formal workshop outputs from transcripts and supporting material. |
| `document-writer` | Builds substantial final documents with tracked working materials, citations, and document export tooling. |

## Download Options

- Download the full pack from [latest release](https://github.com/fenrick/consulting-workflows/releases/latest) if your runtime supports multiple skills in one archive.
- Download a single `<skill-name>-vX.Y.Z.zip` asset if your runtime expects one skill per archive.
- Use the collection asset `consulting-workflows-vX.Y.Z.zip` if you want the whole set in one shot.

Single-skill archives are published because some runtimes only accept one skill per ZIP. The release process publishes both formats on every tagged release.

## Quick Start

1. Download the latest collection ZIP or a single-skill ZIP from the releases page.
2. Unpack the archive into your runtime's local skills directory.
3. For Codex-style runtimes, place unpacked folders under your configured skills home such as `$CODEX_HOME/skills`.
4. For Claude-style runtimes, place unpacked folders into the runtime's local skills directory.

## Repository Layout

- `skills/`: installable skills (`SKILL.md` plus supporting assets, scripts, and references)
- `scripts/`: validation, packaging, and portfolio test harness scripts
- `tests/`: fixtures used by end-to-end checks

## Quality Checks

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_skill_portfolio.py
python3 scripts/run_portfolio_tests.py
```

## Security Scans

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

Build the collection ZIP and one ZIP per skill:

```bash
python3 scripts/package_skill_pack.py
```

Build versioned artifacts:

```bash
python3 scripts/package_skill_pack.py --version 1.2.3
```

Default outputs:

- `dist/consulting-workflows.zip`
- `dist/<skill-name>.zip` for each skill under `skills/`

Versioned outputs:

- `dist/consulting-workflows-vX.Y.Z.zip`
- `dist/<skill-name>-vX.Y.Z.zip` for each skill under `skills/`

Use `--include-repo-meta` only for internal sharing. Host runtimes generally only need the skill folders.

## Release Model

- Releases are automated by `semantic-release` on pushes to `main`.
- Commit messages must follow Conventional Commits such as `feat:`, `fix:`, and `chore:`.
- `CHANGELOG.md` and GitHub Releases are updated automatically when a release is cut.
- Each release publishes the collection archive and a single-skill archive for every packaged skill.
