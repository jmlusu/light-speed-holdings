# Changelog

> Format follows [Keep a Changelog](https://keepachangelog.com/).

---

## [0.6.0] — 2026-09-02

### Added

- **Executive Scorecard**: CEO KPI set expanded from 6 to 11 metrics (task throughput, task success rate, agent utilization, cost efficiency, build success rate, escalation resolution time, escalation rate, approval turnaround, error rate, security posture, strategic alignment).
- **Dashboard UX**: Chart.js external tooltips, agent detail modal with role/reports-to/direct-reports, inline component detail panel on the home dashboard.

### Changed

- **Version**: 0.5.1 → 0.6.0
- **Reporting Structure**: Executive `reports_to` rewired to human CEO; legal moved under CLO; stale `direct_reports` pruned and reconciled in the agent registry.

### Fixed

- **Dashboard org-chart drift**: `direct_reports` on `chief_of_staff`, `coo`, `clo`, and `qa_lead` cleaned to match authoritative `reports_to` lines (verified via `ai-company sync-registry --verify`).

---

## [0.5.1] — 2026-08-18

### Added

#### Phase 2: Infrastructure & Quality (Parallel Track)
- **Daemon Mode** (S3-06/S3-07): Full executor daemon lifecycle — PID management (`~/.ai-company/daemon.pid`), signal handling (SIGTERM/SIGINT/Windows Ctrl+C), health status file (`logs/executor-daemon.json`), cross-platform stop sentinel, CLI `executor start --daemon` / `executor stop` / `executor status` (980 lines in `src/ai_company/executor/daemon.py`).
- **Background Schedulers**: KPI snapshot scheduler (`dashboard/kpis/scheduler.py`), HITL expiry sweep (`ApprovalGate._sweep_expired_approvals`), governance sweep (`GovernanceScheduler` in `data/governance.py`) — all wired into daemon tick loop.
- **Dashboard Daemon API**: `GET /api/v1/daemon/status` endpoint reading health file → returns `state`, `pid`, `uptime_seconds`, `is_pid_alive`, `stale` flag.
- **WebSocket Daemon Broadcast**: `daemon` topic in `dashboard/ws.py`; `ExecutorDaemon._broadcast_health()` fires after each tick for real-time UI.
- **Daemon Test Suite**: 31 tests across `test_daemon_lifecycle.py`, `test_daemon_detach.py`, `test_scheduler_daemon.py` — all passing.

#### Code Quality
- **mypy strict mode enabled**: ~90 strict-mode errors fixed across 20+ source files:
  - Bare `dict` → `dict[str, Any]` in `message_bus.py` (16), `api.py` (13), `mobile_api.py` (7), `kpi_transformer.py` (3), `briefing.py`, `hr.py`, `scheduler.py` (2)
  - Missing return types (`-> None`) added to `_load_config`/`_save_config`/`_load_events` in `approval.py`, `escalation.py`, `scheduler.py`
  - Untyped `**kwargs` → `**kwargs: Any` in ETL pipelines (`kpi_snapshot.py`, `governance.py`, `orchestration/scheduler.py`)
  - 10 unused `type: ignore` comments removed (`logging.py`, `tool_runner.py`, `embeddings.py`, `daemon.py`, `monitoring.py`, `agent_loop.py`, `app.py`)
  - Generic type args added: `ExtractionResult[Any]`, `TransformResult[Any]`, `ServiceResult[Any]`, `Popen[Any]`
  - `pyproject.toml` updated: `strict = true` (replaces individual `warn_*` flags)

### Changed

- **Version**: 0.5.0 → 0.5.1
- **Agent Registry**: 131 agents
- **Tests**: 1878 passing (3 pre-existing async failures unrelated to changes)
- **Code Quality Gates**: ruff ✅, mypy strict ✅ (180 files), pytest ✅

### Fixed

- **mypy strict**: All 90 strict-mode errors resolved — project now type-checks clean with `strict = true`
- **Release workflow**: Trusted publishing already configured (OIDC, `pypa/gh-action-pypi-publish@release/v1`)

---

## [0.5.0] — 2026-08-13

### Added

#### Product & Business
- **Sprint 9** (2026-08-13): Business architecture & master service catalog; 131-agent positioning (external messaging, strategic brief, agent-facing standards); recurring revenue engine (8 recurring products, conversion framework, enterprise payment terms).
- **Sprint 8** (2026-08-12): Operationalization — inbox purge, README/env setup, Malawi service catalog portfolio (4 new agents, governance blocking, SOPs, client intake CLI, legal package).

#### Security & Architecture
- **Dashboard RBAC** (ADR-012): role-gated write endpoints, loopback-restricted open mode (`src/ai_company/security/rbac.py`).
- **ADR-010** (T1 event-bus alignment): report-only MessageBus perf benchmark extended with write latency and sustained throughput; explicit push-bus adapter trigger.

#### CI / Tooling
- **CI hardening**: version-check job de-flaked (unused setup-uv step dropped); dependabot bumps — `checkout@v7`, `setup-python@v7`, `upload-artifact@v7`, `action-gh-release@v3`, `docker/setup-buildx-action@v4`.

### Changed
- **Storage**: SQLite-first mirror experiment retired (ADR-011 superseded); file-bus + FileStore remain the default.
- **Docs**: workspace artifacts archived (`docs/archive/2026-08-13-workspace-artifacts/`); planning docs (STATUS, TASK-BOARD, BACKLOG, REMAINING-WORK-INVENTORY) reconciled to current reality.
- **Docs**: agent-count reconciliation 127 → 131 — README, STATUS, DEVELOPMENT, USER-GUIDE, ux guides, Sprint 9 architecture, and Malawi service catalog now reference 131 agents; `docs/AGENT-REGISTRY-TABLE.md` is now generated by `AgentGenerator.generate_agent_table()` (wired into `generate_all()`); doc-count drift guard added (`tests/docs/test_doc_agent_counts.py`).

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
