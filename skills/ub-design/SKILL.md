---
name: ub-design
description: Apply ub-mode-inspired domain, boundary, state-ownership and incremental-design principles to an authorized system proposal or consequential architecture decision.
---

# Scoped system design

This is an original adaptation of [ub-mode](https://github.com/unclebob/ub-mode/blob/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f/SKILL.md). Establish the intended behavior and operating conditions before elaborating a design. Preserve the user's scope/approach decision and identify consequential assumptions that remain unapproved.

Compare credible reuse and implementation options. Model domain states and invariants explicitly; place input validation at boundaries, keep responsibility for mutable state clear, and design repeated operations or recovery according to the required semantics. Prefer coherent small units that can be demonstrated and checked.

Keep ordinary local code decisions with the software owner. Escalate significant interface, domain-model or resource changes through the relevant decision. A failed approach warrants examining its assumptions, not an unlimited chain of patches.

Return representative success/failure paths, interfaces, alternatives, tradeoffs and demonstrable increments with acceptance evidence. Review testability and practical verification before implementation. Do not demand executed mutation or coverage evidence for code that does not yet exist. A design-only task ends with its approved-scope proposal and outstanding decision; this skill does not start implementation, cleanup or Git publication.
