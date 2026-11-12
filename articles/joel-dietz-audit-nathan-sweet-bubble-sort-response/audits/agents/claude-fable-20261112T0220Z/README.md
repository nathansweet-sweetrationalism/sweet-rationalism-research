# Run `claude-fable-20261112T0220Z`

Start with `report.md` (findings) or `PROGRESS.md` (stage-by-stage log). `result.json` is the machine-readable submission.

## Reproduce (Python 3.10+, standard library only, network required)

Run from this directory:

```
python scripts/package_check.py ../../.. <empty work dir> out_package.json
python scripts/independent_checks.py <cache dir> out_independent.json
python scripts/public_text_checks.py out_text.json
```

`panel_checks.py`, `proposed_prompt_patch.py` and `link_doi_check.py` need the private draft (or its link list). They are included so the coordinator can rerun them with authorized access. `build_result.py` assembles `result.json` from `logs/`.

No upstream code is executed by any script here. The scripts are original to this audit and offered under the repository licence. Live results depend on third-party hosts (GitHub raw, PubMed, Crossref, Substack) and may change; hashes of what was retrieved are in the receipts.

`.gitattributes` in this directory turns off line-ending conversion so that `SHA256SUMS.txt` matches on every platform.
