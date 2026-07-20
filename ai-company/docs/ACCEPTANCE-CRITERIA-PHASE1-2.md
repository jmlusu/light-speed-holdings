# Acceptance Criteria — Phase 1-2 Remaining Work

**Author:** Product Owner  
**Date:** 2026-07-20  
**Scope:** All architecture gaps (GAP-001 through GAP-020)  
**Status:** ACTIVE

---

## 1. Definition of Done (General)

Every architecture gap resolution must meet these criteria:

| Criterion | Verification |
|-----------|-------------|
| Code implemented | Source file exists, passes ruff + mypy |
| Unit tests written | New tests in `tests/unit/` or `tests/integration/` |
| Test coverage >= 80% | `pytest --cov=src/ai_company/<module>` |
| Integration verified | Module works with existing components |
| No regressions | Full test suite passes (`pytest`) |
| Documentation updated | Relevant docs/ updated (if public API changed) |
| Lint clean | `ruff check src/` — 0 errors |
| Type clean | `mypy src/` — 0 errors |

---

## 2. GAP-001 — Route Executor I/O Through MessageBus

**Severity:** CRITICAL  
**Points:** 5

### User Story
> As a developer, I want all task inbox reads and writes to go through the MessageBus so that there is a single source of truth for task state and no race conditions.

### Acceptance Criteria

- [ ] `MessageBus.get_pending_tasks() -> list[Task]` method exists and returns pending tasks from inbox.json
- [ ] `MessageBus.update_status(task_id, status, result=None)` method exists and updates task status atomically
- [ ] `Executor._get_pending_tasks()` calls `self.bus.get_pending_tasks()` instead of reading file directly
- [ ] `Executor._update_task_status()` calls `self.bus.update_status()` instead of writing file directly
- [ ] `Executor._complete_task()` calls `self.bus.update_status()` instead of writing file directly
- [ ] No direct `inbox.json` reads/writes exist in `executor/loop.py` (grep confirms 0 matches)
- [ ] Unit test: `test_message_bus_get_pending_tasks` — creates inbox, verifies tasks returned
- [ ] Unit test: `test_message_bus_update_status` — updates task, verifies status persisted
- [ ] Integration test: `test_executor_uses_message_bus` — mock MessageBus, verify it's called
- [ ] `pytest tests/unit/test_message_bus.py` passes
- [ ] `pytest tests/unit/test_executor.py` passes

### Test Requirements

```python
# tests/unit/test_message_bus.py
def test_get_pending_tasks_returns_pending_only():
    """Only tasks with status='pending' are returned."""
    
def test_get_pending_tasks_empty_inbox():
    """Empty inbox returns empty list, not error."""
    
def test_update_status_persists_to_file():
    """Status change is written to inbox.json."""
    
def test_update_status_with_result():
    """Result dict is stored alongside status."""
```

### Documentation Requirements
- Update `docs/ARCHITECTURE.md` if MessageBus API changes
- Add docstring to new MessageBus methods

---

## 3. GAP-002 — Create FileStore Abstraction

**Severity:** CRITICAL  
**Points:** 8

### User Story
> As a developer, I want a FileStore abstraction that handles atomic reads/writes and optional file locking so that concurrent components don't corrupt shared JSON/YAML state.

### Acceptance Criteria

- [ ] `src/ai_company/store/__init__.py` exists and exports `FileStore`
- [ ] `src/ai_company/store/file_store.py` implements `FileStore` class
- [ ] `FileStore.read_json(path) -> Any` — reads and parses JSON atomically
- [ ] `FileStore.write_json(path, data)` — writes to temp file, then renames (atomic)
- [ ] `FileStore.read_yaml(path) -> Any` — reads and parses YAML atomically
- [ ] `FileStore.write_yaml(path, data)` — writes to temp file, then renames (atomic)
- [ ] File locking: concurrent writes don't corrupt data (test with threading)
- [ ] Cross-platform: works on Windows (msvcrt) and Unix (fcntl) — use portalocker or manual
- [ ] `FileStore` used by MessageBus, ApprovalGate, EscalationManager
- [ ] Unit test: `test_read_write_json_roundtrip` — write then read returns same data
- [ ] Unit test: `test_read_write_yaml_roundtrip` — write then read returns same data
- [ ] Unit test: `test_atomic_write_no_corruption` — crash mid-write doesn't corrupt
- [ ] Unit test: `test_concurrent_writes` — 10 threads writing simultaneously
- [ ] Unit test: `test_missing_file_returns_none` — read non-existent file returns None
- [ ] `pytest tests/unit/test_file_store.py` passes
- [ ] `ruff check src/ && mypy src/` clean

### Test Requirements

```python
# tests/unit/test_file_store.py
def test_read_write_json_roundtrip(tmp_path):
    """Write JSON, read back, verify equality."""
    
def test_read_write_yaml_roundtrip(tmp_path):
    """Write YAML, read back, verify equality."""
    
def test_atomic_write_no_corruption(tmp_path):
    """Simulate crash during write; original file intact."""
    
def test_concurrent_writes(tmp_path):
    """10 threads writing to same file; no corruption."""
    
def test_missing_file_returns_none(tmp_path):
    """Read non-existent file returns None, not exception."""
    
def test_auto_creates_parent_directories(tmp_path):
    """Write to nested path creates directories automatically."""
```

### Documentation Requirements
- Create `docs/ADR-003-FileStore.md` — architecture decision record
- Document cross-platform locking strategy

---

## 4. GAP-003 — Integrate Tier Rules into ToolRunner

**Severity:** HIGH  
**Points:** 5

### User Story
> As a developer, I want ToolRunner to consult the tier classification system so that tool actions get appropriate approval levels based on risk, not a binary dangerous/safe check.

### Acceptance Criteria

- [ ] `ToolRunner.__init__` accepts optional `tier_classifier: TierClassifier | None`
- [ ] `ToolRunner.run_plan()` calls `classify_tool_action()` instead of checking `DANGEROUS_TOOLS`
- [ ] Classification result includes tier level (0-4), risk score, and recommended approval
- [ ] Tier 0-1 actions auto-approved without HITL
- [ ] Tier 2+ actions routed to HITL with tier-specific timeout
- [ ] Backward compatible: when no TierClassifier provided, falls back to DANGEROUS_TOOLS check
- [ ] Unit test: `test_tier0_auto_approved` — read action auto-approves
- [ ] Unit test: `test_tier2_hits_hitl` — write action triggers HITL
- [ ] Unit test: `test_tier4_requires_ceo` — dangerous action escalates to CEO
- [ ] `pytest tests/unit/test_tool_runner.py` passes

### Test Requirements

```python
# tests/unit/test_tool_runner.py
@pytest.mark.parametrize("tool,expected_tier", [
    ("read", 0),
    ("write", 2),
    ("execute", 3),
    ("code_interpreter", 3),
])
def test_classify_tool_action(tool, expected_tier):
    """Each tool maps to correct tier."""
    
def test_tier0_auto_approved(runner, hitl_gate):
    """Tier 0 actions never trigger HITL."""
    
def test_backward_compat_without_classifier():
    """Without tier classifier, DANGEROUS_TOOLS still works."""
```

### Documentation Requirements
- Update `docs/ARCHITECTURE.md` with tier-to-approval mapping

---

## 5. GAP-004 — Non-Blocking HITL Gate

**Severity:** HIGH  
**Points:** 5

### User Story
> As a developer, I want the HITL gate to be non-blocking so that the executor can continue processing other tasks while waiting for human approval.

### Acceptance Criteria

- [ ] New `TaskStatus.AWAITING_APPROVAL` enum value added
- [ ] `HITLGate.request()` returns immediately (non-blocking) with request_id
- [ ] `HITLGate.check_status(request_id) -> ApprovalStatus` polls without blocking
- [ ] `Executor._process_task()` checks if task is awaiting_approval and skips to next
- [ ] Separate poll loop in `Executor.start()` checks resolved approvals and resumes tasks
- [ ] Timeout behavior: unresolved approvals after timeout → auto-deny or escalate per tier
- [ ] Unit test: `test_hitl_request_returns_immediately` — no time.sleep in request
- [ ] Unit test: `test_executor_skips_awaiting_approval` — processes other tasks
- [ ] Unit test: `test_approval_resumes_task` — approved task resumes execution
- [ ] `pytest tests/unit/test_hitl_gate.py` passes
- [ ] `pytest tests/unit/test_executor.py` passes

### Test Requirements

```python
def test_hitl_request_returns_immediately():
    """request() completes in < 100ms, no blocking."""
    
def test_executor_skips_awaiting_tasks():
    """While task A awaits approval, task B is processed."""
    
def test_timeout_auto_denies():
    """After timeout, awaiting task is auto-denied."""
```

---

## 6. GAP-005 — Wire Memory Engine into Executor

**Severity:** HIGH  
**Points:** 8

### User Story
> As a developer, I want the executor to read and write memories on every task so that agents can learn from past experiences and build institutional knowledge.

### Acceptance Criteria

- [ ] After task completion: `memory.store("episodic", {"task_id": ..., "agent": ..., "outcome": ...})` called
- [ ] After task failure: `memory.store("episodic", {"task_id": ..., "error": ..., "context": ...})` called
- [ ] Before task execution: `memory.recall("semantic", query=task.instruction)` retrieves relevant context
- [ ] Memory context injected into agent system prompt when available
- [ ] Periodic consolidation: `memory.consolidate()` runs every N tasks (configurable)
- [ ] Feature flag: memory integration can be disabled via config for backward compat
- [ ] Unit test: `test_episodic_memory_stored_on_completion`
- [ ] Unit test: `test_episodic_memory_stored_on_failure`
- [ ] Unit test: `test_semantic_memory_recalled_before_execution`
- [ ] Unit test: `test_memory_context_injected_into_prompt`
- [ ] Integration test: `test_memory_roundtrip` — store then recall
- [ ] `pytest tests/unit/test_memory_engine.py` passes

### Test Requirements

```python
def test_episodic_memory_stored_on_completion(memory_engine):
    """Successful task creates episodic memory."""
    
def test_memory_context_enriches_prompt(memory_engine):
    """Relevant memories are included in agent prompt."""
    
def test_consolidation_merges_related_memories(memory_engine):
    """Consolidation reduces memory count."""
```

---

## 7. GAP-006 — Wire WebSocket Broadcast

**Severity:** HIGH  
**Points:** 3

### User Story
> As a dashboard user, I want real-time updates when tasks complete, approvals are needed, or escalations occur so that I don't have to refresh the page.

### Acceptance Criteria

- [ ] `broadcast_kpi_update()` called on task completion with KPI data
- [ ] `broadcast_alert({"type": "approval_needed", ...})` called when HITL triggers
- [ ] `broadcast_alert({"type": "escalation", ...})` called on escalation
- [ ] WebSocket connection receives events within 2 seconds of state change
- [ ] Unit test: `test_broadcast_called_on_task_completion`
- [ ] Unit test: `test_broadcast_called_on_approval_needed`
- [ ] `pytest tests/unit/test_websocket.py` passes

---

## 8. GAP-007 — Integrate Scheduler into Executor Loop

**Severity:** HIGH  
**Points:** 5

### User Story
> As a developer, I want scheduled tasks to be automatically injected into the executor's inbox when they are due so that recurring operations (daily briefings, periodic reports) happen without manual triggers.

### Acceptance Criteria

- [ ] `Executor.__init__` initializes `self.scheduler = Scheduler()`
- [ ] At start of `tick()`: `self.scheduler.get_pending_tasks()` called
- [ ] For each due task: `Task` created from template, sent via MessageBus
- [ ] After execution: `self.scheduler.mark_completed(task_id)` called
- [ ] Unit test: `test_scheduler_injects_due_tasks` — due task appears in inbox
- [ ] Unit test: `test_scheduler_skips_future_tasks` — future task not injected
- [ ] Unit test: `test_completed_task_marked_in_scheduler`
- [ ] `pytest tests/unit/test_scheduler.py` passes

---

## 9. GAP-008 — Persist Escalation Events

**Severity:** HIGH  
**Points:** 3

### User Story
> As a developer, I want escalation events to be persisted to disk so that they survive process restarts and can be reviewed in the dashboard.

### Acceptance Criteria

- [ ] `EscalationManager._save_config()` persists both `self.rules` AND `self.events`
- [ ] `EscalationManager._load_config()` loads events from file on startup
- [ ] Events are appended, not overwritten (history preserved)
- [ ] Event archival: resolved events moved to `escalation_archive.yaml` after 30 days
- [ ] Unit test: `test_escalation_events_persist_across_restarts`
- [ ] Unit test: `test_event_archival`
- [ ] `pytest tests/unit/test_escalation.py` passes

---

## 10. GAP-009 — CostTracker Persistence

**Severity:** MEDIUM  
**Points:** 2

### User Story
> As a developer, I want CostTracker to rebuild its accumulators from the JSONL log on startup so that budget enforcement works across process restarts.

### Acceptance Criteria

- [ ] `CostTracker.__init__` calls `_rebuild_accumulators()`
- [ ] `_rebuild_accumulators()` reads `cost_log.jsonl` and sums costs by day and task_id
- [ ] After restart, `check_budget()` uses accurate accumulated values
- [ ] Unit test: `test_rebuild_accumulators_after_restart`
- [ ] `pytest tests/unit/test_cost_tracker.py` passes

---

## 11. GAP-010 — Dashboard CORS + Auth

**Severity:** MEDIUM  
**Points:** 5

### User Story
> As a developer, I want the dashboard API to require authentication for write operations and restrict CORS to known origins so that unauthorized users cannot manipulate tasks or approvals.

### Acceptance Criteria

- [ ] CORS origins configurable via `CORS_ORIGINS` env var (default: localhost only)
- [ ] API key middleware on POST/DELETE endpoints: `X-API-Key` header required
- [ ] API key configurable via `API_KEY` env var
- [ ] Rate limiting: configurable per-endpoint (default: 100 req/min)
- [ ] Unauthenticated write returns HTTP 401 with clear error message
- [ ] Unit test: `test_unauthenticated_post_returns_401`
- [ ] Unit test: `test_rate_limit_returns_429`
- [ ] `pytest tests/unit/test_dashboard_api.py` passes

---

## 12. GAP-011 — Dashboard API Uses MessageBus

**Severity:** MEDIUM  
**Points:** 2

### User Story
> As a developer, I want the dashboard API to use MessageBus for all task operations so that there is a single write path and no race conditions.

### Acceptance Criteria

- [ ] `MessageBus` injected into API router via FastAPI dependency
- [ ] `POST /api/tasks` calls `bus.send_task()` instead of reading/writing file
- [ ] `GET /api/tasks` calls `bus.get_inbox()` instead of reading file directly
- [ ] No direct `inbox.json` reads in `dashboard/api.py` (grep confirms 0)
- [ ] Unit test: `test_api_task_creation_uses_bus`
- [ ] `pytest tests/unit/test_dashboard_api.py` passes

---

## 13. GAP-012 — Fix Priority Forwarding

**Severity:** MEDIUM  
**Points:** 2

### User Story
> As a developer, I want AgentLoop to forward the task's actual priority to the model router so that high-priority tasks get premium models.

### Acceptance Criteria

- [ ] `AgentLoop.run()` stores task priority as `self._current_priority`
- [ ] `_call_llm()` uses `self._current_priority` instead of hardcoded "medium"
- [ ] Unit test: `test_critical_task_gets_premium_model`
- [ ] Unit test: `test_low_task_gets_fast_model`
- [ ] `pytest tests/unit/test_agent_loop.py` passes

---

## 14. GAP-015 — Fix LLM Retry Provider Cycling

**Severity:** MEDIUM  
**Points:** 3

### User Story
> As a developer, I want LLM retries to cycle through providers round-robin so that a failure in one provider doesn't block all retry attempts.

### Acceptance Criteria

- [ ] Retry logic uses flat loop with provider index: `provider_idx = attempt % len(chain)`
- [ ] Attempt 0 → provider 0, attempt 1 → provider 1, etc.
- [ ] Unit test: `test_retry_cycles_through_providers` — verify different providers per attempt
- [ ] Unit test: `test_max_retries_exhausted` — all attempts fail, returns error
- [ ] `pytest tests/unit/test_llm_client.py` passes

---

## 15. GAP-016 — Remove shell=True

**Severity:** MEDIUM  
**Points:** 5

### User Story
> As a security engineer, I want ToolRunner to use `shlex.split()` instead of `shell=True` so that shell injection attacks are prevented.

### Acceptance Criteria

- [ ] `subprocess.run(command, shell=True, ...)` replaced with `subprocess.run(shlex.split(command), shell=False, ...)`
- [ ] Command allowlist validation: only approved binaries can execute
- [ ] Blocked commands logged with full command string for audit
- [ ] Integration with tier_rules for dangerous command detection
- [ ] Unit test: `test_shell_injection_prevented` — `"rm -rf /"` blocked
- [ ] Unit test: `test_valid_command_allowed` — `"ls -la"` executes
- [ ] `grep -r "shell=True" src/` returns 0 matches
- [ ] `pytest tests/unit/test_tool_runner.py` passes

---

## 16. GAP-017 — Task Timeout & Dead Letter Queue

**Severity:** MEDIUM  
**Points:** 5

### User Story
> As a developer, I want stale in-progress tasks to be recovered or moved to a dead letter queue so that crashed executors don't leave tasks permanently stuck.

### Acceptance Criteria

- [ ] `Task` model has `created_at` and `updated_at` timestamps
- [ ] On `tick()` startup: scan for in_progress tasks older than configurable timeout
- [ ] Stale tasks moved to dead letter queue (`dlq.json`)
- [ ] `ai-company orchestrator dlq list` command shows dead-lettered tasks
- [ ] `ai-company orchestrator dlq retry <id>` retries a DLQ task
- [ ] Unit test: `test_stale_task_moved_to_dlq`
- [ ] Unit test: `test_fresh_task_not_moved`
- [ ] `pytest tests/unit/test_executor.py` passes

---

## 17. Remaining Gaps (GAP-013, GAP-014, GAP-018, GAP-019, GAP-020)

### GAP-013 — Wire KPI Collectors (3 points)

- [ ] `collect_all_kpis()` uses registry pattern to discover all 7 department modules
- [ ] All 7 department KPIs appear in dashboard
- [ ] Unit test per department collector
- [ ] `pytest tests/unit/test_kpi_collector.py` passes

### GAP-014 — Fix BriefingGenerator (1 point)

- [ ] Replace `self.bus._load_tasks()` with `self.bus.get_all_tasks()`
- [ ] Add `MessageBus.get_all_tasks()` as public method
- [ ] Unit test: `test_briefing_uses_public_api`
- [ ] `pytest tests/unit/test_briefing.py` passes

### GAP-018 — Structured Logging (5 points)

- [ ] `structlog` or `python-json-logger` configured
- [ ] `task_id` added as correlation ID in log context
- [ ] All modules use `logger`, not `print()` (grep confirms)
- [ ] JSON log format with consistent fields
- [ ] `pytest tests/unit/test_logging.py` passes

### GAP-019 — Agent Spec Validation (3 points)

- [ ] `AgentContext.validate()` method checks required fields
- [ ] Warnings logged for missing mission/responsibilities
- [ ] `ai-company agents validate` CLI command exists
- [ ] `pytest tests/unit/test_agent_context.py` passes

### GAP-020 — End-to-End Integration Tests (5 points)

- [ ] `tests/integration/test_pipeline.py` exists
- [ ] Test: create task → executor picks up → agent loop runs → tool executes → result saved
- [ ] Mock LLMClient returns deterministic ReAct responses
- [ ] Dashboard API reads completed task correctly
- [ ] `pytest tests/integration/` passes

---

## 18. Test Coverage Targets

| Module | Current | Target | Gap |
|--------|---------|--------|-----|
| executor/ | ~60% | 85% | +25% |
| orchestrator/ | ~50% | 80% | +30% |
| llm/ | ~70% | 90% | +20% |
| dashboard/ | ~40% | 75% | +35% |
| memory/ | ~55% | 80% | +25% |
| store/ (new) | 0% | 90% | +90% |
| audit/ (new) | 0% | 90% | +90% |
| **Overall** | **~55%** | **80%** | **+25%** |

---

*This document is updated as gaps are resolved. Each resolved gap is marked with completion date and verification evidence.*
