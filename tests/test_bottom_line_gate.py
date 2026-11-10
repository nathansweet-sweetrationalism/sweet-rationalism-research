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
