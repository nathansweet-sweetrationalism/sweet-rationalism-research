# MailPoet email-safe distribution and script-loaded computational panels

**Current state (12 November 2026):** WordPress article #218725796 is published. Newsletter #63 is still a standard MailPoet draft, **not sent or scheduled**. The article itself contains **14 hyperlink triggers and no embedded `<details>` instructions or code textareas**. The website uses a JavaScript loader to reconstruct the same fourteen panels (seven unique test types, each at quick and analysis locations). This changes the email's source from 220 KB of embedded test-panel HTML to fourteen ordinary links.

## Immutable publication provenance

- Canonical article: https://sweetrationalism.com/articles/epistemology/joel-dietz-audit-nathan-sweet-bubble-sort-response/
- Before migration, full WordPress post body: [PRE_SCRIPT_MIGRATION_BODY_2026-11-12.html](PRE_SCRIPT_MIGRATION_BODY_2026-11-12.html), 322,766 UTF-16 code units
- Independent source data: [COMPUTATIONAL_PANEL_TEMPLATES_2026-11-12.txt](COMPUTATIONAL_PANEL_TEMPLATES_2026-11-12.txt), seven JSON templates; each quick/analysis pair was checked identical after normalization of its panel ID
- Active WordPress Code Snippets #118: [PANEL_LOADER_SNIPPET_118.php](PANEL_LOADER_SNIPPET_118.php), exposing public GET `/wp-json/rcf/v1/dietz-panels` and site-only JavaScript
- Older WordPress Code Snippets #117: [DEEP_LINK_REVEAL_SNIPPET_117.php](DEEP_LINK_REVEAL_SNIPPET_117.php), fragment reveal for formerly embedded panels; may be redundant now. Do not deactivate without confirming the replacement.
- Actual readback: WordPress post modified 2026-11-12T13:57:16 site time, raw body SHA-256 `4e291e99c9c2dd21f0d909426b2d818eb4de1f14193e78ed3e368f8497bd49fd`, 107,940 UTF-16 code units. GitHub `article.html` tracks this revision.

## Exact behavior and limitations

In WordPress source the quick-check list contains seven links, **each with its test title exactly once**. No redundant preceding `<strong>` title. There are seven additional links in the analysis, totaling fourteen. All links target `#rcf-computational-<type>-<quick|analysis>-open`. The JavaScript loader queries the versioned public REST endpoint, validates the seven templates and their identifiers, reconstructs original `<details>` and `<textarea>` elements, replaces the fourteen source links with the panels, and opens the one targeted by the location hash.

The HTML-only (including MailPoet) representation has only hyperlinks. This is a separation of *content location*, not cosmetic CSS hiding. Native browser script execution is required to display interactive panel contents. If browser JS or source download fails, plain links remain clickable, but **they cannot expand text** until the loader succeeds. Do not assert universal browser compatibility. The source payload is public and reproducible on GitHub.

**Verification evidence:** The same-origin endpoint probe returned HTTP 200 with seven template keys. Static artifact tests validate 14 anchors, seven templates, citation text, two linked badges and duplicate-title removal. A public browser agent's report on script presence/DOM was inconsistent with the authenticated WordPress and REST readbacks, so a successful client-side hydration in all browsers is **not independently confirmed** by those reports alone. Verify manually in signed-out desktop and mobile browsers and capture the real DOM and network waterfall before claiming browser-level success.

## DOI badge layout (on-site only)

One naturally wrapping paragraph contains `Cite as:`, licensing and `Versions and archives:`, with the full DOI resolver URLs, Zenodo record, GitHub and changelog links. It is immediately followed by **one separate paragraph containing both original official linked Zenodo badges**, side-by-side, without `<br>` tags. `Bottom line.` follows. Do not remove either badge or split them onto separate forced lines to repair MailPoet.

## Newsletter #63 instructions

1. Open MailPoet → Newsletters → Draft #63. Select **Excerpt**, **not Full post**, in its post content block. If using a hand-crafted email, remove the full-post block and insert [MAILPOET_EMAIL_63_SNIPPET.html](MAILPOET_EMAIL_63_SNIPPET.html) as a concise Text block. A standard subject may require a direct title rather than a contextual Post Notification shortcode; preview the rendered subject.
2. Preserve the unsent state, subscriber lists and mandatory unsubscribe footer. Check desktop/mobile preview, post title/author metadata and that no full computational prompts appear. The fourteen on-site hyperlinks are still present if the email uses the raw article post body, but the recommended email is shorter, with seven representative links.
3. WordPress Code Snippets #9 (`Mail Poet Full Post Length`) was explicitly deactivated. It formerly forced globally generated excerpts to **1000 words**; changing the excerpt setting no longer requires that workaround. The article also has a short manual excerpt.
4. Follow a test link in a normal browser and verify the correct panel opens with full copy-ready instructions, while other panels remain closed. For the special `#...-open` case, inspect rendered DOM and network calls; browser-agent extraction without code execution cannot demonstrate this.
5. Save the email draft and inspect a test preview. Do **not** send or schedule to live subscribers without fresh owner authorization.

## Scientific scope

The payload split does not change any of the actual 14 instructions or the seven executable test packages; it changes only their delivery. The article's published Zenodo version DOI `10.5281/zenodo.24151128` is immutable; the repository's latest `article.html` is a later live website edition. The MailPoet preview and JavaScript hydration are **interface tests**, not proof of the article's scientific claims.
