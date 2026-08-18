# CEO Dashboard — Control Plane Inventory

Read-only inventory of the existing CEO dashboard for the J.A.R.V.I.S. visual re-skin
(wayfinder ticket #100). Written 2026-08-16. Every claim cites the source file path and,
where useful, line numbers. Data-source classification legend:

- **REAL** — live data read from a populated operational source at request time.
- **MOCKED / TEST** — the source exists but holds fixture/test data.
- **EMPTY** — the source exists but contains no meaningful records (or the file is absent).
- **CONFIG-ONLY** — the source is static configuration (targets/definitions), not telemetry.

## 1. Overview

- Server: FastAPI app built by `create_app()` in `src/ai_company/dashboard/app.py:237`; module-level
  `app = create_app()` at `app.py:481`. Title "Light Speed Holdings — CEO Dashboard".
- Frontend: server-rendered Jinja2 page shells + one Alpine.js component (`dashboard()` in
  `static/js/app.js`) that fetches JSON and renders client-side. Tailwind + Alpine + Chart.js
  are all loaded from CDNs in `templates/base.html`.
- Six tabs served by page routes (`app.py:406-434`): `/` (Dashboard), `/agents`, `/tasks`,
  `/kpis`, `/costs`, `/escalations` (labelled "Approvals" in the nav, `app.py:229`).
- REST API mounted at `/api/v1` (`api.py:38`), mobile API at `/api/v1/mobile`
  (`mobile_api.py:26`), WebSocket at `/ws/v1/dashboard` (`ws.py:135`), ops endpoints
  `/metrics`, `/health`, `/ready` unversioned (`monitoring.py:392/402/568`). Versioning per
  ADR-014.
- Auth: `DASHBOARD_AUTH_MODE` defaults to `api_key` (fail-closed); `open` mode is loopback-only
  (`app.py:154-178`, `app.py:295-301`). See Security constraints.

## 2. Templates

Directory: `src/ai_company/dashboard/templates/` (bound in `app.py:113`, rendered via
`Jinja2Templates` at `app.py:304`).

- `base.html` — shared shell:
  - Tailwind Play CDN `<script src="https://cdn.tailwindcss.com">` + inline `tailwind.config`
    defining the entire theme palette: `brand` (sky: `#0ea5e9`-family) and `surface`
    (slate: `#94a3b8`-family), `darkMode: 'class'` (`base.html:9-30`).
  - Alpine pinned at `alpinejs@3.15.12` (`base.html:33`); comment warns Alpine 3.14+ removed an
    internal the E2E suite relies on — do not bump casually.
  - Chart.js `chart.js@4.4.0` (`base.html:36`); custom CSS `/static/css/style.css` (`base.html:39`).
  - `<body class="bg-surface-950 text-surface-200 ..." x-data="dashboard()" x-init="init()">`
    (`base.html:43-45`); `<html class="dark">` hardcoded (`base.html:2`).
  - Header binds live fields via `x-text`: uptime (`kpis.uptime_seconds`), WS badge
    (`wsConnected` → Live/Offline), online client count (`wsClients`) (`base.html:62-83`).
    Header carries inline `style="contain: layout style;"` to isolate reflows (`base.html:54`).
  - Nav tabs rendered from `_tab_context()` (`app.py:194-234`) with server-side inline SVG
    icons; active tab uses `border-brand-500 text-brand-400` (`base.html:88-107`).
  - Toast (`base.html:115-137`, colour classes hardcoded per type) and an API-failure banner
    (`base.html:146-159`, amber styling).
  - Footer hardcodes "AI Company Builder v0.1.0" (`base.html:163`).
- `index.html` — Dashboard tab. 6 KPI cards (Pending, In Progress, Completed, Failed,
  Escalated, Cost Today) with `<template x-if="!isLoading">` skeleton loaders; two charts:
  `#taskStatusChart` (doughnut) and `#departmentChart` (horizontal bar) (`index.html:110-122`).
- `kpis.html` — three charts: `#companyKPIChart`, `#kpiComparisonChart` (radar),
  `#kpiTargetChart` (current-vs-target bar) (`kpis.html:59-136`).
- `costs.html` — two charts: `#costTrendChart` (line), `#costAgentChart` (bar)
  (`costs.html:55-62`).
- `agents.html`, `tasks.html`, `escalations.html` — table/list surfaces (no canvases).
- Every page that fetches does so from `static/js/app.js`, keyed off
  `window.location.pathname` (`app.js:591-617`):
  - `/` → `/api/v1/dashboard`, `/api/v1/departments`, `/api/v1/tasks`
  - `/agents` → `/api/v1/agents`
  - `/tasks` → `/api/v1/tasks`, `/api/v1/tasks/paginated`
  - `/kpis` → `/api/v1/kpis`, `/api/v1/kpis/summary`, `/api/v1/company-kpis`, plus
    `/api/v1/kpis/live` (`app.js:769`)
  - `/costs` → `/api/v1/costs/summary`
  - `/escalations` → `/api/v1/approvals`, `/api/v1/escalations`

## 3. Static assets

Directory: `src/ai_company/dashboard/static/` (mounted at `/static`, `app.py:438-443`).

- `css/style.css`:
  - `[x-cloak]{display:none}` (`style.css:7`).
  - Layout-shift guards: `.kpi-card, .chart-container, .table-wrap { contain: layout style; }`
    (`style.css:37-39`); `.chart-container` pairs with `maintainAspectRatio:false` and explicit
    heights `.chart-container-sm 200px / -md 250px / -lg 320px` (`style.css:128-130`).
  - Skeleton loader keyframes + `.skeleton`, `.skeleton-number`, `.skeleton-text`,
    `.skeleton-row` (`style.css:58-94`).
  - `.kpi-card:hover` lift, `.line-clamp-2`, kanban drop-zone styles, `.ws-status` fixed-width
    badge, `.nav-tabs` scrollbar styling, responsive media queries, print + reduced-motion
    blocks (`style.css:97-284`).
- `js/app.js` — single `dashboard()` Alpine component (1,197 lines):
  - State: `kpis`, `agents`, `tasks`, `wsConnected`, `wsClients`, `ws`, `toast`,
    `apiStatus`, `isLoading`; WS hardening (`_wsMaxReconnectAttempts: 8`, 60s recovery probe),
    polling (`_pollIntervalMs: 15000`, `_pollInFlight`/`_pollQueued`), chart coalescing
    (`_kpiChartsRaf`, `_kpiChartsPending`, `_latestKpis`, `_latestDepartments`), and
    scroll-lock state (`_scrollLock`, `_savedScroll`, `_pendingRestoreRaf`, `_scrollGuardActive`).
  - `connectWebSocket()` builds `${ws|wss}://${host}/ws/v1/dashboard` and appends
    `?api_key=` only if `window.DASHBOARD_API_KEY` is set (`app.js:319-323`) — it is never set
    anywhere (see Security constraints). Keepalive `ping` every 25s (`app.js:415-426`).
  - `fetchJSON()` (`app.js:536-566`): 15s AbortController timeout; maps 429 → "Too many
    requests", 401 → "Session expired"; sends **no** `X-API-Key` header (only
    `Content-Type` on POST/PATCH).
  - Mutations: create task (`app.js:883`), approve/reject (`app.js:902/910`), resolve
    escalation (`app.js:918`), update/delete task (`app.js:960/996`).
- `js/charts.js` — Chart.js integration (423 lines):
  - Global defaults: `color #94a3b8`, `borderColor rgba(51,65,85,0.3)`, font
    `'Inter', system-ui, sans-serif`, legend `usePointStyle`, `animation.duration 300`,
    `responsive true`, `maintainAspectRatio false` (`charts.js:7-33`).
  - `COLORS` palette: amber/blue/emerald/red/purple/brand/slate/cyan, each with 0.15-alpha fill
    + hex border/point (`charts.js:36-45`).
  - `updateOrCreateChart(id, ctx, config)` (`charts.js:83-104`) — updates in place, skips
    redraws when the JSON data signature is unchanged; a re-skin that bypasses it reintroduces
    the destroy→collapse→scroll bug documented at `charts.js:69-82`.
  - Chart builders: `updateChartsFromKPIs` (`charts.js:108`, doughnut + dept bar),
    `initKPICharts` (`charts.js:185`, radar + target bar), `initCompanyKPICharts`
    (`charts.js:299`), `initCostCharts` (`charts.js:348`, trend line + agent bar). Cost trend
    explicitly "never mock data" (`charts.js:352-353`).

## 4. API surface (REST, `/api/v1`)

Router at `api.py:38`. All state I/O routes through `StateStore` (`repository.py`, configured
in `app.py:388-393` via `DASHBOARD_DATA_DIR` or `get_data_root()`); tasks read/write via a
shared `MessageBus` backed by `.opencode/inbox.json` (`api.py:46-58`, `api.py:54`).

| Method | Path | Source | Class |
|--------|------|--------|-------|
| GET | `/dashboard` (`api.py:526`) | tasks SQLite-first, `orchestrator/approvals.yaml`, `orchestrator/escalation.yaml`, `orchestrator/scheduler.yaml`, registry | REAL (tasks are test fixtures) |
| GET | `/kpis/live` (`api.py:577`) | `kpis.collect_all_kpis(database=...)` | REAL (mostly zero values) |
| GET | `/kpis` (`api.py:1115`) | `company/config/kpis.yaml` definitions | CONFIG-ONLY |
| GET | `/kpis/summary` (`api.py:1122`) | same YAML, flattened | CONFIG-ONLY |
| GET | `/kpis/history/{department}` (`api.py:1348`) | SQLite `kpi_values` (via `data_service.get_kpi_history`) | REAL |
| GET | `/kpis/trends/{department}` (`api.py:1397`) | SQLite KPI history | REAL |
| GET | `/kpis/alerts` (`api.py:1439`) | `analytics.AlertEngine` + rules | REAL-ish (rules) |
| GET | `/kpis/collect` (`api.py:1542`) | collects all, stores file snapshot + SQLite ingest | trigger |
| GET | `/kpis/summary-stats/{department}` (`api.py:1582`) | `analytics.compute_summary` over history store | REAL |
| GET | `/company-kpis` (`api.py:1146`) | `data_service.get_company_kpi_summary` (`data_service.py:263`): KPI-003/KPI-004 computed from live task window, others from config | REAL (2) + CONFIG-ONLY (3) |
| GET | `/ceo-dashboard` (`api.py:1163`) | aggregates `collect_all_kpis`, tasks, registry, cost tracker, escalations, approvals, scheduler | MIXED (see §5) |
| GET | `/agents` (`api.py:595`) | `company/agent-registry.json` | REAL (131 agents) |
| GET | `/agents/performance` (`api.py:601`) | SQLite-first `data_service.get_agent_performance_report`, file fallback | REAL |
| GET | `/agents/{name}/performance` (`api.py:643`) | SQLite-first, file fallback | REAL |
| GET | `/agents/{name}` (`api.py:660`) | registry | REAL |
| GET | `/org-chart` (`api.py:672`) | registry tree | REAL |
| GET | `/tasks` (`api.py:714`) / `/tasks/paginated` (`api.py:728`) | MessageBus / inbox | TEST data |
| POST | `/tasks` (`api.py:836`), PATCH `/tasks/{id}` (`api.py:886`), DELETE `/tasks/{id}` (`api.py:913`) | MessageBus writes | write |
| GET | `/approvals` (`api.py:936`), POST `/approvals/{id}/approve` (`api.py:961`), POST `/approvals/{id}/reject` (`api.py:984`) | `orchestrator/approvals.yaml` | REAL (mix of test + human records) |
| GET | `/escalations` (`api.py:1010`), POST `/escalations/{task_id}/resolve` (`api.py:1018`) | escalation.yaml / SQLite | EMPTY |
| GET | `/departments` (`api.py:1051`) | registry grouping | REAL |
| GET | `/departments/{dept}/kpis` (`api.py:1103`) | `company/config/kpis.yaml` | CONFIG-ONLY |
| GET | `/departments/{dept}/dashboard` (`api.py:1258`) | collector snapshot | REAL |
| GET | `/models` (`api.py:1061`), `/models/tiers` (`api.py:1074`) | `company/models.yaml` | CONFIG-ONLY |
| GET | `/scheduler` (`api.py:1093`) | `orchestrator/scheduler.yaml` | EMPTY |
| GET | `/costs/summary` (`api.py:1625`) | SQLite `cost_records` (via `data_service.get_cost_summary`, `data_service.py:79`) else cost_tracker.json + audit + KPI history | REAL |
| GET | `/governance` (`api.py:1699`) | SQLite `DataGovernance` report | REAL |

Mobile (`/api/v1/mobile`, `mobile_api.py:26`): `/dashboard` (`:193`), `/tasks` (`:254`),
`/actions/batch` (`:321`), `/actions/quick-approve` (`:460`), `/approvals/stack` (`:489`),
`/approvals/swipe` (`:539`), `/kpis/compact` (`:591`), `/kpis/trend` (`:627`),
`/notifications/register` (`:699`), `/notifications/unregister` (`:749`),
`/notifications/preferences` (`:767`), `/notifications/status` (`:801`), `/sync` (`:823`),
`/batch` (`:892`). Same file-backed sources as main API; batch actions call
`_approve_request`/`_reject_request`/`_resolve_escalation`/`_delegate_task`
(`mobile_api.py:348-434`).

Ops (`monitoring.py`): `/metrics` Prometheus text (`:392`), `/health` deep check of files,
providers, disk, memory, DLQ (`:402`), `/ready` 503-on-missing-registry probe (`:568`).

## 5. WebSocket

- Endpoint `/ws/v1/dashboard` (`ws.py:135`). Handshake gated by origin check (`ws.py:104-132`:
  no Origin, same-host Origin, or CORS allowlist) and `require_ws_role("run", ?api_key=)`
  (`ws.py:161`); failure closes with code 1008.
- Client → server message types: `ping` → `pong`, `subscribe` (topics), `unsubscribe`
  (`ws.py:181-216`). Unknown types get an `error` reply.
- Server → client message types: `connected`, `kpi_update`, `alert`, `task_update` (with
  `event` created/completed/failed/escalated), `department_kpi`, `escalation`, `subscribed`,
  `unsubscribed`, `pong`, `error` — broadcast helpers at `ws.py:229-296`.
- Topics: `kpis`, `alerts`, `tasks`, `escalations`, `department:{dept}`; empty subscription set
  = receive-all (back-compat) (`ws.py:74-79`).
- `ConnectionManager` (in-memory, per-process): `_connections`, `_subscriptions`,
  `active_count`, prune-on-send-failure (`ws.py:21-94`).
- MessageBus bridge: `make_message_bus_broadcast_callback()` (`ws.py:304-323`) and the
  `_bus_broadcast` closure in `api.py:61-67` push task lifecycle events onto the loop.

## 6. Data sources per surface (verified against the working tree)

SQLite database `data/ai_company.db` (created at boot by `app.py:458-477` at
`<StateStore base>/data/ai_company.db`). Verified contents (read-only queries):

| Table | Rows | Notes |
|-------|------|-------|
| `tasks` | 7 | all `completed`; receivers are `test-receiver`/`test_receiver`/`technical-documentation-lead` → **TEST** |
| `cost_records` | 83 | models `gemini-3.5-flash` ($0.07) + `llama3.1:8b` ($0.00), 2026-08-07→08-13 → **REAL** |
| `escalation_events` | 0 | → **EMPTY** |
| `kpi_values` | 230 | 5 snapshots (latest 2026-08-14T19:56); many `current 0` (e.g. legal `compliance_score` 0/100) → **REAL but zero-valued** |
| `audit_events` | 2227 | → **REAL** |
| `memory_entries` | 0 | → **EMPTY** |
| `schema_meta` | 1 | schema_version = 1 → DB considered usable |

Operational files (all exist unless noted):

- `.opencode/inbox.json` — 5 KB, **7 TEST tasks** (`test-task-001`, `test-claim-001`, etc.),
  all `completed` → task surfaces render test data.
- `orchestrator/approvals.yaml` — **575 KB / ~21,400 lines**, mixed fixture + human
  (`human-ceo`) approval records incl. expired/approved/rejected → **REAL (noisy)**.
- `orchestrator/cost_tracker.json` — 344 B; `total_spent: 0.0`, `llm_spend: 0.0`, empty
  `by_model`/`by_agent`/`daily_trend` → **EMPTY** (file is a tracker template).
- `orchestrator/escalation.yaml` — 167 B; only `rules` (task-timeout), no `events` →
  escalations surface **EMPTY**.
- `orchestrator/scheduler.yaml` — 10 B; `tasks: []` → **EMPTY**.
- `orchestrator/sales/pipeline.json`, `orchestrator/sales/leads.json` — **absent** → sales
  collector yields zeros (`kpis/sales.py:17-18`).
- `orchestrator/cs/surveys.json` — documented as present-but-empty (`config/company/kpis.yaml:44`).
- `company/agent-registry.json` — **131 agents** (real company org: human-ceo, chief-of-staff,
  cto, coo, etc.) → **REAL**.
- `company/config/kpis.yaml` — department KPI definitions/targets (engineering, hr, marketing,
  sales, finance, customer_success, legal) → **CONFIG-ONLY**.
- `config/company/kpis.yaml` — 5 company KPIs; KPI-001 (ARR), KPI-002 (CSAT), KPI-005 (eNPS)
  have `current: null` ("n/a", no source); KPI-003/KPI-004 have file-computed snapshot
  `current`s and are recomputed live by `data_service.get_company_kpi_summary` →
  **CONFIG-ONLY + 2 computed**.
- `config/company/kpis.yaml` header explicitly states the CEO decision that company KPIs
  "MUST be COMPUTED FROM REAL SOURCES, not hardcoded dummy values" (`config/company/kpis.yaml:3-4`).

Collector read path (`kpis/base.py`): SQLite-first (`_tasks_from_sqlite`, `_cost_from_sqlite`,
`_escalations_from_sqlite`) with legacy-file fallback (`_tasks_from_bus` → MessageBus;
`base.py:99-180`). Seven collectors registered (`kpis/__init__.py:20-28`).

## 7. Security constraints

- **Auth middleware applies to every request**, including page HTML and static files: in
  `api_key` mode a missing/incorrect `X-API-Key` returns 401 for `/`, `/static/*`, etc.
  (`app.py:361-369`, `app.py:154-178`). The browser JS never sends a key and
  `window.DASHBOARD_API_KEY` is never injected (no template reference), so **the UI works in
  practice only in `open` loopback mode** (`DASHBOARD_AUTH_MODE=open`, enforced loopback-only
  `app.py:295-301`). This matches ADR-013's stated problem.
- **ADR-013 is only partially implemented.** `sessions.py` defines
  `mint_bootstrap_token`/`resolve_session_token` (`sessions.py:89/103`), but no
  `GET /api/bootstrap-token` route exists anywhere in `src/`, `resolve_session_token` is not
  called by `rbac.py`/`_check_api_key`/`ws.py`, and WS auth reads only the static
  `?api_key=` query (`ws.py:161`). Implementation ticket #77 is the planned work.
- RBAC (ADR-012): `Role` hierarchy run < approve < admin; env keys `DASHBOARD_RUN_KEY` /
  `DASHBOARD_APPROVE_KEY` / `DASHBOARD_ADMIN_KEY` (`DASHBOARD_API_KEY` = admin alias);
  `require_role()` on REST, `require_ws_role()` on WS. Implemented in
  `src/ai_company/security/rbac.py`.
- CORS allowlist: localhost-only default (`http://localhost[:3000]`, `http://127.0.0.1[:3000]`);
  wildcard `*` stripped (`app.py:311-326`).
- Rate limit: in-memory sliding window, 100 req/min/IP default (`DASHBOARD_RATE_LIMIT`,
  `app.py:337`, `app.py:124-146`), 429 + `X-RateLimit-*` headers.
- Default CSP (`app.py:70-78`, override `DASHBOARD_CSP`):
  `script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://cdn.jsdelivr.net;`
  `style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;`
  `img-src 'self' data:; font-src 'self' data:;`
  `connect-src 'self' ws: wss:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'`.
  `'unsafe-eval'` is required by Alpine v3 (`app.py:60-64`).
- Other headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
  `Referrer-Policy: strict-origin-when-cross-origin`,
  `Permissions-Policy: geolocation=(), microphone=(), camera=()`, HSTS default 1 year
  (`DASHBOARD_HSTS_MAX_AGE`) (`app.py:79-88`).
- WebSocket CSWSH: origin allowlist + same-host check (`ws.py:104-132`).

## 8. Re-skin constraints and breakage risks

1. **CSP blocks new CDNs/fonts.** Adding a Google Fonts `<link>` requires extending
   `font-src`/`style-src`; any new script host must be added to `script-src` (`app.py:70-78`).
2. **Theme lives in one inline block.** All brand/surface colours are defined inline in
   `base.html:10-30` and referenced as Tailwind class names (`bg-surface-950`,
   `text-brand-400`, …) throughout templates; a re-skin starts (and ends) there, but hexes also
   leak into templates (emerald/red/amber status colours, `base.html:71-79,121-126`),
   `charts.js` COLORS, and `style.css`.
3. **Dark-only, single mode.** `<html class="dark">` is hardcoded (`base.html:2`); there is no
   light-mode or accent theming path beyond editing classes inline.
4. **Inline styles resist CSS overrides.** `style="contain: layout style;"` on the header
   (`base.html:54`) and the `scroll-locked` body binding (`base.html:45`) are layout-critical;
   changing the header/scroll model requires touching `app.js` scroll-lock logic too.
5. **Chart canvases are id-bound.** Charts.js reads fixed canvas ids
   (`taskStatusChart`, `departmentChart`, `companyKPIChart`, `kpiComparisonChart`,
   `kpiTargetChart`, `costTrendChart`, `costAgentChart`). Renaming or restructuring them
   without updating `charts.js` silently renders nothing.
6. **Chart height comes from CSS containers.** `maintainAspectRatio:false` +
   `.chart-container{-sm/-md/-lg}` fixed heights (`style.css:114-130`) are what stop charts
   collapsing to 0px during destroy/recreate (documented `charts.js:27-32`).
7. **Chart animation is tuned to the poll cadence.** 300ms animation vs 15s polling
   (`charts.js:16-23`); `updateOrCreateChart`'s no-op guard (`charts.js:83-104`) prevents
   poll/WS duplicate redraws. Reintroducing full destroy/recreate reopens the
   auto-scroll bug (history at `charts.js:69-82`, `index.html:99`).
8. **Alpine version is pinned for E2E compatibility.** `alpinejs@3.15.12` with an explicit
   warning not to bump (`base.html:32-33`).
9. **X-text bindings in the header must stay wired.** Uptime, WS Live/Offline badge, and
   online-client count (`base.html:62-83`) depend on `kpis.uptime_seconds`, `wsConnected`,
   `wsClients` from `app.js`; a re-skinned header that drops these removes working telemetry
   display.
10. **Skeleton/loading states are bespoke.** `.skeleton*` classes + `<template x-if>` guards
    (`style.css:58-94`) must be recreated or removed with the new design.
11. **Nav icons are server-side SVG strings.** Tab definitions (incl. inline SVG) live in
    `_tab_context()` in `app.py:194-234`, not in templates — re-skinning the nav touches Python.
12. **Payload contracts are fixed by Pydantic + Alpine reads.** KPI card labels
    (Pending/In Progress/…) are hardcoded in `index.html` and `charts.js:115`; Alpine reads
    `kpis.pending_tasks` etc. (`models.py:10-22`). Adding new metrics means backend changes.
13. **Approvals page data is noisy/expired.** `/escalations` tab renders approvals whose file
    is dominated by fixture/expired records; visual work should not assume clean data.
14. **Most surfaces show empty or test data today.** Escalations, scheduler, sales, memory,
    surveys and several dept KPIs render zeros; the only rich live surfaces are audit events,
    cost records, approvals, and the 131-agent registry. A re-skin can't fix data gaps.

## 9. UNKNOWN — could not determine

- Whether `GET /api/bootstrap-token` (ADR-013) is implemented on a branch or in uncommitted
  work outside `src/ai_company/dashboard`; not present in the current source tree.
- The deployed auth mode / env values (`.env` not read); dashboard behaviour under
  `api_key` mode from a browser is untested here.
- Whether the mobile endpoints have a live consumer (no mobile client in `src/ai_company/dashboard`).
- Whether `chart.js@4.4.0` uses `Inter` at runtime (font is declared in Chart.js defaults but
  `Inter` is never loaded — falls back to `system-ui`).
