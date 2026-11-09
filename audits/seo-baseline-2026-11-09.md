# Sweet Rationalism SEO Baseline — 2026-11-09

Source: authenticated Google Site Kit Search Console Search Analytics and GA4 reports, retrieved 2026-11-09. Canonical: https://sweetrationalism.com/. The measurements are observations, not proof of what caused ranking changes.

## Comparison periods

| Metric | May 9–Aug 8, 2026 | Aug 9–Nov 8, 2026 |
|---|---:|---:|
| Search Console page clicks | 296 | 343 |
| Search Console page impressions | 48,766 | 27,446 |
| Page-dimension CTR, computed | 0.61% | 1.25% |
| GA4 Organic Search sessions | 494 | 489 |
| GA4 Organic Search engagement rate | 46.56% | 51.53% |

Query-dimension rows omit anonymized terms, so their totals are NOT sitewide totals. Historical URLs, indexing changes, seasonal demand, attribution and Google updates confound causal interpretation.

## Search queries, Aug 9–Nov 8

| Query | Impressions | Clicks | CTR | Position |
|---|---:|---:|---:|---:|
| michael levin bubble sort | 110 | 36 | 32.7% | 1.66 |
| michael levin criticism | 48 | 7 | 14.6% | 5.71 |
| michael levin controversy | 58 | 2 | 3.45% | 5.97 |
| michael levin sorting algorithm | 29 | 2 | 6.90% | 5.90 |
| is michael levin legit | 32 | 1 | 3.13% | 6.88 |
| michael levin platonic space | 16 | 2 | 12.5% | 41.75 |

These are site impressions, not total keyword volumes. Search demand and organic competition require separate evidence. The new Segall index was published Nov 9, so its search performance cannot yet be judged.

## Key query-to-page findings

- Bubble-sort query: 30 clicks / 87 impressions went to the previous physics/computer-science URL containing 1960s-algorithm-theory; further impressions went to old biology and current classical-algorithm variants. Inspect redirects and Google-selected canonical before changing slugs again.
- Michael Levin criticism: the published response article had 4 clicks / 30 impressions, and the scholarly criticism index had 3 clicks / 22 impressions. Keep distinct article intent; cross-link where it serves the evidence.
- Michael Levin controversy: the response article had 2 clicks / 42 impressions; the index had 0 clicks / 19 impressions. Test a precise, non-sensational answer about the contested claims before metadata changes.
- Historical URL impressions do not authorize restoring deliberately hidden, unlisted or noindex posts. Leave those untouched.

## Organic search engagement sample, Aug 9–Nov 8

- Previous 1960s bubble-sort path: 93 sessions, 52 engaged, 55.9% engagement.
- Published Levin response article: 51 sessions, 31 engaged, 60.8% engagement.
- Levin evidence index: 18 sessions, 12 engaged, 66.7% engagement.
- Mind Everywhere current canonical page: 12 sessions, 8 engaged, 66.7% engagement.
- Total GA4 Organic Search: 489 sessions, 51.5% engagement. The landing-page/channel extract is limited to its first 250 rows.

## Technical and archive findings

- 36 public published articles had Yoast self-canonical, index/follow status and corresponding GitHub article files on Nov 9; drafts and restricted material were excluded.
- The Segall evidence index is live. WordPress article bodies and later reciprocal inline Brash/Mind Everywhere links were committed to the GitHub archive.
- Yoast XML sitemap feature enabled; check actual accepted sitemap and URL inspection results in Search Console.
- Yoast refused to overwrite a pre-existing manually managed llms.txt, and its generator was disabled again. Inspect existing file manually before curating. Google Search does not use llms.txt for generative search inclusion (Google Search Central).
- Duplicate content is not inherently a Google spam-policy violation, but selecting the canonical URL is Google's decision. WordPress self-canonical signals and archive provenance should be retained.
- WordPress Site Health: one critical theme-update label (Kadence), six plugin updates, two inactive plugins. PHP log repeats duplicate WP_DEBUG_LOG and WP_DEBUG_DISPLAY warnings in wp-config.php lines 106–107; no overdue cron events. Backups/staging needed before maintenance.

## Next tests

1. Search Console URL Inspection plus real HTTP redirect-chain tests on historical bubble-sort URLs. Record Google-selected and user-declared canonicals.
2. Confirm sitemap contains only intended indexable public content and the new Segall hub.
3. Track matched query/page metrics over 28 days and compare with unaffected pages. Do not attribute a traffic change without controls.
4. Inspect old hand-maintained llms.txt for public-only links and current framework names.
5. Keep the current high-performing bubble-sort title/snippet unless fresh evidence shows a better query intent match.

No causal SEO improvement is claimed by this document.
