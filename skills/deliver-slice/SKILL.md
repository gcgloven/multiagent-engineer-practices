---
name: deliver-slice
description: Implement and verify a useful increment against inspected requirements, design, acceptance and assigned readiness gates. Use for fixes, features, MVP delivery, refactoring and release preparation, including revisiting design when implementation evidence invalidates it.
---

# Deliver a reliable increment

Develop a useful capability with enough understanding and evidence for its intended use. Incremental delivery controls the size of a commitment; it does not require shallow investigation, the fewest files, or the first plausible design. Explore when uncertainty warrants it, converge when the evidence supports a direction, and reopen the design when observations contradict it.

## Establish the engineering problem

Read the task, relevant repository instructions, current implementation, and available runtime evidence. Identify who uses the result, what they are trying to accomplish, and the failure or unmet need in that journey. Separate the requested outcome from a proposed implementation. For a bug, reproduce the observed behavior before repairing it when the environment allows; otherwise identify the exact reproduction gap. For research-derived work, carry the claim, operating conditions, and evidence limits into the engineering brief.

Trace the affected entry point through state changes, dependencies, persistence, and consumers. Distinguish a documented contract from inferred behavior. Record assumptions that affect correctness or compatibility; an open question blocks only work that depends on its answer. Investigation can begin before a formal requirements document exists.

## Check the assigned implementation boundary

Before coding the deliverable, read the requirements, design and roadmap supplied by the caller, including their revisions, accepted scope, applicable reviews and unresolved decisions. Verify that any required upstream gate is satisfied for this slice. An existing inspected issue, design or code contract can supply the needed evidence; a document title, author's “done,” or a review PASS for a different scope cannot. Record whether the assignment authorizes implementation, a design proposal or an exploratory spike.

If the caller reserves human scope, roadmap or milestone approval, verify its actual source and covered revision/scope separately from technical readiness. Lead's instruction, a ticket assignment or a reviewer PASS cannot replace that approval. Missing approval stops dependent implementation; return the concrete proposal or gap through the assigned route. Reuse already documented authority without requesting it again, and stop at the next human checkpoint even when the current implementation passes.

A tiny correction can inherit the accepted contract. A selected **quick MVP test** permits new isolated prototype code with a compact question, scope/non-goals, assumptions, interfaces, demonstration/checks, resource budget and stop condition; it does not require a full product PRD or roadmap. Record what its evidence can establish. Durable delivery, migrations and consequential operating changes need the corresponding requirements/design decisions. Follow the caller's selected mode rather than upgrading a prototype to the full route merely because it adds code.

If that basis is missing, develop the missing requirements/design within the assignment's authority or return the concrete gap to its assigned owner. Progress unaffected investigation. A bounded spike can test an uncertain mechanism under labeled assumptions when authorized; it cannot be reported as the accepted MVP or release-ready product. Routine technical decisions can be resolved without another permission request. Seek steering only for consequential choices outside delegated authority, and preserve any explicit caller gate.

## Explore and choose a design

Read [engineering-design.md](references/engineering-design.md) when the cause, interface, or design is uncertain. It gives a contract map, option-comparison method, and criteria for switching between investigation and implementation.

Use the amount of exploration needed to distinguish credible choices. A local correction may be obvious; a stateful or cross-system change may justify competing designs, a spike, stakeholder feedback, or a specialist. Compare correctness, operator/user experience, failure behavior, compatibility, changeability, and delivery cost. A new module or dependency is reasonable when those benefits justify it. A smaller diff is not automatically a better design.

State the chosen behavior, constraints, checks and target. For roadmap execution, work from the assigned increment/child and its dependencies, write boundaries, acceptance and budget; return detailed implementation and review evidence there. For a quick MVP test, work from the compact brief and stop after the demonstrated result and next decision. Record consumed and remaining budget across partial returns. Neither an agent-created hardening requirement nor a new activation expands the assignment. Preserve consequential decisions and valid evidence when replanning.

## Implement and test the behavior

Keep contracts, invariants, failure handling, and tests aligned as the design develops. Exercise the changed user or system path, not only isolated helpers. Use the repository's required checks and add evidence for risks the change introduces. A meaningful regression test fails for the original defect and passes for the correction; do not encode incidental implementation details as the contract.

Read [verification.md](references/verification.md) to choose coverage and distinguish code inspection, test-design review, executed checks, and independent verification. Update the coverage map after implementation: an added state, field, dependency, or failure path can create a gap in the original test plan. Tests may reveal design problems; return to design rather than accumulating patches around a false assumption.

Keep changed design decisions and affected gate evidence current. A repair that materially changes supported input, performance, data semantics or recovery can require reassessing the design/acceptance boundary as well as rerunning tests. Do not quietly trade away a requested quality objective to obtain a functional PASS. Report the tradeoff and resolve it with the authorized decision owner when it exceeds the accepted design.

## Review, repair, and deliver

Prepare substantive code changes and release candidates for independent qualified verification. Give the reviewer the exact candidate, objective, contracts/criteria, meaningful executed evidence, known limits, and prior findings. If review is part of the current assignment, use its route; otherwise return the implementation and self-checks to the requester with the independent-review boundary stated. A solo request does not automatically authorize dispatching a squad. The reviewer can challenge assumptions and test sufficiency; the author's passing test suite is input, not independent approval. Findings identify evidence, consequence, owner, and a closure check. Nonblocking improvements do not prevent accepted work from finishing.

When repairing a reviewed problem, keep the finding identity, attempted changes, and verification evidence across handoffs. Use the current assignment's repair budget and stopping condition; do not invent a fixed counter or additional coordination chain. Ordinary edit/test iterations, exploration, and valid negative experiments remain distinct from failed repairs of an identified defect.

For a release or operational handoff, read [release-evidence.md](references/release-evidence.md). Distinguish a verified implementation from readiness in an internal service, integrated pilot, or live industrial environment. This skill does not grant deployment or equipment-operation authority.

Maintain [the delivery record](assets/delivery-record.md), or the equivalent sections of an existing canonical project artifact, for substantive work. Keep the current slice, acceptance, gate status and next decision discoverable. A tiny correction can use a concise existing issue record; it does not need a new project document.

Finish with a substantive chat account of what now works, how it was checked, which criteria and phase gates are satisfied, material limits, and the next accountable decision. Link the canonical local artifacts and exact evidence rather than returning only filenames or copying the entire investigation. Put decisive check results in a compact table and include a short diff/code excerpt or visual when that helps the reader assess the change. Attach a focused evidence item when it improves inspection or reuse; do not upload the whole report, source tree, or raw log instead of the explanation. Update one current index and summarize revision deltas. Follow the caller's return route and status ownership; completing an implementation or repair step does not independently advance the overall workflow.
