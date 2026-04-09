# Roadmap

_Last updated: 2026-04-09_

This roadmap is the implementation tracking document for `shizuku-finder`.
It is intended to be updated whenever a meaningful implementation milestone lands.

## Progress summary

| Phase | Title | Status | Completion |
|---|---|---:|---:|
| 1 | Foundation and repository bootstrap | In progress | 45% |
| 2 | Core crawler architecture and real scanner migration | Not started | 0% |
| 3 | Filtering, evidence, confidence, and review workflows | Not started | 0% |
| 4 | Output redesign, diffing, and reporting polish | Not started | 0% |
| 5 | Workflow automation, publication, and operational hardening | In progress | 20% |
| 6 | Source expansion and ecosystem coverage | Not started | 0% |
| 7 | Testing, validation, and cutover readiness | Not started | 0% |

**Overall estimated completion:** 18%

---

## Phase 1 — Foundation and repository bootstrap
**Status:** In progress  
**Completion:** 45%

### Objective
Create the new `shizuku-finder` repository structure, package layout, project tooling, and planning/documentation baseline so the refactor can proceed in a clean and extensible way.

### Completed
- Initialized `shizuku-finder` repository.
- Added `pyproject.toml` with package metadata and development tooling scaffolding.
- Added `.gitignore` and `.env.example`.
- Added initial package files under `src/shizuku_finder/`.
- Added initial CLI entrypoint and seed pipeline.
- Added SQLite-backed storage scaffold.
- Added initial markdown, JSON, CSV, and review-needed report writers.
- Added CI workflow and Dependabot configuration.
- Added planning files:
  - `docs/change-requests.md`
  - `docs/feature-backlog.md`
  - `docs/roadmap.md`
  - `docs/migration-plan.md`
- Added seed structured ignore rules file.
- Added first automated test to prove output generation and DB creation.

### Remaining
- Replace placeholder README with a real project overview.
- Add richer package documentation and usage examples.
- Expand test scaffolding beyond the single smoke test.
- Add development ergonomics such as formatter/type-check hooks if retained in final toolchain.

### Exit criteria
This phase is complete when the repository is fully self-describing, installable, and ready for real scanner code to replace placeholder seed behavior.

---

## Phase 2 — Core crawler architecture and real scanner migration
**Status:** Not started  
**Completion:** 0%

### Objective
Replace the seed pipeline with the actual crawler engine and migrate the existing scanners from `app-crawler` into the new package architecture.

### Scope
- Port F-Droid scanner logic.
- Port GitHub code scanner logic.
- Port GitHub metadata scanner logic.
- Introduce proper scanner interfaces and orchestration flow.
- Move network and GitHub access behind cleaner client/service layers.
- Eliminate direct script-style orchestration from the old design.

### Planned implementation details
- Add scanner base abstractions.
- Introduce orchestrator service to coordinate all sources.
- Normalize app records from all scanners into a unified domain model.
- Preserve and improve current discovery capability while accepting approved behavior changes.

### Exit criteria
This phase is complete when `python -m shizuku_finder scan` produces real scan results from supported sources instead of placeholder seed data.

---

## Phase 3 — Filtering, evidence, confidence, and review workflows
**Status:** Not started  
**Completion:** 0%

### Objective
Improve result quality by building structured filtering, evidence capture, confidence scoring, and manual review routing into the scan pipeline.

### Scope
- Replace flat ignore handling with structured rule processing.
- Rebuild known-app filtering against the target list repository.
- Capture evidence for each match.
- Add confidence scoring system.
- Route uncertain findings into review-needed outputs.

### Planned implementation details
- Build README/list indexing service.
- Implement canonical URL and name normalization.
- Store per-app evidence entries and confidence contributions.
- Add structured exclusion reasons and categories.
- Introduce clearer duplicate handling and source precedence.

### Exit criteria
This phase is complete when every reported app has traceable matching evidence, a confidence score, and a deterministic filtering path.

---

## Phase 4 — Output redesign, diffing, and reporting polish
**Status:** Not started  
**Completion:** 0%

### Objective
Replace the old summary-only mindset with a multi-output reporting layer that supports human review, machine consumption, and change tracking between runs.

### Scope
- Redesign `SUMMARY.md`.
- Improve review-needed output.
- Finalize JSON and CSV schema.
- Add run-to-run diff reporting.
- Improve sectioning, grouping, and confidence visibility in outputs.

### Planned implementation details
- Split confirmed vs review-needed findings clearly.
- Group or annotate results by confidence, source, or release status as appropriate.
- Generate diff artifacts showing new, changed, and removed findings.
- Keep outputs deterministic for testing and automation.

### Exit criteria
This phase is complete when the reporting layer is stable enough to serve as the canonical output surface for both users and automation.

---

## Phase 5 — Workflow automation, publication, and operational hardening
**Status:** In progress  
**Completion:** 20%

### Objective
Refactor the old automation model into workflows that match the new architecture, while preserving scheduled execution and publication behavior in a cleaner form.

### Completed
- Added base CI workflow.
- Added first scheduled scan workflow scaffold.
- Added Dependabot configuration.

### Remaining
- Wire the workflow to the real CLI pipeline once scanners are migrated.
- Make target-list checkout configurable instead of hardcoded.
- Decide final publication flow for generated outputs.
- Ensure cache restore/save behavior works with the new SQLite-backed approach.
- Harden workflow behavior around failures, partial results, and non-changes.

### Exit criteria
This phase is complete when the repository can run scheduled scans end-to-end in GitHub Actions and publish results without relying on placeholder data or brittle upstream assumptions.

---

## Phase 6 — Source expansion and ecosystem coverage
**Status:** Not started  
**Completion:** 0%

### Objective
Implement the approved change request to expand discovery beyond the original sources where those sources are reliable and worth maintaining.

### Candidate sources
- GitLab
- Codeberg
- Additional F-Droid-compatible indexes
- Other curated Android app sources that provide reproducible and inspectable data

### Constraints
- New sources must support consistent crawling.
- Match evidence must be capturable.
- False-positive rates must be manageable.
- The source must fit the confidence-scoring model.

### Exit criteria
This phase is complete when at least one additional source beyond the original `app-crawler` scope has been integrated and validated.

---

## Phase 7 — Testing, validation, and cutover readiness
**Status:** Not started  
**Completion:** 0%

### Objective
Validate the refactored system thoroughly enough that it can replace the old workflow with confidence.

### Scope
- Expand unit tests.
- Add integration coverage for scanners and outputs.
- Add regression comparisons against representative legacy behavior where useful.
- Validate workflow execution paths.
- Confirm database and output stability.

### Planned implementation details
- Add fixture-based tests for scanner normalization.
- Add snapshot tests for markdown and review outputs.
- Add tests for ignore rules, confidence scoring, and evidence serialization.
- Add end-to-end run validation in CI where practical.

### Exit criteria
This phase is complete when `shizuku-finder` is ready to act as the primary maintained crawler/report pipeline.

---

## Update protocol

This file should be updated whenever one of the following happens:
- a phase completion percentage changes materially;
- a new implementation milestone lands;
- a phase moves from not started to in progress or from in progress to complete;
- scope is added, deferred, or removed;
- workflow/publication strategy changes.

### Update rules
- Keep percentages realistic rather than optimistic.
- Update the **overall estimated completion** whenever any phase percentage changes.
- Add newly completed work into the relevant phase’s **Completed** section.
- Add newly identified work into the relevant phase’s **Remaining** or **Scope** section.
- Do not silently remove scope; if scope changes, rewrite the phase description clearly.
