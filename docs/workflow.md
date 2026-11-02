# Working rules and decision gates

Identify whether the work needs discovery, empirical validation, delivery, or some combination before choosing the agent chain. For open inquiry, start with a provisional question and a useful learning checkpoint. For delivery, define the observable acceptance boundary. Keep the current question or task, artifacts, and evidence in one authoritative record. Use [the task template](../templates/task.md) to preserve consequential context.

This page explains the supplied squad policies. Select the [squad roster](../README.md#squad-rosters) that fits the recurring work, or call a specialist directly. Direct calls use their task's scope and stopping conditions; they do not silently start this coordination loop.

Use the [stable terminology](terminology.md) where engineering work benefits from durable references; open research can use a natural task-specific structure. The squad passes only relevant conventions and IDs. See the [leader loop](leader-loop.md) for event-by-event routing and a worked repair counter.

## Human-readable output and local documents

Return the useful answer and evidence highlights in the responsible Multica thread: detailed child results there, integrated milestone/final synthesis on the parent. Use compact tables, code/data excerpts, or visuals in the comment when they clarify the result. Keep canonical documents and raw evidence in the supplied directory with exact links. Attach a focused chart, snippet, or evidence extract when it makes review or reuse easier; do not upload a whole report, dataset, or source tree instead of explaining the result. If a local link is inaccessible, include the necessary content inline and use a focused accessible evidence item where helpful.

Substantial inquiry ends with a coherent research/discussion summary, and substantial design ends with a design document suitable for human review. A paper review uses the full seven numbered sections per paper unless the user explicitly narrows it; a final synthesis does not replace them. Documents preserve reasoning for reuse, while inline responses make it understandable now. Progress updates can be short; final deliverables must meet the requested depth.

## Required engineering phases

For a general task whose mode is unclear, offer **Roadmap plan** versus **Quick MVP test**, with a recommended first deliverable, estimated effort and tradeoff. Wait for that choice before dependent implementation; honor explicit mode and execution authorization without asking again. A clear explanation, review or correction does not need this choice.

A **quick MVP test** uses the [compact brief](../templates/quick-mvp.md): question, included/excluded behavior, assumptions/interfaces, demonstration or measurement, necessary checks, owner, budget and stop point. It permits new isolated prototype code and stops with evidence and the next decision. Required review covers that claim; a full product roadmap is not a prerequisite. It does not authorize migrations, live operational changes or other consequential external effects.

**Roadmap planning and execution** use the phases below for durable capabilities, integrations and consequential operating changes. For a new substantial system, first present a concrete scope/approach proposal and wait for human approval before elaborating its dependent design. Then present the numbered roadmap for human approval before creating the live backlog. Implementation needs the user's authorization for the named milestone, budget and stop point; return its evidence at the next reserved human checkpoint. The user may approve multiple named milestones in advance. Reuse real prior approvals without asking again. Technical readiness remains separate from these human decisions; not every phase row needs a separate approval.

The scope proposal explains the user workflow, actual behavior and exclusions, proposed engine/libraries or reuse, credible alternatives, important assumptions and effort implications. Review this before spending repeated technical-review rounds on a speculative model. An explicit request for early draft children permits proposed backlog records only; it does not accept their design or authorize implementation. Silence, a callback, a technical PASS or a request for more explanation cannot approve scope. Preserve the decision source, timestamp, exact scope/revision, allowed next action and budget in the parent. See the deployable [human checkpoint policy](../squads/common.md#human-decision-checkpoints).

Use one [living engineering brief](../templates/engineering-brief.md), or equivalent named sections in the project's existing documents. A development task list alone cannot satisfy the first three phases.

| Phase | Required review surface | Exit evidence |
| --- | --- | --- |
| Requirements / PRD | Stakeholders and problem, goals/stories, scope/non-goals, functional requirements, domain rules, measurable acceptance and operating envelope, metrics, questions and risks. | Current slice is understandable; consequential unknowns have explicit decisions, owners or blockers. Assumptions are labeled with the scope they permit. |
| Architecture / design | System boundaries and components, data/control flow, interface and failure contracts, credible alternatives, rationale and consequential decisions, feasibility limits. | Design explains how the accepted behavior will work; required independent assessment covers consequential claims/contracts. Product and technical assumptions agree. |
| MVP roadmap / implementation readiness | Demonstrable increments from learning prototype to useful MVP and intended operating target; each has scope, dependencies, acceptance, verification, owner and revisit condition. | Selected slice has a buildable design and feasible checks; blocking questions are resolved. A spike may resolve a named uncertainty but does not pass the product gate. |
| Implementation | Versioned candidate and focused checks traceable to the selected slice. | Candidate is ready for the assigned independent review; code completion is not release approval. |
| Independent verification | Exact candidate, assessed criteria, evidence and findings; requested outputs checked separately from correctness of a subset. | Blocking findings for the selected transition are closed; remaining exclusions and gaps are explicit. |
| Acceptance / readiness | Current deliverables, remaining roadmap, target-specific operating evidence and accountable decision. | Requested scope is complete for the named target and accepted under existing authority. Release still respects any reserved human decision. |

Record `phase | candidate/artifact versions | gate | criteria passed/blocked | open decision + owner | next transition + owner`. The Lead advances only when this record is supported by evidence. A narrow technical PASS does not accept an unspecified performance target or complete an unexecuted benchmark. Changed requirements/design invalidate only the affected evidence and gates.

### Child issues and bounded execution

A roadmap with multiple independently verifiable outputs, parallel implementation owners or milestone dependencies requires actual linked [child issues](../templates/work-package.md) before implementation, after the human approves the proposed map. Each child has an outcome, owner/write boundaries, explicit dependencies and parallel siblings, criteria/reviewer, human approval reference, budget and activation gate. Use `[MVP01-SUB01]` within approved MVP groupings or `[SUB01]` for a flat backlog; preserve stable numbers and Multica IDs. Create unstarted children in backlog. Mark explicitly requested early drafts as proposed and awaiting approval. Check technical evidence and human execution authority before activation, even when the platform supports stages. Waiting for approval is an intentional checkpoint; a creation capability failure is a different blocker. Do not claim a proposed map is a created backlog.

The parent stores the goal, mode, child index, milestone state, total budget and decisions. Implementation, full review findings and repairs belong to children. Send the parent milestone outcomes, material blockers and final synthesis rather than copying every return. Parallel children need separate write targets and an integration owner. Completion includes the integrated user workflow, not merely closed children.

Bound each author/review/repair package by a concrete task-appropriate time/compute or run budget. Lead can choose a modest bound inside existing authority, making it visible before dispatch. Track consumption across partial returns and new findings; checkpoints and restarts cannot reset the allocation. At the boundary, report evidence and remaining work, then finish or explicitly replan within remaining authority. The repair counter below is an additional limit, not the only bound on implementation. Label user-required, inherited, provisional and optional constraints so invented hardening cannot silently enlarge the request.

### Quick corrective route

Use this only for a small correction restoring already specified behavior, with no new product scope, architecture, public contract, data semantics, migration, or consequential operational change. Record why it qualifies, the existing criterion, reproduced defect, affected code, focused checks and applicable independent review. A one-file change can still require the full route. Missing requirements are not a reason to call work a quick fix. If inspection exposes broader design uncertainty, switch to the full route before dependent implementation.

For a known defect with an existing criterion and reproduction, Lead can authorize one conditional inspection-and-repair assignment. Record the proposed route and exclusions; the worker documents evidence that every eligibility condition holds before editing, or stops and returns the unresolved decision. Lead confirms the route from that evidence on return. This permission applies only to the corrective route; substantive implementation still needs the required Lead gate decisions first.

### Exploration and partial completion

Open research has learning checkpoints rather than mandatory product phases. For paper-review requests, including "review and benchmark these papers," the initial benchmark compares evidence reported in the papers: cite locations, task/workload, hardware, baselines, metrics, and limits. No algorithm/harness coding, implementation setup, author-code execution, or tests follow from that wording. PDF extraction/rendering and document preparation remain reading aids. Deliver the review/comparison, then let Lead propose a bounded technical benchmark and ask the human whether to proceed. Reuse clear existing human authorization for technical execution. Track that execution separately only when authorized; a proposed future run does not make the completed review partial.

## Work modes

| Mode | Complete when | Typical owner |
| --- | --- | --- |
| Exploration / topic search | At a checkpoint, explain what was learned, competing frames, useful branches, and source limits. Continue or conclude according to the inquiry; the question can evolve. | Scout |
| Paper explanation / review | The requested mechanism, novelty, or evidence question is answered at the appropriate depth. | Paper Reviewer |
| Analytics | Findings and calculations are reproducible; distributions, missingness, alternative explanations, units, and limits are clear. An exploratory checkpoint can open further analysis. | Analyst |
| Product/design explanation | The requested audience can follow the need, mechanism, project fit, tradeoffs, actual state, and material uncertainty; understanding is not claimed without feedback. | Product Manager, on demand |
| Engineering design | The current slice's behavior, critical contracts, options/rationale, and validation route are coherent; blocking assumptions and required design review have been addressed. | Systems Engineer; Product Manager and Verifier when their contribution is needed. |
| Experiment | A bounded method yields a supported, unsupported, or inconclusive conclusion with trustworthy evidence. | Analyst; Software Engineer if implementation is substantial |
| Prototype | The chosen design or feasibility question has a useful answer; checks establish that the answer is credible. | Software Engineer |
| MVP / maintenance | A narrow, useful behavior meets its acceptance criteria and applicable independent verification. | Software Engineer; Lead routes Test & Code Review Engineer review. |
| Release preparation | The specific candidate has the evidence required for the actual deployment target and an accountable release decision. | Software Engineer and qualified reviewer; Lead coordinates in squad mode. |

These modes can share the mixed squad, or have separate presets with distinct loops. A specialist can change methods for ordinary supporting work. Within a squad, the Lead coordinates ownership and return routes. On a direct request, the specialist returns its result and identifies any further expertise or independent review needed; it does not assume authority to dispatch a team. A mode change that materially changes scope, cost, authority, or the promised result requires a decision under the existing task authority.

## Three kinds of loop

| Loop | What advances it | What a checkpoint means |
| --- | --- | --- |
| **Discovery and design** | New evidence, stakeholder needs, contradictions, models, or alternatives. | Summarize learning; deepen, broaden, reframe, synthesize, or conclude. Keep worthwhile branches visible. No predetermined success claim or iteration count is required. |
| **Empirical learning** | A valid observation that discriminates among explanations or tests a transfer claim. | Judge measurement validity separately from the hypothesis. A negative or inconclusive result may guide another study within the agreed resource envelope. |
| **Defect repair** | A candidate addressing an identified blocking finding, followed by verification. | Close the finding or count an unsuccessful repair. The two-round rule below applies to this loop. |

The leader selects the loop appropriate to the evidence, rather than interpreting every return as PASS or FAIL. Discovery may include several specialists when different perspectives add value. Use [problem framing](../skills/frame-problem/SKILL.md) for needs, system models, and options; [investigation](../skills/investigate-question/SKILL.md) for sources; [analysis](../skills/analyze-data/SKILL.md) for data. Templates support the reasoning and need not dictate every answer's headings.

A learning checkpoint is normally an agent's synthesis and next-action decision, not a request for user permission. Continue authorized work while the direction remains useful. Surface a decision when scope, material resources, authority, or an agreed pause boundary changes. A broad inquiry still needs an agreed resource envelope for substantial execution; this is distinct from requiring a narrow answer in advance.

## Inquiry → experiment → MVP

For a substantial idea, [Research → Design → Delivery](research-design-delivery.md) makes the engineering decision explicit between evidence and implementation. Enter at any appropriate stage. A separate design squad is optional when the delivery task already has a sound design; Product Manager's walkthrough is available without becoming a mandatory gate.

An inquiry may stop with understanding. If an experiment is selected, pass the question, relevant sources and contrary evidence, assumptions, comparator, operating conditions, and budget. Define the observations that would change the decision before expensive execution. Keep raw data, executable analysis, and exclusions.

Check the experiment's validity independently before relying on a consequential claim. A correctly executed experiment can reject the proposed method. Repair invalid execution; do not treat an inconvenient scientific result as a defect to remove.

When evidence supports an MVP, hand over the claim and its limits, code/data/config identity, required invariants, and engineering acceptance criteria. Select one end-to-end capability. Establish useful module boundaries around today's interfaces and replaceable decisions. Keep a short roadmap of later operating requirements; implement them when the target requires them. Prototype code can be retained or replaced based on evidence about its fitness.

Pivot when the hypothesis fails, the operating requirement changes, or a better-supported approach meets the need. Record the reason and reuse unaffected evidence. A pivot does not erase repair history or authorize a larger budget. Full product discovery, pricing, marketing, or GTM starts only after an explicit scope decision.

## Independent verification

Require a separate qualified check for substantive code changes, consequential scientific claims, and release readiness. Substantive changes affect behavior, interfaces, data integrity, concurrency, failure handling, or operation. A scientific claim is consequential when it is used to select a method, justify performance or correctness, or guide deployment. For uncertain cases, judge impact rather than diff size.

Minor edits, focused explanations, and exploratory notes receive appropriate author checks. They do not automatically need another agent. A broad or high-stakes domain judgment may need a human specialist; naming an agent Verifier does not establish competence.

The author supplies the candidate and checks. The assigned Test & Code Review Engineer or Verifier returns PASS, FAIL, or BLOCKED for a specified transition, with consolidated findings and closure conditions. State whether prior checks covered the method, implementation, scientific conclusion, or release readiness; a method PASS alone does not approve an adoption claim. A review never approves changes the same reviewer authored. Verify affected changes on repair, retain valid evidence for unchanged inputs, and stop once accepted criteria are met. Keep suggestions accompanying PASS as optional follow-up rather than dispatching another development/review round. If Lead challenges PASS, it must name an unmet accepted criterion and evidence before reopening the affected scope.

## Two-round repair rule

This is the supplied squads' coordination policy. It is stored in `squads/common.md` and transmitted with repair assignments; reusable agent prompts and skills do not hardcode it.

Initial review identifies the problem; it is not a repair round. An attempted fix followed by unsuccessful verification of that same problem counts as one unsuccessful round. Track the problem and its counter across runs, agents, and task renames. Classify unavailable infrastructure as a blocker rather than inventing a scientific failure.

Ordinary initial edit/test cycles, exploratory branches, valid negative experiments, and a revised research question do not increment this counter. Preserve scientific uncertainty instead of turning it into an artificial defect to close.

After two unsuccessful rounds, report the evidence, suspected blocker, and smallest next decision. Stop repeating the approach. The coordinator may choose a materially different approach within the agreed scope and remaining task budget, recording its rationale and keeping the earlier failures visible. Repeating the same approach requires user steering. If budget is missing for substantial additional execution or has been exhausted, obtain that decision before continuing. Changing agents or restarting context does not reset the budget.

## Readiness depends on the operating target

The letters below describe environments, not universal maturity scores. Choose the actual target and measurable acceptance conditions at task start; later promotion needs new evidence. A and B can prepare for C, but not every project must reach C.

| Target | Evidence to establish for this project | Decision owner |
| --- | --- | --- |
| **A — Internal tool or service** | A useful user path; data correctness; relevant tests; reproducible setup; suitable access controls; representative workload; observable failures; recovery or rollback appropriate to state; maintenance/run instructions and an owner. | Internal service owner accepts the declared operating envelope. |
| **B — Integrated operational pilot** | A evidence plus actual interface and compatibility checks; representative dependency failures; isolation and bounded exposure; monitoring and stop criteria; exercised recovery/rollback; pilot users, duration, and success thresholds. Use a representative staging or shadow environment before introducing operational effects. | System/integration owner authorizes the bounded pilot. |
| **C — Live industrial operation** | A/B evidence applicable to the target plus domain-specific hazard and failure analysis; validated operating envelope; required protective mechanisms and safe-state behavior; operational commissioning, intervention, and recovery evidence; traceability and qualified operator/engineering review. Where applicable, identify the governing standards and required assurance process before designing the release gate. | Accountable operational/domain authority authorizes the specific candidate and rollout conditions. |

Select checks based on actual hazards and consequences. This starter supplies a workflow, not a safety certification or universal industrial acceptance checklist. A simulation result or successful pilot alone cannot establish readiness to control live equipment. Evidence gaps remain visible as gaps; a prompt's PASS label cannot resolve them.

Prepare the release candidate and evidence before requesting the release decision. Do not repeatedly ask about already authorized checks. Passing verification does not expand permission to deploy, mutate operational data, or actuate equipment.

## Keep coordination inexpensive

Maintain one current state and one owner per work target. Send precise input links, the question or acceptance boundary, an appropriate checkpoint, and one return route. Use parallel workers for independently ready work or valuable complementary perspectives. Check active work before dispatching. Preserve useful depth in linked evidence while avoiding repeated full reports, duplicate acknowledgments, a reviewer for every specialty, and polishing without a purpose.

The deployable squad instructions carry this decision policy; this guide is explanatory and is not uploaded by the installer. The starter does not implement durable locks, enforced counters, or a scheduler. Verify actual instruction delivery, dispatch, completion, and accounting in a small Multica pilot before relying on them. Track useful output, repair causes, unnecessary handoffs, repeated context, and actual usage where available. Improve a demonstrated failure before adding another role or rule.
