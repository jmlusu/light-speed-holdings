# PROJECT STATUS — Light Speed Holdings / AI Company Builder

> **Last verified:** 2026-08-11
> **Source of truth:** Derived from `ai-company/docs/STATUS.md`, `ai-company/docs/ARCHITECTURE.md`, `ai-company/docs/ARCHITECTURE-GAPS.md`, `ai-company/docs/AUDIT-FIXES-2026-08-10.md`, `ai-company/docs/CODE_REVIEW_2026-08-10.md`, `ai-company/docs/PRODUCT-ROADMAP.md`, and `ai-company/.ai-company/state/`. All counts re-verified against the live tree on 2026-08-11 (ruff, mypy, pytest, `ai-company --help`, git, file counts).

---

## 1. Current Architecture

The project is a **Python 3.12+ CLI tool** (`ai-company`, `pyproject.toml` version `0.1.0`, packaged with setuptools, environments managed with **uv**) that generates and orchestrates an AI agent hierarchy from YAML configuration. No web server beyond the optional FastAPI dashboard.

### Core workflow

```
company-registry.yaml (127 agents, 18 departments)
        │
        ▼
  RegistryLoader → Parser → Resolver → Validator (registry/) — anchored to package root (AI_COMPANY_ROOT override, CWD-independent)
        │
        ▼
  CompanyRegistry (Pydantic models, models/)
        │
        ├──► BootstrapEngine (builder/) → .opencode/agents/*.md via 13 Jinja2 templates
        │         └──► company/*.yaml (derived configs), company/agent-registry.json
        │
        ├──► Executor (executor/loop.py)
        │         ├──► MessageBus (orchestrator/message_bus.py) — .opencode/inbox.json via FileStore (atomic + locking)
        │         ├──► AgentLoop (executor/agent_loop.py) — ReAct, multi-turn LLM↔tool
        │         ├──► ToolRunner + HITLGate + tier_rules (5-tier classification)
        │         ├──► DeadLetterQueue, MemoryEngine recall, AuditWriter
        │         └──► CostTracker (SQLite mirror) + CircuitBreaker (llm/)
        │
        ├──► DecisionEngine (decision/), WorkflowEngine (workflow/, 9 workflows), GraphEngine (graph/, 4 graph types)
        └──► Dashboard (dashboard/) — FastAPI REST + WebSocket, 7-department KPI collectors, governance/retention
```

### Module map (`ai-company/src/ai_company/`, **182 `.py` files**, 26+ subpackages)

| Package | Purpose |
|---------|---------|
| `cli/` | Typer app — **30 top-level commands** verified 2026-08-11 (`sop`, `raci`, `sync-registry`, `generate`, `status`, `agents` [incl. `validate`], `board`, `bootstrap`, `governance`, `workflows`, `memory`, `executives`, `departments`, `doctor`, `marketing`, `sales`, `customer-success`, `legal`, `llm`, `hr`, `specialists`, `orchestrator`, `models`, `dashboard`, `executor`, `company`, `decision`, `graph`, `security`, `validate`). Lazy sub-app registration (`_LAZY_SUB_APPS`) |
| `executor/` | Agentic loop, tool runner, HITL gates, dead-letter queue, daemon, task leases + store locking |
| `llm/` | Multi-provider client, `providers/` (openai-compatible, ollama), **`oauth2.py`** (`OAuth2TokenManager`), cost tracker, circuit breaker (honors `ProviderErrorCategory`), JSON parser |
| `orchestrator/` | MessageBus, scheduler, escalation/postmortem, approval, briefing, tier rules, agent protocol |
| `models/` | ~55 Pydantic domain models + enums (split across `task.py`, `company.py`, `board.py`, `executive.py`, `department.py`, `agent.py`, `workflow.py`, etc.) |
| `registry/` | Loader, parser, resolver, validator, sync (19 YAML configs); package-root anchored |
| `builder/` + `bootstrap/` | BootstrapEngine (full company generation) + DevBootstrap (idempotent dev-machine provisioning) |
| `decision/`, `workflow/`, `graph/` | Decision, workflow, and graph engines |
| `memory/` | 6-type memory store + consolidation + vector store |
| `audit/` | JSONL audit trail (events, writer, reader, executor integration) |
| `dashboard/` | FastAPI app (fail-closed auth), REST API, WebSocket, KPI collectors, analytics, governance/retention, mobile API |
| `doctor/` | System diagnostics |
| `security/` | Secrets scanner, PII detector, memory encryption, key manager, content filter |
| `ml/` | Embeddings, anomaly detection, performance, predictive scaling, prompt optimizer |
| `services/` | Base + sales, marketing, legal, hr, customer_success |
| `data/` | SQLite-backed stores (task, memory, audit, escalation, KPI pipeline, governance, cost/agent/growth analytics) |
| `store/` | Atomic file store + file locking (msvcrt/fcntl) |
| `org_chart/` | Org chart generation + registry normalizer |
| `ai/`, `prompts/` | Eval benchmarks, prompt registry, LLM evaluators |
| `config/`, `utils/` | Config loader, logging/file utilities (structured JSON logging + correlation IDs) |

### Key runtime facts

- **127 agents** in `ai-company/company-registry.yaml`; **127 generated `.md` files** in `ai-company/.opencode/agents/` **and** root `.opencode/agents/` (the 7 legacy underscore duplicates and root-level surplus files were removed since 2026-08-07 — root now holds exactly 127).
- Agent naming convention: registry IDs use underscores (`board_chair`); generated files/config references use hyphens (`board-chair`). `ai-company validate` checks config references resolve to generated files.
- **Canonical tool vocabulary** (2026-08-10): `read` (127 agents), `edit` (120), `grep`/`list` (102), `bash` (77), `webfetch` (17), `task` (1). Legacy aliases (`websearch`/`web_search` → `webfetch`, `code_interpreter` → `bash`, `write` → `edit`, `delegate` → `task`) mapped in `generator.py::_TOOL_MAP`.
- **Shared operating standards**: `templates/agents/operating-standards.md` → `.opencode/operating-standards.md`; all 127 cards reference it instead of inlining 5 byte-identical principles. `executor/context.py` resolves principles from the shared doc with a backward-compatible fallback.
- Registry loading is **CWD-independent** (anchored to package root, `AI_COMPANY_ROOT` env override).
- Cost tracker + task/audit mirrors persist to SQLite.
- Git: branch `main`; only tag present is `recovery-2026-07-26` (docs reference a `v0.3.0` tag, not present in current repo history).

### Verified quality gates (2026-08-11)

- **pytest:** `1805/1858 tests collected` (53 e2e deselected) — no collection errors (`test_security.py`, `test_ml.py` now collect clean; 109 tests between them).
- **ruff:** clean (`All checks passed`).
- **mypy:** clean (`Success: no issues found in 181 source files`).
- **CLI:** `ai-company --help` renders 30 top-level commands.

---

## 2. Completed Work

### Milestones
- **Sprint 1 — Complete:** Code hardening + audit trail (GAP-001/002/006/011/012/014), FileStore atomic writes + locking, tier-rules integration.
- **Sprint 2 — Complete (2026-07-21):** 13/13 items; executor → MessageBus routing, non-blocking HITL gates, escalation persistence, cost tracker, shell-injection hardening (GAP-003/004/009/010/015/016).
- **Sprint 3 — Complete (2026-07-22):** 8/8 items; GAP-014/015/017/020 closure, E2E pipeline test, 30 WebSocket tests, governance CLI, memory CLI, org-chart test rewrite (56 tests). **1205 tests**.
- **Sprint 4 — Complete (2026-08-08):** Quality & completeness. GAP-019 (agent spec validation — `agents validate` CLI + `AgentContext.validate()`) **closed**, daemon lifecycle, key rotation, token counting, CLI type hints/docstrings, dashboard security hardening, 22 new agent skills + manifest, real KPI computation (`scripts/compute_company_kpis.py`), T012 `llm usage` + LLM budget caps/auto-suspend. Commits `d11608f`, `359489d`, `4765f76`. **1745 tests**.
- **Sprint 5 / T009 — Complete (2026-08-09):** OAuth2 client-credentials — `OAuth2TokenManager` (`llm/oauth2.py`), in-memory token cache with TTL, fail-closed, wired into `OpenAICompatibleProvider` + `LLMClient` (opt-in `oauth2:` block per provider). **1778 tests**.
- **Sprint 6 — Complete (2026-08-10):** Audit fixes + runtime hardening. Commits `3f587e9` (registry anchored to package root, lazy CLI, canonical tool vocabulary, operating-standards dedup), `f4d2867` (`ProviderErrorCategory`, circuit breaker ignores `auth`, bounded cost tracker), `d076303` (task leases, store locking, DLQ re-enqueue delegation), `5f32e6d` (E2E Alpine `$data` migration). ECL archived at `harness/changes/archive/2026-08-10-audit-fixes-and-runtime-hardening`. **1805 tests**. See `docs/AUDIT-FIXES-2026-08-10.md`.
- **Post-Sprint-6 commits (not yet ECL-archived):** `9c6a7d8` (CI lazy-help ANSI-safe + Reports-To drift), `80bd38f` (root-aware MessageBus/AuditWriter/service defaults), `b00acb0` (ML embedding test skip when HF download unavailable).

### Feature inventory
- **30-command CLI** surface; lazy imports keep help fast.
- **Agent ecosystem:** 127 agents / 18 departments (53-role expansion 2026-07-21); all invokable via `@` in OpenCode from workspace-level `.opencode/agents/`.
- **Governance:** autonomous GitHub Action (cron every 6 h), postmortem store/template/CLI, SOPs (incident-response, deployment, hr-onboarding, budget-approval, cost-management), RACI matrices (hiring, escalation, deployment), 5-tier approval matrix + decision framework.
- **Dashboard & analytics:** 7-department KPI collectors, company KPIs computed from live telemetry, data retention/governance engine (`run_retention()` + `GovernanceScheduler`, `GET /api/v1/governance`), adaptive polling, coalesced chart redraws, resilient WebSocket.
- **Security:** dashboard auth **fail-closed by default** (`DASHBOARD_AUTH_MODE` defaults `api_key`; mutating endpoints reject when no key configured), configurable CORS + CSP, memory encryption + HKDF key derivation, secret scanner, PII detector, content filter, OAuth2, key rotation, LLM provider error classification.
- **Observability:** structured JSON logging with correlation IDs (`logging_config.py`, `utils/logging.py`), zero `print()` in `src/`, JSONL audit trail, SQLite mirrors.
- **CI/CD:** ruff, mypy, pytest + **72% coverage gate**, `uv audit` dependency check, **generated-files drift check**, Dependabot (weekly, GitHub Actions + pip), bandit, harness lint, quality-gate aggregator job.
- **Engineering:** uv package manager, pre-commit hooks, DevBootstrap provisioning, ECL change harness.

### Gap closure (`ARCHITECTURE-GAPS.md` — 20 gaps)
- **RESOLVED (20/20):** GAP-001…GAP-020. GAP-019 (agent spec validation) closed in Sprint 4 — `agents validate` CLI exists (`cli/agents.py:78`) and `AgentContext.validate()` runs per spec.
- ⚠️ `ARCHITECTURE-GAPS.md` summary table still lists GAP-019 as 🔴 Open — **stale; the live CLI has the command** (see Technical Debt → doc drift).

### Code review (2026-08-10) — `docs/CODE_REVIEW_2026-08-10.md`
- Maturity score **B+ / 8.2** (Architecture 8.5, Code Quality 8.0, Testing 8.0, Security 7.5, DevOps 8.5, Docs 8.5). Project would reach **A- / 9.0** once short-term recommendations are addressed.
- **Resolved since the review:** dashboard auth fail-closed default (was HIGH) — `app.py:7-10,168`; test collection errors in `test_security.py`/`test_ml.py` (was MEDIUM) — both collect clean (109 tests).

---

## 3. Technical Debt

Source: `ai-company/.ai-company/state/TECH_DEBT.md` (TD-1…TD-10, stale as of 2026-07-16) + fresh findings + code-review follow-ups.

| ID | Debt | Status (2026-08-11) |
|----|------|---------------------|
| TD-1 | Ruff `E402` imports in `llm/client.py` | ✅ Resolved — ruff clean on full `src/` |
| TD-2 | Legacy root `src/ai_company/` staging area | ❌ Open — remove; confusing duplication |
| TD-3 | Two `.venv` dirs (root + `ai-company/`) | ❌ Open — root env used by `daily-check.ps1` |
| TD-4 | `models.py` single file (~607 lines) | 🔶 Partially split (`models/task.py`, `company.py`, etc.); finish migration |
| TD-5 | Memory engine uses direct file I/O | ❌ Open — should route through `store/file_store.py` |
| TD-6 | No Dependabot | ✅ Resolved — `.github/dependabot.yml` (weekly, GitHub Actions + pip) |
| TD-7 | No coverage threshold in CI | ✅ Resolved — 72% gate in `ci.yml` |
| TD-8 | No hash-check on generated files | ✅ Resolved — `generated-check` CI job (`git diff --exit-code`) |
| TD-9 | Dashboard known-issue backlog | 🔶 Mostly resolved (adaptive polling, coalesced redraws, resilient WS); residual polish |
| TD-10 | No pre-commit enforcement in CI | 🔶 Partial — hooks local only; bandit + ruff + mypy run as CI jobs instead |
| NEW | **Runtime tool-vocabulary gap** — `executor/tool_runner.py` still includes `code_interpreter`; no `webfetch`/`web_search` runtime tool, while cards advertise `webfetch` | Flagged in AUDIT-FIXES as pre-existing follow-up |
| NEW | **Legacy module duplication** — `builder.py`, `registry.py`, `graph.py` coexist with packages | Code review finding #2 (HIGH); deprecate or remove |
| NEW | **HITL approval expiry sweep** — pending approvals never auto-expire | Code review finding #5 (MEDIUM) |
| NEW | **mypy not strict** — `warn_return_any` off; stubs missing for sentence-transformers/scikit-learn | Code review finding #6 (MEDIUM) |
| NEW | **Coverage target** 72% < 80% goal (target 85% on executor/LLM/HITL) | Code review recommendation #6 |
| NEW | **Generator duplication** — `_render_agent()` helper not extracted (`generator.py:248-346`) | Code review finding #7 (LOW) |
| NEW | **Doc drift** — `ARCHITECTURE-GAPS.md` summary still marks GAP-019 open; README cites "1528 tests passing" and "1494 tests" comment (actual 1805); `.ai-company/state/*` (ROADMAP, TECH_DEBT, NEXT_ACTIONS, CURRENT_SPRINT) stale since 2026-07-16/17 | Reconcile next doc pass |
| NEW | **Version/release drift** — `pyproject.toml` version `0.1.0`; docs reference `v0.3.0` tag; only git tag present is `recovery-2026-07-26` | Decide canonical versioning; consider re-tag |
| NEW | **In-flight uncommitted work** — 4 workflow files modified: `astral-sh/setup-uv@v6` → `@v7` (`.github/workflows/{autonomous,ci,monitoring,release}.yml`) | Commit/park |

---

## 4. Roadmap

Source: `ai-company/docs/PRODUCT-ROADMAP.md` (bi-weekly review, owner CPO) + `.ai-company/state/ROADMAP.md` (stale) + `docs/CODE_REVIEW_2026-08-10.md` roadmap.

| Phase | Name | Theme | Status |
|-------|------|-------|--------|
| 1 | Foundation | Structure, CLI, registry, generator | ✅ Complete |
| 2 | Core Operations | MessageBus, models, orchestrator, tests | ✅ Complete |
| 3 | Growth Functions | Marketing, Sales, CS, Legal, HR modules | ✅ Substantially complete (all 5 service modules + KPIs) |
| 4 | Specialist Agents | Financial analyst, DevOps, data scientist, compliance | ✅ Mostly complete via 53-role expansion |
| 5 | Autonomous Coordination | Scheduled cycles, escalation, approval gates, self-healing | 🔶 Partial — 6 h GitHub Actions cycle + daemon exist; scheduled-cycle daemon mode (S3-06) deferred |
| 6 | Self-Improving | Learning, feedback loops, agent-led improvement | ⬜ Planned |
| — | **Sprint 7 (next)** | Code-review follow-ups + tool-vocabulary runtime sync | 🟡 NOT STARTED (proposed scope below) |

### Sprint status
| Sprint | Status | Tests | Notes |
|--------|--------|-------|-------|
| 1 | ✅ COMPLETE | — | Code hardening + audit trail |
| 2 | ✅ COMPLETE | 1093 | 13 items |
| 3 | ✅ COMPLETE | 1205 | 8 items |
| 4 | ✅ COMPLETE | 1745 | Quality & completeness (GAP-019) |
| 5 | ✅ COMPLETE | 1778 | T009 OAuth2 client-credentials |
| 6 | ✅ COMPLETE | 1805 | Audit fixes + runtime hardening |

### Deferred / open items (from `docs/STATUS.md` Remaining Work)
- Scheduled-cycle daemon mode (S3-06).
- Runtime tool-vocabulary sync (`executor/tool_runner.py` — implement `webfetch`/`web_search`, remove `code_interpreter`).
- Code-review follow-ups (`docs/CODE_REVIEW_2026-08-10.md`): dashboard auth fail-closed default (✅ done), HITL approval expiry sweep, legacy module deprecation, mypy strict mode.

### Code-review recommendations roadmap
- **Short-term (1-2 sprints):** dashboard auth fail-closed (✅ done); HITL expiration sweep; remove/deprecate legacy modules.
- **Medium-term (2-4 sprints):** mypy `warn_return_any` + type stubs; coverage 72% → 80% (>85% executor/LLM/HITL); property-based tests (Hypothesis for MessageBus/ApprovalGate/EscalationManager); `_render_agent()` refactor.
- **Long-term (4+ sprints):** end-to-end stress test (FileStore locking under load); CD pipeline to staging on merge to main; async executor consideration.

### Backlog
- `ai-company/docs/BACKLOG.md`: 48 items / 267 pts (MoSCoW), M/S-series mapped to GAPs.
- `ai-company/docs/PHASE-4-PLAN.md`, `PHASE-5-PLAN.md`: Phase 5 autonomous coordination plans.
- `ai-company/.ai-company/state/NEXT_ACTIONS.md`: performance analytics, adaptive workflows, multi-tenant, plugin architecture, marketplace (stale — re-groom).

---

## 5. Priorities

1. **Commit/park in-flight CI bump** — `setup-uv` v6→v7 across 4 workflow files (currently uncommitted).
2. **Runtime tool-vocabulary sync** — align `executor/tool_runner.py` with the canonical card vocabulary (`webfetch`/`web_search`, drop `code_interpreter`).
3. **HITL approval expiry sweep** — auto-reject/expire pending approvals (code-review #5).
4. **Deprecate legacy modules** — `builder.py`, `registry.py`, `graph.py` (code-review #2).
5. **Quality hardening** — mypy strict (`warn_return_any`), coverage 72% → 80%, property-based tests.
6. **Doc reconciliation** — fix stale `ARCHITECTURE-GAPS.md` (GAP-019), README test counts, `.ai-company/state/*`; decide canonical version/tag story.
7. **Re-open ECL cycle** — next active change via harness (`lint-ecl.ps1`) covering items 2-6.
8. **Phase 5/6 backlog** — scheduled-cycle daemon mode, performance analytics, CD pipeline, stress test, async executor (long-term).

---

## 6. Known Issues

| Severity | Issue | Status / Source |
|----------|-------|-----------------|
| HIGH | Runtime tool set mismatch — cards advertise `webfetch` but `tool_runner.py` has no matching tool; still exposes `code_interpreter` | `docs/AUDIT-FIXES-2026-08-10.md` (flagged follow-up); not yet fixed |
| HIGH | Legacy modules (`builder.py`, `registry.py`, `graph.py`) coexist with modern packages | `docs/CODE_REVIEW_2026-08-10.md` finding #2 |
| MED | HITL approvals can remain pending forever (no expiry sweep) | Code review finding #5 |
| MED | Mypy not strict; broad `except Exception` in some critical paths at DEBUG level | Code review findings #3/#6 |
| MED | Concurrent dashboard API + executor writes can clobber shared JSON/YAML state outside the MessageBus path | GAP-002 residue; `store/file_store.py` atomic writes exist but not applied everywhere |
| LOW | `models.py` still large; memory engine bypasses `file_store.py` | TD-4, TD-5 |
| LOW | `board-chair` card missing `reports_to` (1 validation warning) | `agents validate` — pre-existing |
| LOW | Doc drift: GAP-019 marked open in ARCHITECTURE-GAPS.md; README test counts stale (1528/1494 vs 1805); `.ai-company/state/*` stale; version tag drift (`0.1.0` in pyproject, no `v0.3.0` tag) | Verified 2026-08-11 |
| INFO | 4 workflow files modified but uncommitted (`setup-uv` v6→v7) | `git status` 2026-08-11 |
| FIXED | Dashboard auto-scroll instability / chart flicker / WS disconnect loops | Resolved 2026-08-07 — adaptive polling, coalesced redraws, resilient WebSocket (`ccf1650`) |
| FIXED | Executor bypassed MessageBus (direct `inbox.json` I/O) | GAP-001 — all inbox I/O via `self.bus.*` |
| FIXED | Dashboard auth fail-open default | Resolved — `DASHBOARD_AUTH_MODE` defaults `api_key`; mutating endpoints reject without key |
| FIXED | S3-05 LLM retry provider cycling (always hit provider 0) | Fixed 2026-07-22; round-robin locked by `test_llm.py` |
| FIXED | `inbox.json` test pollution from marketing-service | Purged 2026-08-07 |

---

## 7. Operational Instructions

### Project roots
- **Repo root:** `C:\Users\jmlus\light-speed-holdings` (Windows path — never `/workspace/...`).
- **Active project:** `ai-company/` (pyproject.toml, uv.lock, `.venv`, src/, tests/).
- **Planning/docs:** `ai-company/docs/` (STATUS, ARCHITECTURE, ARCHITECTURE-GAPS, PRODUCT-ROADMAP, BACKLOG, AUDIT-FIXES-2026-08-10, CODE_REVIEW-2026-08-10, ECL, SPRINT-*).
- **Change harness (ECL):** `ai-company/harness/` — currently inactive (Sprint 6 archived 2026-08-10). Active-change files (if any) take precedence over this document.

### Daily ops
```powershell
cd ai-company
.\scripts\dev.ps1            # venv + deps + lint + tests + agent regen
.\scripts\dev.ps1 status     # project status
.\scripts\dev.ps1 test       # test suite
.\scripts\dev.ps1 lint       # ruff + mypy
# or
uv run ai-company --help     # CLI entry point (30 commands)
uv run ai-company doctor run # diagnostics
uv run ai-company agents list
uv run ai-company agents validate  # spec validation (GAP-019)
```
Root-level `daily-check.ps1` runs `doctor run` + `agents list` and flags pending CI secrets.

### Manual setup (fresh machine)
```bash
cd ai-company
uv sync --extra dev            # install project + dev deps (respects uv.lock)
pre-commit install             # hooks: ruff, mypy, bandit, yaml, whitespace
uv run ai-company bootstrap    # or automated DevBootstrap
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
- **`ci.yml`** (root): jobs `lint`, `typecheck`, `test` (with 72% coverage gate), `harness`, `security` (bandit), `dependencies` (`uv audit`), `generated-check`, `gate`. (Old `ai-company/.github/workflows/` copies deleted.)
- **`monitoring.yml`** (root): CI health alert issue creation + cycle check.
- **`release.yml`** (root): release pipeline.
- **Dependabot:** weekly updates for GitHub Actions + pip (`/ai-company`).
- **Pre-commit:** `pre-commit run --all-files`.

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
- Generated `.opencode/agents/*.md` files are regenerated from the registry — do not hand-edit (CI `generated-check` will fail on drift).
