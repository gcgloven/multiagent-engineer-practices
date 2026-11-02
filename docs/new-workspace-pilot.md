# Set up and test a fresh workspace

Run these commands from the `multica-engineer-practices` repository on the Linux machine and account that runs the agents. The full research dependency lock is validated with Python 3.12; the quality-only bootstrap requires Python 3.11 or newer. Have Git, Python virtual-environment support and an authenticated Multica CLI 0.7.1 or newer available. Authentication is interactive and is not embedded in configuration files.

First discover IDs from the new workspace. A workspace member ID is not a runtime ID.

```bash
multica version
multica auth status
multica workspace list --full-id
multica --workspace-id NEW_WORKSPACE_UUID runtime list --output json
multica --workspace-id NEW_WORKSPACE_UUID project list --output json
```

Create the test project in Multica if needed. Use its UUID below. For a named connection, add `--profile YOUR_PROFILE` to discovery and pilot commands, and set the profile in the setup configuration.

```bash
cp setup.example.toml setup.local.toml
```

Edit `setup.local.toml`: fill in `workspace_id`, `runtime_id`, and the same ID in `host.local_runtime_ids`. This last field is your explicit declaration that the runtime executes on this host. Set `research=true` for PDF and numerical/plotting libraries. Keep `update_existing=false` for an empty workspace. Optional `runtime_map` entries select other runtimes on this same host; the installer verifies membership in the workspace. Optional native skill directories install the same complete method folders for independently launched compatible CLIs; reload those clients after installation.

```bash
python3 -B scripts/setup.py --config setup.local.toml --plan
python3 -B scripts/setup.py --config setup.local.toml --apply
python3 -B scripts/setup.py --config setup.local.toml --doctor
```

Plan inspects all selected targets before installation. Apply installs pinned tools and parsers under `.multica/tools`, runs disposable known-success/failure fixtures, installs optional native skills, then configures nine agents, twelve skills and the selected squads. Shared unchanged objects are reused. Doctor checks the host environment and reads back configured instructions, bindings and rosters without launching agents. Its local bundle regeneration is not a workspace mutation. The new Docling extraction skill does not add Docling or its model assets to the pinned research pack; provision those separately in the executing runtime when selecting that extraction path.

Apply records progress under `.multica/setup`. Installation is not atomic. If interrupted, inspect the journal and workspace; set `update_existing=true` for an intentional refresh/recovery and rerun the plan. Existing identical objects become no-ops. Changed managed instructions/bindings and rosters are replaced in update mode; models/access settings and human squad members are preserved. Changed managed configuration is snapshotted in the private setup journal directory before updates. Changed native skill directories are moved to `.multica/setup/native-backups`, outside the skill discovery directories. Do not use update mode against active production work as a substitute for an explicit migration plan.

The tools live in their own virtual environment and include Crapper, Dryer, Mutator, their parser libraries, an EDN report reader and Python test/coverage dependencies. Source checkouts and their licenses remain under the environment's `sources` directory; exact Git revisions are recorded in [toolkits.lock.json](../toolkits.lock.json). PDF/analysis libraries use a separate pinned requirements list. The host check does not establish primary-source browsing, image understanding, project dependencies or managed-agent execution.

For a remote execution host, run this checkout's host bootstrap there, using the same service account and a runtime-accessible path. `--host-only` performs no Multica operations. This release does not remotely install packages through a runtime ID, and the unified setup refuses to claim readiness for runtimes not declared local.

```bash
python3 -B scripts/setup.py --config setup.local.toml --host-only --plan
python3 -B scripts/setup.py --config setup.local.toml --host-only --apply
```

To configure workspace objects alone, the lower-level installer remains available. It does not install tool backends or inject the unified setup's absolute tool paths:

```bash
python3 -B scripts/install_multica.py --workspace-id NEW_WORKSPACE_UUID \
  --runtime-id NEW_RUNTIME_UUID --squad-profile all
# Add --apply to create; add --update-existing for an intentional refresh.
```

Prepare one new batch of disposable inputs on the execution host. The current suite uses authored, generic engineering examples: log inspection, retry reliability, import measurements, configuration validation, and bounded software changes. Requests, fixtures and operator expectations are public in [pilot_cases.py](../scripts/pilot_cases.py); use separate private cases for a hidden evaluation. Choose a new batch for each clean retest or changed case definition. Fixture preparation refuses to overwrite an existing batch, preserving prior agent work. Older batches retain their original issue descriptions and inputs; the current launcher rejects a description that differs from this suite.

```bash
PILOT_BATCH="generic-engineering-v1"
PILOT_WORKDIR="$PWD/.multica/pilots"
MULTICA_WORKSPACE_ID="NEW_WORKSPACE_UUID"
MULTICA_PROJECT_ID="NEW_TEST_PROJECT_UUID"

python3 -B scripts/pilot_issues.py --list
python3 -B scripts/pilot_issues.py --batch "$PILOT_BATCH" \
  --workdir "$PILOT_WORKDIR" --init-fixtures
```

Preview and then create the nine parked tickets:

```bash
python3 -B scripts/pilot_issues.py \
  --workspace-id "$MULTICA_WORKSPACE_ID" --project-id "$MULTICA_PROJECT_ID" \
  --batch "$PILOT_BATCH" --workdir "$PILOT_WORKDIR"

python3 -B scripts/pilot_issues.py \
  --workspace-id "$MULTICA_WORKSPACE_ID" --project-id "$MULTICA_PROJECT_ID" \
  --batch "$PILOT_BATCH" --workdir "$PILOT_WORKDIR" --apply
```

The seeder resolves exact squad names, searches including closed issues for stable batch/case identities, creates unassigned backlog issues, then assigns each squad with `--no-start`. It uses description files inside the repository working directory, with no routing mentions or attachments. Repeating the same command reuses existing cases and never resets their status. It can recover an issue created before a lost response or failed assignment. Ambiguous duplicates, changed descriptions, changed ownership, truncated results or another project using the same batch stop the operation for inspection. A local lock prevents simultaneous invocations from this checkout; it is not a cross-machine transaction lock.

Read-back tolerates Multica removing the description file's final newline or normalizing CRLF line endings. Actual description changes still stop recovery. Ownership checks verify both the squad UUID and `assignee_type=squad`. After an uncertain create/assign outcome, inspect the saved report and existing issue before retrying. Reuse the same arguments only when the source cases and runtime directory are unchanged; a changed suite needs a new batch. Recovery preserves existing files and never launches agents implicitly.

Use `--cases P01,P05` to seed a subset. For customized squad names, supply `--squad-map path/to/map.json`, mapping catalog profile keys such as `software-delivery` to exact installed names. The report records issue and squad IDs plus expected outcomes; expectations are not inserted into the agent request.

| Case | Squad | Main observation |
| --- | --- | --- |
| P01 | Research and Engineering | Frames a log-inspection utility and waits for the needed scope/mode choice. |
| P02 | Open Research | Critiques a fictional retry-reliability claim and proposes three experiments without executing them. |
| P03 | Analytics to Engineering | Normalizes import throughput and challenges a speed claim from unequal workloads/machines. |
| P04 | Software Delivery | Repairs an inclusive file-size boundary with independent review of test quality. |
| P05 | Engineering Design | Proposes configuration-validation scope, library/CLI options and schema reuse before detailed planning. |
| P06 | Software Delivery | Demonstrates a JSONL summary CLI with normal, empty and invalid-input checks, then stops. |
| P07 | Engineering Design | Creates exactly three proposed configuration-tool children, numbered and parked. |
| P08 | Software Delivery | Delivers only the configuration-defaults function; the later CLI remains unauthorized. |
| P09 | Software Delivery | Exposes a weak file-size assertion or surviving mutant and reports missing evidence honestly. |

Launch one case after reviewing its ticket and runtime access. This command starts agent work and consumes resources. Preview first by omitting `--apply`:

```bash
python3 -B scripts/pilot_issues.py \
  --workspace-id "$MULTICA_WORKSPACE_ID" --project-id "$MULTICA_PROJECT_ID" \
  --batch "$PILOT_BATCH" --workdir "$PILOT_WORKDIR" --launch P01 --apply
```

Launch requires an assigned backlog issue with no run history, the original description/runtime directory and the configured squad owner. Pass the same `--squad-map` when using customized names. It will not rerun an active, completed or previously executed case. Inspect the actual run after an uncertain launch outcome; do not repeat it blindly. Run the remaining cases individually. Approvals and follow-up decisions are human inputs; the script never manufactures them or auto-approves the next milestone.

```bash
multica --workspace-id "$MULTICA_WORKSPACE_ID" issue get ISSUE_UUID --output json
multica --workspace-id "$MULTICA_WORKSPACE_ID" issue children ISSUE_UUID --output json
multica --workspace-id "$MULTICA_WORKSPACE_ID" issue runs ISSUE_UUID --output json
multica --workspace-id "$MULTICA_WORKSPACE_ID" issue comment list ISSUE_UUID \
  --roots-only --summary --compact --output json
```

Use the expected outcomes and [behavioral acceptance guide](pilot-acceptance.md) to record observed evidence. Check actual children, statuses, runs, changed files, candidate identity and review independence. An agent stating that it is waiting while creating or activating dependent work fails the relevant gate test. A completed run is not a behavioral pass. To continue P05, approve the exact chosen scope, request its numbered map, then approve backlog creation separately; inspect each boundary before authorizing implementation.

For project quality checks, use the toolkit Python and explicit commands. The following Python example uses a project with `subject.py` and unittest tests; adapt its interpreter, paths, scope and budget to the project:

```bash
TOOL_BIN="/absolute/environment/path/from/setup-report/venv/bin"
mkdir -p /absolute/project/target/coverage/python
"$TOOL_BIN/python" scripts/quality_check.py --repo /absolute/project \
  --bin "$TOOL_BIN" --profile standard --seconds 300 --workers 2 \
  --test-command "$TOOL_BIN/python -m unittest discover" \
  --coverage-command "$TOOL_BIN/python -m coverage run --source=subject -m unittest discover && $TOOL_BIN/python -m coverage lcov -o target/coverage/python/lcov.info" \
  --coverage-report target/coverage/python/lcov.info subject.py
```

Use `rigorous` for targeted mutation or `quick-mvp` for baseline-only evidence. Supply commands appropriate to the project's environment; the tools environment is suitable only when it contains the project's dependencies. Outputs go into `.quality-evidence` and `.metrics` in the selected project. Exit 0 means checks completed without detected evidence gaps/review items; 1 means review is required; 2 means blocked or incomplete evidence. None grants independent approval. Keep detailed logs in the case evidence and summarize decisive results in the ticket.

UML Viewer, platform-enforced human gates, remote package execution, GPU/robotics frameworks and automated human acceptance are not installed by this setup. They remain distinct integrations with their own acceptance requirements.
