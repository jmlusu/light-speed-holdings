# CEO Dashboard — Complete Data Element Mapping

> Generated: 2026-08-24 | Covers: All 7 frontend sections + 2 backend-only aggregations

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (index.html)                       │
│  Alpine.js reads `this.orgHealth`, `this.kpis`, `this.tasks`, etc. │
│  Each polled via REST every ~10s from /api/v1/*                     │
└───────────────┬─────────────────────────────────────────────────────┘
                │ HTTP GET /api/v1/*
┌───────────────▼─────────────────────────────────────────────────────┐
│                     REST API LAYER (api.py)                         │
│  Router prefix: /api/v1                                            │
│  30+ endpoints; 6 serve the main dashboard                         │
└───────────────┬─────────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────────┐
│              DATA SERVICE LAYER (data_service.py)                   │
│  SQLite-first, file-fallback pattern (Sprint 1 / S1.3)            │
│  Functions: get_all_tasks(), get_cost_summary(),                   │
│             get_company_kpi_summary(), get_kpi_history()           │
└───────┬─────────────┬─────────────┬───────────────┬────────────────┘
        │             │             │               │
┌───────▼──────┐ ┌────▼────┐ ┌─────▼─────┐ ┌──────▼──────┐
│   SQLite     │ │  YAML   │ │   JSON    │ │  MessageBus │
│  (DB file)   │ │ configs │ │  files    │ │  (inbox)    │
│              │ │         │ │           │ │             │
│ tasks        │ │ approval│ │ agent-    │ │ .opencode/  │
│ cost_records │ │ escaltion│ │ registry  │ │ inbox.json  │
│ kpi_history  │ │ scheduler│ │ cost_     │ │             │
│              │ │ kpis.yaml│ │ tracker   │ │             │
└──────────────┘ └─────────┘ └───────────┘ └─────────────┘
```

---

## Section 1: Org Health Hero (Hero Gauge)

**API Endpoint:** `GET /api/v1/org-health`
**Frontend Variable:** `this.orgHealth`
**Load Trigger:** `fetchOrgHealth()` on page init + poll

| Element | Frontend Binding | API Field | Source | Fallback Chain |
|---------|-----------------|-----------|--------|----------------|
| **Composite Score (0-100)** | `orgHealth?.score` | `score` | `OrgHealthCalculator.compute()` — weighted sum of 4 components | — (computed, not stored) |
| **Health Band** | `orgHealth?.band` | `band` | `OrgHealthCalculator._score_to_band()` | "red" default if no band matches |
| **Collected At** | `orgHealth?.collected_at` | `collected_at` | `datetime.now(timezone.utc).isoformat()` | — |
| **Trend History** | (chart data) | `trend[]` | SQLite `KPIPipeline.get_history("org_health", kpi_key="composite_score")` | File `KPIHistoryStore.get_history()` fallback |

### Component Breakdown (expandable)

| Component | Weight | Score Computation | Source |
|-----------|--------|-------------------|--------|
| **task_success_rate** | 30% | `completed / total * 100` over 30-day window | SQLite tasks → `.opencode/inbox.json` via `_company_window_tasks()` |
| **agent_utilization** | 25% | `active_agents / registered_agents * 100` | Active: sender/receiver IDs from tasks; Registered: `company-registry.yaml` |
| **cost_efficiency** | 25% | `100 - (spent/budget * 100) + 50`, clamped 0-100 | SQLite `CostAnalytics.total_cost()` → `orchestrator/cost_tracker.json` |
| **error_rate** | 20% | `100 - (error_tasks/total * 100)` | Tasks with status "failed"/"error"/"cancelled" |

**Config:** `config/org_health.yaml` (bands + component weights)

---

## Section 2: Alert Bar (Below Gauge)

**API Endpoint:** `GET /api/v1/dashboard`
**Frontend Variable:** `this.kpis`

| Element | Frontend Binding | API Field | Source | Fallback |
|---------|-----------------|-----------|--------|----------|
| **Pending Approvals** | `kpis.pending_approvals` | `KPIs.pending_approvals` | `orchestrator/approvals.yaml` — requests with `status=pending` AND (`expires_at` absent OR > now) | 0 |
| **Open Escalations** | `kpis.open_escalations` | `KPIs.open_escalations` | `orchestrator/escalation.yaml` — events with `resolved != true` | 0 |
| **In-Progress Tasks** | `kpis.in_progress_tasks` | `KPIs.in_progress_tasks` | SQLite `TaskStore.count_by_status()` → `.opencode/inbox.json` | 0 |

---

## Section 3: Charts Row

### Task Status Chart

**API Endpoint:** `GET /api/v1/dashboard`
**Frontend Variable:** `this.kpis` → `updateChartsFromKPIs()`

| Chart Slice | KPI Field | Source |
|-------------|-----------|--------|
| Pending | `kpis.pending_tasks` | Task count where `status == "pending"` |
| In Progress | `kpis.in_progress_tasks` | Task count where `status == "in_progress"` |
| Completed | `kpis.completed_tasks` | Task count where `status == "completed"` |
| Failed | `kpis.failed_tasks` | Task count where `status == "failed"` |
| Escalated | `kpis.escalated_tasks` | Task count where `status == "escalated"` |

**Task Source:** SQLite `TaskStore.get_all()` → fallback to `MessageBus.get_all_tasks()` → `.opencode/inbox.json`

### Department Load Chart

**API Endpoint:** `GET /api/v1/departments`
**Frontend Variable:** `this.departments`

| Chart Data | Source |
|------------|--------|
| Agent count per department | `company/agent-registry.json` — `department` field per agent |

---

## Section 4: Cost Breakdown

**API Endpoint:** `GET /api/v1/costs/summary`
**Frontend Variable:** `this.costSummary`, `this.agentCosts`

| Element | Frontend Binding | API Field | Source | Fallback |
|---------|-----------------|-----------|--------|----------|
| **Total Spent** | `costSummary.total` | `total_spent` | SQLite `CostAnalytics.total_cost()` | `orchestrator/cost_tracker.json` → `total_spent` |
| **Avg Cost / Task** | `costSummary.avgPerTask` | `avg_cost_per_task` | `total_spent / completed_tasks` | 0 |
| **Total Tasks** | `costSummary.totalTasks` | `total_tasks` | SQLite `TaskStore.count()` | `len(tasks)` from inbox |
| **Completed Tasks** | — | `completed_tasks` | SQLite `TaskStore.count_by_status()["completed"]` | Count from inbox |
| **LLM Spend** | — | `llm_spend` | SQLite `CostAnalytics.total_cost()` | `orchestrator/cost_tracker.json` → `llm_spend` |
| **Budget** | — | `total_budget` | — | `orchestrator/cost_tracker.json` → `total_budget` |
| **Budget Utilization %** | `this.budgetPct` | `budget_utilization` | `(total_spent / total_budget) * 100` | 0 |
| **Top 5 Agents** | `agentCosts` (sliced) | `per_agent_costs[]` | SQLite `CostAnalytics.breakdown_by_agent()` — `{agent_name, cost_usd, calls}` | Audit JSONL `.opencode/audit` → `metadata.cost` per agent |
| **Cost Trend Sparkline** | `costSummary.costTrend` | `cost_trend[]` | SQLite `CostAnalytics.daily_cost_trend()` — `{day, total_cost}` | `KPIHistoryStore.get_history("finance", kpi_key="budget_utilization")` |

---

## Section 5: Recent Tasks Table

**API Endpoint:** `GET /api/v1/tasks`
**Frontend Variable:** `this.tasks` (sliced to first 10)

| Column | Binding | Source |
|--------|---------|--------|
| Receiver | `t.receiver_id` | Task `receiver_id` |
| Instruction | `t.instruction` | Task `instruction` |
| Priority | `t.priority` | Task `priority` (high/medium/low) |
| Status | `t.status` | Task `status` (pending/in_progress/completed/failed/escalated) |
| Created | `t.created_at` | Task `created_at` (ISO timestamp) |

**Data Source:** SQLite `TaskStore.get_all()` → fallback `MessageBus.get_all_tasks()` → `.opencode/inbox.json`

---

## Section 6: /kpis Page (Department KPI Cards)

**API Endpoints:** `GET /api/v1/kpis`, `GET /api/v1/kpis/live`, `GET /api/v1/kpis/summary`, `GET /api/v1/company-kpis`

### Department KPI Definitions (card layout)
**Endpoint:** `GET /api/v1/kpis`
**Frontend Variable:** `this.kpiDepartments`

| Element | Source |
|---------|--------|
| Department names | `company/departments.yaml` — `departments.{name}` |
| KPI definitions (id, name, target, unit) | `company/config/kpis.yaml` — `departments.{dept}.kpis[]` |

### Live KPI Values (overlaid on definitions)
**Endpoint:** `GET /api/v1/kpis/live`
**Frontend Variable:** `this.liveKPIData`, merged via `mergeLiveKPIValues()`

| Element | Source |
|---------|--------|
| `current`, `target`, `unit`, `status` per KPI | `collect_all_kpis()` → 8 department collectors |

**Department Collectors:**

| Department | Collector | Key Sources |
|------------|-----------|-------------|
| engineering | `EngineeringKPICollector` | MessageBus tasks, `orchestrator/escalation.yaml`, `orchestrator/scheduler.yaml`, SOP freshness |
| finance | `FinanceKPICollector` | `company/config/kpis.yaml`, `orchestrator/cost_tracker.json`, `company/agent-registry.json`, SQLite revenue |
| hr | `HRKPICollector` | `company/agent-registry.json`, `company/departments.yaml` |
| marketing | `MarketingKPICollector` | `orchestrator/marketing/campaigns.json`, `content_log.json`, SQLite tasks |
| sales | `SalesKPICollector` | `orchestrator/sales/pipeline.json`, `leads.json`, SQLite tasks |
| customer_success | `CustomerSuccessKPICollector` | SOP freshness, ticket resolution time |
| legal | `LegalKPICollector` | SOP freshness, compliance items |
| org_health | `OrgHealthKPICollector` | `OrgHealthCalculator` composite score |

### Company-Level KPIs
**Endpoint:** `GET /api/v1/company-kpis`
**Frontend Variable:** `this.companyKPIs`, `this.companyKPISummary`
**Computed by:** `data_service.get_company_kpi_summary()`

| KPI | Target | Current | Source | Status |
|-----|--------|---------|--------|--------|
| **KPI-001** Annual Recurring Revenue | $10M | `null` | No revenue ledger exists | `info` |
| **KPI-002** Customer Satisfaction | 95% | `null` | `orchestrator/cs/surveys.json` (empty) | `info` |
| **KPI-003** Agent Utilization Rate | 80% | Computed | `distinct active agents / registered agents * 100` over 30-day window | `on_track` / `below_target` |
| **KPI-004** Build Success Rate | 99.5% | Computed | `completed / (completed + failed) * 100` over 30-day window | `on_track` / `below_target` |
| **KPI-005** Employee Net Promoter Score | 75 | `null` | No people-survey source | `info` |

---

## Section 7: /escalations Page

**API Endpoints:** `GET /api/v1/approvals`, `GET /api/v1/escalations`
**Frontend Variable:** `this.approvals`, `this.escalations`

### Approvals
| Field | Source |
|-------|--------|
| `id`, `task_id`, `agent_id`, `status`, `risk_level`, `cost_estimate` | `orchestrator/approvals.yaml` → `requests[]` |
| Filter: only `status == "pending"` AND (`expires_at` absent OR > now) | — |

### Escalations
| Field | Source |
|-------|--------|
| `task_id`, `from_agent`, `to_agent`, `reason`, `resolved` | `orchestrator/escalation.yaml` → `events[]` |
| Filter: only `resolved != true` | — |

---

## Section 8: /tasks Page (Paginated)

**API Endpoint:** `GET /api/v1/tasks/paginated?page=N&page_size=N&sort_by=...&sort_dir=...`
**Frontend Variable:** `this.tasks`, `this.taskTotal`, `this.taskTotalPages`, `this.taskCountsByStatus`

| Field | Source |
|-------|--------|
| `items[]` | SQLite `TaskStore` with pagination → `MessageBus.get_all_tasks()` fallback |
| `total` | `TaskStore.count()` |
| `counts_by_status` | `TaskStore.count_by_status()` |
| Filters: `priority`, `department`, `agent`, `status` | Query params applied to task list |

---

## Section 9: CEO Dashboard Aggregate (Backend-Only)

**API Endpoint:** `GET /api/v1/ceo-dashboard`
**Returns:** Consolidated JSON with all sections combined

| Sub-section | Source |
|-------------|--------|
| `company_health.departments` | `collect_all_kpis()` — all 8 department collectors |
| `company_health.company_kpis` | `config/company/kpis.yaml` → `kpis.company[]` |
| `agent_performance` | `company/agent-registry.json` — count by type/department |
| `cost_tracking` | `orchestrator/cost_tracker.json` → `total_budget`, `total_spent`, `llm_spend` |
| `task_pipeline` | `_read_all_tasks()` — count by status |
| `escalation_alerts` | `orchestrator/escalation.yaml` → unresolved events |
| `pending_approvals` | `orchestrator/approvals.yaml` → pending + non-expired |
| `scheduled_tasks` | `orchestrator/scheduler.yaml` → `tasks[]` |
| `uptime_seconds` | `time.time() - _START_TIME` |

---

## Data Source Inventory

### SQLite Tables (Sprint 3, S1.3)
| Table | Class | Key Fields |
|-------|-------|------------|
| `tasks` | `TaskStore` | id, sender_id, receiver_id, instruction, priority, status, created_at |
| `cost_records` | `CostAnalytics` | agent_name, cost_usd, calls, day |
| `kpi_history` | `KPIPipeline` | department, kpi_key, current_value, target_value, unit, status, timestamp |

### YAML Configs
| Path | Used By |
|------|---------|
| `config/org_health.yaml` | Org health bands + component weights |
| `config/company/kpis.yaml` | Company-level KPI targets + definitions |
| `company/departments.yaml` | Department names + structure |
| `company/agent-registry.json` | Agent list (name, type, department) |
| `orchestrator/approvals.yaml` | Approval requests |
| `orchestrator/escalation.yaml` | Escalation events |
| `orchestrator/scheduler.yaml` | Scheduled tasks |

### JSON State Files
| Path | Used By |
|------|---------|
| `.opencode/inbox.json` | Task list (via MessageBus) |
| `orchestrator/cost_tracker.json` | Budget + spend totals |
| `.opencode/audit` (JSONL) | Per-agent cost breakdown (file fallback) |
| `orchestrator/cs/surveys.json` | Customer satisfaction (empty) |
| `orchestrator/marketing/campaigns.json` | Marketing campaigns |
| `orchestrator/sales/pipeline.json` | Sales pipeline |

### StateStore Allowlist (`repository.py`)
All dashboard file I/O goes through `StateStore` → `FileStore`, restricted to:
```
.opencode/inbox.json
orchestrator/approvals.yaml
orchestrator/escalation.yaml
orchestrator/scheduler.yaml
orchestrator/devices.yaml
company/agent-registry.json
company/departments.yaml
company/models.yaml
company/config/kpis.yaml
config/company/kpis.yaml
orchestrator/cost_tracker.json
.opencode/audit
.opencode/dead_letter_queue.json
orchestrator/kpi_snapshots/  (prefix)
memory/                      (prefix)
.opencode/decompositions/    (prefix)
```

---

## Fallback Chain Summary

Every data path follows the **SQLite-first, file-fallback** pattern:

1. **SQLite** (if `Database` is usable AND table has records)
2. **File** (JSON/YAML via `StateStore`)
3. **Hard-coded default** (0, empty list, 50.0 for health scores)

This ensures the dashboard never renders blank — it always has data to show, even if stale.
