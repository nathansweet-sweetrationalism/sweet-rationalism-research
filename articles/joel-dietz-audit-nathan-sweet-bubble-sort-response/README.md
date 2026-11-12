# Responding to Joel Dietz: independent reproducibility materials

**Status: published 2026-11-12.** The article is public, and its archived release is deposited on Zenodo (DOIs below). This directory holds the reproducibility materials, source references, audit evidence and release files for it. It is a record of narrow code, arithmetic and source checks, not a certification of any biological or metaphysical conclusion. Agreement among AI audits is not independent replication.

Canonical WordPress article:
https://sweetrationalism.com/articles/epistemology/joel-dietz-audit-nathan-sweet-bubble-sort-response/

Canonical site: https://sweetrationalism.com/

Research repository: https://github.com/nathansweet-sweetrationalism/sweet-rationalism-research

External material under assessment: https://github.com/fractastical/morpholib/tree/4bed72c17f09bf336e36e7472e64d457db3b0195

## Cite and versions

Cite as: Sweet, N. (2026). *Responding to Joel Dietz (MIT)’s “77.6++%” Defense of Michael Levin’s Biological Causal Platonism and His Demonstrable Misrepresentations of My Actual Argument* [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.24151128. The Zenodo archive is licensed CC BY 4.0.

- This version (DOI): https://doi.org/10.5281/zenodo.24151128
- All versions (concept DOI): https://doi.org/10.5281/zenodo.24151127
- Zenodo record: https://zenodo.org/records/24151128
- Article: https://sweetrationalism.com/articles/epistemology/joel-dietz-audit-nathan-sweet-bubble-sort-response/
- Release files in this directory: [`release/`](release/) (main archive, revision-history archive, audit text, `SHA256SUMS.txt`); the Zenodo copies have identical MD5s
- [Changelog](CHANGELOG.md) and [release status](release_status.json)
- Machine-readable citation: [`CITATION.cff`](CITATION.cff)


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
