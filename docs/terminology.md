# Optional IDs for requirements, decisions, and evidence

These prefixes provide stable references when a coordinated engineering task needs to connect goals, requirements, decisions, criteria, and evidence across artifacts or handoffs. They are not a universal schema or document checklist. Open research may follow the question, method, and project in a more natural form, such as notes, a source map, a paper-review structure, or a locally useful convention. Use IDs only when they improve the work, unless a user or project explicitly requires them. These references live inside the authoritative task or artifact; they are not new Multica issue types or separate required documents.

This vocabulary belongs to the project or selected workflow, not individual agent prompts or reusable skills. A worker receives only the conventions and criteria relevant to its assignment, with accessible source references or the needed text. Direct specialist requests can use plain language or the caller's own conventions.

| Prefix | Meaning | Use it when | Example |
| --- | --- | --- | --- |
| `G-` | Product or project goal | The outcome explains why the work matters. Internal R&D goals count. | `G-1`: Help readers apply a concept to a new question. |
| `U-` | User story | A stakeholder's workflow or benefit needs clarification. | `U-1`: As a note author, add a worked example beside a definition. |
| `FR-` | Functional requirement | Describe behavior the system must provide. | `FR-1`: Save and display an optional worked-example section. |
| `BR-` | Business or domain rule | A policy or invariant constrains valid behavior. It need not be commercial. | `BR-1`: A validation error must preserve the author's existing draft. |
| `AC-` | Acceptance criterion | Define observable evidence required to accept the current scope. | `AC-1`: An invalid replacement leaves the saved draft unchanged. |
| `KPI-` | Success metric | Track whether the capability achieves the intended outcome. | `KPI-1`: Correct answers on predefined unseen application questions, with missing responses reported. |
| `OP-` | Open question / unresolved decision | Record uncertainty with an owner and the decision it blocks, if any. | `OP-1`: Would clearer definitions help more than adding worked examples? |
| `RISK-` | Risk item | A possible adverse outcome needs an owner, mitigation, or acceptance decision. | `RISK-1`: Longer notes may increase reading effort without improving application. |
| `ADR-` | Architecture decision record | A consequential design choice needs its rationale, alternatives, and revisit condition preserved. | `ADR-1`: Make worked examples optional so existing notes remain readable. |
| `FINDING-` | Review finding | An observed problem needs evidence, a responsible owner, and a verifiable closure condition. | `FINDING-1`: Saving an invalid example overwrites the previous draft. |

`G-` means goal. Use descriptive gate names such as “experiment accepted” or “pilot ready”; do not also call gates `G-1`.

## Important distinctions

**FR versus BR versus AC:** FR states the capability; BR constrains valid behavior; AC says how this candidate will be accepted. One criterion may cover several rules, and several criteria may be needed for one requirement.

**KPI versus AC:** a KPI is a measure, not automatically a release gate. Define its unit, population, measurement window, baseline, and conditions. When a threshold determines acceptance, reference the KPI from an AC and specify the threshold and evaluation method there. Do not silently turn every monitored metric into a blocker.

**OP versus RISK versus FINDING:** OP is what is unresolved; RISK is what might go wrong; FINDING is what a review actually observed. Mark which OPs block the current action. Unrelated questions can stay open, and an experiment can be the authorized work that resolves an OP. “Inconclusive within the budget” is a valid recorded answer, not permission to pretend the uncertainty is resolved.

**ADR versus plan:** keep ADRs for significant tradeoffs or hard-to-reverse decisions. Routine implementation choices do not need a separate record.

## Use the convention when it helps

- Engineering work with cross-task traceability: use the relevant goal, requirement, criterion, decision, or finding IDs; omit categories that do not apply.
- Open research: choose a fitting structure for the inquiry. Natural-language questions, source/evidence links, competing explanations, and learning checkpoints are often enough; no canonical ID prefixes are required.
- An MVP: add IDs for the behavior, evidence, decisions, and risks that need stable references; do not fill unused categories.

Keep related entries together in the issue or a working document. Separate files when ownership, size, or reuse makes that useful. Do not create a ticket for every ID.

## Linking and revision

An example relationship is `G-1 → FR-1 + BR-1 → AC-1 → check result @ candidate v2`. A `FINDING-1` then points to the violated AC/BR, actual evidence, impact, owner, and closure check. A KPI can also feed an AC. A research OP can resolve to evidence without creating an FR.

IDs are stable within their document or task. Across tasks, cite **artifact link + ID**, or an explicit task namespace. Do not renumber existing entries for neatness or reuse a retired ID. Put definitions in one authoritative place and link to them from handoffs.

When an entry's meaning changes, record the revision and reassess only the dependent evidence and gates. A prior PASS does not automatically survive changed requirements, data, code, or measurement conditions. Retain superseded decisions and findings when they explain the current result.

A blocking finding needs a stable problem identity for the [repair loop](leader-loop.md). Merging duplicates or moving the work to another issue must preserve its attempt history. An optional improvement is explicitly nonblocking. If a review discovers a missing acceptance condition, have the owner resolve it; do not invent a requirement simply to fail the candidate.

Some projects use these prefixes as strict artifact conventions; honor that requirement when it is supplied. Otherwise, keep the structure proportionate to the work. Nonblocking questions may remain open, and inquiry can evolve without turning every question into a requirement or every result into a decision.
