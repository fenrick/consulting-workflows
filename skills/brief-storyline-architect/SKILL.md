---
name: brief-storyline-architect
description: Use when converting a project brief plus evidence inputs into a consulting-grade storyline structure, including governing question, top-level argument, section logic, evidence requirements, and unresolved proof gaps.
---

# Brief Storyline Architect

Use this skill to produce a BCG/McKinsey-style narrative backbone before authoring.

## Bundled materials

- `references/workflow.md`
- `references/quality-standard.md`
- `assets/templates/storyline-architecture-template.md`
- `assets/templates/open-questions-template.md`
- `assets/templates/decision-log-template.md`

## Inputs

- project brief (`tracking/document-brief.md` or equivalent)
- evidence catalog outputs from `input-evidence-cataloger`
- key source materials in `inputs/processed/`

## Core outcome

Produce a top-down storyline that is testable against evidence.

## Required outputs

1. `tracking/storyline-architecture.md`
2. `tracking/open-questions.md` updates for proof gaps
3. `tracking/decision-log.md` entries for major storyline choices

## Quality gate

Apply `references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep storyline state in `tracking/storyline-architecture.md`
- keep unresolved proof gaps in `tracking/open-questions.md`
- keep storyline judgment calls in `tracking/decision-log.md`

## Back-iteration loop

1. draft initial storyline pillars and support logic
2. challenge each claim against evidence coverage
3. revise storyline for weak logic or overlap
4. update outputs and unresolved items before handoff

## Storyline contract

`tracking/storyline-architecture.md` should contain:

1. governing question
2. audience and decision context
3. top-level answer
4. 3-7 storyline pillars with one-sentence claims
5. section-level support logic per pillar
6. required evidence per claim
7. risk and objection handling notes
8. unresolved issues and next validation steps

## Quality rules

- Claims must be falsifiable and evidence-bound.
- No section should exist without a clear decision or implication purpose.
- Separate what is known, inferred, and unknown.
- Keep the storyline concise enough to fit on one review page before expansion.

## Do not

- jump into full prose drafting
- treat weakly supported claims as settled
- bury unresolved proof gaps
