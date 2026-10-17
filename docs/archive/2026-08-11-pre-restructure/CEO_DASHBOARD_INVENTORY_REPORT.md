# CEO Dashboard Data Source Inventory & Remediation Plan

> **Status:** Updated 2026-08-08 (post-verification). First-step execution (dummy removal + real structures) is **COMPLETE**. Code-path wiring is **BROKEN** — see (d). No further destructive changes made in this pass.

## (a) Full Source Inventory with REAL/DUMMY Classification

| # | Data Source | Path | Classification | Description | Evidence |
|---|-------------|------|----------------|-------------|----------|
| 1 | SQLite (canonical) | `data/ai_company.db` (parent root) | **REAL (EMPTY)** | 7 tables, schema v1, 0 rows everywhere | Verified counts=0 for all tables |
| 2 | SQLite (dashboard-facing) | `ai-company/data/ai_company.db` | **DUMMY (BACKFILLED SEED)** | 1039 tasks, 4001 audit_events, 27 cost_records — created by `ai-company/run_backfill.py`; dashboard reads this via `get_database_path()` | Verified row counts |
| 3 | Task Inbox (File) | `.opencode/inbox.json` | **MIXED** | 5 tasks: 1 real registry-bugfix (completed) + 2 real escalations (CS, HR) + 2 test "do something" tasks from human-ceo (created 15:42 today) | Verified task list |
| 4 | Task Inbox (original) | `.opencode/inbox.json.purged-20260807T130617.bak` | **DUMMY (archive)** | 94 old tasks, archived | Count=94 |
| 5 | Audit Log (JSONL) | `.opencode/audit.jsonl` | **REAL** | 90 real task_created events from 2026-07-26 | Verified first lines |
| 6 | Approvals | `orchestrator/approvals.yaml` | **CLEANED** (was DUMMY: 27 fake HITL records) | Now `requests: []`; original at `orchestrator/approvals.yaml.bak` (27 fake records task-001..006, agents a-f) | Verified both files |
| 7 | Escalations | `orchestrator/escalation.yaml` | **CLEANED** (was MISSING) | Created, now `events: []` | Verified |
| 8 | Scheduler | `orchestrator/scheduler.yaml` | **CLEANED** (was MISSING) | Created, now `tasks: []` | Verified |
| 9 | Devices | `orchestrator/devices.yaml` | **CLEANED** (was MISSING) | Created, now `devices: []` | Verified |
| 10 | Cost Tracker | `orchestrator/cost_tracker.json` | **CLEANED** (was MISSING) | Created, zeroed structure (total_budget/spent, by_agent/model/provider, daily_trend) | Verified |
| 11 | Company KPIs (Config) | `ai-company/config/company/kpis.yaml` | **CLEANED** (was DUMMY current values) | Removed hardcoded current (ARR $2.5M etc.); targets kept | Verified — dashboard reports 5 KPIs, current=None where not computed |
| 12 | Department KPIs (Config) | `ai-company/company/config/kpis.yaml` | **REAL (DEFINITIONS)** | Valid KPI definitions with targets | Verified |
| 13 | Agent Registry (YAML) | `ai-company/company-registry.yaml` | **REAL** | Source of truth for agents | 127 agents |
| 14 | Agent Registry (JSON) | `ai-company/company/agent-registry.json` | **REAL** | Generated registry used by dashboard | 127 agents |
| 15 | Departments Config | `ai-company/company/departments.yaml` | **REAL** | 17 departments | Verified |
| 16 | Models Config | `ai-company/company/models.yaml` | **REAL** | Model routing policy | Verified |
| 17 | Memory (Episodic) | `memory/episodic.json` | **CLEANED** (was DUMMY: 620 test entries) | Now `[]`; archived to `backup/memory_archive_20260808_151916` | Verified |
| 18 | Memory (Semantic) | `memory/semantic.json` | **CLEANED** (was DUMMY: 3 test entries) | Now `[]`; archived | Verified |
| 19 | Sales Data | `orchestrator/sales/pipeline.json`, `leads.json` | **CLEANED** (was MISSING) | Created, both `[]` | Verified |
| 20 | Marketing Data | `orchestrator/marketing/campaigns.json`, `content_log.json` | **CLEANED** (was MISSING) | Created, both `[]` | Verified |
| 21 | CS Data | `orchestrator/cs/tickets.json`, `surveys.json` | **CLEANED** (was MISSING) | Created, both `[]` | Verified |
| 22 | Legal Data | `orchestrator/legal/contracts.json`, `compliance_log.json` | **CLEANED** (was MISSING) | Created, both `[]` | Verified |
| 23 | KPI Snapshots | `orchestrator/kpi_snapshots/` | **CREATED (empty)** | Required for trend analysis | Directory exists, empty |
| 24 | Dashboards Dir | `dashboards/` | **MISSING** | Expected by some components | Not found |

## (b) Numbered Action List with Assigned Owners & Status

| # | Action | Owner (Subagent) | Status | Evidence |
|---|--------|------------------|--------|----------|
| 1 | Purge dummy approvals.yaml → empty valid structure | `data-engineer` | **COMPLETE** | `requests: []`; backup at `approvals.yaml.bak` |
| 2 | Create empty escalation.yaml | `data-engineer` | **COMPLETE** | `events: []` |
| 3 | Create empty scheduler.yaml | `data-engineer` | **COMPLETE** | `tasks: []` |
| 4 | Create empty devices.yaml | `data-engineer` | **COMPLETE** | `devices: []` |
| 5 | Create zeroed cost_tracker.json | `financial-analyst` | **COMPLETE** | Zeroed fields verified |
| 6 | Remove dummy current values from config/company/kpis.yaml | `cfo` | **COMPLETE** | Targets kept; dashboard shows 5 KPIs with computed values |
| 7 | Create orchestrator subdirectories (sales, marketing, cs, legal, kpi_snapshots) | `data-engineer` | **COMPLETE** | All exist |
| 8 | Populate sales data files with real structure (empty) | `sales-owner` | **COMPLETE** (structure only) | `[]` files; real data needs CRM |
| 9 | Populate marketing data files with real structure (empty) | `marketing-owner` | **COMPLETE** (structure only) | `[]` files |
| 10 | Populate CS data files with real structure (empty) | `customer-success-owner` | **COMPLETE** (structure only) | `[]` files |
| 11 | Populate legal data files with real structure (empty) | `legal-owner` | **COMPLETE** (structure only) | `[]` files |
| 12 | **FIX: Backfill the CORRECT SQLite DB** — `ai-company/data/ai_company.db` was backfilled with seed data by `run_backfill.py` (1039 tasks). Decision needed: clear it, or migrate seed to canonical `data/ai_company.db` | `data-engineer` / `orchestration-owner` | **BLOCKED — needs CEO/CTO call** | Row counts verified |
| 13 | Archive dummy memory, start fresh | `memory-owner` | **COMPLETE** | `[]`; archive at `backup/memory_archive_20260808_151916` |
| 14 | **FIX: Resolve path-mismatch so dashboard reads real data** — see (d) B-1 | `dashboard-owner` / `chief-of-staff` | **BLOCKED** | `api.py`, `repository.py`, `paths.py` reverted to pre-fix state; `get_data_root()` returns `ai-company`, runtime data at parent root |
| 15 | Verify dashboard endpoints return real data | `qa-automation-engineer` | **BLOCKED** | Depends on #14; see (d) |
| 16 | Run full test suite for regressions | `qa-lead` | **BLOCKED** | Depends on #14 |
| 17 | Generate before/after diff proof | `chief-of-staff` | **PARTIAL** | This report + backups; full diff after #14 |

## (c) Evidence That First Step (Dummy Removal + Real Data) Is Complete

**1. Dummy approvals removed** — `orchestrator/approvals.yaml`:
```yaml
requests: []
```
Original dummy (27 fake records, `task-001`..`task-006`, agents `agent-a`..`agent-f`) preserved at `orchestrator/approvals.yaml.bak`:
```yaml
requests:
- id: hitl-0f35be6f051d
  task_id: task-001
  agent_id: agent-a
  action: tool:execute
  ...
```

**2. Missing files created with valid empty structures** — `escalation.yaml` (`events: []`), `scheduler.yaml` (`tasks: []`), `devices.yaml` (`devices: []`), `cost_tracker.json` (zeroed), `orchestrator/sales|marketing|cs|legal/*.json` (all `[]`), `orchestrator/kpi_snapshots/` (empty dir).

**3. Dummy current values removed from `ai-company/config/company/kpis.yaml`** — dashboard `get_company_kpi_summary` now returns 5 KPIs; KPI-003 computed 3.9% (below_target), KPI-004 100.0% (on_track) from files; KPI-001/002/005 `current: None`.

**4. Memory cleaned** — `memory/episodic.json` and `memory/semantic.json` are now `[]` (4 bytes each). 620+3 dummy entries archived to `backup/memory_archive_20260808_151916`.

**5. Backup exists** — `backup/backup_20260808_150343` (contains pre-cleanup `.opencode/`, `orchestrator/`, `memory/`, `data/`, `ai-company/config/`).

**6. Dashboard now executes end-to-end** (read-only probe `test_ceo_dashboard3.py`):
- `get_ceo_dashboard()` returns: 127 agents, 5 company KPIs, 7 department KPI groups (10/4/6/6/6/7/8 KPIs), task pipeline, escalations=0, approvals=0.
- Note: task pipeline reads 1035 tasks from the **backfilled seed DB** (see (d) B-2) — NOT the 5-task inbox. This is the dummy-data leak.

## (d) Blockers Needing CEO/CTO Attention

| # | Blocker | Impact | Needs Decision From |
|---|---------|--------|---------------------|
| B-1 | **Path-root mismatch (CRITICAL)** — Runtime data (`.opencode/`, `orchestrator/`, `memory/`, `data/`) lives at **parent root** `C:\Users\jmlus\light-speed-holdings`, but `ai_company.paths.get_data_root()` returns **`ai-company`** (project root). KPI collectors use `self.root = get_project_root()` = `ai-company`, so paths like `orchestrator/escalation.yaml` resolve to `ai-company/orchestrator/escalation.yaml` (missing) instead of the parent-root file. My earlier fix (parent-root-aware `get_data_root()` + `ai-company/` prefix mapping in `api.py`/`repository.py`) was **reverted between sessions** — git status confirms `paths.py`, `repository.py`, `api.py` are unmodified. Scenario A (root=ai-company): registry=127 ✓ but orchestrator files invisible. Scenario B (root=parent): orchestrator visible ✓ but registry=0 and company_kpis=0. Neither single root works. | Dashboard shows wrong/empty data depending on launch root; KPIs that depend on orchestrator files silently read zeros | CTO (decision: single data root vs. dual-root mapping) |
| B-2 | **Backfilled seed DB masquerading as real** — `ai-company/data/ai_company.db` contains 1039 tasks / 4001 audit events / 27 cost records from `run_backfill.py`. `get_database_path()` = `get_data_root()/data/ai_company.db` = the seed DB, so the dashboard reports 1001 pending tasks that don't exist in the 5-task inbox. Either this is intended test data to be cleared, or it should be moved to canonical `data/ai_company.db` and re-derived from real sources. | Task pipeline + engineering/agent KPIs + cost analytics show fabricated numbers | CTO / CAIO |
| B-3 | **No real department operational data** — Sales/Marketing/CS/Legal files are structurally present but empty (`[]`). No CRM/ticketing/contract systems. KPIs legitimately zero until integration. | Department dashboards empty | CEO (strategic) / CTO (technical) |
| B-4 | **Model cost tracking** — No real LLM API costs recorded (mock providers). `cost_tracker.json` zeroed. | Finance KPIs, budget_utilization | CFO / CTO |
| B-5 | **Dashboard authentication** — GAP-011 authz not fully implemented; real data exposure needs auth before production. | Security/compliance | CISO / CTO |
| B-6 | **Code edits reverted** — path-mapping changes made earlier today are gone. Execution phase must re-apply them (or a better dual-root strategy) and verify with `pytest tests/dashboard` + `test_ceo_dashboard*.py`. | All dashboard fixes depend on this | CTO / chief-of-staff |

## (e) Recommended Scope for NEXT Step

1. **P0 — Fix data-root strategy (B-1/B-6).** Decide: (a) single data root = parent (preferred, matches AGENTS.md "Project Location"), with `ai-company/` prefix mapping for files under the project; or (b) keep `get_data_root()` = `ai-company` and add parent-aware allowlist entries. Implement in `paths.py` + `dashboard/repository.py` + `dashboard/api.py`, then verify: registry=127, inbox=5 tasks, approvals=0, cost=0, company KPIs=5, engineering KPIs computed from inbox not seed DB.
2. **P0 — Resolve seed DB (B-2).** Clear `ai-company/data/ai_company.db` OR relocate/rename to `backup/`; backfill canonical `data/ai_company.db` only from real sources (audit.jsonl, inbox.json, registry) after B-1 is decided.
3. **P1 — Regression gate.** `ruff check src/ && mypy src/ && pytest` (1,526+ baseline) + dashboard endpoint smoke tests.
4. **P1 — Department data integration.** Define real source/SOP for Sales/Marketing/CS/Legal (CRM, ticketing, contract management) or accept explicit zero-KPI policy.
5. **P2 — Cost tracking + KPI snapshots + auth.** Activate real LLM keys, automate daily snapshot collection, complete GAP-011 authz.
