---
name: analyze-data
description: Explore, explain, and evaluate datasets, experiment results, or operational measurements; develop defensible findings and, when requested, translate them into testable engineering improvements.
---

# Analyze data and develop evidence

Use this skill when the work depends on what a dataset can support: exploratory data analysis, troubleshooting measurements, comparing conditions, checking a scientific claim, or selecting an engineering improvement. A clear explanation, a useful visualization, a revised question, or an inconclusive result can complete the task. Implementation is an optional next mode.

## Establish the question without closing exploration

Identify the audience, question, source material, and decision if one exists. For an open request, begin by mapping what is present, what is missing, and which questions the data makes possible. Propose a provisional analysis direction and revise it as patterns emerge. Do not invent a numerical acceptance threshold just to make inquiry look like delivery work.

Choose the mode that fits the current question; switching modes is allowed and should be visible:

| Mode | Appropriate result | Read when needed |
| --- | --- | --- |
| Orientation / explanation | Dataset map, metric definitions, supported rundown, unanswered questions | [Evidence and method reference](references/analysis-method.md#establish-the-evidence) |
| Exploratory analysis | Distributions, relationships, segments, alternative explanations, productive follow-ups | [Explore before selecting an explanation](references/analysis-method.md#explore-before-selecting-an-explanation) |
| Confirmatory comparison | Prespecified estimand, matched conditions, uncertainty, qualified conclusion | [Compare and challenge](references/analysis-method.md#compare-and-challenge) |
| Engineering diagnosis | Ranked mechanisms with discriminating evidence; a change proposal if justified | [From finding to change](references/analysis-method.md#from-finding-to-change) |

Read the relevant reference sections, not the whole package by default. Use the [analysis ledger](assets/analysis-ledger.md) for a substantial or resumable study; a direct answer does not require a separate document for every field.

## Make the evidence trustworthy

Record source identity and version, observation unit, time basis, collection conditions, and transformations. Inspect actual data before selecting a model. Reconcile totals across successful, failed, missing, excluded, and incomplete observations. Keep failure conditions visible even when they cannot enter a performance estimate.

Define the metric with its formula, denominator, unit, direction, and eligibility rule. Keep event, run, subject, and experimental-condition counts distinct. A million events from three runs are not a million independent repetitions. Label synthetic data, calculated quantities, measured values, and inferred mechanisms separately.

Select analysis dimensions because they could change the answer: tails and distributions, subgroups, time, workload, scale, controls, interactions, missingness, or sensitivity. Coverage follows the question and consequences; there is no compulsory chart count or fixed maximum number of hypotheses. Explain material omissions rather than manufacturing an exhaustive catalog.

## Iterate through inquiry checkpoints

An exploration cycle is **observe → interpret → challenge → choose the next informative inquiry**. Keep competing explanations alive while evidence is weak. At a useful checkpoint, report what changed in understanding, remaining uncertainty, promising branches, and the cost of continuing. Continue within the agreed objective and resources; seek steering for a material change to either.

A new hypothesis, null result, failed scientific prediction, or uninformative analysis is not a failed software repair. Preserve attempts to fix actual implementation or evidence-quality defects, and follow any retry limit supplied by the current assignment. For example, repeatedly repairing a broken data join is repair; trying alternative explanations for a valid pattern is exploration. This method does not define a universal retry count.

## Promote evidence deliberately

Prepare consequential scientific claims for independent qualified review of the evidence and inference. Follow the assignment's review route when supplied; otherwise return the evidence and review boundary to the requester without automatically forming a squad. When engineering action is selected, hand off the supported finding, alternative explanations, target behavior, actual operating conditions, and a validation plan that can distinguish improvement from a changed workload or broken correctness.

Keep new ideas as open questions or recommendations until adopted. Do not silently turn a statistical pattern into a requirement or broaden existing acceptance criteria. Map a selected improvement to its requirement, acceptance evidence, and relevant risks, using identifiers supplied by the caller when present. The engineer may suggest a more effective intervention; the analyst owns neither an automatic code mandate nor final release authority.

Finish with an answer at the requested depth, accessible evidence and reproduction steps, limitations that affect interpretation, and the available next decisions. Put the result and key data highlights in the Multica chat, not just in a linked file. Prefer a compact summary table for a few important comparisons and a chart when it reveals structure or uncertainty; accompany each with the population, axes, units, conditions, and supported takeaway. Attach/embed a focused chart or small, sanitized data extract when the visual or exact rows make the result easier to inspect; keep full raw datasets and analysis files in the canonical location and link them.
