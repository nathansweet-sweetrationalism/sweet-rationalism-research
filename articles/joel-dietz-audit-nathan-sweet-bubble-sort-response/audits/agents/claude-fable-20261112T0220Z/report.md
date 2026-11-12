# Independent audit report: `claude-fable-20261112T0220Z`

Agent: Claude Code (desktop) running Claude Fable 5.2 (`claude-fable-5-2`, Anthropic). One session, 12 November 2026 UTC.
Target: WordPress post 218725796, status `draft`, modified `2026-11-11T20:31:22`, content SHA-256 `034280325838f1cd563709772311e2de3556f56931b9229538ef944c70c51a98`. Rechecked unchanged before submission.
Base commit `2ee1a42`; upstream pin `fractastical/morpholib@4bed72c`; upstream HEAD at audit `8965854` (one commit later, none of the tested files changed).

**Read `ADDENDUM.md` first: the draft changed after this report (owner-approved panel repair) and defect 8 is withdrawn.**

This is evidence for the release coordinator. It does not close any gate and does not authorize publication. No draft text is in this directory. WordPress was read only.

## What held up

1. **All seven executable checks reproduce from live pinned sources**, and each was confirmed by a second implementation written for this audit (`scripts/independent_checks.py`: AST parsing and exact fractions, where the article harness uses regular expressions and floats).
   - Validator: 14 status values, all the constant `"VERIFIED"`, no conditional on the error anywhere in the file. Saved CSV rows include 34.11% and 11.71% error, both VERIFIED.
   - Score: mean of the seven labels is exactly 5429/70 = 77.557, shown as 77.6; the label is a string literal. Leave-one-out range 74.47 to 88.23. Upstream errata arithmetic (88.1, 65.7, 84.2, 81.6) reproduces.
   - Xenobot: the closed-form sweep is centred at 65.0 and peaks there; the companion text says 105 degrees; the number 105 is not in the model file.
   - Tadpole: the model converges to whichever target it is handed (200 seeded random targets).
   - Ports: four cross-language assertions (three final arrays, one C++ vs JS benchmark dictionary); none covers intermediate frames or Python benchmark values.
   - Authorship: 53.125% becomes 57.444% when the intro row is duplicated.
   - DOIs: the three DOIs printed upstream resolve to unrelated papers; PubMed and Crossref give the correct ones.
2. **Packages**: the seven ZIPs are byte-identical on GitHub, WordPress and in the repository; CRCs pass; the bundled harness equals the repository harness.
3. **Bibliography**: all ten DOIs in the draft reference list match their cited works in Crossref/DataCite.
4. **Attribution**: the phrases the draft attributes to Dietz that I could test are present verbatim at the pin (list in `result.json`, assessment `QUOTE-attribution`). The block quotation of the author in the pinned Dietz article does alter its opening subject, and it stops immediately before the symmetry paragraph. The author's self-quotations are verbatim in his published article. The linked biography and transcript say what the draft says they say.
5. **Arithmetic**: 17 distinct numerical or formal statements inventoried; none refuted.

## Confirmed defects, in priority order

| # | Defect | Evidence | Proposed minimal repair | Before / after |
|---|---|---|---|---|
| 1 | All 14 copyable prompts name a flag `--offline` that the verifier rejects (exit 2), and never name the real `--selftest`. | `logs/panel_checks.json`, `logs/package_check.json` | Replace the quoted flag with `python audit.py --selftest`. | 14 to 0; repository `inventory_article_code.py` goes from 14 structural failures (exit 1) to 0 (exit 0). |
| 2 | All 14 prompts tell the agent to read `verify.py`; no ZIP contains it. | same | `verify.py` to `audit.py`. | 14 to 0 |
| 3 | The human instructions beside all 14 panels name a status `FIXTURE_CHECK_ONLY`; the code prints `SELFTEST_ONLY`. | same | Use `SELFTEST_ONLY`. | 14 to 0 |
| 4 | Two phrases the draft presents in quotation marks as Dietz's wording are not verbatim. His subtitle says "reductionist blog critics" and his headline says "77.6++% Overall". | `logs/public_text_checks.json` | Quote his exact words, or drop the quotation marks and present the phrase as the author's characterization. | Owner's wording decision; no patch drafted. |
| 5 | The harness validator "negative control" line is a hardcoded sentence, and its regex counts a conditional status as a literal one. It would not notice an upstream fix. | `logs/harness_status_controls.FIXTURE_ONLY.json` | Derive the control from the parsed status expression (the AST approach in `scripts/independent_checks.py`). | Not patched; described only. |
| 6 | A missing `--config` file is reported as `UNRESOLVED` "Source retrieval failed". | `logs/audit_py_patch_before_after.txt` | `proposed_patches/audit_py_config_error.patch` | `UNRESOLVED`/exit 2 becomes `NOT_RUN`/exit 1 with a configuration message; seven live outputs hash-identical before and after; seven selftests pass. |
| 7 | The `PROMPT.md` inside each ZIP differs from the article prompt, and it and the ZIP `README.md` link the GitHub ZIP on branch `main`, not the pinned commit. | `logs/package_check.json` | Rebuild ZIPs with the pinned URL, or say in the article that the bundled prompt is a short form. Needs new hashes. | Not patched. |
| 8 | Link attributes: 84 of 103 external links lack `target="_blank"`, 102 lack `noreferrer`, 3 of 47 internal links open a new tab (AGENTS.md rule 26). | `logs/link_doi_results.json`, private link list | WITHDRAWN as stated: the site adds these attributes when serving pages. See `ADDENDUM.md`. | n/a |
| 9 | The self-quotation block shows two passages as consecutive; 487 characters separate them in the original. | `logs/public_text_checks.json` | Add an ellipsis. | Not patched. |
| 10 | The Bayes-factor sentence omits the condition Pr(E\|D) > 0. | `logs/independent_checks.json` | Add "with nonzero likelihood". | Not patched. |

Defects 1 to 3 are fixed together by three string substitutions (42 lines, +154 characters, line count unchanged). The patched HTML and diff are held privately for the owner; ZIP URLs, escaping and quick/analysis pair identity are unchanged by the patch.

Defect 5 matters for symmetry: the draft faults an unconditional verdict upstream, and its own harness prints one unconditional line. The upstream finding itself stands on the independent AST check.

## Rival readings worth keeping

- Validator: "VERIFIED" may be meant as "benchmark executed" or "trend reproduced". No such criterion is in the code.
- Xenobot: 65 and 105 may be two angle conventions. Not resolved here. The separate Stokes sweep was not executed, and its sampled angles do not include 105.
- Score: hardcoded figure labels are ordinary; the errata documents the arithmetic.
- Authorship: the split direction depends on the row chosen. The intro split is the largest increase (57.44); other rows give 50.33 to 55.56. The draft says the recalculation is illustrative, and a range would be more complete.
- The two-word characterization in defect 4 may be intended as scare quotes; a reader cannot tell.

## Not run or unresolved

Upstream Stokes solver; full-text passage support in the cited papers; the analysis behind p = 0.061; browser copy/expand behaviour; a full end-to-end run of a prompt in a second agent; prose, cohesion and evidence-retention gates; inbound-link inventory; Yoast head and unlist-plugin state; WordPress revision history (connector timed out); private correspondence. No proof assistant, SMT solver or computer algebra system was used, because no claim in the draft goes beyond exact rational arithmetic and one field identity.

## Gate recommendations (all 18)

| Gate | Suggest | Why |
|---|---|---|
| wp_metadata | partial | The quoted score phrase in the headline is not verbatim. |
| navigation | partial | Panels intact, but three instruction defects in each. |
| bibliography | done | Ten DOIs match. |
| source_ledger | partial | Two non-verbatim quoted phrases; paper full texts unchecked. |
| executable_live | done | Seven live checks, seven independent reimplementations, controls. |
| formal | partial | Arithmetic exact; empirical bridges unverified. |
| prose | open | Not run. |
| bottom_line | partial | Structural pass only. |
| framework_links | partial | Present and live; placement not reviewed. |
| link_audit | partial | Status and anchors checked; rule 26 not met. |
| repro_scaffold | done | Mirrors identical and intact. |
| history | partial | Not examined. |
| release_assets, github_snapshot, doi, owner, publish, visibility | open | Owner or post-release steps. |

## Submission validator

`agents/validate_submission.py` passes on this directory under Linux (Python 3.12.3 in WSL, the same platform as CI): 16 assessments, 18 gates, 38 hashed files, 14 panels, 17 math claims. On Windows the same script rejects any submission that has files in subdirectories, because it compares `str(path.relative_to(folder))` (backslashes) with the forward-slash paths in `SHA256SUMS.txt`. Suggested fix for the coordinator: use `.as_posix()` on that line. Not patched here because the script is shared.

## Check on my own work

My first patch to `package_check.py` was malformed and was pushed in a broken state for one commit (`70fc9b7`); it was repaired in the next commit and the receipts were regenerated in the one after. A first version of the Fig. 7A row lookup in `independent_checks.py` picked the wrong table row and was corrected before the stage 2 commit. Statuses in `result.json` were set by the agent from the receipts; `build_result.py` only assembles them.
