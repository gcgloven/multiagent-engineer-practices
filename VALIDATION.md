# Validation

The public package contains nine agent profiles, five squad presets and twelve method skills. The generated bundle is a local inventory of prompts and complete skill archives. It does not implement a separate agent runtime. Historical results below retain the counts of the package checked on their stated date.

## Reproduce local checks

Run from the repository root with Python 3.12 or newer. These offline tests use temporary directories, authored fixtures and a simulated Multica CLI; they do not create live workspace objects.

```bash
python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
python3 -B -m unittest discover -s examples/analytics-to-engineering -p 'test_*.py' -v
python3 -B -m unittest discover -s examples/code-to-reliable-delivery -p 'test_*.py' -v
python3 -B scripts/prepare.py
```

The checks cover complete resource packaging, deterministic archives, unsafe-path rejection, installer reconciliation, setup configuration, ticket seeding and launch safeguards, and quality-evidence interpretation. The teaching examples cover cookbook quantity parsing and an offline article-preview compiler using fictional inputs.

## Local verification — 2026-10-30

| Check | Observed result |
| --- | --- |
| Offline script suite | 66 tests passed. |
| Quantity-analysis example | 10 tests passed. |
| Article-preview example | 12 tests passed. |
| Generated package | Nine agent prompts, five squad policies and eleven complete skill archives generated. |

These results apply to the local source and offline fixtures. Live workspace acceptance remains a separate check below.

## Host and runtime checks

Follow the [setup and test guide](docs/new-workspace-pilot.md) to provision tools and check a real execution host. With the configured tools environment, run the disposable known-success and known-failure fixtures:

```bash
TOOL_BIN="/absolute/path/to/tools/venv/bin"
"$TOOL_BIN/python" -B scripts/test_toolkit_smoke.py --bin "$TOOL_BIN"
```

A successful host check establishes tool behavior under that account and environment. Managed-agent access, instruction delivery, callbacks, independent review, budgets and human decision boundaries require the [behavioral acceptance cases](docs/pilot-acceptance.md). Record the actual environment and observed evidence in your private workspace.

## Evidence limits

Passing packaging and simulated-CLI tests establishes local behavior under those fixtures. A completed agent run is not automatically a behavioral pass. Instruction-based gates depend on the configured runtime and agents; the installer does not mechanically enforce them. No performance, cost, scientific reproduction or production-readiness claim follows from these checks.

The research journey is illustrative. The analytics and delivery examples use authored teaching inputs; their results do not establish broad data coverage or production integration. Validate PDF extraction, rendering and interpretation in the actual worker runtime using the [PDF capability checklist](docs/pdf-capabilities.md#check-the-configured-worker-before-relying-on-it).

For publication checks and the boundary between source files and local evidence, see [publishing this repository](docs/publication.md).
