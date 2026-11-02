# Paper review and PDF capabilities

The Paper Reviewer is a specialist with a scientific reading method and document tools. Its capability should include mechanism explanation, evidence criticism, literature comparison, and useful recommendations. PDF conversion alone cannot supply those judgements.

The [review-paper skill](../skills/review-paper/SKILL.md) provides triage, focused explanation, deep review, and synthesis. An ordinary request to review a paper defaults to a full seven-section critical review, including exactly three prioritized experiment proposals; an explicitly narrower request remains focused. It includes [PDF dissection](../skills/review-paper/references/pdf-dissection.md), [claim and baseline analysis](../skills/review-paper/references/evidence-and-recommendations.md), and a reusable [claim ledger](../skills/review-paper/assets/claim-ledger.md). Open exploration remains valid. Intended use is optional; proposing experiments does not authorize running them or require adoption of the method.

## Recommended configuration

Give the Paper Reviewer:

1. **`review-paper`**, for scientific reading and interpretation.
2. **`extract-paper-pdf` plus the Docling tool in the executing runtime**, for reusable Markdown/JSON extraction and bounded reading with page provenance; an available PDF renderer and vision-capable viewer support direct visual checks. An existing extractor/renderer is the fallback when Docling is unavailable.
3. **Primary-source browsing**, when novelty, competing methods, access, or freshness requires it.
4. **Optional extraction tools**, selected by the document's actual difficulties: OCR for scans, table-aware extraction for numerical comparisons, or structured parsing for a collection of papers.

A named skill is an instruction package. A Python library, command-line program, model, or rendering service is an execution dependency. Registering a skill does not by itself install those dependencies, enable image understanding, or verify that a remote Multica runtime can access the paper.

## Actual skill options

| Option | Useful capability | Recommendation and boundary |
| --- | --- | --- |
| **This repository: `review-paper`** | Scientific interpretation, PDF evidence checks, comparisons, conditional recommendations, and empirical handoffs. | Assign to Paper Reviewer. Package the entire folder, including references and the template. It is portable and does not require a particular PDF vendor. |
| **This repository: [`extract-paper-pdf`](../skills/extract-paper-pdf/SKILL.md)** | Docling conversion, source/configuration reuse, bounded reading, page provenance, and extraction-quality checks. | Bound to Paper Reviewer alongside `review-paper`. The Markdown skill is packaged locally; Docling/model installation remains runtime setup. It preserves deep-review coverage and does not commission benchmark execution. |
| **OpenAI curated `pdf` skill** | PDF reading, rendering and visual checks, plus creation/extraction workflows. | A concrete public skill candidate for Codex-compatible environments. Pair with `review-paper`; verify dependencies and runtime support. The source carries Apache-2.0 terms, separate from this repository's MIT license. [Skill source](https://github.com/openai/skills/tree/main/skills/.curated/pdf), [license](https://github.com/openai/skills/blob/main/skills/.curated/pdf/LICENSE.txt). |
| **Platform-provided Codex PDF skill** | The available local skill supports page rendering and text/table inspection, plus PDF authoring and forms. | Use it where the platform already supplies it. Its presence in one Codex environment does not establish its availability in a Multica worker. Do not assume it is byte-for-byte identical to the public curated skill. |
| **Docling `docling` usage skill** | Routes conversion, extraction, export, and other Docling tasks to supporting references. | Optional when adopting Docling for difficult PDFs or corpus workflows. Docling documents a skill bundled in its Python package and manual registration for runtimes that do not discover it. This is an actual skill, in addition to the tool dependency. [Official skill documentation](https://docling-project.github.io/docling/usage/agent_skills/). |
| **Anthropic `pdf` skill** | PDF processing, text/table extraction, and OCR-oriented workflows. | An option in a permitted Claude environment, not a package to copy into this MIT repository. Its own skill license is proprietary and contains redistribution restrictions. Check the applicable terms and runtime availability. [Skill source](https://github.com/anthropics/skills/tree/main/skills/pdf), [skill license](https://github.com/anthropics/skills/blob/main/skills/pdf/LICENSE.txt). |

External skills are linked, not bundled or installed. The configuration above is a recommendation; live Multica capability and scientific output quality still need testing.

The local bundle binds `extract-paper-pdf` to Paper Reviewer. It uses Docling's existing CLI rather than adding an executable helper to skill archives. Successful conversions are reused by source hash and recorded tool/settings; Markdown is read in coherent sections, while JSON/image payloads stay on disk until relevant. Extraction completion and reading coverage are tracked separately. This instruction binding does not add Docling to the pinned research environment or refresh live Multica objects.

## Tool capabilities to select when needed

| Tool or library | When it earns its place | Limits and review obligation |
| --- | --- | --- |
| **Poppler utilities** | Page metadata, searchable text extraction, and rendering pages for visual inspection. | A renderer does not interpret the image; text may lose structure. Verify critical objects against the rendering. [Poppler project](https://poppler.freedesktop.org/). |
| **pdfplumber** | Inspecting text geometry, cropping regions, and extracting tables from machine-generated PDFs. | Its project documentation describes best results on machine-generated PDFs and no OCR. Check extracted cells, headers, and footnotes against the page. [Project documentation](https://github.com/jsvine/pdfplumber). |
| **PyMuPDF** | Programmatic page rendering, text regions, image extraction, and related document inspection in one library. | Useful as an alternative capability, not an additional mandatory dependency. Review its AGPL/commercial licensing before embedding or distributing it. [Documentation](https://pymupdf.readthedocs.io/en/latest/), [license information](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright). |
| **OCRmyPDF** | Scanned papers or mixed pages that need searchable OCR text. | Keep the original. OCR text is a derived representation; verify consequential values, signs, and notation visually. [Official documentation](https://ocrmypdf.readthedocs.io/en/latest/). |
| **Docling** | Layout-aware conversion and structured outputs, including table/figure export, when ordinary extraction proves inadequate or repeated corpus work justifies it. | Select and validate the relevant pipeline on representative papers; document models/options used. Do not assume every formula/table is faithfully recovered. [Official documentation](https://docling-project.github.io/docling/). |
| **GROBID** | Scientific-document structure, bibliographic metadata, references, and citation contexts in larger paper collections. | Useful for corpus navigation and reference linking. Its structured extraction is not a critical review or a guarantee of correct scientific interpretation. [Official introduction](https://grobid.readthedocs.io/en/latest/Introduction/). |

Start with capabilities already available and expand when they improve evidence quality or repeated work. A difficult scanned mathematical paper can justify OCR, high-resolution inspection, and careful manual transcription. A clean digital paper may need only ordinary extraction plus page inspection. These are different workloads, not a contest to minimize tool count.

## What the agent should produce

For a focused explanation, produce a faithful mechanism explanation with a worked example and exact source locations. For a full review, check full-paper and relevant supplement coverage, the seven-section response, a compact closest-prior-work comparison, qualified claim judgments, and three prioritized proposed experiments with controls, measurements, and recommendation-changing outcomes. For synthesis, compare formulations and evaluation conditions before ranking results. Preserve unanswered questions that are scientifically useful. Evidence gaps should limit the relevant conclusions rather than be filled with invented results or source locations.

Recommendations should state what to try or read, why, under what conditions, and what evidence would change the advice. A theorem under idealized execution is not a guarantee for a physical system. A promising benchmark may justify a transfer experiment; it does not establish production readiness. No fixed number of experiments or mandatory report sections is required.

## Check the configured worker before relying on it

Use representative documents rather than a successful skill import as the acceptance check:

- **Digital, multi-column paper:** locate a claim, preserve reading order, inspect the supporting figure/table and caption, and cite physical and printed page numbering correctly.
- **Scanned or mixed PDF:** identify extraction uncertainty; use OCR only where needed; visually verify a consequential value or symbol and keep the original available.
- **Equation/appendix-dependent paper:** explain the assumptions and mechanism, trace the supporting appendix, and distinguish explanation from proof verification or reproduction.
- **Cross-paper comparison:** refuse an unsupported shared leaderboard when metrics or workloads differ; explain the differences and offer a fair comparison route.
- **Exploratory follow-up:** reuse the paper map, pursue a worthwhile question, and avoid forcing an implementation plan when the user is seeking understanding.

Record the tools and versions actually available, what was inspected, what remains uncertain, and whether results are a configuration check or a scientific evaluation. No external skills were installed, no live Multica agents were changed, and no real-paper capability benchmark was performed as part of writing this recommendation. External source pages were checked on 2026-10-29; verify them again when selecting a version for installation.
