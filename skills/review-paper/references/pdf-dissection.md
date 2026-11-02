# PDF dissection and source integrity

Use this reference when the evidence is a PDF or an extraction derived from one. The goal is a faithful, navigable representation of the paper, including material that plain text loses.

## Establish the source

Record title, authors, DOI/arXiv identifier when present, version/date, retrieval or supplied-file origin, and page count. Verify identity from the title page and authoritative landing page when available; PDF metadata can be missing or stale. For a durable review, hash the local original so later extractions can be tied to the same bytes. Keep a corrected or OCR copy separate from the original.

Create a page map as needed, for example:

| Physical PDF page, 1-based | Printed label | Content |
| --- | --- | --- |
| 1 | unnumbered | Title, abstract |
| 5 | 4 | Algorithm 1, definitions |
| 12 | A-1 | Supplementary experiment |

Do not infer a single offset for every page: cover sheets, appendices, and combined proceedings can change numbering. If a tool uses zero-based page indices, convert explicitly. Cite "PDF p. 5, printed p. 4, Algorithm 1" where ambiguity matters. For unpaginated HTML, use stable section and figure labels and say that the source differs from the PDF.

## Acquire two complementary views

When the assigned capabilities include `extract-paper-pdf`, use its Docling extraction/reuse method to prepare the two views. Retain structured page provenance, read coherent sections with coverage notes, and revisit specific evidence across follow-ups. Reuse usable supplied extractions. A skill binding does not establish that Docling is installed in the worker runtime.

An available PDF capability, or a renderer plus text extraction, is sufficient when Docling is unavailable. These example local commands remain a fallback; avoid another whole-paper extraction merely to duplicate a successful conversion:

```bash
# Replace these paths with the selected file and an existing work directory.
pdfinfo "/path/to/paper.pdf"
sha256sum "/path/to/paper.pdf"
pdftotext -layout "/path/to/paper.pdf" "/path/to/work/paper-layout.txt"
pdftoppm -f 5 -l 5 -r 160 -png "/path/to/paper.pdf" "/path/to/work/paper-page"
```

Use extracted text to locate sections, definitions, captions, references, and keywords. Inspect a page rendering with an image-capable viewer to establish reading order and verify relied-on visual evidence. Rendering a file without opening its image is not visual inspection. For deep review, read the full paper and relevant appendices and supplementary material, including proofs and evaluation details; state any unavailable or unread material and how it limits the review. For triage, a sampled reading is acceptable if labeled.

## Route by extraction symptoms

| Symptom | Response | What to preserve |
| --- | --- | --- |
| Columns interleave or captions interrupt paragraphs | Read page images; try layout/block extraction or column crops for that region. | Original page locator and the corrected reading order. |
| Text is absent or garbled on a scanned page | Use an available OCR capability on a copy, with the appropriate language; visually verify consequential terms and numbers. | OCR method, affected pages, and unresolved uncertainty. |
| A table becomes an unstructured number list | Extract/crop the table with a table-aware tool, then compare against the rendered page. | Row/column hierarchy, units, caption, footnotes, merged headers. |
| Equations lose signs, subscripts, or quantifiers | Inspect an enlarged rendering and relevant definitions; use source TeX/HTML if legitimately available. | Verified transcription and any unresolved symbols. |
| Figure crop omits axes, legend, or caption | Expand the crop or inspect the complete page before interpretation. | Axis scales, units, legend, caption, uncertainty conventions. |
| Supplement or code is unavailable | Review the accessible paper and qualify claims that depend on the missing material. | Exact missing artifact and the conclusions it limits. |

Do not run OCR over already reliable text merely to use another tool. Conversely, readable prose does not prove that dense equations and table cells are correct. If extraction methods disagree, resolve against the page image where possible; keep unresolved discrepancies visible.

## Inspect the scientific objects

**Figures:** identify what each axis, color, curve, symbol, and error bar represents. Check log scales, normalized quantities, truncated axes, selected examples, and whether a curve is measured, simulated, or theoretical. A visually estimated value is approximate. If exact numerical comparison matters, seek the underlying table/data or report digitization uncertainty.

**Tables:** preserve headings, units, sample counts, metric direction, missing entries, significance marks, and footnotes. Distinguish a dash or timeout from zero. Check whether bold means a best score, statistical significance, or author emphasis. Do not average across incomparable workloads or reconstruct raw observations from reported averages.

**Equations and algorithms:** define symbols, dimensions, domains, constraints, and initial conditions. Track preconditions and theorem quantifiers. Follow the connection from pseudocode to the property claimed. Test understanding with a small example and a boundary case; a hand-worked example illustrates behavior but does not prove a theorem or reproduce a benchmark.

**Proofs:** read the actual argument and its cited dependencies, not only the theorem statement. Check the implication chain, quantifiers, regularity or feasibility conditions, and boundary cases relevant to the claimed guarantee. Directly inspect ambiguous symbols or layout against the PDF. Distinguish a proof step you checked from a cited lemma you did not inspect, an intuitive reformulation, or an unresolved gap.

**Appendices and supplements:** follow references that qualify a main result, define exclusions, provide proofs, or describe hyperparameters. Distinguish an assumption stated only in the appendix from a missing assumption. Check whether linked code/data correspond to the reviewed version before calling them reproducibility support.

## Keep uncertainty local and actionable

For each consequential ambiguity, record the object, location, interpretation attempted, and consequence. Example: "Table 2, PDF p. 8: the scan does not distinguish 0.8 from 0.6 for method B; ranking B against C is unresolved; the surrounding method explanation remains usable."

The result should make follow-up reading cheaper: stable source identity, reusable extraction/page map, relevant evidence locations, and a short list of unresolved extraction problems. It need not include every page image or a second full copy of the paper.
