# AI Company Builder — Agent Guide

## Project Location

This project's actual filesystem root is `C:\Users\jmlus\light-speed-holdings`, NOT `/workspace/...` or any other container-style path. Always use this Windows path.

**Governance docs:** `.ai-company\` holds the constitution and governing documents. Read only the file relevant to the current task (e.g. `.ai-company\constitution\11-GIT-STANDARDS.md` before any git work) — do not load the directory wholesale.

**Git: `main` is protected** (GitHub ruleset, 6 required checks) — work on a branch, open a PR, merge only when checks are green; see §5 and `.ai-company\constitution\11-GIT-STANDARDS.md`.

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
| Known issues | `docs/known-issues.md` | Historical issues, observations, and fixes |

## 3 Where To Work

| Section | Document | Description |
|---------|----------|-------------|
| 3.1 | [System Architecture](docs/ARCHITECTURE.md) | Module hierarchy, data flow, key files |
| 3.2 | [ECL](docs/ECL.md) | Change lifecycle, context loading, harness workflow |
| 3.3 | [Status](docs/STATUS.md) | Recent handoff, current state |
| 3.4 | [Deployment](docs/DEPLOYMENT.md) | Environments, ports, website deploy verification, Vercel failure runbook |

## 4 Context Loading

1. Read this file.
2. Read [ECL](docs/ECL.md) for change lifecycle and context rules.
3. If `harness/changes/active/summary.md` exists, read active change files before any task-specific docs.
4. If no active change exists and `harness/evolution/pending.md` exists, read it before `docs/STATUS.md`.
5. If no active change exists and no pending evolution exists, read [Status](docs/STATUS.md).
6. Read the relevant source files for the task.
7. Run `uv run graphify query "<task>"` to surface prior bug fixes and decisions relevant to the task; the knowledge graph is indexed on every commit by the post-commit `capture-fix` + `graphify-rebuild` hooks.

## 5 Development Commands

**Branch rule:** `main` is protected — branch + PR, 6 required checks must pass before merge (`.ai-company\constitution\11-GIT-STANDARDS.md`).

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

See §6 Verification — the single source of the minimum-verification table.

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

**Operational rules** (session record: [docs/PORTS-MONITORING-2026-10-07.md](docs/PORTS-MONITORING-2026-10-07.md); issues tracked in §16):

1. **Dev cold-start tolerance:** the first request after `npm run dev` exceeds the 15 s probe timeout while Vite optimizes the dependency graph — automated probes must retry once after the `VITE ready in ...` log line and allow ≥30 s.
2. **Port conflicts:** kill lingering `node.exe` processes before restarting (`taskkill /F /IM node.exe`), verify ports are free (`netstat -an | findstr "1440 1441"`), then restart with `npm run dev` (1441) or `npm run preview` (1440).

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

## 14 Agent skills

### Dispatch guardrails (subagents vs. skills) — READ BEFORE DELEGATING

`task`'s `subagent_type` and `skill`'s `name` are **separate namespaces** with separate
allowed values. Passing a skill name (e.g. `ecl-harness-engineer`) as a `subagent_type`
is rejected by the runtime. Never derive a `subagent_type` from a `.agents/skills/` path
or a skill title. Validate against the system-prompt agent roster before calling `task`;
if a name isn't a known `subagent_type`, pick a valid roster entry or do the work
directly — and say honestly which you did. Full rules and the cross-reference table:
`docs/agents/subagents-vs-skills.md`.

### Skills CLI install hygiene

Run `git status` after any `npx skills` (skills CLI) command, before continuing with the task.
A single-skill install with `--skill` currently installs every skill in the registry (38 of 1 on
2026-10-12); the extras show up as untracked `.agents/skills/` paths — revert the ones you did
not ask for in the same session. Commit `skills-lock.json` only in its corrected state: it lists
every installed skill, so `skills update` restores anything still listed in it.

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
| Brand base | `ls-design-system` | ALWAYS loaded first by any creative skill; brand tokens live in `brand/tokens/` (canonical-only, not mirrored) + `brand/guidelines/`; `static/brand/` + `public/brand/` mirror other brand assets — see `brand/CANONICAL_SOURCES.md` |
| Orchestrator | `ls-creative-director` | Brief intake (artifact/audience/objective/narrative/visual language) → routes to one production skill + support skills |
| Production | `ls-frontend-design`, `ls-presentation-design`, `ls-document-design`, `ls-social-media-design`, `ls-brand-advertising` | Generate the artifact, delegating rendering to existing engines (python-pptx, Vite React SPA at repo-root `src/`, k-dense-*, Playwright) |
| Support | `ls-diagramming`, `ls-documentation-engineering`, `ls-visual-storytelling` | Diagram/graphic/doc-IA assets used inside produced artifacts |
| Gatekeeper | `ls-artifact-qa` | ALWAYS runs last on every artifact: Visual / Brand / UX / Accessibility / Content QA → APPROVE or FIX→re-render. Includes Playwright visual checks via `ls-artifact-qa` skill (see `.agents/skills/ls-artifact-qa/`) |

**Rules:** Any creative task starts at `ls-creative-director` (or loads `ls-design-system` directly) and ends at `ls-artifact-qa`. Brand tokens are the single source of truth — never invent brand colors/fonts. Rendering reuses existing engines rather than rebuilding them.

## 15 Evidence, Honesty and Execution Integrity Policy

1. Never invent, infer as fact, or fabricate an explanation for an action, file modification, failure, decision, or historical event.

2. Never claim that a file was read, modified, tested, committed, deployed, or verified unless the corresponding action and result are supported by available evidence.

3. Distinguish explicitly between:
   - What was requested
   - What was attempted
   - What actually happened
   - What was independently verified
   - What remains unknown

4. Never invent the expansion of an acronym, the existence of a project, stakeholder approval, prior authorization, document contents, test results, performance metrics, or the contents of a previous investigation.

5. When asked why an action occurred, consult available task instructions, tool logs, audit records, shell history where available, Git history, and relevant file diffs. State the limits of the evidence.

6. If the cause cannot be established, say: "I cannot determine the cause from the available evidence." Do not substitute a plausible explanation.

7. If challenged on a factual claim, recheck the underlying evidence. Do not defend the claim merely because it appeared in an earlier response.

8. If an earlier statement is disproved, explicitly retract it, identify the unsupported claim, state what is actually known, and identify what remains unresolved.

9. Never describe work as approved, pre-planned, harmless, necessary, or within scope unless the applicable evidence supports that description.

10. Report unexpected modifications, failed actions, missing evidence, and scope violations immediately. Do not silently conceal, revert, or rewrite the history of an incident.

11. Do not fabricate evidence, logs, citations, tool results, timestamps, or test outcomes.

12. Compliance is determined by independent evidence and validation, not by the agent's assertion that it followed this policy.

## 16 Known Issues Tracker (Permanent Record)

Moved to `docs/known-issues.md`. Add new entries there; do not remove existing entries without a replacement fix.

## 17 Tool Usage Issues (Session Records)

Moved to `docs/tool-usage-issues.md`. Add new entries there; do not remove existing entries without a replacement fix.

## Deck Generation Navigation

Moved to `docs/deck-generation.md`. Leading word: generate. One source of truth: company-registry.yaml.

# PowerShell Environment Rules (CRITICAL)

The `bash` tool runs **PowerShell 5.1**, NOT bash or CMD. Follow these rules strictly.

## NEVER USE THESE PATTERNS:

### Command Chaining
- ❌ `command1 && command2` → ✅ Use separate tool calls
- ❌ `command1 || command2` → ✅ Use separate tool calls or `if` statements
- ❌ `cd /path && ls` → ✅ Use separate `bash` calls for each command

### Unix/Unix-like Syntax
- ❌ `2>/dev/null` → ✅ Use `2>$null` or omit error suppression
- ❌ `ls -la`, `ls -l`, `ls -a` → ✅ Use `dir` or `Get-ChildItem` without flags
- ❌ `head -20`, `tail -20` → ✅ Use `Select-Object -First 20` or `Select-Object -Last 20`
- ❌ `grep pattern` → ✅ Use `Select-String -Pattern "pattern"`
- ❌ `find . -name "*.py"` → ✅ Use `Get-ChildItem -Recurse -Filter "*.py"` or the `glob` tool
- ❌ `cat file.txt` → ✅ Use `Get-Content file.txt` or `type file.txt`
- ❌ `echo $VAR` → ✅ Use `echo $env:VAR` or `Write-Output $env:VAR`

### CMD Syntax
- ❌ `if exist file (command)` → ✅ Use `if (Test-Path file) { command }`
- ❌ `for %f in (*.py) do command` → ✅ Use `foreach ($f in Get-ChildItem *.py) { command }`
- ❌ `dir /b /s` → ✅ Use `Get-ChildItem -Recurse` or the `glob` tool

### Path Formats
- ❌ `/c/Users/username/...` (Git Bash style) → ✅ Use `C:\Users\username\...`
- ❌ `C:/Users/username/...` → ✅ Use `C:\Users\username\...`

## ALWAYS USE:

### For File Operations
- ✅ Use the `read` tool to read file contents
- ✅ Use the `glob` tool to find files by pattern
- ✅ Use `dir` or `Get-ChildItem` to list directory contents

### For Command Execution
- ✅ Single command per `bash` tool call (no chaining)
- ✅ `dir` instead of `ls` (without Unix flags)
- ✅ `Get-Content` or `type` instead of `cat`
- ✅ `Get-ChildItem -Recurse` instead of `find`
- ✅ `Select-String` instead of `grep`
- ✅ `Select-Object -First N` instead of `head -N`
- ✅ `2>$null` instead of `2>/dev/null`

### For Error Handling
- ✅ Let errors surface naturally (don't suppress with `2>/dev/null`)
- ✅ Use `try/catch` blocks for complex error handling
- ✅ Check `$LASTEXITCODE` for command success

## Examples:

### ❌ BAD (will fail):
```powershell
cd /c/Users/jmlus/project && git status
ollama --version 2>/dev/null || echo "not found"
ls -la src/ | head -20
find . -name "*.py" -type f 2>/dev/null
if exist .env (type .env) else (echo "no .env")
```

### ✅ GOOD:
- Call `bash` with command `git status` (the tool already handles `workdir`).
- Use the `glob` tool with pattern `**/*.py` instead of `find . -name "*.py" | head -20`.
- Call `bash` with `ollama --version`. If it fails, read the error output.

## If you MUST chain commands or use modern PowerShell syntax

Explicitly invoke PowerShell 7:
- `pwsh -Command "Get-ChildItem -Recurse -Filter '*.py' | Select-Object -First 20"`

## Python Execution in PowerShell 5.1

When testing Python code, verifying imports, or running scripts, **NEVER chain commands with `&&` or `||`**. PowerShell 5.1 throws a Parser Error and aborts the task.

### ❌ NEVER DO THIS:
- `python -c "import sys" && echo "Success"`
- `python test.py || echo "Failed"`
- `cd src && python main.py`

### ✅ ALWAYS DO THIS INSTEAD:

**Option 1: Single, standalone Python command (best for quick checks)**

Run the Python command by itself. If it fails, the tool returns the Python traceback — all the feedback you need. Do not append success messages.
```powershell
python -c "import os; print(os.getenv('EVAL_LLM_PROVIDER'))"
```

**Option 2: The "Write then Execute" pattern (for anything multi-step)**

1. Use the `write` tool to create a check script:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   try:
       from ai_company.llm.providers.openai_compatible import OpenAICompatibleProvider
       print("Import successful. EVAL_LLM_PROVIDER is:", os.getenv("EVAL_LLM_PROVIDER"))
   except ImportError as e:
       print("Import failed:", e)
   ```
2. Run it with a single `bash` call: `python .tmp/test_gemini.py`
3. Read the clean output.

This gives the agent a safe, deterministic escape hatch: it no longer has to guess how to chain commands, because it has a sanctioned step-by-step procedure guaranteed to work in PowerShell 5.1.

# 🧠 CRITICAL: CONTEXT OPTIMIZATION & STATE MANAGEMENT

To prevent context bloat, preserve cache hits, and avoid infinite retry loops, you MUST adhere to the following context management rules:

## 1. The "Two-Strike" Rule for Tool Failures
- If a tool call fails **twice** with the same type of error (e.g., PowerShell Parser Error, File Not Found), you MUST STOP trying variations of that command.
- **Action:** Immediately pivot to a fundamentally different tool (e.g., if `bash` fails twice, switch to `glob` or `read`). Do not attempt a 3rd variation of the same broken pattern.

## 2. The Discovery Hierarchy (Strict Order of Operations)
When looking for information, you MUST use tools in this exact order of preference. Do not skip to `bash` unless explicitly required.
1. **`glob`**: For finding files by pattern (e.g., `**/llm/**/*.py`).
2. **`read`**: For reading file contents OR listing directory contents (passing a directory path to `read` returns a clean, token-efficient list of entries).
3. **`bash`**: ONLY for single, atomic, verified commands (e.g., `git log --oneline -5`, `ollama --version`). NEVER for file discovery.

## 3. No Broad Directory Dumps
- ❌ NEVER run `dir`, `ls`, or `find` without highly specific filters.
- ✅ ALWAYS use `glob` with precise patterns (e.g., `**/*provider*.py`) or pass the specific directory path to the `read` tool to get a clean, truncated entry list.

## 4. Maintain a "Running Findings" State
Before making a new tool call, briefly summarize what you **already know** in your `<reasoning>` block.
- Example: *"Known: Ollama is running on 11434, .env has Gemini key, src/ai_company/llm/providers only contains __pycache__. Next step: Check git history for deleted provider files."*
- This compresses historical context into a dense, token-efficient summary, preventing you from re-exploring dead ends.

## 5. Leverage `todowrite` as Memory Anchors
- Use the `todowrite` tool not just for planning, but to explicitly mark discoveries as `completed`.
- Checking off a todo acts as a strong attention anchor for the LLM, signaling "this path is exhausted, move on."

## 6. Truncate Verbose Outputs
- If a tool returns a massive output (e.g., a 500-line directory listing), do not paste it back into your reasoning. Summarize it: *"Found 42 Python files, primarily in src/ai_company/archify/."*

# TOOL SELECTION PRIORITY (Follow this order strictly)

## File Operations:
1. **Reading files**: Use `read` tool (NEVER bash `cat`/`type`)
2. **Finding files**: Use `glob` tool with specific patterns (NEVER bash `find`/`dir /s`)
3. **Listing directories**: Use `read` tool on directory path (NEVER bash `ls`/`dir`)
4. **Searching content**: Use `grep` tool if available, otherwise `read` + manual scan

## System Operations:
1. **Git commands**: Single command only (NO chaining with &&)
2. **Version checks**: Single command only (e.g., `ollama --version`)
3. **Process checks**: Use `tasklist | findstr "name"` (single pipeline only)
4. **Port checks**: Use `netstat -an | findstr "port"` (single pipeline only)

## NEVER USE bash for:
- File discovery (use `glob`)
- File reading (use `read`)
- Directory listing (use `read` on directory)
- Complex multi-step operations (break into separate tool calls)

# STATE MANAGEMENT (Prevent redundant exploration)

Before making ANY tool call, briefly state in your reasoning:
- "Known: [what you've already discovered]"
- "Unknown: [what you need to find]"
- "Next: [specific action to take]"

Example:
"Known: Ollama is running on 11434, .env has Gemini key, src/ai_company/llm/providers exists but is empty.
Unknown: Where are the actual provider implementations?
Next: Check git history for deleted provider files."

This prevents:
- Re-reading the same directory multiple times
- Re-running the same failed commands
- Losing track of what you've already verified

# PATH HANDLING (Critical for Windows)

## Path Format Rules:
- NEVER use `/c/Users/...` (Git Bash style) in bash commands
- ALWAYS use `C:\Users\...` or relative paths
- When using `read`/`glob` tools, paths may show as `C:\c\Users\...` - this is a display artifact, use the actual path

## Working Directory:
- The bash tool's `workdir` parameter handles path conversion
- You do NOT need to `cd` before running commands
- If you must change directories, use a separate bash call: `cd C:\path`

## Common Mistakes to Avoid:
❌ `ls /c/Users/jmlus/project`
✅ `dir C:\Users\jmlus\project` or just `dir` (if workdir is set)

❌ `cat /c/Users/jmlus/project/.env`
✅ Use `read` tool with path `/c/Users/jmlus/project/.env`

# VERIFICATION PROTOCOL (Prevent silent failures)

After EVERY significant action, verify it worked:

## File Edits:
1. Use `edit` tool to make change
2. Immediately use `read` tool to verify the change
3. Only proceed if verification succeeds

## File Creation:
1. Use `write` tool to create file
2. Use `read` tool to verify content
3. Only proceed if file exists and has correct content

## Command Execution:
1. Run the command
2. Check exit code (0 = success)
3. If non-zero, diagnose before retrying (don't just retry the same command)

## Example:
❌ BAD: Edit file → immediately move to next task
✅ GOOD: Edit file → read file to verify → move to next task

# RETRY BUDGET (Prevent infinite loops)

## Maximum Retries:
- Same command with same syntax: **1 retry** (then change approach)
- Same command with different syntax: **2 retries** (then switch tools)
- Same tool with different parameters: **3 retries** (then escalate)

## Escalation Protocol:
After exhausting retries:
1. STOP trying the same approach
2. State clearly: "Tool X failed Y times with error Z"
3. Switch to a fundamentally different tool or method
4. If all methods fail, report the limitation and move on

## Example:
❌ BAD: Try `find` → fails → try `find` with different flags → fails → try `find` again
✅ GOOD: Try `find` → fails → try `glob` tool → succeeds or report limitation

# TASK DECOMPOSITION (For complex requests)

When given a complex task, break it into atomic steps:

1. **Discovery Phase**: Use `read`/`glob` to understand current state
2. **Planning Phase**: Use `todowrite` to create checklist
3. **Execution Phase**: One atomic operation per tool call
4. **Verification Phase**: Verify each step before proceeding
5. **Summary Phase**: Report what was done and what remains

## Atomic Operations:
- Read ONE file
- Search ONE pattern
- Edit ONE file
- Run ONE command
- Verify ONE change

## Never Combine:
❌ "Read file and edit it"
✅ "Read file" → "Edit file" → "Verify edit"

# OUTPUT COMPRESSION (Prevent context bloat)

## When Tool Returns Large Output:
1. Do NOT paste entire output into reasoning
2. Summarize key findings in 2-3 sentences
3. Extract only relevant data points
4. Reference the full output location if needed

## Examples:
❌ BAD: "The directory listing shows: [500 lines of files]"
✅ GOOD: "Found 42 Python files, primarily in src/ai_company/archify/ (3 files) and src/ai_company/llm/ (empty except __pycache__)"

❌ BAD: "The git log shows: [100 commits]"
✅ GOOD: "Recent commits show: 4f0a4e08 reverted to Ollama, fa4a4c29 added HTTP provider, 4d39675c deleted evals/"

# EARLY EXIT (Know when to stop investigating)

Stop investigating a path when:
1. **Directory is empty** (only __pycache__) → move to next directory
2. **File doesn't exist** → check git history or report missing
3. **Command fails 3 times** → report limitation and move on
4. **Pattern not found** → try broader pattern or report absence
5. **Tool consistently fails** → switch to alternative tool

## Red Flags (Stop and Report):
- "File not found" after checking multiple paths
- "Directory empty" after checking subdirectories
- "Command not recognized" after trying alternatives
- "Permission denied" after verifying paths

## Action:
State clearly: "Investigation of X yielded no results because Y. Moving to Z."

# TOOL CALL STRATEGY

## Use Parallel Calls (multiple tools in one response) when:
- Tasks are independent (no dependencies)
- You're gathering initial information
- You're verifying multiple unrelated items

Example:
✅ Read .env, Read models.yaml, Read client.py (all independent)

## Use Sequential Calls (one tool at a time) when:
- Each step depends on the previous result
- You're debugging an error
- You're making edits that need verification

Example:
✅ Read file → Edit file → Verify edit (each depends on previous)

## Never Mix:
❌ Read file A, Edit file B, Read file C (editing requires verification first)
# ENVIRONMENT DETECTION (First 3 tool calls)

At the start of any session, quickly establish:

1. **Shell Type**: Run `echo $PSVersionTable` or `$PSVersionTable.PSVersion`
   - If PowerShell 5.1: Apply strict syntax rules
   - If PowerShell 7+: Can use && and ||

2. **Working Directory**: Run `pwd` or `$PWD`
   - Confirm you're in the right repository

3. **Available Tools**: Check for key tools
   - `git --version`
   - `python --version` or `py --version`
   - `ollama --version` (if relevant)

## Adapt Based on Environment:
- PowerShell 5.1: Use only single commands, no chaining
- PowerShell 7+: Can use modern syntax
- Missing tools: Report and work around limitations
