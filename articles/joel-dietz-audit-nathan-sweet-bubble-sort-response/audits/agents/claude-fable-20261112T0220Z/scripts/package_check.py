#!/usr/bin/env python3
"""Independent package/mirror/CLI check for the seven test ZIPs. Stdlib only.
Downloads both mirrors named in sources.json, hashes, compares to the repo copy,
lists ZIP members with CRC, compares bundled audit.py/test.json with repository
files, then runs each package's audit.py in a disposable directory under several
CLI invocations (live, selftest, obsolete flag, no flag, malformed config).
Usage: python package_check.py <article_dir> <work_dir> <out_json>
"""
import hashlib, json, pathlib, subprocess, sys, urllib.request, zipfile, io, shutil, platform

def sha(b): return hashlib.sha256(b).hexdigest()
def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "independent-audit/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read(), dict(r.headers).get("Content-Type")
    except Exception as e:
        return None, None, repr(e)

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180, encoding="utf-8", errors="replace")
    status = None
    try: status = json.loads(p.stdout).get("status")
    except Exception: pass
    return {"cmd": " ".join(cmd[1:]), "exit": p.returncode, "status": status,
            "stdout_sha256": sha(p.stdout.encode()), "stderr_head": p.stderr[:300]}, p.stdout

def main():
    art, work, out = map(pathlib.Path, sys.argv[1:4])
    src = json.loads((art / "sources.json").read_text(encoding="utf-8"))
    repo_audit = (art / "audit.py").read_bytes()
    res = {"python": platform.python_version(), "platform": platform.platform(),
           "repo_audit_sha256": sha(repo_audit), "tests": {}}
    for tid, t in src["tests"].items():
        r = {}
        gs, gb, gi = get(t["github_zip_url"]); ws, wb, wi = get(t["wp_zip_url"])
        local = (art / "packages" / t["wp_zip"]).read_bytes()
        r["github"] = {"http": gs, "sha256": gb and sha(gb), "bytes": gb and len(gb), "info": gi}
        r["wordpress"] = {"http": ws, "sha256": wb and sha(wb), "bytes": wb and len(wb), "info": wi}
        r["repo_head_copy_sha256"] = sha(local)
        r["mirrors_identical"] = bool(gb and wb and gb == wb)
        r["github_equals_repo_head"] = bool(gb and gb == local)
        z = zipfile.ZipFile(io.BytesIO(gb or local))
        r["zip_testzip_bad_member"] = z.testzip()
        r["members"] = [{"name": i.filename, "size": i.file_size, "crc": f"{i.CRC:08x}",
                         "sha256": sha(z.read(i))} for i in z.infolist()]
        names = {i.filename.split("/")[-1]: i.filename for i in z.infolist()}
        r["unsafe_paths"] = [i.filename for i in z.infolist() if i.filename.startswith(("/", "\\")) or ".." in i.filename]
        r["has_verify_py"] = "verify.py" in names
        r["has_PROMPT_md"] = "PROMPT.md" in names
        if "audit.py" in names:
            norm = lambda b: b.replace(bytes([13, 10]), bytes([10]))  # Windows checkouts convert LF to CRLF
            r["bundled_audit_equals_repo_audit"] = norm(z.read(names["audit.py"])) == norm(repo_audit)
            r["bundled_audit_sha256"] = sha(z.read(names["audit.py"]))
        if "test.json" in names:
            a = json.loads(z.read(names["test.json"])); b = json.loads((art / "test-data" / f"{tid}.json").read_text(encoding="utf-8"))
            r["bundled_test_json_equals_repo_test_data"] = a == b
        d = work / tid
        if d.exists(): shutil.rmtree(d)
        d.mkdir(parents=True); z.extractall(d)
        base = pathlib.Path(names["audit.py"]).parent if "audit.py" in names else pathlib.Path(".")
        cwd = d / base
        runs = []
        for label, args in [("live", ["--live"]), ("selftest", ["--selftest"]),
                            ("obsolete_offline_flag", ["--offline"]), ("no_flag", []),
                            ("both_flags", ["--live", "--selftest"]),
                            ("missing_config", ["--live", "--config", "nope.json"])]:
            rec, stdout = run([sys.executable, "-I", "audit.py"] + args, cwd)
            rec["label"] = label; runs.append(rec)
            (work / f"{tid}.{label}.stdout.json").write_text(stdout, encoding="utf-8")
        (cwd / "bad.json").write_text("{not json", encoding="utf-8")
        rec, _ = run([sys.executable, "-I", "audit.py", "--selftest", "--config", "bad.json"], cwd)
        rec["label"] = "malformed_config"; runs.append(rec)
        # unreachable-source control: same spec with an unroutable URL
        spec = json.loads((cwd / "test.json").read_text(encoding="utf-8"))
        for s in spec["sources"].values(): s["url"] = "https://raw.githubusercontent.com/fractastical/morpholib/0000000000000000000000000000000000000000/none"
        (cwd / "dead.json").write_text(json.dumps(spec), encoding="utf-8")
        rec, _ = run([sys.executable, "-I", "audit.py", "--live", "--config", "dead.json"], cwd)
        rec["label"] = "dead_source_url"; runs.append(rec)
        r["runs"] = runs
        res["tests"][tid] = r
    out.write_text(json.dumps(res, indent=1), encoding="utf-8")
    for tid, r in res["tests"].items():
        print(tid, "gh", r["github"]["http"], "wp", r["wordpress"]["http"], "mirror_eq", r["mirrors_identical"],
              "gh=head", r["github_equals_repo_head"], "audit_eq", r.get("bundled_audit_equals_repo_audit"),
              "tj_eq", r.get("bundled_test_json_equals_repo_test_data"), "verify.py", r["has_verify_py"],
              "PROMPT", r["has_PROMPT_md"], [m["name"] for m in r["members"]])
        for x in r["runs"]: print("   ", x["label"], x["exit"], x["status"], x["stderr_head"][:90].replace("\n", " "))

if __name__ == "__main__":
    main()
