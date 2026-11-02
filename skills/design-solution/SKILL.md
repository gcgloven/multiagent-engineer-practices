---
name: design-solution
description: Develop or assess architecture and an MVP roadmap from inspected requirements, with alternatives, interface and failure contracts, phased demonstrations, and validation gates. Use for new systems, integrations, substantive features, architecture changes, or research-to-prototype handoffs; a corrective local fix can reuse its valid design.
---

# Design a buildable solution

## Establish the design question

Determine whether the request is to propose a design, compare options, refine an existing decision, or review a proposal. Read the actual problem, stakeholder workflow, relevant research or measurements, current code/interfaces, operating target, and constraints. Identify the decision this work should enable. A design-only request can finish with a usable decision and handoff; it does not require implementing the product.

Distinguish known behavior, adopted requirements, preferences, hypotheses, and unknowns. Research evidence has an applicability boundary: preserve workload, data, assumptions, contradictory results, and what was actually reproduced. A promising paper or chart does not establish that a mechanism will work in the target system. Clarify consequential missing context while progressing work that does not depend on it.

Identify the selected mode and requirements basis. For a quick MVP test, its compact question/scope/assumptions/interfaces/checks/budget brief supplies prototype design coverage. For durable delivery, changed contracts, data semantics, migrations or operating targets, establish the corresponding requirements and architecture. A tiny correction can inherit a valid contract. Reuse inspected evidence rather than requiring a particular document title.

For substantial work, expose missing stakeholder behavior, acceptance or quality constraints before choosing a production design. Draft a concrete scope/approach proposal within authority, naming the intended behavior, exclusions, credible alternatives and proposed engine/libraries or reuse when relevant. Preserve the caller's human checkpoints: when approval of this direction is pending, return the proposal before elaborating its dependent architecture, ticket breakdown or repair loop. A technical consistency review does not establish stakeholder acceptance or permission to implement. Reuse documented approval without asking again.

## Model behavior before selecting components

Walk a representative user or system scenario from trigger through result. Include a relevant failure or recovery path. Map actors, data/state ownership, domain invariants, interfaces, and external dependencies at a level that exposes decisions. Explain how the proposed behavior improves the existing journey.

Inspect affected code and callers before prescribing a new abstraction. An interface includes inputs, outputs, units, invariants, ordering, errors, and operational expectations, not just function names. Place responsibility where a change can be understood and tested locally. Prefer interfaces that hide useful complexity; do not add a service, plugin framework, or adapter layer for a hypothetical future variation.

Choose depth according to the decision. A corrective local change may need a sketch and interface examples. A new system or substantial feature needs an understandable architecture: system boundary, component/module responsibilities, data and state ownership, external dependencies, and how a representative request traverses them. Include a component/data-flow diagram, state or sequence model when it clarifies those relationships; an equally concrete prose model can suffice. Proposed file boundaries are useful when grounded in inspected code, but a file list is not an architecture.

Specify critical contracts at those boundaries: inputs/outputs and examples, validation and supported domain, identity and units, ordering, error/timeout behavior, retry or duplicate handling, compatibility, and applicable migration/recovery behavior. State which component enforces each important invariant. Define relevant numerical or workload limits before attempting unrestricted correctness or performance claims. Unsupported input needs an observable outcome, rather than silently broadening the contract during implementation.

## Compare viable approaches

Compare alternatives when the choice is consequential or uncertain. Include retaining the present behavior or changing the workflow when credible. Assess user value, correctness, scientific validity, implementation and operating cost, reversibility, maintainability, and compatibility. Explain why the selected option fits the evidence and what would change the choice. Do not invent alternatives to fill a fixed quota.

Use a bounded spike, mockup, calculation, or experiment when it resolves a material uncertainty within the task's authority and resources. State the question and what outcome would change the decision before conducting the probe. Preserve negative results. Label temporary code and simulated inputs; a successful probe is not production verification. If the scope is explanation or design only, do not silently convert it into a delivery assignment.

## Build a demonstrable MVP roadmap

Apply this section when the caller selected roadmap planning or durable delivery and the required scope/approach approval is present. A quick MVP test needs only a bounded demonstration brief and its next decision; do not make a full roadmap a prerequisite. Planning does not authorize execution. For a large Multica roadmap, first present the proposed numbered work packages with dependencies, owner, acceptance/reviewer, budget and human decision points. Follow the caller's backlog approval gate and title convention before creating real children; an explicitly requested draft backlog remains visibly proposed and unstarted. If approval is pending or the caller owns creation, return the map and next decision. Do not claim prose rows are created issues. Keep detailed work in children and the overall decision/coverage in the parent.

Describe a **useful end-to-end MVP**, its accepted inputs and failure behavior, affected interfaces, and observable acceptance. An exploratory spike can precede it when needed, but distinguish answering a feasibility question from delivering usable behavior. For work intended to evolve, show a short path from this first outcome to the specified pilot, internal service or production target. Do not add commercial launch or deployment work absent from the objective.

Each increment states the capability a user or system can demonstrate, included/excluded scope, prerequisite decisions, responsible owner, verification evidence and exit condition, and the next authorized decision. A list such as “build API, add tests, deploy” is an implementation checklist; it does not explain what becomes usable or why progression is justified. Group work by observable outcomes and uncertainty. Later increments may remain conditional, with a trigger for revising or discarding them.

Define applicable phase gates from the caller's workflow: for example requirements accepted for the named scope; design coherent and ready for the slice; behavior independently verified; readiness demonstrated for the actual target. Name evidence and decision ownership, not automatic approvals or an all-agent sequence. Inspect existing valid evidence to satisfy a gate instead of recreating it. A missing future implementation result is not a design defect, but the plan must say how that result will be established.

Define applicable measurement and operational needs early: baseline and comparison conditions, security/data constraints, representative load, observability, recovery, migration, and rollback. Apply only the dimensions relevant to the target. An internal offline prototype and a live service need different evidence. When an acceptance threshold is unresolved, record the proposed measurement and the owner decision needed; collecting a measurement alone cannot pass that acceptance gate.

Separate unknowns that block the first slice from explicitly accepted temporary assumptions and later work. Assign an owner and next probe to a blocker. State a readiness assessment for the named slice: requirements basis, architecture/contracts, demonstrable scope, validation route, required reviews and accepted assumptions. Record missing evidence and which work remains authorized. Resolve routine decisions within existing authority; obtain steering only where a consequential choice exceeds it. Design readiness does not certify code correctness or release readiness.

## Explain and hand off the decision

Use the [architecture and MVP design brief](templates/design-brief.md) for substantial design or a cross-owner handoff. It can extend one existing project record; mark genuinely inapplicable parts with a reason rather than omitting consequential requirements or design decisions. Explain the design through a concrete journey: need → behavior → mechanism → tradeoff → demonstrable increment → validation. Preserve the caller's terminology and identifiers; this method defines no project numbering convention.

Maintain the current design, roadmap and decision status in a canonical local project artifact or the caller's chosen authoritative record. Post a substantive chat summary of the proposed architecture, key tradeoff, phase/gate status, next usable increment and open decisions, with links to the exact artifact/evidence. Include a compact comparison table, interface/code excerpt, or diagram in chat when it helps; attach a focused visual or excerpt when it materially improves review or reuse. Do not use a full-file upload instead of the explanation. Ordinary revisions update the canonical record and report the delta.

Return the design revision, selected and rejected options, rationale, unresolved limits, implementation boundary, and intended validation. If a review is assigned, the reviewer assesses the proposal against its evidence and operating constraints and identifies concrete gaps with closure conditions. Missing future implementation results are not failures of a design-only assignment. Use the supplied review route; otherwise state any qualified review still needed and return to the requester without automatically dispatching a team.

Follow the current task's checkpoints and stop conditions. Revisit an affected decision when a key assumption fails; retain valid evidence and explain downstream consequences. Designing alternatives and learning from valid negative probes are not defect-repair failures. This skill does not select the next squad or grant implementation or release authority.
