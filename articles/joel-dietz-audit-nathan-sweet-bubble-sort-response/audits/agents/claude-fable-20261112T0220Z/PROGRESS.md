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

## Not yet done (in order)
2. Independent second implementations of each decisive calculation, with negative controls.
3. Upstream source reading at the pin and at current HEAD (later fixes).
4. Article mathematical-claim inventory and verification.
5. Bibliography/DOI identity checks; quotation and attribution checks against Dietz's pinned texts.
6. Editorial gate scripts on the private draft (hashes and counts only reported here).
7. `result.json`, `report.md`, validator, pull request.
