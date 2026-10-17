# CEO APPROVAL MEMO
## Dashboard Data Source Audit — Real vs Dummy Classification & Real-Data Population Authorization

**Date:** 2026-08-08
**From:** Human CEO
**To:** Chief of Staff, CTO, CDO, Dashboard Owner, Business Intelligence Engineer, Data Engineer, Data Scientist, QA Lead, ML Engineer
**Classification:** EXECUTIVE DECISION — ACTION REQUIRED

---

## 1. EXECUTIVE SUMMARY

Completed comprehensive inventory of **18 data sources** feeding the CEO Dashboard. **11 sources are DUMMY/MOCK/PLACEHOLDER** (test artifacts, synthetic data, empty directories). **7 sources are REAL** (production warehouse, live agent executions, generated org artifacts, configuration).

**Decision:** Authorize immediate cross-organizational purge of all dummy data and first-step population of dashboard with real data from production sources.

---

## 2. COMPLETE DATA SOURCE INVENTORY

| # | Source Path | Classification | Evidence | Rows/Size | Status |
|---|-------------|----------------|----------|-----------|--------|
| 1 | `data/ai_company.db` (root) | **DUMMY** | All tables empty (tasks=0, audit=0, kpi=0, cost=0) | 176 KB schema only | 🔴 PURGE |
| 2 | `ai-company/data/ai_company.db` | **REAL** | 214 tasks, 2,891 audit events from live agent runs | 1.6 MB | ✅ LIVE |
| 3 | `orchestrator/approvals.yaml` (root) | **DUMMY** | Test data: "agent-a", "task-001", "rm -rf /", $0 budgets | 257 lines | 🔴 PURGE |
| 4 | `ai-company/orchestrator/approvals.yaml` | **DUMMY** | Same test pattern, 7,483 lines of synthetic approvals | 192 KB | 🔴 PURGE |
| 5 | `memory/episodic.json` (root) | **DUMMY** | "test-agent", $0.00 budgets, duplicate campaigns | 622 entries | 🔴 PURGE |
| 6 | `ai-company/memory/episodic.json` | **DUMMY** | Same test pattern from test harness runs | 622 entries | 🔴 PURGE |
| 7 | `memory/semantic.json` (root) | **DUMMY** | 3 test resolutions, $0.00 contract values | 3 entries | 🔴 PURGE |
| 8 | `ai-company/memory/semantic.json` | **DUMMY** | Identical test data | 3 entries | 🔴 PURGE |
| 9 | `dashboards/` (root) | **MISSING** | Directory does not exist | N/A | 🟡 CREATE |
| 10 | `ai-company/dashboard/kpi_history/` | **EMPTY** | Directory exists, zero KPI data files | 0 files | 🟡 POPULATE |
| 11 | `company/*.yaml` (root) | **MISSING** | Directory does not exist | N/A | 🟡 CREATE |
| 12 | `ai-company/company/departments.yaml` | **REAL** | 17 departments, missions, executives, headcounts | 119 lines | ✅ LIVE |
| 13 | `ai-company/company/models.yaml` | **REAL** | Model routing, 7 providers, 3 tiers, routing rules | 141 lines | ✅ LIVE |
| 14 | `ai-company/company/agent-registry.json` | **REAL** | 127 agents, generated from registry | 136 KB | ✅ LIVE |
| 15 | `ai-company/company/org-chart.md` | **REAL** | Generated org structure | — | ✅ LIVE |
| 16 | `ai-company/company-registry.yaml` | **REAL** | Single source of truth for all agents | 126 KB | ✅ LIVE |
| 17 | `.opencode/agents/*.md` (root) | **REAL** | 127 generated agent definitions | 127 files | ✅ LIVE |
| 18 | `ai-company/.opencode/agents/*.md` | **REAL** | 127 generated agent definitions (project) | 127 files | ✅ LIVE |
| 19 | `workflows/instances/` | **REAL** | 1,118 workflow execution traces | 1,118 files | ✅ LIVE |

**TOTALS:** 11 DUMMY/MISSING/EMPTY | 8 REAL/LIVE

---

## 3. REAL DATA SOURCES CONFIRMED LIVE (Source-of-Truth)

| Source | What It Feeds | Owner |
|--------|---------------|-------|
| `ai-company/data/ai_company.db` → `tasks`, `audit_events` | Operational KPIs, task throughput, agent utilization, approval latency | **Data Engineer** (pipelines), **Dashboard Owner** (API) |
| `ai-company/company/departments.yaml` | Org structure, headcount vs target, budget category rollups | **Business Intelligence Engineer** |
| `ai-company/company/models.yaml` | Model cost tracking, tier utilization, provider fallback rates | **ML Engineer**, **Data Scientist** |
| `ai-company/company/agent-registry.json` | Agent inventory, capability matrix, department coverage | **Dashboard Owner**, **BI Engineer** |
| `ai-company/company-registry.yaml` | Source-of-truth for agent registry (authoritative) | **Data Engineer** (catalog) |
| `workflows/instances/` | End-to-end process latency, success/failure rates, handoff quality | **QA Lead** (quality gates), **Process Quality Manager** |
| `.opencode/agents/*.md` | Live agent permissions, tool access, escalation paths | **Security/Compliance** (audit) |

---

## 4. AUTHORIZATION & DELEGATION

### Primary Leadership
| Role | Agent | Mandate |
|------|-------|---------|
| **Program Lead** | **Chief of Staff** | Own end-to-end execution, coordinate across all departments, report completion to CEO |
| **Technical Lead** | **CTO** | Own data pipeline integrity, schema contracts, API contracts, migration safety |
| **Data Domain Lead** | **CDO** | Own data quality framework, catalog, governance, BI layer accuracy |

### Cross-Functional Execution Squad (8 Agents)
| Agent | Department | Specific Deliverable |
|-------|------------|---------------------|
| **Data Engineer** | Data | Build/repair ETL: `ai_company.db` → warehouse → dashboard API; implement data quality checks; populate `kpi_history/` |
| **Business Intelligence Engineer** | Data | Build self-service CEO dashboard connecting Finance, Sales, Marketing, Ops, Tech, Data, People metrics |
| **Data Scientist** | Data | Derive predictive KPIs (pipeline velocity, churn risk, capacity saturation); validate model cost attribution |
| **Dashboard Owner** | Technology | Own REST API + WebSocket broadcast; ensure live-state reads (not stale files); CORS/auth lockdown |
| **ML Engineer** | AI Research | Instrument model routing telemetry (tier utilization, provider latency, fallback rates) into dashboard |
| **QA Lead** | QA | Define & enforce quality gates: schema validation, data freshness SLAs, zero-stub leakage tests |
| **Process Quality Manager** | QA | Audit workflow instances for data completeness; verify no synthetic data in production flows |
| **Observability Engineer** | Technology | Instrument dashboard API with metrics, traces, alerts; ensure real-time visibility |

---

## 5. FIRST-STEP REAL-DATA POPULATION — REQUIRED EVIDENCE

Before CEO sign-off, **each workstream must produce**:

| Checkpoint | Evidence Required | Verifier |
|------------|-------------------|----------|
| **Dummy Purge Complete** | `git diff` showing removal of all 11 dummy sources; no `task-00*`, `agent-[a-f]`, `$0.00`, `test-agent` patterns in any data file | QA Lead |
| **Warehouse Populated** | `ai_company.db` `kpi_values` table ≥ 100 rows with real task/audit-derived KPIs; `cost_records` populated from model routing logs | Data Engineer |
| **KPI History Live** | `ai-company/dashboard/kpi_history/` contains ≥ 7 department KPI files (JSON/Parquet) with timestamps, values, metadata | BI Engineer |
| **Dashboard API Live** | `GET /api/v1/dashboard/kpis` returns real data (not mocks); WebSocket broadcasts on KPI change; auth enforced | Dashboard Owner |
| **BI Layer Validated** | Self-service dashboard renders real cross-department metrics; drill-through to task/audit detail works | BI Engineer + Data Scientist |
| **Quality Gates Green** | `ruff check src/ && mypy src/ && pytest` pass; zero stub leakage in test suite; schema contracts validated | QA Lead |
| **No Synthetic Leakage** | Grep audit: zero occurrences of `test-agent`, `task-00`, `agent-[a-f]`, `rm -rf`, `$0.00` in any production data path | Process Quality Manager |

---

## 6. RESOURCE/SCRUM REALLOCATION APPROVED

| Reallocation | Approved | Notes |
|--------------|----------|-------|
| Data Engineer: 100% allocation to ETL + warehouse (pause feature work) | ✅ | Critical path |
| BI Engineer: 100% allocation to CEO dashboard (pause self-service v2) | ✅ | Executive-facing priority |
| Dashboard Owner: 100% allocation to API hardening + live-state reads | ✅ | GAP-010/011 blocking |
| QA Lead + Process Quality: Joint ownership of "zero stub leakage" gate | ✅ | New shared mandate |
| ML Engineer: Add model telemetry to dashboard scope (20% capacity) | ✅ | Cost attribution dependency |
| Observability Engineer: Dashboard observability as Sprint 1 deliverable | ✅ | Prerequisite for trust |

**Budget:** No new budget required. Reallocation within existing headcount targets (departments.yaml).

---

## 7. REMAINING GAPS REQUIRING CEO DECISION

| Gap | Impact | Options | Decision Needed |
|-----|--------|---------|-----------------|
| `memory_entries` table empty in production DB | No semantic/episodic memory feeding dashboard | (A) Backfill from `workflows/instances/` (B) Enable live memory writes from agents (C) Defer to Phase 2 | **Choose A/B/C** |
| `escalation_events` table empty | No escalation tracking in dashboard | (A) Instrument orchestrator to write escalations (B) Parse from approvals.yaml (C) Defer | **Choose A/B/C** |
| `cost_records` empty | No model cost visibility | (A) Integrate model routing `models.yaml` tiers with usage logs (B) Add cost estimator per agent type (C) Defer | **Choose A/B/C** |
| Root-level `dashboards/` and `company/` dirs missing | Dashboard owner expects config there | (A) Symlink from `ai-company/` (B) Migrate dashboard to read from `ai-company/` (C) Create stub dirs | **Choose A/B/C** |

**Decision Deadline:** Before Sprint 1 planning (2026-08-11). Chief of Staff to present options with CTO/CDO recommendation.

---

## 8. SIGN-OFF

**First-step real-data population (dummy removal + live data wiring) is AUTHORIZED to proceed.**

**Verification Standard:** No CEO sign-off until all 7 evidence checkpoints in Section 5 are met with artifacts attached.

**Target Completion:** 2026-08-15 (1 week)

---

**Signed:**
Human CEO
Light Speed Holdings
2026-08-08

---

### Distribution List (Action Required)
- [ ] **Chief of Staff** — Program ownership, weekly status to CEO
- [ ] **CTO** — Technical architecture, schema contracts, API review
- [ ] **CDO** — Data quality framework, catalog, governance
- [ ] **Data Engineer** — ETL, warehouse, kpi_history population
- [ ] **Business Intelligence Engineer** — Cross-dept dashboard, self-service
- [ ] **Data Scientist** — Predictive KPIs, model cost attribution
- [ ] **Dashboard Owner** — REST API, WebSocket, live-state, auth
- [ ] **ML Engineer** — Model routing telemetry integration
- [ ] **QA Lead** — Quality gates, schema validation, stub leakage tests
- [ ] **Process Quality Manager** — Workflow data completeness audit
- [ ] **Observability Engineer** — Dashboard observability, alerting
