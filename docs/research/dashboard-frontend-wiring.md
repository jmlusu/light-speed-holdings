# Research: Dashboard frontend wiring for gauge + KPI cards

Catalog of existing frontend scaffolding for adding an Org Health hero gauge and
company-KPI cards to the main Dashboard `/` (wayfinder ticket #25).

## Templates

- `src/ai_company/dashboard/templates/index.html` — current `/` view: a
  `kpi-grid` of 6 KPI cards (Pending, In Progress, Completed, Failed, Escalated,
  Cost Today) using `<template x-if="!isLoading">` skeleton loaders; each renders
  from the Alpine `kpis.*` state. Layout: KPI cards row, then chart rows.
- `src/ai_company/dashboard/templates/base.html` — layout shell. Defines the
  Alpine `dashboard()` root component factory, CSP meta tag, and the Tailwind
  config block (CSP constraint: **inline scripts limited to the existing
  Tailwind config** — no new inline JS allowed).

## Alpine state (`static/js/app.js`)

The `dashboard()` component state object holds:

- `kpis: { pending_tasks, in_progress, completed, failed, escalated,
  pending_approvals, open_escalations, last_activity, cost_today, ... }`
- `companyKPIs: []` — array of company-level KPI cards.
- `companyKPISummary: null` — aggregated company metrics.
- `allKPIsList: []`, `kpiDepartments: []`, `liveKPIData: null`.
- Methods: `loadDashboard()` (fetches `/api/dashboard` + schedules live WS),
  `loadKPIs()` (fetches `/api/kpis` + per-dept detail), `loadCompanyKPISummary()`
  (fetches `/api/company-kpi-summary`), `scheduleKPICharts()` +
  `_mergeKPIPayload()` (coalesces live + poll payloads), `_kpiChartsRaf` /
  `_kpiChartsPending` (frame-coalesced redraw).

## Data flow

- **REST poll:** `/api/dashboard` → `KPIs`; `/api/kpis/live` → live snapshots;
  `/api/company-kpi-summary` → summary; `/api/kpis/history/{dept}` → NDJSON
  history.
- **WebSocket:** `dashboard/ws.py` broadcasts `kpi_update`, `task_update`,
  `approval_alert`, `escalation_alert`, `alert`; `app.js` reconnects with
  keepalive ping; `debouncedPoll()` 30s fallback while WS live
  (`static/js/app.js` `connectWebSocket()` + WS router `switch(msg.type)`).

## Charts (`static/js/charts.js`)

- `initKPICharts(...)`, `initCompanyKPICharts(...)`, `updateChartsFromKPIs(...)`
- Doughnut "progress" style used for KPI cards; line charts for trends.
- Chart.js already bundled (no new dependency needed for a gauge).

## Insertion point / constraints

- Hero gauge + KPI cards go **after the current KPI cards row, before the charts
  row** in `index.html`.
- Gauge render: Chart.js `doughnut` (no new deps) or a custom SVG; trend
  sparkline via Chart.js `line`.
- Listen for WS `kpi_update` with a `org_health` payload; merge into
  `companyKPIs`/`companyKPISummary` for live refresh.
- CSP: reuse existing Tailwind-config block; no extra inline scripts.

## Verdict for #31 (prototype the hero)

All scaffolding exists: state shape (`companyKPIs`, `companyKPISummary`), data
sources (`/api/company-kpi-summary`, `/api/dashboard`), WS path (`kpi_update`),
charting (`charts.js`), and the insertion slot. The prototype ticket (#31) can
build the gauge from existing pieces without touching architecture.

Artifact for wayfinder #25 — wiring catalog complete.
