# Project Status

> **Last Updated**: 2026-10-18
> **Version**: 0.1.0
> **Phase**: Foundation (Complete) → Intelligence (Complete) → Autonomy (Current)

---

## Current Health

| Metric | Status |
|--------|--------|
| Tests | 2,642 passed, 2 skipped (67 deselected) |
| Lint | Clean (ruff: 0 findings) |
| Type Check | Clean (mypy: 0 errors, 232 files) |
| CLI | 40 commands operational |
| Agents | 91 generated (182 files in `.opencode/agents/`, incl. 91 `.bak` backups) |

---

## Architecture Maturity

| Component | Maturity | Notes |
|-----------|----------|-------|
| Configuration Layer | Production | 19 YAML files, 4-module registry |
| Domain Models | Production | 17+ Pydantic models |
| Agent Generation | Production | 7 templates, Jinja2 inheritance |
| Bootstrap Engine | Production | Full company generation |
| Decision Engine | Production | Approval matrix, risk, decision tree |
| Workflow Engine | Production | 9 workflows, step tracking, SLA |
| Memory Engine | Production | 6 types, persistence, consolidation |
| Graph Engine | Production | 4 types, BFS pathfinding |
| CLI | Production | 40 commands via Typer |
| Task Orchestration | Production | MessageBus routing, DLQ, delegation, scheduler integration |
| LLM Integration | Production | Multi-provider (openai_compatible/ollama/llamacpp), circuit breaker, cost tracking, cache |
| Dashboard | Production (API) | REST + WebSocket live updates, briefing/KPI/approval endpoints; `dashboard autonomous` CLI shortcut shipped (US-A09) |
| Executor | Production | Loop, daemon, approval gates, dead-letter, graceful shutdown |

---

## Implemented Components

### Configuration (19 files)
- Company: company, vision, strategy, culture, governance, policies, kpis, budget
- Board: board, committees, meetings, voting
- Executives: 12 roles
- Departments: 12 departments
- Specialists: 17 agents
- Decision: approval_matrix, risk_matrix, decision_tree
- Workflows: 9 workflows

### Models (17+)
Company, CompanyStructure, Vision, Strategy, Culture, Governance, Policy, KPI, Budget, BoardMember, Committee, Executive, Department, Agent, Workflow, Task, Risk, DecisionRecord

### Engines (4)
- DecisionEngine: approvals, risk assessment, decision tree navigation
- WorkflowEngine: 9 workflows, step tracking, SLA monitoring, task conversion
- MemoryStore: 6 types (episodic, semantic, procedural, relational, temporal, aggregate), persistence
- GraphEngine: 4 types (org_chart, decision_graph, workflow_graph, knowledge_graph), BFS

### Templates (7)
base.md.j2, executive.md.j2, department.md.j2, specialist_v2.md.j2, board_v2.md.j2, workflow.md.j2, config.md.j2

### CLI Commands (40)
Original 22: company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator, models, dashboard, executor, doctor, marketing, sales, customer-success, legal, hr, generate, status

Added since M6: sop, raci, sync-registry, transform-public-registry, create-deck, bootstrap, governance, knowledge, llm, archify, publishing, media, mcp, security, validate, client, onboarding, consulting

---

## Pending Components

| Component | Priority | Effort |
|-----------|----------|--------|
| Workflow-triggered scheduling (P5-05: `WorkflowEngine.to_tasks()` not yet wired to MessageBus) | Medium | Low |
| Dashboard completion (US-A09: dashboard UI acceptance criteria 658-662 still open; `dashboard autonomous` CLI shortcut shipped 2026-10-18) | Medium | Low |
| Performance analytics | Low | High |

---

## Recent Work

| Date | Milestone | Deliverable |
|------|-----------|-------------|
| 2026-10-18 | M11 | LLM hardening verified: multi-provider client, circuit breaker, cost tracker, cache, rate limiting (84 scoped tests) |
| 2026-10-18 | M10 | BriefingGenerator + CLI + dashboard endpoint + CI cron; Scheduler wired into executor loop (48 scoped tests) |
| 2026-10-18 | M9 | ApprovalGate 5-tier, expiry sweep, notifications, escalation engine (174 scoped tests) |
| 2026-10-18 | M8 | MessageBus loop, dead-letter, delegation, graceful shutdown, daemon (157 scoped tests) |
| 2026-07-16 | M6 | Full CLI wiring (22 commands), documentation updates |
| 2026-07-16 | M5 | MemoryEngine (6 types), GraphEngine (4 types), 25 tests |
| 2026-07-16 | M4 | DecisionEngine, WorkflowEngine, 23 tests |
| 2026-07-16 | M3 | BootstrapEngine, CLI company command, 7 tests |
| 2026-07-16 | M2 | 7 Jinja2 templates, multi-format generator |
| 2026-07-16 | M1 | 19 YAML configs, 17+ models, registry system, 21 tests |

---

## Pre-existing Issues

- None known. The former E402 import-order warnings in `src/ai_company/llm/client.py` are resolved (ruff clean as of 2026-10-18).

---

## Related Documents

- [CURRENT_SPRINT.md](CURRENT_SPRINT.md) — What we're working on now
- [ROADMAP.md](ROADMAP.md) — Full phase-by-phase roadmap
- [MILESTONES.md](MILESTONES.md) — Milestone tracking
- [TECH_DEBT.md](TECH_DEBT.md) — Known issues
- [CHANGELOG.md](CHANGELOG.md) — Version history
