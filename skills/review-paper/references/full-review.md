# Full critical review contract

Use this contract for an ordinary request to review a paper, including "review this paper" or "review this critically." An explicitly narrower triage, mechanism explanation, or synthesis request follows its chosen mode instead. A later focused follow-up does not require repeating the full review.

Obtain the identifiable paper from the supplied PDF or link. Identify the version reviewed and read the full paper and relevant appendices and supplementary material. Inspect consequential figures, tables, equations, algorithms, and proofs directly, resolving ambiguous extraction against the source. State unavailable or unread material and its effect on the assessment. Intended use is optional: without it, assess both research and implementation value.

Verify novelty against original papers and other primary sources, searching beyond author-selected comparisons. Inspect relevant official code, configurations, and artifacts when available. Distinguish inspected availability, executed checks, and successful reproduction. These review activities do not authorize substantial computation, installation, or deployment.

Deliver the following **seven numbered sections for each reviewed paper** directly in the conversation or assigned issue by default. Use one comment per paper when helpful. When local documentation is requested or needed, also maintain a canonical document at the agreed location and link it; the document supports but does not replace the chat review. Use concise comparison tables, method diagrams, or selected figure/table evidence in chat when they improve understanding. Attach only a focused figure or evidence extract when it helps inspection; do not upload the whole paper or review as a substitute for the response. Use precise source references for important factual claims: section, equation, figure, table, appendix, and page where useful. Link external primary sources near the claims they support with enough bibliographic detail to identify the work.

## Depth check

Seven headings alone do not make a full review. A reader should be able to reconstruct the central mechanism from its inputs, operative steps, assumptions, and worked example; understand the consequential difference from primary predecessor evidence actually inspected; and connect each major conclusion to evidence and a specific limitation. Expand the analysis where these connections remain implicit. Do not pad it to a word count.

Name the relevant predecessor passages and evidence objects checked, not just a related-paper title or link. Qualify novelty if those sources remain unread. For a guarantee, explain the relevant reasoning and assumptions you inspected; distinguishing this from formal certification does not remove that inspection. State unread dependencies and their effect on the particular claim. A blanket disclaimer about unverified proofs or unreproduced results cannot substitute for claim-specific analysis.

## 1. Core idea

Explain the problem, proposed solution, and main result in plain language. Give one concrete example showing how the method behaves. Label an invented toy example as illustrative rather than experimental evidence. Clarify what problem the paper actually solves when its motivation suggests a broader one.

## 2. What is actually new?

Identify the closest predecessor or predecessors and explain why each is relevant. Do not force a single predecessor when several are equally close. Separate the authors' novelty claims from your source-based assessment, and distinguish work predating the paper from later developments.

Explain exactly what changed in formulation, algorithm, assumptions, or guarantees. Distinguish conceptual advances, engineering adaptations, combinations of existing ideas, and experimental contributions. A small change can have meaningful consequences; algorithmic complexity alone is not a novelty judgment.

Include a compact comparison table covering the paper and its closest prior work:

| Work and relation/date | Mechanism | Assumptions | Guarantees or evidence | Consequential difference |
| --- | --- | --- | --- | --- |
| Reviewed paper | | | | |
| Closest predecessor, with source | | | | |

Add rows for the actual comparison; label later developments separately. Report an unverified novelty claim and the missing evidence when access or search coverage prevents verification. Do not invent predecessor identities, citation details, or findings to complete the table.

## 3. How the method works

Walk through the key mechanism, using equations or pseudocode where useful. Define notation, inputs, outputs, and important components. Explain why each component is needed and which components are inherited versus new. Carry the example through the decisive operations or reasoning steps, showing how the state or conclusion changes. Naming components or paraphrasing the abstract without their interaction is insufficient.

State the assumptions and the conditions under which guarantees hold. Inspect relevant derivations and proofs, distinguishing intuitive explanation, verified reasoning steps, assumptions, and unresolved gaps. Clearly label your reformulations and derived equations. Preserve quantifiers, units, boundary conditions, and algorithm order when they affect the argument.

## 4. Does the evidence support the claims?

Assess baseline strength, implementation parity, tuning effort, compute and data budgets, datasets and splits, leakage risks, metrics, ablations, sample sizes, seeds, variability, and uncertainty as applicable. Treat missing information as **unreported**, without assuming favorable or unfavorable settings. Avoid judging a theoretical paper by irrelevant empirical requirements, but assess any empirical claims it makes.

Separate theoretical guarantees from empirical observations. Label major claims **established within the stated scope**, **partially supported**, or **untested**, with reasons and citations. Make the scope explicit: a reported result under a paper's conditions is not your independent reproduction or a universal guarantee. Report contrary evidence and demonstrated errors clearly rather than hiding them behind a support label.

Distinguish statistical evidence from practical significance. Missing uncertainty estimates limit what can be concluded; they do not alone prove that the observed effect is false. Check whether the experiment isolates the proposed contribution or whether a competing explanation remains plausible.

## 5. Limitations and failure cases

Identify restrictive assumptions, demonstrated failures, plausible failure modes, scalability limits, and missing experiments. Explain the mechanism behind each substantive concern and cite the relevant evidence. Label your own hypotheses; do not present conjectures as observed failures.

Differentiate a flaw in the method, a limitation of the evaluation, an extraction ambiguity, and an implementation mismatch. A clearer definition, reanalysis, narrower conclusion, or source check may resolve a concern more appropriately than another experiment.

## 6. Practical relevance

Assess implementation requirements and reproducibility, including official code, data, configurations, and artifacts actually inspected. Examine licensing when verified, dependencies, hardware, runtime, memory, and deployment constraints. Separate reported measurements, your calculations or estimates, and unknown costs. An available repository is not evidence that its code matches the paper or reproduces its results.

For robotics papers, assess applicable motion and dynamics constraints, collision checking, continuous execution, replanning, sensing and localization uncertainty, communication delays, and simulation-to-real limitations. Discuss ROS 2 or Isaac Sim relevance where applicable, distinguishing documented integrations from your proposed integration approach. Apply these dimensions when the topic warrants them, rather than inventing a robotics use case for an unrelated paper.

Connect relevance to the user's intended use when supplied; otherwise distinguish research value from implementation value. Explain prerequisites and mismatches without turning the review into a mandated product roadmap.

## 7. Verdict

State the strongest contribution, biggest weakness, and a clear recommendation: **skim**, **study deeply**, **reproduce**, or **consider adopting**. Tie the recommendation and confidence to the intended use and available evidence; research and implementation recommendations may differ. Explain the conditions attached to the recommendation rather than assigning unsupported numerical confidence.

Propose **exactly three prioritized experiments per paper**, ordered by their value for resolving consequential uncertainty. For each, specify:

1. **Question:** which claim, mechanism, or transfer assumption it examines.
2. **Control or baseline:** the comparator and relevant matched conditions.
3. **Measurement:** what would be observed, with units or outcome criteria where meaningful.
4. **Recommendation-changing outcome:** what result would strengthen, weaken, or reverse the advice.

Use experiments appropriate to the work, such as a controlled ablation, matched comparison, or transfer/failure-condition probe. Prioritize informative tests over three generic repetitions of the same concern. Preserve valid negative and inconclusive outcomes. These are proposed experiments, not reports of executed work or permission to run them. If the current request already authorizes empirical work, complete its feasible agreed scope and report the runs separately; do not require a new task merely because review and execution are distinct deliverables. Otherwise present the proposals for selection and resource decisions before execution.
