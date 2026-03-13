---
name: presentation-storyboard-builder
description: Use when transforming a validated storyline and evidence inputs into a presentation storyboard, including slide-by-slide purpose, key message, evidence payload, and narrative flow for executive review.
---

# Presentation Storyboard Builder

Use this skill to create a slide skeleton before deck production.

## Inputs

- `tracking/storyline-architecture.md`
- `tracking/source-register.md`
- `tracking/review-notebook.md`
- project brief and key processed inputs

## Core outcome

Produce a presentation storyboard that maps narrative flow and slide intent.

## Required outputs

1. `tracking/presentation-storyboard.md`
2. slide map with numbered sequence and transition logic
3. `tracking/open-questions.md` updates for unsupported slides

## Quality gate

Apply `skills/consulting-workflows/references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep slide logic in `tracking/presentation-storyboard.md`
- keep unsupported slide claims in `tracking/open-questions.md`
- keep narrative tradeoffs explicit in slide notes

## Back-iteration loop

1. draft slide sequence and messages
2. test each slide claim against available evidence
3. remove weak or redundant slides and tighten transitions
4. refresh outputs and unresolved items before handoff

## Storyboard contract

For each slide:

- slide number and working title
- audience takeaway in one sentence
- evidence payload (data, quote, diagram, case, or decision prompt)
- presenter note (why this slide exists)
- transition from previous slide
- risk or objection note if relevant

Include:

- opening sequence (context and objective)
- middle sequence (analysis and implications)
- closing sequence (decision points and next steps)

## Quality rules

- One core message per slide.
- Evidence must match the message claim.
- Flow should support an executive skim and a deep read.
- Avoid slide duplication between sections unless the audience differs.

## Do not

- produce visual design assets at this stage
- write dense report prose into slide bullets
- keep slides that do not advance the storyline
