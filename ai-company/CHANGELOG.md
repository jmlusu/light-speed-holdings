# Changelog

All notable changes to AI Company Builder are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Sprint 4 planned items: structured logging, agent spec validation, OAuth2, memory encryption

## [0.3.0] - 2026-07-22

### Added
- **Sprint 3 — Gap Closure & Quality:**
  - GAP-014 fixed: BriefingGenerator uses public `get_all_tasks()` API (S3-04)
  - GAP-015 fixed: LLM retry cycles providers round-robin (S3-05)
  - Full pipeline E2E integration test — 10 tests covering happy path, failure, memory, audit, tools (S3-08)
  - WebSocket integration tests — 30 tests covering broadcast, topic filtering, connection lifecycle, error handling (S3-01)
  - Dashboard API endpoint tests — 9 tests covering agents, tasks, KPIs, org chart (S3-07)
  - Data governance CLI — `ai-company governance report/audit-trail/risk-summary/retention/compliance/owners/policies` (S3-02)
  - Memory CLI enhanced — `ai-company memory stats/search/recall` commands (S3-03)
  - Organization chart test suite rewritten — 56 tests covering RegistryNormalizer, OrganizationChart, DataModels, Integration, Performance
- **Sprint 2 — Code Hardening & Governance:**
  - Audit trail (JSONL writer, query/filter, integration with executor)
  - 5-tier approval system (classify_tool_action, tier-aware HITL gate, two-person rule)
  - Memory engine wiring (episodic/semantic/procedural recording on task completion)
  - HITL async fix (threading.Event replaces time.sleep, non-blocking executor)
  - WebSocket broadcasts (KPI snapshots + approval/escalation alerts)
  - LLM streaming support (SSE/NDJSON parsing for OpenAI, Anthropic, Ollama)
  - Scheduler-to-Executor wiring (autonomous cycle from scheduled tasks)
  - Deployment infrastructure (release.yml, release.ps1, CHANGELOG)
  - Autonomous GitHub Action (cron every 6 hours) for orchestrator/executor ticks
  - Postmortem system: models, store, template rendering, CLI commands (`orchestrator postmortem`)
  - Incident response SOP (`sop-incident-response.md`)
  - Deployment SOP (`sop-deployment.md`)
  - RACI matrix template + hiring workflow RACI (`raci-hiring.md`)
  - Department KPI dashboards (7 departments, 28 KPIs) with API endpoints
  - Dashboard CLI: `ai-company dashboard kpi list/show`
  - SOP/RACI CLI commands: `ai-company sop`, `ai-company raci`
  - README.md with full project documentation
  - CHANGELOG.md
  - CONTRIBUTING.md
  - User guide (`docs/USER-GUIDE.md`)

### Fixed
- DataTransformer.registry_to_enhanced() frozen model mutation bug — now uses `model_copy(update=...)`
- Ruff E402 warnings in `llm/client.py` (import ordering)
- 7 lint errors in org_chart modules (unused imports/variables)
- Hyphenated `org-chart/` directory merged into `org_chart/`
- LLM retry provider cycling — flat loop with `attempt % len(provider_chain)` round-robin

### Removed
- 5 dead bootstrap scripts (`build_project.py`, `setup_files.py`, `phase3_setup.py`, `add_missing_agents.py`, `generate-dashboard.py`)
- Legacy empty modules (`utils/`, `validator/`, `opencode/`, `templates/` src, `cli/init.py`, `cli/config.py`)
- Legacy `validator.py` (superseded by `registry/validator.py`)
- Legacy `cli/commands.py` (superseded by `cli/main.py`)

## [0.2.0] - 2026-07-17

### Added
- V2 Foundation: 57 Pydantic models, registry system (loader/parser/resolver/validator)
- 14 Jinja2 templates with type-based selection
- BootstrapEngine for full company generation from config
- DecisionEngine (approval matrix, risk assessment, decision tree)
- WorkflowEngine (9 workflows, step tracking, SLA monitoring)
- MemoryEngine (6 memory types with persistence)
- GraphEngine (4 graph types, BFS pathfinding)
- 22 CLI subcommands wired through Typer
- FastAPI dashboard with REST API endpoints
- Model router with 3-tier cost control (fast/standard/premium)
- 5 LLM providers registered (opencode, deepseek, ollama, openai, anthropic)
- 183 unit tests
- CI pipeline (lint, test, harness)
- Governance docs (risk register, board governance, model routing policy)

## [0.1.0] - 2026-07-17

### Added
- Initial project structure
- CLI framework (Typer)
- Agent registry (`company-registry.yaml`)
- Agent generator (Jinja2 templates → `.opencode/agents/*.md`)
- MessageBus for task delegation
- Basic briefing generator
- 27 agents across 7 departments
