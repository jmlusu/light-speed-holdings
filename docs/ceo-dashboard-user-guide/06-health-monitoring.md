# Health Monitoring & Diagnostics

This section explains how to monitor the health of the CEO Dashboard, interpret its diagnostic signals, and resolve issues when something goes wrong. Whether you are a technical administrator keeping the system operational or a COO who needs to know "is the dashboard healthy?", this chapter gives you the tools to answer that question quickly and act on what you find.

---

## Dashboard Health at a Glance

The dashboard exposes its health status in two ways: a visual status indicator you can see without navigating anywhere, and a structured health check you can query programmatically.

### Visual Status Indicators

The **top header bar** on every page shows two real-time health signals:

| Indicator | What It Means | Location |
|-----------|---------------|----------|
| **WebSocket status dot** (green pulsing = *Live*, red = *Offline*) | Whether the dashboard's real-time connection is active. A green dot means data is streaming; a red dot means the frontend has fallen back to polling or is stale. | Top-right of header bar |
| **Uptime counter** | How long the dashboard process has been running since the last restart. Resets to zero on every restart. | Top-right of header bar, next to the status dot |

[Screenshot: Header bar annotated with WebSocket status dot, uptime counter, and client count]

When the WebSocket connection drops, a full-width **amber banner** appears at the top of the viewport: "Connection lost — working in offline mode." Data continues to load via polling fallback, but real-time updates stop until the connection restores.

### The Org Health Score Gauge

The most important single health indicator is the **Org Health Score** gauge on the Dashboard home page. This circular gauge displays a composite score from 0 to 100 and labels it with a color band:

| Band | Score Range | Meaning | Action |
|------|-------------|---------|--------|
| 🟢 Green (healthy) | 80–100 | Organization is operating within normal parameters. | Monitor. No action needed. |
| 🟡 Amber (degraded) | 50–79 | One or more components are underperforming. Investigate. | Click the gauge to expand the component grid and identify which metric is dragging the score down. |
| 🔴 Red (critical) | 0–49 | Multiple components are failing or one is severely degraded. | Immediate investigation required. Follow the diagnostic workflows below. |

> 💡 **Tip**: Click the gauge to expand the 2x2 component grid. Each card shows the component name, its current score, a color-coded status dot, and a mini sparkline chart. Click any card to see the detailed score breakdown with its weight in the composite.

[Screenshot: Org Health Score gauge expanded to show four component cards with sparkline charts]

### Status Bar Summary

Below the gauge, the **Alerts Bar** provides a compact summary of pending items that require attention:

- **Pending approvals** (amber badge) — tasks waiting for human approval
- **Open escalations** (red badge) — issues raised to the CEO or COO
- **In-progress tasks** (blue badge) — tasks currently being worked by agents

A healthy dashboard shows a green gauge, a green WebSocket dot, and low or zero counts in the amber and red badges. If any of these shift to warning colors, proceed to the relevant section below.

---

## The Org Health Score — Deep Dive

The **Org Health Score** ([see Glossary](#glossary)) is not a single measurement. It is a weighted composite of four independent component scores, each measuring a different dimension of organizational performance. Understanding how these components work — and how their weights interact — is essential for interpreting the score correctly and making informed configuration changes.

### Component Breakdown

| Component | Weight | What It Measures | Data Source | Score Behavior |
|-----------|--------|-------------------|-------------|----------------|
| **Task Success Rate** | 0.30 | Ratio of completed tasks to total tasks in the last 30 days | Message Bus (`inbox.json`) via `_company_window_tasks()` | Higher completion rate = higher score. Returns `None` when no tasks exist in the window. |
| **Agent Utilization** | 0.25 | Active agents (those appearing in recent tasks) as a percentage of all registered agents | Agent registry + Message Bus task data | More agents working = higher score. Capped at 100. Returns `None` when no agents are registered. |
| **Cost Efficiency** | 0.25 | Budget utilization — how much of the allocated budget has been spent | Cost summary from the data layer | Lower spend relative to budget = higher score. Returns `None` when no budget is configured. |
| **Error Rate** | 0.20 | Inverse of the error/exception rate across agent operations | Task statuses in the Message Bus (failed, error, cancelled tasks) | Fewer errors = higher score. A 0% error rate scores 100; a 10% error rate scores 90. Returns `None` when no tasks exist. |

### How the Composite Score Is Calculated

The calculator at `ai_company/dashboard/org_health.py` performs these steps on each evaluation:

1. **Collect component values.** Each component scorer returns a value from 0 to 100, or `None` if no data is available.
2. **Filter to available data.** Components returning `None` are excluded from the composite — the score reflects only dimensions where data exists.
3. **Compute weighted average.** The remaining component values are multiplied by their respective weights, summed, and divided by the sum of the active weights. This ensures that a missing component does not artificially lower the score — its weight is redistributed proportionally across the remaining components.
4. **Clamp and round.** The result is clamped to 0–100 and rounded to the nearest integer.
5. **Map to band.** The integer score is compared against the configured band thresholds to determine the color label.

#### Example Calculation

Suppose all four components are available and return these values:

| Component | Weight | Value | Weighted Contribution |
|-----------|--------|-------|-----------------------|
| Task Success Rate | 0.30 | 85 | 25.5 |
| Agent Utilization | 0.25 | 60 | 15.0 |
| Cost Efficiency | 0.25 | 70 | 17.5 |
| Error Rate | 0.20 | 95 | 19.0 |

Composite = (25.5 + 15.0 + 17.5 + 19.0) / (0.30 + 0.25 + 0.25 + 0.20) = 77.0 / 1.00 = **77** → 🟡 Amber

Now suppose the Cost Efficiency component has no data (`None`):

| Component | Weight | Value | Weighted Contribution |
|-----------|--------|-------|-----------------------|
| Task Success Rate | 0.30 | 85 | 25.5 |
| Agent Utilization | 0.25 | 60 | 15.0 |
| Error Rate | 0.20 | 95 | 19.0 |

Composite = (25.5 + 15.0 + 19.0) / (0.30 + 0.25 + 0.20) = 59.5 / 0.75 = **79** → 🟡 Amber

The score *increased* because the lower-scoring Cost Efficiency component was removed, and the weights were redistributed proportionally.

> ⚠️ **Warning**: A rising Org Health Score is not always good news. If a component returns `None` because its data source is unavailable (e.g., the Message Bus is down and no tasks can be read), the score may rise while the organization is actually degraded. Always check the component breakdown, not just the composite number.

### Configuring Weights and Bands

The composite score behavior is defined in `config/org_health.yaml`. You can modify this file to adjust how the score responds to organizational changes.

#### Band Thresholds

```yaml
bands:
  green:
    min: 80
    max: 100
  amber:
    min: 50
    max: 79
  red:
    min: 0
    max: 49
```

To make the green band harder to achieve (e.g., only scores of 90+ are "healthy"), change `green.min` to `90` and `amber.max` to `89`. To create a wider amber zone, lower `amber.min` to `40` and raise `green.min` to `85`.

#### Component Weights

```yaml
components:
  - name: task_success_rate
    weight: 0.30
  - name: agent_utilization
    weight: 0.25
  - name: cost_efficiency
    weight: 0.25
  - name: error_rate
    weight: 0.20
```

> ⚠️ **Warning**: Weights **must** sum to 1.0. The calculator validates this at startup and logs a warning if the sum deviates by more than 0.01. If you add or remove a component, adjust the remaining weights to maintain a total of 1.0.

#### What Configuration Changes Mean

| Change | Effect on Score |
|--------|-----------------|
| Increase `task_success_rate` weight to 0.40 | Task completion becomes more influential. A drop in task completion will pull the score down faster. |
| Decrease `error_rate` weight to 0.10 | Errors matter less. The score is more resilient to error spikes but less sensitive to error recovery. |
| Raise `green.min` to 90 | The "healthy" bar is higher. The dashboard shows amber more often, flagging marginal performance earlier. |
| Lower `amber.min` to 30 | The red zone shrinks. Only severe degradation triggers a red alert, reducing alert fatigue. |

> 💡 **Tip**: Start with conservative weight changes (shift by 0.05 at a time) and observe the score over a few days before making further adjustments. The score is sensitive to weight redistribution because it uses a proportional recalculation.

### Historical Trend Interpretation

The Org Health Score is designed to be evaluated over time, not just as a point-in-time snapshot. The component breakdown includes mini sparkline charts that show recent history.

| Trend Pattern | What It Means | Likely Cause |
|---------------|---------------|--------------|
| Score consistently ≥ 80 (green) | Stable, healthy operations | All components performing within normal bounds |
| Score fluctuating between 50–79 (amber) | Intermittent issues or one struggling component | Check which component card shows the lowest value and most volatile sparkline |
| Score steadily declining over days | Progressive degradation — a component is getting worse | Identify the declining component and investigate its data source |
| Score suddenly drops from green to red | Acute failure — something broke | Check the Alert System for fired alerts, then follow the "High error rate" diagnostic workflow |
| Score rises after being low, but a component shows `None` | The score is masking a problem — a data source went offline | Check the `/health` endpoint for missing dependencies |

> 📝 **Note**: The `OrgHealthCalculator.detect_anomalies()` method can automatically flag unusual component score movements using Z-score analysis. Anomalies are classified as "warning" (Z-score > 2.0) or "critical" (Z-score > 3.0). This is useful for catching sudden shifts that might otherwise go unnoticed in a slowly declining trend.

---

## Health Endpoints Reference

The dashboard exposes three HTTP endpoints for health monitoring. These are intended for external monitoring systems, load balancers, CI pipelines, and manual diagnosis.

### GET `/health` — Deep Health Check

**Purpose**: Comprehensive status check covering dependencies, disk, memory, and task state.

**When to use**: Manual diagnosis, automated health monitoring, and as a liveness check that goes beyond "is the process running?"

**Expected response (200)**:

```json
{
  "status": "ok",
  "service": "ai-company-dashboard",
  "version": "1.0.0",
  "uptime_seconds": 3642.1,
  "checks": {
    "inbox": "ok",
    "registry": "ok",
    "agents": "ok (12 files)",
    "config": "ok",
    "llm_providers": "2 configured",
    "audit_log": "ok (45.3 KB)",
    "disk_space": "12.4 GB free / 47.6 GB (26%)",
    "process_memory": "84.2 MB RSS",
    "memory_store": "ok (128 entries)",
    "dead_letter_queue": "empty"
  },
  "metrics_summary": {
    "tasks_total": 156,
    "tasks_completed": 142,
    "tasks_failed": 8,
    "llm_cost_usd": 12.4567,
    "success_rate_pct": 91.0
  },
  "timestamp": "2026-08-26T14:30:00+00:00"
}
```

**What each check verifies**:

| Check | What It Confirms | "Missing" Means |
|-------|-------------------|-----------------|
| `inbox` | `.opencode/inbox.json` is readable | The Message Bus file is absent — tasks cannot be created or tracked |
| `registry` | `company/agent-registry.json` exists | No agent definitions are available — the dashboard cannot display agents |
| `agents` | `.opencode/agents/*.md` files exist (reports count) | Agent markdown files have not been generated — the `ai-company generate` step was not run |
| `config` | `company/models.yaml` exists | LLM model configuration is missing |
| `llm_providers` | Environment variables for LLM API keys are set | No LLM providers are configured — agents cannot call language models |
| `audit_log` | `.opencode/audit` is readable (reports size) | No audit trail exists — agent operations are not being logged |
| `disk_space` | Free disk space on the volume | N/A — always reports a value or "unavailable" |
| `process_memory` | Current RSS memory usage of the dashboard process | N/A — always reports a value or "unavailable" |
| `memory_store` | `memory/` directory exists and contains JSON files | The persistent memory store is absent |
| `dead_letter_queue` | `.opencode/dead_letter_queue.json` is readable | N/A — an empty queue is healthy |

**Overall status logic**: If any check returns "missing" or "error", the overall `status` field is `"degraded"` instead of `"ok"`. A `"degraded"` status means the dashboard is running but operating with reduced capability.

> 📝 **Note**: All file checks are anchored at the configured `StateStore` root directory, not the process working directory. This means the health check is accurate regardless of which directory you launched the dashboard from.

### GET `/ready` — Readiness Probe

**Purpose**: Lightweight readiness check for Kubernetes-style orchestration. Returns `200` when the dashboard can serve requests, or `503` when core dependencies are missing.

**When to use**: Automated dependency checks, load balancer health routing, and CI/CD deployment gates. This is the endpoint a container orchestrator should poll to decide whether to route traffic to this instance.

**What it checks (hard requirements only)**:

| Dependency | Why It's Hard | Failure Mode |
|------------|---------------|--------------|
| `company/agent-registry.json` | The dashboard cannot function without agent definitions | 503 with `"reason": "registry missing"` |
| `.opencode/agents/` directory | The dashboard serves agent data from this directory | 503 with `"reason": "agents directory missing"` |

**Expected response (200 — ready)**:

```json
{
  "status": "ready"
}
```

**Expected response (503 — not ready)**:

```json
{
  "status": "not ready",
  "reason": "registry missing"
}
```

> ⚠️ **Warning**: A 503 from `/ready` means the dashboard **cannot** serve its primary functions. Unlike `/health` which reports degraded states, `/ready` makes a binary decision: ready or not ready. If you see 503s in your load balancer logs, the agent registry or agents directory is missing — run `ai-company generate` to rebuild them.

### GET `/metrics` — Prometheus Exporter

**Purpose**: Expose operational metrics in Prometheus text exposition format for integration with external monitoring systems (Prometheus, Grafana, Datadog, etc.).

**When to use**: When you need to feed dashboard health data into an existing monitoring stack, build custom dashboards, or set up long-term alerting rules.

**Content type**: `text/plain; version=0.0.4; charset=utf-8`

**Metrics exported**:

| Metric Name | Type | Description |
|-------------|------|-------------|
| `process_start_time_seconds` | gauge | Unix timestamp when the process started |
| `ai_company_uptime_seconds` | gauge | Seconds since process start |
| `ai_company_process_rss_bytes` | gauge | Current resident set size in bytes (requires `psutil`) |
| `ai_company_process_vms_bytes` | gauge | Current virtual memory size in bytes (requires `psutil`) |
| `ai_company_process_open_fds` | gauge | Number of open file descriptors (requires `psutil`) |
| `ai_company_process_max_rss_bytes` | gauge | Peak resident set size in bytes (Linux/macOS) |
| `ai_company_cpu_user_seconds_total` | counter | Total user CPU time |
| `ai_company_cpu_system_seconds_total` | counter | Total system CPU time |
| `ai_company_llm_requests_total` | counter | Total LLM API requests |
| `ai_company_llm_errors_total` | counter | Total LLM API errors |
| `ai_company_llm_cost_usd_total` | gauge | Total LLM cost across all providers |
| `ai_company_llm_cost_anthropic_usd` | gauge | LLM cost from Anthropic |
| `ai_company_llm_cost_openai_usd` | gauge | LLM cost from OpenAI |
| `ai_company_llm_cost_deepseek_usd` | gauge | LLM cost from DeepSeek |
| `ai_company_llm_cost_other_usd` | gauge | LLM cost from other providers |
| `ai_company_task_success_rate_pct` | gauge | Live task success rate as a percentage |
| `ai_company_llm_error_rate_pct` | gauge | LLM error rate as a percentage |
| `ai_company_llm_avg_cost_per_request_usd` | gauge | Average cost per LLM request |
| `ai_company_circuit_breaker_trips_total` | counter | Total circuit breaker trip events |
| `ai_company_circuit_breaker_half_open_total` | counter | Total circuit breaker half-open transitions |
| `ai_company_tasks_by_status{status="..."}` | gauge | Task count per status (completed, failed, pending, etc.) |
| `ai_company_agent_tasks_total{agent="..."}` | counter | Total tasks per agent |
| `ai_company_agent_successes_total{agent="..."}` | counter | Successful tasks per agent |
| `ai_company_agent_failures_total{agent="..."}` | counter | Failed tasks per agent |
| `ai_company_llm_model_calls_total{model="..."}` | counter | LLM calls per model |
| `ai_company_llm_model_cost_usd{model="..."}` | gauge | LLM cost per model |
| `ai_company_llm_model_tokens_in_total{model="..."}` | counter | Input tokens per model |
| `ai_company_llm_model_tokens_out_total{model="..."}` | counter | Output tokens per model |

> 📝 **Note**: In-memory counters (LLM requests, errors, costs) reset when the dashboard process restarts. The audit-log-derived metrics (per-agent, per-model) are computed from the persistent audit trail and survive restarts.

---

## KPI Snapshot System

The dashboard periodically collects Key Performance Indicator snapshots across all departments and stores them for historical analysis. This system runs in the background as part of the executor daemon.

### How Periodic Collection Works

The **KPI Snapshot Scheduler** (`ai_company/dashboard/kpis/scheduler.py`) is a time-gated wrapper that the executor daemon calls on every poll tick:

1. The daemon polls at its configured interval (default: every few seconds).
2. On each tick, the scheduler checks whether enough time has elapsed since the last snapshot (default interval: **300 seconds / 5 minutes**).
3. If the interval has elapsed, the scheduler triggers a full collection run.
4. The collection run invokes **8 department-specific KPI collectors** in sequence.

The collectors are:

| Collector | Department |
|-----------|------------|
| `EngineeringKPICollector` | Engineering |
| `HRKPICollector` | HR |
| `FinanceKPICollector` | Finance |
| `MarketingKPICollector` | Marketing |
| `SalesKPICollector` | Sales |
| `CustomerSuccessKPICollector` | Customer Success |
| `LegalKPICollector` | Legal |
| `OrgHealthKPICollector` | Org Health (composite) |

### What Gets Stored

Each collector returns a dictionary of KPI values for its department. These are ingested into two storage layers:

1. **SQLite database** — via `KPIPipeline.ingest_snapshot()`. This is the primary data store for the dashboard's real-time KPI views and trend analysis.
2. **NDJSON history files** — via `KPIHistoryStore.store_snapshot()`. Each department gets a file at `dashboard/kpi_history/<department>_history.ndjson`, one JSON object per line per snapshot. This provides a durable, append-only history that survives database corruption.

Each stored KPI entry contains:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO 8601 timestamp of the collection |
| `department` | Department identifier (e.g., `"engineering"`) |
| `kpi_key` | The specific KPI name (e.g., `"tasks_completed"`, `"failure_rate"`) |
| `current` | The numeric value at time of collection |
| `target` | The target value (if defined), otherwise `null` |
| `unit` | Unit of measurement (e.g., `"count"`, `"percent"`, `"usd"`) |
| `status` | Status indicator (`"ok"`, `"warning"`, `"critical"`) |

Non-numeric KPIs (such as agent-by-department breakdowns that return dictionaries) are automatically skipped during storage.

### Viewing Historical Snapshots

You can retrieve stored history through the `KPIHistoryStore` API:

| Operation | Method | Description |
|-----------|--------|-------------|
| Get all history for a department | `get_history(department)` | Returns all stored entries, oldest first |
| Filter by specific KPI | `get_history(department, kpi_key="failure_rate")` | Returns history for one KPI only |
| Filter by time range | `get_history(department, since="2026-08-25T00:00:00")` | Returns entries after the specified timestamp |
| Get the latest snapshot | `get_latest(department)` | Returns the most recent collection for a department |
| List departments with data | `list_departments()` | Returns department IDs that have stored history |
| Count stored entries | `count_entries(department)` | Returns the total number of stored KPI entries |

### Retention and Cleanup

KPI history files grow as new snapshots are appended. To manage storage:

- Use `clear(department)` to remove all history for a specific department.
- Use `clear()` to remove all history across all departments.
- The NDJSON files are located at `dashboard/kpi_history/` under the configured data directory.

> 💡 **Tip**: If you are running the dashboard in production, consider adding a periodic cleanup job that removes history files older than your retention window (e.g., 90 days). The `KPIHistoryStore` does not enforce automatic retention — it stores everything you give it.

---

## Alert System

The **Alert Engine** (`ai_company/dashboard/analytics.py`) evaluates threshold-based rules against live KPI snapshots and fires alerts when conditions are violated. Alerts are a critical part of the monitoring loop — they surface problems before they become crises.

### How Alert Rules Work

An alert rule defines a condition on a specific KPI. Each KPI snapshot is evaluated against all active rules. When a rule's condition is true, an alert fires.

Each rule has these properties:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Human-readable name (e.g., "High failure rate") |
| `department` | string | Department this rule applies to, or `"*"` for all departments |
| `kpi_key` | string | The KPI to watch (e.g., `"failure_rate"`) |
| `operator` | string | Comparison: `gt` (>), `lt` (<), `gte` (>=), `lte` (<=), `eq` (=) |
| `threshold` | number | The numeric value to compare against |
| `severity` | string | `info`, `warning`, or `critical` |
| `enabled` | boolean | Whether this rule is active |

### Configuring Thresholds

Rules can be managed programmatically or loaded from a JSON file.

**Loading rules from a JSON file**:

```json
[
  {
    "name": "High failure rate",
    "department": "*",
    "kpi_key": "failure_rate",
    "operator": "gt",
    "threshold": 10.0,
    "severity": "warning",
    "enabled": true
  },
  {
    "name": "Critical task backlog",
    "department": "engineering",
    "kpi_key": "pending_tasks",
    "operator": "gt",
    "threshold": 50.0,
    "severity": "critical",
    "enabled": true
  }
]
```

**Example threshold scenarios**:

| Scenario | Rule |
|----------|------|
| Alert when any department's failure rate exceeds 10% | `kpi_key: "failure_rate"`, `operator: "gt"`, `threshold: 10.0`, `department: "*"` |
| Alert when Engineering's pending tasks drop below 5 (idle team) | `kpi_key: "pending_tasks"`, `operator: "lt"`, `threshold: 5.0`, `department: "engineering"` |
| Alert when total cost exceeds $100 | `kpi_key: "total_cost"`, `operator: "gt"`, `threshold: 100.0`, `department: "*"` |
| Info notification when a KPI exactly equals its target | `kpi_key: "tasks_completed"`, `operator: "eq"`, `threshold: 100.0`, `severity: "info"` |

### Where Alerts Appear

| Location | What You See |
|----------|-------------|
| **Toast notifications** (bottom-right) | Each fired alert triggers a toast with the severity icon, alert name, department, KPI, and current value vs threshold |
| **Alerts Bar** on Dashboard home | Aggregated count of active alerts by severity |
| **Escalation stack** (top-right) | Critical alerts that require human action appear here with *Resolve* / *Dismiss* buttons |

### Alert History

Fired alerts are logged with a timestamp, the rule name, the triggering KPI value, and the threshold it violated. The alert message follows this format:

```text
[SEVERITY] Rule Name: department.kpi_key = value (operator threshold)
```

Example:

```text
[WARNING] High failure rate: engineering.failure_rate = 12.5 (gt 10.0)
[CRITICAL] Critical task backlog: engineering.pending_tasks = 67 (gt 50.0)
```

---

## Diagnostic Workflows

When something goes wrong, these step-by-step procedures help you identify the root cause and restore normal operation. Each workflow starts with symptoms and narrows to a specific cause.

### Workflow 1: Dashboard Won't Start

**Symptoms**: The dashboard process fails to start, exits immediately, or shows an error in the console.

**Diagnostic tree**:

1. **Check if a process is already running on the dashboard port.**
   - If another instance is using port `8420` (production) or `8421` (staging), the new process will fail with an address-already-in-use error.
   - **Fix**: Stop the existing process or configure a different port.

2. **Check if the required environment variables are set.**
   - At minimum, you need `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` for LLM functionality.
   - The dashboard itself will start without LLM keys, but agent operations will fail.
   - **Fix**: Set the required keys in your `.env` file or export them in your shell.

3. **Check if `company/agent-registry.json` exists.**
   - The readiness probe (`/ready`) will return 503 if this file is missing.
   - **Fix**: Run `ai-company generate` to regenerate the registry and agent files.

4. **Check if the SQLite database is accessible.**
   - If the database file is locked by another process, the dashboard may fail to initialize the data layer.
   - **Fix**: Ensure no other dashboard instance is running. If the database is corrupted, check for WAL/SHM files and remove stale locks.

5. **Check the logs for the specific error.**
   - Look at the console output or log files for a Python traceback. The most common startup errors are `ImportError` (missing dependency), `FileNotFoundError` (missing data directory), and `PermissionError` (insufficient file access).

6. **Verify Python version and dependencies.**
   - The dashboard requires Python 3.12+. Run `python --version` to confirm.
   - Run `uv sync` or `pip install -e .` to ensure all dependencies are installed.

### Workflow 2: Data Looks Wrong

**Symptoms**: KPI values on the dashboard don't match what you expect, scores seem too high or too low, or charts show unexpected patterns.

**Verification steps**:

1. **Check the Org Health Score components.**
   - Click the gauge to expand the component grid. Identify which component has the unexpected value.
   - If a component shows `None` or "No data", its data source is unavailable — the score may be artificially inflated because that component is excluded from the composite.

2. **Verify the data source directly.**
   - **Task data**: Check `.opencode/inbox.json` for the raw task list. Count completed vs total tasks manually to verify the task success rate.
   - **Agent data**: Check `company/agent-registry.json` to confirm the expected number of registered agents.
   - **Cost data**: Check the cost summary in the data layer or audit log.

3. **Check the KPI snapshot timestamp.**
   - If the snapshot is stale (more than 5 minutes old), the KPI scheduler may not be running.
   - Check the daemon status at `GET /api/v1/daemon/status`. The `last_tick_at` field shows when the daemon last ran.

4. **Check for stale NDJSON history.**
   - If the history files at `dashboard/kpi_history/` haven't been updated recently, the snapshot scheduler's interval may have elapsed but the collection is failing silently.
   - Check the daemon logs for KPI collection errors.

5. **Compare the Prometheus `/metrics` endpoint.**
   - The `ai_company_task_success_rate_pct` gauge in `/metrics` is computed live from the Message Bus. If it disagrees with the Org Health Score's task success rate component, the data sources may be reading from different points in time.

### Workflow 3: Real-Time Updates Stopped

**Symptoms**: The WebSocket status dot in the header bar turns red, the "Connection lost" banner appears, and charts stop updating.

**WebSocket diagnosis**:

1. **Check if the WebSocket endpoint is reachable.**
   - The WebSocket connects to `ws://<host>:<port>/ws/v1`. If the dashboard is behind a reverse proxy, ensure the proxy supports WebSocket upgrades (HTTP `Upgrade: websocket` header).

2. **Check the browser console.**
   - Open your browser's developer tools (F12) and look at the Console tab for WebSocket errors. Common messages include:
     - `WebSocket connection to 'ws://...' failed` — the server is unreachable
     - `WebSocket closed with code 1006` — abnormal closure, usually a network issue
     - `WebSocket closed with code 1008` — policy violation, often a CORS or auth issue

3. **Verify the WebSocket topics.**
   - The dashboard subscribes to these topics: `kpis`, `tasks`, `escalations`, `approvals`, `daemon`, `org_health`.
   - If the connection is established but you're not receiving updates on a specific topic, the server-side publisher for that topic may not be producing messages.

4. **Check the dashboard process health.**
   - A healthy WebSocket requires the dashboard process to be alive and responsive. Call `GET /health` to verify the process is running and check the `uptime_seconds` field.

5. **Test the polling fallback.**
   - The dashboard is designed to fall back to HTTP polling when the WebSocket drops. If polling is also failing, the issue is likely network connectivity or the dashboard process itself — not WebSocket-specific.

6. **Restart the WebSocket connection.**
   - If the WebSocket is stuck, the frontend will automatically attempt reconnection with exponential backoff. You can force a reconnection by refreshing the page.

### Workflow 4: KPIs Not Updating

**Symptoms**: KPI charts on the dashboard show the same values over time, or the KPI history stops growing.

**Scheduler diagnosis**:

1. **Check if the daemon is running.**
   - Call `GET /api/v1/daemon/status`. The response shows:
     - `state`: Should be `"running"`. If `"not_running"`, the daemon has never been started. If `"stale (process dead)"`, the daemon process has crashed.
     - `ticks_completed`: Should be increasing. If it's stuck at a fixed number, the daemon loop is frozen.
     - `last_tick_at`: Should be recent. If it's old, the daemon is not polling.

2. **Check the KPI scheduler interval.**
   - The default snapshot interval is 300 seconds (5 minutes). If the scheduler is running but snapshots appear infrequent, this is expected behavior.
   - To force an immediate snapshot, the scheduler's `reset()` method resets the internal timer so the next `run_due()` call triggers immediately.

3. **Check the SQLite database.**
   - If the database is unavailable (returns `None` from `get_database()`), the snapshot scheduler skips collection silently with a debug-level log message.
   - Verify the database path is correct and the file is accessible.

4. **Check for collection errors in the logs.**
   - The scheduler wraps collection in a try/except and logs exceptions at the `exception` level. Look for messages starting with "KPI snapshot failed" in the daemon logs.

5. **Verify the collectors are returning data.**
   - Each of the 8 department collectors reads from different data sources. If a specific department's KPIs are not updating while others are, the issue is likely in that collector's data source (e.g., a missing or corrupted file that the collector reads).

### Workflow 5: High Error Rate

**Symptoms**: The Org Health Score has dropped, the Error Rate component shows a low value, or alerts fire for high failure rates.

**Investigation procedure**:

1. **Identify which component is driving the score down.**
   - Expand the Org Health Score component grid. Check the Error Rate card — if it's red or has a volatile sparkline, this is the primary contributor.

2. **Check the task status breakdown.**
   - In the `/health` endpoint response, review `metrics_summary.tasks_failed` vs `metrics_summary.tasks_total`.
   - On the Dashboard home page, check the "Tasks by Status" chart for the proportion of failed tasks.

3. **Examine the audit log.**
   - The audit trail at `.opencode/audit` records every task completion with success/failure metadata. Look for patterns:
     - Are failures concentrated in one agent? (Check `ai_company_agent_failures_total` in `/metrics`)
     - Are failures concentrated in one department? (Check the task status breakdown)
     - Did failures start at a specific time? (Check the audit log timestamps)

4. **Check LLM provider health.**
   - High LLM error rates often indicate provider-side issues. Check `ai_company_llm_errors_total` and `ai_company_llm_error_rate_pct` in `/metrics`.
   - If circuit breaker trips are increasing (`ai_company_circuit_breaker_trips_total`), the LLM provider is returning errors frequently enough to trigger the breaker.

5. **Check the dead letter queue.**
   - The `/health` endpoint reports `dead_letter_queue` status. If there are pending items in the dead letter queue, tasks are failing repeatedly and being quarantined.

6. **Review error patterns over time.**
   - Use the `compute_trends()` function or the KPI history API to compare the current error rate against historical values. A sudden spike suggests an acute issue (provider outage, configuration change); a gradual increase suggests a systemic problem (resource exhaustion, model degradation).

---

## Monitoring Integration

The `/metrics` endpoint provides a standard Prometheus text exposition format that integrates with the most common monitoring stacks.

### Prometheus Configuration

Add this scrape configuration to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "ai-company-dashboard"
    scrape_interval: 30s
    static_configs:
      - targets: ["localhost:8420"]
    metrics_path: "/metrics"
```

### Grafana Dashboard Panels

The exported metrics support these common Grafana panel configurations:

| Panel | Query | Type |
|-------|-------|------|
| Dashboard Uptime | `ai_company_uptime_seconds` | Stat |
| LLM Cost Rate | `rate(ai_company_llm_cost_usd_total[5m])` | Time series |
| Task Success Rate | `ai_company_task_success_rate_pct` | Gauge (0–100) |
| LLM Error Rate | `ai_company_llm_error_rate_pct` | Gauge (0–100) with threshold bands |
| Cost by Provider | `ai_company_llm_cost_*_usd` (stacked) | Time series, stacked area |
| Agent Success vs Failure | `ai_company_agent_successes_total` vs `ai_company_agent_failures_total` | Bar chart |
| Process Memory | `ai_company_process_rss_bytes` | Time series |
| Circuit Breaker Events | `ai_company_circuit_breaker_trips_total` | Counter, rate over 5m |
| Tasks by Status | `ai_company_tasks_by_status` (per-label) | Pie or bar chart |

### Key Alert Rules for Prometheus

```yaml
# Alert when LLM error rate exceeds 15% for 5 minutes
- alert: HighLLMErrorRate
  expr: ai_company_llm_error_rate_pct > 15
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "LLM error rate is {{ $value }}%"

# Alert when dashboard is down
- alert: DashboardDown
  expr: up{job="ai-company-dashboard"} == 0
  for: 1m
  labels:
    severity: critical

# Alert when process memory exceeds 500MB
- alert: HighMemoryUsage
  expr: ai_company_process_rss_bytes > 524288000
  for: 10m
  labels:
    severity: warning
```

> 💡 **Tip**: Combine Prometheus metrics with the Org Health Score from the dashboard's API for a complete monitoring picture. Prometheus gives you infrastructure-level visibility; the Org Health Score gives you organizational-level visibility.

---

## Health Check Quick Reference Card

This one-page reference summarizes every health indicator, what it measures, its thresholds, and what to do when it signals a problem.

| Indicator | Where to Find It | Healthy | Warning | Critical | Action When Unhealthy |
|-----------|-------------------|---------|---------|----------|----------------------|
| **Org Health Score** | Dashboard home gauge | 🟢 ≥ 80 | 🟡 50–79 | 🔴 < 50 | Expand component grid → identify lowest component → follow diagnostic workflow |
| **WebSocket Status** | Header bar (top-right) | 🟢 Green pulsing | — | 🔴 Red | Check network, browser console, restart page |
| **`/health` status** | `GET /health` → `status` field | `"ok"` | `"degraded"` | — | Check `checks` object for "missing" entries → fix data sources |
| **`/ready` status** | `GET /ready` | `200 OK` | — | `503 Not Ready` | Run `ai-company generate` to rebuild registry/agents |
| **Task Success Rate** | Component card or `/metrics` → `ai_company_task_success_rate_pct` | ≥ 80% | 50–79% | < 50% | Check failed tasks in audit log → identify failing agent or LLM provider |
| **Agent Utilization** | Component card or compute from registry + task data | ≥ 70% | 30–69% | < 30% | Check if agents are blocked, tasks are available, registry is current |
| **Cost Efficiency** | Component card or cost summary | ≥ 70% | 40–69% | < 40% | Review LLM costs in `/metrics` → check for runaway agent loops |
| **Error Rate** | Component card or `/metrics` → `ai_company_llm_error_rate_pct` | ≤ 5% | 5–15% | > 15% | Check LLM provider status, circuit breaker trips, dead letter queue |
| **Daemon Status** | `GET /api/v1/daemon/status` → `state` | `"running"` | — | `"stale (process dead)"` or `"not_running"` | Restart the daemon process |
| **Disk Space** | `GET /health` → `checks.disk_space` | > 20% free | 10–20% free | < 10% free | Clean up old logs, audit files, or KPI history |
| **Process Memory** | `GET /health` → `checks.process_memory` | < 200 MB | 200–500 MB | > 500 MB | Check for memory leaks, restart the process |
| **Dead Letter Queue** | `GET /health` → `checks.dead_letter_queue` | `"empty"` | N pending > 0 | N pending > 10 | Review quarantined tasks, identify recurring failures |
| **LLM Providers** | `GET /health` → `checks.llm_providers` | ≥ 1 configured | — | `0 configured` | Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in `.env` |
| **Audit Log** | `GET /health` → `checks.audit_log` | `"ok (N KB)"` | `"error reading"` | `"missing"` | Check file permissions, verify `.opencode/audit` exists |
| **Alert Rules** | Dashboard Alerts Bar or toast notifications | 0 pending | 1–5 pending | > 5 pending or any critical | Review alerts, resolve escalations, adjust thresholds |

> 📝 **Note**: "Warning" thresholds in this table are approximate guidelines. The actual behavior depends on your configured band thresholds in `config/org_health.yaml` and your alert rules. Customize these to match your organization's risk tolerance.

---

*This section covers the complete health monitoring and diagnostics capability of the CEO Dashboard. For real-time data flow details, see [Section 12 — Real-Time Features](12-real-time-features.md). For troubleshooting other dashboard issues, see [Section 16 — Troubleshooting](16-troubleshooting.md).*

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-26 | Doctor Owner | Initial Health Monitoring & Diagnostics section. Covered org health score, health endpoints, KPI snapshot system, alert system, diagnostic workflows, monitoring integration, and quick reference card. |
