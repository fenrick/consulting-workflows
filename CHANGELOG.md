# Changelog

All notable changes to this skill pack are documented in this file.

## [Unreleased]

- Added CI workflow running validation and full portfolio tests.
- Added dedicated security scan workflow and local security scan runner.
- Added release hardening docs (`CONTRIBUTING.md`, `SECURITY.md`).
- Added packaging script for distributable zip archives.
- Added output-contract and wording-compliance checks to portfolio tests.
- Added explicit Python dependency manifests (`requirements.txt`, `requirements-dev.txt`).
- Reworked packaging defaults to skill-folder-only archives for neutral runtime import.
- Added per-skill self-contained references/workflows/templates across all non-trivial skills.
- Added self-containment test gates to prevent parent-folder dependency regressions.

## [0.1.0] - 2026-03-13

- Initial multi-skill consulting workflow pack:
  - `consulting-workflow-orchestrator`
  - `input-evidence-cataloger`
  - `evidence-consistency-auditor`
  - `brief-storyline-architect`
  - `report-storyboard-builder`
  - `presentation-storyboard-builder`
  - `workshop-writeup-composer`
  - `document-writer`
