# Term Sheet

## Purpose

This file keeps repeated document terms stable. Use it when drafting, revising, or checking for terminology drift.

If a distinction matters, make it explicit. Otherwise keep the preferred term.

## Default document terms

### Core narrative terms

- `theme`: a repeated and validated pattern observed across the evidence
- `finding`: the section-level or grouped conclusion drawn from related evidence
- `improvement focus`: the practical area that future work should address

### Structural and operating terms

- `platform`: the broader operating environment being reviewed, including applications, data, technology, controls, and dependencies
- `application`: a distinct software product or application service within the platform estate
- `module`: a named functional part of the platform or system itself
- `integration`: a defined data or process connection between systems or services
- `release`: a packaged change moved through the delivery lifecycle
- `environment`: a production, training, or non-production instance used for operation, testing, or deployment

### Data and reporting terms

- `system of record`: the authoritative operational source for a given business record
- `reporting layer`: the reporting structures, stores, extracts, and downstream reporting logic built from operational data
- `source record`: use only when the trace back to the originating operational record matters

### Decision and control terms

- `boundaries`: where work happens, where data sits, and where changes can be made
- `ownership`: who is accountable for a module, process, or decision area
- `decision rights`: who can approve, reject, or direct a change

## Usage rules

- Do not cycle between `trusted record`, `main record`, `statewide record`, and `system of record` unless the distinction is deliberate and explained.
- Do not cycle between `reporting zone`, `reporting platform`, and `reporting layer` unless the architecture source requires a specific distinction.
- Prefer `theme` over `issue` when the point is a repeated pattern rather than a single problem.
- Prefer `finding` over `takeaway`, `lesson`, or `headline`.
- Prefer `improvement focus` over `priority area` or `opportunity` unless the user explicitly wants a different label.

## Style rules for repeated concepts

- Use the same term across headings, body text, figure captions, and summary tables.
- If the glossary defines a term, the running text should usually match it.
- Repetition is acceptable for technical accuracy. Synonym variety is not a virtue when it blurs the concept.
