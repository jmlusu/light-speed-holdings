# Command Center — Read-Only API Reference

> Added in PR #127 (2026-08-19). All endpoints are read-only, no authentication required for `/health`.

## `GET /health`

Deep health check with dependency, disk, and memory status. **Exempt from dashboard auth** (`DASHBOARD_AUTH_MODE`).

**Response** `200 OK`

```json
{
  "status": "ok",
  "checks": {
    "inbox": "ok",
    "registry": "ok",
    "agents": "ok (135 files)",
    "config": "ok",
    "llm_providers": "2 configured",
    "audit_log": "ok (42.3 KB)",
    "disk_space": "ok (128.5 GB free)",
    "process_memory": "ok (45.2 MB)",
    "memory_store": "ok (12 entries)",
    "dead_letter_queue": "empty"
  }
}
```

| Field | Description |
|-------|-------------|
| `status` | `"ok"` if all checks pass, `"degraded"` if any check is missing or errored |
| `checks.inbox` | `inbox.json` accessibility via StateStore allowlist |
| `checks.registry` | `company/agent-registry.json` exists |
| `checks.agents` | `.opencode/agents/` directory — file count |
| `checks.config` | `company/models.yaml` exists |
| `checks.llm_providers` | Count of configured LLM API keys (env vars) |
| `checks.audit_log` | `.opencode/audit` trail size |
| `checks.disk_space` | Available disk space |
| `checks.process_memory` | Dashboard process memory usage |
| `checks.memory_store` | Memory engine entry count |
| `checks.dead_letter_queue` | DLQ pending task count |

**Source**: `src/ai_company/dashboard/monitoring.py:403`

---

## `GET /api/v1/briefing`

Aggregated executive briefing — priority-ordered attention items for the CEO.

**Response** `200 OK`

```json
{
  "items": [
    {
      "id": 0,
      "title": "Escalation: Agent X blocked on approval",
      "source": "agent-x → ceo",
      "priority": "high",
      "type": "escalation",
      "timestamp": "2026-08-19T15:30:00Z",
      "task_id": "task-abc-123"
    }
  ],
  "summary": {
    "total_items": 5,
    "high_priority": 2,
    "medium_priority": 3,
    "types": {
      "escalation": 1,
      "approval": 2,
      "failed_task": 1,
      "revenue_alert": 1
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `items[].priority` | `"high"` or `"medium"` |
| `items[].type` | One of: `escalation`, `approval`, `failed_task`, `revenue_alert`, `workflow_failure` |
| `summary.total_items` | Total attention items |
| `summary.high_priority` | Count of high-priority items |
| `summary.medium_priority` | Count of medium-priority items |
| `summary.types` | Breakdown by item type |

**Data sources** (in priority order):
1. Escalation alerts from SQLite `escalation_events` table (fallback: `orchestrator/escalation.yaml`)
2. Pending approvals from `orchestrator/approvals.yaml`
3. Failed tasks from MessageBus inbox
4. Revenue/cost alerts from KPI data
5. Workflow step failures

**Source**: `src/ai_company/dashboard/api.py:2380`

---

## `GET /api/v1/models/telemetry`

Per-model telemetry summary derived from audit log entries.

**Response** `200 OK`

```json
[
  {
    "model": "gpt-4o",
    "request_count": 142,
    "success_rate": 0.972,
    "avg_latency_ms": 1250.5,
    "total_cost": 8.42
  },
  {
    "model": "claude-sonnet-4-20250514",
    "request_count": 89,
    "success_rate": 0.989,
    "avg_latency_ms": 890.3,
    "total_cost": 3.21
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Model identifier (e.g., `gpt-4o`, `claude-sonnet-4-20250514`) |
| `request_count` | integer | Total tool_call + tool_result events for this model |
| `success_rate` | float | Ratio of successful tool_results (no error) to total events |
| `avg_latency_ms` | float | Average latency in milliseconds (from `latency_ms` metadata) |
| `total_cost` | float | Cumulative cost in USD (from `cost` metadata) |

**Behavior**:
- Aggregates `tool_call` / `tool_result` events from `.opencode/audit` JSONL trail
- Returns empty list `[]` when no audit data is available
- Results sorted alphabetically by model name

**Source**: `src/ai_company/dashboard/api.py:1370`
