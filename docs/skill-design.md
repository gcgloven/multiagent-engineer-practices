# How the skills are designed

A profile defines a specialist's responsibility. A skill teaches a method: when to use it, how to reason and act, what evidence to inspect, how to adapt depth, and what a useful result contains. The squad coordinates work; project context supplies actual systems, data, authority, and commands. This separation keeps a scientific method reusable without turning every agent prompt into a handbook.

The [Multica Best Practices skill library](https://github.com/it235/multica-best-practices) provides the main structural reference: an actionable entry point backed by focused references, traceability rules, templates, and helpers. Its platform-specific workflow is not a prerequisite for these methods. The source's [MIT license](https://github.com/it235/multica-best-practices/blob/main/LICENSE) and the method-level adaptation crosswalk are recorded here; source and license checked 2026-11-02. See [design.md](design.md) for the broader source attribution.

Methods work for both direct specialist requests and coordinated assignments. They preserve caller-provided references and stopping conditions without installing an ID vocabulary, retry count, or squad pipeline of their own. A consequential conclusion can require independent review before adoption while still returning a useful analysis directly to the requester; the method itself does not dispatch a team.

## What each package contains

| Layer | Purpose | How to assess it |
| --- | --- | --- |
| Name and description | Let an agent select the method for an actual request. | Does it identify concrete triggers and adjacent work that belongs elsewhere? |
| `SKILL.md` procedure | Orient the agent, choose a mode, perform the work, assess evidence, and deliver or hand off. | Could a specialist follow it without inventing the whole method? Does it allow justified changes in direction? |
| `references/` | Supply deeper methods, judgment dimensions, worked reasoning, and failure modes. | Are important choices explained, including what would make a conclusion invalid? |
| `assets/` or `templates/` | Preserve useful working state: claims, alternatives, data identity, decisions, and checks. | Does the record help inquiry or handoff? Can irrelevant fields be omitted? |
| Executable helpers, when useful | Make repeated deterministic operations reproducible. | Do they perform a real operation, validate inputs, and expose evidence limits? A skill does not need a script merely to look substantial. |

Read supporting material when its method is needed; do not paste every reference into every run. Conversely, a short entry point is not a substitute for substantive content. Package the whole skill folder so the references it names are actually available to the worker.

The current twelve skills are Markdown method packages. The repository's two runnable examples live under `examples/`; they demonstrate reasoning and verification rather than installing a generic harness. The local archive generator currently accepts Markdown resources in `references/`, `assets/`, and `templates/`. Host installers and quality/pilot runners live under `scripts/`, outside skill archives. Adding executable resources inside a skill archive still needs an explicit packaging and validation change.

## Concepts carried over from the reference

| Reference method | Concept retained | Adaptation here |
| --- | --- | --- |
| `product-manager/multica-pm-requirement-spec` | User need, scope, constraints, dependencies, ambiguity, and acceptance. | `frame-problem` starts with needs and alternative problem frames. Acceptance becomes firm when adopting a delivery promise; open inquiry can retain provisional questions. |
| `architect/multica-technical-design` | Inspect current code, affected components, dependencies, alternatives, risks, and verification. | `design-solution` makes a proposal implementable without assuming it has been built; `deliver-slice` applies proportionate design during implementation. Minimum code or minimum change is not a universal objective. |
| `tester/multica-test-t1-design` and its coverage/design-trace references | Rich reference index; dimensions derived from the actual requirement; traceability between acceptance, design, and checks. | Select relevant behavior, failure, boundary, state, integration, and operating dimensions. Do not cap test counts arbitrarily or turn design details into invented requirements. |
| `tester/multica-test-t2-coverage` | Check implemented coverage against the actual change and expected behavior. | Inspect what tests establish, identify meaningful omissions, and retain valid evidence for unchanged behavior. |
| `reviewer/multica-review-backend` | Concrete review dimensions, actionable findings, blocking versus advisory feedback, and follow-up verification. | Independent verification focuses on consequential claims and changes; a finding includes evidence and a closure check. Optional polishing does not reopen a satisfied gate. |
| `leader/multica-verification` | Acceptance must map to observable evidence; author self-check and independent review differ. | Record which candidate and transition were reviewed. The leader routes evidence instead of duplicating a qualified technical review. |
| `tester/multica-test-orchestration` | Clear input/output contracts and separation of method from integration details. | Keep Multica routing in the integration and squad layers. No mandatory external document system, test platform, or document chain. |

The engineering reference adds domain modeling, useful increments, deep modules, empirical prototypes, source-based research, and reviews tied to behavior. The [problem-framing method](../skills/frame-problem/references/design-methods.md) also uses divergent and convergent thinking: understand and expand possibilities, then make supported choices, returning to discovery when evidence changes the frame. A framework supplies questions and methods rather than prescribing a ceremony for every task.

## Concrete capabilities

| Package | Detailed methods and reusable record | Evidence of usefulness in this kit |
| --- | --- | --- |
| [frame-problem](../skills/frame-problem/SKILL.md) | Stakeholder journey, problem frames, system/domain model, alternatives, tradeoffs; problem-frame template. | The study-note and article-preview examples distinguish an initial request from its underlying need. |
| [design-solution](../skills/design-solution/SKILL.md) | Behavior and interfaces, credible options, evidence-backed assumptions, failure/recovery, first slice and validation; design brief. | Design-only assignments can finish with an implementable proposal; required verification is scoped to the decision rather than nonexistent implementation results. |
| [explain-work](../skills/explain-work/SKILL.md) | Audience and decision, artifact-grounded mechanism, concrete example, tradeoffs and product fit; explanation patterns. | A quick rundown stays concise; a teaching follow-up can deepen it. Proposed, implemented, tested, and verified states remain distinct. |
| [investigate-question](../skills/investigate-question/SKILL.md) | Search strategy, provenance, contradictions, synthesis, question evolution; inquiry ledger. | Research can end in understanding or produce a justified empirical handoff. |
| [review-paper](../skills/review-paper/SKILL.md) | Default seven-section full review; explicit narrower modes; full paper/PDF dissection, primary novelty comparisons, claim/evidence analysis and practical recommendations; claim ledger. | Contract review covers the original depth requirements, including three prioritized proposed experiments. Real-paper runtime evaluation remains pending. |
| [extract-paper-pdf](../skills/extract-paper-pdf/SKILL.md) | Docling conversion, reusable Markdown/JSON with page provenance, bounded reading, full-review coverage, and targeted visual checks. | Bound to Paper Reviewer in the local catalog; CLI guidance is source-checked. Runtime extraction quality and token savings remain unmeasured. |
| [analyze-data](../skills/analyze-data/SKILL.md) | Units, missingness, distributions, interactions, confounding, sensitivity, reproducibility; analysis ledger. | [Journey B](../examples/analytics-to-engineering.md) separates an authored quantity corpus from executed parser results. |
| [run-experiment](../skills/run-experiment/SKILL.md) | Exploratory/confirmatory design, comparators, measurement validity, repetition, failures, inference, transfer; experiment record. | Journeys A/B separate a valid negative result from broken execution and avoid unsupported performance claims. |
| [deliver-slice](../skills/deliver-slice/SKILL.md) | Code/runtime understanding, design alternatives, behavior checks, compatibility, observability, recovery, release evidence; delivery record. | [Journey C](../examples/code-to-reliable-delivery.md) reproduces article-preview defects and verifies its accepted behavior. |

## Validation and improvement

Check package structure and links, then exercise realistic requests. For inquiry, assess whether the method can follow a worthwhile new question without inventing evidence or forcing a product plan. For engineering, assess whether it reaches the promised acceptance boundary and reveals relevant operating gaps. Test authoring and review independently where consequences require it.

Skill validation, a well-written prompt, or a successful import does not establish runtime capability. A Multica pilot must check resource delivery, PDF/tool access, handoffs, review quality, and actual outcomes. Record observed friction and improve the method that caused it. See [validation](../VALIDATION.md).
