# AI Company Builder — Master Orchestration Plan

**Author:** Chief of Staff  
**Date:** 2026-07-21  
**Status:** ACTIVE  
**Total Remaining Work:** 52.5 hours across 5 agents  
**Project Completion:** ~85%

---

## Executive Summary

Sprint 1 (code hardening + audit trail) and Sprint 2 (security + integration) are complete. The remaining 52.5 hours span 19 tasks across Dashboard Enhancements, Memory Engine, Autonomous Coordination, Code Quality, Test Coverage, and Advanced Features. This plan sequences all work across 3 sprints to minimize blockers, maximize parallelism, and ensure quality gates between iterations.

**Key Decision:** The remaining work breaks cleanly into 3 sprints. Sprint 3 focuses on core feature completion (WebSocket, Memory, Scheduling). Sprint 4 focuses on quality hardening (tests, logging, validation). Sprint 5 handles advanced features and polish. This sequencing ensures functional features land first, then quality assurance validates them, then advanced capabilities extend them.

---

## 1. Task Inventory & Estimation

### 1.1 All Remaining Tasks

| ID | Task | Owner | Hours | Priority | Dependencies | Files Touched |
|----|------|-------|-------|----------|--------------|---------------|
| **S3-01** | WebSocket broadcast full wiring | lead-frontend | 3.0 | P2 | None (ws.py + api.py already wired) | `dashboard/ws.py`, `dashboard/api.py` |
| **S3-02** | OpenAPI/Swagger docs | lead-frontend | 2.0 | P2 | S3-01 (API must be stable) | `dashboard/app.py`, `dashboard/api.py` |
| **S3-03** | Rate limiting (slowapi) | lead-frontend | 1.0 | P2 | None | `dashboard/app.py` |
| **S3-04** | Periodic memory consolidation | lead-backend | 2.0 | P2 | None | `executor/loop.py`, `memory/engine.py` |
| **S3-05** | Memory search (keyword + semantic) | lead-backend | 2.5 | P2 | None | `memory/engine.py` |
| **S3-06** | Memory retention TTL | lead-backend | 1.5 | P2 | S3-04 (consolidation runs before pruning) | `memory/engine.py` |
| **S3-07** | Scheduled cycle daemon | lead-backend | 3.0 | P2 | None | `orchestrator/scheduler.py`, `executor/loop.py` |
| **S3-08** | Structured logging with correlation IDs | lead-backend | 3.0 | P3 | None | `src/ai_company/**` (cross-cutting) |
| **S3-09** | Agent spec validation CLI | lead-backend | 2.0 | P3 | None | `executor/context.py`, `cli/agents.py` |
| **S3-10** | CLI type hints/docstrings | lead-backend | 2.5 | P3 | None | `cli/*.py` (24 files) |
| **S3-11** | Full pipeline integration test (mocked LLM) | qa_engineer | 3.0 | P3 | S3-01, S3-04 (need stable executor + dashboard) | `tests/integration/` |
| **S3-12** | CLI command test suite | qa_engineer | 2.5 | P3 | S3-10 (CLI must be stable) | `tests/unit/test_cli_*.py` |
| **S3-13** | API endpoint test suite | qa_engineer | 2.5 | P3 | S3-01, S3-03 (API must be stable) | `tests/unit/test_dashboard_*.py` |
| **S3-14** | Approval escalation tests | qa_engineer | 2.0 | P3 | None | `tests/unit/test_approval*.py` |
| **S3-15** | OAuth2 or API key rotation | security_engineer | 3.0 | P3 | S3-03 (rate limiting first) | `dashboard/app.py`, `orchestrator/approval.py` |
| **S3-16** | Memory encryption for sensitive data | security_engineer | 2.0 | P3 | S3-04 (memory must be stable) | `memory/engine.py`, `store/file_store.py` |
| **S3-17** | Token counting integration | lead-backend | 1.5 | P3 | None | `llm/cost_tracker.py`, `executor/agent_loop.py` |
| **S3-18** | Close GAP-014 (BriefingGenerator private method) | lead-backend | 0.5 | P2 | None | `orchestrator/briefing.py` |
| **S3-19** | Close GAP-015 (LLM retry provider cycling) | lead-backend | 1.5 | P2 | None | `llm/client.py` |
| | **TOTAL** | | **40.0** | | | |

> **Note:** The user-provided estimate of 52.5h includes some overlap with completed work. The revised estimate of 40h for the 19 remaining tasks is based on actual source code audit on 2026-07-21. The 12.5h difference accounts for items already partially implemented (WebSocket broadcast calls in api.py/ws.py, memory consolidation_all() exists but not wired to executor, etc.).

### 1.2 Capacity by Agent

| Agent | Available Hours | Tasks Assigned | Utilization |
|-------|-----------------|----------------|-------------|
| lead-backend | 24h | S3-04, S3-05, S3-06, S3-07, S3-08, S3-09, S3-10, S3-17, S3-18, S3-19 | 18.0h (75%) |
| lead-frontend | 11h | S3-01, S3-02, S3-03 | 6.0h (55%) |
| qa_engineer | 10h | S3-11, S3-12, S3-13, S3-14 | 10.0h (100%) |
| security_engineer | 6h | S3-15, S3-16 | 5.0h (83%) |
| content-writer | 1.5h | (No new tasks — all SOPs complete) | 0% |

> **Capacity buffer:** 12.5h across all agents for unexpected complexity, bug fixes, or rework.

---

## 2. Task Dependency Graph

### 2.1 Dependency Chains

```
CRITICAL PATH (longest chain):
S3-01 (WebSocket wiring) ──→ S3-02 (OpenAPI docs)
                          ──→ S3-13 (API endpoint tests)
S3-04 (Memory consolidation) ──→ S3-06 (Memory TTL)
                              ──→ S3-16 (Memory encryption)
S3-03 (Rate limiting) ──→ S3-15 (OAuth2/key rotation)

SECONDARY CHAINS:
S3-07 (Scheduled daemon) ──→ S3-04 (Memory consolidation — consolidation runs on schedule)
S3-10 (CLI type hints) ──→ S3-12 (CLI tests — tests validate typed interfaces)

INDEPENDENT (can start immediately):
S3-05 (Memory search)         — no downstream deps
S3-08 (Structured logging)    — no downstream deps
S3-09 (Agent spec validation) — no downstream deps
S3-14 (Approval tests)        — no downstream deps
S3-17 (Token counting)        — no downstream deps
S3-18 (BriefingGenerator fix) — no downstream deps
S3-19 (LLM retry fix)         — no downstream deps
```

### 2.2 Visual Dependency Map

```
Phase 1 (Week 1)                    Phase 2 (Week 2)                 Phase 3 (Week 3)
─────────────────                   ─────────────────                 ─────────────────
                                   
  S3-01 ──┬──→ S3-02 ──────→ S3-13      S3-11
  S3-03 ──┤
           ├──→ S3-15
  S3-04 ──┼──→ S3-06
           │         └──→ S3-16
  S3-05   │
  S3-07 ──┘
                                   
  S3-08   (parallel)               S3-12
  S3-09   (parallel)
  S3-10 ─────────────────────────→ S3-12
  S3-14   (parallel)
  S3-17   (parallel)
  S3-18   (parallel)
  S3-19   (parallel)
```

### 2.3 Shared File Conflicts

| File | Agents Touching | Conflict Risk | Mitigation |
|------|----------------|---------------|------------|
| `dashboard/app.py` | lead-frontend (S3-01, S3-03, S3-02), security_engineer (S3-15) | **HIGH** | Sequential: lead-frontend finishes S3-03 before S3-15 starts |
| `memory/engine.py` | lead-backend (S3-04, S3-05, S3-06), security_engineer (S3-16) | **MEDIUM** | Sequential: lead-backend finishes S3-04/05/06 before S3-16 |
| `executor/loop.py` | lead-backend (S3-04, S3-07) | **LOW** | Same agent, internal coordination |
| `cli/agents.py` | lead-backend (S3-09) | **LOW** | Single agent |
| `llm/client.py` | lead-backend (S3-19) | **LOW** | Single agent |

**Resolution:** Security tasks (S3-15, S3-16) are sequenced AFTER the files they depend on are stable. No concurrent edits to the same file across agents.

---

## 3. Sprint Plan

### Sprint 3 — Feature Completion (Weeks 1-2)
**Goal:** Complete all P2 features — Dashboard real-time, Memory enhancements, Autonomous scheduling, and API hardening.

| ID | Task | Owner | Day | Hours | Gate |
|----|------|-------|-----|-------|------|
| S3-01 | WebSocket broadcast wiring | lead-frontend | 1-2 | 3.0 | WS events flow end-to-end |
| S3-03 | Rate limiting (slowapi) | lead-frontend | 2 | 1.0 | 429 on >100 req/min |
| S3-02 | OpenAPI/Swagger docs | lead-frontend | 3 | 2.0 | `/docs` renders correctly |
| S3-18 | Fix BriefingGenerator private method | lead-backend | 1 | 0.5 | No `_load_tasks()` calls |
| S3-19 | Fix LLM retry provider cycling | lead-backend | 1 | 1.5 | Retry cycles providers round-robin |
| S3-04 | Periodic memory consolidation | lead-backend | 2-3 | 2.0 | `consolidate_all()` in executor loop |
| S3-05 | Memory search enhancement | lead-backend | 3-4 | 2.5 | Keyword + vector search works |
| S3-06 | Memory retention TTL | lead-backend | 4 | 1.5 | Old memories auto-pruned |
| S3-07 | Scheduled cycle daemon | lead-backend | 5-6 | 3.0 | Cron-like task scheduling |
| S3-14 | Approval escalation tests | qa_engineer | 2-3 | 2.0 | 10+ approval test cases |
| | **Sprint 3 Total** | | | **17.0** | |

**Sprint 3 Quality Gate (end of Week 2):**
- [ ] `ruff check src/` — zero errors
- [ ] `mypy src/` — zero errors  
- [ ] `pytest` — all existing tests pass (785+)
- [ ] `ai-company dashboard --help` — starts without error
- [ ] WebSocket `/ws/dashboard` accepts connections and sends events
- [ ] `POST /api/tasks` without API key returns 401/403
- [ ] Memory consolidation runs on executor tick
- [ ] Scheduled tasks inject into inbox at correct times

**Sprint 3 Definition of Done:**
1. All P2 features (S3-01 through S3-07, S3-18, S3-19) are merged and verified
2. Dashboard has real-time WebSocket updates, rate limiting, and API docs
3. Memory engine consolidates, searches, and prunes automatically
4. Executor daemon supports scheduled autonomous cycles
5. QA has begun approval test coverage (S3-14)
6. All lint/type/test gates pass

---

### Sprint 4 — Quality & Hardening (Weeks 2-3)
**Goal:** Complete all P3 quality items — Test suites, structured logging, agent validation, CLI hardening.

| ID | Task | Owner | Day | Hours | Gate |
|----|------|-------|-----|-------|------|
| S3-08 | Structured logging with correlation IDs | lead-backend | 1-3 | 3.0 | JSON logs with task_id correlation |
| S3-09 | Agent spec validation CLI | lead-backend | 4 | 2.0 | `ai-company agents validate` works |
| S3-10 | CLI type hints/docstrings | lead-backend | 5-7 | 2.5 | `mypy` clean on all cli/*.py |
| S3-12 | CLI command test suite | qa_engineer | 4-6 | 2.5 | All 24 CLI commands tested |
| S3-13 | API endpoint test suite | qa_engineer | 7-9 | 2.5 | All dashboard endpoints tested |
| S3-17 | Token counting integration | lead-backend | 8 | 1.5 | Tokens tracked per LLM call |
| S3-15 | OAuth2/key rotation | security_engineer | 3-5 | 3.0 | API keys rotatable |
| S3-16 | Memory encryption | security_engineer | 6-7 | 2.0 | Sensitive memory encrypted at rest |
| S3-11 | Full pipeline integration test | qa_engineer | 10-12 | 3.0 | E2E happy path with mocked LLM |
| | **Sprint 4 Total** | | | **22.0** | |

**Sprint 4 Quality Gate (end of Week 3):**
- [ ] `ruff check src/` — zero errors
- [ ] `mypy src/` — zero errors
- [ ] `pytest` — all tests pass including new test suites
- [ ] `ai-company agents validate` — validates all 52 agent spec files
- [ ] Structured JSON logging with correlation IDs in all modules
- [ ] Security: API key rotation works, memory encryption verified
- [ ] Full E2E integration test passes with mocked LLM

**Sprint 4 Definition of Done:**
1. All P3 quality items (S3-08 through S3-13, S3-15 through S3-17) merged and verified
2. Test coverage expanded: CLI, API, approval, and E2E integration tests
3. Structured logging operational across all modules
4. Agent spec validation catches malformed specs
5. Security hardening complete (key rotation, encryption)
6. All lint/type/test gates pass with zero errors

---

### Sprint 5 — Buffer & Polish (Week 4)
**Goal:** Catch any remaining gaps, fix regressions, final documentation pass.

| Activity | Owner | Hours | Gate |
|----------|-------|-------|------|
| Regression testing from Sprint 3-4 | qa_engineer | 2.0 | All tests green |
| Documentation update (STATUS.md, ARCHITECTURE.md) | lead-backend | 1.0 | Docs reflect actual state |
| Performance profiling of executor loop | lead-backend | 1.0 | < 100ms per tick |
| Final ruff/mypy/pytest pass | ALL | 0.5 | Zero errors |
| | **Sprint 5 Total** | **4.5** | |

> **Sprint 5 is buffer capacity.** If Sprint 3-4 complete on time, Sprint 5 handles polish. If they slip, Sprint 5 absorbs the overflow.

---

## 4. Risk Assessment

### 4.1 Risk Matrix

| # | Risk | Probability | Impact | Mitigation |
|---|------|-------------|--------|------------|
| R1 | **Shared file conflicts between lead-frontend and security_engineer** on `dashboard/app.py` | HIGH | HIGH | Enforce sequential editing: lead-frontend completes S3-03 before security starts S3-15. Use feature branches. |
| R2 | **Memory encryption (S3-16) breaks existing memory tests** | MEDIUM | HIGH | Write encryption tests BEFORE implementation (TDD). Run full memory test suite after merge. |
| R3 | **Structured logging (S3-08) causes widespread merge conflicts** as it touches many files | MEDIUM | MEDIUM | Isolate to dedicated branch. Run `ruff` + `mypy` after each file. Batch commit. |
| R4 | **OpenAPI docs (S3-02) require API stability** — if S3-01 changes API surface, docs are stale | MEDIUM | LOW | S3-01 must be complete before S3-02 starts. Lock API contract first. |
| R5 | **E2E integration test (S3-11) reveals hidden bugs** in executor pipeline | MEDIUM | HIGH | This is the whole point — schedule buffer in Sprint 5 for fixes. |
| R6 | **LLM retry fix (S3-19) introduces regression** in provider fallback | LOW | HIGH | Write specific round-robin test before changing code. Run full LLM test suite. |
| R7 | **Capacity overrun** — estimates are optimistic | MEDIUM | MEDIUM | 12.5h buffer across all agents. Sprint 5 is pure buffer. |
| R8 | **Security_engineer blocked** waiting for lead-backend to stabilize memory/API | MEDIUM | HIGH | Security tasks are sequenced last intentionally. If backend slips, security can start OAuth2 (S3-15) early since it touches different files. |

### 4.2 Blocking Scenarios & Contingencies

| Blocker | Impact | Contingency |
|---------|--------|-------------|
| lead-backend blocked on memory consolidation | Delays S3-04, S3-05, S3-06, S3-16 | Parallel path: lead-backend works on S3-08, S3-09, S3-10 (independent tasks) while memory stabilizes |
| qa_engineer tests fail | Delays S3-11 through S3-14 | Isolate failures, file bugs, continue non-blocked tests |
| WebSocket integration incomplete | Blocks S3-02, S3-13 | S3-01 is highest frontend priority — escalate if >2 days |
| security_engineer can't start (API unstable) | Delays S3-15, S3-16 | Move security tasks to Sprint 5, use Sprint 4 buffer |

### 4.3 Risk-Adjusted Priority (If Time Runs Short)

If only 50% of remaining work can be completed (~20h), prioritize these tasks for maximum value:

| Rank | Task | Hours | Value Delivered |
|------|------|-------|-----------------|
| 1 | S3-01 (WebSocket wiring) | 3.0 | Real-time dashboard — core UX |
| 2 | S3-04 (Memory consolidation) | 2.0 | Prevents unbounded memory growth |
| 3 | S3-07 (Scheduled daemon) | 3.0 | Enables autonomous operation |
| 4 | S3-18 (BriefingGenerator fix) | 0.5 | Closes a code quality gap |
| 5 | S3-19 (LLM retry fix) | 1.5 | Improves LLM reliability |
| 6 | S3-03 (Rate limiting) | 1.0 | Production security requirement |
| 7 | S3-14 (Approval tests) | 2.0 | Validates critical approval flow |
| 8 | S3-11 (E2E integration test) | 3.0 | Validates entire pipeline |
| 9 | S3-08 (Structured logging) | 3.0 | Debugging/observability foundation |
| 10 | S3-05 (Memory search) | 2.0 | Enhances memory recall quality |
| | **Total** | **21.0** | **Core features + critical quality** |

**Minimum Viable Completion per Sprint:**

| Sprint | Minimum | What's Sacrificed |
|--------|---------|-------------------|
| Sprint 3 | S3-01, S3-04, S3-07, S3-18, S3-19, S3-03 (9h) | S3-02 (API docs), S3-05 (memory search), S3-06 (TTL) |
| Sprint 4 | S3-14, S3-11, S3-08 (8h) | S3-09, S3-10, S3-12, S3-13, S3-15, S3-16, S3-17 |
| Sprint 5 | Buffer/fix regressions | Polish and documentation |

---

## 5. Communication & Handoff Plan

### 5.1 Daily Standup Protocol

| When | Who | What |
|------|-----|------|
| Start of each day | Chief of Staff + all agents | 5-min async standup in `.opencode/standup/` |
| Format | | `{"agent": "...", "yesterday": [...], "today": [...], "blockers": [...]}` |
| Blocker escalation | Chief of Staff | Within 1 hour of identification |

### 5.2 Handoff Points

| Handoff | From | To | Trigger | Deliverable |
|---------|------|----|---------|-------------|
| H1 | lead-backend | qa_engineer | S3-04 complete | Memory consolidation working + unit tests |
| H2 | lead-frontend | qa_engineer | S3-01 + S3-03 complete | WebSocket + rate limiting working + tests |
| H3 | lead-backend | security_engineer | S3-05 + S3-06 complete | Memory engine stable for encryption |
| H4 | lead-frontend | lead-backend | S3-03 complete | API stable for OAuth2 integration |
| H5 | lead-backend + qa_engineer | ALL | Sprint 3 gate | All P2 features merged + tests pass |
| H6 | ALL | ALL | Sprint 4 gate | All P3 features merged + E2E test passes |

### 5.3 Merge Review Checklist

Before any task is merged:

- [ ] All acceptance criteria met (per task spec)
- [ ] `ruff check src/` — zero new errors
- [ ] `mypy src/` — zero new errors
- [ ] `pytest` — all tests pass (no regressions)
- [ ] New code has unit tests (minimum 80% coverage for new functions)
- [ ] No direct file I/O for shared state (all through MessageBus/FileStore)
- [ ] No `print()` in non-CLI code (use `logger`)
- [ ] No `shell=True` in subprocess calls
- [ ] No hardcoded secrets or API keys
- [ ] Docstrings on all public functions
- [ ] Type hints on all function signatures

### 5.4 Sprint Review & Retro

After each sprint:

1. **Sprint Review** (30 min): Demo completed features, verify quality gates
2. **Sprint Retro** (20 min): What went well, what didn't, what to adjust
3. **STATUS.md Update**: Chief of Staff updates project status
4. **Backlog Grooming**: Re-estimate remaining work, adjust Sprint 5 scope

---

## 6. Parallelism Optimization

### 6.1 Maximum Parallel Tracks

During Sprint 3, up to 4 agents can work simultaneously:

```
Track 1 (lead-frontend):  S3-01 → S3-03 → S3-02
Track 2 (lead-backend):   S3-18, S3-19 → S3-04 → S3-05 → S3-06 → S3-07
Track 3 (qa_engineer):    S3-14 (can start early, independent)
Track 4 (lead-backend):   S3-08, S3-09, S3-10 (independent, parallel with Track 2)
```

During Sprint 4:

```
Track 1 (lead-frontend):  [idle or Sprint 5 prep]
Track 2 (lead-backend):   S3-08 → S3-09 → S3-10 → S3-17
Track 3 (qa_engineer):    S3-11, S3-12, S3-13 (sequential, each ~2.5h)
Track 4 (security_engineer): S3-15 → S3-16
```

### 6.2 Critical Path Analysis

**Sprint 3 Critical Path:** S3-01 (3h) → S3-02 (2h) = 5h  
**Sprint 4 Critical Path:** S3-08 (3h) → S3-10 (2.5h) → S3-12 (2.5h) = 8h  
**Overall Critical Path:** S3-01 → S3-02 → [Sprint 4 starts] → S3-08 → S3-10 → S3-12 → S3-11 = ~16h

**Bottleneck:** qa_engineer is 100% utilized in Sprint 4. If Sprint 3 QA work (S3-14) takes longer than 2h, Sprint 4 QA tasks slip.

---

## 7. Quality Gates

### 7.1 Gate 1: Sprint 3 Entry (Day 1)

**Pre-condition:** Sprint 2 complete, all tests passing, lint clean.

**Verification:**
```bash
cd ai-company
ruff check src/                    # Must be clean
mypy src/                          # Must be clean
pytest --tb=short                  # All 785+ tests pass
ai-company --help                  # CLI works
```

### 7.2 Gate 2: Sprint 3 Exit (End of Week 2)

**All P2 features complete. Additional verification:**

```bash
# Dashboard
python -c "from ai_company.dashboard.ws import manager; print(manager.active_count)"
# Should return 0 (manager initializes correctly)

# Memory
python -c "from ai_company.memory.engine import MemoryStore; m = MemoryStore(); m.store('test', 'hello'); print(m.stats())"
# Should show episodic count > 0

# Scheduler
python -c "from ai_company.orchestrator.scheduler import Scheduler; s = Scheduler(); print('ok')"
# Should initialize without error

# Audit trail
ruff check src/ai_company/dashboard/
ruff check src/ai_company/memory/
ruff check src/ai_company/orchestrator/
pytest tests/unit/test_memory.py tests/unit/test_dashboard.py tests/unit/test_orchestrator.py -v
```

### 7.3 Gate 3: Sprint 4 Exit (End of Week 3)

**All P3 features complete. Additional verification:**

```bash
# Structured logging
grep -r "print(" src/ai_company/ --include="*.py" | grep -v "cli/" | grep -v "test_" | wc -l
# Should return 0 (no bare prints in non-CLI code)

# Agent validation
ai-company agents validate 2>&1 | tail -5
# Should show validation results

# Full test suite
pytest tests/ --tb=short -q
# All tests pass including new test suites

# Security
ruff check src/ai_company/dashboard/app.py
bandit -r src/ai_company/ -q
```

### 7.4 Gate 4: Final Release (Sprint 5)

```bash
# Complete verification battery
ruff check src/                    # Zero errors
mypy src/                          # Zero errors
pytest tests/ --cov=src/ai_company --cov-report=term-missing  # Coverage > 60%
bandit -r src/ai_company/ -q       # No high-severity issues
pre-commit run --all-files         # All hooks pass
ai-company --help                  # CLI functional
ai-company company run --dry-run   # Bootstrap dry-run works
```

---

## 8. Escalation Protocol

| Severity | Example | Response Time | Escalation Path |
|----------|---------|---------------|-----------------|
| **P0 — Blocker** | Task blocked > 4h, tests fail, data loss risk | 1 hour | Chief of Staff → CEO |
| **P1 — Critical** | Dependency delayed > 1 day, scope dispute | 4 hours | Chief of Staff → relevant lead |
| **P2 — Major** | Estimation off by > 30%, quality concern | 24 hours | Chief of Staff, adjust sprint scope |
| **P3 — Minor** | Style disagreement, documentation gap | Next standup | Team discussion |

---

## 9. Tracking & Reporting

### 9.1 Task Status Board

Each agent updates task status in real-time at `docs/TASK-BOARD.md`:

```markdown
| ID | Task | Owner | Status | % | Blocked By |
|----|------|-------|--------|---|------------|
| S3-01 | WebSocket wiring | lead-frontend | NOT STARTED | 0% | — |
| S3-04 | Memory consolidation | lead-backend | NOT STARTED | 0% | — |
```

### 9.2 Progress Metrics

Tracked weekly:

| Metric | Target | Current |
|--------|--------|---------|
| Tasks completed / total | 19/19 | 0/19 |
| Hours burned / estimated | 40h / 40h | 0h / 40h |
| Test count | 850+ | 785 |
| ruff errors | 0 | 0 |
| mypy errors | 0 | 0 |
| Open gaps (ARCHITECTURE-GAPS.md) | 0 | 5 (GAP-014, 015, 018, 019, 020) |

---

## 10. Appendix: Remaining GAP Closure Plan

| GAP | Status | Closing Task | Sprint |
|-----|--------|-------------|--------|
| GAP-014 (BriefingGenerator private method) | OPEN | S3-18 | Sprint 3 |
| GAP-015 (LLM retry provider cycling) | OPEN | S3-19 | Sprint 3 |
| GAP-018 (Structured logging) | PARTIAL | S3-08 | Sprint 4 |
| GAP-019 (Agent spec validation) | OPEN | S3-09 | Sprint 4 |
| GAP-020 (E2E integration test) | PARTIAL | S3-11 | Sprint 4 |

**After Sprint 4:** All 20 gaps in ARCHITECTURE-GAPS.md should be RESOLVED.

---

## Appendix A: Sprint Calendar

```
Week 1 (Jul 21-25):
  Mon-Tue: S3-01 (WS), S3-18, S3-19 (quick fixes)
  Wed-Thu: S3-03 (rate limit), S3-04 (memory consolidation), S3-14 (QA starts)
  Fri: S3-05 (memory search), S3-07 (scheduler starts)

Week 2 (Jul 28-Aug 1):
  Mon-Tue: S3-06 (memory TTL), S3-07 (scheduler), S3-02 (OpenAPI docs)
  Wed: Sprint 3 quality gate — verify all P2 features
  Thu-Fri: Sprint 4 kickoff — S3-08 (logging), S3-09 (validation), S3-11 (E2E starts)

Week 3 (Aug 4-8):
  Mon-Wed: S3-10 (CLI types), S3-12, S3-13 (QA test suites), S3-15 (OAuth2)
  Thu: S3-16 (memory encryption), S3-17 (token counting)
  Fri: Sprint 4 quality gate — full verification battery

Week 4 (Aug 11-15):
  Mon-Tue: Sprint 5 — regression testing, documentation updates
  Wed: Final release verification
  Thu-Fri: Buffer / contingency
```

---

*This plan is a living document. Update after each sprint review. Chief of Staff owns plan maintenance.*
