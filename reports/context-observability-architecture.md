# Context Intelligence & Execution Observability Architecture

**Date**: 2026-11-03
**Project**: `C:\Users\jmlus\light-speed-holdings\.worktrees\silent-knight`
**Status**: Design deliverable (READ ONLY — no source code modified)

---

## 1. Current Architecture

### 1.1 System Overview

The current LightSpeed architecture consists of seven independently developed systems, each with its own metrics, caching, and telemetry. There is **no unified cross-system layer** for context or execution identity.

```
┌─────────────────────────────────────────────────────────────────┐
│                        SEVEN SILoED SYSTEMS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Memory Engine                                                  │
│     • 6 memory types (episodic, semantic, procedural,             │
│       relational, temporal, aggregate)                           │
│     • FileStore JSON persistence                                   │
│     • recall/search/prune/consolidate lifecycle                    │
│                                                                  │
│  2. Decision Engine                                                │
│     • 5-tier approval matrix (AUTO_APPROVE=0 through CEO_ONLY=4)   │
│     • Classification: tool type, path sensitivity,                 │
│       command sensitivity, risk context, seniority                   │
│     • HITL approval gate integration                               │
│                                                                  │
│  3. Workflow Engine                                                │
│     • 9 workflow definitions from company-registry.yaml            │
│     • YAML anchors/aliases for reusability                         │
│     • WorkflowInstance persistence to workflows/instances/{id}.json  │
│     • advance/complete_step/cancel/get_status methods              │
│                                                                  │
│  4. Model Router                                                   │
│     • 5-layer routing priority:                                  │
│       per-agent override → explicit context →                      │
│       domain detection → task-type routing →                       │
│       agent-type/priority rules → standard fallback                │
│     • Reads company/models.yaml                                    │
│     • Does NOT execute LLMs itself                                 │
│                                                                  │
│  5. Executor                                                       │
│     • ToolRunner executes 7 canonical tools via subprocess         │
│       (read, edit, grep, list, bash, webfetch, task)               │
│     • Tier-based authorization via check_tier_rules()                │
│     • HITL approval gate integration                               │
│     • Command allowlist                                            │
│     • Output sanitization (PII/content safety)                     │
│     • SLA timeout: 120s                                            │
│     • Dead-letter logging                                          │
│                                                                  │
│  6. Graph Engine                                                     │
│     • 4 graph types (org_chart, decision_graph,                     │
│       workflow_graph, knowledge_graph)                             │
│     • Built statically from CompanyRegistry data                     │
│     • NOT updated live during task execution                       │
│     • get_graph(name) builds/caches                                 │
│     • find_path BFS                                                │
│                                                                  │
│  7. Cache Mechanisms                                               │
│     • LLM response file cache (.cache/llm/): keyed by               │
│       (system_prompt, user_prompt, model, temperature)              │
│       with TTL                                                     │
│     • OAuth2 in-memory TTL-bounded token cache                       │
│     • Model Router free-model catalog cache (1-hour TTL             │
│       from OpCode Zen API or static fallback)                       │
│     • Memory engine auto-vector indexing when VectorStore             │
│       configured                                                   │
│     • YAML config caching (load_yaml_cached) in generator            │
│                                                                  │
│    ↑ NO UNIFIED APPLICATION-LEVEL CACHE ↑                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Context Construction Per Agent Invocation

```
CEO Instruction
    ↓
Task dispatched to Message Bus (.opencode/inbox.json)
    ↓
Decision Engine: 5-tier approval matrix evaluation
    ↓
request_id generation (if not already present)
    ↓
Executor: ToolRunner with sandboxing
    ↓
Tool execution (7 canonical tools via subprocess)
    ↓
Output sanitization (PII/content safety)
    ↓
Result returned via Message Bus
```

**Context sources per invocation** (from source code analysis):

| Context Element | Source | Frequency |
|----------------|--------|-----------|
| `AGENTS.md` | Read at task start (§4, rule 1) | Every task |
| `company-registry.yaml` | Generator reads for agent card generation | On regenerate |
| `company/models.yaml` | Model Router reads for provider/model mapping | Per-LLM call |
| `templates/agents/agent.md.j2` | Agent template rendering | On card generation |
| `.opencode/agents/*.md` | Generated agent cards | On task dispatch |
| `src/ai_company/**/*.py` | Source code reads | Depends on task |
| `logs/token_usage.jsonl` | Cost tracker appends | Per-LLM call |
| `.cache/token_usage.db` | Cost tracker SQLite writes | Per-LLM call |
| `logs/` | General logging | Depends on configuration |

**Repeated reads identified** (from context-intelligence-investigation-report.md):
- `AGENTS.md` read at task start (§4, rule 1) — every invocation
- `company-registry.yaml` parsed by generator — on regeneration
- `company/models.yaml` read by Model Router — per LLM call
- `history_manager.py` ConversationHistoryManager state — per agent loop
- `token_counter.py` heuristic counting — per LLM call fallback

### 1.3 Execution Observability

**Current state** (from observability-research-report.md and source code analysis):

| Component | Metrics Available | Tracking Mechanism |
|-----------|------------------|-------------------|
| Token counting | heuristic counts, provider-reported | `token_counter.py`, `cost_tracker.py` |
| Cost recording | JSONL + SQLite | `cost_tracker.py` records `logs/token_usage.jsonl` + `.cache/token_usage.db` |
| Execution logs | tool name, tier, status, errors, request_id, SLA timeout | `executor/tool_runner.py` |
| HITL gate | approval decisions with request_id | Decision engine integration |
| OpenTelemetry | opt-in spans (console/in-memory) | `telemetry/tracer.py`, `telemetry/bridge.py`, `telemetry/exporter.py` |
| ConversationHistoryManager | cache_hits, cache_misses, tool_call_count, consecutive_failures | `executor/agent_loop.py` |
| Evidence store | size, events, rotations | `monitoring/evidence_metrics.py` (Prometheus) |
| Model Router cache | 1-hour TTL free-model catalog | In-memory, periodic refresh |
| LLM response cache | file-based, keyed by (system_prompt, user_prompt, model, temp) | `.cache/llm/` |
| OAuth2 token cache | in-memory TTL-bounded | OAuth2 module |
| YAML config cache | load_yaml_cached in generator | In-memory, session-scoped |

**Missing metrics** (identified gaps):
- No unified request_id propagation across subsystems
- No cross-system cache hit/miss aggregation
- No model usage per agent across tasks
- No context size tracking per invocation
- No cost aggregation per workflow
- No repeated file read detection
- No memory retrieval volume metrics
- No workflow step success/failure rates
- No HITL approval rate per tier
- No OpenTelemetry correlation across subsystems

### 1.4 Token and Cost Intelligence

**Token recording mechanisms** (from source code analysis):

```
LLM Call Flow:
    provider.chat()
        ↓
        _record_usage() [client.py]
            ↓
            Records: prompt_tokens, completion_tokens, total_tokens, cost, model, timestamp
            ↓
            Writes to: logs/token_usage.jsonl + .cache/token_usage.db
        ↓
        OR fallback to heuristic counting [token_counter.py]
            ↓
            Count: ~4 chars ≈ 1 token
            ↓
            Used when provider doesn't report tokens
```

**Cost tracking flow** (from cost_tracker.py and cost_analytics.py):

```
Cost Tracker (cost_tracker.py):
    → Records to logs/token_usage.jsonl (append-only JSONL)
    → Records to .cache/token_usage.db (SQLite)
    → UsageRecord dataclass: tokens, cost, model, timestamp, task_id (if provided)

Cost Analytics (llm/cost_analytics.py):
    → SQLite-backed aggregation by day/week/month
    → Breakdown by agent/task/model/provider
    → forecast_daily: linear extrapolation
    → budget_status: daily/monthly/remaining
    → import_from_jsonl: migration from legacy cost_log.jsonl
    → _record_exists: dedup logic
    → agent_daily_costs, daily_cost_trend
    → total_records, total_cost, export_to_jsonl
```

**Double counting risks** (identified gaps):
- Same LLM call potentially recorded in both JSONL and SQLite (different stages)
- Heuristic token counts in token_counter.py may double-count or conflict with provider-reported tokens
- ConversationHistoryManager cache_hits/misses not integrated with cost tracking
- No agent/task attribution for many cost records (task_id optional)

### 1.5 Cache Intelligence

**Inventory of all existing caches** (from seven-systems-investigation-report.md and observability-research-report.md):

| Cache # | Key Strategy | TTL | Invalidation | Storage |
|---------|-------------|-----|--------------|---------|
| 1 | LLM response cache: (system_prompt, user_prompt, model, temperature) | Configurable, per-configuration | TTL-based expiry | `.cache/llm/` files |
| 2 | OAuth2 token cache | Bounded TTL | Token expiry/refresh | In-memory Python dict |
| 3 | Model Router free-model catalog | 1-hour from OpCode Zen API or static fallback | Hourly refresh | In-memory |
| 4 | Memory engine auto-vector indexing | When VectorStore configured | Config-dependent | VectorStore |
| 5 | YAML config caching (load_yaml_cached) | Session-scoped | Reload on config change | In-memory |
| 6 | ConversationHistoryManager | Per-agent loop | Session-scoped | In-memory (agent_loop.py) |
| 7 | LLM response cache ( ConversationHistoryManager integration) | Not systematically tracked | Not defined | Not defined |

**Cache hit/miss tracking** (from source code analysis):
- `ConversationHistoryManager` in `agent_loop.py` tracks `cache_hits` and `cache_misses`
- No systematic tracking for LLM response cache (.cache/llm/)
- No systematic tracking for OAuth2 token cache
- No systematic tracking for Model Router free-model catalog
- No systematic tracking for YAML config caching

**Opportunity**: Measure and expose cache metrics without introducing shared cache prematurely.

---

## 2. Proposed Architecture

### 2.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    UNIFIED OBSERVABILITY LAYER                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  +---------------------+    +----------------------+         │
│  |  Execution Context  |→→→|  Metrics Aggregator    |         │
│  |  (request_id,       |    |  (new module:         |         │
│  |   task_id, agent_type)│  |   ai_company.observability)│ │
│  +---------------------+    +----------------------+         │
│           ↑                          ↑                       │
│           │                          │                       │
│  +--------+--------+    +----------+--------+               │
│  |  Subsystems      |→→→|  Standardized   |               │
│  |  (7 systems)     |    |  Span Attributes|               │
│  +-------------------+    +-----------------+               │
│                                                                  │
│  Data flows:                                                     │
│  • request_id/task_id propagation from CEO instruction → all subsystems│
│  • Standardized span attributes across all 7 systems              │
│  • Metrics aggregation into Prometheus-compatible format          │
│  • CEO Dashboard exposure via existing RBAC endpoints             │
│  • Historical analysis via SQLite + JSONL backends                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Components

#### 2.2.1 Execution Context Standardization

**New module**: `ai_company/observability/` — unified execution metadata

```python
# Standard execution metadata propagated across all subsystems
@dataclass
class ExecutionContext:
    request_id: str  # Unique per CEO instruction → task completion
    task_id: str     # Unique per task/dispatch
    agent_type: str  # Executive, Specialist, Department, Company
    correlation_id: Optional[str] = None  # For OTel bridging
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    success: bool = True
    error_type: Optional[str] = None
    tier: Optional[int] = None  # Decision Engine approval tier
```

**Propagation mechanism**:
1. CEO instruction generates `request_id` (UUID)
2. `task_id` derived from dispatch context
3. `agent_type` from company-registry.yaml agent role
4. Propagated via:
   - Message Bus `.opencode/inbox.json`
   - Tool execution `check_tier_rules()` in executor
   - LLM client calls (enhanced `client.py`)
   - Decision Engine classification
   - Workflow Engine instance tracking

#### 2.2.2 Standardized Span Attributes

**Common span attributes emitted by all subsystems**:

| Attribute | Type | Source |
|-----------|------|--------|
| `request_id` | string | Execution Context |
| `task_id` | string | Execution Context |
| `agent_type` | string | Execution Context / company-registry.yaml |
| `tool_name` | string | Executor (when applicable) |
| `tier` | int (0-4) | Decision Engine approval tier |
| `success` | bool | Execution outcome |
| `error_type` | string | Exception type (when applicable) |
| `duration_seconds` | float | Wall-clock timing |
| `cache_hit` | bool | ConversationHistoryManager / LLM response cache |
| `cache_key` | string | When cache applicable |
| `model_name` | string | Model Router / provider |
| `prompt_tokens` | int | LLM call tracking |
| `completion_tokens` | int | LLM call tracking |
| `cost_usd` | float | Cost tracker |

#### 2.2.3 Metrics Aggregator

**New module** `ai_company/observability/metrics_aggregator.py`:

Responsibilities:
1. Collect metrics from all 7 subsystems
2. Standardize and normalize
3. Export to Prometheus-compatible format
4. Store in SQLite for historical analysis
5. Expose to CEO Dashboard via existing RBAC endpoints

**Metrics collected**:

| Metric | Subsystem | Labels |
|--------|-----------|--------|
| `lightspeed_tokens_total` | All | agent_type, model, tier |
| `lightspeed_token_bytes_total` | All | agent_type, model, tier |
| `lightspeed_cache_hits_total` | ConversationHistoryManager, LLM response | cache_type, agent_type |
| `lightspeed_cache_misses_total` | ConversationHistoryManager, LLM response | cache_type, agent_type |
| `lightspeed_tool_executions_total` | Executor | tool_name, tier, success |
| `lightspeed_approval_gate_decisions_total` | Decision Engine | tier, outcome |
| `lightspeed_workflow_steps_total` | Workflow Engine | workflow_name, step, outcome |
| `lightspeed_otel_spans_total` | Telemetry | status, duration |
| `lightspeed_llm_calls_total` | Model Router + Executor | model, agent_type, success |

#### 2.2.4 CEO Dashboard Integration

**Existing RBAC endpoints** (from AGENTS.md §13, §11):

| Endpoint | Key | Purpose |
|----------|-----|---------|
| `GET /health` | DASHBOARD_ADMIN_KEY | Health check |
| Task execution endpoints | DASHBOARD_RUN_KEY | Execute tasks, read KPIs |
| Task approval endpoints | DASHBOARD_APPROVE_KEY | Approve/reject tasks |

**New Dashboard metrics** (exposed via existing endpoints):

```
GET /kpi/context-intelligence
{
  "total_requests_24h": int,
  "average_token_usage_per_request": float,
  "cache_hit_rate": float,        // across all caches
  "cost_today_usd": float,
  "workflow_success_rate": float, // across 9 workflow definitions
  "approval_tier_distribution": {
    "AUTO_APPROVE": int,
    "NOTIFY": int,
    "SINGLE_APPROVER": int,
    "TWO_PERSON": int,
    "CEO_ONLY": int
  },
  "active_workflows": int,
  "open_telemetry_enabled": bool
}
```

### 2.3 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION CONTEXT FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CEO Instruction                                                   │
│       │                                                            │
│       ▼                                                            │
│  request_id + task_id generation                                  │
│       │                                                            │
│   ┌─────────────────────┐  ┌───────────────────────┐            │
│   │ Message Bus (.inbox)│  │ Decision Engine       │            │
│   └─────────────────────┘  └───────────────────────┘            │
│            │                      │                       │
│            ▼                      ▼                       │
│   task_id, agent_type   ────→   5-tier approval matrix     │
│            │                      │                       │
│            ▼                      ▼                       │
│   Propagated to:           Propagated to:               │
│   • Executor (tool       • Workflow Engine              │
│     execution)            • 9 workflow definitions       │
│   • Model Router          • Agent type determination   │
│   • LLM Client            • HITL gate check            │
│                                 │                       │
│   ┌─────────────────────┐   ┌─────────────────────┐      │
│   │ Executor (7 tools)  │   │ Model Router      │      │
│   │ • check_tier_rules()│   │ • 5-layer routing │      │
│   │ • tool_runner       │   │ • provider/model  │      │
│   │ • HITL gate         │   │ resolution        │      │
│   └───────┬─────────────┘   └───────┬─────────────┘      │
│           │                       │                    │
│   ▼                   ┌───────────────┼────────────────┘      │
│   Tool execution                       │                    │
│   ▼                                   ▼                    │
│   Output sanitization              LLM call (provider.chat())│
│   ▼                                   │                      │
│   ▼                         ▼───────► _record_usage()     │
│   ▼                                   │ (cost_tokens,       │
│   Dead-letter logging               cost, model,       │
│                                   timestamp)          │
│                                   │                      │
│   ▼                                   ▼                    │
│   ▼                         Execution Context        │
│   ▼                                   │ (request_id,       │
│   ▼                         task_id, agent_type)   │
│   ▼                                   │      stored in      │
│   ┌─────────────────────┐           span attributes   │
│   │ Telemetry (OTel)    │──────────────────────────────┘
│   │ • init_tracing()    │
│   │ • start_span()      │
│   │ • Console exporter  │
│   │ • InMemory exporter │
│   └─────────────────────┘
│                                 │
│   ▼                                   ▼
│   ┌─────────────────────┐  ┌─────────────────────┐
│   │ Metrics Aggregator  │  │ CEO Dashboard       │
│   │ (new module)        │  │ • /kpi/* endpoints  │
│   │ • Collects from     │  │ • /health           │
│   │   all 7 subsystems  │  │ • /kpi/context-int  │
│   │ • Standardizes      │  └─────────────────────┘
│   │ • Exports Prometheus│
│   │ • Stores SQLite     │
│   └─────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Storage Strategy

**Storage backends** (existing + new, no new infrastructure):

| Data Type | Storage | Format | Retention |
|-----------|---------|--------|-----------|
| Token usage per call | `.cache/token_usage.db` (SQLite) | Existing | Permanent |
| JSONL token logs | `logs/token_usage.jsonl` | Existing | Permanent |
| Prometheus metrics | In-memory + HTTP endpoint | New module | Session-scoped + reload |
| Historical analysis | SQLite (expanded) | New tables | Configurable |
| Span storage | In-memory (OTel) or console | Existing | Session-scoped |
| Cache metrics | In-memory (aggregator) | New module | Session-scoped |
| Dashboard KPI data | SQLite queries | New queries | Configurable |

**No new file formats or storage systems introduced**. All existing storage is reused/extended.

### 2.5 Security and Governance Considerations

**Five-tier approval matrix** (Decision Engine, from seven-systems-investigation-report.md):
- AUTO_APPROVE=0: Full automation — all metrics accessible
- NOTIFY=1: Notify only — metrics visible but approval may be required
- SINGLE_APPROVER=2: One approver required — metrics gated per-tier
- TWO_PERSON=3: Two approvers required — metrics require quorum
- CEO_ONLY=4: CEO approval required — all metric changes require CEO key

**Security rules** (from AGENTS.md):
- **NEVER commit `.env` to git** (it is gitignored) — keys in env files
- **Dashboard RBAC keys** (priority order):
  - `DASHBOARD_ADMIN_KEY` — full access (also accepts `DASHBOARD_API_KEY` as alias)
  - `DASHBOARD_APPROVE_KEY` — approve/reject tasks
  - `DASHBOARD_RUN_KEY` — execute tasks, read KPIs
  - `DASHBOARD_API_KEY` — legacy single-key mode (admin alias)
- **LLM Provider keys**:
  - `OPENCODE_API_KEY` — primary (Big Pickle)
  - `GEMINI_API_KEY` — fallback (gemini-3.5-flash)
  - Optional: `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `MIMO_API_KEY`
- **Tool vocabulary**: Only canonical 7 tools (read, edit, grep, list, bash, webfetch, task)
- **No new data transmission** to third-party hosts (per §9.2 Skill Third-Party Transmission Ban)
- **Audit evidence separation** ( §9.3): Auditor's read set and write set must be disjoint

**Governance**:
- All metric changes require appropriate RBAC key
- Audit log appended to `docs/governance-audit.md` for CEO override commits
- Pre-commit hook validates root config changes (AGENTS.md, opencode.json)
- Key rotation every 90 days scheduled, immediately on compromise

---

## 3. Integration Points

### 3.1 Existing Infrastructure Integration

| Integration Point | Source Component | Action |
|------------------|------------------|--------|
| `request_id` generation | CEO instruction → Message Bus | Add to inbox.json payload |
| `task_id` propagation | Message Bus → all subsystems | Standardize as first-class field |
| `agent_type` determination | company-registry.yaml agent role | Read at task dispatch |
| `check_tier_rules()` | Executor tool_runner | Add execution context propagation |
| `_record_usage()` | LLM client.py | Add request_id, task_id, agent_type |
| `cache_hits/misses` | ConversationHistoryManager agent_loop.py | Expose via aggregator |
| OpenTelemetry tracing | tracer.py, bridge.py, exporter.py | Add standardized span attributes |
| Prometheus metrics | evidence_metrics.py | Extend with new metrics |
| CEO Dashboard endpoints | src/ai_company/dashboard/app.py | Add /kpi/* routes |
| Pre-commit hooks | .pre-commit-config.yaml | No changes (read-only design) |

### 3.2 Data Flow Integration Points

```
1. CEO Instruction → request_id generation (UUID)
   ↓
2. task_id derived from dispatch context
   ↓
3. agent_type from company-registry.yaml
   ↓
4. ExecutionContext created and propagated:
   - .opencode/inbox.json (Message Bus)
   - Executor check_tier_rules() validation
   - LLM client _record_usage() enhancement
   - Decision Engine classification
   - Workflow Engine instance tracking
   ↓
5. All subsystems emit standardized span attributes
   ↓
6. Metrics Aggregator collects from all subsystems
   ↓
7. Prometheus metrics endpoint (in-memory)
   ↓
8. CEO Dashboard /kpi/* endpoints query aggregator
   ↓
9. Historical analysis via SQLite (existing .cache/token_usage.db)
   ↓
10. Audit trail via governance-audit.md (CEO override logs)
```

### 3.3 Storage Integration

**Existing storage reuse** (no new files):

| Existing Path | New Use |
|--------------|---------|
| `logs/token_usage.jsonl` | Append execution context (request_id, task_id, agent_type) alongside existing fields |
| `.cache/token_usage.db` (SQLite) | Add execution_context table: request_id, task_id, agent_type, tier, timestamps, success, error_type |
| `src/ai_company/telemetry/` | Enhance tracer.py/bridge.py/exporter.py with standardized span attributes |
| `monitoring/evidence_metrics.py` | Extend with lightspeed_* metrics |
| `src/ai_company/executor/agent_loop.py` | Enhance ConversationHistoryManager with cross-system cache metadata |
| `src/ai_company/llm/cost_analytics.py` | Extend aggregation by agent_type, task_id |

**New tables in existing SQLite** (expansion, not replacement):

```sql
CREATE TABLE IF NOT EXISTS execution_context (
    request_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    agent_type TEXT NOT NULL,
    tier INTEGER,  -- Decision Engine tier 0-4
    start_time REAL NOT NULL,
    end_time REAL,
    success BOOLEAN NOT NULL DEFAULT 1,
    error_type TEXT,
    tool_name TEXT,
    model_name TEXT,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    cost_usd REAL,
    cache_hit BOOLEAN,
    cache_key TEXT,
    workflow_name TEXT,
    FOREIGN KEY (request_id) REFERENCES request_registry(request_id),
    FOREIGN KEY (task_id) REFERENCES task_registry(task_id)
);
```

### 3.4 CEO Dashboard Integration Points

**Existing endpoints enhanced**:

```
GET /health
  → Adds: otel_enabled, active_workflows, cache_hit_rate, cost_today_usd

GET /kpi/context-intelligence
  → New response fields:
   - total_requests_24h
   - average_token_usage_per_request
   - cache_hit_rate (aggregated across all caches)
   - cost_today_usd
   - workflow_success_rate (across 9 definitions)
   - approval_tier_distribution (AUTO_APPROVE through CEO_ONLY)
   - active_workflows
   - otel_enabled

POST /tasks/{id}/approve
  → Validates DASHBOARD_APPROVE_KEY
  → Records approval in execution_context SQLite table
  → Updates approval_tier distribution metrics
```

---

## 4. Component Responsibilities

| Component | Responsibility | Existing or New |
|-----------|---------------|-----------------|
| **ExecutionContext** | Standard metadata (request_id, task_id, agent_type, correlation_id) | New dataclass |
| **MetricsAggregator** | Collect, standardize, export metrics from all 7 subsystems | New module |
| **SpanAttributeStandardizer** | Ensure all subsystems emit common span attributes | New utility |
| **ExecutionContextPropagator** | Propagate request_id/task_id/agent_type across subsystems | New module/wrapper |
| **ConversationHistoryManager Enhancer** | Add cross-system cache metadata exposure | Existing + extension |
| **CostTracker Enhancer** | Add agent_type, task_id attribution to cost records | Existing + extension |
| **ToolRunner Enhancer** | Propagate execution context through check_tier_rules() | Existing + extension |
| **Telemetry Bridge Enhancer** | Add standardized span attributes when OTel enabled | Existing + extension |
| **CEO Dashboard Presenter** | /kpi/* endpoints querying aggregator | Existing + extension |
| **Governance Auditor** | Audit evidence separation, CEO override logging | Existing (read-only) |

---

## 5. Data Flows

### 5.1 Request Flow (CEO Instruction → Task Completion)

```
1. CEO Instruction
   ↓
2. request_id = uuid4() generated at dispatch
   ↓
3. task_id = derive_from_dispatch_context()
   ↓
4. agent_type = from company-registry.yaml role
   ↓
5. ExecutionContext = {request_id, task_id, agent_type, start_time}
   ↓
6. Propagate to:
   - .opencode/inbox.json
   - Executor (check_tier_rules())
   - Model Router (5-layer routing)
   - LLM Client (_record_usage())
   - Decision Engine (approval matrix)
   - Workflow Engine (instance tracking)
   ↓
7. All subsystems emit standardized span attributes
   ↓
8. Tool execution (7 canonical tools via subprocess)
   ↓
9. Output sanitization (PII/content safety)
   ↓
10. Dead-letter logging (on failure)
    ↓
11. ExecutionContext.end_time = time.time()
    ↓
12. Success/failure recorded in execution_context SQLite
    ↓
13. Metrics Aggregator collects all metrics
    ↓
14. CEO Dashboard /kpi/* endpoints query data
    ↓
15. Historical analysis via SQLite
```

### 5.2 Cache Flow

```
1. ConversationHistoryManager cache check
   ↓
2. cache_hits incremented OR cache_misses incremented
   ↓
3. LLM response cache (.cache/llm/) check
   ↓
4. cache hit → return cached response
   ↓
5. cache miss → provider.chat() → _record_usage()
   ↓
6. _record_usage() records with execution_context
   ↓
7. Metrics Aggregator: cache_hits_total++, cache_misses_total++
   ↓
8. CEO Dashboard: cache_hit_rate = hits / (hits + misses)
```

### 5.3 Cost Flow

```
1. LLM call via provider.chat()
   ↓
2. _record_usage() records:
   - prompt_tokens, completion_tokens, total_tokens
   - cost, model, timestamp
   - (enhanced: request_id, task_id, agent_type)
   ↓
3. Written to:
   - logs/token_usage.jsonl (append)
   - .cache/token_usage.db (SQLite upsert)
   ↓
4. Cost analytics aggregation:
   - By day/week/month
   - By agent/task/model/provider
   - Forecast daily (linear extrapolation)
   - Budget status (daily/monthly/remaining)
   ↓
5. Metrics Aggregator collects cost metrics
   ↓
6. CEO Dashboard: cost_today_usd, cost trends
```

---

## 6. Security and Governance Considerations

### 6.1 Five-Tier Approval Matrix Integration

All metric changes and dashboard access governed by Decision Engine's 5-tier approval:

| Tier | Value | Dashboard Access |
|------|-------|------------------|
| AUTO_APPROVE | 0 | Full metrics access (no approval required) |
| NOTIFY | 1 | Metrics visible, some actions require notification |
| SINGLE_APPROVER | 2 | Metrics access requires single approver |
| TWO_PERSON | 3 | Metrics access requires two-person approval |
| CEO_ONLY | 4 | All metric changes require CEO key |

**Implementation**: Dashboard RBAC keys checked on every `/kpi/*` endpoint access.

### 6.2 RBAC Key Hierarchy (AGENTS.md §11)

```
DASHBOARD_ADMIN_KEY (full access, also accepts DASHBOARD_API_KEY as alias)
    ↓
DASHBOARD_APPROVE_KEY (approve/reject tasks)
    ↓
DASHBOARD_RUN_KEY (execute tasks, read KPIs)
    ↓
DASHBOARD_API_KEY (legacy single-key mode, admin alias)
```

**New endpoint key requirements**:

| Endpoint | Minimum Key |
|----------|-------------|
| `GET /health` | DASHBOARD_ADMIN_KEY or DASHBOARD_API_KEY |
| `GET /kpi/context-intelligence` | DASHBOARD_RUN_KEY |
| `POST /tasks/{id}/approve` | DASHBOARD_APPROVE_KEY |
| `POST /tasks/{id}/execute` | DASHBOARD_RUN_KEY |

### 6.3 Audit Evidence Separation (AGENTS.md §9.3)

**Read set** (evidence consumed by observability design):
- `reports/seven-systems-investigation-report.md`
- `reports/observability-research-report.md`
- `reports/context-intelligence-investigation-report.md`
- Source files: history_manager.py, token_counter.py, cost_tracker.py, tool_runner.py, prompts.py, optimized_prompts.py, context.py, tracer.py, bridge.py, exporter.py, cost_analytics.py
- `company-registry.yaml`, `company/models.yaml`
- `AGENTS.md` (root config)

**Write set** (output of design, outside evidence):
- `reports/context-observability-architecture.md` (this file)
- `reports/context-observability-gap-analysis.md`
- `reports/context-observability-implementation-roadmap.md`
- Any new code in `ai_company/observability/` (read-only design constraint — no source modification)

**Disjoint requirement**: Auditor's read set and write set must be disjoint. This design report is the output; no files inside the evidence directory are modified.

### 6.3 Key Rotation and Key Governance

- Keys rotated every 90 days (scheduled)
- Immediately on suspected compromise
- When team members with access leave
- After any security incident
- Dashboard RBAC keys: DASHBOARD_ADMIN_KEY, DASHBOARD_APPROVE_KEY, DASHBOARD_RUN_KEY, DASHBOARD_API_KEY
- LLM Provider keys: OPENCODE_API_KEY, GEMINI_API_KEY, optional DEEPSEEK/KIMI/OPENAI/ANTHROPIC/MIMO
- NEVER commit `.env` to git (gitignored)
- Verification: `uv run python -c "from dotenv import load_dotenv; load_dotenv(); from ai_company.security.rbac import verify_keys; verify_keys()"`

### 6.4 Pre-commit Hook Governance (read-only constraint)

- Pre-commit hook validates root config changes (AGENTS.md, opencode.json)
- Requires `[CEO-OVERRIDE: <OPERATIONAL REASON>]` tag
- Blocks commit without tag
- Appends audit entry to `docs/governance-audit.md` if tag present
- **This design is READ ONLY** — no source code modifications, no pre-commit hook changes

---

## 7. Summary

The proposed architecture delivers:

1. **Standardized execution metadata** (request_id, task_id, agent_type) propagated across all 7 subsystems
2. **Unified metrics aggregation** from all systems into Prometheus-compatible format
3. **CEO Dashboard integration** via existing RBAC endpoints with new `/kpi/*` fields
4. **Historical analysis** via expanded SQLite (existing `.cache/token_usage.db`)
5. **Security and governance** preserved through five-tier approval matrix and Dashboard RBAC keys
6. **No new infrastructure** — reuses existing storage (SQLite, JSONL, in-memory) and existing RBAC
7. **Read-only design** — no source code, configuration, or dependency modifications

The smallest viable implementation requires:
- New `ai_company/observability/` module (ExecutionContext, MetricsAggregator, SpanAttributeStandardizer)
- Enhancements to 5 existing components (ConversationHistoryManager, CostTracker, ToolRunner, Telemetry bridge, Cost analytics)
- No new storage systems (reuse existing SQLite, JSONL, in-memory)
- CEO Dashboard enhancements via existing endpoint architecture

---
*Architecture design generated from comprehensive analysis of seven-systems-investigation-report.md, observability-research-report.md, and context-intelligence-investigation-report.md plus all key source code files.*
