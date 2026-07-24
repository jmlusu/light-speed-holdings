# CAIO Strategic AI Report — Light Speed Holdings

**Author**: Chief AI Officer (CAIO)
**Date**: 2026-07-24
**Status**: Final
**Scope**: Full AI/ML infrastructure audit, quality assessment, gap analysis, Sprint 4 plan

---

## 1. AI INFRASTRUCTURE STATUS

### 1.1 LLM Abstraction Layer — OPERATIONAL

| Component | Status | Location | Assessment |
|-----------|--------|----------|------------|
| LLMClient | ✅ Production | `llm/client.py` (324 lines) | Multi-provider, retry (5 attempts), JSON parse fallback |
| ModelRouter | ✅ Production | `model_router.py` (551 lines) | 5-layer routing: per-agent → context → domain → type+priority → fallback |
| CostTracker | ✅ Production | `llm/cost_tracker.py` (327 lines) | JSONL + dual persistence (JSONL + SQLite), daily/task budgets |
| CostAnalytics | ✅ Production | `data/cost_analytics.py` (511 lines) | SQLite aggregation, forecasting, breakdown by agent/task/model/provider |
| CircuitBreaker | ✅ Production | `llm/circuit_breaker.py` (76 lines) | CLOSED→OPEN→HALF_OPEN state machine, 3-failure threshold, 60s recovery |
| JSON Parser | ✅ Production | `llm/json_parser.py` (61 lines) | 3-strategy fallback: direct → markdown block → brace extraction |
| Provider Abstraction | ✅ Production | `llm/providers/base.py` (131 lines) | ABC with chat(), chat_stream(), is_available() |
| OpenAI-Compatible | ✅ Production | `llm/providers/openai_compatible.py` (269 lines) | OpenAI + Anthropic SSE parsing, bearer + x-api-key auth |
| Ollama Provider | ✅ Production | `llm/providers/ollama.py` | Local fallback, no API key needed |
| Streaming | ✅ Production | Both providers | SSE parsing with chunk-by-chunk yield |

**Provider Catalog (5 providers):**

| Provider | Backend | Default Model | Tier | Purpose |
|----------|---------|---------------|------|---------|
| OpenCode | openai_compatible | big-pickle | fast + standard | Primary (fast tier) |
| DeepSeek | openai_compatible | deepseek-chat | standard + premium | Balanced capability |
| Ollama | ollama | llama3.1:8b | fast (fallback) | Local, free, zero-latency |
| OpenAI | openai_compatible | gpt-4o-mini | reserved | Fallback |
| Anthropic | openai_compatible | claude-sonnet-4 | reserved | Fallback (x-api-key auth) |

**Tier Configuration:**
- **fast**: opencode/big-pickle → ollama/llama3.1:8b (cheapest, low-latency)
- **standard**: deepseek/deepseek-chat → opencode/big-pickle (balanced)
- **premium**: deepseek/deepseek-coder → opencode/big-pickle (best reasoning)

**Routing Quality Assessment:** The 5-layer routing system is architecturally sound. Per-agent overrides (highest priority) allow locking specific agents to specific models. Domain-aware detection uses keyword heuristics (6 domains: finance, legal, security, code_review, deployment, data_science) with a 2-hit minimum threshold. The quality-based fallback chain (fast → standard → premium) ensures degraded-but-functional operation when providers fail.

### 1.2 Agent Execution Loop — OPERATIONAL

| Component | Status | Location | Assessment |
|-----------|--------|----------|------------|
| AgentLoop | ✅ Production | `executor/agent_loop.py` (366 lines) | ReAct pattern, multi-turn, cost tracking, HITL gates |
| ToolRunner | ✅ Production | `executor/tool_runner.py` | shlex.split() (no shell=True), tier_rules, audit logging |
| HITLGate | ✅ Production | `executor/hitl_gate.py` | Non-blocking via concurrent.futures.Future |
| Prompts Engine | ✅ Production | `executor/prompts.py` (479 lines) | v2 optimized: role prefixes, tool instructions, few-shot examples |
| AgentContext | ✅ Production | `executor/context.py` | Parsed agent spec cards from registry |

**AgentLoop Architecture:**
- ReAct pattern: Reason → Act → Observe → Repeat
- Max iterations: 10 (configurable via LoopConfig)
- Budget enforcement: daily + per-task caps checked every iteration
- Quality fallback: resolve_with_fallback() builds provider chain across tiers
- Error recovery guidance: per-error-type recovery instructions injected into iteration feedback
- Token accumulation: tracks prompt_tokens + completion_tokens across all iterations
- Cost recording: dual-write to JSONL (CostTracker) + SQLite (CostAnalytics)

**Prompt Engineering (v2):**
- 4 agent-type personas (Executive, Specialist, Board, Department) with behavioral rules
- Type-specific tool instructions with error recovery patterns
- Few-shot JSON examples per type
- Iteration feedback with context-aware guidance (error diagnosis, remaining budget)
- Escalation rules embedded in system prompt

### 1.3 Memory Engine — OPERATIONAL

| Component | Status | Location | Assessment |
|-----------|--------|----------|------------|
| MemoryStore | ✅ Production | `memory/engine.py` (578 lines) | 6 memory types, FileStore persistence |
| MemoryEntry | ✅ Production | `memory/engine.py` | Content-hash deduplication, access counting |
| VectorStore | ✅ Available | `memory/vector_store.py` | Optional cosine-similarity search |
| EmbeddingEngine | ✅ Available | `ml/embeddings.py` (211 lines) | sentence-transformers (all-MiniLM-L6-v2), caching |
| Encryption | ✅ Available | `security/memory_encryption.py` | AES-256 at-rest encryption |
| Pruning | ✅ Production | `memory/engine.py` | Age-based + per-type cap |
| Consolidation | ✅ Production | `memory/engine.py` | Semantic dedup + aggregate rollup |

**Memory Types:**
1. Episodic — events and experiences
2. Semantic — facts and knowledge
3. Procedural — how-to knowledge
4. Relational — entity relationships
5. Temporal — time-based records
6. Aggregate — summaries and rollups

### 1.4 ML Intelligence Layer — OPERATIONAL

| Component | Status | Location | Assessment |
|-----------|--------|----------|------------|
| TaskComplexityScorer | ✅ Production | `ml/complexity.py` (301 lines) | 6-signal weighted scoring, 0.0–1.0 scale |
| PromptOptimizer | ✅ Production | `ml/prompt_optimizer.py` (516 lines) | Audit-log analysis, A/B variant testing |
| AgentPerformanceTracker | ✅ Production | `ml/performance.py` (311 lines) | Per-agent metrics, Ridge regression prediction |
| AnomalyDetector | ✅ Production | `ml/anomaly.py` (322 lines) | Z-score + IQR dual detection |
| PredictiveScaling | ✅ Production | `ml/predictive_scaling.py` (352 lines) | Task volume + cost forecasting |
| EmbeddingEngine | ✅ Available | `ml/embeddings.py` (211 lines) | Local sentence-transformer embeddings |

**TaskComplexityScorer Signals:**
- keyword_density (25%): complex vs simple keyword hits per 100 words
- structural (15%): word count, list items, code blocks
- pattern_match (20%): regex patterns for system-building, multi-component tasks
- tool_complexity (15%): execute/delegate vs read/list tools
- priority (10%): low→0.2, medium→0.5, high→0.7, critical→0.9
- agent_type (15%): specialist→0.4, lead→0.6, executive→0.7, board→0.8

**Routing Integration:** `ModelRouter.resolve_with_complexity()` overrides tier selection based on complexity score: ≤0.33→fast, 0.34–0.66→standard, ≥0.67→premium. Override is advisory — per-agent and context rules still take precedence.

### 1.5 Analytics & Monitoring — OPERATIONAL

| Component | Status | Location | Assessment |
|-----------|--------|----------|------------|
| AgentPerformanceAnalytics | ✅ Production | `data/agent_analytics.py` (311 lines) | SQLite: completion rates, tool usage, error analysis |
| CostAnalytics | ✅ Production | `data/cost_analytics.py` (511 lines) | SQLite: daily/weekly/monthly, breakdowns, forecasting |
| AnomalyDetector | ✅ Production | `ml/anomaly.py` | Z-score + IQR, metric windows, alert persistence |
| Dashboard | ✅ Production | `dashboard/app.py` | X-API-Key auth, CORS, WebSocket broadcast |

### 1.6 Agent Hierarchy — DEPLOYED

- **127 agents** deployed to workspace-level `.opencode/agents/`
- All agents invokable via `@` in terminal
- Organization: Board, C-Suite (CEO, CTO, CFO, COO, CISO, CPO, CSO), 8 departments, 53 new roles added 2026-07-21
- 12 Jinja2 templates for agent generation
- Registry: 19 YAML config files → typed CompanyRegistry

---

## 2. QUALITY METRICS

### 2.1 Code Quality

| Metric | Value | Status |
|--------|-------|--------|
| ruff lint | 0 errors | ✅ Clean |
| mypy type check | 0 errors (164 files) | ✅ Clean |
| pytest | 1205 passing (0 failures) | ✅ Green |
| pre-commit hooks | ruff, mypy, bandit, trailing-whitespace, end-of-file | ✅ Active |

### 2.2 AI Performance Metrics (Designed but Not Yet Collecting Live Data)

| Metric | Tracking Mechanism | Current State |
|--------|-------------------|---------------|
| Task completion rate | AgentPerformanceAnalytics (SQLite) | Schema ready, needs live task data |
| Per-agent success rate | AgentPerformanceTracker (JSON) | Schema ready, needs execution records |
| Model usage distribution | CostAnalytics.model_usage_distribution() | Schema ready, needs cost records |
| Task duration stats | AgentPerformanceAnalytics.task_duration_stats() | Schema ready, needs completed tasks |
| Error analysis | AgentPerformanceAnalytics.error_analysis() | Schema ready, needs audit events |
| Prompt effectiveness | PromptOptimizer.analyze_prompt_effectiveness() | Reads audit JSONL, needs events |
| Cost per task | CostTracker + CostAnalytics | Dual-write active when task_id provided |
| Anomaly detection | AnomalyDetector | Z-score + IQR active, needs metric feed |

### 2.3 Model Routing Quality

| Indicator | Status | Notes |
|-----------|--------|-------|
| Domain detection accuracy | ⚠️ Untested | Keyword heuristics — no evaluation benchmark |
| Complexity scoring accuracy | ⚠️ Untested | 6-signal heuristic — no ground truth validation |
| Fallback success rate | ⚠️ Not tracked | CircuitBreaker records failures but no fallback-chain metrics |
| Tier appropriateness | ⚠️ Not measured | No A/B comparison of tier routing decisions vs outcomes |

### 2.4 Prompt Quality

| Indicator | Status | Notes |
|-----------|--------|-------|
| v2 prompt templates | ✅ Deployed | Role-specific personas, few-shot examples, error recovery |
| Prompt regression tests | ⚠️ Not implemented | No snapshot tests for prompt drift |
| A/B variant testing | ✅ Infrastructure ready | PromptOptimizer has variant creation + outcome recording |
| Prompt length optimization | ✅ Analyzed | Optimal range calculation via PromptOptimizer |
| Keyword impact analysis | ✅ Analyzed | Harmful/helpful keyword detection from audit logs |

---

## 3. GAPS ANALYSIS

### 3.1 Critical Gaps (P0)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| **GAP-T01** | **Token counting integration** | No pre-flight token estimation; tasks can exceed context windows silently. Budget checks use post-hoc token counts from API responses, not pre-call estimates. | 4h |
| **GAP-T02** | **Eval benchmarks not implemented** | No systematic evaluation of model quality, routing accuracy, or prompt effectiveness. `.benchmarks/` directory exists but is empty. Cannot measure whether routing decisions improve outcomes. | 8h |
| **GAP-T03** | **No prompt optimization loop** | PromptOptimizer reads audit logs and generates insights, but there is no automated pipeline to apply suggestions, create variants, or measure improvements. A/B testing infrastructure exists but is not wired into the execution loop. | 6h |

### 3.2 High Gaps (P1)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| **GAP-T04** | **No model quality evaluation** | Cannot compare model performance across providers (e.g., does DeepSeek outperform OpenCode for code tasks?). No accuracy, latency, or cost-per-quality metrics. | 6h |
| **GAP-T05** | **Complexity scorer not calibrated** | TaskComplexityScorer uses static heuristic weights. No feedback loop from actual task outcomes to tune weights. Simple tasks may be routed to premium (over-spending) or complex tasks to fast (quality degradation). | 4h |
| **GAP-T06** | **No token budget pre-check** | AgentLoop.config has max_tokens=4096 but no enforcement of context window limits. Long conversation histories can push prompts beyond model limits. | 3h |
| **GAP-T07** | **Cost tracker MODEL_COSTS outdated** | Pricing table has Claude 3.5 Sonnet/Haiku, GPT-4 Turbo — models that may be deprecated. Missing newer models (Claude 4, o3, Gemini). | 1h |

### 3.3 Medium Gaps (P2)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| **GAP-T08** | **No streaming token tracking** | execute_task_stream() yields chunks but doesn't track per-chunk usage. Final chunk usage may be incomplete for some providers. | 2h |
| **GAP-T09** | **Prompt regression testing missing** | No snapshot tests to detect prompt drift when templates are modified. Could silently degrade agent behavior. | 3h |
| **GAP-T10** | **No cross-provider latency tracking** | CircuitBreaker tracks failures but not response times. Cannot optimize for latency vs quality tradeoffs. | 2h |
| **GAP-T11** | **Embedding model not configurable** | EmbeddingEngine defaults to all-MiniLM-L6-v2. No CLI or config to switch models for different use cases. | 1h |
| **GAP-T12** | **No multi-turn context compression** | Long ReAct loops build unbounded conversation_history. No summarization or truncation strategy for context window management. | 4h |

### 3.4 Low Gaps (P3)

| ID | Gap | Impact | Effort |
|----|-----|--------|--------|
| **GAP-T13** | **No model warm-up/prefetch** | Cold starts on Ollama models can add latency. No preload or keep-warm mechanism. | 2h |
| **GAP-T14** | **No provider health dashboard** | CircuitBreaker state is in-memory only. No visibility into provider health across processes. | 2h |
| **GAP-T15** | **No token usage per-tool breakdown** | CostTracker records per-call tokens but not per-tool within a multi-tool iteration. | 2h |

---

## 4. AI STRATEGY PLAN — SPRINT 4

### Sprint 4 Theme: **Intelligence Operationalization**

Sprint 4 transforms the AI infrastructure from "built and functional" to "measured and optimized." The three pillars are: (1) token-aware execution, (2) evaluation benchmarks, and (3) prompt optimization loop.

### 4.1 Pillar 1: Token-Aware Execution (S4-01 through S4-04)

**Objective:** Prevent context window overflow, enable pre-flight cost estimation, and enforce token budgets.

| Task | Description | Effort | Owner |
|------|-------------|--------|-------|
| S4-01 | **Token counter utility** — Create `llm/token_counter.py` with tiktoken-based counting for GPT/Claude models and fallback estimation for others. Expose `count_tokens(text, model) -> int`. | 3h | ml-engineer |
| S4-02 | **Pre-flight cost estimation** — Enhance `LLMClient.execute_task()` to estimate token count before API call using token_counter. Check against cost budget before sending. Log estimated vs actual in UsageRecord. | 2h | ml-engineer |
| S4-03 | **Context window enforcement** — Add `max_context_tokens` to LoopConfig. In AgentLoop.run(), truncate conversation_history when total estimated tokens exceed limit. Implement smart truncation: keep system prompt + last N iterations, summarize middle. | 4h | llm_platform_owner |
| S4-04 | **Update MODEL_COSTS** — Refresh pricing table with current model pricing (Claude 4, o3, Gemini 2.5). Add model→context_window mapping for token budget enforcement. | 1h | ml-engineer |

**Verification:**
- `python -c "from ai_company.llm.token_counter import count_tokens; print(count_tokens('hello world', 'gpt-4o'))"` returns int > 0
- AgentLoop with long history truncates gracefully without API errors
- CostTracker records `estimated_tokens` alongside `actual_tokens`

### 4.2 Pillar 2: Evaluation Benchmarks (S4-05 through S4-08)

**Objective:** Establish ground-truth evaluation for routing accuracy, model quality, and task completion.

| Task | Description | Effort | Owner |
|------|-------------|--------|-------|
| S4-05 | **Eval benchmark framework** — Create `benchmarks/` package with `EvalDataset`, `EvalRunner`, `EvalResult` classes. Support task-level eval (input→expected output) and routing-level eval (input→expected tier). | 4h | eval_benchmarks_engineer |
| S4-06 | **Routing accuracy benchmark** — Create 50 labeled test cases: (task_prompt, expected_domain, expected_tier). Run through ModelRouter.resolve() and measure accuracy. Target: ≥80% domain detection, ≥85% tier appropriateness. | 3h | eval_benchmarks_engineer |
| S4-07 | **Task completion benchmark** — Create 20 end-to-end test cases with mocked LLM providers. Each case: (agent_spec, task, expected_tool_sequence, expected_result_pattern). Run through AgentLoop and verify tool usage + completion. | 4h | eval_benchmarks_engineer |
| S4-08 | **Model comparison eval** — Run same 10 prompts across all 3 tiers (fast/standard/premium). Measure: JSON parse success rate, task completion rate, latency, cost. Produce comparison report. | 3h | ai_safety_lead |

**Verification:**
- `python -m benchmarks.run_routing_eval` produces accuracy report
- `python -m benchmarks.run_task_eval` produces completion report
- Results saved to `.benchmarks/results/` as JSON

### 4.3 Pillar 3: Prompt Optimization Loop (S4-09 through S4-12)

**Objective:** Close the feedback loop between prompt performance and prompt design.

| Task | Description | Effort | Owner |
|------|-------------|--------|-------|
| S4-09 | **Prompt version tracking** — Add `prompt_version` field to UsageRecord and LoopResult. Track which prompt template version produced each result. Enables prompt-level analytics. | 2h | prompt-engineer |
| S4-10 | **Variant auto-selection** — Wire PromptOptimizer into AgentLoop. Before each task, call `optimizer.select_variant()` to pick the best-performing prompt variant. Fall back to default if no qualified variant. | 3h | prompt-engineer |
| S4-11 | **Outcome feedback pipeline** — After each task completion, call `optimizer.record_variant_outcome(variant_id, success)`. Wire into AgentLoop's completion path. | 2h | prompt-engineer |
| S4-12 | **Prompt snapshot tests** — Create `tests/test_prompt_snapshots.py`. For each agent type, snapshot the system prompt output. On future runs, diff against snapshot to detect drift. | 3h | eval_benchmarks_engineer |

**Verification:**
- PromptOptimizer.get_variant_performance() returns ranked variants after 10+ tasks
- Prompt snapshots exist for all 4 agent types
- `pytest tests/test_prompt_snapshots.py` passes

### 4.4 Sprint 4 Timeline

| Week | Focus | Tasks | Hours |
|------|-------|-------|-------|
| Week 1 | Token-aware execution | S4-01, S4-02, S4-04 | 6h |
| Week 2 | Context enforcement + Eval framework | S4-03, S4-05 | 8h |
| Week 3 | Benchmarks + Prompt optimization | S4-06, S4-07, S4-09, S4-10 | 12h |
| Week 4 | Model comparison + Prompt loop + Snapshots | S4-08, S4-11, S4-12 | 8h |
| **Total** | | **12 tasks** | **34h** |

### 4.5 Success Criteria for Sprint 4

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Token counting accuracy | ±5% of tiktoken | Compare count_tokens() vs API-reported usage |
| Context window overflow | 0 occurrences | No LLMResponseError from token limit |
| Routing accuracy | ≥80% domain, ≥85% tier | Eval benchmark results |
| Task completion (mocked) | ≥90% | End-to-end eval results |
| Prompt variant adoption | ≥1 variant with 10+ impressions | PromptOptimizer.get_variant_performance() |
| Prompt drift detection | 0 silent drifts | Snapshot test pass rate |
| Model cost visibility | 100% calls tracked | CostAnalytics records match LLMClient calls |
| Sprint 4 tests passing | 1205+ (no regressions) | pytest |

---

## 5. STRATEGIC RECOMMENDATIONS

### 5.1 Immediate (Sprint 4)

1. **Token counting is the highest-ROI investment.** Without it, we're flying blind on context window limits and cost estimation. The current post-hoc tracking is necessary but insufficient.

2. **Evaluation benchmarks unlock data-driven decisions.** We have 5 providers and 3 tiers but no measurement of which combination works best for which task types. The routing benchmark (S4-06) will immediately reveal whether our keyword-based domain detection is accurate.

3. **Prompt optimization should be automated, not manual.** The PromptOptimizer infrastructure is built but not wired in. Connecting it to the execution loop (S4-10, S4-11) creates a self-improving system.

### 5.2 Medium-Term (Post-Sprint 4)

1. **ML-enhanced routing calibration.** Use TaskExecutionRecord data to train a real classifier for complexity scoring instead of static heuristics. The `ml/` package has the infrastructure; it needs data.

2. **Cross-provider quality benchmarking.** Run standardized evals monthly across all providers. Track quality/cost/latency tradeoffs. Feed results back into tier configuration.

3. **Context compression for long-running agents.** As agent tasks grow in complexity, conversation histories will exceed context windows. Implement summarization-based truncation.

### 5.3 Long-Term (Q3-Q4 2026)

1. **Embedding-based routing.** Replace keyword heuristics with embedding similarity for domain detection. The EmbeddingEngine is built; it just needs to be applied to routing.

2. **Federated model evaluation.** Share anonymized performance data across deployments to build community benchmarks for model quality.

3. **Autonomous prompt evolution.** Use LLMs to generate prompt variants, evaluate them against benchmarks, and promote winners — a self-improving prompt pipeline.

---

## Appendix A: Architecture Diagram (Textual)

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Hierarchy (127 agents)          │
│  Board → C-Suite → Departments → Specialists            │
└───────────────────────┬─────────────────────────────────┘
                        │ task
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  AgentLoop (ReAct)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Prompts  │→ │   LLM    │→ │  Tools   │──┐           │
│  │ Engine   │  │  Client  │  │  Runner  │  │           │
│  └──────────┘  └────┬─────┘  └──────────┘  │           │
│                     │                       │           │
│              ┌──────┴──────┐                │           │
│              │  ModelRouter │                │           │
│              │  (5 layers)  │                │           │
│              └──────┬──────┘                │           │
│                     │                       │           │
│              ┌──────┴──────┐                │           │
│              │  Complexity  │                │           │
│              │   Scorer     │                │           │
│              └─────────────┘                │           │
│                                             │           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │           │
│  │  Cost    │  │ Circuit  │  │  HITL    │  │           │
│  │ Tracker  │  │ Breaker  │  │  Gate    │  │           │
│  └──────────┘  └──────────┘  └──────────┘  │           │
└─────────────────────────────────────────────┼───────────┘
                                              │
                    ┌─────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────────┐
│              Provider Layer (5 providers)                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐       │
│  │OpenCode │ │ DeepSeek│ │ Ollama  │ │OpenAI  │       │
│  │Big Pickl│ │  chat   │ │llama3.1 │ │gpt-4o  │       │
│  └─────────┘ └─────────┘ └─────────┘ └────────┘       │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Analytics & Intelligence Layer              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │   Cost   │ │  Agent   │ │ Anomaly  │ │ Prompt   │  │
│  │Analytics │ │Analytics │ │Detector  │ │Optimizer │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│  │Performance│ │Predictive│ │ Embedding│               │
│  │ Tracker  │ │ Scaling  │ │ Engine   │               │
│  └──────────┘ └──────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────┘
```

## Appendix B: File Reference

| Module | Key Files | Lines |
|--------|-----------|-------|
| LLM Client | `llm/client.py` | 324 |
| Model Router | `model_router.py` | 551 |
| Cost Tracker | `llm/cost_tracker.py` | 327 |
| Circuit Breaker | `llm/circuit_breaker.py` | 76 |
| JSON Parser | `llm/json_parser.py` | 61 |
| Provider Base | `llm/providers/base.py` | 131 |
| OpenAI Provider | `llm/providers/openai_compatible.py` | 269 |
| Agent Loop | `executor/agent_loop.py` | 366 |
| Prompts Engine | `executor/prompts.py` | 479 |
| Memory Engine | `memory/engine.py` | 578 |
| Complexity Scorer | `ml/complexity.py` | 301 |
| Prompt Optimizer | `ml/prompt_optimizer.py` | 516 |
| Performance Tracker | `ml/performance.py` | 311 |
| Anomaly Detector | `ml/anomaly.py` | 322 |
| Predictive Scaling | `ml/predictive_scaling.py` | 352 |
| Embedding Engine | `ml/embeddings.py` | 211 |
| Cost Analytics | `data/cost_analytics.py` | 511 |
| Agent Analytics | `data/agent_analytics.py` | 311 |
| Models Config | `company/models.yaml` | 119 |
| Routing Policy | `docs/MODEL-ROUTING-POLICY.md` | 71 |
| Prompt Guide | `docs/PROMPT-ENGINEERING-GUIDE.md` | 381 |
| **Total AI-relevant** | | **~6,400** |
