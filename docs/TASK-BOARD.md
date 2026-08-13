# AI Company Builder — Task Board

> **RECONCILIATION NOTICE (2026-08-13):** This board is now **historical**. Sprints 1–9 are
> complete and all 20 architecture gaps (GAP-001…020) are resolved and verified — see
> `docs/ARCHITECTURE-GAPS.md` and `docs/STATUS.md`. Every task below has been verified DONE in
> source as of 2026-08-13. Live work is tracked on GitHub wayfinder maps #7 (finish-dev / operate)
> and #33 (mission-control dashboard), not in this file.

**Sprint 3 Status:** COMPLETE
**Last Updated:** 2026-08-13
**Sprint Goal:** Complete all P2 features — Dashboard real-time, Memory enhancements, Autonomous scheduling

---

## Sprint 3 Tasks

| ID | Task | Owner | Status | % | Blocked By | Notes |
|----|------|-------|--------|---|------------|-------|
| S3-01 | WebSocket broadcast full wiring | lead-frontend | DONE | 100% | — | KPI snapshot + approval/escalation broadcasts wired end-to-end |
| S3-02 | OpenAPI/Swagger docs | lead-frontend | DONE | 100% | — | FastAPI auto `/docs` + `/openapi.json` (`dashboard/app.py`) |
| S3-03 | Rate limiting (slowapi) | lead-frontend | DONE | 100% | — | `_RateLimiter`, `DASHBOARD_RATE_LIMIT` default 100 req/min |
| S3-04 | Periodic memory consolidation | lead-backend | DONE | 100% | — | `memory/consolidation.py` scheduler wired into executor tick (GAP-005) |
| S3-05 | Memory search enhancement | lead-backend | DONE | 100% | — | `ai-company memory stats/search/recall` CLI |
| S3-06 | Memory retention TTL | lead-backend | DONE | 100% | — | `prune()` + consolidation pruning of old entries |
| S3-07 | Scheduled cycle daemon | lead-backend | DONE | 100% | — | Executor daemon mode (`executor start --daemon`); scheduler wired (GAP-007) |
| S3-14 | Approval escalation tests | qa_engineer | DONE | 100% | — | Approval-matrix + escalation test suites |
| S3-18 | Fix BriefingGenerator private method | lead-backend | DONE | 100% | — | Close GAP-014 — `briefing.py:42` uses `get_all_tasks()` |
| S3-19 | Fix LLM retry provider cycling | lead-backend | DONE | 100% | — | Close GAP-015 — `client.py:133-134` round-robin cycling |
| | **Sprint 3 Total** | | | **10/10** | | **17.0h estimated** |

---

## Sprint 4 Tasks

| ID | Task | Owner | Status | % | Blocked By | Notes |
|----|------|-------|--------|---|------------|-------|
| S3-08 | Structured logging with correlation IDs | lead-backend | DONE | 100% | — | Close GAP-018 — structured JSON logging with correlation IDs |
| S3-09 | Agent spec validation CLI | lead-backend | DONE | 100% | — | Close GAP-019 — `agents validate` |
| S3-10 | CLI type hints/docstrings | lead-backend | DONE | 100% | — | Issue #13 closed |
| S3-11 | Full pipeline integration test | qa_engineer | DONE | 100% | — | E2E pipeline integration suite |
| S3-12 | CLI command test suite | qa_engineer | DONE | 100% | — | Issue #12 closed |
| S3-13 | API endpoint test suite | qa_engineer | DONE | 100% | — | Dashboard API endpoint tests |
| S3-15 | OAuth2/key rotation | security_engineer | DONE | 100% | — | T009 OAuth2 + key rotation tooling |
| S3-16 | Memory encryption | security_engineer | DONE | 100% | — | `enable_encryption()` + `EncryptionKeyManager` in `memory/engine.py` |
| S3-17 | Token counting integration | lead-backend | DONE | 100% | — | LLM usage + token counting (T012) |
| | **Sprint 4 Total** | | | **9/9** | | **22.0h estimated** |

---

## Sprint 5 Tasks (Buffer)

| ID | Task | Owner | Status | % | Notes |
|----|------|-------|--------|---|-------|
| REGRESSION | Regression testing | qa_engineer | DONE | 100% | Passed across Sprints 3-9; 1878-test suite |
| DOCS | Documentation update | lead-backend | DONE | 100% | STATUS.md, ARCHITECTURE.md, ADR-001…012 |
| PERF | Performance profiling | lead-backend | DONE | 100% | Report-only perf suite `test_message_bus_perf.py` + ADR-010 trigger |
| FINAL | Final verification pass | ALL | DONE | 100% | ruff + mypy + pytest green (CI) |
| | **Sprint 5 Total** | | | **4/4** | **4.5h estimated** |

---

## Capacity Summary

| Agent | Sprint 3 | Sprint 4 | Sprint 5 | Total | Available |
|-------|----------|----------|----------|-------|-----------|
| lead-backend | 11.0h | 7.0h | 1.0h | 19.0h | 24h |
| lead-frontend | 6.0h | 0h | 0h | 6.0h | 11h |
| qa_engineer | 2.0h | 8.0h | 2.0h | 12.0h | 10h* |
| security_engineer | 0h | 5.0h | 0h | 5.0h | 6h |
| **Total** | **19.0h** | **20.0h** | **3.0h** | **42.0h** | **51h** |

> *qa_engineer has 10h estimated but 12h assigned — 2h buffer comes from Sprint 5 regression testing being flexible.

---

## Blockers

| ID | Blocked Task | Blocked By | Since | Status |
|----|-------------|------------|-------|--------|
| — | No current blockers | — | — | — |

---

## Recently Completed

| ID | Task | Completed | By |
|----|------|-----------|-----|
| S2-01 | Route Inbox I/O through MessageBus | 2026-07-20 | lead-backend |
| S2-02 | Atomic FileStore abstraction | 2026-07-20 | lead-backend |
| S2-03 | Dashboard API uses MessageBus | 2026-07-20 | lead-backend |
| S2-04 | Tier rules integrated | 2026-07-20 | lead-backend |
| S2-05 | Non-blocking HITL gate | 2026-07-20 | lead-backend |
| S2-06 | AgentLoop priority forwarding | 2026-07-20 | lead-backend |
| S2-07 | CostTracker persistence | 2026-07-20 | lead-backend |
| S2-08 | Dashboard CORS/auth | 2026-07-20 | lead-frontend |
| S2-09 | LLM retry cycling | 2026-07-20 | lead-backend |
| S2-10 | Remove shell=True | 2026-07-20 | lead-backend |
| S2-11 | Department SOPs | 2026-07-20 | content_creator |
| S2-12 | Audit wiring | 2026-07-20 | lead-backend |
| S2-13 | Escalation persistence | 2026-07-20 | lead-backend |
