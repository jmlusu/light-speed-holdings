# AI Company Builder — Agent Guide

## Project Location

This project's actual filesystem root is `C:\Users\jmlus\light-speed-holdings`, NOT `/workspace/...` or any other container-style path. Always use this Windows path.

## 1 Project Snapshot

- **What it is**: Python CLI tool for creating and orchestrating AI agent hierarchies. Agents are defined in `company-registry.yaml` and generated into OpenCode-compatible markdown files.
- **Core workflow**: Registry YAML → Jinja2 template → `.opencode/agents/*.md` + `company/*.yaml`
- **Runtime shape**: Python 3.12+ CLI (Typer), no web server. Packages via setuptools, environments managed with uv.
- **Start here**: [Architecture](docs/ARCHITECTURE.md), [Development](docs/DEVELOPMENT.md), [ECL](docs/ECL.md)

## 2 Core Workflow / Domain Model

| Concept | Source | What Agents Need To Know |
|---------|--------|--------------------------|
| Agent Registry | `company-registry.yaml` | Single source of truth for all agents (id, name, tools, permissions) |
| Generator | `src/ai_company/generator.py` | Reads registry, renders Jinja2 template, writes `.opencode/agents/*.md` |
| Agent Template | `templates/agents/agent.md.j2` | OpenCode-native format with `mode: subagent` + `permission:` blocks |
| CLI Entry | `src/ai_company/cli/main.py` | Typer app, 30 subcommands registered here |
| Task System | `src/ai_company/orchestrator/message_bus.py` | JSON-based task queue at `.opencode/inbox.json` |
| Domain Models | `src/ai_company/models/models.py` | Pydantic models: Executive, Specialist, Department, Company |

## 3 Where To Work

| Section | Document | Description |
|---------|----------|-------------|
| 3.1 | [System Architecture](docs/ARCHITECTURE.md) | Module hierarchy, data flow, key files |
| 3.2 | [ECL](docs/ECL.md) | Change lifecycle, context loading, harness workflow |
| 3.3 | [Status](docs/STATUS.md) | Recent handoff, current state |

## 4 Context Loading

1. Read this file.
2. Read [ECL](docs/ECL.md) for change lifecycle and context rules.
3. If `harness/changes/active/summary.md` exists, read active change files before any task-specific docs.
4. If no active change exists and `harness/evolution/pending.md` exists, read it before `docs/STATUS.md`.
5. If no active change exists and no pending evolution exists, read [Status](docs/STATUS.md).
6. Read the relevant source files for the task.

## 5 Development Commands

### Quick Start (New Developers)

```powershell
.\scripts\dev.ps1           # Full onboarding: venv, deps, lint, tests, agents
.\scripts\dev.ps1 status    # Show project status
.\scripts\dev.ps1 test      # Run test suite
.\scripts\dev.ps1 lint      # Run linter + type checker
```

### Manual Setup

```bash
uv sync --extra dev            # Install project + dev deps (creates .venv, respects uv.lock)
pre-commit install           # Enable git hooks (ruff, mypy, bandit, etc.)
ai-company --help            # CLI entry point (uv run ai-company --help if venv not activated)
uv run ruff check src/       # Lint
uv run mypy src/             # Type check
uv run pytest                # Tests
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"  # Regenerate agents
```

### Pre-commit Hooks

Hooks run automatically on `git commit`. To run manually:

```bash
pre-commit run --all-files    # Run all hooks
pre-commit run ruff           # Run just ruff
pre-commit run mypy           # Run just mypy
pre-commit run bandit         # Run just bandit
```

Installed hooks: trailing-whitespace, end-of-file-fixer, check-yaml, ruff (lint+format), mypy, bandit (security).

### Disaster Recovery

```powershell
.\scripts\backup.ps1                  # Backup .opencode/, company/, results/
.\scripts\backup.ps1 -KeepCount 14    # Keep 14 days of backups
```

### Staging Environment

```bash
docker compose -f docker-compose.staging.yml up --build       # Start staging
docker compose -f docker-compose.staging.yml --profile worker up   # With worker
docker compose -f docker-compose.staging.yml --profile monitoring up  # With Prometheus
```

Staging dashboard runs on host port **8421** (maps to container 8420; production: 8420).

## 6 Verification

| Change Type | Minimum Verification |
|-------------|----------------------|
| Generator / template | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| CLI commands | `ai-company --help` + `ai-company <command> --help` |
| Models / orchestrator | `pytest` |
| Any source change | `ruff check src/ && mypy src/ && pytest` |
| Harness / docs | `pwsh scripts/lint-ecl.ps1` |

## 7 Safety Boundaries

- Agents may modify business/application code when the user's task requires it.
- Do not edit secrets, local env files, generated build outputs, dependency folders, or unrelated user changes.
- Active ECL change constraints are the current task source of truth and override generic project guidance.
- Do not overwrite active ECL change context; park or close it through the harness script first.
- Do not hand-edit `harness/changes/INDEX.json`; it is generated by script only.

## 8 Tool Vocabulary (Canonical)

The canonical runtime tool vocabulary for all agent cards (OpenCode v2 permission keys) is:

| Tool | Purpose | Notes |
|------|---------|-------|
| `read` | Read file contents | |
| `edit` | Exact string replacement in files | |
| `grep` | Search file contents with regex | |
| `list` | List directory entries | |
| `bash` | Execute shell commands | |
| `webfetch` | Fetch web content (HTTP/HTTPS) | |
| `task` | Launch sub-agent for complex work | |

**Alias policy (backward-compatible only):** The following legacy names are accepted as aliases but must not appear in newly generated cards:
- `write` → `edit`
- `execute` → `bash`
- `delegate` → `task`
- `web_search` / `websearch` → `webfetch`
- `code_interpreter` → **removed** (not an alias; rejected at runtime)

Agent generators must emit only the canonical 7 tools. ToolRunner validates against this list; unknown tools return an error.

## 9 Governance Rules

### 9.1 HITL Expiry Sweep

The `ApprovalGate` runs a periodic sweep (wired into the daemon/governance cadence) that transitions expired `PENDING` approval requests to `EXPIRED`. This prevents stale approvals from blocking the inbox indefinitely. Agents and dashboards should treat `EXPIRED` as a terminal state requiring re-submission.

## 10 Verification

| Change Type | Minimum Verification |
|-------------|----------------------|
| Generator / template | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| CLI commands | `ai-company --help` + `ai-company <command> --help` |
| Models / orchestrator | `pytest` |
| Any source change | `ruff check src/ && mypy src/ && pytest` |
| Harness / docs | `pwsh scripts/lint-ecl.ps1` |

## 11 Security — Key Rotation Procedure

**When to rotate:**
- Every 90 days (scheduled)
- Immediately on suspected compromise
- When team members with access leave
- After any security incident

**Procedure:**
1. **Generate new keys** for each provider/service (OpenCode, Gemini, Dashboard RBAC keys)
2. **Update local `.env`** with new values — NEVER commit `.env` to git (it's gitignored)
3. **Update deployed environments** (staging, production) via your secrets manager / platform:
   - GitHub Actions secrets for CI/CD
   - Docker / container platform secrets for runtime
   - Cloud provider secret stores (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
4. **Verify health endpoints** respond with new keys:
   - `curl http://<host>:8420/health` (production)
   - `curl http://<host>:8421/health` (staging)
5. **Revoke old keys** after confirming new ones work across all environments
6. **Update `.env.example`** placeholders if key format/naming changed
7. **Document rotation** in CHANGELOG.md with date and reason

**Dashboard RBAC keys** (in priority order):
- `DASHBOARD_ADMIN_KEY` — full access (also accepts `DASHBOARD_API_KEY` as alias)
- `DASHBOARD_APPROVE_KEY` — approve/reject tasks
- `DASHBOARD_RUN_KEY` — execute tasks, read KPIs
- `DASHBOARD_API_KEY` — legacy single-key mode (admin alias)

**LLM Provider keys:**
- `OPENCODE_API_KEY` — primary (Big Pickle)
- `GEMINI_API_KEY` — fallback (gemini-3.5-flash)
- Optional: `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

**Verification commands:**
```bash
# Local verification
uv run python -c "from ai_company.security.rbac import verify_keys; verify_keys()"

# Staging verification
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" http://localhost:8421/health

# Production verification (adjust host/port)
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" https://api.example.com/health
```

## Agent skills

### Issue tracker

GitHub issues, via the `gh` CLI. External PRs are not a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo (no `CONTEXT.md`/`CONTEXT-MAP.md` yet) — read `AGENTS.md`, `docs/`, and past decisions in `docs/adr/`. See `docs/agents/domain.md`.
