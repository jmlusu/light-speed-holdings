---
title: "Marketing Site Analytics Governance and Durable Journey Events"
slug: "marketing-site-analytics-governance-and-durable-journey-events"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "accepted"
spec_review: "approved"
plan_review: "approved"
modules:
  - "dashboard"
  - "data"
  - "cli"
  - "vercel-edge"
files:
  - "src/ai_company/dashboard/journey_event_store.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/data/governance.py"
  - "src/ai_company/cli/dashboard.py"
  - "api/journey-events.ts"
  - "vite.config.ts"
  - "tests/unit/test_journey_event_store.py"
  - "tests/unit/test_port_assignments.py"
tags:
  - "marketing-site"
  - "journey-events"
  - "data-governance"
  - "ports"
  - "p0"
validation_status: "pass"
validation_results:
  - "lint-ecl.ps1: PASS"
  - "ruff check (new/changed files): PASS"
  - "mypy src (journey_event_store.py, governance.py): PASS"
  - "pytest test_journey_event_store.py + test_alert_store.py + test_port_assignments.py: 22 passed"
created_at: "2026-10-11"
updated_at: "2026-10-11"
session_id: "ad74f022-3f32-4d40-b0c4-13e78fc670dc"
owner_agent: "jmlus"
claimed_at: "2026-10-11"
---

# Summary

## Outcome

All four P0 actions landed under the LIGHTSPEED task lock:

- **A1 durable journey-event store**: `JourneyEventStore` (FileStore JSON, 400-day retention, AlertStore pattern) at `<state base>/dashboard/journey_events.json`; dashboard `POST`/`GET` `/api/v1/marketing-site/journey-events` endpoints; Vercel edge function `api/journey-events.ts` now best-effort forwards to `DASHBOARD_INGEST_URL` (2000 ms timeout, optional `X-API-Key` via `DASHBOARD_INGEST_KEY`) with in-memory fallback; response surfaces `dataQuality: 'file' | 'none'`.
- **A2 governance registration**: `marketing_site_events` registered in `DEFAULT_POLICIES` (owner `cmo`, `INTERNAL`, 400 days, `ARCHIVE`) with `_TIMESTAMP_COLUMNS` entry and `DEFAULT_OWNERS` Marketing owner.
- **G-1 port-guard test**: `tests/unit/test_port_assignments.py` locks the 1440/1441 vs 8420/8421 contract (7/7 pass).
- **G-2 + G-3 runtime guards**: dashboard CLI refuses 1440/1441; Vite `dashboardPortGuard()` refuses 8420/8421.

## Decisions

- Ingest path is authenticated by dashboard API-key middleware only (no `require_role` on POST), matching the webhook machine-to-machine pattern; GET requires `require_role("run")`.
- Edge forwards are best-effort (non-fatal on failure); durability is reported as `none` until the operator sets `DASHBOARD_INGEST_URL` + a valid `DASHBOARD_INGEST_KEY`.
- Pre-existing ruff BLE001 at `api.py:2505` (webhook handler) left untouched per task-lock scope.
- G-4 PM2 path, G-5 identity assertion, G-6 frontend CI guard, G-7 prod risk note, and A4–A7 logged as P1/out-of-scope follow-ups (G-5 belongs to a concurrent session's change).

## Validation

- `pwsh scripts/maintenance/lint-ecl.ps1`: PASS (historical slug-collision warnings only; none for this slug).
- `uv run ruff check` on new/changed files: PASS.
- `uv run mypy src/ai_company/dashboard/journey_event_store.py src/ai_company/data/governance.py`: PASS.
- `uv run pytest tests/unit/test_journey_event_store.py tests/unit/test_alert_store.py tests/unit/test_port_assignments.py -q`: 22 passed.
- `api/journey-events.ts` re-read and verified: constants + `forwardToDashboard()` + `dataQuality` in handler/response.

## Next Step

- None - change closed. Operator follow-up: set `DASHBOARD_INGEST_URL` and `DASHBOARD_INGEST_KEY` (matching a configured dashboard RBAC key) before production; without them the edge keeps `dataQuality: none` (in-memory fallback only).
