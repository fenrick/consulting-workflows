---
name: workshop-writeup-composer
description: Use when converting workshop transcripts and workshop input/output artifacts into a formal, consistent workshop write-up that captures context, participants, discussion signals, decisions, outputs, and agreed next steps.
---

# Workshop Writeup Composer

Use this skill for formal workshop reporting from explicit workshop materials.

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

Apply `skills/consulting-workflows/references/quality-standard.md` before finalizing outputs.

## Working materials discipline

- keep write-up content in `tracking/workshop-writeup.md`
- keep transcript/artifact traceability in `tracking/workshop-evidence-map.md`
- keep unresolved workshop points in `tracking/open-questions.md`

## Back-iteration loop

1. draft write-up from transcript and artifacts
2. re-check decisions, outputs, and actions against source evidence
3. reconcile conflicts across session artifacts
4. refresh outputs and unresolved items before handoff

## Do not

- infer decisions not present in transcript or artifacts
- omit dissent or unresolved points
- collapse separate workshop sessions without clear labeling
