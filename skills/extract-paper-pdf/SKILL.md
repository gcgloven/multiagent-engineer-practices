---
name: extract-paper-pdf
description: Use Docling to extract scientific PDFs into reusable Markdown and structured JSON for paper review, preserving page provenance and reducing repeated raw-text reads. Apply when preparing or revisiting PDF evidence; scientific critique and benchmark execution remain separate tasks.
---

# Extract paper evidence with Docling

Prepare a faithful, reusable reading bundle. Docling is the executable extraction tool; this skill governs source identity, reuse, bounded reading, and extraction checks. It complements the scientific review method supplied by the task and does not change the requested review depth.

## Choose the execution path

- Reuse a supplied local paper and existing usable extraction before downloading or converting it again. Confirm the source version and hash. A changed scientific question alone does not require reconversion.
- Locate Docling in the actual worker environment and record its version. A registered skill is not an installed tool. Read [Docling commands](references/docling-commands.md) when converting or resolving a CLI/version issue.
- Prefer local standard-pipeline conversion. Use native text for clean digital PDFs; enable OCR for scanned or mixed pages that need it. Add formula enrichment or another expensive stage only for a concrete extraction gap within the task's resource boundary.
- Model files may need an initial download even with local inference. Follow the environment's installation/download authority. If Docling or its models are unavailable, state the capability gap and use an available PDF extractor/renderer when that can support the requested review. Do not claim that fallback output came from Docling.

## Convert once and retain the evidence

Keep the original unchanged. In the assigned project directory, use a separate extraction directory identified by source SHA-256 and conversion configuration. Record Docling version, material pipeline/OCR options, and model identity when available. Match those inputs when deciding whether to reuse a prior Docling conversion.

The useful bundle contains:

- Markdown for reading and search, with external image references or placeholders rather than base64 image payloads in text returned to the model.
- Structured JSON for document objects and their page/bounding-box provenance; retain it on disk instead of printing it into context.
- A compact conversion record: source identity/hash, tool version, options, output paths, completion/partial/failure status, and extraction problems. Do not mark a partial conversion complete.
- A section/page index and reading-coverage notes in the existing evidence record. Reuse existing notes rather than creating another report by default.

Write a new conversion into a fresh directory. Reuse it only after checking completion and required outputs; preserve a previously valid extraction if conversion fails. Prefer focused repair of a bad object/page to restarting all papers. Keep any changed settings and affected pages identifiable.

## Read with bounded context and full coverage

1. Inspect the outline and page/object map, then read coherent sections in document order. For a deep review, cover the full paper and relevant appendices/supplements. Record unread or inaccessible portions and the conclusions they limit. Retrieval of a few matching passages does not establish full-paper coverage.
2. Read section-sized excerpts, keeping table headings/units/footnotes and equation definitions with the passage that needs them. Avoid arbitrary character cuts through scientific objects. If a result is truncated, retrieve the missing range explicitly; distinguish a shortened trace display from an actually truncated model input.
3. Preserve concise evidence notes with exact section/page/object locations as reading progresses. On follow-up, search the saved bundle and reopen the needed passage or figure instead of replaying the entire PDF, all notes, and issue history. Revisit already-read material when a specific uncertainty or changed claim requires it.
4. Keep one accountable extraction owner per source version. Share artifact paths, source identity, and evidence locations with other specialists. The Lead normally receives the review and decisive evidence references; a qualified independent reviewer opens the original evidence needed for its own judgment.

Use the installed Docling version's structure-aware chunking if useful for a larger collection or context limit. Keep headings, captions, and page provenance attached; treat token limits as transport bounds rather than scientific section boundaries. Ordinary local search can be sufficient for a small paper set. Creating embeddings or introducing a vector service is not a prerequisite for extraction.

## Check consequential extraction

Compare important figures, tables, equations, algorithms, and ambiguous symbols against the original PDF rendering, using an image-capable viewer. Saved images alone do not establish visual inspection. Verify reading order on multi-column pages and check units, signs, subscripts, headers, legends, and footnotes where the review depends on them.

Derive physical PDF page locations from the JSON provenance and verify against the original. Keep printed page labels separate; Markdown line numbers are navigation aids, not PDF page citations. Do not infer that text proximity guarantees the correct figure/table association.

Keep unresolved extraction errors local to the affected claim. A successful conversion does not establish that every page was read or that a scientific claim is correct. Follow the review's existing method for interpreting evidence and checking novelty.

## Return

Return the bundle location, source/version, conversion status, reading coverage, decisive evidence locations, and unresolved extraction gaps. Keep acknowledgments and diagnostic output short; deliver the substantive scientific review through its requested route.

PDF conversion/rendering are reading aids. This skill does not authorize cloning paper implementations, writing benchmark code, running experiments, or changing agent/squad configuration. Preserve any explicit human execution authorization separately. Report token savings only when measured on comparable reviews with the same coverage.
