# Consulting Workflow Orchestrator Validation Checklist

## Stage control checks

- Every active stage has a status in `tracking/workflow-status.md`.
- Every active stage has a runbook entry.
- Required outputs for each completed stage exist.
- Blocked stages explain what is missing and why.

## Handoff checks

- Open questions were carried forward, not dropped.
- Decision and exception logs were updated at each gate.
- Downstream stages are using the current upstream artifact versions.
- Reopened stages triggered downstream review where needed.

## Closure checks

- A backward pass was run.
- No stage is marked `ready` with missing required outputs.
- The current workflow state can be reconstructed from tracking files alone.
