# THE CHICHEWA AI INITIATIVE
## Executive Presentation — Light Speed Holdings
**CONFIDENTIAL | Board & CEO Only | August 2026**

---

## SLIDE 1: THE OPPORTUNITY IN ONE SENTENCE

> **Malawi has built the world's first National Language Data Trust for Chichewa (12M speakers). We can provide the agent orchestration platform that turns this data into scalable, multi-modal AI services for African agriculture — starting with 10,000 farmers in 9 months.**

---

## SLIDE 2: WHY NOW — CONVERGENCE OF THREE FORCES

| Force | Signal | Our Window |
|-------|--------|------------|
| **Supply** | 7,000+ hrs Chichewa audio/text (ZBS, Govt archives) — World Bank + Gates funded | **Data ready NOW** |
| **Demand** | 80% of Malawi in agriculture; <30% smartphone penetration; voice-first required | **Massive unmet need** |
| **Tech Readiness** | LLaMA-3 + Whisper + Piper + our Agent Platform = production-grade low-resource language stack | **We can build FIRST** |

**First-mover advantage:** No one has deployed multi-agent orchestration for African language AI at national scale.

---

## SLIDE 3: STRATEGIC FIT — OUR PLATFORM MEETS THEIR NEED

| Initiative Need | Our Platform Capability | Moat |
|-----------------|------------------------|------|
| UlangiziAI is monolithic → needs specialist agents | **Agent Registry + Orchestration + MessageBus** (YAML-defined, generated) | **Platform, not project** |
| Voice + WhatsApp + IVR + USSD channels | **Channel-agnostic adapters** (single agent logic, multi-interface) | **Write once, deploy everywhere** |
| Scale Chichewa → Tumbuka, Yao, Sena, Lomwe | **Agent Factory pattern** (80% registry reuse) | **Replicable across 50+ Bantu languages** |
| Public developer access planned | **Developer Portal + SDK + API** (our core product) | **Own the ecosystem layer** |

---

## SLIDE 4: THE ASK — "PLATFORM PARTNER" ENGAGEMENT

| Dimension | Detail |
|-----------|--------|
| **Role** | Technology/Platform Partner (not vendor, not grantee) |
| **Investment** | **$2.8M direct + $1.6M contingency = $4.4M over 12 months** |
| **Team** | 12.5 FTE (7 ML/Backend, 2 Voice, 1.5 DevOps, 1 Frontend, 1 PM) |
| **Target** | 10,000 active farmers by Month 9; MSA with Malawi Govt by Month 12 |
| **Revenue Path** | Platform SaaS ($300k Y1) + Prof Services ($400k) + Grants ($1M) = **$1.85M Y1** |

---

## SLIDE 5: 3-PHASE ROADMAP

```
PHASE 1 (M1-3): FOUNDATION          PHASE 2 (M4-6): INTEGRATION         PHASE 3 (M7-12): SCALE
├─ Data pipeline (1,000 hrs)        ├─ SFT Chichewa model (50k QA)      ├─ IVR production (1,000 calls/day)
├─ Tokenizer + Continued PT         ├─ 6 specialist agents + orchestr.  ├─ RLHF from farmer feedback
├─ Agent Registry v1 (6 agents)     ├─ Whisper FT + Piper TTS           ├─ Dialect LoRAs (3 regions)
├─ Dev Sandbox (API + SDK)          ├─ WhatsApp voice E2E               ├─ Public API GA + Hackathon
└─ GATE 1: OI MoU signed            └─ GATE 2: Pilot ready              └─ GATE 3: Scale decision + MSA
```

---

## SLIDE 6: KEY PARTNERSHIPS — TIER 1 (MUST CLOSE DAYS 1-30)

| Partner | What We Need | What They Get | Structure |
|---------|--------------|---------------|-----------|
| **Opportunity International** | Co-dev UlangiziAI v2; farmer access; ag knowledge base | Multi-agent architecture; scale to new languages; platform ownership | **JDA** — Revenue share on premium; grant-funded core |
| **Zodiak Broadcasting (ZBS)** | 7,000hr audio archive license | Revenue share; co-branded "ZBS AI" hotline; digital transformation | **Data License + Co-Marketing** — $50k/yr + 10% rev share |
| **Malawi Ministry of Agriculture** | National integration; extension officer network; Govt dashboard | 2,000+ officers AI-enabled; policy insights; capacity building | **MoU → MSA** — $200-500k/yr + WB co-financing |
| **World Bank (Digital Dev)** | Technical partner designation; co-funding | Implementation capacity; innovation showcase; sustainability | **Trust Fund / DGF** — $1M target |

---

## SLIDE 7: MVP — ULANGIZIAI v2 (90-DAY PILOT)

**6 Specialist Agents + Orchestrator → WhatsApp (Text + Voice) → 50 Farmers**

| Agent | Domain | Data Source |
|-------|--------|-------------|
| **Weather** | Forecasts, planting windows, alerts | MET Malawi + satellite |
| **Markets** | Commodity prices, buyer contacts, transport | MACE + RATIN + farmer reports |
| **Crops** | Varieties, calendars, intercropping | Ministry of Ag + CGIAR |
| **Pests** | ID, IPM, pesticide safety (regulated) | CABI + Ministry bulletins |
| **Finance** | Input loans, insurance, mobile money | NBS Bank + Airtel Money + NGOs |
| **Subsidies** | AIP eligibility, depot stock, redemption | Ministry + Logistics Unit |

**Human-in-loop:** Extension officers review <70% confidence; farmer feedback → RLHF

---

## SLIDE 8: FINANCIAL SNAPSHOT

| Category | 12-Month Investment |
|----------|---------------------|
| **Personnel (12.5 FTE)** | $2.98M |
| **GPU Compute (Training + Inference)** | $0.42M |
| **Telecom (IVR, WhatsApp, SMS)** | $0.06M |
| **Legal, Travel, Malawi Office** | $0.24M |
| **Contingency (20%)** | $0.59M |
| **TOTAL** | **$4.43M** |

| Revenue Projection (Base Case) | Y1 | Y2 | Y3 |
|--------------------------------|-----|-----|-----|
| Platform SaaS | $300k | $800k | $2.0M |
| Professional Services | $400k | $600k | $800k |
| API/Usage | $150k | $500k | $1.2M |
| Grants/Contracts | $1.0M | $500k | $200k |
| **TOTAL REVENUE** | **$1.85M** | **$2.4M** | **$4.2M** |

**Unit Economics at Scale (Y3):** $0.80/farmer/yr cost | 3.0x LTV/CAC | 78% gross margin

---

## SLIDE 9: TOP 5 RISKS & MITIGATIONS

| Risk | Likelihood × Impact | Mitigation |
|------|---------------------|------------|
| **1. Political/Policy Reversal** | Medium × Critical | Multi-stakeholder MoUs; WB backing; portable architecture |
| **2. Data Access Delayed** | Medium × High | Synthetic data pipeline; Common Voice; legal escalation path |
| **3. Model Quality Insufficient** | Medium × High | Ensemble with English; human-in-loop; continuous eval |
| **4. Compute Cost Overrun** | High × Medium | Reserved instances; distillation; CPU fallback |
| **5. Farmer Adoption < Target** | Medium × High | Co-design; community liaisons; voice-first UX; incentives |

**Risk Philosophy:** Speed to pilot (90 days) de-risks technical, adoption, and partner risks simultaneously.

---

## SLIDE 10: GOVERNANCE & DECISION RIGHTS

```
STEERING COMMITTEE (Monthly)     → Budget >$100k, Strategic pivots, Partner MSAs
  CEO (Chair) • CTO • COO • CLO • CSO • CFO • CoS
         │
PMO (Bi-weekly)                  → Sprint scope, Resources, Risk escalation
  CoS • PM • Workstream Leads
         │
├── TECH (CTO)     ├── BUSINESS (BD)     ├── PRODUCT (CPO)
├── LEGAL (CLO)    ├── RESEARCH (ML)     └── COMMS (CMO)
```

**Gate Reviews (CEO/Board Decisions):**
- **Gate 1 (Day 30):** OI MoU signed + ZBS NDA → Release budget + hiring
- **Gate 2 (Day 60):** Technical feasibility confirmed → Phase 2 go-ahead
- **Gate 3 (Day 90):** Pilot results → Scale / Pivot / Pause + MSA negotiation

---

## SLIDE 11: IMMEDIATE ACTIONS — THIS WEEK

| Action | Owner | Deadline |
|--------|-------|----------|
| CEO calls: OI CEO, ZBS Director, WB Task Team Leader | CEO/CoS | **Day 3** |
| Tiger Team formed + charter signed | CoS | **Day 3** |
| Technical deep-dive with OI/Gooey.AI engineering | CTO/Lead Backend | **Day 7** |
| MoU templates drafted (OI, ZBS, Govt) | CLO | **Day 7** |
| Malawi visas + local counsel retained | COO/Ops | **Day 10** |
| GPU quota reserved (A100/H100) | CTO/DevOps | **Day 10** |
| **Gate 1 Target: Signed OI JDA** | CEO/BD | **Day 30** |

---

## SLIDE 12: THE VISION — BEYOND CHICHEWA

```
YEAR 1: Chichewa → 10K farmers → Malawi national platform
YEAR 2: +Tumbuka (2M) + Yao (2M) → 100K farmers → Regional platform
YEAR 3: +Sena, Lomwe, Bemba, Shona → 1M farmers → Continental platform
YEAR 5: Agent Factory for 50+ African languages → $100M ARR potential
```

**We become the "AWS for African Language AI" — the orchestration layer everyone builds on.**

---

## SLIDE 13: DECISION REQUESTED

> **Approve $4.4M / 12-month investment for "The Chichewa AI Initiative" as a strategic Platform Partner engagement, authorizing Gate 1 execution (Week 1-4) with go/no-go at Day 30.**

### Options:
- [ ] **APPROVE** — Full engagement per this plan
- [ ] **APPROVE WITH MODIFICATIONS** — [Specify: budget, scope, timeline, partners]
- [ ] **PILOT ONLY** — $1.5M / 6 months to Gate 2 (technical validation only)
- [ ] **DEFER** — Revisit in Q1 2027 with more market data
- [ ] **DECLINE** — Not a strategic priority

---

## APPENDIX: ONE-PAGE MEMO FOR BOARD PRE-READ

**Available separately** — includes full risk register, detailed financial model, legal framework, competitive landscape, and technical architecture diagrams.

---

**Prepared by:** Chief of Staff
**Date:** August 20, 2026
**Classification:** CONFIDENTIAL — Board/CEO Only
**Version:** 1.0
