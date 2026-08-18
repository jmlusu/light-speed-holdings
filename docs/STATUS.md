# Project Status

> If `harness/changes/active/summary.md` exists, active change files are the current task source of truth. Read them first.

## Last Updated

2026-08-18

## Current State

- **Phase B: Async Approval Engine (2026-08-17, shipped)**: Implemented suspend-to-disk for HITL-parked tasks (issue #42, T9 requirement). `SuspendStore` persists agent loop state (conversation history, iteration metadata, cost accumulators) to `.opencode/suspended_states/{task_id}.json` via atomic FileStore writes. `AgentLoop.run()` restores from `SuspendedState` on resume, continuing from the parked iteration instead of re-executing from scratch. `ApprovalNotifier` fires WebSocket broadcasts immediately on park + optional HMAC-signed webhook POST (config: `company/config/webhooks.yaml`). 30-day retention with daemon governance sweep. ADR-017 documented. 28 new tests (17 SuspendStore + 11 ApprovalNotifier), all passing. Gates: ruff/mypy clean, 1743 tests passing (1 pre-existing doc failure). ECL archived as `harness/changes/archive/2026-08-17-phase-b-async-approval-engine-42`.

- **J.A.R.V.I.S. Theme System (2026-08-17, shipped)**: Implemented the Control Plane theme across the entire CEO dashboard. CSS custom property design tokens (`control-plane-theme.css`), self-hosted Rajdhani + JetBrains Mono fonts, `.jarvis-glass` panel treatment, `.chrome-scanline` header texture, status-pulse keyframes, token-derived chart palette via `getComputedStyle`. All 7 content templates + base.html migrated from `surface-*`/`brand-*` to `jarvis-*` tokens. CSP unchanged. `prefers-reduced-motion` respected. ECL archived as `harness/changes/archive/2026-08-17-implement-j-a-r-v-i-s-theme-system-105`. Gates: ruff/mypy clean, 38 dashboard tests passing. Parent issue #105. Blocked by #101 (visual-language decision, CLOSED) and #104 (shell prototype, CLOSED).

- **v0.5.0 release (2026-08-13, shipped)**: Post-Sprint-9 hardening — dashboard RBAC (ADR-012, `src/ai_company/security/rbac.py`), SQLite-first storage experiment retired (ADR-011 superseded), workspace artifacts archived (issue #10), planning docs reconciled, CI version-check de-flaked, dependabot deps merged (#2 #3 #4 #5 #21), release pipeline fixes (Docker COPY of untracked `orchestrator/` removed, PyPI trusted-publisher config pending on pypi.org). Tagged `v0.5.0` (commit `89b20ba`, pushed with main), GitHub release published with wheel+sdist, final main CI green. See `Remaining Work` below.
- **Sprint 9 (2026-08-13) Complete**: Business architecture & master service catalog (Phase 1+2), 131-agent positioning — external messaging, strategic brief, agent-facing standards (Phase 3), recurring revenue engine — 8 recurring products, conversion framework, enterprise payment terms (Phase 4). Commits `9439316`, `77a2d08`, `5998ea9`. Plus ADR-010 (T1 event-bus alignment with report-only MessageBus perf benchmark) and ADR-011 (SQLite-first storage mirror, later retired in `83b08bb`).
- **Sprint 8 (2026-08-12) Complete**: Operationalization — inbox purge, README/env setup, Malawi service catalog portfolio launch (4 new agents, governance blocking, SOPs, client intake CLI, legal package). Archived as `harness/changes/archive/2026-08-12-sprint-8-operationalization-purge-inbox-fix-readme-env-setup-malawi-service-catalog`. v0.4.0 tagged at `3363a09`.
- **Sprint 7 (2026-08-11) Complete**: Doc reconciliation via active ECL `harness/changes/active` (`sprint-7-documentation-reconciliation-and-remaining-gap-019-fixes`). Tool vocabulary canonicalization, HITL expiry, and quality hardening completed in commit `1b30d8f`. Canonical runtime tool vocabulary = `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task` (`code_interpreter` removed; `write`/`execute`/`delegate`/`web_search` retained as backward-compatible aliases). `ApprovalGate` gains a HITL expiry sweep (expired PENDING → `EXPIRED`) wired into the daemon/governance cadence. Doc reconciliation (T002-T014) complete. All validation gates pass: lint-ecl ✅, ruff ✅, mypy ✅, pytest 1856 passed ✅, version consistency ✅. Archived as `harness/changes/archive/2026-08-11-sprint-7-documentation-reconciliation-and-remaining-gap-019-fixes`. Baseline before change: 1805/1858 tests, ruff/mypy clean.
- **v0.5.1 release (2026-08-18, shipped)**: Phase 2 Infrastructure & Quality complete — Daemon mode (S3-06/S3-07) shipped with PID management, signal handling, health status file, cross-platform stop sentinel, CLI `start --daemon`/`stop`/`status` (980 lines in `executor/daemon.py`); background schedulers (KPI snapshot, HITL expiry sweep, governance sweep) wired into daemon loop; `/api/v1/daemon/status` endpoint + WebSocket `daemon` topic broadcast added to dashboard; 31 daemon tests passing. **mypy strict mode enabled** — ~90 errors fixed across 20+ files (bare `dict` → `dict[str, Any]`, missing return types, untyped `**kwargs`, unused `type: ignore` removal). Gates: ruff/mypy clean (180 files), 1878 tests passing (3 pre-existing async failures). Tagged `v0.5.1` (commit TBD), GitHub release pending.
- **Sprint 6 (2026-08-10) Complete**: Audit fixes + runtime hardening. Archived as `harness/changes/archive/2026-08-10-audit-fixes-and-runtime-hardening`. Registry loading anchored to the package root (`AI_COMPANY_ROOT` override, CWD-independent), lazy CLI sub-app registration, tool-vocabulary canonicalized across all 127 agent cards (`websearch`/`web_search` → `webfetch`, `code_interpreter` → `bash`, `write` → `edit`, `delegate` → `task`), Operating Principles deduplicated into shared `operating-standards.md`. LLM error classification (`ProviderErrorCategory`; circuit breaker ignores `auth`), bounded cost/decision logs, task lease fields + store locking, DLQ re-enqueue delegation, E2E Alpine `$data` migration. Commits `3f587e9`, `f4d2867`, `d076303`, `5f32e6d`. **1805 tests passing**, ruff/mypy clean. See `docs/AUDIT-FIXES-2026-08-10.md`.
- **Sprint 5 (T009) Complete**: OAuth2 client-credentials auth (2026-08-09). Archived as `harness/changes/archive/2026-08-09-sprint-5-t009-oauth2-client-credentials`. New `src/ai_company/llm/oauth2.py` — `OAuth2TokenManager` (client-credentials grant, in-memory token cache with TTL, fail-closed), wired into `OpenAICompatibleProvider` (per-request bearer token) and `LLMClient` (opt-in `oauth2:` block per provider in `company/models.yaml`). `ProviderConfig` extended. 11 new tests. 1778 tests passing, ruff/mypy clean.
- **Sprint 4 Complete**: Quality & completeness (2026-08-08). Archived as `harness/changes/archive/2026-08-08-sprint-4-quality-completeness`. Commits `d11608f` (auth hardening, key rotation, token counting, CLI polish), `359489d` (platform-independent CLI help + daemon stop tests), `4765f76` (22 new agent skills + real KPI derivation). 1745 tests passing, ruff/mypy clean.
- **CEO Dashboard Operationalization Plan**: Sprint 3 complete (items 1-3). See `docs/CEO-DASHBOARD-OPERATIONALIZATION-PLAN.md`. Latest work (2026-08-07): data retention / governance engine wired end-to-end — `run_retention()` + `GovernanceScheduler` in `data/governance.py` (batched archive fix, rowid anonymize fix), daemon enforcement via `--governance-interval`, and `GET /api/v1/governance` report endpoint. 1526 tests passing.
- **Sprint 1 Complete**: All critical code hardening and audit trail work done.
- **Sprint 2 Complete**: All 13 Sprint 2 items done and verified — code audit confirmed implementation in source, documentation sync completed 2026-07-21.
- **Sprint 3 Complete**: All 8 Sprint 3 items done — gap closure (GAP-014, GAP-015), E2E pipeline test, WebSocket tests, governance CLI, memory CLI, dashboard API tests, org chart test rewrite. 1205 tests passing. v0.3.0 release tagged 2026-07-22.
- **Agent Deployment**: All 131 agents deployed to workspace-level `.opencode/agents/` — every agent now invokable via `@` in terminal.
- **Organization Expansion**: 53 new roles added across all departments (2026-07-21) — competitive edge roles identified by CEO Advisor, CAIO, CISO, COO, CPO, CTO, CSO, General, and Human CEO agents.
- **Models**: 17+ Pydantic models in `src/ai_company/models/models.py` (Company, Executive, Department, Agent, Workflow, Task, Risk, Decision, Postmortem, etc.)
- **Registry**: 4-module system — `registry/loader.py`, `parser.py`, `resolver.py`, `validator.py` — loads 19 YAML config files into typed `CompanyRegistry`.
- **Templates**: 12 Jinja2 templates — `base.md.j2`, `executive.md.j2`, `department.md.j2`, `specialist_v2.md.j2`, `board_v2.md.j2`, `workflow.md.j2`, `config.md.j2`, `postmortem.md.j2`, `sop.md.j2`, `raci.md.j2`, `agent.md.j2`, and one additional template.
- **Generator**: Template selection by agent type + `generate_from_registry()` for full registry-based generation.
- **BootstrapEngine**: `builder/__init__.py` — creates 24 directories, generates agents + configs from registry.
- **Executor**: `executor/loop.py` — polls inbox.json, runs AgentLoop (multi-turn ReAct), dead-letter queue, memory recall, audit logging.
- **AgentLoop**: `executor/agent_loop.py` — ReAct pattern, multi-turn LLM↔tool interaction, cost tracking, HITL gates, budget enforcement.
- **DecisionEngine**: `decision/engine.py` — evaluates actions against approval matrix, risk assessment, decision tree navigation.
- **WorkflowEngine**: `workflow/engine.py` — 9 workflow definitions, step tracking, SLA monitoring, task conversion.
- **MemoryEngine**: `memory/engine.py` — 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate) with persistence + executor integration.
- **GraphEngine**: `graph/engine.py` — 4 graph types (org_chart, decision_graph, workflow_graph, knowledge_graph) with BFS pathfinding.
- **Audit Trail**: `audit/` — AuditEvent, AuditWriter, AuditReader with executor integration (tool calls, task lifecycle, HITL decisions).
- **Dead-Letter Queue**: `executor/dead_letter.py` — stale task detection, DLQ with retry.
- **Circuit Breaker**: `llm/circuit_breaker.py` — LLM provider fail-fast after N errors.
- **Cost Tracker**: `llm/cost_tracker.py` — JSONL logging, daily/task budgets, per-model pricing.
- **Postmortem**: `orchestrator/escalation.py` — Postmortem + PostmortemStore models for incident tracking, resolution, and template rendering.
- **KPIs**: `company/config/kpis.yaml` — Department-level KPI definitions for 7 departments (engineering, hr, marketing, sales, customer_success, legal, finance).
- **KPI Collectors**: `dashboard/kpis/__init__.py` — All 7 department collectors wired and operational.
- **Analytics**: `dashboard/analytics.py` — History tracking, trend analysis, alert rules, summary rollups.
- **CLI**: 30 commands registered (5 root + 25 lazy sub-apps) — root: generate, status, sop, raci, sync-registry; lazy: company, decision, graph, workflows, memory, agents, board, departments, executives, specialists, orchestrator (with postmortem sub-app), models, dashboard (with kpi sub-app), executor, doctor, marketing, sales, customer-success, legal, hr, llm, bootstrap, security, validate, governance (report/audit-trail/risk-summary/retention/compliance/owners/policies).
- **FileStore**: `src/ai_company/store/file_store.py` exists with atomic writes (temp + rename) and platform-aware locking.
- **MessageBus**: `get_pending_tasks()` and `update_task_status()` present; executor routes all inbox I/O through it. WebSocket broadcast hooks present.
- **ToolRunner**: uses `shlex.split()` (no `shell=True`), consults `tier_rules.classify_tool_action()`, and logs via `log_tool_call()` / `log_hitl_decision()`.
- **HITLGate**: non-blocking via `concurrent.futures.Future` (`request_and_wait`).
- **Dashboard**: `app.py` has `X-API-Key` auth + configurable CORS. `ws.py` has broadcast functions (task/KPI/alert/escalation).
- **Escalation**: events persisted to YAML via `_save_config()` / `_load_config()`.
- **Tests**: 1743 tests passing (1 pre-existing doc failure) — as of 2026-08-17.

## Organization Expansion (2026-07-21)

### New Roles Added (53 total)

| Phase | Roles | Department | Priority |
|-------|-------|-----------|----------|
| **Phase 1: Immediate** | VP of Engineering, Data Engineer, AI Safety Lead, Program Manager, UX Research Lead, Technical Documentation Lead, Head of Developer Relations, Culture & Values Officer | Technology, Data, AI Research, Operations, Product, Marketing, People | Critical |
| **Phase 2: Weeks 1-8** | Red Team Engineer, Constitutional AI Owner, MLOps Engineer, Platform Engineer, Product Marketing Manager, Head of Business Development, Head of Competitive Intelligence, AI Security Specialist, Penetration Testing Lead, Incident Response Lead, DevSecOps Lead, Growth PM, DX Engineer, Product Designer, Eval Benchmarks Engineer, Prompt Engineer | AI Research, Technology, Marketing, Business Dev, Security, Product | Critical/High |
| **Phase 3: Weeks 9-16** | Frontend Architect, API Architect, Observability Engineer, Scalability Architect, Data Privacy Officer, Supply Chain Security Engineer, Security Architect, SOC 2 Analyst, Vendor Manager, Capacity Planner, Business Continuity Manager | Technology, Legal, Security, Operations | High |
| **Phase 4: Weeks 17-24** | Technical Writer, Learning & Development Lead, Employee Experience Lead, Investor Relations Lead, Revenue Operations Analyst, Solutions Engineer, Corporate Development Lead, Internal Comms Lead, Knowledge Manager, Process Quality Manager, Industry Analyst Relations Manager, Business Intelligence Engineer, Threat Intelligence Analyst, AI Ethics Board Chair, Human-AI Interaction Designer | Product, People, Finance, Sales, Strategy, Operations, Marketing, AI Research, Executive | High/Medium |

### Structural Improvements
- CTO span of control reduced from 9+ to 1 (VP of Engineering absorbs execution layer)
- Product department created with 8 roles under CPO
- Strategy department created with 2 roles under CSO
- Business Development function created reporting to CEO
- AI Safety hierarchy established (AI Safety Lead → Red Team, Constitutional AI, Ethics)
- **All 131 agents deployed** to workspace-level `.opencode/agents/` — fully invokable via `@`

## Code Quality

- **ruff**: ✅ Clean (0 errors) — as of 2026-08-13.
- **mypy**: ✅ Clean (0 errors) — as of 2026-08-13.
- **pytest**: ✅ 1743 tests passing — as of 2026-08-17.
- **Coverage**: ✅ 78.12% (gate: 72%) — as of 2026-08-13.
- **Dead code**: Removed 5 one-time bootstrap scripts

## Documentation

- `docs/ARCHITECTURE.md` — System architecture and module hierarchy (updated 2026-07-20)
- `docs/ARCHITECTURE-GAPS.md` — 20 identified integration gaps with severity ratings (20 resolved)
- `docs/adr/010-t1-event-bus-alignment.md`, `docs/adr/011-storage-sqlite-first-mirror.md` (superseded), `docs/adr/012-dashboard-rbac.md` — Architecture Decision Records
- `docs/INTEGRATION-ARCHITECTURE.md` — Integration seam analysis
- `docs/STATUS.md` — This file
- `docs/SPRINT-1-TRACKER.md` — Sprint 1 task tracker (COMPLETE)
- `docs/SPRINT-1-BACKLOG.md` — Sprint 1 original backlog
- `docs/SPRINT-2-BACKLOG.md` — Sprint 2 prioritized backlog (13 items, 41 hours)
- `docs/SPRINT-3-BACKLOG.md` — Sprint 3 prioritized backlog (8 items, 22 hours)
- `docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md` — CEO dashboard architecture analysis
- `docs/EXECUTIVE_DASHBOARD_V1_STRATEGIC_PLAN.md` — Executive dashboard strategic plan
- `docs/IMPLEMENTATION_SUMMARY.md` — Implementation summary
- `docs/PHASE_3_COORDINATION_PLAN.md` — Phase 3 coordination plan
- `docs/DEVELOPER-GUIDE.md` — Developer onboarding guide
- `docs/ECL.md` — Change lifecycle and context loading rules
- `docs/COMPANY-CONSTITUTION.md` — Principles and decision order
- `docs/DECISION-FRAMEWORK.md` — Decision engine rules
- `docs/ORGANIZATION.md` — Organization overview
- `docs/MODEL-ROUTING-POLICY.md` — Provider catalog, tiers, routing rules, cost control
- `docs/RISK-REGISTER.md` — 14-item risk register with mitigations and owners
- `docs/BOARD-GOVERNANCE.md` — Board charter, meeting cadence, voting rules, decision authority
- `docs/REMAINING-WORK-INVENTORY.md` — Full inventory of remaining work items
- `docs/sop-incident-response.md` — Incident response SOP
- `docs/sop-deployment.md` — Agent deployment SOP
- `docs/sop-hr-onboarding.md` — HR onboarding SOP
- `docs/sop-budget-approval.md` — Budget approval SOP
- `docs/raci-hiring.md` — RACI matrix for hiring workflow
- `docs/raci-escalation.md` — RACI matrix for escalation workflow
- `docs/raci-deployment.md` — RACI matrix for deployment workflow

## Recent Work

- **2026-08-17**: Phase B: Async Approval Engine (#42, T9) — `SuspendStore` persists agent loop state to `.opencode/suspended_states/{task_id}.json` on HITL park; `AgentLoop.run()` restores from `SuspendedState` on resume (conversation history + iteration metadata preserved, no re-execution from scratch). `ApprovalNotifier` fires WebSocket broadcast + optional HMAC-signed webhook POST (config: `company/config/webhooks.yaml`). 30-day retention with daemon sweep. ADR-017. 28 new tests. Gates: ruff/mypy clean, 1743 tests passing. ECL archived as `harness/changes/archive/2026-08-17-phase-b-async-approval-engine-42`. Also parked #40 (OTel tracing) as pending.
- **2026-08-17**: J.A.R.V.I.S. Theme System COMPLETE — Control Plane theme shipped across CEO dashboard. `control-plane-theme.css` (CSS custom properties, `.jarvis-glass`, `.chrome-scanline`, status-pulse keyframes, `@font-face`), self-hosted Rajdhani + JetBrains Mono woff2 fonts, Tailwind `jarvis.*` tokens, token-derived chart palette via `getComputedStyle`. All 7 content templates + base.html migrated from `surface-*`/`brand-*` to `jarvis-*`. CSP unchanged, `prefers-reduced-motion` respected. ECL archived as `harness/changes/archive/2026-08-17-implement-j-a-r-v-i-s-theme-system-105`. Gates: ruff/mypy clean, 38 dashboard tests passing. Parent issue #105, blocked by #101/#104.
- **2026-08-13**: Sprint 9 hardening + hard gates — dashboard RBAC (commit `c6f67e3`, ADR-012: role-gated write endpoints, loopback-restricted open mode), SQLite-first storage experiment retired (`83b08bb`, ADR-011 superseded), CI version-check de-flaked (`ccf1bbf`). Full suite 1878 passed, coverage 78.12%, ruff/mypy clean. Workspace artifacts archived (`docs/archive/2026-08-13-workspace-artifacts/`, issue #10). Planning docs reconciled (TASK-BOARD, BACKLOG, REMAINING-WORK-INVENTORY).
- **2026-08-12**: Sprint 8 COMPLETE — operationalization: inbox purge, README/env setup, Malawi service catalog portfolio (4 new agents, governance blocking, SOPs, client intake CLI, legal package). Archived ECL `2026-08-12-sprint-8-operationalization-purge-inbox-fix-readme-env-setup-malawi-service-catalog`. v0.4.0 tagged at `3363a09`.
- **2026-08-10**: Sprint 6 COMPLETE — audit fixes + runtime hardening. ECL archived as `harness/changes/archive/2026-08-10-audit-fixes-and-runtime-hardening`. Four commits: `3f587e9` (registry anchored to package root + lazy CLI + canonical tool vocabulary + shared operating-standards dedup, 145 files), `f4d2867` (LLM `ProviderErrorCategory` classification, circuit breaker ignores `auth`, bounded cost tracker, 9 files), `d076303` (task leases, store locking, DLQ delegation, bounded decision log, SQLite mirror fixes, 16 files), `5f32e6d` (E2E scroll tests migrated to Alpine `$data`). Gates: ruff/mypy clean (181 files), **1856 tests passing** (53 e2e deselected), `AgentGenerator().generate_all()` 127 agents / 0 errors. Documented in `docs/AUDIT-FIXES-2026-08-10.md`.
- **2026-08-09**: Sprint 5 T009 COMPLETE — OAuth2 client-credentials auth flow. `OAuth2TokenManager` in `src/ai_company/llm/oauth2.py`: client-credentials grant, in-memory token cache with TTL + safety margin, fail-closed on missing credentials or token-fetch failure. Wired into `OpenAICompatibleProvider` (per-request bearer token, `is_available()` honors OAuth2) and `LLMClient._init_providers()` (opt-in per provider via `oauth2:` block in `company/models.yaml`; API-key path unchanged). `ProviderConfig` gained an `oauth2` field. 11 new tests in `tests/unit/test_oauth2.py`. Gates: ruff/mypy clean, 1778 tests passing.
- **2026-08-08**: Sprint 4 COMPLETE — quality & completeness. Commits: `d11608f` (GAP-019 agent spec validation, daemon lifecycle, key rotation, token counting, CLI type hints/docstrings, test suites for CLI/dashboard/escalation, dashboard security hardening), `359489d` (platform-independent CLI help + daemon stop tests), `4765f76` (22 new agent skills + manifest, company KPIs computed from real sources per CEO decision via `scripts/compute_company_kpis.py`, `run_backfill.py` SQLite utility). T012 `ai-company llm usage` and LLM budget caps/auto-suspend landed shortly after via autonomous commits `169ecf7`/`2aa4ec1`. ECL change archived as `harness/changes/archive/2026-08-08-sprint-4-quality-completeness`. Gates: ruff/mypy clean, **1745 tests passing**, CLI help verified. 35 scratch files cleaned from workspace.
- **2026-08-07**: CEO Dashboard Operationalization Plan — Sprint 3 item 3 shipped (`550b11b`): data retention / governance engine end-to-end — `run_retention()` + `GovernanceScheduler` in `data/governance.py` with batched archive (fixed latent bug: each batch appended then only that batch deleted) and rowid-based anonymize (fixed latent bug: `agent_id` + `content` hashed). `ExecutorDaemon` gains `--governance-interval` enforcement; `GET /api/v1/governance` endpoint returns full report (`available`, `tables`, `owners`, `policies`). 8 real-DB tests (`test_governance_engine.py`). CI green: ruff/mypy/pytest (1526 passing).
- **2026-08-07**: CEO Dashboard Operationalization Plan — Sprint 3 item 2 shipped (`9a5a244`): `get_company_kpi_summary()` read-through accessor computes company KPIs vs targets from real telemetry — Build Success Rate (KPI-004) and Agent Utilization (KPI-003) computed from the task window (SQLite-first, inbox fallback); ARR/CSAT/eNPS report configured values. `GET /api/v1/company-kpis` returns the full summary shape (`collected_at`, `period_days`, `kpis[]` with `status/gap/computed/source`, `summary`). Frontend gained a "Company KPIs vs Targets" card grid + Current-vs-Target chart, and department KPI cards now merge live telemetry instead of rendering "undefined". 7 new tests (`tests/unit/test_company_kpis.py`). 1501 tests passing.
- **2026-07-22**: Sprint 3 COMPLETE — all 8 items done. Fixed test_org_chart.py (832 lines rewritten, 56 tests passing). Fixed DataTransformer.registry_to_enhanced() frozen model bug. Created governance CLI (7 commands, 9 tests). Enhanced memory CLI (stats/search/recall). Created WebSocket integration tests (30 tests). Created dashboard API tests (9 tests). Total: 1205 tests passing, 0 ruff errors. v0.3.0 release tagged. **Agent deployment**: All 127 agents deployed to workspace-level `.opencode/agents/` — every agent now invokable via `@`.
- **2026-07-21**: Sprint 3 backlog created (docs/SPRINT-3-BACKLOG.md). Code audit reveals ~60% of planned Sprint 3 items already implemented in source. Revised scope: 8 items, 22 hours effort. Sprint 2 finalization — fixed 2 stale rate limiter test assertions (1091→1093 passing), confirmed mypy 0 errors (164 files), marked S2-03/S2-07 as Done in backlog, all CI gates green. Documentation sync — all docs updated to reflect actual project state.
- **2026-07-20**: Sprint 1 completed. All Track B (code hardening) and Track C (audit trail) items done. Sprint 2 backlog created. All documentation updated to reflect actual state.
- **2026-07-19**: Phase 5 design specs — 3 approval UX documents covering 5-tier action system, dashboard approval queue with WebSocket, and enhanced CLI commands.
- **2026-07-17**: Governance layer — autonomous GitHub Action (cron every 6h), postmortem template + store + CLI, incident response + deployment SOPs, RACI template + hiring workflow RACI, department KPI dashboards (7 departments, 28 KPIs), dashboard CLI, postmortem CLI, sop/raci CLI commands, 8 new tests.
- **2026-07-17**: Cleanup pass — fixed E402 ruff warnings in llm/client.py, deleted 5 dead scripts, wired all 5 providers in opencode.json, created 3 governance/policy docs.

## Historical Audits

Point-in-time audit reports. These are frozen snapshots — refer to `STATUS.md` for the current living state.

| Report | Date | Test Count | Purpose |
|--------|------|------------|---------|
| `docs/archive/2026-08-11-pre-restructure/DOCUMENTATION_AUDIT_REPORT.md` | 2026-08-11 | 1856 | Documentation audit: version drift, stale counts, SOP v1/v2 duplicates, missing feature docs |
| `docs/archive/2026-08-11-pre-restructure/CEO_DASHBOARD_FINAL_REPORT.md` | 2026-08-08 | 1763 | CEO dashboard real-data operationalization; test isolation analysis |
| `docs/archive/2026-08-11-pre-restructure/CEO_DASHBOARD_INVENTORY_REPORT.md` | 2026-08-08 | N/A | 24 data sources inventoried; path-root mismatch findings |
| `docs/archive/2026-08-11-pre-restructure/TECHNICAL_READINESS_REPORT.md` | 2026-08-08 | N/A | Audit verified dashboard reads `ai-company/` not repo root; dummy data in read path |
| `docs/archive/2026-08-11-pre-restructure/SKILL_INTEGRATION_ANALYSIS.md` | 2026-08-07 | N/A | 29 skills installed; collision risk assessment |
| `docs/archive/2026-08-11-pre-restructure/PROJECT_STATUS.md` | 2026-08-11 | 1805 | Consolidated status (pre-Sprint-7); derives from STATUS.md + others |

## Sprint Status

| Sprint | Status | Tests | Items |
|--------|--------|-------|-------|
| Sprint 1 | ✅ COMPLETE | — | Code hardening + audit trail |
| Sprint 2 | ✅ COMPLETE | 1093 passing | 13 items — all Done |
| Sprint 3 | ✅ COMPLETE | 1526 passing | 8 items — all Done |
| Sprint 4 | ✅ COMPLETE | 1745 passing | Quality & completeness |
| Sprint 5 | ✅ COMPLETE | 1778 passing | T009 OAuth2 client-credentials |
| Sprint 6 | ✅ COMPLETE | 1805 passing | Audit fixes + runtime hardening |
| Sprint 7 | ✅ COMPLETE | 1856 passing | Tool vocabulary + HITL expiry + quality hardening + doc reconciliation |
| Sprint 8 | ✅ COMPLETE | — | Operationalization: inbox purge, README/env, Malawi service catalog, client intake CLI |
| Sprint 9 | ✅ COMPLETE | 1878 passing | Business architecture, 131-agent positioning, recurring revenue engine, ADR-010/011 |

## Remaining Work

- **Hard gates (2026-08-13)**: v0.5.0 release (stale v0.4.0), CI-health zombie #20 closed, RBAC #37 closed, feasibility artifacts #10 archived, dependabot PRs (#2 #3 #4 #5 #21) merged/closed, planning docs reconciled.
- **Sprint 9**: COMPLETE (2026-08-13) — business architecture, 131-agent positioning, recurring revenue engine.
- **Sprint 8**: COMPLETE (2026-08-12). Archived.
- **Sprint 7**: COMPLETE — Tool vocabulary canonicalization + HITL expiry + quality hardening + doc reconciliation (2026-08-11). Archived.
- **Sprint 4**: COMPLETE — quality & completeness.
- **Sprint 5 (T009)**: COMPLETE — OAuth2 client-credentials. T012 `llm usage` also done.
- **Sprint 6**: COMPLETE — audit fixes + runtime hardening (2026-08-10).
- **Phase 2 (2026-08-18) COMPLETE**: Daemon mode (S3-06/S3-07), background schedulers, `/api/v1/daemon/status` + WebSocket broadcast, mypy strict mode — all shipped in v0.5.1.
- **Deferred**: Dashboard auth fail-closed default is superseded — RBAC (ADR-012) now gates write endpoints and loopback-restricts open mode. T1 push-bus adapter trigger is explicit in ADR-010 (two consecutive CI benchmark runs breaching read-p95 >10 ms or 127-agent fan-out >5 s). Legacy module deprecation is resolved — `builder.py`/`registry.py`/`graph.py` no longer exist; `builder/`, `registry/`, `graph/` are packages.
