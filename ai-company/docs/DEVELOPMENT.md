# Development — AI Company Builder

> Local development, testing, and contribution guide for the AI Company Builder.
> For the change lifecycle see [ECL](ECL.md); for deployment see [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md).

## 1 Repository Layout

The active project lives in `ai-company/` at the repository root
(`C:\Users\jmlus\light-speed-holdings` on this machine — never `/workspace/...`).

| Path | Purpose |
|------|---------|
| `ai-company/src/ai_company/` | Package source (CLI, executor, orchestrator, memory, dashboard, ...) |
| `ai-company/tests/` | Unit, integration, e2e, and performance tests |
| `ai-company/company-registry.yaml` | Single source of truth for agents (127 agents, 18 departments) |
| `ai-company/templates/` | Jinja2 templates used by the generator |
| `ai-company/docs/` | Architecture, status, ECL, and planning documents |
| `ai-company/scripts/` | `dev.ps1`, `backup.ps1`, ECL harness scripts |
| `ai-company/.opencode/` | Runtime data: `agents/*.md`, `inbox.json`, `dead_letter.json` |
| `ai-company/harness/` | ECL change tracking (currently inactive) |
| `.opencode/` (repo root) | Legacy parallel agent area (134 `.md` — 127 canonical + 7 legacy duplicates) |

The core workflow is: `company-registry.yaml → Jinja2 template → .opencode/agents/*.md + company/*.yaml`.
See [ARCHITECTURE.md](ARCHITECTURE.md) for the full module hierarchy and data flow.

## 2 Prerequisites

- Python 3.12+ (uv can manage a 3.12 interpreter via `.python-version`)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- Git
- At least one LLM provider API key (`OPENCODE`, `DEEPSEEK`, `OPENAI`, `ANTHROPIC`, `GEMINI`, or `KIMI`).
  Ollama works locally without a key (`http://localhost:11434`).

## 3 Quick Start

PowerShell (recommended on Windows):

```powershell
cd ai-company
.\scripts\dev.ps1           # Full onboarding: venv, deps, lint, tests, agents
.\scripts\dev.ps1 setup     # venv + deps + pre-commit + agent generation
.\scripts\dev.ps1 test      # Run test suite (with coverage)
.\scripts\dev.ps1 lint      # ruff check + format check + mypy
.\scripts\dev.ps1 status    # Show project status
.\scripts\dev.ps1 generate  # Regenerate agents from company-registry.yaml
.\scripts\dev.ps1 clean     # Remove build/cache artifacts
```

Manual setup (bash):

```bash
cd ai-company
uv sync --extra dev            # install project + dev deps (respects uv.lock)
pre-commit install             # enable git hooks (ruff, mypy, bandit, ...)
uv run ai-company --help       # CLI entry point
```

## 4 Common Commands

```bash
uv run pytest                                  # Full test suite (1494 tests collected, 53 skipped)
uv run pytest tests/unit/test_models.py        # Single test file
uv run pytest -k "postmortem"                  # Pattern match
uv run ruff check src/ tests/                  # Lint
uv run ruff format src/ tests/                 # Format (check with --check)
uv run mypy src/ --ignore-missing-imports      # Type check (177 source files)
uv run pre-commit run --all-files              # Run all pre-commit hooks

# Regenerate agent markdown files from the registry
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"

# CLI
uv run ai-company --help
uv run ai-company doctor run           # System diagnostics
uv run ai-company agents list          # List generated agents
uv run ai-company company run          # Bootstrap the full company
uv run ai-company executor start       # Start the autonomous executor
uv run ai-company dashboard kpi list   # View KPIs
```

## 5 Verification Gates

| Change Type | Minimum Verification |
|-------------|----------------------|
| Generator / template | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| CLI commands | `ai-company --help` + `ai-company <command> --help` |
| Models / orchestrator | `pytest` |
| Any source change | `ruff check src/ && mypy src/ && pytest` |
| Harness / docs | `pwsh scripts/lint-ecl.ps1` |

## 6 ECL Change Lifecycle

Changes that span more than two files, touch APIs/data models/architecture, need user confirmation, or are likely to exceed 20 minutes should be tracked as an ECL change. Small local fixes can skip it.

```text
new -> active/in_progress
active -> close completed|abandoned|blocked -> archive/YYYY-MM-DD-slug
active -> park -> parking/YYYY-MM-DD-slug -> resume -> active
```

```powershell
.\scripts\harness-change.ps1 new "Title"     # Create a change
.\scripts\harness-change.ps1 status          # Show active change
.\scripts\harness-change.ps1 close completed # Archive + rebuild INDEX
.\scripts\harness-change.ps1 park            # Park active change
.\scripts\harness-evolve.ps1 check           # Check auto-evolve threshold
.\scripts\lint-ecl.ps1                       # Validate ECL structure
```

Rules: only one active change at a time; never hand-edit `harness/changes/INDEX.json`; active change files override `docs/STATUS.md` for the current task. See [ECL.md](ECL.md) for the full manual.

## 7 Documentation Map

| Document | Purpose |
|----------|---------|
| `docs/ARCHITECTURE.md` | Module hierarchy, naming conventions, data flow |
| `docs/ARCHITECTURE-GAPS.md` | 20-gap register with per-gap status and evidence |
| `docs/STATUS.md` | Current state and recent work |
| `docs/ECL.md` | Change lifecycle manual |
| `docs/DEPLOYMENT-GUIDE.md` | Docker, production, CI/CD, security |
| `docs/DEVELOPER-GUIDE.md` | Additional onboarding notes |
| `docs/PRODUCT-ROADMAP.md` | Phase and sprint roadmap |
| `docs/BACKLOG.md` | Backlog (48 items, MoSCoW) |
| `docs/API-REFERENCE.md` | API reference |

## 8 Backups

```powershell
cd ai-company
.\scripts\backup.ps1                  # Backup .opencode/, company/, results/
.\scripts\backup.ps1 -KeepCount 14    # Keep 14 days of backups
```

## 9 Staging

```bash
docker compose -f docker-compose.staging.yml up --build              # Staging dashboard
docker compose -f docker-compose.staging.yml --profile worker up     # + worker
docker compose -f docker-compose.staging.yml --profile monitoring up # + Prometheus
```

Staging dashboard: host port **8421** → container **8420** (production: 8420). See [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md) for the full deployment reference.

## 10 Notes

- Registry IDs use underscores (`financial_analyst`); generated filenames and config references use hyphens (`financial-analyst`). Run `ai-company validate` to check config references resolve to generated agent files.
- `.opencode/inbox.json` is the task queue. Test runs may inject synthetic tasks — treat `marketing-service`-style entries as pollution when inspecting the queue.
- Do not hand-edit generated files in `.opencode/agents/`; regenerate from `company-registry.yaml`.
- `harness/changes/INDEX.json` is script-generated only.
