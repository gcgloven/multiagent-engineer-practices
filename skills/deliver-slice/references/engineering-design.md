# Investigate, frame, explore, decide

Use this reference for a substantive feature, uncertain defect, integration, or design change. It supplies design reasoning for the caller's workflow. Reuse current requirements and architecture when inspected and valid; do not recreate phases merely to fill documents. Conversely, a new contract, product scope, data meaning or migration cannot be treated as a tiny correction because its implementation is short.

## Frame the problem in its operating context

Start with a concrete journey: actor → trigger → expected behavior → current outcome → consequence. Ask which parts are observations, assumptions, stakeholder preferences, and constraints. For an internal service, the actor may be a script, analyst, operator, or another system. A failing test is evidence; its expected value still needs a defensible contract.

For a reported defect, preserve a reproducible input, current output, expected output, revision, and relevant configuration. Distinguish the symptom from a causal hypothesis. Use a targeted trace, failing regression, or discriminating experiment to test the hypothesis. If there are several explanations, choose evidence that would separate them rather than repeatedly editing the suspected line.

For a feature, inspect the current journey before accepting the proposed solution. An operator's need to understand stalled work might require explicit status and recovery actions, rather than another dashboard. Explore the problem and the solution together, returning to stakeholders when evidence changes the understanding of their need.

## Trace the contract and responsibilities

Record a short map when more than one component or owner is involved:

| Boundary | Inspect | Record |
| --- | --- | --- |
| Entry | Caller, payload, authorization, validation | Accepted inputs and observable rejection behavior |
| State | Allowed transitions, ordering, concurrency, retries | Invariants; authoritative state and owner |
| Data | Units, identity, persistence, schema evolution | Compatibility, retention, migration/recovery constraints |
| Dependency | Timeout, partial failure, backpressure, ownership | Failure contract and retry/idempotency expectations |
| Consumer | API/UI/report or downstream actuator | Meaning of fields, readiness signals, and errors |

Only investigate applicable rows. For example, a pure formatter has no persistence migration. Mark inferred contracts as inferred; do not silently convert them into agreed requirements.

## Compare credible alternatives

When the decision is consequential, compare alternatives that could actually solve the problem. Include retaining the current behavior or an operational workaround when useful. Do not invent alternatives merely to fill a table.

| Option | Why it could work | Evidence needed | Main cost/risk | Revisit condition |
| --- | --- | --- | --- | --- |
| Correct the current component | Its responsibility and interface remain appropriate | Defect reproduced; contract remains coherent | Local patch may preserve a deeper assumption | Similar failures reveal a missing domain boundary |
| Extract an explicit domain boundary | Several callers need the same invariant | Call-site map; interface and ownership agreement | Migration/compatibility work | Boundary remains unused or leaks responsibilities |
| Replace the mechanism | Current model cannot express needed behavior | Comparative spike or evidence about constraints | Larger transition and rollback burden | Proposed advantage disappears under representative conditions |

Selection should account for user value, correctness, uncertainty, operational failure, changeability, and cost. Prefer clear ownership and replaceable decisions. Do not create abstraction for its own sake, but do not reject architecture because it adds files. Design for the next credible requirements; record what would justify broader generalization.

A short spike can compare mechanisms without a production commitment. State what it learned, which assumptions remain, and which code is suitable to keep. A useful result can be a refined question, rejected option, or clearer contract.

## Converge on a delivery plan

Tie the current scope to observable criteria. Preserve the caller's requirement, criterion, risk, and decision identifiers when supplied; otherwise use clear references appropriate to the task. Do not promote every design preference into a new acceptance blocker.

Make the architecture understandable through component responsibilities, data/state ownership, critical interfaces and failure/recovery behavior. Tie the choice to alternatives and constraints. A class list or collection of implementation tasks does not explain how a user/system outcome works.

Order increments by dependency and uncertainty: establish a useful end-to-end behavior, extend it through the needed integration, then establish operating evidence for the intended target. Each increment specifies a demonstration, included/excluded scope, prerequisite decisions, acceptance and exit evidence, owner, and next decision. A bounded feasibility spike can precede a usable MVP; label its learning outcome and avoid presenting it as product readiness. Use a compatibility adapter or staged migration when necessary. Plan monitoring and recovery while choosing the design, not after deployment.

Check the caller's required upstream design/requirements gates before delivery. Identify accepted assumptions and their scope, not only a list of unknowns. A missing target or quality criterion may permit measurement and exploration, but it cannot be silently satisfied by whatever result the implementation produces. Keep the roadmap, current gate evidence and resulting decision in the canonical record.

Reopen the decision if a key assumption fails, stakeholders reject the behavior, the operating target changes, or a critical risk appears. Record what changed and which evidence is invalidated. A wider investigation within authorized scope can be the right next action; needing more thought is not itself an escalation condition.
