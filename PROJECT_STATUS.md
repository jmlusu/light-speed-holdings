# PROJECT STATUS — Light Speed Holdings / AI Company Builder

> **Last verified:** 2026-08-07
> **Source of truth:** This file is derived from `ai-company/docs/STATUS.md`, `ai-company/docs/ARCHITECTURE-GAPS.md`, `ai-company/docs/PRODUCT-ROADMAP.md`, and `ai-company/.ai-company/state/`. All counts below were re-verified against the live tree on 2026-08-07.

---

## 1. Current Architecture

The project is a **Python 3.12+ CLI tool** (`ai-company`, v0.1.0, packaged with setuptools, environments managed with **uv**) that generates and orchestrates an AI agent hierarchy from YAML configuration.

### Core workflow

```
company-registry.yaml (127 agents, 18 departments)
        │
        ▼
  RegistryLoader → Parser → Resolver → Validator (registry/)
        │
        ▼
  CompanyRegistry (Pydantic models, models/models.py)
        │
        ├──► BootstrapEngine (builder/) → .opencode/agents/*.md via 13 Jinja2 templates
        │         └──► company/*.yaml (derived configs)
        │
        ├──► Executor (executor/loop.py)
        │         ├──► MessageBus (orchestrator/message_bus.py) — .opencode/inbox.json
        │         ├──► AgentLoop (executor/agent_loop.py) — ReAct, multi-turn LLM↔tool
        │         ├──► ToolRunner + HITLGate + tier_rules (5-tier classification)
        │         ├──► DeadLetterQueue, MemoryEngine recall, AuditWriter
        │         └──► CostTracker + CircuitBreaker (llm/)
        │
        ├──► DecisionEngine (decision/) — approvals, risk assessment, decision trees
        ├──► WorkflowEngine (workflow/) — 9 workflows, step tracking, SLA
        ├──► GraphEngine (graph/) — 4 graph types, BFS pathfinding
        └──► Dashboard (dashboard/) — FastAPI REST + WebSocket, 7-department KPI collectors
```

### Module map (`ai-company/src/ai_company/`, 175 `.py` files, 26 subpackages)

| Package | Purpose |
|---------|---------|
| `cli/` | Typer app — **29 top-level commands** (24 Typer groups + 5 direct: `sop`, `raci`, `sync-registry`, `generate`, `status`) |
| `executor/` | Agentic loop, tool runner, HITL gates, dead-letter queue, daemon |
| `llm/` | Multi-provider client (base, ollama, openai-compatible), cost tracker, circuit breaker, JSON parser |
| `orchestrator/` | MessageBus, scheduler, escalation/postmortem, approval, briefing, tier rules, agent protocol |
| `models/` | ~55 Pydantic domain models + 8 enums |
| `registry/` | Loader, parser, resolver, validator, sync (19 YAML configs) |
| `builder/` + `bootstrap/` | BootstrapEngine (full company generation) + **DevBootstrap** (idempotent dev-machine provisioning, new) |
| `decision/`, `workflow/`, `graph/` | Decision, workflow, and graph engines |
| `memory/` | 6-type memory store (episodic, semantic, procedural, relational, temporal, aggregate) + consolidation + vector store |
| `audit/` | JSONL audit trail (events, writer, reader, executor integration) |
| `dashboard/` | FastAPI app, REST API, WebSocket, KPI collectors, analytics, retention, mobile API |
| `doctor/` | System diagnostics |
| `security/` | Secrets scanner, PII detector, memory encryption, key manager, content filter |
| `ml/` | Embeddings, anomaly detection, performance, predictive scaling, prompt optimizer |
| `services/` | Base + sales, marketing, legal, hr, customer_success |
| `data/` | SQLite-backed stores (task, memory, audit, escalation, KPI pipeline, governance, cost/agent/growth analytics) |
| `store/` | Atomic file store + file locking (msvcrt/fcntl) |
| `org_chart/` | Org chart generation + registry normalizer |
| `ai/`, `prompts/` | Eval benchmarks, prompt registry, LLM evaluators |
| `config/`, `utils/` | Config loader, logging/file utilities |

### Key runtime facts

- **127 agents** defined in `ai-company/company-registry.yaml`, 127 generated `.md` files in `ai-company/.opencode/agents/` — registry → JSON → generated agents are in sync.
- Agent naming convention: registry IDs use underscores (`board_chair`), generated files and config references use hyphens (`board-chair`). `ai-company validate` checks config references resolve to generated files.
- Root `.opencode/agents/` still holds **134 `.md` files** — 127 canonical (duplicates of `ai-company/.opencode/agents/`) + **7 legacy underscore duplicates** (`compliance_officer`, `customer_success_owner`, `data_scientist`, `employee_experience_lead`, `financial_analyst`, `industry_analyst_relations_manager`, `learning_development_lead`) that are byte-identical to their hyphen-named counterparts.
- Cost tracker persists to SQLite (migrated 2026-07-23).

### Verified quality gates (2026-08-07)

- **pytest:** 1494 tests collected (`tests/` — 78 unit, 13 integration, 4 e2e, 1 performance, 9 root-level).
- **ruff:** clean (`All checks passed`).
- **mypy:** clean (`Success: no issues found in 177 source files`).

---

## 2. Completed Work

### Milestones
- **Sprint 1 — Complete:** Code hardening + audit trail (Track B/C), file store with atomic writes + locking, tier rules integration.
- **Sprint 2 — Complete:** 13/13 items done (2026-07-21); executor → MessageBus routing, HITL non-blocking gates, escalation persistence, cost tracker.
- **Sprint 3 — Complete:** 8/8 items done (2026-07-22); GAP-014/015 closure, E2E pipeline test, 30 WebSocket tests, governance CLI (7 commands), memory CLI, dashboard API tests, org-chart test rewrite (832 lines, 56 tests). **v0.3.0 tagged 2026-07-22.**
- **Sprint 4 — NOT STARTED.**

### Feature inventory
- 29-command CLI surface, 7 department KPI collectors (engineering, hr, marketing, sales, customer_success, legal, finance).
- Governance layer: autonomous GitHub Action (cron every 6 h), postmortem store/template/CLI, SOPs (incident-response, deployment, hr-onboarding, budget-approval), RACI matrices (hiring, escalation, deployment).
- Agent ecosystem: **53 new roles added 2026-07-21** across all departments (4 phases); all 127 agents deployed and invokable via `@` in OpenCode.
- Security: memory encryption + HKDF key derivation (salt mixing removed), InvalidTag catch on decrypt, blind `Exception` → specific `ValueError`/`OSError` cleanup, secret scanner, PII detector, content filter.
- Engineering: migrated to **uv** package manager (2026-08-06), ruff exception-handling rules applied, runtime/generated artifacts untracked, DevBootstrap provisioning added (new, uncommitted).

### Gap closure (ARCHITECTURE-GAPS.md — 20 gaps)
- **RESOLVED (16):** GAP-001, 002, 003, 004, 006, 007, 008, 009, 010, 012, 013, 014, 015, 016, 017, 020. GAP-001 closed 2026-08-07 — executor routes all inbox I/O through `MessageBus` (`loop.py:197,223,247,297,382,424`).
- **PARTIAL (3):** GAP-005 (memory consolidation scheduler wired into the executor loop; cadence verification pending), GAP-011 (read paths still bypass MessageBus), GAP-018 (structured logging).
- **OPEN (1):** GAP-019 (agent spec validation).

---

## 3. Technical Debt

Source: `.ai-company/state/TECH_DEBT.md` (TD-1…TD-10) + fresh findings.

| ID | Debt | Notes |
|----|------|-------|
| TD-1 | Ruff `E402` imports in `llm/client.py` | Reported fixed 2026-07-17; re-verify |
| TD-2 | Legacy root `src/ai_company/` staging area | README says "ignore; has syntax errors"; confusing duplication |
| TD-3 | Two `.venv` dirs (root + `ai-company/`) | Root `.venv` is used by daily-check.ps1; `ai-company/.venv` is the uv-managed project env |
| TD-4 | `models.py` is ~607 lines with ~55 classes | Being split per-domain (models/task.py, company.py, etc.); migration partially done |
| TD-5 | Memory uses direct file I/O | Should route through store/file_store.py |
| TD-6 | No Dependabot / dependency update automation | `safety` available but not wired to CI |
| TD-7 | No coverage threshold in CI | pytest-cov installed; not enforced |
| TD-8 | No hash-check on generated files | Generator output drift not detected automatically |
| TD-9 | Dashboard known-issue backlog | P0: auto-scroll instability (see Known Issues) |
| TD-10 | No pre-commit enforcement on all paths | Hooks installed locally; not a CI gate |
| — | README test counts | Fixed 2026-08-07 — README now cites 1494 tests (was "727 passing" / "Run all 1408 tests") |
| — | Stale/duplicate artifacts | Root `.opencode/agents/` (134 vs 127), `agent-list.txt` (legacy `spec_*`/`board-*` names), root `orchestrator/` data dir, `.bak` files |
| — | Data hygiene | `.opencode/inbox.json` contains test/pollution tasks from `marketing-service`; `harness/` ECL is initialized but inactive (INDEX.json `[]`, no active change, no pending evolution) |
| — | Doc drift (partially fixed 2026-08-07) | Root README/AGENTS.md links repointed to `ai-company/docs/`; `ai-company/docs/DEVELOPMENT.md` created; gap statuses + test counts reconciled. Remaining: several planning docs still stale vs. per-item status flags |
| — | In-flight uncommitted work | Modified: `.github/workflows/autonomous.yml`, `daily-check.ps1`; deleted `ai-company/.github/workflows/{autonomous,ci}.yml`; untracked `bootstrap/`, `cli/bootstrap.py`, `test_dev_bootstrap.py` |

---

## 4. Roadmap

Source: `ai-company/docs/PRODUCT-ROADMAP.md` (bi-weekly review, owner CPO) + `.ai-company/state/ROADMAP.md`.

| Phase | Name | Theme | Status |
|-------|------|-------|--------|
| 1 | Foundation | Structure, CLI, registry, generator | ✅ Complete |
| 2 | Core Operations | MessageBus, models, orchestrator, tests | ✅ Complete |
| 3 | Growth Functions | Marketing, Sales, CS, Legal, HR modules | ✅ Substantially complete (all 5 service modules + KPIs exist) |
| 4 | Specialist Agents | Financial analyst, DevOps, data scientist, compliance | Mostly complete via 53-role expansion |
| 5 | Autonomous Coordination | Scheduled cycles, escalation, approval gates, self-healing | Partial — 6 h GitHub Actions cycle exists (autonomous.yml) |
| 6 | Self-Improving | Learning, feedback loops, agent-led improvement | Planned |
| — | **Sprint 4** | **Quality & completeness** | 🔴 **NOT STARTED** |

### Sprint 4 scope (from `ai-company/docs/CHANGELOG.md` Unreleased + STATUS.md)
- Structured logging with correlation IDs (GAP-018)
- Scheduled cycle daemon mode (S3-06)
- Agent spec validation CLI
- CLI type hints/docstrings
- OAuth2 / key rotation
- Memory encryption (partially done — `security/memory_encryption.py` exists)
- Token counting integration

### Phase 5/6 backlog (from `.ai-company/state/NEXT_ACTIONS.md`)
- Performance analytics, adaptive workflows, multi-tenant support, plugin architecture, marketplace.

### Backlog
- `ai-company/docs/BACKLOG.md`: 48 items / 267 pts (MoSCoW), M/S-series items mapped to GAPs.
- `ai-company/docs/PHASE-4-PLAN.md`, `PHASE-5-PLAN.md`: Phase 5 autonomous coordination planned.

---

## 5. Priorities

1. **Commit/park in-flight work** — bootstrap feature (DevBootstrap + CLI + tests), workflow file moves, `daily-check.ps1` change. These are uncommitted and would be lost on any destructive operation.
2. **Start Sprint 4 (quality & completeness)** — highest-value items: structured logging w/ correlation IDs, agent spec validation CLI, token counting. (Backlog: 48 items/267 pts.)
3. **GAP-001 closed** (2026-08-07) — executor routes all inbox I/O through `MessageBus` (`loop.py:197,223,247,297,382,424`).
4. **Finish GAP-005/GAP-011** — verify consolidation cadence (scheduler wired in `loop.py:201-202`); move dashboard/mobile read paths through MessageBus.
5. **Dashboard P0 stability** — auto-scroll/flicker/WebSocket-reconnect issues (see Known Issues).
6. **Doc reconciliation wrap-up** — links fixed, `DEVELOPMENT.md` created, gap/test counts corrected. Remaining manual ops: delete `agent-list.txt`, dedupe root `.opencode/agents/` (7 legacy underscore files), purge test-polluted `ai-company/.opencode/inbox.json` (backup first).
7. **Ops** — configure GEMINI_API_KEY + KIMI_API_KEY as GitHub Actions secrets (pending since 2026-08-13 reminder in `daily-check.ps1`).
8. **CI hardening** — coverage gate, Dependabot, generated-file hash check, safety scan in CI.

---

## 6. Known Issues

| Severity | Issue | Status / Source |
|----------|-------|-----------------|
| P0 | Dashboard auto-scroll instability — kanban jumping, table re-render, chart flicker, WebSocket disconnects, silent API failures, reconnect loops | `docs/QA-DASHBOARD-STABILIZATION.md`; root causes identified (10 s polling, chart destroy/recreate, no scroll guards); e2e coverage exists |
| FIXED | Executor bypassed MessageBus — direct `inbox.json` reads/writes in the executor | GAP-001; resolved 2026-08-07 — all inbox I/O now via `self.bus.*` (`loop.py:197,223,247,297,382,424`) |
| HIGH | Concurrent dashboard API + executor writes can clobber shared JSON/YAML state | GAP-002 residue; `store/file_store.py` atomic writes exist but not applied everywhere |
| MED | HITL gate blocks executor thread up to 30 min per approval | README known gap; non-blocking via `concurrent.futures.Future` implemented — verify |
| MED | WebSocket broadcast functions exist but were not called | README known gap; dashboard WS integration tests added in Sprint 3 — verify |
| MED | Dashboard CORS/auth posture historically lax | README said "all origins, no auth"; `app.py` now has `X-API-Key` + configurable CORS (GAP-010 resolved) — re-verify live config |
| FIXED | S3-05 LLM retry provider cycling regression — `provider_idx = attempt % len(provider_chain)` always hit provider 0 on retries | `SPRINT3-DELEGATION-SUMMARY.md`; fixed 2026-07-22 |
| OPS | GEMINI/KIMI API keys not configured in GitHub Actions | `daily-check.ps1` reminder dated 2026-08-13 |
| FIXED | Root README/AGENTS.md linked to missing root-level docs; `docs/DEVELOPMENT.md` missing | Fixed 2026-08-07 — links repointed to `ai-company/docs/`; `ai-company/docs/DEVELOPMENT.md` created |
| DATA | `inbox.json` polluted with marketing-service test tasks; `memory/` holds run/test data (not status records) | Fresh finding 2026-08-07 |

---

## 7. Operational Instructions

### Project roots
- **Repo root:** `C:\Users\jmlus\light-speed-holdings` (Windows path — never `/workspace/...`).
- **Active project:** `ai-company/` (pyproject.toml, uv.lock, `.venv`, src/, tests/).
- **Planning/docs:** `ai-company/docs/` (STATUS, ARCHITECTURE, ARCHITECTURE-GAPS, PRODUCT-ROADMAP, BACKLOG, CHANGELOG, ECL, SPRINT-*).
- **Change harness (ECL):** `ai-company/harness/` — currently inactive; active-change files (if any) take precedence over this document.

### Daily ops
```powershell
cd ai-company
.\scripts\dev.ps1            # venv + deps + lint + tests + agent regen
.\scripts\dev.ps1 status     # project status
.\scripts\dev.ps1 test       # test suite
.\scripts\dev.ps1 lint       # ruff + mypy
# or
uv run ai-company --help     # CLI entry point
uv run ai-company doctor run # diagnostics
uv run ai-company agents list
```
Root-level `daily-check.ps1` runs `doctor run` + `agents list` and flags pending CI secrets.

### Manual setup (fresh machine)
```bash
cd ai-company
uv sync --extra dev            # install project + dev deps (respects uv.lock)
pre-commit install             # hooks: ruff, mypy, bandit, yaml, whitespace
uv run ai-company bootstrap    # or automated DevBootstrap (new)
```

### Verification gates (per AGENTS.md)
| Change | Command |
|--------|---------|
| Generator/template | `uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"` |
| CLI | `ai-company --help` + `ai-company <command> --help` |
| Models/orchestrator | `uv run pytest` |
| Any source change | `uv run ruff check src/ && uv run mypy src/ && uv run pytest` |
| Harness/docs | `pwsh scripts/lint-ecl.ps1` |

### CI / automation
- **`autonomous.yml`** (root): cron every 6 h + `workflow_dispatch` (`both`/`orchestrator-only`/`executor-only`) → orchestrator tick → executor tick → briefing → uploads `ai-company/.opencode/daily_briefing.md` (30-day retention). Secrets: OPENCODE, DEEPSEEK, GEMINI, KIMI, OPENAI, ANTHROPIC API keys.
- **`ci.yml`** (root): ruff lint, mypy, pytest + quality-gate on push/PR to main. (Old `ai-company/.github/workflows/` copies were deleted; the `monitoring.yml` health-check referenced by the old ci.yml does not exist.)
- **Pre-commit:** run manually via `pre-commit run --all-files`.

### Disaster recovery / backups
```powershell
cd ai-company
.\scripts\backup.ps1                  # backup .opencode/, company/, results/
.\scripts\backup.ps1 -KeepCount 14    # keep 14 days
```

### Staging environment
```bash
docker compose -f docker-compose.staging.yml up --build                       # staging
docker compose -f docker-compose.staging.yml --profile worker up              # + worker
docker compose -f docker-compose.staging.yml --profile monitoring up          # + Prometheus
```
Staging dashboard: host port **8421** → container **8420** (production: **8420**).

### Safety rules
- Do not edit secrets, local env files, generated build outputs, or dependency folders.
- Do not hand-edit `ai-company/harness/changes/INDEX.json` — script-generated only.
- If an active ECL change exists, park/close it through the harness script before overwriting its context.
