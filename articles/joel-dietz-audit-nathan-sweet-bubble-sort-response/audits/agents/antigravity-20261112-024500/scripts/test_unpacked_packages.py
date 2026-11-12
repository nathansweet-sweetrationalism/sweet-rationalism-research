import os
import zipfile
import subprocess
import sys
import tempfile
import json

pkg_dir = r"scratch/repos/sweet-rationalism-research/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages"

results = {}
for fname in sorted(os.listdir(pkg_dir)):
    if not fname.endswith(".zip"):
        continue
    fpath = os.path.join(pkg_dir, fname)
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(fpath, "r") as zf:
            zf.extractall(tmpdir)
        
        # Test selftest
        p_self = subprocess.run([sys.executable, "audit.py", "--selftest"], cwd=tmpdir, capture_output=True, text=True)
        # Test live
        p_live = subprocess.run([sys.executable, "audit.py", "--live"], cwd=tmpdir, capture_output=True, text=True)
        
        results[fname] = {
            "selftest_exit": p_self.returncode,
            "selftest_status": json.loads(p_self.stdout).get("status") if p_self.returncode == 0 else p_self.stderr,
            "live_exit": p_live.returncode,
            "live_status": json.loads(p_live.stdout).get("status") if p_live.returncode == 0 else p_live.stderr,
        }
        print(f"[{fname}] selftest: {results[fname]['selftest_status']} | live: {results[fname]['live_status']}")

with open("scratch/unpacked_package_tests.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
