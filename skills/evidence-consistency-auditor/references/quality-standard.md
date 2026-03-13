# Evidence Consistency Audit Quality Standard

## Purpose

This file defines the quality bar for contradiction finding, weak-support analysis, and risk handling across claim-bearing artifacts.

Use it during the initial audit and every re-audit.

## Core standard

- Every flagged inconsistency cites source locations.
- Confirmed contradictions stay separate from hypotheses.
- Supersession decisions are explicit.
- No issue is closed without a reason.

## Authoring standard

- Keep the report factual and compact.
- Distinguish severity from confidence.
- Do not rewrite upstream artifacts silently.
- Use neutral language and avoid blame.

## Tracking standard

- The report lives in `tracking/evidence-consistency-report.md`.
- Unresolved items stay in `tracking/open-questions.md`.
- Risk acceptance stays in `tracking/decision-log.md`.
- Re-audit results must replace stale issue state, not sit beside it as parallel truth.

## Handoff standard

- Anyone reviewing the report must be able to see which issues are open, which are resolved, and which were accepted as residual risk.
- Source strength and issue status must be explicit enough to support downstream correction work.
- The report must not overstate certainty where evidence remains mixed or incomplete.
