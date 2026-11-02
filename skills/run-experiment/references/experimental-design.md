# Experimental design and validity

## Match the design to the claim

| Claim / uncertainty | Design considerations | Failure to avoid |
| --- | --- | --- |
| Candidate improves a metric | Comparable workload, baseline implementation, resources, interval, correctness; paired inputs when appropriate. | Comparing an optimized small workload to an unoptimized large one. |
| A parameter causes an effect | Control/randomize other factors; identify units and confounders; use suitable interventions. | Calling observational association causal. |
| Factors interact | Cover necessary combinations; distinguish balanced designs from failed/missing cells; explain interaction scale. | Inferring interactions from disconnected aggregate endpoints. |
| Behavior stays correct | Domain invariants, boundary/adversarial states, valid differential/reference checks. | Treating successful parsing as proof that the resulting content is correct. |
| Result generalizes | Representative conditions, sensitivity, environment variability, held-out evaluation where appropriate. | Treating one synthetic trace as the entire operating envelope. |
| Published result reproduces | Original code/data/config/version and tolerance; document substitutions and implementation differences. | Calling a conceptual reimplementation an exact reproduction. |
| Interaction is useful | Representative scenarios and feedback from intended users when available. | Reporting agent opinion as user research. |

## Measurement and analysis

For decisive metrics specify numerator, denominator, unit, aggregation, window, and population. For a timed task, state whether reading, preparation, and review are included. Account for failures and censored/incomplete observations; a success-only estimate describes a selected subset rather than the whole population.

For speedup preserve workload and correctness parity. Explain replication units, observation dependence, and uncertainty. Thousands of correlated events from one run are not thousands of independent runs. Separate exploratory comparisons from later confirmation; handle selection and multiple comparisons in proportion to the claim.

Inspect distributions, boundary conditions, and interactions rather than relying only on a mean. Preserve failed conditions and distinguish a measurement failure, implementation failure, and valid unfavorable outcome. Check alternate reasonable exclusions or transformations to see whether the conclusion depends on an analysis choice.

## Review questions

Can a qualified reader reproduce the decisive calculation? Are transformations traceable? What remains untested? Does the claim exceed the design? Was a favorable comparison selected after seeing results but presented as preplanned? Would another plausible measurement definition reverse the conclusion?

Use these checks to establish evidence quality. Rigor follows the conclusion asserted and its consequences; behavioral prototypes and scientific benchmarks need different forms of validity.
