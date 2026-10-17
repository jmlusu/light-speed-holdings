# Spec

## Intake Review

- Intake type: Small Change
- Input shape: plan-first (user selected "CEO Alert Center" as trivially the roadmap's alerting leg)
- Questions asked this round: 1 (next-step choice)

## Goal And Evidence

- Real problem or user request: Dashboard business readiness requires surfacing threshold alerts, but the existing `AlertEngine` is **stateless** — `GET /api/v1/kpis/alerts` evaluates live and returns fired alerts with no history, no acknowledge/snooze/clear, and no UI. A CEO cannot see recurring or resolved alerts.
- Current behavior: `AlertEngine` + 7 default `AlertRule`s evaluate a KPI snapshot ad hoc in `api.py:2260`. Fired alerts are returned in the response only; nothing persists. A `broadcast_alert` WebSocket helper exists (`ws.py:621`) but is not wired to the alert feed.
- Source of evidence: `docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md` (Phase 2 "alert rules engine with 7 default rules", Phase 3 "alert escalation"; Alert Center integration patterns), `src/ai_company/dashboard/api.py:2260`, `ws.py:621`.

## User Scenarios And Success

- Primary user/system scenario: A CEO opens the dashboard Alert Center. If any KPI crossed a threshold, an alert appears with severity and message; they can acknowledge it, snooze it for a few hours, or clear it. Recurring and historical alerts persist across reloads, and new fired alerts appear live via WebSocket.
- Success criteria: Persisted alerts survive reload; lifecycle transitions (ack/snooze/clear) reflected in list + detail; dedupe prevents spam; retention prunes old entries; RBAC guards write ops; real-time push on new fire.
- Acceptance criteria:
  1. `GET /api/v1/alerts` returns persisted alerts with status filtering and fields `id, rule_name, department, kpi_key, severity, message, fired_at, status, snoozed_until`.
  2. Firing from `GET /api/v1/kpis/alerts` persists `active`/`snoozed` alerts (dedupe identical active/snoozed).
  3. `POST /api/v1/alerts/{id}/ack|/snooze|/clear` transition status; invalid/cross-state writes return 4xx; unauthorized return 401/403.
  4. A background scheduler pass evaluates default rules and persists new fires on a cadence.
  5. Alert Center UI section renders the feed, severity badges, status filter, and ack/snooze/clear actions; updates live on the "alerts" WS topic.

## Non-Goals

- No new alert-rules engine or rule configuration UI (rule set remains the 7 defaults).
- No multi-channel delivery (SMS/webhook) or 5-tier escalation routing — deferred to a later escalation ECL.
- No per-alert assignment/ownership model.
- No SQLite migration for alerts (FileStore JSON mirrors existing KPI-history convention).

## Constraints

- Reuse `AlertEngine`/`AlertRule`/`Alert` from `analytics.py`; no dependency additions.
- Persist under the dashboard data root using `FileStore` (matching `KPIHistoryStore`).
- Write endpoints follow the existing dashboard RBAC key gate pattern.
- Frontend stays vanilla/Alpine + Tailwind; zero new npm deps.
- ECL rule: one active change at a time; routine 30s-TTL / cache rules apply only if a cache is introduced (not required for the store itself).

## Assumptions

- The dashboard data root and `FileStore` base dir resolve consistently with `get_project_root()`.
- Alerts carry a stable identity from a server-generated `id` (uuid4).
- `broadcast_alert` accepts an alert dict and pushes on the `alerts` topic (already true).

## Open Questions

- None blocking. (Resolution of lifecycle semantics + retention window documented in Decisions; scheduler cadence defaults to the existing KPI scheduler interval.)

## Resolved Clarifications

- User selected "CEO Alert Center" over escalation routing and /metrics as the next step. Minimal in-house first; escalation delivery deferred.
