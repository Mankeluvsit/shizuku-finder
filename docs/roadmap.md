# Roadmap

_Last updated: 2026-04-09_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 70% |
| 2. Scanner migration and orchestration | 55% |
| 3. Filtering, evidence, confidence | 25% |
| 4. Output redesign and diffing | 0% |
| 5. Workflow automation and publication | 40% |
| 6. New source expansion | 0% |
| 7. Testing and cutover readiness | 25% |

**Overall estimated completion:** 46%

## Current pass highlights
- Ported GitHub metadata scanner with local clone/cache inspection.
- Added repo cache utility for shallow clone reuse and signature scanning.
- Wired CLI to run F-Droid, IzzyOnDroid, GitHub code, and GitHub metadata scanners.
- Added target-list filtering through README index service.
- Made scheduled workflow support configurable target-list checkout.
- Added tests for README indexing and repo cache text detection.

## Next pass targets
- Improve scanner resilience and client boundaries.
- Implement canonical normalization and source precedence.
- Start output redesign and diff report generation.
- Add at least one new source beyond the original scope.
