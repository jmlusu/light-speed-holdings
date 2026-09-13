---
title: "Executive KPI Scorecard + Rich Org Chart"
slug: "executive-kpi-scorecard"
status: "proposed"
location: "proposals"
phase: "plan"
intake_status: "done"
spec_review: "pending"
plan_review: "pending"
modules:
  - "src/ai_company/dashboard/kpis/executive_scorecard.py"
  - "src/ai_company/dashboard/api.py"
  - "src/ai_company/dashboard/analytics.py"
  - "src/ai_company/graph/engine.py"
  - "src/ai_company/company/config/kpis.yaml"
  - "src/ai_company/dashboard/static/js/org-chart-interactive.js"
  - "src/ai_company/dashboard/templates/org-chart.html"
  - "src/ai_company/dashboard/templates/command-center.html"
  - "tests/unit/test_executive_scorecard.py"
  - "tests/unit/test_org_chart_metrics.py"
tags:
  - "dashboard"
  - "executive-kpis"
  - "org-chart"
  - "business-readiness"
validation_status: "unknown"
created_at: "2026-08-31"
updated_at: "2026-08-31"
---

# Executive KPI Scorecard + Rich Org Chart

## Priority
P1 — Completes the executive-facing features the CEO needs to run the business (from `CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md` Phase 2).

## Outcome
1. **Executive Scorecard** — `GET /api/v1/ceo-dashboard` returns unified model: health score (0-100), per-KPI `status` (on_track/attention/critical), `trend` (up/stable/down), `source` (real_telemetry vs configured), and department health rollup.
2. **KPI Targets** — Extend `company/config/kpis.yaml` with 6 executive targets (task_throughput, agent_utilization, cost_efficiency, build_success_rate, escalation_resolution_time, approval_turnaround).
3. **Trend/Anomaly** — Extend `analytics.py` with `compute_period_comparison()`, `compute_moving_average()`, `detect_anomaly()`.
4. **Rich Org Chart** — `/api/v1/org-chart?include_metrics=true` returns nodes with `metrics` (capacity %, active/completed tasks, utilization_trend), `risk` (succession_risk, bus_factor, last_review), and `summary` (total agents, executives, specialists, avg span-of-control).
5. **Interactive org chart** — Search, department filter, capacity filter, click-to-drill detail panel, zoom/pan, expand/collapse.

## Scope
Multiple files. API + data model + graph + frontend. ECL required.

## Key Decisions
- Executive health score = weighted average across 7 department health scores (weights defined in `kpis.yaml`)
- KPI `source` field distinguishes `real_telemetry` (computed from inbox/state) vs `configured` (from YAML config) — transparency for executive users
- Org chart capacity = `active / (active + queued) * 100`; succession_risk derived from direct-reports count, unique skills, tenure
- Org chart metrics read from live MessageBus state, not stale files (aligns with GAP-011)

## Risks
- Org chart metrics may be expensive to compute on large org (135 agents) — cache with 30s TTL
- Executive scorecard needs careful weighting — default weights, adjustable via config

## Verification
- `ruff check src/` — 0 errors
- `mypy src/` — 0 errors
- New unit tests: `tests/unit/test_executive_scorecard.py`, `tests/unit/test_org_chart_metrics.py`
- E2E Playwright: org chart search/filter/drill works
- Manual: `GET /api/v1/ceo-dashboard` returns scorecard with health, trends, sources

## Owner
`dashboard-owner` (lead) + `graph-owner` (org chart) + `business-intelligence-engineer` (KPI targets) + `frontend-engineer` (org chart UI).
