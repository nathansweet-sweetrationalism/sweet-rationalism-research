import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evidence_retention_audit import audit, doi_from_url, extract, normalized


class EvidenceRetentionAuditTests(unittest.TestCase):
    def test_whitespace_and_quote_style_are_not_losses(self):
        self.assertEqual(normalized('“Test  the hypothesis”'), normalized('"Test the hypothesis"'))

    def test_doi_from_resolver(self):
        self.assertEqual(doi_from_url("https://doi.org/10.5555/ABC.2019"), "10.5555/abc.2019")

    def test_quote_loss_and_doi_change_reported(self):
        original = {"quotes": [{"normalized": "verified quoted words", "quote": "verified quoted words"}],
                    "doi_links": [{"doi": "10.5555/original"}]}
        candidate = {"quotes": [], "doi_links": [{"doi": "10.5555/replacement"}]}
        out = audit(original, candidate)
        self.assertEqual(len(out["missing_or_modified_quote_occurrences"]), 1)
        self.assertEqual(out["source_dois_not_in_candidate"], ["10.5555/original"])

    def test_nested_html_parsing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.html"
            path.write_text('<p><em>“A quoted passage with at least six words retained verbatim.”</em> '
                            '<a href="https://doi.org/10.1111/TEST">paper</a></p>', encoding="utf-8")
            out = extract(path)
            self.assertEqual(len(out["quotes"]), 1)
            self.assertEqual(out["doi_links"][0]["doi"], "10.1111/test")


if __name__ == "__main__":
    unittest.main()
