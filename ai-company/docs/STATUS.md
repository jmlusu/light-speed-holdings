# Project Status

> If `harness/changes/active/summary.md` exists, active change files are the current task source of truth. Read them first.

## Last Updated

2026-07-19

## Current State

- **V2 Complete + Governance Layer Done**: All 6 milestones delivered. Dead code removed, lint clean, all 5 providers wired. Governance documentation complete.
- **Models**: 17+ Pydantic models in `src/ai_company/models/models.py` (Company, Executive, Department, Agent, Workflow, Task, Risk, Decision, Postmortem, etc.)
- **Registry**: 4-module system — `registry/loader.py`, `parser.py`, `resolver.py`, `validator.py` — loads 19 YAML config files into typed `CompanyRegistry`.
- **Templates**: 12 Jinja2 templates — `base.md.j2`, `executive.md.j2`, `department.md.j2`, `specialist_v2.md.j2`, `board_v2.md.j2`, `workflow.md.j2`, `config.md.j2`, `postmortem.md.j2`, `sop.md.j2`, `raci.md.j2`, `agent.md.j2`.
- **Generator**: Template selection by agent type + `generate_from_registry()` for full registry-based generation.
- **BootstrapEngine**: `builder/__init__.py` — creates 24 directories, generates agents + configs from registry.
- **DecisionEngine**: `decision/engine.py` — evaluates actions against approval matrix, risk assessment, decision tree navigation.
- **WorkflowEngine**: `workflow/engine.py` — 9 workflow definitions, step tracking, SLA monitoring, task conversion.
- **MemoryEngine**: `memory/engine.py` — 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate) with persistence.
- **GraphEngine**: `graph/engine.py` — 4 graph types (org_chart, decision_graph, workflow_graph, knowledge_graph) with BFS pathfinding.
- **Postmortem**: `orchestrator/escalation.py` — Postmortem + PostmortemStore models for incident tracking, resolution, and template rendering.
- **KPIs**: `company/config/kpis.yaml` — Department-level KPI definitions for 7 departments (engineering, hr, marketing, sales, customer_success, legal, finance, devops).
- **CLI**: 24 commands registered — company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator (with postmortem sub-app), models, dashboard (with kpi sub-app), executor, doctor, marketing, sales, customer-success, legal, hr, generate, status, sop, raci.
- **Tests**: 183 passing, mypy clean, ruff clean.
- **CI**: `.github/workflows/ci.yml` — lint, test, harness jobs on push/PR to main.
- **Autonomous**: `.github/workflows/autonomous.yml` — cron-scheduled orchestrator/executor tick every 6 hours.
- **Providers**: All 5 providers registered in `.opencode/opencode.json` (opencode, deepseek, ollama, openai, anthropic).

## Code Quality

- **ruff**: All checks passed (0 errors)
- **mypy**: No issues found in 81 source files
- **pytest**: 183/183 tests passing
- **Dead code**: Removed 5 one-time bootstrap scripts (build_project.py, setup_files.py, phase3_setup.py, add_missing_agents.py, generate-dashboard.py)

## Documentation

- `docs/ARCHITECTURE.md` — System architecture and module hierarchy
- `docs/ECL.md` — Change lifecycle and context loading rules
- `docs/COMPANY-CONSTITUTION.md` — Principles and decision order
- `docs/DECISION-FRAMEWORK.md` — Decision engine rules
- `docs/ORGANIZATION.md` — Organization overview
- `docs/MODEL-ROUTING-POLICY.md` — Provider catalog, tiers, routing rules, cost control
- `docs/RISK-REGISTER.md` — 10-item risk register with mitigations and owners
- `docs/BOARD-GOVERNANCE.md` — Board charter, meeting cadence, voting rules, decision authority
- `docs/sop-incident-response.md` — Incident response SOP (detection → triage → resolve → learn)
- `docs/sop-deployment.md` — Agent deployment SOP (prepare → validate → generate → deploy)
- `docs/raci-hiring.md` — RACI matrix for the AI agent hiring workflow

## Recent Work

- **2026-07-19**: Phase 5 design specs — 3 approval UX documents covering 5-tier action system, dashboard approval queue with WebSocket, and enhanced CLI commands.
- **2026-07-17**: Governance layer — autonomous GitHub Action (cron every 6h), postmortem template + store + CLI, incident response + deployment SOPs, RACI template + hiring workflow RACI, department KPI dashboards (7 departments, 28 KPIs), dashboard CLI (`ai-company dashboard kpi list/show`), postmortem CLI (`ai-company orchestrator postmortem list/show/create/update/render`), sop/raci CLI commands, 8 new tests.
- **2026-07-17**: Cleanup pass — fixed E402 ruff warnings in llm/client.py, deleted 5 dead scripts, wired all 5 providers in opencode.json, created 3 governance/policy docs.
- **M1**: Config YAMLs (19 files), 17+ Pydantic models, registry system (loader/parser/resolver/validator), 21 new tests.
- **M2**: 7 Jinja2 templates with inheritance, multi-format generator with template selection.
- **M3**: BootstrapEngine — generates all agents, configs, directories from registry. CLI `company run` command.
- **M4**: DecisionEngine (approval matrix, risk assessment, decision tree) + WorkflowEngine (9 workflows, step tracking, SLA). 23 new tests.
- **M5**: MemoryEngine (6 types, persistence, consolidation) + GraphEngine (4 types, BFS pathfinding). 25 new tests.
- **M6**: Full CLI wiring (22 commands), documentation updates.

## Remaining Work

- **Phase 5 (current)**: Approval gate hardening — 5-tier action system, dual-approval, timeout escalation. Design specs complete:
  - `docs/APPROVAL-UX-SPEC.md` — Tier definitions, per-tier UX, escalation paths, HITL integration
  - `docs/APPROVAL-DASHBOARD-UI.md` — Dashboard approval queue, WebSocket real-time, REST API extensions
  - `docs/APPROVAL-CLI-COMMANDS.md` — Enhanced CLI commands (list, approve, reject, show, history, tiers, stats, watch)
- Wire actual metric collection into KPI dashboards (currently definitions only, no live data)
- Add more department SOPs (HR, Legal, Finance)
- Implement scheduled cycle automation (long-running orchestrator daemon)
- Add approval gate integration to GitHub Action (human-in-the-loop before deployments)
