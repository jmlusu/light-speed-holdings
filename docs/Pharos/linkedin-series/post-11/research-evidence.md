# Research Evidence - Post 11: Lessons From Building LightSpeed

**Post:** 11
**Framework Layer:** H - Humans Authorize (series close)
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified |
|-------|--------|----------|
| ADR-032 consolidated 152 registered agents → 90; single registry became source of truth | ADR-032; series plan core thesis | ✅ |
| 90 agents, 20 departments canonical | ADR-032; series plan | ✅ |
| Five-tier matrix ADR-017: `autonomous → HITL-approved → reviewed → snoozed → cleared` (exact order) | ADR-017; `orchestrator/approval.py` | ✅ |
| Approval sweep: expired PENDING → EXPIRED, terminal, re-submission required | AGENTS.md §9.1 | ✅ |
| CEO decision 2026-08-08: "Company KPIs must be COMPUTED FROM REAL SOURCES, not hardcoded dummy values" | `config/company/kpis.yaml` header (verbatim) | ✅ |
| KPI-003 Agent Utilization current 1.5 / target 80; nulls render "n/a" | `config/company/kpis.yaml` | ✅ |
| KPI-004 Build Success Rate current 100.0 / target 99.5 | `config/company/kpis.yaml` | ✅ |
| Live org graph: every node carries capacity, activity, trend, risk | `graph/engine.py` `OrgNode` | ✅ |
| Tasks carry leases; failures → dead-letter path with audit trail; SLA clocks per workflow step | `orchestrator/message_bus.py`; `workflow/engine.py` | ✅ |
| Canonical seven tools: read, edit, grep, list, bash, webfetch, task | AGENTS.md §8 | ✅ |
| Gate stack: registry, queue, matrix, sweep, audit log, sandbox, breakers, honesty badges | Modules cited across Posts 7–10 evidence files | ✅ |
| Variable cost per-model/per-department from week one; 90-day pilot per-agent cost on invoice; cost curve as dial | Business model docs; dashboard cost analytics | ✅ |
| Scheduler reliability failures surfaced in metrics rather than hidden | Series plan Post 11 anchor (scheduler reliability); Pharaohs/reliability notes | ✅ |
| Honesty badges as decision-point confidence signal | Posts 7–10; publishing honesty artifacts | ✅ |
| Data in-country defaults, models registered, foreign-owned models behind safeguards | Posts 4, 8 evidence; sovereignty design | ✅ |
| "152" figure predates consolidation; dormant agents in denominator | ADR-032 rationale | ✅ |
| First-person singular voice designated for Post 11 | User directive / plan (H layer, lessons post) | ✅ |
| Series cadence: 11 posts Mon/Wed/Fri 07:00 CAT; Posts 1–3 scheduled, #194 pending for live POSTs | `results/pharos/publish_queue.json`; digital-asset-register | ✅ |
| Next phase: sector deep-dives (health, financial inclusion, public service) | Series plan roadmap sections (Posts 6–7 themes → future) | ✅ |

## Excluded Claims (do NOT include in draft)

| Claim | Reason |
|-------|--------|
| Exact dates/times of the 152→90 consolidation sessions | Not pinned to a dated artifact in current source set |
| Revenue, customer names, or funding figures | No revenue ledger (KPI-001 null) |
| Specific dollar cost figures for the pilot | Cost system exists; no specific figures quoted in series to date |
| "First AI-native company in Malawi/Africa" style claims | Unverifiable marketing claim |
| Attribution of failures to named third parties (vendors, tools) | No incident artifact naming third parties |
| Series performance results (impressions, engagement) | Not yet published; #194 pending |

## Notes

- The "lessons" voice is first-person singular by design; institutional facts (KPIs, ADRs) remain traceable to artifacts even when narrated personally.
- "Scheduler missed runs" is narrated qualitatively per series plan anchor; no incident count or date attached.
- The inversion recommendation (registry → queue → KPIs → forbidden list → tier → agents) is a series synthesis, presented as personal counsel, not as an existing program.