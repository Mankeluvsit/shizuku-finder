# shizuku-finder

`shizuku-finder` is the refactored successor to `app-crawler`.
It is now a modular Shizuku discovery crawler, reporting pipeline, and automation-friendly Python package with multi-source discovery, SQLite-backed history, structured filtering, diff artifacts, and scheduled publication support.

## Current implementation status

The repository currently includes:
- package structure under `src/shizuku_finder/`
- multi-source scanners for F-Droid, IzzyOnDroid, GitHub code search, GitHub metadata, GitLab, and Codeberg
- failure-aware orchestration that keeps successful scanner output even when one scanner fails
- known-app suppression against a checked-out target list repository
- normalization, dedupe, source precedence, and calibrated confidence scoring
- SQLite-backed historical state for diff generation between runs
- generated artifacts:
  - `SUMMARY.md`
  - `REVIEW_NEEDED.md`
  - `DIFF.md`
  - `DIFF.json`
  - `summary.json`
  - `summary.csv`
  - `RUN_SUMMARY.json`
- CI workflow with Ruff, mypy, and pytest
- scheduled scan workflow with publication hardening and GitHub job summary output
- fixture-driven and end-to-end tests covering scanners, pipeline behavior, reporting, workflow expectations, and storage

## Generated artifacts

- `SUMMARY.md`: grouped human-readable report with source and confidence details
- `REVIEW_NEEDED.md`: items that require manual inspection
- `DIFF.md`: markdown diff between the previous and current run
- `DIFF.json`: machine-readable diff payload
- `summary.json`: machine-readable full result set
- `summary.csv`: spreadsheet-friendly export
- `RUN_SUMMARY.json`: machine-readable run status, counts, and scanner failures

## Development

Install locally:

```bash
python -m pip install -e .[dev]
```

Run tests:

```bash
pytest
```

Run the scan command:

```bash
python -m shizuku_finder scan
```

Example with explicit output paths:

```bash
python -m shizuku_finder scan \
  --target-list-path ./list \
  --summary-file SUMMARY.md \
  --json-file summary.json \
  --csv-file summary.csv \
  --review-file REVIEW_NEEDED.md \
  --diff-file DIFF.md \
  --diff-json-file DIFF.json \
  --run-summary-file RUN_SUMMARY.json
```

## Status

Implementation tracking remains in `docs/roadmap.md`.
The current codebase is in late-stage refinement rather than early scaffolding.
