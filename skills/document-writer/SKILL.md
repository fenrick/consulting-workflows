---
name: document-writer
description: Use when producing substantial evidence-led documents via a markdown-first workflow with tracked working materials and optional packaged export.
---

# Document Writer

Use this skill when the task needs disciplined document workflow ownership, not just a final packaged file.

## When to use

- substantial reports from mixed source material
- architecture, review, audit, or assessment documents
- markdown-first drafting with traceable evidence and controlled editorial passes
- Mermaid-backed diagrams that need reproducible PNG/SVG render outputs for embedding
- optional packaged export through Pandoc

## Bundled materials (progressive disclosure order)

1. Read this `SKILL.md` for contract and boundaries.
2. Read `references/workflow.md` for full operating method.
3. Read `references/validation-checklist.md` before handoff.
4. Use `references/repo-map.md` for path/layout expectations.
5. Use `references/term-sheet.md` for stable terms.
6. Use `references/tracking-readme.md` for tracking template intent.
7. Use `assets/tracking-templates/` and front-end templates only when scaffolding.
8. Run `scripts/` only after workflow setup is complete.

## Working materials discipline

- keep canonical prose in markdown working files
- keep observations, findings, decisions, and open items in tracking files
- keep scripts as transform/export tooling only
- do not store substantive narrative in generator code
- build every substantial document through the cyclic loop: skeleton, bullet points, paragraphs, narrative flow, humanise, neutral voice and simple language

Apply quality checks from `references/quality-standard.md`.

## Required tracking artifacts

- `tracking/document-brief.md`
- `tracking/source-register.md`
- `tracking/section-status.md`
- `tracking/decision-log.md`
- `tracking/open-questions.md`
- `tracking/editorial-pass.md`
- `tracking/release-check.md`
- `tracking/review-notebook.md` (for review/audit/assessment work)
- `tracking/findings-workbook.md` (for review/audit/assessment work)

## Minimum workflow

1. Scaffold files:
   - `python3 scripts/scaffold_document.py`
2. Replace title/subtitle placeholders immediately.
3. Lock the citation path before drafting:
   - APA v7 bibliography entries in `report-body/references.bib`
   - Pandoc/Writage in-text citations such as `[@smith2024]`
4. Draft and revise in markdown (`report-body/`), not in `full/`, using the cyclic authoring loop from `references/workflow.md`.
5. Render Mermaid diagrams when needed:
   - `python3 scripts/render_mermaid.py report-body/diagrams/example.mmd --output-dir report-body/media`
6. Assemble:
   - `python3 scripts/assemble_report.py`
7. Export packaged output only after assembly is stable:
   - `python3 scripts/export_docx.py --assemble --reference-doc assets/reference.docx`
8. Run validation and prose pass before release.
9. Share working files and packaged output together.

## Authoring boundary

- helper tools may inspect/extract, but markdown workflow remains canonical
- packaged output generation is downstream packaging, not the authoring surface
- if the user explicitly requires direct binary editing from the start, treat this skill as supporting context, not primary authoring

## Runtime dependency

- `requirements.txt` (secure XML parsing dependency for `scripts/export_docx.py`)
- repo-root `package.json` dev dependency `@mermaid-js/mermaid-cli` for high-resolution diagram rendering

## Bundled resources

- `scripts/assemble_report.py`
- `scripts/export_docx.py`
- `scripts/render_mermaid.py`
- `scripts/scaffold_document.py`
- `scripts/package_skill.py`
- `assets/reference.docx`
- `assets/mermaid/mermaid-config.json`
- `assets/title-block-template.md`
- `assets/front-end-outline-template.md`
- `assets/tracking-templates/`
- `references/workflow.md`
- `references/quality-standard.md`
- `references/validation-checklist.md`
- `references/term-sheet.md`
- `references/tracking-readme.md`
- `references/repo-map.md`

## Do not

- draft substantial prose only in chat
- bypass tracking artifacts
- treat packaged output as the only deliverable
- hide canonical document prose inside scripts
