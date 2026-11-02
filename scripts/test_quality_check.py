import argparse
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

import quality_check as quality


class QualityTests(unittest.TestCase):
    def test_missing_zero_or_null_analysis_is_not_pass(self):
        for entries in ([], [{'coverage': None, 'crap': None}], [{'coverage': 0, 'crap': 2}]):
            self.assertEqual(quality.assess({'entries': entries}, {'candidates': []})['state'], 'evidence-gap')

    def test_exact_threshold_and_duplicates_require_review(self):
        report = quality.assess({'entries': [{'coverage': 100, 'crap': 10}]}, {'candidates': [{}]})
        self.assertEqual(report['state'], 'review-required')
        self.assertEqual(len(report['review_items']), 2)

    def test_zero_mutants_and_uncovered_are_gaps(self):
        crap = {'entries': [{'coverage': 100, 'crap': 1}]}
        for reports in ([], [{'forms': [{'killed': 1, 'uncovered': 2}]}]):
            self.assertEqual(quality.assess(crap, {'candidates': []}, reports)['state'], 'evidence-gap')

    def test_failing_baseline_cannot_succeed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'source.py').write_text('value = 1\n')
            args = argparse.Namespace(repo=root, paths=['source.py'], profile='quick-mvp',
                                      test_command=f'{sys.executable} -c "raise SystemExit(1)"', seconds=10, workers=1)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(quality.run(args), 2)

    def test_unsupported_source_stops_before_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'kernel.cu').write_text('')
            args = argparse.Namespace(repo=root, paths=['kernel.cu'])
            with self.assertRaises(quality.QualityError):
                quality.run(args)


if __name__ == '__main__':
    unittest.main()
