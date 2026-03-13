---
name: input-evidence-cataloger
description: Use when cataloging and parsing mixed input documents into a factual evidence inventory, including provenance, authorship/date signals, format/version relationships, supersession checks, archive/folder maps, and high-confidence content statements with explicit unknowns.
---

# Input Evidence Cataloger

Use this skill for intake and initial content discovery before storyline or drafting work.

## Bundled materials

- `references/workflow.md`
- `references/quality-standard.md`
- `assets/templates/source-register-template.md`
- `assets/templates/review-notebook-template.md`
- `assets/templates/open-questions-template.md`
- `assets/templates/document-map-template.md`

## Core outcome

Produce a high-quality evidence catalog with:

- source inventory
- archive or folder document map
- factual statements from each source
- provenance and metadata signals
- supersession and version relationships
- open questions for unresolved facts

## Required outputs

1. `tracking/source-register.md` with one row per source
2. `tracking/review-notebook.md` with factual statement extraction and confidence tags
3. `tracking/open-questions.md` with missing provenance or conflicting evidence
4. `inputs/processed/document-map.md` for zip/folder structure and replacement relationships

## Quality gate

Apply `references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep extracted statements in `tracking/review-notebook.md`
- keep provenance and version metadata in `tracking/source-register.md`
- keep uncertainties in `tracking/open-questions.md`

## Back-iteration loop

1. run initial extraction and cataloging
2. re-check supersession and provenance after full inventory
3. reconcile contradictions and refresh factual statements
4. update outputs and unresolved items before handoff

## Parsing rules

- Prefer direct extraction over inference.
- Separate facts from assumptions.
- Mark source confidence and ambiguity explicitly.
- If author/date are unavailable, mark as unknown and record where you looked.
- If a file appears superseded, record both files and the replacement rationale.
- For archives, map internal paths and classify each file role.

## Suggested sequence

1. inventory all files under `inputs/`
2. classify by format and evidence role
3. extract machine-readable text where possible
4. map archive/folder structures
5. generate factual statements per document
6. detect supersession chains and unresolved conflicts
7. publish the four required outputs

## Do not

- write recommendations during intake
- hide uncertainty
- collapse multiple source versions into one without traceability
- treat contextual files as controlled evidence unless explicitly confirmed
