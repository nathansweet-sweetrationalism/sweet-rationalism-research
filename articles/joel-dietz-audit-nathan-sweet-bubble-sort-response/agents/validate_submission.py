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
    if gates - submitted:
        fail("Account explicitly for every release gate; missing: " + ", ".join(sorted(gates-submitted)))
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
    if {str(p.relative_to(folder)) for p in files} != set(recorded):
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
