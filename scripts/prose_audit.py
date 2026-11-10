#!/usr/bin/env python3
"""Heuristic scholarly-prose linter. Not an AI-authorship or quality classifier.

Only standard-library dependencies. Intentionally excludes quotations, code and
reference sections from automatic scoring; inspect excluded material manually.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


WORDS = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
SENTENCES = re.compile(r"(?<=[.!?])\s+(?=[A-Z“\"])")
ANTITHESIS = re.compile(
    r"\bnot(?:\s+[\w'’–-]+){1,12}\s+but\b|"
    r"\bnot\s+(?:merely|just|only)\b.{0,130}?\bbut\b|"
    r"\bthe\s+question\s+is\s+not\b",
    re.IGNORECASE,
)
REVERSE_CONTRAST = re.compile(r"\brather than\b|\binstead of\b", re.IGNORECASE)
TRIAD = re.compile(
    r"\b[a-zA-Z][\w'-]*(?:\s+[a-zA-Z][\w'-]*){0,3},\s+"
    r"[a-zA-Z][\w'-]*(?:\s+[a-zA-Z][\w'-]*){0,3},\s+"
    r"(?:and|or)\s+[a-zA-Z][\w'-]*(?:\s+[a-zA-Z][\w'-]*){0,3}\b",
    re.IGNORECASE,
)
SIGNPOST = re.compile(
    r"\b(?:the deeper point|the key takeaway|in other words|to be clear|"
    r"what matters is|this is where|it is important to note|"
    r"it is worth noting|as we have seen|in conclusion|"
    r"let us (?:now )?(?:turn|examine|consider)|"
    r"this section (?:will|has)|importantly|crucially|ultimately)\b",
    re.IGNORECASE,
)
GENERIC = re.compile(
    r"\b(?:delve(?:s|d)? into|tapestry|multifaceted|"
    r"ever-evolving landscape|in today's (?:world|landscape)|"
    r"unlock(?:ing)? the potential|testament to|"
    r"robust and nuanced|plays a pivotal role)\b",
    re.IGNORECASE,
)
REFERENCE = re.compile(
    r"^(?:references?|bibliograph(?:y|ies)|works cited|"
    r"(?:full )?scholarly references|appendix [a-z]:? (?:full )?(?:scholarly )?references)",
    re.IGNORECASE,
)
SKIP_TAGS = {"script", "style", "pre", "code", "blockquote", "nav", "footer", "aside"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


@dataclass(frozen=True)
class Block:
    section: str
    text: str


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.section = "(opening)"
        self.skip_depth = 0
        self.active_tag: str | None = None
        self.active_text: list[str] = []
        self.heading_level = 0
        self.reference_level: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self.skip_depth:
            if tag not in VOID_TAGS:
                self.skip_depth += 1
            return
        if tag in SKIP_TAGS:
            self.skip_depth = 1
            return
        if self.active_tag is None and re.fullmatch(r"h[1-6]", tag):
            self.active_tag = tag
            self.heading_level = int(tag[1])
            self.active_text = []
        elif self.active_tag is None and tag in {"p", "li"}:
            self.active_tag = tag
            self.active_text = []
        elif tag == "br" and self.active_tag:
            self.active_text.append(" ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.skip_depth:
            self.skip_depth -= 1
            return
        if tag != self.active_tag:
            return
        value = re.sub(r"\s+", " ", "".join(self.active_text)).strip()
        if tag.startswith("h"):
            if self.reference_level is not None and self.heading_level <= self.reference_level:
                self.reference_level = None
            self.section = value or "(untitled heading)"
            if REFERENCE.match(self.section):
                self.reference_level = self.heading_level
        elif value and self.reference_level is None:
            self.blocks.append(Block(self.section, value))
        self.active_tag = None
        self.active_text = []

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and self.active_tag:
            self.active_text.append(data)


def extract_blocks(source: str, fmt: str) -> list[Block]:
    if fmt == "html":
        parser = ArticleParser()
        parser.feed(source)
        parser.close()
        return parser.blocks

    blocks: list[Block] = []
    section = "(opening)"
    lines: list[str] = []
    fenced = False
    reference_level: int | None = None

    def flush() -> None:
        nonlocal lines
        value = re.sub(r"\s+", " ", " ".join(lines)).strip()
        if value and reference_level is None:
            blocks.append(Block(section, value))
        lines = []

    for raw in source.splitlines() + [""]:
        stripped = raw.strip()
        if stripped.startswith(("```", "~~~")):
            flush()
            fenced = not fenced
            continue
        if fenced or stripped.startswith(">"):
            flush()
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)", stripped)
        if heading:
            flush()
            level = len(heading.group(1))
            if reference_level is not None and level <= reference_level:
                reference_level = None
            section = heading.group(2)
            if REFERENCE.match(section):
                reference_level = level
        elif not stripped:
            flush()
        else:
            lines.append(re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", stripped))
    return blocks


def _excerpt(text: str, start: int = 0, end: int | None = None, limit: int = 190) -> str:
    end = end if end is not None else start + 50
    first = max(0, start - 45)
    last = min(len(text), max(end + 55, first + limit))
    return ("…" if first else "") + text[first:last].strip() + ("…" if last < len(text) else "")


def _ngrams(text: str, n: int = 4) -> set[tuple[str, ...]]:
    words = [w.lower() for w in WORDS.findall(text)]
    return set(zip(*(words[i:] for i in range(n)))) if len(words) >= n else set()


def analyze(source: str, fmt: str = "html", max_examples: int = 5) -> dict:
    blocks = extract_blocks(source, fmt)
    total_words = sum(len(WORDS.findall(b.text)) for b in blocks)
    findings: dict[str, list[dict]] = defaultdict(list)

    def record(category: str, block: Block, text: str, at: int = 0, end: int | None = None) -> None:
        findings[category].append({
            "section": block.section,
            "excerpt": _excerpt(text, at, end),
        })

    all_openings: dict[tuple[str, str], list[Block]] = defaultdict(list)
    qualified: list[tuple[Block, set[tuple[str, ...]], int]] = []

    for block in blocks:
        for category, pattern in (
            ("antithetical_contrast", ANTITHESIS),
            ("reverse_contrast", REVERSE_CONTRAST),
            ("three_part_list", TRIAD),
            ("formulaic_signpost", SIGNPOST),
            ("generic_fluency", GENERIC),
        ):
            for match in pattern.finditer(block.text):
                record(category, block, block.text, match.start(), match.end())
        for at, char in enumerate(block.text):
            if char == "—":
                record("em_dash", block, block.text, at, at + 1)
        if block.text.count("?") >= 3:
            record("question_cluster", block, block.text)

        for sentence in SENTENCES.split(block.text):
            opening = " ".join(w.lower() for w in WORDS.findall(sentence)[:3])
            if len(opening.split()) >= 3:
                all_openings[(block.section, opening)].append(block)
        word_count = len(WORDS.findall(block.text))
        if word_count >= 35:
            qualified.append((block, _ngrams(block.text), word_count))

    for (section, phrase), occurrences in all_openings.items():
        if len(occurrences) >= 3:
            findings["repeated_sentence_opening"].append({
                "section": section, "opening": phrase, "occurrences": len(occurrences),
                "excerpt": _excerpt(occurrences[0].text),
            })

    # Same-length prefilter limits the quadratic comparisons for long articles.
    duplicate_cap = 30
    for idx, (left, lgrams, ln) in enumerate(qualified):
        if len(findings["near_duplicate_paragraph"]) >= duplicate_cap:
            break
        for right, rgrams, rn in qualified[idx + 1:]:
            if min(ln, rn) / max(ln, rn) < 0.65:
                continue
            union = lgrams | rgrams
            if union and len(lgrams & rgrams) / len(union) >= 0.72:
                findings["near_duplicate_paragraph"].append({
                    "section": left.section,
                    "other_section": right.section,
                    "excerpt": _excerpt(left.text),
                    "other_excerpt": _excerpt(right.text),
                })
                if len(findings["near_duplicate_paragraph"]) >= duplicate_cap:
                    break

    rates = {
        name: round(len(items) * 1000 / total_words, 2) if total_words else 0
        for name, items in sorted(findings.items()) if items
    }
    section_counts: dict[str, Counter] = defaultdict(Counter)
    for category, items in findings.items():
        for item in items:
            section_counts[item["section"]][category] += 1
    local_clusters = [
        {"section": section, "signal": category, "count": count}
        for section, counts in section_counts.items()
        for category, count in counts.items()
        if count >= (1 if category in {"repeated_sentence_opening", "near_duplicate_paragraph"} else 3)
    ]
    local_clusters.sort(key=lambda item: (-item["count"], item["section"], item["signal"]))
    guide = {
        "antithetical_contrast": 6.0,
        "reverse_contrast": 5.0,
        "three_part_list": 8.0,
        "formulaic_signpost": 5.0,
        "generic_fluency": 2.0,
        "em_dash": 8.0,
    }
    return {
        "status": "heuristic editorial leads; human verification required",
        "format": fmt, "prose_blocks": len(blocks), "prose_words": total_words,
        "counts": {name: len(items) for name, items in sorted(findings.items()) if items},
        "per_1000_words": rates,
        "high_recurrence": [name for name, rate in rates.items() if rate >= guide.get(name, float("inf"))],
        "local_clusters": local_clusters[:50],
        "examples": {name: items[:max_examples] for name, items in sorted(findings.items()) if items},
        "exclusions": "HTML blockquotes/code/nav/footer/aside and headed references; Markdown quote/code/reference blocks",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="HTML or Markdown source, or '-' for stdin")
    parser.add_argument("--format", choices=("auto", "html", "markdown"), default="auto")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-examples", type=int, default=5)
    args = parser.parse_args(argv)
    raw = sys.stdin.read() if str(args.path) == "-" else args.path.read_text(encoding="utf-8")
    fmt = args.format if args.format != "auto" else ("html" if str(args.path).endswith((".html", ".htm")) else "markdown")
    result = analyze(raw, fmt, max(0, args.max_examples))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['prose_words']} prose words in {result['prose_blocks']} blocks")
        for name, count in result["counts"].items():
            mark = " [review frequency]" if name in result["high_recurrence"] else ""
            print(f"{name}: {count} ({result['per_1000_words'][name]}/1k){mark}")
            for example in result["examples"].get(name, [])[:3]:
                print(f"  - [{example['section']}] {example['excerpt']}")
        print("These patterns require editorial judgment; they do not establish AI origin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
