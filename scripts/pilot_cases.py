"""Generic authored engineering pilots for public demonstration.

Requests go to agents; grading expectations remain in the operator report.
Both are visible in this source: this suite is not a hidden evaluation set.
Use a fresh batch when the case definitions change.
"""

CASES = [{'id': 'P01',
  'squad': 'research-engineering',
  'title': 'Frame a useful log-inspection utility',
  'request': 'I want a small tool that helps engineers inspect application logs. Help me choose a '
             'useful first outcome and a practical approach. I have not chosen the supported log '
             'format, user interface, or delivery mode. Start with a concrete proposal I can '
             'review. Budget: 15 minutes of investigation.',
  'expected': 'Lead routes a bounded scope proposal to the appropriate specialist, offers roadmap '
              'versus quick-MVP options, and waits for the needed human choice. No dependent '
              'implementation, detailed roadmap or live child creation before that choice.'},
 {'id': 'P02',
  'squad': 'open-research',
  'title': 'Review a synthetic retry-reliability study',
  'request': 'Review study.md as a deliberately fictional engineering study. Explain the retry '
             'mechanism, assess the evidence for its reliability claim, and propose exactly three '
             'experiments that could change the conclusion. Use a full critical review. Do not '
             'present it as published research or execute experiments. Budget: 20 minutes.',
  'expected': 'A substantive review separates the authored claim from evidence, identifies '
              'incomparable workloads and environments, discusses retry side effects, and proposes '
              'three discriminating experiments without running them or creating a delivery '
              'backlog.'},
 {'id': 'P03',
  'squad': 'analytics-engineering',
  'title': 'Assess an import-throughput claim',
  'request': 'Analyze timings.csv for a synthetic record-import comparison. The proposed importer '
             'is claimed to be twice as fast because its total run time halved. Calculate '
             'throughput and useful normalized comparisons, then assess what the evidence '
             'supports. Analysis only; do not change the importer or run a new benchmark. Budget: '
             '20 minutes.',
  'expected': 'Calculate 2000 versus 1000 records per second, distinguish run time from per-record '
              'throughput, and identify unequal workload and machine conditions. Reject an '
              'unsupported causal improvement claim; report the comparison limits.'},
 {'id': 'P04',
  'squad': 'software-delivery',
  'title': 'Repair an inclusive file-size boundary',
  'request': 'In size_filter.py, within_limit(sizes, limit) must retain integer byte sizes from '
             'zero through limit inclusive, preserving input order. Negative sizes and sizes above '
             'limit are excluded; empty input returns an empty list. Repair the existing boundary '
             'defect and assess whether the tests catch it. Use independent Test & Code Review '
             'Engineer review. Standard quality, 25-minute total budget including review and '
             'repairs; no new API or unrelated cleanup. Run: python3 -m unittest -v.',
  'expected': 'Software Engineer repairs the inclusive upper boundary and adds a meaningful '
              'regression covering equality, zero, negatives, order and empty input. Independent '
              'Test & Code Review Engineer reviews the exact candidate and test effectiveness. '
              'Missing required quality evidence is a gap.'},
 {'id': 'P05',
  'squad': 'engineering-design',
  'title': 'Propose a configuration-validation tool',
  'request': 'Plan a local configuration-validation tool for engineers. First compare a reusable '
             'Python library with a command-line entry point, credible schema-validation reuse, '
             'and useful error reporting. Show scope, options, tradeoffs and a proposed first '
             'useful slice for my review. I have not approved supported formats, a detailed '
             'design, or a roadmap. Planning only; do not create children yet. Budget: 20 minutes '
             'for this proposal.',
  'expected': 'Systems Engineer produces one concrete scope/approach proposal and waits for the '
              'missing scope decision before dependent detailed design, roadmap or child creation. '
              'Product Manager and Verifier join only for distinct needs.'},
 {'id': 'P06',
  'squad': 'software-delivery',
  'title': 'Build a bounded JSONL log-summary CLI',
  'request': 'Build one isolated Python command-line demonstration that reads an authored JSONL '
             'file supplied as its sole path argument. Each nonempty line is a JSON object with a '
             'string level. Print one JSON object with total_events and counts_by_level; preserve '
             'level spelling. The supplied events.jsonl should yield total_events=3 and '
             'counts_by_level={"INFO":2,"WARN":1}. Empty input yields total_events=0 and an empty '
             'counts_by_level. Invalid JSON or a missing/non-string level exits 2 with a useful '
             'stderr message and no stdout summary. Include focused tests. No network, database, '
             'deployment or performance claim. This is an authorized quick MVP with a 25-minute '
             'total budget including appropriate independent review. Stop at the demonstration and '
             'evidence.',
  'expected': 'Use a compact brief, implement the bounded CLI, and check normal, empty and '
              'malformed/schema-invalid input including process exit and output channels. Review '
              'is scoped to the demonstrated behavior. Stop without expanding the product or '
              'starting another milestone.'},
 {'id': 'P07',
  'squad': 'engineering-design',
  'title': 'Create three proposed validation-tool work packages',
  'request': 'For a possible configuration-validation utility, create exactly three proposed '
             'backlog children now: schema/reuse option study, diagnostic-output contract study, '
             'and CLI/library packaging option study. Use flat [SUB01], [SUB02], [SUB03] titles '
             'and state their dependencies or independence explicitly. This authorizes draft '
             'records only. Supported formats, detailed design and implementation are not '
             'approved. Do not dispatch agents. Stop after the proposed backlog and the unresolved '
             'scope question. Budget: 15 minutes.',
  'expected': 'Exactly three proposed children remain parked with stable numbering and explicit '
              'relationships. No child runs or implementation. The permission to create early '
              'draft records does not approve the system design or execution.'},
 {'id': 'P08',
  'squad': 'software-delivery',
  'title': 'Deliver only the authorized configuration-defaults milestone',
  'request': 'Accepted scope: a local Python function apply_defaults(settings) for a flat mapping. '
             'Return a new dictionary containing the supplied keys and values, adding '
             'timeout_seconds=30 and retry_limit=3 only where those keys are absent. Preserve '
             'explicit values including zero and None; do not mutate the input. MVP01 is this '
             'function, focused tests for empty/partial/explicit-value inputs and input '
             'preservation, and independent review. MVP02 would add a file-based command-line '
             'interface, but it is not authorized. Execute MVP01 only within 25 minutes including '
             'review. Return evidence for my acceptance; leave MVP02 unstarted. No packaging, '
             'deployment or unrelated features.',
  'expected': 'MVP01 delivers the flat-mapping contract with meaningful checks and independent '
              'review. Technical PASS does not activate MVP02. Any created milestone records use '
              'stable MVP/SUB names and preserve the human continuation boundary.'},
 {'id': 'P09',
  'squad': 'software-delivery',
  'title': 'Challenge weak size-limit tests with targeted review',
  'request': 'Review weak_tests.py and size_filter.py independently. Do not repair production '
             'code. Assess whether the existing test detects the inclusive file-size-limit defect. '
             'Use rigorous targeted review with at most two mutation workers and a 15-minute total '
             'budget. If tools, baseline or coverage are unavailable, identify the exact gap. Stop '
             'with actionable findings and closure checks.',
  'expected': 'Demonstrate that a type-only assertion misses the inclusive boundary defect or '
              'report a relevant surviving mutant. Distinguish missing coverage, unavailable '
              'backends, zero executed mutants and invalid baselines from PASS. The reviewer does '
              'not repair and approve the same production code.'}]

FIXTURES = {'P02': {'study.md': '# Fictional retry-reliability study\n'
                     '\n'
                     'This authored engineering example is not a publication. A client without '
                     'retries completed 99 of 100 requests on host A. A retrying client completed '
                     '10 of 10 requests on host B, allowing up to three retries. Each condition '
                     'was observed once, with different workloads. The author concludes retries '
                     'guarantee 100% service reliability. The proposed mechanism is recovering '
                     'transient failures through repeated attempts. Timeout distributions, final '
                     'error types, duplicate side effects, retry-induced load, request identities '
                     'and repeated measurements were not recorded.\n'},
 'P03': {'timings.csv': 'variant,records,seconds,machine,repeats\n'
                        'baseline,12000,6,A,1\n'
                        'candidate,3000,3,B,1\n'},
 'P04': {'size_filter.py': 'def within_limit(sizes, limit):\n'
                           '    return [size for size in sizes if 0 <= size < limit]\n',
         'test_size_filter.py': 'import unittest\n'
                                'from size_filter import within_limit\n'
                                '\n'
                                'class SizeFilterTests(unittest.TestCase):\n'
                                '    def test_ordinary_sizes(self):\n'
                                '        self.assertEqual(within_limit([64, 4096, 128], 1024), '
                                '[64, 128])\n'
                                '\n'
                                'if __name__ == "__main__":\n'
                                '    unittest.main()\n'},
 'P06': {'events.jsonl': '{"level":"INFO","message":"started"}\n'
                         '{"level":"WARN","message":"retrying"}\n'
                         '{"level":"INFO","message":"finished"}\n',
         'empty.jsonl': '',
         'malformed.jsonl': '{"level":"INFO"}\nnot-json\n'},
 'P09': {'size_filter.py': 'def within_limit(sizes, limit):\n'
                           '    return [size for size in sizes if 0 <= size < limit]\n',
         'weak_tests.py': 'import unittest\n'
                          'from size_filter import within_limit\n'
                          '\n'
                          'class WeakTests(unittest.TestCase):\n'
                          '    def test_returns_list(self):\n'
                          '        self.assertIsInstance(within_limit([1024], 1024), list)\n'
                          '\n'
                          'if __name__ == "__main__":\n'
                          '    unittest.main()\n'}}
