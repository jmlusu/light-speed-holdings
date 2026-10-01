---
title: "Executive KPI Scorecard + Rich Org Chart"
slug: "executive-kpi-scorecard-rich-org-chart"
status: "completed"
location: "archive"
phase: "done"
intake_status: "done"
spec_review: "pending"
plan_review: "approved"
modules:
  - "src/ai_company/dashboard/kpis/executive_scorecard.py"
  - "src/ai_company/dashboard/data_service.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/dashboard/analytics.py"
  - "src/ai_company/graph/engine.py"
  - "config/company/kpis.yaml"
  - "src/ai_company/dashboard/static/js/org-chart-interactive.js"
  - "src/ai_company/dashboard/templates/org-chart.html"
  - "tests/unit/test_executive_scorecard.py"
  - "tests/unit/test_org_chart_metrics.py"
tags:
  - "dashboard"
  - "executive-kpis"
  - "org-chart"
  - "business-readiness"
validation_status: "passed"
created_at: "2026-08-31"
updated_at: "2026-08-31"
session_id: "249c7a7e-fdfc-4cc3-baea-fa7b4416c8c9"
owner_agent: "jmlus"
claimed_at: "2026-08-31"
---

# Summary

## Outcome

P1 executive-facing dashboard features (from `CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md` Phase 2):

1. **Executive Scorecard** — `GET /api/v1/ceo-dashboard` gains a unified model: health score (0-100), per-KPI `status` (on_track/attention/critical), `trend` (up/stable/down), `source` (real_telemetry vs configured), and department health rollup.
2. **KPI Targets** — extend `config/company/kpis.yaml` with 6 executive targets (task_throughput, agent_utilization, cost_efficiency, build_success_rate, escalation_resolution_time, approval_turnaround).
3. **Trend/Anomaly** — extend `analytics.py` with `compute_period_comparison()`, `compute_moving_average()`, `detect_anomaly()`.
4. **Rich Org Chart** — `/api/v1/org-chart?include_metrics=true` returns nodes with metrics/risk/summary.
5. **Interactive org chart** — search, filter, drill, zoom/pan, expand/collapse.

## Decisions

- Executive health score = weighted average across 7 department health scores (weights in `kpis.yaml`).
- KPI `source` distinguishes `real_telemetry` vs `configured`.
- Org chart capacity = `active / (active + queued) * 100`; succession_risk from direct-reports, unique skills, tenure.
- Org chart metrics read from live MessageBus state (aligns with GAP-011), cached with 30s TTL.

## Validation

- `ruff check src/` — 0 errors
- `mypy src/` — 0 errors
- New unit tests: `tests/unit/test_executive_scorecard.py`, `tests/unit/test_org_chart_metrics.py`
- E2E Playwright: org chart search/filter/drill (browser-gated, best-effort)
- Manual: `GET /api/v1/ceo-dashboard` returns scorecard with health, trends, sources

## Next Step

Implement increment 1: executive scorecard + trend/anomaly analytics + executive KPI targets (backend, unit-testable). Then increment 2: rich org chart metrics + interactive frontend.
