---
name: evidence-consistency-auditor
description: Use when validating claim consistency across briefs, source catalogs, storylines, and draft skeletons by detecting contradictions, supersession issues, weak support, and unresolved evidence gaps before drafting or release.
---

# Evidence Consistency Auditor

Use this skill after intake and before full drafting to harden factual integrity.

## Bundled materials

Read in this order:

1. `references/workflow.md`
2. `references/validation-checklist.md`
3. `references/quality-standard.md`
4. `references/term-sheet.md`
5. `references/repo-map.md`
6. `references/tracking-readme.md`
7. `assets/templates/evidence-consistency-report-template.md`
8. `assets/templates/open-questions-template.md`
9. `assets/templates/decision-log-template.md`

## Inputs

- `tracking/source-register.md`
- `tracking/review-notebook.md`
- `tracking/storyline-architecture.md` if available
- `tracking/report-storyboard.md` or `tracking/presentation-storyboard.md` if available
- key processed inputs referenced by claims

## Core outcome

Produce a consistency audit that identifies contradictions, stale references, and weakly supported claims.

## Required outputs

1. `tracking/evidence-consistency-report.md`
2. `tracking/open-questions.md` updates for unresolved claim checks
3. `tracking/decision-log.md` updates for accepted risk decisions

## Audit checks

- claim-to-source traceability
- source supersession validity
- contradictory statements across artifacts
- unsupported or weakly supported claims
- version/date mismatch risks

## Quality gate

Apply `references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep audit findings in `tracking/evidence-consistency-report.md`
- keep unresolved contradictions in `tracking/open-questions.md`
- keep accepted residual risks in `tracking/decision-log.md`
- build findings from issue skeleton to evidence bullets to short prose summary

## Back-iteration loop

1. run first-pass consistency audit
2. re-check after storyline/storyboard revisions
3. confirm contradictions are resolved or explicitly risk-accepted
4. refresh outputs and unresolved items before handoff

## Do not

- rewrite storyline content without recording rationale
- silently drop contradictory evidence
- treat unresolved gaps as resolved
