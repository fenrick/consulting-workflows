# Document Workflow

## Purpose

This file describes the working method for assembling a high-quality document from mixed source material. It covers whole-document flow, section-level drafting, evidence control, tooling, and release preparation.

Use this process unless the user gives a better one.

If the target project does not already use the same directories as this bundle, adapt the path names once at setup and keep them stable through the rest of the work.

Treat markdown plus tracking files as the default authoring surface. Binary office formats are packaging or inspection outputs unless the user explicitly asks for direct editing in those formats.

Treat code and generator scripts as tooling only. Canonical document content should remain in markdown working files and tracking files, not buried in program source.

When using the bundled scripts from a shared skill install, run them from the target project root or pass explicit paths. Do not compensate for a bad working directory by moving document prose into code.

Source-reading helpers such as spreadsheet, PDF, or document-format tools may be used to inspect inputs. They do not become the authoring workflow. Their output should be notes, extracted facts, or validation results that feed back into markdown drafting.

## Working files

- `tracking/document-brief.md`
- `tracking/source-register.md`
- `tracking/section-status.md`
- `tracking/decision-log.md`
- `tracking/open-questions.md`
- `tracking/editorial-pass.md`
- `tracking/release-check.md`
- `tracking/review-notebook.md`
- `tracking/findings-workbook.md`
- `report-body/`
- `full/`

## Operating sequence

### 1. Start the document

Before drafting, establish the operating frame.

Create or update:

- a document brief
- a source register
- a section status tracker
- a decision log
- an open questions list
- an editorial pass log
- a title block with a real title and subtitle

For substantial documents, also scaffold:

- an executive summary
- an introduction

For review, audit, or assessment-style documents, also create:

- a findings workbook
- a review notebook for running observations, insights, and emerging findings while sources are being processed

Use the tracking templates from the target project or from `assets/tracking-templates/`.

Create the title block from `assets/title-block-template.md` if the target project does not already have one.
Create the front end from `assets/front-end-outline-template.md` if the target project does not already have one.

If the target project is being started from scratch, prefer:

```bash
python3 scripts/scaffold_document.py
```

Record:

- document purpose
- intended audience
- required voice
- likely output format
- source hierarchy
- hard constraints
- current phase

Do not carry placeholder title or subtitle text beyond the scaffolding step.

### 2. Intake and classify sources

Do not start writing until the source base is mapped.

For each source, record:

- file name
- source type
- role: primary, supporting, or contextual
- status: unread, indexed, reviewed, or verified for citation
- how it may be used
- any limits or format issues

When there are multiple versions of the same source:

- identify the current lead version
- keep earlier versions for baseline wording or change tracking only
- note any format substitutions such as PDF replacing PPTX

While processing sources, also update the review notebook with:

- observations worth keeping even if they are not yet findings
- insights that connect multiple sources
- tentative findings with confidence notes
- open questions or verification tasks triggered by the source

Do not force later passes to rediscover important patterns from first sources if they can be preserved cleanly during intake.

If a source helper is used here, promote what it finds into the source register and review notebook. Do not leave important observations stranded in a tool transcript or script output.

### 3. Set the writing frame

Before editing the body, lock these items:

- document purpose in one sentence
- what the document is not
- stable terms
- section order
- expected finding structure
- citation method

Default citation contract:

- APA v7 bibliography formatting
- Pandoc/Writage in-text citations such as `[@key]`
- no manual markdown footnote citations unless the user explicitly asks for them

For review-style documents, the document should read as a baseline that informs later decisions, not as a disguised recommendation paper.

If the audience includes non-specialists:

- state clearly what the system, proposal, or process is
- state clearly what it is not
- identify the main user or stakeholder groups visible in the evidence
- put this orientation before dense findings

### 4. Build or confirm the structure

Check that the structure serves the story before refining sentences.

At document level:

- front end should state purpose, scope, method, and organising logic early
- front end should normally include an executive summary and an introduction for any substantial document
- for review documents with several user types or trust boundaries, add an early orientation section and at least one overview figure
- body sections should each have a clear job
- comparative or market material should be bounded
- closing sections should separate decisions from delivery planning where relevant
- the evidence section should act as a real reviewed-source register

For architecture, codebase, or system-review documents aimed at mixed audiences, the usual shape should include:

- what the system is and is not
- user or operating flows reconstructed from evidence where formal documentation is missing
- the main findings in narrative form
- an appendix findings register with rating, impact, consequence, and evidence

At section level:

- start with a clear opener
- group related material together
- land the section point explicitly
- make sure headings match the current organising frame

The number and naming of sections should follow the document, not this template. The only hard contract is ordered `NN - Title.md` files for assembly.

### 5. Draft a section

### Step 1: gather the inputs

For the section in scope:

- list the primary sources
- list the supporting sources
- identify any figures used
- check the term sheet
- note any known factual gaps

### Step 2: write the opener

The opener should do three things:

- orient the reader
- state what kind of pressure, topic, or pattern the section covers
- explain why it matters in practice

If the opener sounds like slide commentary, rewrite it.

### Step 3: draft the content blocks the section needs

For each content block:

1. state the pattern plainly
2. explain where it appears
3. explain why it matters
4. keep examples grounded
5. avoid drifting into solution design

### Step 4: land the section close

The section close should:

- name what must be protected
- name what needs to change
- state the improvement focus in plain language

If the close only repeats the body text, it is too weak.

### 6. Handle figures properly

Every figure must earn its place.

Treat figure format as a delivery risk, not only a design choice.

If the figure starts as Mermaid:

- keep the editable `.mmd` source in `report-body/diagrams/` or an equivalent tracked path
- use the bundled ELK-based neutral config unless the document has a stronger visual requirement
- render a high-resolution PNG for embedding with `python3 scripts/render_mermaid.py`
- expect the export path to place Mermaid figures at a controlled document width rather than stretching every figure to full page width
- keep the SVG output if future editing is likely
- record the render path in the editorial pass log if someone else will package the document

When the output may pass through Writage or Word:

- do not rely on SVG alone
- keep the editable source if useful, for example SVG
- also export a PNG fallback beside it
- reference the PNG in markdown unless the user explicitly wants the SVG path
- record any media-format limitation in the editorial log if it affects delivery

Before a figure:

- say what it shows
- say why it matters
- translate technical or model-heavy content for non-specialist readers
- include a caption

After a figure:

- connect it back to the section logic
- avoid leaving the image to speak for itself

For tables:

- include a caption
- keep headings and units explicit
- explain the point of the table in the surrounding prose

If a figure is impressive but not useful, cut it.

If a figure is reconstructed from code or other evidence rather than copied from an existing document:

- say that directly in the body
- keep the diagram simpler than the source material
- explain what the non-specialist reader should notice

### 7. Keep terminology stable

Use `controls/term-sheet.md`.

During each pass:

- search for drift terms
- standardise repeated concepts
- check headings, body text, captions, and summary sections together

Do not rewrite a stable term just because it has appeared twice already. That is how drift starts.

### 8. Keep the comparative section in bounds

Comparative material should:

- provide context
- test assumptions
- show what other arrangements are possible

It should not:

- take over the report
- pretend to describe the current state directly
- read like a separate market report
- quietly become a recommendation in disguise

Keep it selective. Judgment matters more than breadth.

## Back-iteration loop

### 9. Run the editing passes in the right order

Use this sequence:

1. structure pass
2. evidence pass
3. terminology pass
4. voice and sentence pass
5. figure and caption pass
6. references pass
7. final assembled read-through

Do not spend time polishing sentences inside a broken structure.

For substantial work, run these passes as a loop, not a single sweep:

1. skeleton draft
2. bullet points
3. paragraphs
4. narrative flow pass
5. humanise the awkward machine phrasing
6. restore neutral voice and simple language
7. run the humaniser again
8. read the whole document in sequence
9. repeat until the flow holds together cleanly and the latest humaniser pass makes only trivial changes

The loop matters because a document that reads well section by section can still fail once read end to end.

### 10. Assemble the combined draft

When the split sections are ready, assemble the combined output:

```bash
python3 scripts/assemble_report.py
```

Useful variants:

```bash
python3 scripts/assemble_report.py --source-dir report-body --output-file "full/output.md"
python3 scripts/assemble_report.py --skip-media
python3 scripts/assemble_report.py --skip-bibliography
```

If the project has assembly regression tests, run them after changes to assembly behaviour.

Check:

- heading order
- title block
- title and subtitle are real, not template placeholders
- executive summary and introduction are present for substantial documents
- table of contents will be generated from level 1 headings for substantial documents unless deliberately disabled
- title, executive summary, table of contents, introduction, and body appear in that order in the exported document
- copied media
- copied bibliography
- obvious duplicate spacing or truncated sections

If packaged document output is required, prefer the Pandoc path:

```bash
python3 scripts/export_docx.py --assemble
```

Useful variants:

```bash
python3 scripts/export_docx.py --input full/combined-report.md --output full/report
python3 scripts/export_docx.py --reference-doc assets/reference.docx
python3 scripts/export_docx.py --no-citeproc
python3 scripts/export_docx.py --no-toc
```

Defaults:

- input: `full/combined-report.md`
- output: packaged document in the output directory
- reference doc: `assets/reference.docx`
- bibliography: assembled bibliography if present, otherwise the source bibliography
- table of contents: generated from level 1 headings unless deliberately disabled
- Mermaid fenced blocks with `<!-- FigureCaption: ... -->` comments are preprocessed into embedded PNG figures with styled `ImageCaption` paragraphs

If Pandoc or the reference doc is missing, stop and fix the toolchain rather than improvising a less repeatable path.

Do not switch to direct binary-document authoring here unless the user explicitly asked for it or the layout must be controlled in that format from the start.

If another export path is used, it must consume the canonical markdown draft. Do not migrate the document body into a Node, Python, or template generator just to produce the final file.

For local-only export tuning:

- it is acceptable to keep disposable comparison files under `tests/` while tuning the export path
- treat those files as local fixtures, not portfolio assets
- compare generated output against the local fixture and then keep only the code changes, not the fixture itself
- do not commit ad hoc fixture documents, generated DOCX files, or borrowed reference artifacts unless they have been deliberately curated for the repo

### 11. References and evidence register pass

Before release:

- populate the active bibliography file for any document-backed statement that uses Pandoc citations
- confirm every in-text citation resolves
- remove orphaned bibliography entries that are no longer cited unless the section is a reviewed-source register
- normalise titles and identifiers
- format bibliography entries to APA v7 unless the user explicitly requested a different style
- distinguish reviewed documents from sampled or indexed material
- make sure comparative context is not presented as direct evidence
- update the release checklist if one is being used

Code-specific implementation evidence may still be cited directly in prose by file and line reference when that is clearer than a bibliography citation.

### 12. Final voice pass

Use the strongest plain-language sections as the benchmark for the weakest sections.

Check for:

- abstract nouns piling up
- over-authored transitions
- sentence density
- advisory or strategic tone where the document should stay descriptive
- inconsistent framing between the front end and later sections

Run the `humanizer` skill as repeated final checks, not one token pass. Keep the document voice; remove the machine habits.

Minimum release expectation:

- run the humaniser at least twice on substantial documentation
- review the output after each pass
- stop only when the next pass would make trivial or no meaningful changes

### 13. Use skills deliberately

Use the smallest relevant skill set for the task. In environments that provide companion skills, the usual choices are:

- `humanizer` for the final prose-quality pass on every substantial document change
- `humanizer` should usually be run multiple times near release rather than once
- `doc` when packaged document output, Writage behaviour, or layout fidelity matters after the content workflow is already in place
- `pdf` when PDF rendering, pagination, or extraction fidelity matters
- `slides` when building or editing editable diagrams, figures, or presentation assets
- `spreadsheet` when findings registers, evidence logs, or tabular appendices need stronger structure than markdown alone

If a document relies on exported media or office formats, record the tool path used in the editorial log.

Do not hand control of the document workflow to a format-specific helper just because the final deliverable is a packaged document or PDF file.

Do not let a code generator become the hidden canonical source of the document.

Do not let a spreadsheet helper become the hidden planner of the document either. Source extraction is upstream of writing, not a substitute for it.

### 14. Commit and branch discipline

When a major pass is complete:

- commit the coherent set of changes
- use a message that says what changed in substance
- if the user asks to commit all changes, stage the full dirty tree unless there is a clear reason not to

When resetting the repo for a new document stream:

- create a new branch first
- preserve generic tooling and process docs
- remove document-specific content deliberately
- replace it with reusable templates rather than leaving gaps

## Handoff and closure

### 15. Minimum release gate

The document is not ready until:

- the front end states purpose, scope, and organising logic clearly
- section labels and findings are stable
- evidence claims are traceable
- figures are explained in plain language
- references resolve
- the assembled output reads cleanly in order
- the remaining open questions are explicit
- the packaged output travels with the working markdown and tracking files
