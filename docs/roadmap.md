# Roadmap

_Last updated: 2026-04-09_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 84% |
| 2. Scanner migration and orchestration | 84% |
| 3. Filtering, evidence, confidence | 70% |
| 4. Output redesign and diffing | 58% |
| 5. Workflow automation and publication | 62% |
| 6. New source expansion | 52% |
| 7. Testing and cutover readiness | 80% |

**Overall estimated completion:** 74%

## Current pass highlights
- Added fixture-driven validation for the F-Droid scanner.
- Added SQLite round-trip validation for persisted review-needed state.
- Refactored the F-Droid scanner to support direct fixture parsing for deterministic tests.
- Increased confidence in scanner correctness and storage stability without relying on live network responses.

## Next pass targets
- stronger end-to-end scan assertions
- better error reporting and confidence calibration
- more fixture-driven validation for non-F-Droid scanners
