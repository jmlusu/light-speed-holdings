---
title: "In-House Alerting System: Engine, Channels, Escalation"
slug: "in-house-alerting"
status: "proposed"
location: "proposals"
phase: "plan"
intake_status: "done"
spec_review: "pending"
plan_review: "pending"
modules:
  - "src/ai_company/dashboard/alerting/__init__.py"
  - "src/ai_company/dashboard/alerting/engine.py"
  - "src/ai_company/dashboard/alerting/rules.py"
  - "src/ai_company/dashboard/alerting/channels.py"
  - "src/ai_company/dashboard/alerting/escalation.py"
  - "src/ai_company/dashboard/alerting/state.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/dashboard/ws.py"
  - "src/ai_company/dashboard/templates/alerts.html"
  - "src/ai_company/dashboard/static/js/alerts.js"
  - "tests/unit/test_alert_engine.py"
  - "tests/unit/test_alert_channels.py"
  - "tests/unit/test_alert_escalation.py"
  - "tests/test_alert_ui_e2e.py"
tags:
  - "alerting"
  - "dashboard"
  - "business-readiness"
  - "reliability"
validation_status: "unknown"
created_at: "2026-08-31"
updated_at: "2026-08-31"
---

# In-House Alerting System: Engine, Channels, Escalation

## Priority
P1 — Completes the alerting pillar for business readiness. Platform decision: **build minimal in-house first** (per CEO directive), deferring PagerDuty/Opsgenie integration until alert volume justifies it.

## Outcome
1. **Alert Engine** (`dashboard/alerting/engine.py`) — Rule evaluation against KPI snapshots, state machine (open → acknowledged → resolved → closed), cooldown window to prevent alert storms, 30s evaluation cadence.
2. **12 Default Alert Rules** (`dashboard/alerting/rules.py`):
   - build_success_rate_lt_95 (CRITICAL)
   - escalation_count_gt_5 (WARNING)
   - escalation_age_gt_24h (CRITICAL)
   - approval_pending_gt_10 (WARNING)
   - cost_daily_gt_budget_50pct (WARNING)
   - cost_daily_gt_budget_90pct (CRITICAL)
   - agent_utilization_lt_50 (WARNING)
   - agent_utilization_lt_30 (CRITICAL)
   - task_failure_rate_gt_10pct (WARNING)
   - ws_connection_drop_rate_gt_5pct (WARNING)
   - kpi_collection_failure (CRITICAL)
   - system_health_score_lt_60 (CRITICAL)
3. **Channel Delivery** (`dashboard/alerting/channels.py`) — WebSocket broadcast (immediate), email (critical), webhook (external Slack/Teams, critical).
4. **5-Tier Escalation** (`dashboard/alerting/escalation.py`) — T1 manager (1h), T2 department head (2h), T3 executive (4h), T4 cross-dept (8h), T5 human CEO (immediate).
5. **Alert State Persistence** (`dashboard/alerting/state.py`) — JSON store with atomic writes, cooldown tracking, history retention (30 days).
6. **Alert UI** — Banner for active alerts, Alert Center page, detail slide-out with runbook link, acknowledge/resolve buttons, history tab.
7. **API Endpoints** — `GET /api/v1/alerts`, `GET /api/v1/alerts/history`, `POST /api/v1/alerts/{id}/acknowledge`, `POST /api/v1/alerts/{id}/resolve`.

## Key Decisions
- In-house build, no external alerting dependency yet (per user directive #4)
- Alert cooldown default 30 min/rule — prevents storming
- WS broadcast always; email only for CRITICAL; webhook only for CRITICAL (configurable)
- Escalation SLA timers evaluated on the governance sweep cadence (reuse existing daemon loop, don't add new scheduler)
- Alerts stored as JSON (not SQLite) — consistent with dashboard state file pattern; 30-day retention via existing governance sweep

## Risk
- Email dependency: uses SMTP — must not block WS if email configured but sending fails (fail-open: log + continue)
- Alert storms: cooldown window + aggregation ("3 new tasks assigned" → 1 alert)
- Escalation timers: must survive daemon restarts (persist `escalated_at` in state store)

## Verification
- Unit tests: `tests/unit/test_alert_engine.py` (20+), `test_alert_channels.py` (10+), `test_alert_escalation.py` (15+)
- Integration: rule triggers → alert created → WS broadcast → state persisted → cooldown respected
- E2E Playwright: `tests/test_alert_ui_e2e.py` (banner shows, Alert Center lists, acknowledge→history, resolve→closed)
- `ruff check src/` — 0 errors
- `mypy src/` — 0 errors
- Full `pytest -m "not e2e"` green

## Owner
`dashboard-owner` (lead) + `observability-engineer` (channels) + `orchestration-owner` (escalation) + `frontend-engineer` (UI).
