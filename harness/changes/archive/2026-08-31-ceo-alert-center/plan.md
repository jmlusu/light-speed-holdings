# Plan

## Technical Approach

1. **AC-1 — Durable store** (`src/ai_company/dashboard/alert_store.py`): `AlertStore` wrapping `FileStore` at the dashboard data root (`dashboard/alerts.json`). Persists a JSON list of fired-alert dicts. Lifecycle states `active / acknowledged / snoozed / cleared`; `snoozed` adds `snoozed_until`. Methods: `add(alerts)` (dedupe same active/snoozed `(rule_name, department, kpi_key, severity)`), `list(status=None)`, `acknowledge(id)`, `snooze(id, until_hours=4)`, `clear(id)`, `clear_all(severity=None)`, plus 30-day retention pruning on write. Concurrency-safe using `FileStore.lock` (matching task/IPC conventions).
2. **AC-2 — API wiring** (`api.py`): `GET /api/v1/alerts` (status/severity filters, returns newest-first); `POST /api/v1/alerts/{id}/ack|/snooze|/clear` behind the existing RBAC key gate (reject unknown id / invalid transition with 400/404, unauthorized with 401/403). Refactor the existing `GET /kpis/alerts` endpoint to persist fired alerts through `AlertStore.add(...)` (additive — it still returns the live evaluation). Add a `run_alert_evaluation()` helper in `data_service.py` that evals the default rules + persists, callable from the KPI scheduler cadence (`kpis/scheduler.py`) so the feed fills without a manual GET.
3. **AC-3 — Frontend** (`templates/index.html` + `static/js/app.js`): an "Alert Center" section on the CEO dashboard — a feed of persisted alerts with severity color badges, status filter tabs, and acknowledge/snooze/clear buttons per row (and clear-all). Subscribe to the existing `alerts` WS topic (via `app.js` dashboard WS) to prepend new fires live. Reuse the existing Tailwind/Alpine styling and `_authFetch` fetch helper.
4. **AC-4 — Tests**: `tests/unit/test_alert_store.py` (dedupe, lifecycle transitions, retention pruning, unknown-id handling) and `tests/unit/test_alert_center_api.py` (list/ack/snooze/clear contract + RBAC deny + persisted-from-eval). Wire `run_alert_evaluation()` into the scheduler with a unit test for the eval+persist path.

## Impacted Modules And Files

- `src/ai_company/dashboard/alert_store.py` (new)
- `src/ai_company/dashboard/data_service.py` (`run_alert_evaluation`)
- `src/ai_company/dashboard/api.py` (`/alerts` CRUD + persist on `/kpis/alerts`)
- `src/ai_company/dashboard/scheduler.py` (or `kpis/scheduler.py`) — alert pass on cadence
- `src/ai_company/dashboard/templates/index.html` + `static/js/app.js` (Alert Center UI)
- `tests/unit/test_alert_store.py`, `tests/unit/test_alert_center_api.py` (new)
- `config/company/` — no change needed (rule set stays in code)
- `docs/STATUS.md`, `CHANGELOG.md` (at close)

## Interfaces, Data, Permissions

- `AlertStore` data shape (`alerts.json`):
  ```json
  {"id": "<uuid>", "rule_name": "…", "department": "…", "kpi_key": "…",
   "current_value": 0.0, "threshold": 0.0, "operator": "gt", "severity": "warning",
   "message": "…", "fired_at": "<iso>", "status": "active",
   "snoozed_until": null, "updated_at": "<iso>"}
  ```
- Endpoints:
  - `GET /api/v1/alerts?status=&severity=` → `{"alerts": [...], "count": n}` (read, run key)
  - `POST /api/v1/alerts/{id}/ack` → 200 `{id, status}`; 400 invalid id; 401/403 RBAC
  - `POST /api/v1/alerts/{id}/snooze?until_hours=4` → 200; 400 invalid id
  - `POST /api/v1/alerts/{id}/clear` → 200; `POST /api/v1/alerts/clear-all` (optional)
- Permissions: read = `DASHBOARD_RUN_KEY`; write (ack/snooze/clear) = `DASHBOARD_APPROVE_KEY` or `DASHBOARD_RUN_KEY` per existing `_check_api_key` tiering. Follow the exact RBAC helper already used by other write endpoints.

## Spec Gaps Found From Planning

- Storage path must mirror `KPIHistoryStore`'s base-dir resolution exactly; confirmed via `get_project_root() / … / dashboard / alerts.json`.
- Write-token tiering: acknowledge/snooze/clear are non-destructive workflow actions; I'll gate them at the same tier as other task lifecycle writes (approve key, falling back to run key) to match existing dashboard conventions.

## Risks And Mitigations

- **Concurrency on `alerts.json`**: single writer with `FileStore.lock`; low write frequency (only on fires/actions) → negligible contention.
- **Feed spam from repeated fires**: dedupe on identical active/snoozed alert prevents duplicate rows.
- **Scheduler double-fire r**ace with manual GET: both routes go through `AlertStore.add` dedupe, so overlapping evaluations are idempotent.
- **Frontend scope creep**: restrict to the minimal feed + lifecycle; no rule-config UI (non-goal).

## Verification Plan

- `ruff check src/` and `mypy src/` clean.
- New suites: `pytest tests/unit/test_alert_store.py tests/unit/test_alert_center_api.py` (plus eval+persist test).
- Regression: `test_dashboard_api_response`, `test_kpi_collectors`, `test_company_kpis`, `test_data_service`, `test_scheduler_daemon`.
- `pwsh scripts/lint-ecl.ps1` passes; close ECL with status update in `docs/STATUS.md` + `CHANGELOG.md`.
