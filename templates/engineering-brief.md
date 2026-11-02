# Living engineering brief

Keep this in the project directory. It can combine the PRD, architecture and roadmap in one readable document, or index existing authoritative documents. Replace placeholders with real decisions/evidence. Keep stable IDs for applicable records using the squad convention; do not invent entries to fill every category. An implementation task list supplements this brief.

## Current state and review index

- Current phase and intended transition:
- Brief/candidate/repository revisions:
- Current PRD, design, roadmap and verification links:
- Gate: passed / blocked / not assessed, with criteria and evidence:
- Unresolved decision, owner and consequence:
- Next action, owner and authority:
- Selected mode and execution authority: roadmap plan or roadmap execution; use the separate [quick MVP brief](quick-mvp.md) for an isolated demonstration:
- Parent issue, total budget and current milestone/child links:

## Human decisions

Present a concrete scope/approach proposal before dependent detailed design, then the numbered roadmap before live child creation. Explain intended behavior, exclusions, engine/libraries or reuse, alternatives, assumptions and effort. Separate technical PASS from human approval. Preserve an existing explicit approval without asking again.

| Decision | State | Human source and timestamp | Exact scope/revision | Permitted next action, budget and stop point |
| --- | --- | --- | --- | --- |
| Scope and approach | Proposed / approved / changes requested | Actual user instruction | Proposed behavior and approach | Detailed design within that direction |
| Roadmap and backlog | Proposed / approved / changes requested | Actual user instruction | Numbered map and dependencies | Create approved backlog; early drafts only if explicitly requested |
| Implementation milestone | Proposed / approved / changes requested | Actual user instruction | Named MVP/children and design | Bounded execution, then reserved human review |

Use `[MVP01]` for a demonstrable milestone and `[MVP01-SUB01]` for its child outcomes, or `[SUB01]` for a flat child map. Include explicit dependencies and parallel siblings; stable title numbers do not replace issue identities or dependency gates.

## PRD — problem and expected behavior

Explain the stakeholder's current problem and the useful outcome in plain language. Distinguish observed needs, user instructions and assumptions. Identify scope/non-goals and intended operating target.

| Record | Statement | Provenance | Evidence or rationale | Priority / scope |
| --- | --- | --- | --- | --- |
| G-… / U-… | Goal or stakeholder story | User / inherited / provisional | Source of need | Current or later |
| FR-… / BR-… | Required behavior or domain rule | User / inherited / provisional / optional | What depends on it | Current or later |

| Criterion | Related requirement/rule | Observable check and acceptance threshold | Environment / data | Evidence status |
| --- | --- | --- | --- | --- |
| AC-… | Relevant IDs | Include normal and consequential failure behavior | Defined scope | Planned / observed / independently checked |

Define consequential units, workload, concurrency, accuracy, latency/throughput, resource and compatibility constraints. If a value is unknown, record the decision rather than inventing acceptance. KPI records define unit, population, window and baseline; a decisive threshold belongs in an AC. A bounded learning prototype may investigate an unknown without claiming it has met it.

## Architecture — how the behavior will work

Explain the system boundary, component responsibilities and data/control flow. Include a diagram when it clarifies the mechanism. Specify interfaces, schemas, units, invariants, state ownership, failure/recovery behavior and relevant integration/operating constraints. Trace important choices to the PRD.

| Decision | Credible alternatives | Selected approach and evidence | Costs / limits / revisit condition |
| --- | --- | --- | --- |
| ADR-… | Include a simpler existing option when viable | Explain the tradeoff | What would change the decision |

Work through a representative request or scenario from input to output, including a consequential failure case. State which claims are supported, which need a spike, and which need independent qualified review. Do not call a design verified merely because its author checked it.

## MVP roadmap — demonstrable increments

Each increment delivers useful behavior or answers a named uncertainty. Start with a bounded slice and show the route to the actual intended operating target; later scope stays revisable. Do not substitute a list of modules to code for outcomes and exit evidence.

| Increment | Outcome and scope | Dependencies / owner | Exit criteria and verification | Next decision / revisit trigger |
| --- | --- | --- | --- | --- |
| Learning prototype, if needed | Named uncertainty | Inputs and resources | Valid observation that resolves or bounds it | Continue / redesign / stop |
| Useful MVP | End-to-end stakeholder behavior | Accepted requirements/design | Applicable ACs and independent checks | Accept scope / next increment |
| Intended operating target | Maintenance/integration/rollout scope | Environment and accountable owner | Representative operation, observability, recovery and target-specific evidence | Authorized rollout or remaining gap |

Remove inapplicable sample rows and add actual increments. No commercial/GTM expansion is implied. Identify the selected slice, implementation plan and permitted resources only after its readiness criteria are satisfied.

For multiple independently verifiable outcomes, parallel owners or milestone dependencies, create actual [child issues](work-package.md) under the available authority before implementation. Planning-only work leaves them in backlog. Record the result of creation, not placeholder IDs:

| Child issue link | Output / owner | Dependencies and stage | Acceptance / reviewer | Work budget / remaining | Gate decision and evidence |
| --- | --- | --- | --- | --- | --- |

Activate only ready, authorized children. Keep detailed implementation and reviews there; update the parent for milestones, blockers and decisions. Check integrated acceptance before completing the overall request.

## Questions, risks and review findings

| Record | Evidence / question | Blocks which action? | Owner and resolution / closure condition |
| --- | --- | --- | --- |
| OP-… | Unresolved choice or missing knowledge | Named gate or nonblocking | Decision/evidence needed |
| RISK-… | Plausible adverse outcome, with mechanism | Current or later scope | Mitigation or accepted exposure |
| FINDING-… | Observed problem, exact candidate and reproduction | Violated criterion and impact | Repair, independent closure evidence, attempt history |

Preserve accepted assumptions with their justification, scope and revisit condition. Renaming work or choosing another approach does not erase repair history. A review finding is not a speculative risk, and an unresolved question need not block unrelated progress.

## Gate and deliverable record

| Phase / transition | Exact artifacts and criteria | Passed / blocked / not assessed | Evidence and decision owner | Next owner |
| --- | --- | --- | --- | --- |
| Requirements ready | PRD revision + relevant IDs | Actual state | Evidence | Owner |
| Design ready | Architecture + consequential decisions | Actual state | Review scope | Owner |
| Slice ready to build | Roadmap increment + validation plan | Actual state | Decision and remaining limits | Owner |
| Candidate verified | Candidate + applicable criteria | Actual state | Independent result | Owner |
| Named target accepted | All requested outputs + readiness scope | Actual state | Accountable decision | Owner |

Before a final handoff, account for every user-requested deliverable separately. Planned experiments are not measurements; a smoke check is not a comparative benchmark; a narrow repair PASS does not satisfy unreviewed criteria. Keep required missing outputs partial/blocked until resolved or explicitly descoped.

## Human review summary

Explain what problem is addressed, why this design fits, how it works, what was actually built/tested, the strongest evidence and limitations, and the current decision. Post this substantively in the ticket/chat with exact links to this brief and current evidence. Add a short summary table, code/data excerpt, or visual when it makes the decision easier to review. A final report must be understandable without reconstructing the run history. Keep canonical documents local and attach only focused evidence when it improves inspection or reuse; a full-file upload does not replace the chat explanation.
