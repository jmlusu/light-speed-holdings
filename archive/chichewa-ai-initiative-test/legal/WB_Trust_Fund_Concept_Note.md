# WORLD BANK TRUST FUND CONCEPT NOTE
## Digital Development Trust Fund / Development Grant Facility
### "Chichewa AI Agricultural Advisory Platform — Scaling Digital Inclusion in Malawi"

**Submitted by:** Light Speed Holdings (Technical Partner) + Ministry of Agriculture, Malawi (Government Counterpart)
**Date:** August 2026
**Classification:** CONFIDENTIAL — For WB Internal Review Only

---

## 1. EXECUTIVE SUMMARY

| Field | Detail |
|-------|--------|
| **Project Title** | Chichewa AI Agricultural Advisory Platform: From Pilot to National Scale |
| **Countries** | Malawi (primary); Replicable to Zambia, Mozambique, Tanzania |
| **Sector** | Digital Development / Agriculture / Human Capital |
| **Trust Fund Window** | Digital Development Trust Fund (primary) / DGF (secondary) |
| **Requested Amount** | **$1,000,000** (over 24 months) |
| **Co-Financing** | Light Speed Holdings: $2.5M (platform + model dev); Gates Foundation: $0.75M (aligned); Govt Malawi: In-kind (data, officers, infra) |
| **Total Project Cost** | **$4.25M** (24 months) |
| **Implementation Period** | 24 months (Sep 2026 – Aug 2028) |
| **WB Task Team Leader** | [Name], Digital Development Practice, AFE |
| **Government Counterpart** | Ministry of Agriculture (Principal Secretary) |
| **Technical Partner** | Light Speed Holdings Inc. |

---

## 2. DEVELOPMENT CHALLENGE

### 2.1 The Problem
Malawi's 3.5 million smallholder farming households face a **critical advisory gap**:
- **Extension ratio**: 1 officer per 1,750 farmers (target 1:400)
- **Language barrier**: 80%+ speak Chichewa; digital tools English-only
- **Channel limitation**: Radio/SMS one-way; no interactive, personalized advice
- **Subsidy leakage**: AIP verification manual; 30%+ error/fraud estimated
- **Gender gap**: Women farmers 40% less likely to access advisory

### 2.2 The Opportunity
**June 2026**: Malawi launched the **world's first National Language Data Trust** for Chichewa (12M speakers), backed by World Bank ($5M) and Gates Foundation ($3M), compiling **7,000+ hours of audio/text** — a unique digital public good.

**Existing asset**: UlangiziAI (Opportunity International + Gooey.AI) — 5,000 farmers on WhatsApp, but monolithic, text-only, no IVR, no government integration.

### 2.3 The Gap
**No platform exists** to operationalize this Data Trust into scalable, multi-modal, government-integrated services. The missing layer: **agent orchestration infrastructure** that transforms raw data → specialist AI agents → multi-channel deployment (WhatsApp, IVR, USSD) → national scale.

---

## 3. PROJECT DESCRIPTION

### 3.1 Theory of Change
```
DATA TRUST (7,000hr Chichewa)
    → AGENT ORCHESTRATION PLATFORM (Light Speed)
    → MULTI-AGENT ULANGIZIAI v2 (6 specialists + orchestrator)
    → MULTI-CHANNEL DEPLOYMENT (WhatsApp, IVR, USSD, Web)
    → GOVERNMENT INTEGRATION (Extension officers, AIP, Dashboard)
    → SCALE (10K → 100K → 1M farmers)
    → REPLICABLE PLAYBOOK (Tumbuka, Yao, Sena, Bemba, Shona...)
```

### 3.2 Project Components

#### **Component 1: Platform & Model Development ($600k WB / $1.7M Total)**
| Activity | Description | Timeline |
|----------|-------------|----------|
| 1.1 Data Pipeline | ZBS audio → diarization → Whisper transcription → alignment → quality filter → HF dataset | M1-4 |
| 1.2 Tokenizer & Continued PT | Chichewa-optimized tokenizer (fertility <2.5); 1B token continued pretraining on LLaMA-3-8B | M2-5 |
| 1.3 Supervised Fine-Tuning | 50k agricultural QA pairs (Ministry + CGIAR + farmer queries) → instruction-tuned model | M4-7 |
| 1.4 Voice Models | Whisper-large-v3 Chichewa FT (WER<10%); Piper TTS (2 voices, MOS>3.5) | M4-8 |
| 1.5 Agent Orchestration Platform | Agent Registry (YAML), MessageBus, Orchestrator, Channel Adapters (WhatsApp, IVR, USSD, API) | M1-6 |
| 1.6 RLHF / RLAIF | Farmer feedback + officer ratings → preference learning → 15% quality gain | M9-18 |

#### **Component 2: Pilot & Validation ($200k WB / $0.8M Total)**
| Activity | Description | Timeline |
|----------|-------------|----------|
| 2.1 Pilot Design | 50 farmers × 3 districts; RCT design with WB DIME; Gender-stratified | M2-3 |
| 2.2 WhatsApp Deployment | 2-way messaging; Voice notes; Farmer profiles; Officer escalation | M4-6 |
| 2.3 IVR Sandbox | Asterisk + SIP; *384# toll-free; DTMF + speech; AIP verification flow | M5-7 |
| 2.4 Extension Officer Copilot | AI-assisted responses; Knowledge base; Workflow integration | M5-8 |
| 2.5 Impact Evaluation | Baseline/midline/endline; Yield, income, adoption, women's empowerment | M6, M12, M18 |

#### **Component 3: Government Integration & Scale ($150k WB / $1.0M Total)**
| Activity | Description | Timeline |
|----------|-------------|----------|
| 3.1 Ministry Dashboard | Real-time adoption, crop alerts, policy simulation, officer activity | M7-12 |
| 3.2 AIP Integration | IVR eligibility check; Depot stock; Complaint logging; Grievance redress | M8-14 |
| 3.3 National Rollout Prep | 10-district scale plan; Procurement specs; Budget submission (FY28) | M10-18 |
| 3.4 Multi-Language Factory | Template: Chichewa → Tumbuka (2M speakers) in 6 weeks; Yao, Sena, Lomwe | M12-24 |

#### **Component 4: Capacity Building & Knowledge ($50k WB / $0.25M Total)**
| Activity | Description | Timeline |
|----------|-------------|----------|
| 4.1 ML Engineering Training | 50 Malawian engineers (Unima, MUST, Mzuzu); Curriculum + apprenticeships | M6-24 |
| 4.2 Open Knowledge Products | Model cards, benchmarks, training code, playbook → Public (12-mo embargo) | M12-24 |
| 4.3 Regional Dissemination | Africa AI Forum, Indaba, Malawi AI Forum; Playbook for 5+ countries | M18-24 |

---

## 4. ALIGNMENT WITH WORLD BANK PRIORITIES

| WB Priority | Project Alignment |
|-------------|-------------------|
| **Digital Transformation** | First national-scale AI platform for African language; Government-owned digital public infrastructure |
| **Agricultural Productivity** | Direct advisory to 100K+ farmers; Evidence-based yield/income impact (RCT) |
| **Digital Inclusion** | Voice-first (IVR/USSD) reaches feature-phone users (70% of farmers); Chichewa language |
| **Gender Equality** | 50% women farmer target; Gender-disaggregated M&E; Women officer recruitment |
| **Capacity Building** | 50 Malawian ML engineers; University partnerships; Open curriculum |
| **Regional Public Good** | Replicable agent factory for 50+ Bantu languages; Open benchmarks |
| **IDA19/20 Themes** | Human Capital, Jobs & Economic Transformation, Governance & Institutions |
| **Digital Malawi Project (P173456)** | Directly supports Component 2 (Digital Platforms) and Component 3 (Digital Skills) |

---

## 5. IMPLEMENTATION ARRANGEMENTS

### 5.1 Governance Structure
```
STEERING COMMITTEE (Quarterly)
  Co-Chairs: PS Ministry of Agriculture / CEO Light Speed
  Members: WB TTL, Gates Rep, MACRA, Extension Director, ICT Director, AIP Coordinator

TECHNICAL WORKING GROUP (Bi-weekly)
  Lead: ICT Director (Govt) / Lead Backend (Light Speed)
  Members: Extension officers, ML engineers, DevOps, Data officers, Security

IMPLEMENTATION UNIT (Light Speed)
  Project Director (CTO-level), Malawi Country Lead, PM, 12.5 FTE technical team
```

### 5.2 Procurement
- **Light Speed Services**: Single-source justified (unique platform + Data Trust alignment) — WB prior review
- **Telecom (IVR/USSD)**: Competitive (Airtel vs TNM) — National competitive bidding
- **Cloud/GPU**: Competitive (Lambda, RunPod, AWS, Azure) — Shopping
- **Local Consultants** (M&E, legal, translation): National competitive / Individual consultant selection

### 5.3 Financial Management
- **Flow**: WB → Light Speed (Designated Account) → Sub-contractors
- **Reporting**: Quarterly IFRs; Annual audit (Big 4); WB supervision missions (semi-annual)
- **Currency**: USD (Light Speed); MWK (Govt counterpart) — hedged at signing rate

---

## 6. RESULTS FRAMEWORK

### 6.1 PDO Indicators
| Indicator | Baseline | Y1 Target | Y2 Target | Data Source |
|-----------|----------|-----------|-----------|-------------|
| **Farmers receiving AI advisory (disaggregated by gender)** | 5,000 | 25,000 (50% women) | 100,000 (50% women) | Platform analytics + survey |
| **Extension officers using AI copilot** | 0 | 200 | 1,000 | Officer login analytics |
| **AIP subsidy verifications via IVR** | 0 | 10,000 | 100,000 | IVR logs + AIP database |
| **Query resolution rate** | 45% | 70% | 80% | Farmer survey (quarterly) |
| **Model accuracy (agricultural QA benchmark)** | 60% | 83% | 87% | Continuous eval pipeline |

### 6.2 Intermediate Results Indicators
| Indicator | Target | Component |
|-----------|--------|-----------|
| Chichewa model WER (ASR) | <10% | 1.4 |
| Chichewa model MOS (TTS) | >3.5 | 1.4 |
| Agent Registry agents deployed | 6 + orchestrator | 1.5 |
| Developer portal registered users | 100 | 1.6 |
| Malawian engineers trained | 50 | 4.1 |
| Open benchmarks published | 5 (Chichewa, Tumbuka, Yao, Sena, Lomwe) | 4.2 |
| Regional playbook downloads | 500 | 4.3 |

---

## 7. RISKS & MITIGATION

| Risk | Rating | Mitigation |
|------|--------|------------|
| **Political instability / policy reversal** | High | Multi-stakeholder MoUs; WB backing; Portable architecture; Election-cycle planning |
| **Data access delays (ZBS, Govt)** | High | Synthetic data pipeline; Common Voice fallback; Legal escalation; WB convening |
| **Model quality insufficient for agriculture** | Substantial | Ensemble with English; Human-in-loop fallback; Continuous eval; External audit |
| **Compute cost overrun** | Substantial | Reserved instances; Model distillation (8B→1B); CPU fallback; Budget contingency |
| **Farmer adoption below target** | Substantial | Co-design; Community liaisons; Voice-first UX; Incentives (airtime, input vouchers) |
| **Regulatory block (MACRA IVR license)** | Moderate | Early engagement; Legal pre-clearance; USSD fallback; WB policy dialogue |
| **Talent acquisition failure** | Moderate | Remote-first; Contractor pipeline; University partnerships; Diaspora engagement |
| **Partner misalignment** | Moderate | Quarterly steering; Clear JDA scopes; Exit clauses; WB mediation |
| **Safety incident (bad advice)** | Low/High | Constitutional AI guardrails; Red teaming; Insurance; 24hr incident response |
| **Traditional knowledge disputes** | Low/Moderate | Community consent framework; Benefit sharing; WIPO guidelines; Legal review |

---

## 8. SUSTAINABILITY & EXIT STRATEGY

### 8.1 Financial Sustainability (Post-Grant)
| Revenue Stream | Year 2 | Year 3 | Year 5 |
|----------------|--------|--------|--------|
| Govt Platform Contract | $300k | $600k | $1.5M |
| IVR Operations | $150k | $300k | $500k |
| Developer API | $50k | $200k | $1M |
| Regional Licenses | $0 | $100k | $2M |
| **Total** | **$500k** | **$1.2M** | **$5M** |

### 8.2 Institutional Sustainability
- **Government Ownership**: Model = National Asset; Platform on Govt cloud; Officers trained
- **Local Capacity**: 50 engineers → core team for maintenance + new languages
- **Open Standards**: Platform APIs open; Model benchmarks public; No vendor lock-in
- **Regional Network**: Malawi as hub for SADC language AI replication

### 8.3 Exit Triggers (Grant Close)
- MSA signed between Ministry and Light Speed (3-year + options)
- 50 engineers certified; 3 university curricula updated
- Tumbuka model deployed; Playbook published
- Platform generating >$500k ARR from non-grant sources

---

## 9. ENVIRONMENTAL & SOCIAL SAFEGUARDS (ESS10)

### 9.1 Stakeholder Engagement Plan
| Stakeholder | Engagement Method | Frequency |
|-------------|-------------------|-----------|
| Smallholder farmers (men/women) | Focus groups, CATI surveys, IVR feedback | Quarterly |
| Extension officers | Workshops, WhatsApp group, monthly pulse | Monthly |
| Farmer organizations (NASFAM, CISANET) | Advisory board meetings | Quarterly |
| Traditional leaders | Community meetings (consent for cultural knowledge) | Per language expansion |
| Private sector (agritechs, fintechs) | Hackathons, API sandbox, partnership dialogues | Bi-annual |

### 9.2 Grievance Redress Mechanism
- **Channel 1**: IVR *384*9# (voice complaint, auto-transcribed, routed)
- **Channel 2**: WhatsApp "Report Issue" button
- **Channel 3**: Extension officer (paper form → digitized)
- **Channel 4**: WB Grievance Redress Service (GRS) — escalation
- **SLA**: Acknowledgment 24hr; Resolution 14 days; Appeal 30 days

### 9.3 Gender Action Plan
- 50% women in pilot cohort; Gender-disaggregated all metrics
- Women extension officer recruitment target: 40%
- Female voice option for TTS (Piper female speaker)
- Gender-specific crop advisory (legumes, vegetables, nutrition)

---

## 10. BUDGET SUMMARY (USD)

| Component | WB Trust Fund | Light Speed | Gates / Other | Govt In-Kind | Total |
|-----------|---------------|-------------|---------------|--------------|-------|
| **1. Platform & Model** | 400,000 | 1,000,000 | 300,000 | — | 1,700,000 |
| **2. Pilot & Validation** | 200,000 | 300,000 | 200,000 | 100,000 | 800,000 |
| **3. Govt Integration** | 150,000 | 500,000 | 150,000 | 200,000 | 1,000,000 |
| **4. Capacity & Knowledge** | 50,000 | 100,000 | 50,000 | 50,000 | 250,000 |
| **Project Management (5%)** | 40,000 | 95,000 | 35,000 | 17,500 | 187,500 |
| **Contingency (10%)** | 84,000 | 199,500 | 73,500 | 36,750 | 393,750 |
| **TOTAL** | **924,000** | **2,194,500** | **808,500** | **404,250** | **4,331,250** |

**WB Request: $1,000,000** (rounded; includes 10% contingency buffer)

---

## 11. IMPLEMENTATION TIMELINE

```
MONTH:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
──────────────────────────────────────────────────────────────────────────────
1.1 Data Pipeline          ████████████
1.2 Tokenizer/PT                 ████████████████
1.3 SFT                              ████████████
1.4 Voice Models                       ████████████████
1.5 Platform Core  ██████████████████████████████
1.6 RLHF                                               ████████████
2.1 Pilot Design     ████
2.2 WhatsApp Deploy          ██████████
2.3 IVR Sandbox                    ██████████
2.4 Officer Copilot                     ████████████
2.5 Impact Eval        B────────M────────E
3.1 Dashboard                              ████████████
3.2 AIP Integration                            ██████████████
3.3 Rollout Prep                                       ████████████████
3.4 Multi-Lang Factory                                                ████████████████
4.1 Training                                                ████████████████████████
4.2 Open Knowledge                                                             ████████████
4.3 Dissemination                                                                          ████████
B=Baseline, M=Midline, E=Endline
```

---

## 12. COMPARATIVE ADVANTAGE OF LIGHT SPEED HOLDINGS

| Criterion | Assessment |
|-----------|------------|
| **Unique Platform** | Only agent orchestration platform designed for low-resource languages (YAML → OpenCode agents + MessageBus) |
| **Data Trust Alignment** | Technical architecture matches Data Trust output (audio → agents → multi-channel) |
| **Malawi Commitment** | CEO/CoS on ground; Malawi liaison hired; Local counsel retained |
| **Track Record** | AI Company Builder (open source); 30+ agent templates; Production CLI tooling |
| **Partnership Model** | Platform partner (not vendor) — aligned incentives with Govt/OI/ZBS |
| **Cost Efficiency** | $0.80/farmer/yr at scale vs. $5-10 for human-only extension |

---

## 13. NEXT STEPS & DECISION POINTS

| Milestone | Target Date | Decision Required |
|-----------|-------------|-------------------|
| **Concept Note Review** | Week 1-2 (Sep 2026) | TTL clearance to proceed |
| **Stakeholder Alignment Workshop** | Week 3 (Lilongwe) | MoU signatures (OI, ZBS, MinAg) |
| **Full Proposal Development** | Week 4-8 | WB team + Light Speed co-draft |
| **Technical Review Panel** | Week 10 | Architecture validation |
| **Trust Fund Committee** | Week 14 | Funding approval |
| **Grant Effectiveness** | Week 18 | Legal agreements signed |
| **Implementation Start** | Week 20 (Oct 2026) | Team mobilized; GPU reserved |

---

## 14. CONTACT INFORMATION

| Role | Name | Email | Phone |
|------|------|-------|-------|
| **Light Speed — CEO** | [Name] | ceo@lightspeed.ai | +1-xxx-xxx-xxxx |
| **Light Speed — CTO** | [Name] | cto@lightspeed.ai | +1-xxx-xxx-xxxx |
| **Light Speed — Malawi Lead** | [Name] | malawi@lightspeed.ai | +265-xx-xxx-xxx |
| **Ministry of Agriculture — PS** | Dr. Godfrey Chingoma | ps@agriculture.gov.mw | +265-xx-xxx-xxx |
| **Ministry of Agriculture — ICT Director** | [Name] | ict@agriculture.gov.mw | +265-xx-xxx-xxx |
| **World Bank — TTL** | [Name] | [name]@worldbank.org | +265-xx-xxx-xxx |
| **World Bank — Digital Dev Practice Manager** | [Name] | [name]@worldbank.org | +1-202-xxx-xxxx |

---

## ANNEXES (TO BE ATTACHED)

1. **Annex A**: Light Speed Company Profile & Platform Architecture
2. **Annex B**: Chichewa Data Trust — Data Inventory & Quality Assessment
3. **Annex C**: UlangiziAI v1 Assessment & Gap Analysis
4. **Annex D**: Draft MoUs (OI, ZBS, MinAg) — Term Sheets attached
5. **Annex E**: Draft JDA (Light Speed × Opportunity International)
6. **Annex F**: Draft Data License (Light Speed × ZBS)
7. **Annex G**: M&E Framework (with DIME RCT design)
8. **Annex H**: Gender Action Plan (detailed)
9. **Annex I**: Stakeholder Engagement Plan (detailed)
10. **Annex J**: Risk Register (full 15-risk register with mitigation owners)
11. **Annex K**: Procurement Plan (18-month)
12. **Annex L**: Financial Management Assessment (Light Speed)

---

*End of Concept Note — For World Bank Internal Review and Decision*
