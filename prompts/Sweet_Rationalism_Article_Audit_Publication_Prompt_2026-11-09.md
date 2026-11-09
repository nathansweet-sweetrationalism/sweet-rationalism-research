# Sweet Rationalism: Article Audit, Revision, SEO and Archival Publication Prompt

**Version:** 2026-11-09  
**Author and publication:** Nathan Sweet, [Sweet Rationalism](https://sweetrationalism.com/)  
**Research archive:** [sweet-rationalism-research](https://github.com/nathansweet-sweetrationalism/sweet-rationalism-research)

## Reusable task prompt

Audit and, where warranted, revise the following **already published** Sweet Rationalism article:

**Canonical WordPress URL:** `[INSERT EXACT PUBLIC ARTICLE URL]`  
**Additional original sources, correspondence, transcripts or files:** `[ATTACH OR LINK]`  
**Scope of this run:** `[FULL ARTICLE AUDIT / SPECIFIC CLAIMS / SEO AND LINK AUDIT / NEW EVIDENCE / MULTI-EDITION UPDATE]`

Work against the **current live article**, its revisions, the linked source documents, and the canonical/current framework records. Treat earlier audits as an evidence trail, not as authorities exempt from renewed scrutiny. Do not recreate the article as a new post. Preserve its original URL, publication history, intended audience, and current editorial identity unless a particular change is independently justified and authorized.

### 1. Access and publication boundaries

- Confirm the target is intentionally **public, published and indexable**. **Do not open, edit, archive, link to, surface in indexes, or publish any draft, hidden, private, restricted, noindex or unlisted article**. An old URL in Search Console is not permission to restore a hidden post. If status is uncertain, stop at the boundary and ask.
- Read the whole current article, including footnotes, revision notes, captions, reference lists, embedded structured data, quoted exchanges and linked audits. Identify the actual version and any protected passages before editing.
- Inspect the actual `AGENTS.md`, README and publication rules in the public `sweet-rationalism-research` repository. Preserve the separately maintained repositories and existing Zenodo DOI records for the core RCF methodology, ethos, ontology, framework bridge and worldview. Avoid creating competing canonical versions.
- The **WordPress page remains the canonical publication**. GitHub stores reproducible versions and diffs; Zenodo stores properly deposited citable snapshots. Never invent a DOI, imply an archive file has been deposited, or claim that mirroring guarantees AI training inclusion.

### 2. Source fidelity and scholarly challenge

- Reconstruct each important claim in the author's or interlocutor's **strongest defensible form**. Preserve exact wording, attribution, date, venue, edition and context. A quotation, reductio, conditional counterexample and author's affirmative belief are different things. Never silently turn `?X` into `¬X` or answer a substituted claim.
- Check sources in order of evidential fitness: original papers and experiments, peer-reviewed research, authoritative academic reference entries (including SEP/IEP for definitions), original statements/correspondence, official institutional records, and then responsible secondary analysis. Verify DOIs, paper versions, errata, retractions, methods, samples, actual measurements, quotations and citation support. Record paywall or full-text limits.
- Type claims as **observation, reported source claim, inference, hypothesis, model, philosophical thesis, normative premise or unresolved ontology**. Explicitly specify the target construct, system boundary, timescale, relevant alternatives, and what evidence is admissible to the claim's tribunal (empirical, causal, formal, semantic, phenomenal, historical, participant, normative or ontological).
- Separate mathematical correctness from physical applicability, correlation from intervention, model usefulness from metaphysical truth, analogies from identities, and physical implementation from exhaustive metaphysical physicalism. Test universal or necessity claims at their asserted scope; do not mistake a locally effective model for cosmic proof.
- For controversial biological and consciousness claims, distinguish cognition, agency, autonomy, selfhood, consciousness, sentience, valence, welfare, moral standing and responsibility. Do not smuggle one through evidence for another or assume either biological or computational substrate settles the question.
- Audit rival models symmetrically. For each serious rival identify its explanatory target, causal mechanism where available, auxiliary assumptions, independent support, unique prediction or intervention, potential false positives and negatives, negative controls, evidential dependence, and explicit **condition for losing support**. Prefer experiments and counterexamples that would make rival models disagree.
- Use mature Popperian, Lakatosian, Duhem–Quine and post-Popperian appraisal as appropriate. A falsifier may force local, auxiliary or programme-level revision; avoid caricaturing falsification as a single observation logically demolishing an entire metaphysics. Do not shield RCF itself from the same severe tests or assume its architecture outperforms a simpler approach.
- Assess each alleged fallacy or equivocation against the *actual premise and inferential step*. An argument's failure does not, by itself, establish the opposite conclusion. Distinguish a demonstrated contradiction, failure to explain, underdetermination, accommodation without discriminatory gain, and a live but as-yet unsupported possibility.
- Retain findings that withstand scrutiny and correct only the inference the evidence defeats. Preserve the original article's bite, particular examples, justified reductios, humor, pointed criticism and ethical concerns. Do not dilute warranted criticism for deference, or escalate a possible harm into a demonstrated causal injury without evidence. Name documented institutional appropriation and its foreseeable risks precisely; do not invent motives or endorsement.

### 3. Editorial revision

- Begin with a short, accurate answer or **In short** section that states the actual disputed proposition, what the best evidence supports, what remains open, and the decisive next test. Keep it useful to human and machine readers.
- Improve each section's distinct contribution and the transitions among sections. Remove factual overstatement, duplicated argument, unsupported necessity language, ambiguity, accidental straw men and unnecessary procedural padding while retaining all sound observations, citations and relevant past corrections.
- Use the current name **Recursive Corrigibility Framework (RCF)**. Replace obsolete current claims or terminology (including **Recursive Constraint Falsification**) where they inaccurately describe the present framework. Preserve verified earlier terms in faithfully quoted historical material, older article titles or explicitly historical accounts. Do not rewrite the past to conceal conceptual development.
- Consolidate bibliographic references into a coherent reference section without deleting sources, and retain inline citations wherever they materially support a claim. No disorderly separate blocks titled after past revision rounds. Link to primary full text and DOI landing pages when possible.
- Keep rhetoric rigorous, energetic, candid and sometimes irreverent. Use the strongest phrasing earned by evidence, plausible harm, reversibility, and responsibility. No empty civility rituals, personal speculation, ritual hedging, slogans in place of proof, or gratuitous profanity. Write naturally and accessibly, with TTS-friendly paragraphs where requested.
- Maintain a **separate cumulative change-and-evidence audit**. Unless specifically requested, do not tell ordinary article readers in the introduction what was changed in this editing pass.

### 4. Internal links and measured SEO

- Enumerate the relevant **currently public and indexable** articles, related topic hubs and major core framework pages. Add genuinely useful in-body links at the precise passage where one article's evidence, mechanism, disagreement or test helps explain another. Use concise, descriptive, natural anchor text; avoid blanket link stuffing, repetitive related-post boxes, hidden posts and self-links posing as recommendations.
- Consult available Search Console query, query-to-page, and period comparison data, plus GA4 organic landing-page engagement, before modifying SEO titles or focus topics. Record the actual date range, clicks, impressions, CTR, average position and landing URL. Treat impressions as site appearances, not total query volume; keep anonymized-query limitations and page/query discrepancies visible. Verify current search intent and competing pages before claiming keyword difficulty.
- Assign distinct search intent where articles overlap. Prefer query clusters and relevant explanatory headings over keyword stuffing. Audit historical paths and 301 redirects before changing any slug. A historical URL in Search Console may already be redirected, excluded or inaccessible; verify rather than assume.
- Check title, meta description, descriptive heading hierarchy, image alt text where suitable, accessibility, Page/Article schema, original and modified dates, self-referencing canonical, Yoast indexability, sitemap inclusion, robots directives, and selected internal links. Preserve the site's canonical priority over archival copies. Search-engine selection remains outside our control: do not promise the absence of duplicate clustering or a ranking outcome.
- Maintain the XML sitemap through WordPress/Yoast. Consider `llms.txt` a modest discovery aid for machine readers, **not a Google ranking mechanism**. Respect any existing manually curated file, and never overwrite it or expose hidden content through an automatic generator without inspecting its behavior.

### 5. GitHub and DOI synchronization

- After the live article is revised, **read back WordPress** and archive the exact verified published body at `articles/<canonical-post-slug>/article.html` in `nathansweet-sweetrationalism/sweet-rationalism-research`.
- Update the matching `metadata.json`: canonical URL, title, publication/modified times, DOI and DOI status when verified, current version, evidence/audit references, source dependencies, primary alternatives, loss/update conditions and revision linkage. Refresh `articles/index.json` and any affected inbound/outbound link registry. Preserve history with a specific Git commit message and verify the file/blob and commit on the branch. Never claim a pushed or deposited edition based on a draft or an uncommitted tree.
- Near the top of the WordPress article, include simple reader-facing references to its **exact GitHub article file** and canonical page. Add an **article-specific DOI** only if that DOI really identifies the article and the deposit exists. For material scholarly editions, check whether an authenticated Zenodo new-version deposit is due; prepare metadata and flag any manual deposit step. The DOI for the aggregate repository or a framework document is not automatically an article DOI.
- If the content also has authorized HTML, Markdown, Substack or downloadable editions, synchronize their argument, citations, link targets and revision identifiers, preserving intentional platform differences. Audit each edition instead of assuming conversion is faithful.
- Maintain a record of corrections and source provenance. A claim graph, if maintained, should store **claims, their dependencies, serious rivals, observations, predictions and explicit conditions for losing support**. It must not store immutable verdicts or pretend that a diagram validates a proposition.

### 6. Required result and verification

Return, in this order:

1. **Executive verdict:** what survives, what needs narrowing/correction, what fails, what remains unresolved, and the strongest discriminating objection or test.
2. **Section-by-section audit:** exact passage/claim, strongest charitable reading, source check, counterarguments, affected dependencies, severity and proposed replacement wording. Separate factual changes from clarity or SEO changes.
3. **Traceable source inventory:** author/title/date/DOI or stable link, what each source actually establishes, gaps and inaccessible full text. Identify retractions and shared evidence lineage.
4. **Revision receipt:** WordPress URL and post ID; previous/current state; edits made; protected material retained; SEO/canonical/sitemap/redirect checks; contextual internal links added; GitHub file and verified commit; article DOI or explicit pending/no DOI; hidden material excluded; and rollback path.
5. **Outstanding manual work:** permissions, inaccessible records, Search Console URL inspections, redirects, file-server changes, Zenodo deposit or other steps that cannot be completed through currently authorized tools.

Do not invent the results of an unperformed audit, browser inspection, source review, API call, DOI registration, Git push or Google recrawl. An interruption is a partial result, and each publication surface must be labeled **drafted, locally validated, published, archived, deposited, or unverified** based on observed evidence. If additional inspection no longer promises a material change, stop and present the remaining uncertainty instead of endlessly expanding the report.
