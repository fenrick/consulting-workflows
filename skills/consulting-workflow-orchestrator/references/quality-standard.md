# Consulting Workflow Orchestrator Quality Standard

## Purpose

This file defines the control standard for running the full skill pipeline without hidden blockers or fake progress.

Use it at each stage gate and again before closure.

## Core standard

- No stage advances without declared artifacts.
- Blockers, exceptions, and unresolved items stay visible.
- The runbook is the operational truth, not chat memory.
- Backward validation is mandatory before closure.

## Authoring standard

- Status notes must be plain and factual.
- Do not disguise blockers with optimistic language.
- Do not use `in progress` as a substitute for missing outputs.
- Rework must be described clearly enough that another operator can see what reopened and why.

## Tracking standard

- Sequence, blockers, decisions, and stage state must be current in `tracking/workflow-runbook.md` and `tracking/workflow-status.md`.
- Cross-stage unresolved items must be carried in `tracking/open-questions.md`.
- Exceptions and risk acceptances must be carried in `tracking/decision-log.md`.
- Stage state must be reconstructable from tracking files alone.

## Handoff standard

- Each stage must declare whether it is `ready`, `blocked`, or still being worked.
- Downstream stages must be using the current upstream artifact version.
- Closure is allowed only when the active path has no hidden dependency or undocumented blocker.
