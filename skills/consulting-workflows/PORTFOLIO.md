# Consulting Workflows Skill Portfolio

Recommended repo/portfolio name:

- `evidence-to-storyline-skillpack`

Alternative names:

- `consulting-document-factory`
- `insight-to-deliverable-skills`

## Skill map

1. `consulting-workflow-orchestrator`
2. `input-evidence-cataloger`
3. `brief-storyline-architect`
4. `evidence-consistency-auditor`
5. `report-storyboard-builder`
6. `presentation-storyboard-builder`
7. `workshop-writeup-composer`
8. `document-writer` (canonical skill at `skills/consulting-workflows/skills/document-writer/`)

## Nested structure

```text
skills/
  consulting-workflows/
    skills/
      consulting-workflow-orchestrator/
      input-evidence-cataloger/
      brief-storyline-architect/
      evidence-consistency-auditor/
      report-storyboard-builder/
      presentation-storyboard-builder/
      workshop-writeup-composer/
      document-writer/
    references/
    scripts/
```

## Task breakdown

1. Intake and evidence discovery
- inventory all input files, folder trees, and archive contents
- capture provenance and metadata (author, date, format, version/supersession)
- produce factual statements and open questions for uncertain claims

2. Brief-to-storyline design
- convert brief + evidence catalog into a top-down storyline
- define section hypotheses, support logic, and priority messaging
- flag proof gaps and required validations

3. Report storyboard build
- convert storyline into a written skeleton (headings, section intent, evidence hooks)
- define what each section must prove and what artifacts it needs

4. Presentation storyboard build
- convert storyline into slide skeleton (slide purpose, key message, evidence payload)
- map narrative flow, transitions, and executive decision points

5. Drafting and production
- use `document-writer` to produce working markdown, tracking files, and packaged output

6. Workshop write-up variant
- use `workshop-writeup-composer` when inputs are workshop transcripts plus workshop artifacts
- produce a consistent formal workshop write-up with explicit inputs and outputs

7. Orchestration and quality enforcement
- use `consulting-workflow-orchestrator` to enforce stage-gate checks
- run portfolio quality checks before handoff

## Overlap model

- `input-evidence-cataloger` feeds both storyline and drafting skills
- `evidence-consistency-auditor` hardens claims before storyboard and drafting
- `brief-storyline-architect` feeds both storyboard skills
- `report-storyboard-builder` and `presentation-storyboard-builder` share section logic but differ in output grammar
- `workshop-writeup-composer` is a specialization path that can feed `document-writer`
- `document-writer` is the canonical authoring and packaging workflow

## TODO candidate skill

- `exec-qa-red-team`
- purpose: run a senior-executive challenge pass over storyline, report storyboard, and workshop write-up to stress-test logic, clarity, and decision-readiness

## Quality checks

Run:

```bash
python3 skills/consulting-workflows/scripts/validate_skill_portfolio.py
```
