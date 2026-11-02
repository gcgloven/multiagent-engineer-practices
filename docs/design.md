# Design decisions and sources

## Intended users and first release

This kit serves engineers who also investigate research, interpret data, build experiments, and deliver software for internal stakeholders. It supports open-ended learning as well as a roadmap from small useful MVPs to internal services, operational pilots, and live industrial deployments.

The first release targets Multica. Direct specialist assignment and a coordinated squad are both supported. A specialist handles ordinary supporting tasks; a lead coordinates distinct specialists. Independent verification is reserved for substantive code changes, consequential scientific claims, and release readiness. Scope changes, substantial resources, and release boundaries remain explicit decisions under the user's authority.

Three worked journeys cover research → experiment → MVP, analytics → engineering, and existing code → reliable delivery. The latter two include runnable local teaching fixtures. Full product/GTM work is an optional scope expansion. Codex and Claude adapters are deferred until a Multica pilot demonstrates useful behavior. A CLI installer provisions configuration and supports explicit updates; this version has no model API framework, custom scheduler, or automatic execution of a cross-squad pipeline.

## Concepts adapted from the references

| Concept | Application here |
| --- | --- |
| Substantive, composable methods | Twelve skills with procedures, focused references, and useful working records; supporting depth is loaded when useful. |
| Clarification and shared terminology | Clarify consequential unknowns; keep project terms and units with project context. A clear task needs no compulsory interview. |
| Small working increments and feedback loops | Build one observable slice; test behavior and measurement validity at meaningful boundaries. |
| Source-based research and cheap prototypes | Inquiry can end in understanding. Experiments preserve scientific validity even when implementation is temporary. |
| Deep modules / narrow interfaces | Encapsulate current complexity and replaceable decisions; avoid speculative layers. |
| Separate roles, methods, coordination, and task context | Agent profiles, skills, squad policy, and a compact issue brief have different responsibilities. |
| Capability-driven teams and routing | Profiles are available capabilities. Direct assignment and coordinated specialist work are first-class paths; team size follows expertise, uncertainty, and consequence. |
| Concrete evidence handoffs and bounded repair | The squad preserves candidate identity, decisive evidence, findings, and its repair history; assignments carry the relevant stop condition. |
| Progressive disclosure | Each agent receives shared evidence/ownership principles plus its specialty. Squad terminology and loops stay with the squad; assignments pass only the applicable conventions. |
| Divergent and convergent problem solving | Discovery can broaden or reframe; design compares credible alternatives. Learning checkpoints do not force delivery gates onto research. |
| Distinct learning and repair loops | Preserve exploratory analysis and valid negative experiments. Count failed repairs only against an identified defect and verification boundary. |

We adapt the principles rather than reproducing a full starter pipeline. Fixed reviewer rosters, mandatory document chains, maximum parallelism, and generic research-to-product progression do not fit every task. Scientific experiments also need stronger measurement discipline than a disposable UI sketch.

Efficiency means avoiding waste across the whole task, including incorrect framing, premature convergence, weak measurements, and costly redesign. A deeper study, additional perspective, or larger architectural change can be the appropriate choice. See the [skill design crosswalk](skill-design.md) for the reference methods used.

## Reusable agents, selectable loops

The English [Multica Best Practices templates](https://github.com/it235/multica-best-practices) show the useful pattern: `software-development`, `software-development-reviewed`, and `bug-fix` reuse roles while changing the squad's sequence and review loop. Its software-development README explicitly puts routing in the squad and warns that copying the full workflow into each agent creates redundancy and contradictions. Its squad instructions define the artifact vocabulary and advancement rules.

We adopt that separation, with five workflows: open research, engineering design, analytics to engineering, software delivery, and a mixed research/engineering squad. We do not copy every reference restriction: some reference agents still assume a Leader, embed IDs, or hardcode review rounds. Those assumptions would make standalone research and specialist calls unnecessarily dependent on a particular team.

| Configuration layer | Owns | Does not prescribe |
| --- | --- | --- |
| Agent instructions | Specialty, judgment, evidence standards, direct versus assigned return behavior. | An ID dictionary, a particular squad's sequence, or a fixed retry count. |
| Installed skill | A reusable procedure and supporting methods/records. | Squad membership, routing, or an automatic research-to-product pipeline. |
| Squad instructions | Use-case loop, roles to engage, gates, terminology, repair budget, dispatch and return policy. | Every domain method or project-specific acceptance value. |
| Project/issue | Actual objective, sources, candidate, acceptance, scope, permissions, and accessible return destination. | New standing policy for unrelated tasks. |

The generator composes `squads/common.md` with one profile into each deployable squad prompt. This avoids maintaining separate copies of coordination rules. Generated specialist prompts contain none of that squad policy. Since Multica documents that squad instructions reach the Lead, the Lead must include applicable terms, criteria, stop conditions, and return route in every dispatched assignment. A bare ID or repository link that a worker cannot access is insufficient.

Use one mixed squad when continuity matters; use distinct presets when a repeated use case needs a different loop. Share compatible agent identities and method packages across squads. Separate contexts and access explicitly where needed: sharing an agent also shares its configured runtime and bindings, and squad membership is not a security boundary. See [installation](multica-installation.md) for explicit reuse and existing-install migration.

## Product understanding and engineering design

The reference Product Manager separates stakeholder needs, behavior, scope, and acceptance from the Architect's technical options, affected code, interfaces, and implementation risks. Here Product Manager is an independent role for that product perspective and optional explanations. The accepted version 2 setup separates Systems Engineer for consequential domain/architecture decisions from Software Engineer for implementation. Test & Code Review Engineer independently assesses code and test effectiveness; Verifier retains distinct evidence questions. Ordinary code-level design stays with the software owner. Lead coordinates these contributions and does not replace their authorship.

The engineering reference's teaching guidance distinguishes sustained learning from an explanation in passing. `explain-work` adopts audience grounding, concrete examples, and optional feedback without creating course files or quizzes for a quick rundown. Product explanation is not a technical verification gate and does not turn an internal research project into GTM work.

An explicit Engineering Design squad provides a place to decide behavior, compare mechanisms, define interfaces, and prepare the first useful slice. Its acceptance boundary is implementation readiness; delivery still requires evidence about the built candidate. Clear changes can be designed locally in Software Delivery. See [Research → Design → Delivery](research-design-delivery.md) for entry points, optional explanations, and versioned handoffs.

## Sources and attribution

- **Skills For Real Engineers**, Matt Pocock, MIT: [upstream repository](https://github.com/mattpocock/skills). Concepts include source-based research, prototypes, domain modeling, review, incremental delivery, and writing useful agent instructions.
- **Multica Best Practices**, MIT, copyright Multica Squad Playbook Contributors: [upstream repository](https://github.com/it235/multica-best-practices), [license](https://github.com/it235/multica-best-practices/blob/main/LICENSE), checked 2026-11-02. Concepts include requirement framing, technical design, test coverage, verification evidence, and separating role instructions from reusable methods. The [skill design crosswalk](skill-design.md) explains the adaptations; the copyright notice is retained in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
- LangChain's [Subagents guide](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents) is the coordination-pattern reference for the README's supervisor/specialist comparison, checked 2026-11-02. This kit applies centralized delegation and result integration through Multica's issue and callback runtime; it does not import LangChain code or establish LangChain's default worker-state semantics.
- Public Multica documentation and installed CLI help establish configuration details. The official [squad composition and execution guide](https://multica.ai/docs/squads), [agent configuration guide](https://multica.ai/docs/agents-create), [skills guide](https://multica.ai/docs/skills), and [complete setup tutorial](https://multica.ai/docs/tutorial) are linked from the README and were checked 2026-11-02. See also the [local setup guide's sources](../integrations/multica/README.md). They do not prove that a particular self-hosted runtime behaves identically.
- Design Council's [Framework for Innovation](https://www.designcouncil.org.uk/resources/framework-for-innovation/) informs the distinction between divergent and convergent discovery and design. The linked source is credited under its stated CC BY 4.0 terms; no source diagram is reproduced.
- External PDF skills and tools are source-linked in [PDF capabilities](pdf-capabilities.md). They are recommendations, not bundled dependencies, and retain their respective license terms.

The wording in this kit is newly authored. Upstream MIT notices are retained in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for attribution and reuse clarity. No performance improvement is claimed from prompt size alone.

## Required review surfaces

Efficiency removes repeated coordination, not the reasoning needed for a decision. Substantial engineering requires a PRD, architecture and MVP roadmap with evidence-backed phase gates before implementation. These can share the [living engineering brief](../templates/engineering-brief.md). A narrowly eligible correction inherits its existing contract; a new feature does not become a correction because its code is short. The [workflow](workflow.md) defines the route and state requirements.

Substantial research concludes with a developed study/discussion result; ordinary paper reviews preserve all seven sections per paper. The Lead checks the complete user request separately from each scoped technical verdict. Canonical documents remain local and agents explain them inline. These requirements address observed failure modes without requiring every available role or an automatic dispatch chain.
