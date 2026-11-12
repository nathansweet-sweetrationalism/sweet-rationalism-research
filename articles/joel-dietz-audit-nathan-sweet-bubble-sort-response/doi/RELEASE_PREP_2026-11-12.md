# Article-specific Zenodo DOI release preparation

**Status:** PREPARATION ONLY; no DOI reserved or registered, and no public manuscript deposit.
**Article:** WordPress post `218725796`, slug `joel-dietz-audit-nathan-sweet-bubble-sort-response`.
**Source sign-off:** On 2026-11-11 America/Detroit, Nathan Sweet reported completing all primary-source verifications personally and authorized proceeding to the DOI stage. This is author attestation, not an assertion of independent replication.

## Candidate freeze reference
- WordPress status at readback: `draft`.
- WordPress `post.modified`: `2026-11-11T22:21:52` (local WordPress time).
- Raw Gutenberg body SHA-256 (UTF-8 bytes): `6150cd11254be6ac5bc41df70305e169fb5cb489aa9d3759e9c5cb97f079e807`.
- Raw body length: 312,603 UTF-16 code units. This is **not** a word count.
- This fingerprint describes the readback only; the exact release snapshot MUST be reread, rehashed, and compared against the immutable deposit before publishing.
- Current draft readback contains 14 computational instruction panels. Static text scan: 0 references to unsupported `--offline`, 0 to nonexistent `verify.py`; `--selftest` and `SELFTEST_ONLY` are present. These counts do not certify runtime reproducibility.

## Depositing policy
- Create a **separate manual Zenodo upload** for this article, not a DOI for the entire multipaper GitHub repository. Reserve its article-specific DOI in an unpublished draft if account access permits.
- The reserved DOI is not registered or resolvable until Zenodo publication. Zenodo normally registers the version-specific and concept DOIs at first publication. Record both actual identifiers after publication; do not invent them.
- Do not publish the Zenodo deposit before the final exact candidate, public artifacts and owner publication approval are checked.
- The browser-assisted DOI workflow on 2026-11-11 encountered the Zenodo login screen, so no account-specific deposit inspection or DOI reservation was possible.
- Suggested record type: **Publication / Other** or the closest appropriate **Journal article / Report** subtype available in the live Zenodo UI. Accurately describe this as an independent scholarly article, not externally peer-reviewed or a journal publication.
- Author: **Nathan Sweet**. Verify preferred author display name/ORCID, access, license and release date with the owner or existing authoritative profile before committing deposit metadata.
- Use the published WordPress article URL as related identifier (when public); link the exact article-specific GitHub research directory, not the repository-level DOI.
- No third-party copyrighted PDF collection or nonredistributable source text should be bundled. Link and cite primary sources instead.

## Required frozen release objects
1. Exact final published `article.html` (same body as WP readback) and `metadata.json` with permalink, title, author, version, publication date and actual DOI fields.
2. Public UTF-8 revision/audit TXT, precise historical diff and complete reconstruction ZIP, preserving copyright and permissions.
3. Accepted independent agent audits with distinct provenance (source branch, commit, checker/tool versions, method, raw execution logs, inputs and hashes). Distinguish independent from duplicated inputs.
4. Seven reproducible source-check packages, 14 public instruction-panel receipts, their test data and SHA-256 manifest; distinguish fixture-only and live-source results.
5. File inventory and `SHA256SUMS.txt` for *every* object in the immutable Zenodo deposit; check ZIP integrity and extraction.
6. Human-reviewed citation, mathematics, logic, code, link, accessibility and public-visibility receipts; list residual limits honestly.
7. Published version notes and cross-links among WordPress, GitHub, Zenodo specific-version DOI and concept DOI after the latter become real.

## Remaining release gates
The source ledger is closed by the author's sign-off; independent computation, formal proof duties, final prose, history, release assets, immutable GitHub snapshot, owner approval, publish and visibility remain distinct and cannot be inferred from source attestation. See `../release_status.json` for live state. Do not merge unchecked agent findings or relabel an unexecuted test as reproduced.

## Publication-order invariant
`owner approves exact candidate → freeze/hash → publish canonical WP article and verify → commit exact public HTML and archives → complete article-specific Zenodo deposit with matching files → publish Zenodo record → read back real DOIs → backlink both identifiers and verify public links`.

If DOI needs to appear in the immutable files, reserve it first in the Zenodo **draft** and then prepare the matching frozen files; only call it *reserved* until registered.
