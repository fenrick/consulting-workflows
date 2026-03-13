# Evidence Consistency Audit Workflow

## Purpose

This workflow tests whether claims across working materials can survive factual scrutiny before drafting or release.

It is an audit pass, not a writing pass.

## When to use this workflow

Use it after intake and before major drafting, or whenever upstream artifacts change enough to risk contradiction drift.

Do not use it as a substitute for storyline or report writing.

## Working files

- `tracking/evidence-consistency-report.md`
- `tracking/open-questions.md`
- `tracking/decision-log.md`

## Operating sequence

### 1. Set up the audit files

Create or refresh the working files.

### 2. Define the audit scope

List the claim-bearing artifacts in scope and state the comparison boundary clearly.

### 3. Build the contradiction skeleton

Start with a table of:

- claim
- source location
- comparison artifact
- issue type
- severity
- current status

### 4. Expand the evidence bullets

For each issue, capture:

- what conflicts
- which source is newer or stronger
- whether the conflict is real, apparent, or unresolved
- what needs to change
- who owns the next step

### 5. Write the audit narrative

Once the issue table is stable, write short prose that explains:

- the highest-risk contradictions
- the main weak-support patterns
- the most important supersession problems
- what must be fixed before drafting or release

## Back-iteration loop

Use this cycle for each material revision:

1. contradiction skeleton
2. evidence bullets
3. short prose summary
4. flow pass for issue ordering
5. humanise awkward machine phrasing
6. restore neutral voice and simple language

## Handoff and closure

Before handoff:

- unresolved issues stay in `tracking/open-questions.md`
- accepted risk decisions go in `tracking/decision-log.md`
- the live report is updated in `tracking/evidence-consistency-report.md`
- `references/validation-checklist.md` has been run
