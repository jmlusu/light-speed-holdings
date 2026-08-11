# Contributing to AI Company Builder

## Development Setup

```bash
cd ai-company
uv sync --extra dev            # Creates .venv and installs project + dev deps from uv.lock
```

## Code Style

- **Python:** 3.12+ syntax
- **Line length:** 100 characters
- **Formatter:** `uv run ruff format src/`
- **Linter:** `uv run ruff check src/`
- **Type checker:** `uv run mypy src/`

## Before Submitting

Run the full verification suite:

```bash
uv run ruff check src/                # Lint
uv run ruff format --check src/       # Format check
uv run mypy src/                      # Type check
uv run pytest                         # All tests
```

All checks must pass before merging.

## Project Structure

```
src/ai_company/
├── cli/            # Typer CLI commands (one file per domain)
├── models/         # Pydantic domain models
├── registry/       # YAML config → typed models
├── orchestrator/   # Scheduler, escalation, approval, briefing
├── executor/       # LLM-based task execution
├── decision/       # Approval matrix, risk, decision trees
├── workflow/       # Workflow definitions and engine
├── memory/         # 6-type memory store
├── graph/          # Org chart, decision, workflow, knowledge graphs
├── llm/            # Multi-provider LLM client
├── dashboard/      # FastAPI REST API
├── builder.py      # Bootstrap engine
├── generator.py    # Agent file generator
└── model_router.py # 3-tier cost-aware routing
```

## Adding a New CLI Command

1. Create `src/ai_company/cli/your_module.py`
2. Define `app = typer.Typer(help="...")`
3. Add commands with `@app.command()`
4. Register in `cli/main.py`: `app.add_typer(your_app, name="your-module")`
5. Add tests in `tests/unit/test_your_module.py`

## Adding a New Model

1. Add to `src/ai_company/models/models.py`
2. Export from `src/ai_company/models/__init__.py`
3. Add tests in `tests/unit/test_models.py`

## Testing

```bash
pytest                         # All tests
pytest tests/unit/test_models.py  # Single file
pytest -k "test_name"          # By name pattern
pytest -v                      # Verbose output
```

Tests use `pytest` with `tmp_path` fixtures for file-based tests. Mock external services (LLM APIs) — never call real APIs in tests.

## Commit Messages

Use conventional commits:

- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `test: add tests`
- `refactor: restructure code`
- `chore: maintenance tasks`

## Reporting Issues

Open an issue with:
1. Description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details (OS, Python version)
