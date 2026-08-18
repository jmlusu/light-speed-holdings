# Research: Dashboard telemetry sources for the Org Health score

Catalog of data sources, their shapes, and gaps for computing an Org Health
score (Req. F5 / F4; maps to wayfinder ticket #23).

## Sources (callers / stores)

| Source | Module | Query / accessor | Update cadence | Output shape |
|--------|--------|------------------|----------------|--------------|
| Task pipeline (file) | `dashboard/data_service.py` | `_read_all_tasks`, `get_all_tasks` | on each KPI collect + live via WS | list[dict] with `status` ∈ pending/in_progress/completed/failed/escalated, `department`, `cost_usd`, `started_at`, `completed_at`, `agent_id` |
| KPI history (file) | `dashboard/analytics.py` `KPIHistoryStore` | `get_history`, `list_departments` | per collect cycle, NDJSON append | entries with `timestamp`, `current`, `target`, per-KPI values per department |
| SQLite state store | `dashboard/repository.py` `StateStore` | read-through `DashboardStateStore` | on demand; mirrors JSON | relational snapshot of tasks, kpis, approvals, escalations |
| LLM cost / budget | `llm/cost_tracker.py` `CostTracker` | `check_budget`, `daily_budget_exceeded`, per-agent cost export (`_per_agent_costs_from_audit`) | per LLM call | token counts, `cost_usd`, daily + per-task budget state |
| Audit trail | `audit/reader.py` `AuditReader` | `iter_events`, filter by type/id | append-only JSONL + SQLite mirror | immutable `AuditEvent` records carrying `correlation_id`, task/agent, tool, cost |

## Live KPIs surfaced today (`dashboard/api.py`)

- `collect_all_kpis()` → `/api/v1/dashboard` / `/api/v1/ceo-dashboard`:
  `KPIs` model = pending_tasks, in_progress, completed, failed, escalated,
  pending_approvals, open_escalations, last_activity, cost_today, etc.
- `get_company_kpi_summary()` → KPI-003 (agent utilization), KPI-004 (build
  success rate); KPI-001/002/005 have no backing source (render "n/a").

## Gaps (no known source)

- Revenue/lead/mrr (KPI-001), pipeline value (KPI-002), lead-gen (KPI-005).
- Per-agent token-spike / loop / hallucination telemetry (F4) — only z-score
  cost/error-rate anomaly detection exists (`ml/anomaly.py`).
- No persisted 0–100 trend for the score yet.

## Verdict for #26 (Org Health composition)

Enough inputs exist to compose: task-success ratio (completed/failed/escalated),
agent utilization (KPI-003), build success (KPI-004), open approvals/escalations,
and budget burn — all with known accessors. The revenue/lead KPIs need a
separate effort; treat them as 0/unavailable in the score.

Artifact for wayfinder #23 — catalog complete. Findings live here; link from the
Org Health composition ticket (#26).
