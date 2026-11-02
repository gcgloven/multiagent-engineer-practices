#!/usr/bin/env python3
"""Real-tool fixtures in a disposable directory, never in a user's project."""
import argparse
from pathlib import Path
import shlex
import tempfile

from quality_check import read_edn, assess, execute
import time


def smoke(binary):
    binary = binary.resolve()
    python = binary / 'python'
    with tempfile.TemporaryDirectory(prefix='multica-tool-smoke-') as temp:
        root = Path(temp)
        (root / 'subject.py').write_text('def decide(age):\n    if age >= 18:\n        return "adult"\n    return "minor"\n')
        (root / 'test_subject.py').write_text('import unittest\nfrom subject import decide\n\nclass Tests(unittest.TestCase):\n    def test_weak(self):\n        self.assertIsInstance(decide(18), str)\n')
        repeated = '    total = 0\n    for value in values:\n        if value > 0:\n            total += value * 2\n    return total\n'
        (root / 'duplicate.py').write_text('def alpha(values):\n' + repeated + '\ndef beta(values):\n' + repeated)

        def call(args, expected=0):
            code = execute([str(x) for x in args], root, time.monotonic() + 60, root / 'last.log')
            if code != expected:
                raise AssertionError(f'{Path(str(args[0])).name}: expected {expected}, got {code}: ' + (root / 'last.log').read_text()[-2000:])

        call([binary / 'crapper', '--no-coverage', 'subject.py'])
        crap = read_edn(root / '.metrics/crap.edn')
        assert crap['entries'], 'Parser did not analyze the fixture'
        assert assess(crap, {'candidates': []})['state'] == 'evidence-gap'
        call([binary / 'dryer', '--threshold', '0.8', 'duplicate.py'])
        assert read_edn(root / '.metrics/dry.edn')['candidates'], 'Known duplicate was missed'
        (root / 'target/coverage/python').mkdir(parents=True)
        test_command = shlex.join([str(python), '-m', 'unittest', 'discover'])
        coverage_command = shlex.join([str(python), '-m', 'coverage', 'run', '--source=subject', '-m', 'unittest', 'discover']) + ' && ' + shlex.join([str(python), '-m', 'coverage', 'lcov', '-o', 'target/coverage/python/lcov.info'])
        call([python, Path(__file__).with_name('quality_check.py'), '--repo', root,
              '--bin', binary, '--profile', 'standard', '--test-command', test_command,
              '--coverage-command', coverage_command, '--coverage-report',
              'target/coverage/python/lcov.info', 'subject.py'])
        call([binary / 'mutator', '--mutate-all', '--no-coverage', '--max-workers', '2',
              '--test-command', shlex.join([str(python), '-m', 'unittest', 'discover']), 'subject.py'], 3)
        mutations = [read_edn(p) for p in (root / '.metrics/mutate').glob('*.edn')]
        assert any(f.get('survived', 0) for m in mutations for f in m['forms']), 'Weak test did not yield a survivor'
        (root / 'test_subject.py').write_text('import unittest\nclass Tests(unittest.TestCase):\n    def test_failure(self):\n        self.fail("intentional baseline failure")\n')
        call([binary / 'mutator', '--no-coverage', '--test-command',
              shlex.join([str(python), '-m', 'unittest', 'discover']), 'subject.py'], 2)
        assert assess({'entries': []}, {'candidates': []}, [])['state'] == 'evidence-gap'
        # Optional research pack: real PDF rendering and a headless plot.
        try:
            import pypdf
        except ImportError:
            pass
        else:
            import pypdfium2
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import numpy as np
            writer = pypdf.PdfWriter()
            writer.add_blank_page(width=200, height=200)
            writer.write(root / 'fixture.pdf')
            document = pypdfium2.PdfDocument(root / 'fixture.pdf')
            page = document[0]
            rendered = page.render().to_pil()
            assert rendered.size == (200, 200)
            page.close(); document.close()
            plt.plot(np.array([0, 1]), np.array([0, 1]))
            plt.savefig(root / 'plot.png'); plt.close()
            assert (root / 'plot.png').stat().st_size > 0
    print('Real-tool fixtures passed: parsed code, missing coverage, duplicates, surviving mutant, failed baseline, zero analysis, and optional PDF/plot capability.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bin', type=Path, required=True)
    smoke(parser.parse_args().bin)
