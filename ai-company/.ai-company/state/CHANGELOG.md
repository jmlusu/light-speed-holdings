# Changelog

> Format follows [Keep a Changelog](https://keepachangelog.com/).

---

## [0.1.0] — 2026-07-17

### Added

#### Agent Job Descriptions
- Added `responsibilities: list[str]` field to `BoardMember` model
- Updated `config/board/board.yaml` with 10 responsibilities per board member (7 members, 70 total)
- Updated `config/executives/executives.yaml` with 10 responsibilities per executive (15 executives, 150 total)
- Updated `config/agents/specialists.yaml` with 10 responsibilities per specialist (22 specialists, 220 total)
- Added 3 new executives: ceo-advisor, chief-ai-officer, cpo
- Added 10 new specialists: product-designer, product-owner, fullstack-engineer, qa-lead, qa-automation-engineer, growth-hacker, business-developer, market-analyst, recruiter, content-creator
- Fixed `config/__init__.py` config loader to unwrap YAML top-level keys (company, board, executives, etc.)
- Updated `generator.py` to pass `responsibilities` to board template
- Regenerated all 56 agent .md files with full responsibilities
- 440 total responsibilities across all agents

#### Configuration Layer
- 19 YAML configuration files across 7 categories
- Company config: company, vision, strategy, culture, governance, policies, kpis, budget
- Board config: board, committees, meetings, voting
- Executive config: 12 executive roles
- Department config: 12 departments
- Specialist config: 17 specialist agents
- Decision config: approval_matrix, risk_matrix, decision_tree
- Workflow config: 9 workflow definitions
- Registry system: loader, parser, resolver, validator

#### Domain Models
- 17+ Pydantic models: Company, Executive, Department, Agent, BoardMember, Workflow, Task, Risk, Decision, etc.
- Enums: AgentType, Seniority, TaskStatus, TaskPriority, RiskLevel
- Backward-compatible field defaults

#### Templates
- 7 Jinja2 templates with inheritance
- Base template with block system (identity, extra_sections, metrics, escalation)
- Executive, department, specialist, board templates extending base
- Workflow and config templates (standalone)

#### Generation
- AgentGenerator with template selection by agent type
- generate_from_registry() for full registry-based generation
- BootstrapEngine for complete company scaffolding

#### Engines
- DecisionEngine: approval matrix matching, risk assessment, decision tree navigation
- WorkflowEngine: 9 workflows, step tracking, SLA monitoring, task conversion
- MemoryStore: 6 memory types, JSON persistence, consolidation
- GraphEngine: 4 graph types, BFS pathfinding

#### CLI
- 22 Typer subcommands
- company run/status with dry-run
- decision evaluate/matrix/tree
- graph list/show/path
- workflows list/run/status/advance
- memory list/add/search/consolidate
- agents, board, departments, executives, specialists
- orchestrator, models, dashboard, executor, doctor
- marketing, sales, customer-success, legal, hr

#### Testing
- 175 unit tests across 14 test modules
- Tests for models, registry, bootstrap, decision, workflow, memory, graph, generator

#### Infrastructure
- CI pipeline: ruff, mypy, pytest, harness lint
- ECL change lifecycle
- AGENTS.md agent operating guide

---

## [Unreleased]

### Planned
- Task execution loop
- HITL gates
- Briefing generation
- Scheduler
- Dashboard completion
- Performance analytics

---

## Related Documents

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Current status
- [ROADMAP.md](ROADMAP.md) — Full roadmap
- [RELEASE_PLAN.md](RELEASE_PLAN.md) — Release plan
