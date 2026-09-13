# Design: Revenue Attribution Model

| Field | Value |
|-------|-------|
| **Status** | Proposed |
| **Date** | 2026-08-19 |
| **Owner** | `@jmlus` |
| **Related Files** | `src/ai_company/data/revenue_analytics.py`, `src/ai_company/dashboard/kpis/`, `static/js/app.js`, `src/ai_company/models/models.py` |
| **Requirement** | F5 — Real-time output metrics tied to individual agent performance (e.g. $12k pipeline at $42 in API fees) |

---

## 1. What Exists Today

The foundation is solid. We already have:

| Layer | What | Where |
|-------|------|-------|
| Data | `RevenueAnalytics` class — per-agent costs, per-task revenue, ROI, department rollups, daily trend | `src/ai_company/data/revenue_analytics.py` |
| Models | `RevenueAttribution` (agent-level) and `RevenueSummary` (rollup) Pydantic models | `src/ai_company/models/models.py` |
| API | `/api/v1/revenue-attribution` endpoint (already wired in `api.py`) | `src/ai_company/dashboard/api.py` |
| Collector | `KPICollector` ABC — `department` attr + `collect() -> dict` abstract method | `src/ai_company/dashboard/kpis/base.py` |
| Frontend | Alpine.js `dashboard()` component with `kpis` object, WebSocket `kpi_update` listener, Chart.js gauges + sparklines | `static/js/app.js`, `src/ai_company/dashboard/static/js/ceo-hero-prototype.js` |

### Gaps to close for F5

| Gap | Problem |
|-----|---------|
| No metric taxonomy | Revenue, pipeline, and cost metrics are scattered across `RevenueAnalytics`, `finance.py`, and `sales.py` with no shared vocabulary |
| No attribution model definition | `RevenueAnalytics` uses "last-task-wins" implicitly but this is undocumented and not configurable |
| No agent-level revenue widget | The dashboard shows cost-per-agent (leaderboard) but no revenue-per-agent or ROI-per-agent |
| No cost-to-revenue linkage on frontend | Users see $42 API fees and $12k pipeline as separate numbers with no visual connection |

---

## 2. Metric Taxonomy

All revenue attribution metrics fall into three tiers. Every metric must have a **canonical name**, **unit**, **aggregation rule**, and **source table**.

### 2.1 Tier 1 — Raw Signals

| Canonical Name | Unit | Source | Description |
|----------------|------|--------|-------------|
| `task.cost` | USD | `cost_records.cost_usd` | LLM / tool cost for a single task execution |
| `task.revenue` | USD | `revenue_transactions.amount` | Revenue from a transaction linked to a task via `linked_task_id` |
| `task.duration_ms` | ms | `tasks.started_at` → `tasks.completed_at` | Wall-clock time for a task |
| `task.tokens_in` | count | `cost_records.input_tokens` | Input tokens consumed |
| `task.tokens_out` | count | `cost_records.output_tokens` | Output tokens consumed |

### 2.2 Tier 2 — Agent-Level Metrics

Derived by aggregating Tier 1 over a time window, grouped by `agent_id`.

| Canonical Name | Formula | Unit | Description |
|----------------|---------|------|-------------|
| `agent.revenue` | `SUM(task.revenue)` where `task.agent = X` | USD | Total revenue attributed to an agent |
| `agent.cost` | `SUM(task.cost)` where `task.agent = X` | USD | Total cost incurred by an agent |
| `agent.roi` | `agent.revenue / agent.cost` | ratio | Return on investment. `∞` → show as `—` |
| `agent.revenue_per_task` | `agent.revenue / agent.tasks_completed` | USD/task | Average revenue per completed task |
| `agent.cost_per_task` | `agent.cost / agent.tasks_completed` | USD/task | Average cost per completed task |
| `agent.tasks_completed` | `COUNT(tasks)` where `status = 'completed'` | count | Volume of work delivered |
| `agent.pipeline_value` | `SUM(task.revenue)` where `status ∈ {pending, in_progress}` | USD | Forward-looking pipeline (not yet closed) |

### 2.3 Tier 3 — Department & Company Rollups

| Canonical Name | Formula | Unit |
|----------------|---------|------|
| `dept.revenue` | `SUM(agent.revenue)` for agents in department | USD |
| `dept.cost` | `SUM(agent.cost)` for agents in department | USD |
| `dept.roi` | `dept.revenue / dept.cost` | ratio |
| `company.revenue` | `SUM(dept.revenue)` | USD |
| `company.cost` | `SUM(dept.cost)` | USD |
| `company.roi` | `company.revenue / company.cost` | ratio |
| `company.revenue_trend` | Daily `SUM(task.revenue)` over period | USD/day |

### 2.4 Naming Convention

All metric names follow the pattern `{scope}.{noun}` where scope is `task`, `agent`, `dept`, or `company`. This maps directly to API response keys and Alpine.js state properties.

---

## 3. Attribution Model

Revenue must be traced from a dollar amount back to the agent(s) that created it. We define three strategies, defaulting to **task-linked**.

### 3.1 Strategy: Task-Linked (Default)

```
revenue_transaction.linked_task_id → tasks.id → tasks.assignee → agent_id
```

- A revenue transaction links to exactly **one task** via `linked_task_id`.
- That task has exactly **one assignee**.
- 100% of the transaction amount is attributed to that agent.

**When to use:** Most cases. The task is the atomic unit of work.

### 3.2 Strategy: Multi-Agent Split

For tasks with multiple agents (e.g. `Sales Agent` qualifies a lead, `Finance Agent` closes it):

```python
# Proportional split by token cost
agent_a_cost = 30.00  # Sales Agent
agent_b_cost = 12.00  # Finance Agent
total_cost = 42.00
revenue = 12_000.00

agent_a_revenue = revenue * (agent_a_cost / total_cost)  # $8,571.43
agent_b_revenue = revenue * (agent_b_cost / total_cost)  # $3,428.57
```

- Split proportional to each agent's cost contribution on the task.
- Stored in a `revenue_attribution_splits` table (new).
- **Not implemented yet** — task-linked is sufficient for V1.

### 3.3 Strategy: Time-Decay

For revenue that arrives long after the work:

```python
# Revenue credited inversely proportional to days since task completion
days_since = (revenue_date - task_completed_date).days
weight = 1 / (1 + days_since * decay_factor)
```

- Useful for SaaS subscriptions where an agent's work generates revenue over months.
- **Not implemented yet** — V2 enhancement.

### 3.4 Attribution Edge Cases

| Scenario | Rule |
|----------|------|
| Revenue transaction has no `linked_task_id` | Attributed to `"unattributed"` bucket. Visible in dashboard as a warning. |
| Task has no `assignee` | Revenue attributed to `"unassigned"` bucket. |
| Agent no longer in registry | Revenue still attributed by historical `agent_id`. Department shows as `"unknown"`. |
| Revenue currency ≠ USD | Converted via `revenue_transactions.exchange_rate` before attribution. |

---

## 4. Widget Design

### 4.1 Revenue Attribution Hero Card

Placed in the dashboard's KPI card row (alongside existing pending/completed/failed cards).

```
┌─────────────────────────────────────────────────┐
│  💰 Revenue Attribution            30d ▾        │
│                                                 │
│  $12,847.00               ROI: 305.88x          │
│  total revenue             $42.00 cost          │
│                                                 │
│  ████████████████████░░░░  $12,847 / $15,000    │
│  pipeline: $2,153.00                              │
│                                                 │
│  Top Performer                                   │
│  ┌─────────────────────────────────────┐         │
│  │ 🏆 sales-agent    $11,200  ROI 467x │         │
│  └─────────────────────────────────────┘         │
└─────────────────────────────────────────────────┘
```

**State properties (Alpine.js):**

```javascript
revenueAttribution: {
  totalRevenue: 12847.00,
  totalCost: 42.00,
  overallRoi: 305.88,
  pipelineValue: 2153.00,
  targetRevenue: 15000.00,
  topPerformer: { agentId: 'sales-agent', revenue: 11200, roi: 467 },
  byAgent: [],       // full list
  byDepartment: [],  // grouped
  periodDays: 30,
}
```

### 4.2 Agent ROI Leaderboard

Extends the existing cost leaderboard (see `app.js` `leaderboard` array) with revenue columns.

| Agent | Tasks | Revenue | Cost | ROI | Rev/Task |
|-------|-------|---------|------|-----|----------|
| sales-agent | 47 | $11,200 | $24.00 | 467x | $238.30 |
| finance-agent | 12 | $1,647 | $18.00 | 91.5x | $137.25 |
| ops-agent | 31 | $0 | $0.00 | — | $0.00 |

**Sort options:** revenue (default), ROI, cost, tasks completed.

### 4.3 Revenue vs Cost Trend Chart

Dual-axis line chart (Chart.js, matching existing `initCompanyKPICharts()` pattern):

- **Left axis:** Revenue (USD) — green line
- **Right axis:** Cost (USD) — red line
- **X axis:** Days (last 30)
- **Overlay:** Shaded area between lines represents net profit

Data source: `/api/v1/revenue-attribution/trend` (new endpoint, wrapping `RevenueAnalytics.get_revenue_trend()`).

### 4.4 Department Revenue Breakdown

Horizontal bar chart showing revenue by department, with cost overlay:

```
Sales       ████████████████████████  $11,200  ($24)
Finance     ████                      $1,647   ($18)
Operations  ░                         $0       ($0)
```

---

## 5. Data Flow

### 5.1 Ingestion Path

```
Revenue Transaction
    │
    ▼
revenue_transactions table
    │  (linked_task_id, amount, currency, status)
    ▼
tasks table
    │  (assignee → agent_id)
    ▼
cost_records table
    │  (agent_name, cost_usd, input_tokens, output_tokens)
    ▼
RevenueAnalytics.get_revenue_attribution()
    │  joins: revenue_transactions → tasks → cost_records
    ▼
RevenueSummary model
    │  (total_revenue, total_cost, overall_roi, by_agent[], by_department[])
    ▼
API response → Alpine.js state → Widgets
```

### 5.2 Real-Time Updates

The existing WebSocket `kpi_update` listener in `app.js` handles live updates. We extend the payload:

```javascript
// Current payload (from app.js line ~400)
{
  "type": "kpi_update",
  "data": {
    "pending": 5,
    "completed": 12,
    // ... existing fields
  }
}

// Extended payload (new fields)
{
  "type": "kpi_update",
  "data": {
    // ... existing fields
    "revenue": {
      "total": 12847.00,
      "cost": 42.00,
      "roi": 305.88,
      "pipeline": 2153.00,
      "top_performer": { "agent": "sales-agent", "revenue": 11200 }
    }
  }
}
```

### 5.3 Collector Integration

New collector subclassing `KPICollector`:

```python
# src/ai_company/dashboard/kpis/revenue.py

from ai_company.dashboard.kpis.base import KPICollector

class RevenueCollector(KPICollector):
    department = "revenue"

    def __init__(self, revenue_analytics: RevenueAnalytics) -> None:
        self._analytics = revenue_analytics

    async def collect(self) -> dict:
        summary = self._analytics.get_revenue_attribution(period_days=30)
        return {
            "total_revenue": summary.total_revenue,
            "total_cost": summary.total_cost,
            "overall_roi": summary.overall_roi,
            "by_agent": [
                {
                    "agent_id": a.agent_id,
                    "department": a.department,
                    "revenue": a.revenue_attributed,
                    "cost": a.cost_incurred,
                    "roi": a.roi,
                    "tasks": a.tasks_completed,
                    "revenue_per_task": a.revenue_per_task,
                }
                for a in summary.by_agent
            ],
            "by_department": [
                {
                    "department": a.department,
                    "revenue": a.revenue_attributed,
                    "cost": a.cost_incurred,
                    "roi": a.roi,
                    "tasks": a.tasks_completed,
                }
                for a in summary.by_department
            ],
        }
```

Register in `ALL_COLLECTORS` (`kpis/__init__.py`):

```python
from ai_company.dashboard.kpis.revenue import RevenueCollector

ALL_COLLECTORS = [
    BudgetCollector(),
    LLMSpendCollector(),
    PipelineCollector(),
    LeadsCollector(),
    TaskCompletionCollector(),
    RevenueCollector(revenue_analytics=...),  # injected
]
```

---

## 6. API Contract

### 6.1 `GET /api/v1/revenue-attribution`

**Query params:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `period_days` | int | 30 | Lookback window |

**Response (200):**

```json
{
  "total_revenue": 12847.00,
  "total_cost": 42.00,
  "overall_roi": 305.88,
  "period_days": 30,
  "by_department": [
    {
      "agent_id": "sales__department_total",
      "department": "sales",
      "tasks_completed": 47,
      "revenue_attributed": 11200.00,
      "cost_incurred": 24.00,
      "roi": 466.67,
      "revenue_per_task": 238.30
    }
  ],
  "by_agent": [
    {
      "agent_id": "sales-agent",
      "department": "sales",
      "tasks_completed": 47,
      "revenue_attributed": 11200.00,
      "cost_incurred": 24.00,
      "roi": 466.67,
      "revenue_per_task": 238.30
    }
  ]
}
```

> **Status:** This endpoint already exists in `api.py` and wraps `RevenueAnalytics.get_revenue_attribution()`.

### 6.2 `GET /api/v1/revenue-attribution/trend` (New)

**Query params:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `period_days` | int | 30 | Lookback window |

**Response (200):**

```json
{
  "trend": [
    { "date": "2026-07-21", "revenue": 420.00, "revenue_usd": 420.00 },
    { "date": "2026-07-22", "revenue": 1350.00, "revenue_usd": 1350.00 }
  ],
  "period_days": 30
}
```

> **Status:** `RevenueAnalytics.get_revenue_trend()` already exists. Needs an API endpoint wrapper.

### 6.3 `GET /api/v1/kpis` (Extended)

Add `revenue` key to the existing summary response:

```json
{
  "pending": 5,
  "completed": 12,
  "failed": 1,
  "escalated": 0,
  "in_progress": 3,
  "revenue": {
    "total": 12847.00,
    "cost": 42.00,
    "roi": 305.88,
    "pipeline": 2153.00
  }
}
```

> **Status:** Requires extending `collect_all_kpis()` to include the `RevenueCollector` output.

---

## 7. Implementation Plan

### Phase 1 — Backend (V1)

| Task | Effort | Depends On |
|------|--------|------------|
| Create `kpis/revenue.py` — `RevenueCollector` subclass | S | — |
| Register `RevenueCollector` in `ALL_COLLECTORS` | S | RevenueCollector |
| Add `/api/v1/revenue-attribution/trend` endpoint | S | — |
| Extend `/api/v1/kpis` response with `revenue` key | M | RevenueCollector |

### Phase 2 — Frontend (V1)

| Task | Effort | Depends On |
|------|--------|------------|
| Add `revenueAttribution` state to Alpine.js `dashboard()` | S | Phase 1 |
| Build Revenue Hero Card component | M | revenueAttribution state |
| Extend Agent Leaderboard with revenue/ROI columns | S | revenueAttribution state |
| Add Revenue vs Cost dual-axis chart | M | `/trend` endpoint |

### Phase 3 — Enhancements (V2)

| Task | Effort |
|------|--------|
| Multi-agent revenue split (`revenue_attribution_splits` table) | L |
| Time-deay attribution for SaaS revenue | L |
| Department revenue breakdown chart | M |
| Export revenue report to CSV/XLSX | S |

---

## 8. Success Criteria

| Criterion | How We Know |
|-----------|-------------|
| Every revenue dollar traces to an agent | `agent.revenue + unattributed = total_revenue` within rounding |
| Dashboard shows revenue + cost + ROI in one view | Visual inspection of Hero Card |
| Real-time updates work | WebSocket `kpi_update` includes revenue data within 5s of task completion |
| No regressions | `pytest` passes, existing cost leaderboard unchanged |
| Attribution accuracy | Manual audit: 10 random transactions verified against agent assignments |
