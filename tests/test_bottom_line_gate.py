import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("bottom_line_gate", Path(__file__).resolve().parents[1] / "scripts/bottom_line_gate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
inspect_html = module.inspect_html


CONTENT = (
    "<p><strong>Bottom line.</strong> A recorded experiment gives us a real empirical observation, "
    "but the proposed new explanation requires a comparison that distinguishes it from a stronger "
    "conventional rival. Popper's falsifiability and Mayo's severe testing help specify that "
    "comparison. We must identify who tested the idea, what was actually measured, where the "
    "mechanism enters, and what result would favor the distinct ontology rather than a simpler "
    "causal model. The present result warrants a narrow conclusion under its tested conditions; "
    "a future intervention could justify revising that assessment, and none of it settles every "
    "possible account of reality.</p>"
)


class BottomLineGateTests(unittest.TestCase):
    def test_good_after_two_metadata_lines(self):
        page = "<h1>Article title</h1><p>Research record: source</p><p>Versions and archives: DOI</p>" + CONTENT + "<h2>Abstract</h2>"
        result = inspect_html(page, required_terms=["Mayo", "Popper"])
        self.assertTrue(result["pass_structural"])

    def test_citation_and_versions_precede_bottom_line(self):
        deck = "<p><em>Opening deck.</em></p>"
        citation = "<p><strong>Cite as:</strong> " + ("Citation details and licensing. " * 16) + "</p>"
        versions = "<p><strong>Versions and archives:</strong> DOI with badge and GitHub link.</p>"
        result = inspect_html(deck + citation + versions + CONTENT)
        self.assertTrue(result["pass_structural"], result["failures"])

    def test_citation_after_bottom_line_fails(self):
        result = inspect_html(CONTENT + "<p><strong>Cite as:</strong> Citation details.</p>")
        self.assertFalse(result["pass_structural"])
        self.assertTrue(any("must precede" in x for x in result["failures"]))

    def test_versions_before_citation_fails(self):
        result = inspect_html("<p>Versions and archives: DOI</p><p>Cite as: Citation.</p>" + CONTENT)
        self.assertFalse(result["pass_structural"])
        self.assertTrue(any("metadata order" in x for x in result["failures"]))

    def test_single_italic_deck_before_bottom_line_passes(self):
        deck = "<!-- wp:paragraph -->" + "<p><em>" + "word " * 60 + "</em></p>" + "<!-- /wp:paragraph -->"
        self.assertTrue(inspect_html(deck + CONTENT)["pass_structural"])

    def test_non_italic_long_preamble_still_fails(self):
        preamble = "<p>" + "word " * 60 + "</p>"
        self.assertFalse(inspect_html(preamble + CONTENT)["pass_structural"])

    def test_second_long_paragraph_after_deck_still_fails(self):
        deck = "<p><em>" + "word " * 60 + "</em></p><p>" + "word " * 60 + "</p>"
        self.assertFalse(inspect_html(deck + CONTENT)["pass_structural"])

    def test_absent_fails(self):
        self.assertFalse(inspect_html("<h1>Article</h1><p>The question is difficult.</p>")["pass_structural"])

    def test_after_abstract_fails(self):
        self.assertFalse(inspect_html("<h1>Article</h1><h2>Abstract</h2>" + CONTENT)["pass_structural"])

    def test_after_long_intro_fails(self):
        intro = "<p>" + ("This is a substantial contextual paragraph. " * 10) + "</p>"
        self.assertFalse(inspect_html(intro + CONTENT)["pass_structural"])

    def test_wrong_scholar_term_fails_when_requested(self):
        self.assertFalse(inspect_html(CONTENT, required_terms=["Lakatos"])["pass_structural"])


if __name__ == "__main__":
    unittest.main()
