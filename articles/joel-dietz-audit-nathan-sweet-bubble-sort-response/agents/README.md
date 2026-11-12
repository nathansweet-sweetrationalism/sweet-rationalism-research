# Independent agent audit submissions

The canonical full task prompt is [INDEPENDENT_AUDIT_HANDOFF.md](INDEPENDENT_AUDIT_HANDOFF.md). Start agents with the entire prompt or the short launcher that directs them to this file. It is designed for Codex, Claude Code, Antigravity, and comparable coding agents with authorized GitHub and WordPress access.

Each agent audits the **current authenticated WordPress draft** independently and submits only **public-safe evidence** to `audits/agents/<unique-run-id>/` on its **own branch and pull request**. Public branches and pull requests must never contain unreleased article HTML, verbatim new manuscript quotations, private correspondence, images from protected previews, secrets or WordPress credentials. Keep exact private quotation ledgers and annotated draft diffs outside this public repository. No agent may publish/unhide the article, submit a Zenodo DOI, or edit the central release status directly.

The [agent result schema](AGENT_RESULT_SCHEMA.json) defines machine-readable findings and gate recommendations. Run:

```bash
python3 articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/agents/validate_submission.py \
  articles/joel-dietz-audit-nathan-sweet-bubble-sort-response/audits/agents/<run-id>
```

The GitHub Actions [submission check](../../../../.github/workflows/dietz-independent-audit-submissions.yml) runs on pull requests. Its success establishes only format, provenance-field, gate-coverage and checksum consistency. It does not establish independent replication, scholarly accuracy, privacy or authorization to publish.

**Coordinating results:** Inspect each pull request's reproducible script, exact source versions, command receipts, scope, counterexample and limitations. Compare independently generated results, identify copied/shared dependencies, and resolve conflicts before updating [release_status.json](../release_status.json). Only a coordinator should edit that release ledger. `done` for an editorial gate still requires the applicable human/owner review. A signed-off report can later be included in the article's combined computational-audit ZIP, preserving the original agent/model and source hashes.

**Current publication boundary:** Article #218725796 is unpublished. No article-specific Zenodo DOI has yet been verified; preparing and reviewing audit data is not a release decision.
