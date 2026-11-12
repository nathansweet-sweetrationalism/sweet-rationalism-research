# Adversarial review of independent agent evidence (2026-11-12 UTC)

**Subject:** WordPress draft 218725796 and the pinned `fractastical/morpholib` edition at `4bed72c17f09bf336e36e7472e64d457db3b0195`.
**Scope:** independent computational audit intake and selective correction; **not** a completed peer review, Zenodo deposit or authorization to publish.
**Privacy:** this record contains public-source findings and non-reconstructive references only. Private draft snapshots and exact textual redlines stay outside public GitHub.

## Intake and dispositions

| Source | Where to review | Decision | Reason and retained limitations |
|---|---|---|---|
| Claude Fable 5.2 | [PR #1](https://github.com/nathansweet-sweetrationalism/sweet-rationalism-research/pull/1), `audits/agents/claude-fable-20261112T0220Z/` | **Merged as scoped research evidence** | CI succeeded; seven narrow live-source checks, second implementations, negative controls, DOI checks, 14-panel inventory and explicit limitations. The agent withdrew its raw-HTML external-link attribute claim; post-submission panel repairs are documented in ADDENDUM.md. Reproducibility is narrower than biological experimental replication. |
| Codex | [audit branch](https://github.com/nathansweet-sweetrationalism/sweet-rationalism-research/tree/audit/joel-dietz/codex-20261112T0045Z-a418d1) | **Retain as independent candidate corroboration; no completed PR** | Independently calculates rational score and section-sensitivity examples, model sweep, ODE convergence and negative controls; Z3 countermodel and sorting-metric dissociation. Branch still labels itself IN PROGRESS and lacks final submission result.json, full 18-gate report, SHA256SUMS and validated PR. Do not mark it a finished agent review. |
| Gemini 4 Argon / Antigravity | [audit branch](https://github.com/nathansweet-sweetrationalism/sweet-rationalism-research/tree/audit/joel-dietz/antigravity-20261112-024500) | **Selectively accepted observations; broader certifications rejected** | Overlapping source observations are useful, but the report contains specific arithmetic/source errors, claim-status overpromotions, and inadequate independent model reproduction. Windows checksum path correction was accepted independently as a minimal one-line improvement; the full branch was not merged. |

## Findings retained after checking against source code and competing agent methods

1. Pinned upstream benchmark data have 14 `VERIFIED` statuses with saved relative-error values up to 34.11% and 11.71%; the upstream Python dictionary assignments are unconditional. This is a code-and-saved-data observation, not by itself evidence that all simulations failed.
2. The seven displayed percentages average exactly `5429/70 = 77.557142857...`, displayed as 77.6%. The generator embeds the score and mean as display strings; the mere use of fixed display literals is not an accusation of fabricated inputs or proof of Platonism.
3. The pinned Xenobot closed-form mouth-angle sweep is `np.linspace(0.0,120.0,25)` and its efficiency curve is stipulated to peak near 65°. The separate narrative cites 105°. Different angle conventions or separate solvers remain possible; the separate Stokes solver and real biological inference are not settled by this narrow comparison.
4. The reduced tadpole model receives `target_nf65_landmarks` as a parameter. Conditional convergence toward that input does not independently establish the source of biological goals.
5. Cross-language checks compare selected end-state arrays and a C++/JavaScript benchmark dictionary. They are not a complete assertion-by-assertion audit of all intermediary kymograph frames or Python benchmarks.
6. The authorship-section arithmetic supports one hypothetical change from 53.125% to 57.444...% when the introductory row is duplicated. **Sensitivity direction depends on the row chosen**; these values are author-supplied estimates, not measured causal contributions.
7. Three upstream bibliography DOI mismatches are supported by pinned text and primary metadata. This affects citation identity, not the validity of the underlying biological papers.

## Unsupported or incorrect claims withheld

- Antigravity reports that the Xenobot sweep has **maximum grid angle 65°**. The pinned source explicitly defines a grid **0°–120°**; **65° is the fitted efficiency peak**, not the maximum sampled angle. Its grid-maximum claim is rejected.
- Antigravity reports the split-introduction authorship mean **56.1667%**. The pinned eight-row data, the article's stated split convention and independent exact arithmetic give **517/9 = 57.444...%**. Its number is rejected.
- Antigravity lists four `/foundations/...` URLs as canonical foundation links. The actual required canonical URLs are under `/frameworks/` as specified in `docs/ARTICLE_QUALITY_GATES.md`. The purported `/foundations/` verification is rejected.
- A reported `p = 0.061` not passing a conventional `0.05` threshold **does not prove the absence of a general biological law**, nor verify the paper's underlying experimental design, sampling or effect size. Treat the primary result as incompletely audited.
- Antigravity's "all ten mathematical claims proved" certification is rejected where the script merely assigns numbers and boolean values rather than extracting and testing the corresponding primary source or formal premises. No proof assistant or actual full-text statistical analysis was established.
- The original v2 article harness has a real **self-audit defect**: its 900% "negative control" observation is a hardcoded statement and its regex can count a conditional status assignment (or comment-only text) as a literal one. Independent AST checks support the real pinned-source result, but the original harness alone cannot earn that verdict. Carry this limitation into the next version and combined audit ZIP.

## Narrow changes made or already incorporated in protected WordPress

- The article's italic reader deck now precedes its Bottom line; the structural checker was revised to accept **one complete italic deck** without allowing unrelated substantive preamble. Negative controls cover missing Bottom line, extraneous prose and non-italic preamble.
- Copyable instructions were corrected from nonexistent `verify.py` and `--offline` to `audit.py` and `--selftest`; the displayed fixture status now matches `SELFTEST_ONLY`. Agent addendum documents the change and its hashes.
- The original headline notation `77.6++%` and exact `reductionist blog critics` phrase now have faithful attribution where quoted. The article marks a self-quotation omission and states the Bayes-factor denominator must be positive. Authorship sensitivity no longer suggests its direction is universal.
- The public submission validator compares checksum paths using portable POSIX normalized relative paths.

## Still required before a new article DOI or public release

**Hard unresolved:** full-text source-passage and revision/retraction audit of each bearing scholarly study, independent assessment of the `p=0.061` claim and its comparator, complete section-by-section and cross-article editorial review, exact dialogue quotation retention/privacy, sitewide eligible inbound-link matrix, signed-out Yoast/unlisting/canonical checks, fixed and versioned v2/v3 harness distinction, executable combined audit ZIP with matching hashes, final article capture and metadata, and exact-candidate owner signoff.

**Release protocol:** WordPress remains canonical. No public manuscript copy, tag/release, Zenodo deposit or DOI assignment is authorized by this evidence intake. Agent agreement is not counted as independent empirical replication when it shares the same pinned code, data, or test implementation. Every accepted result needs a source version, script, controls, loss condition, and limitation.

**Reconsideration conditions:** Correct upstream models or metadata, a checked angle-coordinate transformation, genuinely matched biological comparisons, new independent experiments, verified contrary paper passages, or a failed reproduction of the above exact source claims should revise this record rather than being treated as disloyalty or ignored.
