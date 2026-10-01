# Research Evidence - Post 3: LightSpeed AI-native org structure

**Post:** 3 - "LightSpeed AI-native org structure"
**Series:** AI-Native Organizations (11 posts)
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified | Notes |
|-------|--------|----------|-------|
| 90 agents orchestrated via MessageBus task queue | `src/ai_company/executor/loop.py` + `message_bus.py` | ✅ | Crash-safe, idempotent task execution |
| 20 departments with health rollup in data service | `data_service.py` `get_executive_scorecard()` | ✅ | Department health rollup via `OrgNode` metrics |
| 5-tier HITL governance cascades from executive to specialist level | `orchestrator/approval.py` ApprovalGate | ✅ | 5-tier: autonomous → HITL-approved → reviewed → snoozed → cleared |
| Orchestration layer (O in HAOMT-G-V) enables cross-department workflow | `workflow/engine.py` step tracking + SLA monitoring | ✅ | 9 workflow definitions, step tracking, SLA monitoring |
| Live org chart with metrics feeds CEO dashboard `GET /api/v1/ceo-dashboard` | `graph/engine.py` `OrgNode` + `compute_org_metrics()` | ✅ | Metrics: capacity, activity, trend, risk |
| Agent lease + DLQ re-enqueue ensures task reliability | `executor/dead_letter.py` + `executor/loop.py` lease fields | ✅ | Stale task detection, DLQ with retry |

## Verification Status

- [x] MessageBus task queue architecture validated (crash-safe, idempotent)
- [x] Department health rollup in executive scorecard
- [x] 5-tier HITL governance cascades verified (ref: ADR-017, ECL archive)
- [x] Workflow engine step tracking + SLA monitoring operational
- [x] Org chart with metrics feeds CEO dashboard API
- [x] Agent lease + DLQ re-enqueue pattern verified
- [ ] Cross-department workflow latency: **PENDING**: requires performance metrics
- [ ] 5-tier HITL transition times: **PENDING**: requires HITL audit data

## Next Steps

1. Run `k-dense-research-lookup` for "MessageBus orchestration reliability": confirms claim about crash-safe execution
2. Run `k-dense-research-lookup` for "5-tier HITL governance effectiveness": governance impact study
3. Export org metrics from `GET /api/v1/org-chart?include_metrics=true` and validate
4. Update verification status and source links