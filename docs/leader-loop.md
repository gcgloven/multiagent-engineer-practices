# How the squad leader coordinates discovery and delivery

The leader makes an evidence-based coordination decision each time it is invoked. It reads current state and requested outputs, checks the current phase/gate, selects the next needed action, delegates once, and stops. A worker's result gives the next invocation new evidence. Routine dispatch decisions can be short; the final synthesis must explain the work and its outcome substantively. The leader does not stay running to poll workers, implement the fix, or repeat the reviewer's technical review.

This applies to coordinated work under a selected squad. The generic Lead prompt supplies coordination competence; the selected squad supplies the actual loop. Open research, engineering design, analytics to engineering, software delivery, and mixed research/engineering share the dispatch mechanics but have different transitions and stopping points. A direct specialist request has no mandatory Lead stage. Product Manager can provide an explanation on demand; membership does not require that extra handoff.

Multica supplies the squad execution protocol. The checks below are the starter's decision policy. They are not a new scheduler, database, or mechanically enforced retry counter. See the [Multica setup](../integrations/multica/README.md) for runtime configuration and callback details.

For a squad-owned issue, the documented sequence is: the leader dispatches using the roster's exact mention, records an evaluation, and ends its run; the worker posts its result as a plain comment without another routing mention; that return wakes the leader. Keep the parent `in_progress` while work remains, then `in_review` when the overall outcome is ready. `done` belongs to the human or existing integration. A leader invited by a squad mention onto another assignee's issue does not take over its status. These are documented runtime behaviors. Validate these behaviors in your configured runtime using the behavioral acceptance cases. [Multica squad execution](https://multica.ai/docs/squads).

If using staged sub-issues, Multica also provides parent wakeups; inspect the configured trigger before adding another. A child that is closed or cancelled still requires outcome assessment before the next gate advances. A run finishing is not the same as its issue being accepted. [Issue wakeups](https://multica.ai/docs/issue-wakeups), [assignment behavior](https://multica.ai/docs/assigning-issues).

## Decide whether a loop is needed

For a simple explanation, lookup, or minor edit, one specialist performs suitable self-checks and returns the answer. Discovery can need repeated investigation, design, and synthesis without requiring a technical PASS/FAIL gate at each return. A coordinated verification loop is needed for substantive changes, consequential scientific claims, and release readiness. A research loop may end in a supported, unsupported, or inconclusive conclusion; it does not keep running until an idea succeeds.

Within one implementation assignment, the Software Engineer can run normal edit/test iterations. The two-round counter concerns unsuccessful **repair followed by verification of an already identified problem**. It does not count every command or test run during initial implementation. All work remains within the task budget.

## Coordinate open inquiry

Begin with a provisional frame: what the user is exploring, available evidence, meaningful uncertainties, and a resource envelope for substantial work. A learning checkpoint asks what changed and which direction is now useful. It does not require the final question, acceptance criteria, or product plan to be known.

For example, the Scout finds conflicting explanations for a performance pattern. The Lead can assign a Paper Reviewer to inspect the mechanism and an Analyst to explore the observed interaction. On return, it compares the evidence and keeps remaining alternatives visible. It might broaden the literature search, inspect instrumentation, design a discriminating experiment, or synthesize what is known. These are productive research iterations, not failed repairs.

Proceed within the user's authorized inquiry. Ask for steering only when a material scope/resource decision or an agreed pause boundary needs the user. When the evidence supports adoption, make the transition explicit: state the claim, limits, candidate engineering behavior, and independent review needed. Do not carry a provisional exploratory conclusion into implementation as an established fact.

## On each leader invocation

1. Read the original requested deliverables and output depth, current phase/gate record, changed result, candidate identity, and relevant AC/BR/OP/FINDING entries. Inspect active equivalent work before dispatching. For substantial engineering, check PRD, architecture and MVP-roadmap readiness; missing inputs are work to complete, not permission to jump to implementation.
2. If work is already active or this result has already been handled, do not start another run or post a repetitive comment. Still record the runtime-required evaluation, including the reason no action is needed.
3. Check whether the next action is within scope, authority, and remaining budget. Resolve only the missing consequential decision.
4. Select one next owner for each independently ready output. Send exact inputs, candidate/criteria, relevant terminology definitions, required output depth/structure, working directory, expected evidence, applicable stop condition, and one return route. Require a substantive chat-ready result with useful evidence highlights and exact canonical links; request focused visual or data/code evidence attachments when they improve inspection or reuse, not routine whole-file copies. Workers do not receive the squad policy automatically. Parallelize only when ownership and integration are clear.
5. Save the intended transition and active assignment in the authoritative record. Dispatch through one supported route, record the runtime's required evaluation, and stop. On return, reconcile the actual run/candidate before advancing. If dispatch outcome is ambiguous, inspect runs rather than retrying blindly.

An active-run check is advisory, not a lock. A missing return is a blocker to investigate; it is not proof that a worker finished or permission to launch a duplicate. Concurrent leader invocations and durable state must be checked in the workspace pilot.

## Pass the convention with the work

For a repair, the Lead could send this assignment, replacing the bracketed references with accessible evidence:

```text
Software Engineer: repair the title-rendering defect in candidate v1 [revision link].
For this task AC means acceptance criterion; FINDING means an observed review
defect. AC-2 requires titles to render as plain text. FINDING-1 records that
v1 renders title markup as active HTML [review evidence and reproduction].
Preserve other accepted behavior. Return a changed candidate, focused checks,
and remaining limitations in [actual return issue]. This is repair attempt 1;
the squad stops the same approach after two unsuccessful verified repairs.
Do not claim independent approval; return the candidate for the assigned review.
```

The specialist can act from that assignment without knowing the squad's entire vocabulary or pipeline. The Lead keeps the counter and routes the returned candidate to verification. An exploratory assignment instead carries a learning question, sources, resource boundary, and useful checkpoint; it need not include ACs, findings, or a repair counter.

## Mode, child issues and return placement

An ambiguous general task gets one concrete choice between roadmap planning and a quick MVP test; explicit choices are followed directly. New substantial planning first returns a concrete scope/approach proposal for human approval, then a numbered roadmap for approval before backlog creation. Explicit early-draft requests permit proposed parked children only. A quick MVP test uses a compact brief and returns its bounded demonstration before further implementation. The [working rules](workflow.md#required-engineering-phases) define the routes and human checkpoints.

Large work uses one child per independently verifiable outcome, with stable MVP/SUB titles, explicit dependencies/parallel siblings, owner/write targets, acceptance/reviewer and budget. Keep implementation and review detail in the child; the parent stores the child index and human approval record and receives milestones, material blockers and decisions. Before activation, check dependency acceptance and the actual human authorization for the named milestone. A technical PASS or callback cannot satisfy a missing human checkpoint; preserve the wait without dispatching. Before continuing a partial return, check consumed and remaining work budget as well as the defect-repair count. A new callback does not grant a new allocation.

## Route the result

| Result | Leader action |
| --- | --- |
| Inquiry or analysis checkpoint | Reconcile what was learned, contradictions, and open branches. Continue, broaden, reframe, synthesize, or conclude within the objective and resource envelope. No artificial repair count or mandatory PASS/FAIL. |
| Author completed an ordinary task | Check the requested output is present and close through the applicable runtime path. No mandatory review stage. |
| Systems Engineer supplied a design proposal | Assess the implementation-readiness boundary and route only required consequential design review. A design pass does not establish that code exists or release evidence is complete. |
| Product Manager supplied a requested explanation | Return the source-grounded explanation to its audience. Do not turn the explanation into a second technical approval or dispatch chain. |
| Author supplied a reviewable candidate | Send that candidate and relevant criteria to the independent Test & Code Review Engineer. The author does not approve its own work. |
| Reviewer PASS | Record the exact review scope and candidate, then reconcile every required output and gate. Advance only the transition that evidence supports. A correction PASS cannot complete missing benchmarking, accept an unknown performance target, or authorize deployment. |
| Reviewer FAIL | Keep consolidated blocking FINDINGs. Return only affected work to its owner with closure conditions; preserve unrelated valid evidence. |
| Reviewer BLOCKED | Record the missing input, access, environment, or qualified judgment, its owner, and resumption condition. Resume when that condition changes. Do not spend repair attempts on absent infrastructure or repeatedly poll. |
| Two unsuccessful repair rounds on the same problem | Report evidence, blocker, and the smallest next decision. Stop the same approach. A materially different approach is possible within existing scope and remaining budget; repeating the same approach requires user steering. |
| Valid negative or inconclusive experiment | Finish the question or propose the next scoped decision. This is not a verification failure merely because the hypothesis was unsuccessful. |

For multiple parallel outputs, the join advances only when every required output is accepted for the intended transition. Repair only failed branches. Missing future roadmap features are not failures of the current slice. Review-of-review and optional polish are not automatic stages.

Before marking the parent ready, use a small completion table: requested output → current local artifact/inline result → actual evidence → complete/partial/blocked → next owner. Preserve explicitly descoped work with its decision. A review checkpoint on a partial result is possible, but must say partial and must not close the broader request. Finish substantial research with an integrated discussion/study summary and substantial design with an understandable design document; do not ask the human to reconstruct the answer from dispatch comments.

## One repair example

The labels and evidence below are illustrative, not measured results.

| Event | Stored state for `FINDING-1` | Next action |
| --- | --- | --- |
| Initial review of `v1` finds article titles interpreted as HTML instead of plain text, violating `AC-2` | Open; failed repair rounds = 0; exact result and affected criterion linked | Software Engineer corrects title rendering. |
| Repair candidate `v2` still fails closure checks | Open; failed repair rounds = 1 | Software Engineer receives the remaining finding; Test & Code Review Engineer later checks the repair and affected regressions. |
| Repair candidate `v3` still fails those checks | Open; failed repair rounds = 2 | Lead reports the evidence and next decision; no identical third attempt. |
| A different method is selected within scope and budget | Keep both failures; record the alternative's rationale and its own bounded stop condition | Dispatch only the changed work. A new name or worker alone is not a different method. |

After an alternative is chosen, do not silently zero the problem's total history. Budget and explicit approach boundaries still apply. Repeated alternatives cannot create an unlimited loop.

Store this in one issue description/metadata record or a linked runtime-accessible task file. It need not be another document:

```text
Outcome/mode: verify article-preview text rendering
Review scope: content correctness; not deployment readiness
Candidate: v3 [code/config/check evidence links]
Criteria: [artifact]#AC-2; requirement [artifact]#FR-1
Problem: FINDING-1; blocking; title markup rendered as active HTML
Owner/active run: Software Engineer / none
History: v2 FAIL, v3 FAIL; two unsuccessful repair rounds
Budget: actual remaining authorized time/compute
Next: report blocker; alternative needs rationale and a bounded stop
```

For engineering records that need durable cross-handoff references, use the applicable [stable IDs](terminology.md). Open research can keep its own natural structure. Store actual identifiers and links in the project when IDs are used; never send placeholders in a dispatched assignment.

## Visual summary of the required-review path

![Leader routes evidence and bounded repairs](leader-loop.svg)

The picture covers a candidate requiring independent review; it does not describe discovery or impose a linear research pipeline. It also omits ordinary one-owner tasks, which can finish without independent review. The repair branch returns to affected verification; every return goes through the leader's state and budget checks. Each arrow between owners is a handoff/return event, not a continuously running leader. [Editable diagram source](leader-loop.mmd).
