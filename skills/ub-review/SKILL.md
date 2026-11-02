---
name: ub-review
description: Independently review software correctness and test effectiveness using scoped ub-mode-inspired inspection, adversarial cases and selected complexity, duplication and mutation checks.
---

# Independent software and test review

This is an original adaptation of [ub-mode](https://github.com/unclebob/ub-mode/blob/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f/SKILL.md). Review the exact accepted candidate and criteria, including the agreed base-to-candidate change and affected contracts. Do not rely only on a tool's working-tree `--changed` option for committed work.

Trace important acceptance conditions to observable tests. Inspect failure paths, boundaries, state, resource handling and concurrency as applicable. Develop independent counterexamples; challenge assertions that can pass while required behavior is broken. Reuse current trustworthy evidence and run missing material checks within budget.

Use quick-MVP, standard or rigorous scope from the assignment. Standard adds applicable complexity/coverage and duplication assessment. Rigorous adds targeted mutation and integration/failure checks. Run passing baseline tests before interpreting mutation results. Tools are evidence sources, not the reviewer.

For Crapper, missing coverage or no analyzed functions is not success. The upstream below-10 target is strict; a CLI threshold of 10 alone allows equality. For Dryer, explicitly select 0.8 when using that policy; its default is 0.82 and duplicate reports may exit zero. Review semantic duplication and justify exceptions rather than forcing abstraction. For Mutator, distinguish survivors, uncovered sites, zero executed sites, compile failures and timeouts. Reconsider cached kills after test or dependency changes. Python wrapper checks do not cover C/C++ or CUDA internals.

Use the configured quality runner and project commands; report required unavailable checks as blocked or partial. Bound paths, workers and wall time. Do not invent a universal mutation percentage or require future features to accept the current increment.

Consolidate findings into blocking defects, evidence gaps and optional improvements. Include location, evidence, impact and closure check. Diagnostic tests may be authored independently; production repairs return to the author. If the reviewer writes production code, another qualified reviewer owns approval of that change.

Return the candidate, criteria and inspected scope, actual results, findings and limitations. Re-review only repairs and affected regressions unless new evidence justifies more. Technical PASS does not grant human approval, a release, or more budget.
