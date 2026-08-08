# Project Status

> If `harness/changes/active/summary.md` exists, active change files are the current task source of truth. Read them first.

## Last Updated

2026-08-08

## Current State

- **Sprint 4 Complete**: Quality & completeness (2026-08-08). Archived as `harness/changes/archive/2026-08-08-sprint-4-quality-completeness`. Commits `d11608f` (auth hardening, key rotation, token counting, CLI polish), `359489d` (platform-independent CLI help + daemon stop tests), `4765f76` (22 new agent skills + real KPI derivation). 1745 tests passing, ruff/mypy clean.
- **CEO Dashboard Operationalization Plan**: Sprint 3 complete (items 1-3). See `docs/CEO-DASHBOARD-OPERATIONALIZATION-PLAN.md`. Latest work (2026-08-07): data retention / governance engine wired end-to-end — `run_retention()` + `GovernanceScheduler` in `data/governance.py` (batched archive fix, rowid anonymize fix), daemon enforcement via `--governance-interval`, and `GET /api/governance` report endpoint. 1526 tests passing.
- **Sprint 1 Complete**: All critical code hardening and audit trail work done.
- **Sprint 2 Complete**: All 13 Sprint 2 items done and verified — code audit confirmed implementation in source, documentation sync completed 2026-07-21.
- **Sprint 3 Complete**: All 8 Sprint 3 items done — gap closure (GAP-014, GAP-015), E2E pipeline test, WebSocket tests, governance CLI, memory CLI, dashboard API tests, org chart test rewrite. 1205 tests passing. v0.3.0 release tagged 2026-07-22.
- **Agent Deployment**: All 127 agents deployed to workspace-level `.opencode/agents/` — every agent now invokable via `@` in terminal.
- **Organization Expansion**: 53 new roles added across all departments (2026-07-21) — competitive edge roles identified by CEO Advisor, CAIO, CISO, COO, CPO, CTO, CSO, General, and Human CEO agents.
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
- **CLI**: 26 commands registered — company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator (with postmortem sub-app), models, dashboard (with kpi sub-app), executor, doctor, marketing, sales, customer-success, legal, hr, generate, status, sop, raci, governance (report/audit-trail/risk-summary/retention/compliance/owners/policies).
- **FileStore**: `src/ai_company/store/file_store.py` exists with atomic writes (temp + rename) and platform-aware locking.
- **MessageBus**: `get_pending_tasks()` and `update_task_status()` present; executor routes all inbox I/O through it. WebSocket broadcast hooks present.
- **ToolRunner**: uses `shlex.split()` (no `shell=True`), consults `tier_rules.classify_tool_action()`, and logs via `log_tool_call()` / `log_hitl_decision()`.
- **HITLGate**: non-blocking via `concurrent.futures.Future` (`request_and_wait`).
- **Dashboard**: `app.py` has `X-API-Key` auth + configurable CORS. `ws.py` has broadcast functions (task/KPI/alert/escalation).
- **Escalation**: events persisted to YAML via `_save_config()` / `_load_config()`.
- **Tests**: 1526 tests passing (53 skipped, 0 failures) — all green as of 2026-08-07.

## Organization Expansion (2026-07-21)

### New Roles Added (53 total)

| Phase | Roles | Department | Priority |
|-------|-------|-----------|----------|
| **Phase 1: Immediate** | VP of Engineering, Data Engineer, AI Safety Lead, Program Manager, UX Research Lead, Technical Documentation Lead, Head of Developer Relations, Culture & Values Officer | Technology, Data, AI Research, Operations, Product, Marketing, People | Critical |
| **Phase 2: Weeks 1-8** | Red Team Engineer, Constitutional AI Owner, MLOps Engineer, Platform Engineer, Product Marketing Manager, Head of Business Development, Head of Competitive Intelligence, AI Security Specialist, Penetration Testing Lead, Incident Response Lead, DevSecOps Lead, Growth PM, DX Engineer, Product Designer, Eval Benchmarks Engineer, Prompt Engineer | AI Research, Technology, Marketing, Business Dev, Security, Product | Critical/High |
| **Phase 3: Weeks 9-16** | Frontend Architect, API Architect, Observability Engineer, Scalability Architect, Data Privacy Officer, Supply Chain Security Engineer, Security Architect, SOC 2 Analyst, Vendor Manager, Capacity Planner, Business Continuity Manager | Technology, Legal, Security, Operations | High |
| **Phase 4: Weeks 17-24** | Technical Writer, Learning & Development Lead, Employee Experience Lead, Investor Relations Lead, Revenue Operations Analyst, Solutions Engineer, Corporate Development Lead, Internal Comms Lead, Knowledge Manager, Process Quality Manager, Industry Analyst Relations Manager, Business Intelligence Engineer, Threat Intelligence Analyst, AI Ethics Board Chair, Human-AI Interaction Designer | Product, People, Finance, Sales, Strategy, Operations, Marketing, AI Research, Executive | High/Medium |

### Structural Improvements
- CTO span of control reduced from 9+ to 1 (VP of Engineering absorbs execution layer)
- Product department created with 8 roles under CPO
- Strategy department created with 2 roles under CSO
- Business Development function created reporting to CEO
- AI Safety hierarchy established (AI Safety Lead → Red Team, Constitutional AI, Ethics)
- **All 127 agents deployed** to workspace-level `.opencode/agents/` — fully invokable via `@`

## Code Quality

- **ruff**: ✅ Clean (0 errors) — as of 2026-08-07.
- **mypy**: ✅ Clean (0 errors, 177 files) — as of 2026-08-07.
- **pytest**: ✅ 1501 tests passing (53 skipped) — as of 2026-08-07.
- **Dead code**: Removed 5 one-time bootstrap scripts

## Documentation

- `docs/ARCHITECTURE.md` — System architecture and module hierarchy (updated 2026-07-20)
- `docs/ARCHITECTURE-GAPS.md` — 20 identified integration gaps with severity ratings (6 resolved)
- `docs/INTEGRATION-ARCHITECTURE.md` — Integration seam analysis
- `docs/STATUS.md` — This file
- `docs/SPRINT-1-TRACKER.md` — Sprint 1 task tracker (COMPLETE)
- `docs/SPRINT-1-BACKLOG.md` — Sprint 1 original backlog
- `docs/SPRINT-2-BACKLOG.md` — Sprint 2 prioritized backlog (13 items, 41 hours)
- `docs/SPRINT-3-BACKLOG.md` — Sprint 3 prioritized backlog (8 items, 22 hours)
- `docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md` — CEO dashboard architecture analysis
- `docs/EXECUTIVE_DASHBOARD_V1_STRATEGIC_PLAN.md` — Executive dashboard strategic plan
- `docs/IMPLEMENTATION_SUMMARY.md` — Implementation summary
- `docs/PHASE_3_COORDINATION_PLAN.md` — Phase 3 coordination plan
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

- **2026-08-08**: Sprint 4 COMPLETE — quality & completeness. Commits: `d11608f` (GAP-019 agent spec validation, daemon lifecycle, key rotation, token counting, CLI type hints/docstrings, test suites for CLI/dashboard/escalation, dashboard security hardening), `359489d` (platform-independent CLI help + daemon stop tests), `4765f76` (22 new agent skills + manifest, company KPIs computed from real sources per CEO decision via `scripts/compute_company_kpis.py`, `run_backfill.py` SQLite utility). Deferred to next sprint: T009 OAuth2 client credentials, T012 `ai-company llm usage`. ECL change archived as `harness/changes/archive/2026-08-08-sprint-4-quality-completeness`. Gates: ruff/mypy clean, **1745 tests passing**, CLI help verified. 35 scratch files cleaned from workspace.
- **2026-08-07**: CEO Dashboard Operationalization Plan — Sprint 3 item 3 shipped (`550b11b`): data retention / governance engine end-to-end — `run_retention()` + `GovernanceScheduler` in `data/governance.py` with batched archive (fixed latent bug: each batch appended then only that batch deleted) and rowid-based anonymize (fixed latent bug: `agent_id` + `content` hashed). `ExecutorDaemon` gains `--governance-interval` enforcement; `GET /api/governance` endpoint returns full report (`available`, `tables`, `owners`, `policies`). 8 real-DB tests (`test_governance_engine.py`). CI green: ruff/mypy/pytest (1526 passing).
- **2026-08-07**: CEO Dashboard Operationalization Plan — Sprint 3 item 2 shipped (`9a5a244`): `get_company_kpi_summary()` read-through accessor computes company KPIs vs targets from real telemetry — Build Success Rate (KPI-004) and Agent Utilization (KPI-003) computed from the task window (SQLite-first, inbox fallback); ARR/CSAT/eNPS report configured values. `GET /api/company-kpis` returns the full summary shape (`collected_at`, `period_days`, `kpis[]` with `status/gap/computed/source`, `summary`). Frontend gained a "Company KPIs vs Targets" card grid + Current-vs-Target chart, and department KPI cards now merge live telemetry instead of rendering "undefined". 7 new tests (`tests/unit/test_company_kpis.py`). 1501 tests passing.
- **2026-07-22**: Sprint 3 COMPLETE — all 8 items done. Fixed test_org_chart.py (832 lines rewritten, 56 tests passing). Fixed DataTransformer.registry_to_enhanced() frozen model bug. Created governance CLI (7 commands, 9 tests). Enhanced memory CLI (stats/search/recall). Created WebSocket integration tests (30 tests). Created dashboard API tests (9 tests). Total: 1205 tests passing, 0 ruff errors. v0.3.0 release tagged. **Agent deployment**: All 127 agents deployed to workspace-level `.opencode/agents/` — every agent now invokable via `@`.
- **2026-07-21**: Sprint 3 backlog created (docs/SPRINT-3-BACKLOG.md). Code audit reveals ~60% of planned Sprint 3 items already implemented in source. Revised scope: 8 items, 22 hours effort. Sprint 2 finalization — fixed 2 stale rate limiter test assertions (1091→1093 passing), confirmed mypy 0 errors (164 files), marked S2-03/S2-07 as Done in backlog, all CI gates green. Documentation sync — all docs updated to reflect actual project state.
- **2026-07-20**: Sprint 1 completed. All Track B (code hardening) and Track C (audit trail) items done. Sprint 2 backlog created. All documentation updated to reflect actual state.
- **2026-07-19**: Phase 5 design specs — 3 approval UX documents covering 5-tier action system, dashboard approval queue with WebSocket, and enhanced CLI commands.
- **2026-07-17**: Governance layer — autonomous GitHub Action (cron every 6h), postmortem template + store + CLI, incident response + deployment SOPs, RACI template + hiring workflow RACI, department KPI dashboards (7 departments, 28 KPIs), dashboard CLI, postmortem CLI, sop/raci CLI commands, 8 new tests.
- **2026-07-17**: Cleanup pass — fixed E402 ruff warnings in llm/client.py, deleted 5 dead scripts, wired all 5 providers in opencode.json, created 3 governance/policy docs.

## Sprint Status

| Sprint | Status | Tests | Items |
|--------|--------|-------|-------|
| Sprint 1 | ✅ COMPLETE | — | Code hardening + audit trail |
| Sprint 2 | ✅ COMPLETE | 1093 passing | 13 items — all Done |
| Sprint 3 | ✅ COMPLETE | 1526 passing | 8 items — all Done |
| Sprint 4 | ✅ COMPLETE | 1745 passing | Quality & completeness |

## Remaining Work

- **Sprint 4**: COMPLETE — quality & completeness. Deferred to next sprint: OAuth2 client credentials (T009), `ai-company llm usage` CLI (T012), structured logging with correlation IDs (GAP-018), scheduled cycle daemon mode (S3-06).
