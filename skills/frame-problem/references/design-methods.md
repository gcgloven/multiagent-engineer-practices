# Selecting a framing method

Use methods to answer real questions. Combine or revisit them as the investigation develops.

| Situation | Method | Useful artifact / check |
| --- | --- | --- |
| A solution is requested but its purpose is unclear | Walk through a concrete stakeholder task: trigger, inputs, steps, decisions, pain, workaround, desired outcome. | Current journey and opportunity statement; distinguish observed behavior from assumptions. |
| Disciplines use the same word differently | Build a domain model using examples and counterexamples. Define entities, events, states, units, invariants; compare with code/data. | Shared terms and state/context diagram; preserve unresolved disagreement. |
| Symptoms cross services or people | Map system boundaries and ownership. Follow a real unit of work end to end. | Candidate failure locations and missing measurements; a diagram is not proof of a bottleneck. |
| Several causes fit the evidence | Compare explanations, predicted observations, supporting/contrary evidence, and discriminating probes. | Next probes selected for information value; plausible causal stories remain hypotheses. |
| Design is narrowing prematurely | Compare operational, algorithmic, interface, and architectural alternatives that fit the problem. Include status quo and improving measurement where credible. | Tradeoffs and unresolved assumptions, with no predetermined winner. |
| An abstract idea is difficult to evaluate | Sketch a workflow/interface, enact a scenario, or build a behavioral prototype. Use feedback to refine problem and design. | Concrete interaction evidence; identify who actually evaluated it. |
| A choice must survive handoff | Record decision, alternatives, rationale, evidence, consequences, reversibility, and revisit trigger. | ADR for consequential choices; routine decisions can stay in the task. |

## Divergence and convergence

The Design Council's Double Diamond alternates exploration and focus across discovering a problem, defining it, developing possibilities, and delivering a solution. It permits returning to earlier understanding. Here it is a thinking aid, not four compulsory documents or approval gates. [Design Council Framework for Innovation](https://www.designcouncil.org.uk/resources/framework-for-innovation/).

Combine stakeholder understanding with explicit technical models, measurements, and constraints. Design thinking does not replace numerical correctness, experimental controls, interface contracts, or operational assurance. A passing test also cannot establish that the right stakeholder problem was solved.

## Traps to check

- **Premature criteria:** early targets may be hypotheses or preferences. Mark their status; confirm decisive criteria before the evaluation used for adoption.
- **Minimal-change fixation:** a patch may preserve the cause. Compare lifecycle cost and operating fit, not line count alone.
- **Framework theater:** filled boxes are not evidence. Use artifacts that improve reasoning or handoff.
- **Endless divergence:** checkpoint learning, prune disproven branches, and examine the value of further inquiry. A checkpoint need not end the conversation.
- **Unsupported consensus:** preserve conflicts and decision authority. Do not fabricate interviews, measurements, or approval.
