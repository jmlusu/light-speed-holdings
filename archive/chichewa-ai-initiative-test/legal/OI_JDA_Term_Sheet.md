# JOINT DEVELOPMENT AGREEMENT — TERM SHEET
## Light Speed Holdings × Opportunity International
### "UlangiziAI v2 Multi-Agent Platform Co-Development"

**Status:** DRAFT — For Discussion Only
**Date:** August 2026
**Confidentiality:** CONFIDENTIAL

---

## 1. PARTIES

| Party | Role | Entity |
|-------|------|--------|
| **Light Speed Holdings Inc.** | Platform Provider / Technology Partner | Delaware C-Corp |
| **Opportunity International** | Agricultural Domain Partner / Implementer | US 501(c)(3) / Malawi NGO |

---

## 2. PURPOSE & SCOPE

**Objective:** Co-develop **UlangiziAI v2** — a multi-agent agricultural advisory system for Malawian smallholder farmers, built on Light Speed's Agent Orchestration Platform, deploying via WhatsApp, IVR, and future channels.

### Scope Includes:
- Decomposition of monolithic UlangiziAI into 6 specialist agents + orchestrator
- Integration with Light Speed platform (Agent Registry, MessageBus, Model Serving, Channel Adapters)
- Chichewa language model fine-tuning (agricultural domain)
- Voice pipeline (ASR + TTS) for WhatsApp voice notes + IVR
- Pilot with 50 farmers → 10,000 farmers over 12 months
- Extension officer human-in-the-loop workflow

### Out of Scope (Phase 1):
- Market linkage / financial product origination
- Insurance product development
- Multi-language expansion (Tumbuka, Yao — Phase 2)

---

## 3. RESPONSIBILITIES

### Light Speed Holdings (Platform Provider)
| Deliverable | Timeline | Acceptance Criteria |
|-------------|----------|---------------------|
| Agent Registry v1 (6 agents + orchestrator YAML) | Day 45 | Registry validates; Generator produces working agents |
| Chichewa SFT model (50k ag QA pairs) | Day 60 | >85% accuracy on UlangiziAI eval set |
| WhatsApp voice E2E pipeline | Day 75 | P95 < 3s; 90%+ completion rate |
| Developer sandbox (API + Python SDK) | Day 60 | External dev can call `/chat` and `/agent/invoke` |
| IVR sandbox (Asterisk + SIP) | Day 75 | 10 concurrent calls; DTMF + speech |
| Platform SLA (production) | Day 120 | 99.5% uptime; <2s P95 latency |

### Opportunity International (Domain Partner)
| Deliverable | Timeline | Notes |
|-------------|----------|-------|
| Agricultural knowledge base (structured) | Day 30 | Crop calendars, pest IDs, market data, Ministry bulletins |
| Farmer cohort for pilot (50 farmers, 3 districts) | Day 60 | Diverse crops, literacy levels, gender balance |
| Extension officer panel (5 officers) | Day 60 | For human-in-loop review + RLHF labeling |
| WhatsApp Business API access | Day 30 | Template approval; opt-in management |
| Ministry of Ag data access facilitation | Day 45 | Official bulletins, AIP data, depot stock |
| User research / usability testing | Ongoing | Monthly farmer feedback sessions |

---

## 4. INTELLECTUAL PROPERTY

### 4.1 Ownership
| Asset | Owner | License to Counterparty |
|-------|-------|-------------------------|
| **Light Speed Platform** (Agent Registry, MessageBus, Orchestration, Channel Adapters, Model Serving, Developer Portal) | Light Speed | Royalty-free, non-exclusive license for UlangiziAI v2 deployment |
| **Agent Definitions** (YAML specs, prompts, tool configs for 6 specialist agents) | **Joint** | Each party may use independently; improvements shared |
| **Agricultural Knowledge Base** (structured content, FAQs, decision trees) | Opportunity International | Perpetual, worldwide, royalty-free for platform operation |
| **Fine-Tuned Model Weights** (Chichewa agricultural LLM) | **Joint** | Each party may deploy commercially; improvements shared |
| **Training Data** (farmer interactions, RLHF labels, officer corrections) | **Joint** (anonymized) | Each party may use for model improvement |
| **Farmer Personal Data** | Farmers (data subjects) | OI = Controller; Light Speed = Processor (per DPA) |

### 4.2 Model Weights — Special Provisions
- Base model: LLaMA-3-8B (Apache 2.0) — per upstream license
- Fine-tuned weights: Joint ownership; either party may commercialize
- **National Asset Clause**: If Malawi Government exercises rights, both parties grant royalty-free license to Government
- **Open Science**: Benchmark results (not weights) publishable after 12-month embargo

---

## 5. COMMERCIAL TERMS

### 5.1 Phase 1 (Months 1-12) — Grant-Funded Core
| Component | Funding Source | Amount |
|-----------|----------------|--------|
| Platform development (Light Speed) | Light Speed internal | $1.2M |
| Chichewa model training | Light Speed internal | $0.5M |
| Pilot operations (farmers, officers, devices) | OI / Gates / WB grants | $0.8M |
| **Total Phase 1** | | **$2.5M** |

### 5.2 Phase 2+ (Month 13+) — Commercial
| Revenue Stream | Split | Notes |
|----------------|-------|-------|
| **Government/NGO Platform SaaS** | 60% Light Speed / 40% OI | OI provides domain support; Light Speed provides platform |
| **Premium Farmer Services** (market linkage, insurance, finance) | 20% Light Speed / 80% OI | OI originates; Light Speed provides tech |
| **Developer API Usage** (third-party agritechs) | 70% Light Speed / 30% OI | OI provides ag data feeds |
| **Data/Insights Products** (Govt dashboard, analytics) | 50% / 50% | Joint product |

### 5.3 Most Favored Nation
If Light Speed grants more favorable commercial terms to any other agricultural NGO/Govt partner for substantially similar services, OI receives equivalent terms prospectively.

---

## 6. DATA PROTECTION & PRIVACY

### 6.1 Roles
- **Controller**: Opportunity International (farmer relationship, consent)
- **Processor**: Light Speed Holdings (platform, inference, analytics)
- **Sub-processors**: Pre-approved list (AWS, Lambda Labs, Twilio, ClickHouse); 30-day notice for new

### 6.2 Key DPA Terms
- **Data Residency**: Primary Malawi (local K8s); Secondary EU; No US without SCCs
- **Retention**: Voice 90 days → auto-delete; Text 2 years; Model weights perpetual
- **Farmer Rights**: Access, rectification, erasure, portability via *384*0# or WhatsApp
- **Breach Notice**: 24hr to OI; 72hr to MACRA/WB; Farmer notice in Chichewa
- **Audit**: OI may audit annually; Light Speed provides SOC 2 Type II

### 6.3 Consent Architecture (Layered)
1. **Voice Consent (IVR)**: "Press 1 to agree to recording for service improvement"
2. **Granular Purpose Consent (WhatsApp)**: ☐ Advice ☐ Model improvement ☐ Research ☐ Third-party
3. **Community Consent**: Village headman + cooperative approval for cultural knowledge
4. **Withdrawal**: *384*0# → 30-day technical fulfillment; confirmation SMS

---

## 7. GOVERNANCE

### 7.1 Steering Committee (Quarterly)
| Seat | Appointee |
|------|-----------|
| Chair | Alternating (Light Speed CEO / OI CEO) |
| Light Speed | CTO, CoS |
| Opportunity International | CTO, UlangiziAI Product Lead |
| Observer | World Bank Task Team Leader (invited) |

**Decisions**: Budget >$50k, scope changes, IP disputes, commercial terms, pilot expansion

### 7.2 Working Groups (Bi-weekly)
- **Technical**: Lead Backend (LS) + ML Lead (OI) — architecture, integrations, model eval
- **Product**: PM (LS) + Product Lead (OI) — user stories, prioritization, UX
- **Field Operations**: Malawi Liaison (LS) + Country Director (OI) — pilot logistics, farmer feedback

---

## 8. PERFORMANCE METRICS & SLAs

| Metric | Target | Measurement | Remedy |
|--------|--------|-------------|--------|
| API Uptime | 99.5% | Monthly | Service credits: 5% fee per 0.1% below |
| Query Resolution Rate | >70% (v2) vs 45% (v1) | Monthly farmer survey | Root cause analysis + sprint |
| Farmer CSAT | >4.0/5.0 | Quarterly | Co-design session + UX iteration |
| Model Accuracy (Ag QA) | >83% | Continuous eval | Retraining sprint |
| Voice Pipeline Latency | P95 < 2.5s | Continuous | Infrastructure scaling |
| Extension Officer Adoption | >80% weekly active | Monthly | Training + workflow integration |

---

## 9. TERM & TERMINATION

| Provision | Term |
|-----------|------|
| **Initial Term** | 3 years from Effective Date |
| **Renewal** | 2 × 1-year options (mutual agreement) |
| **Termination for Convenience** | 180 days written notice (after Year 1) |
| **Termination for Cause** | 60-day cure period (material breach) |
| **Insolvency** | Immediate |
| **Force Majeure** | 90 days → either party may terminate |

### 9.1 Transition Obligations (on Termination/Expiry)
- **Data Export**: All farmer data, interaction logs, model artifacts in open formats (JSONL, Parquet, Safetensors) within 60 days
- **Model Weights**: Joint ownership continues; both parties retain full rights
- **Platform Access**: 180-day wind-down access for OI to migrate
- **Knowledge Transfer**: 20 hours documented handover; runbooks, architecture docs

---

## 10. LIABILITY & INDEMNIFICATION

| Cap | Amount |
|-----|--------|
| **Aggregate Liability Cap** | 12 months' fees paid/payable (excl. grants) |
| **Exclusions from Cap** | IP infringement, data breach (gross negligence), willful misconduct |
| **Indemnification** | Each party indemnifies for own IP violations, regulatory breaches |
| **Agricultural Advice Liability** | OI indemnifies Light Speed for content accuracy; Light Speed indemnifies for platform failures |

---

## 11. DISPUTE RESOLUTION

1. **Good Faith Negotiation** (30 days) — Steering Committee level
2. **Mediation** (ICC Rules, Lilongwe or London) — 60 days
3. **Arbitration** (ICC, 3 arbitrators, English law, Lilongwe seat) — Binding
4. **Injunctive Relief** — Either party may seek in competent court

---

## 12. KEY DEFINITIONS

| Term | Definition |
|------|------------|
| **"Agent"** | YAML-defined autonomous unit with tools, permissions, prompt, model config |
| **"Orchestrator"** | Meta-agent routing queries to specialist agents + synthesizing responses |
| **"MessageBus"** | JSON task queue (.opencode/inbox.json) + executor loop |
| **"SFT"** | Supervised Fine-Tuning (instruction tuning on agricultural QA pairs) |
| **"RLHF"** | Reinforcement Learning from Human Feedback (officer + farmer ratings) |
| **"ASR/TTS"** | Automatic Speech Recognition / Text-to-Speech (Whisper + Piper) |
| **"IVR"** | Interactive Voice Response (Asterisk + SIP trunk) |

---

## 13. SIGNATURES

| Light Speed Holdings | Opportunity International |
|---------------------|---------------------------|
| Name: _______________ | Name: _______________ |
| Title: _______________ | Title: _______________ |
| Date: _______________ | Date: _______________ |

---

## APPENDIX A: AGENT REGISTRY v1 — 6 SPECIALIST AGENTS

| Agent ID | Name | Domain | Primary Tools | Escalation Threshold |
|----------|------|--------|---------------|---------------------|
| `weather-agent` | Weather Advisor | Forecasts, planting windows, alerts | MET API, satellite imagery | <0.7 confidence |
| `market-agent` | Market Advisor | Commodity prices, buyers, transport | MACE, RATIN, farmer reports | <0.7 confidence |
| `crop-agent` | Crop Advisor | Varieties, calendars, intercropping | Ministry bulletins, CGIAR | <0.7 confidence |
| `pest-agent` | Pest Advisor | ID, IPM, pesticide safety | CABI, Ministry alerts | <0.8 confidence (safety) |
| `finance-agent` | Finance Advisor | Input loans, insurance, mobile money | NBS Bank, Airtel Money APIs | <0.7 confidence |
| `subsidy-agent` | Subsidy Advisor | AIP eligibility, depot stock, redemption | Ministry AIP data, logistics | <0.7 confidence |
| `orchestrator` | UlangiziAI Orchestrator | Routing, synthesis, HIL escalation | All above + human queue | N/A |

---

*End of Term Sheet — Subject to Legal Review and Mutual Agreement*
