#!/usr/bin/env python3
"""Surface quotation and citation losses between scholarly HTML editions.

This is a high-recall *review queue*, not an automated verdict on fidelity.
No source quotation is considered verified merely because text was retained.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse

from lxml import html


QUOTES = re.compile(r'“([^”\n]{20,2000})”|"([^"\n]{20,2000})"')
DOI = re.compile(r'10\.\d{4,9}/[^\s"<>?#]+', re.IGNORECASE)
BLOCKS = (
    "descendant-or-self::p[not(ancestor::p)]|"
    "descendant-or-self::li[not(ancestor::li)]|"
    "descendant-or-self::blockquote|descendant-or-self::figcaption"
)


def normalized(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).casefold()
    s = re.sub(r"[‘’'“”\"‐‑–—−]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def doi_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    text = unquote(parsed.path)
    hit = DOI.search(text)
    if not hit:
        return None
    return hit.group().rstrip(".,;:)").casefold()


def extract(path: Path) -> dict:
    tree = html.fromstring(path.read_text(encoding="utf-8"))
    quotes = []
    for section_no, node in enumerate(tree.xpath(BLOCKS), 1):
        prose = " ".join(node.text_content().split())
        for match in QUOTES.finditer(prose):
            quotation = next(x for x in match.groups() if x is not None)
            if len(quotation.split()) < 5:
                continue
            quotes.append({
                "quote": quotation,
                "normalized": normalized(quotation),
                "source_block": section_no,
                "context": prose[:350],
            })
    dois = []
    for a in tree.xpath("//a[@href]"):
        url = a.get("href") or ""
        doi = doi_from_url(url)
        if doi:
            dois.append({"doi": doi, "url": url, "anchor": " ".join(a.text_content().split())[:140]})
    return {"quotes": quotes, "doi_links": dois}


def audit(before: dict, after: dict) -> dict:
    remaining = Counter(q["normalized"] for q in after["quotes"])
    missing = []
    retained = []
    for item in before["quotes"]:
        key = item["normalized"]
        if remaining[key]:
            remaining[key] -= 1
            retained.append(item)
        else:
            missing.append(item)

    previous_dois = {d["doi"] for d in before["doi_links"]}
    current_dois = {d["doi"] for d in after["doi_links"]}
    return {
        "status": "human adjudication required; quote presence is not source authenticity",
        "source_quote_count": len(before["quotes"]),
        "candidate_quote_count": len(after["quotes"]),
        "exact_normalized_quote_occurrences_retained": len(retained),
        "missing_or_modified_quote_occurrences": missing,
        "source_unique_dois": len(previous_dois),
        "candidate_unique_dois": len(current_dois),
        "source_dois_not_in_candidate": sorted(previous_dois - current_dois),
        "candidate_dois_not_in_source": sorted(current_dois - previous_dois),
        "release_rule": (
            "For each missing source quote/DOI, preserve, correct with verified provenance, "
            "or explicitly quarantine pending consent/verification; never silently delete argument-bearing evidence."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path, help="Write full JSON review queue at this private path")
    args = parser.parse_args()
    report = audit(extract(args.original), extract(args.candidate))
    print(json.dumps({k: v if not isinstance(v, list) else len(v) for k, v in report.items()}, indent=2))
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
