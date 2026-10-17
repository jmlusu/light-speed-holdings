# Spec

## Intake Review

- Intake type: Structured Change (multi-file: API + data model + graph + frontend)
- Input shape: plan-first (proposal summary.md exists)
- Questions asked this round: 1 (scope sequencing — increment into testable backend core + frontend)

## Goal And Evidence

- Real problem or user request: CEO needs a unified, current-state dashboard to run the business — a single health score, per-KPI status/trend/source, and a rich org chart with live metrics — not scattered per-department views.
- Current behavior: `/ceo-dashboard` returns an aggregate of departments/tasks/agents/cost but no unified health score, no per-KPI trend, no second source granularity beyond `config`/`real`. `/company-kpis` returns per-KPI status/gap/source but no trend and no executive (non-company-specific) targets. `/org-chart` returns node graph without live metrics.
- Source of evidence: `docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md` Phase 2; proposal `harness/changes/proposals/2026-08-31-executive-kpi-scorecard/summary.md`.

## User Scenarios And Success

- Primary user/scenario: CEO opens the dashboard and sees (a) one executive health number with per-KPI status/trend/source, and (b) an org chart with per-agent capacity, activity, and succession risk.
- Success criteria:
  - `GET /api/v1/ceo-dashboard` returns `health_score` (0-100), `departments[].health`, and each KPI has `status` (on_track/attention/critical), `trend` (up/stable/down), `source` (real_telemetry/configured).
  - `config/company/kpis.yaml` exposes 6 executive targets with weights.
  - `analytics.py` exposes `compute_period_comparison`, `compute_moving_average`, `detect_anomaly`, all unit-tested.
  - `GET /api/v1/org-chart?include_metrics=true` returns node `metrics`/`risk` + top-level `summary`.
- Acceptance criteria: new unit tests (`test_executive_scorecard.py`, `test_org_chart_metrics.py`) pass; ruff/mypy clean; existing dashboard tests green.

## Non-Goals

- No change to approval/decision workflows.
- No new database migrations.
- Frontend interactive org chart (zoom/pan/search/drill) is a follow-on increment; its E2E is best-effort (browser-gated in this environment).

## Constraints

- Only one active ECL change at a time.
- Must not break existing `/company-kpis`, `/ceo-dashboard`, or `/org-chart` contracts; additive changes only.
- Org-chart metric reads must go through live MessageBus state, not stale files.

## Assumptions

- KPI config schema in `config/company/kpis.yaml` (`kpis.company[]` with `id/name/target/unit`).
- Health score weights default in config, adjustable.

## Open Questions

- None blocking. Frontend org-chart scope (zoom/pan vs search/filter/drill) may tighten based on what `org-chart-interactive.js` already implements from prior uncommitted work.

## Resolved Clarifications

- Scope sequenced into increments: (1) backend executive scorecard + trend/anomaly + targets; (2) org-chart metrics + interactive frontend.
