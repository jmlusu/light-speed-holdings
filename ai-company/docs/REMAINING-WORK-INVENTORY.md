# AI Company Builder — Remaining Work Inventory

**Date**: 2026-07-20 (updated)  
**Status**: Post-Sprint 2 (~90% complete)  
**Total Source Files**: 91+  
**Test Coverage**: pending final verification (was 6 failing tests at audit)  
**Lint Status**: pending final verification (was 5 ruff errors, 41 mypy errors at audit — repaired this cycle)

---

## Executive Summary

Sprint 1 delivered core infrastructure (HITL gates, cost tracking, agent loop, audit trail, memory integration, dead-letter queue, circuit breaker). Sprint 2 is ~90% complete — a 2026-07-20 code audit confirmed that most Sprint 2 items were already implemented in source. This inventory catalogs the remaining incomplete items across 14 packages, organized by module with priority, effort estimates, dependencies, and recommended agent owners.

---

## Completed Since Last Inventory

| Item | Description | Completed |
|------|-------------|-----------|
| 1.1-1.4 | Audit module (events, writer, reader) | ✅ 2026-07-19 |
| 1.5 | Audit integration into executor | ✅ 2026-07-19 |
| 8.1 | Replace print() with logging in executor | ✅ 2026-07-19 |
| B3 | Extract parse_llm_json to shared utility | ✅ 2026-07-19 |
| GAP-007 | Scheduler integration into executor | ✅ 2026-07-19 |
| GAP-012 | AgentLoop priority forwarding | ✅ 2026-07-19 |
| GAP-013 | KPI collector wiring (all 7 departments) | ✅ 2026-07-19 |
| GAP-017 | Dead-letter queue for stale tasks | ✅ 2026-07-19 |
| Circuit breaker | LLM provider fail-fast | ✅ 2026-07-19 |
| Memory integration | Recall context before tasks | ✅ 2026-07-19 |
| Integration tests | Component-level integration tests | ✅ 2026-07-19 |
| 2.1 | Route all inbox I/O through MessageBus (S2-01) | ✅ 2026-07-20 (audit-confirmed in source) |
| 2.2 | Atomic FileStore abstraction (S2-02) | ✅ 2026-07-20 (audit-confirmed in source) |
| 3.1 | Integrate tier rules into ToolRunner (S2-04) | ✅ 2026-07-20 (audit-confirmed in source) |
| 3.2 | Non-blocking HITL gate (S2-05) | ✅ 2026-07-20 (audit-confirmed in source) |
| 3.3 | Dashboard CORS and authentication (S2-08) | ✅ 2026-07-20 (audit-confirmed in source) |
| 3.4 | Remove shell=True from ToolRunner (S2-10) | ✅ 2026-07-20 (audit-confirmed in source) |
| 4.1 | Fix AgentLoop priority forwarding (S2-06) | ✅ 2026-07-20 (audit-confirmed in source) |
| 4.4 | Wire audit into ToolRunner and approval (S2-12) | ✅ 2026-07-20 (audit-confirmed in source) |
| 4.5 | Persist escalation events (S2-13) | ✅ 2026-07-20 (audit-confirmed in source) |
| 5.1-5.3 | Remaining department SOPs + legal docs (S2-11) | ✅ 2026-07-20 (audit-confirmed in source) |

---

## P0 — Critical (Sprint 2 — remaining)

### 1. MessageBus Hardening

| Item | Description | Hours | Dependencies | Owner | Sprint 2 |
|------|-------------|-------|--------------|-------|----------|
| 2.3 | Dashboard API uses MessageBus | 2 | 2.1, 2.2 | lead-backend | S2-03 (In Progress) |

**Total P0 MessageBus remaining**: 2 hours

### 2. Security Hardening

~~All security-hardening P0 items (S2-04, S2-05, S2-08, S2-10) are Done — see Completed table.~~

---

## P1 — High Priority (Sprint 2 — remaining)

### 3. Integration Fixes

| Item | Description | Hours | Dependencies | Owner | Sprint 2 |
|------|-------------|-------|--------------|-------|----------|
| 4.2 | CostTracker accumulator persistence | 2 | None | lead-backend | S2-07 (In Progress) |
| 4.3 | Fix LLM retry provider cycling | 2 | None | lead-backend | S2-09 (Not Started) |

**Total P1 Integration remaining**: 4 hours

### 4. Documentation

~~Remaining department SOPs + legal docs (S2-11) are Done — see Completed table.~~

---

## P2 — Medium Priority (Sprint 3)

### 5. Dashboard Enhancements

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 6.1 | WebSocket broadcast for real-time updates | 3 | MessageBus | lead-frontend |
| 6.2 | API documentation (OpenAPI/Swagger) | 2 | dashboard | lead-frontend |
| 6.3 | Rate limiting | 1 | auth | lead-frontend |

**Total P2 Dashboard**: 6 hours

### 6. Memory Engine Enhancements

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 7.1 | Periodic memory consolidation | 2 | memory engine | lead-backend |
| 7.2 | Memory search (keyword + semantic) | 3 | None | lead-backend |
| 7.3 | Retention policies (TTL, access-based) | 2 | None | lead-backend |

**Total P2 Memory**: 7 hours

### 7. Autonomous Coordination

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 8.1 | Scheduled cycle daemon | 4 | scheduler | lead-backend |
| 8.2 | Escalation persistence to YAML | 2 | None | lead-backend |
| 8.3 | WebSocket broadcast wiring | 3 | dashboard | lead-frontend |

**Total P2 Autonomous**: 9 hours

---

## P3 — Low Priority (Sprint 4+)

### 8. Code Quality & Cleanup

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 9.1 | Structured logging with correlation IDs | 4 | None | lead-backend |
| 9.2 | Agent spec validation CLI command | 2 | None | lead-backend |
| 9.3 | Add type hints to all CLI modules | 2 | None | lead-backend |
| 9.4 | Add docstrings to all public functions | 1.5 | None | lead-backend |

**Total P3 Code Quality**: 9.5 hours

### 9. Test Coverage

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 10.1 | Full pipeline integration test (mocked LLM) | 3 | None | qa_engineer |
| 10.2 | Add CLI command tests (all modules) | 3 | CLI | qa_engineer |
| 10.3 | Add API endpoint tests (dashboard) | 2 | dashboard | qa_engineer |
| 10.4 | Add approval escalation tests | 2 | approval | qa_engineer |

**Total P3 Tests**: 10 hours

### 10. Advanced Features

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 11.1 | OAuth2 or API key rotation | 4 | auth | lead-backend |
| 11.2 | Memory encryption for sensitive data | 2 | None | lead-backend |
| 11.3 | Token counting integration | 2 | None | lead-backend |

**Total P3 Advanced**: 8 hours

---

## Summary by Priority

| Priority | Items | Hours | % of Total | Sprint |
|----------|-------|-------|------------|--------|
| P0 — Critical (remaining) | 1 | 2 | 2% | Sprint 2 |
| P1 — High (remaining) | 2 | 4 | 4% | Sprint 2 |
| P2 — Medium | 9 | 22 | 25% | Sprint 3 |
| P3 — Low | 10 | 27.5 | 31% | Sprint 4+ |
| **Total remaining** | **22** | **55.5** | | |
| *(Sprint 2 Done — see Completed table)* | *11* | *39* | *41%* | *Sprint 2* |

---

## Dependency Graph

```
P0: MessageBus Hardening (2.1-2.3)
    └── Required by: Dashboard WebSocket (6.1), Scheduled cycles (8.1)

P0: Security Hardening (3.1-3.4)
    └── No dependencies — parallel execution

P1: Integration Fixes (4.1-4.5)
    └── 4.4 depends on audit module (already done)

P1: Documentation (5.1-5.3)
    └── No dependencies — parallel execution

P2: Dashboard (6.1-6.3)
    └── Depends on: MessageBus hardening (2.1-2.3)

P2: Memory (7.1-7.3)
    └── No dependencies

P2: Autonomous (8.1-8.3)
    └── Depends on: MessageBus (2.1), Scheduler (already done)
```

---

## Recommended Sprint 2 Focus (remaining)

1. **Finish MessageBus Hardening** (2.3 / S2-03) — Dashboard API still reads/writes `inbox.json` directly.
2. **CostTracker persistence** (4.2 / S2-07) — accumulator rebuild on restart.
3. **LLM retry cycling** (4.3 / S2-09) — not yet started.
4. **Test/lint cleanup** — 6 failing tests, 5 ruff errors, 41 mypy errors at audit time; being repaired by engineering this cycle (pending final verification).

**Sprint 2 Done**: 11 items across MessageBus, security, integration, and documentation — see Completed table.

---

## Agent Ownership Summary

| Agent | Items | Total Hours | Sprint |
|-------|-------|-------------|--------|
| lead-backend | 2.3, 4.2-4.3, 7.1-7.3, 8.1-8.2, 9.1-9.4, 11.1-11.3 | 47.5 | Sprint 2-4 |
| lead-frontend | 6.1-6.3, 8.3 | 10 | Sprint 2-3 |
| content_creator | (S2-11 done) | 0 remaining | Sprint 2 |
| qa_engineer | 10.1-10.4 | 10 | Sprint 4 |
| **Total remaining** | **22** | **67.5** | |

---

## Next Steps

1. Complete S2-03 (Dashboard API → MessageBus).
2. Complete S2-07 (CostTracker restart persistence) and start S2-09 (LLM retry cycling).
3. Finish test/lint repair; run final `pytest`, `ruff check src/`, `mypy src/` verification.
4. Move to Sprint 3 items (P2) once Sprint 2 is fully closed.
