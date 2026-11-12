#!/usr/bin/env python3
"""Assemble result.json from the committed receipts in logs/. Stdlib only.
Usage: python build_result.py <run_dir>
Every status below was set by the auditing agent from the named receipt; this script only assembles them.
"""
import json, pathlib, sys
run = pathlib.Path(sys.argv[1])
L = lambda n: json.loads((run / "logs" / n).read_text(encoding="utf-8"))
ind, pk, pan, pub, lnk = L("independent_checks.json"), L("package_check.json"), L("panel_checks.json"), L("public_text_checks.json"), L("link_doi_results.json")
PIN = "4bed72c17f09bf336e36e7472e64d457db3b0195"
C, S = ind["checks"], ind["sources"]
ev = lambda key: {"url": S[key]["url"], "sha256": S[key]["sha256"]}
rc = lambda f: {"file": "logs/" + f}
SANDVE = "Sandve et al. 2013, PLOS Comput Biol, doi:10.1371/journal.pcbi.1003285 (recorded inputs, versions, exact transformations)"
WILSON = "Wilson et al. 2017, PLOS Comput Biol, doi:10.1371/journal.pcbi.1005510 (versioned scripts, raw data kept)"
ASA = "Wasserstein & Lazar 2016, The American Statistician, doi:10.1080/00031305.2016.1154108 (p-value is not a hypothesis probability)"
OT = "Oberkampf & Trucano 2002, Prog Aerosp Sci, doi:10.1016/S0376-0421(02)00005-2 (code verification vs model validation)"
PY = "Python 3.11.9 standard library (fractions, decimal, ast, csv)"

def A(id, gate, scope, status, obs, evidence, lim, loss, controls=None, rivals=None, commands=None):
    d = {"id": id, "release_gate": gate, "scope": scope, "status": status, "observations": obs, "evidence": evidence,
         "limitations": lim, "loss_conditions": loss}
    if controls: d["controls"] = controls
    if rivals: d["rivals"] = rivals
    if commands: d["commands"] = commands
    return d

live_cmd = lambda t: [{"command": f"python audit.py --live   (inside the extracted {t} ZIP; also python audit.py --live --config test-data/{t}.json from the article directory)", "exit_code": 0, "stdout_path": f"logs/live/{t}.live.stdout.json"},
                      {"command": "python scripts/independent_checks.py <cache> logs/independent_checks.json", "exit_code": 0, "stdout_path": "logs/independent_checks.json"}]
assessments = [
 A("T-validator", "executable_live", "Whether the pinned validator's VERIFIED label depends on the computed error; what the saved CSV records.", "CONFIRMED_WITHIN_SCOPE",
   ["AST: 14 dict literals carry relative_error_pct and status; all 14 status values are the constant \"VERIFIED\"; 0 if/compare/assert nodes reference the error.",
    "CSV: 14 rows, all VERIFIED; largest saved error 34.11% (0.37 published, 0.496 replicated), next 11.71%.",
    "File contains the literal title \"14/14 Published Benchmarks Verified\", two PASS literals, no FAIL literal.",
    "Guide table: 0.5581 (C++), 0.5581 (JS), 0.496 (Python) for the same target; 0.5581 is 50.84% above 0.37."],
   [ev("validator"), ev("csv"), ev("guide"), rc("independent_checks.json"), rc("live/validator.live.stdout.json")],
   ["Verdict logic and saved numbers only; nothing here says the simulations are wrong.", "The 900% figure in the article is a synthetic control, not an upstream measurement."],
   ["An acceptance threshold or uncertainty test applied to these rows anywhere in the pinned repository would change the finding.", "A later upstream commit making status conditional (none as of upstream HEAD 8965854)."],
   controls=["Hypothetical thresholds (ours): 1% fails 7 rows, 5% fails 2, 10% fails 2, 25% fails 1.", "A constant expression cannot vary with input, so any synthetic error value keeps VERIFIED."],
   rivals=["The label may be intended as 'benchmark was executed' or 'qualitative trend reproduced'; the code states no such criterion."], commands=live_cmd("validator")),
 A("T-xenobot", "executable_live", "Whether the pinned companion's 105 degree statement matches the pinned model's closed-form efficiency sweep.", "CONFIRMED_WITHIN_SCOPE",
   ["Companion text says 105 degrees three times, including that both fluid simulations find it.",
    "Model: eta_sweep is a Gaussian centred at 65.0; argmax 65.0 on the code grid and on a 0.001 degree grid; value at 65 is 3.4 times value at 105.",
    "The token 105 does not occur in the model file; theta_mouth_deg defaults to 65.0."],
   [ev("claims"), ev("xeno"), rc("independent_checks.json"), rc("live/xenobot.live.stdout.json")],
   ["Upstream code was not executed. The separate Stokes capture sweep was not run; its sampled angles (0,20,35,50,65,80,95,110,120) do not include 105.", "Kriegman et al. 2021 full text was not checked for the angle convention."],
   ["A documented second angle convention mapping 65 to 105 (for example opening versus body arc) in the paper or repository.", "A Stokes sweep result peaking near 105 under an independently specified geometry."],
   controls=["Moving the stipulated centre to 40, 80 moves the optimum to 40, 80; a centre of 105 gives 96.6 because of the spill penalty."],
   rivals=["105 and 65 may be two conventions for one geometry; or the companion text carries a transcription error."], commands=live_cmd("xenobot")),
 A("T-tadpole", "executable_live", "Whether the reduced tadpole model's target is an input, and what convergence then shows.", "CONFIRMED_WITHIN_SCOPE",
   ["closed_loop_attractor_rhs is linear in X - X_star (homing plus pairwise coupling) and vanishes at the target.", "X_star is read from params[\"target_nf65_landmarks\"] (4 loads).",
    "Independent RK4 reimplementation with 200 seeded random targets converges to whichever target is supplied (worst distance 9.6e-6)."],
   [ev("tadpole"), rc("independent_checks.json"), rc("live/tadpole.live.stdout.json")],
   ["A statement about the reduced model only; not about embryos or the origin of a biological target.", "The upstream parameter JSON was not fetched; the property test uses random positive K and nonnegative symmetric C."],
   ["A model variant in which the target is derived from data not supplied as a parameter.", "Negative K or asymmetric C in the canonical parameters (would break the convergence argument)."],
   controls=["eta = 0 (the model's off switch): landmarks do not move."], rivals=["The simulation may be offered only as a conditional illustration, in which case a supplied target is unobjectionable."], commands=live_cmd("tadpole")),
 A("T-score", "executable_live", "Arithmetic and provenance of the 77.6% headline and its sensitivity.", "CONFIRMED_WITHIN_SCOPE",
   ["Seven labels 66.7, 13.5, 86.5, 96.1, 95.0, 95.0, 90.1; exact mean 5429/70 = 77.557..., displayed 77.6.", "MEAN is a string literal; the generator has no numeric aggregation call.",
    "Leave-one-out range 74.47 to 88.23. Errata formulas reproduce 88.1, 65.7, 84.2 and 81.6 exactly as printed."],
   [ev("gen"), ev("errata"), ev("article"), rc("independent_checks.json"), rc("live/score.live.stdout.json")],
   ["Arithmetic of displayed labels. Hardcoding does not show the scores were invented; the errata documents the arithmetic.", "An unweighted mean of unlike judgments is not a probability."],
   ["A pipeline upstream that regenerates the tile labels from per-claim test results."],
   controls=["Altering one score makes the hardcoded label disagree with the recomputed mean (detected).", "Hypothetical Claim 2 weight 0, 0.5, 1, 2, 3 gives 88.23, 82.48, 77.56, 69.55, 63.32."],
   rivals=["Hardcoded labels are normal in figure scripts; the score may be computed elsewhere."], commands=live_cmd("score")),
 A("T-ports", "executable_live", "Which quantities the pinned cross-language verifier asserts equal.", "CONFIRMED_WITHIN_SCOPE",
   ["Five assert statements; four are cross-language: three final-array equalities (C++, JS, Python) and one C++ versus JS benchmark dictionary.", "No assert compares Python benchmark values or intermediate frames.",
    "The Python paper-benchmark routine uses numpy default_rng; the cross-language path uses SplitMix64."],
   [ev("ports"), ev("guide"), rc("independent_checks.json"), rc("live/ports.live.stdout.json")],
   ["Only this verifier and the guide were parsed; a grep of sorting-morphogenesis at the pin found no other frame comparison, but this is not a proof of absence across the whole repository."],
   ["Another upstream test asserting frame-by-frame or Python benchmark parity."], rivals=["Final-state equality may be all the 'bit-exact' claim was meant to cover."], commands=live_cmd("ports")),
 A("T-authorship", "executable_live", "Sensitivity of the mean human-prose estimate to how sections are divided.", "CONFIRMED_WITHIN_SCOPE",
   ["Prose column estimates (% AI) 8, 50, 60, 58, 25, 40, 72, 62; mean human share 53.125%.", "Duplicating the intro row gives 57.444%.",
    "Splitting other rows instead moves the mean the other way or less: range 50.33 to 57.44 across the eight possible splits."],
   [ev("renderer"), rc("independent_checks.json"), rc("live/authorship.live.stdout.json")],
   ["Assumes both halves of a split row keep the same estimate.", "Says nothing about real contribution shares."],
   ["A documented unit (words, time, decisions) and weighting rule for the estimates."], controls=["All eight single-row splits computed."],
   rivals=["The author presents them as estimates, and the figure is computed from its own matrix, as its docstring says."], commands=live_cmd("authorship")),
 A("T-doi", "executable_live", "Whether three DOIs printed in the pinned bibliography identify the cited papers.", "CONFIRMED_WITHIN_SCOPE",
   ["10.1111/evo.12502 resolves to a copepod dominance paper in Evolution; 10.1093/sysbio/syz029 to a Basidiomycota phylogenomics paper; 10.1242/dev.175950 to a DND1 germ-cell paper.",
    "PubMed gives 10.1371/journal.pone.0112732, 10.1098/rspb.2020.1053 and 10.1242/dev.175893 for the cited titles; Crossref metadata for those matches title, journal, volume and authors."],
   [ev("article"), rc("link_doi_results.json"), rc("live/doi.live.stdout.json")],
   ["Identity only. A wrong DOI does not bear on the cited experiments."], ["A corrected upstream bibliography (none at HEAD 8965854)."],
   controls=["Fixture control with all-correct DOIs: per-row matches become true (logs/harness_status_controls.FIXTURE_ONLY.json)."], commands=live_cmd("doi")),
 A("PKG-mirrors", "repro_scaffold", "Identity, integrity and CLI behaviour of the seven v2 ZIPs on both hosts.", "CONFIRMED_WITHIN_SCOPE",
   ["Both mirrors HTTP 200 for all seven; bytes identical across mirrors and to the repository copy; CRC clean; no unsafe paths.", "Bundled audit.py identical in all seven and equal to the repository file after newline normalization; bundled test.json equals test-data/<id>.json.",
    "--live exit 0 OBSERVATION_REPRODUCED x7; --selftest exit 0 SELFTEST_ONLY x7 (fixture only); dead source URL gives exit 2 UNRESOLVED with no fixture fallback."],
   [rc("package_check.json"), rc("package_check.stdout.txt")], ["Two hosts are availability channels, not independent corroboration."], ["Any byte difference between mirrors or a changed ZIP at the pinned commit URL."],
   controls=["--offline, no flag, both flags, missing config, malformed config, dead URL each run for all seven."]),
 A("PROMPT-defects", "navigation", "Whether the 14 copyable prompts and their human instructions match the shipped packages and CLI.", "DISCONFIRMED_WITHIN_SCOPE",
   ["All 14 prompts name a flag --offline that audit.py does not accept (exit 2, argparse error) and never name --selftest.", "All 14 prompts tell the agent to read verify.py; no ZIP contains it.",
    "All 14 human-instruction blocks name a status FIXTURE_CHECK_ONLY; audit.py prints SELFTEST_ONLY.", "The repository's own inventory_article_code.py fails on the current draft with 14 structural failures.",
    "ZIP PROMPT.md is a different, shorter text than the article prompt, and it and README.md link the GitHub ZIP on branch main, not the pinned commit."],
   [rc("panel_checks.json"), rc("package_check.json"), rc("proposed_prompt_patch.before_after.json")],
   ["The live path (--live) is stated correctly everywhere, so an agent following the prompt still gets a real result; the defects affect the fixture path and file-inspection step."],
   ["A package version that ships verify.py and accepts --offline."],
   controls=["Three-substitution private patch: defects 14/14/14 to 0/0/0; inventory script 14 failures to 0; ZIP URLs, escaping and pair identity unchanged."]),
 A("HARNESS-symmetry", "executable_live", "Whether the article's own audit.py computes the outcomes it reports.", "PARTIAL",
   ["validator test: the 'synthetic_900_pct_negative_control' observation is a hardcoded sentence; the regex also counts a conditional `\"status\": \"VERIFIED\" if ...` as a literal assignment.",
    "doi test: status is the same whether DOIs match or not; the per-row matches field carries the result.", "A missing --config file is reported as UNRESOLVED 'Source retrieval failed' (FileNotFoundError is an OSError)."],
   [rc("harness_status_controls.FIXTURE_ONLY.json"), rc("audit_py_patch_before_after.txt"), {"file": "proposed_patches/audit_py_config_error.patch"}],
   ["On the real pinned source the reported conclusions are correct (independent AST check). The weakness is that the harness would not notice an upstream fix."],
   ["Harness revised to derive the control from the parsed status expression."],
   controls=["Fixture with one conditional status and fixture with all-correct DOIs (FIXTURE-ONLY, synthetic)."]),
 A("QUOTE-attribution", "source_ledger", "Verbatim checks of the draft's attributions against the pinned Dietz files, the live Substack page and the author's published article.", "PARTIAL",
   ["Present verbatim at the pin: p = 0.061; 'quantitative law of vertebrate evolution'; '4.5x higher (from 4.90 to 21.95)'; '400+ papers in the last decade'; '36,000 words'; 'blog critics' flat 0.50 prediction'; 'Computer-science bloggers, Nathan Sweet among them'; 'none of this required \"Platonism,\"'; '0.0% is a lower bound'.",
    "Dietz's block quotation opens 'Joel Dietz points...' where the original's subject is the 2025 talk; it ends at 'A repair must buy fresh risk.'; the symmetry paragraph follows immediately in the original and is absent from the pinned article.",
    "The author's three self-quotations are verbatim in his published article.", "Linked biography says over 400 peer-reviewed publications and an independent lab from 2000; the linked automated transcript contains 'physicalism is false'.",
    "NOT verbatim: the phrase 'reductionist blogger' (Substack subtitle says 'reductionist blog critics'; pinned text says 'reductionist dismissals'); the draft headline's quoted score phrase (Dietz writes '77.6++% Overall'; the draft's quoted form orders the symbols differently and adds a word that does not occur in his text).",
    "The draft's self-quotation block shows two passages as consecutive; 487 characters separate them in the original."],
   [rc("public_text_checks.json"), rc("independent_checks.json"), ev("article"), ev("claims")],
   ["Exact-substring checks; they do not judge whether a characterization is fair.", "'Only critic named' was not exhaustively verified.", "Private correspondence (25 October emails) was not examined."],
   ["A Dietz text containing the exact quoted phrases."],
   rivals=["Quotation marks around 'reductionist blogger' may be intended as scare quotes for the author's own compression; a reader cannot tell."]),
 A("BIB-identity", "bibliography", "Identity of the ten DOIs in the draft's reference list.", "CONFIRMED_WITHIN_SCOPE",
   ["All ten resolve in Crossref or DataCite to the cited title, container, volume, pages and author family names; no update or retraction notices returned."],
   [rc("link_doi_results.json")], ["Metadata identity only; no cited passage was read in full text.", "Entries without a DOI (Balaguer SEP, Huh et al. PMLR, Jiang et al. arXiv) were link-status checked only."],
   ["A Crossref record that changes, or a retraction notice."]),
 A("LINK-status", "link_audit", "Signed-out availability and link attributes of the draft's links.", "PARTIAL",
   ["93 unique HTTP links; 83 return 200; the others are publisher 403 bot blocks and the draft's own URL (404 signed-out).", "All 16 in-page anchors resolve.",
    "Raw stored HTML: 84 of 103 external links lack target=_blank and 102 lack noreferrer. CORRECTION (see ADDENDUM.md): the site adds these attributes at render time, so this is not a rule 26 failure on served pages; rendered draft not verified."],
   [rc("link_doi_results.json"), rc("panel_checks.json")], ["Status codes only; destination relevance was not reviewed link by link.", "No sitewide inbound-link inventory was made."], ["Draft links edited."]),
 A("GATE-structural", "bottom_line", "Structural editorial gates run on the private draft.", "PARTIAL",
   ["bottom_line_gate.py passes: Bottom line is the first block, 116 words.", "core_framework_links_gate.py --strict: all four canonical framework URLs present; all four return 200 signed-out."],
   [{"file": "PRIVATE_EVIDENCE_INDEX.md"}], ["Structural only; semantic and source review of the Bottom line remains a human task."], ["Draft edited."]),
 A("MATH-formal", "formal", "Formal and arithmetic content of the draft (see math_inventory).", "PARTIAL",
   ["All 17 inventoried numerical statements reproduce exactly from pinned sources.", "The Bayes-factor sentence is a field identity valid for Pr(E|D) > 0.",
    "No proof assistant or SMT solver was used: no claim exceeds exact rational arithmetic and one field identity."],
   [rc("independent_checks.json")], ["Empirical premises (equal likelihoods, what the experiments show) are not checked by arithmetic.", "The 'smallest formal statement' does not state the Pr(E|D) > 0 condition."],
   ["Any transcription difference between the draft's numbers and the pinned sources."]),
 A("NOT-RUN", "prose", "Categories not executed in this run.", "NOT_RUN",
   ["Upstream Stokes solver not executed; full-text passage checks of peer-reviewed papers not done; browser copy/expand behaviour not tested; evidence-retention audit against a historical snapshot not run; whole-article prose and cohesion review not done; sitewide inbound-link inventory, Yoast head and unlist-plugin state not inspected; WordPress revisions list unavailable (connector timeout)."],
   [], ["These remain open for another agent or the owner."], []),
]

def M(cid, loc, typ, scope, run_result, indep, status, lim, loss, methods=(SANDVE, WILSON)):
    return {"claim_id": cid, "locations": loc, "type": typ, "scope": scope, "tool": PY, "tool_version": "3.11.9",
            "method_sources": list(methods), "run_result": run_result, "independent_check": indep, "status": status,
            "limitations": lim, "loss_conditions": loss}
ic = {"receipt": "logs/independent_checks.json", "second_implementation": "scripts/independent_checks.py (AST and Fraction), compared with audit.py --live output in logs/live/"}
sc, va, xe, ta, au = C["score"], C["validator"], C["xenobot"], C["tadpole"], C["authorship"]
math = [
 M("M01-mean-77.6", ["bottom line", "seven-claims section", "score figure caption", "score panels"], "exact arithmetic", "Mean of seven displayed scores", {"exact": sc["exact_mean"], "rounded": sc["mean_rounded_1dp"]}, ic, "PROVED_DERIVATION", ["Rounded to one decimal."], ["Different source labels."]),
 M("M02-structural-88.1", ["opening paragraph", "score discussion"], "exact arithmetic", "Upstream structural mean (100, 40.5, 100, 96.1, 95, 95, 90.1)/7", {"rounded": sc["structural7_rounded"], "formula_present_at_pin": sc["formulas_present"]["structural7_in_article"]}, ic, "PROVED_DERIVATION", ["Inputs are upstream's own adjusted scores."], ["Formula absent at pin."]),
 M("M03-leave-one-out", ["sensitivity caption"], "exact arithmetic", "Leave-one-out means of the seven scores", {"min_max": sc["leave_one_out_min_max"]}, ic, "PROVED_DERIVATION", ["Draft rounds to 74.5 and 88.2."], ["Different labels."]),
 M("M04-errata-history", ["'++' section"], "exact arithmetic", "81.6 then 65.7 then 77.6 headline history (errata S16, S17)", {"pillars": sc["pillars_rounded"], "four_claim": sc["four_claim_rounded"], "structural4": sc["structural4_rounded"], "present": sc["formulas_present"]}, ic, "PROVED_DERIVATION", ["Order of revisions read from errata rows."], ["Errata text differs."]),
 M("M05-claim2-weight", ["weighting figure caption"], "exact arithmetic", "Hypothetical reweighting of Claim 2 changes the aggregate", {"weight_to_mean": sc["hypothetical_claim2_weight_to_mean"]}, ic, "PROVED_DERIVATION", ["Hypothetical, not the source's method. The draft's figure values were not read from the image."], ["n/a"]),
 M("M06-zero-dualist", ["bottom line", "score discussion"], "source statement", "Upstream reports 0.0% of dualist points earned", {"present_at_pin": sc["formulas_present"]["zero_dualist_in_article"]}, ic, "BOUNDED_TESTS_PASSED", ["A scoring statement by the source, not a measurement."], ["Sentence absent."]),
 M("M07-34.11", ["quick checks", "benchmark section", "CSV figure caption"], "exact arithmetic", "0.370 vs 0.496 recorded as 34.11% error", {"csv_max_error": va["csv_max_error"], "recomputed_from_rounded": [r for r in va["csv_rows_detail"] if r["id"] == "fig7a_bubble_dg_f3"][0]}, ic, "BOUNDED_TESTS_PASSED", ["Recomputing from the rounded CSV values gives 34.05; the CSV's 34.11 comes from the unrounded replicate. The draft quotes the CSV."], ["CSV differs."]),
 M("M08-11.71", ["quick checks", "benchmark section"], "exact arithmetic", "Second benchmark row at 11.71%", {"row": [r for r in va["csv_rows_detail"] if r["csv_err"] == "11.71"][0]}, ic, "BOUNDED_TESTS_PASSED", ["Same rounding note (11.69 from rounded values)."], ["CSV differs."]),
 M("M09-50.8", ["benchmark section"], "exact arithmetic", "0.5581 is about 50.8% above 0.37", {"pct": va["cpp_js_0_5581_vs_published_0_37_pct"]}, ic, "PROVED_DERIVATION", [], ["Guide table differs."]),
 M("M10-14-of-14-unconditional", ["quick checks", "benchmark section", "validator panels"], "algorithm property", "VERIFIED label is independent of computed error", {"literal_statuses": va["dict_literals_with_status_and_error"], "conditionals": va["conditionals_or_asserts_referencing_relative_error"], "lines_352_353": va["lines_352_353"]}, ic, "PROVED_DERIVATION", ["Static AST property of one file at the pin."], ["A conditional elsewhere post-processing the status."], methods=(SANDVE, OT)),
 M("M11-900-control", ["negative control captions"], "algorithm property", "Synthetic 900% input keeps VERIFIED", {"reason": va["synthetic_900pct_control"]}, {"receipt": "logs/independent_checks.json", "note": "Follows from M10; the shipped audit.py does not compute it (see HARNESS-symmetry)."}, "PROVED_DERIVATION", ["Synthetic control, not a measurement."], ["M10 fails."], methods=(OT,)),
 M("M12-xenobot-65-105", ["quick checks", "Claim 7", "xenobot panels"], "numerical model", "Closed-form sweep peaks at stipulated 65; text says 105", {"centre": xe["gaussian_centre_deg"], "argmax_fine": xe["argmax_fine_grid_0_001"], "at_65": xe["value_at_65"], "at_105": xe["value_at_105"]}, ic, "BOUNDED_TESTS_PASSED", ["Stokes solver not run; angle convention unresolved."], ["Second documented convention."], methods=(OT, SANDVE)),
 M("M13-tadpole-target", ["Claim 6", "tadpole figure captions", "tadpole panels"], "numerical solution", "Model converges to whichever target is supplied", {"trials": ta["property_test_trials"], "worst_distance": ta["worst_abs_distance_from_supplied_target_at_T40"], "argument": ta["fixed_point_argument"]}, ic, "BOUNDED_TESTS_PASSED", ["Linear-stability argument stated, not machine-checked; random parameters, RK4 step 0.01, T = 40."], ["Non-positive K or asymmetric C."], methods=(OT,)),
 M("M14-authorship-53.1-57.4", ["authorship paragraph", "authorship panels"], "exact arithmetic", "Row split changes mean human-prose estimate", {"before_after": au["rounded"], "all_splits": au["split_each_row_in_turn"]}, ic, "PROVED_DERIVATION", ["Result depends on which row is split; intro is the maximum."], ["Matrix differs."]),
 M("M15-bayes-factor-1", ["'crucial result' section"], "formal identity", "Equal likelihoods give Bayes factor 1", C["bayes_identity"], {"note": "Exact rational samples plus the field axiom p * p^-1 = 1 for p != 0; no proof assistant used because the statement is a one-line field identity."}, "PROVED_DERIVATION", ["Requires Pr(E|D) > 0, which the draft does not state.", "Whether D and D+P assign equal likelihoods is a modelling premise."], ["P specified so that it assigns a different likelihood."], methods=(ASA,)),
 M("M16-p-0.061", ["Claim 4"], "statistical statement", "Upstream reports p = 0.061 for the nearest-relative comparison", {"present_at_pin": C["source_text"]["p_0_061_in_claims"]}, {"note": "Substring presence only; the underlying test, data and assumptions were not reproduced."}, "EMPIRICAL_BRIDGE_UNVERIFIED", ["p = 0.061 is not below 0.05; 'did better' is a point-estimate statement. Underlying analysis not rerun."], ["Upstream registry record differs."], methods=(ASA,)),
 M("M17-ablation-4.5", ["Claim 1"], "exact arithmetic", "4.90 to 21.95 described as 4.5-fold", {"ratio": C["source_text"]["ablation_ratio"], "present_at_pin": C["source_text"]["ablation_4_5x"]}, ic, "PROVED_DERIVATION", ["21.95/4.90 = 4.48."], ["Numbers differ at pin."]),
]

kinds = {p["panel_id"]: p for p in pan["panels"]}
prompt_checks = []
for pid, p in sorted(kinds.items()):
    t = pk["tests"][p["kind"]]
    prompt_checks.append({"panel_id": pid, "status": "PARTIAL", "source_prompt_sha256": p["prompt_sha256"],
        "primary_zip_url": p["primary_zip_url"], "backup_zip_url": p["backup_zip_url"], "cli_command": "python audit.py --live",
        "run_mode": "PINNED_REMOTE_SOURCES (live) executed once per unique package; quick/analysis prompts are byte-identical",
        "evidence": [{"file": "logs/panel_checks.json"}, {"file": "logs/package_check.json"}, {"file": f"logs/live/{p['kind']}.live.stdout.json"},
                     {"zip_sha256": t["github"]["sha256"], "mirrors_identical": t["mirrors_identical"], "live_exit": 0, "live_status": "OBSERVATION_REPRODUCED"}],
        "limitations": ["Prompt names nonexistent --offline flag and never names --selftest.", "Prompt names verify.py; package ships audit.py.",
                        "Adjacent human instructions name status FIXTURE_CHECK_ONLY; code prints SELFTEST_ONLY.", "Copy/expand behaviour not tested in a browser.",
                        "Prompt was not run end to end inside a second coding agent."],
        "controls": ["--offline exits 2", "no flag exits 2", "dead source URL exits 2 UNRESOLVED", "malformed config exits 1"], "independently_checked": True})

G = lambda id, st, reason, ids: {"id": id, "suggested_state": st, "reason": reason, "assessment_ids": ids}
gates = [
 G("wp_metadata", "partial", "Not re-audited beyond reading the Yoast fields; the headline's quoted score phrase is not verbatim (see QUOTE-attribution).", ["QUOTE-attribution"]),
 G("navigation", "partial", "All 14 panels and 16 anchors are present and intact, but every panel carries three instruction defects; reopen until the three-substitution repair is applied.", ["PROMPT-defects"]),
 G("bibliography", "done", "All ten DOIs match their cited works in Crossref/DataCite. Passage-level support is tracked under source_ledger, not here.", ["BIB-identity"]),
 G("source_ledger", "partial", "Most attributions are verbatim at the pin; two quoted phrases are not verbatim and one self-quotation elides a paragraph. Paper full texts and correspondence were not checked.", ["QUOTE-attribution", "BIB-identity"]),
 G("executable_live", "done", "All seven live checks reproduce, each has an independent second implementation and negative controls. Harness weaknesses are recorded and do not change the seven results.", ["T-validator", "T-xenobot", "T-tadpole", "T-score", "T-ports", "T-authorship", "T-doi", "HARNESS-symmetry"]),
 G("formal", "partial", "Every numerical statement reproduces and the one formal identity holds with a positivity condition the draft omits. Empirical bridges and the p = 0.061 analysis are unverified.", ["MATH-formal"]),
 G("prose", "open", "Not run.", ["NOT-RUN"]),
 G("bottom_line", "partial", "Structural gate passes; semantic and source review is a human task.", ["GATE-structural"]),
 G("framework_links", "partial", "All four canonical URLs present and return 200 signed-out; contextual placement not reviewed.", ["GATE-structural", "LINK-status"]),
 G("link_audit", "partial", "Link status and anchors checked; typed inbound/outbound audit not done.", ["LINK-status"]),
 G("repro_scaffold", "done", "Seven ZIPs byte-identical on both hosts and to the repository, CRC clean, harness identical to repository copy. ZIP README/PROMPT.md point to branch main, a minor inconsistency.", ["PKG-mirrors"]),
 G("history", "partial", "Not examined; the revisions list could not be read (connector timeout).", []),
 G("release_assets", "open", "Not examined.", []),
 G("github_snapshot", "open", "Must stay open until owner-approved publication.", []),
 G("doi", "open", "No article DOI exists; not examined further.", []),
 G("owner", "open", "Owner decision.", []),
 G("publish", "open", "Post is a draft at snapshot and at recheck.", []),
 G("visibility", "open", "Not examined; draft URL returns 404 signed-out, as expected.", ["LINK-status"]),
]
result = {
 "schema": "sweet-rationalism-agent-audit/v1", "run_id": run.name,
 "agent": {"tool": "Claude Code (desktop app, Agent SDK)", "model": "Claude Fable 5.2 (claude-fable-5-2), Anthropic", "runtime": "Windows 11, Python 3.11.9, git; no proof assistant, SMT solver or CAS installed or used"},
 "snapshot": {"wordpress_post_id": 218725796, "wordpress_status": "draft", "wordpress_modified": "2026-11-11T20:31:22", "wordpress_modified_gmt": "2026-11-12T01:31:22",
              "wordpress_content_sha256": pan["article_sha256"], "wordpress_content_characters": 312103, "rechecked_unchanged_before_submission": True,
              "github_base_commit": "2ee1a4233d37339e27580e59e83af3284f0027d1", "upstream_commit": PIN,
              "upstream_head_at_audit": "8965854534703a1083974929cb19bd1dc83ef8a2", "upstream_tested_files_changed_since_pin": 0, "package_commit": "7eeb8ccd1f7b4d81186340b62ef300cfacdee14f"},
 "assessments": assessments, "gate_recommendations": gates,
 "open_items": [
  "Apply the three-substitution prompt repair to all 14 panels (owner; private diff prepared).",
  "Replace or unquote the two non-verbatim quoted phrases so quoted words match Dietz's ('reductionist blog critics'; '77.6++% Overall').",
  "Mark the elision in the D-versus-D+P self-quotation block.", "State Pr(E|D) > 0 in the Bayes-factor sentence.",
  "Consider noting that the authorship split direction depends on the row chosen (range 50.3 to 57.4).",
  "Make audit.py compute its validator control and distinguish conditional from literal status; apply proposed config-error patch.",
  "Align ZIP README/PROMPT.md with the commit-pinned URL and the article prompt, or state that they differ (requires new ZIPs and hashes).",
  "Verify link attributes on the rendered draft (raw-HTML finding withdrawn; see ADDENDUM.md).", "ADDENDUM: draft changed after snapshot by owner-approved panel repair; new content SHA-256 f4d791fda72274f5e310ffcf8c36453cb068153bfa65080f0cbb4aef3de16734.",
  "UNRESOLVED: xenobot angle convention (65 vs 105); Stokes sweep not executed.",
  "NOT_RUN: full-text passage support in Zhang et al., Kriegman et al., Pinet et al., Huh et al., Jiang et al.; the p = 0.061 analysis; browser copy/expand; prose, cohesion and evidence-retention gates; inbound-link inventory; Yoast head and unlist-plugin state; WordPress revisions; private correspondence."],
 "privacy": {"reviewed_public_safe": True, "unpublished_manuscript_excluded": True, "reviewed_by": "Claude Fable 5.2 (agent self-review; owner review still required)",
             "note": "Public files contain hashes, counts, public-source quotations and short phrase-level findings only. The draft, extracted prompts, patched HTML and diff are held locally."},
 "prompt_checks": prompt_checks, "math_inventory": math,
 "coverage": {"panel_ids_enumerated": 14, "unique_packages_enumerated": 7, "math_claims_count": len(math),
  "article_commands_enumerated": ["python audit.py --live", "py -3 audit.py --live", "python audit.py --selftest", "python audit.py --offline (named in prompts; does not exist)", "python audit.py --live --config test-data/<id>.json (repository form)"],
  "script_inventory": ["audit.py (repository and seven bundled copies, identical)", "test-data/*.json x7 and bundled test.json x7 (identical)", "agents/inventory_article_code.py", "agents/validate_submission.py",
                       "scripts/bottom_line_gate.py", "scripts/core_framework_links_gate.py", "scripts/prose_audit.py (ran; output not analysed)", "scripts/evidence_retention_audit.py (NOT_RUN)", "scripts/logic_audit.py (NOT_RUN: no propositional ledger built)",
                       "upstream, read not executed: make_claim_aggregation.py, validate_kymograph_and_paper.py, verify_multilang_ports.py, render_13yo_illustrations.py, 2020-kriegman-xenobot-evolutionary-biobots.py, 2019-bischof-xenopus-craniofacial-remap.py"],
  "public_safety_review": True, "math_sections_summary": "17 distinct claims inventoried: 11 derived exactly, 5 bounded tests passed, 1 empirical bridge unverified, 0 refuted."},
}
(run / "result.json").write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print("assessments", len(assessments), "math", len(math), "prompts", len(prompt_checks), "gates", len(gates))
