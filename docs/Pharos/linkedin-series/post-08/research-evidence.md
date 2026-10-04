# Research Evidence - Post 8: AI Governance in Malawi

**Post:** 8
**Framework Layer:** G - Governance
**Generated:** 2026-09-28

## Claim-to-Source Map

| Claim | Source | Verified |
|-------|--------|----------|
| Four skeptic objections (bandwidth, data protection, tech debt, AI skepticism) with engineered answers | `docs/` Reservations Playbook (`reservations-playbook` skill, positioning.md mapping) | ✅ |
| "We operate in this reality daily" (low bandwidth) | Reservations Playbook: voice column | ✅ |
| Offline-first, local models, WhatsApp-native, PWA queues | Reservations Playbook: engineered answer for bandwidth | ✅ |
| Data Protection Act 2017/2024 + GDPR by default | Malawi DPA 2017 (amended 2024); `config/company/policies.yaml` | ✅ |
| Sovereign in-country data, no foreign-owned models without in-country safeguards | Policy documentation; AGENTS.md §9.2 skill transmission ban (vendor allow-list posture) | ✅ |
| Model deployments registered like agents (scope, permissions, owner) | `company-registry.yaml`; ADR-032 | ✅ |
| Registry as auditor-readable source ("who can see what") | `company-registry.yaml` single source of truth (AGENTS.md §2) | ✅ |
| Five-tier approval matrix (ADR-017): autonomous → HITL-approved → reviewed → snoozed → cleared | `src/ai_company/orchestrator/approval.py`; ADR-017 | ✅ |
| Data access actions default to Tier 2 (HITL-approved) | `orchestrator/approval.py` tier assignment rules | ✅ |
| Approval sweep retires stale requests (EXPIRED terminal state) | AGENTS.md §9.1 HITL Expiry Sweep | ✅ |
| Every agentic decision logged: who, what, when, tier | `orchestrator/approval.py` audit log | ✅ |
| Audit structure without understanding models ("check-this, not trust-me") | Reservations Playbook: voice column; series Posts 6–7 language | ✅ |
| 90-day pilot, no rip-and-replace, no multi-year lock-in, visible variable cost | Business model documentation; series-wide claim | ✅ |
| Variable cost tracked per-model, per-department | `dashboard/data_service.py` cost analytics | ✅ |
| KPI-003 Agent Utilization computed from real sources (not hardcoded) | `config/company/kpis.yaml` (CEO decision 2026-08-08 comment) | ✅ |
| KPI-004 Build Success Rate computed from inbox, target 99.5 | `config/company/kpis.yaml` | ✅ |
| ADR-032: agents consolidated from scripts/session prompts into one registry | ADR-032; AGENTS.md §8 (tool vocabulary consolidation) | ✅ |
| "You cannot govern a population you cannot enumerate" | Series Posts 6–7 (registry rationale) | ✅ |
| Circuit breakers around shared state | `orchestrator` circuit-breaker module; platform-reliability-engineer ownership | ✅ |
| Honesty badges ("when the system does not know, it says so") | Reservations Playbook: "AI failed before" answer; honesty badges referenced in ADR-017 context | ✅ |
| Autonomy earned per action class, not granted at onboarding | Series Posts 6–7 ("install the gates before the autonomy") | ✅ |
| Tier definitions: T1 routine/no commitment; T2 data access/customer-facing; T3 policy/budget; T4 deferred high-impact; T5 treasury/external/legal | `orchestrator/approval.py` | ✅ |
| MACRA as Malawi regulator (authorization, accountability, cross-border questions) | Policy track: regulator briefings for MACRA (AGENTS.md agentic-policy-analyst scope) | ✅ |
| National AI Strategy consultation (Malawi) | Policy track: Malawi National AI Strategy consultation | ✅ |
| SADC Agentic AI Governance Framework | Policy track: SADC Agentic AI Governance Framework | ✅ |
| UNDP / development partners funding pilots | Policy track: UNDP regulator briefings; series plan §8 stakeholder map | ✅ |
| 90 canonical agents (ADR-032) | ADR-032; `source-of-truth.yaml` | ✅ |
| Start with 3–5 agents, one queue before agents, utilization day one, gates before autonomy | Series Posts 5–7 "What a ... Can Copy" blocks | ✅ |
| Low bandwidth changes who can supervise what (governance constraint, not just technical) | Reservations Playbook framing (bandwidth objection) | ✅ |

## Excluded Claims (do NOT include in draft)

| Claim | Reason |
|-------|--------|
| Specific DPA penalty amounts or sections | Not verified against statute text in this session |
| MACRA positions or statements attributed to named officials | No source; policy track briefings not yet delivered |
| "+30% productivity" and similar performance percentages | Untraceable to registry/results |
| SME leapfrog statistics | Not verifiable from repo artifacts |
| Subscriber/engagement projections | Series plan targets are goals, not results |

## Notes

- Policy-landscape items (MACRA, National AI Strategy, SADC framework, UNDP) are framed as *the questions these ask* (who decides, on what basis, how would we know), not as claims about their current positions, consistent with policy-track framing.
- Reservations Playbook answers are quoted structurally (mechanism per reservation) rather than verbatim to keep the voice in builder register.