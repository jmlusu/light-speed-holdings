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

## 3 Where To Work

| Section | Document | Description |
|---------|----------|-------------|
| 3.1 | [System Architecture](docs/ARCHITECTURE.md) | Module hierarchy, data flow, key files |
| 3.2 | [ECL](docs/ECL.md) | Change lifecycle, context loading, harness workflow |
| 3.3 | [Status](docs/STATUS.md) | Recent handoff, current state |
| 3.4 | [Deployment](docs/DEPLOYMENT.md) | Environments, ports, website deploy verification, Vercel failure runbook |

## 4 Context Loading

1. This file is already loaded into context — do not re-read it.
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
| Any source change | `ruff check src/`, then `mypy src/`, then `pytest` — separate commands, not chained (no `&&` in PowerShell 5.1, see §17) |
| Frontend (Vite/React) | `npx tsc --noEmit`, then `npm run build` |
| Harness / docs | `pwsh scripts/maintenance/lint-ecl.ps1` |

## 7 Safety Boundaries

- Agents may modify business/application code when the user's task requires it.
- Do not edit secrets, local env files, generated build outputs, dependency folders, or unrelated user changes.
- Active ECL change constraints are the current task source of truth and override generic project guidance.
- Do not overwrite active ECL change context; park or close it through the harness script first.
- Do not hand-edit `harness/changes/INDEX.json`; it is generated by script only.
- **Ask before creating a worktree.** Never create a git worktree without explicit user consent. When approved, create it under `.worktrees/` in the repository root (gitignored), never in `%TEMP%`. The native worktree tool places worktrees outside the repository, so use `git worktree add .worktrees/<name> -b <branch> origin/main` for project-local placement.
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

Rotate keys every 90 days (scheduled), immediately on suspected compromise, when team members with access leave, and after any security incident. NEVER commit `.env` to git (it is gitignored).

Full procedure: [docs/KEY-ROTATION.md](docs/KEY-ROTATION.md). Dashboard RBAC keys: [docs/DASHBOARD_KEY_ROTATION.md](docs/DASHBOARD_KEY_ROTATION.md).

**LLM provider keys:** `OPENCODE_API_KEY` (primary), `GEMINI_API_KEY` (fallback), and optional `DEEPSEEK_API_KEY`, `KIMI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `MIMO_API_KEY`.

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
A single-skill install with `--skill` currently installs every skill in the registry (38 skills installed instead of 1, on
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

Branded creative output routes through the `ls-*` skills in `.agents/skills/`. Layer order: `ls-design-system` (brand base, ALWAYS loaded first) → `ls-creative-director` (brief intake, routes to one production skill plus support skills) → production (`ls-frontend-design`, `ls-presentation-design`, `ls-document-design`, `ls-social-media-design`, `ls-brand-advertising`) with support (`ls-diagramming`, `ls-documentation-engineering`, `ls-visual-storytelling`) → `ls-artifact-qa` (gatekeeper, ALWAYS last).

**Rules:** Any creative task starts at `ls-creative-director` (or loads `ls-design-system` directly) and ends at `ls-artifact-qa`. Brand tokens are the single source of truth — never invent brand colors/fonts. Rendering reuses existing engines rather than rebuilding them.

Brand tokens: `brand/tokens/` + `brand/guidelines/` (canonical; see `brand/CANONICAL_SOURCES.md`). Layer table and QA scope: [docs/agents/creative-stack.md](docs/agents/creative-stack.md).

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

The full tracker (every row, date and status) lives in [`docs/KNOWN-ISSUES.md`](docs/KNOWN-ISSUES.md). Add new issues there as new rows; never delete a row without a documented replacement fix. Standing directives distilled from it:

- After a squash-merge, local `main` diverges from `origin/main`: run `git fetch`, then `git reset --hard origin/main` — only when local `main` holds no unpushed work you still need.
- Vercel `ignoreCommand` contract: exit 0 = skip (CANCELED), exit ≥1 = build. `.vercelignore` must keep `scripts/deploy/vercel-ignore-build.sh` reachable using the parent-chain pattern (`/scripts/*`, `!/scripts/deploy/`, `/scripts/deploy/*`, `!/scripts/deploy/vercel-ignore-build.sh`); `scripts/test/check-vercelignore.py` guards it.
- Dev server cold start and port conflicts: see §12. Dashboard vs Vite/React ports: see §13.

## 17 Windows / PowerShell 5.1 Rules

The default shell is Windows PowerShell 5.1. Full incident record: [`docs/agents/tool-issues.md`](docs/agents/tool-issues.md) (add new issues there as new rows).

- No `&&` — run commands as separate steps, or use `pwsh -Command "cd 'path'; & command"`.
- `-First` / `-Last` take positive numbers only.
- PowerShell expands `$(...)` and `$vars` and splits nested quotes before the native command sees them. Write multi-statement PowerShell, and any one-liner containing `$(...)`, `$vars` or nested quoting (including heredocs and line continuations), to a temp `.ps1` and run it with `powershell -File <path>.ps1`. Inline `gh --jq` expressions must be single-quoted, single-field, with no string literals.
- `gh pr merge`: run it from `C:\Users\jmlus\light-speed-holdings`, never from a temp worktree. Then `git push origin --delete <branch>` and `git fetch --prune` from the main checkout.
- Worktree removal failing with "Filename too long": `git config --global core.longpaths true` (one-time); fallback `cmd /c rmdir /S /Q "<path>"`.
- After `harness-change.ps1 reindex`, if `git status` shows ` M harness/changes/INDEX.json` with an empty `git diff`, restore it with `git checkout -- harness/changes/INDEX.json`.
- Cherry-pick stuck in a conflict state: stage all resolutions and `git cherry-pick --continue`, or abort and merge instead.
- After resolving merge conflicts in, or editing, a `.tsx` file, run `npx tsc --noEmit` and fix errors before committing; keep JSX inside `return (...)`.

## 18 Governance Protocol — CEO Override for Root Config Files

### 18.1 Protocol Overview

The files `AGENTS.md` and `opencode.json` are **root configuration files** that control agent behavior and tool permissions across the entire organization. To prevent unauthorized automated changes (by agents, bots, or CI) while preserving the Human CEO's ability to make immediate operational decisions, the following protocol is enforced:

**Any commit modifying `AGENTS.md` or `opencode.json` must include a CEO Override tag in the commit message:**

```text
[CEO-OVERRIDE: <OPERATIONAL REASON>]
```

### 18.2 Behavior Matrix

| Commit Touches Root Config? | Tag Present? | Result |
|----------------------------|--------------|--------|
| No | N/A | Pass |
| Yes | Yes | Pass + Auto-log to `docs/governance-audit.md` |
| Yes | No | **BLOCKED** with error message |

### 18.3 Audit Log

All successful overrides are appended to [`docs/governance-audit.md`](docs/governance-audit.md) with:
- Timestamp
- Actor (git config user.name)
- Files modified
- Commit SHA
- Branch name
- Override reason

### 18.4 Enforcement

This protocol is enforced by a **pre-commit hook** (`scripts/lint/validate-root-config.ps1`) configured in `.pre-commit-config.yaml`. The hook:
- Runs on every commit
- Detects staged changes to `AGENTS.md` or `opencode.json`
- Validates the commit message for the override tag
- Blocks the commit with a clear error message if the tag is missing
- Appends an audit entry to `docs/governance-audit.md` if the tag is present

The tag is plain text and does not authenticate the committer. Agents must never add it on their own authority — only the Human CEO supplies the override reason.

### 18.5 Usage Examples

**Allowed (Human CEO operational change):**
```bash
git commit -m "Add emergency agent permission [CEO-OVERRIDE: Production incident response]"
```

**Blocked (automated/agent change without authorization):**
```bash
git commit -m "Update agent permissions"  # FAILS - no override tag
```

### 18.6 Rollback

If the hook causes issues, remove it from `.pre-commit-config.yaml` and delete `scripts/lint/validate-root-config.ps1`. The audit log at `docs/governance-audit.md` can be retained for history or archived.

## 19 Token and Context Efficiency

- Read each file once per session.
- Use grep or line ranges for big files.
- Don't re-read after an edit unless a test or build fails.
- Stop and ask after three calls with no new information.
- Put a `steps` cap on the build agent.
## 20 Deck Generation

Trigger word: `generate` (in a prompt about the pitch deck). Script: `static/brand/templates/generate-pitch-deck.py` — converts `ai_venture_studio_client_presentation.md` (Part 5) into a 13-slide PPTX using brand tokens from `brand/tokens/`.

- If `ai_venture_studio_client_presentation.md` is present and complete → run `uv run python static/brand/templates/generate-pitch-deck.py`.
- If `ai_venture_studio_client_presentation_deck_spec.md` needs review first → read the spec, verify slide count (13), then run the script.
- Before delivery, brand compliance (`brand/guidelines/brand-guidelines.md` Sec. 9) must pass → verify navy rail, color palette and type scale.
- CTO validation: PORTFOLIO D (Consumer Platforms) must appear on Slide 4, confirmed via `company-registry.yaml` agent roles.
- One source of truth: `company-registry.yaml` — agent roles and KPIs (ATC >90%, velocity <60d, correction ratio, 3x capital efficiency) are authoritative; the deck only references them.
- Brand tokens (navy #070A40, red #E63946, cyan #00BFFF) and the compliance checklist (Sec. 9) are defined in `brand/tokens/brand-tokens.json` and `brand/guidelines/brand-guidelines.md`.
