# Consulting Workflow Orchestrator Validation Checklist

## Purpose

Use this checklist to prove that the workflow state is real, current, and safe to advance.

If the tracking files cannot explain the state of the work, the workflow is not under control.

## How to use this checklist

Run it at each stage gate and again at closure.

- Check stage control before allowing a handoff.
- Check cross-stage continuity after rework.
- Check closure criteria before declaring the run complete.

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
