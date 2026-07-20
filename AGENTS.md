# AGENTS.md

## Project Overview

AI Company Builder — a Python tool for creating and orchestrating AI agent hierarchies. Agents are defined in `company-registry.yaml` and generated into OpenCode-compatible markdown files. Features a multi-turn agentic loop (ReAct pattern), audit trail, memory integration, dead-letter queue, KPI dashboards, and 24 CLI commands.

## Repository Structure

- **`ai-company/`** — The active project root (has `pyproject.toml`, `.venv/`, `src/`, `tests/`, `docs/`)
- **`ai-company/src/ai_company/`** — Source code (all modules below)
- **`ai-company/tests/`** — 727 tests (unit + integration), pytest
- **Root `src/ai_company/`** — Legacy/staging area (contains code with syntax errors; do NOT work here)
- **Root files** (`setup_phase6.py`, etc.) — One-time setup scripts, not part of active codebase

## Vision & Roadmap

One human CEO supervises AI executives, managers, and specialists. Goal: automate 70-90% of routine knowledge work (research, drafting, coding, docs, reporting).

**Implementation phases:**
1. ✅ Foundation — Project structure, CLI framework, agent registry, generator
2. ✅ Core Operations — MessageBus, Pydantic models, 24 CLI commands, 727 tests
3. ✅ Audit & Memory — Audit trail package, memory integration, dead-letter queue, circuit breaker
4. 🔲 Security & Gating — 5-tier approval system, HITL non-blocking, file locking, dashboard auth
5. 🔲 Autonomous Coordination — Scheduled cycles, WebSocket broadcast, escalation persistence

## Development

```bash
# From ai-company/ directory
cd ai-company
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"

# Run CLI
ai-company --help
python -m ai_company.cli.main --help

# Run tests (727 total)
pytest

# Lint / typecheck (both clean)
ruff check src/
mypy src/
```

## Key Commands

| Task | Command |
|------|---------|
| Run all tests | `pytest` |
| Run single test file | `pytest tests/unit/test_models.py` |
| Run integration tests | `pytest tests/integration/` |
| Lint | `ruff check src/` |
| Type check | `mypy src/` |
| Generate agents from registry | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| Bootstrap full company | `ai-company company run` |
| Start executor | `ai-company executor start` |
| Run diagnostics | `ai-company doctor run` |

## Architecture

- **Entry point**: `ai_company.cli.main:app` (Typer app, 24 subcommands)
- **Agent hierarchy**: `company-registry.yaml` → Jinja2 templates → `.opencode/agents/*.md`
- **Agentic loop**: `executor/agent_loop.py` — ReAct pattern with multi-turn LLM↔tool interaction, cost tracking, HITL gates
- **Executor**: `executor/loop.py` — Polls inbox.json, processes tasks via AgentLoop, dead-letter queue, memory recall
- **Task system**: `orchestrator/message_bus.py` — JSON-based task queue at `.opencode/inbox.json`
- **Audit trail**: `audit/` — JSONL event logging (tool calls, HITL decisions, task lifecycle)
- **Memory**: `memory/` — 6-type memory store (episodic, semantic, procedural, relational, temporal, aggregate) with executor integration
- **Models**: Pydantic models in `models/` (Company, Executive, Department, Agent, Task, Workflow, Risk, Decision, etc.)
- **Decision engine**: `decision/engine.py` — Approval matrix, risk assessment, decision tree navigation
- **Workflow engine**: `workflow/engine.py` — 9 workflow definitions, step tracking, SLA monitoring
- **Graph engine**: `graph/engine.py` — 4 graph types (org chart, decision, workflow, knowledge) with BFS pathfinding
- **Dashboard**: `dashboard/` — FastAPI REST API, WebSocket, KPI collectors (7 departments), analytics
- **LLM layer**: `llm/` — Multi-provider client (5 providers), cost tracker, circuit breaker, shared JSON parser

## Current State

**Fully working (727 tests, ruff clean, mypy clean):**
- CLI: 24 subcommands (company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator, models, dashboard, executor, doctor, marketing, sales, customer-success, legal, hr, generate, status, sop, raci)
- Executor with multi-turn AgentLoop (ReAct pattern), HITL gates, cost tracking
- Audit trail package (events, writer, reader, integration hooks in executor)
- Memory engine with executor integration (recall context before task execution)
- Dead-letter queue for stale tasks (30-min timeout)
- Circuit breaker for LLM providers
- KPI collectors for all 7 departments (engineering, finance, hr, legal, marketing, sales, customer_success)
- Analytics layer (history tracking, trend analysis, alert rules)
- Dashboard REST API with WebSocket support
- Registry system (4 modules: loader, parser, resolver, validator) loading 19 YAML configs
- 12 Jinja2 templates for agent generation
- BootstrapEngine for full company generation
- DecisionEngine, WorkflowEngine, MemoryEngine, GraphEngine
- 4 SOPs (incident response, deployment, HR onboarding, budget approval) + 3 RACI matrices
- Scheduler integrated into executor loop

**Known gaps (remaining work):**
- Executor bypasses MessageBus for direct file I/O (GAP-001)
- No file locking on shared JSON/YAML state (GAP-002)
- Tier rules not integrated into ToolRunner (GAP-003)
- HITL gate blocks executor thread (GAP-004)
- WebSocket broadcast functions never called (GAP-006)
- Escalation events not persisted (GAP-008)
- Dashboard CORS allows all origins (GAP-010)
- Dashboard API reads files directly (GAP-011)
- Remaining department SOPs needed (marketing, sales, customer-success, legal, operations)
- No integration tests for full end-to-end pipeline

## Conventions

- Python 3.12+
- Line length: 100 (ruff + black)
- Test path: `tests/` with `pythonpath = ["src"]` in pyproject.toml
- Agent IDs: snake_case (e.g., `chief_of_staff`, `lead_backend`)
- Task inbox: `.opencode/inbox.json` (JSON array of Task objects)
- All modules use `logging.getLogger(__name__)` — bare `print()` only in CLI output

## Gotchas

- Root `src/ai_company/cli.py` has syntax errors on lines 41 and 81 — ignore this directory, work in `ai-company/`
- Two `.venv` directories exist (root + `ai-company/`); always use `ai-company/.venv/`
- `tests/unit/test_security.py` has a collection error (missing dependency) — skip with `pytest --ignore=tests/unit/test_security.py`
- `tests/unit/test_ml.py` has a collection error — skip with `pytest --ignore=tests/unit/test_ml.py`
- `src/ai_company/data/kpi_pipeline.py` has ruff errors (missing `json` import) — new file needing fix
- `src/ai_company/services/sales.py` has ruff E741 warnings (ambiguous variable `l`) — new file needing fix
- Windows environment: PowerShell scripts in `ai-company/scripts/`
- Dashboard API uses FastAPI; run with `ai-company dashboard start` or directly via uvicorn
