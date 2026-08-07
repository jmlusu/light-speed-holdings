# CEO Dashboard — Operationalization Plan

Status: **Plan approved — Sprint 2 complete, Sprint 3 items 1-2 complete**
Author: Jack Mlusu
Updated: 2026-08-07

## 1. Objective

Operationalize the CEO Dashboard so every metric the UI renders comes from the
system's **real operational telemetry** — tasks, audit events, LLM cost logs,
escalations, approvals, and KPI collectors — instead of hardcoded values,
client-side placeholder math, or empty zeros.

The dashboard is today a hybrid: a small slice of real data reaches the API only
when the server is launched from the `ai-company/` directory (CWD-relative
paths), and the majority of the KPI surface is zeros, hardcoded sample values,
or fabricated client-side numbers. This plan removes those dependencies in
phases.

## 2. Current-State Assessment (2026-08-07)

| Area | Finding |
|------|---------|
| KPI collectors | `kpis/base.py:28` and `kpis/__init__.py:38` resolve the project root with `Path(__file__).resolve().parents[3]`, which lands in the wrong directory (`src/`), so collectors miss the real `ai-company/` operational files. |
| Server boot | `app.py` defaults `DASHBOARD_DATA_DIR` to `"."` (CWD) — real data only appears when launched from `ai-company/`. |
| Inbox | `api.py:get_bus()` uses `".opencode/inbox.json"` (CWD-relative). |
| Costs page | `app.js:loadCosts()` fabricates costs client-side (`completed * $0.025`, `$10` daily budget) instead of calling `/api/costs/summary`. |
| Cost trend chart | `charts.js:initCostCharts()` generates `Math.random()` mock trend data. |
| KPI history | `KPIHistoryStore()` defaults its storage dir to `Path("dashboard/kpi_history")` (CWD-relative). |
| Data layer | SQLite schema v1 (`tasks`, `audit_events`, `cost_records`, `kpi_values`, `escalation_events`, `memory_entries`) exists with all stores (`TaskStore`, `AuditStore`, `CostAnalytics`, `KPIPipeline`, `EscalationStore`), but the dashboard reads almost none of it. |

Real operational data available today:

- `.opencode/inbox.json` — 152 demo/seeded tasks
- `.opencode/audit.jsonl` — ~2.8k audit events (LLM cost data in `metadata.cost`)
- `orchestrator/approvals.yaml` (54 requests), `orchestrator/escalation.yaml`,
  `orchestrator/scheduler.yaml`
- `company/agent-registry.json`, `config/company/kpis.yaml`

## 3. Guiding Principles

1. **SQLite-first, file-fallback.** The dashboard reads from the SQLite data
   layer when it holds data; otherwise it falls back to the file-based stores so
   the dashboard is never blank.
2. **CWD-independent.** All path resolution goes through a single deterministic
   resolver. The dashboard behaves identically no matter where it is launched.
3. **No fabricated numbers.** Every rendered value traces to a real source file,
   store, or collector. Placeholders and `Math.random()` mock data are removed.
4. **Incremental, verifiable.** Each sprint lands behind the same gates
   (`ruff check src/ && mypy src/ && pytest`).

## 4. Phases

### Sprint 1 — Deterministic roots + stop the fabrication (this plan)

| Task | Description | Owner |
|------|-------------|-------|
| S1.1 | Deterministic project/data root resolution via a new `ai_company/paths` module; fix `parents[3]` in `kpis/base.py` and `kpis/__init__.py`; make `DASHBOARD_DATA_DIR` default to the project root; fix `KPIHistoryStore` default storage dir; fix `get_bus()` inbox path. Env overrides: `AI_COMPANY_ROOT`, `DASHBOARD_DATA_DIR`. | Backend engineer |
| S1.2 | Replace client-side fabricated costs: `app.js:loadCosts()` calls `/api/costs/summary`; `charts.js` cost trend uses real history when available. | Frontend engineer |
| S1.3 | Add `dashboard/data_service.py` — read-through accessor (SQLite-first, file-fallback) for tasks, cost summary, and KPI history; route `api.py` reads through it. | Backend engineer |
| S1.4 | Add `ai-company dashboard backfill` CLI to import `.opencode/inbox.json`, `.opencode/audit.jsonl`, `results/cost_log.jsonl`, `dashboard/kpi_history/*.ndjson`, and `orchestrator/escalation.yaml` into SQLite (idempotent, `INSERT OR REPLACE`). | Backend engineer |
| S1.5 | Tests for the new `paths` module, `data_service` read-through behaviour, and the backfill CLI; run `ruff` + `mypy` + `pytest` gates. | QA / Test engineering |

### Sprint 2 — Live pipelines into SQLite

- Make the executor + orchestrator write tasks/audit/costs directly to SQLite
  (SQLite becomes the live source, files become exports).
- Wire `dashboard/kpis/*` collectors to read from SQLite when populated.
- Periodic KPI snapshot scheduler (Cron inside the daemon, not only at boot).

### Sprint 3 — Full CEO surface on real data

- Per-agent performance, model usage, and error analysis from
  `AgentPerformanceAnalytics` on top of backfilled audit data.
- Company-level KPIs vs targets from `config/company/kpis.yaml`.
- Retention/governance (`data/governance.py`) so backfilled data ages out safely.

## 5. Verification Gates (every sprint)

- `uv run ruff check src/`
- `uv run mypy src/`
- `uv run pytest`
- CLI: `ai-company --help` + `ai-company dashboard --help` + `ai-company dashboard backfill --help`
- Manual smoke: `ai-company dashboard` then confirm `/api/ceo-dashboard`,
  `/api/costs/summary`, `/api/kpis/live` return non-zero, real values.

## 6. Definition of Done (Sprint 1)

- [x] `ai_company.paths.get_project_root()` returns the `ai-company/` root from
      any CWD, with `AI_COMPANY_ROOT` override honoured.
- [x] KPI collectors resolve the same root and read real operational files.
- [x] `/api/costs/summary` values (not client-side) drive the costs page and
      charts; no `Math.random()` trend data.
- [x] `ai-company dashboard backfill` populates SQLite from existing files and
      is safe to re-run.
- [x] All gates green.

## 7. Definition of Done (Sprint 2, Item 1 — write-through)

- [x] `MessageBus` accepts an optional `database`; when provided, every task
      mutation (create / status change / delete) is mirrored to the SQLite
      `tasks` table via `TaskStore`, best-effort and never raising.
- [x] `AuditWriter`/`init_audit` accept an optional `database`; events are
      mirrored to `audit_events` via `AuditStore` while the JSONL file stays
      primary.
- [x] `CostTracker` accepts an optional `database`; `record_usage()` is
      mirrored to `cost_records` via `CostAnalytics` while `cost_log.jsonl`
      stays primary.
- [x] `Executor(...)` wires the database through to MessageBus, CostTracker,
      and audit; `ai-company executor start/tick/run-task` gain a `--db-path`
      option.
- [x] Dashboard `get_bus()` constructs its MessageBus with the shared SQLite
      database, so dashboard task writes land in the same store.
- [x] Without a database every component behaves exactly as before (file-only)
      — no behaviour change, full backward compatibility.
- [x] Unit tests cover all three mirrors plus the `database=None` path; gates
      green (`ruff check src/`, `mypy src/`, `pytest`).

## 8. Definition of Done (Sprint 2, Item 2 — SQLite-first KPI collectors)

- [x] `KPICollector` accepts an optional `database`; when populated, tasks /
      costs / escalations are read from SQLite (`TaskStore`, `CostAnalytics`,
      `EscalationStore`) with the legacy files as fallback.
- [x] Engineering reads tasks + escalations, finance reads costs, and
      customer-success / sales / marketing / legal read department tasks from
      SQLite when populated.
- [x] `collect_all_kpis()` accepts `database=` and resolves the project root
      via `get_project_root()` (fixes the `parents[3]` bug).
- [x] Dashboard `/api/kpis/live` and `/api/kpis/collect` pass the shared SQLite
      database through to the collectors.
- [x] Without a database (or with an empty one) every collector behaves exactly
      as before (file-only) — no behaviour change, full backward compatibility.
- [x] Unit tests cover SQLite-populated vs file-fallback paths; gates green
      (`ruff check src/`, `mypy src/`, `pytest`).

## 9. Definition of Done (Sprint 2, Item 3 — periodic snapshot scheduler)

- [x] `dashboard/kpis/scheduler.py` provides `run_snapshot()` (collect all KPIs
      and ingest into SQLite via `KPIPipeline`) and a time-gated
      `KPISnapshotScheduler` with a configurable interval.
- [x] The executor daemon runs the scheduler inside its polling loop — cron in
      the daemon, not only at boot — with `--kpi-snapshot-interval` on
      `ai-company executor start` (default 300 s; `0` disables).
- [x] Collection is best-effort and never raises; no snapshot is taken when the
      database is unavailable.
- [x] Unit tests cover interval gating, disable, reset, no-database, and
      store-to-SQLite behaviour; gates green (`ruff check src/`, `mypy src/`,
      `pytest`).

## 10. Definition of Done (Sprint 3, Item 1 — per-agent performance, model usage, error analysis)

- [x] `dashboard/data_service.py` exposes `get_agent_performance_report()` and
      `get_agent_performance_summary()` — SQLite-first read-through accessors
      wrapping `AgentPerformanceAnalytics`, returning `None` when empty so
      callers fall back to files.
- [x] `GET /api/agents/performance` returns `leaderboard`, `model_usage`,
      `task_durations`, and `error_analysis` alongside the legacy
      registry-based `agents` list, with a `source` field (`sqlite` | `files`).
- [x] `GET /api/agents/{name}/performance` returns a single agent's full summary
      (tasks, completion/error rates, tool usage, cost, audit events).
- [x] The `/agents/{name}` route shadowing that made `/api/agents/performance`
      return 404 is fixed — the performance routes register before the dynamic
      `/agents/{name}` route.
- [x] File-derived fallbacks mirror the `full_report` shape so the endpoints
      never render blank before a backfill has run.
- [x] Unit/integration tests cover both the SQLite and file-fallback paths;
      gates green (`ruff check src/`, `mypy src/`, `pytest`).

## 11. Definition of Done (Sprint 3, Item 2 — company KPIs vs targets from live telemetry)

- [x] `dashboard/data_service.py` exposes `get_company_kpi_summary(days=30,
      project_root=None)` — reads `config/company/kpis.yaml` for the 5 company
      KPI targets and computes `current` from telemetry where mappable:
      `KPI-004` Build Success Rate from task completion (`completed / (completed
      + failed)`, `days`-window), `KPI-003` Agent Utilization Rate from distinct
      active agents vs the `company-registry.yaml` count; SQLite-first with
      `.opencode/inbox.json` fallback (`source`: `sqlite` | `files` | `config`).
      Never raises — missing config returns an empty summary.
- [x] `GET /api/company-kpis?days=30` returns the full summary shape
      (`collected_at`, `period_days`, `kpis[]` with `id/name/category/owner/
      frequency/unit/target/current/status/gap/computed/source`, and
      `summary` counts by status) — replaces the previous raw static list;
      `days` validated (`ge=1, le=365`, 422 otherwise).
- [x] Frontend KPI page renders a "Company KPIs vs Targets" card grid
      (current/target/unit/status badge/gap/live-or-config hint) plus a
      Current-vs-Target bar chart; department KPI cards no longer render
      "undefined" — live telemetry values are merged onto definitions.
- [x] Unit/integration tests cover SQLite + file-fallback + config-fallback +
      missing-config + window-filter + endpoint contract (7 new tests);
      gates green (`ruff check src/ tests/`, `mypy src/`, `pytest` —
      1501 passing).
