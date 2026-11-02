---
name: frame-problem
description: Frame ambiguous research or engineering work and develop stakeholder requirements, scope, acceptance, and unresolved decisions. Use for problem exploration, a new-system or product requirements brief, or when evidence challenges the current solution direction.
---

# Frame an engineering problem

## Establish the working situation

Understand what prompted the work, who experiences the problem, how they work today, and what a better outcome would enable. Inspect supplied evidence and existing behavior. A requested implementation is a candidate solution; investigate the need it serves. Internal operators, analysts, and maintainers are stakeholders too.

For a clear accepted defect, inspect and use the existing frame. For ambiguity, select methods from [the method guide](references/design-methods.md). The [frame template](templates/problem-frame.md) captures developing understanding without pretending it is settled.

Establish the intended mode and deliverable. When a general task leaves the preference open, offer roadmap planning versus a quick MVP test with a concrete first outcome and effort tradeoff; honor an explicit choice. A selected quick MVP uses a compact question, scope, assumptions, interfaces, checks, budget and stop point. It can add prototype code without a full product specification. Durable system changes, migrations and consequential operating behavior need an appropriate requirements basis; a tiny correction can inherit an existing contract. Reuse valid work and label user requirements separately from provisional assumptions and optional hardening.

Honor the caller's human decision checkpoints. For an unapproved consequential interpretation, prepare a reviewable scope/approach proposal with intended behavior, exclusions, alternatives, proposed technology or reuse and effort implications. Return it for the assigned human decision before developing dependent details. A selected planning mode, a request for more explanation or a technical review does not approve the agent's proposed product meaning. Reuse a real prior approval; do not ask again for decisions already settled. Ticket creation and implementation remain separate permissions.

## Explore the problem space

- Map actors, decisions, data flows, boundaries, dependencies, and failure consequences. Identify intended versus observed behavior.
- Separate observations, assumptions, stakeholder preferences, and explanations. Challenge overloaded terms and inspect counterexamples.
- Investigate competing frames when they change the solution: a slow workflow might involve computation, poor visibility, queue policy, or repeated manual reconciliation.
- Use relevant sources, task walkthroughs, data exploration, authorized interviews, and informative probes. Record contradictions and unanswered questions. Never invent stakeholder feedback.

A fixed hypothesis, acceptance number, or solution is not required before discovery. A better question or map of competing explanations can be the useful output.

## Turn understanding into usable requirements when a build is intended

Use the [requirements/PRD brief](templates/requirements-brief.md) for roadmap planning and durable engineering delivery. For a quick MVP test, apply only the decisions needed in its compact demonstration brief. Develop enough content for the user or next owner to assess the intended result:

- Who needs the capability, the present journey and evidence of the problem, the proposed outcome, and meaningful non-goals.
- Observable functional behavior, domain/data rules and relevant units, successful and failure/recovery scenarios, affected consumers, and compatibility or migration expectations.
- The intended operating target and applicable quality constraints: for example accuracy, latency, capacity, reliability, data protection or maintainability. A metric needs its workload, measurement boundary, units and target status. “Fast,” “accurate,” or “production grade” alone does not establish acceptance.
- Acceptance conditions and how they can be checked, together with the source and status of each consequential requirement. Distinguish an authorized decision from a proposed assumption, and identify the owner of unresolved choices.

Inspect existing documents, code and evidence for currency, scope and contradictions before accepting them as the requirements basis. A document called “PRD” is not evidence that its choices were agreed; a concise existing issue can be sufficient if it contains the needed decisions. Preserve the caller's identifiers and terminology without introducing a new numbering scheme.

Classify unknowns by the next action they affect. An unanswered product choice can permit a labeled exploratory spike with a question, scope and stopping boundary. It cannot silently become an accepted requirement or evidence of release readiness. Resolve decisions within delegated authority; seek steering only for consequential choices outside it. Useful framing and unaffected analysis can continue while a dependent implementation decision remains open.

## Develop and compare options

When there is enough understanding for a productive comparison, state a provisional frame. Consider the status quo, operational/process changes, changes to the existing system, and new technical approaches when relevant. Generate genuinely different alternatives; do not create straw options to justify a preferred design.

Compare benefits, scientific support, stakeholder fit, compatibility, maintainability, observability, reversibility, operating risk, and resource costs. Mark unknowns rather than inventing numeric scores. Prototype or investigate the assumptions that distinguish credible options. A larger redesign is valid when a local patch cannot satisfy the operating requirements.

## Checkpoint and choose the next mode

At a useful discovery checkpoint, report changed understanding, credible possibilities, the next useful inquiry, and resource implications. Continue exploration or reframe within the authorized objective. Seek a decision when scope, significant resources, or authority changes—not for every new question.

Converge when evidence supports a choice at the current level of consequence. Hand off the requirements basis, behavior, constraints, tradeoffs, uncertainty, and verification approach. Record a consequential decision with its real alternatives and revisit condition using the project's existing format. Exploration can end with synthesis without a build commitment. The caller or active squad determines whether the next action is design, another inquiry or completion; this method does not automatically dispatch it.

Keep the current brief in one canonical local project artifact, or the authoritative record explicitly chosen by the caller. In the result comment explain the substantive outcome, key requirements or changed understanding, evidence, remaining decisions, and next accountable action, then link the exact record/version. Add a concise summary table, quote/code excerpt, or visual when it clarifies the problem or options. Attach a focused artifact when that format materially improves review or reuse; do not routinely upload a full brief or duplicate file instead of explaining it. If the recipient cannot access the local link, include the relevant content inline and attach only the smallest useful evidence item where supported.

## Quality checks

Can the reader distinguish need from proposed solution? Are assumptions and missing perspectives visible? Have credible alternatives been examined against the actual context? Does the next step address meaningful uncertainty or deliverable quality? Have you preserved disagreement instead of manufacturing consensus?

Reframing, generating alternatives, and learning from valid negative results are discovery, not failed repairs. Honor the current task's budget and stopping conditions; this method does not introduce a squad or a repair counter.
