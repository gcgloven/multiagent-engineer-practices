"""Exercise parser boundaries and prevent misleading fixture summaries."""

import csv
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from analyze_and_verify import ROOT, analyze
from processor import baseline, candidate


class QuantityChecks(unittest.TestCase):
    def test_existing_integer_and_decimal_values_are_preserved(self):
        for text, wanted in [("0", Fraction(0)), (" 12 ", Fraction(12)),
                             ("0.125", Fraction(1, 8)), ("2.50", Fraction(5, 2))]:
            with self.subTest(text=text):
                self.assertEqual(baseline(text), wanted)
                self.assertEqual(candidate(text), wanted)

    def test_fraction_and_mixed_number_gap_is_reproduced_and_fixed(self):
        for text, wanted in [("7/8", Fraction(7, 8)), ("9/4", Fraction(9, 4)),
                             (" 4  2/3 ", Fraction(14, 3))]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    baseline(text)
                self.assertEqual(candidate(text), wanted)

    def test_decimal_result_is_exact(self):
        self.assertEqual(candidate("0.1") + candidate("0.2"), Fraction(3, 10))

    def test_ambiguous_or_unsupported_notation_is_rejected(self):
        for text in ("-1/2", "1/0", "1 0/2", "1 2/2", "1.5/2", "1/2/3",
                     "1 cup", "½", "1,5", "1-2", ".5", "1e3", "NaN", "inf", ""):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    candidate(text)

    def test_non_text_input_is_rejected(self):
        for parser in (baseline, candidate):
            for value in (None, 1, 0.5, []):
                with self.subTest(parser=parser.__name__, value=value):
                    with self.assertRaises(TypeError):
                        parser(value)


class AnalysisFixtureChecks(unittest.TestCase):
    def setUp(self):
        with (ROOT / "observations.csv").open(newline="") as source:
            self.rows = list(csv.DictReader(source))

    def analyze_rows(self, rows):
        with tempfile.TemporaryDirectory(prefix="cookbook-fixture-") as directory:
            path = Path(directory) / "observations.csv"
            with path.open("w", newline="") as target:
                writer = csv.DictWriter(target, fieldnames=self.rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            return analyze(path)

    def test_results_keep_failure_cases_and_rejected_inputs_visible(self):
        result = self.analyze_rows(self.rows)
        self.assertEqual(result["cases_checked"], 18)
        self.assertEqual(result["baseline_failure_count"], 6)
        self.assertEqual(result["candidate_failure_count"], 0)
        self.assertEqual({row["notation"] for row in result["baseline_failures"]}, {"fraction", "mixed"})
        self.assertEqual(result["by_notation"]["invalid"],
                         {"cases": 6, "baseline_correct": 6, "candidate_correct": 6})
        self.assertEqual(len(result["observations"]), 18)

    def test_subset_reports_actual_coverage_without_inventing_missing_groups(self):
        result = self.analyze_rows(self.rows[:3])
        self.assertEqual(set(result["by_notation"]), {"integer"})
        self.assertEqual(result["cases_checked"], 3)
        self.assertEqual(result["baseline_failure_count"], 0)

    def test_duplicate_case_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate case ID"):
            self.analyze_rows(self.rows + [self.rows[0]])

    def test_invalid_expected_value_is_rejected(self):
        rows = [dict(row) for row in self.rows]
        rows[0]["expected_denominator"] = "0"
        with self.assertRaisesRegex(ValueError, "invalid expected quantity"):
            self.analyze_rows(rows)

    def test_missing_or_inconsistent_oracle_is_rejected(self):
        for field, value in (("expected_outcome", "unknown"), ("notation", "invalid")):
            with self.subTest(field=field):
                rows = [dict(row) for row in self.rows]
                rows[0][field] = value
                with self.assertRaises(ValueError):
                    self.analyze_rows(rows)


if __name__ == "__main__":
    unittest.main()
