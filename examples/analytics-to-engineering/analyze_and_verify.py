"""Execute parsers against authored examples and report checks as JSON.

The input examples and expected answers are synthetic teaching material. The
reported parser outcomes are measured by executing the local implementations.
No package dependencies, network access, file writes, or timing measurements.
"""

import csv
import hashlib
import io
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from processor import baseline, candidate


ROOT = Path(__file__).resolve().parent
FIELDS = {
    "case_id", "notation", "quantity", "expected_outcome",
    "expected_numerator", "expected_denominator",
}
NOTATIONS = {"integer", "decimal", "fraction", "mixed", "invalid"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_fixture(path):
    raw = Path(path).read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
    require(reader.fieldnames is not None and len(reader.fieldnames) == len(FIELDS)
            and set(reader.fieldnames) == FIELDS, "unexpected fixture columns")
    rows = list(reader)
    require(bool(rows), "empty fixture")
    identifiers = set()
    for row in rows:
        require(set(row) == FIELDS and all(value is not None for value in row.values()),
                "malformed fixture row")
        require(bool(row["case_id"]) and row["case_id"] not in identifiers,
                "missing or duplicate case ID")
        identifiers.add(row["case_id"])
        require(row["notation"] in NOTATIONS, "unknown notation label")
        require(row["expected_outcome"] in {"value", "reject"}, "unknown expected outcome")
        if row["expected_outcome"] == "value":
            numerator = int(row["expected_numerator"])
            denominator = int(row["expected_denominator"])
            require(numerator >= 0 and denominator > 0, "invalid expected quantity")
            require(row["notation"] != "invalid", "inconsistent notation and expected outcome")
        else:
            require(not row["expected_numerator"] and not row["expected_denominator"],
                    "rejected cases cannot specify a value")
            require(row["notation"] == "invalid", "inconsistent notation and expected outcome")
    return rows, hashlib.sha256(raw).hexdigest()


def observe(parser, text):
    try:
        value = parser(text)
        return {"outcome": "value", "numerator": value.numerator, "denominator": value.denominator}
    except ValueError:
        return {"outcome": "reject"}


def expected(row):
    if row["expected_outcome"] == "reject":
        return {"outcome": "reject"}
    value = Fraction(int(row["expected_numerator"]), int(row["expected_denominator"]))
    return {"outcome": "value", "numerator": value.numerator, "denominator": value.denominator}


def analyze(path=ROOT / "observations.csv"):
    rows, source_hash = read_fixture(path)
    by_notation = defaultdict(lambda: {"cases": 0, "baseline_correct": 0, "candidate_correct": 0})
    observations = []
    for row in rows:
        wanted = expected(row)
        before = observe(baseline, row["quantity"])
        after = observe(candidate, row["quantity"])
        group = by_notation[row["notation"]]
        group["cases"] += 1
        group["baseline_correct"] += before == wanted
        group["candidate_correct"] += after == wanted
        observations.append({
            "case_id": row["case_id"], "notation": row["notation"], "quantity": row["quantity"],
            "expected": wanted, "baseline": before, "candidate": after,
            "baseline_correct": before == wanted, "candidate_correct": after == wanted,
        })
    failures = [row for row in observations if not row["baseline_correct"]]
    candidate_failures = [row for row in observations if not row["candidate_correct"]]
    return {
        "input_origin": "authored fictional cookbook cases and expected answers; no user or service data",
        "observation_origin": "parser outputs obtained by executing the local Python implementations",
        "fixture_sha256": source_hash,
        "processor_sha256": hashlib.sha256((ROOT / "processor.py").read_bytes()).hexdigest(),
        "cases_checked": len(rows), "by_notation": dict(sorted(by_notation.items())),
        "baseline_failure_count": len(failures),
        "candidate_failure_count": len(candidate_failures),
        "baseline_failures": failures, "candidate_failures": candidate_failures,
        "observations": observations,
        "claim_limit": "correctness on the authored cases only; no estimate of real-world format prevalence or product readiness",
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2, sort_keys=True, allow_nan=False))
