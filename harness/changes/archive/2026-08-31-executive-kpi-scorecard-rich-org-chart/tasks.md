# Tasks

Only one active change at a time.

## Increment 1 — Executive scorecard backend

- [x] T001 [P1] [US1] Add `compute_period_comparison`, `compute_moving_average`, `detect_anomaly` to src/ai_company/dashboard/analytics.py with unit tests (tests/unit/test_analytics_trends.py)
- [x] T002 [P1] [US1] Add 6 executive KPI targets + weights to config/company/kpis.yaml under `kpis.executive`
- [x] T003 [P1] [US1] Add `get_executive_scorecard()` to src/ai_company/dashboard/data_service.py producing health_score, per-KPI status/trend/source, and department rollup
- [x] T004 [P1] [US1] Wire `executive_scorecard` section into src/ai_company/dashboard/api.py `GET /api/v1/ceo-dashboard` additively
- [x] T005 [P1] [US1] Add tests/unit/test_executive_scorecard.py (accessor + endpoint contract)

## Increment 2 — Rich org chart

- [x] T006 [P1] [US2] Add org-chart metrics + risk computation to src/ai_company/graph/engine.py reading live task state
- [x] T007 [P1] [US2] Extend src/ai_company/dashboard/api.py `GET /api/v1/org-chart` with `include_metrics=true` returning per-node metrics/risk + summary (30s TTL)
- [x] T008 [P2] [US2] Add frontend org-chart search/filter/capacity filter, click-to-drill detail panel, zoom/pan, expand/collapse in src/ai_company/dashboard/static/js/org-chart-interactive.js + templates/org-chart.html
- [x] T009 [P1] [US2] Add tests/unit/test_org_chart_metrics.py; E2E Playwright org-chart search/filter/drill (best-effort)

## Cross-cutting

- [x] T010 [P1] Verify increment 1: ruff check src/, mypy src/, targeted pytest (24 new + dashboard/regression suites green)
- [x] T011 [P1] Verify increment 2: ruff, mypy, targeted pytest green
- [x] T012 [P1] Close ECL change (update docs/STATUS.md, CHANGELOG) pending Increment 2 completion
