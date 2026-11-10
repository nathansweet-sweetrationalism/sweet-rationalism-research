import sys
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from prose_audit import analyze  # noqa: E402


class ProseAuditTests(unittest.TestCase):
    def test_contrasts_triad_and_signposts(self):
        text = (
            "<h2>Argument</h2><p>This is not a proof but a proposal. "
            "We have order, pattern, and control. Crucially, we should check it.</p>"
        )
        result = analyze(text)
        self.assertGreaterEqual(result["counts"]["antithetical_contrast"], 1)
        self.assertGreaterEqual(result["counts"]["three_part_list"], 1)
        self.assertGreaterEqual(result["counts"]["formulaic_signpost"], 1)

    def test_quoted_text_code_and_references_excluded(self):
        text = (
            "<h2>Main</h2><p>Ordinary prose remains readable.</p>"
            "<blockquote><p>It is not this but that. Crucially.</p></blockquote>"
            "<pre><code>not x but y</code></pre>"
            "<h2>References</h2><p>Not one but two references.</p>"
            "<h2>Appendix</h2><p>This is not a law but a sample.</p>"
        )
        result = analyze(text)
        self.assertEqual(result["counts"]["antithetical_contrast"], 1)
        self.assertNotIn("formulaic_signpost", result["counts"])

    def test_near_duplicate_across_sections(self):
        paragraph = (
            "A careful revision records the original passage, its conditional assumptions, "
            "the actual evidential target, the strongest competing account, a measurable "
            "difference in predictions, and the exact conditions under which this "
            "interpretation ought to lose support after a serious independent test."
        )
        result = analyze(
            f"<h2>One</h2><p>{paragraph}</p><h2>Two</h2><p>{paragraph}</p>"
        )
        self.assertEqual(result["counts"]["near_duplicate_paragraph"], 1)

    def test_markdown_quote_and_code_excluded(self):
        text = (
            "# Title\n\n> The claim is not a theory but a conjecture.\n\n"
            "```text\nNot this but that.\n```\n\n"
            "The hypothesis is not proven but it is testable.\n"
        )
        result = analyze(text, "markdown")
        self.assertEqual(result["counts"]["antithetical_contrast"], 1)

    def test_empty_document_is_honest(self):
        result = analyze("", "html")
        self.assertEqual(result["prose_words"], 0)
        self.assertEqual(result["counts"], {})

    def test_local_cluster_survives_low_global_rate(self):
        repeated = "This is not a result but a proposal. " * 3
        padding = "Ordinary explanations can be clear and varied. " * 200
        result = analyze(f"<h2>Local</h2><p>{repeated}</p><h2>Other</h2><p>{padding}</p>")
        self.assertTrue(any(
            item["section"] == "Local" and item["signal"] == "antithetical_contrast"
            and item["count"] == 3
            for item in result["local_clusters"]
        ))


if __name__ == "__main__":
    unittest.main()
