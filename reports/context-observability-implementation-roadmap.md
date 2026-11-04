# Context Intelligence & Execution Observability Implementation Roadmap

**Date**: 2026-11-03
**Project**: `C:\Users\jmlus\light-speed-holdings\.worktrees\silent-knight`
**Status**: Design deliverable (READ ONLY — no source code modified)

---

## 1. phased Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
**Goal**: Establish standardized execution metadata and basic metrics aggregation

| # | Task | Description | Dependencies | Acceptance Criteria |
|---|------|-------------|-------------|---------------------|
| P1.1 | **Create ExecutionContext dataclass** | New `ai_company/observability/execution_context.py` with `request_id`, `task_id`, `agent_type`, `correlation_id`, `start_time`, `end_time`, `success`, `error_type`, `tier`, `tool_name`, `model_name`, `prompt_tokens`, `completion_tokens`, `cost_usd`, `cache_hit`, `cache_key` | None | Dataclass defined; can be instantiated and serialized to/from JSON |
| P1.2 | **Add request_id to Message Bus** | Enhance `.opencode/inbox.json` payload to include `request_id` and `task_id` at dispatch | None | Task dispatched with request_id and task_id fields; verified via `ai-company inbox list` |
| P1.3 | **Propagate ExecutionContext through Executor** | Enhance `check_tier_rules()` in `tool_runner.py` to accept and propagate ExecutionContext | P1.1, P1.2 | Tool execution logs include request_id, task_id, agent_type; SLA timeout still 120s |
| P1.4 | **Enhance _record_usage() with execution context** | `llm/client.py` `_record_usage()` always records `request_id`, `task_id`, `agent_type`; flags `heuristic_vs_provider_reported` | P1.1 | `logs/token_usage.jsonl` and `.cache/token_usage.db` include new fields; cost_analytics.py reads them |
| P1.5 | **Expose ConversationHistoryManager cache metrics** | Add `cache_hit_rate` property to `ConversationHistoryManager`; export via metrics aggregator | Existing `agent_loop.py` | `cache_hit_rate = cache_hits / (cache_hits + cache_misses)` computed; accessible externally |

**Phase 1 Deliverables**:
- `ai_company/observability/execution_context.py` (new)
- Enhanced `inbox.json` payload format
- Enhanced `tool_runner.py` check_tier_rules() signature
- Enhanced `client.py` _record_usage() with execution context
- ConversationHistoryManager.cache_hit_rate property
- Updated `logs/token_usage.jsonl` schema
- Updated `.cache/token_usage.db` schema (migration script)

**Phase 1 Risks**:
- Low: All changes are additive (new fields, not modifying existing)
- Medium: SQLite schema migration may fail on existing databases; migration script required
- Low: No source code modifications that break existing functionality (read-only design constraint)

---

### Phase 2: Metrics Aggregation (Weeks 3-4)
**Goal**: Collect metrics from all 7 subsystems and expose via Prometheus/CEO Dashboard

| # | Task | Description | Dependencies | Acceptance Criteria |
|---|------|-------------|-------------|---------------------|
| P2.1 | **Create MetricsAggregator module** | New `ai_company/observability/metrics_aggregator.py` that collects from all 7 subsystems | P1.1-P1.5 | Module imports from all 7 systems; exposes `get_prometheus_metrics()` returning str |
| P2.2 | **Collect Executor metrics** | Tool execution counts, success/failure rates, tier distribution, SLA timeout violations | P1.3 | Prometheus counters: `lightspeed_tool_executions_total`, `lightspeed_tool_sla_violations_total` |
| P2.3 | **Collect Decision Engine metrics** | Approval gate decisions per tier, approval rates | Existing decision engine | Prometheus histogram: `lightspeed_approval_gate_decisions_total` by tier (0-4) |
| P2.4 | **Collect Workflow Engine metrics** | Step success/failure rates across 9 definitions, active workflow count | P1.1-P1.5 | Prometheus gauges: `lightspeed_workflow_active_total`, `lightspeed_workflow_step_success_total`, `lightspeed_workflow_step_failure_total` |
| P2.5 | **Collect Model Router metrics** | Free-model catalog cache hit/miss, routing distribution per layer | Existing model_router | Prometheus counters: `lightspeed_model_router_cache_hits_total`, `lightspeed_model_router_cache_misses_total`, `lightspeed_model_router_routing_distribution` by layer |
| P2.6 | **Collect Cache metrics** | LLM response cache hit/miss, OAuth2 token cache expiry, Model Router free-model catalog, YAML config cache hit/miss, ConversationHistoryManager cache hit/miss | P1.5 | Prometheus counters: `lightspeed_cache_*_hits_total`, `lightspeed_cache_*_misses_total` for each cache type |
| P2.7 | **Collect Token and Cost metrics** | Total tokens, cost per agent/task/model, daily/weekly/monthly aggregation, budget status | P1.4, llm/cost_analytics.py | Prometheus counters/histograms: `lightspeed_tokens_total`, `lightspeed_cost_usd_total`, `lightspeed_cost_per_agent`, `lightspeed_budget_remaining` |
| P2.8 | **Prometheus HTTP endpoint** | New endpoint on CEO Dashboard (existing FastAPI/uvicorn on port 8420/8421) | P2.1-P2.7 | `GET /metrics` returns Prometheus-formatted metrics; accessible via `curl -H "X-API-Key: $DASHBOARD_RUN_KEY" http://localhost:8421/metrics` |

**Phase 2 Deliverables**:
- `ai_company/observability/metrics_aggregator.py` (new, ~200-300 lines)
- Prometheus-formatted metrics export (~20+ metrics)
- `GET /metrics` endpoint on CEO Dashboard
- Verification: `curl -H "X-API-Key: $DASHBOARD_RUN_KEY" http://localhost:8421/metrics` returns metrics

**Phase 2 Risks**:
- Medium: Collecting from all 7 subsystems may reveal missing metrics; some subsystems may not emit required data initially
- Low: Prometheus format is well-established; existing infrastructure supports it
- Medium: Dashboard port (8420/8421) may have conflicts; verify port free before deployment

---

### Phase 3: Dashboard Integration (Weeks 5-6)
**Goal**: Expose aggregated metrics via CEO Dashboard /kpi/* endpoints

| # | Task | Description | Dependencies | Acceptance Criteria |
|---|------|-------------|-------------|---------------------|
| P3.1 | **Enhance /health endpoint** | Add observability health checks: otel_enabled, active_workflows, cache_hit_rate, cost_today_usd | P2.8 | `GET /health` returns: `{status: "healthy", otel_enabled: bool, active_workflows: int, cache_hit_rate: float, cost_today_usd: float}` |
| P3.2 | **Create /kpi/context-intelligence endpoint** | New endpoint with comprehensive context intelligence metrics | P2.1-P2.7 | `GET /kpi/context-intelligence` returns JSON with: total_requests_24h, average_token_usage_per_request, cache_hit_rate, cost_today_usd, workflow_success_rate, approval_tier_distribution, active_workflows, otel_enabled |
| P3.3 | **Create /kpi/approval-distribution endpoint** | Approval tier distribution across all tasks | P2.3 | `GET /kpi/approval-distribution` returns: `{AUTO_APPROVE: int, NOTIFY: int, SINGLE_APPROVER: int, TWO_PERSON: int, CEO_ONLY: int}` counts and percentages |
| P3.4 | **Create /kpi/workflow-status endpoint** | Workflow health across 9 definitions | P2.4 | `GET /kpi/workflow-status` returns per-definition success/failure counts, active workflows, success rates |
| P3.5 | **Create /kpi/cache-effectiveness endpoint** | Cache hit rates per type | P2.6 | `GET /kpi/cache-effectiveness` returns hit rates for: LLM response, OAuth2, Model Router free-model catalog, YAML config, ConversationHistoryManager |
| P3.6 | **RBAC key validation on all /kpi/* endpoints** | Validate DASHBOARD_RUN_KEY (or DASHBOARD_ADMIN_KEY) on every access | AGENTS.md §11 | All /kpi/* endpoints require valid API key; 401 returned for missing/invalid key |

**Phase 3 Deliverables**:
- Enhanced `GET /health` response
- `GET /kpi/context-intelligence` endpoint
- `GET /kpi/approval-distribution` endpoint
- `GET /kpi/workflow-status` endpoint
- `GET /kpi/cache-effectiveness` endpoint
- RBAC validation on all new endpoints
- Verification via curl commands with DASHBOARD_RUN_KEY

**Phase 3 Risks**:
- Low: Endpoints are additive; existing endpoints unchanged
- Medium: RBAC key validation must correctly integrate with existing Dashboard RBAC system (DASHBOARD_RUN_KEY, DASHBOARD_ADMIN_KEY, DASHBOARD_API_KEY)
- Low: JSON response format must match existing Dashboard API patterns

---

### Phase 4: Advanced Features (Weeks 7-8)
**Goal**: Advanced observability capabilities and historical analysis

| # | Task | Description | Dependencies | Acceptance Criteria |
|---|------|-------------|-------------|---------------------|
| P4.1 | **Historical SQLite analysis queries** | Expand `.cache/token_usage.db` with execution_context table; add queries for historical analysis | P1.4, P2.1-P2.7 | SQLite has `execution_context` table with request_id, task_id, agent_type, tier, timestamps, success, error_type, tool_name, model_name, prompt_tokens, completion_tokens, cost_usd, cache_hit, cache_key, workflow_name; verifiable via Python queries |
| P4.2 | **Cost forecasting integration** | Integrate `llm/cost_analytics.py` forecasting with real-time metrics aggregator | P1.4, P2.7 | `forecast_daily` linear extrapolation incorporates real-time token/cost data from aggregator |
| P4.3 | **Agent-type context profiling** | Analyze historical token usage patterns per agent_type (Executive, Specialist, Department, Company) | P2.5, historical SQLite queries | Agent-type context size profiles: average prompt_tokens, completion_tokens, total_tokens per agent_type; verifiable via SQL queries |
| P4.4 | **Cache effectiveness over time** | Historical cache hit rate trends (daily/weekly/monthly) | P2.6, historical data | Time-series cache hit rates per cache type; chartable via external tool (Grafana, etc.) |
| P4.4 | **Approval trend analysis** | AUTO_APPROVE through CEO_ONLY usage trends over time | P2.3, historical SQLite queries | Time-series approval tier distribution; verifiable via SQL queries |
| P4.5 | **Real-time alerting thresholds** | Configure configurable thresholds (e.g., cache_hit_rate < 70%, cost_per_day > budget, approval_tier shifting toward CEO_ONLY) | P2.8, P4.1-P4.4 | Alert conditions configurable; can trigger notifications (implementation: choose: PagerDuty, email, or internal dashboard alert) |

**Phase 4 Deliverables**:
- Expanded `execution_context` SQLite table and migration script
- Cost forecasting integration with real-time data
- Agent-type context profiling reports
- Cache effectiveness time-series data
- Approval trend time-series data
- Configurable alerting thresholds (optional, choose one: notification mechanism)

**Phase 4 Risks**:
- Low: SQLite migration script is additive; existing data preserved
- Medium: Historical analysis queries depend on data being present (needs Phase 1+2 deployment)
- Low: Agent-type profiling requires sufficient historical data; may start with empty results

---

### Phase 5: Optimization (Weeks 9-10)
**Goal**: Refinement, cleanup, and ensuring no regressions

| # | Task | Description | Dependencies | Acceptance Criteria |
|---|------|-------------|-------------|---------------------|
| P5.1 | **Verify no regressions in existing functionality** | All existing endpoints, tools, and workflows unchanged; existing tests pass | All prior phases | `uv run pytest` passes; `ai-company --help` unchanged; all 7 canonical tools functional |
| P5.2 | **Validate SQL migrations** | Migration scripts applied to fresh and existing databases; no data loss | P1.5, P4.1 | `uv run python -c "from ai_company.observability.migration import migrate_db; migrate_db()` succeeds on test DB; existing .cache/token_usage.db data preserved |
| P5.3 | **Verify RBAC integration** | All /kpi/* endpoints correctly validated with Dashboard keys; no unauthorized access | P3.6 | Test with valid key → 200; test with invalid key → 401; test with no key → 401 |
| P5.3 | **Confirm Prometheus metrics format** | `GET /metrics` returns valid Prometheus format; verifiable via `python -c "import prometheus_client; ..."` | P2.8 | Metrics endpoint returns parseable format; `prometheus_client.parser.parse()` succeeds |
| P5.4 | **Document all changes** | Update this roadmap with completion status; add to CHANGELOG.md if applicable | All prior phases | Roadmap updated with dates, completion status, and any deviations |

**Phase 5 Deliverables**:
- Regression test suite passing
- SQL migration validated
- RBAC integration verified
- Prometheus format validated
- Documentation updated

**Phase 5 Risks**:
- Low: All verification steps are confirmatory; no new code that could introduce bugs
- Medium: SQL migration on production databases requires care; have rollback plan
- Low: RBAC integration test covers key scenarios; existing hook governance unchanged

---

## 2. Dependencies Summary

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
  │           │           │           │           │
  ▼           ▼           ▼           ▼           ▼
ExecutionContext Metrics Aggregator Dashboard Advanced
  (request_id,   (collect from  (/enable /kpi/* (historical
  task_id,       all 7 subsys)   endpoints)   analysis)
  agent_type)     + Prometheus    + RBAC
```

**Critical path**: P1.1 → P1.2 → P1.3 → P1.4 → P1.5 → P2.1-P2.8 → P3.1-P3.6 → P4.1-P4.5 → P5.1-P5.4

**Optional branches**: P4.2 (cost forecasting integration) can start after P1.4; P4.3-P4.5 (historical analysis) can start after P2.1-P2.7 are deployed.

---

## 3. Testing Requirements

### 3.1 Unit Tests

| Test Target | Description | Example |
|-------------|-------------|---------|
| ExecutionContext dataclass | Instantiation, JSON serialization/deserialization | `python -c "from ai_company.observability.execution_context import ExecutionContext; ec = ExecutionContext(request_id='x', task_id='y', agent_type='Executive'); assert ec.request_id == 'x'"` |
| MetricsAggregator | Import from all 7 subsystems, get_prometheus_metrics() returns str | `python -c "from ai_company.observability.metrics_aggregator import MetricsAggregator; m = MetricsAggregator(); metrics = m.get_prometheus_metrics(); assert isinstance(metrics, str)"` |
| _record_usage() enhancement | Always records request_id, task_id, agent_type | Verify `logs/token_usage.jsonl` line includes new fields |
| ConversationHistoryManager.cache_hit_rate | Property computation | `python -c "from ai_company.executor.agent_loop import ConversationHistoryManager; mgr = ConversationHistoryManager(); mgr.cache_hits = 5; mgr.cache_misses = 5; assert mgr.cache_hit_rate == 0.5"` |

### 3.2 Integration Tests

| Test Target | Description | Example |
|-------------|-------------|---------|
| Request propagation | CEO instruction → request_id → all subsystems | Dispatch task; verify request_id in inbox.json, tool logs, cost records, OTel spans (if enabled) |
| Cost attribution | LLM call → _record_usage() → execution_context SQLite | Execute task; query `.cache/token_usage.db` execution_context table for recorded fields |
| Dashboard RBAC | /kpi/* endpoints require valid key | `curl -H "X-API-Key: bad_key" http://localhost:8421/kpi/context-intelligence` → 401 |
| Prometheus format | /metrics endpoint valid format | `python -c "from prometheus_client.parser import parse; list(parse(response.text))` succeeds" |
| SQLite migration | Existing data preserved, new table added | Migrate fresh DB + existing DB; query both for expected data |

### 3.3 End-to-End Tests

| Scenario | Description | Success Criteria |
|----------|-------------|------------------|
| CEO instruction flow | Dispatch task → complete → verify metrics captured | request_id present in: inbox.json, tool execution logs, cost records, (if OTel enabled) spans |
| Cache hit/miss tracking | Execute tasks with cache hits and misses; verify metrics aggregator counts | `lightspeed_cache_hits_total` and `lightspeed_cache_misses_total` increment correctly |
| Cost per task | Execute tasks; verify cost attribution to agent_type, task_id | `.cache/token_usage.db` execution_context table has cost_usd, agent_type, task_id for each call |
| Dashboard metrics query | CEO queries /kpi/context-intelligence with valid key | JSON response has all expected fields: total_requests_24h, average_token_usage_per_request, cache_hit_rate, cost_today_usd, workflow_success_rate, approval_tier_distribution, active_workflows, otel_enabled |
| RBAC denial | CEO queries /kpi/context-intelligence without key or with invalid key | 401 Unauthorized; no data leaked |

---

## 4. Acceptance Criteria (Overall)

The implementation is complete when all of the following are true:

### 4.1 Technical Acceptance Criteria

- [ ] `ExecutionContext` dataclass defined in `ai_company/observability/execution_context.py`
- [ ] `request_id` and `task_id` propagated through Message Bus (.opencode/inbox.json)
- [ ] `check_tier_rules()` in tool_runner.py accepts and propagates ExecutionContext
- [ ] `_record_usage()` in client.py always records `request_id`, `task_id`, `agent_type`, and `heuristic_vs_provider_reported` flag
- [ ] `ConversationHistoryManager.cache_hit_rate` property computed and accessible
- [ ] `MetricsAggregator` module collects from all 7 subsystems
- [ ] `GET /metrics` endpoint returns Prometheus-formatted metrics (20+ metrics)
- [ ] `GET /health` enhanced with: otel_enabled, active_workflows, cache_hit_rate, cost_today_usd
- [ ] `GET /kpi/context-intelligence` returns JSON with all 8 expected fields
- [ ] `GET /kpi/approval-distribution` returns tier distribution counts/percentages
- [ ] `GET /kpi/workflow-status` returns per-definition success/failure counts
- [ ] `GET /kpi/cache-effectiveness` returns hit rates for all 5 cache types
- [ ] All /kpi/* endpoints require valid DASHBOARD_RUN_KEY (or DASHBOARD_ADMIN_KEY)
- [ ] `uv run pytest` passes (existing tests unchanged)
- [ ] SQL migration script successfully migrates existing .cache/token_usage.db
- [ ] No source code modifications that break existing functionality (read-only constraint satisfied)

### 4.2 Governance Acceptance Criteria

- [ ] No `.env` changes committed to git (env files remain gitignored)
- [ ] No root config changes (AGENTS.md, opencode.json) without CEO-OVERRIDE tag (per §18.1)
- [ ] Pre-commit hook governance unchanged (read-only design)
- [ ] Dashboard RBAC keys (DASHBOARD_ADMIN_KEY, DASHBOARD_APPROVE_KEY, DASHBOARD_RUN_KEY, DASHBOARD_API_KEY) still functional
- [ ] Key rotation procedures (every 90 days) unchanged
- [ ] Audit evidence separation maintained (read set and write set disjoint)
- [ ] Governance-audit.md not modified by this design (read-only)

### 4.3 Performance Acceptance Criteria

- [ ] ExecutionContext propagation adds ≤ 1ms overhead per tool execution
- [ ] MetricsAggregator.collect() completes in ≤ 50ms
- [ ] GET /metrics response time ≤ 100ms
- [ ] GET /kpi/* endpoint response time ≤ 200ms
- [ ] No SLA timeout increase (remains 120s)
- [ ] No increase in tool execution duration (tool_runner.py SLA unchanged)

### 4.4 Security Acceptance Criteria

- [ ] No third-party data transmission (per §9.2 Skill Third-Party Transmission Ban)
- [ ] PII/content sanitization unchanged (tool_runner.py unchanged in this regard)
- [ ] Audit evidence separation maintained (read set/write set disjoint)
- [ ] RBAC key validation on /kpi/* endpoints does not leak information on 401 response
- [ ] Key rotation procedures unchanged

---

## 5. Risks and Mitigations

| # | Risk | Mitigation |
|---|------|------------|
| R1 | **SQLite migration fails on production databases** | - Migration script is additive (ADD COLUMN, CREATE TABLE IF NOT EXISTS)<br>- Backup .cache/token_usage.db before migration<br>- Rollback: original schema preserved if migration fails<br>- Test on staging before production |
| R2 | **Dashboard RBAC integration issues** | - Existing RBAC key hierarchy (DASHBOARD_ADMIN_KEY > DASHBOARD_APPROVE_KEY > DASHBOARD_RUN_KEY > DASHBOARD_API_KEY) documented<br>- Test each key level separately<br>- If integration fails, disable new endpoint RBAC (optional feature, not critical) |
| R3 | **Missing metrics from some subsystems** | - Phase 1-2 deployment reveals which subsystems emit required data<br>- Missing metrics have graceful degradation (prometheus metric with label `unordered` or `0` value)<br>- Prioritize Phase 3 Dashboard endpoints on most-critical metrics first |
| R4 | **Performance overhead too high** | - ExecutionContext propagation designed as ≤ 1ms overhead<br>- MetricsAggregator.collect() designed as ≤ 50ms<br>- If overhead higher, optimize: cache metrics in memory, batch exports, reduce metric count |
| R5 | **OpenTelemetry opt-in resistance from teams** | - Make OTel default-on with AI_COMPANY_OTEL=1 for enhanced features, NoOp fallback when not set<br>- Phased rollout: Phase 1-2 metrics don't require OTel; OTel enhancements in Phase 4 optional |
| R6 | **Cache hit/miss tracking not enabled in some systems** | - ConversationHistoryManager cache_hits/misses already exist; enable exposure<br>- Other caches (LLM response, OAuth2, etc.): optional instrumentation in Phase 4<br>- Core metrics (tokens, costs, approvals, workflows) work without full cache tracking |
| R7 | **Historical analysis queries return empty results initially** | - Phase 1-2 deposit data into execution_context SQLite table<br>- Phase 3-5 analytics build on deposited data<br>- Empty results in early months are expected; not a failure |
| R8 | **RBAC key validation bypass or info leakage** | - 401 response on invalid/missing key; no data in response body<br>- Validate that error messages don't expose internal details<br>- Follow existing Dashboard RBAC patterns exactly |

---

## 6. Unresolved Questions (to be addressed in later phases or by CEO)

| # | Question | Current Status |
|---|----------|----------------|
| U1 | **Should OTel be default-on or opt-in?** | Design recommends default-on with NoOp fallback when AI_COMPANY_OTEL not set; CEO to confirm |
| U2 | **Which alerting mechanism for real-time thresholds?** | P4.5 lists options: PagerDuty, email, internal dashboard; CEO/product to choose |
| U3 | **Cache hit/miss tracking for which caches is mandatory vs optional?** | Core: ConversationHistoryManager (already exists), Cost attribution, Token usage, Approval tiers, Workflow health. Optional: LLM response cache, OAuth2 token cache, Model Router free-model catalog, YAML config cache (Phase 4) |
| U4 | **Agent-type context profiling: 4 agent types (Executive, Specialist, Department, Company) or more granular?** | Current 4 types from company-registry.yaml; CEO to confirm granularity |
| U5 | **Historical analysis time window: daily/weekly/monthly?** | Default: all three; CEO to confirm prioritization |
| U6 | **Prometheus metrics: expose exactly which metrics, and in what detail?** | Draft list of 20+ metrics in Phase 2; CEO/product to prioritize and validate |
| U7 | **SDK/client library for metrics aggregator?** | Not in scope for Phase 1-3; may be needed for external dashboard integrations; CEO to decide |
| U8 | **Long-term: replace siloed metrics with this unified layer, or coexist?** | Design assumes coexistence with siloed systems during transition; CEO to decide on migration timeline |

---

## 7. Implementation Checklist

### Pre-Implementation
- [ ] Review this roadmap with CEO/CISO (governance compliance)
- [ ] Confirm Dashboard RBAC key hierarchy is acceptable
- [ ] Confirm AI_COMPANY_OTEL default-on policy
- [ ] Take backup of .cache/token_usage.db and logs/token_usage.jsonl
- [ ] Verify staging environment available for testing

### Phase 1 (Weeks 1-2)
- [ ] Create `ai_company/observability/execution_context.py`
- [ ] Enhance `.opencode/inbox.json` payload with request_id, task_id
- [ ] Enhance `tool_runner.py` check_tier_rules() to propagate ExecutionContext
- [ ] Enhance `llm/client.py` _record_usage() with execution context fields
- [ ] Add ConversationHistoryManager.cache_hit_rate property
- [ ] Update `logs/token_usage.jsonl` schema (append new fields)
- [ ] Update `.cache/token_usage.db` schema migration script
- [ ] Test: SQLite migration on fresh + existing DB

### Phase 2 (Weeks 3-4)
- [ ] Create `ai_company/observability/metrics_aggregator.py`
- [ ] Implement collection from all 7 subsystems
- [ ] Implement Prometheus-formatted metrics export (~20 metrics)
- [ ] Add `GET /metrics` endpoint to CEO Dashboard
- [ ] Test: `curl -H "X-API-Key: $DASHBOARD_RUN_KEY" http://localhost:8421/metrics`

### Phase 3 (Weeks 5-6)
- [ ] Enhance `GET /health` with observability health checks
- [ ] Create `GET /kpi/context-intelligence` endpoint
- [ ] Create `GET /kpi/approval-distribution` endpoint
- [ ] Create `GET /kpi/workflow-status` endpoint
- [ ] Create `GET /kpi/cache-effectiveness` endpoint
- [ ] Implement RBAC key validation on all /kpi/* endpoints
- [ ] Test: curl commands with valid and invalid keys

### Phase 4 (Weeks 7-8)
- [ ] Expand execution_context SQLite table and migration script
- [ ] Integrate cost forecasting with real-time metrics
- [ ] Implement agent-type context profiling queries
- [ ] Implement cache effectiveness time-series queries
- [ ] Implement approval trend time-series queries
- [ ] Configure alerting thresholds (CEO choice: mechanism and values)

### Phase 5 (Weeks 9-10)
- [ ] Verify no regressions in existing functionality
- [ ] Validate SQL migrations
- [ ] Verify RBAC integration
- [ ] Confirm Prometheus metrics format
- [ ] Update roadmap with completion status
- [ ] Update CHANGELOG.md if applicable

### Post-Implementation
- [ ] Monitor production metrics for 48 hours
- [ ] Address any reported issues
- [ ] Document lessons learned
- [ ] Plan next iteration (if any)

---

## 8. Summary

**Implementation Philosophy**: Smallest viable architecture that reuses existing infrastructure, establishes standard execution metadata, aggregates metrics across subsystems, supports CEO Dashboard exposure, and preserves security/governance.

**Key Principles**:
1. **Read-only design**: No source code modifications that break existing functionality
2. **Incremental rollout**: Phase 1 → Phase 5; each phase independently verifiable
3. **Reuse existing storage**: SQLite (.cache/token_usage.db), JSONL (logs/token_usage.jsonl), in-memory (Prometheus), HTTP (CEO Dashboard)
4. **RBAC-integrated**: All new endpoints respect existing Dashboard key hierarchy
5. **Governance-preserving**: No root config changes without CEO-OVERRIDE; audit evidence separation maintained
6. **No new infrastructure**: Reuses existing Vite/React app port architecture, Docker ports, etc.

**Expected Token Savings**: Not quantified (per design constraint — token savings only where supported by evidence). Expected benefits are in **observability and governance**, not direct token consumption reduction. Indirect benefits may include:
- Better context budgeting via size tracking
- Reduced waste from repeated file reads via awareness (not automatic caching)
- Cost attribution enabling optimization

**Roadmap Duration**: 10 weeks (Phases 1-5)
**Critical Path**: P1.1 → P1.2 → P1.3 → P1.4 → P1.5 → P2.1-P2.8 → P3.1-P3.6 → P4.1-P4.5 → P5.1-P5.4

**Success Criteria**: All 28 acceptance criteria (technical + governance + performance + security) verified passing.

---
*Implementation roadmap generated from comprehensive analysis of seven-systems-investigation-report.md, observability-research-report.md, context-intelligence-investigation-report.md, and all key source code files.*
