# Roadmap

_Last updated: 2026-04-09_

## Progress summary

| Phase | Completion |
|---|---:|
| 1. Foundation and bootstrap | 76% |
| 2. Scanner migration and orchestration | 68% |
| 3. Filtering, evidence, confidence | 58% |
| 4. Output redesign and diffing | 45% |
| 5. Workflow automation and publication | 48% |
| 6. New source expansion | 35% |
| 7. Testing and cutover readiness | 38% |

**Overall estimated completion:** 58%

## Current pass highlights
- Added a new source beyond the original scope: **GitLab**.
- Integrated GitLab scanning into the active CLI pipeline.
- Added source precedence during normalization/deduping.
- Added normalization utility coverage.
- Added review-classification coverage.
- Continued progress on confidence and source-quality handling.

## Next pass targets
- improve GitLab scanner resilience and paging
- add at least one more external source or deeper source controls
- add output snapshot tests and workflow validation
- refine confidence/source precedence further
