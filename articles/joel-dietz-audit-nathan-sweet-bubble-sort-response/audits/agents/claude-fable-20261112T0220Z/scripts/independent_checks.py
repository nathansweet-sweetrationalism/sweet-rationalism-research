#!/usr/bin/env python3
"""Independent second implementation of the seven decisive checks, plus the
article's other arithmetic. Written without reusing the repository audit.py:
it parses upstream Python with `ast` (audit.py uses regex), uses exact
`fractions.Fraction` arithmetic, and adds negative controls.

Never executes upstream code. Python 3.10+ standard library only.
Usage: python independent_checks.py <cache_dir> <out_json>
Sources are fetched once from commit-pinned raw URLs and cached by path.
"""
import ast, csv, hashlib, io, json, math, pathlib, re, sys, urllib.request
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

PIN = "4bed72c17f09bf336e36e7472e64d457db3b0195"
RAW = f"https://raw.githubusercontent.com/fractastical/morpholib/{PIN}/"
FILES = {
    "gen": "docs/media/make_claim_aggregation.py",
    "article": "docs/SUBSTACK_LEVIN_LATENT_SPACE_ARTICLE.md",
    "claims": "docs/SUBSTACK_LEVIN_LATENT_SPACE_CLAIMS.md",
    "errata": "docs/ERRATA_AND_REFEREE_AUDIT_LOG.md",
    "validator": "sorting-morphogenesis/validate_kymograph_and_paper.py",
    "csv": "sorting-morphogenesis/figures/zhang_2025_validation_benchmarks.csv",
    "ports": "sorting-morphogenesis/verify_multilang_ports.py",
    "guide": "sorting-morphogenesis/REPLICATION_AND_PORT_GUIDE.md",
    "renderer": "sorting-morphogenesis/render_13yo_illustrations.py",
    "xeno": "models/2020-kriegman-xenobot-evolutionary-biobots.py",
    "tadpole": "models/2019-bischof-xenopus-craniofacial-remap.py",
}
OUT = {"pin": PIN, "sources": {}, "checks": {}}


def fetch(cache, key):
    p = cache / FILES[key].replace("/", "__")
    if not p.exists():
        req = urllib.request.Request(RAW + FILES[key], headers={"User-Agent": "independent-audit/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            p.write_bytes(r.read())
    b = p.read_bytes()
    OUT["sources"][key] = {"url": RAW + FILES[key], "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return b.decode("utf-8")


def pct(x, places="0.1"):
    x = F(x)
    return str((Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(places), ROUND_HALF_UP))


def check(name, **kw):
    OUT["checks"][name] = kw
    return kw


def mean(xs):
    return sum(xs, F(0)) / len(xs)


def score(S):
    tree = ast.parse(S["gen"])
    tiles = mean_const = None
    computed_mean = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "TILES":
                tiles = ast.literal_eval(node.value)
            if node.targets[0].id == "MEAN":
                mean_const = node.value.value if isinstance(node.value, ast.Constant) else None
                computed_mean = not isinstance(node.value, ast.Constant)
    vals = [F(t[3].rstrip("%")) for t in tiles]
    m = mean(vals)
    loo = [mean(vals[:i] + vals[i + 1:]) for i in range(len(vals))]
    # Does any call in the file aggregate TILES numerically?
    aggregates = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", "")) in ("sum", "mean", "fmean", "average")]
    # Errata arithmetic, transcribed from the pinned errata/article formulas (S16, S17).
    structural7 = mean([F(x) for x in ("100", "40.5", "100", "96.1", "95.0", "95.0", "90.1")])
    four = mean([F(x) for x in ("66.7", "13.5", "86.5", "96.1")])
    structural4 = mean([F(x) for x in ("100", "40.5", "100", "96.1")])
    pillars = mean([F(x) for x in ("55.6", "96.0", "93.3")])
    points = {"7.4/11.1": F("7.4") / F("11.1") * 100, "1.5/11.1": F("1.5") / F("11.1") * 100,
              "9.6/11.1": F("9.6") / F("11.1") * 100, "32.0/33.3": F("32.0") / F("33.3") * 100}
    formulas_present = {
        "structural7_in_article": "(100% + 40.5% + 100% + 96.1% + 95.0% + 95.0% + 90.1%) / 7 = 88.1%" in S["article"],
        "s16_four_claim_in_errata": "(66.7% + 13.5% + 86.5% + 96.1%) / 4 = 65.7%" in S["errata"],
        "s16_pillars_in_errata": "(55.6% + 96.0% + 93.3%) / 3 = 81.6%" in S["errata"],
        "zero_dualist_in_article": "`0.0%` of the dualist points were earned" in S["article"],
    }
    # Hypothetical weight sensitivity on Claim 2 (ours, not the source's method).
    def weighted(w):
        ws = [F(1)] * 7; ws[1] = F(w)
        return sum(a * b for a, b in zip(ws, vals)) / sum(ws)
    weights = {w: pct(weighted(w), "0.01") for w in ("0", "0.5", "1", "2", "3")}
    # Negative control: perturb one score; the hardcoded label must then disagree.
    bad = vals[:]; bad[1] = F("93.5")
    neg = pct(mean(bad)) + "%" != mean_const
    return check("score",
        seven_scores=[str(v) for v in vals], exact_mean=f"{m.numerator}/{m.denominator}",
        mean_decimal=str(Decimal(m.numerator) / Decimal(m.denominator))[:10], mean_rounded_1dp=pct(m),
        hardcoded_MEAN=mean_const, MEAN_is_string_literal=not computed_mean,
        numeric_aggregation_calls_in_generator=len(aggregates),
        rounded_mean_equals_label=pct(m) + "%" == mean_const,
        leave_one_out_min_max=[pct(min(loo), "0.01"), pct(max(loo), "0.01")],
        leave_one_out_all=[pct(x, "0.01") for x in loo],
        structural7_rounded=pct(structural7), four_claim_rounded=pct(four),
        structural4_rounded=pct(structural4), pillars_rounded=pct(pillars),
        point_ratios_rounded={k: pct(v) for k, v in points.items()},
        formulas_present=formulas_present,
        hypothetical_claim2_weight_to_mean=weights,
        negative_control_perturbed_score_detected=neg,
        scope="Arithmetic of displayed labels only. Not a probability of any ontology.")


def validator(S):
    tree = ast.parse(S["validator"])
    status_nodes, conditional = [], 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant)]
            if "status" in keys and "relative_error_pct" in keys:
                v = node.values[keys.index("status")]
                status_nodes.append(v.value if isinstance(v, ast.Constant) else "NON_LITERAL")
        if isinstance(node, (ast.If, ast.IfExp, ast.Compare, ast.Assert)):
            if "relative_error" in ast.unparse(node):
                conditional += 1
    lines = S["validator"].splitlines()
    rows = list(csv.DictReader(io.StringIO(S["csv"])))
    rec = []
    for r in rows:
        pub, rep = F(r["published_value"]), F(r["replicated_value"])
        rec.append({"id": r["benchmark_id"], "csv_err": r["relative_error_pct"], "status": r["status"],
                    "recomputed_from_rounded_values": pct(abs(rep - pub) / pub * 100, "0.01")})
    errs = [F(r["relative_error_pct"]) for r in rows]
    # Counter-control: under hypothetical thresholds, how many rows would fail? (ours, illustrative)
    hyp = {f"{t}%": sum(e > t for e in errs) for t in (1, 5, 10, 25)}
    guide_row = next((l for l in S["guide"].splitlines() if "0.5581" in l), "")
    return check("validator",
        dict_literals_with_status_and_error=len(status_nodes),
        all_status_values_literal_VERIFIED=set(status_nodes) == {"VERIFIED"},
        conditionals_or_asserts_referencing_relative_error=conditional,
        lines_352_353=[lines[351].strip(), lines[352].strip()],
        figure_title_14_of_14_present='"14/14 Published Benchmarks Verified"' in S["validator"],
        pass_literal_count=S["validator"].count("✓ PASS"), fail_literal_count=len(re.findall(r"FAIL|✗", S["validator"])),
        csv_rows=len(rows), csv_all_VERIFIED=all(r["status"] == "VERIFIED" for r in rows),
        csv_max_error=str(max(errs)), csv_rows_detail=rec,
        hypothetical_threshold_fail_counts=hyp,
        synthetic_900pct_control="status expression is a constant; no input value can change it",
        guide_fig7a_row=guide_row.strip(),
        cpp_js_0_5581_vs_published_0_37_pct=pct((F("0.5581") - F("0.37")) / F("0.37") * 100, "0.01"),
        numpy_default_rng_in_validator="np.random.default_rng" in S["validator"],
        splitmix_in_ports="SplitMix64" in S["ports"],
        scope="Verdict logic and saved CSV only. Says nothing about whether the simulations are right.")


def xenobot(S):
    tree = ast.parse(S["xeno"])
    exprs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("eta_sweep", "spill_penalty", "theta_deg", "compacted_cells_curve"):
            exprs.setdefault(node.targets[0].id, ast.unparse(node.value))
    nums = lambda s: [float(x) for x in re.findall(r"(?<![\w.])\d+\.\d+", s)]
    a, b, c, w = nums(exprs["eta_sweep"])            # 6.0 + 12.5*exp(-((t-65)/26)^2)
    cut, c2, w2 = nums(exprs["spill_penalty"])[:3]   # t>85: exp(-((t-85)/38)^2)
    def curve(t, centre=c):
        eta = a + b * math.exp(-(((t - centre) / w) ** 2))
        spill = math.exp(-(((t - c2) / w2) ** 2)) if t > cut else 1.0
        return eta * spill * 3.0 * 4.0
    grid = [i * 120.0 / 24 for i in range(25)]        # np.linspace(0, 120, 25)
    fine = [i / 1000 for i in range(0, 120001)]
    arg_grid, arg_fine = max(grid, key=curve), max(fine, key=curve)
    # Negative control: move the stipulated centre; the "optimum" moves with it up to the spill cut-off.
    ctrl = {str(k): max(fine, key=lambda t: curve(t, k)) for k in (40.0, 65.0, 80.0, 105.0)}
    angle_105_in_model = len(re.findall(r"(?<![\d.])105(?:\.0)?(?![\d.])", S["xeno"]))
    return check("xenobot",
        eta_sweep_expr=exprs["eta_sweep"], spill_penalty_expr=exprs["spill_penalty"], theta_grid_expr=exprs["theta_deg"],
        gaussian_centre_deg=c, argmax_on_code_grid=arg_grid, argmax_fine_grid_0_001=arg_fine,
        value_at_65=round(curve(65.0), 4), value_at_105=round(curve(105.0), 4),
        ratio_65_over_105=round(curve(65.0) / curve(105.0), 3),
        control_centre_to_argmax=ctrl,
        claims_doc_105_deg_mentions=S["claims"].count("105°"),
        claims_doc_both_fluid_sims_sentence="Both of our fluid simulations find the same angle: `105°`" in S["claims"],
        standalone_105_tokens_in_model_file=angle_105_in_model,
        theta_mouth_default_65=bool(re.search(r"theta_mouth_deg:\s*float\s*=\s*65\.0", S["xeno"])),
        stokes_sweep_exists_separately="simulate_stokes_stem_cell_capture" in S["xeno"],
        stokes_sweep_angles=re.search(r"theta_sweep = np\.array\(\[([^\]]+)\]", S["xeno"]).group(1),
        scope="The closed-form AFPO efficiency curve has a stipulated centre. The separate Stokes capture sweep was NOT run here (upstream code is not executed); its sampled angles do not include 105.")


def tadpole(S):
    tree = ast.parse(S["tadpole"])
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "closed_loop_attractor_rhs")
    body = [ast.unparse(s) for s in fn.body if not isinstance(s, ast.Expr)]
    loads = len(re.findall(r'params\["target_nf65_landmarks"\]', S["tadpole"]))
    # Independent reimplementation of the documented RHS (homing + coupling), pure Python, RK4.
    def rhs(X, Xs, K, C, eta):
        d = [[x[0] - s[0], x[1] - s[1]] for x, s in zip(X, Xs)]
        out = []
        for i in range(len(X)):
            v = [-K[i] * d[i][0], -K[i] * d[i][1]]
            for j in range(len(X)):
                v[0] -= C[i][j] * (d[i][0] - d[j][0]); v[1] -= C[i][j] * (d[i][1] - d[j][1])
            out.append([eta * v[0], eta * v[1]])
        return out
    def integrate(X, Xs, K, C, eta=1.0, T=40.0, h=0.01):
        add = lambda A, B, s: [[a[0] + s * b[0], a[1] + s * b[1]] for a, b in zip(A, B)]
        for _ in range(int(T / h)):
            k1 = rhs(X, Xs, K, C, eta); k2 = rhs(add(X, k1, h / 2), Xs, K, C, eta)
            k3 = rhs(add(X, k2, h / 2), Xs, K, C, eta); k4 = rhs(add(X, k3, h), Xs, K, C, eta)
            X = [[x[0] + h / 6 * (a[0] + 2 * b[0] + 2 * c[0] + d[0]), x[1] + h / 6 * (a[1] + 2 * b[1] + 2 * c[1] + d[1])]
                 for x, a, b, c, d in zip(X, k1, k2, k3, k4)]
        return X
    import random
    rng = random.Random(20261112)
    worst = 0.0
    for trial in range(200):  # seeded property test: arbitrary start, arbitrary supplied target
        n = 5
        K = [rng.uniform(0.3, 2.0) for _ in range(n)]
        cval = rng.uniform(0.0, 0.5)
        C = [[0.0 if i == j else cval for j in range(n)] for i in range(n)]
        X0 = [[rng.uniform(-5, 5), rng.uniform(-5, 5)] for _ in range(n)]
        Xs = [[rng.uniform(-9, 9), rng.uniform(-9, 9)] for _ in range(n)]
        XT = integrate(X0, Xs, K, C)
        worst = max(worst, max(abs(a[k] - b[k]) for a, b in zip(XT, Xs) for k in (0, 1)))
    # Control: eta = 0 (the model's "MMP off" switch) must not move toward the target.
    X0 = [[1.0, 1.0]] * 5; Xs = [[4.0, -2.0]] * 5
    frozen = integrate(X0, Xs, [1.0] * 5, [[0.0] * 5] * 5, eta=0.0, T=5.0) == X0
    # audit.py's 1-D illustration, exact: x_n = t + (x0 - t)(1 - h)^n
    ill = {t: round(t + (4.0 - t) * (1 - 0.025) ** 400, 5) for t in (-2.0, 9.0)}
    return check("tadpole",
        rhs_body=body, target_parameter_loads=loads,
        fixed_point_argument="RHS is linear in diff = X - X_star and vanishes at diff = 0; with K_i > 0 and symmetric C >= 0 the matrix K + Laplacian(C) is positive definite, so diff -> 0 for any supplied X_star.",
        property_test_trials=200, property_test_seed=20261112, worst_abs_distance_from_supplied_target_at_T40=worst,
        property_test_passed=worst < 1e-4, eta_zero_control_stays_put=frozen,
        audit_py_illustration_closed_form=ill,
        scope="Shows the reduced model converges to whatever target it is handed. Not a statement about embryos or about where a biological target comes from.")


def ports(S):
    tree = ast.parse(S["ports"])
    asserts = [ast.unparse(n.test) for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    cross = [a for a in asserts if any(k in a for k in ("cpp_data", "js_data", "py_kymo"))]
    compares_python_benchmarks = any("benchmarks" in a and "py" in a for a in cross)
    compares_frames = any(re.search(r"frame|history|kymograph_n42'\]\s*==|trajectory", a) for a in cross)
    row = next((l for l in S["guide"].splitlines() if "0.5581" in l), "")
    cells = [c.strip(" `") for c in row.split("|")][3:]
    return check("ports",
        total_assert_statements=len(asserts), cross_language_asserts=cross,
        python_benchmark_values_asserted_equal=compares_python_benchmarks,
        intermediate_frames_asserted_equal=bool(compares_frames),
        guide_fig7a_cells=cells,
        scope="Only this verifier file and the guide were parsed. Other upstream tests could compare more; see the upstream grep receipt in logs/.")


def authorship(S):
    tree = ast.parse(S["renderer"])
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "render_fig8_ai_vs_human_authorship_heatmap")
    mat = sections = dims = None
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            nm = node.targets[0].id
            if nm == "ai_matrix": mat = ast.literal_eval(node.value.args[0])
            if nm == "sections": sections = ast.literal_eval(node.value)
            if nm == "dims": dims = ast.literal_eval(node.value)
    col = next(i for i, d in enumerate(dims) if "Prose" in d)
    ai = [F(str(r[col])) for r in mat]
    human = 100 - mean(ai)
    split_same = 100 - mean([ai[0]] + ai)            # intro split in two, both halves keep the intro estimate
    # Sensitivity: the result depends on which row is split; report all eight.
    by_row = {sections[i]: pct(100 - mean([ai[i]] + ai), "0.01") for i in range(len(ai))}
    return check("authorship",
        rows=len(mat), cols=len(mat[0]), prose_column_index=col, prose_column_label=dims[col].replace("\n", " "),
        ai_prose_estimates=[str(x) for x in ai],
        human_prose_mean=pct(human, "0.001"), after_duplicating_intro_row=pct(split_same, "0.001"),
        rounded=[pct(human), pct(split_same)],
        split_each_row_in_turn=by_row,
        docstring_says_computed_from_matrix="COMPUTED from `ai_matrix`" in (ast.get_docstring(fn) or ""),
        scope="Arithmetic sensitivity of an unweighted mean of estimates. Assumes both halves of the split row keep the same estimate. Says nothing about real contribution shares.")


def text_claims(S):
    c, a, e = S["claims"], S["article"], S["errata"]
    has = lambda doc, s: s in doc
    return check("source_text",
        p_0_061_in_claims=has(c, "`p = 0.061`"), p_0_061_in_article=has(a, "`p = 0.061`"),
        quantitative_law_of_vertebrate_evolution=has(c, "quantitative law of vertebrate evolution"),
        ablation_4_5x=has(c, "4.5× higher (from 4.90 to 21.95)"), ablation_ratio=pct(F("21.95") / F("4.90"), "0.01"),
        papers_last_decade=has(a, "his lab has produced 400+ papers in the last decade"),
        words_36000=has(a, "36,000 words Nathan Sweet originally sent him"),
        critics_flat_0_50=has(c, "blog critics’ flat `0.50` prediction"),
        bloggers_named=has(c, "Computer-science bloggers, Nathan Sweet among them"),
        reductionist_dismissals=has(a, "reductionist dismissals"),
        exact_phrase_reductionist_blogger_in_pinned_article=("reductionist blogger" in a.lower()),
        exact_phrase_reductionist_blogger_in_pinned_claims=("reductionist blogger" in c.lower()),
        sufficiency_not_falsity=has(a, "Sufficiency of `D` is not falsity of `P`"),
        lower_bound_sentence=has(a, "`0.0%` is a lower bound"),
        zero_cell_mismatches=has(a, "`0` cell mismatches"),
        s16_s17_rows=[bool(re.search(r"\*\*S16\*\*", e)), bool(re.search(r"\*\*S17\*\*", e))],
        scope="Exact-substring presence in the pinned files only.")


def bayes():
    # Bayes-factor identity used in the article: equal likelihoods give BF = 1, provided Pr(E|D) > 0.
    samples = [F(1, 10 ** k) for k in range(0, 12)] + [F(3, 7), F(999, 1000), F(1)]
    ok = all(p / p == 1 for p in samples)
    undefined_at_zero = True
    try:
        F(0) / F(0)
        undefined_at_zero = False
    except ZeroDivisionError:
        pass
    return check("bayes_identity",
        statement="For real p with 0 < p <= 1: if Pr(E|D+P) = Pr(E|D) = p then Pr(E|D+P)/Pr(E|D) = 1.",
        derivation="p/p = 1 for every nonzero element of a field (multiplicative inverse axiom).",
        exact_rational_samples_checked=len(samples), all_equal_one=ok,
        boundary_case_p_zero_is_undefined=undefined_at_zero,
        scope="Algebra only. Whether D and D+P really assign equal likelihood to E is an empirical/modelling premise, not checked here.")


def main():
    cache, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    cache.mkdir(parents=True, exist_ok=True)
    S = {k: fetch(cache, k) for k in FILES}
    for fn in (score, validator, xenobot, tadpole, ports, authorship, text_claims):
        try:
            fn(S)
        except Exception as exc:  # keep going; record the failure rather than hide it
            check(fn.__name__, error=type(exc).__name__ + ": " + str(exc))
    bayes()
    out.write_text(json.dumps(OUT, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: (v.get("error") or "ok") for k, v in OUT["checks"].items()}))


if __name__ == "__main__":
    main()
