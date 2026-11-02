# Evidence and method reference

Use sections relevant to the question. This is a set of decision aids, not a mandatory linear report template.

## Establish the evidence

Create a small provenance map before interpreting derived results:

| Element | What to establish | Consequence if unclear |
| --- | --- | --- |
| Source | Dataset or query identity, revision/hash, collection or extraction time, access boundary | Results may refer to different versions; preserve the exact input used. |
| Observation | Event, interval, run, participant, device, facility, or condition | Choose aggregation and uncertainty at the appropriate level. |
| Population | Sampling/selection mechanism, inclusion window, operating conditions | Restrict applicability; check selection and survivorship bias. |
| Schema | Types, units, keys, null semantics, timestamp/timezone, categorical levels | Detect silent coercion, duplicate joins, mixed units, and invalid ordering. |
| Transformation | Filters, joins, deduplication, imputation, normalization, derived columns | Reconcile input/output counts and make assumptions inspectable. |
| Measurement | Instrument resolution, warm-up, clock basis, censoring, collection overhead | A plausible number can measure the wrong boundary. Validate before ranking. |

Inspect representative raw records as well as summaries. Verify join cardinality and row-count changes. Count unique entities separately from repeated observations. A missing value may mean not observed, not applicable, failed, or zero; do not merge these meanings automatically. Preserve source data and reproduce transformations in a script, query, or notebook when the result is meant to be repeated.

For rates and ratios, explicitly state numerator, denominator, interval, and aggregation. `mean(A/B)`, `mean(A)/mean(B)`, and `sum(A)/sum(B)` answer different questions. Per-page accuracy, per-document accuracy, and corpus-level accuracy can differ substantially; state the weighting and eligibility rules. Clarify whether a percentile describes observations within groups, group-level summaries, or pooled observations. Describe `±` as standard deviation, standard error, confidence interval, or observed range; never leave it ambiguous.

## Explore before selecting an explanation

Start with a breadth pass appropriate to the data. Follow up where it reveals uncertainty that matters. The questions below guide coverage; choose useful plots and summaries rather than producing every possible plot.

| Dimension | Useful questions | Common failure to challenge |
| --- | --- | --- |
| Completeness and failures | Which groups, periods, or design cells are absent? Is absence systematic? | Dropping failed or slow cases makes the surviving system look healthy. |
| Distribution | Where are typical values, tails, modes, outliers, and pile-ups? | A mean hides long waits, bimodality, or saturation. |
| Time and sequence | Are there warm-up effects, drift, bursts, seasonality, or autocorrelation? | Apparent treatment effects are collection-order effects. |
| Segments and scale | Does the pattern change with workload, site, device, cohort, or size? | A pooled association reverses inside groups or only holds at one scale. |
| Relationships | Which associations are robust, nonlinear, or sensitive to conditioning? | Correlation is presented as a mechanism or a causal effect. |
| Factors and interactions | Does a factor's effect depend on another factor? Are relevant cells observed? | A single baseline comparison conceals interactions or missing corners. |
| Sensitivity | Does the decision change with plausible exclusions, windows, thresholds, or definitions? | One convenient processing choice determines the conclusion. |

Keep a hypothesis ledger: observation, possible mechanism, competing explanation, evidence for/against, and a discriminating next check. Alternative explanations can include workload mix, instrumentation changes, censoring, resource contention, and incorrect denominators. Do not require a fixed number of hypotheses when one is decisive or several remain credible.

Use plots to inspect assumptions as well as communicate results: raw points beside summaries, distributions beside means, time traces for drift, and grouped or interaction views for factors. Avoid connecting unordered categories as though they form a numerical trajectory. State whether error bars describe variation between runs, estimation uncertainty, or variation across conditions.

Exploratory search is legitimate. Label relationships discovered after looking at the data as exploratory. If a later decision requires strong confirmation, use fresh/held-out data, a prespecified follow-up, or an explicit adjustment appropriate to the analysis. Do not retrofit a hypothesis as though it were fixed before exploration.

## Compare and challenge

Before a confirmatory run or high-stakes conclusion, agree on:

- The estimand: the quantity or difference being estimated, in which population and conditions.
- The baseline and treatment, independent sampling/experimental unit, controls, and outcome definitions.
- Eligibility, exclusions, failed/incomplete observations, warm-up, and any censoring treatment.
- Comparison design: pairing, randomization or allocation, repetitions, resource equivalence, and measurement window.
- Practical effect size and uncertainty needed for a decision; any acceptance threshold must come from an adopted requirement or explicit decision.

Match comparisons on factors that materially affect the result. If paired runs share seed, input, and environment, report within-pair effects and variation at the pair level. Clustered or temporally dependent observations need an appropriate analysis rather than assuming independent rows. Report sample size and uncertainty honestly; a small sample may support diagnosis but not a stable tail or reliability estimate.

For a factorial design, show the observed cell/replicate coverage before estimating effects. Decide whether main effects, interactions, restricted contrasts, or only descriptive results are identifiable. Do not silently fill missing design cells or generalize from the surviving corner conditions. Missingness itself may be a useful finding. A ratio of ratios is an interaction measure, not a whole-system speedup; give its formula and neutral value.

Keep correctness separate from performance eligibility. A faster run that drops output, changes domain behavior, or fails a correctness check cannot establish a safe improvement. A timeout may be counted in reliability/coverage while being unsuitable for the same completed-run latency estimate. State the censored or excluded category and its denominator.

Distinguish effect size, uncertainty, and decision relevance. A statistically detectable change may be operationally immaterial; a large but uncertain change may justify another experiment. Profiling can locate a promising component, but a causal claim about an optimization needs a matched intervention and preserved behavior. Changes across dates, hardware, software, and workload together do not isolate one cause.

## From finding to change

Engineering promotion is a decision checkpoint, not the default ending of analysis. Useful outcomes include a clear explanation, a reliable report, improved instrumentation, a new study, an operational adjustment, or a code change.

When selecting a code change, make the reasoning inspectable:

| Link | Evidence to carry forward |
| --- | --- |
| Observation → candidate mechanism | Source records, plots, profiles, and competing explanations; confidence and unresolved gaps. |
| Mechanism → intervention | Why the proposed change should affect the outcome; conditions where it may not help. |
| Intervention → contract | Intended behavior, invariants, operating range, and unchanged comparisons; caller-supplied requirement/criterion references when useful. |
| Contract → implementation | Candidate revision, configuration, dependency changes, ownership, and rollback/fallback where relevant. |
| Implementation → verification | Correctness and regression checks, matched measurement, failures, uncertainty, and independent review. |
| Verification → use | Supported scope, readiness gaps, operational owner, and the next release decision. |

A negative engineering result need not invalidate the analysis: the mechanism may exist while the selected intervention costs more elsewhere. Reopen the corresponding hypothesis, preserve the result, and choose another inquiry or stop. A consequential claim and a substantive implementation may need different reviewer expertise; one reviewer may cover both only when qualified and the two conclusions remain distinct.

For internal use, establish reproducibility, maintainability, ordinary failure behavior, and an accountable owner. For an integrated pilot, add representative contracts and failure/recovery evidence. Live industrial operation needs the appropriate operational and safety authorization and domain-specific readiness; an analytical result does not grant it.

## Report at two depths

Lead with the answer, strength of evidence, and decision implications. Link the detailed ledger, transformations, figures, and reproduction command rather than reciting every intermediate exploration. Preserve important abandoned hypotheses and negative results when they prevent repeated work or explain the final interpretation. State what was inspected, calculated, executed, and left untested.
