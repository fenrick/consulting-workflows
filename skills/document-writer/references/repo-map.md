# Bundle Map for the Document Writer Skill

## Purpose

This map shows where canonical document content, media, bibliography, tracking files, and packaging outputs should live.

Use it to keep authoring state in predictable locations and stop the delivery tooling from becoming the hidden source of truth.

## Main working surfaces

- `report-body/`: canonical split draft
- `report-body/diagrams/`: editable Mermaid source files when diagrams are authored in Mermaid
- `report-body/media/`: images referenced by the split draft
- `report-body/references.bib`: bibliography for Pandoc/Writage citations
- `report-body/title-block.md`: document title and subtitle block
- `full/`: assembled output and copied media
- `assets/reference.docx`: reference document for Pandoc export
- `assets/title-block-template.md`: starting point for the title block
- `assets/front-end-outline-template.md`: starting point for the executive summary and introduction

## Scripts

- `scripts/assemble_report.py`: combines split sections into `full/combined-report.md`
- `scripts/export_docx.py`: exports the assembled markdown to a packaged document using Pandoc
- `scripts/render_mermaid.py`: renders Mermaid source files to high-resolution PNG/SVG outputs for embedding
- `scripts/scaffold_document.py`: creates the baseline title block, front-end section files, and tracking files
- `scripts/package_skill.py`: packages the entire skill as a shareable zip

Run these from the target project root unless explicit paths are provided.

## Controls

Common target-repo control files:

- `workflow.md`: working method and pass order
- `controls/validation-checklist.md`: release and editing gate
- `controls/term-sheet.md`: stable terminology
- `controls/references.bib`: optional mirror if the target repo stores bibliography controls outside `report-body/`

Mirrored bundle references:

- `references/workflow.md`
- `references/validation-checklist.md`
- `references/term-sheet.md`

## Tracking templates

- target repo: usually `tracking/*.md`
- bundle copies: `assets/tracking-templates/*.md`
- editable diagram config: `assets/mermaid/mermaid-config.json`

## Typical flow

1. Create the tracking set.
2. Process sources and keep the review notebook current.
3. Promote stable items into the findings workbook.
4. Draft or revise `report-body/`.
5. Render or refresh Mermaid-derived media in `report-body/media/`.
6. Assemble.
7. Export the packaged document if needed.
8. Run the validation and prose passes.

## Handoff note

The packaged output should travel with the working markdown, tracking files, bibliography, and media assets. The bundle is not complete if only the final document survives.
