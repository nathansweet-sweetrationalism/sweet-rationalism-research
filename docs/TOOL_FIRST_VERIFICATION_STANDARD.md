# Source-first, tool-first verification standard

Established 2026-11-11. This is a workflow specification, not evidence for any particular scientific or philosophical conclusion.

## Priority

Use independently retrievable evidence and deterministic tools for as much of a research or publication task as the question permits. Minimize reliance on a language model's recall, generated narrative, untested intuitions, or another model's verdict. More tools are useful only when they add relevant checks or independent information; duplicate checks on the same source do not amount to independent confirmation.

Apply this standard to every article audit, agent prompt, downloadable replication package, external coding-agent handoff, and associated publishing action. In public-facing instructions describe the actual steps plainly, without methodology acronyms or specialist internal framework vocabulary.

## Required procedure

1. **Exact target and provenance.** Quote the precise claim, identify the person or work making it, distinguish what was observed from what was inferred, and declare version, system, boundary, time frame, units, scope, and alternative interpretations. Preserve relevant qualifications, dates, corrections, and counterexamples.
2. **Independent sources.** Read the canonical original text, published primary research, official DOI records, and exact repository code/data. Use working URLs and pinned immutable revisions, not model memory or search-result paraphrases. Record retrieval method, URL, source SHA-256 when available, repository commit, date and any access failure. Check later corrections separately from historical revisions.
3. **Executable questions.** Convert each material assertion into a specified test with inputs, procedure, expected result, measured result, acceptance rule, and what would overturn it. Prefer parsers, exact source comparison, CSV/JSON processing, Git diffs, Python standard-library calculations, symbolic/logic solvers, unit tests, statistical tools, or formal checks when appropriate to the proposition. Inspect scripts and dependencies before running them; never execute untrusted upstream code without a safety review.
4. **Independent checks and controls.** Whenever feasible, run a separately implemented cross-check and relevant positive/negative controls, boundary cases, or counterexamples. Fix seeds, versions, tolerances and sample size for stochastic or numerical claims. If no discriminating test exists, identify the remaining uncertainty and what evidence could resolve it. Do not adjust thresholds after reading outcomes without documenting that post hoc change.
5. **Rival explanations and loss conditions.** Compare at least one serious alternative, including simpler mechanistic or organizational accounts when appropriate. Specify which result would lower support for each account. A failed model does not automatically establish its rival unless the alternatives are exhaustive; a successful mathematical simulation does not by itself establish a nonphysical cause, real-world phenomenon, or welfare claim. Keep empirical, formal, explanatory, and ethical claims distinct.
6. **Symmetric correction.** Apply the same standards to every person, favored hypothesis, generated tool, prompt, and audit procedure. Inspect the possibility of quotation errors, wrong datasets, code bugs, benchmark selection, correlated sources, mis-scoped claims, or inaccessible evidence. Record useful failures and update downstream dependencies; do not erase falsifying outputs.
7. **Responsible results.** Return an evidence ledger with claim type, system/scope, version and hashes, source URLs, procedures and runnable commands, environment, observed stdout/stderr/exit status, control outcomes, result, possible alternate explanations, uncertainty, limitations and specific reversal conditions. Recommended labels: `CONFIRMED_WITHIN_SCOPE`, `DISCONFIRMED_WITHIN_SCOPE`, `PARTIAL`, `UNRESOLVED`, `NOT_RUN`. Never invent citations, logs, model probabilities, future test completions or DOI deposits. Distinguish actual empirical evidence from an artificial negative control and a fixture-only smoke test.
8. **Consequences.** For claims affecting biological or artificial systems, identify whose interests, agency or welfare might be affected, who has authority to intervene, likely externalities and irreversible risks. Do not transfer uncertain theoretical conclusions into normative permission without a separate explicit justification.
9. **Review the workflow itself.** Check that prompts and software do what they claim, that reported status is computed from actual tests, and that the procedure remains open to correction. Avoid graph structures that freeze conclusions; record claims, evidence, dependencies, alternative models, and conditions that change support instead.

## Source-first computational prompt and download fallbacks

For each test package, place **full URLs** directly in the copy-ready prompt:
- Primary downloadable test ZIP hosted in GitHub or in the canonical website's WordPress media library.
- Independently hosted fallback ZIP. If no second ZIP exists, link the exact open-source files and a deterministic build script instead; never pretend a repository page is a ZIP download.
- The original article, the respondent's primary text, any companion, exact pinned upstream code/data files, DOI metadata, and the commit ID.
- The canonical website article and its GitHub research-record directory. Verify whether the URL is publicly available rather than assuming a draft preview is accessible.

The coding agent downloads the package itself, verifies hashes when known, reads README, manifest, and scripts before execution, retrieves original sources independently, performs the checks, and returns a reproducible ledger. The human-facing ZIP download remains optional. If access is blocked, document the failure, try the actual fallback, and use the source-code reconstruction path if provided; otherwise report `UNRESOLVED`. Never silently replace a live source test with packaged fixtures.

For nontechnical readers: choose a test; open Codex, Claude Code, Antigravity or another coding agent with browser/filesystem capabilities; paste the complete prompt into a new task; approve only necessary access to an isolated working directory; ask for commands, outputs, original-source references, discrepancies and counterexamples. Attach a downloaded ZIP manually only if automated retrieval fails.

## Publication boundary

This repository can host an article-specific reproducibility scaffold before publication, but a draft, protected article body, private audit correspondence or unreleased source archive must not be published accidentally. Preserve the author's release review. Before the final public release, verify the canonical site URL, exact GitHub files, published article body and approved archival DOI records. Do not invent a DOI or publish ahead of authorization.
