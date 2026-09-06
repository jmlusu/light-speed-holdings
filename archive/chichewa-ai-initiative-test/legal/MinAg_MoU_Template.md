# MEMORANDUM OF UNDERSTANDING
## Light Speed Holdings Inc. × Republic of Malawi (Ministry of Agriculture)
### "National AI Agricultural Advisory Platform Partnership"

**Status:** DRAFT — For Discussion Only
**Date:** August 2026
**Classification:** OFFICIAL — Government Use

---

## 1. PARTIES

| Party | Represented By | Authority |
|-------|----------------|-----------|
| **Light Speed Holdings Inc.** | Chief Executive Officer | Delaware Corporation, registered foreign company in Malawi |
| **Ministry of Agriculture, Republic of Malawi** | Hon. Minister of Agriculture / Principal Secretary | Government of Malawi, pursuant to Public Finance Management Act |

**Witnessed By:** World Bank Malawi Country Office (Digital Development Practice)

---

## 2. BACKGROUND & CONTEXT

### 2.1 National Initiatives
- **Malawi 2063**: Pillar 1 — Agricultural Productivity & Commercialization
- **Digital Malawi Project** (P173456, $100M IDA): Digital platforms for service delivery
- **National Language Data Trust** (Launched June 2026): Chichewa AI for digital inclusion
- **Affordable Inputs Programme (AIP)**: National subsidy program reaching 3.5M farmers

### 2.2 Current Challenge
- 2,000+ extension officers serve 3.5M farming households (ratio 1:1,750)
- Advisory delivery: In-person, radio, SMS — limited personalization, no real-time interaction
- Farmer query resolution: ~45% via existing UlangiziAI (monolithic, text-only, English/Chichewa)
- Subsidy verification: Manual, paper-based, prone to leakage and delays

### 2.3 Opportunity
Deploy **multi-agent, multi-modal AI platform** (Light Speed Agent Orchestration Platform) to:
- Scale advisory from 5,000 → 100,000+ farmers via WhatsApp, IVR, USSD
- Enable real-time subsidy verification via toll-free IVR (*384#)
- Provide Ministry with real-time adoption, impact, and policy dashboards
- Build Malawian AI engineering capacity (50 engineers trained)

---

## 3. PURPOSE & SCOPE

### 3.1 Objective
Establish a **Public-Private Partnership** for a National AI Agricultural Advisory Platform ("the Platform") that integrates with Ministry extension services, AIP subsidy systems, and the National Language Data Trust.

### 3.2 Scope of Collaboration

| Phase | Timeline | Activities |
|-------|----------|------------|
| **Phase 1: Pilot** | Months 1-6 | 50 farmers × 3 districts; 5 extension officers; WhatsApp + IVR sandbox |
| **Phase 2: District Scale** | Months 7-12 | 10,000 farmers × 10 districts; 200 officers; Full IVR toll-free; Govt dashboard beta |
| **Phase 3: National Rollout** | Year 2-3 | 100,000+ farmers; All 28 districts; 2,000+ officers; Multi-language (Tumbuka, Yao) |
| **Phase 4: Ecosystem** | Year 3+ | Developer platform; Private sector integration; Regional replication |

### 3.3 Key Use Cases
1. **Farmer Advisory**: Multi-agent (Weather, Markets, Crops, Pests, Finance, Subsidies) via WhatsApp/IVR
2. **Extension Officer Copilot**: AI-assisted responses, knowledge base, escalation workflow
3. **AIP Subsidy Verification**: Toll-free IVR (*384#) — eligibility, depot stock, complaint logging
4. **Ministry Dashboard**: Real-time adoption, crop alerts, policy simulation, impact tracking
5. **Capacity Building**: 50 Malawian ML engineers trained (curriculum + apprenticeships)

---

## 4. RESPONSIBILITIES

### 4.1 Light Speed Holdings (Technology Partner)
| Deliverable | Timeline | Success Criteria |
|-------------|----------|------------------|
| Agent Orchestration Platform (core) | Month 3 | 6 agents + orchestrator; MessageBus; Model serving; Channel adapters |
| Chichewa Agricultural LLM (SFT) | Month 4 | >85% accuracy on Ministry ag QA benchmark |
| Voice Pipeline (ASR + TTS) | Month 5 | Whisper WER <10%; Piper MOS >3.5; P95 latency <2.5s |
| WhatsApp Business Integration | Month 4 | Template approved; Opt-in flow; 2-way messaging |
| IVR Platform (Asterisk + SIP) | Month 6 | 100 concurrent calls; DTMF + speech; Toll-free ready |
| Ministry Dashboard (Beta) | Month 8 | Adoption metrics, crop alerts, officer activity, policy insights |
| API / Developer Portal | Month 9 | OpenAPI spec; Python/JS SDKs; Rate limits; Documentation |
| Capacity Building Program | Month 6-18 | 50 engineers trained; Curriculum open-sourced |

### 4.2 Ministry of Agriculture (Government Partner)
| Deliverable | Timeline | Notes |
|-------------|----------|-------|
| **Official Agricultural Data Access** | Month 1 | Crop calendars, pest bulletins, variety lists, AIP guidelines, depot locations |
| **Extension Officer Network** | Month 2 | 5 officers (pilot) → 200 (Phase 2) → 2,000+ (national); MOUs with DADOs |
| **Farmer Registry Access** | Month 3 | AIP beneficiary list (for IVR verification); Data sharing agreement per DPA |
| **MACRA Licensing Support** | Month 3 | IVR toll-free short code (*384#); USSD gateway; Regulatory clearance |
| **Telecom Coordination** | Month 4 | Airtel/TNM engagement; Zero-rated API; SIP trunk provisioning |
| **Policy Champion** | Ongoing | Ministerial directive for officer adoption; Budget line for national rollout |
| **Monitoring & Evaluation** | Quarterly | Joint M&E framework; RCT design (with World Bank); Impact reporting |

### 4.3 Shared Responsibilities
- **Data Governance**: Joint Data Protection Impact Assessment (DPIA); Farmer consent architecture
- **Security**: Joint security audit (quarterly); Incident response plan; MACRA compliance
- **Monitoring**: Quarterly steering committee; Annual independent evaluation
- **Communication**: Joint press releases; Farmer awareness campaigns; Officer training

---

## 5. DATA GOVERNANCE & PRIVACY

### 5.1 Data Roles (Per Malawi Data Protection Act 2024)
| Data Type | Controller | Processor | Legal Basis |
|-----------|------------|-----------|-------------|
| Farmer Personal Data (AIP registry, phone, location) | Ministry | Light Speed | Public task / Consent |
| Farmer Interactions (queries, voice, feedback) | Ministry | Light Speed | Consent (layered) |
| Extension Officer Data | Ministry | Light Speed | Employment contract |
| Model Weights / Analytics | **Joint** | — | National Asset |

### 5.2 Key Principles
- **Data Sovereignty**: Primary storage in Malawi (Government Data Center / Local K8s); EU backup only
- **Farmer Consent**: Layered (Voice IVR → Granular WhatsApp → Community for cultural knowledge)
- **Withdrawal Right**: *384*0# → 30-day purge; Confirmation SMS
- **Retention**: Voice 90 days; Text 2 years; Analytics 5 years; Model weights perpetual
- **Breach Notification**: 24hr Ministry → 72hr MACRA → 72hr World Bank → Farmer notice (Chichewa)

### 5.3 Data Sharing Agreements
Separate DPAs to be executed for:
1. Ministry → Light Speed (Farmer registry, AIP data, officer data)
2. Light Speed → Ministry (Analytics, dashboards, model insights)
3. Tri-party (Ministry, Light Speed, World Bank) for M&E data

---

## 6. INTELLECTUAL PROPERTY

### 6.1 Ownership
| Asset | Owner | License Terms |
|-------|-------|---------------|
| **Light Speed Platform** (Orchestration, Registry, MessageBus, Channel Adapters, Model Serving, Dev Portal) | Light Speed | Royalty-free, non-exclusive, perpetual for Ministry use |
| **Chichewa Agricultural Model Weights** | **National Asset (Government of Malawi)** | Light Speed: Commercial license worldwide; Ministry: Sovereign use; Open benchmark publication (12-mo embargo) |
| **Agent Definitions** (6 specialist agents + orchestrator YAML) | **Joint** | Each party may use independently; Improvements shared |
| **Ministry Data** (Agricultural content, AIP data, farmer registry) | Ministry | Light Speed: Training + inference only; No redistribution |
| **Dashboard / Analytics** | **Joint** | Ministry: Unlimited internal; Light Speed: Platform showcase (anonymized) |

### 6.2 National Asset Clause
The Chichewa Agricultural Model is declared a **National Digital Asset** of Malawi. Government retains:
- Right to deploy on any infrastructure (Govt cloud, partner cloud, edge)
- Right to license to other public entities (health, education, finance)
- Right to require open publication of benchmarks (not weights)
- Right to audit model for bias, safety, cultural alignment

### 6.3 Open Science Commitment
- Training methodology, data sources, evaluation results → Public (after 12-month embargo)
- Model card per Partnership on AI standards
- Chichewa benchmarks contributed to Masakhane / HuggingFace

---

## 7. COMMERCIAL TERMS

### 7.1 Phase 1 (Pilot: Months 1-6) — Grant-Funded
| Component | Funding Source | Amount |
|-----------|----------------|--------|
| Platform Development | Light Speed Internal | $1.2M |
| Model Training | Light Speed Internal | $0.5M |
| Pilot Operations | World Bank Trust Fund / Gates | $0.8M |
| **Total** | | **$2.5M** |

### 7.2 Phase 2+ (National: Year 2+) — Government Contract
| Service | Annual Fee (Target) | Notes |
|---------|---------------------|-------|
| Platform License (2,000+ officers, 100k+ farmers) | $300,000 | Includes support, updates, SLA |
| IVR Toll-Free Operations | $150,000 | Telecom costs + platform |
| Ministry Dashboard & Analytics | $100,000 | Custom reports, policy simulation |
| Capacity Building (ongoing) | $50,000 | Train-the-trainer, curriculum updates |
| **Total Annual** | **$600,000** | Subject to appropriation; 3-year MSA |

### 7.3 Payment Terms
- **Currency**: USD (indexed to MWK/USD at signing) or MWK (at prevailing rate)
- **Schedule**: Quarterly in advance (Platform); Monthly arrears (IVR usage)
- **Appropriation Clause**: Subject to Parliamentary appropriation; 90-day notice if funds unavailable

### 7.4 World Bank Co-Financing
- Ministry to request WB co-financing via Digital Malawi Project restructuring
- Target: 50% Government / 50% IDA for Years 1-2
- Light Speed supports proposal development (technical annexes, costing)

---

## 8. GOVERNANCE

### 8.1 Steering Committee (Quarterly)
| Role | Representative |
|------|----------------|
| **Co-Chairs** | Principal Secretary (Ministry) / CEO (Light Speed) |
| **Ministry** | Director of Extension, ICT Director, AIP Coordinator, M&E Lead |
| **Light Speed** | CTO, COO, Malawi Country Lead, Legal Counsel |
| **Observers** | World Bank TTL, Gates Foundation Rep, MACRA Rep (invited) |

**Mandate**: Strategic direction, budget approval >$100k, policy alignment, dispute resolution, annual review

### 8.2 Technical Working Group (Bi-weekly)
| Role | Representative |
|------|----------------|
| **Lead** | ICT Director (Ministry) / Lead Backend (Light Speed) |
| **Members** | Extension officers, ML engineers, DevOps, Data officers, Security |
| **Mandate** | Sprint planning, technical blockers, security, data pipeline, integrations |

### 8.3 District Implementation Committees (Monthly — Phase 2+)
- Chaired by DADO (District Agriculture Development Officer)
- Members: Extension officers, Light Speed field lead, Farmer org reps, Telecom rep
- Mandate: Farmer onboarding, feedback collection, issue escalation

---

## 9. PERFORMANCE METRICS & SLAs

### 9.1 Platform SLAs (Production — Phase 2+)
| Metric | Target | Measurement | Remedy |
|--------|--------|-------------|--------|
| API Uptime | 99.9% | Monthly | Service credits: 2% monthly fee per 0.1% below |
| IVR Availability | 99.5% | Monthly | Service credits: 5% monthly fee per 0.1% below |
| Query Resolution Rate | >75% | Quarterly farmer survey | Root cause + retraining sprint |
| Farmer CSAT | >4.2/5.0 | Quarterly | Co-design + UX iteration |
| Model Accuracy (Ag QA) | >87% | Continuous eval | Monthly retraining |
| Voice Latency (P95) | <2s | Continuous | Infrastructure scaling |
| Dashboard Refresh | <1hr | Continuous | Pipeline optimization |

### 9.2 Impact KPIs (Reported Quarterly)
| KPI | Baseline | Year 1 Target | Year 3 Target |
|-----|----------|---------------|---------------|
| Active Farmer Users | 5,000 | 25,000 | 250,000 |
| Extension Officers Active | 0 | 500 | 2,000 |
| Queries per Farmer/Month | 2 | 15 | 30 |
| Women Farmer Reach | 30% | 45% | 50% |
| Crop Yield Improvement (RCT) | — | +8% | +20% |
| AIP Verification via IVR | 0 | 50,000 | 500,000 |
| Malawian Engineers Trained | 0 | 20 | 50 |

---

## 10. SECURITY & COMPLIANCE

### 10.1 Security Standards
- **Platform**: SOC 2 Type II (Year 1); ISO 27001 (Year 2)
- **Infrastructure**: Malawi Government Data Center (preferred) or certified local cloud
- **Encryption**: AES-256 at rest; TLS 1.3 in transit; HSM for key management
- **Access**: RBAC + MFA; Privileged access logging; Quarterly penetration test
- **Incident Response**: 1-hour detection; 4-hour containment; 24hr notification (per DPA)

### 10.2 Regulatory Compliance
- **MACRA**: IVR/USSD licensing; Telecom consumer protection
- **DPA 2024**: Data protection impact assessment; DPO appointment
- **World Bank Safeguards**: ESS10 (Stakeholder Engagement); Grievance redress mechanism
- **Export Controls**: Model weights not exported without Ministry approval

---

## 11. TERM & TERMINATION

| Provision | Term |
|-----------|------|
| **MoU Term** | 18 months (to MSA execution) |
| **MSA Target** | Signed by Month 12 |
| **MSA Initial Term** | 3 years + 2 × 1-year options |
| **Termination for Convenience (MoU)** | 30 days written notice |
| **Termination for Cause (MSA)** | 90-day cure period (material breach) |
| **Force Majeure** | 120 days → either party may terminate |
| **Insolvency / Regulatory Revocation** | Immediate |

### 11.1 Transition Obligations (MSA Expiry/Termination)
- **Data Return**: All Ministry data in open formats (Parquet, JSONL) within 60 days
- **Model Weights**: Government retains full rights; Light Speed provides export package
- **Platform Access**: 180-day wind-down; Source code escrow (trigger: insolvency)
- **Knowledge Transfer**: 40 hours documented handover; Runbooks; Trained staff retention
- **Capacity**: Trained Malawian engineers remain with Government/ecosystem

---

## 12. DISPUTE RESOLUTION

1. **Technical Working Group** (15 days) — Operational issues
2. **Steering Committee** (30 days) — Strategic/commercial issues
3. **Mediation** (Malawi Arbitration Centre, Lilongwe) — 60 days
4. **Arbitration** (Malawi Arbitration Act, 3 arbitrators, English law, Lilongwe seat) — Binding
5. **Sovereign Immunity**: Ministry does not waive sovereign immunity except for arbitration award enforcement

---

## 13. ANTI-CORRUPTION & INTEGRITY

- Both Parties comply with: Malawi Corrupt Practices Act, WB Anti-Corruption Guidelines, US FCPA
- **Zero Tolerance**: No bribes, kickbacks, improper advantages
- **Grievance Channel**: Anonymous reporting to WB Integrity Vice Presidency + Ministry Internal Audit
- **Audit Rights**: Ministry Auditor General + WB may audit any time

---

## 14. FORCE MAJEURE

Neither Party liable for delays due to: war, pandemic, natural disaster, government action, telecom infrastructure failure — **provided** written notice within 10 days; mitigation efforts documented.

---

## 15. SIGNATURES

| LIGHT SPEED HOLDINGS INC. | MINISTRY OF AGRICULTURE, REPUBLIC OF MALAWI |
|---------------------------|---------------------------------------------|
| Signature: _______________ | Signature: _______________ |
| Name: _______________ | Name: _______________ |
| Title: Chief Executive Officer | Title: Hon. Minister of Agriculture / Principal Secretary |
| Date: _______________ | Date: _______________ |
| | **Witness (World Bank):** _______________ |

---

## APPENDIX A: PILOT DISTRICTS & FARMER COHORT (PHASE 1)

| District | EPA | Target Farmers | Crops | Extension Officers |
|----------|-----|----------------|-------|-------------------|
| **Lilongwe** | Mitundu | 20 | Maize, Groundnut, Soy | 2 |
| **Kasungu** | Kasungu | 15 | Tobacco, Maize, Beans | 2 |
| **Mzimba** | Mzimba | 15 | Maize, Potato, Cassava | 1 |
| **Total** | | **50** | | **5** |

**Selection Criteria**: Gender balance (50% women); Age diversity (18-65); Literacy mix; Smartphone + feature phone users; AIP beneficiaries + non-beneficiaries

---

## APPENDIX B: MINISTRY DATA PROVISION SPECIFICATION

| Dataset | Format | Frequency | Access Method | Sensitivity |
|---------|--------|-----------|---------------|-------------|
| Crop Calendar | CSV/JSON | Annual | API / Secure FTP | Public |
| Pest/Disease Bulletins | PDF/JSON | Weekly | API | Public |
| Variety Registry | CSV | Quarterly | Secure FTP | Public |
| AIP Beneficiary List | CSV/Parquet | Seasonal | Secure API (auth) | **High (PII)** |
| Depot Stock Levels | JSON | Daily | API | Medium |
| Extension Officer Registry | CSV | Quarterly | Secure FTP | Medium |
| Soil/Climate Data | GeoTIFF/NetCDF | Static | Secure FTP | Public |

---

*End of MoU — Subject to Legal Review, Ministerial Approval, and World Bank Concurrence*
