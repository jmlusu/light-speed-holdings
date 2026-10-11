# Tasks

## Format

- `- [ ] T001 [P?] [US?] Action with target path and validation note`
- `[P]` means parallel-safe. `[US1]` maps to a user story when stories exist.

## Setup / Intake

- [x] T001 Review `spec.md` and `plan.md` gates before implementation.

## Implementation

- [x] T002 [P] A2: register `marketing_site_events` in `src/ai_company/data/governance.py` (policy + timestamp column + owner). Validation: mypy + import check.
- [x] T003 [P] A1: create `src/ai_company/dashboard/journey_event_store.py` (`JourneyEventStore`, 400-day retention, `get_journey_event_store()`). Validation: `pytest tests/unit/test_journey_event_store.py`.
- [x] T004 A1: add `POST`/`GET` `/marketing-site/journey-events` to `src/ai_company/dashboard/api.py` (before `/kpis/collect`). Validation: ruff + mypy.
- [x] T005 A1: update `api/journey-events.ts` with `DASHBOARD_INGEST_URL`/`KEY`/`TIMEOUT_MS`, `forwardToDashboard()`, `dataQuality` in response. Validation: re-read file.
- [x] T006 [P] G-1: add `tests/unit/test_port_assignments.py` locking 1440/1441 vs 8420/8421. Validation: 7/7 pass.
- [x] T007 G-2: refuse 1440/1441 in `src/ai_company/cli/dashboard.py`. Validation: covered by G-1 tests.
- [x] T008 G-3: `dashboardPortGuard()` in `vite.config.ts` refuses 8420/8421. Validation: covered by G-1 tests.

## Validation

- [x] T009 Record `validation_results` in summary.md; run lint-ecl, ruff, mypy, targeted pytest; close via `harness-change.ps1 close completed`.

## Deferred Tasks

- Deferred: G-4 PM2 hardcoded `vite.exe` path (`ecosystem.config.cjs`); G-5 identity assertion (`scripts/dev/health-check.ps1` — concurrent session); G-6 frontend CI guard; G-7 prod risk note; A4–A7 deeper analytics follow-ups. Classification: OUT-OF-SCOPE / OPTIONAL under the LIGHTSPEED task lock.
