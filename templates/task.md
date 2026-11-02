# Task brief

For a direct narrow question, the request can remain one sentence. For an ambiguous general task, offer roadmap planning versus a quick MVP test once. Use the [quick MVP brief](quick-mvp.md) for a bounded demonstration, or the [engineering brief](engineering-brief.md) for a roadmap. A large roadmap must link real [child work packages](work-package.md) before implementation when ticket creation is authorized and available.

Use the mandatory [ID vocabulary](../docs/terminology.md) for applicable coordinated records. Keep the outcome, ACs, and any OPs/FINDINGs together here; do not invent irrelevant categories. Cite artifact link + ID rather than reproducing the specification in every comment.

- **Outcome / provisional question:** what prompted this work and what is currently uncertain.
- **Selected mode and checkpoint:** roadmap plan, roadmap execution, quick MVP test, inquiry/explanation or quick correction. Record the choice and whether execution beyond planning is authorized; preserve any existing user decision.
- **Inputs:** exact source/artifact links, repository and revision, data/config versions.
- **Requested outputs:** each deliverable and its depth/format; keep review, research synthesis, design, execution and benchmarking distinct when requested together.
- **Working location and return:** canonical project directory/file links; substantive chat result with decisive evidence highlights. Use a compact table, code/data excerpt, or visual when useful; attach focused evidence when it improves review or reuse, not a whole-file substitute.
- **Current state:** phase, current artifact/candidate versions, gate and passed/blocked criteria, unresolved decision and owner, next transition and owner. For a quick correction, record eligibility and inherited acceptance; for inquiry, record the learning checkpoint.
- **Scope / authority:** allowed work, consequential exclusions, existing release authority.
- **Human checkpoints:** scope/approach, numbered roadmap/backlog and named implementation milestone as applicable; actual approval source, timestamp, revision, budget and next reserved pause. Record technical readiness separately. A proposal awaiting approval is an intentional stop, not permission to create or activate children.
- **Operating target:** internal service, integrated pilot, live industrial, or not applicable.
- **Developing understanding, when useful:** observations, competing explanations or designs, important assumptions, and open branches.
- **Acceptance, when adopting a delivery or confirmatory claim:** observable behavior or evidence; numeric thresholds where decisive. Do not invent a fixed success threshold for open discovery.
- **Review boundary, when needed:** proposed design, method, implementation, scientific conclusion, or release transition; identify what prior checks actually cover.
- **Resource envelope:** concrete work and total-roadmap budgets covering author work, reviews and repairs; consumed/remaining amount and next demonstration checkpoint. A restart or new finding does not reset them.
- **Children and gates:** proposed numbered map first, then linked outcome-based issues after backlog approval; dependencies, parallel siblings, acceptance evidence, owners and human execution authorization. Use the squad's stable MVP/SUB titles. Explicit early drafts and other unstarted children remain backlog; the parent holds milestone summaries, with detailed work/review in children.
- **Owner / return route:** one worker, or a coordinating lead for multiple specialists.
- **Explanation, when useful:** audience and question for an optional Product Manager rundown; omit when the task needs no extra explanation.

## Compact handoff or result

Explain the outcome and reasoning in chat, with decisive evidence/checks, material limits, exact current file links and next owner/decision. Use a concise summary table, relevant code/data excerpt, or visual where it clarifies the result. Keep full documents and raw evidence local; attach only a focused artifact that helps the reader inspect or reuse the result. A link or upload alone is not the response.

Before final delivery, compare every original requested output against actual evidence. Mark each complete, partial, blocked or deferred by an explicit scope decision. State what a review PASS covered. Missing required work prevents an overall complete/ready claim even when a subset passed.

For an inquiry checkpoint, record: question as currently understood → new evidence and contradictions → credible interpretations/options → useful branches → next inquiry or synthesis. Link the fuller analysis; do not flatten uncertainty into a PASS/FAIL label.

For a review loop, keep one durable state entry:

`problem/FINDING ID | affected AC/BR/OP | candidate/evidence | active owner/run | failed repair rounds | approach | budget remaining | next action/resumption condition`

Initial review discovers findings. A repair round is an attempted fix followed by verification of the same problem. Environment failures are blockers, not invented evidence of a failed algorithm. Preserve prior attempts when changing approaches.

Discovery, valid negative experiments, and ordinary initial edit/test cycles are not failed repair rounds.
