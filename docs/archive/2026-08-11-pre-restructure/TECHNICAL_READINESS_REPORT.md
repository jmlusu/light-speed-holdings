# TECHNICAL READINESS REPORT
## CEO Dashboard Real-Data Population — Verified Audit & Remediation Plan

**Date:** 2026-08-08
**Prepared by:** CTO (Chief Technology Officer)
**For:** CEO / Chief of Staff
**Status:** AUDIT VERIFIED — Remediation Plan Ready for Execution

---

## Executive Summary

This report supersedes the earlier version dated 2026-08-08. Runtime verification (code path tracing + live collection) found the earlier report's central premise to be **incorrect**: it assumed the dashboard state root is the repo root and recommended "Option C — configure `DASHBOARD_DATA_DIR=ai-company`". In reality:

1. `get_project_root()` (`ai-company/src/ai_company/paths.py`) already resolves to **`ai-company/`** (marker walk finds `ai-company/pyproject.toml`; env overrides `AI_COMPANY_ROOT`/`DASHBOARD_DATA_DIR` are **not set**).
2. Therefore the dashboard **already reads the `ai-company/` level** — `ai-company/data/ai_company.db`, `ai-company/.opencode/inbox.json`, `ai-company/orchestrator/*`, `ai-company/config/company/kpis.yaml`, `ai-company/company/*`.
3. The earlier cleanup (root-level `orchestrator/`, `memory/`, `data/`, `.opencode/`) cleaned the **wrong root** — those paths are NOT the dashboard's read paths.
4. The dummy data the CEO flagged **is still live in the dashboard's real read path**: `ai-company/orchestrator/approvals.yaml` (dummy approvals rendered on CEO dashboard) and `ai-company/config/company/kpis.yaml` (hardcoded dummy "current" values rendered as `company_kpis`).

The audit is complete and non-destructive. The remediation plan (Section b) names the owning subagent for every stub/fixture. No data was purged during this audit.

---

## (a) Source-of-Truth Map with REAL vs STUB Classification (Verified 2026-08-08)

Legend: 🔴 DUMMY/STUB (feeds dashboard UI) · 🟡 MIXED/UNVERIFIED · 🟢 REAL · ⚪ EMPTY/ABSENT (renders zero)

### READ PATH — what the dashboard actually serves (boot StateStore base_dir = `ai-company/`)

| # | Data Source | Path (resolved) | Class | Evidence (this audit) |
|---|-------------|-----------------|-------|------------------------|
| 1 | SQLite Warehouse | `ai-company/data/ai_company.db` | 🟢 REAL | 7 tables: tasks=**1,039**, audit_events=**4,001**, cost_records=**27**, escalation_events=0, kpi_values=0, memory_entries=0; SCHEMA_VERSION=1 |
| 2 | Task Inbox (MessageBus) | `ai-company/.opencode/inbox.json` | 🟡 MIXED | 1,035 tasks: 1001 pending / 32 completed / 1 in_progress / 1 waiting_approval; senders are nearly all demo-workflow agents (hr-service 403, marketing-service 185, sales-service 155, legal-service 124, customer_success-service 62); ~371 instructions contain demo/test markers ("Test", "First", $0.0 budgets) |
| 3 | Audit Log | `ai-company/.opencode/audit.jsonl` | 🟡 MIXED | 4,241 lines, all `task_created`, 2026-07-20 → 2026-08-08; same demo-workflow agents dominate (hr-service 1,837, marketing-service 846, sales-service 714, legal-service 562, customer_success-service 282) |
| 4 | Approvals | `ai-company/orchestrator/approvals.yaml` | 🔴 DUMMY | 83 requests (46 pending / 19 approved / 18 rejected); **54 dummy** (`task-*`, `agent-a..f`, `t1/t2/t3`, 9× `rm -rf` descriptions); ~29 real-looking HITL entries (`hitl-{uuid}` → real task ids); file 30,470 B / 1,182 lines, last written today 17:13 |
| 5 | Escalations | `ai-company/orchestrator/escalation.yaml` | 🟢 REAL (CONFIG) | Rules only (`rule: task-timeout`, escalate_to chief_of_staff, timeout 30); `events:` absent → open_escalations = 0 |
| 6 | Scheduler | `ai-company/orchestrator/scheduler.yaml` | ⚪ EMPTY | `tasks: []` → scheduled = 0 |
| 7 | Cost Tracker | `ai-company/orchestrator/cost_tracker.json` | ⚪ MISSING | File **does not exist** → `get_ceo_dashboard` cost_summary zeros, despite 27 real SQLite cost_records (data_service cost path exists but CEO summary uses the file) |
| 8 | Company KPIs Config | `ai-company/config/company/kpis.yaml` | 🔴 DUMMY | Hardcoded currents: ARR 2,500,000 / CSAT 88 / Utilization 65 / Build Success 97.2 / eNPS 62 (targets 10M/95/80/99.5/75). **git-tracked** (commits 527af3c, fde705e). Rendered as `company_kpis` in `get_ceo_dashboard`. |
| 9 | Department KPI Definitions | `ai-company/company/config/kpis.yaml` | 🟢 REAL | Valid definitions with targets; no dummy currents; git-tracked (44dfc7f) |
| 10 | Agent Registry | `ai-company/company/agent-registry.json` | 🟢 REAL | 127 agents across 18 departments; generated from `company-registry.yaml` |
| 11 | Departments / Models | `ai-company/company/departments.yaml`, `ai-company/company/models.yaml` | 🟢 REAL | 17 departments; 7 providers / 3 tiers / routing rules |
| 12 | Sales ops | `ai-company/orchestrator/sales/pipeline.json`, `leads.json` | ⚪ MISSING | Files absent → sales KPIs all zero |
| 13 | Marketing ops | `ai-company/orchestrator/marketing/campaigns.json`, `content_log.json` | ⚪ MISSING | Files absent → marketing KPIs all zero (except 1 inbox task → 100% completion) |
| 14 | CS ops | `ai-company/orchestrator/cs/tickets.json`, `surveys.json` | ⚪ MISSING | Files absent → CS KPIs all zero |
| 15 | Legal ops | `ai-company/orchestrator/legal/contracts.json`, `compliance_log.json` | ⚪ MISSING | Files absent → legal KPIs all zero (except 3 inbox tasks → 33.3%) |
| 16 | Episodic Memory | `ai-company/memory/episodic.json` | 🟡 MIXED | 35 entries (was 622 at audit start — partially reduced), demo-flavored ($0.0 budgets, service agents); feeds MemoryStore, not dashboard KPI panels |
| 17 | Semantic Memory | `ai-company/memory/semantic.json` | 🟡 MIXED | 3 entries, $0.00 values; not dashboard UI |
| 18 | KPI Snapshot History | `ai-company/dashboard/kpi_history/` | ⚪ EMPTY | 0 files → no trends |
| 19 | Workflow Instances | `ai-company/workflows/instances/` + root `workflows/instances/` | 🟡 MIXED | Root copies are **git-tracked** dev traces (`simple_*` done, `hiring_*` running, 8 files, commit 16f06f3); ai-company copies gitignored |

### NON-READ PATH — repo root (cleaned previously; NOT served by dashboard at boot)

| # | Path | Class | Notes |
|---|------|-------|-------|
| 20 | `data/ai_company.db` | ⚪ EMPTY | All tables 0 rows; not read at boot (CWD-dependent `get_state_store()` would read it, but `create_app()` configures to `ai-company/`) |
| 21 | `.opencode/inbox.json` (root) | 🟡 MIXED | 5 tasks (3 real-ish, 2 "do something" dummies); root audit.jsonl 90 lines; not read at boot |
| 22 | `orchestrator/*`, `memory/*`, `config/company/kpis.yaml` (root) | 🟢 CLEANED | approvals.yaml 12 B, escalation.yaml 10 B, scheduler.yaml 9 B, cost_tracker.json 179 B zeroed, per-dept `[]`, memory `[]`, root kpis.yaml absent |

### Live KPI snapshot (collected 2026-08-08 with boot-equivalent config)

- **engineering**: task_completion_rate **3.1%** (target 95) — driven by 1,035 inbox tasks, 1001 pending; escalation_rate 0 (no escalation events); scheduled 0
- **hr**: 127 agents; department_coverage **0.0%** (17 declared); agents_by_department breakdown REAL
- **finance**: budget_utilization 0.0%, estimated_llm_spend 0.0, total_budget 90, cost_per_agent 0.0 (cost_tracker missing)
- **marketing/sales/customer_success**: all target metrics zero/empty (missing data files)
- **legal**: contracts/compliance zero; legal_task_completion 33.3% (3 inbox tasks)
- **company_kpis** (CEO view): dummy ARR $2.5M / CSAT 88 / etc. from `config/company/kpis.yaml`

---

## (b) Concrete List of Code/Fixtures/Stubs to Remove/Fix — With Owning Subagent

### PRIORITY 1 — Stub leakage in the dashboard's real read path (do first; each is a small, reversible file edit + test)
| # | Path | Action | Owner | Status |
|---|------|--------|-------|--------|
| 1 | `ai-company/orchestrator/approvals.yaml` | Preserve the ~29 real `hitl-*` requests; purge 54 dummy requests (`task-*`, `agent-a..f`, `t1/t2/t3`, `rm -rf` descriptions) | **data-engineer** | 🔴 PENDING |
| 2 | `ai-company/config/company/kpis.yaml` | Replace hardcoded dummy currents with either computed values from warehouse or `current: null` + display "n/a"; keep targets. Remove the "company" KPI config from git if not needed; add collector for ARR/CSAT/eNPS if source exists | **data-engineer** + **financial-analyst** | 🔴 PENDING |
| 3 | `ai-company/orchestrator/cost_tracker.json` | Create valid structure (`{"total_budget":...,"total_spent":...,"by_agent":{},...}`) or change `get_ceo_dashboard` cost_summary to read SQLite `cost_records` (27 real rows) | **backend-engineer** + **data-engineer** | 🔴 PENDING |
| 4 | `ai-company/orchestrator/sales/*`, `marketing/*`, `cs/*`, `legal/*` | Create empty valid structures (`[]` or schema-shaped) so collectors render explicit zeros, not missing-file fallback; then populate via SOP or integrations | **sales-owner**, **marketing-owner**, **customer-success-owner**, **legal-owner** | 🔴 PENDING |
| 5 | `ai-company/memory/episodic.json` / `semantic.json` | Archive demo entries; replace with `[]` or real backfill (MemoryStore; not dashboard UI but feeds agent context) | **memory-owner** | 🔴 PENDING |

### PRIORITY 2 — Root-cause the demo stream (prevent regeneration)
| # | Path | Action | Owner | Status |
|---|------|--------|-------|--------|
| 6 | `ai-company/workflows/instances/` + demo workflows (`hiring_*`, `simple_*`) | Identify which workflow/simulator generates the hr-service/marketing-service/sales-service/legal-service/customer_success-service task flood; gate demo runs to a sandbox dir or disable scheduler-driven demo workflows; ensure no demo data lands in inbox.json/audit.jsonl | **platform-engineer** | 🔴 PENDING |
| 7 | Inbox/audit demo backlog (1,035 tasks / 4,241 events, ~36% demo-flavored) | Decide retention: archive demo-originated tasks to `ai-company/results/` backup; keep real HITL + escalations + CEO tasks; update MessageBus/audit collectors to tag source workflow | **data-engineer** + **dashboard-owner** | 🔴 PENDING (needs CEO decision — Section d) |
| 8 | Root dev/test scripts (`test_ceo_dashboard*.py`, `test_store4.py`, `check_*.py`) | These are ad-hoc audit scripts at repo root that read/write orchestrator paths; retire or move under `ai-company/tests/` with temp dirs so they never touch production data paths | **qa-lead** | 🔴 PENDING |
| 9 | `ai-company/memory/vector_index/vector_index.json` (30 MB) | Confirm it's a real index or rebuildable artifact; if rebuildable, move to gitignore + regenerate | **ml-engineer** | ⚪ REVIEW |

### PRIORITY 3 — Test fixtures / legitimate source patterns (NO ACTION — expected)
| # | Item | Classification | Notes |
|---|------|----------------|-------|
| 10 | `ai-company/tests/fixtures/dashboard_data.py`, `tests/integration/*.py` | TEST FIXTURE | Factory functions only; verify all write to temp dirs (test_cost_tracker_integration uses `task-001`, test_audit_integration uses `agent-a` — confirm scoped to tmp_path) |
| 11 | `src/ai_company/orchestrator/approval_prompts.py`, `tier_rules.py` | LEGITIMATE | `rm -rf` is a Tier-4 dangerous-command classification pattern, not dummy data |
| 12 | `ai-company/company/config/kpis.yaml` | REAL | Definitions with targets; keep as source for dept collectors |

### PRIORITY 4 — Path/architecture hardening
| # | Item | Action | Owner | Status |
|---|------|--------|-------|--------|
| 13 | `get_state_store()` default base_dir `"."` (CWD) | Make the bare default resolve via `get_project_root()` so ad-hoc scripts and tests never accidentally read/write the repo-root duplicate set | **backend-engineer** | 🔴 PENDING |
| 14 | Root vs ai-company duplicate data dirs | Document that `ai-company/` is the single dashboard data root; delete or ignore the repo-root `data/`, `orchestrator/`, `memory/` duplicates (already gitignored) | **platform-engineer** | 🔴 PENDING |

---

## (c) Path-Mismatch Confirmation + Exact Fix

### Confirmed
- `ai-company/src/ai_company/paths.py::get_project_root()` returns `C:\Users\jmlus\light-speed-holdings\ai-company` (marker walk → `ai-company/pyproject.toml`).
- `get_data_root()` = `get_project_root()` when `DASHBOARD_DATA_DIR` and `AI_COMPANY_ROOT` are unset — they are unset.
- `dashboard/app.py::create_app()` → `configure_state_store(str(get_data_root()))`; `init_database(Path(base_dir)/"data"/"ai_company.db")` → **`ai-company/data/ai_company.db`**.
- `dashboard/api.py` `_load_yaml("orchestrator/approvals.yaml")`, `_load_yaml("config/company/kpis.yaml")`, `_load_json("orchestrator/cost_tracker.json")` all resolve under StateStore base_dir **`ai-company/`**.
- The CEO's suspicion is **confirmed in direction, with a nuance**: there are two parallel data roots; the dashboard serves `ai-company/`, while the prior cleanup only touched repo root.

### Exact fix (no data moves needed)
1. Do **NOT** set `DASHBOARD_DATA_DIR` — the default already points at the populated warehouse. (The prior report's "Option C" was already the runtime default.)
2. Purge/fix the stub files listed in (b) Priority 1 — those are the only remaining dummy values reaching the UI.
3. Decide the demo-workload question (Section d #2) before cleaning inbox/audit so real data is not lost.
4. Harden `get_state_store()` default and retire root-level duplicates to prevent future divergence.

---

## (d) Architecture/Sign-Off Items Requiring CEO Decision

| # | Blocker | Impact | Options | Recommendation |
|---|---------|--------|---------|----------------|
| 1 | **Which tasks are "real"?** Inbox/audit are genuine orchestrator executions but ~36% originated from demo workflows (hr-service/marketing-service/etc., hiring/simple instances, $0 budgets, "Test"/"First"/"Deal" instructions). | Engineering completion 3.1%, all dept task KPIs, agent analytics skewed by demo flood | A) Purge demo-originated tasks/events  B) Keep all, tag by source  C) Archive to `results/` backup, reset stream | **Option C** — archive + reset; preserves evidence, dashboard reflects real workload |
| 2 | **Sales/Marketing/CS/Legal have no real operational source** (no CRM/ticketing/contracts). | Those dept dashboards show zeros | A) Manual-entry SOP for dept heads  B) Integrations (future)  C) Accept zeros | **Option A** immediately; B as Phase 2 |
| 3 | **LLM cost = $0** (local ollama provider). 27 cost_records, all $0.00. | Finance cost KPIs meaningless | A) Wire real provider + key  B) Estimator per agent type  C) Accept $0 and label "local inference" | **Option B** — realistic estimates; C as interim label |
| 4 | **Company KPIs config is dummy** (ARR/CSAT/eNPS/Utilization/Build Success). | CEO dashboard company_kpis show fake numbers | A) Computed from warehouse  B) Manual CFO quarterly input  C) Hide until real | **Option B** — CFO provides authoritative company-level numbers; wire to config |
| 5 | **Dashboard auth**: `DASHBOARD_AUTH_MODE=api_key` fail-closed, no `DASHBOARD_API_KEY` set. | Write endpoints blocked; read endpoints open? | A) Generate + distribute API key  B) OAuth (Phase 2) | **Option A** |
| 6 | **KPI history empty** (`dashboard/kpi_history/` = 0 files). | No trend charts | A) Daily KPI snapshot job  B) Backfill from audit (7 days) | **Option A + B** |
| 7 | **Git-tracked demo fixtures** (`workflows/instances/hiring_*.json`, `simple_*.json`, and the dummy `config/company/kpis.yaml`). | Demo state versioned in repo | A) Remove from git + ignore  B) Keep as fixtures under tests/ | **Option B** — move to `ai-company/tests/fixtures/`, keep `config/company/kpis.yaml` only if needed as a template |

---

## Verification Checklist (aligns with CEO Approval Memo)

| Checkpoint | Evidence Required | Status |
|------------|-------------------|--------|
| Stub leakage at read path | `ai-company/orchestrator/approvals.yaml` and `ai-company/config/company/kpis.yaml` contain no `task-00*`, `agent-[a-f]`, `rm -rf`, hardcoded dummy currents | ❌ PENDING |
| Warehouse populated | `ai-company/data/ai_company.db` tasks=1,039, audit=4,001, cost=27 (verified) | ✅ VERIFIED |
| KPI history live | `ai-company/dashboard/kpi_history/` ≥ 7 files | ❌ PENDING |
| Dashboard API real data | `/api/ceo/dashboard` returns computed dept KPIs + real approvals (0 dummy) + real costs | ❌ PENDING |
| Demo stream gated | No new demo-originated tasks in inbox after gate; source-tagged | ❌ PENDING |
| No synthetic leakage | Grep `task-00`, `agent-[a-f]`, `rm -rf`, `$0.00`, `test-agent` in production read paths = 0 | ❌ PENDING (root level clean only) |
| Quality gates green | `ruff check src/ && mypy src/ && pytest` | ✅ PASS (no src changes yet; re-verify after fixes) |

---

## Next Steps

1. **CEO sign-off on Section (d) #1 (demo task disposition) and #4 (company KPI source)** — these block the inbox/audit and company-KPI cleanup.
2. Assign Priority 1 items to owning subagents (data-engineer, backend-engineer, financial-analyst, dept owners) per (b).
3. Assign Priority 2 items (platform-engineer gates demo workflows; qa-lead retires root ad-hoc scripts).
4. Assign Priority 4 hardening (backend-engineer `get_state_store()`; platform-engineer repo-root duplicate retirement).
5. After fixes: re-run `collect_all_kpis()` + `GET /api/ceo/dashboard` and verify zero stub leakage; run full quality gates.
6. Re-verify live: start dashboard (port 8420), open CEO view, confirm real approvals/costs/company KPIs.

---

## Sign-Off

**Audit COMPLETE and VERIFIED (non-destructive).** The dashboard already reads the populated `ai-company/` warehouse; the remaining dummy values reaching the CEO UI are `ai-company/orchestrator/approvals.yaml` (dummy approvals) and `ai-company/config/company/kpis.yaml` (hardcoded company KPI currents), plus missing per-dept files causing zero KPI sections. The earlier root-level cleanup did not affect the dashboard read path. Remediation ownership is assigned in Section (b); two decisions (demo task disposition, company KPI source) require CEO sign-off before data cleanup.

**Prepared by:** CTO
**Date:** 2026-08-08
**Distribution:** CEO, Chief of Staff, CDO, Data Engineer, BI Engineer, Dashboard Owner, QA Lead, CFO, CISO
