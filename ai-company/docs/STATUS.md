# Project Status

> If `harness/changes/active/summary.md` exists, active change files are the current task source of truth. Read them first.

## Last Updated

2026-07-20

## Current State

- **Sprint 1 Complete**: All critical code hardening and audit trail work done. 727 tests passing. Ruff + mypy clean.
- **Models**: 17+ Pydantic models in `src/ai_company/models/models.py` (Company, Executive, Department, Agent, Workflow, Task, Risk, Decision, Postmortem, etc.)
- **Registry**: 4-module system — `registry/loader.py`, `parser.py`, `resolver.py`, `validator.py` — loads 19 YAML config files into typed `CompanyRegistry`.
- **Templates**: 12 Jinja2 templates — `base.md.j2`, `executive.md.j2`, `department.md.j2`, `specialist_v2.md.j2`, `board_v2.md.j2`, `workflow.md.j2`, `config.md.j2`, `postmortem.md.j2`, `sop.md.j2`, `raci.md.j2`, `agent.md.j2`, and one additional template.
- **Generator**: Template selection by agent type + `generate_from_registry()` for full registry-based generation.
- **BootstrapEngine**: `builder/__init__.py` — creates 24 directories, generates agents + configs from registry.
- **Executor**: `executor/loop.py` — polls inbox.json, runs AgentLoop (multi-turn ReAct), dead-letter queue, memory recall, audit logging.
- **AgentLoop**: `executor/agent_loop.py` — ReAct pattern, multi-turn LLM↔tool interaction, cost tracking, HITL gates, budget enforcement.
- **DecisionEngine**: `decision/engine.py` — evaluates actions against approval matrix, risk assessment, decision tree navigation.
- **WorkflowEngine**: `workflow/engine.py` — 9 workflow definitions, step tracking, SLA monitoring, task conversion.
- **MemoryEngine**: `memory/engine.py` — 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate) with persistence + executor integration.
- **GraphEngine**: `graph/engine.py` — 4 graph types (org_chart, decision_graph, workflow_graph, knowledge_graph) with BFS pathfinding.
- **Audit Trail**: `audit/` — AuditEvent, AuditWriter, AuditReader with executor integration (tool calls, task lifecycle, HITL decisions).
- **Dead-Letter Queue**: `executor/dead_letter.py` — stale task detection, DLQ with retry.
- **Circuit Breaker**: `llm/circuit_breaker.py` — LLM provider fail-fast after N errors.
- **Cost Tracker**: `llm/cost_tracker.py` — JSONL logging, daily/task budgets, per-model pricing.
- **Postmortem**: `orchestrator/escalation.py` — Postmortem + PostmortemStore models for incident tracking, resolution, and template rendering.
- **KPIs**: `company/config/kpis.yaml` — Department-level KPI definitions for 7 departments (engineering, hr, marketing, sales, customer_success, legal, finance).
- **KPI Collectors**: `dashboard/kpis/__init__.py` — All 7 department collectors wired and operational.
- **Analytics**: `dashboard/analytics.py` — History tracking, trend analysis, alert rules, summary rollups.
- **CLI**: 24 commands registered — company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator (with postmortem sub-app), models, dashboard (with kpi sub-app), executor, doctor, marketing, sales, customer-success, legal, hr, generate, status, sop, raci.
- **Tests**: 727 collected, ruff clean, mypy clean.

## Code Quality

- **ruff**: All checks passed (0 errors)
- **mypy**: No issues found in 81+ source files
- **pytest**: 727 tests collected (2 collection errors in test_security.py and test_ml.py — skip with `--ignore`)
- **Known lint issues**: None — all resolved (json import and E741 warnings fixed)
- **Dead code**: Removed 5 one-time bootstrap scripts

## Documentation

- `docs/ARCHITECTURE.md` — System architecture and module hierarchy (updated 2026-07-20)
- `docs/ARCHITECTURE-GAPS.md` — 20 identified integration gaps with severity ratings (6 resolved)
- `docs/INTEGRATION-ARCHITECTURE.md` — Integration seam analysis
- `docs/STATUS.md` — This file
- `docs/SPRINT-1-TRACKER.md` — Sprint 1 task tracker (COMPLETE)
- `docs/SPRINT-1-BACKLOG.md` — Sprint 1 original backlog
- `docs/SPRINT-2-BACKLOG.md` — Sprint 2 prioritized backlog (13 items, 41 hours)
- `docs/DEVELOPER-GUIDE.md` — Developer onboarding guide
- `docs/ECL.md` — Change lifecycle and context loading rules
- `docs/COMPANY-CONSTITUTION.md` — Principles and decision order
- `docs/DECISION-FRAMEWORK.md` — Decision engine rules
- `docs/ORGANIZATION.md` — Organization overview
- `docs/MODEL-ROUTING-POLICY.md` — Provider catalog, tiers, routing rules, cost control
- `docs/RISK-REGISTER.md` — 14-item risk register with mitigations and owners
- `docs/BOARD-GOVERNANCE.md` — Board charter, meeting cadence, voting rules, decision authority
- `docs/REMAINING-WORK-INVENTORY.md` — Full inventory of remaining work items
- `docs/sop-incident-response.md` — Incident response SOP
- `docs/sop-deployment.md` — Agent deployment SOP
- `docs/sop-hr-onboarding.md` — HR onboarding SOP
- `docs/sop-budget-approval.md` — Budget approval SOP
- `docs/raci-hiring.md` — RACI matrix for hiring workflow
- `docs/raci-escalation.md` — RACI matrix for escalation workflow
- `docs/raci-deployment.md` — RACI matrix for deployment workflow

## Recent Work

- **2026-07-20**: Sprint 1 completed. All Track B (code hardening) and Track C (audit trail) items done. Sprint 2 backlog created. All documentation updated to reflect actual state.
- **2026-07-19**: Phase 5 design specs — 3 approval UX documents covering 5-tier action system, dashboard approval queue with WebSocket, and enhanced CLI commands.
- **2026-07-17**: Governance layer — autonomous GitHub Action (cron every 6h), postmortem template + store + CLI, incident response + deployment SOPs, RACI template + hiring workflow RACI, department KPI dashboards (7 departments, 28 KPIs), dashboard CLI, postmortem CLI, sop/raci CLI commands, 8 new tests.
- **2026-07-17**: Cleanup pass — fixed E402 ruff warnings in llm/client.py, deleted 5 dead scripts, wired all 5 providers in opencode.json, created 3 governance/policy docs.

## Sprint Status

| Sprint | Status | Tests | Items |
|--------|--------|-------|-------|
| Sprint 1 | ✅ COMPLETE | 727 | Code hardening + audit trail |
| Sprint 2 | 🟡 PLANNED | — | 13 items, 41 hours (security + integration) |
| Sprint 3 | 🔴 NOT STARTED | — | Autonomous coordination |
| Sprint 4 | 🔴 NOT STARTED | — | Quality & completeness |

## Remaining Work

- **Sprint 2 (next)**: Security & integration hardening — FileStore abstraction, MessageBus single source of truth, 5-tier approval system, non-blocking HITL, dashboard auth, remaining SOPs
- Wire periodic memory consolidation into executor loop
- Implement WebSocket broadcast for real-time dashboard updates
- Persist escalation events to YAML
- Add structured logging with correlation IDs
- Add agent spec validation CLI command
- Full end-to-end integration test with mocked LLM
