# Consulting Skill Quality Standard

This standard applies to all skills in `skills/consulting-workflows/`.

## Output quality contract

Every skill output should be:

- factual and source-bound
- explicit about unknowns and assumptions
- decision-useful, not generic commentary
- traceable to input artifacts
- structured for handoff to the next skill

## Required quality checks

Before finalizing any skill output:

1. confirm each major claim has an evidence source or is tagged as unknown
2. remove speculative language that is not supported by inputs
3. verify output files are written to the declared paths
4. update `tracking/open-questions.md` for unresolved gaps
5. update `tracking/decision-log.md` for material judgment calls

## Consistent writing style

- use plain, precise language
- avoid inflated consultant filler
- keep bullets actionable
- prefer concrete nouns and verbs over abstractions

## Handoff integrity

Each skill must leave:

- a clear artifact for the next skill
- a clear list of unresolved items
- no hidden state in chat-only reasoning

## Working materials discipline

- maintain working artifacts in `tracking/` (or declared equivalents) for every stage
- avoid storing analysis state only in generated deliverables
- keep unresolved items and decisions live throughout the workflow

## Back-iteration standard

- run at least one explicit back-iteration pass per stage
- re-check claims against sources after structural changes
- re-open and update `open-questions` when contradictions appear
