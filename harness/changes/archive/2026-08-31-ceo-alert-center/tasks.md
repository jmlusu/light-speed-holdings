# Tasks

## Setup / Intake

- [x] T001 [P0] Review `spec.md` and `plan.md`; mark intake done, phase `plan`, run Plan Review.

## Implementation — AC-1 Durable alert store

- [x] T002 [P1] [US1] Add `src/ai_company/dashboard/alert_store.py` — `AlertStore` with FileStore-backed `add` (dedupe active/snoozed by rule_name+department+kpi_key+severity), `list_alerts(status=None)`, `acknowledge`, `snooze(until_hours)`, `clear`, `clear_all`, and 30-day retention pruning; lifecycle states `active/acknowledged/snoozed/cleared`.

## Implementation — AC-2 API wiring

- [x] T003 [P1] [US1] Add `run_alert_evaluation()` to `src/ai_company/dashboard/data_service.py` — evaluate the 7 default `AlertRule`s via `AlertEngine` against `collect_all_kpis()` and persist fired alerts through `AlertStore.add` (idempotent).
- [x] T004 [P1] [US1] Add `GET /api/v1/alerts` (status/severity filters, newest-first) and `POST /api/v1/alerts/{id}/ack|/snooze|/clear` (+ `clear-all`) in `src/ai_company/dashboard/api.py`, gated by the existing dashboard RBAC key tier.
- [x] T005 [P1] [US1] Refactor `GET /kpis/alerts` in `api.py` to persist fired alerts via `AlertStore.add` (additive — still returns live evaluation) + live WS broadcast; wire `run_alert_pass()` into the KPI scheduler cadence.

## Implementation — AC-3 Frontend

- [x] T006 [P2] [US1] Add an Alert Center section to `src/ai_company/dashboard/templates/index.html` + `static/js/app.js`: persisted-alert feed with severity badges, status filter tabs, per-row acknowledge/snooze/clear, and live prepend via the existing `alerts` WebSocket topic.

## Validation

- [x] T007 [P1] Add `tests/unit/test_alert_store.py` (dedupe, lifecycle transitions, retention pruning, unknown-id) and `tests/unit/test_alert_center_api.py` (list/ack/snooze/clear contract + persisted-from-eval).
- [x] T008 [P1] Verify: `ruff check src/`, `mypy src/`, targeted `pytest` (new suites + dashboard/KPI/scheduler regression) green; `pwsh scripts/lint-ecl.ps1` passes; close ECL (update `docs/STATUS.md`, `CHANGELOG.md`).

## Deferred Tasks

- Deferred — multi-channel alert delivery (SMS/webhook) + 5-tier escalation routing: separate escalation ECL (Phase 3 roadmap).
