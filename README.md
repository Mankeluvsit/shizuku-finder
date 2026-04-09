# shizuku-finder

`shizuku-finder` is the refactored successor to `app-crawler`.
It is being rebuilt as a modular Shizuku discovery crawler, reporting pipeline, and automation-friendly Python package.

## Current implementation status

The repository currently includes:
- package structure under `src/shizuku_finder/`
- CLI entrypoint for scan execution
- SQLite-backed storage scaffold
- markdown, JSON, CSV, and review-needed report writers
- structured ignore-rule loading
- scanner base abstraction
- first migrated real scanner: F-Droid
- orchestration service for scanner aggregation
- CI and scheduled workflow scaffolding
- planning and migration documents

## Immediate next steps

1. Wire the CLI into the orchestrator path.
2. Port the GitHub code scanner.
3. Port the GitHub metadata scanner.
4. Rebuild known-app filtering against the target list repository.
5. Expand confidence, evidence, and diff reporting.

## Development

Install locally:

```bash
python -m pip install -e .[dev]
```

Run tests:

```bash
pytest
```

Run the current scan command:

```bash
python -m shizuku_finder scan
```
