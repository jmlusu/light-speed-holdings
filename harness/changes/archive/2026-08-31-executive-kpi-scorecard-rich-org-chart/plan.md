# Plan

Deliver the executive KPI scorecard + rich org chart in increments so each lands with its own passing tests.

## Increment 1 — Executive scorecard + trend/anomaly + targets (backend, unit-testable)

1. **`analytics.py`** — add pure, tested helpers:
   - `compute_period_comparison(current, previous) -> float | None` (pct change, None when prev is 0/None)
   - `compute_moving_average(series, window=7) -> list[float | None]`
   - `detect_anomaly(series, std_devs=2) -> list[int]` (indices whose value deviates >N std-dev from window mean)
2. **`config/company/kpis.yaml`** — add 6 executive KPIs under `kpis.company` (or a new `kpis.executive` block): `task_throughput`, `agent_utilization`, `cost_efficiency`, `build_success_rate`, `escalation_resolution_time`, `approval_turnaround`, each with `target`, `unit`, `weight`.
3. **Executive scorecard** — new `data_service.get_executive_scorecard(days=30) -> dict`:
   - computes each executive KPI `current` from live task telemetry,
   - per-KPI `status` (on_track/attention/critical per target),
   - `trend` via `compute_period_comparison` (current vs prior window),
   - `source` (real_telemetry/configured),
   - overall `health_score` (0-100) = weighted average of per-KPI attainment (weights from config),
   - `departments` health rollup reusing existing per-department KPI snapshots.
4. **`api.py`** — extend `GET /api/v1/ceo-dashboard` to include `health_score`, `executive_kpis[]` (status/trend/source), `departments[].health` — additive to existing response.
5. **Tests** — `tests/unit/test_analytics_trends.py`, `tests/unit/test_executive_scorecard.py`.

## Increment 2 — Rich org chart metrics + interactive frontend

6. **`graph/engine.py`** — add org-chart metric computation (capacity, active/completed tasks, utilization_trend) + risk (succession_risk, bus_factor, last_review) reading live task state.
7. **`api.py`** — `GET /api/v1/org-chart?include_metrics=true` returns per-node `metrics`/`risk` + top-level `summary`; 30s TTL cache.
8. **Frontend** — org-chart search/filter/capacity filter, click-to-drill detail panel, zoom/pan, expand/collapse in `org-chart-interactive.js` + `org-chart.html` (build on existing uncommitted work).
9. **Tests** — `tests/unit/test_org_chart_metrics.py`; E2E Playwright (best-effort).

## Sequence / dependency

- Increment 1 is independent and fully unit-testable → implement first, verify.
- Increment 2 depends on graph + api patterns from Increment 1 for consistency.
- F4 (prompt scaffold) remains deferred.

## Verification per increment

- Increment 1: `ruff check src/`, `mypy`, `pytest tests/unit/test_analytics_trends.py tests/unit/test_executive_scorecard.py` + targeted dashboard suites.
- Increment 2: above + `pytest tests/unit/test_org_chart_metrics.py`; E2E best-effort (browser-gated).
