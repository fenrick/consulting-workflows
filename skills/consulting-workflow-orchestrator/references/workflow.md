# Consulting Workflow Orchestrator Workflow

## Purpose

This workflow coordinates the full consulting skill chain without letting stages blur together.

The orchestrator owns sequence, gate enforcement, blocker visibility, and back-iteration.

## When to use this workflow

Use it when the job spans multiple skills and the risk is loss of control between stages.

Do not use it for one-off isolated skill runs that do not require stage gating.

## Working files

- `tracking/workflow-runbook.md`
- `tracking/workflow-status.md`
- `tracking/open-questions.md`
- `tracking/decision-log.md`

## Operating sequence

### 1. Initialise the run

Create or refresh the working files and record the engagement objective, active skill path, and known blockers.

### 2. Lock the pipeline path

Choose the stage path explicitly.

Default path:

1. `input-evidence-cataloger`
2. `evidence-consistency-auditor`
3. `brief-storyline-architect`
4. `report-storyboard-builder`
5. `presentation-storyboard-builder`
6. `document-writer`

Variant path for workshop-led work:

1. `workshop-writeup-composer`
2. `evidence-consistency-auditor`
3. storyline and storyboard stages as needed
4. `document-writer`

### 3. Run each stage with a gate

Before advancing a stage, confirm:

- required outputs exist
- blockers are explicit
- open questions are logged
- decisions and exceptions are logged
- the stage-specific validation checklist has been run

If any of these are false, the stage is `blocked`.

### 4. Keep the runbook current

For each stage, maintain:

- objective
- required inputs
- outputs produced
- blockers
- handoff status
- owner
- last validation result

## Back-iteration loop

When the forward path is complete, run the back-iteration loop:

1. review the final draft or storyboard state
2. check for contradictions against upstream artifacts
3. reopen the earliest broken stage
4. repair downstream outputs in order
5. update runbook and status files

## Handoff and closure

The workflow closes only when:

- all active stages are `ready`
- all material blockers are resolved or explicitly accepted
- open questions are either closed or deliberately parked
- the current artifact path can be explained from the tracking files alone
