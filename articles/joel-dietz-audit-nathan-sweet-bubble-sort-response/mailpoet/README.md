# MailPoet email-only handoff, newsletter draft #63 (NOT SENT)

**Scope:** Newsletter draft 63, type `standard`, verified draft at 2026-11-12. User wants a concise MailPoet email, not the full WordPress manuscript.

## Required MailPoet editor actions
1. Open MailPoet → Emails → Newsletters → draft #63. Do **not** send or schedule.
2. Identify any **Posts** block or **Automatic Latest Content** block rendering this article as **Full post**. In Display options change the content amount to **Excerpt** (or remove it and use one Text block with the companion `MAILPOET_EMAIL_63_SNIPPET.html`). Preserve mandatory unsubscribe/footer elements and appropriate featured image.
3. Insert one MailPoet **Text** block with content from `MAILPOET_EMAIL_63_SNIPPET.html`; it has a concise argument and seven distinct direct links to working expandable panels on the website (the 14 panels repeat seven test types). Do not paste raw `<details>` markup, code packages, Gutenberg HTML, JavaScript, or 14 full prompts into email.
4. In the Text block use MailPoet's HTML view or native hyperlink controls to create the links. The citation/archive section is **one ordinary paragraph** with natural wrapping; do not import the on-site Zenodo SVG badges, `<br>` delimiters, or images. There are no explicit `<br>` tags.
5. Newsletter draft #63 is of type `standard`. Historical sent newsletters #62 and earlier showed `[newsletter:post_title]` resolving to the post title in the rendered subject despite that type, so do **not** claim the shortcode necessarily fails. Verify its expansion in this draft’s subject preview. Optional concise subject: `Joel Dietz’s 77.6% Audit: Seven Reproducible Source Checks`.
6. Save as **draft**, preview on desktop/mobile, confirm the mail has NO massive code/instructions, no DOI badge blank-space gaps, no unexpected HTML text, and all seven hyperlinks point to the live article with fragment `#rcf-computational-...-open`.
7. Confirm one hyperlink in a live browser opens the relevant hidden panel automatically. The link IDs exist as descendants of HTML `<details>`, because in Chromium navigating to a hidden child ID reveals the enclosing `<details>` (a link to the root details element itself did not open it in testing). Test on more browsers before claiming universal compatibility.
8. Confirm the unsubscribed testing preview and actual MailPoet test send reach only a permitted test recipient. Never send to the live subscriber list without explicit authorization.

## Why website and email must differ
The live article has fourteen copy-ready computational panels across seven distinct checks, and official DOI badge images separated from their resolver URLs by deliberate line breaks. The email is a separate medium: many email clients do not support expandable `<details>` and MailPoet transforms Gutenberg content. Leave the site layout and Zenodo badge accessibility unchanged. Keep newsletter metadata compact, with no badge images.

**Source provenance:** Site article post ID 218725796, permalink https://sweetrationalism.com/articles/epistemology/joel-dietz-audit-nathan-sweet-bubble-sort-response/. The article-specific Zenodo DOI is `10.5281/zenodo.24151128`. MailPoet official guidance: https://kb.mailpoet.com/article/143-mailpoet-email-editor and https://kb.mailpoet.com/article/206-how-to-modify-post-excerpt-length.

## Site helper evidence

WordPress Code Snippets entry #117 is active, scoped to the Dietz response article and copied verbatim in [DEEP_LINK_REVEAL_SNIPPET_117.php](DEEP_LINK_REVEAL_SNIPPET_117.php). A public browser first saw closed panels with the direct link; after activation plus post cache invalidation it observed an open validator panel and visible copy-ready instructions, with the others closed. The browser could not locate the inline script element in the final DOM, so the behavior is **observed**, but the mechanism is not independently established.

Code Snippets entry #9 (`Mail Poet Full Post Length`) is also active and currently sets `mailpoet_newsletter_post_excerpt_length` to **1000** words globally. This is an identified source of overly long **automatically generated** excerpts. It was **not changed**, to avoid altering unrelated newsletters. The current WordPress article has a short manual excerpt; selecting MailPoet **Excerpt** rather than **Full post** should use it. The actual MailPoet editor still needs to be updated and previewed.
