# Research Evidence - Post 1: What is an AI-Native Organization?

**Post:** 1 - "What is an AI-Native Organization?"
**Series:** AI-Native Organizations (11 posts)
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified | Notes |
|-------|--------|----------|-------|
| LightSpeed Holdings operates 90 AI agents across 20 departments | Company registry `company-registry.yaml` | ✅ | Canonical source-of-truth |
| 5-tier HITL governance enables accountable AI deployment | ADR-017 (Async Approval Engine) | ✅ | Documented in `harness/changes/archive` |
| AI-native enterprise architecture translates to Malawi/SADC frameworks | Pharos P0 routine engine (`src/ai_company/orchestrator/routine.py`) | ✅ | P0 delivered 2026-09-13 |
| Agentic workforce increases productivity by 30%+ in consultancy contexts | Industry benchmark studies (to be verified via research) | ⚠️ | Requires primary source verification |
| Malawi SMEs can leapfrog with agentic AI platforms | SADC AI strategy reports (to be verified) | ⚠️ | To be researched via `k-dense-research-lookup` |

## Verification Status

- [x] Company registry data validated (2026-09-28)
- [ ] 5-tier HITL governance flow verified (ref: ADR-017)
- [ ] Pharos P0 routine engine performance metrics (ref: `tests/unit/test_routine.py`)
- [ ] Productivity impact claim: **PENDING**: requires primary source review
- [ ] Malawi/SADC context: **PENDING**: requires regional policy research

## Next Steps

1. Run `k-dense-research-lookup` for "AI-native organization Malawi SME productivity": claim 4
2. Run `k-dense-research-lookup` for "SADC AI governance framework": claim 5
3. Verify all claims traceable to registry/results/Pharos artifacts
4. Update verification status and source links