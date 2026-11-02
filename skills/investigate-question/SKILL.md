---
name: investigate-question
description: Explore a technical or scientific topic, explain supplied sources, compare approaches, or develop a research direction using attributable evidence. Use for conceptual and literature investigation, including open-ended inquiry whose question may evolve.
---

# Investigate a question or research space

## Select the inquiry mode

| Mode | Working approach | Useful output |
| --- | --- | --- |
| Open exploration | Discover concepts, connections, competing explanations, and promising questions. | Topic map, research frontier, annotated reading path, or a better question. |
| Focused explanation | Inspect the relevant source/mechanism and prerequisites. | Answer with a concrete example, source locations, and limits. |
| Landscape / comparison | Establish approach families and useful comparison dimensions. | Evidence-based comparison, missing coverage, and where claims are incomparable. |
| Decision research | Evaluate approaches against the actual operating problem. | Recommendation or deferral with assumptions and discriminating follow-up. |

Infer mode and depth from the conversation. Allow the question to evolve. A study need not choose a product or define a hypothesis before learning the area. For substantial PDF dissection use a paper-review method if available; this skill supports source-based inquiry on its own.

Preserve each requested output using a compact record in the existing task. In paper research, initial benchmarking compares the papers' reported results, conditions, and limitations. It does not authorize implementation, dependency setup, or running author code/tests. Deliver the source-based comparison, then offer a bounded technical benchmark for the human's decision if useful. Reuse explicit human authorization already covering that execution. Track authorized empirical work separately; paper-reported values, proposals, and smoke checks are different evidence. Make input, capability, or resource limitations explicit.

## Build and examine evidence

Read [search and synthesis methods](references/inquiry-methods.md) when designing a search or combining conflicting sources. Use the [inquiry ledger](templates/inquiry-ledger.md) for continuing investigation; a focused answer may need only source links.

1. Establish what is known from supplied materials, prior discussion, and accessible code/data. Separate assumptions from findings.
2. Choose a reading/search strategy for the mode. Track scope, inclusion rationale, dates/versions, and coverage gaps. Include foundational and contrary work. Inspect primary evidence behind consequential secondary claims.
3. Read mechanisms and evaluation conditions, not only abstracts or headline numbers. Distinguish definitions, proofs, reported experiments, practitioner observations, and inference.
4. Compare alternatives on shared dimensions. Preserve incompatible workloads, baselines, metrics, and assumptions instead of manufacturing a single ranking.
5. Follow branches that develop understanding or expose an important gap. Summarize their contribution and reconnect them to the inquiry. Prune unproductive branches while retaining reasons.

## Synthesize and continue deliberately

Explain relationships, disagreements, confidence, and what would change the interpretation. Choose concept maps, mechanism examples, comparisons, or annotated reading paths according to the understanding needed. Depth follows the question; deep studies deserve substantial analysis.

At discovery checkpoints report learning and useful directions. Continue productive inquiry within the objective and resource envelope. Converge when the requested understanding or decision is supported, the user chooses to conclude, or the agreed resource boundary is reached. Do not impose an arbitrary source count, length, or number of turns.

End with a human-reviewable synthesis or discussion in the conversation or assigned issue: findings with evidence, credible alternative explanations, unresolved questions and limits, a recommendation, and the next decision. The recommendation may be to continue a specific line of inquiry, seek missing evidence, retain uncertainty, or take no engineering action. Scale these elements to the question; a focused explanation need not reproduce a full research dossier. A run ending, source list, uploaded file, or short status update alone is not that synthesis. At a resource boundary, distinguish a useful interim conclusion from completion of outstanding requested work.

When local documentation is requested or needed, maintain one canonical document and link it from the substantive chat synthesis. Do not substitute a file link or upload for the discussion. Include a concise source/claim table, key evidence excerpt, or chart when it clarifies what the research supports. Attach a focused figure or data extract when it makes the evidence easier to inspect or reuse; keep the full source and raw data in the canonical location. If the recipient cannot access the local file, put the necessary conclusion and evidence in chat and provide the smallest useful accessible evidence item where supported. Before concluding, reconcile the requested outputs against delivered evidence, including any separately requested experiments or benchmarks.

## Recommendations and transfer

For adoption, state the recommendation, applicable conditions, supporting and contrary evidence, tradeoffs, and unresolved claims. Prepare consequential scientific conclusions for qualified independent review. Use a supplied authorized review route; otherwise return the claim, evidence, and review still needed to the requester without automatically dispatching a team. Recommend reproduction or experimentation when it resolves material uncertainty; do not present published results as locally reproduced.

Pass selected claims, contrary evidence, source locations, and operating assumptions into the next method. Other branches may remain open. Further reading, broader inquiry, or insufficient evidence may be the appropriate outcome.

Unavailable material limits its associated claim, not all useful investigation. Record gaps and continue unaffected work. Preserve scope, resources, and permissions. Discovery iterations are learning; use the current task's checkpoint and stopping conditions without importing an engineering repair loop.
