# Contributing to AI Company Builder

## Development Setup

```bash
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

## Documentation Drift Prevention

Factual claims in documentation (agent counts, department counts, KPI counts, etc.) are
validated against source-of-truth files on every commit. If your change affects any
source-of-truth file, you must update all dependent documentation.

### Source of Truth

| Claim | Source File | Current Value |
|-------|-------------|---------------|
| Department count | `company-registry.yaml` | 20 |
| Agent count | `company-registry.yaml` | 144 |
| KPI count | `company/config/kpis.yaml` | 25 |
| Template count | `templates/**/*.j2` | 9 |
| LLM providers | `company/models.yaml` | 9 |

The canonical manifest is at `docs/source-of-truth.yaml`.

### How It Works

1. **Pre-commit hook** runs `scripts/validate-drift.ps1` on every commit
2. If drift is detected, the commit is blocked
3. Fix the stale documentation before committing

### When to Update Docs

If your PR changes:
- `company/departments.yaml` → update all "X departments" references in docs
- `company-registry.yaml` → update all "X agents" references in docs
- `company/config/kpis.yaml` → update KPI count references
- `templates/` → update template count references
- `company/models.yaml` → update provider count references

### Ownership

| Area | Owner | Responsibility |
|------|-------|----------------|
| `company-registry.yaml` | CEO / Chief of Staff | Canonical agent definitions |
| `company/departments.yaml` | CEO / Chief of Staff | Canonical department list |
| `docs/source-of-truth.yaml` | Knowledge Manager | Manifest accuracy |
| `scripts/validate-drift.ps1` | DevOps Lead | Script maintenance |
| `tests/docs/test_doc_drift.py` | QA Lead | Test maintenance |
| Active docs (`docs/*.md`, `README.md`) | Technical Documentation Lead | Content accuracy |
| Archived docs (`docs/archive/`) | N/A | Historical records — do not update |

### Running Validation Manually

```powershell
.\scripts\validate-drift.ps1           # PowerShell
uv run pytest tests/docs/test_doc_drift.py -v  # pytest
```

## Reporting Issues

Open an issue with:
1. Description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details (OS, Python version)
