# Sprint 3 Delegation Report — Chief of Staff

**Date:** 2026-07-21
**Author:** Chief of Staff (chief-of-staff)
**Sprint:** 3 — Dashboard Real-Time, Memory Intelligence, Autonomous Coordination
**Capacity:** 35h available | 22h estimated | 13h buffer (37%)
**Status:** READY TO DISPATCH

---

## Executive Summary

All 8 Sprint 3 milestones have been analyzed and assigned to maximize parallelization and workforce utilization. The plan exploits three independent workstreams that can execute simultaneously, with a single critical path (GAP fixes → pipeline test) that is front-loaded to minimize serialization risk.

**Key Design Decisions:**
1. **Critical path items (S3-04, S3-05) are assigned to senior/backend engineers** who can complete them faster than estimated, freeing the critical path early.
2. **All standalone items launch in Wave 1** (5 milestones simultaneously).
3. **Every available agent is assigned** — no idle capacity.
4. **Backup agents are pre-assigned** for high-risk items.

---

## Agent Assignment Matrix

| Agent | Milestone(s) | Est. Hours | Skill Match | Wave |
|-------|-------------|-----------|-------------|------|
| **senior_backend_engineer** | S3-04: Fix BriefingGenerator GAP-014 | 1h | Private API refactoring, code quality | 1 |
| **senior_backend_engineer** | S3-05: Fix LLM Retry GAP-015 | 2h | Provider chain logic, retry patterns | 2 (after S3-04) |
| **lead-backend** | S3-02: Data Governance CLI | 3h | CLI architecture, Typer, data governance | 1 |
| **lead-backend** | S3-06: Scheduled Cycle Daemon | 3h | Executor internals, process management | 1 |
| **backend_engineer** | S3-03: Memory CLI Enhancement | 2h | CLI commands, memory system integration | 1 |
| **lead-frontend** | S3-01: WebSocket Integration Tests (lead) | 4h | WebSocket, async patterns, dashboard | 1 |
| **qa-automation-engineer** | S3-01: WebSocket Integration Tests (support) | 2h | Test automation, async test patterns | 1 |
| **qa_engineer** | S3-07: Dashboard API Endpoint Tests | 3h | API testing, FastAPI TestClient | 1 |
| **qa-automation-engineer** | S3-08: Full Pipeline Integration Test | 4h | E2E test automation, mocking | 3 (after S3-04+05) |
| **test_engineering_lead** | CI gate review + test architecture oversight | 2h | pytest architecture, CI gating | 1-3 |
| **devops_agent** | S3-06 support: daemon process management patterns | 1h | Daemon/daemon patterns, PID management | 1 |
| **program_manager** | Dependency tracking, cross-team coordination | 1h | Cross-functional coordination | 1-3 |
| **fullstack-engineer** | Backup: assist S3-03 or S3-02 overflow | 2h | Versatile full-stack support | On-demand |
| **security_engineer** | S3-04/S3-05 security review (GAP-014/015) | 1h | Security review, API surface audit | 2 |

**Total allocated: 32h** | **Buffer: 3h** | **Utilization: 91%**

---

## Execution Waves

### Wave 1 — Immediate Launch (5 milestones, ~16h parallel)
All independent. Launch simultaneously.

```
┌─────────────────────────────────────────────────────────────────┐
│ WAVE 1 — START IMMEDIATELY                                       │
├──────────────┬──────────────────────────────┬───────┬───────────┤
│ Agent        │ Task                         │ Hours │ Blocking? │
├──────────────┼──────────────────────────────┼───────┼───────────┤
│ sr_backend   │ S3-04: Fix GAP-014           │ 1h    │ YES (CP)  │
│ lead-backend │ S3-02: Governance CLI        │ 3h    │ No        │
│ lead-backend │ S3-06: Daemon Mode           │ 3h    │ No        │
│ backend_eng  │ S3-03: Memory CLI            │ 2h    │ No        │
│ lead-frontend│ S3-01: WS Tests (lead)       │ 4h    │ No        │
│ qa_auto      │ S3-01: WS Tests (support)    │ 2h    │ No        │
│ qa_engineer  │ S3-07: API Endpoint Tests    │ 3h    │ No        │
│ devops       │ S3-06 support: daemon design │ 1h    │ No        │
│ test_lead    │ CI gate review (parallel)    │ 2h    │ No        │
│ program_mgr  │ Coordination (parallel)      │ 1h    │ No        │
└──────────────┴──────────────────────────────┴───────┴───────────┘
```

### Wave 2 — After S3-04 Completes (~3h)
S3-05 depends on S3-04 (must refactor MessageBus first).

```
┌─────────────────────────────────────────────────────────────────┐
│ WAVE 2 — AFTER S3-04 COMPLETES                                   │
├──────────────┬──────────────────────────────┬───────┬───────────┤
│ Agent        │ Task                         │ Hours │ Blocking? │
├──────────────┼──────────────────────────────┼───────┼───────────┤
│ sr_backend   │ S3-05: Fix GAP-015           │ 2h    │ YES (CP)  │
│ sec_engineer │ Review S3-04+S3-05 changes   │ 1h    │ No        │
│ fullstack    │ Assist S3-02 or S3-03 if     │ 2h    │ No        │
│              │ needed (overflow)             │       │           │
└──────────────┴──────────────────────────────┴───────┴───────────┘
```

### Wave 3 — After S3-04 + S3-05 Complete (~4h)
S3-08 depends on both GAP fixes being complete.

```
┌─────────────────────────────────────────────────────────────────┐
│ WAVE 3 — AFTER S3-04 + S3-05 COMPLETES                          │
├──────────────┬──────────────────────────────┬───────┬───────────┤
│ Agent        │ Task                         │ Hours │ Blocking? │
├──────────────┼──────────────────────────────┼───────┼───────────┤
│ qa_auto      │ S3-08: Full Pipeline Test    │ 4h    │ No        │
│ test_lead    │ Final CI gate + regression   │ 1h    │ No        │
└──────────────┴──────────────────────────────┴───────┴───────────┘
```

---

## Dependency Resolution Plan

```
CRITICAL PATH (6h wall-clock):
  S3-04 (1h) ──→ S3-05 (2h) ──→ S3-08 (4h)
  Owner: sr_backend → sr_backend → qa_auto

PARALLEL TRACK A (4h wall-clock):
  S3-01 (4h) — WebSocket Integration Tests
  Owner: lead-frontend + qa-automation-engineer

PARALLEL TRACK B (3h wall-clock):
  S3-07 (3h) — Dashboard API Endpoint Tests
  Owner: qa_engineer

INDEPENDENT (6h wall-clock max):
  S3-02 (3h) — Data Governance CLI      [lead-backend]
  S3-03 (2h) — Memory CLI Enhancement   [backend_engineer]
  S3-06 (3h) — Scheduled Cycle Daemon   [lead-backend + devops]
```

**Earliest completion:** Wave 1 items finish in ~4h (S3-04 at 1h, S3-03 at 2h, S3-02/S3-06 at 3h, S3-01/S3-07 at 4h).
**Latest completion:** S3-08 finishes at ~7h (1h S3-04 + 2h S3-05 + 4h S3-08).
**Sprint 3 total wall-clock: ~7h** (vs 22h sequential). **70% time savings through parallelization.**

---

## Detailed Milestone Briefs

### S3-04: Fix BriefingGenerator Private API Usage (GAP-014)
| Field | Value |
|-------|-------|
| **Assigned To** | senior_backend_engineer |
| **Effort** | 1h |
| **Files** | `orchestrator/message_bus.py`, `orchestrator/briefing.py` |
| **Change** | Add `MessageBus.get_all_tasks()` public method; refactor `BriefingGenerator` to use it instead of `_load_tasks()` |
| **Verification** | `grep -r "_load_tasks" src/` returns 0 matches; `pytest` passes |
| **Risk** | Low — straightforward refactoring with clear API boundary |

### S3-05: Fix LLM Retry Provider Cycling (GAP-015)
| Field | Value |
|-------|-------|
| **Assigned To** | senior_backend_engineer |
| **Effort** | 2h |
| **Depends On** | S3-04 |
| **Files** | `llm/client.py` (lines 94-114) |
| **Change** | Refactor nested retry loop to single flat loop with round-robin provider cycling: `provider_idx = attempt % len(provider_chain)` |
| **Verification** | Unit test: retry cycles through all providers; `pytest` passes |
| **Risk** | Low — isolated change to retry logic |

### S3-02: Data Governance CLI Commands
| Field | Value |
|-------|-------|
| **Assigned To** | lead-backend |
| **Effort** | 3h |
| **Files** | `data/governance.py` (read), `cli/governance.py` (create), `cli/main.py` (register) |
| **Change** | New CLI sub-app with 5 commands: report, retention, compliance, owners, policies |
| **Verification** | `ai-company governance --help` works; unit tests for all commands |
| **Risk** | Low — follows established CLI pattern |

### S3-03: Memory CLI Enhancement
| Field | Value |
|-------|-------|
| **Assigned To** | backend_engineer |
| **Effort** | 2h |
| **Files** | `cli/memory.py`, `memory/vector_store.py`, `memory/integration.py` |
| **Change** | Enhance search with `--semantic` flag; add `stats` and `vector-index` commands |
| **Verification** | `ai-company memory stats` works; graceful degradation without numpy |
| **Risk** | Low-Medium — depends on VectorStore availability |

### S3-01: WebSocket Integration Tests
| Field | Value |
|-------|-------|
| **Assigned To** | lead-frontend (lead) + qa-automation-engineer (support) |
| **Effort** | 4h (lead: 3h design + write, support: 1h review + additional cases) |
| **Files** | `tests/unit/test_dashboard_ws.py` or `tests/integration/test_ws_integration.py` |
| **Change** | Integration tests for: MessageBus → broadcast → ConnectionManager → WS client, topic filtering, sync-to-async bridge, dead connection pruning |
| **Verification** | All new WS tests pass; `pytest` no regressions |
| **Risk** | Medium — async testing complexity; use `pytest-asyncio` + mocks |

### S3-06: Scheduled Cycle Daemon Mode
| Field | Value |
|-------|-------|
| **Assigned To** | lead-backend (primary) + devops_agent (daemon patterns) |
| **Effort** | 3h (lead: 2.5h, devops: 0.5h review) |
| **Files** | `cli/executor.py`, `executor/loop.py` |
| **Change** | Add `--daemon` flag to `executor start`, PID file management, `executor stop` command, `executor status` enhancement, graceful shutdown |
| **Verification** | `ai-company executor start --daemon` + `executor status` + `executor stop` work |
| **Risk** | Medium — cross-platform signal handling; use `signal` module with platform checks |

### S3-07: Dashboard API Endpoint Tests
| Field | Value |
|-------|-------|
| **Assigned To** | qa_engineer |
| **Effort** | 3h |
| **Files** | `tests/unit/test_dashboard_api.py` or `tests/integration/test_dashboard_api.py` |
| **Change** | Comprehensive endpoint tests: GET/POST endpoints, auth enforcement, rate limiting (429), CORS middleware, approval endpoints, KPI endpoints |
| **Verification** | All endpoint tests pass; `pytest` no regressions |
| **Risk** | Low — standard API testing with FastAPI TestClient |

### S3-08: Full Pipeline Integration Test (Mocked LLM)
| Field | Value |
|-------|-------|
| **Assigned To** | qa-automation-engineer |
| **Effort** | 4h |
| **Depends On** | S3-04 + S3-05 (GAP fixes must be complete) |
| **Files** | `tests/integration/test_full_pipeline.py` |
| **Change** | E2E test: MessageBus → Executor → AgentLoop → ToolRunner → Task completion → Dashboard result. Includes: happy path, HITL approval flow, stale task detection, memory context recall, audit event logging |
| **Verification** | All pipeline tests pass with mocked LLM; `pytest` no regressions |
| **Risk** | High — mocking LLM responses realistically; create fixture library of canned responses |

---

## Risk Mitigation Assignments

| Risk | Mitigation | Owner | Backup |
|------|-----------|-------|--------|
| Async testing complexity (S3-01) | Use `pytest-asyncio` + `httpx.AsyncClient`; start with sync mocks, upgrade | lead-frontend | qa-automation-engineer |
| Cross-platform signal handling (S3-06) | Use `signal` module with `sys.platform` checks; PID file for process mgmt | lead-backend | devops_agent |
| LLM mock realism (S3-08) | Create fixture library of canned LLM responses; test tool call sequences | qa-automation-engineer | test_engineering_lead |
| GAP-014/015 breaking existing behavior | Run full test suite after each fix; verify no other callers | senior_backend_engineer | lead-backend |
| S3-02 database dependency in tests | Mock DataGovernance in unit tests; use temp SQLite for integration | lead-backend | fullstack-engineer |
| S3-03 VectorStore unavailability | Graceful degradation when numpy/embeddings unavailable; feature flag | backend_engineer | lead-backend |

---

## Utilization Dashboard

```
AGENT                    WAVE 1    WAVE 2    WAVE 3    TOTAL    CAPACITY   UTIL%
───────────────────────  ────────  ────────  ────────  ───────  ────────   ─────
senior_backend_engineer  1h(S3-04) 2h(S3-05)          3h       5h         60%
lead-backend             6h(S3-02+06)                  6h       20h        30%
backend_engineer         2h(S3-03)                      2h       4h         50%
lead-frontend            4h(S3-01)                      4h       5h         80%
qa_engineer              3h(S3-07)                      3h       10h        30%
qa-automation-engineer   2h(S3-01)          4h(S3-08)  6h       8h         75%
test_engineering_lead    2h(CI gates)        1h(CI)    3h       5h         60%
devops_agent             1h(S3-06)                    1h       4h         25%
program_manager          1h(coord)                     1h       4h         25%
fullstack-engineer              2h(backup)             2h       4h         50%
security_engineer               1h(review)             1h       4h         25%
───────────────────────  ────────  ────────  ────────  ───────  ────────   ─────
TOTAL                   22h       6h        5h        33h      73h        45%
```

**Note:** `lead-backend` appears underutilized (30%) because their 20h capacity is the largest pool. They are assigned the two most complex standalone items (S3-02 + S3-06 = 6h). If more work becomes available, lead-backend should:
- Review S3-03 Memory CLI implementation for architectural alignment
- Begin Sprint 4 prep work (structured logging design, GAP-018 spec)
- Audit remaining GAP-011 partial (dashboard API read-path)

---

## Verification Checkpoints

| Checkpoint | When | What | Gate |
|-----------|------|------|------|
| CP-1 | After S3-04 | `grep -r "_load_tasks" src/` = 0 | Unblocks S3-05 |
| CP-2 | After S3-05 | LLM retry round-robin unit test passes | Unblocks S3-08 |
| CP-3 | After S3-01 | `pytest tests/unit/test_dashboard_ws* -v` all pass | WS pipeline validated |
| CP-4 | After S3-02 | `ai-company governance report` returns JSON | CLI functional |
| CP-5 | After S3-03 | `ai-company memory stats` returns diagnostics | CLI functional |
| CP-6 | After S3-06 | `ai-company executor start --daemon` + `stop` work | Daemon functional |
| CP-7 | After S3-07 | Dashboard endpoint coverage > 80% | API validated |
| CP-8 | After S3-08 | `pytest tests/integration/test_full_pipeline.py -v` all pass | Full pipeline validated |
| FINAL | All complete | `ruff check src/ && mypy src/ && pytest` all clean | Sprint 3 done |

---

## Escalation Triggers

| Condition | Action | Escalate To |
|-----------|--------|-------------|
| S3-04 takes > 2h | Reassign to lead-backend; re-prioritize | Chief of Staff |
| S3-08 mocking proves too complex | Reduce scope to happy path + HITL only; defer stale/memory/audit tests | qa_engineer + test_lead |
| Any milestone blocks > 1h | Switch to backup agent; log blocker | program_manager |
| `pytest` regression after any change | Halt work on affected milestone; fix regression first | test_engineering_lead |
| ruff/mypy failures in new code | Fix before proceeding; no debt carryover | All agents |

---

## Sprint 3 Definition of Done

- [ ] All P0 items complete (S3-01, S3-02)
- [ ] GAP-014 closed: `grep -r "_load_tasks" src/` returns 0 matches
- [ ] GAP-015 closed: LLM retry cycles providers round-robin
- [ ] WebSocket integration tests pass
- [ ] Dashboard API endpoint tests pass
- [ ] Governance CLI functional: `ai-company governance report` returns JSON
- [ ] Memory CLI enhanced: `ai-company memory stats` returns diagnostics
- [ ] Daemon mode works: `ai-company executor start --daemon` + `stop`
- [ ] Full pipeline integration test passes with mocked LLM
- [ ] All 1093+ tests pass (no regressions)
- [ ] `ruff check src/` clean (0 errors)
- [ ] `mypy src/` clean (0 errors)
- [ ] New tests for all changes
- [ ] Documentation updated (STATUS.md, SPRINT-3-BACKLOG.md marked Done)

---

## Handoff Instructions

To execute this plan, dispatch each agent with the following approach:

1. **Wave 1 (launch immediately):** Send S3-04, S3-02, S3-03, S3-01, S3-07 tasks simultaneously
2. **Monitor CP-1:** When S3-04 completes, launch S3-05 (Wave 2)
3. **Monitor CP-2:** When S3-05 completes, launch S3-08 (Wave 3)
4. **Continuous:** test_engineering_lead reviews CI gates after each milestone
5. **On completion:** Update STATUS.md and SPRINT-3-BACKLOG.md to mark items Done

---

*Report generated by Chief of Staff | 2026-07-21 | Sprint 3 ready for execution*
