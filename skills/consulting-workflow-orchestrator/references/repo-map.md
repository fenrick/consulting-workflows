# Consulting Workflow Orchestrator Repo Map

## Purpose

This map shows where workflow control state should live so that orchestration survives handoffs and interruptions.

## Main files

- `tracking/workflow-runbook.md`: detailed control log for each stage
- `tracking/workflow-status.md`: compact status board
- `tracking/open-questions.md`: cross-stage unresolved items
- `tracking/decision-log.md`: cross-stage decisions and exceptions

## Templates

- `assets/templates/workflow-runbook-template.md`
- `assets/templates/workflow-status-template.md`

## Typical flow

1. Initialise runbook and status.
2. Set the pipeline path.
3. Advance stages only through written gates.
4. Run backward validation before closure.
