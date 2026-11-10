import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from core_framework_links_gate import CORE_URLS, inspect


class CoreFrameworkLinksGateTests(unittest.TestCase):
    def test_all_four_are_required(self):
        body = "<div>" + "".join(f'<a href="{url}">{name}</a>' for name, url in CORE_URLS.items()) + "</div>"
        out = inspect(body)
        self.assertTrue(out["all_four_present"])
        self.assertEqual(out["missing"], [])

    def test_three_of_four_fails(self):
        links = list(CORE_URLS.items())[:3]
        out = inspect("<div>" + "".join(f'<a href="{url}">{name}</a>' for name, url in links) + "</div>")
        self.assertFalse(out["all_four_present"])
        self.assertEqual(out["missing"], ["ethos"])

    def test_unlinked_terms_surface_and_linked_terms_are_excluded(self):
        body = '<div><p>Our RCF applies here. <a href="' + CORE_URLS["rcf"] + '">RCF</a></p></div>'
        report = inspect(body)
        hits = [x for x in report["unlinked_named_mentions_for_human_review"] if x["name"] == "rcf"]
        self.assertEqual(len(hits), 1)

    def test_query_fragment_and_trailing_slash_accepted(self):
        links = "".join(f'<a href="{url}?source=paper#methods">{name}</a>' for name, url in CORE_URLS.items())
        self.assertTrue(inspect("<div>" + links + "</div>")["all_four_present"])


if __name__ == "__main__":
    unittest.main()
