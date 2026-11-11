# Software review and human handoff

For a small development task, keep implementation and review together and return one decision a human can assess without reconstructing the conversation. Independent review checks a self-tested candidate. It does not replace the author's responsibility for diagnosis, design and regression checks.

## Default sequence and stop boundary

1. Software Engineer implements the accepted behavior, reviews the diff, checks the changed journey and important failure paths, and returns one candidate with actual checks and known gaps. Ordinary edit/test iterations stay inside this assignment.
2. Test & Code Review Engineer completes the agreed reviewable scope within budget and returns a consolidated findings batch. A broken prerequisite may prevent further testing; name every unchecked area and its resumption condition instead of claiming a complete review.
3. If required, Software Engineer repairs the batch, addressing shared causes and checking affected behavior. Preserve finding identities and candidate history.
4. The reviewer verifies closure and affected regressions. Reopen a broader area only for specific new evidence, recording why. Report serious new defects even if the allowance has ended.
5. Lead returns one integrated decision: scoped PASS, or a partial/FAIL/BLOCKED result with remaining risks and the next proposed action. Keep runtime-required callbacks and evaluations, but avoid repeating full worker reports.

For a small task needing independent review, the default allowance is **one repair cycle**: the consolidated repair batch plus its closure review. The initial review is not a repair cycle. A batch consumes its cycle whether it succeeds, remains incomplete, or closes old defects while exposing another. Record the allowance alongside a time/compute or run budget before dispatch. Larger authorized tasks may establish a different explicit allowance based on scope and risk. Tasks that need no independent review retain their direct route.

The allowance applies to the whole task, separately from the [same-problem failed-repair limit](../squads/common.md#bounded-repair-policy). A different finding, worker, issue or approach cannot reset either history or resources. Lead checks remaining cycles before dispatching repairs. At the default boundary, unresolved blockers return to the human with a concrete proposed extension and cost, unless an existing explicit authorization already covers it. No automatic additional repair cycle follows. Stopping does not mean accepting defective work.

These are prompt and coordination rules, not a runtime counter or scheduler. Packaging checks do not prove that agents follow them, and no token savings are claimed without measurement.

## Classify before ordering a repair

| Classification | Treatment |
| --- | --- |
| Demonstrated defect | Cite location, evidence/reproduction, affected accepted criterion, impact and testable closure; repair within allowance. |
| Suspected defect | Investigate or reproduce before making repair mandatory. A suspicion is not automatically a demonstrated blocker. |
| Evidence gap | State which claim cannot be established, why, owner and resumption condition; required unavailable evidence prevents acceptance of that claim. |
| Requirement/design mismatch | Cite both conflicting expectations and identify the decision owner. Resolve consequential semantics before dependent implementation. |
| Optional improvement | Keep outside required closure unless the authorized scope explicitly adopts it. |

Do not freeze a findings list to hide a newly discovered defect. Preserve it, adjust the scoped verdict, and respect the stopping boundary. Do not silently change the expected behavior to make a test pass.

## Current review record

Update one record in the development issue or linked runtime-accessible artifact. Reuse existing acceptance and evidence sections rather than introducing another ledger. A human should be able to read this record and assess the candidate without opening every handoff.

```text
Outcome and intended behavior:
Accepted scope/criteria and decision sources:
Candidate/base and relevant configuration:
Review scope completed:
Checks run and results; evidence links:
Unchecked areas, reason and resumption condition:
Remaining risks and unresolved contract choices:
Total resource budget: allocated / consumed / remaining
Repair cycles: allowed / consumed / remaining
Same-problem failed-repair history: linked per finding
Active owner/run and one return route:
Scoped verdict, recommendation and next human decision:
```

| Finding / class | Accepted criterion and evidence | Repair / candidate | Closure check and result | Owner / state |
| --- | --- | --- | --- | --- |

Workers return candidate changes, changed findings, actual new checks and the next decision. Reference unchanged acceptance and valid evidence rather than copying them. Lead updates this record without restating the full report. Keep old evidence linked to its candidate. Put detailed work in the development issue; a parent receives the compact outcome and material decisions. A handoff alone does not justify another issue.

## Live behavioral acceptance cases

Use fictional inputs in a configured workspace pilot and record actual run/candidate evidence. These scenarios specify expected behavior; they are not completed runtime tests.

| Scenario | Expected behavior |
| --- | --- |
| A reviewable candidate contains several independent defects | Reviewer completes the agreed reviewable scope and returns one batch; Lead does not dispatch a repair for each finding. |
| A broken entry point prevents remaining checks | Reviewer names unchecked areas and resumption conditions; no complete-review claim. Remaining checks consume the existing allowance when resumed. |
| Review produces a suspicion, conflicting expectations and an optional improvement | Investigate the suspicion, route the consequential contract decision and keep optional work outside required closure. No automatic three-item repair order. |
| Repair closes every original finding but closure review finds a new blocker | Preserve the new blocker and return the next human decision at the one-cycle boundary. A new identifier does not start another cycle. |
| Repair introduces a regression | Reviewer reports it with evidence; no false PASS or automatic allowance renewal. |
| An optional suggestion accompanies PASS | Finish the accepted scope without another development round. |
| The user explicitly authorizes an extension | Record its scope, resources and new cycle ceiling while preserving consumed cycles and prior evidence. |
| A human opens the issue after several returns | Current candidate, findings/closure, completed and unchecked areas, risks, resource use and next decision are visible in one record. |

For an efficiency comparison, use comparable task scope and quality requirements. Record elapsed time, agent activations, findings per review batch, total repair cycles, and input/output/cache token usage separately where available. Distinguish cache reads from fresh input and compare billed cost only when provider pricing data is available. Lower token use alone does not establish equivalent correctness.
