# Context Intelligence & Execution Observability Gap Analysis

**Date**: 2026-11-03
**Project**: `C:\Users\jmlus\light-speed-holdings\.worktrees\silent-knight`
**Status**: Design deliverable (READ ONLY — no source code modified)

---

## 1. Existing Capabilities

### 1.1 Token Tracking (Per-System, Siloed)

| Capability | System | Evidence |
|-----------|--------|----------|
| Heuristic token counting | `token_counter.py` | ~4 chars ≈ 1 token; fallback when provider doesn't report |
| Provider-reported token recording | `cost_tracker.py` | JSONL (`logs/token_usage.jsonl`) + SQLite (`.cache/token_usage.db`) |
| Per-call token tracking | `LLMClient._record_usage()` | prompt_tokens, completion_tokens, total_tokens, cost, model, timestamp |
| Token budget enforcement | `agent_loop.py` ConversationHistoryManager | `_estimate_token_usage()` > `max_tokens` check |
| Daily/weekly/monthly cost aggregation | `llm/cost_analytics.py` | SQLite-backed: agent_daily_costs, daily_cost_trend, total_records, total_cost |
| Forecasting | `llm/cost_analytics.py` | `forecast_daily`: linear extrapolation |
| Budget status | `llm/cost_analytics.py` | `budget_status`: daily/monthly/remaining |

### 1.2 Execution Observability (Per-System, Siloed)

| Capability | System | Evidence |
|-----------|--------|----------|
| Tool execution logging | `executor/tool_runner.py` | Tool name, tier, status, errors, request_id, SLA timeout (120s) |
| HITL gate integration | Decision Engine | Approval decisions with request_id tracking |
| Security logging | Executor | Rejected commands, PII detection, command allowlist violations |
| Dead-letter logging | Executor | Failed executions for post-mortem analysis |
| ConversationHistoryManager metrics | `agent_loop.py` | cache_hits, cache_misses, tool_call_count, consecutive_failures, total_summarizations |
| OpenTelemetry tracing | `telemetry/tracer.py`, `bridge.py`, `exporter.py` | opt-in via AI_COMPANY_OTEL=1; console/in-memory/exporters; NoOp fallback |
| Correlation ID ↔ OTel bridging | `telemetry/bridge.py` | set_correlation_id_from_task(), _hash_to_trace_id/_hash_to_span_id (SHA-256), subtask_context() |
| Evidence store metrics | `monitoring/evidence_metrics.py` | Prometheus: EVIDENCE_STORE_SIZE (gauge), EVIDENCE_EVENTS_TOTAL (counter), EVIDENCE_ROTATIONS_TOTAL (counter) |

### 1.3 Cache Tracking (Per-System, Siloed)

| Capability | System | Evidence |
|-----------|--------|----------|
| ConversationHistoryManager cache_hits/misses | `agent_loop.py` | `self.cache_hits: int = 0`, `self.cache_misses: int = 0` |
| Model Router free-model catalog | `model_router/` | 1-hour TTL from OpCode Zen API or static fallback |
| LLM response file cache | `.cache/llm/` | Keyed by (system_prompt, user_prompt, model, temperature); TTL configurable |
| OAuth2 token cache | OAuth2 module | In-memory TTL-bounded token cache |
| YAML config caching | Generator `load_yaml_cached` | In-memory, session-scoped; caches company-registry.yaml, company/models.yaml |

### 1.4 Context Intelligence (Per-Agent, Siloed)

| Capability | System | Evidence |
|-----------|--------|----------|
| AgentContext parsing | `executor/context.py` | From .md spec cards, YAML frontmatter, shared standards doc referencing |
| _derive_tools from permission block | `executor/context.py` | Permission string derivation |
| parse_agent_spec_content | `executor/context.py` | Shared standards resolution |
| Token-optimized prompt building | `executor/optimized_prompts.py` | Conditional section loading based on task type (refactor/architecture/debug/complex) |
| Dynamic few-shot from memories | `executor/optimized_prompts.py` | Task-type detection via keyword matching |
| build_optimized_system_prompt | `executor/optimized_prompts.py` | Dynamic section loading, token budget enforcement (~len//4) |
| build_optimized_user_prompt | `executor/optimized_prompts.py` | Token-optimized prompt builder |
| estimate_prompt_tokens | `executor/optimized_prompts.py` | Using token_counter (~4 chars/token) |
| Token budget enforcement | `executor/optimized_prompts.py` | ~len//4 threshold |
| build_system_prompt_typed | `prompts.py` | Typed role prefixes, tool instructions per agent type, response formats, memory context injection |

---

## 2. Missing Capabilities

### 2.1 Unified Cross-System Metrics (COMPLETE GAP)

| Missing Capability | Impact | Evidence of Gap |
|-------------------|--------|-----------------|
| No unified request_id propagation across all 7 systems | Cannot correlate events across subsystems | bridge.py correlation ID ↔ OTel bridging only active when OTel enabled (AI_COMPANY_OTEL=1); not systematic |
| No cross-system cache hit/miss aggregation | Cannot compare cache effectiveness across LLM response, OAuth2, YAML config, ConversationHistoryManager | Each cache tracked independently; no common metrics format or aggregation |
| No model usage per agent across tasks | Cannot answer "Which agents use which models most?" | Token usage recorded per LLM call but no agent_type attribution; task_id optional |
| No context size tracking per invocation | No way to know estimated context usage per task execution | Token estimates heuristic-only (~4 chars/token); no per-invocation context size tracking |
| No cost aggregation per workflow | Cannot compute total cost of a multi-step workflow | Costs recorded per LLM call; no workflow-level aggregation; 9 workflow definitions have no cost tracking |
| No repeated file read detection | No metric for "how many times was this file read across all agents?" | File reads tracked per-tool (read tool in executor); no cross-agent deduplication |
| No memory retrieval volume metrics | Cannot track how many memories are recalled per task | Memory Engine has recall/search/prune/consolidate but no per-task retrieval volume metric |
| No workflow step success/failure rates | Cannot assess workflow health across all 9 definitions | Workflow Engine has advance/complete_step/cancel/get_status but no success/failure rate tracking per step |
| No HITL approval rate per tier | Cannot assess approval matrix effectiveness in production | Decision Engine has 5-tier matrix (AUTO_APPROVE=0 through CEO_ONLY=4) but no approval rate tracking |
| No OpenTelemetry correlation across subsystems when OTel disabled | OTel spans siloed per-system; no unified tracing | bridge.py only active when OTel enabled; NoOp fallback when disabled |

### 2.2 Token and Cost Intelligence Gaps

| Missing Capability | Impact | Evidence of Gap |
|-------------------|--------|-----------------|
| Unified token usage aggregation across all agents/workflows | Cannot track total token consumption LightSpeed-wide | Token tracking: heuristic in token_counter.py, provider-reported in cost_tracker.py; no aggregation layer |
| Distinguish provider-reported vs heuristic vs cache-write tokens | Risk of double counting; cannot accurately attribute costs | cost_tracker.py records provider-reported OR fallback to heuristic; no cache-hit distinction |
| No cost attribution to agents, tasks, and workflows | Cannot compute cost per agent, per task, per workflow | task_id optional in _record_usage(); agent_type not systematically recorded |
| No cache-read vs cache-write token distinction | Double counting risk: cache hits may still incur minimal token costs | No mechanism to distinguish cache hits from cache misses in token recording |
| No daily/per-agent cost breakdown in dashboard | CEO cannot assess agent-level cost efficiency | cost_analytics.py provides aggregation by agent/task/model/provider but not exposed via Dashboard RBAC endpoints |
| No real-time cost budget enforcement | No way to prevent cost overruns during task execution | Budget enforcement in agent_loop.py per-task, but no real-time aggregate or cross-agent view |

### 2.3 Cache Intelligence Gaps

| Missing Capability | Impact | Evidence of Gap |
|-------------------|--------|-----------------|
| Systematic cache hit/miss tracking across all 5 caches | Cannot measure cache effectiveness LightSpeed-wide | Only ConversationHistoryManager tracks cache_hits/misses; other caches (LLM response, OAuth2, Model Router, YAML config) have no systematic tracking |
| Cache key transparency | Cannot debug cache misses or optimize keys | LLM response cache key (system_prompt, user_prompt, model, temp) not exposed; no key logging |
| Cache TTL enforcement verification | Cannot confirm caches are invalidating correctly | TTLs configured but no monitoring; OAuth2 TTL "bounded" but no expiry tracking |
| Cross-cache comparison | Cannot say "LLM response cache has 85% hit rate while OAuth2 has 95%" | Each cache uses different metrics; no common format or aggregation |
| Cache hit rate per agent type | Cannot assess which agent types benefit most from caching | No mechanism to attribute cache hits/misses to agent_type |
| Cache invalidation monitoring | No alerting when caches fail to invalidate | No monitoring of cache invalidation events or failures |

### 2.4 Context Intelligence Gaps

| Missing Capability | Impact | Evidence of Gap |
|-------------------|--------|-----------------|
| Cross-agent context deduplication | Same AGENTS.md, configuration files read repeatedly waste resources | §4 Context Loading rule 1: "Read this file" (AGENTS.md) every task; no caching or reuse across agents |
| Context size estimation per agent type | Cannot predict token budget needs | Token counter heuristic (~4 chars/token) only; no per-agent-type context size profile |
| Context summarisation triggers | No automatic summarisation when context exceeds threshold | agent_loop.py has token budget enforcement but no proactive summarisation |
| Shared standards doc referencing efficiency | `parse_agent_spec_content` reads shared standards each time; no cache | No evidence of caching parsed spec content across invocations |
| Memory context injection effectiveness | No metric for how memories improve prompt quality or token efficiency | Memories injected via prompts.py/optimized_prompts.py but no outcome tracking |
| Prompt optimization effectiveness measurement | No before/after token comparison for optimized vs plain prompts | optimized_prompts.py builds optimized prompts but no metrics on token savings |
| Agent-type context profiles | Cannot say "Executive agents use X tokens, Specialist agents use Y" | No per-agent-type context profiling |

### 2.5 OpenTelemetry and Telemetry Gaps

| Missing Capability | Impact | Evidence of Gap |
|-------------------|--------|-----------------|
| Unified OTel correlation when disabled | No tracing across subsystems when AI_COMPANY_OTEL≠1 | bridge.py only active when OTel enabled; NoOp fallback provides no correlation |
| Standardized span attributes across all subsystems | Inconsistent span data; hard to query across systems | Each subsystem emits different span attributes; no common schema |
| Auto-instrumentation for cross-system operations | Manual span creation required; error-prone | No auto-instrumentation for CEO instruction → task completion flow |
| Real-time dashboards from OTel spans | No aggregation or visualization of OTel data | OTel data stored in-memory or console only; no persistent export for dashboards |
| OTel correlation across task boundaries | Subtask context inheritance not systematic | bridge.py subtask_context() exists but only for OTel-enabled scenarios; not systematic |

### 2.5 CEO Dashboard Gaps

| Missing Capability | Impact | Evidence of Gap |
|-------------------|--------|-----------------|
| /kpi/context-intelligence endpoint | Does not exist; CEO cannot query context intelligence metrics | No such endpoint in src/ai_company/dashboard/app.py |
| Cache hit rate display | CEO cannot see aggregate cache effectiveness | Only ConversationHistoryManager cache_hits/misses visible internally |
| Workflow success rate dashboard | CEO cannot assess 9 workflow definitions health | No workflow success/failure rate exposure |
| Approval tier distribution | CEO cannot see AUTO_APPROVE through CEO_ONLY usage rates | Decision Engine tier data not aggregated for dashboard |
| Real-time cost per task | CEO cannot see cost of individual tasks or workflows | cost_analytics.py provides aggregation but not Dashboard-exposed |
| Cache effectiveness per type | CEO cannot compare LLM cache vs OAuth2 vs YAML config cache | No unified cache metrics endpoint |

---

## 3. Duplicated Functionality

### 3.1 Token Counting Duplication

| Duplicate | Locations | Assessment |
|-----------|-----------|------------|
| Heuristic ~4-chars/token counting | `token_counter.py` (standalone); potentially duplicated in `optimized_prompts.py` `estimate_prompt_tokens()` | Both use same heuristic; no shared module |
| Provider-reported token recording | `cost_tracker.py` `_record_usage()` | Separate from heuristic; no integration |
| Token budget enforcement | `agent_loop.py` ConversationHistoryManager `_estimate_token_usage()` | Different implementation; no shared base |

### 3.2 Cost Recording Duplication

| Duplicate | Locations | Assessment |
|-----------|-----------|------------|
| JSONL token usage logging | `cost_tracker.py` `log_usage()` | Append to `logs/token_usage.jsonl` |
| SQLite token usage storage | `cost_tracker.py` `.cache/token_usage.db` | Same DB, but may have different schema/versions |
| Cost analytics aggregation | `llm/cost_analytics.py` | Reads from same `.cache/token_usage.db`; separate queries/aggregations |
| Legacy cost_log.jsonl migration | `llm/cost_analytics.py` `import_from_jsonl()` | Migration from pre-existing format; dedup with `_record_exists` |

### 3.3 OpenTelemetry Duplication

| Duplicate | Locations | Assessment |
|-----------|-----------|------------|
| Tracer initialization | `telemetry/tracer.py` `init_tracing()` | Stands alone; no import/reuse from other modules |
| Span creation | `telemetry/tracer.py` `start_span()` | Context manager; no shared attribute schema |
| Correlation ID bridging | `telemetry/bridge.py` | Exists but only active when OTel enabled; no fallback when disabled |
| Console exporter | `telemetry/exporter.py` `ConsoleSpanExporter` | Standalone; no shared with in-memory exporter beyond base pattern |
| In-memory exporter | `telemetry/exporter.py` `InMemorySpanExporter` | Standalone test utility; no shared export format |

### 3.4 Cache Duplication

| Duplicate | Locations | Assessment |
|-----------|-----------|------------|
| ConversationHistoryManager cache | `agent_loop.py` | Per-agent loop only; not shared with other systems |
| LLM response file cache | `.cache/llm/` | File-based; no systematic hit/miss tracking |
| OAuth2 token cache | OAuth2 module | In-memory TTL-bounded; no cross-system visibility |
| YAML config caching | Generator `load_yaml_cached` | Session-scoped in-memory; no hit/miss tracking |
| Free-model catalog cache | Model Router | 1-hour TTL; no systematic tracking |

### 3.4 Context Duplication

| Duplicate | Locations | Assessment |
|-----------|-----------|------------|
| AgentContext parsing | `executor/context.py` | Parses .md spec cards; no reuse across invocations |
| System prompt building | `prompts.py` `build_system_prompt_typed()` | Typed roles; no reuse |
| Optimized prompt building | `executor/optimized_prompts.py` | Token-optimized; no shared state with other systems |
| Shared standards resolution | `executor/context.py` `parse_agent_spec_content()` | Read each time; no cache |

---

## 4. Technical Debt

### 4.1 Identified Technical Debt Items

| # | Debt Item | Location | Risk | Remediation |
|---|-----------|----------|------|-------------|
| TD-01 | **Siloed metrics with no aggregation layer** | All 7 systems | High — cannot produce LightSpeed-wide KPIs | Build `ai_company/observability/metrics_aggregator.py` |
| TD-02 | **No unified request_id/task_id propagation** | CEO instruction → all subsystems | Medium — cannot correlate events | Standardize ExecutionContext and propagate via Message Bus |
| TD-03 | **Double counting risk: JSONL + SQLite token recording** | `cost_tracker.py` records to both | Medium — potential inflated cost metrics | Unified recording pattern; dedup logic |
| TD-04 | **Heuristic token counting with no provider override tracking** | `token_counter.py` fallback | Low-Medium — cannot distinguish source of token counts | Enhance _record_usage() to flag heuristic vs provider-reported |
| TD-05 | **No cache hit/miss tracking for 4 of 5 caches** | LLM response, OAuth2, Model Router, YAML config | Medium — cannot measure cache effectiveness | Systematic tracking exposure via aggregator |
| TD-06 | **OpenTelemetry opt-in only, no default tracing** | `AI_COMPANY_OTEL=1` required | Medium — limited observability by default | Make tracing opt-out with NoOp as default; enhanced bridge |
| TD-07 | **ConversationHistoryManager metrics not exposed externally** | `agent_loop.py` internal only | Low — cannot from CEO Dashboard | Expose via metrics aggregator + Dashboard /kpi/* endpoints |
| TD-07 | **Cost analytics not integrated with execution context** | `cost_analytics.py` separate from tool execution | Medium — cannot attribute costs to specific tasks/requests | Add request_id, task_id, agent_type to cost records |
| TD-08 | **No context size estimation per agent type** | No per-type profiling | Low-Medium | Create agent-type context profiles from historical data |
| TD-09 | **Five-tier approval matrix not integrated with dashboard** | Decision Engine metrics not exposed | Medium — CEO cannot assess approval effectiveness |Expose approval tier distribution via /kpi/* endpoints |
| TD-10 | **No workflow step success/failure tracking** | Workflow Engine 9 definitions | Medium — cannot assess workflow health | Add step outcome tracking to execution_context SQLite table |

### 4.2 Debt Priority

**Critical (must fix before deployment)**:
- TD-01: Siloed metrics with no aggregation layer (blocks all KPI generation)
- TD-02: No unified request_id/task_id propagation (blocks correlation)
- TD-03: Double counting risk JSONL + SQLite (blocks accurate cost metrics)

**Important (should fix in Phase 1)**:
- TD-04: Heuristic token counting tracking source
- TD-05: Cache hit/miss tracking for 4 caches
- TD-06: OTel opt-in only → make default
- TD-07: ConversationHistoryManager metrics exposure
- TD-07 (duplicate number, likely TD-08): Cost analytics integration

**Low (nice-to-have)**:
- TD-08: Context size per agent type
- TD-09: Approval tier distribution dashboard
- TD-10: Workflow step success/failure tracking

---

## 5. Prioritized Gaps

### 5.1 Priority 1 (Immediate — 1-2 weeks)
1. **Standardized ExecutionContext** (request_id, task_id, agent_type) propagation across all subsystems
2. **MetricsAggregator module** that collects from all 7 subsystems and exports Prometheus-format metrics
3. **Enhanced _record_usage()** to always record request_id, task_id, agent_type (flag heuristic vs provider-reported)
4. **ConversationHistoryManager cache hit rate exposure** via metrics aggregator

### 5.2 Priority 2 (Short-term — 2-4 weeks)
5. **OpenTelemetry default-on** with NoOp fallback when AI_COMPANY_OTEL not set (currently opt-in only)
6. **Standardized span attributes** across all subsystems (request_id, task_id, agent_type, tier, success, duration)
7. **Cost attribution to agents/tasks** via execution_context SQLite table expansion
8. **CEO Dashboard /kpi/context-intelligence** endpoint with core metrics

### 5.3 Priority 3 (Medium-term — 1-3 months)
9. **Cross-cache hit/miss aggregation** (LLM response, OAuth2, Model Router, YAML config, ConversationHistoryManager)
10. **Agent-type context profiling** (token usage patterns per agent role)
11. **Approval tier distribution dashboard** (AUTO_APPROVE through CEO_ONLY rates)
12. **Workflow step success/failure rates** across 9 definitions

### 5.4 Priority 4 (Long-term — 3-6 months)
13. **Real-time cache invalidation monitoring** with alerting
14. **Predictive cost budget enforcement** during task execution
15. **Auto-instrumentation** for cross-system operations (CEO instruction → task completion spans)
16. **Historical trend analysis** (week/month/year-over-year metric trends)

---

## 6. Duplication and Redundancy Summary

| Area | # of Duplicate Implementations | Assessment |
|------|------------------------------|------------|
| Token counting | 2-3 (token_counter.py, optimized_prompts.py estimate_prompt_tokens, potential cost_tracker fallback) | Same heuristic; no shared module |
| Cost recording | 2 (JSONL + SQLite from cost_tracker.py; analytics from cost_analytics.py reading same DB) | Potential double counting; no unified pattern |
| OpenTelemetry | 3-4 (tracer.py, bridge.py, exporter.py Console, exporter.py InMemory) | Fragmented; no shared attribute schema |
| Cache tracking | 5 (ConversationHistoryManager + 4 others, none systematically tracked) | Each isolated; no common metrics |
| Context building | 2-3 (context.py AgentContext, prompts.py build_system_prompt_typed, optimized_prompts.py build_optimized_system_prompt) | Similar purposes; no sharing |
| Token budget enforcement | 2 (agent_loop.py, optimized_prompts.py) | Different thresholds; no shared base |

**Key insight**: The duplication is not accidental — it reflects the seven-siloed architecture where each system independently solved similar problems. The proposed unified architecture consolidates these into standardized components while preserving existing functionality.

---

## 7. Summary

**Existing strengths** (what works well):
- Token counting heuristic (~4 chars/token) is consistent
- CostTracker provides JSONL + SQLite with analytics
- ConversationHistoryManager has cache_hits/misses tracking
- ToolRunner provides sandboxed execution with tier authorization
- OpenTelemetry opt-in with console/in-memory exporters
- bridge.py provides correlation ID ↔ OTel bridging when enabled
- Decision Engine 5-tier approval matrix is well-defined
- Evidence store Prometheus metrics exist

**Critical gaps** (what's missing):
- No unified cross-system metrics or context
- No systematic request_id/task_id propagation
- No cost attribution to agents/tasks/workflows
- No cache hit/miss tracking for 4 of 5 caches
- OpenTelemetry opt-in only (should be default)
- CEO Dashboard lacks /kpi/context-intelligence endpoint
- Significant duplicated functionality across siloed systems

**Design recommendation**: The smallest viable implementation creates a unified `ai_company/observability/` module that standardizes execution metadata, aggregates metrics from all subsystems, and exposes findings via the existing CEO Dashboard RBAC architecture — without introducing new storage systems or breaking governance.

---
*Gap analysis generated from comprehensive analysis of seven-systems-investigation-report.md, observability-research-report.md, context-intelligence-investigation-report.md, and all key source code files.*
