# AI Company Builder — Remaining Work Inventory

**Date**: 2026-07-20 (updated)  
**Status**: Post-Sprint 1  
**Total Source Files**: 91+  
**Test Coverage**: 727 tests collected  
**Lint Status**: ruff clean, mypy clean

---

## Executive Summary

Sprint 1 delivered core infrastructure (HITL gates, cost tracking, agent loop, audit trail, memory integration, dead-letter queue, circuit breaker). This inventory catalogs all remaining incomplete items across 14 packages, organized by module with priority, effort estimates, dependencies, and recommended agent owners.

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

---

## P0 — Critical (Sprint 2)

### 1. MessageBus Hardening

| Item | Description | Hours | Dependencies | Owner | Sprint 2 |
|------|-------------|-------|--------------|-------|----------|
| 2.1 | Route all inbox I/O through MessageBus | 4 | None | lead-backend | S2-01 |
| 2.2 | Create atomic FileStore abstraction | 6 | 2.1 | lead-backend | S2-02 |
| 2.3 | Dashboard API uses MessageBus | 2 | 2.1, 2.2 | lead-backend | S2-03 |

**Total P0 MessageBus**: 12 hours

### 2. Security Hardening

| Item | Description | Hours | Dependencies | Owner | Sprint 2 |
|------|-------------|-------|--------------|-------|----------|
| 3.1 | Integrate tier rules into ToolRunner | 4 | None | lead-backend | S2-04 |
| 3.2 | Non-blocking HITL gate | 4 | 3.1 | lead-backend | S2-05 |
| 3.3 | Dashboard CORS and authentication | 3 | None | lead-frontend | S2-08 |
| 3.4 | Remove shell=True from ToolRunner | 2 | None | lead-backend | S2-10 |

**Total P0 Security**: 13 hours

---

## P1 — High Priority (Sprint 2)

### 3. Integration Fixes

| Item | Description | Hours | Dependencies | Owner | Sprint 2 |
|------|-------------|-------|--------------|-------|----------|
| 4.1 | Fix AgentLoop priority forwarding | 1 | None | lead-backend | S2-06 |
| 4.2 | CostTracker accumulator persistence | 2 | None | lead-backend | S2-07 |
| 4.3 | Fix LLM retry provider cycling | 2 | None | lead-backend | S2-09 |
| 4.4 | Wire audit into ToolRunner and approval | 3 | audit module | lead-backend | S2-12 |
| 4.5 | Persist escalation events | 2 | None | lead-backend | S2-13 |

**Total P1 Integration**: 10 hours

### 4. Documentation

| Item | Description | Hours | Dependencies | Owner | Sprint 2 |
|------|-------------|-------|--------------|-------|----------|
| 5.1 | Remaining department SOPs (5) | 6 | None | content_creator | S2-11 |
| 5.2 | Terms of Service (DRAFT) | 2 | None | content_creator | S2-11 |
| 5.3 | Privacy Policy (DRAFT) | 2 | None | content_creator | S2-11 |

**Total P1 Documentation**: 10 hours

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
| P0 — Critical | 7 | 25 | 28% | Sprint 2 |
| P1 — High | 8 | 20 | 22% | Sprint 2 |
| P2 — Medium | 9 | 22 | 25% | Sprint 3 |
| P3 — Low | 10 | 27.5 | 31% | Sprint 4+ |
| **Total** | **34** | **94.5** | **100%** | |

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

## Recommended Sprint 2 Focus

1. **MessageBus Hardening** (2.1-2.3) — Foundation for all reliability
2. **Security Hardening** (3.1-3.4) — Critical for production use
3. **Integration Fixes** (4.1-4.5) — Close remaining gaps

**Sprint 2 Estimate**: ~45 hours (25 P0 + 20 P1)

---

## Agent Ownership Summary

| Agent | Items | Total Hours | Sprint |
|-------|-------|-------------|--------|
| lead-backend | 2.1-2.3, 3.1-3.2, 3.4, 4.1-4.5, 7.1-7.3, 8.1-8.2, 9.1-9.4, 11.1-11.3 | 54.5 | Sprint 2-4 |
| lead-frontend | 3.3, 6.1-6.3, 8.3 | 10 | Sprint 2-3 |
| content_creator | 5.1-5.3 | 10 | Sprint 2 |
| qa_engineer | 10.1-10.4 | 10 | Sprint 4 |
| **Total** | **34** | **84.5** | |

---

## Next Steps

1. Begin Sprint 2 with MessageBus hardening (S2-01, S2-02, S2-03)
2. Parallel track: security hardening (S2-04, S2-05, S2-08, S2-10)
3. Content creator works on SOPs in parallel
4. Review Sprint 2 progress at mid-sprint checkpoint
