# Changelog

All notable changes to AI Company Builder are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- Sprint 2: Audit trail (JSONL writer, query/filter, integration with executor)
- Sprint 2: 5-tier approval system (classify_tool_action, tier-aware HITL gate, two-person rule)
- Sprint 2: Memory engine wiring (episodic/semantic/procedural recording on task completion)
- Sprint 2: HITL async fix (threading.Event replaces time.sleep, non-blocking executor)
- Sprint 2: WebSocket broadcasts (KPI snapshots + approval/escalation alerts)
- Sprint 2: LLM streaming support (SSE/NDJSON parsing for OpenAI, Anthropic, Ollama)
- Sprint 2: Scheduler-to-Executor wiring (autonomous cycle from scheduled tasks)
- Sprint 2: Deployment infrastructure (release.yml, release.ps1, CHANGELOG)
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
- Ruff E402 warnings in `llm/client.py` (import ordering)

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
