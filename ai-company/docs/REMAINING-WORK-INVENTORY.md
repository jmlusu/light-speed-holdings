# AI Company Builder — Remaining Work Inventory

**Date**: 2026-07-19  
**Status**: Post-Sprint 1  
**Total Source Files**: 91  
**Test Coverage**: 359 tests passing  
**Lint Status**: ruff clean

---

## Executive Summary

Sprint 1 delivered core infrastructure (HITL gates, cost tracking, agent loop, SOPs). This inventory catalogs all remaining incomplete items across 14 packages, organized by module with priority, effort estimates, dependencies, and recommended agent owners.

---

## P0 — Critical (Complete Before Sprint 2)

### 1. Audit Module (Missing Entirely)

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 1.1 | Create `src/ai_company/audit/__init__.py` | 0.5 | None | claude-arch |
| 1.2 | Create `src/ai_company/audit/events.py` — Event models (AuditEvent, severity levels, metadata) | 2 | Pydantic models | claude-arch |
| 1.3 | Create `src/ai_company/audit/writer.py` — Async JSONL writer with rotation | 3 | events.py | claude-arch |
| 1.4 | Create `src/ai_company/audit/reader.py` — Query/filter/export capabilities | 2 | writer.py | claude-arch |
| 1.5 | Integrate audit events into message_bus.py, approval.py, executor/loop.py | 3 | 1.2-1.4, message_bus | claude-dev |
| 1.6 | Add audit retention policy (configurable, default 90 days) | 1 | 1.3 | claude-dev |

**Total P0 Audit**: 11.5 hours

---

## P1 — High Priority (Sprint 2)

### 2. Message Bus Enhancements

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 2.1 | Add correlation_id (UUID) to all Task messages | 1 | None | claude-dev |
| 2.2 | Implement ACK/NACK protocol with TTL | 3 | 2.1 | claude-dev |
| 2.3 | Atomic file writes (write to .tmp, then rename) | 1 | None | claude-dev |
| 2.4 | Add retry queue with exponential backoff | 2 | 2.2 | claude-dev |
| 2.5 | Dead letter queue for failed tasks | 1.5 | 2.2 | claude-dev |

**Total P1 Message Bus**: 8.5 hours

### 3. Approval System (5-Tier)

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 3.1 | Refactor approval.py to use tier_rules.py classification | 2 | tier_rules.py | claude-dev |
| 3.2 | Implement 5-tier escalation paths (auto → lead → exec → CEO → board) | 4 | 3.1 | claude-dev |
| 3.3 | Add timeout-based escalation (configurable per tier) | 2 | 3.2 | claude-dev |
| 3.4 | Implement two-person rule for Tier 4-5 | 2 | 3.2 | claude-dev |
| 3.5 | Add approval audit trail (writes to audit module) | 1 | audit module | claude-dev |

**Total P1 Approval**: 11 hours

### 4. LLM Provider Enhancements

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 4.1 | Add streaming support to base.py | 3 | None | claude-ml |
| 4.2 | Add health check endpoint per provider | 1.5 | None | claude-ml |
| 4.3 | Circuit breaker pattern (fail-fast after N errors) | 2 | None | claude-ml |
| 4.4 | Token counting integration (tiktoken for OpenAI, local for Ollama) | 2 | None | claude-ml |
| 4.5 | Cost calculation per request (cache + compute) | 1.5 | 4.4 | claude-ml |

**Total P1 LLM**: 10 hours

---

## P2 — Medium Priority (Sprint 3)

### 5. Dashboard Enhancements

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 5.1 | Add authentication (JWT/session) to API endpoints | 3 | None | claude-dev |
| 5.2 | Implement WebSocket reconnection logic | 1.5 | None | claude-dev |
| 5.3 | Add rate limiting to API endpoints | 1 | None | claude-dev |
| 5.4 | Real-time KPI streaming (SSE or WebSocket) | 2 | kpi_collector | claude-dev |
| 5.5 | Add CORS configuration for production | 0.5 | None | claude-dev |

**Total P2 Dashboard**: 8 hours

### 6. Memory Engine Enhancements

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 6.1 | Add semantic classification for memories | 3 | None | claude-ml |
| 6.2 | Implement retention policies (TTL, access-based) | 2 | None | claude-dev |
| 6.3 | Add encryption for sensitive memories | 2 | None | claude-dev |
| 6.4 | Implement memory consolidation rules | 2 | 6.1 | claude-ml |
| 6.5 | Add memory search (keyword + semantic) | 3 | 6.1 | claude-ml |

**Total P2 Memory**: 12 hours

### 7. CLI Module Completion

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 7.1 | Implement `cli/board.py` — Board meeting scheduling, minutes | 3 | None | claude-dev |
| 7.2 | Implement `cli/workflows.py` — Full workflow lifecycle (beyond stubs) | 4 | message_bus | claude-dev |
| 7.3 | Implement `cli/memory.py` — Enhanced memory management | 2 | memory engine | claude-dev |
| 7.4 | Implement `cli/executives.py` — Executive performance tracking | 2 | None | claude-dev |
| 7.5 | Implement `cli/departments.py` — Department analytics | 2 | None | claude-dev |
| 7.6 | Add `cli/audit.py` — Audit log query/export | 1.5 | audit module | claude-dev |

**Total P2 CLI**: 14.5 hours

---

## P3 — Low Priority (Sprint 4+)

### 8. Code Quality & Cleanup

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 8.1 | Replace print() with logging in executor/loop.py (lines 100-101, 107, 115) | 0.5 | None | claude-dev |
| 8.2 | Replace print() with logging in generator.py (lines 63, 73, 75, 160) | 0.5 | None | claude-dev |
| 8.3 | Replace print() with logging in orchestrator/briefing.py (line 77) | 0.25 | None | claude-dev |
| 8.4 | Add type hints to all CLI modules | 2 | None | claude-dev |
| 8.5 | Add docstrings to all public functions | 1.5 | None | claude-dev |

**Total P3 Code Quality**: 4.75 hours

### 9. Test Coverage Gaps

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 9.1 | Add integration tests for message_bus ACK/NACK | 2 | 2.2 | qa-engineer |
| 9.2 | Add integration tests for approval escalation | 2 | 3.2 | qa-engineer |
| 9.3 | Add unit tests for LLM provider circuit breaker | 1.5 | 4.3 | qa-engineer |
| 9.4 | Add unit tests for memory encryption | 1 | 6.3 | qa-engineer |
| 9.5 | Add API endpoint tests (dashboard) | 2 | 5.1 | qa-engineer |
| 9.6 | Add CLI command tests (all modules) | 3 | 7.1-7.6 | qa-engineer |

**Total P3 Tests**: 11.5 hours

### 10. Documentation & Developer Experience

| Item | Description | Hours | Dependencies | Owner |
|------|-------------|-------|--------------|-------|
| 10.1 | Add API documentation (OpenAPI/Swagger) | 2 | dashboard | claude-dev |
| 10.2 | Create architecture decision records (ADRs) | 3 | None | claude-arch |
| 10.3 | Add inline code comments for complex logic | 2 | None | claude-dev |
| 10.4 | Create developer onboarding guide | 2 | None | claude-dev |

**Total P3 Documentation**: 9 hours

---

## Summary by Priority

| Priority | Items | Hours | % of Total |
|----------|-------|-------|------------|
| P0 — Critical | 6 | 11.5 | 14% |
| P1 — High | 13 | 29.5 | 35% |
| P2 — Medium | 12 | 34.5 | 41% |
| P3 — Low | 10 | 25.25 | 30% |
| **Total** | **41** | **100.75** | **100%** |

---

## Dependency Graph

```
P0: Audit Module (1.1-1.6)
    └── Required by: Approval audit trail (3.5), CLI audit (7.6)

P1: Message Bus (2.1-2.5)
    └── Required by: Workflow CLI (7.2)

P1: Approval System (3.1-3.5)
    └── Depends on: Audit Module (1.2-1.4)

P1: LLM Providers (4.1-4.5)
    └── No dependencies

P2: Dashboard (5.1-5.5)
    └── Depends on: Audit Module (for logs)

P2: Memory Engine (6.1-6.5)
    └── No dependencies

P2: CLI Modules (7.1-7.6)
    └── Depends on: Audit Module (7.6), Message Bus (7.2), Memory Engine (7.3)
```

---

## Recommended Sprint 2 Focus

1. **Complete Audit Module** (1.1-1.6) — Foundation for all logging/tracking
2. **Message Bus Enhancements** (2.1-2.5) — Reliable task delivery
3. **Approval System 5-Tier** (3.1-3.5) — Critical for HITL governance

**Sprint 2 Estimate**: ~31 hours (11.5 + 8.5 + 11)

---

## Agent Ownership Summary

| Agent | Items | Total Hours |
|-------|-------|-------------|
| claude-arch | 1.1-1.4, 10.2 | 10 |
| claude-dev | 1.5-1.6, 2.1-2.5, 3.1-3.5, 5.1-5.5, 7.1-7.6, 8.1-8.5, 10.1, 10.3-10.4 | 68.25 |
| claude-ml | 4.1-4.5, 6.1, 6.4-6.5 | 13.5 |
| qa-engineer | 9.1-9.6 | 11.5 |
| **Total** | **41** | **103.25** |

---

## Next Steps

1. Review this inventory with the team
2. Prioritize P0 items for immediate execution
3. Assign sprint 2 tasks to agents
4. Begin with audit module creation (foundation for all other work)
