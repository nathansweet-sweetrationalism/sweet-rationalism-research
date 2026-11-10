#!/usr/bin/env python3
"""Check four mandatory framework citations in an HTML article.

This is a structural gate and unlinked-mention lead list; naturalness, reader
value, correct scope and repetition remain human editorial responsibilities.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from lxml import html


CORE_URLS = {
    "rcf": "https://sweetrationalism.com/frameworks/recursive-corrigibility-framework/",
    "ontology": "https://sweetrationalism.com/frameworks/ontology-scale-relative-realism/",
    "bridge": "https://sweetrationalism.com/frameworks/interoperability-framework-bridge/",
    "ethos": "https://sweetrationalism.com/frameworks/sweet-rationalism-a-foundational-framework/",
}
TERMS = {
    "rcf": re.compile(r"\b(?:RCF|Recursive Corrigibility Framework)\b", re.I),
    "ontology": re.compile(r"\b(?:PBSRR|Provisional Boundary.{0,15}Scale.Relative Realism|my ontology)\b", re.I),
    "bridge": re.compile(r"\b(?:Framework Bridge|interoperability framework bridge|my framework bridge)\b", re.I),
    "ethos": re.compile(r"\b(?:Sweet Rationalism Ethos|my ethos|our ethos)\b", re.I),
}


def path_key(url: str) -> tuple[str, str]:
    u = urlsplit(url)
    return (u.netloc.lower().removeprefix("www."), u.path.rstrip("/").lower())


def inspect(body: str) -> dict:
    root = html.fromstring(body)
    links = {path_key(a.get("href", "")): a for a in root.xpath("//a[@href]")}
    missing = [name for name, url in CORE_URLS.items() if path_key(url) not in links]
    unlinked = []
    for element in root.iter():
        if element.tag in {"script", "style", "noscript", "a"}:
            continue
        if any(p.tag in {"a", "script", "style", "noscript"} for p in element.iterancestors()):
            continue
        text = element.text or ""
        for name, pattern in TERMS.items():
            for m in pattern.finditer(text):
                unlinked.append({"name": name, "term": m.group(0), "context": text[:180].strip()})
        # Tail text follows the current element's closing tag and is *not*
        # within that element's link, but may still be in a linked ancestor.
        if not any(p.tag in {"a", "script", "style", "noscript"} for p in element.iterancestors()):
            tail = element.tail or ""
            for name, pattern in TERMS.items():
                for m in pattern.finditer(tail):
                    unlinked.append({"name": name, "term": m.group(0), "context": tail[:180].strip()})
    return {
        "all_four_present": not missing,
        "missing": missing,
        "canonical_urls": CORE_URLS,
        "unlinked_named_mentions_for_human_review": unlinked,
        "scope": "structural HTML link gate; unlinked terms may legitimately recur in historical quotes, titles or long text",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", type=Path)
    parser.add_argument("--strict", action="store_true", help="Fail if any of the four canonical URLs is absent")
    args = parser.parse_args()
    report = inspect(args.html_file.read_text(encoding="utf-8"))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.strict and not report["all_four_present"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
