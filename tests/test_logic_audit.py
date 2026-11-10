import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("logic_audit", Path(__file__).resolve().parents[1] / "scripts/logic_audit.py")
logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic)


class LogicAuditTests(unittest.TestCase):
    def test_modus_ponens(self):
        result = logic.check_claim({"id": "mp", "premises": ["P", "implies(P,Q)"], "conclusion": "Q"})
        self.assertEqual(result["status"], "valid_classical_propositional")

    def test_affirming_consequent_countermodel(self):
        result = logic.check_claim({"id": "ac", "premises": ["implies(P,Q)", "Q"], "conclusion": "P"})
        self.assertEqual(result["status"], "invalid_countermodel")
        self.assertEqual(result["countermodel"], {"P": False, "Q": True})

    def test_inconsistent_premises(self):
        result = logic.check_claim({"id": "boom", "premises": ["P", "not P"], "conclusion": "Q"})
        self.assertEqual(result["status"], "vacuous_inconsistent_premises")

    def test_tautology(self):
        self.assertEqual(logic.check_claim({"id": "t", "premises": [], "conclusion": "P or not P"})["status"], "valid_classical_propositional")

    def test_disallow_python_code(self):
        for f in ("__import__('os').system('echo no')", "P == Q", "P[0]", "P+Q"):
            with self.subTest(f=f), self.assertRaises(logic.LogicInputError):
                logic.parse_formula(f)

    def test_duplicate_ids(self):
        with self.assertRaises(logic.LogicInputError):
            logic.run({"claims": [{"id": "a", "premises": [], "conclusion": "True"}] * 2})


if __name__ == "__main__":
    unittest.main()
