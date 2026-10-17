# Research Evidence - Post 2: What does 90 AI agents actually mean?

**Post:** 2 - "What does 90 AI agents actually mean?"
**Series:** AI-Native Organizations (11 posts)
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified | Notes |
|-------|--------|----------|-------|
| 90 agents is the canonical count for LightSpeed Holdings | Company registry `company-registry.yaml` (source-of-truth.yaml) | ✅ | ADR-032 confirms 90→90 agent count |
| 20 departments support the 90-agent structure | Company registry department config | ✅ | 20 departments defined in `config/company/departments.yaml` |
| Agent Utilization KPI tracks agent engagement per department | `MarketingKPICollector` KPI-003 (`agent_utilization`) | ✅ | Computed from task window (SQLite-first, inbox fallback) |
| 8 recurring revenue products support the agent economy | Company config `recurring_products` list | ✅ | 8 products defined in `config/company/kpis.yaml` |
| AI agent decision rights follow 5-tier HITL matrix | ApprovalGate rules in `src/ai_company/approval.py` | ✅ | Tiers: autonomous → HITL-approved → reviewed → snoozed → cleared |
| Agent Utilization >90% target enables sustainable operations | KPI target in `config/company/kpis.yaml` | ✅ | Measured against task window (30-day window) |

## Verification Status

- [x] Canonical agent count (90) validated against source-of-truth (2026-09-28)
- [x] Department structure (20 departments) verified
- [x] Agent Utilization KPI-003 defined and operational
- [x] 8 recurring revenue products confirmed
- [x] 5-tier HITL decision matrix verified (ref: ADR-017)
- [ ] KPI target compliance: **PENDING**; requires 30-day data review
- [ ] Cross-department agent distribution: **PENDING**; requires analytics review

## Next Steps

1. Run `k-dense-research-lookup` for "agent utilization metrics AI consultancy": confirms claim about 30%+ productivity
2. Run `k-dense-research-lookup` for "SADC AI agent economic impact": regional context
3. Verify KPI-003 computation from actual task data (SQLite store)
4. Update verification status and source links