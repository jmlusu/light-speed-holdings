---
title: "CEO Alert Center"
slug: "ceo-alert-center"
status: "completed"
location: "archive"
phase: "validate"
intake_status: "done"
spec_review: "pending"
plan_review: "approved"
modules:
  - "src/ai_company/dashboard/alert_store.py"
  - "src/ai_company/dashboard/data_service.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/dashboard/scheduler.py"
  - "src/ai_company/dashboard/templates/index.html"
  - "src/ai_company/dashboard/static/js/app.js"
  - "tests/unit/test_alert_store.py"
  - "tests/unit/test_alert_center_api.py"
tags:
  - "dashboard"
  - "alerting"
  - "business-readiness"
validation_status: "passed"
created_at: "2026-08-31"
updated_at: "2026-08-31"
session_id: "253e0f06-f353-4d4d-a670-7f053e80c7ae"
owner_agent: "jmlus"
claimed_at: "2026-08-31"
---

# Summary

## Outcome

Persist and surface threshold alerts from the existing `AlertEngine` as a **CEO Alert Center** — a filtered, queued feed backed by a durable store with acknowledge/snooze/clear lifecycle, real-time WebSocket "alert" push, and a dashboard UI section. Complements the shipped executive scorecard + rich org chart as the alerting leg of dashboard business readiness.

## Decisions

- **Reuse** `AlertEngine`/`AlertRule` from `analytics.py` threshold evaluation (no new rules engine). The 7 default rules in `api.py` stay the source.
- **Persistence** via `FileStore` JSON list at the dashboard data root (`dashboard/alerts.json`) — matches the existing KPI-history storage convention (SQLite-first mirror is retired).
- **Lifecycle states**: `active` → `acknowledged` / `snoozed` → `cleared`. `snoozed` carries a `snoozed_until` timestamp; cleared/acknowledged entries older than 30 days are pruned on write (retention).
- **Dedupe**: a new alert is skipped if an identical `(rule_name, department, kpi_key, severity)` is already `active` or `snoozed`.
- **Write endpoints** guarded by the existing dashboard RBAC approve/run key pattern (`_check_api_key`).
- **Frontend**: minimal in-house alert feed section (no new deps) — severity badges, status filter, acknowledge/snooze/clear, real-time via the existing "alerts" WS topic.

## Validation

- `ruff check src/`, `mypy src/` — 0 errors.
- New unit tests: `tests/unit/test_alert_store.py` (store lifecycle + retention + dedupe), `tests/unit/test_alert_center_api.py` (list/ack/snooze/clear contract + RBAC).
- Targeted regression (dashboard/alerts/KPI suites) green.
- ECL lint passes.

## Next Step

Run Plan Review (phase → implement) then implement AC-1 persistence store → AC-2 API → AC-3 frontend → AC-4 tests.
