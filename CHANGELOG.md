# [1.3.0](https://github.com/fenrick/consulting-workflows/compare/v1.2.0...v1.3.0) (2026-03-13)


### Features

* **pages:** generate and deploy per-skill docs site ([0bfb45f](https://github.com/fenrick/consulting-workflows/commit/0bfb45fed3e2ea8214b756c6f1ba8a10e582c709))

# [1.2.0](https://github.com/fenrick/consulting-workflows/compare/v1.1.0...v1.2.0) (2026-03-13)


### Features

* **repo:** improve GitHub project presentation ([f4db9c5](https://github.com/fenrick/consulting-workflows/commit/f4db9c5d77294ffda20e2d769c6492e0c8d1d550))

# [1.1.0](https://github.com/fenrick/consulting-workflows/compare/v1.0.1...v1.1.0) (2026-03-13)


### Features

* **release:** package versioned collection and per-skill archives ([431a12b](https://github.com/fenrick/consulting-workflows/commit/431a12be0b3a7e07474598cff84f6c39c60eea90))

## [1.0.1](https://github.com/fenrick/consulting-workflows/compare/v1.0.0...v1.0.1) (2026-03-13)


### Bug Fixes

* **release:** upload packaged skill zip as release asset ([cb0ed4e](https://github.com/fenrick/consulting-workflows/commit/cb0ed4e760293ff26bdf64e744219d74aff617f3))

# 1.0.0 (2026-03-13)


### Features

* add consulting workflow orchestrator and stage-gate flow ([53f4a1a](https://github.com/fenrick/consulting-workflows/commit/53f4a1a27b028fd339fae95befe4b055e8f856c2))
* add document-writer skill with pandoc export tooling ([5141728](https://github.com/fenrick/consulting-workflows/commit/5141728a4934cf2ff3c1e9246496d4403e543af3))
* add input evidence cataloger and consistency auditor skills ([31a8789](https://github.com/fenrick/consulting-workflows/commit/31a87891c807ea9157a7f58b247d36d691b93213))
* add report and presentation storyboard builder skills ([6213a37](https://github.com/fenrick/consulting-workflows/commit/6213a3743925032ad55434a3cc4a61befc825686))
* add workshop writeup composer skill ([11f4978](https://github.com/fenrick/consulting-workflows/commit/11f4978104ee703dfdebf199a769330cee8060e5))
* **ci:** add quality and security CI workflows ([5c9aca7](https://github.com/fenrick/consulting-workflows/commit/5c9aca7fe495f4521738a45783900264ae54b715))
* **ci:** adopt semantic-release for automated versioning and releases ([08c1fd8](https://github.com/fenrick/consulting-workflows/commit/08c1fd8b50bd00882ba4b27d073157b5fb8137e1))

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
