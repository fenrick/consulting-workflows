---
name: document-writer
description: Use when building substantial evidence-led documents from mixed source material through a markdown-first, tracked drafting workflow, especially reviews, architecture reports, audits, and assessment writing. Use it for document workflow ownership, not just because the final deliverable may need packaged file output.
---

# Document Writer

This skill packages a disciplined, markdown-first document-writing workflow for substantial reports built from mixed source material.

The portable contract is this folder plus `SKILL.md`. The `agents/` directory is optional host metadata. Ignore it on platforms that do not use it.

The bundle works best in document projects that use split markdown drafts, tracked review state, and optional document export at the end, but it carries its own scripts, reference document, and tracking templates so it can be shared as a standalone skill.

## When to use

Use this skill when the task involves any of the following:

- building a substantial report from mixed source material
- running a tracked document workflow rather than a one-off edit
- writing architecture, security, review, audit, or assessment documents
- maintaining split markdown sections in an ordered source directory
- managing source intake, findings tracking, and editorial passes
- exporting the assembled report via Pandoc

Do not trigger this skill only because someone asked for a packaged file. Trigger it when the task needs the writing workflow itself.

The workflow requires a real title and subtitle before assembly or export. Placeholder front matter is for scaffolding only.

Portfolio quality gate:

- apply `skills/consulting-workflows/references/quality-standard.md`

## Working materials discipline

- keep canonical prose in markdown working files
- keep evidence and judgment state in tracking files
- keep handoff artifacts synchronized with assembled and packaged outputs

For substantial documents, the front end should also include:

- an executive summary
- an introduction
- a generated table of contents from level 1 headings unless deliberately disabled

## Dispatch rules

Treat this skill as the primary workflow owner for document creation.

Default authoring surface:

- tracking files plus markdown source sections

Packaging and inspection surfaces:

- document export for delivery or layout inspection
- PDF for rendering and pagination checks

Do not jump straight into direct binary-document authoring just because packaged output is one possible deliverable.

Only make a document-format or PDF helper the primary path when one of these is true:

- the user explicitly asks for direct editing of an existing binary document
- the user explicitly wants the document authored directly in a binary document format
- layout fidelity must be managed in the binary file from the start

Otherwise:

- write and review the content in the tracked markdown workflow first
- assemble the combined draft
- export to a packaged document or PDF at the end

Tool precedence:

- spreadsheet helpers may inspect or extract source material
- document-format helpers may inspect, validate, or package the final output
- this skill still owns the writing workflow and canonical document body

If a spreadsheet, PDF, or document-format helper is used, it should hand structured notes back into the markdown workflow rather than taking over authorship.

Canonical content location:

- document prose lives in markdown working files
- findings and observations live in tracking files
- scripts may transform, assemble, export, or validate content

Scripts are not an authoring surface for substantive document prose.

Do not embed the report body, section text, or large narrative blocks inside Node, Python, or other generator scripts.

## Portable bundle shape

The portable parts of this skill are:

- `SKILL.md`
- `scripts/`
- `assets/`
- `references/`

Optional adapter metadata:

- `agents/openai.yaml`

If the host platform supports plain skill folders with `SKILL.md`, this bundle is enough. If the host platform supports extra metadata, keep the adapter files as a thin layer around the same core bundle.

## Project setup

Before starting, map the target project to these working surfaces:

- source sections directory
- source media directory
- source bibliography file
- assembled output directory
- tracking directory
- reference document path

The bundle scripts assume the default layout used by this skill:

- source sections: `report-body/`
- source media: `report-body/media/`
- source bibliography: `report-body/references.bib`
- assembled output: `full/`
- tracking files: `tracking/`
- reference document: `assets/reference.docx`
- title block template: `assets/title-block-template.md`
- front-end outline template: `assets/front-end-outline-template.md`

If the target project uses different paths, adapt them once at setup and keep them stable for the rest of the document stream.

## Script execution rules

Run the bundled scripts from the target project root unless you pass explicit paths.

That means:

- `assemble_report.py` should see the target project's source sections and output directories from the current working directory
- `export_docx.py` should read the target project's assembled markdown and bibliography from the current working directory
- `scaffold_document.py` should create the baseline working files in the target project before drafting starts

Do not work around path problems by moving the writing into code, templates, or generator scripts.

## Core workflow

1. Read the bundled guidance first:
   - `references/workflow.md`
   - `references/validation-checklist.md`
   - `references/term-sheet.md`
2. Scaffold the working files with:
   - `python3 scripts/scaffold_document.py`
3. Replace the placeholder title and subtitle immediately.
4. For review-style work, make sure the scaffolded review notebook and findings workbook are kept current.
5. Draft in the source sections directory, not in the assembled output directory.
6. Assemble the combined draft with:
   - `python3 scripts/assemble_report.py`
7. If packaged document output is needed, export with:
   - `python3 scripts/export_docx.py --assemble --reference-doc assets/reference.docx`
8. Run the validation pass and finish with a prose-quality pass.
9. At handoff, share the working files and the packaged output together.

If another host skill or tool offers document generation, use it only as a downstream packaging or inspection step unless the user explicitly asked for direct binary-document authoring.

If a generator script is used for delivery, it must read from the canonical markdown content rather than becoming the place where the writing actually lives.

Concrete anti-pattern:

- read a spreadsheet with a spreadsheet helper
- create markdown notes
- then generate the actual document body inside a Node or Python document-generation script

That is not compliant with this workflow. The document body must stay in markdown working files.

## Drafting loop

Use this loop for substantial documents:

1. build a skeleton draft
2. flesh out the evidence, reasoning, and section landings
3. rewrite for flow and coherence
4. run a prose-quality or humanizing pass
5. check the whole document flow again
6. repeat until the document reads cleanly in sequence

Do not treat one linear drafting pass as enough for serious work.

Checks for each loop:

- the structure still matches the document purpose
- paragraphs land one point at a time
- transitions are earned rather than padded
- headings still match the actual content
- the tone sounds like a careful human writer, not generated filler

## Tracking set to create

Always start with:

- document brief
- source register
- section status tracker
- decision log
- open questions log
- editorial pass log
- release check

For review, audit, and assessment work, also create:

- review notebook
- findings workbook

Use the bundled templates from `assets/tracking-templates/` unless the target project already has established equivalents.

Create the title block from `assets/title-block-template.md` and replace both placeholder lines before the first assembled draft.

For substantial documents, scaffold the front end from `assets/front-end-outline-template.md` before writing the body sections.

## What the review notebook is for

The review notebook is the running memory of source processing.

Use it to capture:

- observations
- cross-source insights
- tentative findings
- follow-up checks

Do not wait until the writing pass to preserve those notes. The point is to avoid having to rediscover patterns from first sources.

## Media and document export rules

- Keep editable figure sources when useful.
- If Writage or Word is in the delivery path, do not rely on SVG alone.
- Create PNG fallbacks beside SVGs.
- Prefer the PNG reference in markdown unless the user wants otherwise.
- Keep the Pandoc reference document at `assets/reference.docx`.
- Ensure `rsvg-convert` is on `PATH` if SVG conversion is expected during Pandoc export.

Pandoc document export defaults:

- input: assembled markdown file in the output directory
- output: packaged document in the output directory
- reference doc: `assets/reference.docx` unless the project supplies a different one
- bibliography: assembled bibliography file if present, otherwise the source bibliography file
- table of contents: generated from level 1 headings unless deliberately disabled

## Companion capabilities

Use the smallest relevant set the host environment provides:

- prose cleanup or style-scrub capability for the final prose pass
- document-format editing or inspection capability when delivery fidelity matters
- PDF rendering or inspection capability when pagination matters
- slide or diagram tooling when building editable visuals
- spreadsheet tooling when findings or evidence registers are easier to manage in structured tables first

Examples in Codex environments are `humanizer`, `doc`, `pdf`, `slides`, and `spreadsheet`. These are examples, not hard dependencies.

## Bundled resources

- `scripts/assemble_report.py`
- `scripts/export_docx.py`
- `scripts/scaffold_document.py`
- `scripts/package_skill.py`
- `assets/reference.docx`
- `assets/title-block-template.md`
- `assets/front-end-outline-template.md`
- `assets/tracking-templates/`

## References to read as needed

- `references/workflow.md`
- `references/validation-checklist.md`
- `references/term-sheet.md`
- `references/tracking-readme.md`
- `references/repo-map.md`

## Packaging

To create a shareable archive of the skill folder:

- `python3 scripts/package_skill.py`

Optional output path:

- `python3 scripts/package_skill.py --output /tmp/document-writer-skill.zip`

## Delivery rule

Do not share only the packaged output.

Share together:

- the markdown working files
- the tracking files
- the assembled draft
- the packaged output

## Do not

- draft substantial prose only in chat
- let the report become the only place findings exist
- rely on manual Word import when a repeatable Pandoc path is available
- assume the audience is technical if the user has not said so
- put canonical document prose into generator code
- hide substantive content inside Node, Python, or template scripts
- run the bundled scripts from the wrong working directory and then compensate by bypassing the markdown workflow
- let spreadsheet or Word helper skills take over authorship after source inspection
