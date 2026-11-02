---
name: explain-work
description: Explain research, analysis, technical design, or implemented work in terms of stakeholder need, mechanism, tradeoffs, evidence, and project fit. Use for a quick rundown, design walkthrough, stakeholder explanation, or an optional teaching conversation; it does not automatically create a specification or course.
---

# Explain the work and its purpose

## Choose the explanation the reader needs

Identify what the reader wants to understand or decide and what they already know. Use the request and available context; ask a focused question only when a missing distinction would materially change the explanation. A quick rundown should remain quick. When the reader says an explanation did not land, change the framing or example rather than repeating the same terms at greater length.

Select the relevant parts of this method. Explaining a small change need not cover the project's entire strategy. A product-fit discussion may need stakeholder and evidence detail, while a technical walkthrough may need an interface example. For deeper walkthroughs or contrasting audience needs, use [explanation patterns](references/explanation-patterns.md).

## Establish what the artifacts support

Inspect the source needed for the requested explanation: task, paper, data/result, design, code/diff, test output, or product brief. Preserve the candidate or source identity where it matters. If a document says what should happen and the code shows what currently happens, explain the difference.

Distinguish proposed, implemented, inspected, tested, measured, and verified claims. Tests of local behavior do not establish adoption, production readiness, or business benefit. Cite the decisive source or artifact near the claim and identify material missing evidence. If implementation evidence is unavailable, explain the proposed design as a proposal; do not reconstruct a fictional implementation.

## Connect purpose, mechanism, and fit

Start with the useful outcome and the stakeholder situation it addresses. Follow one concrete case through the relevant behavior: input or trigger, important decisions or transformations, output, and consequence for the person or system using it. Define unfamiliar terms on first use and preserve established project vocabulary without imposing a new glossary.

Explain why the design takes this shape, including the tradeoff that matters for the reader. Separate recorded rationale from your interpretation. Include a failure condition, limitation, or counterexample when it changes how the result should be understood. Use a diagram, comparison, or worked example when it makes the mechanism clearer; do not add decoration or unrelated architecture detail.

Connect the work to an existing project outcome or decision only where that link is supported. Make the chain visible: capability changes behavior; changed behavior may improve an outcome; evidence is needed for each claimed improvement. Identify dependencies or operating assumptions. Do not turn a plausible benefit into established product fit, or treat every research result as a feature recommendation.

## Explain interactively when useful

For teaching, explain one coherent idea, work through an example, then offer a small application or invite the reader to explain it back. Feedback should target the specific misconception. Participation is optional; do not quiz the user before answering a simple question or claim that understanding has been demonstrated without a response. Follow-up questions can deepen or redirect the explanation without starting a course or mandatory loop.

## Finish at the requested depth

Return an explanation the reader can use, with material uncertainty and the next decision only if one is needed. A short response, conversation, or annotated artifact may be enough. Create persistent notes or a formal deliverable only when the request or agreed workflow calls for it. This skill does not initiate implementation, dispatch agents, approve technical work, or add gates, terminology, or retry counters.
