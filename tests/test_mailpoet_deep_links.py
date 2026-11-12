"""Static regression checks for email deep links into the 14 on-site test panels.

This tests HTML targets, not mail-client compatibility or browser UX.
"""
from pathlib import Path
import re
import unittest

ARTICLE = (Path(__file__).resolve().parents[1] / "articles" /
           "joel-dietz-audit-nathan-sweet-bubble-sort-response" / "article.html")


class MailPoetDeepLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = ARTICLE.read_text(encoding="utf-8")

    def test_all_fourteen_panels_have_descendant_targets(self):
        panels = list(re.finditer(
            r'<details\b(?=[^>]*\bclass="rcf-computational-test")'
            r'(?=[^>]*\bid="(rcf-computational-[^"]+)")[^>]*>'
            r'[\s\S]*?</summary>\s*<div\s+id="([^"]+)"',
            self.body,
        ))
        self.assertEqual(len(panels), 14, "Seven distinct tests, each in quick and detailed views")
        ids = [m.group(1) for m in panels]
        targets = [m.group(2) for m in panels]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(targets), len(set(targets)))
        for original, target in zip(ids, targets):
            self.assertEqual(target, original + "-open")

    def test_site_disclosures_remain_collapsed(self):
        detail_starts = re.findall(r'<details\b[^>]*class="rcf-computational-test"[^>]*>', self.body)
        self.assertEqual(len(detail_starts), 14)
        self.assertFalse(any(re.search(r'\bopen(?:\s|>|=)', s) for s in detail_starts),
                         "All instruction panels should remain collapsed until opened")

    def test_opening_archive_metadata_retains_both_inline_doi_badges(self):
        marker = '<p class="sr-citation-and-archives"'
        self.assertEqual(self.body.count(marker), 1)
        opening = self.body.split(marker, 1)[1].split("</p>", 1)[0]
        self.assertEqual(opening.count('<img '), 2)
        self.assertNotIn("<br", opening)
        self.assertEqual(opening.count('class="sr-doi-badge"'), 2)
        for doi in ("10.5281/zenodo.24151128", "10.5281/zenodo.24151127"):
            self.assertIn("https://doi.org/" + doi, opening)
            self.assertIn("https://zenodo.org/badge/DOI/" + doi + ".svg", opening)
            self.assertIn('alt="DOI: ' + doi + '"', opening)
        self.assertIn("display:inline !important", opening)

    def test_existing_opening_citation_doi_and_bottom_line_order(self):
        positions = [self.body.index(marker) for marker in (
            "<strong>Cite as:</strong>", "<strong>Versions and archives:</strong>",
            "<strong>Bottom line.</strong>")]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
