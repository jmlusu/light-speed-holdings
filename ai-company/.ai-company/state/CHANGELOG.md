# Changelog

> Format follows [Keep a Changelog](https://keepachangelog.com/).

---

## [0.4.0] — 2026-08-11

### Added

#### Deployment & Release Infrastructure
- **Multi-stage Dockerfile** with builder and runtime stages for smaller production images
- **Docker Build/Push to GHCR** in release workflow with multi-arch support via Buildx
- **PyPI Trusted Publishing** via OIDC (no API tokens required) — configured in release workflow
- **SemVer Validation** in CI and release: verifies `pyproject.toml` version matches git tag and CHANGELOG
- **Version Sync Check** in CI: ensures pyproject.toml, CHANGELOG, and latest git tag are in sync
- **GitHub Release Automation** with artifact attachment and auto-generated release notes

#### Docker & Compose Harmonization
- **Production `docker-compose.yml`** now mirrors `docker-compose.staging.yml` structure:
  - Named network (`ai-company`) for service discovery
  - Healthcheck on dashboard service (curl `/health`)
  - Profiles: `worker`, `monitoring` (production); `staging`, `worker`, `monitoring` (staging)
  - Prometheus service under `monitoring` profile
  - Environment variable parity with `${VAR:-}` substitution for all API keys
  - Port mapping: prod 8420:8420, staging 8421:8420
- **`.dockerignore`** excluding `.env`, `.git`, caches, logs, results, virtual envs

#### Dashboard Health & Monitoring
- **Health endpoint** (`/health`) confirmed in monitoring router with deep dependency checks
- **Readiness endpoint** (`/ready`) for Kubernetes-style probes
- **Prometheus `/metrics`** endpoint with agent performance, LLM costs, memory, and system metrics

### Changed

#### Dockerfile
- Refactored from single-stage to **multi-stage** (builder → runtime)
- Builder stage: installs build deps, runs `uv sync --frozen --no-dev`
- Runtime stage: copies only `.venv` and required runtime directories (`config/`, `orchestrator/`, `templates/`, `company/`, `docs/`, `.opencode/`, `scripts/`, `src/`)
- Non-root user (`appuser`) in both stages
- Healthcheck uses `/health` endpoint

#### CI/CD Workflows
- New `release.yml`: version-check → build → publish-pypi → docker → github-release
- New `ci.yml`: lint-and-typecheck, test, version-check, harness-lint jobs
- Ruff, mypy, bandit, pytest gates on every PR and push

### Fixed
- Version drift between `pyproject.toml` (0.4.0), CHANGELOG, and git tags
- Missing healthcheck in production compose
- Inconsistent environment variables between staging and production compose

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

## Related Documents

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Current status
- [ROADMAP.md](ROADMAP.md) — Full roadmap
- [RELEASE_PLAN.md](RELEASE_PLAN.md) — Release plan
