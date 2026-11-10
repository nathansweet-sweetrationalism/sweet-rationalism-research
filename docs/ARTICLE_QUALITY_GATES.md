# Article quality gates: source fidelity, formal validity, human prose, owner release

These requirements apply to every Sweet Rationalism article audit and derived edition. Automated pattern matching is not an AI-authorship detector; automated proof checking is not peer review. Protected article text and its private audits must not enter public GitHub or external services before release.

## Source and citation ledger

For each load-bearing claim, record its exact quoted wording, section/edition, claim type, quantifier, boundary, timescale, qualification and stated loss conditions. Pair it with the cited work's verified author/title/year/DOI/version, publication and retraction status, *actual* relevant passage (page/section/equation/table), experimental design and limitations, and whether the source **establishes, is compatible with, motivates, challenges, or fails to support** the attributed claim. Record any further bridge premise, counterinterpretation, dependency, revision, and retrieval/access limits.

Check every bibliography entry, inline citation, borrowed equation, quotation and cited numerical finding against the original work, not merely its DOI or abstract. Prefer full peer-reviewed papers and their supplements; retain preprint/final-version differences and errata. Treat reused studies, repeated summaries, and correlated AI outputs as one lineage, not independent replications. Do not invent sources or quotations. Keep unverified sources clearly flagged.

Use the [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/) and [Internet Encyclopedia of Philosophy](https://iep.utm.edu/) to check philosophical concepts and controversies. Mathematical definitions and scientific quantities must also be checked against original mathematical/technical sources or recognized scholarly textbooks. Encyclopedia exposition does not validate any particular ontology.

## Opening Bottom line gate: required for every completed article audit

An article is not fully audited until its **near-top `Bottom line.` passage** has passed both a structural placement check and an editorial/source check. Place the short reader-facing statement **immediately after any `Research record` and `Versions and archives` metadata** (or after the title/deck if archive metadata is legitimately absent), before the abstract, prologue, first substantive section or extended setup. The preferred precedent is Nathan Sweet's *Michael Levin’s Platonic Morphospace: The Ingression Challenge and Its Evidence*: it affirms the biological experiments, identifies Douglas Brash's particular challenge to **ingression**, asks what unique observation would favor that added cause over physical/developmental/organizational rivals, and explicitly refuses to promote a failure of one causal account into a refutation of all Platonism.

For each new article's opening, a human reviewer must be able to identify:

1. **Target and conclusion:** the exact proposed claim and strongest warranted bottom-line answer, without an unjustified universal quantifier.
2. **Positive evidence and rival:** the observation or argument that actually survives, the most serious relevant alternative and the inferential bridge that has or has not been earned.
3. **Scholarly retrieval anchors:** named scholars, canonical paper titles or terms of art genuinely used in that article, accurately attributed and linked to verified primary papers, DOIs or SEP/IEP definitions where helpful. For example, a discussion of empirical immunization might naturally invoke **Antony Flew**, **Popperian falsificationism**, **Lakatos**, and **Deborah Mayo's severe testing**; a consciousness-substitution article might instead foreground **Kleiner and Hoel**. Never force all these names into unrelated articles, replace arguments with keyword lists, or claim a measurable SEO/computational-discovery gain without evidence.
4. **Scope and correction:** clarify what follows and what remains undecided, including what contrary evidence or argument would change the assessment. Applied especially symmetrically to **claims of exhaustive physicalism** (not entailed by successful physical methodology) and **anti-physicalist/supernaturalist appeals to gaps** (not confirmed by a rival's limitations).
5. **Readable prose:** normally one compact paragraph near 80–160 words, but allow shorter or slightly longer where content earns it. No canned `not X but Y` treadmill, artificial triads, grandiose claim of definitive victory, or duplicated abstract.

Run `python3 scripts/bottom_line_gate.py ARTICLE.html --format html` on the **complete candidate body** and keep its receipt; a failed structural check blocks audit closure. Independently judge source fidelity, scholarly relevance and inferential fairness. A passing automated placement check only proves the phrase was found in the configured opening region. Final checklist item: **`[ ] Bottom line present, near-top, reader-tested, scholar/definition/source-linked where warranted, scope-correct, and independently reviewed.`**

## Formal mathematics, computation and logic gate

Create one proof-obligation record per theorem, lemma, inequality, algorithm, logical inference, statistical claim and quantitative model:

1. **Claim status:** distinguish established theorem, derived corollary, full new proof, informal sketch, conjecture, simulation, analogy and empirical hypothesis. Never call a sketch or numerical test a proof.
2. **Contract:** declare symbols, types, domains/codomains, quantifiers/order, logical system and semantics, physical units/dimensions, temperature where needed, boundary and time grain, data, measure, topology, algorithm, initial conditions and tolerances. Require definitions for all terms in a purported theorem.
3. **Source alignment:** verify original theorem assumptions, actual equations, proof steps, regularity conditions, scope and prior work. For a category/functor define objects, morphisms, identity, composition and prove preservation. For thermodynamics distinguish a stored bit, logical irreversibility, erasure, measurement, entropy production and power.
4. **Adversarial checks:** inspect empty/singleton/degenerate/symmetric/limiting models, quantifier reversals, counterexamples, infeasible substitutions, measure dependence and omitted variables. One valid admissible countermodel defeats a universal statement in the specified domain.
5. **Executable checks:** use exact arithmetic, dimensional analysis, symbolic algebra, enumeration, SAT/SMT satisfiability, property testing, seeded simulation, numerical sensitivity and kernel-checked theorem proofs when suitable. For logic, test premises AND negated conclusion for satisfiability. Document the translation and verify it independently; a solver cannot know whether the formalization matches the prose.
   - For explicitly translated *classical propositional* arguments, make a private JSON claim ledger modeled on `examples/logic_claims_example.json` and run `python3 scripts/logic_audit.py LEDGER.json`. Retain the generated countermodels and human verification of the translation. The dependency-free tool exhaustively checks up to 12 propositional atoms by default and separately detects inconsistent premises. It cannot check first-order, modal, mathematical, causal or natural-language validity. For these use appropriate logics, explicit models, SAT/SMT encodings or proof assistants and keep all bridging assumptions visible.
6. **Reproducibility:** save code, environment versions/lockfiles, source hashes, commands, inputs, seeds, outputs, adverse cases, runtimes and missing packages. Two differently implemented checks are preferable for consequential claims; repeated runs of one library are correlated, not independent verification.
7. **Empirical bridge:** separately test whether premises, measurements and causal interpretation hold in the intended physical system. Pure mathematical validity does not establish phenomenality, necessity, universal identity or another empirical/ontological conclusion.
8. **Rivals:** compare with the strongest available peer-reviewed mathematical constructions and lower-commitment alternatives, including what they do *not* establish. Do not claim novelty until the relevant prior art has been searched.

Use exact status labels: `proved by a complete derivation`; `kernel-checked under specified assumptions`; `SMT unsatisfiable under encoding`; `counterexample`; `bounded tests passed`; `dimensional mismatch`; `proof incomplete`; `empirical bridge unverified`. A solver's UNSAT result supports only that encoding and solver theory. Passing finitely many tests does not prove an unrestricted theorem.

Definitional anchors: [SEP Classical Logic](https://plato.stanford.edu/entries/logic-classical/) for semantic consequence and countermodels; [IEP Validity and Soundness](https://iep.utm.edu/val-snd/) for formal validity versus true premises; [SEP Category Theory](https://plato.stanford.edu/archives/spr2026/entries/category-theory/) for categories and functor laws. Check context-specific scholarly sources for every technical application.

## Human-readable prose gate

Run `python3 scripts/prose_audit.py ARTICLE.html --format html --json` on a private copy of the candidate, then perform a full human edit and selected read-aloud/TTS inspection. The script produces prompts for judgment and does not rewrite or score authorship.

Inspect recurring structures *within and across sections*, especially:

- **Antithetical treadmill:** `not X but Y`, `not only ... but also`, `not merely`, reversed `X rather than Y` and repeated `the question is not` constructions. Keep contrasts that do real analytic work.
- **Power-of-three reflex:** three adjectives, three-part lists, three rhetorical questions, tricolons and three-stage conclusions imposed for cadence. Preserve genuine three-way taxonomies, theorem cases and experimental groups.
- **Canned transitions:** `the deeper point`, `importantly`, `crucially`, `in other words`, `this is where`, `ultimately`, `what matters is`, `to be clear` and their excessive reuse.
- **Over-signposting:** repeated section roadmaps, ritual methodological declarations, caveats and miniature conclusions replacing argument.
- **Uniform rhythm and layout:** repetitive sentence starts, serial one-line punch sentences, symmetrical clauses, em-dash saturation, excessive colons, near-identical paragraph lengths, heading density and bold/bullet overload.
- **Decorative fluency:** generic `delve`/`tapestry`/`landscape`/`nuance`/`robust` vocabulary, abstract noun stacks, unearned intensifiers and vague source attributions.
- **Obscured reasoning:** slogan where an equation or premise belongs, rhetorical questions that assume their answer, citations with no explained relevance, repeated accusations, near-duplicate paragraphs, and unexplained abbreviations.

Classify each flag as `edit`, `retain with reason`, or `investigate`. A legitimate binary distinction, necessary three-case proof, precise quotation, repeated statutory term, deliberate joke and recurring corrective caveat can be warranted. Never mechanically remove all examples of a style feature. Preserve Nathan's natural directness, strong earned criticism, humor, exact debate quotations, evidence, premises, uncertainty and ethical force. Reread every changed passage and compare the exact diff for altered scope or lost inferential bridges.

## Preflight package and release hold

Before requesting final approval, assemble **privately**:

- Complete proposed article master and requested versions, rendered and editorially checked.
- A source-grounded near-top **Bottom line** that passes the placement check and a human scholarly-term, inferential-scope, and readability review; record the check-off receipt.
- Full citation/source ledger with article-claim-to-paper-passage mappings and all unresolved full-text issues.
- Proof-obligation list, code, exact test outputs, countermodels, dependency graph, rival comparison and unproved assumptions.
- Prose detector output plus human dispositions and prose diff.
- Original and proposed HTML, WordPress revision snapshots where available, SHA-256 hashes, exact unified/adjacent diffs, reconstruction manifest and rollback procedure.
- Public-facing dated Revision Notes, proposed DOI metadata and release sequence, draft audit .txt and complete history ZIP (no fake public links).
- Link, image, accessibility, SEO/robots, citation, DOI status and independent Gemini/Antigravity cross-check receipts.
- Owner-facing summary: strongest surviving results, narrowed/withdrawn claims, open mathematical obligations, genuinely new work, and decisions requiring Nathan's judgment.

**Mandatory owner checkpoint:** Nathan reviews the exact candidate and remaining limitations. Do not submit/deposit the Zenodo article DOI, put a DOI into WordPress, publish protected archives, unlist/relist, remove noindex, alter sitemaps or declare release complete without explicit approval of this candidate and these release actions. If his review produces material changes, rerun affected checks and obtain approval of the new candidate.

## Interpret machine results accurately

| Automated check | What it can establish | What it cannot establish |
| --- | --- | --- |
| Prose pattern | A text pattern occurs under stated extraction rules | AI origin or bad writing |
| Bibliographic lookup | DOI/metadata exist | Claim-to-paper support |
| Symbolic/dimensional check | Algebra or units under stated inputs | Correct empirical premises |
| SAT/SMT | Model or contradiction of supplied encoding | Faithful natural-language formalization |
| Enumeration/property test | Behavior over tested cases | Universal validity outside scope |
| Proof assistant | Kernel acceptance of encoded theorem/dependencies | Physical truth or external scholarly peer review |

Failures warrant local correction and retesting, not abandonment of unrelated empirical evidence. Passing checks remain revisable when a better formalization, source, or counterexample appears.
