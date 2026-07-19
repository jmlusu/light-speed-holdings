# Integration Architecture — AI Company Builder

> **Owner**: Chief Information Officer (CIO)  
> **Last Updated**: 2026-07-19  
> **Status**: Active Build-Out (Phase 5 — Integration Gap Closure)

This document maps what is **implemented**, what is **partially wired**, and what remains **disconnected**. The goal is to identify the exact integration seams and close them.

---

## 1. Implementation Status Matrix

### 1.1 Module Status

| Module | File | Status | Wired Into Executor? | Tests? | Risk |
|--------|------|--------|---------------------|--------|------|
| **AgentLoop** | `executor/agent_loop.py` (353 lines) | **IMPLEMENTED** — full ReAct loop, budget checks, cost recording, 3-strategy JSON parsing | **NO** — Executor still uses `llm.execute_task()` (single-pass) | Yes | HIGH — core agentic behavior unreachable |
| **CostTracker** | `llm/cost_tracker.py` (289 lines) | **IMPLEMENTED** — JSONL logging, daily/task budgets, per-model pricing, summaries | **NO** — AgentLoop accepts it as `Optional` but Executor never instantiates it | Yes | MEDIUM — costs untracked, no budget enforcement |
| **Executor** | `executor/loop.py` (274 lines) | **IMPLEMENTED** but **BYPASSES** AgentLoop | N/A (is the integration point) | Yes | HIGH — single-pass, no iteration, no cost tracking |
| **MessageBus** | `orchestrator/message_bus.py` (31 lines) | **BASIC** — JSON read/write only | Yes (Executor reads inbox) | Yes | MEDIUM — no atomic writes, no correlation, no backup |
| **ApprovalGate** | `orchestrator/approval.py` (112 lines) | **IMPLEMENTED** — request/approve/reject/expiry, YAML persistence | Yes (via HITLGate) | Yes | LOW — works, but no tier system |
| **HITLGate** | `executor/hitl_gate.py` (77 lines) | **IMPLEMENTED** — blocking poll for dangerous tools | Yes (ToolRunner) | Yes | LOW — blocking design may stall executor |
| **ToolRunner** | `executor/tool_runner.py` (216 lines) | **IMPLEMENTED** — sandboxed execution, security path check | Yes (Executor + AgentLoop) | Yes | LOW — no audit trail |
| **KPICollector** | `dashboard/kpi_collector.py` (115 lines) | **PARTIAL** — engineering only, no live data pipeline | N/A (dashboard) | Partial | MEDIUM — only 1 of 7 depts has live KPIs |
| **Dashboard API** | `dashboard/api.py` (346 lines) | **IMPLEMENTED** — full REST endpoints | N/A (standalone) | Yes | LOW |
| **AuditWriter** | Does not exist | **NOT STARTED** | N/A | No | HIGH — no audit trail for compliance |
| **WebSocket** | `dashboard/ws.py` | Exists (file present) | N/A (dashboard) | Unknown | LOW — non-blocking enhancement |

### 1.2 Dependency Graph (Accurate)

```mermaid
graph TD
    subgraph "IMPLEMENTED — Working"
        MB[MessageBus<br/>basic JSON]
        EXEC[Executor<br/>single-pass]
        LLM[LLM Client<br/>5 providers]
        TR[ToolRunner<br/>sandboxed]
        HITL[HITLGate<br/>blocking poll]
        AG[ApprovalGate<br/>YAML persistence]
        API[Dashboard API<br/>15+ endpoints]
        CT[CostTracker<br/>JSONL + budgets]
        AL[AgentLoop<br/>ReAct pattern]
    end

    subgraph "NOT WIRED"
        AW[AuditWriter<br/>DOES NOT EXIST]
    end

    subgraph "PARTIAL"
        KT[KPICollector<br/>engineering only]
    end

    %% Existing wiring
    EXEC -->|Polls| MB
    EXEC -->|Calls directly| LLM
    EXEC -->|Delegates tools| TR
    TR -->|Dangerous tools| HITL
    HITL -->|Wraps| AG

    %% AgentLoop wiring (exists in code but NOT used by Executor)
    AL -.->|Accepts| LLM
    AL -.->|Accepts| TR
    AL -.->|Accepts| CT
    EXEC -.->|SHOULD delegate to| AL

    %% CostTracker wiring (exists in AgentLoop but Executor skips it)
    CT -.->|Logs from| AL

    %% KPI wiring (partial)
    KT -.->|Reads| MB
    API -.->|Fetches| KT

    %% Missing wiring
    TR -.->|SHOULD log to| AW
    AL -.->|SHOULD log to| AW
```

**Legend**: Solid lines = active wiring. Dashed lines = exists in code but not connected, or does not exist yet.

---

## 2. Integration Gaps (Ordered by Priority)

### GAP 1: Executor → AgentLoop [HIGH RISK]

**Problem**: `Executor._process_task()` (lines 130-186 of `loop.py`) calls `self.llm.execute_task()` directly — a single-pass LLM call that returns one JSON response. The `AgentLoop` class (353 lines) implements multi-turn ReAct with iteration, tool feedback loops, and budget enforcement, but is never invoked.

**Current flow** (broken):
```
Executor._process_task()
  → self.llm.execute_task()       # single LLM call
  → self.runner.run_plan()         # execute tools once
  → mark complete
```

**Required flow** (target):
```
Executor._process_task()
  → AgentLoop.run()
      → iteration 1: LLM → plan → tools → feedback
      → iteration 2: LLM → plan → tools → feedback
      → ...
      → done: LoopResult
  → mark complete
```

**What needs to change in `executor/loop.py`**:
1. Import `AgentLoop` and `LoopConfig`
2. Instantiate `CostTracker` and pass to `AgentLoop`
3. Replace lines 147-172 with:
   ```python
   agent_ctx = parse_agent_spec(task.receiver_id, self.agents_dir)
   loop = AgentLoop(
       llm=self.llm,
       runner=self.runner,
       cost_tracker=self.cost_tracker,
       config=LoopConfig(max_iterations=10),
   )
   result = loop.run(
       agent=agent_ctx,
       user_prompt=user_prompt,
       agent_name=task.receiver_id,
       task_id=task.id,
       priority=task.priority.value,
   )
   ```
4. Map `LoopResult` → existing `_complete_task()` and `_save_artifacts()` calls

**Dependencies**: `executor/context.py` (parse_agent_spec returns `AgentContext`), `executor/prompts.py` (build_system_prompt_typed, build_user_prompt_typed)

**Risk**: **HIGH** — Without this, the system is single-pass only. No tool iteration, no error recovery, no budget enforcement. Every task gets exactly one LLM call + one tool plan execution.

**Estimated effort**: 2-3 hours (surgical edit to `_process_task` + test updates)

---

### GAP 2: No Audit Trail Package [HIGH RISK]

**Problem**: There is no `src/ai_company/audit/` directory. The Integration Architecture references `AuditWriter` as a module to hook into `ToolRunner.run_step()`, but it does not exist. No file write, command execution, or code interpretation is logged to an audit trail.

**Impact**:
- No compliance trail for regulated operations
- Cannot reconstruct what files an agent modified
- No forensic capability after incidents
- Violates the project's own `docs/COMPANY-CONSTITUTION.md` principles

**What needs to exist**:
```
src/ai_company/audit/
  __init__.py
  writer.py          # AuditWriter class — JSONL append to logs/audit/
  models.py          # AuditEvent Pydantic model
  query.py           # Search/filter audit events
```

**Integration points**:
1. `executor/tool_runner.py` → after `_execute_tool()` returns, call `AuditWriter.log_event()`
2. `executor/agent_loop.py` → log each LLM call (model, tokens, cost) as an audit event
3. `orchestrator/approval.py` → log approval requests and decisions
4. `orchestrator/message_bus.py` → log task sends and status changes

**Risk**: **HIGH** — No auditability means no trust, no compliance, no incident forensics. Blocks any enterprise or regulated use case.

**Estimated effort**: 4-6 hours (new package + 4 integration hooks + tests)

---

### GAP 3: CostTracker Not Instantiated [MEDIUM RISK]

**Problem**: `AgentLoop.__init__()` accepts `cost_tracker: CostTracker | None = None` and has full logic to check budgets and record usage (lines 144-180). But since Executor never creates a `CostTracker` instance and never passes one to `AgentLoop`, all cost tracking is dead code.

**What needs to change**:
1. In `Executor.__init__()`, add:
   ```python
   from ai_company.llm.cost_tracker import CostTracker
   self.cost_tracker = CostTracker(results_dir="results")
   ```
2. Pass `self.cost_tracker` when constructing `AgentLoop` in `_process_task()`

**Risk**: **MEDIUM** — Costs accumulate without tracking. No budget enforcement. Could lead to runaway LLM spend without visibility.

**Estimated effort**: 30 minutes

---

### GAP 4: MessageBus Lacks Response Correlation [MEDIUM RISK]

**Problem**: The current `MessageBus` (31 lines) is a thin JSON read/write wrapper. It has no concept of:
- **Response correlation**: When Agent A sends a task to Agent B, there's no mechanism for Agent A to wait for or receive the response
- **Atomic writes**: Multiple concurrent writes can corrupt `inbox.json`
- **Backup/recovery**: No `.bak` file or snapshot mechanism
- **Task status transitions**: No state machine enforcement (pending → in_progress → completed/failed)

**Current code** (entire class is 31 lines):
```python
class MessageBus:
    def send_task(self, task): ...       # append to JSON
    def get_inbox(self, agent_id): ...   # filter by receiver
    def get_sent(self, agent_id): ...    # filter by sender
```

**What the Integration Architecture spec requires**:
- Atomic writes (write to `.tmp` then `os.rename`)
- Backup file (`inbox.json.bak`)
- Response correlation (task_id → response mapping)
- State machine enforcement

**Risk**: **MEDIUM** — Concurrent executor ticks or multiple agents writing could corrupt the inbox. No response correlation means delegation is fire-and-forget.

**Estimated effort**: 3-4 hours

---

### GAP 5: Approval Tier System [MEDIUM RISK]

**Problem**: The `ApprovalGate` treats all actions uniformly — every approval request has the same process regardless of whether it's reading a file or deploying to production. The 3 approval UX spec documents (`APPROVAL-UX-SPEC.md`, `APPROVAL-DASHBOARD-UI.md`, `APPROVAL-CLI-COMMANDS.md`) define a 5-tier system:

| Tier | Actions | Approval Required | Timeout |
|------|---------|-------------------|---------|
| 1 - Auto | read, list, grep | None | N/A |
| 2 - Soft | write (non-critical) | Optional warning | None |
| 3 - Gate | write (critical), execute | Single approval | 30 min |
| 4 - Dual | deploy, financial | Two approvals | 60 min |
| 5 - Board | legal, budget >$1000 | Board vote | 24 hours |

**Current state**: `ToolRunner.DANGEROUS_TOOLS = {"write", "execute", "code_interpreter"}` — all treated as Tier 3 with single approval. No tier classification exists in the data model.

**What needs to change**:
1. Add `tier: int` field to `ApprovalRequest`
2. Add tier lookup logic in `ToolRunner` or `AgentLoop`
3. Implement dual-approval logic for Tier 4
4. Wire tier config to `company/approvals.yaml`

**Risk**: **MEDIUM** — All dangerous actions get the same friction. Low-risk writes block the executor unnecessarily. High-risk actions (deploy, financial) don't get sufficient protection.

**Estimated effort**: 4-5 hours

---

### GAP 6: HITLGate Blocking Design [LOW-MEDIUM RISK]

**Problem**: `HITLGate.request_and_wait()` uses `time.sleep()` polling in a blocking loop (lines 55-62 of `hitl_gate.py`). If a human doesn't respond within `timeout_minutes`, the entire executor is stalled for that task.

**Impact**:
- Executor `tick()` blocks on a single task waiting for approval
- Other tasks in the same batch are delayed
- No async/await pattern, no callback mechanism

**Risk**: **LOW-MEDIUM** — Works for low-volume, but becomes a bottleneck under load. Not blocking until the system scales beyond single-task processing.

**Estimated effort**: 2-3 hours (refactor to async or callback pattern)

---

### GAP 7: Missing Department SOPs [LOW RISK]

**Problem**: The project has 4 SOPs out of 8 required:
- ✅ `docs/sop-incident-response.md`
- ✅ `docs/sop-deployment.md`
- ✅ `docs/sop-hr-onboarding.md`
- ✅ `docs/sop-budget-approval.md`
- ❌ `docs/sop-legal-review.md`
- ❌ `docs/sop-sales-pipeline.md`
- ❌ `docs/sop-customer-escalation.md`
- ❌ `docs/sop-data-retention.md`

**Risk**: **LOW** — SOPs are documentation, not code. They don't block functionality but are needed for operational completeness and the 8-department coverage goal.

**Estimated effort**: 1-2 hours per SOP (template-driven, low complexity)

---

### GAP 8: KPI Collector — Only Engineering Department [LOW RISK]

**Problem**: `kpi_collector.py` only implements `collect_engineering_kpis()`. The KPI config (`company/config/kpis.yaml`) defines KPIs for 7 departments, but only engineering has a collector function. The `/api/kpis/live` endpoint returns only engineering data.

**Risk**: **LOW** — Dashboard shows partial data. Non-blocking for functionality but incomplete for CEO visibility.

**Estimated effort**: 2-3 hours (6 more collector functions, following the engineering pattern)

---

## 3. Data Flow Diagrams

### 3.1 Current Task Lifecycle (Single-Pass — What Actually Runs)

```mermaid
sequenceDiagram
    participant User
    participant MB as MessageBus
    participant Exec as Executor
    participant LLM as LLM Client
    participant TR as ToolRunner
    participant HITL as HITLGate

    User->>MB: send_task(instruction)
    MB->>Exec: tick() polls inbox.json
    Exec->>LLM: execute_task(instruction)
    LLM-->>Exec: {plan, result}
    Exec->>TR: run_plan(plan, hitl_gate)
    loop Each dangerous tool step
        TR->>HITL: request_and_wait()
        HITL-->>TR: approved/denied
    end
    TR-->>Exec: step_results
    Exec->>MB: update_task(COMPLETED)
    Note over Exec: NO iteration. NO cost tracking. NO audit.
```

### 3.2 Target Task Lifecycle (Agentic Loop — What Should Run)

```mermaid
sequenceDiagram
    participant User
    participant MB as MessageBus
    participant Exec as Executor
    participant AL as AgentLoop
    participant LLM as LLM Provider
    participant TR as ToolRunner
    participant CT as CostTracker
    participant AW as AuditWriter

    User->>MB: send_task(instruction)
    MB->>Exec: tick() polls inbox.json
    Exec->>AL: run(agent, prompt, task_id)

    loop Agentic Iteration (Max 10)
        AL->>CT: check_budget(task_id)
        CT-->>AL: allowed/denied
        AL->>LLM: chat(system, user)
        LLM-->>AL: ChatResponse (model, tokens)
        AL->>CT: record_usage(model, tokens)
        AL->>TR: run_plan(plan)
        TR->>AW: log_event(tool, args, result)
        TR-->>AL: step_results
        AL->>AW: log_event(iteration_complete)
        Note over AL: If done=false and plan non-empty: continue
    end

    AL-->>Exec: LoopResult (response, iterations, cost)
    Exec->>MB: update_task(COMPLETED, result)
    Exec->>AW: log_event(task_completed)
```

### 3.3 Cost Tracking Flow (Current vs Target)

**Current**: CostTracker exists but is never instantiated. No data flows.

**Target**:
```mermaid
flowchart LR
    A[AgentLoop._call_llm] -->|model, tokens| B[CostTracker.record_usage]
    B -->|append| C[results/cost_log.jsonl]
    B -->|in-memory| D[daily/task accumulators]
    D -->|check| E[budget enforcement]
    C -->|read| F[Dashboard /api/costs]
    F -->|display| G[CEO Browser]
```

---

## 4. Configuration Hierarchy

| Setting | Source | Override | Default | Status |
|---------|--------|----------|---------|--------|
| **LLM Budgets** | `company/models.yaml` | `LLM_BUDGET_LIMIT` (env) | None (Unlimited) | Code exists, not wired |
| **Approval Tiers** | `company/approvals.yaml` | CLI Flag | All Tier 3 | Design specs exist, not implemented |
| **KPI Targets** | `company/config/kpis.yaml` | None | Historical Average | Config exists, collector partial |
| **Audit Retention** | Code Constant | `AUDIT_RETENTION_DAYS` (env) | 30 days | Not implemented |
| **Agent Max Iterations** | `LoopConfig.max_iterations` | `AGENT_MAX_LOOPS` (env) | 10 | Code exists, not wired |
| **WS Heartbeat** | Code Constant | None | 30s | Exists in ws.py |

---

## 5. Error Handling Strategy

### 5.1 LLM Failure Chain (IMPLEMENTED in AgentLoop + LLMClient)
1. **AgentLoop fallback**: Iterates through provider chain in tier (lines 281-302 of `agent_loop.py`)
2. **LLMClient retry**: Up to 5 attempts for JSON parse failures (lines 95-121 of `client.py`)
3. **Escalate**: Task marked `failed` with detailed error message
4. **Budget guard**: `CostTracker.check_budget()` stops iteration before next LLM call

### 5.2 Tool Failure Chain (PARTIALLY IMPLEMENTED)
1. **ToolRunner**: Catches exceptions per step (lines 78-84 of `tool_runner.py`)
2. **AgentLoop feedback**: Tool errors are fed back to LLM via `build_iteration_feedback()` ✅
3. **HITL denial**: Tool denied → continues with remaining steps ✅
4. **Audit trail**: NOT IMPLEMENTED — no logging of tool failures

### 5.3 MessageBus Integrity (SPECIFIED BUT NOT IMPLEMENTED)
1. **Atomic Write**: NOT IMPLEMENTED — direct `write_text()` with no temp file
2. **Fallback**: NOT IMPLEMENTED — no `.bak` file mechanism
3. **Concurrent access**: NOT PROTECTED — multiple processes could corrupt JSON

### 5.4 KPI Collector Failure (IMPLEMENTED for engineering)
1. **Isolation**: `collect_all_kpis()` calls per-department functions ✅
2. **Partial Return**: Engineering-only for now; other departments return empty
3. **Error handling**: Not yet needed (only one collector exists)

---

## 6. Risk Summary

| # | Gap | Risk | Impact if Not Fixed | Effort to Fix | Dependencies |
|---|-----|------|---------------------|---------------|-------------|
| 1 | Executor → AgentLoop not wired | **HIGH** | Single-pass only, no iteration, no budget enforcement | 2-3h | None — surgical edit |
| 2 | No audit trail package | **HIGH** | No compliance, no forensics, no file change tracking | 4-6h | None — new package |
| 3 | CostTracker not instantiated | **MEDIUM** | Untracked LLM spend, no budget enforcement | 30min | None — one constructor call |
| 4 | MessageBus lacks correlation | **MEDIUM** | Fire-and-forget delegation, possible JSON corruption | 3-4h | None — rewrite needed |
| 5 | No approval tier system | **MEDIUM** | Uniform friction for all actions | 4-5h | Design specs exist |
| 6 | HITLGate blocking design | **LOW-MED** | Executor stalls on pending approvals | 2-3h | Async refactor |
| 7 | Missing department SOPs (4/8) | **LOW** | Incomplete operational docs | 4-8h total | None — docs only |
| 8 | KPI collector partial (1/7) | **LOW** | Dashboard shows only engineering | 2-3h | None — follows pattern |

### Recommended Implementation Order

1. **GAP 3** (CostTracker instantiation) — 30 min, unblocks GAP 1
2. **GAP 1** (Wire AgentLoop into Executor) — 2-3h, core value unlock
3. **GAP 2** (Audit trail package) — 4-6h, compliance foundation
4. **GAP 4** (MessageBus hardening) — 3-4h, reliability
5. **GAP 5** (Approval tier system) — 4-5h, security refinement
6. **GAP 7** (Remaining SOPs) — 4-8h, can run in parallel
7. **GAP 8** (KPI collectors) — 2-3h, can run in parallel
8. **GAP 6** (HITL async refactor) — 2-3h, optimization

**Total remaining integration work**: ~22-32 hours across all gaps.
