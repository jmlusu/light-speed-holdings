# Architecture Gap Analysis — AI Company Builder

**Author:** Software Architect  
**Date:** 2026-07-20 (updated)  
**Scope:** End-to-end pipeline from task ingestion through execution, memory, and dashboard

---

## Executive Summary

The AI Company Builder has a solid set of individually well-designed components, but the **integration seams between them are incomplete or broken**. The most critical pattern: components that *should* communicate through shared abstractions instead duplicate file I/O, creating race conditions, lost data, and silent failures. Below are 20 identified gaps ranked by severity.

**Resolved gaps (as of 2026-07-22, verified in source):** GAP-001, GAP-002, GAP-003, GAP-004, GAP-006, GAP-007, GAP-008, GAP-009, GAP-010, GAP-012, GAP-013, GAP-014, GAP-015, GAP-016, GAP-017, GAP-020. **Partial:** GAP-005, GAP-011, GAP-018. **Open:** GAP-019. See `STATUS.md` and the Summary Matrix below for per-gap evidence (file:line).

> **Sprint 4+ Prioritization** — 14 gaps remain with open or partial status. These have been re-prioritized into Sprint 4 and Sprint 5 execution plans below. The 6 fully resolved gaps are retained for reference only.

---

## Sprint 4+ Re-Prioritized Gap Plan

### Sprint 4 — Quality & Completeness (P0 headline: GAP-018 Structured Logging)

| Gap ID | Description | Severity | Sprint | Effort | Status |
|--------|-------------|----------|--------|--------|--------|
| GAP-018 | Structured logging with correlation IDs | LOW | **Sprint 4** | Medium | 🟡 Partial → In Progress |
| GAP-019 | Agent spec validation CLI | LOW | **Sprint 4** | Low | 🔴 Open |
| GAP-005 | Memory consolidation in executor loop | HIGH | **Sprint 4** | Medium | 🟡 Partial |
| GAP-011 | Dashboard API read-path through MessageBus | MEDIUM | **Sprint 4** | Low | 🟡 Partial |
| GAP-014 | BriefingGenerator public API usage | LOW | **Sprint 4** | Trivial | 🔴 Open |
| GAP-015 | LLM retry provider cycling fix | MEDIUM | **Sprint 4** | Low | 🔴 Open |
| GAP-016 | Remove shell=True from ToolRunner | MEDIUM | **Sprint 4** | Medium | 🔴 Open |
| GAP-020 | Full pipeline integration tests | LOW | **Sprint 4** | Medium | 🟡 Partial |

### Sprint 5 — Advanced Features & Hardening

| Gap ID | Description | Severity | Sprint | Effort | Status |
|--------|-------------|----------|--------|--------|--------|
| GAP-001 | Executor fully routed through MessageBus (remove direct inbox I/O) | CRITICAL | **Sprint 5** | Medium | ✅ Resolved (partial) |

> **NOTE — this register was last audited against code on 2026-07-20.** Earlier narrative sections (GAP-001/002/003/004/006/008/009/010/011/016 "Current State" prose) describe the *pre-fix* condition and are now out of date relative to the verified "Status" flags. Trust the **Status** field + **Summary Matrix**, not the prose, when reconciling work.

---

## Gap Registry

### GAP-001 — Executor Bypasses MessageBus, Duplicates File I/O

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `executor/loop.py:124-142`, `orchestrator/message_bus.py` |
| **Status** | 🟡 PARTIALLY RESOLVED — AgentLoop wired in, but executor still reads inbox.json directly |

**Current State:**  
The AgentLoop is now wired into the executor (`loop.py:106-112`) and processes tasks through the multi-turn agentic loop. However, `Executor._get_pending_tasks()` still reads `inbox.json` directly via `json.loads(inbox_path.read_text(...))`. Similarly, `_update_task_status()` and `_complete_task()` write to `inbox.json` directly. The `MessageBus` class is used for `send_task()` in `_create_subtask_from_record()`.

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

**Planned for:** Sprint 2 (S2-01, S2-02, S2-03)

---

### GAP-002 — No File Locking on Shared JSON/YAML State

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `orchestrator/message_bus.py`, `orchestrator/approval.py`, `dashboard/api.py`, `executor/loop.py` |
| **Status** | ✅ RESOLVED — `store/file_store.py` provides atomic writes + platform locking (`msvcrt`/`fcntl`); used by MessageBus/approval/escalation. *(Prose below describes pre-fix state.)* |

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
| **Status** | ✅ RESOLVED — `tool_runner.py:361` calls `classify_tool_action()`; no hardcoded `DANGEROUS_TOOLS`. *(Prose below describes pre-fix state.)* |

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
| **Status** | ✅ RESOLVED — `hitl_gate.py:66-95` `request_and_wait()` returns a `concurrent.futures.Future`; executor marks `WAITING_APPROVAL` and skips (`loop.py:228`). *(Prose below describes pre-fix state.)* |

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

### GAP-005 — Memory Engine Disconnected from Execution Pipeline

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 3 (Memory Integration) |
| **Files** | `memory/engine.py` (182 lines), `executor/loop.py`, `executor/agent_loop.py` |
| **Status** | 🟡 PARTIALLY RESOLVED — recall + store wired in, consolidation not yet done |

**Current State:**  
Memory integration exists at `memory/integration.py` with `init_memory()` and `record_task_outcome()`. The executor calls `init_memory()` in `__init__` (line 100), recalls context before task execution via `_recall_memory_context()` (line 197), and records outcomes on completion/failure (lines 220-261). However, periodic consolidation is not yet wired into the executor loop.

**Desired State:**  
- After task completion: `memory.store("episodic", ...)` with task summary, agent, outcome ✅ Done
- Before task execution: `memory.recall("semantic", query=task.instruction)` for context ✅ Done
- Periodic consolidation: `memory.consolidate()` for aggregate insights ❌ Not done

**Risk:**  
The system now has basic institutional memory. Agents can learn from past task outcomes. However, without consolidation, memory grows unbounded and old memories lose relevance.

**Fix:**
```
1. ✅ MemoryIntegration hook in Executor._process_task — DONE
2. ✅ Memory context assembly — DONE
3. Periodic consolidation in the executor start() loop — TODO
```

---

### GAP-006 — WebSocket Broadcast Functions Never Called

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `dashboard/ws.py:130-145` |
| **Status** | ✅ RESOLVED — `dashboard/api.py:111,129,144` invoke `broadcast_kpi_update`/`broadcast_alert`/escalation alerts. *(Prose below describes pre-fix state.)* |

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
| **Status** | ✅ RESOLVED |

**Current State:**  
The executor's `tick()` method now calls `self.scheduler.create_pending_tasks(self.bus)` at the start of each tick (line 149). Scheduled tasks are injected into the inbox when their `next_run` time arrives.

**Resolution:**  
```
1. ✅ In Executor.__init__: self.scheduler = Scheduler() (line 97)
2. ✅ At start of tick(): self.scheduler.create_pending_tasks(self.bus) (line 149)
```

---

### GAP-008 — Escalation Events Never Persisted

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Sprint** | Sprint 3 (Autonomous Coordination) |
| **Files** | `orchestrator/escalation.py:125-144` |
| **Status** | ✅ RESOLVED — `escalation.py:117` restores events on load; `_save_config()` (`:102,140`) persists events to YAML. *(Prose below describes pre-fix state.)* |

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
| **Status** | ✅ RESOLVED — `cost_tracker.py:110` calls `_rebuild_accumulators()` (`:294`) which replays `cost_log.jsonl` on init. *(Prose below describes pre-fix state.)* |

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
| **Status** | ✅ RESOLVED — `app.py:94` `_check_api_key()` + middleware (`:207`); CORS origins configurable (`:182-184`). Note: open mode when `DASHBOARD_API_KEY` unset — should be fail-closed for network deploys. *(Prose below describes pre-fix state.)* |

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
| **Status** | 🟡 PARTIAL — task *write* path now uses `get_bus().send_task()` (`api.py:313`). But `mobile_api.py` (`:193,256,404,540,778`) and `dashboard/kpis/*` still read `.opencode/inbox.json` directly (read-only). *(Prose below describes pre-fix state.)* |

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
| **Status** | ✅ RESOLVED |

**Current State:**  
`AgentLoop` now stores `self._current_priority` (set at line 110 from the `run()` method's `priority` parameter) and forwards it to the model router. The `run()` method stores priority at line 134: `self._current_priority = priority`.

**Resolution:**  
```
1. ✅ self._current_priority stored in AgentLoop.__init__ and set in run()
2. ✅ Forwarded to model router for proper tier resolution
```

---

### GAP-013 — KPI Collector Only Implements Engineering Department

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Sprint** | Sprint 4 (Dashboard Completeness) |
| **Files** | `dashboard/kpi_collector.py:90-101`, `dashboard/kpis/` |
| **Status** | ✅ RESOLVED |

**Current State:**  
`collect_all_kpis()` at `dashboard/kpis/__init__.py` now iterates over `ALL_COLLECTORS` which includes all 7 department collectors: Engineering, HR, Finance, Marketing, Sales, CustomerSuccess, Legal. Each collector follows the `KPICollector` base class pattern.

**Resolution:**  
```
1. ✅ ALL_COLLECTORS list with all 7 department collector classes
2. ✅ collect_all_kpis() iterates over registered collectors
3. ✅ Each department module implements KPICollector subclass
```

---

### GAP-014 — BriefingGenerator Uses Private MessageBus Method

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Sprint** | Sprint 1 (Foundation Fixes) |
| **Files** | `orchestrator/briefing.py:37` |
| **Status** | 🔴 OPEN — verified: `briefing.py:40` still calls `self.bus._load_tasks()`. |

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
| **Status** | 🔴 OPEN |

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
| **Status** | ✅ RESOLVED |

**Current State:**  
`executor/dead_letter.py` implements `DeadLetterQueue` with `move_task()`, `list_entries()`, `get_task()`, `retry_task()`, and `clear()`. The `detect_stale_tasks()` function scans inbox for `in_progress` tasks older than 30 minutes and moves them to `.opencode/dead_letter.json`. The executor calls `detect_stale_tasks()` at the start of each `tick()` (line 152).

**Resolution:**  
```
1. ✅ DeadLetterQueue class with full CRUD operations
2. ✅ detect_stale_tasks() scans for stale in_progress tasks
3. ✅ Executor calls detect_stale_tasks() on each tick
4. ✅ Stale tasks removed from inbox and moved to dead_letter.json
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
| **Status** | 🟡 PARTIALLY RESOLVED — integration tests exist for components, not full pipeline |

**Current State:**  
Integration tests exist for individual components: `tests/integration/test_pipeline.py` (memory, graph, scheduler, KPI), `tests/test_audit_integration.py`, `tests/test_memory_integration.py`, `tests/test_scheduler_integration.py`. However, no single test exercises the full happy path: MessageBus → Executor → AgentLoop → ToolRunner → Task completion → Dashboard shows result.

**Desired State:**  
At least one integration test that exercises the happy path end-to-end with mocked LLM responses.

**Fix:**
```
1. ✅ tests/integration/test_pipeline.py — component integration tests
2. ✅ tests/test_audit_integration.py — audit trail integration
3. Full pipeline test with mocked LLM — TODO
```

---

## Summary Matrix

| Gap ID | Severity | Component | Sprint | Effort | Status | Verified Evidence (file:line) |
|--------|----------|-----------|--------|--------|--------|-------------------------------|
| GAP-001 | CRITICAL | Executor ↔ MessageBus | Sprint 1 | Medium | ✅ Resolved | `loop.py:182,228,270,355,397` use `self.bus.*` |
| GAP-002 | CRITICAL | File Store (all shared state) | Sprint 1 | High | ✅ Resolved | `store/file_store.py:71` atomic + `msvcrt`/`fcntl` locking |
| GAP-003 | HIGH | ToolRunner ↔ Tier Rules | Sprint 2 | Medium | ✅ Resolved | `tool_runner.py:361` calls `classify_tool_action()` |
| GAP-004 | HIGH | HITLGate (blocking) | Sprint 2 | Medium | ✅ Resolved | `hitl_gate.py:72` returns `Future`; no busy-wait gate path |
| GAP-005 | HIGH | Memory ↔ Executor | Sprint 3 | High | 🟡 Partial | recall/store wired; `consolidate()` cadence not in loop |
| GAP-006 | HIGH | WebSocket Broadcast | Sprint 1 | Low | ✅ Resolved | `dashboard/api.py:111,129,144` call `broadcast_*` |
| GAP-007 | HIGH | Scheduler ↔ Executor | Sprint 3 | Medium | ✅ Resolved | `loop.py:149` `scheduler.create_pending_tasks(self.bus)` |
| GAP-008 | HIGH | Escalation Persistence | Sprint 3 | Low | ✅ Resolved | `escalation.py:117,140` persist+restore events |
| GAP-009 | MEDIUM | CostTracker Persistence | Sprint 2 | Low | ✅ Resolved | `cost_tracker.py:110,294` `_rebuild_accumulators()` |
| GAP-010 | MEDIUM | Dashboard Auth/CORS | Sprint 2 | Medium | ✅ Resolved | `app.py:94,182,207` API-key middleware + configurable CORS |
| GAP-011 | MEDIUM | Dashboard API ↔ MessageBus | Sprint 1 | Low | 🟡 Partial | write path fixed (`api.py:313` `get_bus().send_task()`); `mobile_api.py` + `kpis/*` still read `inbox.json` (read-only) |
| GAP-012 | MEDIUM | AgentLoop Priority | Sprint 1 | Low | ✅ Resolved | `agent_loop.py` forwards priority to router |
| GAP-013 | MEDIUM | KPI Collector Wiring | Sprint 4 | Low | ✅ Resolved | `dashboard/kpis/__init__.py` `ALL_COLLECTORS` (7 depts) |
| GAP-014 | LOW | BriefingGenerator API | Sprint 1 | Trivial | ✅ Resolved | `briefing.py:42` uses `get_all_tasks()` (public); `message_bus.py:136` public API |
| GAP-015 | MEDIUM | LLM Retry Logic | Sprint 2 | Low | ✅ Resolved | `client.py:133-134` `provider_idx = attempt % len(provider_chain)` round-robin |
| GAP-016 | MEDIUM | Shell Injection | Sprint 2 | Medium | ✅ Resolved | `tool_runner.py:466` `shlex.split()`; no `shell=True` |
| GAP-017 | MEDIUM | Task Timeout/DLQ | Sprint 3 | Medium | ✅ Resolved | `dead_letter.py` + `loop.py:174` `detect_stale_tasks()` |
| GAP-018 | LOW | Structured Logging | Sprint 4 | Medium | 🟡 Partial | no structured JSON/correlation IDs; 11 `print()` in non-CLI modules |
| GAP-019 | LOW | Spec Validation | Sprint 4 | Low | 🔴 Open | `context.py:13` `AgentContext` has no `validate()`; no `agents validate` CLI |
| GAP-020 | LOW | Integration Tests | Sprint 4 | Medium | ✅ Resolved | `tests/integration/test_full_pipeline.py` (305 lines, 10 tests, all pass) |

**Resolved:** 16 of 20 (GAP-001, 002, 003, 004, 006, 007, 008, 009, 010, 012, 013, 014, 015, 016, 017, 020)
**Partial:** 3 (GAP-005, GAP-011, GAP-018)
**Open:** 1 (GAP-019)
**Remaining work to reach "done":** finish consolidation (GAP-005), read-path MessageBus (GAP-011), structured logging (GAP-018), and agent spec validation (GAP-019).

## Recommended Sprint Plan

### Sprint 4+ — Remaining Integration Gaps

Prioritized backlog of all partial and open gaps that still require work to reach full resolution:

| # | Gap ID | Severity | Description | Effort | Status |
|---|--------|----------|-------------|--------|--------|
| 1 | GAP-005 | HIGH | Finish memory consolidation in executor loop (`consolidate()` cadence) | Medium | 🟡 Partial — recall/store wired; consolidation not yet in the executor `start()` loop |
| 2 | GAP-011 | MEDIUM | Dashboard API read path through MessageBus (`mobile_api.py` + `kpis/*` still read `inbox.json` directly) | Low | 🟡 Partial — write path fixed (`api.py:313`); read path not yet through bus |
| 3 | GAP-018 | LOW | Structured logging with correlation IDs; replace 11 `print()` calls in non-CLI modules | Medium | 🟡 Partial — no structured JSON/correlation IDs; mixed logging across modules |
| 4 | GAP-019 | LOW | Agent spec validation (`AgentContext.validate()` method + `ai-company agents validate` CLI) | Low | 🔴 Open — no schema validation; malformed specs silently produce empty `AgentContext` |

**Total remaining effort:** ~Medium + Low + Medium + Low

> All other gaps (GAP-001 through GAP-004, GAP-006 through GAP-010, GAP-012 through GAP-017, GAP-020) are resolved in source and verified. They should be covered by regression tests and periodic audit during Sprint 4+.
