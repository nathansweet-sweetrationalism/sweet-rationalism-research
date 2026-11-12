#!/usr/bin/env python3
"""Per-panel audit of the 14 expandable prompt panels in a PRIVATELY held draft.
Emits only hashes, URLs, flags and counts (no prompt or manuscript text). Stdlib only.
Usage: python panel_checks.py <private article.json or raw html> <article_dir> <out.json> [--net]
"""
import hashlib, html, json, pathlib, re, sys, urllib.request, urllib.error
UA = {"User-Agent": "Mozilla/5.0 (independent-audit)"}
def http(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r: return r.status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return repr(e)[:80]
raw = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8-sig")
if raw.lstrip().startswith("{"):
    raw = json.loads(raw)["content"]
art = pathlib.Path(sys.argv[2]); net = "--net" in sys.argv
src = json.loads((art / "sources.json").read_text(encoding="utf-8"))["tests"]
flags = set(re.findall(r'"(--[a-z]+)"', (art / "audit.py").read_text(encoding="utf-8")))
statuses = set(re.findall(r'"([A-Z_]{6,})"', (art / "audit.py").read_text(encoding="utf-8")))
panels, cache = [], {}
for m in re.finditer(r'<details\b([^>]*)\bid="(rcf-computational-([a-z]+)-(quick|analysis))"[^>]*>([\s\S]*?)</details>', raw):
    pid, kind, place, body = m.group(2), m.group(3), m.group(4), m.group(5)
    ta = re.search(r"<textarea\b([^>]*)>([\s\S]*?)</textarea>", body)
    prompt = html.unescape(ta.group(2)); outside = body[:ta.start()] + body[ta.end():]
    urls = sorted(set(re.findall(r"https://[^\s<>\"')]+", prompt)))
    out_links = [html.unescape(u) for u in re.findall(r'href="([^"]+)"', outside)]
    out_codes = [html.unescape(re.sub(r"<[^>]+>", "", c)) for c in re.findall(r"<code>([\s\S]*?)</code>", outside)]
    used_flags = sorted(set(re.findall(r"--[a-z]+", prompt)))
    rec = {
        "panel_id": pid, "kind": kind, "place": place,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(), "prompt_chars": len(prompt),
        "textarea_attrs_readonly": "readonly" in ta.group(1),
        "raw_textarea_has_unescaped_lt": "<" in ta.group(2),
        "roundtrip_escape_ok": html.unescape(html.escape(prompt, quote=False)) == prompt,
        "primary_zip_url": src[kind]["github_zip_url"], "backup_zip_url": src[kind]["wp_zip_url"],
        "prompt_has_primary_zip_url": src[kind]["github_zip_url"] in prompt,
        "prompt_has_backup_zip_url": src[kind]["wp_zip_url"] in prompt,
        "outside_has_primary_zip_link": src[kind]["github_zip_url"] in out_links,
        "outside_has_backup_zip_link": src[kind]["wp_zip_url"] in out_links,
        "outside_code_snippets": out_codes,
        "prompt_cli_flags": used_flags, "flags_not_in_audit_py": [f for f in used_flags if f not in flags],
        "prompt_mentions_selftest": "--selftest" in prompt,
        "prompt_mentions_verify_py": "verify.py" in prompt, "prompt_mentions_audit_py": "audit.py" in prompt,
        "prompt_status_words": sorted(set(re.findall(r"\b(CONFIRMED|REFUTED|PARTIAL|UNRESOLVED|NOT_RUN|OBSERVATION_REPRODUCED|SELFTEST_ONLY|FIXTURE_CHECK_ONLY)\b", prompt))),
        "audit_py_status_words": sorted(s for s in statuses if s in ("OBSERVATION_REPRODUCED", "SELFTEST_ONLY", "UNRESOLVED", "SOURCE_CHANGED_OR_CHECK_FAILED", "SELFTEST_FAILED", "NOT_RUN")),
        "prompt_pins_upstream_commit": "4bed72c17f09bf336e36e7472e64d457db3b0195" in prompt,
        "upstream_paths_in_sources_json_all_in_prompt": all(p in prompt for p in src[kind]["paths"]),
        "upstream_paths_missing_from_prompt": [p for p in src[kind]["paths"] if p not in prompt],
        "prompt_url_count": len(urls), "outside_link_count": len(out_links),
        "outside_links_missing_noreferrer": len(re.findall(r'<a\b(?![^>]*noreferrer)[^>]*href="https?://(?!sweetrationalism\.com)', outside)),
    }
    if net:
        for u in urls:
            if u not in cache: cache[u] = http(u.rstrip(".,;"))
        rec["prompt_urls_non_200"] = {u: cache[u] for u in urls if cache[u] != 200}
    panels.append(rec)
by = {}
for p in panels: by.setdefault(p["kind"], []).append(p)
summary = {"panel_count": len(panels), "unique_prompt_hashes": len({p["prompt_sha256"] for p in panels}),
           "pairs_identical": {k: v[0]["prompt_sha256"] == v[1]["prompt_sha256"] for k, v in by.items() if len(v) == 2},
           "audit_py_flags": sorted(flags), "url_status_cache_size": len(cache)}
json.dump({"article_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(), "summary": summary, "panels": panels},
          open(sys.argv[3], "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print(json.dumps(summary))
for p in panels[:7]:
    print(p["kind"], {k: p[k] for k in ("textarea_attrs_readonly", "raw_textarea_has_unescaped_lt", "prompt_has_primary_zip_url", "prompt_has_backup_zip_url", "outside_has_primary_zip_link", "outside_has_backup_zip_link", "flags_not_in_audit_py", "prompt_mentions_selftest", "prompt_mentions_verify_py", "prompt_status_words", "upstream_paths_missing_from_prompt", "outside_links_missing_noreferrer")}, p.get("prompt_urls_non_200"), p["outside_code_snippets"])
