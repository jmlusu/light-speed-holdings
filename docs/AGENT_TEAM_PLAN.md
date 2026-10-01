# Adjusted Team Composition — Light Speed Holdings

**Date:** 2026-08-31
**Purpose:** Team adjustment to hit the four priorities: (A) developer velocity, (B) system reliability, (C) user experience / user satisfaction, (D) business readiness of the CEO dashboard.
**User directives incorporated:**
- Add `security-architect` to the team.
- Business readiness = **feature completeness** (executive KPIs, org chart, alerting), not just deployment.
- Priority ordering: **UX → user satisfaction** first.
- Alerting: **build minimal in-house first** (defer PagerDuty/Opsgenie).
- Timeline: **8 weeks**.

---

## 1. What changed in the team

| Change | Reason |
|--------|--------|
| **+ `security-architect`** (specialist, reports to `ciso`) | New hire per user directive. Owns the auth boundary (the F7 auth primitive from the architecture review) and hardens dashboard RBAC/CORS. |
| **+ `security-compliance-lead`** exists already | Confirmed present in registry (`dashboard-owner`, `platform-reliability-engineer`, `observability-engineer`, `dashboard-owner`, `qa-lead`, `frontend-engineer` all verified). |
| Slight role emphasis shift | `frontend-engineer` + `dashboard-owner` absorb the run-of-play on UX ("user satisfaction") and executive KPI work; `observability-engineer` + `dashboard-owner` absorb in-house alerting channels. |

No removals. The 135-agent registry stands; we are adding one specialist and re-weighting ownership, not shrinking scope.

---

## 2. Goal → Agent mapping (with our four priorities)

### Goal A — Developer velocity
| Effort | Owner | Key sub-agents |
|--------|-------|----------------|
| Reduce generator/test friction | `developer-experience-engineer` | `platform-engineer`, `qa-lead` |
| Tighten CI/CD + release gates | `release-manager` | `devops-lead`, `test-engineering-lead` |
| Dashboards for internal monitoring | `dashboard-owner`, `observability-engineer` | `business-intelligence-engineer` |

### Goal B — System reliability
| Effort | Owner | Key sub-agents |
|--------|-------|----------------|
| Executor/store hardening | `platform-reliability-engineer` | `orchestration-owner`, `store` owners |
| Alerting (in-house) | `observability-engineer` | `dashboard-owner`, `frontend-engineer` |
| Architecture consolidation (F6, F1) | `software-architect` | `backend-engineer` |

### Goal C — User experience (user satisfaction) — **top priority**
| Effort | Owner | Key sub-agents |
|--------|-------|----------------|
| UX fix sprint (UX-001..012, DASH-001..008) | `frontend-engineer` | `dashboard-owner`, `ux-research-lead` |
| UX verification & acceptance | `ux-research-lead` | `product-designer` |

### Goal D — Business readiness (feature completeness)
| Effort | Owner | Key sub-agents |
|--------|-------|----------------|
| Executive KPI scorecard (FK-001..) | `dashboard-owner` | `business-intelligence-engineer` |
| Rich org chart + metrics | `graph-owner` | `frontend-engineer` |
| In-house alerting (FK-010..) | `dashboard-owner` | `observability-engineer`, `orchestration-owner` |
| Security hardening of all of it | `security-architect` | `security-compliance-lead` |

---

## 3. The 8-week core squad (flat, cross-functional)

A lean delivery squad drawn from the registry to execute the plan fast. Keeps span-of-control small and unblocks the four priorities:

| Role | Agent | Primary lanes |
|------|-------|---------------|
| **Lead / PM** | `product-owner` | Backlog, sprint gates |
| **UX sprint lead** | `frontend-engineer` | UX-001..012, DASH-001..008 |
| **Dashboard backend** | `dashboard-owner` | KPI scorecard, API, alerting engine |
| **Org chart** | `graph-owner` | Org chart + graph metrics |
| **KPI/targets** | `business-intelligence-engineer` | `kpis.yaml`, weights, trends |
| **Reliability** | `observability-engineer` | In-house alert channels, WS |
| **Security (new)** | `security-architect` | Auth primitive (F7), RBAC/CORS, alert endpoint auth |
| **Quality** | `qa-lead` | Test gates, E2E, red/green baseline |
| **UX sign-off** | `ux-research-lead` | User-satisfaction acceptance |

Escalation path up to `software-architect` (architecture) and `security-architect` (anything touching the auth boundary), reviewed by `lead-frontend` / `lead-backend` / `lead-devops` as one senior peer-review panel.

---

## 4. 8-week sequencing (respects single-active-ECL rule + UX-first)

| Week | Theme | Primary change | Squad focus |
|------|-------|----------------|-------------|
| 1 | UX critical fixes | proposal → **Active**: `ux-critical-fixes` | frontend-engineer + ux-research-lead |
| 2 | UX done, QA gate | close `ux-critical-fixes` | qa-lead + regression |
| 3 | Executive KPI scorecard | **Active**: `executive-kpi-scorecard` (phase A: scorecard + kpis.yaml) | dashboard-owner + BI engineer |
| 4 | Executive KPI (phase B: org chart) | continue `executive-kpi-scorecard` | graph-owner |
| 5 | In-house alerting (engine+rules) | **Active**: `in-house-alerting` | dashboard-owner + observability |
| 6 | In-house alerting (channels+escalation) | continue `in-house-alerting` | observability + orchestration |
| 7 | Security hardening + consolidation | follow-up `security-hardening` / arch tasks | security-architect |
| 8 | Wrap / acceptance / release | close all, ship | product-owner + qa-lead |

**Single-active-ECL constraint honored:** only one of the three proposals is `Active` at a time; the others sit in `proposals/` and move `new → active` only as each closes (per `docs/ECL.md`).

---

## 5. Where the architecture-review candidates land

From the `improve-codebase-architecture` HTML report — **implementation status as of this session**:

| Finding | Status | Where / owner |
|---------|--------|---------------|
| **F6** — MessageBus storage seam bypass | ✅ **implemented** | `FileStore.read_json_list()`; `MessageBus._load_tasks` delegates. |
| **F1** — unify task read-throughs | ✅ **implemented** | `data_service.get_all_tasks_fallback()`; `_read_all_tasks` + `_tasks_from_sqlite` delegate. |
| **F2+F3** — KPI helper dedup | ✅ **implemented** | `_sop_freshness()` + `_compute_avg_duration()` in `KPICollector` base. |
| **F7** — single auth primitive | ✅ **implemented** | `rbac.authenticate()`; `_resolve_role` + `_check_api_key` delegate. |
| **F5** — WS broadcast collapse | ✅ **implemented** | `_broadcast_event()` builder; all 10 wrappers route through it. |
| **F4** — prompt scaffold, A/B-gated | ⚠️ **deferred** | Do not consolidate — would break the A/B experiment gate. |

All implemented findings passed `ruff check src/`, `mypy`, and the affected unit/integration suites. F4 remains open deliberately to avoid corrupting the ongoing prompt A/B test.

---

## 6. Artifacts produced by this adjustment

- `docs/UX_USER_SATISFACTION_TASK_BREAKDOWN.md` (UX-001..012, DASH-001..008)
- `docs/FEATURE_COMPLETENESS_TASK_BREAKDOWN.md` (FK-001..014)
- `harness/changes/proposals/2026-08-31-ux-critical-fixes/`
- `harness/changes/proposals/2026-08-31-executive-kpi-scorecard/`
- `harness/changes/proposals/2026-08-31-in-house-alerting/`
- Architecture review: `%TEMP%\opencode\architecture-review\architecture-review-2026-08-31.html`
