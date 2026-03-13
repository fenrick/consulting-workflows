# Consulting Workflow Orchestrator Workflow

1. Initialize runbook and status artifacts.
2. Execute pipeline stages in declared order.
3. Enforce gate checks on each stage output.
4. Block progression on unresolved blockers.
5. Run backward pass to catch contradictions.
6. Close only when all stages are `ready`.

