# Pre-Sprint-4 Backlog — Executive Summary

**Date:** 2026-07-24
**Prepared By:** VP of Engineering
**Classification:** Internal — Executive Review

---

## Situation

28 outstanding issues must be resolved before Sprint 4 can begin. These span security vulnerabilities, architecture gaps, testing gaps, data integrity problems, and code quality issues. Total estimated effort: 38-43 hours.

## Key Findings

### 1. Resource Over-Allocation Detected

| Resource | Original Load | Capacity | Status |
|----------|--------------|----------|--------|
| lead_backend | 23h (115%) | 20h | 🔴 Over-allocated |
| security_engineer | 12.5h (104%) | 12h | 🔴 Over-allocated |

**Recommendation:** Defer PRE-14 (Key Rotation, 6h) to Sprint 4 and split PRE-08 (Structured Logging, 6h) across two sprints. This brings both resources within capacity.

### 2. Critical Security Items Require Immediate Attention

| Item | Risk | Effort | Impact if Delayed |
|------|------|--------|-------------------|
| PRE-01: Wire encryption | Data at rest unencrypted | 0.5h | Compliance violation |
| PRE-03: Auth fail-closed | Dashboard open to unauthorized writes | 1h | Data breach risk |
| PRE-04: Centralize bus | Race conditions on shared state | 4h | Data corruption |
| PRE-02: WS auth | Unauthenticated WebSocket access | 2h | Data exfiltration |

**These 4 items (7.5h) must complete on Day 1.**

### 3. Dependency Chain Risks

```
PRE-01 → PRE-06 → PRE-10 (encryption chain)
PRE-04 → PRE-07 (bus centralization chain)
PRE-02 → PRE-14, PRE-15 (auth chain)
```

**Risk:** If PRE-04 is delayed, PRE-07 (6h) is blocked. This is the highest-impact dependency in the backlog.

### 4. Risk Register Staleness

R15, R16, R17, R18 are marked "Open" in `docs/RISK-REGISTER.md` but Sprint 2 claims these were resolved. The risk register must be updated as part of PRE-05 to ensure leadership has accurate risk visibility.

## Executive Decisions Required

| Decision | Options | Recommendation | Deadline |
|----------|---------|----------------|----------|
| Resource rebalancing | A) Keep all 28 items, accept overload; B) Defer PRE-14 + split PRE-08 | **Option B** — reduces total to 37h, eliminates over-allocation | Today |
| PRE-14 ownership | A) security_engineer; B) Defer to Sprint 4 | **Defer** — security_engineer at 54% after deferral | Today |
| PRE-15 scope | A) All 8 UX items; B) Defer 4 lower-priority items | **Defer 4** — DASH-006, DASH-007, DASH-008, DASH-005 to Sprint 4 | Today |
| Quality gate enforcement | A) Block Sprint 4 if gates fail; B) Allow conditional entry | **Block** — gates exist for a reason | Sprint 4 start |

## Quality Gates (Non-Negotiable)

Before Sprint 4 begins, ALL of the following must pass:

- [ ] `pytest` — 1231+ tests passing (1205 existing + 26 new)
- [ ] `ruff check src/` — 0 errors
- [ ] `mypy src/` — 0 errors
- [ ] `grep -r "inbox.json" dashboard/ | wc -l` = 0
- [ ] `grep -r "print(" src/ --include="*.py" | grep -v cli/ | wc -l` = 0
- [ ] Memory encryption round-trip test passes
- [ ] WebSocket auth test passes
- [ ] `DASHBOARD_AUTH_MODE=closed` is default
- [ ] Risk register updated (R17, R18 = Mitigated)

## Timeline

| Day | Phase | Hours | Items | Gate |
|-----|-------|-------|-------|------|
| Day 1 | Security First | 6.5h | PRE-01, PRE-02, PRE-03, PRE-04 | Security items complete |
| Day 2 | Data Integrity | 9.5h | PRE-05, PRE-06, PRE-07 | No direct inbox.json reads |
| Day 3 | Testing | 9h | PRE-09, PRE-10, PRE-11 | 1231+ tests passing |
| Day 4 | Code Quality | 13h | PRE-08, PRE-08B, PRE-12, PRE-13 | 0 print() calls |
| Day 5 | UX Polish + Buffer | 4h | PRE-15 (partial) | Dashboard WCAG AA |

**Total:** 42h (within 38-43h estimate)

## Risk Mitigation Strategies

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PRE-07 breaks KPI endpoints | 30% | HIGH | Run full KPI test suite before/after; revert if >2 tests fail |
| PRE-08 changes log format | 50% | MEDIUM | Document new format in DEVELOPMENT.md; update CI parsers |
| PRE-12 breaks frontend | 20% | HIGH | Keep legacy routes as redirects; test with frontend team |
| PRE-14 requires migration | 40% | MEDIUM | Support both old and new key formats during transition |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Lead backend burnout | 40% | HIGH | Rebalance workload; defer 2 items to Sprint 4 |
| Scope creep in PRE-15 | 30% | MEDIUM | Strict timebox: 4h max, defer remaining items |
| Test regression from PRE-08 | 20% | HIGH | Run test suite after each logging change; commit frequently |

## Recommendations Summary

1. **Approve resource rebalancing** — Defer PRE-14, split PRE-08, defer 4 of 8 PRE-15 items
2. **Start PRE-01 immediately** — 0.5h, unblocks 3 downstream items
3. **Assign PRE-04 to lead_backend today** — Critical path, 4h, no dependencies
4. **Run full test suite after each phase** — Catch regressions early
5. **Update risk register as part of PRE-05** — Ensure leadership has accurate risk visibility
6. **Block Sprint 4 if quality gates fail** — Gates exist for a reason

---

**Next Steps:** Present to CTO for approval, then begin Day 1 execution.

**Escalation Path:** VP of Engineering → CTO (architecture decisions, cross-team coordination)
