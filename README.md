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

**727 tests passing.** Ruff lint clean. Mypy type-check clean.

### Known Gaps

- Executor bypasses MessageBus for direct file I/O
- No file locking on shared JSON/YAML state
- Tier rules not integrated into ToolRunner
- HITL gate blocks executor thread (up to 30 min per approval)
- WebSocket broadcast functions exist but are not called
- Dashboard CORS allows all origins (no auth)

See `docs/ARCHITECTURE-GAPS.md` for the full gap analysis.

## Quick Start

```bash
cd ai-company
python -m venv .venv
.venv\Scripts\activate        # Windows (or: source .venv/bin/activate on Linux/Mac)
pip install -e ".[dev]"

# Verify
ai-company --help
pytest
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
# Install dev dependencies
pip install -e ".[dev]"

# Run all 727 tests
pytest

# Lint and type check
ruff check src/
mypy src/

# Regenerate agent files from registry
python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
```

## Project Structure

- `ai-company/` — Active project (pyproject.toml, .venv/, src/, tests/, docs/)
- `src/ai_company/` — Legacy staging area (ignore; has syntax errors)
- Root files (`setup_phase6.py`, etc.) — One-time setup scripts, not part of active codebase

## Documentation

- `docs/ARCHITECTURE.md` — System architecture and module hierarchy
- `docs/ARCHITECTURE-GAPS.md` — 20 identified integration gaps with severity ratings
- `docs/STATUS.md` — Current project status
- `docs/INTEGRATION-ARCHITECTURE.md` — Integration seam analysis
- `docs/SPRINT-1-TRACKER.md` — Sprint 1 task tracker
- `docs/SPRINT-2-BACKLOG.md` — Sprint 2 prioritized backlog
- `docs/DEVELOPER-GUIDE.md` — Developer onboarding guide
- `docs/COMPANY-CONSTITUTION.md` — Principles and decision order
- `docs/DECISION-FRAMEWORK.md` — Decision engine rules
- `docs/MODEL-ROUTING-POLICY.md` — Provider catalog and routing rules
- `docs/RISK-REGISTER.md` — Risk register with mitigations and owners
- `docs/BOARD-GOVERNANCE.md` — Board charter and voting rules

## License

Internal project — Light Speed Holdings.
