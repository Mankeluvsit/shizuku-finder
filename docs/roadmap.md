# Roadmap

_Last updated: 2026-04-09_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 82% |
| 2. Scanner migration and orchestration | 79% |
| 3. Filtering, evidence, confidence | 62% |
| 4. Output redesign and diffing | 58% |
| 5. Workflow automation and publication | 62% |
| 6. New source expansion | 52% |
| 7. Testing and cutover readiness | 66% |

**Overall estimated completion:** 71%

## Current pass highlights
- Added reusable HTTP and GitHub client wrappers to improve client boundaries.
- Refactored GitHub, GitLab, and Codeberg scanners toward shared client usage.
- Added client-level tests for HTTP payload coercion and disabled GitHub behavior.
- Continued reducing scanner-specific network handling duplication.

## Next pass targets
- fixture-driven scanner validation
- stronger filtering parity work
- better error reporting and confidence calibration
- broader end-to-end scan tests
