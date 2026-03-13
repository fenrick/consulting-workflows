---
name: consulting-workflow-orchestrator
description: Use when coordinating the full consulting workflow across intake, storyline, report storyboard, presentation storyboard, and drafting skills with explicit handoffs, quality gates, and unresolved-item tracking.
---

# Consulting Workflow Orchestrator

Use this skill to run the multi-skill process end-to-end with deterministic handoffs.

## Bundled materials

Read in this order:

1. `references/workflow.md`
2. `references/validation-checklist.md`
3. `references/quality-standard.md`
4. `references/term-sheet.md`
5. `references/repo-map.md`
6. `references/tracking-readme.md`
7. `assets/templates/workflow-runbook-template.md`
8. `assets/templates/workflow-status-template.md`

## Pipeline order

1. `input-evidence-cataloger`
2. `evidence-consistency-auditor`
3. `brief-storyline-architect`
4. `report-storyboard-builder`
5. `presentation-storyboard-builder`
6. `workshop-writeup-composer` (variant path for workshop-heavy engagements)
7. `document-writer` (canonical skill at `skills/document-writer`)

## Orchestration outputs

1. `tracking/workflow-runbook.md`
2. `tracking/workflow-status.md`
3. handoff readiness checks per stage

## Stage gate contract

Do not advance a stage unless:

- required outputs for current stage exist
- unresolved items are logged in `tracking/open-questions.md`
- material decisions are logged in `tracking/decision-log.md`
- quality checks in `references/quality-standard.md` are met

For workshop-heavy engagements:

- run `workshop-writeup-composer` before storyline/storyboard stages if workshop outcomes are primary evidence

## Working materials discipline

- keep orchestration state in `tracking/workflow-runbook.md` and `tracking/workflow-status.md`
- enforce updates to `tracking/open-questions.md` and `tracking/decision-log.md` at each gate
- block progression if declared outputs are missing
- treat the runbook as the source of truth for workflow state

## Back-iteration loop

1. run a forward pass through stage gates
2. run a backward quality pass from drafting to intake
3. reopen blocked stages if new contradictions or gaps are found
4. close only when all stage gates are `ready`

## Runbook format

For each stage in `tracking/workflow-runbook.md`:

- objective
- required inputs
- outputs produced
- blockers
- handoff readiness (`ready` or `blocked`)

## Do not

- skip intake
- draft prose before storyline validation
- bypass stage-gate checks
- leave stage decisions only in chat text
