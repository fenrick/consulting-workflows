# Document Writer Quality Standard

## Purpose

This file defines the release-quality standard for substantial documentation work produced with this skill.

Use it during drafting, editorial passes, and release preparation.

## Core standard

- Keep canonical prose in markdown, not generator code.
- Keep factual claims traceable to reviewed inputs.
- Keep open questions and decisions current in tracking files.
- Package output only after workflow checks pass.

## Authoring standard

- Use the cyclic drafting loop for substantial work: skeleton, bullet points, paragraphs, narrative flow, humanise, neutral voice and simple language.
- Near release, run the humaniser pass multiple times until successive passes stop finding meaningful cleanup.
- Keep tone plain, neutral, and evidence-led.
- Use Pandoc/Writage citations in source markdown such as `[@key]`; do not hand-roll citation formatting in prose.

## Tracking standard

- Keep source status current in `tracking/source-register.md`.
- Keep editorial checks current in `tracking/editorial-pass.md` and `tracking/release-check.md`.
- Keep unresolved gaps in `tracking/open-questions.md`.
- Keep the live section state visible in `tracking/section-status.md`.

## Handoff standard

- Use APA v7 as the default bibliography style unless the user explicitly overrides it.
- Every figure and every table must have a caption.
- Mermaid diagrams must default to the ELK layout engine and a neutral palette unless the document has a stronger visual requirement.
- Mermaid diagrams must be rendered to high-resolution PNG, with SVG retained as the editable source where useful.
- Exported Mermaid figures should use the document figure-width policy rather than relying on Pandoc full-width defaults.
- Figures and tables must be introduced in the body and explained in plain language.
