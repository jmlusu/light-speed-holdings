# Developer Guide — AI Company Builder

> Quick start, architecture overview, and contribution guidelines for new contributors.

---

## Quick Start

### Prerequisites

- Python 3.12+
- Git
- Windows, macOS, or Linux

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd light-speed-holdings

# Navigate to the active project
cd ai-company

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install in development mode
pip install -e ".[dev]"

# Verify installation
ai-company --help
pytest
```

### First Run

```bash
# Bootstrap the full company from registry
ai-company company run

# Check system health
ai-company doctor run

# List all agents
ai-company agents list

# Start the autonomous executor
ai-company executor start
```

---

## Architecture Overview

### What It Does

AI Company Builder generates and runs a virtual AI company. One human CEO supervises AI executives, managers, and specialists. The system:

1. **Defines agents** in `company-registry.yaml` (19 YAML config files)
2. **Generates agent files** using Jinja2 templates → `.opencode/agents/*.md`
3. **Executes tasks** through a multi-turn agentic loop (ReAct pattern)
4. **Tracks everything** with audit trails, memory, and cost tracking

### Core Workflow

```
company-registry.yaml
    │
    ▼
Registry (loader → parser → resolver → validator)
    │
    ▼
CompanyRegistry (typed Pydantic models)
    │
    ├──► BootstrapEngine → .opencode/agents/*.md + configs
    │
    └──► Executor (polls inbox.json)
            │
            ├──► AgentLoop (ReAct: LLM ↔ tools, max 10 iterations)
            │       ├──► LLMClient (5 providers, cost tracking)
            │       ├──► ToolRunner (sandboxed execution, HITL gates)
            │       └──► CostTracker (budget enforcement)
            │
            ├──► MemoryEngine (recall context before tasks)
            ├──► DeadLetterQueue (stale task recovery)
            └──► AuditWriter (JSONL event logging)
```

### Module Map

| Module | Path | Purpose |
|--------|------|---------|
| CLI | `src/ai_company/cli/` | 24 Typer subcommands |
| Executor | `src/ai_company/executor/` | Task execution pipeline |
| LLM | `src/ai_company/llm/` | Multi-provider LLM client |
| Orchestrator | `src/ai_company/orchestrator/` | Message bus, approvals, scheduling |
| Models | `src/ai_company/models/` | 17+ Pydantic domain models |
| Registry | `src/ai_company/registry/` | YAML config loading and validation |
| Builder | `src/ai_company/builder/` | Full company generation |
| Decision | `src/ai_company/decision/` | Approval matrix, risk assessment |
| Workflow | `src/ai_company/workflow/` | 9 workflow definitions, SLA tracking |
| Memory | `src/ai_company/memory/` | 6-type memory store |
| Graph | `src/ai_company/graph/` | 4 graph types, BFS pathfinding |
| Audit | `src/ai_company/audit/` | JSONL audit trail |
| Dashboard | `src/ai_company/dashboard/` | FastAPI REST API, KPIs, analytics |

---

## Code Conventions

### Python Style

- **Version**: Python 3.12+ (use `type` union syntax `X | Y`, not `Optional[X]`)
- **Line length**: 100 characters (enforced by ruff)
- **Formatter**: ruff (replaces black)
- **Linter**: ruff
- **Type checker**: mypy

### Code Patterns

```python
# Imports: stdlib → third-party → local
from __future__ import annotations

import json
import logging
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from ai_company.models.task import Task

# Module-level logger
logger = logging.getLogger(__name__)

# Pydantic models with ConfigDict
class EntityBase(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(..., min_length=1)
    name: str = Field(default="")

# Type hints on all public functions
def process_task(task: Task) -> dict[str, Any]:
    """Process a single task through the agentic loop."""
    ...
```

### File Naming

- **Modules**: `snake_case.py`
- **Tests**: `test_<module>.py`
- **Templates**: `<type>.md.j2`
- **Configs**: `<name>.yaml` in `company/` directory

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_models.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_models.py::test_company_creation -v

# Skip the broken security test
pytest --ignore=tests/unit/test_security.py
```

- All new functions must have unit tests
- Test file mirrors source file: `executor/loop.py` → `tests/unit/test_executor.py`
- Use `tmp_path` fixture for file system tests
- Mock external services (LLM providers) in unit tests

---

## Development Workflow

### Making Changes

1. **Create a branch**: `git checkout -b feature/my-feature`
2. **Write tests first** (TDD encouraged): Add test in `tests/unit/`
3. **Implement the change**: In `src/ai_company/`
4. **Verify**: `ruff check src/ && mypy src/ && pytest`
5. **Commit**: Descriptive message following conventional commits
6. **Push and create PR**

### Verification Checklist

| Change Type | Minimum Verification |
|-------------|----------------------|
| Any source change | `ruff check src/ && mypy src/ && pytest` |
| CLI commands | `ai-company --help` + `ai-company <command> --help` |
| Generator / template | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| Models / orchestrator | `pytest tests/unit/test_models.py tests/unit/test_orchestrator.py` |
| Dashboard | `pytest tests/unit/test_dashboard.py` |

### Commit Messages

Follow conventional commits:
```
feat: add file locking to MessageBus
fix: resolve race condition in inbox writes
test: add unit tests for DeadLetterQueue
docs: update architecture gaps status
refactor: extract parse_llm_json to shared utility
```

---

## Key Files to Know

| File | Why It Matters |
|------|----------------|
| `src/ai_company/cli/main.py` | CLI entry point — all 24 subcommands registered here |
| `src/ai_company/executor/loop.py` | Core execution loop — reads inbox, runs AgentLoop, manages lifecycle |
| `src/ai_company/executor/agent_loop.py` | ReAct pattern — multi-turn LLM↔tool interaction |
| `src/ai_company/models/models.py` | All 17+ Pydantic domain models |
| `src/ai_company/registry/__init__.py` | Registry loading entry point |
| `src/ai_company/llm/client.py` | Multi-provider LLM client |
| `src/ai_company/orchestrator/message_bus.py` | Task queue (JSON-based) |
| `src/ai_company/audit/integration.py` | Audit hooks for executor |
| `company-registry.yaml` | Agent definitions (single source of truth) |

---

## Common Tasks

### Adding a New CLI Command

1. Create `src/ai_company/cli/my_command.py`:
```python
import typer

app = typer.Typer(help="My new command")

@app.command()
def do_something(name: str) -> None:
    """Do something useful."""
    typer.echo(f"Doing something with {name}")
```

2. Register in `src/ai_company/cli/main.py`:
```python
from ai_company.cli.my_command import app as my_command_app
app.add_typer(my_command_app, name="my-command", help="My new command")
```

3. Add tests in `tests/unit/test_my_command.py`

### Adding a New Model

1. Add to `src/ai_company/models/models.py`:
```python
class MyModel(EntityBase):
    """Description of what this model represents."""
    field: str = Field(default="", description="Field description")
    count: int = Field(default=0, ge=0)
```

2. Export from `src/ai_company/models/__init__.py`
3. Add tests in `tests/unit/test_models.py`

### Adding a New Audit Event

1. Add event type to `AuditEventType` enum in `audit/events.py`
2. Add logging function in `audit/integration.py`
3. Call from the appropriate executor/orchestrator hook
4. Add tests in `tests/unit/test_audit.py`

---

## Known Issues

- `tests/unit/test_security.py` has a collection error (missing dependency) — skip with `--ignore`
- Root `src/ai_company/cli.py` has syntax errors — work in `ai-company/` directory only
- Two `.venv` directories exist — always use `ai-company/.venv/`
- Windows environment: use PowerShell scripts in `ai-company/scripts/`

---

## Getting Help

- **Architecture docs**: `docs/ARCHITECTURE.md`
- **Gap analysis**: `docs/ARCHITECTURE-GAPS.md`
- **Current status**: `docs/STATUS.md`
- **Sprint backlog**: `docs/SPRINT-2-BACKLOG.md`
- **Risk register**: `docs/RISK-REGISTER.md`
