# Pre-Sprint-4 Coordination Plan

**Date:** 2026-07-24  
**Author:** Chief of Staff  
**Objective:** Orchestrate completion of all 28 outstanding issues before Sprint 4 begins  
**Total Estimated Effort:** 38-43 hours  
**Target Completion:** 2026-07-31 (5 working days)

---

## Executive Summary

This plan coordinates the resolution of 28 outstanding issues (16 primary items + 8 dashboard UX sub-items) across 6 departments. The work is sequenced into 5 phases with clear dependencies, assigned owners, and daily checkpoints. All items must be verified against the completion criteria before Sprint 4 can begin.

---

## Delegation Matrix

| Item ID | Description | Responsible Agent | Supporting Agents | Dependencies | Estimated Effort | Target Date | Status |
|---------|-------------|-------------------|-------------------|--------------|------------------|-------------|--------|
| **PRE-01** | Wire Memory Encryption | security_engineer | lead_backend | None | 0.5h | 2026-07-27 | Pending |
| **PRE-02** | WebSocket Authentication | lead_frontend | security_engineer | None | 2h | 2026-07-27 | Pending |
| **PRE-03** | Dashboard Auth Fail-Closed | lead_frontend | security_engineer | None | 1h | 2026-07-27 | Pending |
| **PRE-04** | Centralize MessageBus Singleton | lead_backend | senior_backend_engineer | None | 4h | 2026-07-27 | Pending |
| **PRE-05** | Update Stale Risk Register | compliance_officer | legal_owner | None | 0.5h | 2026-07-28 | Pending |
| **PRE-06** | Wire GAP-005 Memory Consolidation | lead_backend | memory_owner | PRE-01 | 3h | 2026-07-28 | Pending |
| **PRE-07** | Complete GAP-011 MessageBus Read Path | lead_backend | senior_backend_engineer | PRE-04 | 6h | 2026-07-28 | Pending |
| **PRE-08** | GAP-018 Structured Logging | lead_backend | devops_lead | None | 6h | 2026-07-29 | Pending |
| **PRE-08B** | GAP-019 Agent Spec Validation CLI | qa_engineer | lead_backend | None | 3h | 2026-07-29 | Pending |
| **PRE-09** | Add Circuit Breaker Tests | qa_engineer | test_engineering_lead | None | 2h | 2026-07-29 | Pending |
| **PRE-10** | Add Security Module Tests | qa_engineer | security_engineer | PRE-01 | 4h | 2026-07-29 | Pending |
| **PRE-11** | Add Token Counting Integration | lead_backend | llm_platform_owner | None | 3h | 2026-07-29 | Pending |
| **PRE-12** | Add API Versioning | api_architect | lead_frontend | None | 4h | 2026-07-30 | Pending |
| **PRE-13** | Replace print() Calls | lead_backend | devops_lead | PRE-08 | 1h | 2026-07-30 | Pending |
| **PRE-14** | OAuth2 / API Key Rotation | security_engineer | ciso | PRE-02 | 6h | 2026-07-30 | Pending |
| **PRE-15** | Dashboard UX Fixes (8 items) | lead_frontend | frontend_engineer, senior_frontend_engineer | PRE-02 | 8h | 2026-07-31 | Pending |
| DASH-001 | Auto-scroll on new messages | lead_frontend | frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-002 | Loading indicators | lead_frontend | frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-003 | API error display | lead_frontend | frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-004 | WS reconnect on disconnect | lead_frontend | senior_frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-005 | WS reconnect flicker fix | lead_frontend | senior_frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-006 | aria-live regions | lead_frontend | frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-007 | Mobile touch gestures | lead_frontend | frontend_engineer | None | 1h | 2026-07-31 | Pending |
| DASH-008 | CDN SRI hashes | lead_frontend | security_engineer | None | 1h | 2026-07-31 | Pending |

---

## Dependency Graph

```
Phase 1 (Security First - Day 1)
├── PRE-01 (security_engineer) ──────────┬──► PRE-06 (lead_backend)
│                                        └──► PRE-10 (qa_engineer)
├── PRE-02 (lead_frontend) ─────────────┬──► PRE-14 (security_engineer)
│                                        └──► PRE-15 (lead_frontend)
├── PRE-03 (lead_frontend) (no downstream)
└── PRE-04 (lead_backend) ──────────────► PRE-07 (lead_backend)

Phase 2 (Data Integrity - Day 2)
├── PRE-05 (compliance_officer) (independent)
├── PRE-06 (depends on PRE-01)
└── PRE-07 (depends on PRE-04)

Phase 3 (Testing - Day 3)
├── PRE-09 (qa_engineer) (independent)
├── PRE-10 (depends on PRE-01)
└── PRE-11 (lead_backend) (independent)

Phase 4 (Code Quality - Day 4)
├── PRE-08 (lead_backend) ──────────────► PRE-13 (lead_backend)
├── PRE-08B (qa_engineer) (independent)
├── PRE-12 (api_architect) (independent)
└── PRE-14 (depends on PRE-02)

Phase 5 (UX Polish - Day 5)
└── PRE-15 (depends on PRE-02)
```

---

## Daily Standup Schedule

**Time:** 09:00 UTC daily (05:00 EST)  
**Duration:** 15 minutes  
**Location:** Virtual standup (async updates in #pre-sprint-4 channel)  
**Participants:** Chief of Staff, all responsible agents, supporting agents as needed

### Standup Format
1. **Yesterday:** What did you complete? (Item ID + verification status)
2. **Today:** What will you work on? (Item ID + expected blockers)
3. **Blockers:** Any dependencies not met? Need escalation?

### Daily Checkpoints

| Day | Date | Focus | Key Deliverables | Verification Gate |
|-----|------|-------|------------------|-------------------|
| **Day 1** | 2026-07-27 | Security First | PRE-01, PRE-02, PRE-03, PRE-04 | Encryption wiring, WebSocket auth, dashboard auth, bus singleton |
| **Day 2** | 2026-07-28 | Data Integrity | PRE-05, PRE-06, PRE-07 | Risk register updated, memory consolidation, read path consistency |
| **Day 3** | 2026-07-29 | Testing | PRE-09, PRE-10, PRE-11 | Circuit breaker tests, security module tests, token counting |
| **Day 4** | 2026-07-30 | Code Quality | PRE-08, PRE-08B, PRE-12, PRE-13, PRE-14 | Structured logging, agent validation, API versioning, print replacement, key rotation |
| **Day 5** | 2026-07-31 | UX Polish | PRE-15 (8 items) | All dashboard UX improvements complete |

---

## Escalation Criteria

### Immediate Escalation to Human CEO
- Any item blocked for >4 hours due to missing dependencies
- Security vulnerability discovered during implementation
- Test suite regression (>5 existing tests broken)
- Budget overrun (estimated effort exceeds 150% of original estimate)

### Escalation to Chief of Staff
- Agent unable to complete assigned item due to skill gap
- Cross-department dependency conflict
- Need for additional resources (agent capacity)
- Quality concerns (code review failures)

### Escalation to Department Heads
- Technical architecture decisions (CTO)
- Security policy exceptions (CISO)
- Compliance requirements (CLO)
- Product design decisions (CPO)

---

## Resource Allocation

### Agent Capacity (8-hour workday)

| Agent | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 | Total |
|-------|-------|-------|-------|-------|-------|-------|
| **security_engineer** | PRE-01 (0.5h) | — | — | — | — | 0.5h |
| **lead_frontend** | PRE-02 (2h) + PRE-03 (1h) | — | — | — | PRE-15 (8h) | 11h |
| **lead_backend** | PRE-04 (4h) | PRE-06 (3h) + PRE-07 (6h) | PRE-11 (3h) | PRE-08 (6h) + PRE-13 (1h) | — | 23h |
| **compliance_officer** | — | PRE-05 (0.5h) | — | — | — | 0.5h |
| **qa_engineer** | — | — | PRE-09 (2h) + PRE-10 (4h) + PRE-08B (3h) | — | — | 9h |
| **api_architect** | — | — | — | PRE-12 (4h) | — | 4h |

### Critical Path Items
1. **PRE-04 (MessageBus Singleton)** → Blocks PRE-07 (6h) → Total critical path: 10h
2. **PRE-02 (WebSocket Auth)** → Blocks PRE-14 (6h) + PRE-15 (8h) → Total critical path: 16h
3. **PRE-01 (Memory Encryption)** → Blocks PRE-06 (3h) + PRE-10 (4h) → Total critical path: 7.5h

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| **PRE-07 breaks KPI endpoints** | Medium | High | Run full KPI test suite before/after; feature flag for gradual rollout | lead_backend |
| **PRE-08 changes log format** | High | Medium | Document new format in DEVELOPMENT.md; maintain backward compatibility | lead_backend |
| **PRE-12 breaks frontend** | Medium | High | Keep legacy routes as redirects; versioned endpoints with deprecation notices | api_architect |
| **PRE-14 requires migration** | Medium | Medium | Support both old and new key formats; gradual migration plan | security_engineer |
| **Agent capacity overload** | Low | High | Monitor daily standups; reallocate supporting agents as needed | Chief of Staff |
| **Dependency chain delays** | Medium | High | Start independent items immediately; parallelize where possible | Chief of Staff |

---

## Verification Matrix

Before Sprint 4 can begin, ALL of the following must be true:

| Criterion | Verification Command | Owner | Status |
|-----------|----------------------|-------|--------|
| No print() in non-CLI code | `grep -r "print(" src/ai_company/ --include="*.py" \| grep -v cli/ \| wc -l` = 0 | lead_backend | ⬜ |
| All existing tests pass | `pytest` (1205+ tests) | qa_engineer | ⬜ |
| New tests added (26 minimum) | `pytest tests/unit/test_circuit_breaker.py tests/unit/test_pii_detector.py tests/unit/test_content_filter.py tests/unit/test_memory_encryption.py tests/unit/test_token_counting.py` | qa_engineer | ⬜ |
| Ruff clean | `ruff check src/` | lead_backend | ⬜ |
| Mypy clean | `mypy src/` | lead_backend | ⬜ |
| No direct inbox.json reads in dashboard | `grep -r "inbox.json" dashboard/ \| wc -l` = 0 | lead_backend | ⬜ |
| Dashboard auth fail-closed | `DASHBOARD_AUTH_MODE=closed` is default | lead_frontend | ⬜ |
| Risk register updated | R17, R18 status = "Mitigated" | compliance_officer | ⬜ |
| Memory encryption round-trip | Unit test: encrypt + decrypt round-trip | security_engineer | ⬜ |
| WebSocket auth | Unit test: connect without token → 4001 close | lead_frontend | ⬜ |

---

## Communication Plan

### Daily Updates
- **Async updates** in #pre-sprint-4 channel by 17:00 UTC
- **Blockers** flagged immediately in standup
- **Completion notifications** with verification evidence

### Weekly Report
- **Friday 2026-07-31**: Final status report to Human CEO
- **Include**: Completion matrix, test results, verification evidence, lessons learned

### Documentation Updates
- Update `docs/STATUS.md` after each phase completion
- Update `docs/RISK-REGISTER.md` for PRE-05
- Update `docs/DEVELOPMENT.md` for PRE-08 (logging format)

---

## Success Criteria

### Quantitative
- 28/28 items completed
- 26+ new tests added
- 1205+ existing tests passing
- 0 ruff errors
- 0 mypy errors
- 0 print() calls in non-CLI code

### Qualitative
- All security vulnerabilities addressed
- All data integrity issues resolved
- All architecture gaps closed
- All code quality standards met
- All UX improvements implemented

### Business Value
- Production-ready security posture
- Maintainable, well-tested codebase
- Consistent API with versioning
- Improved developer experience
- Enhanced operational visibility

---

**Next Action:** Chief of Staff to schedule kickoff standup for 2026-07-27 09:00 UTC and assign agents to their items.