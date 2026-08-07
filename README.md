# AI Company Builder

> Orchestrate AI agent hierarchies — one human CEO supervises AI executives, managers, and specialists.

## What It Does

AI Company Builder generates and runs a virtual AI company from YAML configuration files. Define your agents in `company-registry.yaml`, and the system generates OpenCode-compatible agent markdown files, then executes tasks through a multi-turn agentic loop (ReAct pattern) with human-in-the-loop gates, audit trails, and cost tracking.

**Core workflow:**
```
company-registry.yaml → Jinja2 templates → .opencode/agents/*.md + task execution
```

## Current Status

| Component | Status | Tests |
|-----------|--------|-------|
| CLI (24 subcommands) | Working | Covered |
| Multi-turn agent loop (ReAct) | Working | Covered |
| Audit trail (JSONL logging) | Working | Covered |
| Memory engine (6 types) | Working | Covered |
| Dead-letter queue | Working | Covered |
| KPI dashboard (7 departments) | Working | Covered |
| Dashboard REST API + WebSocket | Working | Covered |
| Circuit breaker (LLM providers) | Working | Covered |
| Registry system (19 YAML configs) | Working | Covered |
| Decision/Workflow/Graph engines | Working | Covered |

**1528 tests passing.** Ruff lint clean. Mypy type-check clean (177 source files).

### Known Gaps

Current open gaps (see the [gap register](ai-company/docs/ARCHITECTURE-GAPS.md) for evidence and status):

- GAP-019 — agent spec parsing lacks schema validation (open)

**Resolved:** GAP-001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 016, 017, 018, 020 (19 of 20).

See `ai-company/docs/ARCHITECTURE-GAPS.md` for the full gap analysis.

## Quick Start

```bash
cd ai-company
uv sync --extra dev

# Verify
uv run ai-company --help
uv run pytest
```

## Usage

```bash
# Bootstrap the full company from registry
ai-company company run

# Start the autonomous executor
ai-company executor start

# Run system diagnostics
ai-company doctor run

# View KPIs
ai-company dashboard kpi list

# Manage agents
ai-company agents list

# Run a specific workflow
ai-company workflows run <workflow-id>

# View SOPs and RACI matrices
ai-company sop
ai-company raci
```

## Architecture

```
ai-company/src/ai_company/
├── cli/               # 24 Typer CLI subcommands
├── executor/          # Agentic loop, tool runner, HITL gates, dead-letter queue
├── llm/               # Multi-provider LLM client, cost tracker, circuit breaker
├── orchestrator/      # Message bus, approval, scheduler, escalation, briefing
├── models/            # 17+ Pydantic domain models
├── registry/          # YAML config loader, parser, resolver, validator
├── builder/           # BootstrapEngine — full company generation
├── decision/          # Decision engine — approvals, risk assessment, trees
├── workflow/          # Workflow engine — step tracking, SLA monitoring
├── memory/            # 6-type memory store with executor integration
├── graph/             # 4 graph types with BFS pathfinding
├── audit/             # JSONL audit trail (events, writer, reader)
├── dashboard/         # FastAPI REST API, WebSocket, KPI collectors, analytics
├── doctor/            # System diagnostics
└── generator.py       # Agent .md file generation from templates
```

## Development

```bash
# Install dev dependencies (creates .venv from uv.lock)
uv sync --extra dev

# Run the full test suite (1494 tests)
uv run pytest

# Lint and type check
uv run ruff check src/
uv run mypy src/

# Regenerate agent files from registry
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
```

## Project Structure

- `ai-company/` — Active project (pyproject.toml, .venv/, src/, tests/, docs/)
- `src/ai_company/` — Legacy staging area (ignore; has syntax errors)
- Root files (`setup_phase6.py`, etc.) — One-time setup scripts, not part of active codebase

## Documentation

All documentation lives in `ai-company/docs/`:

- `ai-company/docs/ARCHITECTURE.md` — System architecture and module hierarchy
- `ai-company/docs/ARCHITECTURE-GAPS.md` — 20 identified integration gaps with severity ratings
- `ai-company/docs/STATUS.md` — Current project status
- `ai-company/docs/DEVELOPMENT.md` — Developer setup and local development guide
- `ai-company/docs/DEVELOPER-GUIDE.md` — Developer onboarding guide
- `ai-company/docs/ECL.md` — Change lifecycle and context loading rules
- `ai-company/docs/DEPLOYMENT-GUIDE.md` — Deployment reference
- `ai-company/docs/INTEGRATION-ARCHITECTURE.md` — Integration seam analysis
- `ai-company/docs/SPRINT-1-TRACKER.md` — Sprint 1 task tracker
- `ai-company/docs/SPRINT-2-BACKLOG.md` — Sprint 2 prioritized backlog
- `ai-company/docs/COMPANY-CONSTITUTION.md` — Principles and decision order
- `ai-company/docs/DECISION-FRAMEWORK.md` — Decision engine rules
- `ai-company/docs/MODEL-ROUTING-POLICY.md` — Provider catalog and routing rules
- `ai-company/docs/RISK-REGISTER.md` — Risk register with mitigations and owners
- `ai-company/docs/BOARD-GOVERNANCE.md` — Board charter and voting rules

## License

Internal project — Light Speed Holdings.
