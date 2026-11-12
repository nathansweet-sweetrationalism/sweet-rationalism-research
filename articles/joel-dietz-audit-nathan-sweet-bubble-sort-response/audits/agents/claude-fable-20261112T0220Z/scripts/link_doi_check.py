#!/usr/bin/env python3
"""Check a list of URLs (HTTP status, signed-out) and resolve DOIs against Crossref / DataCite.
Stdlib only. Input: JSON list of {"url": ...}. Output: JSON with per-URL status and DOI metadata.
Usage: python link_doi_check.py links.json out.json
A resolving DOI or a 200 response shows identity/availability only, never claim support.
"""
import json, sys, urllib.request, urllib.error, urllib.parse, concurrent.futures as cf
UA = {"User-Agent": "Mozilla/5.0 (independent-audit link check)"}

def status(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=40) as r:
                return {"url": url, "http": r.status, "final": r.geturl(), "method": method}
        except urllib.error.HTTPError as e:
            last = {"url": url, "http": e.code, "method": method}
        except Exception as e:
            last = {"url": url, "http": None, "error": repr(e)[:160], "method": method}
    return last

def doi_meta(doi):
    try:
        req = urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi), headers=UA)
        m = json.load(urllib.request.urlopen(req, timeout=40))["message"]
        return {"doi": doi, "registry": "crossref", "title": (m.get("title") or [""])[0],
                "container": (m.get("container-title") or [""])[0], "volume": m.get("volume"), "issue": m.get("issue"),
                "page": m.get("page") or m.get("article-number"),
                "year": (m.get("published", {}).get("date-parts") or [[None]])[0][0],
                "authors": [a.get("family") for a in m.get("author", [])],
                "updates": [u.get("type") for u in m.get("update-to", [])] + [u.get("type") for u in m.get("updated-by", [])]}
    except Exception as e:
        try:
            req = urllib.request.Request("https://api.datacite.org/dois/" + urllib.parse.quote(doi), headers=UA)
            a = json.load(urllib.request.urlopen(req, timeout=40))["data"]["attributes"]
            return {"doi": doi, "registry": "datacite", "title": a["titles"][0]["title"], "year": a.get("publicationYear"),
                    "authors": [c.get("familyName") or c.get("name") for c in a.get("creators", [])]}
        except Exception as e2:
            return {"doi": doi, "error": repr(e)[:120] + " | " + repr(e2)[:120]}

def main():
    urls = sorted({r["url"] for r in json.load(open(sys.argv[1], encoding="utf-8")) if r["url"].startswith("http")})
    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(status, urls))
    dois = sorted({u.split("doi.org/", 1)[1] for u in urls if "doi.org/" in u} | set(sys.argv[3:]))
    meta = [doi_meta(d) for d in dois]
    json.dump({"links": res, "dois": meta}, open(sys.argv[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    bad = [r for r in res if r.get("http") != 200]
    print("urls", len(res), "non-200", len(bad))
    for r in bad: print("  ", r.get("http"), r["url"][:150], r.get("error", "")[:60])
    for m in meta: print(json.dumps(m, ensure_ascii=False)[:330])

if __name__ == "__main__":
    main()
