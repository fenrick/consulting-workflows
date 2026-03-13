# [1.4.0](https://github.com/fenrick/consulting-workflows/compare/v1.3.0...v1.4.0) (2026-03-13)


### Bug Fixes

* **site:** improve kicker code contrast ([11dc927](https://github.com/fenrick/consulting-workflows/commit/11dc927f4df3750a327abd32f9108907d078beed))


### Features

* **document-writer:** harden authoring and diagram workflow ([72ddc62](https://github.com/fenrick/consulting-workflows/commit/72ddc629d9fc4572f080aaec23987f666d2cad5d))
* **document-writer:** render mermaid blocks during export ([cdc9366](https://github.com/fenrick/consulting-workflows/commit/cdc9366d7f01d10da9addd17fdc1703bd6ac49c1))
* **document-writer:** set document figure width policy ([977b6d0](https://github.com/fenrick/consulting-workflows/commit/977b6d0c30692943d5331c25840fe3b3cf1fdaf0))
* **document-writer:** style exported figure captions ([e2f87ba](https://github.com/fenrick/consulting-workflows/commit/e2f87ba34c850032779eb4ead56af4899b431da3))
* **document-writer:** tune mermaid defaults ([a4b5385](https://github.com/fenrick/consulting-workflows/commit/a4b53855bba6a45758cf120978901097c257921e))
* **site:** align docs theme with geist design system ([4e47a31](https://github.com/fenrick/consulting-workflows/commit/4e47a31ebad1b8ebc973a3c8c7f42f7f0e08e7dc))
* **site:** normalize skill card description length ([e138019](https://github.com/fenrick/consulting-workflows/commit/e13801961fbd54b3bf977cd2b61c058ac253352e))
* **site:** redesign docs site for v1.4 ([d1496b4](https://github.com/fenrick/consulting-workflows/commit/d1496b467a9277f21585560db9e3d4d9c0310e84))
* **skills:** add card descriptions and version metadata ([ef00478](https://github.com/fenrick/consulting-workflows/commit/ef00478e6b11d1f12ac35d35fcc8560e04625d05))
* **skills:** enforce reference contracts ([bcc43f9](https://github.com/fenrick/consulting-workflows/commit/bcc43f9fd11a319a9bf30d415783a503dd28392f))
* **skills:** standardize reference packs ([78cc9a3](https://github.com/fenrick/consulting-workflows/commit/78cc9a312461e04c5bbede842f24904c300135d7))

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
