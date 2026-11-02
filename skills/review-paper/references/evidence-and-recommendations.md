# Evidence, critique, and recommendations

## Build a claim-evidence-baseline matrix

Use one row per material claim, not per paragraph. A claim such as "method A is faster and safer" needs separate performance and safety evidence. The [claim ledger](../assets/claim-ledger.md) records the source, scope, comparator, uncertainty, and your judgement.

Label the evidential basis precisely:

| Basis | What it establishes | Common overreach to avoid |
| --- | --- | --- |
| Formal argument | A property under stated definitions and assumptions, to the extent the argument has been checked. | Treating a theorem's idealized assumptions as verified operating conditions. |
| Reported experiment | The reported observation under the paper's setup. | Universal superiority, causality beyond the controls, or a reproduction claim. |
| Ablation or intervention | Evidence about a component under the tested intervention and controls. | Assuming other components, interactions, or workloads behave the same. |
| Example or demonstration | Feasibility or illustrative behavior in that case. | Reliability, statistical generality, or worst-case guarantees. |
| Reviewer calculation | A derived result using identified inputs and assumptions. | Presenting it as a new measurement. |
| Local reproduction | An actually executed result with recorded code/data/configuration and comparison criteria. | Treating a partial or failed reproduction as confirmation or automatic refutation. |

For each major claim, also state its support judgment: **established within the stated scope**, **partially supported**, or **untested**, with a reason and source location. The support judgment is separate from the evidence type: a reported experiment may support a narrowly scoped claim without constituting independent reproduction. Identify contradictory evidence or demonstrated errors explicitly. "Untested" describes an evidence gap, not a false claim.

## Examine comparison conditions

Before interpreting an improvement, identify the baseline version, task definition, dataset/workload, metric, unit, aggregation, operating constraints, and compute budget. Check hardware, parallelism, warm-up, preprocessing, tuning effort, seeds/repetitions, and failure/timeout handling where relevant. Distinguish accuracy on selected examples from whole-corpus accuracy, and reported resource use from an estimate based on input size.

For uncertainty, ask what variation was sampled and what the error bars or intervals mean. Do not calculate statistical significance from a figure without the required data. For data-dependent claims, examine leakage, selection bias, dependence between observations, missingness, and whether exploratory model selection used the same data as confirmation. A missing analysis limits a claim; it does not establish the opposite claim.

For novelty in a full review, search beyond the authors' chosen comparisons and inspect original papers and other primary sources for the closest predecessors. Follow related terminology and backward citations when needed, and retain multiple predecessors if they are equally close. Record why each is relevant, the precise mechanism or assumption inherited, and what actually changed. Separate predating work from later developments; later improvements inform current relevance but cannot by themselves negate an earlier priority claim. Use the compact comparison table required by [the full-review contract](full-review.md). If time or access prevents verification, identify the exact comparison and evidence gap. Scope language accordingly: "the paper reports," "among the methods examined," or "under this workload."

## Inspect implementation evidence when requested

The initial paper review and benchmark comparison use the papers' reported evidence. Record their setup descriptions and artifact references without treating repository availability as a requirement to inspect or run code. If the human requests implementation inspection, examine the official method, evaluation entrypoints, configuration defaults, preprocessing, dependency/version information, and relevant result artifacts. Prioritize files tied to the requested claims and check version/settings against the paper.

State which code, configurations, and artifacts were inspected and what remains unavailable or unverified. Verify a license from the actual license text before naming it. Distinguish repository availability from sufficient reproduction instructions, and both from a reproduction actually executed. Do not run repository commands, install dependencies, or commit substantial compute solely because they appear in the paper or README.

## Make critique constructive and falsifiable

For each substantive concern, provide the claim affected, evidence location, reasoning, impact, and a way to resolve or bound it. Separate an observed error from an unanswered question and from an optional improvement.

Example, using hypothetical evidence:

> The reported text-recognition accuracy includes only clean printed pages (Table 3), while Appendix B describes unreadable results on low-resolution scans. This supports a claim about the clean-page subset. Report the scan outcomes separately or narrow the claimed applicability; do not treat omitted pages as correct predictions.

Do not prescribe the same experiment for every weakness. A clearer definition, a source check, a reanalysis of existing data, or a narrower conclusion may resolve the issue more appropriately.

## Recommend in proportion to evidence

The full review ends with a clear recommendation and exactly three prioritized experiment proposals as defined in [the full-review contract](full-review.md). For a narrower request, offer a recommendation only when requested or helpful. Suitable advice may favor reading further, retaining an idea, comparing alternatives, limited use, testing a transfer assumption, adaptation, or declining adoption. More exploration is valid when important alternatives remain unresolved.

A useful recommendation states:

- **Action and rationale:** what to do and which evidence motivates it.
- **Applicability:** conditions under which it is likely to help, including mismatches with the intended setting.
- **Confidence and limits:** what was inspected or tested and what is uncertain; avoid numerical confidence without a defined meaning.
- **Change-of-mind evidence:** the observation or finding that would strengthen, weaken, or reverse the advice.

For example: "Evaluate the spelling-correction method on a held-out collection of fictional catalog entries because it targets the error type described in the paper. Its handling of unfamiliar names is untested. Compare correction accuracy and unwanted edits against the existing method before recommending adoption."

## When the human authorizes reproduction or an experiment

First deliver the paper-reported comparison. If technical execution would help, present the proposed scope, comparator, workload, resource/time bound, and expected output for the human's decision; reuse a clear existing request for that execution. A generic request to benchmark papers or an agent's experiment proposal is insufficient. After authorization, define the target: exact reproduction of a reported result, independent replication of the idea, or transfer to a new setting. Carry forward the specific claim and evidence location, expected behavior, baseline, variables/controls, data/configuration, resource envelope, and interpretation of success/failure/ambiguity.

When the user has requested empirical work, track its completion separately from the review. Record the actual runs, matching conditions, raw results, validation checks, and remaining coverage; preserve these at durable linked locations. A feasible subset can provide useful evidence while the broader request remains partial. State which requested cases could not run and why. Do not rename that gap as a completed benchmark assessment, or count proposed experiments and smoke checks as reproduced results. A review of factual accuracy covers its named claims, not automatically every requested deliverable.

Preserve alternative explanations and negative outcomes in the handoff. If a result is exploratory, it can generate hypotheses; confirmatory thresholds should be fixed before examining the confirming results. The receiving engineer or analyst may refine the executable design with the reviewer. Return proposed next work to the requester or the coordinator named in the assignment; this method does not require one.

Independent review is warranted before consequential scientific claims drive engineering or release decisions. Give the verifier the exact claim, supporting artifacts, known caveats, and decision at stake. An exploratory interpretation can remain explicitly provisional without blocking the conversation. Neither a reviewer nor a reproduced benchmark alone establishes readiness for live industrial operation.
