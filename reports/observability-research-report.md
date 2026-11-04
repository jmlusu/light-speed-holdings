# LightSpeed Observability Research Report

**Date**: 2026-11-03
**Project**: `C:\Users\jmlus\light-speed-holdings\.worktrees\silent-knight`
**Evidence Source**: Source code analysis across seven core LightSpeed systems

---

## Executive Summary

This report presents a comprehensive investigation of LightSpeed's observability, telemetry, and metrics infrastructure across seven core systems. The research examined token counting, execution observability, OpenTelemetry integration, evidence store metrics, cache mechanisms, and identified significant gaps in unified cross-system observability.

**Key Finding**: While individual systems have robust per-system tracking, there is **no unified cross-system observability layer** that aggregates metrics across Memory, Decision, Workflow, Model Router, Executor, Graph, and Cache engines into a single coherent view.

---

## 1. Token Counting and Cost Tracking

### Implementation

| Component | File | Key Features |
|-----------|------|-------------|
| **Heuristic Token Counter** | `ai_company/llm/token_counter.py` | Heuristic counting based on character ratio (4 chars ≈ 1 token); used when provider doesn't report token usage |
| **Cost Tracker** | `ai_company/llm/cost_tracker.py` | Records token usage to: (1) JSONL file (`logs/token_usage.jsonl`), (2) SQLite database (`.cache/token_usage.db`); tracks prompt/completion tokens, cost, model, timestamp |
| **LLMClient Usage Recording** | `ai_company/llm/client.py` | `_record_usage()` method records: provider-reported token counts OR heuristic counts as fallback; provider latency; cost calculation |
| **Conversation History Manager** | `ai_company/executor/agent_loop.py` | `cache_hits`, `cache_misses`, `tool_call_count`, `consecutive_failures`, `total_summarizations`; estimated token budget enforcement |

### Token Budget Enforcement (agent_loop.py)

```python
# Token budget check before tool execution
if self._estimate_token_usage() > self.config.max_tokens:
    # Trigger summarization or reject
```

### Cost Tracking Flow

```
LLM Call → provider.chat() → _record_usage()
    ↓
Records: prompt_tokens, completion_tokens, total_tokens, cost, model, timestamp
    ↓
Writes to: logs/token_usage.jsonl + .cache/token_usage.db
```

### Evidence
- `src/ai_company/llm/token_counter.py` — heuristic counting implementation
- `src/ai_company/llm/cost_tracker.py` — JSONL + SQLite storage
- `src/ai_company/llm/client.py` — `_record_usage()` method
- `src/ai_company/executor/agent_loop.py` — `ConversationHistoryManager` with cache tracking

---

## 2. Execution Observability

### ToolRunner Instrumentation

| Metric | Source | Description |
|--------|--------|-------------|
| **Tool execution logs** | `executor/tool_runner.py` | Logs: tool name, tier, status, errors, request_id, SLA timeout |
| **HITL gate integration** | Decision engine | Records approval decisions with request_id tracking |
| **Security logging** | Executor | Logs rejected commands, PII detection, command allowlist violations |
| **Dead-letter logging** | Executor | Failed executions logged for post-mortem analysis |
| **Experiment metrics** | `ai_company/experiment/` | `ExperimentMetrics` dataclass: request_id, task_id, agent_type, tool_usage, duration, success, error_type |

### Agent Loop Observability

| Metric | Component | Description |
|--------|-----------|-------------|
| `cache_hits` | `ConversationHistoryManager` | Number of cache hits |
| `cache_misses` | `ConversationHistoryManager` | Number of cache misses |
| `tool_call_count` | `ConversationHistoryManager` | Total tool calls made |
| `consecutive_failures` | `ConversationHistoryManager` | Count of consecutive failed tool executions |
| `total_summarizations` | `ConversationHistoryManager` | Total summarizations performed |

### Experiment Metrics

```python
@dataclass
class ExperimentMetrics:
    request_id: str
    task_id: str
    agent_type: str
    tool_usage: Dict[str, int]
    duration_seconds: float
    success: bool
    error_type: Optional[str]
```

### Evidence
- `src/ai_company/executor/tool_runner.py` — tool execution logging
- `src/ai_company/executor/agent_loop.py` — `ConversationHistoryManager` metrics
- `src/ai_company/experiment/` — `ExperimentMetrics` dataclass

---

## 3. OpenTelemetry Telemetry Integration

### Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| **Environment variable** | `AI_COMPANY_OTEL=1` | Enables OpenTelemetry |
| **Console exporter** | Always active | Prints spans to stdout |
| **In-memory exporter** | When OTel not fully configured | Stores spans in memory for later export |
| **Correlation ID bridge** | `ai_company/telemetry/` | Maps correlation_id ↔ OpenTelemetry context |

### Tracer Infrastructure

```
OpenTelemetry tracer → NoOp fallback when OTel disabled
    ↓
Console span export (always active)
    ↓
In-memory span store (fallback when OTel not configured)
    ↓
Correlation ID ↔ OTel context bridge
```

### Span Attributes

Key span attributes recorded:
- `request_id`
- `agent_type`
- `tool_name` (when applicable)
- `tier` (Decision Engine approval tier)
- `duration_seconds`
- `success` / `error_type`
- `cache_hit` (when applicable)

### Evidence
- `src/ai_company/telemetry/` — OpenTelemetry integration
- Correlation ID ↔ OTel context bridging code

---

## 4. Evidence Store Metrics (Prometheus)

### Implementation

| Metric Type | File | Description |
|-------------|------|-------------|
| **Evidence store size** | `monitoring/evidence_metrics.py` | Gauge: current evidence store size |
| **Evidence events** | `monitoring/evidence_metrics.py` | Counter: total evidence events processed |
| **Evidence rotation** | `monitoring/evidence_metrics.py` | Counter: evidence rotations performed |
| **Time-series metrics** | Prometheus format | Exportable for monitoring dashboards |

### Metrics Available

```python
# Prometheus metrics from monitoring/evidence_metrics.py
EVIDENCE_STORE_SIZE  # gauge
EVIDENCE_EVENTS_TOTAL  # counter
EVIDENCE_ROTATIONS_TOTAL  # counter
```

### Evidence
- `src/ai_company/monitoring/evidence_metrics.py` — Prometheus metrics implementation

---

## 5. Cache Mechanisms Tracking

### Per-System Cache Tracking

| Cache Type | Tracking Location | Tracked Metrics |
|------------|------------------|-----------------|
| **ConversationHistoryManager** | `agent_loop.py` | `cache_hits`, `cache_misses` |
| **Model Router free-model catalog** | `model_router/` | 1-hour TTL, refresh status |
| **LLM response file cache** | `.cache/llm/` | Hit/miss rates (not systematically tracked) |
| **OAuth2 token cache** | OAuth2 module | Token expiry, refresh count |
| **YAML config caching** | `generator/load_yaml_cached` | Cache hit ratio (not exposed) |

### ConversationHistoryManager Metrics

```python
# From agent_loop.py
self.cache_hits: int = 0
self.cache_misses: int = 0
```

### Evidence
- `src/ai_company/executor/agent_loop.py` — ConversationHistoryManager cache tracking
- `src/ai_company/monitoring/evidence_metrics.py` — Prometheus evidence store metrics
- `src/ai_company/model_router/` — free-model catalog cache

---

## 6. Gaps in Unified Cross-System Observability

### Missing Metrics

| Gap | Impact |
|-----|--------|
| **No unified token usage aggregation** | Cannot track total token consumption across all agents/workflows |
| **No cross-system cache hit/miss rates** | Cannot compare cache effectiveness across LLM response, OAuth2, YAML config mechanisms |
| **No model usage per agent across tasks** | Cannot answer: "Which agents use which models most?" |
| **No context size tracking per invocation** | No way to know estimated context usage per task execution |
| **No cost aggregation per workflow** | Cannot compute total cost of a multi-step workflow |
| **No repeated file read detection** | No metric for "how many times was this file read across all agents?" |
| **No memory retrieval volume metrics** | Cannot track how many memories are recalled per task |
| **No workflow step success/failure rates** | Cannot assess workflow health across all 9 definitions |
| **No HITL approval rate per tier** | Cannot assess approval matrix effectiveness in production |
| **No OpenTelemetry correlation across subsystems** | OTel spans are siloed per-system, not unified |

### Architectural Limitations

1. **Siloed Metrics**: Each system tracks its own metrics independently
2. **No Central Metrics Aggregator**: No component collects and aggregates metrics from all seven systems
3. **Inconsistent Naming**: Different naming conventions for similar metrics across systems
4. **No Standard Metadata**: No common set of attributes (request_id, task_id, agent_type) across all systems
5. **No Export Format Standardization**: Metrics exported in different formats (JSONL, SQLite, Prometheus, in-memory)

### Evidence
- Cross-system analysis identifying all gaps above
- Comparison of per-system tracking capabilities
- Analysis of existing vs. missing metrics

---

## 7. Recommended Observability Enhancements

### Short-Term (1-2 weeks)

1. **Unified Request Context**
   - Add `request_id` and `task_id` as mandatory attributes to all tool executions
   - Propagate correlation IDs across subsystem boundaries

2. **Standard Metadata Injection**
   - Add `agent_type`, `tool_name`, `tier` as standard span attributes
   - Ensure all subsystems emit these attributes

3. **Token Usage Standardization**
   - Ensure all LLM calls record: prompt_tokens, completion_tokens, cost
   - Standardize on JSONL + SQLite storage pattern

4. **ConversationHistoryManager Export**
   - Expose cache_hit_rate = cache_hits / (cache_hits + cache_misses)
   - Add to Prometheus metrics endpoint

### Medium-Term (1 month)

5. **Unified Metrics Aggregator**
   - Create new module `ai_company/observability/` that collects metrics from all subsystems
   - Exports Prometheus-compatible metrics with standardized labels

6. **Cross-System Token Tracking**
   - Aggregate token usage across all LLM calls
   - Add cost tracking per task/workflow

7. **HITL Approval Metrics**
   - Track approval rates per tier (AUTO_APPROVE through CEO_ONLY)
   - Monitor approval gate effectiveness over time

### Long-Term (2-3 months)

8. **OpenTelemetry Auto-Instrumentation**
   - Auto-create spans for cross-system operations
   - Correlation ID propagation from CEO instruction through executor → all downstream systems

9. **Dashboard-Ready Metrics**
   - Pre-computed metrics for common queries:
     - "Token usage per agent per day"
     - "Cache effectiveness by type"
     - "Workflow success rates"
     - "Cost per task type"

10. **Experiment Metrics Integration**
    - Link `ExperimentMetrics` to the unified observability layer
    - Enable post-experiment analysis across all seven systems

---

## 8. Current Observability Stack Summary

```
| Layer | Component | Metrics Type | Coverage |
|-------|-----------|-------------|----------|
| Token | token_counter.py | heuristic counts | LLM calls only |
| Token | cost_tracker.py | JSONL + SQLite | LLM calls only |
| Token | ConversationHistoryManager | cache_hits/misses | Agent loop only |
| Exec | ToolRunner | tool execution logs | 7 canonical tools |
| Exec | agent_loop.py | ConversationHistoryManager metrics | Agent workflow |
| Telemetry | OpenTelemetry | opt-in tracing | Selected subsystems |
| Evidence | evidence_metrics.py | Prometheus metrics | Evidence stores only |
| Cache | ConversationHistoryManager | cache_hits/misses | Agent loop |
| Cache | Model Router | free-model catalog TTL | Model routing |
| Cache | LLM response cache | file-based (untracked) | LLM responses |
| Cache | OAuth2 token | in-memory TTL | API auth |
| Cache | YAML config | load_yaml_cached | Generator |
```

---

## 9. Verification Commands

### Token Tracking
```bash
# Check token usage logs
cat logs/token_usage.jsonl | head -20

# Check SQLite token usage database
python -c "import sqlite3; conn = sqlite3.connect('.cache/token_usage.db'); cursor = conn.execute('SELECT * FROM token_usage'); print(cursor.fetchall())"
```

### Execution Observability
```bash
# Check tool execution logs
grep -r "tool_runner" src/ai_company/executor/ | head -10
```

### OpenTelemetry
```bash
# Enable and check
export AI_COMPANY_OTEL=1
ai-company --help  # Check for OTel-related options
```

### Evidence Metrics
```bash
# Check Prometheus metrics
python -c "from ai_company.monitoring.evidence_metrics import EvidenceMetrics; m = EvidenceMetrics(); print(m)"
```

### Conversation History Metrics
```bash
# Check cache hit/miss rates
python -c "from ai_company.executor.agent_loop import ConversationHistoryManager; mgr = ConversationHistoryManager(); print(f'hits: {mgr.cache_hits}, misses: {mgr.cache_misses}')"
```

---

## 10. Key Conclusions

1. **Robust Per-System Tracking**: Each of the seven systems has decent individual metrics and telemetry, but they operate in silos.

2. **Token Tracking Coverage**: Token usage is tracked for LLM calls (via cost_tracker) and estimated within the agent loop, but there's no aggregation across all agents or workflows.

3. **OpenTelemetry is Opt-In**: The OpenTelemetry integration requires `AI_COMPANY_OTEL=1` and currently provides limited, siloed tracing rather than unified cross-system observability.

4. **Evidence Store Metrics are Specialized**: Prometheus metrics exist only for evidence stores, not for the other six systems.

5. **ConversationHistoryManager provides the most unified agent-loop metrics** with cache_hits, cache_misses, tool_call_count, and consecutive_failures — but these are agent-loop-specific, not cross-system.

6. **The largest gap is the absence of a unified observability layer** that can aggregate metrics from all seven systems into a single coherent view with standardized metadata (request_id, task_id, agent_type).

7. **Recommended next step**: Create a unified `ai_company/observability/` module that collects, standardizes, and exports metrics from all subsystems, starting with request_id propagation and token usage aggregation.

---
*Research report generated from comprehensive analysis of LightSpeed observability, telemetry, and metrics infrastructure across seven core systems.*
