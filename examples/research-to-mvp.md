# A. Research → experiment → a study-note MVP

This fictional example explores a study-note application for beginners learning unfamiliar concepts. No participant study, paper reproduction, or product evaluation has been performed. The questions, design choices, and acceptance conditions illustrate a workflow; they are not findings about learning effectiveness.

## Explore the need before choosing a feature

Imagine a note author who wants readers to apply an idea to a new problem, rather than only recognize its definition. Possible directions include clearer language, a worked example, an interactive exercise, or better feedback. There is not yet enough evidence to choose among them.

Use problem framing to understand the intended reader, the task they should be able to perform, and the concepts that cause difficulty. Keep assumed difficulties separate from actual reader observations. A Scout can map relevant approaches and locate primary research. A Paper Reviewer can explain a selected paper's mechanism, study design, and limitations. An Analyst can inspect available learning-task data if the project has appropriate data access.

A learning checkpoint can produce a better question, a comparison of mechanisms, or a decision to gather evidence. It does not have to produce an implementation plan. Continue useful inquiry within the agreed resources; informative research iterations do not count as failed repairs.

For the remaining illustration, assume the inquiry selects a comparison between **definition-only notes and notes with a worked example**. This is a chosen branch, not an established recommendation.

## Establish a study contract

> **Question:** Under the selected conditions, does adding a worked example help readers answer a new application question?
>
> **Comparison:** Two note variants for the same concept and a predefined assessment. Identify differences in length, reading time, and prior knowledge that could affect interpretation.
>
> **Evidence:** Preserve source versions, exact note variants, question wording, scoring rubric, assignment procedure, exclusions, and analysis code. Use only appropriately authorized participant data.
>
> **Decision criteria:** Agree before a confirmatory evaluation on the meaningful improvement, relevant uncertainty, and any reading-time or usability constraint. A favorable average alone does not establish a transferable learning effect.
>
> **Resources:** State the permitted study effort, available material, and when a new decision would be needed.
>
> **Outcome:** A supported, unsupported, or inconclusive conclusion with its applicability limits.

If no participant study is authorized or feasible, the work can stop with a literature synthesis, a study design, or a prototype used to inspect the interaction. Agent opinion is not evidence of how actual readers learn.

## Separate prototype checks from scientific evidence

An Engineer can build two note variants behind the same interface. Local checks can establish that the requested text, examples, and assessment controls appear correctly. They cannot establish improved learning.

Before collecting confirmatory evidence, inspect the study design: comparable material, assignment and order effects, reader background, scoring consistency, missing responses, and the distinction between practiced and unseen questions. A qualified reviewer should assess consequential methodological choices. Fix a scoring error as an artifact defect; preserve a valid unfavorable result as evidence.

| Result | Useful next action |
| --- | --- |
| A credible benefit under the tested conditions | Consider an MVP that supports the selected teaching pattern while retaining the study's limits. |
| No benefit, or a harmful tradeoff | Retain the simpler experience or investigate another explanation; do not keep adjusting the outcome definition until the idea wins. |
| Inconclusive evidence | Explain what is unresolved and select an informative follow-up if it fits the objective and resources. |
| Invalid collection or scoring | Identify the defect, repair it, and verify the affected evidence before drawing the conclusion. |

The two-round rule applies after two unsuccessful repair-and-verification attempts on the same identified defect. It does not limit the number of informative questions or valid negative studies. A different approach must retain the earlier failure history and remain within scope and resources.

## Transfer the evidence into an engineering decision

A useful handoff records the claim, applicable readers/material, supporting and contrary evidence, unresolved questions, and the candidate behavior. A finding about one note format does not become a universal requirement for every subject.

If implementation is selected, an illustrative MVP contract could be:

- Authors can create a note with a definition and an optional worked example.
- Readers can distinguish explanatory material from an assessment question.
- Existing notes remain readable when no worked example is supplied.
- Draft content is preserved when validation fails.
- The relevant keyboard and screen-reader interactions are checked in the actual interface.

These are software acceptance conditions. They remain distinct from any claim about learning effectiveness. Independent verification covers substantive implementation changes and the exact candidate; a scientific conclusion needs evidence appropriate to that claim.

## Deliver for a declared operating target

Prepare a complete author-and-reader path, suitable data handling, accessible interaction, reproducible setup, observable failures, and maintenance ownership. Verify saving, invalid input, recovery, and compatibility with existing notes. A useful MVP may need a substantial design decision if those requirements cannot fit the existing model.

A controlled trial with real users needs its own operating limits, support, monitoring, and recovery plan. Wider availability requires the relevant readiness evidence and an accountable release decision. Passing local checks does not establish user benefit or release readiness.

The roadmap can change as evidence improves. It might prioritize clearer definitions instead of worked examples, or conclude that further software work is unnecessary. Keep useful evidence and record why the direction changed.

## Evaluate the agent workflow

Compare the quality of the question, evidence, alternatives, handoffs, and delivered behavior. Record unnecessary repetition, unsupported claims, useful specialist contributions, and user interventions. Measure actual elapsed time and usage when comparing workflows; do not infer efficiency from shorter prompts or fewer agents.
