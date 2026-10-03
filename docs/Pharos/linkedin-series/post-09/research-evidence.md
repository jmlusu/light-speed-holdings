# Research Evidence - Post 9: Measuring AI-native Organizations

**Post:** 9
**Framework Layer:** V - Value & Impact
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified |
|-------|--------|----------|
| KPI-003 Agent Utilization: target 80%, formula = distinct active agents (30-day window) / registered agents × 100 | `config/company/kpis.yaml` | ✅ |
| KPI-003 source: `.opencode/inbox.json + company-registry.yaml`; current snapshot 1.5 at 2026-08-14 | `config/company/kpis.yaml` | ✅ |
| KPI-003 computed at request time by `data_service.get_company_kpi_summary()` | `kpis.yaml` header comment | ✅ |
| KPI-004 Build Success Rate: target 99.5, current 100.0, formula completed/(completed+failed) over 30-day window | `config/company/kpis.yaml` | ✅ |
| KPI-001 ARR `current: null`; no revenue ledger source exists yet | `config/company/kpis.yaml` | ✅ |
| KPI-002 CSAT `current: null`; `orchestrator/cs/surveys.json` exists but empty | `config/company/kpis.yaml` | ✅ |
| KPI-005 eNPS `current: null`; no people-survey source | `config/company/kpis.yaml` | ✅ |
| CEO decision 2026-08-08: "Company KPIs must be COMPUTED FROM REAL SOURCES, not hardcoded dummy values" | `kpis.yaml` header comment (verbatim) | ✅ |
| Each KPI has named owner (cfo, coo, cto, chief-of-staff, chro), target, formula, source | `config/company/kpis.yaml` | ✅ |
| Denominator = governed registry list (ADR-032 single registry) | ADR-032; `company-registry.yaml` | ✅ |
| Org graph nodes carry capacity, activity, trend, risk with short TTL cache | `graph/engine.py` `OrgNode` | ✅ |
| `data_service.get_executive_scorecard()` aggregates department health | `dashboard/data_service.py` | ✅ |
| Tasks carry leases; failures land in dead-letter path with audit trail; SLA clocks per workflow step | `orchestrator/message_bus.py`; `workflow/engine.py` | ✅ |
| Variable cost tracked per-model, per-department, visible from week one | `dashboard/data_service.py` cost analytics; business model docs | ✅ |
| 90-day pilot, per-agent cost on invoice, cost curve as dial not contract | Business model documentation | ✅ |
| Seven-tool canonical vocabulary: read, edit, grep, list, bash, webfetch, task | AGENTS.md §8; `models/models.py` ToolRunner validation | ✅ |
| Action classes enumerable → approval matrix attaches tiers per action class → audit log can count them | `orchestrator/approval.py` design | ✅ |
| Five-tier matrix ADR-017: autonomous → HITL-approved → reviewed → snoozed → cleared | ADR-017; `orchestrator/approval.py` | ✅ |
| Approval sweep retires stale/expired requests (EXPIRED terminal state) | AGENTS.md §9.1 | ✅ |
| 90 agents, 20 departments canonical | ADR-032; series plan core thesis | ✅ |
| Series metrics: impressions, engagement rate, substantive comments, subscriber delta with targets and misses reported | Series plan §9 Metrics Tracking | ✅ |
| KPI nulls render as "n/a" in UI | `kpis.yaml` header comment ("the UI renders 'n/a'") | ✅ |
| 30-day/90-day instrumentation sequence (registry, queue, utilization, success rate, dead-letter, cost, tiers, SLA) | Series design synthesis (Posts 5–7 copy blocks + KPI file) | ✅ |

## Excluded Claims (do NOT include in draft)

| Claim | Reason |
|-------|--------|
| Specific productivity percentages ("+30% productivity") | Untraceable to registry/results |
| Benchmark comparisons to third-party AI maturity scores | Self-reported third-party data, unverifiable |
| SME leapfrog statistics | Not verifiable from repo artifacts |
| Subscriber/engagement results for this series | Targets are goals; no results yet (#194 blocks publication) |
| Named third-party customers or revenue figures | No revenue ledger source exists (KPI-001 null) |

## Notes

- KPI-003 current value (1.5%) is cited deliberately as the honesty example; KPI-004 (100.0) cited alongside so the pair shows selection discipline.
- The `null` KPI pattern is presented as a governance feature (marks work owed), consistent with the CEO decision recorded in the KPI file.
- 30/90-day instrumentation list is framed as series synthesis, not as an existing LightSpeed program artifact.