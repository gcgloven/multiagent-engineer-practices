# Patterns for explaining work

Use a pattern when it helps the reader's current question. These are choices, not mandatory sections or an ordered workflow.

## Quick rundown after engineering work

Answer three linked questions in plain prose: what changed, why the change matters, and what evidence supports the result. Add a limitation when it affects the reader's decision.

For a fictional article preview:

> The preview now displays supplied text literally, so a title containing angle brackets appears as text instead of page markup. The implementation escapes the title before composing the preview. The supplied unit-test output covers that behavior; browser rendering and the saved-file path have not been checked.

Use only evidence actually present in the task. If no tests were run, say the behavior follows from inspection or remains a proposal. Avoid adding an adoption or readiness claim to make a modest fix sound more valuable.

## Technical design walkthrough

Choose a representative input and follow it across the interface the caller uses. Explain what the caller must supply, what the implementation does internally, what it returns, and the error or ordering rule that matters. A small interface may hide substantial useful behavior; the point is what the caller can rely on, not a count of files or layers.

For alternatives, compare one real tradeoff under the actual constraints: an immediate local check might improve feedback while a shared validation step avoids inconsistent results across callers. Explain which behavior the chosen design guarantees and which cost or limitation it accepts. If the design is merely proposed, label the expected behavior and validation still needed. Summarizing a design is not independent verification of it.

## Product or project fit

Trace the proposed value without skipping evidence:

| Link | Useful question | Evidence boundary |
| --- | --- | --- |
| Need to capability | Who has the problem, and what can they do differently? | Stakeholder evidence may be missing; state the assumption. |
| Capability to workflow | Which action, delay, error, or decision changes? | Implemented functionality can be inspected or tested. |
| Workflow to outcome | Why would that change improve the intended result? | A plausible mechanism remains a hypothesis until evaluated. |
| Outcome to adoption | Under what operating conditions is it worth using? | Local tests do not establish operational fit or stakeholder acceptance. |

For an internal study-note tool, adding search can establish that a matching note is retrievable. It does not by itself establish faster study or better retention. A useful explanation identifies that gap without requiring a study unless learning effectiveness is part of the current objective.

## Optional teaching conversation

When the reader wants understanding, adapt the example to their background and intended use. Explain the concrete mechanism before introducing shorthand. An analogy can support that explanation, but state where it stops matching the actual system.

Offer one relevant application, such as asking what would happen if an input failed validation. If the user engages, use their answer to choose the next explanation. If they prefer a direct answer, give it. Do not create course files, learning records, repeated quizzes, or a claimed mastery result from a one-off walkthrough.

## Explaining an inconclusive result

Distinguish the question, what the evidence showed, what remains unresolved, and whether the uncertainty affects the current decision. A sound experiment can reject the preferred hypothesis while still providing useful knowledge. Preserve that result instead of inventing a product benefit, a new requirement, or another mandatory iteration.
