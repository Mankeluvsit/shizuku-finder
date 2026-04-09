# Roadmap

_Last updated: 2026-04-09_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 74% |
| 2. Scanner migration and orchestration | 60% |
| 3. Filtering, evidence, confidence | 45% |
| 4. Output redesign and diffing | 45% |
| 5. Workflow automation and publication | 48% |
| 6. New source expansion | 0% |
| 7. Testing and cutover readiness | 32% |

**Overall estimated completion:** 54%

## Current pass highlights
- Added normalization helpers for names and URLs.
- Added review-needed classification based on confidence and download availability.
- Added run diffing support with added/removed/changed sections.
- Upgraded reporting to show confidence values and review grouping.
- Extended SQLite storage to persist and reload review state.
- Added diff artifact generation to the active CLI path.
- Extended scheduled workflow to publish `DIFF.md`.
- Added diff test coverage.

## Next pass targets
- Add at least one new source beyond the original scope.
- Improve source precedence and stronger confidence logic.
- Add output snapshot tests and more workflow validation.
