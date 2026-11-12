#!/usr/bin/env python3
"""Executable regression tests for the synthetic agent submission validator.

No WordPress source or privately authored manuscript text is used.
"""
import copy
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "agents" / "validate_submission.py"
TEST_DIR = ROOT / "audits" / "agents" / "synthetic_validator_000001"
KIND = ["doi", "tadpole", "xenobot", "score", "ports", "validator", "authorship"]


def fixture():
    gates = json.loads((ROOT / "release_status.json").read_text(encoding="utf-8"))["gates"]
    panel = []
    for kind in KIND:
        for place in ("quick", "analysis"):
            panel.append({
                "panel_id": f"rcf-computational-{kind}-{place}",
                "status": "NOT_RUN",
                "source_prompt_sha256": "0" * 64,
                "primary_zip_url": "https://example.org/fake-primary.zip",
                "backup_zip_url": "https://example.org/fake-backup.zip",
                "cli_command": "python audit.py --live",
                "evidence": [],
                "limitations": ["This is synthetic test data, not an audit."],
            })
    return {
        "schema": "sweet-rationalism-agent-audit/v1",
        "run_id": TEST_DIR.name,
        "agent": {"tool": "Local regression test", "model": "none"},
        "snapshot": {
            "wordpress_post_id": 218725796,
            "wordpress_status": "draft",
            "wordpress_modified": "2026-11-11T00:00:00",
            "wordpress_content_sha256": "0" * 64,
            "github_base_commit": "0" * 40,
            "upstream_commit": "1" * 40,
        },
        "assessments": [{
            "id": "fixture-only", "release_gate": "formal", "scope": "syntax",
            "status": "NOT_RUN", "observations": [], "limitations": [],
            "loss_conditions": [],
        }],
        "gate_recommendations": [{
            "id": item["id"], "suggested_state": "open",
            "reason": "Not executed", "assessment_ids": [],
        } for item in gates],
        "open_items": [],
        "privacy": {"reviewed_public_safe": True,
                    "unpublished_manuscript_excluded": True},
        "prompt_checks": panel,
        "math_inventory": [{
            "claim_id": "synthetic-arithmetic", "locations": ["fixture"],
            "type": "exact_arithmetic", "scope": "synthetic example",
            "tool": "Python standard library", "tool_version": sys.version.split()[0],
            "method_sources": [], "run_result": {}, "independent_check": {},
            "status": "NOT_RUN", "limitations": ["Synthetic fixture"],
            "loss_conditions": ["Any validation inconsistency"],
        }],
        "coverage": {
            "panel_ids_enumerated": 14, "unique_packages_enumerated": 7,
            "math_claims_count": 1, "article_commands_enumerated": [],
            "script_inventory": [], "public_safety_review": True,
        },
    }


def run(fixture_data):
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    (TEST_DIR / "result.json").write_text(json.dumps(fixture_data), encoding="utf-8")
    (TEST_DIR / "report.md").write_text("SYNTHETIC FIXTURE ONLY\n", encoding="utf-8")
    (TEST_DIR / "commands.txt").write_text("No scientific test ran.\n", encoding="utf-8")
    sums = []
    for path in sorted(TEST_DIR.iterdir()):
        if path.name != "SHA256SUMS.txt":
            sums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (TEST_DIR / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="utf-8")
    return subprocess.run([sys.executable, str(VALIDATOR), str(TEST_DIR)],
                          text=True, capture_output=True, check=False)


def main():
    base = fixture()
    try:
        valid = run(base)
        assert valid.returncode == 0, valid.stdout + valid.stderr
        dup = copy.deepcopy(base)
        dup["prompt_checks"][-1]["panel_id"] = dup["prompt_checks"][0]["panel_id"]
        assert run(dup).returncode != 0, "Duplicate panel must fail"
        nomath = copy.deepcopy(base)
        nomath["math_inventory"] = []
        assert run(nomath).returncode != 0, "Missing math inventory must fail"
        count = copy.deepcopy(base)
        count["coverage"]["math_claims_count"] = 2
        assert run(count).returncode != 0, "Incorrect claim count must fail"
        absent = copy.deepcopy(base)
        absent["gate_recommendations"].pop()
        assert run(absent).returncode != 0, "Missing release-gate accounting must fail"
        print("PASS: valid synthetic audit accepted, 4 invalid variants rejected")
    finally:
        shutil.rmtree(TEST_DIR, ignore_errors=True)


if __name__ == "__main__":
    main()
