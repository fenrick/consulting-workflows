---
name: report-storyboard-builder
description: Use when transforming a validated storyline and evidence inputs into a written-report storyboard, including section skeleton, section intent, proof obligations, evidence hooks, and drafting order.
---

# Report Storyboard Builder

Use this skill to create the written report skeleton before detailed prose.

## Inputs

- `tracking/storyline-architecture.md`
- `tracking/source-register.md`
- `tracking/review-notebook.md`
- project brief and key processed inputs

## Core outcome

Produce a report storyboard that tells writers exactly what each section must do.

## Required outputs

1. `tracking/report-storyboard.md`
2. section file plan for `report-body/` (ordered list with expected file names)
3. `tracking/open-questions.md` updates for sections lacking evidence

## Quality gate

Apply `skills/consulting-workflows/references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep section logic in `tracking/report-storyboard.md`
- keep unresolved evidence gaps in `tracking/open-questions.md`
- keep assumptions explicit in section-level notes

## Back-iteration loop

1. build first-pass section storyboard
2. check section claims against storyline and source register
3. tighten overlaps, remove orphan sections, and re-sequence
4. refresh outputs and unresolved items before handoff

## Storyboard contract

For each planned section:

- section title
- section purpose
- key claim(s)
- required evidence
- practical implication
- what not to include
- dependencies on other sections

Include:

- recommended drafting order
- minimum front-end requirements (executive summary, introduction)
- appendix candidates and rationale

## Quality rules

- Keep sections decision-relevant and non-overlapping.
- Tie each section to at least one evidence source or explicit evidence gap.
- Prevent orphan sections that cannot be proven from current inputs.

## Do not

- write full polished prose
- create section headings without a proof obligation
- duplicate storyline content without adaptation for written narrative
