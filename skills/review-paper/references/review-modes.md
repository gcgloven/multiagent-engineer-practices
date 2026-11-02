# Review methods by purpose

These are methods to choose from, not four mandatory phases. Ordinary paper-review requests use deep review by default; explicitly narrower requests use their requested mode. An exploratory conversation may move between them as understanding develops.

## Triage: decide what deserves attention

Read the abstract and introduction for the stated problem, then inspect the method overview, representative evidence, and limitations. Check what kind of contribution the paper claims: formulation, theorem, algorithm, system, dataset, empirical observation, or synthesis. Explain the mechanism in ordinary language and distinguish it from the application domain.

Return the likely relevance, the strongest reason to read further, the main reservation, and the sections that would answer the reader's likely next questions. State that this is sampled reading. A title/abstract-only assessment cannot establish novelty, correctness, reproducibility, or broad superiority.

If relevance is unclear, compare plausible uses rather than demand a premature adoption objective: "This may help with correcting scanned printed text; it says less about handwriting recognition or page-layout recovery."

## Focused explanation: reconstruct the mechanism

Start from the exact question. Locate the definitions, assumptions, theorem/algorithm, and explanation that the answer depends on. Rephrase the mechanism while retaining its operative conditions. Walk through a small example, showing the state before, decision/action, and resulting state. Then show a boundary case or explain why the assumptions matter.

For a mathematical claim, distinguish intuitive explanation, derivation, and proof checking. If checking a proof, follow the actual implication chain and identify which steps are verified, assumed, or unclear. For a figure, first explain how to read it, then what its evidence supports. Do not infer the complete evaluation from one panel.

Keep the answer focused while allowing deeper questions. Reuse the paper map and earlier definitions instead of repeating the full review. If the requested explanation reveals a consequential inconsistency, surface it and investigate the relevant section; do not silently turn it into a separate implementation project.

## Deep review: assess the argument and the evidence

Read the full paper and relevant appendices and supplementary material, identifying the version and any coverage limits. Apply [the seven-section full-review contract](full-review.md), including its closest-prior-work comparison table and exactly three prioritized experiment proposals in the verdict.

Reconstruct the paper's chain of reasoning:

1. **Problem and stakes:** what is optimized or explained, for whom, under which constraints? Is the evaluated problem the same as the motivated one?
2. **Mechanism and assumptions:** what actually changes relative to predecessors? Which conditions are needed for the derivation, guarantee, or empirical behavior?
3. **Evidence:** what theorem, experiment, dataset, ablation, case study, or observation supports each central claim? How directly does it test the claimed contribution?
4. **Alternatives and limitations:** could a baseline mismatch, tuning difference, selection effect, workload property, or implementation detail explain the result? What cannot be concluded?
5. **Implications:** what has been learned, where might it transfer, and what deserves further investigation?

Use the [evidence guide](evidence-and-recommendations.md) and [claim ledger](../assets/claim-ledger.md) for the claims driving your conclusions. Scale the depth to the user's purpose: a methodological critique may require detailed statistics, while an algorithm review may need a careful guarantee/assumption analysis. Avoid scoring every paper against irrelevant criteria.

Evaluate relevant dimensions explicitly:

| Dimension | Investigative questions |
| --- | --- |
| Novelty | Which closest primary predecessors already contain the claimed idea, including work absent from the authors' comparisons? What predates the paper versus follows it? Is the contribution conceptual, empirical, integrative, or implementation-specific? |
| Internal validity | Does the design isolate the mechanism? Are controls, repetitions, exclusions, and uncertainty appropriate to the claim? |
| Comparison fairness | Are metrics, constraints, data, budgets, hardware, tuning effort, and timeout/failure rules aligned? |
| Applicability | Which assumptions match the intended setting, and which are violated or untested? |
| Reproducibility | What do relevant official code, data, configurations, versions, and evaluation procedures actually contain? Do inspected artifacts match the paper? Availability alone is not a successful reproduction. |
| Failure behavior | What happens on difficult, out-of-distribution, degraded, or boundary inputs? Are failures counted or excluded? |

Deliver the seven numbered sections and three prioritized experiment proposals for each paper directly in the conversation by default, following the full-review contract's depth and delivery rules. Within them, use worked examples, equations, compact tables, or diagrams to make the reasoning inspectable. A multi-paper request does not by itself select synthesis mode. The seven-section structure and three experiment proposals do not apply to an explicitly narrower request.

## Synthesis: compare ideas without manufacturing a leaderboard

Establish the comparison frame from the question. Track which papers were included, versions, how they were found, and known gaps. Use backward/forward citation searches or neighboring terminology when useful. Recent papers are not automatically the most relevant; retain foundational sources needed to understand the methods.

Align problem formulation and assumptions before comparing reported scores. Build a matrix with mechanism, guarantee or hypothesis, evidence setting, strengths, limitations, and applicability. Put incompatible measurements in separate groups or mark them incomparable. Distinguish methodological disagreement from different workloads, definitions, and operating conditions.

Synthesize patterns, tensions, and opportunities. Preserve plausible alternative interpretations rather than voting for a winner. If a ranking is needed, make the criteria and tradeoffs explicit. A landscape map or a better research question is a complete outcome. If the user asks for a systematic review, add a reproducible search/selection protocol rather than describing an informal survey as systematic.

## Research checkpoints

At a useful checkpoint, explain what changed in understanding, which evidence supports it, which branches remain plausible, and where further reading could matter. Continue valuable branches within the agreed task and resources. If a new direction materially changes the objective or expected resource use, explain that change before pursuing it. Do not confuse an informative negative result with a failed delivery repair.
