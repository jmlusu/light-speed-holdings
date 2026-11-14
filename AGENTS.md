# AI Company Builder — Agent Guide
## Project Location
This project's actual filesystem root is `C:\Users\jmlus\light-speed-holdings`. Always use this Windows path.

**Governance docs:** `.ai-company\` holds the constitution and governing documents. Read only the file relevant to the current task (e.g. `.ai-company\constitution\11-GIT-STANDARDS.md` before any git work) — do not load the directory wholesale.

**Git: `main` is protected** (GitHub ruleset, 6 required checks) — work on a branch, open a PR, merge only when checks are green.

## Hard Rules (always apply)
- Never delete, overwrite, or restore files you did not create this session, including untracked ones. Stage by explicit path; never `git add .`.
- Never use `--no-verify`, empty "trigger CI" commits, or `git config` changes without asking.
- "Done" means verified in the target environment (CI included). Otherwise say "local only" or "unverified". A PR exists only if `gh pr create` output shows it.
- If CI status can't be read with `gh`, say so and ask. Never search config or env for tokens.
- Shell is PowerShell: no `head`, `tail`, `sed`, `$?`, `2>/dev/null`. Chain with `;`, use `$LASTEXITCODE`, `Select-Object -First N`. On 5.1 also no `&&` or `||`.
- Before any git, PR, or CI work, read `.ai-company\constitution\16-AGENT-GUARDRAILS.md`.

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
| CLI Entry | `src/ai_company/cli/main.py` | Typer app, 37 subcommands registered here |
| Task System | `src/ai_company/orchestrator/message_bus.py` | JSON-based task queue at `.opencode/inbox.json` |
| Domain Models | `src/ai_company/models/models.py` | Pydantic models: Executive, Specialist, Department, Company |

## 3 Context Loading
1. Read this file.
2. Read [ECL](docs/ECL.md) for change lifecycle and context rules.
3. If `harness/changes/active/summary.md` exists, read active change files before any task-specific docs.
4. If no active change exists and `harness/evolution/pending.md` exists, read it before `docs/STATUS.md`.
5. If no active change exists and no pending evolution exists, read [Status](docs/STATUS.md).
6. Read the relevant source files for the task.

## 4 Tool Vocabulary (Canonical)

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

## 5 Ports — Vite App and Server Monitoring
**Assigned ports:**
- Development (`npm run dev`): **http://localhost:1441** — `vite.config.ts` → `server.port`
- Production preview (`npm run preview`, serves `dist/`): **http://localhost:1440** — `vite.config.ts` → `preview.port`

## 6 Application Boundary — CEO Dashboard vs Vite/React App

The CEO Dashboard (internal) and the Vite/React app (external) are **two independent applications**: different runtimes, servers, health checks, and deploy targets. Never serve one on the other's assigned port and never treat them as the same service.

| | CEO Dashboard (internal) | Vite/React app (external) |
|---|---|---|
| Runtime | FastAPI/uvicorn via `ai-company dashboard` (`src/ai_company/dashboard/`) | Vite dev/preview (repo-root `src/`); static `dist/` on Vercel |
| Production port | **8420** — `Dockerfile` (`EXPOSE 8420`, CMD `--port 8420`, healthcheck `:8420`), `docker-compose.yml` `8420:8420` | **443** at `lightspeedholdings.vercel.app` (Vercel) |
| Development port | **8421** — `docker-compose.staging.yml` host `${STAGING_DASHBOARD_PORT:-8421}` → container 8420; local: `uv run ai-company dashboard --port 8421`; tests default `http://localhost:8421` | **1441** (dev) / **1440** (preview) |
| Health check | `GET /health` (JSON) | `GET /` (SPA) |

## 7 Evidence, Honesty and Execution Integrity Policy
Never invent, infer as fact, or fabricate an explanation for an action, file modification, failure, decision, or historical event.

## 8 Tool Usage Issues (Session Records)

| Issue | Fix | Date Identified | Date Fixed | Status |
|-------|-----|-----------------|------------|--------|
| **Bash/PowerShell command execution issues** — Multiple bash tool calls had syntax issues with PowerShell heredocs, line continuations, and string quoting due to different quoting rules between Windows PowerShell 5.1 and bash/cmd. | Follow the shell rules in Hard Rules; break complex commands into simpler steps with careful quoting. | 2026-10-11 | | ⚠️ Workaround |
| **PowerShell `$(...)` expands inside double-quoted `--jq` arguments** — `gh pr view --jq "state=$(.state)"` fails with `(.state) was not recognized` because PowerShell evaluates `$(...)` before `gh` receives the string. Recurred in-session 2026-10-12, so the fix is now a standing directive, not a one-off note. Single-quoting is not sufficient by itself: PS 5.1 does not escape embedded double quotes when building native command lines, so a `--jq` expression containing string literals gets split into multiple arguments (`accepts at most 1 arg(s), received 2`). | | | | |

## 9 LLM Provider Keys

`OPENCODE_API_KEY` (primary), `GEMINI_API_KEY` (fallback); optional `MIMO_API_KEY`, `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`. Keep them in a local `.env` only - never commit secrets.
