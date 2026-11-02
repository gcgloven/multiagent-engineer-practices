# Configure Multica

For automated host provisioning and pilot tickets, use [the setup guide](../../docs/new-workspace-pilot.md).

For a CLI-assisted installation with separate preview and apply steps, see the [installation guide](../../docs/multica-installation.md). The instructions below describe the manual alternative and the pilot workflow.

Configure the profiles and methods useful for your work. Single-owner work can go directly to a specialist; cross-specialty discovery, design, or delivery can go to the squad. Having nine available profiles does not require nine runs per task. Product Manager's explanation can be requested independently at any stage.

**Validation:** commands checked against Multica CLI **0.7.1** and official documentation on **2026-10-29**. Validate the configured prompts and callbacks with a fresh runtime pilot in your own workspace. This is configuration guidance, not an executable harness.

## Prepare and configure agents

From the repository root:

```bash
python3 -B scripts/prepare.py
multica version
multica auth status
multica workspace list --output json
multica runtime list --output json
multica agent list --output json
multica squad list --output json
multica skill list --output json
```

Authenticate with `multica login` if needed. Select `multica workspace switch <workspace-id>`. Inspect existing objects before creating duplicates. Keep account output and credentials private.

On **Agents → New agent**, choose an online runtime, then paste the appropriate generated file into **Instructions**:

| Profile | File under `build/multica/agents/` | Responsibility |
| --- | --- | --- |
| Lead | `lead.md` | Coordinate specialists and decisions |
| Scout | `scout.md` | Explore questions and evidence |
| Paper reviewer | `paper-reviewer.md` | Explain mechanisms, inspect PDF evidence, critically review and compare papers |
| Analyst | `analyst.md` | Explore data, compare explanations, and design valid experiments |
| Product Manager | `product-manager.md` | Clarify stakeholder behavior and explain work, design, and project fit on demand |
| Systems Engineer | `systems-engineer.md` | Domain models, system contracts and architecture |
| Software Engineer | `software-engineer.md` | Authorized code, developer tests and repairs |
| Test & Code Review Engineer | `test-code-review-engineer.md` | Independent software and test-quality review |
| Verifier | `verifier.md` | Independently assess scientific, measurement and design evidence |

Generated files combine common evidence/ownership principles and role instructions. They contain no squad terminology dictionary, workflow sequence, or fixed repair counter. The same agent can answer direct requests and serve multiple squads. Set a supported model, appropriate Access, and concurrency suited to independent work and runtime capacity. Description is display text; behavior belongs in Instructions. See [agent configuration](https://multica.ai/docs/agents-create).

The CLI accepts `--instructions`, without an instruction-file flag; UI paste avoids shell quoting mistakes.

## Add methods selectively

Import the relevant **whole** `skills/<name>/` folder through **Skills → New skill → Import from local**, or use the generated ZIP archives. Attach the imported skills in the agent's Skills tab. Suggested bindings:

| Profile | Methods |
| --- | --- |
| Lead | `frame-problem`; specialists own detailed execution methods. |
| Scout | `investigate-question`, `frame-problem`. |
| Paper Reviewer | `review-paper`; `investigate-question` for broader literature work; an available PDF handling capability as described below. |
| Analyst | `analyze-data`, `run-experiment`; `frame-problem` for ambiguous analytical problems; `ub-coding` for maintained code. |
| Product Manager | `frame-problem`, `explain-work`; product framing and optional source-grounded explanations. |
| Systems Engineer | `design-solution`, `frame-problem`, `ub-design`. |
| Software Engineer | `deliver-slice`, `run-experiment`, `ub-coding`. |
| Test & Code Review Engineer | `deliver-slice`, `ub-review`. |
| Verifier | `design-solution`, `run-experiment`; add `analyze-data` or `review-paper` for the domain being reviewed. Bind methods appropriate to actual review competence. |

Agents select methods from descriptions. Importing a skill stores a workspace snapshot; repository edits do not automatically update it. Read back the imported content and attached resource files. See [skills](https://multica.ai/docs/skills) and the [method design guide](../../docs/skill-design.md).

Example after `python3 -B scripts/prepare.py`:

```bash
multica skill import --file ./build/multica/skills/review-paper.zip --output json
multica agent skills add <agent-id> --skill-ids <skill-id> --output json
```

Repeat import for the selected method archives. Replace IDs with the returned or inspected workspace objects. CLI 0.7.1 accepts `.zip` and `.skill`; its default import conflict behavior is `fail`. Inspect an existing skill before choosing an update policy. `add` preserves existing agent bindings; `set` replaces them.

Each archive has `SKILL.md` at its root and preserves the linked references and templates. A single-file `skill create --content-file` command would omit this supporting content. `build/multica/bundle.json` is a local inventory of hashes and resources, not an importable Multica configuration schema.

## Equip the Paper Reviewer

Attach `review-paper` and supply a PDF capability in the **worker's actual runtime**: searchable text extraction, page rendering, and a model/viewer able to inspect the rendered pages. Use existing PDF tools where adequate. Consider the public OpenAI PDF skill or a platform-provided PDF skill where supported; Docling's usage skill is an optional addition for structured conversion. Scans may need OCR. See [PDF capability recommendations](../../docs/pdf-capabilities.md) for concrete sources, dependency distinctions, and licensing boundaries.

Verify access to a representative digital paper, a difficult table/equation, and a scanned document if scans are in scope. An import alone does not install Poppler, OCR, libraries, or visual capability. Check page references, extracted values, claims versus observations, and the reviewer's ability to continue an exploratory follow-up without forcing an implementation proposal.

## Add coordination when needed

```bash
multica squad create --name "Engineering Practice" --leader <lead-agent-id> --output json
multica squad member add <squad-id> --member-id <specialist-agent-id> \
  --type agent --role "Owns data exploration and evidence analysis" --output json
```

Choose the [preset and roster](../../README.md#squad-rosters), then repeat member addition for its specialists using their existing agent IDs. Paste the complete generated `build/multica/squads/<profile>.md` into that squad's Instructions. The generated file already combines shared coordination with the selected loop. `build/multica/squad.md` is a compatibility copy of the default mixed profile. Do not paste only the source preset: its shared coordination is a separate source file.

**Multica documents that squad instructions reach only the leader.** The Lead must send the relevant terminology definitions, actual criteria, inputs, stop conditions, and return route with each worker assignment. Do not embed the whole squad policy in every agent to compensate. Multica supplies its own leader protocol: delegate, record an evaluation, stop after dispatch, and leave the parent `in_progress` until overall delivery reaches `in_review`. Do not duplicate that machinery with a second scheduler. See [squads](https://multica.ai/docs/squads).

Complete [project context](../../templates/project.md) in a private Multica project description or runtime-accessible file linked from each issue. Record actual agent/Lead/squad UUIDs, exact mention links, accessible workspace/evidence paths, and one return issue/thread. Direct specialists answer the requester; they can identify a useful handoff without automatically launching a squad. When coordinated work is requested, use the configured squad assignment/mention so the Lead receives its policy and roster. Calling Lead directly is suitable for framing and planning; coordination through that route also needs an explicit policy and roster. Never guess IDs or commit workspace configuration here.

For squad workers, include the actual return issue/thread and this instruction in the assignment: “Post one plain result comment with the result/candidate, relevant criteria or findings where applicable, evidence, and limitations; do not add a routing mention to acknowledge completion.” Define any supplied IDs in the assignment or its accessible source. The runtime can wake the leader from that result. A leader invited onto another assignee's issue through a squad mention does not change that issue's status. The [leader loop guide](../../docs/leader-loop.md) distinguishes these callbacks from the prompt-managed repair budget.

## Run a bounded pilot

1. Read back each agent, its skill bindings, and the squad roster in the UI or with `agent get`, `agent skills list`, `squad get`, and `squad member list`, using `--output json`.
2. Create a parked `backlog` issue with the question/objective, inputs, authority, resource envelope, and learning checkpoint or delivery acceptance boundary. Explain that the two-failed-repair rule concerns an identified defect, not discovery iterations. Set ownership using `multica issue assign <issue-id> --to-id <agent-or-squad-id> --no-start`.
3. Inspect `multica issue runs <issue-id> --active --output json`. With no equivalent work active, launch the parked assignee once using `multica issue status <issue-id> todo`. Do not add a launch mention. Subsequent ownership/status bookkeeping uses `--no-start`. Assignment while still in `backlog` does not launch work. See [assignment behavior](https://multica.ai/docs/assigning-issues).
4. For squad work, send one clear handoff per owner. Members report evidence, limitations, and useful next inquiry or decision; ordinary result comments can already wake the leader. Avoid acknowledgment mentions and repeated dispatches.
5. Read back runs and results. Check useful exploration, evidence quality, design reasoning, delivery acceptance, handoff value, and unnecessary turns before expanding. A successful run status alone is not acceptance. Pilot at least an open inquiry and a consequential engineering change so brevity is not mistaken for quality.
