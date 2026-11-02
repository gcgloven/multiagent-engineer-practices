# Workflow and roles version 2

This is the accepted workflow specification for the nine-role setup. It accompanies the executable registry in [catalog.py](../scripts/catalog.py), generated agent instructions and five squad policies. The [setup guide](new-workspace-pilot.md) describes installation and behavioral checks. Human checkpoints and budgets remain agent instructions; these scripts do not enforce a platform-wide scheduler or prevent a separately authorized tool from bypassing them.

| Role | Owns | Boundary |
| --- | --- | --- |
| Lead | Intake, routing, dependencies, approval evidence, remaining budget and integrated outcomes | Does not replace specialist authorship or invent human approval. |
| Scout | Topic exploration, source discovery, technical options and uncertainty | Research recommendations do not start implementation. |
| Paper Reviewer | Scientific mechanism, novelty, evidence, limitations and experiment proposals | Published claims, deductions and reproduced results remain distinct. |
| Analyst | Provenance, measurement contract, calculations, comparisons and interpretation | A pattern or speed claim does not authorize a system change. |
| Product Manager | Stakeholder need, behavior, acceptance and understandable explanations | Product recommendations are not technical approval or release authority. |
| Systems Engineer | Domain model, architecture, interfaces, state ownership and consequential tradeoffs | Ordinary local code design stays with the software owner. Design readiness does not start implementation. |
| Software Engineer | Authorized implementation, developer tests, integration and repairs | Works inside the accepted slice, write scope and budget; cannot provide independent approval of its own code. |
| Test & Code Review Engineer | Independent code inspection, meaningful assertions, adversarial/regression checks and test effectiveness | May create diagnostic tests. Production repairs return to the author; authoring a repair requires another reviewer. |
| Verifier | Scientific claims, measurement validity, qualified design evidence and distinct readiness evidence | Does not add a second generic software review. Its expertise/access must fit the question. |

Software correctness and scientific validity are different questions. A benchmark harness can pass code review while its comparison remains invalid. Routine software delivery uses Software Engineer and Test & Code Review Engineer; add Verifier only for a separate evidence claim. Keep one accountable owner per writable output.

| Squad | Normal route | Conditional contributors |
| --- | --- | --- |
| Research and Engineering | Lead selects the relevant inquiry, design, experiment or delivery loop | All eight specialists are available; only needed roles run. |
| Open Research | Lead → Scout/Paper Reviewer/Analyst as needed → consequential evidence review → research result | A new substantial harness uses an explicit software handoff. No automatic delivery programme. |
| Analytics to Engineering | Analyst → decision about an intervention → authorized software → independent code review and separate claim verification | Systems Engineer for consequential interface/model changes. Valid negative analysis can finish the task. |
| Software Delivery | Accepted slice → Software Engineer → Test & Code Review Engineer → result and applicable human checkpoint | Systems Engineer, PM and Verifier for distinct architecture, product or evidence questions. |
| Engineering Design | Scope proposal → human direction → Systems Engineer design → qualified review → numbered roadmap proposal | PM for requirements; Software Engineer for feasibility; Test & Code Review Engineer for testability or authorized prototype code. |

Lead first identifies the desired output and existing authority. For an ambiguous general task, offer roadmap planning versus a bounded quick MVP once. A clear review, explanation or correction retains its route. An explicit, sufficiently specified quick-MVP build request supplies execution authority without a redundant approval ceremony.

For substantial roadmap work, use the following human checkpoints:

1. Present the intended behavior, exclusions, credible technical alternatives, key assumptions and effort for scope/approach approval.
2. Develop the approved direction and present a numbered roadmap with owners, dependencies, acceptance, budgets and decision points. Obtain approval before creating or materially restructuring live children.
3. Create approved children in backlog. Activate only the exact milestone covered by human execution authority. Return its demonstration and technical evidence for human acceptance before the next milestone unless the user already authorized named milestones and their total budget.

An explicit request for early draft children permits proposed backlog records only. Technical PASS, a callback, silence, elapsed time, an assignment or an explanation request cannot substitute for human approval. Preserve the actual human source, approved artifact revision, scope, permitted next action, budget and stop point. Reuse precise existing approvals.

Use `[MVP01]` for a demonstrable milestone, `[MVP01-SUB01]` for a work package within it, or `[SUB01]` for a flat backlog. Keep numbers stable. State dependencies, stage and parallel siblings explicitly; numerical order alone does not establish a dependency. Issue IDs remain authoritative.

Each assignment includes the requested outcome, mode, exact inputs/candidate, acceptance/review scope, required method and quality depth, allowed write paths, relevant approval, budget and return destination. Implementation and review detail stay in the child; the parent receives decisions, milestones, material blockers and the final synthesis. One callback triggers one decision, not a duplicate dispatch chain.

Count total implementation, review and repair effort against one remaining budget. After two unsuccessful repair-and-verification rounds for the same identified defect, stop that approach and present the evidence and smallest next decision. A materially different bounded approach within existing authority may proceed with recorded rationale. Renaming a finding, changing an agent or opening a new chat does not reset the count or budget.

| Method | Roles | Required behavior |
| --- | --- | --- |
| `ub-coding` | Software Engineer; Analyst for maintained code | Meaningful behavior tests, small checked changes, root-cause repair and scoped refactoring. |
| `ub-review` | Test & Code Review Engineer | Independent inspection and counterexamples; interpret actual quality evidence and report actionable closure checks. |
| `ub-design` | Systems Engineer | Domain boundaries, explicit state ownership, idempotency where required and verifiable increments. |

These methods are original adaptations with attribution to pinned upstream ub-mode. They do not grant Git-push, release, cleanup or scope-expansion authority. Quick-MVP quality covers its demonstration and correctness. Standard adds applicable coverage/complexity and duplication assessment. Rigorous adds targeted mutation and risk-specific integration/failure checks. Required unavailable checks are gaps; optional hardening stays optional.

Crapper, Dryer and Mutator are installed together in a pinned environment, including explicit parser provisioning. The research pack adds PDF extraction/rendering and numerical/plotting libraries. Project-specific testing/coverage, browser or image access, GPU libraries and robotics engines still need the appropriate project/runtime configuration. No Python wrapper measurement certifies an unsupported C/C++ or CUDA kernel.

The old generic Engineer source remains as a migration reference and is no longer generated. Installation creates the two specialized engineering roles and the independent code reviewer. An old live Engineer identity is not renamed or deleted; active work needs an explicit transition. Shared Verifier and other managed profiles are refreshed only through the explicit update mode. A fresh workspace is the recommended pilot target.

Use [the setup and new-workspace pilot guide](new-workspace-pilot.md) to provision, seed and launch the test suite. Configuration read-back, host fixture success and observed managed-run behavior are reported separately.
