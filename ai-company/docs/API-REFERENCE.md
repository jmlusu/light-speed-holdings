# API Reference

REST API and WebSocket documentation for the AI Company Builder CEO Dashboard.

**Base URL:** `http://localhost:8420`  
**OpenAPI Title:** Light Speed Holdings — CEO Dashboard  
**Version:** 0.1.0

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Health Check](#2-health-check)
3. [Dashboard & KPIs](#3-dashboard--kpis)
4. [Agents](#4-agents)
5. [Organization Chart](#5-organization-chart)
6. [Tasks](#6-tasks)
7. [Approvals](#7-approvals)
8. [Escalations](#8-escalations)
9. [Departments](#9-departments)
10. [Model Routing](#10-model-routing)
11. [Scheduler](#11-scheduler)
12. [Department KPIs](#12-department-kpis)
13. [WebSocket Protocol](#13-websocket-protocol)
14. [Data Models](#14-data-models)
15. [Error Handling](#15-error-handling)
16. [Examples](#16-examples)

---

## 1. Authentication

The API currently operates without authentication for local development. For production deployments, implement authentication middleware (see [Deployment Guide](DEPLOYMENT-GUIDE.md)).

**CORS:** All origins are allowed by default (`*`). Restrict in production via the `allowed_origins` configuration.

---

## 2. Health Check

### `GET /health`

Returns the health status of the dashboard service.

**Response:**

```json
{
  "status": "ok",
  "service": "ceo-dashboard"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Service is healthy |

---

## 3. Dashboard & KPIs

### `GET /api/dashboard`

Returns an aggregated KPI snapshot of the entire company. Includes task counts, pending approvals, open escalations, agent count, and uptime.

**Response Model:** `KPIs`

```json
{
  "pending_tasks": 5,
  "in_progress_tasks": 3,
  "completed_tasks": 142,
  "failed_tasks": 2,
  "escalated_tasks": 1,
  "pending_approvals": 3,
  "open_escalations": 1,
  "total_agents": 27,
  "scheduled_tasks": 9,
  "uptime_seconds": 3600.5
}
```

**Side Effects:** Broadcasts KPI snapshot and alerts to all connected WebSocket clients.

---

### `GET /api/kpis/live`

Returns live KPI values computed from operational data using the department KPI collectors. Provides real-time snapshots for all 7 departments.

**Response:**

```json
{
  "engineering": {
    "deployment_frequency": 8,
    "cycle_time_days": 2.1,
    "test_coverage_pct": 87
  },
  "marketing": {
    "campaign_count": 4,
    "total_impressions": 15000
  },
  "sales": {
    "pipeline_value": 250000,
    "conversion_rate": 0.15
  },
  "finance": {
    "budget_utilization": 0.72,
    "cost_per_agent": 120
  },
  "hr": {
    "active_agents": 27,
    "onboarding_queue": 2
  },
  "customer_success": {
    "open_tickets": 8,
    "avg_resolution_hours": 4.2
  },
  "legal": {
    "pending_contracts": 3,
    "compliance_score": 0.95
  }
}
```

**Side Effects:** Broadcasts KPI snapshot to WebSocket clients.

---

## 4. Agents

### `GET /api/agents`

Returns a list of all registered agents from the agent registry.

**Response Model:** `list[AgentSummary]`

```json
[
  {
    "name": "CTO",
    "role": "Chief Technology Officer",
    "type": "Executive",
    "department": "engineering",
    "reports_to": "chief-of-staff",
    "direct_reports": ["lead-engineer", "lead-designer"],
    "description": "Oversees all technology decisions",
    "model": "opencode/big-pickle"
  }
]
```

---

### `GET /api/agents/{name}`

Returns details for a specific agent by name.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Agent name (e.g., `CTO`, `Lead Engineer`) |

**Response Model:** `AgentSummary`

```json
{
  "name": "Lead Engineer",
  "role": "Lead Engineer",
  "type": "Specialist",
  "department": "engineering",
  "reports_to": "CTO",
  "direct_reports": [],
  "description": "Leads the engineering team",
  "model": null
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Agent found |
| 404 | Agent not found |

---

## 5. Organization Chart

### `GET /api/org-chart`

Returns the full organization chart as a nested tree structure, rooted at the Chief of Staff (under the human CEO).

**Response Model:** `list[OrgNode]`

```json
[
  {
    "name": "chief-of-staff",
    "role": "Chief of Staff",
    "type": "Executive",
    "department": "",
    "children": [
      {
        "name": "CTO",
        "role": "Chief Technology Officer",
        "type": "Executive",
        "department": "engineering",
        "children": [
          {
            "name": "Lead Engineer",
            "role": "Lead Engineer",
            "type": "Specialist",
            "department": "engineering",
            "children": []
          }
        ]
      }
    ]
  }
]
```

---

## 6. Tasks

### `GET /api/tasks`

Returns a list of all tasks from the task queue. Supports filtering.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter by status (`pending`, `in_progress`, `completed`, `failed`, `escalated`) |
| `agent` | string | No | Filter by sender or receiver agent ID |

**Response Model:** `list[TaskItem]`

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "sender_id": "human-ceo",
    "receiver_id": "lead-engineer",
    "instruction": "Review PR #42 for the authentication module",
    "status": "pending",
    "priority": "high",
    "created_at": "2026-07-19T10:30:00",
    "completed_at": null,
    "result": null
  }
]
```

---

### `POST /api/tasks`

Creates a new task in the task queue.

**Request Body:** `TaskAssign`

```json
{
  "receiver_id": "lead-engineer",
  "instruction": "Review PR #42 for the authentication module",
  "priority": "high",
  "sender_id": "human-ceo"
}
```

**Request Fields:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `receiver_id` | string | Yes | — | Agent that will execute the task |
| `instruction` | string | Yes | — | Task description/instruction |
| `priority` | string | No | `"medium"` | Task priority: `low`, `medium`, `high`, `critical` |
| `sender_id` | string | No | `"human-ceo"` | Agent creating the task |

**Response:** `TaskItem` (201 Created)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "sender_id": "human-ceo",
  "receiver_id": "lead-engineer",
  "instruction": "Review PR #42 for the authentication module",
  "status": "pending",
  "priority": "high",
  "created_at": "2026-07-19T10:30:00",
  "completed_at": null,
  "result": null
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 201 | Task created successfully |
| 422 | Validation error in request body |

---

## 7. Approvals

### `GET /api/approvals`

Returns all pending approval requests that haven't expired.

**Response Model:** `list[ApprovalItem]`

```json
[
  {
    "id": "REQ-001",
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "agent_id": "cto",
    "action": "deploy to production",
    "description": "Deploy v2.1.0 to production servers",
    "status": "pending",
    "requested_at": "2026-07-19T09:00:00",
    "expires_at": "2026-07-20T09:00:00"
  }
]
```

---

### `POST /api/approvals/{request_id}/approve`

Approves a pending approval request.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `request_id` | string | The approval request ID |

**Request Body:** `ApprovalDecision` (optional)

```json
{
  "approved_by": "human-ceo",
  "notes": "Looks good, proceed with deployment"
}
```

**Response:**

```json
{
  "ok": true,
  "id": "REQ-001"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Request approved |
| 404 | Request not found or already processed |

---

### `POST /api/approvals/{request_id}/reject`

Rejects a pending approval request.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `request_id` | string | The approval request ID |

**Request Body:** `ApprovalDecision` (optional)

```json
{
  "approved_by": "human-ceo",
  "notes": "Not ready yet, needs more testing"
}
```

**Response:**

```json
{
  "ok": true,
  "id": "REQ-001"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Request rejected |
| 404 | Request not found or already processed |

---

## 8. Escalations

### `GET /api/escalations`

Returns all unresolved escalation events.

**Response Model:** `list[EscalationItem]`

```json
[
  {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "rule_id": "timeout-rule",
    "from_agent": "backend-engineer",
    "to_agent": "lead-engineer",
    "reason": "Task exceeded SLA timeout of 30 minutes",
    "timestamp": "2026-07-19T10:30:00",
    "resolved": false
  }
]
```

---

### `POST /escalations/{task_id}/resolve`

Marks an escalation as resolved.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `task_id` | string | The task ID with the open escalation |

**Response:**

```json
{
  "ok": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Escalation resolved |
| 404 | No open escalation found for this task |

---

## 9. Departments

### `GET /api/departments`

Returns all configured departments.

**Response Model:** `list[DepartmentInfo]`

```json
[
  {
    "name": "engineering",
    "executive": "cto",
    "agents": ["lead-engineer", "backend-engineer", "frontend-engineer"],
    "total_agents": 3
  },
  {
    "name": "marketing",
    "executive": "cmo",
    "agents": ["content-writer", "growth-marketer"],
    "total_agents": 2
  }
]
```

---

## 10. Model Routing

### `GET /api/models`

Returns the model routing assignment for every agent.

**Response Model:** `list[ModelRouteItem]`

```json
[
  {
    "agent": "CTO",
    "provider": "opencode",
    "model": "big-pickle",
    "tier": "premium",
    "reason": "Explicit override in agent_overrides"
  },
  {
    "agent": "Content Writer",
    "provider": "deepseek",
    "model": "deepseek-chat",
    "tier": "fast",
    "reason": "Default tier for Specialist agents"
  }
]
```

---

### `GET /api/models/tiers`

Returns the available model tiers with their providers.

**Response Model:** `list[TierInfo]`

```json
[
  {
    "id": "fast",
    "description": "Simple tasks, drafts",
    "providers": [
      {"provider": "deepseek", "model": "deepseek-chat"},
      {"provider": "ollama", "model": "llama3"}
    ]
  },
  {
    "id": "standard",
    "description": "General work",
    "providers": [
      {"provider": "opencode", "model": "big-pickle"},
      {"provider": "openai", "model": "gpt-4o-mini"}
    ]
  },
  {
    "id": "premium",
    "description": "Complex reasoning",
    "providers": [
      {"provider": "opencode", "model": "big-pickle"},
      {"provider": "anthropic", "model": "claude-sonnet"}
    ]
  }
]
```

---

## 11. Scheduler

### `GET /api/scheduler`

Returns all scheduled recurring tasks.

**Response:**

```json
[
  {
    "id": "daily-briefing",
    "name": "Daily Briefing",
    "interval_minutes": 360,
    "next_run": "2026-07-19T12:00:00",
    "enabled": true,
    "task_template": {
      "instruction": "Generate daily executive briefing",
      "receiver_id": "chief-of-staff"
    }
  }
]
```

---

## 12. Department KPIs

### `GET /api/kpis`

Returns all department KPI definitions.

**Response:**

```json
{
  "engineering": {
    "name": "Engineering",
    "kpis": [
      {
        "id": "eng-deploy-freq",
        "name": "Deployment Frequency",
        "target": 10,
        "unit": "per week",
        "frequency": "weekly"
      }
    ]
  },
  "marketing": {
    "name": "Marketing",
    "kpis": [...]
  }
}
```

---

### `GET /api/kpis/summary`

Returns a flat summary of all KPIs across all departments.

**Response:**

```json
[
  {
    "department": "engineering",
    "department_name": "Engineering",
    "kpi_id": "eng-deploy-freq",
    "name": "Deployment Frequency",
    "target": 10,
    "unit": "per week",
    "frequency": "weekly"
  }
]
```

---

### `GET /api/departments/{dept_name}/kpis`

Returns KPI definitions for a specific department.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `dept_name` | string | Department ID (e.g., `engineering`, `marketing`) |

**Response:** Department KPI configuration object.

**Status Codes:**

| Code | Description |
|------|-------------|
| 200 | Department found |
| 404 | Department not found in KPI config |

---

## 13. WebSocket Protocol

### Endpoint

```
ws://localhost:8420/ws/dashboard
```

### Connection Lifecycle

1. Client connects to the WebSocket endpoint
2. Server sends a `connected` message with timestamp and active client count
3. Client may send `ping` messages for application-level keepalive
4. Server broadcasts KPI updates and alerts to all connected clients
5. Client disconnects gracefully (server cleans up)

### Message Types

#### Client → Server

**Ping (keepalive):**
```json
{"type": "ping"}
```

**Subscribe (future feature):**
```json
{"type": "subscribe", "topics": ["kpis", "alerts"]}
```

#### Server → Client

**Connected (on connection):**
```json
{
  "type": "connected",
  "timestamp": "2026-07-19T10:30:00+00:00",
  "active_clients": 1
}
```

**KPI Update:**
```json
{
  "type": "kpi_update",
  "timestamp": "2026-07-19T10:30:00+00:00",
  "payload": {
    "pending_tasks": 5,
    "in_progress_tasks": 3,
    "completed_tasks": 142,
    "failed_tasks": 2,
    "escalated_tasks": 1,
    "pending_approvals": 3,
    "open_escalations": 1,
    "total_agents": 27,
    "scheduled_tasks": 9,
    "uptime_seconds": 3600.5
  }
}
```

**Alert:**
```json
{
  "type": "alert",
  "timestamp": "2026-07-19T10:30:00+00:00",
  "payload": {
    "category": "approval",
    "request_id": "REQ-001",
    "action": "deploy to production",
    "agent_id": "cto",
    "tier": 2
  }
}
```

```json
{
  "type": "alert",
  "timestamp": "2026-07-19T10:30:00+00:00",
  "payload": {
    "category": "escalation",
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "reason": "Task exceeded SLA timeout",
    "agent_id": "backend-engineer"
  }
}
```

**Pong (response to ping):**
```json
{
  "type": "pong",
  "timestamp": "2026-07-19T10:30:00+00:00"
}
```

**Error:**
```json
{
  "type": "error",
  "detail": "Unknown message type: foo"
}
```

### JavaScript Client Example

```javascript
const ws = new WebSocket("ws://localhost:8420/ws/dashboard");

ws.onopen = () => {
  console.log("Connected to dashboard");
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  switch (msg.type) {
    case "kpi_update":
      console.log("KPI Update:", msg.payload);
      updateDashboard(msg.payload);
      break;
    case "alert":
      console.log("Alert:", msg.payload);
      showAlert(msg.payload);
      break;
    case "connected":
      console.log("Active clients:", msg.active_clients);
      break;
  }
};

// Keepalive
setInterval(() => {
  ws.send(JSON.stringify({ type: "ping" }));
}, 30000);
```

### Python Client Example

```python
import asyncio
import json
import websockets

async def dashboard_listener():
    uri = "ws://localhost:8420/ws/dashboard"
    async with websockets.connect(uri) as ws:
        # Receive connected message
        msg = await ws.recv()
        print("Connected:", json.loads(msg))

        # Send periodic pings
        while True:
            await ws.send(json.dumps({"type": "ping"}))
            msg = await ws.recv()
            data = json.loads(msg)

            if data["type"] == "kpi_update":
                print("KPIs:", data["payload"])
            elif data["type"] == "alert":
                print("Alert:", data["payload"])

            await asyncio.sleep(30)

asyncio.run(dashboard_listener())
```

---

## 14. Data Models

All response models are defined in `src/ai_company/dashboard/models.py` using Pydantic v2.

### KPIs

| Field | Type | Description |
|-------|------|-------------|
| `pending_tasks` | int | Tasks waiting to be processed |
| `in_progress_tasks` | int | Tasks currently being executed |
| `completed_tasks` | int | Successfully completed tasks |
| `failed_tasks` | int | Tasks that failed |
| `escalated_tasks` | int | Tasks that were escalated |
| `pending_approvals` | int | Approval requests awaiting response |
| `open_escalations` | int | Unresolved escalations |
| `total_agents` | int | Number of registered agents |
| `scheduled_tasks` | int | Recurring scheduled tasks |
| `uptime_seconds` | float | Dashboard uptime in seconds |

### AgentSummary

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Agent name |
| `role` | str | Job title / role |
| `type` | str | Agent type (Executive, Board, Specialist) |
| `department` | str | Department assignment |
| `reports_to` | str | Parent agent ID |
| `direct_reports` | list[str] | Child agent IDs |
| `description` | str | Agent description |
| `model` | Optional[str] | Assigned LLM model |

### TaskItem

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique task identifier |
| `sender_id` | str | Agent that created the task |
| `receiver_id` | str | Agent assigned to execute |
| `instruction` | str | Task description |
| `status` | str | Task status |
| `priority` | str | Task priority |
| `created_at` | Optional[str] | Creation timestamp |
| `completed_at` | Optional[str] | Completion timestamp |
| `result` | Optional[str] | Execution result |

### TaskAssign

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `receiver_id` | str | — | Agent to assign the task to |
| `instruction` | str | — | Task description |
| `priority` | str | `"medium"` | Task priority level |
| `sender_id` | str | `"human-ceo"` | Agent creating the task |

### ApprovalItem

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Request identifier |
| `task_id` | str | Related task ID |
| `agent_id` | str | Agent requesting approval |
| `action` | str | Action requiring approval |
| `description` | str | Detailed description |
| `status` | str | Request status (pending, approved, rejected) |
| `requested_at` | Optional[str] | Request timestamp |
| `expires_at` | Optional[str] | Expiration timestamp |

### ApprovalDecision

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `approved_by` | str | `"human-ceo"` | Who made the decision |
| `notes` | Optional[str] | Decision notes |

### EscalationItem

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | str | Related task ID |
| `rule_id` | str | Escalation rule that triggered |
| `from_agent` | str | Agent the task was escalated from |
| `to_agent` | str | Agent the task was escalated to |
| `reason` | str | Escalation reason |
| `timestamp` | Optional[str] | When the escalation occurred |
| `resolved` | bool | Whether the escalation has been resolved |

### DepartmentInfo

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Department name/ID |
| `executive` | str | Executive in charge |
| `agents` | list[str] | Agent IDs in the department |
| `total_agents` | int | Total agent count |

### ModelRouteItem

| Field | Type | Description |
|-------|------|-------------|
| `agent` | str | Agent name |
| `provider` | str | LLM provider |
| `model` | str | Model name |
| `tier` | str | Cost tier |
| `reason` | str | Why this model was chosen |

### TierInfo

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Tier identifier |
| `description` | str | Tier description |
| `providers` | list[dict] | Provider/model pairs |

### OrgNode

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Agent name |
| `role` | str | Job title |
| `type` | str | Agent type |
| `department` | str | Department |
| `children` | list[OrgNode] | Nested child nodes |

---

## 15. Error Handling

### HTTP Error Responses

All error responses follow a consistent format:

```json
{
  "detail": "Human-readable error message"
}
```

### Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Resource created |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |

### Common Error Scenarios

**Agent not found:**
```json
{
  "detail": "Agent 'nonexistent-agent' not found"
}
```

**Approval request already processed:**
```json
{
  "detail": "Request 'REQ-001' not found or already processed"
}
```

**Escalation already resolved:**
```json
{
  "detail": "No open escalation for task 'TASK-001'"
}
```

**Department not in KPI config:**
```json
{
  "detail": "Department 'nonexistent' not found in KPI config"
}
```

---

## 16. Examples

### Full Workflow: Create, Approve, Execute

```bash
# 1. Create a task
curl -X POST http://localhost:8420/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_id": "cto",
    "instruction": "Plan Q3 technology roadmap",
    "priority": "high"
  }'

# 2. Check for pending approvals
curl http://localhost:8420/api/approvals

# 3. Approve the request
curl -X POST http://localhost:8420/api/approvals/REQ-001/approve \
  -H "Content-Type: application/json" \
  -d '{"approved_by": "human-ceo", "notes": "Go ahead"}'

# 4. Check KPIs
curl http://localhost:8420/api/dashboard

# 5. Resolve any escalations
curl -X POST http://localhost:8420/api/escalations/TASK-001/resolve
```

### Monitoring via WebSocket

```bash
# Using websocat (CLI tool)
websocat ws://localhost:8420/ws/dashboard

# Send a ping
>{"type": "ping"}
<{"type": "pong", "timestamp": "2026-07-19T10:30:00+00:00"}
```

### Query Model Routing

```bash
# See which model each agent uses
curl http://localhost:8420/api/models

# See available tiers
curl http://localhost:8420/api/models/tiers
```

### Explore the Org Chart

```bash
# Get the full org tree
curl http://localhost:8420/api/org-chart | python -m json.tool

# Get details for a specific agent
curl http://localhost:8420/api/agents/CTO
```
