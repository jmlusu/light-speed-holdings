# Plan

## Technical Approach

- **C5 ReportStore (`src/ai_company/store/report_store.py`, new):** a read-only
  queryable index over report bundles. Walks immediate subdirectories of the
  configured root plus root-level shards; `normalize_timestamp()` parses ISO-8601
  (naive → UTC, `Z` → UTC, explicit offsets preserved) and epoch seconds;
  `Report` dataclass exposes `to_dict()` for JSON transport. `reports()` returns
  newest-first with undated-at-the-end; `latest(n, **filters)` / `oldest(n,
  **filters)` apply bundle/name/agent substring filters. Missing root and
  malformed files are handled defensively (skipped, never raising).
- **C4 Reports API (`api.py`):** `GET /api/v1/reports` uses `ReportStore().latest`
  with over-fetch-then-filter to drop root `cost_log.jsonl` shards by default
  (`include_cost=true` to include) and applies an optional `agent` filter.
  `GET /api/v1/reports/content?path=` resolves the requested path against the
  store root, verifies containment (404 on escape), restricts suffixes to
  `.json`/`.jsonl`, and parses via `_read_documents`.
- **C4 Task Flow API (`api.py`):** `GET /api/v1/tasks/{task_id}/flow` reads the
  task (404 if unknown) and walks `.opencode/audit` via `_get_store().iter_jsonl`
  to collect events that reference the task id; events are de-duplicated by
  (type, timestamp, agent) and sorted chronologically, with created/updated
  status-event fallback from the task's own timestamps.
- **C4 Pages/UI:** `templates/reports.html` (list + content side drawer) and
  `templates/task-flow.html` (task-id trace + timeline); `/reports` and
  `/task-flow` routes plus the two nav tabs in `app.py`; `app.js` adds
  `loadReports()`, `openReport(path)`, `loadTaskFlow(id)`, the supporting data
  fields, and the `/reports` branch in `loadWebPage`/`loadPageData`.

## Impacted Modules And Files

- NEW `src/ai_company/store/report_store.py`
- NEW `tests/unit/test_report_store.py`
- NEW `src/ai_company/dashboard/templates/reports.html`
- NEW `src/ai_company/dashboard/templates/task-flow.html`
- NEW `docs/DASHBOARD-HARDENING-C4-C5-SPEC.md` (record of the approved spec)
- MOD `src/ai_company/dashboard/api.py` (reports + task-flow endpoints)
- MOD `src/ai_company/dashboard/app.py` (routes + tabs)
- MOD `src/ai_company/dashboard/static/js/app.js` (view wiring)
- MOD `tests/integration/test_dashboard_api.py` (C4 integration tests)

## Interfaces, Data, Permissions

- Two new read-only REST endpoints under `/api/v1/reports` and
  `/api/v1/reports/content` plus `GET /api/v1/tasks/{task_id}/flow`. All are
  subject to the router's global RBAC auth; no writes, no permission changes.
- Report paths are user-supplied query params; served content is confined to the
  reports root to prevent traversal (SECURITY).
- No data-model or schema changes; `results/` files stay the single source of
  truth (read-only).

## Spec Gaps Found From Planning

- The root `cost_log.jsonl` shard would pollute a plain "reports" listing with
  duplicate-name cost records; resolved by filtering bundle "." cost shards by
  default with an opt-in flag.
- `Report.path` resolves to an absolute path; the content endpoint re-resolves it
  against the root and the containment check still guards traversal, so both
  absolute and relative `path` values work.

## Risks And Mitigations

- **Concurrent writer on shared dashboard files** (`api.py`, `app.py`,
  `app.js`): the implementing session scoped writes; verified no overlap with
  the (now archived) `cleanup-dummy-tasks` change.
- **Audit-trail events may not key by task id for every task**, so some task
  flows have an empty timeline; mitigated with a created/updated status-event
  fallback so the page still renders meaningfully.
- **Full-suite pytest could not complete within the rollout timeout**; targeted
  dashboard/store suites are green and a full-suite gate remains before archive.

## Verification Plan

- `ruff check src/` — PASS (clean).
- `mypy src/` (strict) — PASS.
- Targeted `pytest tests/unit/test_report_store.py tests/integration/test_dashboard_api.py`
  — PASS (34 tests).
- Broader dashboard regression (`tests/unit` dashboard + store + backlog) —
  PASS (224 tests).
- Live smoke via TestClient over real `results/` — endpoints and pages return
  200 with expected markers.
- Pending gate before archive: full `pytest -q -m "not e2e"`.
