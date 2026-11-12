# Public site branding, automatic GitHub marks, and email DOI layout

Status: Active editorial and presentation policy, adopted 2026-11-12.
Applies to public Sweet Rationalism website articles, pages, excerpts, email newsletters, and public-facing repository descriptions.

## 1. Public-facing platform-neutral wording

- When referring to our own site in **reader-facing editorial prose**, use **Sweet Rationalism website**, **Sweet Rationalism article**, **site archive**, **website revision history**, or another accurate publication-oriented phrase. Do not unnecessarily identify the site's publishing platform, installed themes, extensions, administrative tools, vendors, or versions in body copy, excerpts, metadata labels, newsletter text, frontend prompts, and navigation.
- Preserve **verbatim source quotations, historically attributed statements, bibliographic titles, third-party hostnames, DOI identifiers, immutable archive filenames, code, package links, error messages needed for reproducibility, and public technical records**. Never rewrite another author's words merely to conceal a platform name. If these are required by the research record, factual and source fidelity take precedence.
- Technical instructions in private operational materials may name software explicitly where necessary for correct and safe maintenance. Public GitHub research/reproducibility records may similarly identify tools when those identities are necessary to reproduce an intervention; classify any such material intentionally rather than applying indiscriminate replace-all.
- **Do not claim software anonymity or a security guarantee from generic editorial wording.** Website paths, generated assets, API behavior, response headers, cached copies, and public source repositories can reveal infrastructure. Rely on patched dependencies, least-privilege credentials, access control, backups and security testing. Do not unilaterally update plugins/themes during a separately frozen editorial cycle.

### Existing article repair (2026-11-12)

- Published article #218725796: replaced two incidental references to the publishing platform in prose with “Sweet Rationalism website ZIP locations” and “Sweet Rationalism article”.
- Published consciousness article #2115: changed two *visible link labels* to “Sweet Rationalism website reconstruction history” and “lossless Sweet Rationalism website history ZIP”; preserved exact linked archive filenames and URLs.
- Other indexed matches in published research were third-party domains or attributed quotations. Their text/links remain unchanged.

## 2. Automatic GitHub link glyph on the website

- Use a small **GitHub mark**, rendered automatically by site-wide CSS as an **accessible-decorative pseudo-element** in front of ordinary direct `https://github.com/` links, using a self-contained SVG mask and `currentColor`. There is no portable Unicode character that is the actual GitHub mark; do not prepend substitute emoji or manually edit every anchor.
- Preserve the anchor's readable text, actual URL, keyboard operation and accessible name. Do not add a duplicate icon for a link already containing its own GitHub branding; opt out of the CSS with `class="sr-no-github-icon"`. The icon is decorative; it does not replace textual link context.
- CSS is site-specific. It does not automatically appear in newsletters or feed readers, which often discard site CSS. Do not rely on the mark for meaning.
- Implemented in the Sweet Rationalism website's **persistent Additional CSS** (stylesheet setting, recorded revision 218725935 on 2026-11-12); the original site-scoped snippet **#119 was deactivated** after browsers did not see its injected style. No external icon CDN or font required. The Additional CSS copy was read back and confirmed to contain the `github.com` selector and SVG mask; a signed-out computed-style/visual check is still required before calling it fully verified.

## 3. DOI badges on the website vs in email

- On the **website**: keep an immediately adjacent pair of blocks before `Bottom line.`: (a) a compact, naturally wrapping citation and archives text paragraph with full clickable version and concept DOI URLs; (b) one **single shared row with both original linked official Zenodo badges**, correct alt text and no `<br>` tags. Never silently remove either badge.
- In generated **email**, do not assume website paragraph/image CSS survives content conversion. The newsletter renderer may introduce table-row spacing, strip CSS or reflow linked images, even when both images are siblings in the source. Diagnose the email preview, not just the website markup.
- For adjacent DOI badges in a newsletter use a single email-compatible **presentation table row with two fixed-size cells** (each badge linked independently, image width/height set, zero top/bottom padding/margins). If that table is inserted through a rendering hook, scope the hook to content that has exactly two owned DOI badges; preserve the rest of the newsletter and handle parse failures as a no-op.
- Maintain a separate, concise email presentation (excerpt or approved dedicated email text) for articles with large browser-only computational panels. Their full instructions are loaded only by browsers from an externally archived payload, not stored as hidden content inside the article source. An email contains direct website links to relevant panel anchors.
- Validate **desktop and mobile** newsletter preview and a permitted test recipient before sending; do not send or schedule a campaign without specific authorization.
- The paired email badge transformer is active as site Code Snippets **#120**. The **verified** implementation runs at the newsletter's final `mailpoet_rendering_post_process` HTML stage. The older `mailpoet_sending_newsletter_render_after_pre_process` stage did **not** run on the draft's browser-preview path and must not be treated as proof of layout. On 2026-11-12, the draft #63 rendered HTML was verified to contain one 360px presentation table, one `<tr>`, two `<td>` cells, two original DOI SVG URLs and two distinct corresponding DOI links. No empty padded row occurs between these badges. This is a structural HTML check of the preview; a real email-client test remains outstanding.

## 4. Verification and loss conditions

- **Platform-neutrality test:** review outgoing public copy for incidental vendor/product names, while checking that quotes, URLs, reproductions and third-party credits remain accurate. Historical context is an exception, not a license to silently alter source text.
- **GitHub-link test:** inspect a signed-out article with both a direct GitHub link and a non-GitHub link; the first has one decorative icon, the second has none. Check the site also on keyboard and narrow mobile width. No new link target rewriting.
- **DOI email test:** inspect the generated newsletter DOM and screenshot. Both badges appear on a single horizontal row immediately following the citation text, with no vertical blank strip between them, and each icon remains independently clickable. If not, mark **FAIL** and alter the email-only renderer, not the article archive.
- **Scientific integrity test:** no changes to public technical claims, source quotations, original archive filenames, author attributions, package hashes or immutable DOI deposits without a separate evidence-based audit.

The site-specific title and software configuration used to implement these rules are operational details, not reader-facing editorial content.
