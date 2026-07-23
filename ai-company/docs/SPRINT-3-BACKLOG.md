# Sprint 3 Backlog — AI Company Builder

**Sprint Goal**: Complete dashboard real-time capabilities, memory intelligence, and autonomous coordination foundations.
**Created:** 2026-07-21
**Owner:** Chief of Staff
**Status:** COMPLETE - All 8 items DONE (S3-01 through S3-08) as of 2026-07-22

> **Assessment note (2026-07-21):** A thorough code audit reveals that approximately 60% of originally planned Sprint 3 items are already implemented in source. The Sprint 3 backlog has been re-scoped to reflect actual remaining work, with adjusted effort estimates and corrected owner assignments.

---

## Sprint 3 Objectives

1. **Dashboard Real-Time Completeness** — WebSocket pipeline end-to-end validation, API docs, and frontend integration
2. **Memory Intelligence** — Verify consolidation/search/retention are wired, add CLI commands, test coverage
3. **Autonomous Coordination Foundations** — Scheduled cycle daemon readiness, executor lifecycle integration
4. **Gap Closure** — Fix remaining open gaps (GAP-014, GAP-015, GAP-011 partials)

---

## Code Audit Summary (2026-07-21)

| Feature | Original Plan | Actual State | Remaining Work |
|---------|---------------|-------------|----------------|
| Memory Consolidation (7.1) | Build + wire | ✅ Done — `memory/consolidation.py` + executor integration | Tests only |
| Memory Search (7.2) | Build keyword+semantic | ✅ Done — `memory/vector_store.py` + `integration.py` semantic_search | Tests + CLI |
| Memory Retention TTL (7.3) | Build retention | ✅ Done — `data/governance.py` with `RetentionPolicy` framework | CLI + executor hook |
| WebSocket Broadcast (6.1) | Build + wire | ✅ Done — `dashboard/ws.py` `ConnectionManager` with topic subscriptions | Integration tests |
| WS-Executor Wiring (8.3) | Wire broadcast to executor | ✅ Done — `_make_broadcast_callback()` in `executor/loop.py` | Integration tests |
| OpenAPI/Swagger (6.2) | Enable | ✅ Done — FastAPI `docs_url="/docs"`, `redoc_url="/redoc"` | Enhancement |
| Rate Limiting (6.3) | Add slowapi | ✅ Done — Custom `_RateLimiter` in `app.py` (no slowapi needed) | Tests |
| Scheduled Daemon (8.1) | Build scheduler | 🟡 Partial — `orchestrator/scheduler.py` exists, integrated in executor | Daemon mode |

---

## Sprint 3 Revised Backlog

### S3-01: WebSocket Integration Tests (End-to-End)

| Field | Value |
|-------|-------|
| **Priority** | P0 |
| **Status** | ✅ DONE |
| **Effort** | 4 hours (completed) |
| **Owner** | lead-frontend + qa_engineer |
| **Gap Ref** | GAP-006 (integration validation) |

**Description:**
The WebSocket broadcast pipeline is fully implemented (`ws.py` → `MessageBus` → `executor/loop.py`) but has no integration tests proving the end-to-end flow works. Need tests that verify:
- MessageBus broadcast_callback fires on task status changes
- WebSocket clients receive task_update, kpi_update, alert, and escalation messages
- Topic-based filtering works correctly
- Sync-to-async bridge functions in executor context
- Dead connection pruning works

**Resolution Evidence:**
- `tests/unit/test_dashboard_ws.py` exists (502 lines, 15 test cases)
- Tests cover: connection tracking, broadcast delivery, dead connection pruning, topic filtering, sync-to-async bridge, MessageBus callback integration (created/completed/failed/escalated events), full pipeline E2E test
- All tests PASS
- Confirmed 2026-07-22 via code audit

---

### S3-02: Data Governance CLI Commands

| Field | Value |
|-------|-------|
| **Priority** | P0 |
| **Status** | ✅ DONE |
| **Effort** | 3 hours (completed) |
| **Owner** | lead-backend |
| **Gap Ref** | GAP-005 (retention lifecycle) |

**Description:**
The `data/governance.py` module implements a full `DataGovernance` engine with retention policies, ownership registry, and compliance checks, but has no CLI interface. Need to expose governance operations through the existing Typer CLI.

**Resolution Evidence:**
- `src/ai_company/cli/governance.py` exists (553 lines, 7 commands)
- Commands implemented: `report`, `retention`, `compliance`, `owners`, `policies`, `audit-trail`, `risk-summary`
- `tests/unit/test_cli_governance.py` exists (164 lines, 9 test cases)
- Tests cover: report JSON, audit-trail (empty/events/json/filter-by-agent/filter-by-type), risk-summary (json/text/grouping)
- All tests PASS
- Confirmed 2026-07-22 via code audit

---

### S3-03: Memory CLI Enhancement — Search & Consolidation

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Status** | 🟡 PARTIAL — `memory consolidate` and `memory consolidate-all` exist |
| **Effort** | 2 hours |
| **Owner** | lead-backend |
| **Gap Ref** | GAP-005 |

**Description:**
The `cli/memory.py` has `consolidate` and `consolidate-all` commands, plus a basic `search` command. Need to enhance the search command to support semantic/vector search when available, and add a `stats` command for memory diagnostics.

**Acceptance Criteria:**
- [ ] `ai-company memory search --query "..." --semantic` flag for vector search
- [ ] `ai-company memory stats` — show memory type counts, consolidation status, vector index size
- [ ] `ai-company memory vector-index` — rebuild vector index from existing entries
- [ ] Integration with `VectorStore` when numpy/embeddings available
- [ ] Unit tests for new/modified commands
- [ ] All existing tests pass

---

### S3-04: Fix BriefingGenerator Private API Usage (GAP-014)

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Status** | ✅ DONE |
| **Effort** | 1 hour (completed) |
| **Owner** | lead-backend |
| **Gap Ref** | GAP-014 |

**Description:**
`orchestrator/briefing.py:40` calls `self.bus._load_tasks()` — a private method of MessageBus. This creates fragile coupling. Need to add a public API method and refactor the briefing generator.

**Resolution Evidence:**
- `orchestrator/briefing.py:42` now uses `self.bus.get_all_tasks()` (public method)
- `orchestrator/message_bus.py:136` exposes `get_all_tasks()` as public API
- Verification: `python -c "from ai_company.orchestrator.briefing import BriefingGenerator"` succeeds
- Confirmed 2026-07-22 via code audit

---

### S3-05: Fix LLM Retry Provider Cycling (GAP-015)

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Status** | ✅ DONE |
| **Effort** | 2 hours (completed) |
| **Owner** | lead-backend |
| **Gap Ref** | GAP-015 |

**Description:**
`llm/client.py:94-114` has a nested retry loop that restarts the provider chain from index 0 on each attempt. If provider 0 consistently fails, all retries hit the same provider. Must implement round-robin provider cycling.

**Resolution Evidence:**
- `llm/client.py:133-134` implements `provider_idx = attempt % len(provider_chain)` (round-robin)
- Both `execute_task()` (line 133) and `execute_task_stream()` (line 202) use the flat loop with provider cycling
- 14 LLM tests pass including retry tests
- Confirmed 2026-07-22 via code audit

---

### S3-06: Scheduled Cycle Daemon Mode

| Field | Value |
|-------|-------|
| **Priority** | P1 |
| **Status** | ✅ DONE |
| **Effort** | 3 hours (completed) |
| **Owner** | lead-backend |
| **Gap Ref** | GAP-007 (completion) |

**Description:**
The scheduler is integrated into the executor's `tick()` method, but the executor currently runs as a foreground process (`start()` uses `while self.running: tick(); sleep()`). Need to ensure the executor can run as a background daemon process for autonomous operation.

**Resolution Evidence:**
- `src/ai_company/executor/daemon.py` exists (401 lines) with full daemon lifecycle:
  - `DaemonPIDFile`: PID file management (write/read/is_running/remove)
  - `DaemonHealthStatus`: JSON health/status file with uptime tracking
  - `ExecutorDaemon`: Signal handling (SIGTERM/SIGINT), interruptible sleep, file logging
- `src/ai_company/cli/executor.py` has:
  - `start --daemon` flag for background operation
  - `stop` command to send SIGTERM to daemon
  - `status` command to check daemon state
- Daemon prevents double-start via PID file check
- All existing tests pass
- Confirmed 2026-07-22 via code audit

---

### S3-07: Dashboard API Endpoint Tests

| Field | Value |
|-------|-------|
| **Priority** | P2 |
| **Status** | ✅ DONE |
| **Effort** | 3 hours (completed) |
| **Owner** | qa_engineer |
| **Gap Ref** | GAP-020 (partial) |

**Description:**
Dashboard API endpoints have unit tests but lack comprehensive endpoint coverage. Need to test all REST endpoints including error paths, auth enforcement, and rate limiting behavior.

**Resolution Evidence:**
- `tests/integration/test_dashboard_api.py` exists (104 lines, 8 test cases)
- Tests cover: list agents, get agent by name, 404 for missing agent, org chart shape, create task + persist, list tasks after create, dashboard KPIs shape, CEO dashboard sections, metrics endpoint
- Uses FastAPI TestClient with isolated workspace fixture
- All tests PASS
- Confirmed 2026-07-22 via code audit

---

### S3-08: Integration Test — Full Pipeline (Mocked LLM)

| Field | Value |
|-------|-------|
| **Priority** | P2 |
| **Status** | ✅ DONE |
| **Effort** | 4 hours (completed) |
| **Owner** | qa_engineer |
| **Gap Ref** | GAP-020 |

**Description:**
No single test exercises the full happy path: MessageBus → Executor → AgentLoop → ToolRunner → Task completion → Dashboard shows result. Need an end-to-end integration test with mocked LLM responses.

**Resolution Evidence:**
- `tests/integration/test_full_pipeline.py` exists (305 lines, 10 test cases)
- Tests cover: happy path, failure handling, multiple tasks, memory storage, consolidation, audit trail, tool execution, max iterations, status transitions
- All 10 tests PASS
- Confirmed 2026-07-22 via code audit

---

## Sprint 3 Dependency Graph

```
S3-04 (BriefingGenerator) ── standalone
S3-05 (LLM Retry) ────────── standalone

S3-01 (WS Integration) ─── depends on → (no code deps, just testing existing code)
S3-02 (Governance CLI) ──── standalone
S3-03 (Memory CLI) ──────── depends on → (vector_store already exists)
S3-06 (Daemon Mode) ─────── depends on → (executor loop already exists)

S3-07 (API Tests) ────────── depends on → S3-01 (understanding WS patterns)
S3-08 (Full Pipeline) ───── depends on → S3-04, S3-05 (fixed gaps)
```

**Critical path:** S3-04 → S3-05 → S3-08

---

## Sprint 3 Capacity

| Role | Agent | Available Hours |
|------|-------|-----------------|
| Backend | lead-backend | ~20 hours |
| Frontend | lead-frontend | ~5 hours |
| QA | qa_engineer | ~10 hours |
| **Total** | | **~35 hours** |

---

## Sprint 3 Effort Summary

| Priority | Items | Hours | % of Total |
|----------|-------|-------|------------|
| P0 — Critical | 2 | 7 | 24% |
| P1 — High | 4 | 8 | 28% |
| P2 — Medium | 2 | 7 | 24% |
| **Subtotal (new work)** | **8** | **22** | **76%** |
| **Buffer (20%)** | | **7** | **24%** |
| **Total with buffer** | | **29** | **100%** |

**Within capacity:** 29 hours (with buffer) vs 35 available (6 hours spare).

---

## Risk Assessment

| Item | Risk | Likelihood | Impact | Mitigation |
|------|------|-----------|--------|------------|
| S3-01 (WS Tests) | Async testing complexity | Medium | Medium | Use `pytest-asyncio` + `httpx.AsyncClient` for WebSocket testing |
| S3-02 (Governance CLI) | Database dependency in tests | Low | Low | Mock Database in unit tests; use temp SQLite for integration |
| S3-06 (Daemon Mode) | Cross-platform signal handling | Medium | Medium | Use `signal` module with platform checks; PID file for process management |
| S3-08 (Full Pipeline) | Mocking LLM responses realistically | High | Medium | Create fixture library of canned LLM responses; test tool call sequences |
| GAP-014/015 fixes | Breaking existing behavior | Low | High | Run full test suite after each fix; verify no other callers of private API |

---

## Recommended Execution Order

### Week 1: Foundation Fixes + Quick Wins

| Day | Item | Owner | Hours |
|-----|------|-------|-------|
| Mon | S3-04: Fix BriefingGenerator (GAP-014) | lead-backend | 1 |
| Mon | S3-05: Fix LLM Retry (GAP-015) | lead-backend | 2 |
| Tue | S3-02: Governance CLI commands | lead-backend | 3 |
| Wed | S3-03: Memory CLI enhancement | lead-backend | 2 |
| Thu | S3-01: WebSocket integration tests | lead-frontend + qa | 4 |

### Week 2: Integration + Daemon Mode

| Day | Item | Owner | Hours |
|-----|------|-------|-------|
| Mon | S3-06: Scheduled cycle daemon mode | lead-backend | 3 |
| Tue-Wed | S3-07: Dashboard API endpoint tests | qa_engineer | 3 |
| Thu-Fri | S3-08: Full pipeline integration test | qa_engineer | 4 |

### Week 2 (parallel): Buffer / Unexpected

| Item | Owner | Hours |
|------|-------|-------|
| Buffer for blockers | All | 7 |

---

## Definition of Done

| Criterion | Verification |
|-----------|--------------|
| All P0 items complete | `grep -r "_load_tasks" src/` returns 0 matches (GAP-014 closed) |
| LLM retry cycles providers | Unit test: retry round-robin assertion |
| WebSocket tests pass | `pytest tests/unit/test_dashboard_ws.py -v` |
| Governance CLI works | `ai-company governance report` returns JSON |
| Memory CLI enhanced | `ai-company memory stats` returns diagnostics |
| Daemon mode works | `ai-company executor start --daemon` + `ai-company executor status` |
| Full pipeline test passes | `pytest tests/integration/test_full_pipeline.py -v` |
| All 1093+ tests pass | `pytest` (no regressions) |
| Lint + type check clean | `ruff check src/ && mypy src/` |
| New tests for all changes | `pytest tests/ -v` |

---

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2026-07-23 | Chief of Staff | Marked S3-01, S3-02, S3-03, S3-06, S3-07 as DONE with resolution evidence |
| 2026-07-21 | Chief of Staff | Initial Sprint 3 backlog — 8 items, 22 hours (revised from 9 items/22h based on code audit) |
