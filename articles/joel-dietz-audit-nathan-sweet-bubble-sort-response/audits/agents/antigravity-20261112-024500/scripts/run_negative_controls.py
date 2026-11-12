import os
import subprocess
import sys
import tempfile
import json
import copy

sys.stdout.reconfigure(encoding='utf-8')
dir_path = r"scratch/repos/sweet-rationalism-research/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response"
test_data_dir = os.path.join(dir_path, "test-data")

negative_results = {}

# Test 1: validator - negative control where an assertion fails if "status": "VERIFIED" is missing
with open(os.path.join(test_data_dir, "validator.json"), "r", encoding="utf-8") as f:
    cfg1 = json.load(f)
cfg1_bad = copy.deepcopy(cfg1)
cfg1_bad["sources"]["validator"]["fixture"] = "def check(): return 'FAILED'"
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg1_bad, tf)
    tf_path1 = tf.name
p1 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path1], cwd=dir_path, capture_output=True, text=True)
negative_results["validator"] = {
    "control_type": "corrupted_fixture_no_verified_status",
    "exit_code": p1.returncode,
    "status": json.loads(p1.stdout).get("status") if p1.stdout else "ERROR",
    "detected_failure": p1.returncode != 0
}
os.remove(tf_path1)

# Test 2: xenobot - negative control where narrative angle equals grid max (no discrepancy)
with open(os.path.join(test_data_dir, "xenobot.json"), "r", encoding="utf-8") as f:
    cfg2 = json.load(f)
cfg2_bad = copy.deepcopy(cfg2)
cfg2_bad["sources"]["claim"]["fixture"] = "Claim 7: The angle is 65° exactly."
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg2_bad, tf)
    tf_path2 = tf.name
p2 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path2], cwd=dir_path, capture_output=True, text=True)
negative_results["xenobot"] = {
    "control_type": "no_discrepancy_narrative_matches_code",
    "exit_code": p2.returncode,
    "status": json.loads(p2.stdout).get("status") if p2.stdout else "ERROR",
    "detected_failure": p2.returncode != 0
}
os.remove(tf_path2)

# Test 3: tadpole - negative control where target input is missing
with open(os.path.join(test_data_dir, "tadpole.json"), "r", encoding="utf-8") as f:
    cfg3 = json.load(f)
cfg3_bad = copy.deepcopy(cfg3)
cfg3_bad["sources"]["model"]["fixture"] = "def simulate(): pass # no target landmarks parameter"
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg3_bad, tf)
    tf_path3 = tf.name
p3 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path3], cwd=dir_path, capture_output=True, text=True)
negative_results["tadpole"] = {
    "control_type": "missing_target_input_parameter",
    "exit_code": p3.returncode,
    "status": json.loads(p3.stdout).get("status") if p3.stdout else "ERROR",
    "detected_failure": p3.returncode != 0
}
os.remove(tf_path3)

# Test 4: score - negative control where mean does not equal 77.6%
with open(os.path.join(test_data_dir, "score.json"), "r", encoding="utf-8") as f:
    cfg4 = json.load(f)
cfg4_bad = copy.deepcopy(cfg4)
cfg4_bad["sources"]["generator"]["fixture"] = "MEAN = '99.9%'\nscores = [10, 20]"
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg4_bad, tf)
    tf_path4 = tf.name
p4 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path4], cwd=dir_path, capture_output=True, text=True)
negative_results["score"] = {
    "control_type": "corrupted_score_mean",
    "exit_code": p4.returncode,
    "status": json.loads(p4.stdout).get("status") if p4.stdout else "ERROR",
    "detected_failure": p4.returncode != 0
}
os.remove(tf_path4)

# Test 5: ports - negative control where assertions don't match
with open(os.path.join(test_data_dir, "ports.json"), "r", encoding="utf-8") as f:
    cfg5 = json.load(f)
cfg5_bad = copy.deepcopy(cfg5)
cfg5_bad["sources"]["verifier"]["fixture"] = "def test(): return True # no assert cpp == js"
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg5_bad, tf)
    tf_path5 = tf.name
p5 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path5], cwd=dir_path, capture_output=True, text=True)
negative_results["ports"] = {
    "control_type": "missing_multilang_equality_assertions",
    "exit_code": p5.returncode,
    "status": json.loads(p5.stdout).get("status") if p5.stdout else "ERROR",
    "detected_failure": p5.returncode != 0
}
os.remove(tf_path5)

# Test 6: authorship - negative control with missing table
with open(os.path.join(test_data_dir, "authorship.json"), "r", encoding="utf-8") as f:
    cfg6 = json.load(f)
cfg6_bad = copy.deepcopy(cfg6)
cfg6_bad["sources"]["renderer"]["fixture"] = "No table data here."
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg6_bad, tf)
    tf_path6 = tf.name
p6 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path6], cwd=dir_path, capture_output=True, text=True)
negative_results["authorship"] = {
    "control_type": "corrupted_authorship_table",
    "exit_code": p6.returncode,
    "status": json.loads(p6.stdout).get("status") if p6.stdout else "ERROR",
    "detected_failure": p6.returncode != 0
}
os.remove(tf_path6)

# Test 7: doi - negative control where DOIs match (no discrepancy)
with open(os.path.join(test_data_dir, "doi.json"), "r", encoding="utf-8") as f:
    cfg7 = json.load(f)
cfg7_bad = copy.deepcopy(cfg7)
cfg7_bad["sources"]["bibliography"]["fixture"] = "All DOIs perfectly matched 10.1371/..."
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(cfg7_bad, tf)
    tf_path7 = tf.name
p7 = subprocess.run([sys.executable, "audit.py", "--selftest", "--config", tf_path7], cwd=dir_path, capture_output=True, text=True)
negative_results["doi"] = {
    "control_type": "no_doi_mismatch",
    "exit_code": p7.returncode,
    "status": json.loads(p7.stdout).get("status") if p7.stdout else "ERROR",
    "detected_failure": p7.returncode != 0
}
os.remove(tf_path7)

print("NEGATIVE CONTROL RESULTS:")
for k, v in negative_results.items():
    print(f"  [{k}] Exit: {v['exit_code']} | Status: {v['status']} | Detected failure: {v['detected_failure']}")

with open("scratch/negative_controls_results.json", "w", encoding="utf-8") as f:
    json.dump(negative_results, f, indent=2)
