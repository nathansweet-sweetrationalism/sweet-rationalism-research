# Addendum, 12 November 2026 (after the original submission)

## 1. The draft changed: owner-approved panel repair applied

After reviewing this report the owner approved the three-substitution panel repair (defects 1 to 3) and an override of a peer agent's lock on the post. It was applied to WordPress draft 218725796 by this agent.

- Before: modified `2026-11-11T20:31:22`, content SHA-256 `034280325838f1cd563709772311e2de3556f56931b9229538ef944c70c51a98`.
- After: modified `2026-11-11T21:54:41` (site local; `2026-11-12T02:54:41` GMT), content SHA-256 `f4d791fda72274f5e310ffcf8c36453cb068153bfa65080f0cbb4aef3de16734`, status still `draft`.
- The stored content is byte-identical to the patched copy tested before the edit (same hash as `after_sha256` in `logs/proposed_prompt_patch.before_after.json`). 42 lines differ from the pre-edit content; line count, title and excerpt are unchanged.
- Readback checks on the live draft: repository `inventory_article_code.py` reports 14 panels and 0 structural failures (was 14); `scripts/panel_checks.py` reports 0 panels with `--offline`, 0 with `verify.py`, 14 naming `--selftest`, 0 with `FIXTURE_CHECK_ONLY`; ZIP URLs, escaping and quick/analysis pair identity unchanged.
- Method: a guarded code snippet on the site (hash and match-count checks before writing), since the in-place replace tool refuses posts over 200 KB. The snippet is deactivated and its result option deleted.

Everything in `result.json` and `report.md` describes the earlier snapshot. Any audit run against SHA `0342...` is stale for the 14 panels only; no prose, number, quotation or link outside the panels changed. The seven prompt hashes in `result.json` are the pre-edit hashes.

Gate effect: with defects 1 to 3 repaired, my recommendation for `navigation` no longer rests on them. Defects 4 to 7, 9 and 10 are unchanged.

## 2. Correction to my own finding: defect 8 (link attributes)

Defect 8 counted attributes in the raw stored HTML. The site rewrites link targets when it serves a page. On an already published article the served HTML has 239 external links, none without `target="_blank"` and 3 without `noreferrer`. So the raw-HTML counts do not show a rule 26 failure on the rendered page. The finding is withdrawn as stated. What remains unverified is the rendered draft itself, which cannot be fetched signed-out, and the 3 internal links that carry `target="_blank"` in the raw HTML.
