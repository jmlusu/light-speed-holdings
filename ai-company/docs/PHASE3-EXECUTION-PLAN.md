# Phase 3 Execution Plan — Autonomous Coordination

**Author:** Chief of Staff  
**Date:** 2026-07-19  
**Status:** APPROVED  
**Sprint Duration:** ~2 weeks (target)  
**Agents Dispatched:** 7 (board-technology, caio, chief-ai-officer, content-writer, data-engineer, dept_engineering, chief-of-staff)

---

## 1. Phase 3 Objectives

### Primary Goal
Transform AI Company Builder from a manually-coordinated system into an autonomous, self-governing agent hierarchy with persistent memory, scheduled execution, and real-time observability.

### Success Criteria
| Criterion | Metric | Target |
|-----------|--------|--------|
| Autonomous execution | Scheduled tasks complete without human trigger | 100% of cron jobs fire and complete |
| Memory integration | Agent loop reads/writes memory on every task | Episodic + semantic memories stored per task |
| Observability | Dashboard shows live KPIs from all 7 departments | 7/7 department KPIs wired |
| Security posture | No shell injection, auth on all write endpoints | 0 shell=True, JWT auth on dashboard |
| Task reliability | Stale tasks recovered, failed tasks don't block pipeline | Timeout + DLQ operational |
| Test coverage | Tests for all new functionality | 500+ tests, all passing |
| Documentation | API docs, ADRs, user guides complete | All public APIs documented |

### What Phase 3 is NOT
- Not a feature-freeze release — this is infrastructure hardening
- Not a new agent hiring wave — we optimize what we have
- Not a UI redesign — dashboard gets auth + live data, not a facelift

---

## 2. Sprint 3 Scope — Work Breakdown

### 2.1 Architecture Gap Resolution (4 HIGH-severity gaps)

These are the **foundation** for everything else. No other work should proceed until GAP-005 and GAP-007 are resolved.

| Gap | Description | Effort | Blocks |
|-----|-------------|--------|--------|
| GAP-005 | Memory engine integration into executor pipeline | High | Memory enhancements (6.x), CLI memory (7.3) |
| GAP-007 | Scheduler-to-executor wiring | Medium | Task timeout (GAP-017), autonomous cycles |
| GAP-008 | Escalation event persistence | Low | Dashboard escalation visibility |
| GAP-017 | Task timeout + dead letter queue | Medium | Stale task recovery, reliability |

### 2.2 Remaining Work Items (from inventory)

**P2 — Dashboard Enhancements (Sprint 3 items)**
| Item | Description | Hours | Owner |
|------|-------------|-------|-------|
| 5.1 | JWT/session authentication on API endpoints | 3 | board-technology (arch) + dept_engineering (impl) |
| 5.2 | WebSocket reconnection logic | 1.5 | dept_engineering |
| 5.3 | Rate limiting on API endpoints | 1 | dept_engineering |
| 5.4 | Real-time KPI streaming (SSE/WebSocket) | 2 | data-engineer + dept_engineering |
| 5.5 | CORS configuration for production | 0.5 | board-technology (design) + dept_engineering (impl) |

**P2 — Memory Engine Enhancements**
| Item | Description | Hours | Owner |
|------|-------------|-------|-------|
| 6.1 | Semantic classification for memories | 3 | caio |
| 6.2 | Retention policies (TTL, access-based) | 2 | chief-ai-officer |
| 6.3 | Encryption for sensitive memories | 2 | board-technology (design) + dept_engineering (impl) |
| 6.4 | Memory consolidation rules | 2 | caio |
| 6.5 | Memory search (keyword + semantic) | 3 | caio |

**P2 — CLI Module Completion**
| Item | Description | Hours | Owner |
|------|-------------|-------|-------|
| 7.1 | `cli/board.py` — Board meeting scheduling, minutes | 3 | dept_engineering |
| 7.2 | `cli/workflows.py` — Full workflow lifecycle | 4 | dept_engineering |
| 7.3 | `cli/memory.py` — Enhanced memory management | 2 | chief-ai-officer |
| 7.4 | `cli/executives.py` — Executive performance tracking | 2 | dept_engineering |
| 7.5 | `cli/departments.py` — Department analytics | 2 | dept_engineering |
| 7.6 | `cli/audit.py` — Audit log query/export | 1.5 | dept_engineering |

**P3 — Code Quality & Cleanup (fast wins)**
| Item | Description | Hours | Owner |
|------|-------------|-------|-------|
| 8.1-8.3 | Replace print() with logging (3 files) | 1.25 | dept_engineering |
| 8.4 | Type hints for all CLI modules | 2 | dept_engineering |
| 8.5 | Docstrings for all public functions | 1.5 | content-writer |

**P3 — Test Coverage Gaps**
| Item | Description | Hours | Owner |
|------|-------------|-------|-------|
| 9.1 | Integration tests for message_bus ACK/NACK | 2 | dept_engineering |
| 9.2 | Integration tests for approval escalation | 2 | dept_engineering |
| 9.3 | Unit tests for LLM provider circuit breaker | 1.5 | caio |
| 9.4 | Unit tests for memory encryption | 1 | dept_engineering |
| 9.5 | API endpoint tests (dashboard) | 2 | dept_engineering |
| 9.6 | CLI command tests (all modules) | 3 | dept_engineering |

**P3 — Documentation**
| Item | Description | Hours | Owner |
|------|-------------|-------|-------|
| 10.1 | API documentation (OpenAPI/Swagger) | 2 | content-writer |
| 10.2 | Architecture Decision Records (ADRs) | 3 | board-technology |
| 10.3 | Inline code comments for complex logic | 2 | content-writer |
| 10.4 | Developer onboarding guide | 2 | content-writer |

### 2.3 Sprint 3 Scope Exclusions (deferred to Sprint 4)
- GAP-013: KPI department collector wiring (all 7 depts) — data-engineer begins design, implementation in Sprint 4
- GAP-018: Structured logging with correlation IDs — dept_engineering spikes, full implementation in Sprint 4
- GAP-019: Agent spec validation — deferred
- GAP-020: Full end-to-end integration tests — deferred (subset in Sprint 3)

---

## 3. Agent Assignments

### 3.1 board-technology — Architecture & Security Hardening

**Role:** Architecture authority, security reviewer, ADR author

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| BT-1 | Write ADR-003: FileStore Abstraction | ADR doc in `docs/adr/` with context, decision, consequences | 2 |
| BT-2 | Write ADR-004: Memory Integration Architecture | ADR doc covering 6 memory types, integration points, retention | 2 |
| BT-3 | Write ADR-005: Dashboard Authentication Strategy | ADR comparing JWT vs API key vs OAuth2; recommendation with rationale | 1.5 |
| BT-4 | Security review: Dashboard auth design (GAP-010) | Threat model, auth flow diagram, CORS policy recommendation | 2 |
| BT-5 | Security review: Memory encryption approach (Item 6.3) | Encryption-at-rest design, key management approach | 1.5 |
| BT-6 | Security review: shell=True removal (GAP-016) | Validate dept_engineering's shlex implementation, command allowlist | 1 |
| BT-7 | Architecture review of FileStore atomic writes | Review dept_engineering's FileStore impl, ensure cross-platform locking | 2 |
| BT-8 | Review and approve all ADRs from other agents | Ensure consistency, no conflicts, proper format | 1 |

**Total:** ~13 hours

**Exit Criteria:**
- [ ] 3 ADRs published in `docs/adr/`
- [ ] Security review sign-off on dashboard auth
- [ ] Security review sign-off on memory encryption
- [ ] FileStore architecture approved

---

### 3.2 caio (Chief AI Officer) — AI Strategy, Token Counting, Cost Optimization

**Role:** AI/ML strategy, model optimization, memory intelligence

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| CAIO-1 | Implement semantic memory classification (Item 6.1) | Memories auto-classified into episodic/semantic/procedural/relational/temporal | 3 |
| CAIO-2 | Implement memory consolidation rules (Item 6.4) | Periodic consolidation merges related memories, deduplicates, summarizes | 2 |
| CAIO-3 | Implement memory search — keyword + semantic (Item 6.5) | Search returns ranked results; supports filters by type, agent, time range | 3 |
| CAIO-4 | Design token counting integration (Item 4.4) | Architecture doc for tiktoken (OpenAI) + local counting (Ollama) | 1.5 |
| CAIO-5 | Design cost calculation per request (Item 4.5) | Cost model: cache hit vs compute, per-provider pricing | 1.5 |
| CAIO-6 | Write AI strategy doc for Phase 4 (agent self-improvement) | Draft: feedback loops, prompt optimization, agent performance scoring | 2 |

**Total:** ~13 hours

**Dependencies:**
- GAP-005 (memory integration) must be complete before CAIO-1, CAIO-2, CAIO-3 can start
- CAIO-4 and CAIO-5 are independent — can start immediately

**Exit Criteria:**
- [ ] Semantic classifier works on test memories
- [ ] Consolidation reduces memory count by ≥20% on test data
- [ ] Memory search returns relevant results for 10 test queries
- [ ] Token counting architecture doc reviewed by board-technology
- [ ] Cost model document reviewed by chief-of-staff

---

### 3.3 chief-ai-officer — Model Routing, Prompt Engineering, Agent Self-Improvement

**Role:** Model selection, prompt quality, agent performance

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| CAI-1 | Implement priority-based model routing (GAP-012 fix) | AgentLoop forwards task priority to router; HIGH/CRITICAL get premium models | 2 |
| CAI-2 | Implement memory retention policies (Item 6.2) | TTL-based expiry, access-count-based retention, configurable per memory type | 2 |
| CAI-3 | Design prompt engineering framework | Document: prompt templates, few-shot patterns, chain-of-thought templates | 2 |
| CAI-4 | Design agent self-improvement loop | Document: feedback collection, success metrics, prompt iteration cycle | 2 |
| CAIO-5 | Implement CLI memory management (Item 7.3) | `ai-company memory list/search/delete/consolidate` commands | 2 |
| CAIO-6 | Fix BriefingGenerator private method usage (GAP-014) | Use public `get_all_tasks()` method, add tests | 0.5 |

**Total:** ~10.5 hours

**Dependencies:**
- CAI-2 (retention policies) depends on GAP-005 (memory integration) being complete
- CAI-1 (priority routing) is independent — can start immediately
- CAIO-6 is independent — can start immediately

**Exit Criteria:**
- [ ] Priority routing test: CRITICAL task gets premium model, LOW gets fast model
- [ ] Retention policy removes expired memories on consolidation run
- [ ] Prompt engineering framework doc published
- [ ] Agent self-improvement loop doc published
- [ ] `ai-company memory` commands work end-to-end
- [ ] BriefingGenerator uses public API, no private method access

---

### 3.4 content-writer — Documentation, SOPs, User Guides, API Docs

**Role:** Documentation quality, user experience, knowledge management

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| CW-1 | Generate OpenAPI/Swagger docs from FastAPI (Item 10.1) | `/docs` endpoint serves interactive API documentation | 1.5 |
| CW-2 | Write inline code comments for complex logic (Item 10.3) | All functions in `executor/`, `orchestrator/`, `memory/` have docstrings | 2 |
| CW-3 | Update user guide for Phase 3 features | Memory management, scheduled tasks, dashboard auth sections added | 2 |
| CW-4 | Write Phase 3 release notes | Changelog entry with all additions, fixes, breaking changes | 1 |
| CW-5 | Add docstrings to all public functions (Item 8.5) | All CLI modules and public APIs have Google-style docstrings | 1.5 |
| CW-6 | Write onboarding guide for new developers (Item 10.4) | Step-by-step: setup, architecture overview, how to add a CLI command | 2 |

**Total:** ~10 hours

**Dependencies:**
- CW-1 depends on dashboard auth being implemented (5.1)
- CW-3 depends on knowing final feature set (coordinate with chief-of-staff)
- CW-2, CW-4, CW-5, CW-6 are independent

**Exit Criteria:**
- [ ] `/docs` endpoint serves valid OpenAPI spec
- [ ] All public functions in target modules have docstrings
- [ ] User guide covers memory, scheduling, auth
- [ ] Release notes drafted and reviewed
- [ ] Onboarding guide covers setup through first CLI command

---

### 3.5 data-engineer — KPI Data Pipelines, Analytics Infrastructure, Data Retention

**Role:** Data infrastructure, KPI collection, analytics

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| DE-1 | Wire all 7 department KPI collectors (GAP-013) | `collect_all_kpis()` dynamically discovers all department modules | 2 |
| DE-2 | Implement real-time KPI streaming (Item 5.4) | SSE endpoint pushes KPI updates on change; WebSocket fallback | 2 |
| DE-3 | Design KPI data retention policy | Document: how long KPIs stored, aggregation strategy, archival | 1.5 |
| DE-4 | Add KPI API endpoint tests | Tests for all 7 department endpoints + aggregate endpoint | 2 |
| DE-5 | Design data pipeline for agent performance metrics | Document: task completion rate, avg response time, cost per task | 2 |

**Total:** ~9.5 hours

**Dependencies:**
- DE-2 depends on dashboard auth (5.1) for production deployment
- DE-1 is independent — can start immediately
- DE-4 depends on DE-1 completion

**Exit Criteria:**
- [ ] All 7 department KPIs appear in dashboard
- [ ] SSE endpoint streams KPI updates in real-time
- [ ] KPI retention policy document published
- [ ] KPI API tests pass for all departments
- [ ] Agent performance metrics design doc reviewed

---

### 3.6 dept_engineering — Code Quality, Testing, CI/CD, Deployment

**Role:** Implementation workhorse, code quality, testing

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| DE-ENG-1 | Implement FileStore abstraction (GAP-002) | Atomic JSON/YAML read/write, cross-platform file locking | 3 |
| DE-ENG-2 | Route executor I/O through MessageBus (GAP-001) | All inbox reads/writes go through bus; no direct file access in executor | 2 |
| DE-ENG-3 | Fix shell=True vulnerability (GAP-016) | Use shlex.split(), command allowlist, integrate with tier_rules | 2 |
| DE-ENG-4 | Implement dashboard auth (Item 5.1) | JWT middleware on write endpoints, API key for service-to-service | 3 |
| DE-ENG-5 | Implement rate limiting (Item 5.3) | Slowapi or similar; configurable per-endpoint limits | 1 |
| DE-ENG-6 | WebSocket reconnection logic (Item 5.2) | Auto-reconnect with exponential backoff, max retries | 1.5 |
| DE-ENG-7 | CORS configuration (Item 5.5) | Environment-variable-based CORS origins, secure defaults | 0.5 |
| DE-ENG-8 | Memory encryption for sensitive data (Item 6.3) | Fernet encryption for memories tagged `sensitive`; key from env | 2 |
| DE-ENG-9 | Implement `cli/board.py` (Item 7.1) | Board meeting scheduling, minutes generation, attendance tracking | 3 |
| DE-ENG-10 | Implement `cli/workflows.py` (Item 7.2) | Full workflow lifecycle: create, start, pause, resume, complete | 4 |
| DE-ENG-11 | Implement `cli/executives.py` (Item 7.4) | Executive performance: tasks completed, avg time, cost efficiency | 2 |
| DE-ENG-12 | Implement `cli/departments.py` (Item 7.5) | Department analytics: team performance, budget utilization | 2 |
| DE-ENG-13 | Implement `cli/audit.py` (Item 7.6) | Audit log query: by agent, by date, by severity, export to CSV | 1.5 |
| DE-ENG-14 | Replace print() with logging (Items 8.1-8.3) | All 3 files use stdlib logging, no print() in production code | 1.25 |
| DE-ENG-15 | Add type hints to CLI modules (Item 8.4) | All CLI modules fully typed, mypy clean | 2 |
| DE-ENG-16 | Integration tests: ACK/NACK (Item 9.1) | Tests for message delivery confirmation and negative acknowledgment | 2 |
| DE-ENG-17 | Integration tests: approval escalation (Item 9.2) | Tests for 5-tier escalation with timeout | 2 |
| DE-ENG-18 | Unit tests: memory encryption (Item 9.4) | Tests for encrypt/decrypt cycle, key management | 1 |
| DE-ENG-19 | API endpoint tests (Item 9.5) | Tests for all dashboard REST endpoints | 2 |
| DE-ENG-20 | CLI command tests (Item 9.6) | Tests for all new CLI commands (board, workflows, memory, exec, dept, audit) | 3 |

**Total:** ~40.75 hours

**Critical Path:**
```
DE-ENG-1 (FileStore) → DE-ENG-2 (MessageBus routing) → DE-ENG-10 (Workflows CLI)
DE-ENG-4 (Dashboard auth) → CW-1 (OpenAPI docs)
DE-ENG-3 (shell=True) → DE-ENG-16 (ACK/NACK tests)
```

**Exit Criteria:**
- [ ] FileStore: atomic writes pass concurrent test
- [ ] Executor has zero direct file I/O (all through MessageBus)
- [ ] No `shell=True` in codebase (grep confirms)
- [ ] Dashboard auth: unauthenticated write returns 401
- [ ] Rate limiting: 101st request in window returns 429
- [ ] All new CLI commands have tests
- [ ] All new integration tests pass
- [ ] ruff clean, mypy clean, 0 print() in production code

---

### 3.7 chief-of-staff — Coordination, Tracking, Blocker Resolution

**Role:** Orchestrator, status tracker, blocker escalator

**Sprint 3 Deliverables:**

| # | Task | Acceptance Criteria | Hours |
|---|------|---------------------|-------|
| COS-1 | Create Sprint 3 task board (issue tracking) | GitHub issues for all 50+ tasks with labels and milestones | 2 |
| COS-2 | Daily standup coordination | Async standup thread; collect status from 6 agents daily | ongoing |
| COS-3 | Blocker identification and resolution | Track blockers, escalate to CEO when needed, unblock within 24h | ongoing |
| COS-4 | Cross-agent dependency management | Ensure FileStore → MessageBus → Workflows chain stays on track | ongoing |
| COS-5 | Weekly executive summary | Status report: % complete, risks, blockers, budget burn | 1/week |
| COS-6 | Sprint 3 retrospective facilitation | Post-sprint retro: what worked, what didn't, improvements | 2 |
| COS-7 | Phase 4 planning draft | Based on Sprint 3 outcomes, draft Phase 4 scope and priorities | 3 |

**Total:** ~8 hours + ongoing coordination

**Exit Criteria:**
- [ ] Task board created with all Sprint 3 items
- [ ] Weekly status reports delivered on schedule
- [ ] All blockers resolved or escalated within 24h
- [ ] Sprint 3 retro completed
- [ ] Phase 4 draft ready for CEO review

---

## 4. Dependency Map

### 4.1 Critical Path Dependencies

```
                    ┌─────────────────────────────────────────────┐
                    │           PHASE 3 DEPENDENCY GRAPH          │
                    └─────────────────────────────────────────────┘

    ┌──────────┐     ┌──────────────┐     ┌──────────────┐
    │ GAP-002  │────▶│  GAP-001     │────▶│ Item 7.2     │
    │ FileStore│     │ MessageBus   │     │ Workflows CLI│
    │ (DE-ENG-1)│    │ (DE-ENG-2)   │     │ (DE-ENG-10)  │
    └──────────┘     └──────┬───────┘     └──────────────┘
                            │
                    ┌───────▼───────┐     ┌──────────────┐
                    │  GAP-005      │────▶│ Items 6.1-6.5│
                    │  Memory Integ │     │ Memory Enhance│
                    │ (DE-ENG + CAIO)│    │ (CAIO-1,2,3) │
                    └───────┬───────┘     └──────────────┘
                            │
                    ┌───────▼───────┐     ┌──────────────┐
                    │  GAP-007      │────▶│ GAP-017      │
                    │  Scheduler    │     │ Task Timeout │
                    │ (DE-ENG)      │     │ (DE-ENG)     │
                    └───────────────┘     └──────────────┘

    ┌──────────┐     ┌──────────────┐     ┌──────────────┐
    │ Item 5.1 │────▶│ Item 5.4     │────▶│ CW-1         │
    │ Dashboard│     │ KPI Streaming│     │ OpenAPI Docs │
    │ Auth     │     │ (DE-2)       │     │ (content-writer)│
    │ (DE-ENG-4)│    └──────────────┘     └──────────────┘
    └──────────┘
```

### 4.2 Parallel Work Streams

**Stream A — Infrastructure (no dependencies, start immediately):**
- DE-ENG-1: FileStore abstraction
- DE-ENG-3: Shell injection fix
- DE-ENG-4: Dashboard auth
- CAI-1: Priority-based model routing
- CAIO-6: BriefingGenerator fix
- DE-1: KPI collector wiring
- CAIO-4, CAIO-5: Token counting + cost model design

**Stream B — Memory (after GAP-005):**
- CAIO-1: Semantic classification
- CAIO-2: Consolidation rules
- CAIO-3: Memory search
- CAI-2: Retention policies
- DE-ENG-8: Memory encryption
- CLI-7.3: Memory CLI commands

**Stream C — Orchestration (after GAP-007):**
- GAP-017: Task timeout + DLQ
- CLI-7.2: Workflows CLI
- CLI-7.1: Board CLI
- CLI-7.4: Executives CLI
- CLI-7.5: Departments CLI
- CLI-7.6: Audit CLI

**Stream D — Documentation (parallel, no blockers):**
- CW-1: OpenAPI docs (blocked on dashboard auth)
- CW-2: Inline comments
- CW-3: User guide updates
- CW-4: Release notes
- CW-5: Docstrings
- CW-6: Onboarding guide
- BT-1, BT-2, BT-3: ADRs

**Stream E — Testing (after implementation):**
- DE-ENG-16: ACK/NACK tests
- DE-ENG-17: Escalation tests
- DE-ENG-18: Memory encryption tests
- DE-ENG-19: API tests
- DE-ENG-20: CLI tests
- DE-4: KPI endpoint tests

---

## 5. Risk Mitigation Plan

### 5.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| FileStore cross-platform locking fails on Windows | Medium | High | Board-technology reviews impl; use `msvcrt.locking` with fallback; test on both platforms |
| Memory integration breaks existing tests | Medium | Medium | Run full test suite after each integration point; feature-flag memory reads in executor |
| Dashboard auth breaks existing API consumers | Low | High | Auth is opt-in via env var; default to no-auth for development |
| Shell injection fix breaks legitimate commands | Medium | High | Command allowlist is permissive by default; log blocked commands for tuning |
| LLM provider changes break token counting | Low | Medium | Abstract tokenizer behind interface; mock in tests |

### 5.2 Coordination Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Agent task overlap/duplication | Medium | Medium | Chief-of-staff owns task board; daily async standup; clear ownership matrix |
| Blocker cascades on critical path | High | High | FileStore (DE-ENG-1) is day-1 priority; if blocked, chief-of-staff escalates to CEO within 4h |
| Scope creep during implementation | Medium | Medium | Sprint 3 scope is locked; new items go to Sprint 4 backlog |
| Testing bottleneck at end of sprint | High | Medium | Testing is interleaved (not batched); each agent writes tests alongside implementation |

### 5.3 Budget Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM API costs spike during testing | Low | Low | Use local Ollama for dev/testing; premium models only for integration tests |
| Sprint 3 overruns into Sprint 4 | Medium | Medium | 50+ hours of work across 7 agents; buffer is ~20% (10 hours) |

---

## 6. Timeline and Milestones

### Week 1: Foundation (Days 1-5)

| Day | Milestone | Owner |
|-----|-----------|-------|
| D1 | Sprint 3 kickoff; task board created; FileStore impl starts | COS + DE-ENG |
| D1 | Security reviews begin (dashboard auth, memory encryption) | board-technology |
| D1 | Token counting + cost model design starts | caio |
| D2 | FileStore unit tests pass | DE-ENG |
| D2 | Shell injection fix (shlex + allowlist) complete | DE-ENG |
| D3 | FileStore integrated into MessageBus | DE-ENG |
| D3 | GAP-005 (memory integration) implementation begins | DE-ENG |
| D3 | Dashboard auth implementation begins | DE-ENG |
| D4 | GAP-005 complete: executor reads/writes memory | DE-ENG |
| D4 | Priority-based model routing working | chief-ai-officer |
| D5 | Dashboard auth + rate limiting + CORS complete | DE-ENG |
| D5 | **Milestone 1: FileStore, shell fix, auth, memory integration done** | All |

### Week 2: Integration (Days 6-10)

| Day | Milestone | Owner |
|-----|-----------|-------|
| D6 | Memory enhancements begin (semantic search, consolidation) | caio |
| D6 | GAP-007 (scheduler wiring) implementation | DE-ENG |
| D7 | KPI collector wiring complete (all 7 departments) | data-engineer |
| D7 | GAP-017 (task timeout + DLQ) implementation | DE-ENG |
| D8 | Scheduler + timeout + DLQ all wired | DE-ENG |
| D8 | Memory encryption complete | DE-ENG |
| D9 | All CLI modules implemented | DE-ENG |
| D9 | ADRs drafted (3 ADRs) | board-technology |
| D10 | **Milestone 2: All implementation complete** | All |

### Week 3: Quality & Documentation (Days 11-14)

| Day | Milestone | Owner |
|-----|-----------|-------|
| D11 | Integration tests for ACK/NACK, escalation | DE-ENG |
| D11 | API endpoint tests | DE-ENG |
| D12 | CLI command tests for all new modules | DE-ENG |
| D12 | OpenAPI docs generated | content-writer |
| D13 | All docstrings + inline comments complete | content-writer |
| D13 | User guide updated, onboarding guide written | content-writer |
| D14 | Release notes drafted | content-writer |
| D14 | **Milestone 3: Quality + documentation complete** | All |

### Week 4: Finalize (Days 15-17)

| Day | Milestone | Owner |
|-----|-----------|-------|
| D15 | Full test suite pass (target: 500+ tests) | DE-ENG |
| D15 | ruff + mypy clean | DE-ENG |
| D15 | Sprint 3 retro | COS |
| D16 | Phase 4 planning draft | COS |
| D16 | Final integration verification | COS + DE-ENG |
| D17 | **Milestone 4: Phase 3 complete, ready for CEO review** | COS |

---

## 7. Definition of Done — Phase 3

### 7.1 Functional Requirements

| # | Requirement | Verification |
|---|-------------|-------------|
| FR-1 | All scheduled tasks execute autonomously without human trigger | Run scheduler, observe task completion in inbox.json |
| FR-2 | Agent loop stores episodic and semantic memories on every task | Check memory store after task execution |
| FR-3 | Dashboard shows live KPIs from all 7 departments | Navigate to dashboard, verify all department panels populated |
| FR-4 | Dashboard rejects unauthenticated write requests | curl POST without JWT returns 401 |
| FR-5 | Stale IN_PROGRESS tasks are recovered or moved to DLQ | Create stuck task, run executor, verify recovery |
| FR-6 | No shell=True anywhere in codebase | `grep -r "shell=True" src/` returns empty |
| FR-7 | Memory search returns relevant results for keyword queries | Run `ai-company memory search "test query"` |
| FR-8 | All new CLI commands functional and tested | Run each command, verify output + test coverage |

### 7.2 Quality Requirements

| # | Requirement | Verification |
|---|-------------|-------------|
| QR-1 | All tests pass | `pytest` — 0 failures |
| QR-2 | Test count ≥ 500 | `pytest --co -q \| tail -1` |
| QR-3 | ruff clean | `ruff check src/` — 0 warnings |
| QR-4 | mypy clean | `mypy src/` — 0 errors |
| QR-5 | No print() in production code | `grep -r "print(" src/ --include="*.py" \| grep -v __pycache__` returns empty |
| QR-6 | All public functions have docstrings | Spot-check + mypy --strict on key modules |
| QR-7 | OpenAPI spec served at /docs | Browse to http://localhost:8000/docs |

### 7.3 Documentation Requirements

| # | Requirement | Verification |
|---|-------------|-------------|
| DR-1 | 3 ADRs published in docs/adr/ | File exists, reviewed by board-technology |
| DR-2 | User guide updated with Phase 3 features | docs/USER-GUIDE.md covers memory, scheduling, auth |
| DR-3 | API documentation complete | OpenAPI spec describes all endpoints |
| DR-4 | Onboarding guide published | docs/ONBOARDING.md exists, tested by chief-of-staff |
| DR-5 | Release notes drafted | CHANGELOG.md updated with Phase 3 entries |
| DR-6 | Phase 4 planning draft ready | docs/PHASE4-DRAFT.md exists, reviewed by COS |

---

## 8. Communication Plan

### 8.1 Daily Async Standup

**Time:** End of each work day  
**Format:** Each agent posts to the sprint channel:
```
## [Agent Name] — Day [N]

**Completed:**
- [task]

**In Progress:**
- [task]

**Blocked:**
- [blocker] → escalated to [who]

**Tomorrow:**
- [plan]
```

### 8.2 Escalation Protocol

| Level | Trigger | Action |
|-------|---------|--------|
| L1 — Agent-to-Agent | Dependency wait > 4h | Message blocking agent directly |
| L2 — Chief of Staff | Dependency wait > 8h or technical disagreement | COS mediates, reassigns, or escalates |
| L3 — CEO | Budget overrun, scope change, architectural disagreement | COS briefs CEO, CEO decides |

### 8.3 Weekly Executive Summary

**Delivered by:** Chief of Staff to CEO  
**Day:** End of Week 1 and Week 2  
**Format:**
```
## Phase 3 — Week [N] Executive Summary

**Overall Status:** 🟢 On Track / 🟡 At Risk / 🔴 Blocked

**Completed:** [X] / [Y] tasks
**In Progress:** [list]
**Blocked:** [list with resolution plan]

**Budget:** [hours used] / [hours allocated]
**Risks:** [top 3]
**Decisions Needed:** [any CEO decisions required]
```

---

## 9. Appendix: Hour Summary by Agent

| Agent | Estimated Hours | % of Total |
|-------|----------------|------------|
| board-technology | 13 | 10% |
| caio | 13 | 10% |
| chief-ai-officer | 10.5 | 8% |
| content-writer | 10 | 8% |
| data-engineer | 9.5 | 7% |
| dept_engineering | 40.75 | 31% |
| chief-of-staff | 8 + ongoing | 6% |
| **Buffer (20%)** | **~26** | **20%** |
| **Total** | **~130** | **100%** |

**Note:** dept_engineering carries the heaviest implementation load. If velocity is a concern, consider:
1. Prioritizing Stream A (FileStore, shell fix, auth) over Stream C (CLI modules)
2. Deferring CLI modules 7.4, 7.5 to Sprint 4 if timeline slips
3. Chief-of-staff monitors DE-ENG bandwidth daily and reallocates if needed

---

*This plan is a living document. Chief-of-staff owns updates. Last updated: 2026-07-19.*
