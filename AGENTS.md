# AGENTS.md

## Project Overview

AI Company Builder — a Python tool for creating and orchestrating AI agent hierarchies. Agents are defined in `company-registry.yaml` and generated into OpenCode-compatible markdown files.

## Repository Structure

- **`ai-company/`** — The actual project (has `pyproject.toml`, `.venv/`, `src/`, `tests/`)
- **`src/ai_company/`** — Legacy/staging area (contains code with syntax errors; not the active project)
- **Root files** (`setup_phase6.py`, etc.) — One-time setup scripts, not part of active codebase

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

# Run tests
pytest

# Lint / format / typecheck
ruff check src/
black src/
mypy src/
```

## Key Commands

| Task | Command |
|------|---------|
| Run all tests | `pytest` |
| Run single test file | `pytest tests/unit/test_models.py` |
| Lint | `ruff check src/` |
| Format | `black src/` |
| Type check | `mypy src/` |
| Generate agents from registry | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |

## Architecture

- **Entry point**: `ai_company.cli.main:app` (Typer app)
- **Agent hierarchy**: Defined in `company-registry.yaml` → generated to `.opencode/agents/` via Jinja2 templates
- **Task system**: `ai_company.orchestrator.message_bus` — JSON-based task queue at `.opencode/inbox.json`
- **Models**: Pydantic models in `ai_company/models/` (Executive, Specialist, Department, Company, etc.)

## Conventions

- Python 3.12+
- Line length: 100 (ruff + black)
- Test path: `tests/` with `pythonpath = ["src"]` in pyproject.toml
- Agent IDs: snake_case (e.g., `chief_of_staff`, `lead_backend`)
- Task inbox: `.opencode/inbox.json` (JSON array of Task objects)

## Gotchas

- Root `src/ai_company/cli.py` has syntax errors on lines 41 and 81 — ignore this directory, work in `ai-company/`
- Two `.venv` directories exist (root + `ai-company/`); always use `ai-company/.venv/`
- No CI pipeline configured — manual verification only
- Windows environment: PowerShell scripts in `ai-company/scripts/`
