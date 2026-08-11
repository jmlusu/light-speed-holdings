# Developer Guide — AI Company Builder

> Quick start, architecture overview, and contribution guidelines for new contributors.

---

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- Git
- Windows, macOS, or Linux

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd light-speed-holdings

# Create the virtual environment and install project + dev deps from uv.lock
uv sync --extra dev

# Verify installation
uv run ai-company --help
uv run pytest
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
| CLI | `src/ai_company/cli/` | 30 Typer subcommands (5 root + 25 lazy) |
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
| `src/ai_company/cli/main.py` | CLI entry point — all 30 subcommands registered here (5 root + 25 lazy sub-apps) |
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
- Windows environment: use PowerShell scripts in `scripts/`

---

## OAuth2 Authentication

OAuth2 client-credentials auth for enterprise LLM providers is implemented in `src/ai_company/llm/oauth2.py`.

### Components

| File | Responsibility |
|------|---------------|
| `src/ai_company/llm/oauth2.py` | `OAuth2TokenManager` — fetches, caches, and refreshes tokens |
| `src/ai_company/llm/oauth2.py` | `OAuth2Config` (frozen dataclass) — token URL, env-var credential refs, TTL |
| `src/ai_company/llm/oauth2.py` | `OAuth2Error` — subclass of `LLMProviderError` for fail-closed routing |
| `src/ai_company/llm/providers/openai_compatible.py` | Wired into `OpenAICompatibleProvider` — per-request bearer token |
| `src/ai_company/llm/client.py` | `LLMClient._init_providers()` — opt-in via `oauth2:` block in `company/models.yaml` |

### Configuration

Providers without an `oauth2:` block use static `{ID}_API_KEY` bearer auth. With the block, credentials are resolved from environment variables at request time.

### Security

- Tokens cached in memory only — never persisted to disk.
- 60-second safety margin before expiry triggers proactive refresh.
- Fail-closed: missing credentials or endpoint failure raises `OAuth2Error`, causing the router to skip to the next provider.

### Tests

`tests/unit/test_oauth2.py` (11 tests) covers token caching, refresh timing, fail-closed behavior, and env-var resolution.

---

## ML Module

ML capabilities live in `src/ai_company/ml/` (6 submodules). All use numpy for computation and fall back gracefully when heavyweight dependencies are unavailable.

### Submodules

| File | Class | Purpose |
|------|-------|---------|
| `embeddings.py` | `EmbeddingEngine` | Local sentence-transformer embeddings; lazy load, graceful ImportError fallback |
| `performance.py` | `AgentPerformanceTracker` | Per-agent metrics (success rate, execution time, cost, tokens); simple regression model for time prediction |
| `complexity.py` | `TaskComplexityScorer` | Heuristic scoring (0.0–1.0) to route tasks to the right LLM tier |
| `prompt_optimizer.py` | `PromptOptimizer` | Analyze audit logs for prompt patterns, A/B test variants, suggest improvements |
| `anomaly.py` | `AnomalyDetector` | Statistical anomaly detection (Z-score, IQR) on cost/time/error metrics |
| `predictive_scaling.py` | `PredictiveScalingEngine` | Forecast task volume and recommend tier adjustments |

### Usage

```python
from ai_company.ml import EmbeddingEngine, TaskComplexityScorer

engine = EmbeddingEngine()
embeddings = engine.encode(["task description", "another task"])

scorer = TaskComplexityScorer()
score = scorer.score("Design a microservice architecture with Kubernetes")  # 0.0–1.0
```

### Tests

Tests are in `tests/unit/test_ml.py`. The embedding test is skipped when the HuggingFace model cannot be downloaded.

---

## Security Module

Security modules live in `src/ai_company/security/` (6 submodules plus key management).

### Submodules

| File | Class/Function | Purpose |
|------|---------------|---------|
| `secrets_scanner.py` | `SecretsScanner` | Scans code for leaked API keys, passwords, private keys, connection strings |
| `pii_detector.py` | `PIIDetector` | Detects and masks PII (emails, SSN, credit cards, API keys, phone numbers, IPs) |
| `content_filter.py` | `ContentFilter` | Filters prompt injection, harmful content, code execution attempts, XSS |
| `keys.py` | `APIKeyManager` | API key rotation with overlap period, fail-closed, audit logging |
| `encryption_key_manager.py` | `EncryptionKeyManager` | AES-256 key derivation (HKDF-SHA256) from master secret, dual-key rotation |
| `memory_encryption.py` | encrypt/decrypt/is_encrypted | AES-256-GCM with unique nonces per entry; `ENC:` prefix format |
| `migrate_memory_encrypt.py` | migration utility | Backfill encryption for existing memory entries |

### Usage

```python
from ai_company.security import ContentFilter, PIIDetector

filter = ContentFilter()
result = filter.filter("Sensitive user data: john@example.com")

detector = PIIDetector()
masked = detector.mask("Contact: ssn 123-45-6789")  # "Contact: ssn XXX-XX-XXXX"
```

### Security

- Secrets scanner runs as a CLI tool and pre-commit hook.
- Master secret is read from `MEMORY_ENCRYPTION_KEY` env var (fallback: `JWT_SECRET_KEY`).
- Raw keys are encrypted with secondary HKDF derivation before disk write.

---

## Structured Logging

Structured JSON logging with correlation IDs is configured in `src/ai_company/logging_config.py` (resolved GAP-018).

### Components

| File | Responsibility |
|------|---------------|
| `logging_config.py` | `JSONFormatter`, `HumanFormatter`, `setup_logging()`, `get_logger()` |
| `utils/logging.py` | Shared `ContextVar` correlation ID (`get_correlation_id`, `set_correlation_id`, `new_correlation_id`) |
| `executor/loop.py:292` | `set_correlation_id(task.id)` per task execution |

### Configuration

```python
from ai_company.logging_config import setup_logging, get_logger

# Auto-detects JSON vs human format (JSON in non-TTY/CI, human in terminal)
setup_logging(level="INFO")
logger = get_logger(__name__)

# Or force JSON mode
setup_logging(level="DEBUG", json_mode=True, log_file="logs/app.jsonl")
```

Environment variables:
- `AI_COMPANY_LOG_JSON=1/0` — force JSON or human mode.
- `AI_COMPANY_LOG_LEVEL=DEBUG/INFO/WARNING/ERROR` — level override.

### Output Format

JSON mode emits one JSON object per log line with fields: `ts`, `level`, `logger`, `message`, `correlation_id`, plus any `extra={}` fields attached by the caller.

### Tests

`tests/unit/test_logging.py` (15 tests) covers JSON formatting, human formatting, correlation ID propagation, and env-var configuration.

---

## Getting Help

- **Architecture docs**: `docs/ARCHITECTURE.md`
- **Gap analysis**: `docs/ARCHITECTURE-GAPS.md`
- **Current status**: `docs/STATUS.md`
- **Sprint backlog**: `docs/SPRINT-2-BACKLOG.md`
- **Risk register**: `docs/RISK-REGISTER.md`
