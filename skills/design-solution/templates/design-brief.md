# Architecture and MVP design brief

Use for substantial design and implementation handoff. Extend an existing canonical record and link inspected, valid sections rather than recreating documents. A tiny corrective change can retain its existing requirements/design and record only the local decision and affected verification. The caller owns workflow progression and required approvals.

## Decision summary

- Revision, current decision, audience and intended operating target:
- Need and proposed behavior in a concrete successful/failure journey:
- Main architectural choice and why it fits:
- Current phase and requested next decision:

## Requirements and evidence basis

- Authoritative requirements/PRD revision and accepted scope:
- Stakeholder, domain/data and quality constraints affecting this design:
- Relevant inspected code, research or measurements and applicability limits:
- Assumptions: accepted for this slice, proposed, blocked or deferred; owner and revisit condition:

## Architecture and behavior

Show the system boundary and a representative flow, using a diagram or concrete prose model. Include how failure and recovery traverse the same boundaries.

| Component or module | Responsibility and state/data owner | Inputs, outputs and dependencies | Invariant enforced here |
| --- | --- | --- | --- |

| Critical interface / state transition | Accepted input and meaning | Success and failure behavior | Compatibility / recovery | Verification route |
| --- | --- | --- | --- | --- |

Record relevant identity, units, supported numerical/workload range, ordering, timeout/retry behavior, access rules and migration needs. Distinguish decisions established now from proposed details. Architecture should explain behavior and ownership, not only list files or technology names.

## Alternatives and tradeoffs

| Viable approach | Evidence and benefit | Cost / risk / limitation | Selection rationale or rejection reason |
| --- | --- | --- | --- |

- Consequential choice, reversibility and revisit trigger:
- Probe needed where evidence cannot yet distinguish options:
- Impact of the choice on correctness, performance, operations and future change:

## MVP and subsequent increments

| Increment | Demonstrable user/system outcome and scope | Prerequisites / decisions | Verification and exit evidence | Owner and next decision |
| --- | --- | --- | --- | --- |

Separate a feasibility spike from an MVP that provides usable end-to-end behavior. Include meaningful failure behavior in the first slice. Keep later increments conditional where evidence may redirect the work. A milestone must describe what can be demonstrated and accepted; “write code” or “add tests” alone is not an outcome.

## Validation and phase gates

| Named scope / transition | Criteria and evidence needed | Evidence already inspected | Gap or blocker | Decision owner / status |
| --- | --- | --- | --- | --- |

Cover the caller's applicable transitions: requirements/design readiness, implemented behavior, and the intended operating readiness. Reuse valid evidence. Distinguish review of a design, planned checks, executed checks, independent verification and release authorization. For a performance/accuracy claim, record baseline, workload, measurement boundary, threshold status and comparison method.

## Ready-for-implementation assessment

- Named slice and authorized implementation boundary:
- Requirements, contracts and assumptions ready to build against:
- Required design/claim review and its exact scope:
- Blocking choices/evidence, responsible owner and useful unaffected work:
- Resources, stopping boundary, handoff owner and supplied return route:

## Current record and communication

- Canonical artifact and evidence links; superseded revision references:
- Current phase, accepted outcomes, unresolved decisions/findings, and next accountable action:
- Chat summary: proposed behavior and architecture, decisive tradeoff, next demonstration, gate status, remaining decision; include a compact table or visual when useful:

Keep one current entry for readers. Link detailed evidence and versioned history; routine full-file uploads or repeated inventories do not improve the decision. Put decisive tradeoffs in a compact chat table and attach a focused diagram or evidence extract only when it makes the design easier to inspect or reuse.
