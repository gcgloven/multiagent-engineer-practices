---
name: run-experiment
description: Design, implement, and interpret empirical experiments, reproductions, benchmarks, and behavioral prototypes. Use when observation or a working demonstration can develop understanding or test a claim, separating exploratory and confirmatory work.
---

# Design and run an informative experiment

## Select the empirical mode

Exploration develops explanations, parameter ranges, measurements, or design possibilities. Confirmation evaluates a claim using a declared method and criterion. Reproduction checks a reported result under identified conditions. A behavioral prototype studies interaction or feasibility. Select the mode and label transitions; exploratory tuning is not independent confirmation.

Read [design and validity methods](references/experimental-design.md) for comparisons and scientific claims. Use [the experiment record](templates/experiment-record.md) to preserve methods and deviations. Targets may emerge during exploration; establish decisive criteria before the evaluation used for acceptance.

## Form the measurement contract

Identify the question, intended understanding/decision, experimental unit, inputs, variables, controls, comparators, and invariants. Define metrics with units, denominators, measurement windows, and handling of incomplete/failed runs. Link code, data, configuration, environment, seeds, and commands.

Select representative conditions and boundaries. Examine confounders and interactions; one-factor-at-a-time comparisons can miss the mechanism being studied. Choose repetitions, randomization, blocking, held-out evaluation, uncertainty estimates, and sensitivity checks according to variability and the claim. Explain choices rather than imposing a universal run count.

## Establish validity before scale

Check instrumentation and execution with a manageable case: expected units, clocks/measurement boundaries, domain invariants, baseline equivalence, and edge cases. Inspect raw traces when aggregates could conceal invalid execution. Fast invalid results are not performance evidence.

Set resource limits before substantial execution and track consumption across retries. A selected quick MVP test can include new isolated experiment code under a compact brief; run only its named demonstration and return the evidence and next decision. Do not silently expand its workload, add a production-hardening project or start a roadmap. For a larger study, use assigned work packages and account for missing experiment cells. Preserve raw results, failures, exclusions and analysis code. Informative follow-ups must fit the assigned budget and checkpoint.

## Interpret and refine

Compare like with like and report uncertainty. Separate measured effects, calculations, plausible mechanisms, and established causal conclusions. Examine sensitivity to workload, environment, model assumptions, and analysis choices. Missing or failed design points may invalidate a broader factorial claim rather than simply reduce sample count.

Return supported, unsupported, or inconclusive conclusions for the claim and tested conditions. Exploration can return patterns, explanations, and next probes without a binary verdict. Iteration may refine the question or method; valid negative results are scientific progress.

## Review and engineering transfer

Prepare consequential code changes and scientific conclusions for qualified independent verification. Use the assignment's review route when supplied; otherwise return the result and review boundary to the requester. This method does not initiate a squad. Distinguish implementation correctness, measurement validity, and inference/adoption scope. Supply reproducible evidence, not just a success summary.

When adoption is selected, transfer supported behavior, limits, invariants, risks, and representative checks. Assess prototype code's fitness for reuse. Preserve a roadmap toward the operating environment; laboratory success alone does not qualify deployment.

For an actual implementation or evidence-quality defect, preserve repair attempts and verification evidence and follow the current assignment's stopping condition. Research cycles and valid negative results are not repair attempts. If progress stalls, report the evidence and decision needed instead of repeating an unchanged experiment without purpose. This method sets no universal retry count and grants no new execution or deployment authority.
