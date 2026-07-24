# AI Company Builder — Task Board

**Sprint 3 Status:** ACTIVE  
**Last Updated:** 2026-07-21  
**Sprint Goal:** Complete all P2 features — Dashboard real-time, Memory enhancements, Autonomous scheduling

---

## Sprint 3 Tasks

| ID | Task | Owner | Status | % | Blocked By | Notes |
|----|------|-------|--------|---|------------|-------|
| S3-01 | WebSocket broadcast full wiring | lead-frontend | NOT STARTED | 0% | — | ws.py + api.py already have broadcast calls wired; verify end-to-end |
| S3-02 | OpenAPI/Swagger docs | lead-frontend | NOT STARTED | 0% | S3-01 | API must be stable first |
| S3-03 | Rate limiting (slowapi) | lead-frontend | NOT STARTED | 0% | — | 100 req/min default |
| S3-04 | Periodic memory consolidation | lead-backend | NOT STARTED | 0% | — | Wire consolidate_all() into executor tick |
| S3-05 | Memory search enhancement | lead-backend | NOT STARTED | 0% | — | Keyword + vector search already implemented; verify & expand |
| S3-06 | Memory retention TTL | lead-backend | NOT STARTED | 0% | S3-04 | Pruning depends on consolidation cadence |
| S3-07 | Scheduled cycle daemon | lead-backend | NOT STARTED | 0% | — | Scheduler exists; verify cron-like scheduling |
| S3-14 | Approval escalation tests | qa_engineer | NOT STARTED | 0% | — | Independent; can start immediately |
| S3-18 | Fix BriefingGenerator private method | lead-backend | DONE | 100% | — | Close GAP-014 — `briefing.py:42` uses `get_all_tasks()` |
| S3-19 | Fix LLM retry provider cycling | lead-backend | DONE | 100% | — | Close GAP-015 — `client.py:133-134` round-robin cycling |
| | **Sprint 3 Total** | | | **0/10** | | **17.0h estimated** |

---

## Sprint 4 Tasks

| ID | Task | Owner | Status | % | Blocked By | Notes |
|----|------|-------|--------|---|------------|-------|
| S3-08 | Structured logging with correlation IDs | lead-backend | NOT STARTED | 0% | — | Cross-cutting; batch commit |
| S3-09 | Agent spec validation CLI | lead-backend | NOT STARTED | 0% | — | Close GAP-019 |
| S3-10 | CLI type hints/docstrings | lead-backend | NOT STARTED | 0% | — | 24 CLI files |
| S3-11 | Full pipeline integration test | qa_engineer | NOT STARTED | 0% | S3-01, S3-04 | Needs stable executor + dashboard |
| S3-12 | CLI command test suite | qa_engineer | NOT STARTED | 0% | S3-10 | Tests validate typed interfaces |
| S3-13 | API endpoint test suite | qa_engineer | NOT STARTED | 0% | S3-01, S3-03 | Tests validate stable API |
| S3-15 | OAuth2/key rotation | security_engineer | NOT STARTED | 0% | S3-03 | Rate limiting first |
| S3-16 | Memory encryption | security_engineer | NOT STARTED | 0% | S3-04, S3-05, S3-06 | Memory must be stable |
| S3-17 | Token counting integration | lead-backend | NOT STARTED | 0% | — | |
| | **Sprint 4 Total** | | | **0/9** | | **22.0h estimated** |

---

## Sprint 5 Tasks (Buffer)

| ID | Task | Owner | Status | % | Notes |
|----|------|-------|--------|---|-------|
| REGRESSION | Regression testing | qa_engineer | NOT STARTED | 0% | Buffer for Sprint 3-4 fixes |
| DOCS | Documentation update | lead-backend | NOT STARTED | 0% | STATUS.md, ARCHITECTURE.md |
| PERF | Performance profiling | lead-backend | NOT STARTED | 0% | Executor loop < 100ms |
| FINAL | Final verification pass | ALL | NOT STARTED | 0% | ruff + mypy + pytest |
| | **Sprint 5 Total** | | | **0/4** | **4.5h estimated** |

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
| S2-11 | Department SOPs | 2026-07-20 | content-creator |
| S2-12 | Audit wiring | 2026-07-20 | lead-backend |
| S2-13 | Escalation persistence | 2026-07-20 | lead-backend |
