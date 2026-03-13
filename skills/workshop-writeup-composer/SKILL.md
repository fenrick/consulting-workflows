---
name: workshop-writeup-composer
description: Use when converting workshop transcripts and workshop input/output artifacts into a formal, consistent workshop write-up that captures context, participants, discussion signals, decisions, outputs, and agreed next steps.
---

# Workshop Writeup Composer

Use this skill for formal workshop reporting from explicit workshop materials.

## Bundled materials

Read in this order:

1. `references/workflow.md`
2. `references/validation-checklist.md`
3. `references/quality-standard.md`
4. `references/term-sheet.md`
5. `references/repo-map.md`
6. `references/tracking-readme.md`
7. `assets/templates/workshop-writeup-template.md`
8. `assets/templates/workshop-evidence-map-template.md`
9. `assets/templates/open-questions-template.md`
10. `assets/templates/decision-log-template.md`

## Inputs

- workshop transcript(s)
- workshop pre-reads and briefing materials
- workshop outputs (boards, notes, actions, artifacts)
- participant list and workshop metadata if available

## Core outcome

Produce a formal workshop write-up with traceable evidence from transcript and artifacts.

## Required outputs

1. `tracking/workshop-writeup.md`
2. `tracking/workshop-evidence-map.md`
3. `tracking/open-questions.md` updates for unresolved workshop points
4. `tracking/decision-log.md` updates for confirmed workshop decisions

## Write-up contract

`tracking/workshop-writeup.md` should include:

1. workshop purpose and scope
2. participants and roles (if known)
3. agenda and session structure
4. key discussion points by theme
5. decisions made
6. outputs produced
7. action items with owners and time signals where available
8. unresolved issues and follow-up requirements

## Quality gate

Apply `references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep write-up content in `tracking/workshop-writeup.md`
- keep transcript/artifact traceability in `tracking/workshop-evidence-map.md`
- keep unresolved workshop points in `tracking/open-questions.md`
- build the artifact through skeleton, evidence bullets, short paragraphs, and flow passes

## Back-iteration loop

1. draft write-up from transcript and artifacts
2. re-check decisions, outputs, and actions against source evidence
3. reconcile conflicts across session artifacts
4. refresh outputs and unresolved items before handoff

## Do not

- infer decisions not present in transcript or artifacts
- omit dissent or unresolved points
- collapse separate workshop sessions without clear labeling
