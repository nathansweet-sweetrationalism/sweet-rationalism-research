#!/usr/bin/env python3
"""Exhaustive classical propositional inference checker for explicit JSON claims.

Expressions: symbols, True/False, not, and, or, implies(P,Q), iff(P,Q).
No eval, no Python functions, no first-order or modal semantics.
"""
import argparse
import ast
import itertools
import json
import sys
from pathlib import Path


class LogicInputError(ValueError):
    pass


def parse_formula(source):
    if not isinstance(source, str) or not source.strip():
        raise LogicInputError("expected nonempty formula string")
    try:
        node = ast.parse(source, mode="eval").body
    except SyntaxError as exc:
        raise LogicInputError(f"bad formula: {source!r}") from exc

    def atoms(n):
        if isinstance(n, ast.Name) and n.id not in ("implies", "iff"):
            return {n.id}
        if isinstance(n, ast.Constant) and isinstance(n.value, bool):
            return set()
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            return atoms(n.operand)
        if isinstance(n, ast.BoolOp) and isinstance(n.op, (ast.And, ast.Or)):
            return set().union(*(atoms(v) for v in n.values))
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in ("implies", "iff") and len(n.args) == 2
                and not n.keywords):
            return atoms(n.args[0]) | atoms(n.args[1])
        raise LogicInputError(f"unsupported formula: {type(n).__name__}")

    return node, atoms(node)


def evaluate(n, values):
    if isinstance(n, ast.Name):
        return values[n.id]
    if isinstance(n, ast.Constant):
        return n.value
    if isinstance(n, ast.UnaryOp):
        return not evaluate(n.operand, values)
    if isinstance(n, ast.BoolOp):
        terms = [evaluate(v, values) for v in n.values]
        return all(terms) if isinstance(n.op, ast.And) else any(terms)
    if isinstance(n, ast.Call):
        a, b = [evaluate(v, values) for v in n.args]
        return (not a or b) if n.func.id == "implies" else a == b
    raise AssertionError("unvalidated AST")


def check_claim(claim, max_atoms=12):
    if not isinstance(claim, dict) or not isinstance(claim.get("id"), str) or not claim["id"].strip():
        raise LogicInputError("claim requires a nonempty string id")
    premises = claim.get("premises")
    if not isinstance(premises, list) or len(premises) > 100:
        raise LogicInputError(f"{claim['id']}: premises must be a list of at most 100 formulas")
    parsed = [parse_formula(s) for s in [*premises, claim.get("conclusion")]]
    names = sorted(set().union(*(symbols for _, symbols in parsed)))
    if len(names) > max_atoms:
        raise LogicInputError(f"{claim['id']}: {len(names)} atoms exceeds {max_atoms} limit")
    satisfying = 0
    countermodel = None
    premise_witness = None
    for bits in itertools.product((False, True), repeat=len(names)):
        model = dict(zip(names, bits))
        if all(evaluate(node, model) for node, _ in parsed[:-1]):
            satisfying += 1
            if premise_witness is None:
                premise_witness = model
            if countermodel is None and not evaluate(parsed[-1][0], model):
                countermodel = model
    status = ("vacuous_inconsistent_premises" if satisfying == 0
              else "invalid_countermodel" if countermodel is not None
              else "valid_classical_propositional")
    return {"id": claim["id"], "status": status, "atoms": names,
            "worlds_checked": 2 ** len(names), "premise_satisfying_worlds": satisfying,
            "countermodel": countermodel, "premise_witness": premise_witness,
            "source_claim": claim.get("source_claim"),
            "translation_notes": claim.get("translation_notes"),
            "warning": "This checks the supplied encoding only, not premises or translation fidelity."}


def run(payload, max_atoms=12):
    if not isinstance(payload, dict) or not isinstance(payload.get("claims"), list):
        raise LogicInputError("expected JSON object with claims array")
    ids = [c.get("id") if isinstance(c, dict) else None for c in payload["claims"]]
    if len(ids) != len(set(ids)):
        raise LogicInputError("duplicate claim id")
    return {"scope": "Exhaustive classical propositional semantics, not empirical truth",
            "results": [check_claim(c, max_atoms) for c in payload["claims"]]}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--max-atoms", type=int, default=12)
    args = cli.parse_args()
    if not 0 <= args.max_atoms <= 18:
        cli.error("max-atoms must be 0 through 18")
    try:
        print(json.dumps(run(json.loads(args.input.read_text(encoding="utf-8")), args.max_atoms), indent=2))
    except (OSError, json.JSONDecodeError, LogicInputError) as exc:
        print(f"logic audit error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
