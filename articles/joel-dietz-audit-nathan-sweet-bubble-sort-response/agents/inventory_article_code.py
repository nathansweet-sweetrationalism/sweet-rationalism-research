#!/usr/bin/env python3
"""Extract a PRIVATELY held WordPress article's 14 agent panels without exposing its text.
This is a structural inventory helper, not a proof, math-audit completion, or privacy guarantee.
Python 3.10+ standard library. Never uploads the manuscript.
"""
import argparse
import hashlib
import html
import json
import pathlib
import re
import sys

KINDS = ("doi", "tadpole", "xenobot", "score", "ports", "validator", "authorship")
PLACES = ("quick", "analysis")
EXPECTED = {f"rcf-computational-{k}-{p}" for k in KINDS for p in PLACES}

def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def inventory(content, modified=None):
    panels = []
    failures = []
    pattern = re.compile(r'<details\b[^>]*\bid="(rcf-computational-[^"]+)"[^>]*>[\s\S]*?</details>', re.I)
    for match in pattern.finditer(content):
        block = match.group(0)
        textareas = re.findall(r"<textarea\b[^>]*>([\s\S]*?)</textarea>", block, re.I)
        if len(textareas) != 1:
            failures.append("Expected exactly one textarea for " + match.group(1))
            continue
        # HTML textarea contents are entity-decoded by the browser.
        prompt = html.unescape(textareas[0])
        urls = re.findall(r"https://[^\s<>\"']+", prompt)
        primary = [u for u in urls if "raw.githubusercontent.com/" in u and ".zip" in u]
        backup = [u for u in urls if "sweetrationalism.com/wp-content/uploads/" in u and ".zip" in u]
        panels.append({
            "panel_id": match.group(1),
            "prompt_sha256": sha256(prompt),
            "prompt_characters": len(prompt),
            "primary_zip_url_count": len(set(primary)),
            "backup_zip_url_count": len(set(backup)),
            "live_command_count": len(re.findall(r"python\s+audit\.py\s+--live", prompt)),
            "fixture_command_count": len(re.findall(r"python\s+audit\.py\s+--selftest", prompt)),
            "legacy_verify_commands": len(re.findall(r"(?:python|py)\s+verify\.py", prompt)),
        })
    present = [x["panel_id"] for x in panels]
    if len(present) != len(set(present)):
        failures.append("Duplicate panel IDs")
    absent = EXPECTED - set(present)
    extra = set(present) - EXPECTED
    if absent:
        failures.append("Missing panel IDs: " + ",".join(sorted(absent)))
    if extra:
        failures.append("Unexpected panel IDs: " + ",".join(sorted(extra)))
    for x in panels:
        if x["primary_zip_url_count"] < 1 or x["backup_zip_url_count"] < 1:
            failures.append(x["panel_id"] + " lacks one ZIP mirror")
        if x["live_command_count"] < 1 or x["fixture_command_count"] < 1:
            failures.append(x["panel_id"] + " lacks live or fixture command")
        if x["legacy_verify_commands"]:
            failures.append(x["panel_id"] + " uses obsolete verify.py")
    by_kind = {}
    for kind in KINDS:
        subset = [x for x in panels if f"rcf-computational-{kind}-" in x["panel_id"]]
        if len(subset) == 2:
            by_kind[kind] = {
                "exact_prompt_match": subset[0]["prompt_sha256"] == subset[1]["prompt_sha256"],
                "hashes": [x["prompt_sha256"] for x in subset],
            }
    # Heuristic only: percentages, angles and mathematical notation may appear
    # in quoted strings, prompts and unrelated prose; full human ledger still required.
    candidate_regex = re.compile(r"(?:\b\d+(?:\.\d+)?\s*%|\b\d+\s*°|\bp\s*[=<>]\s*\d+(?:\.\d+)?|\\\[|\\\()")
    candidate_offsets = [m.start() for m in candidate_regex.finditer(content)]
    return {
        "schema": "article-agent-panel-inventory/v1",
        "article_sha256": sha256(content),
        "wordpress_modified": modified,
        "panel_count": len(panels),
        "expected_panel_count": len(EXPECTED),
        "panels": panels,
        "pair_comparison": by_kind,
        "heuristic_math_candidate_count": len(candidate_offsets),
        "heuristic_math_candidate_offsets": candidate_offsets,
        "coverage_warning": "A regex scan cannot classify or prove every mathematical statement; manually adjudicate all sections.",
        "structural_failures": failures,
    }

def main():
    p = argparse.ArgumentParser(description="PRIVATE local article read; public-safe structural report")
    p.add_argument("article", type=pathlib.Path, help="Authorized raw HTML or JSON with content.raw")
    p.add_argument("--out", type=pathlib.Path, required=True, help="Sanitized JSON report")
    args = p.parse_args()
    raw = args.article.read_text(encoding="utf-8-sig")
    modified = None
    if raw.lstrip().startswith("{"):
        try:
            data = json.loads(raw)
            raw = data["content"]["raw"] if isinstance(data.get("content"), dict) else data["content"]
            modified = data.get("modified")
        except (KeyError, TypeError, ValueError) as exc:
            p.error("Invalid JSON WordPress content: " + str(exc))
    report = inventory(raw, modified)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"panel_count": report["panel_count"],
                      "heuristic_math_candidates": report["heuristic_math_candidate_count"],
                      "structural_failure_count": len(report["structural_failures"]),
                      "report_path": str(args.out)}, indent=2))
    return 1 if report["structural_failures"] else 0

if __name__ == "__main__":
    sys.exit(main())
