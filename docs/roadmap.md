# Roadmap

_Last updated: 2026-04-09_

This file tracks implementation progress for `shizuku-finder` and should be updated whenever material work lands.

## Progress summary

| Phase | Title | Status | Completion |
|---|---|---:|---:|
| 1 | Foundation and repository bootstrap | In progress | 65% |
| 2 | Core crawler architecture and real scanner migration | In progress | 35% |
| 3 | Filtering, evidence, confidence, and review workflows | In progress | 15% |
| 4 | Output redesign, diffing, and reporting polish | Not started | 0% |
| 5 | Workflow automation, publication, and operational hardening | In progress | 20% |
| 6 | Source expansion and ecosystem coverage | Not started | 0% |
| 7 | Testing, validation, and cutover readiness | In progress | 15% |

**Overall estimated completion:** 36%

---

## Phase 1 — Foundation and repository bootstrap
**Status:** In progress  
**Completion:** 65%

### Completed
- Repository initialized and packaged with `pyproject.toml`.
- Added `.gitignore`, `.env.example`, README, and planning docs.
- Added core domain models, config, storage, reporting, and CLI modules.
- Added CI workflow, scheduled workflow scaffold, and Dependabot.
- Added initial test coverage for CLI output, ignore rules, and orchestrator filtering.

### Remaining
- Expand package docs and usage examples.
- Add more development ergonomics and broader test coverage.

---

## Phase 2 — Core crawler architecture and real scanner migration
**Status:** In progress  
**Completion:** 35%

### Completed
- Added scanner base abstraction.
- Added orchestrator service.
- Ported F-Droid scanner.
- Ported GitHub code scanner.
- Rewired CLI to run real scanners through the orchestrator.

### Remaining
- Port GitHub metadata scanner.
- Add cleaner client/service boundaries for GitHub and HTTP operations.
- Remove remaining placeholder assumptions from scan flow.

---

## Phase 3 — Filtering, evidence, confidence, and review workflows
**Status:** In progress  
**Completion:** 15%

### Completed
- Added structured ignore-rule loader.
- Added README index for known-app filtering.
- Added filtering service for target-list suppression.
- Added initial evidence model and orchestrator-level ignore filtering.

### Remaining
- Implement canonical normalization and source precedence.
- Expand confidence scoring.
- Add deterministic review-needed routing.
- Rebuild legacy known-app behavior more completely.

---

## Phase 4 — Output redesign, diffing, and reporting polish
**Status:** Not started  
**Completion:** 0%

### Remaining
- Redesign `SUMMARY.md`.
- Add diff reports between runs.
- Finalize reporting schema and grouping.

---

## Phase 5 — Workflow automation, publication, and operational hardening
**Status:** In progress  
**Completion:** 20%

### Completed
- Added CI workflow.
- Added scheduled scan workflow scaffold.
- Added Dependabot configuration.

### Remaining
- Wire workflows to the real pipeline and target-list checkout.
- Finalize publication behavior and cache persistence strategy.
- Harden failure handling.

---

## Phase 6 — Source expansion and ecosystem coverage
**Status:** Not started  
**Completion:** 0%

### Remaining
- Add at least one approved new source beyond the original scope.
- Validate new source evidence quality and false-positive rate.

---

## Phase 7 — Testing, validation, and cutover readiness
**Status:** In progress  
**Completion:** 15%

### Completed
- Added early smoke and service-level tests.

### Remaining
- Add scanner fixtures, output snapshots, and end-to-end validation.
- Verify workflow behavior and report stability.

---

## Update protocol

Update this file whenever:
- a phase percentage changes materially;
- a new milestone lands;
- a phase changes status;
- scope is added, deferred, or removed.
