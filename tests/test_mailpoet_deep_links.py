"""Static contract tests for email-safe, browser-loaded computational panels.

These tests do NOT prove client-side JavaScript execution or email rendering.
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "articles" / "joel-dietz-audit-nathan-sweet-bubble-sort-response"
ARTICLE = ARTICLE_DIR / "article.html"
PANEL_SOURCE = ARTICLE_DIR / "mailpoet" / "COMPUTATIONAL_PANEL_TEMPLATES_2026-11-12.txt"
CANONICAL = ("https://sweetrationalism.com/articles/epistemology/"
             "joel-dietz-audit-nathan-sweet-bubble-sort-response/")
TYPES = {"doi", "tadpole", "xenobot", "score", "ports", "validator", "authorship"}


class MailPoetDeepLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = ARTICLE.read_text(encoding="utf-8")
        cls.payload = json.loads(PANEL_SOURCE.read_text(encoding="utf-8"))

    def test_mailpoet_source_has_no_embedded_test_body(self):
        self.assertNotIn("<details", self.body)
        self.assertNotIn("<textarea", self.body)
        self.assertNotIn("INDEPENDENT SOURCE-FIRST COMPUTATIONAL AUDIT:", self.body)

    def test_all_fourteen_links_preserve_identifiers(self):
        anchors = re.findall(
            r'<a class="rcf-computational-trigger"'
            r'\s+id="(rcf-computational-([a-z]+)-(quick|analysis)-open)"'
            r'\s+data-rcf-panel="([^"]+)"\s+href="([^"]+)"',
            self.body,
        )
        self.assertEqual(len(anchors), 14)
        self.assertEqual(len({a[0] for a in anchors}), 14)
        self.assertEqual({a[1] for a in anchors}, TYPES)
        self.assertEqual({a[2] for a in anchors}, {"quick", "analysis"})
        for link_id, _type, _mode, data_id, href in anchors:
            self.assertEqual(data_id + "-open", link_id)
            self.assertEqual(href, CANONICAL + "#" + link_id)

    def test_quick_check_list_contains_single_title_per_item(self):
        m = re.search(r'<ul class="rcf-computational-checklist"[^>]*>(.*?)</ul>',
                      self.body, flags=re.S)
        self.assertIsNotNone(m)
        html = m.group(1)
        self.assertEqual(html.count("<li "), 7)
        self.assertEqual(html.count('class="rcf-computational-trigger"'), 7)
        self.assertNotIn("<strong>", html, "Duplicate topic labels must not precede the links")
        self.assertEqual(html.count("Instructions To Test This Computationally"), 7)

    def test_external_template_payload_reconstructs_14_panels(self):
        self.assertEqual(self.payload["schema"], "rcf-computational-panels.v1")
        self.assertEqual(self.payload["article_id"], 218725796)
        self.assertEqual(self.payload["placeholder"], "__RCF_PANEL_ID__")
        self.assertEqual(set(self.payload["templates"]), TYPES)
        for name, template in self.payload["templates"].items():
            self.assertIn("<details", template, name)
            self.assertIn("<textarea", template, name)
            self.assertIn('id="__RCF_PANEL_ID__"', template, name)
            self.assertIn("</details>", template, name)
            for mode in ("quick", "analysis"):
                panel_id = f"rcf-computational-{name}-{mode}"
                expanded = template.replace("__RCF_PANEL_ID__", panel_id)
                self.assertIn(f'id="{panel_id}"', expanded)
                self.assertIn("<summary", expanded)

    def test_doi_text_followed_by_separate_two_badge_row(self):
        m = re.search(
            r'<p class="sr-citation-and-archives"[^>]*>(.*?)</p>\s*'
            r'<!-- /wp:paragraph -->\s*<!-- wp:paragraph -->\s*'
            r'<p class="sr-doi-badges"[^>]*>(.*?)</p>',
            self.body, re.S,
        )
        self.assertIsNotNone(m, "Two adjacent metadata paragraphs required")
        citation, badges = m.groups()
        self.assertNotIn("<br", citation + badges)
        self.assertNotIn("<img", citation)
        self.assertEqual(badges.count('<img '), 2)
        for doi in ("10.5281/zenodo.24151128", "10.5281/zenodo.24151127"):
            self.assertIn("https://doi.org/" + doi, citation)
            self.assertIn("https://doi.org/" + doi, badges)
            self.assertIn("https://zenodo.org/badge/DOI/" + doi + ".svg", badges)
            self.assertIn('alt="DOI: ' + doi + '"', badges)

    def test_opening_order_keeps_bottom_line_after_badges(self):
        markers = ("<strong>Cite as:</strong>",
                   "<strong>Versions and archives:</strong>",
                   '<p class="sr-doi-badges"',
                   "<strong>Bottom line.</strong>")
        positions = [self.body.index(mark) for mark in markers]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
