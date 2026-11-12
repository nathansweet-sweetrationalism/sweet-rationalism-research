#!/usr/bin/env python3
"""Validate a public-safe, independently reproducible agent audit submission.

Checks structure, provenance, ledger coverage and submitted file integrity.
Does NOT certify the evidence, draft privacy, scientific claims or author approval.
Python 3.10+ standard library only.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = {"result.json", "report.md", "commands.txt", "SHA256SUMS.txt"}
VALID = {"CONFIRMED_WITHIN_SCOPE", "DISCONFIRMED_WITHIN_SCOPE", "PARTIAL", "UNRESOLVED", "NOT_RUN"}
VALID_GATE = {"done", "partial", "open"}

def fail(message):
    raise ValueError(message)

def validate(folder):
    folder = folder.resolve()
    expected_root = ROOT / "audits" / "agents"
    if not folder.is_relative_to(expected_root.resolve()):
        fail("Submission must be inside this article's audits/agents/ directory")
    missing_files = [x for x in REQUIRED if not (folder / x).is_file()]
    if missing_files:
        fail("Missing required files: " + ", ".join(sorted(missing_files)))
    result = json.loads((folder / "result.json").read_text(encoding="utf-8"))
    if result.get("schema") != "sweet-rationalism-agent-audit/v1":
        fail("Unrecognized result schema")
    if result.get("run_id") != folder.name or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{5,100}", folder.name):
        fail("Run id must equal the unique directory name")
    agent = result.get("agent", {})
    if not agent.get("tool") or not agent.get("model"):
        fail("Name the agent tool and exact model, or disclose that the model is unknown")
    snapshot = result.get("snapshot", {})
    if snapshot.get("wordpress_post_id") != 218725796 or snapshot.get("wordpress_status") != "draft":
        fail("Confirm post 218725796 was a draft at snapshot time")
    if not snapshot.get("wordpress_modified"):
        fail("Missing WordPress modification timestamp")
    if not re.fullmatch(r"[a-f0-9]{64}", str(snapshot.get("wordpress_content_sha256", ""))):
        fail("Missing SHA-256 of exact WordPress draft content")
    for key in ("github_base_commit", "upstream_commit"):
        if not re.fullmatch(r"[a-f0-9]{40}", str(snapshot.get(key, ""))):
            fail("Missing full commit hash for " + key)
    priv = result.get("privacy", {})
    if priv.get("reviewed_public_safe") is not True or priv.get("unpublished_manuscript_excluded") is not True:
        fail("Explicit privacy review/attestation required")
    assessments = result.get("assessments", [])
    if not isinstance(assessments, list) or not assessments:
        fail("No test or argument assessments supplied")
    assessment_ids = set()
    for item in assessments:
        ident = item.get("id")
        if not ident or ident in assessment_ids:
            fail("Assessment IDs must be nonempty and unique")
        assessment_ids.add(ident)
        if item.get("status") not in VALID:
            fail("Invalid status for assessment " + ident)
        if not item.get("release_gate") or not item.get("scope"):
            fail("Every assessment requires a gate ID and precise scope")
        if not isinstance(item.get("observations"), list) or not isinstance(item.get("limitations"), list) or not isinstance(item.get("loss_conditions"), list):
            fail("Missing observation/limitation/loss-condition arrays for " + ident)
        if item["status"] in ("CONFIRMED_WITHIN_SCOPE", "DISCONFIRMED_WITHIN_SCOPE"):
            if not item.get("evidence") or not item.get("observations") or not item.get("loss_conditions"):
                fail("Decisive claim lacks source evidence, observation or defeater: " + ident)
    # Article has 14 separately positioned prompts, seven code-test packages.
    kinds = ("doi", "tadpole", "xenobot", "score", "ports", "validator", "authorship")
    expected_panels = {f"rcf-computational-{kind}-{place}" for kind in kinds
                       for place in ("quick", "analysis")}
    panel_results = result.get("prompt_checks", [])
    if not isinstance(panel_results, list) or len(panel_results) != 14:
        fail("Each of the fourteen prompt-panel occurrences requires a result")
    submitted_ids = [item.get("panel_id") for item in panel_results]
    if len(set(submitted_ids)) != 14 or set(submitted_ids) != expected_panels:
        fail("Prompt-panel IDs missing, duplicated or inconsistent with the actual article")
    for item in panel_results:
        panel_id = item["panel_id"]
        if item.get("status") not in VALID:
            fail("Invalid prompt status: " + panel_id)
        digest = item.get("source_prompt_sha256", "")
        if not re.fullmatch(r"[a-f0-9]{64}", digest):
            fail("Hash the exact copyable prompt bytes: " + panel_id)
        if not all(str(item.get(k, "")).startswith("https://") for k in
                   ("primary_zip_url", "backup_zip_url")):
            fail("Both independently downloadable package URLs required: " + panel_id)
        if not item.get("cli_command") or not isinstance(item.get("evidence"), list):
            fail("Every prompt needs a command and evidence array: " + panel_id)
        if item["status"] == "CONFIRMED_WITHIN_SCOPE" and not item["evidence"]:
            fail("A passed prompt requires source/check evidence: " + panel_id)
        if not isinstance(item.get("limitations"), list):
            fail("List limitations for " + panel_id)
    math_items = result.get("math_inventory", [])
    if not isinstance(math_items, list) or not math_items:
        fail("Mathematical inventory must include every quantitative/formal claim")
    seen_math = set()
    resolved_math = {"PROVED_DERIVATION", "KERNEL_CHECKED",
                     "SMT_UNSAT_WITH_ENCODING", "BOUNDED_TESTS_PASSED", "COUNTEREXAMPLE"}
    for item in math_items:
        cid = item.get("claim_id")
        if not cid or cid in seen_math:
            fail("Mathematical claim IDs must be nonempty and unique")
        seen_math.add(cid)
        for key in ("locations", "type", "scope", "tool", "tool_version",
                    "method_sources", "run_result", "independent_check",
                    "status", "limitations", "loss_conditions"):
            if key not in item:
                fail("Missing mathematical proof duty " + key + " for " + cid)
        if not isinstance(item["locations"], list) or not item["locations"]:
            fail("Mathematical claim needs one or more article locations: " + cid)
        if item["status"] in resolved_math and (
            not item["method_sources"] or not item["run_result"] or
            not item["independent_check"]):
            fail("No methods, executed result or independent check for " + cid)
    coverage = result.get("coverage", {})
    if coverage.get("panel_ids_enumerated") != 14 or coverage.get("unique_packages_enumerated") != 7:
        fail("Expected full fourteen-panel and seven-package audit coverage")
    if coverage.get("math_claims_count") != len(math_items):
        fail("Mathematical inventory count mismatch")
    if coverage.get("public_safety_review") is not True:
        fail("Record separate public-safety review")
    if not isinstance(coverage.get("article_commands_enumerated"), list) or not isinstance(
            coverage.get("script_inventory"), list):
        fail("Missing complete article commands/script inventories")

    gates = {x["id"] for x in json.loads((ROOT / "release_status.json").read_text(encoding="utf-8"))["gates"]}
    submitted = {}
    for x in result.get("gate_recommendations", []):
        gid = x.get("id")
        if gid in submitted or gid not in gates:
            fail("Duplicate or unknown release gate " + str(gid))
        submitted[gid] = x
        if x.get("suggested_state") not in VALID_GATE or not x.get("reason"):
            fail("Gate recommendation lacks state or explanation: " + gid)
        if not isinstance(x.get("assessment_ids"), list) or set(x["assessment_ids"]) - assessment_ids:
            fail("Gate cites missing assessment IDs: " + gid)
        if x["suggested_state"] == "done" and not x["assessment_ids"]:
            fail("A completed gate requires supporting assessment IDs: " + gid)
    if gates - set(submitted):
        fail("Account explicitly for every release gate; missing: " + ", ".join(sorted(gates-set(submitted))))
    if not isinstance(result.get("open_items"), list):
        fail("Missing open-items list")
    # Supply hashes for all submitted files, including reports and scripts.
    files = [p for p in folder.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt"]
    if any(p.stat().st_size > 8_000_000 for p in files):
        fail("Large files must be independently packaged/referenced, not embedded in the audit PR")
    recorded = {}
    for line in (folder / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        mat = re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
        if not mat:
            fail("SHA256SUMS uses standard double-space format")
        digest, relative = mat.groups()
        target = (folder / relative).resolve()
        if not target.is_relative_to(folder) or not target.is_file():
            fail("Hash target invalid or outside audit run: " + relative)
        if relative in recorded:
            fail("Duplicate checksum path: " + relative)
        recorded[relative] = digest
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            fail("SHA-256 mismatch: " + relative)
    if {p.relative_to(folder).as_posix() for p in files} != set(recorded):
        fail("Checksum inventory does not exactly cover the submitted files")
    # This is intentionally only a coarse leak detector; human inspection is mandatory.
    for p in files:
        if p.suffix.lower() not in {".json", ".jsonl", ".md", ".txt", ".py", ".sh", ".csv"}:
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"<!--\s*wp:(?:paragraph|heading|image)|github_pat_[A-Za-z0-9_]{15,}|ghp_[A-Za-z0-9]{15,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----", raw):
            fail("Possible private Gutenberg manuscript, GitHub token or key material: " + str(p))
    return {"result":"SUBMISSION_STRUCTURALLY_VALID_NOT_SCHOLARLY_CERTIFIED", "run_id":folder.name,
            "assessments":len(assessments),"gates_accounted_for":len(submitted),
            "hashed_files":len(files),
            "prompt_panels":len(panel_results),
            "math_claims":len(math_items),
            "warning":"The owner/coordinator must still audit source fidelity and possible private content."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="article's audits/agents/<run-id>")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(pathlib.Path(args.directory)), indent=2))
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"result":"INVALID_SUBMISSION", "reason":str(exc)}, indent=2), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
