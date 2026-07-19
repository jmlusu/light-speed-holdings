# Architecture Gap Analysis — AI Company Builder

**Author:** Software Architect  
**Date:** 2026-07-19  
**Scope:** End-to-end pipeline from task ingestion through execution, memory, and dashboard

---

## Executive Summary

The AI Company Builder has a solid set of individually well-designed components, but the **integration seams between them are incomplete or broken**. The most critical pattern: components that *should* communicate through shared abstractions instead duplicate file I/O, creating race conditions, lost data, and silent failures. Below are 20 identified gaps ranked by severity.

---

## Gap Registry

### GAP-001 — Executor Bypasses MessageBus, Duplicates File I/O

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `executor/loop.py:124-142`, `orchestrator/message_bus.py` |

**Current State:**  
`Executor._get_pending_tasks()` reads `inbox.json` directly via `json.loads(inbox_path.read_text(...))`. Similarly, `_update_task_status()` and `_complete_task()` write to `inbox.json` directly. The `MessageBus` class exists but is only used for `send_task()` in `_create_subtask_from_record()`.

**Desired State:**  
All inbox reads and writes go through `MessageBus` methods. The bus becomes the single source of truth for task state mutations.

**Risk:**  
Two code paths (MessageBus + Executor) writing the same file without coordination creates race conditions. If the dashboard API and executor run concurrently, writes can clobber each other.

**Fix:**
```
1. Add MessageBus.get_pending_tasks() -> list[Task]
2. Add MessageBus.update_status(task_id, status, result=None)
3. Remove direct file I/O from Executor._get_pending_tasks,
   _update_task_status, _complete_task
4. Make inbox.json writes go through a single write-lock path
```

---

### GAP-002 — No File Locking on Shared JSON/YAML State

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `orchestrator/message_bus.py`, `orchestrator/approval.py`, `dashboard/api.py`, `executor/loop.py` |

**Current State:**  
Four independent components read/write `inbox.json`: MessageBus, Executor, Dashboard API (POST /tasks), and BriefingGenerator. All use raw `json.load/dump` with no file locking. Same applies to `approvals.yaml` (ApprovalGate + Dashboard API) and `escalation.yaml`.

**Desired State:**  
A `FileStore` abstraction with atomic writes (write-to-temp + rename) and optional file locking (`fcntl.flock` on Unix, `msvcrt.locking` on Windows).

**Risk:**  
Concurrent writes from executor + dashboard API cause data loss. The JSON array can be truncated mid-write, losing all pending tasks.

**Fix:**
```
1. Create ai_company/store/file_store.py with atomic JSON/YAML read/write
2. Integrate into MessageBus, ApprovalGate, EscalationManager
3. Dashboard API writes go through MessageBus (see GAP-001)
```

---

### GAP-003 — Tier Rules Not Integrated into ToolRunner

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 2 (Security & Gating) |
| **Files** | `orchestrator/tier_rules.py` (418 lines), `executor/tool_runner.py:24,57` |

**Current State:**  
`ToolRunner.DANGEROUS_TOOLS` is a hardcoded set `{"write", "execute", "code_interpreter"}`. The HITL gate is binary: approve or deny. Meanwhile, `tier_rules.py` implements a sophisticated 5-tier classification system with path sensitivity, command analysis, and seniority-based de-escalation — **none of which is used**.

**Desired State:**  
ToolRunner consults `classify_tool_action()` to determine the approval tier. Tier 0-1 actions auto-approve. Tier 2+ go through HITL with tier-specific timeout and approver count.

**Risk:**  
A "write config/README.md" gets the same approval friction as "write src/main.py". A "rm -rf /" command gets the same treatment as "ls". The security posture is weaker than designed.

**Fix:**
```
1. ToolRunner.__init__ takes an optional TierClassifier
2. In run_plan(), call classify_tool_action() instead of checking DANGEROUS_TOOLS
3. Pass tier info to HITLGate for tier-aware approval
4. HITLGate checks TIER_CONFIG[tier].required_approvers and timeout
```

---

### GAP-004 — HITL Gate Blocks Executor Thread with Busy Wait

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 2 (Security & Gating) |
| **Files** | `executor/hitl_gate.py:54-61` |

**Current State:**  
`HITLGate.request_and_wait()` runs a `while datetime.now() < deadline: time.sleep(self.poll_interval)` loop. This blocks the entire executor thread for up to 30 minutes per approval. Since the executor processes tasks sequentially in `tick()`, a single pending approval freezes all task processing.

**Desired State:**  
Non-blocking approval flow. The executor marks the task as "awaiting_approval", yields, and resumes when the approval is resolved (via polling or event).

**Risk:**  
A single HITL request freezes the entire executor pipeline. If the executor runs in a loop (`start()`), it can't process any other tasks while waiting.

**Fix:**
```
1. Add TaskStatus.AWAITING_APPROVAL
2. HITLGate.request() creates the request and returns immediately
3. Executor._process_task checks task status; if awaiting_approval,
   skip and process next task
4. Separate poll loop checks for resolved approvals and resumes tasks
```

---

### GAP-005 — Memory Engine Completely Disconnected from Execution Pipeline

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 3 (Memory Integration) |
| **Files** | `memory/engine.py` (182 lines), `executor/loop.py`, `executor/agent_loop.py` |

**Current State:**  
`MemoryEngine` with 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate) is fully implemented but **nothing in the executor pipeline writes to or reads from it**. Task completion doesn't create episodic memories. Agent decisions don't create procedural memories. The memory is orphaned.

**Desired State:**  
- After task completion: `memory.store("episodic", ...)` with task summary, agent, outcome
- Before task execution: `memory.recall("semantic", query=task.instruction)` for context
- Periodic consolidation: `memory.consolidate()` for aggregate insights

**Risk:**  
The system has no institutional memory. Agents can't learn from past successes/failures. Same mistakes repeat.

**Fix:**
```
1. Add MemoryIntegration hook in Executor._process_task:
   - On completion: store episodic memory
   - On failure: store episodic memory with error context
2. Add memory context assembly in context.py:
   - Before building prompts, recall relevant memories
3. Add periodic consolidation in the executor start() loop
```

---

### GAP-006 — WebSocket Broadcast Functions Never Called

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `dashboard/ws.py:130-145` |

**Current State:**  
`broadcast_kpi_update()` and `broadcast_alert()` are defined but never called from anywhere in the codebase. The WebSocket endpoint accepts connections and handles ping/pong, but there's no mechanism to push data to connected clients.

**Desired State:**  
The executor, approval gate, and escalation manager push events to connected dashboard clients when state changes occur.

**Risk:**  
The WebSocket connection is useless. Clients connect but never receive data. Dashboard must poll REST endpoints instead.

**Fix:**
```
1. Add event bus or callback mechanism in Executor/ApprovalGate
2. On task completion/failure: broadcast_kpi_update()
3. On approval requested: broadcast_alert({"type": "approval_needed", ...})
4. On escalation: broadcast_alert({"type": "escalation", ...})
5. For async integration: use asyncio event queue or a lightweight
   pub/sub (e.g., asyncio.Queue per ConnectionManager)
```

---

### GAP-007 — Scheduler Never Integrated into Executor Loop

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 3 (Autonomous Coordination) |
| **Files** | `orchestrator/scheduler.py` (80 lines), `executor/loop.py` |

**Current State:**  
`Scheduler.get_pending_tasks()` returns tasks whose `next_run <= now`. However, the executor's `tick()` method only processes tasks from `inbox.json`. The scheduler is never called from the executor loop. Scheduled tasks exist in YAML but are never triggered.

**Desired State:**  
`Executor.tick()` checks the scheduler for due tasks and injects them into the inbox.

**Risk:**  
Autonomous cycles (daily briefings, periodic reports, recurring tasks) never execute. The "autonomous coordination" phase is non-functional.

**Fix:**
```
1. In Executor.__init__: self.scheduler = Scheduler()
2. At start of tick(): check self.scheduler.get_pending_tasks()
3. For each due scheduled task: create Task from task_template, send via bus
4. After execution: self.scheduler.mark_completed(task_id)
```

---

### GAP-008 — Escalation Events Never Persisted

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 3 (Autonomous Coordination) |
| **Files** | `orchestrator/escalation.py:125-144` |

**Current State:**  
`EscalationManager.trigger_escalation()` appends events to `self.events` (in-memory list) but `_save_config()` only persists `self.rules`, not `self.events`. Events are lost on process restart. The dashboard reads events from `escalation.yaml`, but the manager never writes them there.

**Desired State:**  
Events are persisted to `escalation.yaml` alongside rules. On load, events are restored from the file.

**Risk:**  
All escalation history vanishes on restart. Dashboard shows empty escalations after restart even though they occurred. Postmortem creation loses context.

**Fix:**
```
1. _save_config(): persist both rules AND events
2. _load_config(): load both rules AND events
3. Add event archival (move resolved events to a separate file after N days)
```

---

### GAP-009 — CostTracker In-Memory Accumulators Lost on Restart

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 2 (Security & Gating) |
| **Files** | `llm/cost_tracker.py:104-107` |

**Current State:**  
`CostTracker._daily_cost` and `_task_costs` are plain dicts initialized empty each time. The JSONL log file persists records, but `check_budget()` reads from the in-memory dicts. After restart, budget enforcement resets to zero.

**Desired State:**  
On initialization, `CostTracker` replays the JSONL log to rebuild in-memory accumulators. Or: daily/task budgets are computed from the log on each check.

**Risk:**  
Budget enforcement is ineffective across restarts. A user could restart the process to bypass budget limits.

**Fix:**
```
1. Add _rebuild_accumulators() in __init__
2. Read cost_log.jsonl and sum costs by day and task_id
3. This is O(n) in log size but acceptable for single-user
```

---

### GAP-010 — Dashboard CORS Allows All Origins with No Authentication

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 2 (Security & Gating) |
| **Files** | `dashboard/app.py:20-27`, `dashboard/api.py` |

**Current State:**  
`allow_origins=["*"]` with `allow_credentials=True`. No authentication middleware. Anyone on the network can create tasks, approve requests, and view all company data. The dashboard API writes directly to shared files.

**Desired State:**  
At minimum: restrict CORS to known origins. Add API key or session-based auth for write endpoints. Add rate limiting.

**Risk:**  
In a multi-user or network-exposed deployment, any client can manipulate tasks and approvals. The CEO dashboard becomes an attack surface.

**Fix:**
```
1. Make CORS origins configurable via environment variable
2. Add API key middleware for POST/DELETE endpoints
3. Add rate limiting (slowapi or similar)
4. For Sprint 3+: add proper auth (OAuth2 or API key rotation)
```

---

### GAP-011 — Dashboard API Reads Files Directly, Bypasses MessageBus

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `dashboard/api.py:62-63, 166, 174-190` |

**Current State:**  
`POST /api/tasks` reads `inbox.json`, appends a task, and writes it back — all outside of MessageBus. `GET /api/tasks` reads the file directly. This creates a second write path alongside MessageBus and Executor.

**Desired State:**  
All task operations go through MessageBus. Dashboard API uses `bus.get_inbox()`, `bus.send_task()`, etc.

**Risk:**  
Race condition: dashboard creates a task at the same moment executor is updating task status. One write clobbers the other.

**Fix:**
```
1. Inject MessageBus instance into the API router (via FastAPI dependency)
2. Replace _load_json(".opencode/inbox.json") with bus.get_inbox()
3. Replace direct file writes with bus.send_task() / bus.update_status()
```

---

### GAP-012 — AgentLoop Hardcodes Priority in _call_llm

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `executor/agent_loop.py:277` |

**Current State:**  
`self.llm.router.resolve(priority="medium")` hardcodes "medium" regardless of the actual task priority passed to `run()`. A CRITICAL task gets routed to the same model tier as a LOW task.

**Desired State:**  
The task's actual priority is forwarded to the model router for proper tier resolution.

**Risk:**  
High-priority tasks don't get escalated to more capable models. Cost optimization opportunities are missed.

**Fix:**
```
1. Store priority as instance variable or pass through to _call_llm
2. Replace: route = self.llm.router.resolve(priority="medium")
   With:    route = self.llm.router.resolve(priority=self._current_priority)
```

---

### GAP-013 — KPI Collector Only Implements Engineering Department

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 4 (Dashboard Completeness) |
| **Files** | `dashboard/kpi_collector.py:90-101`, `dashboard/kpis/` |

**Current State:**  
`collect_all_kpis()` hardcodes `engineering` as the only department. The `kpis/` directory contains 7 department modules (`engineering.py`, `finance.py`, `hr.py`, `legal.py`, `marketing.py`, `sales.py`, `customer_success.py`) but only engineering is wired in.

**Desired State:**  
`collect_all_kpis()` dynamically discovers and calls all department collectors.

**Risk:**  
Dashboard shows incomplete data. 6 of 7 departments have no live KPIs despite the collectors being implemented.

**Fix:**
```
1. Add a registry pattern: DEPARTMENT_COLLECTORS dict
2. collect_all_kpis() iterates over registered collectors
3. Each department module registers its collector function
```

---

### GAP-014 — BriefingGenerator Uses Private MessageBus Method

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `orchestrator/briefing.py:37` |

**Current State:**  
`self.bus._load_tasks()` accesses a private method of MessageBus. If MessageBus internals change, this breaks silently.

**Desired State:**  
BriefingGenerator uses `MessageBus.get_inbox()` or a new public `get_all_tasks()` method.

**Risk:**  
Fragile coupling to MessageBus internals. Minor but a code quality issue.

**Fix:**
```
1. Add MessageBus.get_all_tasks() -> list[Task] as public API
2. Or: refactor BriefingGenerator to use get_inbox(agent_id) per agent
```

---

### GAP-015 — LLM Client execute_task Retry Logic Has Provider Chain Bug

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 2 (Security & Gating) |
| **Files** | `llm/client.py:94-114` |

**Current State:**  
The outer loop is `for attempt in range(1, max_retries + 1)` and the inner loop iterates `provider_chain`. On a successful JSON parse, it returns. On invalid JSON, the `break` at line 111 exits the inner loop and the outer loop continues — restarting the provider chain from the beginning. This means retry attempts don't cycle through providers as intended; they always start from provider 0.

**Desired State:**  
Retries should cycle through providers round-robin, or at minimum try different providers on subsequent attempts.

**Risk:**  
If provider 0 consistently returns invalid JSON, all 5 retries hit the same provider. Fallback to other providers doesn't happen across retries.

**Fix:**
```
1. Use a single flat loop with a provider index that advances:
   for attempt in range(max_retries):
       provider_idx = attempt % len(provider_chain)
       provider_id, model = provider_chain[provider_idx]
```

---

### GAP-016 — ToolRunner Execute Uses shell=True

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 2 (Security & Gating) |
| **Files** | `executor/tool_runner.py:124` |

**Current State:**  
`subprocess.run(command, shell=True, ...)` allows shell injection. An LLM could craft a command like `"; rm -rf / #"` that bypasses path-based security checks. The tier_rules have command patterns but aren't integrated (GAP-003).

**Desired State:**  
Use `subprocess.run(shlex.split(command), shell=False)` or validate the command against an allowlist before execution.

**Risk:**  
Shell injection vulnerability. An adversarial or hallucinating LLM could execute arbitrary commands on the host.

**Fix:**
```
1. Parse command with shlex.split() instead of shell=True
2. Add command allowlist validation (allowlisted binaries + args)
3. Integrate with tier_rules for dangerous command detection (GAP-003)
```

---

### GAP-017 — No Task Timeout or Dead Letter Queue

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 3 (Autonomous Coordination) |
| **Files** | `executor/loop.py`, `models/task.py` |

**Current State:**  
Tasks that fail in the agent loop get marked as `FAILED` with an error message. But tasks stuck in `IN_PROGRESS` (e.g., executor crashed mid-task) are never recovered. There's no timeout mechanism and no dead letter queue for permanently failed tasks.

**Desired State:**  
- Stale in_progress tasks (older than N minutes) are reset to pending or moved to a dead letter queue
- A recovery mechanism runs on executor startup

**Risk:**  
If the executor crashes during task processing, tasks remain in `IN_PROGRESS` forever. They're never retried or cleaned up.

**Fix:**
```
1. Add Task.created_at / updated_at timestamps
2. On tick() startup: scan for in_progress tasks older than timeout
3. Move stale tasks to a dead letter queue or retry them
4. Add a "recovery" command in the CLI
```

---

### GAP-018 — No Structured Logging or Audit Trail

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Sprint** | Sprint 4 (Dashboard Completeness) |
| **Files** | Multiple files |

**Current State:**  
Mixed logging: some modules use `logger.info()` (stdlib logging), some use `print()`, some have no logging at all. No structured (JSON) log format. No correlation IDs linking task → agent → tool calls.

**Desired State:**  
Structured JSON logging with correlation IDs. Every task lifecycle event (created, started, tool_call, completed, failed) is logged with consistent fields.

**Risk:**  
Difficult to debug production issues. No audit trail for compliance.

**Fix:**
```
1. Configure structlog or python-json-logger
2. Add task_id as correlation ID in log context
3. Ensure all modules use the logger, not print()
```

---

### GAP-019 — Agent Spec Cards Not Versioned or Validated

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Sprint** | Sprint 4 (Dashboard Completeness) |
| **Files** | `executor/context.py:31-100`, `generator.py` |

**Current State:**  
`parse_agent_spec()` reads `.opencode/agents/{name}.md` with no schema validation. If a generated spec is malformed (missing sections, wrong frontmatter), the parser silently returns an `AgentContext` with empty fields. No validation, no warnings.

**Desired State:**  
Agent spec parsing includes validation. Malformed specs produce warnings. A `validate` CLI command checks all specs against a schema.

**Risk:**  
Silent degradation: an agent with missing mission/responsibilities runs with generic prompts, producing low-quality output without any indication.

**Fix:**
```
1. Add AgentContext.validate() method
2. Log warnings for missing critical fields (mission, responsibilities)
3. Add "ai-company agents validate" CLI command
4. Integrate validation into the generator output
```

---

### GAP-020 — No Integration Tests for End-to-End Pipeline

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Sprint** | Sprint 4 (Quality & Hardening) |
| **Files** | `tests/` directory |

**Current State:**  
Unit tests exist for models and some utilities. No integration tests that exercise the full pipeline: create task → executor picks it up → agent loop runs → tool executes → result saved → dashboard shows it.

**Desired State:**  
At least one integration test that exercises the happy path end-to-end with mocked LLM responses.

**Risk:**  
Integration gaps are caught only in manual testing. Regressions in the pipeline go undetected.

**Fix:**
```
1. Create tests/integration/test_pipeline.py
2. Mock LLMClient to return deterministic ReAct responses
3. Test: MessageBus → Executor → AgentLoop → ToolRunner → Task completion
4. Test: Dashboard API reads completed task correctly
```

---

## Summary Matrix

| Gap ID | Severity | Component | Sprint | Effort |
|--------|----------|-----------|--------|--------|
| GAP-001 | CRITICAL | Executor ↔ MessageBus | Sprint 1 | Medium |
| GAP-002 | CRITICAL | File Store (all shared state) | Sprint 1 | High |
| GAP-003 | HIGH | ToolRunner ↔ Tier Rules | Sprint 2 | Medium |
| GAP-004 | HIGH | HITLGate (blocking) | Sprint 2 | Medium |
| GAP-005 | HIGH | Memory ↔ Executor | Sprint 3 | High |
| GAP-006 | HIGH | WebSocket Broadcast | Sprint 1 | Low |
| GAP-007 | HIGH | Scheduler ↔ Executor | Sprint 3 | Medium |
| GAP-008 | HIGH | Escalation Persistence | Sprint 3 | Low |
| GAP-009 | MEDIUM | CostTracker Persistence | Sprint 2 | Low |
| GAP-010 | MEDIUM | Dashboard Auth/CORS | Sprint 2 | Medium |
| GAP-011 | MEDIUM | Dashboard API ↔ MessageBus | Sprint 1 | Low |
| GAP-012 | MEDIUM | AgentLoop Priority | Sprint 1 | Low |
| GAP-013 | MEDIUM | KPI Collector Wiring | Sprint 4 | Low |
| GAP-014 | LOW | BriefingGenerator API | Sprint 1 | Trivial |
| GAP-015 | MEDIUM | LLM Retry Logic | Sprint 2 | Low |
| GAP-016 | MEDIUM | Shell Injection | Sprint 2 | Medium |
| GAP-017 | MEDIUM | Task Timeout/DLQ | Sprint 3 | Medium |
| GAP-018 | LOW | Structured Logging | Sprint 4 | Medium |
| GAP-019 | LOW | Spec Validation | Sprint 4 | Low |
| GAP-020 | LOW | Integration Tests | Sprint 4 | Medium |

## Recommended Sprint Plan

### Sprint 1 — Foundation Fixes (CRITICAL + HIGH items)
1. GAP-001: Route all inbox I/O through MessageBus
2. GAP-002: Create atomic FileStore abstraction
3. GAP-006: Wire WebSocket broadcast to executor events
4. GAP-011: Dashboard API uses MessageBus
5. GAP-012: Fix priority forwarding in AgentLoop
6. GAP-014: Fix BriefingGenerator private method usage

### Sprint 2 — Security & Gating (MEDIUM security items)
1. GAP-003: Integrate tier rules into ToolRunner
2. GAP-004: Non-blocking HITL gate
3. GAP-009: CostTracker accumulator persistence
4. GAP-010: Dashboard CORS and auth
5. GAP-015: Fix LLM retry provider cycling
6. GAP-016: Remove shell=True from ToolRunner

### Sprint 3 — Autonomous Coordination (HIGH orchestration items)
1. GAP-005: Memory integration into executor pipeline
2. GAP-007: Scheduler integration into executor loop
3. GAP-008: Persist escalation events
4. GAP-017: Task timeout and dead letter queue

### Sprint 4 — Quality & Completeness (LOW + polish items)
1. GAP-013: Wire all KPI department collectors
2. GAP-018: Structured logging with correlation IDs
3. GAP-019: Agent spec validation
4. GAP-020: End-to-end integration tests
