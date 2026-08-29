# CEO Dashboard — Master Data Dictionary

> **Single source of truth** for all dashboard data: endpoints, models, KPIs, source-to-target mappings, WebSocket events, frontend components, interaction contracts, organizational context, and design tokens.
> **Source of truth**: `src/ai_company/dashboard/` module tree.
> Every table, field, endpoint, and WebSocket topic listed below was verified against the running codebase.
> **Consolidated from**: 7 agent-authored documents (dashboard-owner, chief-of-staff, lead-frontend, senior-frontend-engineer, frontend-architect, frontend-engineer).
> **Last updated**: 2026-08-26

---

## Table of Contents

1. [Purpose & Target User](#1-purpose--target-user)
2. [Dashboard Tabs & Navigation](#2-dashboard-tabs--navigation)
3. [API Endpoint Catalog](#3-api-endpoint-catalog)
4. [Pydantic Model Schemas](#4-pydantic-model-schemas)
5. [KPI Payload Structure & Data Sources](#5-kpi-payload-structure--data-sources)
6. [Data Quality Fields](#6-data-quality-fields)
7. [KPI Definitions](#7-kpi-definitions)
8. [Source-to-Target Mapping](#8-source-to-target-mapping)
9. [Data Access Pattern](#9-data-access-pattern)
10. [Security Model](#10-security-model)
11. [WebSocket Events](#11-websocket-events)
12. [Organizational Hierarchy](#12-organizational-hierarchy)
13. [Data Responsibility Matrix](#13-data-responsibility-matrix)
14. [Frontend Component Architecture](#14-frontend-component-architecture)
15. [Frontend Data Flow & WebSocket Integration](#15-frontend-data-flow--websocket-integration)
16. [Frontend Component Data Contracts](#16-frontend-component-data-contracts)
17. [Task Status Lifecycle](#17-task-status-lifecycle)
18. [Offline Sync & PWA](#18-offline-sync--pwa)
19. [Toast Notification System](#19-toast-notification-system)
20. [API Contracts & Data Flow Diagrams](#20-api-contracts--data-flow-diagrams)
21. [Error Handling & Resilience](#21-error-handling--resilience)
22. [Design System & Theme Tokens](#22-design-system--theme-tokens)
23. [Enum Values](#23-enum-values)

---

## 1. Purpose & Target User

The CEO Dashboard is a **FastAPI + Alpine.js** web application that gives the human CEO a real-time operational view of their AI agent workforce. It is the single pane of glass for:

- **Task pipeline health** — pending, in-progress, completed, failed, escalated counts
- **Agent registry** — who exists, what department they belong to, who they report to
- **KPI monitoring** — 8 department-level collectors + company-level aggregations + live org-health score
- **Cost visibility** — budget utilization, per-agent LLM spend, cost-per-task trends
- **Approval/escalation workflows** — HITL gates, resolve/assign actions
- **Revenue tracking** — manual payment capture, webhook ingestion, ROI attribution
- **Audit & governance** — execution timeline, data-quality gap analysis

**Primary user:** `human-ceo` (authenticated via RBAC key in `X-API-Key` header).
**Auth model:** Three RBAC roles — `admin` (full access), `approve` (approve/reject), `run` (create tasks, manage workflows). All endpoints except `/health` require a valid key.

---

## 2. Dashboard Tabs & Navigation

| Tab | Route | Template | Purpose |
|-----|-------|----------|---------|
| Dashboard | `/` | `index.html` | CEO Hero org health gauge, task status chart, department load chart, cost breakdown, recent tasks |
| Agents | `/agents` | `agents.html` | Agent listing, search, detail |
| Tasks | `/tasks` | `tasks.html` | Paginated task table with filters, sort, kanban board, task detail slide-out, drag-and-drop, task decomposition |
| KPIs | `/kpis` | `kpis.html` | Department KPI cards, live KPI radar chart, target vs current bar chart, company KPI bar chart |
| Costs | `/costs` | `costs.html` | Cost trend line, per-agent cost bar, budget alerts, agent cost breakdown |
| Approvals | `/escalations` | `escalations.html` | Pending approval requests, approve/reject/edit actions, escalation events, resolve |
| Command Center | `/command-center` | `command-center.html` | 3 variants (Bridge, War Room, Cockpit), briefing items, workforce grid, model telemetry, activity stream |
| Mission Control | `/mission-control` | `mission-control.html` | Workflow pipeline UI, workflow instances, start/advance/complete/cancel workflows |
| Onboarding | `/onboarding` | `onboarding.html` | Persona templates (5 types), multi-step wizard, preview, generate |
| Finance | `/finance` | `finance.html` | Revenue, cost analysis |
| Org Chart | `/org-chart` | `org-chart.html` | Hierarchical tree, drag-and-drop reassignment |

---

## 3. API Endpoint Catalog

All endpoints live under the router prefix **`/api/v1`**. Response models are Pydantic schemas from `models.py` unless noted otherwise. Authentication: `X-API-Key` header (role-based). Page routes are exempt from auth (ADR-013).

### 3.1 Dashboard Core

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/dashboard` | `KPIs` | CEO-level KPI snapshot (tasks, approvals, escalations, agents, scheduler). Broadcasts via WebSocket. |
| GET | `/api/v1/kpis/live` | `dict` | Live KPI values from all 8 department collectors. |
| GET | `/api/v1/ceo-dashboard` | `dict` | CEO-wide overview (health, agents, costs, tasks, escalations, approvals, scheduled, company KPIs). |
| GET | `/api/v1/briefing` | `dict` | Executive briefing — priority-ordered attention items with summary metrics. |

### 3.2 Agents

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/agents` | `list[AgentSummary]` | List all registered agents. |
| GET | `/api/v1/agents/performance` | `dict` | Per-agent performance (leaderboard, durations, model usage, errors). |
| GET | `/api/v1/agents/{name}` | `AgentSummary` | Retrieve a single agent by name. |
| GET | `/api/v1/agents/{name}/performance` | `dict` | Single-agent performance summary. |
| GET | `/api/v1/org-chart` | `list[OrgNode]` | Hierarchical org chart rooted at the CEO. |
| PATCH | `/api/v1/agents/{name}/reports-to` | `dict` | Reassign agent's manager (requires `run` role). |

### 3.3 Tasks

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/tasks` | `list[TaskItem]` | List all tasks (optional `status` and `agent` filters). |
| GET | `/api/v1/tasks/paginated` | `PaginatedTasks` | Server-side paginated tasks (filters: status, priority, department, agent; sort: created_at, priority, status, receiver_id). |
| POST | `/api/v1/tasks` | `TaskItem` | Create a new task via MessageBus (requires `run` role). Rejects trivial instructions (≤5 chars, "do x", "test ..."). |
| PATCH | `/api/v1/tasks/{task_id}` | `TaskItem` | Partially update a task (requires `run` role). Broadcasts WebSocket event. |
| DELETE | `/api/v1/tasks/{task_id}` | `dict` | Delete a task by id (requires `run` role). Returns `{"ok": "true", "id": "..."}`. |
| GET | `/api/v1/tasks/{task_id}/subtasks` | `TaskDecomposition` | Get decomposition subtasks for a task. |
| POST | `/api/v1/tasks/{task_id}/decompose` | `TaskDecomposition` | AI-powered rule-based task decomposition. |

### 3.4 Approvals

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/approvals` | `list[ApprovalItem]` | All pending, non-expired approval requests. |
| POST | `/api/v1/approvals/{request_id}/approve` | `dict` | Approve a pending request (requires `approve` role). |
| POST | `/api/v1/approvals/{request_id}/reject` | `dict` | Reject a pending request (requires `approve` role). |
| PATCH | `/api/v1/approvals/{request_id}` | `dict` | Partial update (risk_level, cost_estimate) (requires `approve` role). |

### 3.5 Escalations

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/escalations` | `list[EscalationItem]` | All unresolved escalation events. |
| POST | `/api/v1/escalations/{task_id}/resolve` | `dict` | Resolve an open escalation (requires `approve` role; logs to audit trail). |

### 3.6 KPIs

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/kpis` | `dict` | All KPI *definitions* from `company/config/kpis.yaml`. |
| GET | `/api/v1/kpis/summary` | `list[dict]` | Flat summary of every KPI definition across departments. |
| GET | `/api/v1/kpis/history/{department}` | `list[dict]` | Historical KPI entries for a department (SQLite-first, file fallback). |
| GET | `/api/v1/kpis/trends/{department}` | `list[dict]` | Trend analysis (current vs previous period) for a department's KPIs. |
| GET | `/api/v1/kpis/alerts` | `dict` | Evaluate default alert rules against the latest KPI snapshot. |
| GET | `/api/v1/kpis/collect` | `dict` | Manually trigger a KPI collection cycle, persist to history, return snapshot. |
| GET | `/api/v1/kpis/summary-stats/{department}` | `list[dict]` | Rollup stats (min/max/mean/count) by period (daily/weekly/monthly). |
| GET | `/api/v1/company-kpis` | `dict` | Company-level KPIs vs targets (ARR, CSAT, Utilization, Build Success, eNPS). |

### 3.7 Costs

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/costs/summary` | `dict` | Cost summary: budget utilization, LLM spend, per-agent breakdown, cost trend. |
| POST | `/api/v1/project-costs` | `dict` | Record a project cost entry (requires database). |

### 3.8 Departments

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/departments` | `list[DepartmentInfo]` | List all registered departments. |
| GET | `/api/v1/departments/{name}/kpis` | `dict` | KPI definitions for a specific department. |
| GET | `/api/v1/departments/{name}/dashboard` | `dict` | Per-department drill-down (live KPIs, agents, tasks, escalations). |

### 3.9 Models

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/models` | `list[ModelRouteItem]` | Model routing assignments for all agents. |
| GET | `/api/v1/models/tiers` | `list[TierInfo]` | Available model tiers and provider configurations. |
| GET | `/api/v1/models/telemetry` | `list[ModelTelemetryItem]` | Per-model telemetry (request count, success rate, avg latency, cost) from audit log. |

### 3.10 Scheduler

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/scheduler` | `list[dict]` | All scheduled and recurring tasks from `orchestrator/scheduler.yaml`. |

### 3.11 Org Health

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/org-health` | `dict` | Composite score (0–100), health band, component breakdown, trend. |
| GET | `/api/v1/org-health/trend` | `list[dict]` | Org-health score trend over time (SQLite-first, file fallback). |
| GET | `/api/v1/org-health/anomalies` | `list[dict]` | Z-score anomaly detection on historical org-health component scores. |

### 3.12 Workflows

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/workflows` | `list[WorkflowSummary]` | List all registered workflow definitions. |
| GET | `/api/v1/workflows/instances` | `list[dict]` | List running workflow instances (optional `?workflow_id=`). |
| GET | `/api/v1/workflows/instances/{id}` | `dict` | Full status + step detail for a workflow instance. |
| POST | `/api/v1/workflows/{id}/start` | `dict` | Start a new instance of a workflow definition (requires `run` role). |
| POST | `/api/v1/workflows/instances/{id}/advance` | `dict` | Advance a workflow instance to its next step (requires `run` role). |
| POST | `/api/v1/workflows/instances/{id}/complete-step` | `dict` | Mark the current step as completed (requires `run` role). |
| POST | `/api/v1/workflows/instances/{id}/cancel` | `dict` | Cancel a running workflow instance (requires `run` role). |

### 3.13 Revenue & Payments

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| POST | `/api/v1/payments` | `dict` | Record a manual payment in the revenue ledger. |
| GET | `/api/v1/revenue` | `list[dict]` | List revenue transactions (filters: project_id, offer_id, status). |
| GET | `/api/v1/revenue/summary` | `dict` | Revenue summary with contribution margin (MWK→USD conversion). |
| GET | `/api/v1/revenue/attribution` | `dict` | Revenue attribution by agent/department with ROI calculations. |
| GET | `/api/v1/revenue/roi` | `dict` | ROI calculations for a period. |
| GET | `/api/v1/revenue/trend` | `list[dict]` | Revenue trend over time. |

### 3.14 Webhooks

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| POST | `/api/v1/webhooks/paychangu` | `dict` | PayChangu mobile money webhook (signature verification + idempotent insert). |
| POST | `/api/v1/webhooks/airtel` | `dict` | Airtel Money webhook handler. |
| POST | `/api/v1/webhooks/tnm` | `dict` | TNM Mpamba webhook handler. |

All webhooks: verify provider signature → parse payload → insert into `revenue_transactions` table with idempotency check.

### 3.15 Search & Audit

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/search` | `dict` | Unified search across agents, tasks, KPIs, and audit events. |
| GET | `/api/v1/search/quick` | `dict` | Quick search with minimal fields (command bar). |
| GET | `/api/v1/audit/timeline` | `list[dict]` | Execution timeline (filters: agent_id, status, time_range, q). |
| GET | `/api/v1/audit/execution/{task_id}` | `dict` | Full execution detail for a task. |
| GET | `/api/v1/audit/search` | `list[dict]` | Full-text search across audit events. |

### 3.16 Onboarding

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/onboarding` | `list[dict]` | List onboarding requests (optional `state` filter). |
| GET | `/api/v1/onboarding/{id}` | `dict` | Status of a specific onboarding request. |
| POST | `/api/v1/onboarding/{id}/approve` | `dict` | Approve an onboarding request. |
| POST | `/api/v1/onboarding/{id}/reject` | `dict` | Reject with optional reason. |

### 3.17 Governance

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/governance` | `dict` | Data governance report (SQLite-first). |
| GET | `/api/v1/data-quality` | `dict` | Data quality audit — completeness, gaps, staleness. |

### 3.18 Mobile API

All endpoints under `/api/v1/mobile`. Designed for low-bandwidth and offline-capable clients.

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/mobile/dashboard` | `MobileDashboardSummary` | Condensed dashboard (5 KPIs, urgent alerts, recent tasks). |
| GET | `/api/v1/mobile/tasks` | `PaginatedTaskList` | Cursor-paginated task list. |
| POST | `/api/v1/mobile/actions/batch` | `dict` | Execute multiple actions (approve, reject, reassign, delegate). |
| POST | `/api/v1/mobile/actions/quick-approve` | `dict` | One-tap approve with optional confirmation. |
| GET | `/api/v1/mobile/approvals/stack` | `list[dict]` | Swipe stack of pending approvals. |
| POST | `/api/v1/mobile/approvals/swipe` | `dict` | Process swipe gesture (approve/reject/skip). |
| GET | `/api/v1/mobile/kpis/compact` | `dict` | Minimal KPI widget data. |
| GET | `/api/v1/mobile/kpis/trend` | `list[dict]` | Sparkline data for KPI trend charts. |
| POST | `/api/v1/mobile/notifications/register` | `dict` | Register push notification device. |
| DELETE | `/api/v1/mobile/notifications/unregister` | `dict` | Unregister device. |
| PATCH | `/api/v1/mobile/notifications/preferences` | `dict` | Update notification preferences. |
| GET | `/api/v1/mobile/notifications/status` | `dict` | Notification delivery status. |
| POST | `/api/v1/mobile/sync` | `dict` | Offline sync (replay pending actions). |
| POST | `/api/v1/mobile/batch` | `list[dict]` | Batch GET for multiple resources in one request. |

### 3.19 Monitoring

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/metrics` | `Response` | Prometheus text exposition format (LLM costs, task success, agent performance, model breakdown). |
| GET | `/health` | `dict` | Deep health check (inbox, registry, agents, config, LLM providers, audit, disk, memory, DLQ). |
| GET | `/ready` | `Response` | Readiness probe (503 if registry or agents dir missing). |
| GET | `/api/v1/daemon/status` | `dict` | Executor daemon lifecycle status (pid, uptime, ticks). |

### 3.20 Bootstrap

| Method | Path | Response Model | Description |
|--------|------|----------------|-------------|
| GET | `/api/v1/bootstrap-token` | `dict` | Mint IP-bound session token (ADR-013, unauthenticated). |

---

## 4. Pydantic Model Schemas

All models defined in `src/ai_company/dashboard/models.py` unless noted otherwise.

### 4.1 `KPIs` — CEO-level KPI snapshot

Returned by `GET /api/v1/dashboard`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `pending_tasks` | `int` | `0` | Tasks with `status == "pending"` |
| `in_progress_tasks` | `int` | `0` | Tasks with `status == "in_progress"` |
| `completed_tasks` | `int` | `0` | Tasks with `status == "completed"` |
| `failed_tasks` | `int` | `0` | Tasks with `status == "failed"` |
| `escalated_tasks` | `int` | `0` | Tasks with `status == "escalated"` |
| `pending_approvals` | `int` | `0` | Non-expired approval requests with `status == "pending"` |
| `open_escalations` | `int` | `0` | Escalation events with `resolved == false` |
| `total_agents` | `int` | `0` | Count of agents in `company/agent-registry.json` |
| `scheduled_tasks` | `int` | `0` | Tasks in `orchestrator/scheduler.yaml` |
| `uptime_seconds` | `float` | `0` | Seconds since API server boot |
| `computed_at` | `Optional[str]` | `None` | ISO-8601 UTC timestamp of computation |
| `source` | `dict[str, str]` | `{}` | Map of logical name → file path (see §5) |
| `data_quality` | `dict[str, str]` | `{}` | Data quality indicators (see §6) |

#### `source` map

| Key | Value |
|-----|-------|
| `tasks` | `orchestrator/inbox.json` |
| `agents` | `company-registry.yaml` |
| `approvals` | `orchestrator/approvals.yaml` |
| `escalations` | `orchestrator/escalation.yaml` |
| `scheduler` | `orchestrator/scheduler.yaml` |

### 4.2 `AgentSummary`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Unique agent identifier (e.g. `"cto"`, `"security_compliance_lead"`) |
| `role` | `str` | — | Human-readable role title |
| `type` | `str` | — | Agent type: `"executive"`, `"specialist"`, etc. |
| `department` | `str` | `""` | Department id (e.g. `"engineering"`, `"hr"`) |
| `reports_to` | `str` | `""` | Name of the agent's manager |
| `direct_reports` | `list[str]` | `[]` | Names of agents reporting to this one |
| `description` | `str` | `""` | Free-text mission description |
| `model` | `Optional[str]` | `None` | Assigned LLM model (e.g. `"oc/mimo-v2.5-free"`) |

### 4.3 `TaskItem`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str` | — | UUID of the task |
| `sender_id` | `str` | — | Agent (or `human-ceo`) who created the task |
| `receiver_id` | `str` | — | Agent assigned to execute the task |
| `instruction` | `str` | — | Natural-language task description |
| `status` | `str` | `"pending"` | One of: `pending`, `in_progress`, `completed`, `failed`, `escalated` |
| `priority` | `str` | `"medium"` | One of: `critical`, `high`, `medium`, `low` |
| `created_at` | `Optional[str]` | `None` | ISO-8601 UTC creation timestamp |
| `completed_at` | `Optional[str]` | `None` | ISO-8601 UTC completion timestamp |
| `result` | `Optional[str]` | `None` | Free-text result/deliverable from the agent |

### 4.4 `TaskAssign` — POST `/tasks` request body

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `receiver_id` | `str` | — | Target agent |
| `instruction` | `str` | — | Task description (must be >5 chars, not trivial) |
| `priority` | `str` | `"medium"` | Priority level |
| `sender_id` | `str` | `"human-ceo"` | Sender (defaults to CEO) |

### 4.5 `TaskUpdate` — PATCH `/tasks/{id}` request body

All fields optional; only supplied fields are applied.

| Field | Type | Default |
|-------|------|---------|
| `status` | `Optional[str]` | `None` |
| `priority` | `Optional[str]` | `None` |
| `instruction` | `Optional[str]` | `None` |
| `receiver_id` | `Optional[str]` | `None` |

### 4.6 `PaginatedTasks`

| Field | Type | Description |
|-------|------|-------------|
| `items` | `list[TaskItem]` | Current page of tasks |
| `total` | `int` | Total matching tasks (across all pages) |
| `page` | `int` | Current page number (1-based) |
| `page_size` | `int` | Items per page (10, 20, 50, or 100) |
| `total_pages` | `int` | Total pages |
| `counts_by_status` | `dict[str, int]` | Status → count over the **filtered** (un-paginated) result set |

### 4.7 `ApprovalItem`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str` | — | Unique request identifier |
| `task_id` | `str` | — | Associated task id |
| `agent_id` | `str` | — | Agent requesting approval |
| `action` | `str` | — | Description of the requested action |
| `description` | `str` | — | Full description / context |
| `status` | `str` | `"pending"` | `pending`, `approved`, or `rejected` |
| `requested_at` | `Optional[str]` | `None` | ISO-8601 UTC request timestamp |
| `expires_at` | `Optional[str]` | `None` | ISO-8601 UTC expiry (non-expired only in responses) |
| `risk_level` | `Optional[str]` | `None` | Risk classification |
| `cost_estimate` | `Optional[float]` | `None` | Estimated cost in USD |

### 4.8 `ApprovalDecision` — POST approve/reject body

| Field | Type | Default |
|-------|------|---------|
| `approved_by` | `str` | `"human-ceo"` |
| `notes` | `Optional[str]` | `None` |

### 4.9 `ApprovalUpdate` — PATCH body

All fields optional.

| Field | Type | Default |
|-------|------|---------|
| `risk_level` | `Optional[str]` | `None` |
| `cost_estimate` | `Optional[float]` | `None` |

### 4.10 `EscalationItem`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `task_id` | `str` | — | Task that triggered the escalation |
| `rule_id` | `str` | — | Escalation rule that fired |
| `from_agent` | `str` | — | Agent originating the escalation |
| `to_agent` | `str` | — | Agent the escalation is directed to |
| `reason` | `str` | — | Human-readable reason |
| `timestamp` | `Optional[str]` | `None` | ISO-8601 UTC timestamp |
| `resolved` | `bool` | `False` | Whether the escalation has been resolved |

### 4.11 `DepartmentInfo`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Department display name |
| `executive` | `str` | — | Executive agent overseeing the department |
| `agents` | `list[str]` | `[]` | Agent names in the department |
| `total_agents` | `int` | `0` | Count of agents |

### 4.12 `OrgNode` — org chart

| Field | Type | Default |
|-------|------|---------|
| `name` | `str` | — |
| `role` | `str` | — |
| `type` | `str` | — |
| `department` | `str` | `""` |
| `children` | `list[OrgNode]` | `[]` (recursive) |

### 4.13 `ModelRouteItem`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `agent` | `str` | — | Agent name |
| `provider` | `str` | — | LLM provider (e.g. `"openai"`, `"gemini"`) |
| `model` | `str` | — | Model identifier |
| `tier` | `str` | — | Routing tier |
| `reason` | `str` | `""` | Routing decision explanation |

### 4.14 `ModelTelemetryItem`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `model_id` | `str` | — | Model identifier |
| `request_count` | `int` | `0` | Total API calls |
| `success_rate` | `float` | `0.0` | Fraction of successful calls (0–1) |
| `avg_latency_ms` | `float` | `0.0` | Average response latency in milliseconds |
| `total_cost_usd` | `float` | `0.0` | Total cost in USD |

### 4.15 `TierInfo`

| Field | Type | Default |
|-------|------|---------|
| `id` | `str` | — |
| `description` | `str` | — |
| `providers` | `list[dict[str, str]]` | `[]` |

### 4.16 `TaskDecomposition` / `SubtaskItem`

**TaskDecomposition:**

| Field | Type | Default |
|-------|------|---------|
| `parent_id` | `str` | — |
| `subtasks` | `list[SubtaskItem]` | `[]` |
| `progress_pct` | `float` | `0.0` |

**SubtaskItem:**

| Field | Type | Default |
|-------|------|---------|
| `id` | `str` | — |
| `instruction` | `str` | — |
| `status` | `str` | `"pending"` |

### 4.17 `WorkflowSummary`

| Field | Type | Default |
|-------|------|---------|
| `id` | `str` | — |
| `name` | `str` | — |
| `trigger` | `str` | `""` |
| `owner` | `str` | `""` |
| `steps` | `int` | `0` |

### 4.18 `WorkflowStepItem`

| Field | Type | Default |
|-------|------|---------|
| `id` | `str` | — |
| `name` | `str` | — |
| `action` | `str` | `""` |
| `owner` | `str` | `""` |
| `inputs` | `list[str]` | `[]` |
| `outputs` | `list[str]` | `[]` |
| `status` | `str` | `"pending"` |
| `result` | `str` | `""` |
| `sla_hours` | `int` | `0` |
| `sla_minutes` | `int` | `0` |
| `sla_days` | `int` | `0` |

### 4.19 `WorkflowInstanceItem`

| Field | Type | Default |
|-------|------|---------|
| `instance_id` | `str` | — |
| `workflow_id` | `str` | — |
| `workflow_name` | `str` | — |
| `status` | `str` | `"running"` |
| `current_step` | `Optional[str]` | `None` |
| `current_step_index` | `int` | `0` |
| `total_steps` | `int` | `0` |
| `completed_steps` | `int` | `0` |
| `steps` | `list[WorkflowStepItem]` | `[]` |
| `started_at` | `Optional[str]` | `None` |
| `completed_at` | `Optional[str]` | `None` |
| `context` | `dict[str, Any]` | `{}` |

### 4.20 `WorkflowActionRequest`

| Field | Type | Default |
|-------|------|---------|
| `result` | `str` | `""` |

### 4.21 Additional models (in `api.py`)

| Model | Fields | Endpoint |
|-------|--------|----------|
| `PaymentEntry` | `client_id`, `project_id`, `offer_id`, `service_name`, `currency`, `amount`, `payment_method`, `status`, `installment_type`, `exchange_rate`, `linked_task_id`, `reference`, `recorded_by` | `POST /payments` |
| `ProjectCostEntry` | `project_id`, `cost_type`, `amount_usd`, `amount_mwk`, `description`, `agent_id`, `model`, `tokens` | `POST /project-costs` |

### 4.22 Additional models (in `mobile_api.py`)

| Model | Fields | Endpoint |
|-------|--------|----------|
| `MobileDashboardKPIs` | `pending: int`, `completed: int`, `escalations: int`, `approvals: int`, `agents: int` | `GET /mobile/dashboard` |
| `MobileUrgentAlerts` | `approval_count: int`, `escalation_count: int`, `failed_count: int` | `GET /mobile/dashboard` |
| `MobileTaskSummary` | `id`, `to`, `instruction`, `priority`, `status`, `created` | `GET /mobile/dashboard` |
| `MobileDashboardSummary` | `kpis: MobileDashboardKPIs`, `urgent: MobileUrgentAlerts`, `recent_tasks: list[MobileTaskSummary]`, `connection`, `updated_at` | `GET /mobile/dashboard` |
| `PaginatedTaskList` | `items: list[dict]`, `next_cursor: str \| None`, `total_count: int`, `page_size: int`, `has_more: bool` | `GET /mobile/tasks` |
| `BatchRequest` | `actions: list[BatchAction]`, `continue_on_error: bool` | `POST /mobile/actions/batch` |
| `SwipeDecision` | `request_id: str`, `decision: str`, `gesture: dict \| None`, `notes: str` | `POST /mobile/approvals/swipe` |
| `DeviceRegistration` | `device_token: str`, `platform: str`, `app_version: str`, `device_name: str`, `preferences: dict` | `POST /mobile/notifications/register` |
| `SyncRequest` | `last_sync_at: str \| None`, `pending_actions: list[dict]`, `device_token: str \| None` | `POST /mobile/sync` |

---

## 5. KPI Payload Structure & Data Sources

The `KPIs` model (endpoint §3.1) aggregates data from five distinct operational files:

| Field | Source File | Source Module | Computation |
|-------|-----------|---------------|-------------|
| `pending_tasks` | `orchestrator/inbox.json` (via MessageBus) | `api.py → _read_all_tasks()` | `count(t for t in tasks if status == "pending")` |
| `in_progress_tasks` | `orchestrator/inbox.json` (via MessageBus) | `api.py → _read_all_tasks()` | `count(t for t in tasks if status == "in_progress")` |
| `completed_tasks` | `orchestrator/inbox.json` (via MessageBus) | `api.py → _read_all_tasks()` | `count(t for t in tasks if status == "completed")` |
| `failed_tasks` | `orchestrator/inbox.json` (via MessageBus) | `api.py → _read_all_tasks()` | `count(t for t in tasks if status == "failed")` |
| `escalated_tasks` | `orchestrator/inbox.json` (via MessageBus) | `api.py → _read_all_tasks()` | `count(t for t in tasks if status == "escalated")` |
| `pending_approvals` | `orchestrator/approvals.yaml` | `yaml.safe_load()` | Count of requests where `status == "pending"` AND (`expires_at` is null OR `expires_at > now`) |
| `open_escalations` | `orchestrator/escalation.yaml` | `yaml.safe_load()` | Count of events where `resolved == false` |
| `total_agents` | `company/agent-registry.json` | `api.py → _load_registry()` | `len(registry)` |
| `scheduled_tasks` | `orchestrator/scheduler.yaml` | `yaml.safe_load()` | `len(scheduler_data.get("tasks", []))` |
| `uptime_seconds` | In-memory | `time.time() - _START_TIME` | Seconds since the API process started |
| `computed_at` | Runtime | `datetime.now(timezone.utc).isoformat()` | Computed at request time |
| `source` | Static map | Hardcoded in `api.py` | Logical name → file path |
| `data_quality` | Static map | Hardcoded in `api.py` | Quality indicators (see §6) |

---

## 6. Data Quality Fields

Every API response that aggregates data includes a `data_quality` dict. The dashboard owner guarantees these fields so consumers can trust (or distrust) the numbers.

### 6.1 `KPIs.data_quality` (GET `/dashboard`)

| Key | Value | Meaning |
|-----|-------|---------|
| `completeness` | `"all_fields"` | Every field in the `KPIs` model was populated (no partial data). |
| `task_source` | `"message_bus"` | Tasks were read through the shared `MessageBus` (GAP-011 compliant), not directly from `inbox.json`. |
| `agent_source` | `"registry"` | Agent count came from `company/agent-registry.json`. |

### 6.2 `ceo-dashboard.data_quality` (GET `/ceo-dashboard`)

| Key | Value | Meaning |
|-----|-------|---------|
| `kpi_source` | `"live_collectors"` | KPI data came from the 8 department collector classes. |
| `task_source` | `"message_bus"` | Tasks read through MessageBus. |
| `agent_source` | `"registry"` | Agent data from registry JSON. |
| `cost_source` | `"cost_tracker"` | Cost data from `orchestrator/cost_tracker.json`. |
| `completeness` | `"full"` or `"partial"` | `"full"` when all sections loaded without error; `"partial"` when any section raised. |
| `notes` | string | Semicolon-delimited error messages from any failed sections, or `"All sections loaded"`. |

### 6.3 Live KPI collector `data_quality` (per-KPI values)

Each KPI value produced by the `KPICollector._kpi()` helper includes:

| Key | Type | Values | Meaning |
|-----|------|--------|---------|
| `data_quality` | `str` | `"real"` | Live data collected from operational files/SQLite. |
| `data_quality` | `str` | `"fallback"` | Data came from a degraded or secondary source. |
| `data_quality` | `str` | `"error"` | Collection failed; the value is a default/zero. |
| `status` | `str` | `"on_track"` | Current meets or exceeds target (higher_is_better=True) or stays under target (higher_is_better=False). |
| `status` | `str` | `"below_target"` | Current is below the target (higher_is_better=True). |
| `status` | `str` | `"above_target"` | Current exceeds the target (higher_is_better=False, e.g. failure rate). |
| `status` | `str` | `"info"` | No target configured; value is informational only. |
| `status` | `str` | `"no_data"` | Current value is `None`; no data was available. |
| `error` | `str` | — | Present only when data collection failed. Explains the failure. |

### 6.4 Staleness indicator (`ceo-dashboard`, `org-health`)

| Key | Type | Meaning |
|-----|------|---------|
| `last_updated` | `str` | ISO-8601 UTC timestamp of the most recent data collection. |
| `age_seconds` | `int` | Seconds elapsed since `last_updated`. |
| `is_stale` | `bool` | `True` when `age_seconds > 300` (5 minutes). Dashboard UI should flag stale data. |
| `stale_threshold_seconds` | `int` | The threshold used (`300`). |

---

## 7. KPI Definitions

### 7.1 CEO-Level Dashboard KPIs

Source: `GET /api/v1/dashboard` response model (`Pydantic KPIs` in `src/ai_company/dashboard/models.py`).

| KPI | Field | Type | Description |
|-----|-------|------|-------------|
| Pending Tasks | `pending_tasks` | `int` | Tasks in pending state |
| In-Progress Tasks | `in_progress_tasks` | `int` | Tasks currently being worked on |
| Completed Tasks | `completed_tasks` | `int` | Successfully completed tasks |
| Failed Tasks | `failed_tasks` | `int` | Tasks that failed |
| Escalated Tasks | `escalated_tasks` | `int` | Tasks escalated for approval |
| Pending Approvals | `pending_approvals` | `int` | Awaiting human approval |
| Open Escalations | `open_escalations` | `int` | Unresolved escalations |
| Total Agents | `total_agents` | `int` | Registered agents count |
| Scheduled Tasks | `scheduled_tasks` | `int` | Cron/scheduled tasks |
| Uptime Seconds | `uptime_seconds` | `float` | Dashboard server uptime |
| Computed At | `computed_at` | `str \| None` | ISO timestamp of computation |
| Source | `source` | `dict[str, str]` | Data source provenance map |
| Data Quality | `data_quality` | `dict[str, str]` | Quality indicators per source |

**Computation logic** (from `api.py:get_dashboard`):
- Task counts: read via `MessageBus` (`_read_all_tasks()`), counted by status.
- Pending approvals: loaded from `orchestrator/approvals.yaml`, filtered to `status == "pending"` and not expired.
- Open escalations: loaded from `orchestrator/escalation.yaml`, filtered to `resolved == false`.
- Total agents: count of entries in `company/agent-registry.json`.
- Scheduled tasks: count of entries under `tasks` key in `orchestrator/scheduler.yaml`.
- Uptime: `time.time() - _START_TIME` (module start timestamp).

### 7.2 Department KPI Collectors

All collectors inherit from `KPICollector` (`src/ai_company/dashboard/kpis/base.py`) and are invoked by `collect_all_kpis()` in `src/ai_company/dashboard/kpis/__init__.py`. Each returns `{"department": "...", "collected_at": "...", "kpis": {...}}`.

| Collector Class | `department` | Primary Metrics |
|----------------|-------------|-----------------|
| `EngineeringKPICollector` | `engineering` | Task completion rate, failure rate, avg duration, code quality |
| `HRKPICollector` | `hr` | Agent headcount, department distribution, onboarding pipeline |
| `FinanceKPICollector` | `finance` | Budget utilization, cost-per-task, LLM spend, revenue |
| `MarketingKPICollector` | `marketing` | Campaign metrics, content output |
| `SalesKPICollector` | `sales` | Pipeline value, conversion rate, deal velocity |
| `CustomerSuccessKPICollector` | `customer_success` | Customer satisfaction, escalation rate, resolution time |
| `LegalKPICollector` | `legal` | Compliance score, policy adherence, audit findings |
| `OrgHealthKPICollector` | `org_health` | Composite health score (0–100), component weights, health band |

#### Engineering KPIs

**Source**: `src/ai_company/dashboard/kpis/engineering.py` (`EngineeringKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `task_completion_rate` | 95 | `%` | yes | Completed tasks / total tasks × 100 |
| `failure_rate` | 0 | `%` | no | Failed tasks / total tasks × 100 |
| `escalation_rate` | 5 | `%` | no | Total escalations / total tasks × 100 |
| `pending_tasks` | — | count | — | Tasks in pending state |
| `in_progress_tasks` | — | count | — | Tasks in in_progress state |
| `completed_tasks` | — | count | — | Tasks in completed state |
| `failed_tasks` | 0 | count | no | Tasks in failed state |
| `open_escalations` | 0 | count | no | Unresolved escalation events |
| `total_tasks` | — | count | — | All tasks (all statuses) |
| `scheduled_tasks` | — | count | — | Tasks in `orchestrator/scheduler.yaml` |
| `sop_current` | 1 | bool | yes | Engineering SOP updated within 90 days |
| `sop_freshness_pct` | 100 | `%` | yes | `(90 - days_old) / 90 × 100` when current |

#### HR KPIs

**Source**: `src/ai_company/dashboard/kpis/hr.py` (`HRKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `total_agents` | — | count | — | Number of agents in `company/agent-registry.json` |
| `agents_by_department` | — | breakdown | — | Map of `department → agent_count` |
| `department_coverage` | 100 | `%` | yes | Declared departments with ≥1 agent / total declared |
| `declared_departments` | — | count | — | Number of departments in `company/departments.yaml` |

#### Finance KPIs

**Source**: `src/ai_company/dashboard/kpis/finance.py` (`FinanceKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `budget_utilization` | 90 | `%` | yes | `(total_spent / total_budget) × 100` |
| `estimated_llm_spend` | — | `$` | — | Estimated monthly LLM spend from cost tracker |
| `total_budget` | — | `$` | — | Total budget from cost tracker |
| `total_spent` | — | `$` | — | Total expenditure |
| `cost_per_agent` | 50 | `$/month` | — | `total_spent / total_agents` |
| `active_agents` | — | count | — | Registered agents count |
| `total_revenue` | — | `$` | — | Revenue from `RevenueAnalytics` |
| `overall_roi` | 1.0 | ratio | yes | ROI from `RevenueAnalytics` |
| `revenue_per_task` | — | `$/task` | — | `total_revenue / total_tasks` (by department) |

#### Marketing KPIs

**Source**: `src/ai_company/dashboard/kpis/marketing.py` (`MarketingKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `campaign_generation_rate` | 5 | campaigns | yes | Total campaigns in `campaigns.json` |
| `active_campaigns` | — | count | yes | Campaigns with `status == "active"` |
| `content_quality_score` | 8 | score | yes | Average `quality_score` from `content_log.json` |
| `marketing_task_completion` | 90 | `%` | yes | Completed marketing tasks / total marketing tasks × 100 |
| `total_marketing_tasks` | — | count | — | Tasks routed to `cmo`, `content_creator`, `content_writer`, `growth_hacker` |
| `content_pieces_produced` | — | count | yes | Total entries in `content_log.json` |

#### Sales KPIs

**Source**: `src/ai_company/dashboard/kpis/sales.py` (`SalesKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `pipeline_value` | — | `$` | yes | Sum of `value` fields in `pipeline.json` |
| `total_deals` | — | count | — | Total deals in `pipeline.json` |
| `win_rate` | 25 | `%` | yes | Deals with `stage == "won"` / total deals × 100 |
| `new_leads` | — | count | yes | Leads with `status == "new"` in `leads.json` |
| `sales_task_completion` | 85 | `%` | yes | Completed sales tasks / total sales tasks × 100 |
| `total_sales_tasks` | — | count | — | Tasks routed to `sales` or `business_developer` |

#### Customer Success KPIs

**Source**: `src/ai_company/dashboard/kpis/customer_success.py` (`CustomerSuccessKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `ticket_resolution_time` | 4 | hours | no | Avg `(resolved_at - created_at)` for resolved tickets |
| `open_tickets` | 0 | count | no | Tickets with `status in ("open", "in_progress")` |
| `resolved_tickets` | — | count | yes | Tickets with `status == "resolved"` |
| `total_tickets` | — | count | — | All tickets in `tickets.json` |
| `customer_satisfaction` | 9 | score | yes | Average `score` from `surveys.json` |
| `cs_task_completion` | 90 | `%` | yes | Completed CS tasks / total CS tasks × 100 |
| `total_cs_tasks` | — | count | — | Tasks routed to CS agents |
| `sop_current` | 1 | bool | yes | CS SOP updated within 90 days |
| `sop_freshness_pct` | 100 | `%` | yes | `(90 - days_old) / 90 × 100` when current |

#### Legal KPIs

**Source**: `src/ai_company/dashboard/kpis/legal.py` (`LegalKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `contract_review_time` | 2 | hours | no | Avg `(reviewed_at - created_at)` for reviewed contracts |
| `pending_contract_reviews` | 0 | count | no | Contracts with `status == "pending_review"` |
| `approved_contracts` | — | count | yes | Contracts with `status == "approved"` |
| `total_contracts` | — | count | — | All entries in `contracts.json` |
| `compliance_score` | 100 | `%` | yes | Compliance checks with `result == "pass"` / total checks × 100 |
| `total_compliance_checks` | — | count | — | All entries in `compliance_log.json` |
| `legal_task_completion` | 90 | `%` | yes | Completed legal tasks / total legal tasks × 100 |
| `total_legal_tasks` | — | count | — | Tasks routed to legal agents |
| `sop_current` | 1 | bool | yes | Legal SOP updated within 90 days |
| `sop_freshness_pct` | 100 | `%` | yes | `(90 - days_old) / 90 × 100` when current |

#### Operations KPIs

**Source**: `src/ai_company/dashboard/kpis/operations.py` (`OperationsKPICollector`)

| KPI Key | Target | Unit | Higher Is Better | Description |
|---------|--------|------|------------------|-------------|
| `sop_coverage_pct` | 100 | `%` | yes | Departments with existing SOP file / total departments × 100 |
| `sop_stale_count` | 0 | count | no | SOP files with `Last Updated` older than 90 days |
| `sop_departments_covered` | 8 | count | yes | Number of departments with a present SOP file |
| `dlq_total_entries` | — | count | — | Total entries in `.opencode/dead_letter.json` |
| `dlq_recent_entries` | — | count | — | DLQ entries added in the last 7 days |
| `dlq_retry_rate` | 80 | `%` | yes | DLQ entries with `retry_count > 0` / total DLQ × 100 |
| `inbox_total_tasks` | — | count | — | Total tasks in `.opencode/inbox.json` |
| `inbox_pending_tasks` | — | count | — | Inbox tasks with `status == "pending"` |
| `inbox_in_progress_tasks` | — | count | — | Inbox tasks with `status == "in_progress"` |
| `inbox_stale_tasks` | 0 | count | no | In-progress tasks with `updated_at` older than 30 minutes |
| `registry_valid` | 1 | bool | yes | `company-registry.yaml` file exists and is parseable |
| `registry_agent_count` | — | count | — | Agents declared in `company-registry.yaml` |
| `generated_agent_count` | same as `registry_agent_count` | count | yes | Agent `.md` files in `.opencode/agents/` |
| `agent_sync_status` | 1 | bool | yes | `generated_agent_count == registry_agent_count` |
| `scheduled_tasks` | — | count | — | Tasks in `orchestrator/scheduler.yaml` |
| `open_escalations` | 0 | count | no | Unresolved escalation events |
| `escalation_rate_pct` | 15 | `%` | no | `open_escalations / max(inbox_total, 1) × 100` |

### 7.3 Company-Level KPIs

Source: `GET /api/v1/company-kpis` via `data_service.get_company_kpi_summary()`. Supplemented by `src/ai_company/dashboard/kpis/company_kpis.py` collectors.

| KPI ID | Name | Target | Source | Description |
|--------|------|--------|--------|-------------|
| KPI-001 | ARR | $100,000 | SQLite `revenue_transactions` table | Annual Recurring Revenue |
| KPI-002 | CSAT | 9.0 | `orchestrator/cs/surveys.json` | Customer Satisfaction |
| KPI-003 | Agent Utilization Rate | 80% | Computed from tasks | Active agents / registered |
| KPI-004 | Build Success Rate | 95% | Computed from tasks | completed / (completed+failed) |
| KPI-005 | eNPS | 50 | `orchestrator/hr/enps.json` | Employee Net Promoter Score |

**Collector registry** (`COMPANY_KPI_COLLECTORS`):

| KPI ID | Collector function | Data source |
|--------|-------------------|-------------|
| KPI-001 | `collect_arr` | SQLite → file (`orchestrator/finance/revenue.json`) |
| KPI-002 | `collect_csat` | SQLite → file (`orchestrator/cs/surveys.json`) |
| KPI-005 | `collect_enps` | File (`orchestrator/hr/enps.json`) |

Each collector returns `{"current": value|None, "source": str|None, "data_quality": "real"|"no_data", "computed_at": str|None, "data_gap": str|None}`.

### 7.4 Org Health

**Source**: `src/ai_company/dashboard/org_health.py` (`OrgHealthCalculator`)
**Config**: `config/org_health.yaml`

| Component | Default Weight | Range | Description |
|-----------|---------------|-------|-------------|
| `task_success_rate` | 0.30 | 0–100 | Ratio of completed tasks to total tasks in 30-day window |
| `agent_utilization` | 0.25 | 0–100 | Active agents (sent/received tasks) / registered agents × 100 |
| `cost_efficiency` | 0.25 | 0–100 | `100 - (budget_utilization) + 50`, clamped to [0, 100] |
| `error_rate` | 0.20 | 0–100 | `100 - (failed_tasks / total_tasks × 100)`, inverted error rate |

**Composite score**: Weighted average of available components (components with `None` values are excluded, weights renormalized). Clamped to `[0, 100]`.

**Health bands** (from `config/org_health.yaml` or defaults):

| Band | Min | Max |
|------|-----|-----|
| green | 80 | 100 |
| amber | 50 | 79 |
| red | 0 | 49 |

**Anomaly detection**: Z-score on component score deltas across history. Threshold default: `2.0` (warning), `3.0` (critical).

### 7.5 Alert Rules

Source: `GET /api/v1/kpis/alerts` → `AlertEngine` in `src/ai_company/dashboard/analytics.py`.

| Rule | Condition | Severity | Department | Operator |
|------|-----------|----------|------------|----------|
| High failure rate | `failure_rate > 10%` | critical | `*` (all) | `gt` |
| Elevated failure rate | `failure_rate > 5%` | warning | `*` (all) | `gt` |
| Low task completion | `task_completion_rate < 80%` | warning | `*` (all) | `lt` |
| Open escalations | `open_escalations > 3` | warning | `*` (all) | `gt` |
| Budget overage | `budget_utilization > 95%` | critical | `finance` | `gt` |
| Low customer satisfaction | `customer_satisfaction < 7.0` | warning | `customer_success` | `lt` |
| Low compliance score | `compliance_score < 90%` | critical | `legal` | `lt` |

**Alert evaluation flow**:
1. `collect_all_kpis()` gathers live snapshots from all 8 department collectors.
2. `AlertEngine(rules=default_rules).evaluate(snapshot)` checks each rule against the relevant department's KPI values.
3. Fired alerts are returned with: `rule_name`, `department`, `kpi_key`, `current_value`, `threshold`, `operator`, `severity`, `fired_at`, `message`.
4. Snapshot is also stored in `KPIHistoryStore` for trend analysis.

---

## 8. Source-to-Target Mapping

| Source File | Format | Target KPIs / Dashboard Widget | Consumed By |
|-------------|--------|-------------------------------|-------------|
| `.opencode/inbox.json` | JSON | Task counts (pending/in-progress/completed/failed), inbox health | `MessageBus`, Tasks page, KPI collectors, cost tracker |
| `company/agent-registry.json` | JSON | Agent count, agent list, org chart | Agents page, Org Chart, HR KPIs |
| `company-registry.yaml` | YAML | Agent counting, org health | Dashboard KPIs, Operations KPIs |
| `company/departments.yaml` | YAML | Department list, department coverage | HR KPIs |
| `company/config/kpis.yaml` | YAML | KPI definitions (targets, units, frequencies) | Finance KPIs, KPI summary endpoints |
| `config/company/kpis.yaml` | YAML | Company-level KPIs (ARR, CSAT, eNPS targets) | Company KPI chart, CEO Dashboard |
| `orchestrator/approvals.yaml` | YAML | Pending approvals count, approval list | Approvals page, Dashboard KPIs |
| `orchestrator/escalation.yaml` | YAML | Open escalations, escalation list | Escalations page, Engineering/Legal/Operations KPIs |
| `orchestrator/scheduler.yaml` | YAML | Scheduled tasks | Engineering/Operations KPIs, Scheduler endpoint |
| `orchestrator/cost_tracker.json` | JSON | Cost summary, budget utilization | Costs page, Finance KPIs |
| `.opencode/audit` (directory) | JSONL | Agent analytics, model telemetry, per-agent task costs | Command Center, `/metrics`, model telemetry endpoint |
| `results/cost_log.jsonl` | JSONL | Cost analytics (SQLite backfill) | Costs page |
| `.opencode/audit.jsonl` | JSONL | Legacy audit trail | Audit timeline (fallback) |
| `.opencode/dead_letter_queue.json` | JSON | DLQ health, operations KPIs | Operations KPIs, health check |
| `memory/*.json` | JSON | Health check status | Dashboard health endpoint |
| `.opencode/agents/*.md` | Markdown | Agent count, agent sync status | Operations KPIs, health check |
| `company/models.yaml` | YAML | Model routing | Command Center model telemetry, model endpoints |
| `config/org_health.yaml` | YAML | Org health component weights, band thresholds | Org Health composite score |
| `orchestrator/devices.yaml` | YAML | Push notification devices | Mobile API (register/unregister) |
| `orchestrator/marketing/campaigns.json` | JSON | Campaign count, marketing KPIs | Marketing KPIs |
| `orchestrator/marketing/content_log.json` | JSON | Content pieces produced, quality scores | Marketing KPIs |
| `orchestrator/sales/pipeline.json` | JSON | Pipeline value, deal count, win rate | Sales KPIs |
| `orchestrator/sales/leads.json` | JSON | New leads | Sales KPIs |
| `orchestrator/cs/tickets.json` | JSON | Ticket counts, resolution time, CS task completion | Customer Success KPIs |
| `orchestrator/cs/surveys.json` | JSON | CSAT scores | Company KPIs (KPI-002), Customer Success KPIs |
| `orchestrator/legal/contracts.json` | JSON | Contract reviews, compliance | Legal KPIs |
| `orchestrator/legal/compliance_log.json` | JSON | Compliance score | Legal KPIs |
| `orchestrator/hr/enps.json` | JSON | eNPS score | Company KPIs (KPI-005) |
| `orchestrator/finance/revenue.json` | JSON | ARR (file fallback when SQLite unavailable) | Company KPIs (KPI-001) |
| `config/workflows/workflows.yaml` | YAML | Workflow definitions | Mission Control |
| `docs/sop/*.md` | Markdown | SOP freshness (8 departments) | Engineering/Legal/CS/Operations KPIs |
| `data/ai_company.db` | SQLite | Tasks, audit events, costs, KPI history, escalations, revenue, project costs, search index, agent performance analytics | All dashboard pages (preferred data source) |

---

## 9. Data Access Pattern

The dashboard follows a **SQLite-first, file-fallback** pattern across all data reads:

```
┌─────────────────────────────────────────────────────────┐
│                     API Request                         │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  1. Try SQLite via data service layer                   │
│     (TaskStore, CostAnalytics, KPIPipeline,            │
│      AgentPerformanceAnalytics, EscalationStore,       │
│      AuditStore, SearchIndex, RevenueAnalytics)        │
│     Database: data/ai_company.db                       │
└───────────┬───────────────────────┬─────────────────────┘
            │ success               │ None / empty
            ▼                       ▼
┌──────────────────┐  ┌──────────────────────────────────┐
│  Return SQLite   │  │  2. Fall back to file-based reads │
│  data to client  │  │     via StateStore or MessageBus  │
└──────────────────┘  │                                  │
                      │  Files: inbox.json, registry,     │
                      │  approvals.yaml, escalation.yaml, │
                      │  cost_tracker.json, audit/*.jsonl │
                      └──────────┬───────────────────────┘
                                 │
                                 ▼
                      ┌──────────────────┐
                      │  Return file     │
                      │  data to client  │
                      └──────────────────┘
```

**Key data access components**:

| Component | Role | Database location |
|-----------|------|-------------------|
| `StateStore` | Gateway for all file I/O; enforces path allowlist | Project root |
| `MessageBus` | Task CRUD and broadcast; wraps inbox.json | `.opencode/inbox.json` |
| `TaskStore` | SQLite task operations | `data/ai_company.db` |
| `CostAnalytics` | SQLite cost queries | `data/ai_company.db` |
| `KPIPipeline` | SQLite KPI ingestion and history | `data/ai_company.db` |
| `AgentPerformanceAnalytics` | SQLite agent performance queries | `data/ai_company.db` |
| `EscalationStore` | SQLite escalation events | `data/ai_company.db` |
| `AuditStore` | SQLite audit events and full-text search | `data/ai_company.db` |
| `SearchIndex` | SQLite unified search across entities | `data/ai_company.db` |
| `RevenueAnalytics` | SQLite revenue attribution and ROI | `data/ai_company.db` |
| `KPIHistoryStore` | File-based KPI history (JSON files) | KPI history directory |

**Database initialization**: On app lifespan startup, `init_database(db_path)` is called with `data/ai_company.db` resolved from the configured `StateStore` root.

---

## 10. Security Model

| Aspect | Detail |
|--------|--------|
| **Auth modes** | `api_key` (default, fail-closed) or `open` (localhost-only dev) |
| **API key roles** | `admin` (`DASHBOARD_ADMIN_KEY`), `approve` (`DASHBOARD_APPROVE_KEY`), `run` (`DASHBOARD_RUN_KEY`). Legacy alias: `DASHBOARD_API_KEY` → `admin`. |
| **Fail-closed** | When no key is configured in `api_key` mode, all requests are rejected — never silently exposed. |
| **Session tokens (ADR-013)** | Bootstrap endpoint mints IP-bound, TTL-based tokens (default 3600s). Checked as fallback when header doesn't match a static env key. |
| **Rate limiting** | 100 req/min per IP (configurable via `DASHBOARD_RATE_LIMIT`). Sliding window, in-memory. Returns `429` with `X-RateLimit-*` headers. |
| **CORS** | Configurable via `DASHBOARD_CORS_ORIGINS` (comma-separated). Default: localhost-only. Wildcard `*` is rejected. |
| **WebSocket** | Origin check (CSWSH defense): `Origin` header must match `Host` or be in CORS allowlist. Role gate via `?api_key=` query param (requires `run` role). |
| **Path allowlist** | `StateStore` restricts file I/O to known state files — prevents path traversal. |
| **Security headers** | `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`. Applied via middleware to every response. |
| **Write endpoint auth** | `POST`/`PUT`/`PATCH`/`DELETE` require role permission via `Depends(require_role(...))`. Page routes and static assets are exempt from the API-key middleware. |
| **Webhook security** | Each mobile money provider webhook verifies `X-<Provider>-Signature` before recording transactions. Idempotency keys prevent duplicate records. |
| **Loopback enforcement** | `DASHBOARD_AUTH_MODE=open` is only permitted when `DASHBOARD_HOST` resolves to a loopback interface (127.0.0.x, ::1, localhost). |

---

## 11. WebSocket Events

WebSocket endpoint: `ws://<host>/ws/v1/dashboard` (single multiplexed socket).

Connection protocol: `?api_key=<key>` query parameter (role gate), Origin check (CSWSH defense).

Client messages: `{"type": "ping"}`, `{"type": "subscribe", "topics": [...]}`, `{"type": "unsubscribe", "topics": [...]}`.

### 11.1 WebSocket Topics

| Topic | Message Type | Payload Fields | Subscribers |
|-------|-------------|----------------|-------------|
| `kpis` | `kpi_update` | `{type, topic, timestamp, payload: <all KPI fields>}` | Dashboard home, KPIs page |
| `alerts` | `alert` | `{type, topic, timestamp, payload: {category, request_id, action, agent_id, tier}}` | Global toast notifications |
| `tasks` | `task_update` | `{type, topic, event: created/completed/failed/escalated/updated/deleted, timestamp, payload: <task_dict>}` | Tasks page, kanban board |
| `department:{name}` | `department_kpi` | `{type, topic, department, timestamp, payload: {department, KPI fields}}` | Department drill-down |
| `escalations` | `escalation` | `{type, topic, timestamp, payload: <escalation fields>}` | Escalations page |
| `workflows` | `workflow_update` | `{type, topic, event, instance_id, timestamp, payload: <instance fields>}` | Mission Control |
| `onboarding` | `onboarding_update` | `{type, topic, event, request_id, timestamp, payload: <request fields>}` | Onboarding page |
| `org_health` | `org_health_update` | `{type, topic, timestamp, payload: {score, band, components, ...}}` | Org Health monitor |
| `daemon` | `daemon_health` | `{type, topic, timestamp, payload: {state, pid, started_at, uptime_seconds, ticks_completed, ...}}` | Status indicators |

### 11.2 Broadcast Helpers (in `ws.py`)

| Function | Topic | Triggered by |
|----------|-------|-------------|
| `broadcast_kpi_update(data)` | `kpis` | `GET /dashboard`, `GET /kpis/live`, `GET /ceo-dashboard`, `GET /kpis/collect`, cost summary |
| `broadcast_alert(alert)` | `alerts` | Approval/escalation broadcast helpers |
| `broadcast_task_update(task, event)` | `tasks` | Task create/update/delete via `MessageBus` |
| `broadcast_department_kpis(dept, kpis)` | `department:{name}` | Department drill-down endpoint |
| `broadcast_escalation(escalation)` | `escalations` | Escalation resolution |
| `broadcast_workflow_update(id, event, payload)` | `workflows` | Workflow start/advance/complete/cancel |
| `broadcast_onboarding_update(id, event, payload)` | `onboarding` | Onboarding approve/reject |
| `broadcast_org_health(data)` | `org_health` | Org health computation cycle |
| `broadcast_daemon_health(data)` | `daemon` | Executor daemon tick |

---

## 12. Organizational Hierarchy

### 12.1 Agent Hierarchy

The company is organized into departments with executive agents at the top and specialist agents reporting to them. The hierarchy is defined in `company-registry.yaml` as the single source of truth.

| Department | Executive | Reports To | Specialist Roles |
|------------|-----------|------------|------------------|
| Engineering | cto | human_ceo | lead-backend, lead-frontend, lead-devops, senior-backend-engineer, senior-frontend-engineer, frontend-architect, frontend-engineer, backend-engineer, qa-engineer, qa-automation-engineer, ml-engineer, devops-lead, devsecops-lead, security-architect, platform-engineer, platform-reliability-engineer, test-engineering-lead, release-manager |
| Finance | cfo | human_ceo | financial-analyst, revenue-operations-analyst |
| HR | hr | coo | recruiter, employee-experience-lead, learning-development-lead |
| Marketing | cmo | human_ceo | content-writer, content-creator, brand-strategist, product-marketing-manager, growth-hacker, growth-product-manager, marketing-owner |
| Sales | cso | human_ceo | business-developer, sales-owner |
| Customer Success | customer-success-owner | coo | customer-success, support-agent |
| Legal | clo | human_ceo | compliance-officer, legal-owner |
| Operations | coo | human_ceo | sop-owner, business-continuity-manager, process-quality-manager, capacity-planner, workflow-owner |
| AI/ML | caio | human_ceo | prompt-engineer, ml-services-owner, llm-platform-owner, eval-benchmarks-engineer |
| Data | cdo | human_ceo | data-engineer, data-scientist, business-intelligence-engineer |
| Security | ciso | cto | security-architect, ai-security-specialist, red-team-engineer, penetration-testing-lead, incident-response-lead, soc2-audit-readiness-analyst, supply-chain-security-engineer |
| Product | cpo | human_ceo | product-owner, product-designer, ux-research-lead, ux-analytics-lead, developer-experience-engineer |
| Dashboard | dashboard-owner | cto | *(single owner, no direct specialists)* |
| Program | program-manager | human_ceo | corporate-development-lead, consulting-lead |
| Industry Relations | industry-analyst-relations-manager | cmo | *(single owner, no direct specialists)* |

**Key structural notes:**
- **Board-level agents** (board-chair, board-customer, board-finance, board-product, board-risk, board-strategy, board-technology) sit outside the departmental hierarchy and report directly to the board.
- **Cross-cutting roles** like `ai-ethics-officer`, `ai-safety-lead`, `audit-trail-owner`, `constitutional-ai-owner`, `cultural-values-officer`, `decision-engine-owner`, `hai-designer`, `incident-response-lead`, and `threat-intelligence-analyst` span departments.
- **Security agents** report through the CISO, who reports to the CTO: Security → CTO → CEO.

### 12.2 Org Chart Data Flow

```
company-registry.yaml          (single source of truth)
        │
        ▼ generator
company/agent-registry.json    (runtime registry, JSON)
        │
        ▼ API endpoint
GET /api/v1/org-chart          (recursive OrgNode tree)
        │
        ▼ frontend rendering
org-chart.html + org-chart.js  (interactive tree with drag-and-drop)
```

---

## 13. Data Responsibility Matrix

| Dashboard Section | Data Owner Agent | Data Collector | Frequency |
|-------------------|------------------|----------------|-----------|
| Task Counts | orchestration-owner | MessageBus → `.opencode/inbox.json` | Real-time |
| Agent Registry | registry-owner | `company-registry.yaml` → `company/agent-registry.json` | On change (generator run) |
| KPIs (per department) | Each dept's KPI collector | `kpis/{dept}.py` | 300s (`KPISnapshotScheduler`) |
| Company-wide KPIs | cfo | `company_kpis.py` | 300s |
| Cost Tracking | cfo | `cost_tracker.json` → SQLite | Real-time |
| Approvals Queue | compliance-officer | `approvals.yaml` (via `ApprovalGate`) | Real-time |
| Escalations Queue | orchestration-owner | `escalation.yaml` | Real-time |
| Org Health Score | dashboard-owner | `org_health.py` | 60s auto-refresh |
| Workflows | workflow-owner | `workflows.yaml` → `WorkflowEngine` | Real-time |
| Model Telemetry | llm-platform-owner | `audit/*.jsonl` → Prometheus | Continuous |
| SOP Freshness | sop-owner | `docs/sop/*.md` | On change |
| Revenue | cfo | `revenue.json` → SQLite | On transaction |
| Webhooks / Integrations | integration-engineer | `paychangu/`, `airtel/`, `tnm/` callback handlers | On callback |

**RACI interpretation for dashboard data:**
- **Responsible** (R): The data owner agent listed above — accountable for the data being correct and timely.
- **Accountable** (A): The executive overseeing that department (e.g., CTO for engineering metrics, CFO for financial metrics).
- **Consulted** (C): Cross-cutting roles like `data-scientist` and `business-intelligence-engineer` are consulted when KPIs need redefinition.
- **Informed** (I): dashboard-owner receives all data for rendering; the CEO and board-level agents are informed consumers.

---

## 14. Frontend Component Architecture

### 14.1 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Reactivity | **Alpine.js** (`x-data`, `x-init`, `x-bind`) | Lightweight (~15 KB); no build step; directive-driven state on DOM elements |
| Charts | **Chart.js** (canvas 2D) | CDN-loaded; destroy-safe re-render via `updateOrCreateChart()` wrapper |
| Design System | **J.A.R.V.I.S. Control Plane Theme** (`control-plane-theme.css`) | Custom properties on `:root` — palettes, glass treatment, agent-state colors, motion tokens |
| Styling | **Custom CSS** (no Tailwind, no preprocessors) | 4 stylesheets: `style.css`, `control-plane-theme.css`, `command-center.css`, `command-bar.css` |
| Build | **None** — zero-bundler | All JS loaded via `<script>` tags in templates; no webpack, Vite, or esbuild |
| PWA | **Service Worker** (`sw.js`) + **IndexedDB** offline queue | Cache-first for static assets, network-first for API; background sync for queued mutations |
| Fonts | Self-hosted `Rajdhani` (display) + `JetBrains Mono` (mono) | CSP-safe, no external font requests |

### 14.2 Component Map

| Component | JS File | Alpine Directive | Page(s) | Responsibility |
|-----------|---------|-----------------|---------|----------------|
| Dashboard App | `js/app.js` | `x-data="dashboard()"` | All (via `base.html`) | Global state, WebSocket lifecycle, polling, session token, toast notifications, scroll management, PWA events |
| Charts | `js/charts.js` | N/A (utility module) | Dashboard, KPIs, Costs | Chart.js wrapper: `updateOrCreateChart()` — safe destroy + re-create |
| Command Center | `js/command-center.js` | `x-data="commandCenter()"` | `/command-center` | 3 switchable variants (Bridge, War Room, Cockpit); briefing items, workforce grid, model telemetry, activity stream |
| Command Bar | `js/command-bar.js` + `js/command-bar-service.js` | `x-data="commandBar()"` | Global (Cmd+K / Ctrl+K) | Fuzzy search across routes and actions, quick-action palette, keyboard navigation (↑↓ Enter Esc) |
| Kanban Board | `js/kanban-board.js` | `x-data="kanbanBoard()"` | `/tasks` | 5-column drag-and-drop board (pending → in_progress → review → completed → failed), task decomposition trigger |
| Mission Control | `js/mission-control.js` | `x-data="missionControl()"` | `/mission-control` | Workflow pipeline visualization, start / advance / complete / cancel workflow instances |
| Health Monitor | `js/health.js` | `x-data="healthMonitor()"` | `/dashboard` | Org health score gauge, 7-day trend sparkline, anomaly detection highlights |
| Org Chart | `js/org-chart.js` + `js/org-chart-interactive.js` | `x-data="orgChart()"` | `/org-chart` | Hierarchical tree render, drag-and-drop agent reassignment, live WebSocket updates |
| Onboarding Studio v2 | `js/onboarding-studio-v2.js` | `x-data="onboardingStudioV2()"` | `/onboarding` | 5 persona templates, multi-step wizard, live YAML preview, generation endpoint |
| CEO Hero | `js/ceo-hero-prototype.js` | `x-data="ceoHero()"` | `/dashboard` | 3 switchable display variants: gauge ring, horizontal bar, drill-down card |
| Offline Sync | `js/offline-sync.js` | N/A (service module) | Global (via `app.js` init) | IndexedDB action queue, background sync registration, conflict detection via timestamps, user-resolution modal |
| Service Worker | `sw.js` (root of static/) | N/A | Global | Precache app shell (11 routes + 4 static assets), cache-first static / network-first API, background sync handler |
| SW Registration | `js/sw-registration.js` | N/A | Global (via `base.html`) | Registers `sw.js`, fires `sw-installable` and `sw-update-available` custom events |

---

## 15. Frontend Data Flow & WebSocket Integration

### 15.1 Data Flow Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Page Load                                                 │
│    dashboard().init() fires                                  │
│    ├─ fetchSessionToken()  →  GET /api/v1/bootstrap-token    │
│    ├─ connectWebSocket()   →  ws://host/ws/v1/dashboard      │
│    └─ loadPageData()       →  dispatches to page loader      │
│                                                              │
│ 2. Page Loader (per-route)                                   │
│    GET /api/v1/{endpoint}  →  Alpine reactive properties     │
│    e.g.  tasks, agents, kpis, departments, orgChart          │
│                                                              │
│ 3. Template Rendering                                        │
│    x-data bindings  →  DOM updates (Alpine reactivity)       │
│    charts.js        →  updateOrCreateChart() on canvas       │
│                                                              │
│ 4. Real-Time Push                                            │
│    WebSocket message  →  handleWSMessage(msg)                │
│    ├─ kpi_update   →  merge into this.kpis                   │
│    ├─ task_update  →  merge into this.tasks                  │
│    ├─ alert        →  showToast()                            │
│    └─ department:* →  update department slice                │
│                                                              │
│ 5. Fallback Polling                                          │
│    WS down  →  debouncedPoll() every 15s                     │
│    WS up    →  debouncedPoll() every 30s (background refresh)│
└──────────────────────────────────────────────────────────────┘
```

**Key invariants:**
- Only one `loadPageData()` dispatch runs per route; gated by `_pollInFlight` to prevent overlapping fetches.
- Chart updates are coalesced via `requestAnimationFrame` — `_kpiChartsRaf` ensures at most one redraw per frame.
- Scroll position is saved before WS-triggered data updates and restored after Alpine re-renders (scroll guard pattern).

### 15.2 WebSocket Integration

| Property | Value | Source |
|----------|-------|--------|
| Endpoint | `ws(s)://<host>/ws/v1/dashboard` | `app.js:421` |
| Auth | `?api_key=<bootstrap-token>` query param | ADR-013, `app.js:424-425` |
| Keepalive | `{ type: "ping" }` every **25s** | `app.js:526-533` |
| Reconnection | Exponential backoff: `1s → 2s → 4s → 8s → 16s → 30s` (jittered ×0.5–1.0) | `app.js:514` |
| Max attempts | 8 rapid retries, then 60s probe interval | `app.js:497,505-510` |
| Auth failure | WS close code `1008` → `_refreshSessionToken()` then reconnect | `app.js:467-468` |
| Message format | JSON: `{ type: string, payload?: any, ... }` | `app.js:453-458` |

**Topic-based subscription model** — the server pushes topics; the client switches on `msg.type`:

| Message Type | Payload Shape | Client Action |
|-------------|---------------|---------------|
| `connected` | `{ active_clients: int }` | Update `wsClients` counter |
| `kpi_update` | Full KPI dict | Merge into `this.kpis`, trigger chart coalesced update |
| `task_update` | Task object or list | Merge into `this.tasks`, update pagination counts |
| `alert` | `{ type, title, message }` | `showToast()` notification |
| `department:<name>` | Department data slice | Update `this.departments` matching entry |
| `approval_update` | Approval object | Merge into `this.approvals` |
| `escalation_update` | Escalation object | Merge into `this.escalations`, add to real-time toast list |
| `org_health_update` | Health score + components | Update `this.orgHealth`, re-render CEO Hero |
| `workflow_update` | Workflow state change | Update Mission Control pipeline state |

**Fallback polling** (`debouncedPoll` in `app.js`):
- When WebSocket is **down**: poll every **15s** (`_pollIntervalMs = 15000`).
- When WebSocket is **up**: poll every **30s** as background refresh.
- Polling pauses on `document.hidden` (tab backgrounded) via `visibilitychange` listener.

### 15.3 Session Token Flow (ADR-013)

The dashboard uses IP-bound bootstrap tokens instead of long-lived API keys. Tokens live in memory only — never persisted to `localStorage` or `sessionStorage`.

```
┌───────────────────────────────────────────────────────────────────┐
│ STEP 1 — Token Mint                                              │
│   Page load  →  dashboard().init()                                │
│   GET /api/v1/bootstrap-token                                     │
│   Response:  { token: "bt_...", expires_in: 3600 }               │
│   Stored:    this._sessionToken = data.token                      │
│   Bound to:  client IP address (server-side validation)           │
│                                                                   │
│ STEP 2 — WebSocket Auth                                           │
│   ws://host/ws/v1/dashboard?api_key=<bootstrap-token>             │
│   Server validates token + IP, accepts or rejects (1008)          │
│                                                                   │
│ STEP 3 — REST API Auth                                            │
│   All fetch() calls include:                                      │
│     headers['X-API-Key'] = this._sessionToken                     │
│   (only if header not already set by caller)                      │
│                                                                   │
│ STEP 4 — Transparent Refresh                                      │
│   Trigger:  HTTP 401  OR  WebSocket close code 1008               │
│   Action:   _refreshSessionToken()                                │
│             ├─ GET /api/v1/bootstrap-token  (re-mint)             │
│             ├─ Update _sessionToken                               │
│             └─ Reconnect WebSocket with new token                 │
│                                                                   │
│ STEP 5 — Expiry Handling                                          │
│   TTL = 3600s (1 hour). On expiry, next WS message or API        │
│   call returns 401/1008, triggering Step 4 automatically.         │
│   No proactive timer refreshes the token before expiry.           │
└───────────────────────────────────────────────────────────────────┘
```

**Security properties:**
- Tokens are **IP-bound** — a token minted from `192.168.1.10` is rejected from `10.0.0.5`.
- Tokens exist **in memory only** — no `localStorage`, `sessionStorage`, or cookie storage.
- Token refresh is **transparent** — the user never sees a re-authentication prompt.
- On `visibilitychange` to hidden, polling and timers pause; on return, a fresh poll ensures data consistency.

---

## 16. Frontend Component Data Contracts

### 16.1 Task Assignment Modal

**User Action: Click "Assign Task" Button → Opens Modal**

| Field | Value |
|-------|-------|
| Alpine state | `showAssignModal = true` |
| Form model | `newTask = { receiver_id: '', instruction: '', priority: 'medium', sender_id: 'human-ceo' }` |
| Validation | `receiver_id` and `instruction` must be non-empty |

**User Action: Submit Assignment Form**

| Property | Value |
|----------|-------|
| Trigger | `assignTask()` method |
| Method | `POST` |
| URL | `/api/v1/tasks` |
| Content-Type | `application/json` |
| X-API-Key | Session token from `/api/v1/bootstrap-token` (ADR-013) |

**Request Body** (`TaskAssign` model):

```json
{
  "receiver_id": "agent-engineering",
  "instruction": "Implement the login page with OAuth2",
  "priority": "high",
  "sender_id": "human-ceo"
}
```

| Field | Type | Required | Default | Valid Values |
|-------|------|----------|---------|--------------|
| `receiver_id` | string | yes | — | Agent name from registry |
| `instruction` | string | yes | — | Min 6 chars, not trivial (`/^do [a-z]$/i`), not test (`/^test\s/i`) |
| `priority` | string | no | `"medium"` | `"low"`, `"medium"`, `"high"`, `"critical"` |
| `sender_id` | string | no | `"human-ceo"` | Any agent name or `"human-ceo"` |

**Success Response** (HTTP 201): Full `TaskItem` with `id`, `status: "pending"`, timestamps.

**Error Responses**:

| HTTP Status | Condition | Detail |
|-------------|-----------|--------|
| 400 | `instruction` ≤ 5 chars | `"Instruction too short. Please provide a meaningful task description."` |
| 400 | Matches `/^do [a-z]$/i` | `"Instruction appears to be a placeholder..."` |
| 400 | Matches `/^test\s/i` | `"Instruction appears to be a test placeholder..."` |
| 401 | Invalid/expired session token | Transparent retry with fresh token; then error toast |
| 429 | Rate limited | `"Too many requests — retrying shortly"` |

**Post-action UI behavior**: Reset form, close modal, reload task list, show success toast (auto-dismiss 5s).

### 16.2 Task Drag-and-Drop (Kanban Board)

Two implementations exist: `dashboard()` Kanban in `app.js` and `kanbanBoard()` in `kanban-board.js`. Both use the same API contract.

**Column ↔ Status Mapping**:

| Column ID | Label | Task Status | Color |
|-----------|-------|-------------|-------|
| `backlog` | Backlog | `pending` | amber |
| `in_progress` | In Progress | `in_progress` | blue |
| `review` | Review | `escalated` | orange |
| `completed` | Completed | `completed` | green |
| `failed` | Failed | `failed` | red |

**Drag-Drop Flow**:
1. `ondragstart`: Store `taskId` in `dataTransfer`
2. `ondragover`: Prevent default (allows drop), highlight column
3. `ondrop`: Read `taskId` from `dataTransfer`, call `PATCH /api/v1/tasks/{task_id}` with new status
4. Optimistic UI: Update local state immediately, revert on API error
5. WebSocket: `task_update` event confirms the change to all connected clients

### 16.3 Approval Actions

| Action | Method | URL | Request Body | Post-Action |
|--------|--------|-----|--------------|-------------|
| Approve | `POST` | `/api/v1/approvals/{id}/approve` | `{ approved_by: "human-ceo", notes: "" }` | Remove from list, show toast, decrement `pendingApprovals` |
| Reject | `POST` | `/api/v1/approvals/{id}/reject` | `{ approved_by: "human-ceo", notes: "" }` | Remove from list, show toast |
| Edit Risk | `PATCH` | `/api/v1/approvals/{id}` | `{ risk_level: "high" }` | Update in-place, show toast |

### 16.4 Escalation Resolution

| Action | Method | URL | Post-Action |
|--------|--------|-----|-------------|
| Resolve | `POST` | `/api/v1/escalations/{task_id}/resolve` | Remove from list, show toast, decrement `openEscalations` |

### 16.5 Task Decomposition

| Action | Method | URL | Post-Action |
|--------|--------|-----|-------------|
| Decompose | `POST` | `/api/v1/tasks/{task_id}/decompose` | Display subtask list with progress bar |
| View Subtasks | `GET` | `/api/v1/tasks/{task_id}/subtasks` | Display existing decomposition |

### 16.6 Task Deletion

| Action | Method | URL | Post-Action |
|--------|--------|-----|-------------|
| Delete | `DELETE` | `/api/v1/tasks/{task_id}` | Remove from local list, show toast, update counts |

---

## 17. Task Status Lifecycle

### 17.1 Valid State Transitions

```
                 ┌──────────────┐
                 │   pending    │
                 └──────┬───────┘
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
     ┌────────────┐ ┌──────────┐ ┌──────────┐
     │in_progress │ │escalated │ │ failed   │
     └─────┬──────┘ └────┬─────┘ └──────────┘
           │              │
           ▼              │
     ┌────────────┐       │
     │ completed  │       │
     └────────────┘       │
                          │
            ┌─────────────┘
            ▼
     ┌────────────┐
     │ in_progress│ (reassigned)
     └────────────┘
```

### 17.2 Transition Rules

| From | To | Trigger | Notes |
|------|----|---------|-------|
| `pending` | `in_progress` | Agent picks up task | Auto-set by executor |
| `pending` | `escalated` | Agent cannot handle | Requires human review |
| `pending` | `failed` | Pre-validation failure | e.g., invalid receiver |
| `in_progress` | `completed` | Agent finishes task | Includes result payload |
| `in_progress` | `failed` | Agent encounters error | Error message in `result` |
| `in_progress` | `escalated` | Agent needs human input | Mid-execution escalation |
| `escalated` | `in_progress` | Human resolves escalation | Task resumes |
| `escalated` | `failed` | Human rejects escalation | Task abandoned |
| `escalated` | `completed` | Human directly completes | Rare edge case |

---

## 18. Offline Sync & PWA

### 18.1 Service Worker Architecture

| File | Location | Role |
|------|----------|------|
| `sw.js` | `static/sw.js` (root) | Service Worker — caching strategies, background sync |
| `sw-registration.js` | `static/js/sw-registration.js` | Registration, lifecycle events, A2HS prompt |
| `offline-sync.js` | `static/js/offline-sync.js` | IndexedDB queue, conflict detection, user resolution |

### 18.2 Caching Strategies

| Asset Type | Strategy | Cache Name | Notes |
|-----------|----------|------------|-------|
| Static assets (CSS, JS, fonts, images) | **Cache-first** | `jarvis-v1-static` | Precached on SW install; network fallback |
| HTML pages (routes) | **Network-first** | `jarvis-v1-html` | Fresh content preferred; cached fallback for offline |
| API responses | **Network-first** | `jarvis-v1-api` | Stale-while-revalidate for read endpoints |

### 18.3 App Shell Precache

```
11 routes:  /, /agents, /tasks, /kpis, /costs, /escalations,
            /command-center, /mission-control, /finance,
            /onboarding, /org-chart
4 assets:   control-plane-theme.css, style.css,
            command-bar.css, app.js, command-bar-service.js,
            command-bar.js, manifest.json
```

### 18.4 Offline Queue and Background Sync

| Phase | Behavior |
|-------|----------|
| Queue action | `offline-sync.js` writes mutation (POST/PUT/DELETE) to IndexedDB with timestamp and endpoint |
| Sync trigger | `navigator.serviceWorker.ready` → `SyncManager.register('dashboard-sync')` |
| SW handler | `sw.js` `sync` event fetches queued actions from IndexedDB, replays against API |
| Success | Entry removed from IndexedDB; `sw-sync-complete` custom event dispatched to `app.js` |
| Failure | Entry retained; retry on next `online` event or manual sync |
| Queue count | `app.js` displays `offlineQueueCount` badge; modal shows `offlineQueueActions` list |

### 18.5 Conflict Detection and Resolution

| Scenario | Detection | Resolution |
|----------|-----------|------------|
| Local mutation vs server state | Timestamp comparison — server `updated_at` > local `queued_at` | `showConflictModal = true`; user chooses keep-local / accept-server / merge |
| Stale read after offline | Next GET returns data differing from local cache | Toast warning: "Data has changed since you went offline" |
| Concurrent offline edits | Two devices queue same resource | IndexedDB entry marked `conflict`; user prompted in modal |

---

## 19. Toast Notification System

### 19.1 Toast Data Model

Each toast is an object with the following shape:

```javascript
{
  id: "toast-" + Date.now(),     // unique ID for dismissal
  type: "success" | "error" | "warning" | "info",
  title: "Task Assigned",        // short headline
  message: "New task has been created",  // detail text
  duration: 5000                 // auto-dismiss ms (0 = manual only)
}
```

### 19.2 Toast Triggers

| Trigger | Type | Title | Message |
|---------|------|-------|---------|
| Task assigned | `success` | `"Task Assigned"` | `"New task has been created"` |
| Task updated | `success` | `"Task Updated"` | `"Task status has been changed"` |
| Task deleted | `success` | `"Task Deleted"` | `"Task has been removed"` |
| Approval approved | `success` | `"Approved"` | `"Request has been approved"` |
| Approval rejected | `warning` | `"Rejected"` | `"Request has been rejected"` |
| Escalation resolved | `success` | `"Resolved"` | `"Escalation has been resolved"` |
| API error (401) | `error` | `"Session Expired"` | `"Refresh the page to reconnect"` |
| API error (429) | `warning` | `"Rate Limited"` | `"Too many requests — retrying shortly"` |
| WebSocket disconnected | `error` | `"Connection Lost"` | `"Attempting to reconnect..."` |
| WebSocket reconnected | `success` | `"Connected"` | `"Real-time updates active"` |
| Offline action queued | `info` | `"Queued"` | `"Action will sync when online"` |

### 19.3 Toast Behavior

- Auto-dismiss after `duration` ms (default 5000)
- Stack vertically in bottom-right corner
- Max 5 visible toasts; oldest dismissed when limit exceeded
- Click to dismiss immediately
- Smooth enter/exit animation (slide-in from right, fade-out)

---

## 20. API Contracts & Data Flow Diagrams

### 20.1 Live KPIs Response Shape

```json
{
  "engineering": {
    "task_completion_rate": { "current": 92.5, "target": 95, "unit": "%", "status": "approaching_target" },
    "failure_rate": { "current": 2.1, "target": 0, "unit": "%", "status": "above_target" },
    "escalation_rate": { ... },
    "pending_tasks": { ... },
    "in_progress_tasks": { ... },
    "completed_tasks": { ... },
    "failed_tasks": { ... },
    "open_escalations": { ... }
  },
  "hr": { ... },
  "finance": { ... },
  "marketing": { ... },
  "sales": { ... },
  "customer_success": { ... },
  "legal": { ... },
  "operations": { ... },
  "org_health": { "current": 78.3, "target": 85, "unit": "score", "status": "approaching_target" }
}
```

**KPI envelope fields:**

| Field | Type | Description |
|-------|------|-------------|
| `current` | `float` | Observed value |
| `target` | `float` | Target threshold |
| `unit` | `string` | Display unit (`%`, `count`, `score`, `seconds`) |
| `status` | `string` | Derived: `at_target`, `approaching_target`, `above_target`, `below_target` |

### 20.2 Paginated Tasks Response Shape

```json
{
  "items": [ { "id": "...", "sender_id": "...", "receiver_id": "...", ... } ],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8,
  "counts_by_status": {
    "pending": 45,
    "in_progress": 30,
    "completed": 60,
    "failed": 5,
    "escalated": 10
  }
}
```

---

## 21. Error Handling & Resilience

### 21.1 HTTP Error Responses

| HTTP Status | Condition | Frontend Behavior |
|-------------|-----------|-------------------|
| 400 | Validation failure (trivial instruction, missing fields) | Show error toast with server message |
| 401 | Invalid/expired session token | Transparent token refresh via `_refreshSessionToken()`, then retry request |
| 403 | Insufficient role permissions | Show error toast: "Insufficient permissions" |
| 404 | Resource not found (task, agent, approval) | Show error toast: "Resource not found" |
| 429 | Rate limit exceeded (100 req/min/IP) | Show warning toast; automatic retry after backoff |
| 500 | Server error | Show error toast; log to console; do not retry automatically |

### 21.2 WebSocket Error Handling

| Event | Code | Behavior |
|-------|------|----------|
| Normal close | `1000` | Clean shutdown; no reconnect |
| Auth failure | `1008` | Refresh session token, reconnect with new token |
| Server error | `1011` | Exponential backoff reconnect (1s → 2s → 4s → ... → 30s) |
| Abnormal close | `1006` | Immediate reconnect attempt, then exponential backoff |
| Max retries exceeded | — | Show "Connection lost" toast; switch to polling-only mode (15s interval) |

### 21.3 WebSocket Close Codes

| Code | Name | Meaning | Client Action |
|------|------|---------|---------------|
| `1000` | Normal Closure | Clean shutdown | No reconnect |
| `1001` | Going Away | Server shutting down | Reconnect after 5s |
| `1008` | Policy Violation | Auth failure or CSWSH | Refresh token, reconnect |
| `1011` | Internal Error | Server-side error | Backoff reconnect |
| `1012` | Service Restart | Server restarting | Reconnect after 3s |
| `1013` | Try Again Later | Server overloaded | Reconnect after 30s |
| `1014` | Bad Gateway | Upstream error | Reconnect after 10s |
| `1015` | TLS Handshake | Certificate error | Do not reconnect; show error |

### 21.4 Error Correlation

Every API error response includes an `X-Request-ID` header (generated by FastAPI middleware). Frontend logs this ID to console for debugging. WebSocket errors include `request_id` in the error payload when available.

---

## 22. Design System & Theme Tokens

### 22.1 CSS Architecture

All dashboard CSS lives under `src/ai_company/dashboard/static/css/`. Files are loaded in a strict cascade:

| File | Purpose | Load Order |
|------|---------|------------|
| `control-plane-theme.css` | J.A.R.V.I.S. design tokens (CSS custom properties), font-face declarations, glass-panel utility, agent state classes | 1 — loaded first |
| `style.css` | Reset, base typography, layout grid, component styles, responsive breakpoints | 2 |
| `command-bar.css` | Command bar overlay, search input, result items, keyboard hints | 3 |
| `command-center.css` | Command Center page: arc reactor, briefing panel, workforce grid, activity stream | 4 — page-specific only |

### 22.2 Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--jarvis-bg-base` | `#070b14` | Page background (deep dark navy) |
| `--jarvis-bg-raised` | `#0c1420` | Card and panel backgrounds |
| `--jarvis-bg-overlay` | `#101a2b` | Hover states, active items, overlay surfaces |
| `--jarvis-cyan` | `#22d3ee` | Primary accent — active elements, links, glows, focus rings |
| `--jarvis-text` | `#e2e8f0` | Primary text — headings, body copy |
| `--jarvis-text-muted` | `#94a3b8` | Secondary text — labels, metadata, timestamps |
| `--jarvis-amber` | `#fbbf24` | Warning / waiting state indicator |
| `--jarvis-red` | `#f87171` | Error / blocked / critical state indicator |
| `--jarvis-success` | `#34d399` | Success / online state indicator |

### 22.3 Agent State Colors

| Token | Value | State | Visual Treatment |
|-------|-------|-------|------------------|
| `--jarvis-state-online` | `#34d399` | Idle, connected | Static border + subtle glow |
| `--jarvis-state-thinking` | `#a78bfa` | Processing / reasoning | Pulsing border (2s) |
| `--jarvis-state-executing` | `#22d3ee` | Running tool calls | Pulsing border + expanding glow (1.2s) |
| `--jarvis-state-delegating` | `#818cf8` | Subagent dispatched | Pulsing border (2s) |
| `--jarvis-state-waiting` | `#fbbf24` | Awaiting input/approval | Static border + subtle glow |
| `--jarvis-state-blocked` | `#f87171` | Error / failure | Fast pulsing border (1s) |
| `--jarvis-state-escalated` | `#fb923c` | Requires human action | Pulsing border + glow (1.2s) |
| `--jarvis-state-offline` | `#475569` | Disconnected | Static border, `opacity: 0.6`, no glow |

CSS classes: `.jarvis-state-online`, `.jarvis-state-thinking`, etc. Applied via the `.jarvis-state` base class.

### 22.4 Glass & Surface Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--jarvis-glass-opacity` | `0.72` | Glass panel background opacity |
| `--jarvis-glass-blur` | `12px` | Backdrop-filter blur radius |
| `--jarvis-border-glow` | `rgba(34, 211, 238, 0.12)` | Glass panel border color (subtle cyan) |
| `--jarvis-shadow-glow` | `rgba(34, 211, 238, 0.06)` | Glass panel box-shadow base |

**Glass utility class**: `.jarvis-glass` — `background: rgba(7, 11, 20, 0.72)`, `backdrop-filter: blur(12px)`, `border: 1px solid var(--jarvis-border-glow)`, `box-shadow: 0 0 8px var(--jarvis-shadow-glow)`.

### 22.5 Typography Tokens

| Token | Value | Fallback Stack | Usage |
|-------|-------|----------------|-------|
| `--jarvis-font-display` | `'Rajdhani'` | `'Rajdhani', 'Inter', system-ui, sans-serif` | All headings, body text, panel labels |
| `--jarvis-font-mono` | `'JetBrains Mono'` | `'JetBrains Mono', ui-monospace, Consolas, monospace` | Code, KPI values, timestamps, model tags |

**Font-face declarations** (self-hosted, CSP-safe):

| Font | Weight | File | Usage |
|------|--------|------|-------|
| Rajdhani | 500 (medium) | `/static/fonts/Rajdhani-Medium.woff2` | Headings, nav labels |
| Rajdhani | 700 (bold) | `/static/fonts/Rajdhani-Bold.woff2` | Section headers, emphasis |
| JetBrains Mono | 400 (regular) | `/static/fonts/JetBrainsMono-Regular.woff2` | Data values, code blocks |

All `@font-face` rules use `font-display: swap` to prevent FOIT.

### 22.6 Motion Tokens

| Token | Value |
|-------|-------|
| `--jarvis-motion-duration` | `0.3s` |
| `--jarvis-motion-easing` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--jarvis-pulse-speed` | `2s` |

### 22.7 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + K` | Open Command Bar |
| `F1` | Navigate to Dashboard |
| `F2` | Navigate to Agents |
| `F3` | Open approval edit (in Approvals page) |
| `F5` | Refresh current page data |
| `F6` | Show escalation notifications panel |
| `Escape` | Close any open modal / slide-out / command bar |

### 22.8 Chart Inventory

| Chart | Type | Canvas Target | Data Source | Update Trigger |
|-------|------|---------------|-------------|----------------|
| Task Status Distribution | `doughnut` | `taskStatusChart` | `GET /api/v1/dashboard` → task counts | `kpi_update` WS |
| Department Load | `bar` | `departmentLoadChart` | `GET /api/v1/kpis/live` → department array | `kpi_update` WS |
| KPI Radar | `radar` | `kpiRadarChart` | `GET /api/v1/kpis/live` → per-department KPI scores | `kpi_update` WS |
| KPI Target vs Current | `bar` | `kpiTargetChart` | `GET /api/v1/kpis/live` → target + current pairs | `kpi_update` WS |
| Company KPI Bar | `bar` | `companyKPIChart` | `GET /api/v1/company-kpis` → company-wide KPIs | `kpi_update` WS |
| Cost Trend | `line` | `costTrendChart` | `GET /api/v1/costs/summary` → daily/weekly/monthly series | Cost page load |
| Cost per Agent | `bar` | `costAgentChart` | `GET /api/v1/costs/summary` → per-agent cost array | Cost page load |
| Org Health Trend | `line` | `orgHealthTrendChart` | `GET /api/v1/org-health/trend` → 7-day series | 60s `setInterval` |

---

## 23. Enum Values

### Task Statuses
`pending` → `in_progress` → `completed` | `failed` | `escalated`

### Task Priorities (sort order)
`critical` (0) → `high` (1) → `medium` (2) → `low` (3)

### Approval Statuses
`pending` → `approved` | `rejected`

### Onboarding States
`pending_approval` → `generating` → `testing` → `active` → `archived`

### KPI Status Values
`on_track` | `below_target` | `above_target` | `info` | `no_data`

### Data Quality Values
`real` | `fallback` | `error`

### Health Bands
`green` (≥70) | `amber` (40–69) | `red` (<40)

---

## Appendix A: File Inventory

### JavaScript (`static/js/`)

| File | Purpose |
|------|---------|
| `app.js` | Core Alpine.js app, WS, polling, session tokens, all page state |
| `charts.js` | Chart.js `updateOrCreateChart()` utility |
| `command-center.js` | Command Center variants (Bridge, War Room, Cockpit) |
| `command-bar.js` | Command Bar Alpine component (Cmd+K) |
| `command-bar-service.js` | Fuzzy search index, action registry for Command Bar |
| `kanban-board.js` | Kanban drag-and-drop board for tasks |
| `mission-control.js` | Workflow pipeline visualization |
| `health.js` | Org health monitor, anomaly detection |
| `org-chart.js` | Org chart tree renderer |
| `org-chart-interactive.js` | Org chart drag-and-drop reassignment + WS |
| `onboarding-studio-v2.js` | Onboarding Studio v2 — personas, wizard, YAML preview |
| `ceo-hero-prototype.js` | CEO Hero — 3 switchable display variants |
| `offline-sync.js` | IndexedDB queue, background sync, conflict detection |
| `sw-registration.js` | Service Worker registration + lifecycle events |

### Service Worker

| File | Purpose |
|------|---------|
| `sw.js` | Cache management, background sync handler, offline strategy |

### CSS (`static/css/`)

| File | Purpose |
|------|---------|
| `style.css` | Base layout, responsive grid, typography, component styles |
| `control-plane-theme.css` | J.A.R.V.I.S. design tokens, glass treatment, agent-state colors |
| `command-center.css` | Command Center variant-specific styles |
| `command-bar.css` | Command Bar overlay, search results, keyboard hints |

### Templates (`templates/`)

| File | Route |
|------|-------|
| `base.html` | Layout shell (nav, WS init, script loading) |
| `index.html` | `/` — Dashboard home |
| `agents.html` | `/agents` |
| `tasks.html` | `/tasks` |
| `kpis.html` | `/kpis` |
| `costs.html` | `/costs` |
| `escalations.html` | `/escalations` |
| `command-center.html` | `/command-center` |
| `mission-control.html` | `/mission-control` |
| `onboarding.html` | `/onboarding` |
| `finance.html` | `/finance` |
| `org-chart.html` | `/org-chart` |
