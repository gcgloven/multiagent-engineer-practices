---
name: ub-coding
description: Apply scoped ub-mode-inspired coding discipline to authorized software changes or maintained analytical code, with behavior tests and risk-appropriate quality tools.
---

# Scoped software construction

This is an original adaptation of [ub-mode](https://github.com/unclebob/ub-mode/blob/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f/SKILL.md), not a claim of full upstream compliance.

Establish the accepted behavior, candidate, allowed paths, test command, quality profile and budget. Make the smallest coherent change that achieves the outcome. Prefer an honest failing behavior test, observe its meaningful failure, implement, then check regressions. Explain when an automated test is impractical. A test that merely echoes implementation is not useful evidence.

Inspect the data model and boundaries before adding logic. Keep state ownership explicit, validate external inputs at entry, and make retries or repeated operations safe where the contract requires it. Reproduce and fix the cause of defects. Refactor in small checked units; changing the system model requires the applicable design decision.

Quick MVP: check the promised demonstration and its correctness within the compact brief. Standard: add relevant coverage/complexity and duplication assessment for affected code. Rigorous: add targeted mutation and risk-specific failure/integration checks. Use runtime-provided `crapper`, `dryer`, `mutator` and the repository quality runner when installed. An unavailable required check is a gap, never PASS. Do not install project dependencies opportunistically during a review; use the configured environment and explicit test commands.

Metrics guide judgment within scope. Preserve justified exceptions and expose unsupported languages or uncovered behavior. Do not expand a bounded slice into repository-wide cleanup, or treat an exhausted budget as a fresh allocation on another activation.

Return behavior, exact candidate, commands/results, independent-review needs and limitations. Keep detailed logs with the child evidence and summarize decisive results. Git pushes, releases and cleanup of unrelated work require their actual task authority; this skill grants none.
