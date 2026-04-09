# Roadmap

_Last updated: 2026-04-09_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 78% |
| 2. Scanner migration and orchestration | 72% |
| 3. Filtering, evidence, confidence | 62% |
| 4. Output redesign and diffing | 58% |
| 5. Workflow automation and publication | 48% |
| 6. New source expansion | 52% |
| 7. Testing and cutover readiness | 48% |

**Overall estimated completion:** 63%

## Current pass highlights
- Added a second new external source beyond the original scope: **Codeberg**.
- Integrated Codeberg scanning into the active CLI pipeline.
- Extended source precedence to cover Codeberg.
- Added reporting-oriented tests covering grouped summary/review output and diff sections.
- Increased validation around normalization, scoring, diffing, README indexing, repo cache inspection, and reporting.

## Next pass targets
- improve GitLab and Codeberg pagination/resilience
- add workflow validation and stronger CI assertions
- refine confidence/source precedence further
- add more end-to-end and snapshot-style tests
