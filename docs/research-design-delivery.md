# Work across research, design, and delivery

Use three distinct squads when those contexts help you think and hand off work. Enter at the stage that matches the actual uncertainty, and return to earlier evidence when necessary. Membership makes expertise available; it does not require running every member.

| Stage | Question it answers | Useful result | What may happen next |
| --- | --- | --- | --- |
| Open research | What do we understand, and what is supported by the evidence? | Human-reviewable study/discussion summary with findings, mechanisms, alternatives, limits and recommendation. Full seven-section reviews for each paper; requested empirical work accounted for separately. | More inquiry, a justified conclusion, an experiment, or a design assignment. |
| Engineering design | What should we build, why, and how will useful increments work? | PRD, architecture and decisions, MVP roadmap with exit evidence, current readiness gate, and remaining assumptions. These may share one living document. | Focused investigation, a bounded spike, delivery, or a decision not to build. |
| Software delivery | Can we implement and independently verify that slice under the intended conditions? | Validated upstream PRD/design/roadmap, a specific candidate, actual checks, scoped independent review, operating evidence, and remaining limits. | Repair, revisit an affected design, another slice, or an authorized release. |

The mixed Research and Engineering squad remains useful when you want continuity in one task. The same specialists and methods support either arrangement. Analytics to Engineering remains a focused entry point for data-led improvements.

Choose roadmap planning or a quick MVP test before routing an ambiguous general task. Changing squads is optional. Roadmap execution uses the [phase and human checkpoint rules](workflow.md#required-engineering-phases): approve the concrete scope/approach, approve the numbered roadmap before creating its backlog, then authorize the named implementation milestone. Existing explicit approvals can satisfy these decisions. A selected quick MVP uses a compact demonstration brief, and a tiny correction inherits its existing contract. Large roadmaps create approved gated children before implementation; explicitly requested early drafts remain proposed backlog records. Keep detailed work in children and milestones/human decisions on the parent.

## Give explanation its own owner

The **Product Manager** is a separate agent you can call for a quick rundown at any stage. It connects the work to a stakeholder need and project objective, explains the proposed behavior and tradeoffs, and distinguishes what is known, designed, built, tested, or still uncertain. It can deepen a concept with a concrete example when asked. Internal R&D work does not need a commercial launch plan to benefit from this role.

| Role | Owns |
| --- | --- |
| Product Manager | Why the work matters, whose workflow changes, product scope and acceptance perspective, and an understandable explanation of current evidence/design/progress. |
| Systems Engineer | Domain model, system design, interfaces and consequential tradeoffs. |
| Software Engineer | Authorized implementation, experiments and developer tests. |
| Test & Code Review Engineer | Independent software correctness and test effectiveness. |
| Verifier | Independent assessment of the particular design decision, scientific claim, measurement or readiness-evidence question assigned. |
| Lead | Choosing the useful next contribution, maintaining task state, routing handoffs, and assessing whether the requested transition is supported. |

An independent explaining role is not automatically an independent technical approval. Product Manager can challenge unclear scope or unsupported claims, but a persuasive summary does not verify them. Likewise, explaining a Systems Engineer's design does not grant authority to rewrite it or accept it for production.

Product Manager is available in Engineering Design, Software Delivery, and the mixed squad. Engage it when the user requests a walkthrough, stakeholder value/scope is unclear, or a design choice needs to be understood for a decision. It is optional at other times. A clear bug fix needs no product presentation, and a fresh explanation is not required after every worker return.

## Make design explicit without freezing the roadmap

Engineering Design starts a bounded scope/approach proposal with one Systems Engineer, who can include the concise need and acceptance statement. Add Product Manager only for a named stakeholder/scope gap or a requested explanation, using that proposal as input. If stakeholder framing must come first, resolve it before commissioning technical design. Avoid parallel drafts of the same proposal and repeated Lead paraphrases; return one integrated proposal at the decision checkpoint. Verifier addresses a distinct consequential uncertainty when needed.

Before handing a slice to delivery, establish:

- The intended stakeholder/system outcome and useful end-to-end scope.
- The selected approach, relevant alternatives, rationale, interfaces, and invariants.
- Observable acceptance and a feasible validation route for the slice.
- Evidence supporting consequential assumptions, with applicable review and remaining limitations.
- Which unknowns block implementation, which are accepted assumptions, and which belong to later increments.
- The receiving owner, actual input references, resources, authority, and return destination.

Maintain these decisions in the [living engineering brief](../templates/engineering-brief.md) or clearly named existing PRD/design/roadmap sections. The [design brief](../skills/design-solution/templates/design-brief.md) supports the architecture method. Put canonical documents in the supplied project directory and explain the design substantively in chat with exact links, decisive evidence excerpts, and a useful diagram or summary table when it clarifies the decision. A task list or attachment inventory cannot stand in for this review surface. “Ready to implement” concerns the selected proposal; it does not mean code or release evidence has passed verification.

Keep the roadmap aimed at the intended production environment, with each increment delivering useful behavior and explicit evidence. Reopen the affected decision when a premise fails or the objective changes; do not defend a stale design simply because it was accepted earlier. Preserve the evidence and repair history still relevant to the problem.

## Choose where to start

- **Understand a paper, mechanism, or topic:** call Paper Reviewer or Scout directly; use Open Research for coordinated inquiry.
- **Explain the current project or design:** call Product Manager directly. It should inspect the relevant artifacts and answer, not launch a new design project.
- **A promising idea with unresolved behavior or architecture:** use Engineering Design. Supply research evidence if it exists; design can also start from a user need or existing code.
- **A known defect or accepted feature:** use Software Delivery. A qualifying correction uses the quick route; a substantive feature must have valid PRD/design/roadmap gates even when they are completed within that squad.
- **A substantial design whose purpose or assumptions change during delivery:** return the affected decision to design/research while preserving unaffected work.

## Carry evidence across squads

Changing squads is an explicit handoff, not an assumed runtime chain. The outgoing Lead records the current result and revision, applicable evidence and limits, decisions/criteria, blocking questions, relevant repair history, and the next scoped objective. The receiving Lead checks that this context is accessible and chooses only the work still needed.

Use one actual destination and one supported dispatch/assignment route. Check active work before launch. Reuse the current issue if the runtime preserves the necessary context and ownership; otherwise create/link the receiving issue under the user's existing authority. A new issue is not a fresh evidence or repair history. Missing callback configuration must be resolved rather than inferred. The installer creates squad configuration; it does not automatically start the next squad.

Assigning a newly created issue to a squad hands delegation to its owning Lead. The creation run stops there instead of also mentioning specialists. The owning Lead checks prior assignment comments and queued/running work before using one dispatch route.

## Example requests

**Direct explanation:** “Product Manager, give me a quick rundown of this design: what user problem it addresses, how it works in one concrete scenario, why this approach, what is already implemented, and the main unresolved decision. Use the linked design and code; do not start other agents.”

**Design assignment:** “Engineering Design: use these findings and the current repository to propose the first useful slice. Explain its project fit, compare credible approaches, define the important interfaces and acceptance checks, and identify blockers. Return a buildable proposal; implementation is a later assignment.”

**Delivery assignment:** “Software Delivery: implement the accepted slice from this design revision. Reuse its rationale and criteria, inspect the current code, and obtain independent verification of the substantive change. If a key design assumption fails, report the affected decision and evidence rather than silently changing scope. Request Product Manager's rundown only if it would resolve a comprehension or scope gap.”

Test these three request types separately in the pilot, then test one cross-squad handoff. Check whether the same specialist respects its current task and whether optional explanation remains optional. This guide describes intended behavior; it is not evidence of a successful live Multica run.
