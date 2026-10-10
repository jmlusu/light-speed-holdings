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
| CLI Entry | `src/ai_company/cli/main.py` | Typer app, 37 subcommands registered here |
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
7. Run `uv run graphify query "<task>"` to surface prior bug fixes and decisions relevant to the task; the knowledge graph is indexed on every commit by the post-commit `capture-fix` + `graphify-rebuild` hooks.

## 5 Development Commands

### Quick Start (New Developers)

```powershell
.\scripts\dev\dev.ps1           # Full onboarding: venv, deps, lint, tests, agents
.\scripts\dev\dev.ps1 status    # Show project status
.\scripts\dev\dev.ps1 test      # Run test suite
.\scripts\dev\dev.ps1 lint      # Run linter + type checker
```

### Manual Setup

```bash
uv sync --extra dev            # Install project + dev deps (creates .venv, respects uv.lock)
pre-commit install --hook-type pre-commit --hook-type post-commit  # Enable git hooks (ruff, mypy, bandit, post-commit capture-fix)
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
.\scripts\deploy\backup.ps1                    # Backup .opencode/, company/, results/ (to ~/.lightspeed/backups)
.\scripts\deploy\backup.ps1 -RetentionDays 14  # Keep 14 days of backups
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
| Harness / docs | `pwsh scripts/maintenance/lint-ecl.ps1` |

## 7 Safety Boundaries

- Agents may modify business/application code when the user's task requires it.
- Do not edit secrets, local env files, generated build outputs, dependency folders, or unrelated user changes.
- Active ECL change constraints are the current task source of truth and override generic project guidance.
- Do not overwrite active ECL change context; park or close it through the harness script first.
- Do not hand-edit `harness/changes/INDEX.json`; it is generated by script only.
- **Do not install or run skills that transmit local data** (code, docs, screenshots, prompts, memory) to third-party hosts unless the vendor is on [`docs/APPROVED-VENDORS.md`](docs/APPROVED-VENDORS.md) within the 90-day exception window. See §9.2. Retired: `claude-mem-*`, `scroll-craft`, `greploop*`.

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

### 9.2 Skill Third-Party Transmission Ban

Skills must not send LightSpeed local data (code, diffs, docs, screenshots, prompts, session/memory payloads, PDFs, secrets) to third-party hosts unless the vendor is allow-listed in [`docs/APPROVED-VENDORS.md`](docs/APPROVED-VENDORS.md) and the exception is inside its **90-day** window (or re-signed by CEO/CISO). **CISO of record: Jack Mlusu (Human CEO).** On unexpected transmission: stop the skill, do not retry, report skill + host + payload class to the CEO. Full rule: [`docs/SKILL_CURATION_POLICY.md`](docs/SKILL_CURATION_POLICY.md) § Skill Third-Party Transmission Ban. Retired 2026-09-23: `claude-mem-*`, `scroll-craft`, `greploop`/`greploop-apps` (skills deleted; local `~/.claude-mem` purged).

### 9.3 Audit Evidence Separation

An agent performing an audit must treat its evidence set as read-only: **never write, move, rename, or delete any file inside the evidence directory it is auditing**, and never write its own audit output there. The auditor's read set and write set must be disjoint for the whole run, so findings stay re-derivable from an untouched evidence set and can be independently re-checked.

- **Evidence directory** — any path consumed as evidence: `reports/evidence/`, `audit/*.jsonl`, `.opencode/audit/*`, `harness/changes/*/reviews/`, downloaded `audit-evidence` CI artifacts, `data/orchestrator/escalation_events.jsonl`, `data/orchestrator/dead_letter.jsonl`, `reports/evidence/audit-*.jsonl`.
- **Where output goes** — a directory outside the evidence set (for the weekly audit: `reports/repo-audit-<AUDIT_DATE>.md`, with evidence at `reports/evidence/<AUDIT_DATE>.json`), or a path outside the repository.
- **On violation** — discard the run, re-fetch evidence from a fresh clone or CI artifact, re-run, and report the incident alongside the findings.

## 10 Verification

| Change Type | Minimum Verification |
|-------------|----------------------|
| Generator / template | `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| CLI commands | `ai-company --help` + `ai-company <command> --help` |
| Models / orchestrator | `pytest` |
| Any source change | `ruff check src/ && mypy src/ && pytest` |
| Harness / docs | `pwsh scripts/maintenance/lint-ecl.ps1` |

## 11 Security — Key Rotation Procedure

See also: [docs/DASHBOARD_KEY_ROTATION.md](docs/DASHBOARD_KEY_ROTATION.md) for detailed dashboard RBAC key rotation procedures.

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
- Optional: `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `MIMO_API_KEY`

**Verification commands:**
```bash
# Local verification
uv run python -c "from dotenv import load_dotenv; load_dotenv(); from ai_company.security.rbac import verify_keys; verify_keys()"

# Staging verification
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" http://localhost:8421/health

# Production verification (adjust host/port)
curl -H "X-API-Key: \$DASHBOARD_ADMIN_KEY" https://api.example.com/health
```

## 12 Ports — Vite App and Server Monitoring

**Assigned ports (2026-10-07):**
- Development (`npm run dev`): **http://localhost:1441** — `vite.config.ts` → `server.port`
- Production preview (`npm run preview`, serves `dist/`): **http://localhost:1440** — `vite.config.ts` → `preview.port`
- Dashboard CORS allowlists include both origins (legacy `:3000` retained) in `src/ai_company/dashboard/app.py`, `docker-compose.yml`, `docker-compose.staging.yml`, `.env.staging.example`.
- Updated references: `README.md` (scripts table), `check_server.py`, `docs/IMAGE_SPEC.md` (QA probe URL).

**Monitoring session 2026-10-07, 22:15–22:29 (10+ min, 20 probe cycles, 120 HTTP probes):** both ports stayed listening; 119/120 probes HTTP 200 across `/`, `/insights`, `/solutions` on each port; `dev.log` and `preview.log` scans: **0 error matches**; no crashes, no port drift, no EADDRINUSE.

**Issue found and fixed:**

1. **Dev cold-start probe timeout (1 failure — cycle 1, `:1441/` returned ERR).** The first request after `npm run dev` exceeded the 15 s probe timeout while Vite optimized the 1676-module dependency graph. Re-measured cold start: port binds in ~2.5 s, first request completes in ~6.3 s and returns 200; subsequent requests ~8 ms. **Fix:** documented here — automated health checks and QA probes must tolerate the first dev request (retry once after the `VITE ready in ...` log line, allow ≥30 s timeout). No code change required; reproduced deterministically (warm dep cache ≈ 6 s, cold ≈ >15 s).

**Servers were stopped and ports 1440/1441 released after the session.**

## 13 Application Boundary — CEO Dashboard vs Vite/React App

The CEO Dashboard (internal) and the Vite/React app (external, §12) are **two independent applications**: different runtimes, servers, health checks, and deploy targets. Never serve one on the other's assigned port and never treat them as the same service.

| | CEO Dashboard (internal) | Vite/React app (external) |
|---|---|---|
| Runtime | FastAPI/uvicorn via `ai-company dashboard` (`src/ai_company/dashboard/`) | Vite dev/preview (repo-root `src/`); static `dist/` on Vercel |
| Production port | **8420** — `Dockerfile` (`EXPOSE 8420`, CMD `--port 8420`, healthcheck `:8420`), `docker-compose.yml` `8420:8420` | **443** at `lightspeedholdings.vercel.app` (Vercel) |
| Development port | **8421** — `docker-compose.staging.yml` host `${STAGING_DASHBOARD_PORT:-8421}` → container 8420; local: `uv run ai-company dashboard --port 8421`; tests default `http://localhost:8421` | **1441** (dev) / **1440** (preview), §12 |
| Health check | `GET /health` (JSON) | `GET /` (SPA) |

**Rules:**

1. **Port assignment is hard:** dashboard production = **8420**, dashboard development = **8421**. Do not repoint either.
2. In Docker the dashboard container always listens on 8420; development/staging maps host 8421 → container 8420.
3. The Vite/React app never occupies 8420/8421; the dashboard never occupies 1440/1441.
4. CORS allowlist entries (incl. legacy `:3000`/`:5173`) are permitted browser origins, not port assignments.
5. Bare `uv run ai-company dashboard` still defaults to 8420 (legacy local default); development launches must pass `--port 8421`.

**Transient conflict (2026-10-07):** host 8421 is currently held by the unrelated `athena-frontend-staging` container (separate project), so the staging dashboard is temporarily published on 8422. The assigned development port remains 8421 — restore the default mapping when Athena no longer needs 8421.

## Agent skills

### Dispatch guardrails (subagents vs. skills) — READ BEFORE DELEGATING

`task`'s `subagent_type` and `skill`'s `name` are **separate namespaces** with separate
allowed values. Passing a skill name (e.g. `ecl-harness-engineer`) as a `subagent_type`
is rejected by the runtime. Never derive a `subagent_type` from a `.agents/skills/` path
or a skill title. Validate against the system-prompt agent roster before calling `task`;
if a name isn't a known `subagent_type`, pick a valid roster entry or do the work
directly — and say honestly which you did. Full rules and the cross-reference table:
`docs/agents/subagents-vs-skills.md`.

### Issue tracker

GitHub issues, via the `gh` CLI. External PRs are not a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo (no `CONTEXT.md`/`CONTEXT-MAP.md` yet) — read `AGENTS.md`, `docs/`, and past decisions in `docs/adr/`. See `docs/agents/domain.md`.

### Creative Production Stack (ls-* skills)

Branded creative output routes through a layered skill stack. All `ls-*` skills live in `.agents/skills/`.

**Layers (in order):**

| Layer | Skill(s) | Role |
|-------|----------|------|
| Brand base | `ls-design-system` | ALWAYS loaded first by any creative skill; brand tokens live in `brand/tokens/` + `brand/guidelines/` (canonical root is `brand/**`; `static/brand/` + `public/brand/` are mirrors — see `brand/CANONICAL_SOURCES.md`) |
| Orchestrator | `ls-creative-director` | Brief intake (artifact/audience/objective/narrative/visual language) → routes to one production skill + support skills |
| Production | `ls-frontend-design`, `ls-presentation-design`, `ls-document-design`, `ls-social-media-design`, `ls-brand-advertising` | Generate the artifact, delegating rendering to existing engines (python-pptx, Vite React SPA at repo-root `src/`, k-dense-*, Playwright) |
| Support | `ls-diagramming`, `ls-documentation-engineering`, `ls-visual-storytelling` | Diagram/graphic/doc-IA assets used inside produced artifacts |
| Gatekeeper | `ls-artifact-qa` | ALWAYS runs last on every artifact: Visual / Brand / UX / Accessibility / Content QA → APPROVE or FIX→re-render. Includes Playwright visual checks via `ls-artifact-qa` skill (see `.agents/skills/ls-artifact-qa/`) |

**Rules:** Any creative task starts at `ls-creative-director` (or loads `ls-design-system` directly) and ends at `ls-artifact-qa`. Brand tokens are the single source of truth — never invent brand colors/fonts. Rendering reuses existing engines rather than rebuilding them.
