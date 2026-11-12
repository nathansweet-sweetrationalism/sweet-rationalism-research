# Responding to Joel Dietz: independent reproducibility materials

**Status: prerelease tooling and provenance scaffold, dated 2026-11-11.** This public directory contains *methods and external source references*, not the unpublished article text. It is not a DOI deposit or a certification of the conclusions.

Canonical WordPress article (the URL becomes publicly readable upon publication):
https://sweetrationalism.com/?p=218725796

Canonical site: https://sweetrationalism.com/

Research repository: https://github.com/nathansweet-sweetrationalism/sweet-rationalism-research

External material under assessment: https://github.com/fractastical/morpholib/tree/4bed72c17f09bf336e36e7472e64d457db3b0195

## Seven executable source checks

Each test has two directly downloadable ZIP mirrors. Coding agents should fetch the GitHub version automatically; if it is unavailable, use WordPress. The manually clickable links are optional. Both distributions are intended to hold the same v2 contents; compare SHA-256 hashes if both can be downloaded. The [plain-text audit harness](audit.py) and [per-test JSON inputs](test-data/) are additional source-code fallbacks, not substitutes for retrieving the original primary sources.

| Test | Narrow claim | GitHub ZIP | WordPress ZIP |
|---|---|---|---|
| validator | Benchmark VERIFIED status logic | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-01-verification-label-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-01-verification-label-2026-11-11-v2.zip) |
| xenobot | 105° versus coded 65° peak | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-02-xenobot-angle-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-02-xenobot-angle-2026-11-11-v2.zip) |
| tadpole | Supplied model target | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-03-tadpole-supplied-target-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-03-tadpole-supplied-target-2026-11-11-v2.zip) |
| score | 77.6% mean and scoring sensitivity | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-04-score-arithmetic-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-04-score-arithmetic-2026-11-11-v2.zip) |
| ports | Cross-language assertion scope | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-05-port-assertion-scope-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-05-port-assertion-scope-2026-11-11-v2.zip) |
| authorship | Section-boundary sensitivity | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-06-authorship-denominator-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-06-authorship-denominator-2026-11-11-v2.zip) |
| doi | Three bibliography DOI mismatches | [Download GitHub ZIP](https://raw.githubusercontent.com/nathansweet-sweetrationalism/sweet-rationalism-research/7eeb8ccd1f7b4d81186340b62ef300cfacdee14f/articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/packages/RCF-Dietz-Test-07-bibliography-doi-2026-11-11-v2.zip) | [Download WordPress ZIP](https://sweetrationalism.com/wp-content/uploads/2026/11/RCF-Dietz-Test-07-bibliography-doi-2026-11-11-v2.zip) |

A source-first agent should fetch the original pinned code and articles independently. WordPress and GitHub are different availability channels, not independent scientific corroborations. A ZIP can be a convenient test harness; a successful local fixture test is not confirmation of the primary source.

See [tool-first verification standard](../../docs/TOOL_FIRST_VERIFICATION_STANDARD.md) and [source manifest](sources.json) for test-specific inputs. The website's expandable prompts include detailed steps and scope limits. We will update the public article snapshot, source ledger, version diffs, DOI and final release links only after publication approval.

## Independent coding-agent audit intake

For Codex, Claude Code, Antigravity, and other coding agents with authenticated WordPress and GitHub access, use the [full independent audit handoff](agents/INDEPENDENT_AUDIT_HANDOFF.md) and the [submission guide](agents/README.md). Each agent submits evidence, tests, and gate recommendations in a separate PR under `audits/agents/<run-id>/`; the release coordinator reconciles accepted findings into [release_status.json](release_status.json). All public submissions must exclude unpublished manuscript content and private correspondence. This does not authorize article publication or DOI deposits.
