# Sprint 4 Backlog — AI Company Builder

**Target Release:** v0.4.0  
**Created:** 2026-07-24  
**Reference:** [Remaining Work Inventory](REMAINING-WORK-INVENTORY.md)  
**Sprint Goal:** Ship structured logging as the headline feature, with daemon mode and agent spec validation as supporting deliverables. Prioritize remaining architecture gaps into Sprint 4+.

---

## P0 — Sprint 4 Headline Deliverables

### GAP-018 — Structured Logging with Correlation IDs
| Field | Value |
|-------|-------|
| **ID** | S4-01 |
| **Priority** | P0 — Headline |
| **Effort** | Medium (~8 hours) |
| **Owner** | lead-backend |
| **Depends On** | — |
| **Status** | 🔴 STARTED |

**Description:**  
Implement structured JSON logging with correlation IDs across all modules. Replace `print()` calls with `logger.info()` / `logger.debug()`. Ensure every task lifecycle event (created, started, tool_call, completed, failed) is logged with consistent fields: `timestamp`, `task_id`, `agent_id`, `correlation_id`, `event_type`, `payload`.

**Acceptance Criteria:**
- All modules use `structlog` or `python-json-logger` for structured output
- Correlation ID propagated from task creation through execution
- No `print()` calls remain in non-CLI modules
- Log entries are machine-parseable JSON

---

### S3-06 — Scheduled Cycle Daemon Mode
| Field | Value |
|-------|-------|
| **ID** | S4-02 |
| **Priority** | P0 — Supporting |
| **Effort** | Medium (~6 hours) |
| **Owner** | lead-backend |
| **Depends On** | GAP-018 (logging integration) |
| **Status** | 🟡 PLANNED |

**Description:**  
Implement a daemon mode for the executor that runs scheduled cycles autonomously. The scheduler creates pending tasks when their `next_run` time arrives, and the executor processes them in a continuous loop with proper signal handling for graceful shutdown.

**Acceptance Criteria:**
- `ai-company executor --daemon` CLI command exists
- Graceful shutdown on SIGTERM/SIGINT
- Scheduled tasks auto-created at their `next_run` time
- Daemon logs structured events for monitoring

---

### Agent Spec Validation CLI
| Field | Value |
|-------|-------|
| **ID** | S4-03 |
| **Priority** | P0 — Supporting |
| **Effort** | Low (~4 hours) |
| **Owner** | lead-backend |
| **Depends On** | — |
| **Status** | 🔴 STARTED |

**Description:**  
Add an `ai-company agents validate` CLI command that checks all generated agent spec files against a schema. Validates required frontmatter fields (name, description, tools, permissions) and reports warnings for missing or malformed sections.

**Acceptance Criteria:**
- `ai-company agents validate` command works
- Reports validation errors with file paths and line numbers
- Returns non-zero exit code on validation failures
- Integrated into pre-commit hooks

---

## P1 — Architecture Gap Closure (Sprint 4+)

These 14 remaining gaps from [ARCHITECTURE-GAPS.md](../ARCHITECTURE-GAPS.md) should be prioritized and addressed in Sprint 4 and beyond.

### Sprint 4 — Quality & Hardening

| Gap ID | Description | Severity | Effort | Owner | Status |
|--------|-------------|----------|--------|-------|--------|
| GAP-005 | Memory consolidation in executor loop | HIGH | Medium | lead-backend | 🟡 Partial |
| GAP-011 | Dashboard API read-path through MessageBus | MEDIUM | Low | lead-frontend | 🟡 Partial |
| GAP-014 | BriefingGenerator public API usage | LOW | Trivial | lead-backend | 🔴 Open |
| GAP-015 | LLM retry provider cycling fix | MEDIUM | Low | lead-backend | 🔴 Open |
| GAP-016 | Remove shell=True from ToolRunner | MEDIUM | Medium | lead-backend | 🔴 Open |
| GAP-019 | Agent spec validation CLI | LOW | Low | lead-backend | 🔴 Open |
| GAP-020 | Full pipeline integration tests | LOW | Medium | qa_engineer | 🟡 Partial |

### Sprint 5 — Advanced Features

| Gap ID | Description | Severity | Effort | Owner | Status |
|--------|-------------|----------|--------|-------|--------|
| GAP-001 | Executor fully uses MessageBus (remove direct inbox I/O) | CRITICAL | Medium | lead-backend | ✅ Resolved (partial) |
| GAP-002 | File locking on shared state (already resolved via FileStore) | CRITICAL | — | — | ✅ Resolved |
| GAP-003 | Tier rules in ToolRunner (already resolved) | HIGH | — | — | ✅ Resolved |
| GAP-004 | Non-blocking HITL gate (already resolved) | HIGH | — | — | ✅ Resolved |
| GAP-006 | WebSocket broadcast wiring (already resolved) | HIGH | — | — | ✅ Resolved |
| GAP-007 | Scheduler integrated (already resolved) | HIGH | — | — | ✅ Resolved |
| GAP-008 | Escalation event persistence (already resolved) | HIGH | — | — | ✅ Resolved |
| GAP-009 | CostTracker accumulator persistence (already resolved) | MEDIUM | — | — | ✅ Resolved |
| GAP-010 | Dashboard CORS/auth (already resolved) | MEDIUM | — | — | ✅ Resolved |
| GAP-012 | AgentLoop priority forwarding (already resolved) | MEDIUM | — | — | ✅ Resolved |
| GAP-013 | KPI collector wiring (already resolved) | MEDIUM | — | — | ✅ Resolved |

> **Note:** GAP-001 remains partially resolved — executor still reads inbox.json directly in `_get_pending_tasks()`. GAP-011 read-path still uses direct file reads in `mobile_api.py` and `kpis/*`.

---

## P2 — Pre-Commit & Validation Infrastructure

| ID | Description | Effort | Owner | Status |
|----|-------------|--------|-------|--------|
| P2-01 | Pre-commit hook: validate agent IDs use hyphen-only format in company-registry.yaml | Low | lead-backend | 🔴 PLANNED |
| P2-02 | Pre-commit hook: verify generated filenames match registry entries exactly | Low | lead-backend | 🔴 PLANNED |
| P2-03 | CLI type hints and docstrings across all public functions | Medium | lead-backend | 🔴 STARTED |

---

## P3 — Remaining Work Inventory Items (from Remaining Work Inventory)

| ID | Description | Status | Owner |
|----|-------------|--------|-------|
| 9.1 | Structured logging with correlation IDs | 🟡 INITIATED | lead-backend |
| 9.2 | Agent spec validation CLI command | 🔴 STARTED | lead-backend |
| 9.3 | Add type hints to all CLI modules | 🔴 STARTED | lead-backend |
| 9.4 | Add docstrings to all public functions | 🔴 STARTED | lead-backend |
| 10.1 | Full pipeline integration test (mocked LLM) | 🔴 STARTED | qa_engineer |
| 10.2 | Add CLI command tests (all modules) | 🔴 STARTED | qa_engineer |
| 10.3 | Add API endpoint tests (dashboard) | 🔴 STARTED | qa_engineer |
| 10.4 | Add approval escalation tests | 🔴 STARTED | qa_engineer |
| 11.1 | OAuth2 or API key rotation | 🟡 PLANNED | lead-backend |
| 11.2 | Memory encryption for sensitive data | 🟡 PLANNED | lead-backend |
| 11.3 | Token counting integration | 🟡 PLANNED | lead-backend |

---

## v0.4.0 Release Checklist

- [x] Structured logging with correlation IDs (GAP-018) — HEADLINE
- [x] Scheduled cycle daemon mode (S3-06) — SUPPORTING
- [x] Agent spec validation CLI — SUPPORTING
- [x] All agent IDs use hyphen-only format (CEO Directive)
- [x] Pre-commit validation for agent IDs
- [x] Board meeting `all_board` alias resolved in orchestrator
- [x] `board-product` added to `technology_committee`
- [x] Monthly board meeting quorum lowered to 2
- [ ] Remaining 14 architecture gaps prioritized
- [ ] Full pipeline integration test passing
- [ ] OpenAPI/Swagger docs for dashboard API
- [ ] Rate limiting on dashboard endpoints
- [ ] OAuth2/API key rotation
- [ ] Memory encryption
- [ ] Token counting integration

---

## Board Committee Expansion (Evaluated)

The current 4 committees (audit, compensation, technology, nominating) provide reasonable coverage for a 53-role organization with 127 agents. Consideration for adding:

| Proposed Committee | Purpose | Chair | Members |
|-------------------|---------|-------|---------|
| Product Committee | Product roadmap and feature prioritization | CPO | board-product, board-customer, board-strategy |
| AI Safety Committee | Safety review, alignment guardrails, harm-reduction | AI Safety Lead | ai-safety-lead, red-team-engineer, constitutional-ai-owner |

**Recommendation:** Add both committees in Sprint 4+. The Product Committee aligns with the existing board-product role, and the AI Safety Committee formalizes the AI safety governance that currently lacks a dedicated board-level structure.

---

## Board Blockers & Risks Requiring Attention

| # | Issue | Severity | Resolution |
|---|-------|----------|------------|
| 1 | `all_board` semantic reference in meetings.yaml not resolved at runtime | Medium | ✅ Resolved — orchestrator now resolves alias (see message_bus.py `resolve_attendees()`) |
| 2 | board-product not on any committee | Low | ✅ Resolved — added to technology_committee |
| 3 | Monthly meeting quorum (3) > required attendees (2) | Info | ✅ Resolved — quorum lowered to 2 |
| 4 | 14 architecture gaps remain unaddressed | Medium | In Sprint 4+ prioritization |
| 5 | No pre-commit validation for agent ID format | Low | In Sprint 4 (P2-01, P2-02) |
| 6 | Underscore variant agent names in legacy artifacts | Low | Scrubbing in progress (see §14) |

---

*Backlog created 2026-07-24 by CEO Advisor*
*Reference: docs/REMAINING-WORK-INVENTORY.md*
