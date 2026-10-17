# Plan

## Technical Approach

- A1: `JourneyEventStore` wrapping `FileStore` (same pattern as `AlertStore`); singleton `get_journey_event_store()`; retention prune on write; dashboard API router endpoints before `/kpis/collect`; edge `forwardToDashboard()` with AbortController + optional `X-API-Key`.
- A2: single-file edit to `governance.py` — timestamp column map, default retention policy, default owners.
- G-1: pure-Python port contract tests reading `vite.config.ts`, `ecosystem.config.cjs`, `docker-compose*.yml`, and refusing-ports helpers.
- G-2/G-3: small fail-fast guards at CLI arg parse and Vite config load.

## Impacted Modules And Files

- `src/ai_company/dashboard/journey_event_store.py` (new)
- `src/ai_company/dashboard/api.py` (endpoints)
- `src/ai_company/data/governance.py` (A2)
- `src/ai_company/cli/dashboard.py` (G-2)
- `api/journey-events.ts` (A1 edge)
- `vite.config.ts` (G-3)
- `tests/unit/test_journey_event_store.py` (new)
- `tests/unit/test_port_assignments.py` (G-1)

## Interfaces, Data, Permissions

- `POST /api/v1/marketing-site/journey-events` — body: event object or list; requires `eventType`/`route`/`timestamp`; middleware API-key; returns `{status,count,ids}` 201.
- `GET /api/v1/marketing-site/journey-events?event_type=&route=&limit=` — `require_role("run")`; returns `{events,count,total}`.
- Env: `DASHBOARD_INGEST_URL`, `DASHBOARD_INGEST_KEY` (optional), `DASHBOARD_INGEST_TIMEOUT_MS` (default 2000).
- Store file: `<state base>/dashboard/journey_events.json`; retention 400 days.

## Spec Gaps Found From Planning

- None blocking.

## Risks And Mitigations

- Edge forward failure must not drop analytics: fall back to in-memory buffer and report `dataQuality: none`.
- Port guard false positives: only reject the exact dashboard ports on Vite and the exact marketing ports on the dashboard CLI.
- Concurrent session edits: health-check.ps1 and registry health lines left untouched (G-5 OUT-OF-SCOPE).

## Verification Plan

- `pwsh scripts/maintenance/lint-ecl.ps1`
- `uv run ruff check` on new/changed files
- `uv run mypy` on `journey_event_store.py` + `governance.py`
- `uv run pytest tests/unit/test_journey_event_store.py tests/unit/test_alert_store.py tests/unit/test_port_assignments.py -q`
- Re-read `api/journey-events.ts` for constants + forward + dataQuality
