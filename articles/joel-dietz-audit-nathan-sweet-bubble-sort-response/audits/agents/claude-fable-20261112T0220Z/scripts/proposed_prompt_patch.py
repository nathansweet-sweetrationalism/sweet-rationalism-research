#!/usr/bin/env python3
"""Apply the three minimal panel repairs to a PRIVATE copy of the draft and measure before/after.
Writes the patched HTML and unified diff to a PRIVATE directory; prints only counts.
Repairs: (1) nonexistent "--offline" flag -> real "python audit.py --selftest";
(2) nonexistent verify.py -> audit.py; (3) status label FIXTURE_CHECK_ONLY -> SELFTEST_ONLY (what audit.py prints).
Usage: python proposed_prompt_patch.py <private article.json> <private_out_dir>
"""
import difflib, hashlib, json, pathlib, re, sys
src = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")); out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
a = src["content"]
count = lambda s: {"offline_flag": len(re.findall(r"--offline", s)), "verify_py": len(re.findall(r"verify\.py", s)),
                   "FIXTURE_CHECK_ONLY": s.count("FIXTURE_CHECK_ONLY"), "selftest_command_in_textareas":
                   sum(len(re.findall(r"python\s+audit\.py\s+--selftest", t)) for t in re.findall(r"<textarea\b[^>]*>([\s\S]*?)</textarea>", s))}
b = re.sub(r'(&quot;|")--offline(&quot;|")', r"\1python audit.py --selftest\2", a)
b = b.replace("PROMPT.md and verify.py", "PROMPT.md and audit.py").replace("FIXTURE_CHECK_ONLY", "SELFTEST_ONLY")
(out / "article_patched.json").write_text(json.dumps({"content": b, "modified": src.get("modified")}), encoding="utf-8")
(out / "article_patched.html").write_text(b, encoding="utf-8", newline="")
diff = list(difflib.unified_diff(a.splitlines(), b.splitlines(), "draft", "patched", lineterm="", n=0))
(out / "prompt_patch.diff").write_text("\n".join(diff), encoding="utf-8")
changed = sum(1 for x, y in zip(a.splitlines(), b.splitlines()) if x != y)
print(json.dumps({"before": count(a), "after": count(b), "lines_changed": changed, "line_count_equal": len(a.splitlines()) == len(b.splitlines()),
                  "char_delta": len(b) - len(a), "before_sha256": hashlib.sha256(a.encode()).hexdigest(), "after_sha256": hashlib.sha256(b.encode()).hexdigest()}, indent=1))
