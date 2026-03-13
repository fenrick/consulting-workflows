# Bundle Map for the Document Writer Skill

This is the default layout the bundled scripts expect.

If the target repo uses different directories, adapt the paths once and keep them consistent.

## Main working surfaces

- `report-body/`: canonical split draft
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
- `scripts/scaffold_document.py`: creates the baseline title block, front-end section files, and tracking files
- `scripts/package_skill.py`: packages the entire skill as a shareable zip

Run the first two from the target project root unless explicit paths are provided.

## Controls

Common target-repo control files:

- `workflow.md`: working method and pass order
- `controls/validation-checklist.md`: release and editing gate
- `controls/term-sheet.md`: stable terminology

Mirrored bundle references:

- `references/workflow.md`
- `references/validation-checklist.md`
- `references/term-sheet.md`

## Tracking templates

- target repo: usually `tracking/*.md`
- bundle copies: `assets/tracking-templates/*.md`

## Typical flow

1. Create the tracking set.
2. Process sources and keep the review notebook current.
3. Promote stable items into the findings workbook.
4. Draft or revise `report-body/`.
5. Assemble.
6. Export the packaged document if needed.
7. Run the validation and prose passes.

## Portability notes

- `SKILL.md` is the portable contract.
- `agents/openai.yaml` is optional adapter metadata for hosts that support it.
- The archive created by `scripts/package_skill.py` is the clean handoff unit for other services or coworkers.
- The bundled scripts should consume project markdown and tracking files, not become the place where the writing lives.
