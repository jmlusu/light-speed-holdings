# Spec

## Intake Review

- Intake type: Structured Change
- Input shape: requirement-first (CEO-level 500-word review + task-lock P0 actions)
- Questions asked this round: 0

## Goal And Evidence

- Real problem or user request: Marketing-site journey events were fire-and-forget to a Vercel edge function with no durable backend store, no governance retention, and no port-boundary guards between the Marketing Site (1440/1441) and CEO Dashboard (8420/8421).
- Current behavior: Edge function buffered events in memory only; `marketing_site_events` absent from retention policies; no tests locking the port contract; dashboard CLI and Vite config accepted the other product's ports.
- Source of evidence: A1–A3 audit from the active ECL review; code at `api/journey-events.ts`, `src/ai_company/dashboard/api.py`, `src/ai_company/data/governance.py`, `src/ai_company/cli/dashboard.py`, `vite.config.ts`.

## User Scenarios And Success

- Primary user/system scenario: Journey events POSTed from the marketing site (1441/1440) land on the dashboard ingest endpoint and persist to a FileStore JSON file with 400-day retention; governance knows the table, owner, and retention action; port misuse fails fast in tests and at runtime.
- Success criteria: A1 store + endpoints + edge forward; A2 policy registered; G-1 test green; G-2/G-3 runtime guards reject cross-product ports.
- Acceptance criteria: 22 targeted unit tests pass; ruff/mypy clean on changed files; lint-ecl PASS.

## Non-Goals

- Frontend CI wiring for port tests (G-6), PM2 path hardening (G-4), health-check identity assertion (G-5), production risk note (G-7).
- Full E2E journey-event delivery proof end-to-end in one session (operator must set ingest env vars).
- Fixing the pre-existing BLE001 ruff finding in `api.py:2505`.
- A4–A7 (deeper analytics/governance follow-ups).

## Constraints

- LIGHTSPEED task lock: only P0 actions A1/A2/G-1/G-2/G-3; discoveries classified, not silently expanded.
- Windows paths; PowerShell shell quirks (no `Select-Object -First/-Last` inside `bash()`).
- Do not edit `scripts/dev/health-check.ps1` (concurrent session, G-5).
- Do not hand-edit `harness/changes/INDEX.json`.

## Assumptions

- Operator will configure `DASHBOARD_INGEST_URL` + `DASHBOARD_INGEST_KEY` for durable delivery; until then `dataQuality: none` is correct and not a bug.
- Dashboard RBAC middleware already requires a valid API key on non-exempt paths; edge must send `X-API-Key` when the key is set.

## Open Questions

- None blocking close; operator env setup is a deployment step, not a code gap.

## Resolved Clarifications

- Ingest auth: middleware API-key only on POST (webhook pattern); no `require_role` added.
- Store shape: snake_case query params on `list_events`; camelCase keys preserved in stored rows (edge contract).
