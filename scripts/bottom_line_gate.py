#!/usr/bin/env python3
"""Check the *placement* of a reader-facing article Bottom line.

This is deliberately a structural validator, not a scholar/name validator,
source-fidelity test, SEO predictor, or measurement of writing quality.
Run on the article body (not a complete WordPress theme/page export).
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


BLOCKS = {"p", "h1", "h2", "h3", "h4", "h5", "h6"}
META_PREFIXES = ("research record:", "cite as:", "versions and archives:")
BOTTOM_LINE = re.compile(r"^\s*bottom\s+line\s*[.:]\s*", re.IGNORECASE)
SECTION_HEADER = re.compile(r"^(abstract|prologue|part\s+[ivx]+|section\s+[ivx]+|introduction|overview|method(?:ology)?)\b", re.I)


class ArticleBlocks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, str]] = []
        self.tag: str | None = None
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.tag is None and tag in BLOCKS:
            self.tag = tag
            self.text = []

    def handle_data(self, data: str) -> None:
        if self.tag:
            self.text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == self.tag:
            value = " ".join(" ".join(self.text).split())
            if value:
                self.blocks.append((tag, value))
            self.tag = None
            self.text = []


def inspect_html(content: str, required_terms: list[str] | None = None) -> dict:
    parser = ArticleBlocks()
    parser.feed(content)
    # An optional initial italic deck is reader-facing metadata, not a
    # substantive paragraph. Restrict this exception to a complete first
    # paragraph whose sole content is inside <em>; subsequent prose still blocks.
    leading_deck = bool(re.match(
        r"^\s*(?:<!--\s*wp:paragraph[^>]*-->\s*)?<p>\s*<em>.*?</em>\s*</p>",
        content, flags=re.I | re.S,
    ))
    core: list[tuple[int, str, str]] = []
    for i, (tag, s) in enumerate(parser.blocks):
        lower = s.lower()
        if tag == "h1" or lower.startswith(META_PREFIXES):
            continue
        core.append((i, tag, s))

    candidate = next(((i, tag, text) for i, tag, text in core if BOTTOM_LINE.match(text)), None)
    failures = []
    cautions = []
    if candidate is None:
        failures.append("No paragraph beginning 'Bottom line.' was found")
        first_index = None
        word_count = 0
        extract = ""
    else:
        i, tag, extract = candidate
        first_index = i
        word_count = len(extract.split())
        if tag != "p":
            failures.append("The Bottom line must begin a paragraph, not a heading or list")
        # Opening citation/license and archive metadata belong ABOVE the Bottom line.
        # Do not mistake a long Cite as paragraph for a substantive preamble.
        metadata = [(pos, prefix) for pos, (t, val) in enumerate(parser.blocks)
                    if t == "p" for prefix in META_PREFIXES
                    if val.casefold().startswith(prefix)]
        after = [prefix for pos, prefix in metadata if pos > i]
        if after:
            failures.append("Opening provenance metadata must precede Bottom line: " + ", ".join(after))
        before = [prefix for pos, prefix in metadata if pos < i]
        ranks = [META_PREFIXES.index(prefix) for prefix in before]
        if ranks != sorted(ranks):
            failures.append("Opening provenance metadata order must be Research record, Cite as, Versions and archives")
        preceding = [(t, s) for pos, t, s in core if pos < i]
        if len(preceding) > 2:
            failures.append(f"Bottom line follows {len(preceding)} non-archive blocks; expected near the top")
        if any(SECTION_HEADER.match(s) for _, s in preceding):
            failures.append("Bottom line follows an abstract, introduction or major-section heading")
        if any(t == "p" and len(text.split()) > 38 and not (leading_deck and pos == 0)
               for pos, t, text in core if pos < i):
            failures.append("A full substantive paragraph precedes the Bottom line")
        if word_count < 55 or word_count > 230:
            cautions.append(f"Bottom line length is {word_count} words; normally aim near 80–160 where useful")
        for term in required_terms or []:
            if term.casefold() not in extract.casefold():
                failures.append(f"Requested article-specific term not found: {term}")

    return {
        "pass_structural": not failures,
        "bottom_line_source_block_index": first_index,
        "bottom_line_words": word_count,
        "bottom_line_excerpt": extract[:260],
        "failures": failures,
        "warnings": cautions,
        "human_checks_required": [
            "actual source/citation fidelity",
            "relevant named scholars and technical definitions",
            "strong rival and justified inference bridge",
            "scope, uncertainty and meaningful loss condition",
            "accessible natural prose, no keyword stuffing",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("article", type=Path, help="UTF-8 raw article body")
    p.add_argument("--format", choices=["html"], default="html")
    p.add_argument("--required-term", action="append", default=[], help="Manual article-specific term for exact substring check")
    p.add_argument("--json", action="store_true", help="Print JSON receipt")
    args = p.parse_args()
    result = inspect_html(args.article.read_text(encoding="utf-8"), args.required_term)
    result["file"] = str(args.article)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Bottom line structural gate: " + ("PASS" if result["pass_structural"] else "FAIL"))
        print("words=" + str(result["bottom_line_words"]))
        for note in result["failures"]:
            print("FAIL: " + note)
        for note in result["warnings"]:
            print("WARN: " + note)
        print("Human scholarly/source check is mandatory regardless of structural result.")
    return 0 if result["pass_structural"] else 2


if __name__ == "__main__":
    sys.exit(main())
