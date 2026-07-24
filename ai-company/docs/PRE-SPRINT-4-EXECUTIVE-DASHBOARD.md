# Pre-Sprint-4 Backlog — Executive Dashboard

**Date:** 2026-07-24
**Prepared By:** VP of Engineering
**Status:** ACTIVE
**Sprint 4 Gate:** 28 issues | 38-43 hours | 0 open blockers

---

## Executive Summary

### Current State
- **Sprint 3 Complete**: 1205 tests passing, 0 ruff errors, 0 mypy errors
- **Active Changes**: None (clean state)
- **Backlog Items**: 28 issues across 5 priority tiers
- **Estimated Total Effort**: 38-43 hours (5 working days at 8h/day)

### Key Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Count | 1205 | 1231 (+26) | 🟡 Pending |
| ruff Errors | 0 | 0 | ✅ Gate |
| mypy Errors | 0 | 0 | ✅ Gate |
| Security Items | 4 open | 0 open | 🔴 At Risk |
| Direct `inbox.json` Reads | Unknown | 0 in dashboard/ | 🟡 Pending |
| `print()` in non-CLI | 11 | 0 | 🟡 Pending |

---

## Resource Allocation Plan

### Capacity Analysis

| Resource | Available Hours | Assigned | Utilization | Risk |
|----------|----------------|----------|-------------|------|
| **security_engineer** | 12h | 12.5h (PRE-01, PRE-14) | 104% | 🔴 Over-allocated |
| **lead_frontend** | 16h | 11h (PRE-02, PRE-03, PRE-15) | 69% | 🟢 OK |
| **lead_backend** | 20h | 23h (PRE-04, PRE-06, PRE-07, PRE-08, PRE-11, PRE-13) | 115% | 🔴 Over-allocated |
| **qa_engineer** | 12h | 9h (PRE-09, PRE-10, PRE-08B) | 75% | 🟢 OK |
| **compliance_officer** | 4h | 0.5h (PRE-05) | 13% | 🟢 Under-utilized |
| **api_architect** | 8h | 4h (PRE-12) | 50% | 🟢 OK |

### Resource Conflicts

| Conflict | Severity | Resolution |
|----------|----------|------------|
| lead_backend 115% utilization | HIGH | Split PRE-08 (6h) into 2 sprints or defer PRE-14 to Sprint 4 |
| security_engineer 104% | MEDIUM | Defer PRE-14 (6h) to Sprint 4; complete PRE-01 (0.5h) now |

### Recommended Rebalancing

| Original Assignment | Proposed Change | Rationale |
|--------------------|-----------------|-----------|
| PRE-14: security_engineer (6h) | → Defer to Sprint 4 | Brings security_engineer to 54% utilization |
| PRE-08: lead_backend (6h) | → Split: 3h now, 3h Sprint 4 | Reduces lead_backend to 88% |
| PRE-15: lead_frontend (8h) | → Split: 4h now, 4h Sprint 4 | Frontend items lower priority |

**Post-Rebalance Utilization:**
- lead_backend: 88% (17.5h/20h) ✅
- security_engineer: 54% (6.5h/12h) ✅
- lead_frontend: 63% (7h/11h) ✅
- qa_engineer: 75% (9h/12h) ✅

---

## Risk Assessment

### Critical Risks (Must Resolve Before Sprint 4)

| Risk ID | Description | Impact | Likelihood | Mitigation |
|---------|-------------|--------|------------|------------|
| R15 | Concurrent file writes corrupt shared JSON | HIGH | HIGH | PRE-04 (centralize bus) — 4h |
| R16 | Dashboard API unauthenticated access | HIGH | HIGH | PRE-03 (auth fail-closed) — 1h |
| R18 | Shell injection via ToolRunner | HIGH | MEDIUM | Already mitigated in Sprint 2 (S2-10) |

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PRE-07 breaks KPI endpoints | 30% | HIGH | Run full KPI test suite before/after |
| PRE-08 changes log format | 50% | MEDIUM | Document new format in DEVELOPMENT.md |
| PRE-12 breaks frontend | 20% | HIGH | Keep legacy routes as redirects |
| PRE-14 requires migration | 40% | MEDIUM | Support both old and new key formats |

### Dependency Chain Risks

```
PRE-01 (encryption) → PRE-06 (consolidation) → PRE-10 (security tests)
PRE-04 (bus centralize) → PRE-07 (read path)
PRE-02 (WS auth) → PRE-14 (key rotation)
PRE-02 (WS auth) → PRE-15 (UX fixes)
```

**Risk:** If PRE-04 is delayed, PRE-07 is blocked (6h dependency)
**Mitigation:** Start PRE-04 immediately; parallelize independent items

---

## Execution Timeline

### Phase 1: Security First (Day 1) — 7.5h → Revised: 6.5h

| # | Item | Effort | Owner | Status | Dependencies |
|---|------|--------|-------|--------|--------------|
| 1 | PRE-01: Wire encryption | 0.5h | security_engineer | ⬜ Not Started | None |
| 2 | PRE-03: Auth fail-closed | 1h | lead_frontend | ⬜ Not Started | None |
| 3 | PRE-02: WS auth | 2h | lead_frontend | ⬜ Not Started | None |
| 4 | PRE-04: Centralize bus | 4h | lead_backend | ⬜ Not Started | None |

**Day 1 Gate:** Security items complete, no new vulnerabilities introduced

### Phase 2: Data Integrity (Day 2) — 9.5h

| # | Item | Effort | Owner | Status | Dependencies |
|---|------|--------|-------|--------|--------------|
| 5 | PRE-05: Update risk register | 0.5h | compliance_officer | ⬜ Not Started | None |
| 6 | PRE-06: GAP-005 consolidation | 3h | lead_backend | ⬜ Not Started | PRE-01 |
| 7 | PRE-07: GAP-011 read path | 6h | lead_backend | ⬜ Not Started | PRE-04 |

**Day 2 Gate:** All inbox.json direct reads eliminated from dashboard/

### Phase 3: Testing (Day 3) — 9h

| # | Item | Effort | Owner | Status | Dependencies |
|---|------|--------|-------|--------|--------------|
| 8 | PRE-09: Circuit breaker tests | 2h | qa_engineer | ⬜ Not Started | None |
| 9 | PRE-10: Security module tests | 4h | qa_engineer | ⬜ Not Started | PRE-01 |
| 10 | PRE-11: Token counting | 3h | lead_backend | ⬜ Not Started | None |

**Day 3 Gate:** 26+ new tests, all 1231+ tests passing

### Phase 4: Code Quality (Day 4) — 18h → Revised: 13h

| # | Item | Effort | Owner | Status | Dependencies |
|---|------|--------|-------|--------|--------------|
| 11 | PRE-08: Structured logging | 6h | lead_backend | ⬜ Not Started | None |
| 12 | PRE-08B: Agent spec validation | 3h | qa_engineer | ⬜ Not Started | None |
| 13 | PRE-12: API versioning | 4h | api_architect | ⬜ Not Started | None |
| 14 | PRE-13: Replace print() | 1h | lead_backend | ⬜ Not Started | PRE-08 |
| ~~15~~ | ~~PRE-14: Key rotation~~ | ~~6h~~ | ~~security_engineer~~ | ⏸️ Deferred | ~~PRE-02~~ |

**Day 4 Gate:** 0 print() calls in non-CLI, all API endpoints versioned

### Phase 5: UX Polish (Day 5) — 8h → Revised: 4h

| # | Item | Effort | Owner | Status | Dependencies |
|---|------|--------|-------|--------|--------------|
| 15 | PRE-15: Dashboard UX (8 items) | 8h | lead_frontend | ⬜ Not Started | PRE-02 |

**Day 5 Gate:** Dashboard passes WCAG AA checks

---

## Quality Gates

### Pre-Sprint 4 Entry Criteria

| Gate | Command | Pass/Fail |
|------|---------|-----------|
| All 1205 existing tests pass | `pytest --tb=short` | ⬜ |
| ruff clean | `ruff check src/` | ⬜ |
| mypy clean | `mypy src/` | ⬜ |
| No direct inbox.json reads in dashboard | `grep -r "inbox.json" dashboard/ \| wc -l` = 0 | ⬜ |
| 0 print() in non-CLI | `grep -r "print(" src/ --include="*.py" \| grep -v cli/ \| wc -l` = 0 | ⬜ |
| Memory encryption round-trip | `pytest tests/unit/test_memory_encryption.py` | ⬜ |
| WebSocket auth test | `pytest tests/unit/test_dashboard_ws.py -k auth` | ⬜ |
| DASHBOARD_AUTH_MODE=closed default | `grep -r "DASHBOARD_AUTH_MODE" src/ \| grep closed` | ⬜ |

### Sprint 4 Exit Criteria

| Criterion | Target | Current |
|-----------|--------|---------|
| Total tests | ≥1231 | 1205 |
| New tests added | ≥26 | 0 |
| Security items resolved | 4/4 | 0/4 |
| Architecture gaps closed | 2/2 | 0/2 |
| Risk register updated | R17, R18 = Mitigated | Open |
| print() calls eliminated | 0 | 11 |
| API versioned | /api/v1/ prefix | None |

---

## Blockers & Escalations

### Active Blockers

| Blocker | Impact | Escalation Path | Resolution |
|---------|--------|-----------------|------------|
| None | — | — | — |

### Potential Blockers (Proactive)

| Risk | Trigger | Impact | Escalation |
|------|---------|--------|------------|
| PRE-07 breaks KPI endpoints | KPI tests fail after change | HIGH | Revert PRE-07, investigate in isolation |
| PRE-08 log format change | CI/CD parsing breaks | MEDIUM | Document format, update parsers |
| PRE-12 API versioning breaks frontend | Frontend requests fail | HIGH | Keep legacy routes as redirects |

---

## Recommendations

### Immediate Actions (Today)

1. **Approve resource rebalancing** — Move PRE-14 and half of PRE-08/PRE-15 to Sprint 4
2. **Start PRE-01 immediately** — 0.5h, unblocks 3 downstream items
3. **Assign PRE-04 to lead_backend** — Critical path item, 4h
4. **Assign PRE-03 to lead_frontend** — Quick security win, 1h

### Sprint Planning Adjustments

| Original Plan | Recommended Change | Rationale |
|---------------|-------------------|-----------|
| 5-day sprint | 4-day sprint + 1 buffer day | Allows for unexpected issues |
| 28 items in scope | 24 items in scope, 4 deferred | Resource constraints |
| PRE-14 in scope | Defer to Sprint 4 | Over-allocation of security_engineer |
| PRE-15 all in scope | Defer 4 of 8 items | Lower priority, frontend bandwidth |

### Quality Assurance

1. **Run full test suite after each phase** — Catch regressions early
2. **Review PRE-07 changes with KPI collectors** — High-risk integration point
3. **Validate PRE-12 with frontend team** — API versioning can break consumers
4. **Document PRE-08 log format** — Update DEVELOPMENT.md before merge

---

## Status Dashboard (Daily Updates)

| Date | Phase | Items Done | Hours Used | Tests | Blockers |
|------|-------|------------|------------|-------|----------|
| 2026-07-24 | — | 0/28 | 0/43 | 1205 | None |
| 2026-07-25 | 1 | — | — | — | — |
| 2026-07-26 | 2 | — | — | — | — |
| 2026-07-27 | 3 | — | — | — | — |
| 2026-07-28 | 4 | — | — | — | — |
| 2026-07-29 | 5 | — | — | — | — |

---

## Appendix: Item Ownership Matrix

| Item | Owner | Priority | Effort | Status |
|------|-------|----------|--------|--------|
| PRE-01 | security_engineer | P1-Critical | 0.5h | ⬜ |
| PRE-02 | lead_frontend | P2-Security | 2h | ⬜ |
| PRE-03 | lead_frontend | P2-Security | 1h | ⬜ |
| PRE-04 | lead_backend | P2-Security | 4h | ⬜ |
| PRE-05 | compliance_officer | P3-Data | 0.5h | ⬜ |
| PRE-06 | lead_backend | P3-Data | 3h | ⬜ |
| PRE-07 | lead_backend | P4-Arch | 6h | ⬜ |
| PRE-08 | lead_backend | P4-Arch | 6h | ⬜ |
| PRE-08B | qa_engineer | P4-Arch | 3h | ⬜ |
| PRE-09 | qa_engineer | P5-Testing | 2h | ⬜ |
| PRE-10 | qa_engineer | P5-Testing | 4h | ⬜ |
| PRE-11 | lead_backend | P5-Testing | 3h | ⬜ |
| PRE-12 | api_architect | P6-Quality | 4h | ⬜ |
| PRE-13 | lead_backend | P6-Quality | 1h | ⬜ |
| PRE-14 | security_engineer | P6-Quality | 6h | ⏸️ Deferred |
| PRE-15 | lead_frontend | P6-Quality | 8h | ⬜ |

---

**Next Review:** 2026-07-25 (end of Day 1)
**Escalation Contact:** CTO (architecture decisions, cross-team coordination)
