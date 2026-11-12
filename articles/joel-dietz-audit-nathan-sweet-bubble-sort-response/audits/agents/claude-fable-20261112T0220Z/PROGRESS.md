# Independent audit, run `claude-fable-20261112T0220Z` (IN PROGRESS)

Agent: Claude Code (desktop), model Claude Fable 5.2 (`claude-fable-5-2`), Anthropic.
Branch: `audit/joel-dietz/claude-fable-20261112T0220Z`. Base commit: `2ee1a4233d37339e27580e59e83af3284f0027d1`.
Upstream pin: `fractastical/morpholib@4bed72c17f09bf336e36e7472e64d457db3b0195`.
WordPress snapshot: post 218725796, status `draft`, modified `2026-11-11T20:31:22` (site local), content SHA-256 `034280325838f1cd563709772311e2de3556f56931b9229538ef944c70c51a98` (312,103 characters). No draft text is in this directory.

This file is the resume point. It is updated and pushed after every stage. If the run stops early, everything listed under "Done" is already committed here; `result.json`, `report.md`, `commands.txt` and `SHA256SUMS.txt` are written last, so their absence means the run did not finish and the submission validator has not been run.

## Done

### Stage 1: package, mirror and CLI checks (all 7 packages)
Script: `scripts/package_check.py`. Receipts: `logs/package_check.json`, `logs/package_check.stdout.txt`, `logs/live/*.json`.

- CONFIRMED: both mirrors (commit-pinned GitHub raw, WordPress uploads) return HTTP 200 for all seven v2 ZIPs; bytes are identical across mirrors and identical to the repo copy at the base commit. ZIP CRCs pass; no unsafe member paths. Each ZIP holds `README.md`, `PROMPT.md`, `test.json`, `audit.py`.
- CONFIRMED: the bundled `audit.py` is the same file in all seven ZIPs and equals the repository `audit.py` after newline normalization; each bundled `test.json` equals `test-data/<id>.json`.
- CONFIRMED: `python audit.py --live` exits 0 with `OBSERVATION_REPRODUCED` for all seven; `--selftest` exits 0 with `SELFTEST_ONLY` (FIXTURE-ONLY, not a replication).
- CONFIRMED: an unreachable source URL gives exit 2 `UNRESOLVED` with no fixture fallback.

### Stage 1 defects found (each reproducible from the receipts)
- F1 (prompt/CLI mismatch, all 14 panels): step 6 of the copyable prompt names an `--offline` flag. `audit.py` has no such flag; the run exits 2 with an argparse "unrecognized arguments" error. The real flag is `--selftest`. The copyable prompt text never mentions `--selftest` (the human-facing "Run:" line outside the textarea does).
- F2 (prompt/package mismatch, all 14 panels): step 3 tells the agent to read `verify.py` before running. No ZIP contains `verify.py`; the verifier is `audit.py`.
- F3 (status vocabulary, all 14 panels): the prompt's ledger statuses are `CONFIRMED | REFUTED | PARTIAL | UNRESOLVED`; `audit.py` prints `OBSERVATION_REPRODUCED | SELFTEST_ONLY | UNRESOLVED | SOURCE_CHANGED_OR_CHECK_FAILED | SELFTEST_FAILED`. Not a contradiction (one is the agent's verdict, the other the script's), but nothing in the prompt maps one to the other.
- F4 (two different prompts): the `PROMPT.md` inside each ZIP is a different, shorter text than the article's copyable prompt, and it and the ZIP `README.md` point to the GitHub ZIP on branch `main`, while the article and `sources.json` use the commit-pinned URL.
- F5 (misleading error label): a missing `--config` file is reported as `UNRESOLVED` "Source retrieval failed" (exit 2), because `FileNotFoundError` is an `OSError`. A local configuration mistake is reported as a network failure.
- F6: the repository's own `agents/inventory_article_code.py` reports 14 structural failures on the current draft ("lacks live or fixture command"), because no prompt contains `python audit.py --selftest`. Same root cause as F1.
- The seven quick/analysis prompt pairs are byte-identical within each pair (7 unique prompts, 14 occurrences).

### Stage 2: independent second implementation (all 7 decisive checks + article arithmetic)
Script: `scripts/independent_checks.py` (AST parsing and exact `fractions.Fraction`; does not reuse `audit.py`; never executes upstream code). Receipt: `logs/independent_checks.json` (includes SHA-256 of every pinned upstream file).

Upstream state: pin `4bed72c` (2026-11-10T13:04:20-08:00); upstream HEAD at audit time `8965854534703a1083974929cb19bd1dc83ef8a2` is one commit later and changes none of the eleven files these tests read, so there is no later upstream correction to report.

- score: CONFIRMED. Seven labels 66.7, 13.5, 86.5, 96.1, 95.0, 95.0, 90.1; exact mean 5429/70 = 77.557..., rounds to 77.6. `MEAN` is a string literal and the generator contains no numeric aggregation call. Leave-one-out range 74.47 to 88.23. Upstream errata formulas reproduce: 88.1 (structural, seven), 65.7 and 84.2 (S16), 81.6 (pillars). Negative control (one score altered) is detected.
- validator: CONFIRMED. 14 dict literals carry both `relative_error_pct` and `status`; all 14 status values are the literal `"VERIFIED"`; zero `if`/comparison/`assert` nodes reference the error. Lines 352-353 match. The file contains `"14/14 Published Benchmarks Verified"`, two `PASS` literals, no `FAIL` literal. CSV: 14 rows, all VERIFIED, maximum saved error 34.11%, second 11.71%. 0.5581 against 0.37 is +50.84%.
- xenobot: CONFIRMED within scope. Closed-form sweep is centred at 65.0; argmax is 65.0 on the code grid and on a 0.001-degree grid; value at 65 is 3.4 times value at 105. The token 105 does not occur in the model file; the companion text says 105 degrees three times. Control: moving the stipulated centre moves the optimum. LIMIT: the separate Stokes capture sweep was not executed; its sampled angles (0, 20, 35, 50, 65, 80, 95, 110, 120) do not include 105.
- tadpole: CONFIRMED within scope. RHS is linear in `X - X_star`; target loaded from `params["target_nf65_landmarks"]` (4 loads). Independent RK4 reimplementation, 200 seeded random targets: converges to whichever target is supplied (worst distance 9.6e-6); eta = 0 control does not move.
- ports: CONFIRMED. Five asserts; four cross-language (three final-array equalities across C++/JS/Python, one C++ vs JS benchmark dictionary). No assert compares Python benchmark values or intermediate frames. Guide table row shows 0.5581 / 0.5581 / 0.496.
- authorship: CONFIRMED. Prose column mean human share 53.125%; duplicating the intro row gives 57.444%. NOTE for the article: the direction depends on which row is split (range 50.33 to 57.44 across the eight rows); the intro is the split that raises it most.
- Bayes identity: p/p = 1 for p > 0 (exact rationals; undefined at p = 0). Algebra only.
- Source-text presence at the pin: `p = 0.061`, "quantitative law of vertebrate evolution", "4.5x higher (from 4.90 to 21.95)", "400+ papers in the last decade", "36,000 words", "blog critics' flat 0.50 prediction", "Computer-science bloggers, Nathan Sweet among them", "reductionist dismissals" are all present.
- F7 (quotation check, needs owner attention): the exact phrase "reductionist blogger" does NOT occur in either pinned Dietz file. If the draft presents it inside quotation marks as Dietz's words, it needs either a verbatim source (for example the live Substack subtitle) or rewording as the author's own characterization. Checked further in stage 3.

## Not yet done (in order)
4. Article mathematical-claim inventory and verification.
5. Bibliography/DOI identity checks; quotation and attribution checks against Dietz's pinned texts.
6. Editorial gate scripts on the private draft (hashes and counts only reported here).
7. `result.json`, `report.md`, validator, pull request.
