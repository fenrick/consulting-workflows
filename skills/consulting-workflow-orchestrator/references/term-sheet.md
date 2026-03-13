# Consulting Workflow Orchestrator Term Sheet

## Purpose

Use this sheet to keep workflow control language stable across the runbook, status board, and handoff notes.

## Core terms

- `stage`: a bounded skill step with declared inputs, outputs, and gate
- `gate`: the criteria that must be met before progression
- `runbook`: the detailed operating record for the workflow
- `status file`: the compact view of current stage state
- `blocked`: a stage that cannot progress without new work or a decision
- `ready`: a stage whose outputs are fit for handoff
- `backward pass`: a review from downstream artifacts back to upstream sources

## Usage rules

- Use `blocked` only when there is a real gating condition.
- Use `ready` only when validation passed.
- Prefer `handoff` over `transition` for stage movement.
- Do not invent softer synonyms for blockers; they hide risk.
