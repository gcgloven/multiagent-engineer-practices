# Docling commands for paper extraction

Use these examples in the selected worker environment. Replace example paths with the assigned local paper and a new extraction directory. Commands follow the official documentation checked on 2026-11-02; the installed CLI's help determines which options are available.

## Locate the tool

```bash
command -v docling
docling --version
docling --help
```

An environment-specific absolute path to `docling` is equally suitable. Current documentation exposes a `convert` subcommand; inspect `docling convert --help` when present. Older releases use conversion options directly after `docling`. Adapt the command to that installed interface instead of repeatedly trying unsupported flags.

Installation belongs to runtime setup. When dependency installation is authorized, install the Docling Python package into the chosen environment using that project's dependency manager. Installing this skill or attaching it to Multica does not install Docling, its model assets, or an image viewer. Initial model downloads may need network access. Reuse pre-provisioned models/offline artifacts when configured; avoid enabling remote model services merely to resolve a local setup gap.

Docling also ships a general usage skill inside its Python package. It can supply version-matched API guidance when available; this paper-specific skill remains usable without registering or copying that upstream skill. Consult only the upstream reference needed for the current operation.

## Reuse before conversion

```bash
sha256sum "/path/to/paper.pdf"
```

Check the existing conversion record against that hash, Docling version, and material settings. Reuse a complete matching bundle with present outputs. Keep different paper versions and extraction configurations distinguishable. Source hash and successful conversion are separate from reading coverage.

## Convert a clean digital PDF

Create the fresh output directory first; use its exact path for both the log and output. This example disables OCR for a document with a usable text layer, retains table extraction, and exports Markdown plus structured JSON:

```bash
mkdir -p "/path/to/extractions/new-conversion"
docling convert --from pdf --to md --to json \
  --pipeline standard --no-ocr --image-export-mode referenced \
  --fail-on partial --output "/path/to/extractions/new-conversion" \
  "/path/to/paper.pdf" \
  > "/path/to/extractions/new-conversion/conversion.log" 2>&1
```

Check the exit status immediately. `--fail-on partial` rejects partial results on versions supporting that flag. If an older version lacks it, inspect its reported conversion status and page coverage explicitly; a zero exit code alone is insufficient. Inspect generated filenames instead of assuming every version uses the same basename conventions.

Keep full logs on disk. Return a short status, output paths, and the relevant error excerpt on failure. Do not print complete Markdown, JSON, logs, or encoded images just to confirm that conversion ran.

For scanned or mixed PDFs that require OCR, select `--ocr` and an available local OCR engine/language using the installed help. Inspect affected pages before treating OCR text as reliable. Avoid forcing full-page OCR over already trustworthy text. A formula-enrichment option can help a demonstrated math-extraction problem, but preserve the original and check consequential symbols visually. Record changed settings and their actual results.

With `--image-export-mode referenced`, exported image content uses file references instead of embedded base64. `placeholder` is an alternative when saving image assets is unnecessary. If needed visual evidence is absent from the export, render the relevant original PDF page or region with the available PDF tool and open that image. Do not assume Docling exported every relied-on object as a usable image.

## Navigate saved material

```bash
rg -n '^#{1,6} |Figure [0-9]+|Table [0-9]+|Theorem|Appendix' "/path/to/extractions/new-conversion/paper.md"
sed -n '120,200p' "/path/to/extractions/new-conversion/paper.md"
```

Choose ranges from the actual outline and scientific argument. Markdown headings are extraction output and may need correction against the PDF. Use the JSON object's provenance for page locations and bounding boxes; preserve parent headings/captions and follow object references rather than treating arrays as guaranteed reading order. Verify physical versus printed page numbering against the original.

For token-bounded chunks, consult Docling's chunking documentation or its installed usage skill. The documented `HybridChunker` refines structural chunks using a selected tokenizer. Keep metadata with the returned evidence; no tokenizer or chunk size proves that a full paper was reviewed. Do not add a retrieval framework for a single conversion.

## Official references

- [CLI options and conversion outcomes](https://docling-project.github.io/docling/reference/cli/)
- [Python and CLI quickstart](https://docling-project.github.io/docling/getting_started/quickstart/)
- [Model prefetching, offline use, and pipeline options](https://docling-project.github.io/docling/usage/advanced_options/)
- [Structured Docling document](https://docling-project.github.io/docling/concepts/docling_document/)
- [Structure-aware chunking](https://docling-project.github.io/docling/concepts/chunking/)
- [Docling's bundled usage skill](https://docling-project.github.io/docling/usage/agent_skills/)
