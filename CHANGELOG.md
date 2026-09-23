# Changelog

All notable changes to AI Company Builder are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- **Social Media Manager agent** (`social_media_manager`): new Marketing specialist (reports to CMO) with canonical tool set including `webfetch`; added to `company-registry.yaml` and generated as `.opencode/agents/social-media-manager.md` — registry now **145 agents across 20 departments** (144 AI + 1 human CEO).
- **Digital identity setup runbook**: `docs/marketing/digital-identity-setup.md` — 5-phase runbook (Phase 0 Security → 1 Claim brand → 2 Business infrastructure → 3 Branding → 4 Content) owning issue #194, with the digital-identity tree, ownership model, account tiers, per-platform guidance, master company description, visual asset package, first-content batch, content engine, reserve list, phase plan, and end state.
- **Digital asset register**: `docs/marketing/digital-asset-register.md` — per-platform matrix (URL/username/email/owner/2FA/status) for Facebook, Instagram, X, LinkedIn, TikTok, YouTube, Threads; holds no credentials (password manager only).
- **Process doc enhancements** (additive): `ls-social-media-design/SKILL.md` (digital-identity provisioning precondition), `docs/marketing/daily-cadence-checklist.md` (Phase 0 onboarding, standup attendees, monthly digital-identity health check), `docs/SOCIAL_MEDIA_UPLOAD_CHECKLIST.md` (account-provisioning prepend + time estimate), `docs/marketing/warmup-log.md` (Phase 0 sub-steps).
- **Tests**: `EXPECTED_AGENT_COUNT` bumped to 145; `test_doc_agent_counts.py` + `test_doc_drift.py` green (33 passed / 1 skipped).

### Changed
- **Agent count folded 152 → 90** (62 cuts; 89 AI + 1 Human CEO) across edge files: `docs/STATUS.md`, `TESTING.md`, brand template generators; registry-verified count now 90.
- **Agent count reconciled 144 → 145** across living docs: README.md, USER-GUIDE.md, ORGANIZATION.md (Marketing 9 → 11 + `social-media-manager`), DEVELOPMENT.md, `docs/source-of-truth.yaml`, `company/org-chart.md` (Marketing 10 → 11), `docs/AGENT-REGISTRY-TABLE.md`; `company/agent-registry.json` re-synced via `ai-company sync-registry --verify`.
- **Social media setup plan retired**: `social-media/LIGHTSPEED-SOCIAL-MEDIA-SETUP.md` removed; content preserved in normalized form at `docs/marketing/digital-identity-setup.md`.

## [0.6.0] — 2026-09-02

### Added
- **CEO Alert Center**: durable alert persistence — new `AlertStore` (`src/ai_company/dashboard/alert_store.py`, FileStore-backed `alerts.json`, 30-day retention prune, lifecycle `active/acknowledged/snoozed/cleared`, dedupe by rule+dept+kpi+severity, expired-snooze re-activation) + canonical `default_alert_rules()`.
- **Alert Center API**: `run_alert_evaluation()` in `data_service.py` (evaluates 7 default rules, persists fired alerts idempotently); `GET /api/v1/kpis/alerts` refactored to persist + live-WS broadcast; new `GET /api/v1/alerts` (status/severity filters) and `POST /api/v1/alerts/{id}/ack|/snooze|/clear` + `POST /api/v1/alerts/clear-all`, RBAC-gated (`run` read / `approve` write); KPI scheduler runs `run_alert_pass()` after each snapshot.
- **Alert Center UI**: `jarvis-glass` feed with severity badges, status filter tabs, per-row Ack/Snooze/Clear, and live prepend via the `alerts` WebSocket topic.
- **Tests**: `test_alert_store.py` + `test_alert_center_api.py` (17 tests) — store dedupe/lifecycle/retention + API list/ack/snooze/clear contract.
- **Executive KPI Scorecard** (`data_service.get_executive_scorecard()`): health_score + per-KPI status/trend/source + department rollup wired additively into `GET /api/v1/ceo-dashboard`; 6 configurable executive KPI targets (task_throughput, agent_utilization, cost_efficiency, build_success_rate, escalation_resolution_time, approval_turnaround) in `config/company/kpis.yaml`; trend helpers `compute_period_comparison`/`compute_moving_average`/`detect_anomaly` in `analytics.py`.
- **Rich Org Chart with Metrics & Risk**: `compute_org_metrics()` + `org_chart_summary()` in `graph/engine.py`; `OrgNode` extended with optional `metrics`/`risk` fields; `GET /api/v1/org-chart?include_metrics=true` returns per-node capacity/activity/trend + succession/bus-factor risk with a 30s TTL cache; `X-Org-Summary` header carries aggregate totals (agents, avg span, avg capacity, at-risk count); frontend renders capacity bars, risk strip, and a full Metrics & Risk detail panel; filter dropdown (All / At risk / Senior / Overloaded).
- **Tests**: `test_analytics_trends.py` (12), `test_executive_scorecard.py` (12), `test_org_chart_metrics.py` (9) — 33 new tests.
- **Dashboard UI polish**: external Chart.js tooltips (never clipped by `overflow`/`contain` ancestors) with dark `jarvis`-themed styling; inline component detail panel shown on Org Health card selection (score, weight, sparkline) instead of a separate modal; agent detail modal reachable from department drill-down rosters (shows type, department, reports-to, direct reports, description); cost tooltips with per-agent totals and call counts; dark `color-scheme` for native `<select>`/option elements.
- **Executive KPI expansion** from 6 to 10 targets: added `task_success_rate`, `escalation_rate`, `error_rate`, `security_posture`, `strategic_alignment` to `config/company/kpis.yaml` and the `/api/v1/ceo-dashboard` scorecard.

### Changed
- **Scoring extraction**: Org Health executive scoring logic moved into `src/ai_company/dashboard/scorers.py` (`score_task_throughput`, `score_escalation_rate`, `score_security_posture`, `score_strategic_alignment`) with the calculation details removed from `org_health.py`/`data_service.py`.
- **Drill-down navigation**: Approvals / Escalations / In-Progress dashboard drill-downs now navigate to their dedicated pages (`/escalations?filter=…`, `/tasks?status=…`) instead of rendering inline panels.

### Fixed
- **Onboarding task filtering**: `TaskStore.is_test_task()` now also filters onboarding workflow requests (`Onboarding request for agent…`, `Onboarding for agent…`, `Onboarding approved…`) from dashboard task counts to avoid inbox clutter.
- **Onboarding test isolation**: `OnboardingManager` and `OnboardingService` accept an `approval_config_path` so unit tests no longer read/write the production `orchestrator/approvals.yaml`; tests use an isolated temp `approvals.yaml`.

## [0.5.0] — 2026-08-13

### Added
- **Sprint 9** (2026-08-13): Business architecture & master service catalog; 131-agent positioning (external messaging, strategic brief, agent-facing standards); recurring revenue engine (8 recurring products, conversion framework, enterprise payment terms).
- **Sprint 8** (2026-08-12): Operationalization — inbox purge, README/env setup, Malawi service catalog portfolio (4 new agents, governance blocking, SOPs, client intake CLI, legal package).
- **Dashboard RBAC** (ADR-012): role-gated write endpoints, loopback-restricted open mode (`src/ai_company/security/rbac.py`).
- **ADR-010** (T1 event-bus alignment): report-only MessageBus perf benchmark extended with write latency and sustained throughput; explicit push-bus adapter trigger.
- **CI hardening**: version-check job de-flaked (unused setup-uv step dropped); dependabot bumps — `checkout@v7`, `setup-python@v7`, `upload-artifact@v7`, `action-gh-release@v3`, `docker/setup-buildx-action@v4`.

### Changed
- **Storage**: SQLite-first mirror experiment retired (ADR-011 superseded); file-bus + FileStore remain the default.
- **Docs**: workspace artifacts archived (`docs/archive/2026-08-13-workspace-artifacts/`); planning docs (STATUS, TASK-BOARD, BACKLOG, REMAINING-WORK-INVENTORY) reconciled to current reality.
- **Docs**: agent-count reconciliation 127 → 131 — README, STATUS, DEVELOPMENT, USER-GUIDE, ux guides, Sprint 9 architecture, and Malawi service catalog now reference 131 agents; `docs/AGENT-REGISTRY-TABLE.md` is now generated by `AgentGenerator.generate_agent_table()` (wired into `generate_all()`); doc-count drift guard added (`tests/docs/test_doc_agent_counts.py`).

## [0.4.0] — 2026-08-11

### Added
- **Sprint 7** (2026-08-11): Tool vocabulary canonicalization (`code_interpreter` removed; legacy aliases `write`/`execute`/`delegate`/`web_search` mapped); HITL approval expiry sweep (`ApprovalGate` EXPIRED transition wired into daemon governance cadence); quality hardening (approval matrix, rotate-secrets script, .dockerignore); documentation audit and reconciliation begun.
- **Sprint 6** (2026-08-10): Registry anchored to package root (`AI_COMPANY_ROOT` override); lazy CLI sub-app registration; tool-vocabulary canonicalized across all 127 agent cards; shared operating-standards dedup; `ProviderErrorCategory` classification, circuit breaker ignores auth; bounded cost tracker logs; bounded decision log; task lease fields + store locking; DLQ re-enqueue delegation; E2E Alpine `$data` migration.
- **Sprint 5** (2026-08-09): OAuth2 client-credentials auth flow (`OAuth2TokenManager` with TTL cache, fail-closed); `T012 ai-company llm usage` command; LLM budget caps/auto-suspend.
- **Sprint 4** (2026-08-08): `AgentContext.validate()` + `agents validate` CLI (GAP-019); structured JSON logging with correlation IDs (GAP-018); key rotation; token counting; dashboard security hardening; 22 new agent skills; real KPI computation; daemon lifecycle.
- All 127 agents deployed to workspace-level `.opencode/agents/` — every agent now invokable via `@`

## [0.3.0] - 2026-07-22

### Added
- **Sprint 3 — Gap Closure & Quality:**
  - GAP-014 fixed: BriefingGenerator uses public `get_all_tasks()` API (S3-04)
  - GAP-015 fixed: LLM retry cycles providers round-robin (S3-05)
  - Full pipeline E2E integration test — 10 tests covering happy path, failure, memory, audit, tools (S3-08)
  - WebSocket integration tests — 30 tests covering broadcast, topic filtering, connection lifecycle, error handling (S3-01)
  - Dashboard API endpoint tests — 9 tests covering agents, tasks, KPIs, org chart (S3-07)
  - Data governance CLI — `ai-company governance report/audit-trail/risk-summary/retention/compliance/owners/policies` (S3-02)
  - Memory CLI enhanced — `ai-company memory stats/search/recall` commands (S3-03)
  - Organization chart test suite rewritten — 56 tests covering RegistryNormalizer, OrganizationChart, DataModels, Integration, Performance
- **Sprint 2 — Code Hardening & Governance:**
  - Audit trail (JSONL writer, query/filter, integration with executor)
  - 5-tier approval system (classify_tool_action, tier-aware HITL gate, two-person rule)
  - Memory engine wiring (episodic/semantic/procedural recording on task completion)
  - HITL async fix (threading.Event replaces time.sleep, non-blocking executor)
  - WebSocket broadcasts (KPI snapshots + approval/escalation alerts)
  - LLM streaming support (SSE/NDJSON parsing for OpenAI, Anthropic, Ollama)
  - Scheduler-to-Executor wiring (autonomous cycle from scheduled tasks)
  - Deployment infrastructure (release.yml, release.ps1, CHANGELOG)
  - Autonomous GitHub Action (cron every 6 hours) for orchestrator/executor ticks
  - Postmortem system: models, store, template rendering, CLI commands (`orchestrator postmortem`)
  - Incident response SOP (`sop-incident-response.md`)
  - Deployment SOP (`sop-deployment.md`)
  - RACI matrix template + hiring workflow RACI (`raci-hiring.md`)
  - Department KPI dashboards (7 departments, 28 KPIs) with API endpoints
  - Dashboard CLI: `ai-company dashboard kpi list/show`
  - SOP/RACI CLI commands: `ai-company sop`, `ai-company raci`
  - README.md with full project documentation
  - CHANGELOG.md
  - CONTRIBUTING.md
  - User guide (`docs/USER-GUIDE.md`)

### Fixed
- DataTransformer.registry_to_enhanced() frozen model mutation bug — now uses `model_copy(update=...)`
- Ruff E402 warnings in `llm/client.py` (import ordering)
- 7 lint errors in org_chart modules (unused imports/variables)
- Hyphenated `org-chart/` directory merged into `org_chart/`
- LLM retry provider cycling — flat loop with `attempt % len(provider_chain)` round-robin

### Removed
- 5 dead bootstrap scripts (`build_project.py`, `setup_files.py`, `phase3_setup.py`, `add_missing_agents.py`, `generate-dashboard.py`)
- Legacy empty modules (`utils/`, `validator/`, `opencode/`, `templates/` src, `cli/init.py`, `cli/config.py`)
- Legacy `validator.py` (superseded by `registry/validator.py`)
- Legacy `cli/commands.py` (superseded by `cli/main.py`)

## [0.2.0] - 2026-07-17

### Added
- V2 Foundation: 57 Pydantic models, registry system (loader/parser/resolver/validator)
- 14 Jinja2 templates with type-based selection
- BootstrapEngine for full company generation from config
- DecisionEngine (approval matrix, risk assessment, decision tree)
- WorkflowEngine (9 workflows, step tracking, SLA monitoring)
- MemoryEngine (6 memory types with persistence)
- GraphEngine (4 graph types, BFS pathfinding)
- 22 CLI subcommands wired through Typer
- FastAPI dashboard with REST API endpoints
- Model router with 3-tier cost control (fast/standard/premium)
- 5 LLM providers registered (opencode, deepseek, ollama, openai, anthropic)
- 183 unit tests
- CI pipeline (lint, test, harness)
- Governance docs (risk register, board governance, model routing policy)

## [0.1.0] - 2026-07-17

### Added
- Initial project structure
- CLI framework (Typer)
- Agent registry (`company-registry.yaml`)
- Agent generator (Jinja2 templates → `.opencode/agents/*.md`)
- MessageBus for task delegation
- Basic briefing generator
- 27 agents across 7 departments

## [Creative Production Studio] ls-stack agents x7, count migration 145?152 (2026-09-17)

- Added 7 Marketing specialists (creative_director, presentation_designer, document_designer, diagram_designer, isual_storyteller, rand_advertising_designer, rtifact_qa_reviewer) completing the ls-* Creative Production Stack
- Migrated agent count from 145 (144 AI + 1 Human CEO) to 152 (151 AI + 1 Human CEO) across living docs: README.md, USER-GUIDE.md, ORGANIZATION.md, company/org-chart.md, CHANGELOG.md, docs/source-of-truth.yaml, brand-strategy-validation-report.md, UX_VALIDATION_REPORT.md
- 152 registry entries confirmed (20 exec / 125 spec / 7 board); 152 agent cards generated; i-company sync-registry --verify passed
- Drift gates passed: alidate-drift.ps1, pytest tests/docs/test_doc_drift.py, .\scripts\lint-ecl.ps1, uv run ruff check src/, uv run mypy src/, uv run pytest
- EXPECTED_AGENT_COUNT updated from 145 to 152 in 	ests/docs/test_doc_agent_counts.py
- Org chart company/org-chart.md Marketing section updated from 11 ? 18 agents
- Warmup pack marketing assets updated (tiktok, x-single, x-thread)
- Atomized pillar content updated (docs/marketing/atomized/01 and  2)
- Full doc sweep: 2427/2427 pytest tests passing, drift gates green
- Validation status: pass
