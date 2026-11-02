# Analytics → engineering: understand cookbook quantity failures

This worked example begins with a question about a fictional cookbook editor and ends with a verified parser change. All input strings and expected answers are **authored teaching fixtures**. The reported success and failure counts come from executing the local Python implementations against those fixtures. They are not observations of cookbook users or estimates of how frequently a format appears in real recipes.

## Start with an inquiry

The initial question is: “Which ingredient quantities can this editor read, where does it fail, and what improvement would be justified?” An analyst can begin directly with [analyze-data](../skills/analyze-data/SKILL.md). A lead can coordinate the engineer and independent verifier when the inquiry develops into implementation.

Several explanations deserve attention: an unsupported number format, ambiguous units, locale-specific notation, incorrect expected answers, or a mismatch between the editor's intended contract and its implementation. A useful outcome could be a clarified contract or more examples to investigate. There is no requirement to choose a code change before inspecting the evidence.

For this exercise, the editor reads a quantity separately from its unit and ingredient name. The [fixture](analytics-to-engineering/observations.csv) intentionally samples integers, decimal numbers, fractions, mixed numbers, and invalid inputs. Its expected answers are exact rational values that a reviewer can check by hand. An empty input and malformed quantities remain in the fixture rather than being removed as inconvenient rows.

## Inspect the results by notation

The [analysis script](analytics-to-engineering/analyze_and_verify.py) runs both implementations and compares their outputs to the authored expected answers. A correct result means either returning the specified rational value or rejecting a deliberately unsupported input.

| Fixture group | Cases | Baseline correct | Candidate correct |
| --- | ---: | ---: | ---: |
| Integer | 3 | 3 | 3 |
| Decimal | 3 | 3 | 3 |
| Fraction | 3 | 0 | 3 |
| Mixed number | 3 | 0 | 3 |
| Invalid input | 6 | 6 | 6 |

The six baseline failures cluster in two notation groups. The raw report retains each input, its expected result, and both actual outputs. This supports a specific observation: this baseline rejects the fixture's valid fractions and mixed numbers. The distribution was deliberately constructed, so “one-third of users encounter failures” would be an unsupported claim.

Inspection of the [implementation](analytics-to-engineering/processor.py) explains the observed gap: the baseline recognizes only integer and decimal strings. This is direct evidence about this parser. It does not establish that the editor should accept every form used in cookbooks.

## Explore options and adopt a contract

Reasonable options include documenting decimal-only input, normalizing quantities before they reach the parser, or extending the parser with explicit fraction rules. A broader editor might also need Unicode fractions, locale-aware decimals, ranges, approximate quantities, or unit conversion. Those capabilities need their own requirements and examples; this exercise leaves them unresolved rather than silently interpreting them.

The chosen teaching change adds ordinary fractions and mixed numbers. Both implementations return Python's standard-library `Fraction`, keeping values exact without introducing an external dependency. The mixed-number rule requires a positive proper fractional part; `1 3/2` is rejected as unsupported notation, while the standalone improper fraction `5/2` is valid.

| Identifier | Adopted meaning |
| --- | --- |
| `FR-1` | Parse nonnegative integer, decimal, fraction, and mixed-number quantities into exact rational values. |
| `AC-1` | Preserve the existing integer and decimal results, including surrounding whitespace. |
| `AC-2` | Correctly parse the declared fraction and mixed-number examples; never divide by zero. |
| `AC-3` | Reject unsupported or ambiguous notation without guessing a unit, range, sign, or locale. |
| `OP-1` | Which additional notation should a future editor support, and how would users resolve ambiguity? |
| `RISK-1` | A deliberately small authored fixture cannot establish coverage of real recipe collections. |

The contract is a decision supported by the inquiry. The inquiry could instead continue by assembling a diverse, appropriately licensed sample, reviewing ambiguous formats, or consulting intended users before choosing a broader parser design.

## Implement and verify

Run from the repository root:

```bash
python3 -B examples/analytics-to-engineering/analyze_and_verify.py
python3 -B -m unittest discover -s examples/analytics-to-engineering -p 'test_*.py' -v
```

The first command produces a report for **18 authored cases**. The baseline matches 12 expected outcomes; the candidate matches all 18. The [checked-in report](analytics-to-engineering/verified-results.json) records fixture and implementation hashes, group counts, and all outcomes. Regenerate it by redirecting the first command's output to that file.

The second command runs **10 tests**, with additional cases beyond the CSV. They reproduce and fix the fraction gap, preserve existing behavior, check exact decimal arithmetic, reject unsupported forms and non-text inputs, and verify that the analysis rejects duplicate identifiers and invalid expected answers. A reduced fixture must report its actual coverage rather than inventing absent groups. These checks exercise correctness; they do not measure speed or certify a production editor.

For a real delivery, an independent verifier would inspect the candidate revision, challenge the accepted notation and omitted boundaries, and rerun the relevant checks. This example contains executable local checks, not evidence of a live squad review. If that review identifies a blocking defect, repair and reverify it. After two unsuccessful repair rounds on the same defect, report the evidence and next decision. Exploring a new notation or revising the question does not consume that repair counter.

## Decide the next step from the evidence

The evidence supports the candidate's behavior on the declared cases and tested boundaries. Integration into an editor would still require checking how quantities are entered, how errors are displayed, and how exact values are stored and shown. It would also require a representative coverage decision and an owner for future notation changes.

Record the chosen next step and remaining questions in an [analysis ledger](../skills/analyze-data/assets/analysis-ledger.md). The handoff should explain the observed gap, the accepted grammar, the implemented change, the evidence, and what remains uncertain. It should preserve useful discovery without turning a fixture-level result into a claim about all recipes.
