# Validation Checklist

## Source checks

- Every changed factual claim is traceable to a readable working source set, or is explicitly marked as requiring user-supplied source confirmation.
- No new claim depends solely on contextual material.
- Presentation wording or workshop shorthand has been checked against the working baseline before being lifted into prose.
- Where a PDF has replaced an earlier PPTX or document file, the content match has been verified before citing or paraphrasing it.
- The evidence section records every document reviewed directly in the phase, even if some of those documents are not cited in the main body.
- The evidence section clearly distinguishes directly reviewed documents from corpora that were only indexed, sampled, or partially reviewed.
- For non-trivial reviews, the running review notebook has been updated during source intake so observations and tentative findings are not lost between passes.

## Structure checks

- The working tracking set exists before substantial body drafting starts.
- The title block exists and its placeholder title and subtitle have been replaced.
- For substantial documents, the front end includes an executive summary and an introduction.
- The ordered source section files still read correctly in sequence.
- The first page or two states the document purpose, scope, and organising logic plainly.
- Where the audience includes non-specialists, the front end also states what the subject is and is not.
- Section titles, theme titles, and improvement principles are consistent across files.
- The organising labels are stable wherever they recur.
- Cross-references between sections still make sense after edits.
- The split files do not drift from the intended combined report structure.
- Closing sections separate decisions, planning, and evidence clearly enough that the report cannot be misread as a vague strategy paper.
- Review-style documents with several user types or trust boundaries include enough orientation and flow context before dense findings.

## Voice checks

- Tone remains plain, neutral, and evidence-led.
- No sales language, consultant filler, or blame language has been introduced.
- "What is working" and "what is getting harder" remain balanced where that structure is used.
- Slide shorthand has been rewritten into report prose.
- Abstract nouns do not pile up in the weakest sections.
- Later paragraphs are not overloaded with linked ideas before the sentence lands.
- A final prose-quality pass has been run, and any edits from that pass still preserve the approved departmental tone.

## Content checks

- New material from the lead deliverable has been distributed into the correct report sections, not dumped into one section.
- Any appendix-style additions are clearly separated from the main narrative.
- Figure introductions explain what the reader should take from the image.
- Every figure has a plain-language reason for being there.
- Reconstructed figures are identified as reconstructed where that matters.
- Review-style appendices include a findings register if the document relies on many discrete findings.
- No duplicate paragraphs or near-duplicates remain after merging old and new wording.
- The evidence section proves coverage without overstating completeness. It does not imply that an entire folder was fully reviewed unless that happened.
- Comparative material remains comparative context, not disguised direct evidence.
- Terminology matches `controls/term-sheet.md` unless a specific distinction is intentional.

## File and media checks

- Markdown headings render cleanly.
- Bundled scripts were run from the intended project root or with explicit path arguments.
- Canonical document prose still lives in markdown working files rather than inside generator code.
- Any delivery script reads the document content from markdown or tracked source files instead of embedding large narrative blocks in code.
- Existing media references still point to valid files.
- No orphaned media files are created without a matching reference.
- If Writage or Word is in scope, figure formats have been checked for compatibility and fallback PNGs exist where needed.
- If Pandoc document export is in scope, the reference doc exists and the export path has been smoke-tested.
- For substantial documents, the exported document includes a table of contents from level 1 headings unless it was deliberately disabled.
- No deep-research citation tokens, smart paste artefacts, or malformed markdown remain.
- Every Writage or Pandoc citation key used in the source markdown exists in the active bibliography file.
- Citation syntax uses Writage/Pandoc form such as `[@key]`, not manual markdown footnotes.
- Bibliography entries include full document titles and any relevant formal identifiers where available.
- The assembly command succeeds if the combined output is meant to be current.
- Any assembly regression tests provided by the project succeed if assembly behaviour was touched.
- The packaged output is accompanied by the working markdown and tracking files rather than being shared on its own.

## Review checks

- Read the changed sections in sequence, not in isolation.
- Compare changed sections against the lead deliverable for topical coverage.
- Read the front end after reading the back half to check that the framing still matches the finished document.
- A final prose pass has been run.
- Ask the user to review before treating the update as final, especially where missing source attachments limit fact checking.
