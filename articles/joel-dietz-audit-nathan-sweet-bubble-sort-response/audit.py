#!/usr/bin/env python3
"""Bounded source-code verification. Never runs upstream code. Python 3.10+ stdlib."""
import argparse
import ast
import hashlib
import json
import math
import re
import statistics
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

BASE = Path(__file__).resolve().parent

def http_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SweetRationalism-source-check/1.0"})
    with urllib.request.urlopen(req, timeout=35) as response:
        if response.status != 200:
            raise OSError(f"HTTP {response.status}: {url}")
        return response.read()

def must(condition, explanation):
    if not condition:
        raise AssertionError(explanation)

def verify(test_id, sources, spec, live):
    observations = []
    limits = ["This check establishes only the stated source/code observation, not an ontology.",
              "Fixture mode is a parser smoke test, NOT an independent check of online sources."]
    note = lambda name, value: observations.append({"name": name, "value": value})
    if test_id == "validator":
        source = sources["validator"]
        statuses = len(re.findall(r'"status"\s*:\s*"VERIFIED"', source))
        errors = len(re.findall(r'"relative_error_pct"\s*:', source))
        must(statuses >= 1 and errors >= 1, "Benchmark status/error records are not present")
        note("literal_verified_assignments", statuses)
        note("relative_error_fields", errors)
        note("synthetic_900_pct_negative_control", "VERIFIED literal remains unchanged")
        limits.append("900% is a fabricated negative-control input, not an observed replication discrepancy.")
    elif test_id == "xenobot":
        claim, code = sources["claim"], sources["model"]
        must("105°" in claim, "105 degree source claim missing")
        must("theta_deg - 65.0" in code and "eta_sweep" in code and "spill_penalty" in code,
             "Coded sweep expression not found")
        def curve(theta):
            eta = 6.0 + 12.5 * math.exp(-(((theta - 65.0) / 26.0) ** 2))
            spill = math.exp(-(((theta - 85.0) / 38.0) ** 2)) if theta > 85.0 else 1.0
            return eta * spill * 12.0
        grid = [i * 5.0 for i in range(25)]
        best = max(grid, key=curve)
        note("narrative_angle_degrees", 105.0)
        note("programmed_grid_maximum_degrees", best)
        note("computed_sweep_65_vs_105", {"at_65": round(curve(65), 4),
                                           "at_105": round(curve(105), 4)})
        limits.append("Different angle conventions or another solver could reconcile the numerical contrast.")
    elif test_id == "tadpole":
        source = sources["model"]
        for term in ['params["target_nf65_landmarks"]', "def closed_loop_attractor_rhs(",
                     "diff = X - X_star", "homing = -K[:, None] * diff"]:
            must(term in source, "Expected source mechanism missing: " + term)
        def example(target):
            x = 4.0
            for _ in range(400):
                x += 0.025 * (target - x)
            return round(x, 5)
        note("model_target_input", 'params["target_nf65_landmarks"]')
        note("illustrative_target_intervention", {"target_minus_2": example(-2.0),
                                                    "target_plus_9": example(9.0)})
        limits.append("The illustrative ODE is not a tadpole experiment or a proof about target origin.")
    elif test_id == "score":
        source = sources["generator"]
        vals = [float(x) for x in re.findall(r'"(\d+(?:\.\d+)?)%"\)', source)]
        must(len(vals) == 7, f"Found {len(vals)} scores; seven expected in pinned generator")
        must('MEAN = "77.6%"' in source, "Expected display constant absent")
        means = [sum(vals[:i] + vals[i + 1:]) / 6 for i in range(7)]
        note("seven_displayed_scores", vals)
        note("arithmetic_mean_percent", round(statistics.mean(vals), 4))
        note("leave_one_out_mean_range_percent", [round(min(means), 4), round(max(means), 4)])
        note("display_value_in_source", "77.6%")
        limits.append("An average of scored judgments is not a calibrated probability of P.")
    elif test_id == "ports":
        source = sources["verifier"]
        checks = [line.strip() for line in source.splitlines()
                  if line.strip().startswith("assert ") and any(n in line for n in
                  ("cpp_data", "js_data", "py_kymo"))]
        must(any('["benchmarks"]' in x and "js_data" in x for x in checks),
             "Expected C++/JS benchmark assertion missing")
        must(any('["final_values"]' in x for x in checks),
             "Expected final-array comparisons missing")
        note("matching_array_and_dictionary_assertions", checks)
        note("full_intermediate_frames_proved_by_these_assertions", False)
        limits.append("Other repository tests might cover additional outputs; search before declaring absence.")
    elif test_id == "authorship":
        source = sources["renderer"]
        match = re.search(r'ai_matrix\s*=\s*np\.array\(\[([\s\S]*?)\],\s*dtype=float\)', source)
        must(match is not None, "AI author-estimate matrix not found")
        rows = ast.literal_eval("[" + match.group(1) + "]")
        vals = [float(row[1]) for row in rows]
        must(len(rows) >= 2 and all(len(row) == 5 for row in rows), "Unexpected matrix shape")
        before = 100 - statistics.mean(vals)
        after = 100 - statistics.mean([vals[0]] + vals)
        note("estimated_human_prose_mean_percent", round(before, 4))
        note("after_hypothetical_intro_row_split_percent", round(after, 4))
        note("row_count_before_after", [len(rows), len(rows) + 1])
        limits.append("Section-boundary sensitivity does not reveal real authorship contribution shares.")
    elif test_id == "doi":
        source = sources["bibliography"]
        cases = spec["doi_cases"]
        found = []
        for case in cases:
            row = next((s for s in source.splitlines()
                        if case["title_fragment"].lower() in s.lower()), None)
            must(row is not None, "Source bibliography entry not found: " + case["title_fragment"])
            got = re.search(r'doi:(10\.\d+/[^\s\])]+)', row, re.I)
            must(got is not None, "Source bibliography DOI missing: " + case["title_fragment"])
            cited = got.group(1).rstrip(".,")
            actual = case["primary_doi"]
            if live:
                pmid = case["pmid"]
                xml = ElementTree.fromstring(http_bytes(
                    f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"))
                observed = [x.text for x in xml.findall('.//ArticleId[@IdType="doi"]') if x.text]
                must(bool(observed), "PubMed article has no DOI: " + pmid)
                actual = observed[0]
            found.append({"source_doi": cited, "primary_doi": actual,
                          "matches": cited.lower() == actual.lower(),
                          "article_fragment": case["title_fragment"],
                          "primary_source_checked": bool(live)})
        note("bibliographic_identity_comparison", found)
        limits.append("Incorrect bibliographic metadata is not a refutation of the experiments it cites.")
    else:
        raise ValueError("Unknown test ID: " + test_id)
    return observations, limits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="Fetch pinned primary sources, requires network")
    ap.add_argument("--selftest", action="store_true", help="Run fixture-only parser and arithmetic checks")
    ap.add_argument("--config", default="test.json")
    args = ap.parse_args()
    if args.live == args.selftest:
        ap.error("Choose exactly one of --live or --selftest")
    result = {"status": "NOT_RUN", "time_utc": datetime.now(timezone.utc).isoformat(),
              "mode": "PINNED_REMOTE_SOURCES" if args.live else "LOCAL_FIXTURE_SELFTEST",
              "observations": [], "source_hashes": [], "limitations": []}
    try:
        spec = json.loads((BASE / args.config).read_text(encoding="utf-8"))
        result["test_id"] = spec["id"]
        sources = {}
        for name, item in spec["sources"].items():
            if args.live:
                raw = http_bytes(item["url"])
            else:
                raw = item["fixture"].encode("utf-8")
            sources[name] = raw.decode("utf-8")
            result["source_hashes"].append({"name": name,
              "url": item["url"] if args.live else "FIXTURE_ONLY",
              "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        result["observations"], result["limitations"] = verify(spec["id"], sources, spec, args.live)
        result["status"] = "OBSERVATION_REPRODUCED" if args.live else "SELFTEST_ONLY"
        exit_code = 0
    except (OSError, TimeoutError, urllib.error.URLError) as e:
        result["status"] = "UNRESOLVED"
        result["error"] = "Source retrieval failed; no offline fallback was substituted: " + str(e)
        exit_code = 2
    except Exception as e:
        result["status"] = "SOURCE_CHANGED_OR_CHECK_FAILED" if args.live else "SELFTEST_FAILED"
        result["error"] = type(e).__name__ + ": " + str(e)
        exit_code = 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
