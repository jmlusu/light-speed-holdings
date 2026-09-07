# Last Mile Health (Malawi) — Decision-Maker Map & Entry Point Analysis

**Prepared:** 2026-09-06  
**Sources:** Last Mile Health website, LinkedIn, USAID/Global Fund grant databases, Malawi Ministry of Finance documents, digital health conference programs, mHub ecosystem data, public financial reports

---

## 1. Organizational Chart — Key Decision-Makers (Malawi Office)

| Role | Name | Title | LinkedIn | Email / Contact | Notes |
|------|------|-------|----------|-----------------|-------|
| **Country Director** | **Dalitso Baloyi** | Country Director, Malawi (Sep 2021–present) | [linkedin.com/in/dalitso-baloyi-1562474a](https://www.linkedin.com/in/dalitso-baloyi-1562474a) | — | Overall P&L, MoH relationship, donor engagement, strategy. Quoted in iCHIS launch communications. |
| **Deputy Country Director** | **Susan Wallani** | Deputy Country Director (Apr 2026–present) | [linkedin.com/in/susan-wallani-78036378](https://www.linkedin.com/in/susan-wallani-78036378) | — | Oversees programs, operations, MERL integration, business development. Reports to Country Director. |
| **Director, Digital Health** | **Tasokwa B. Kalua Nkhonjera** | Director, Community Health System Strengthening (prev. Director Digital Health Jul 2023–Sep 2024; Senior Manager Digital Health prior) | [linkedin.com/in/tasokwa-b-kalua-nkhonjera-022a6b2a](https://www.linkedin.com/in/tasokwa-b-kalua-nkhonjera-022a6b2a) | tnkhonjera@lastmilehealth.org (per iCHIS case study) | iCHIS Product Manager (seconded to MoH Digital Health Division). Leads digital health strategy, grant management, partner mobilization. |
| **Senior Manager, Digital Health** | **Kidest Lulu Hagos** | Senior Manager, Digital Health (Malawi) | — | khagos@lastmilehealth.org (per iCHIS case study) | Co-leads iCHIS implementation with Tasokwa; manages training, deployment, district coordination. |
| **Digital Health Specialist** | **Daniel Chaweza** | Digital Health Specialist (Jul 2023–present) | [linkedin.com/in/daniel-chaweza-8aa38118a](https://www.linkedin.com/in/daniel-chaweza-8aa38118a) | — | End-to-end iCHIS design, development, deployment, CHW upskilling. Software engineer / data scientist background. |
| **MERL Specialist** | *(Vacant / recruiting as of 2026)* | MERL Specialist (reports to Director of Programs) | — | — | Job posted on NGO Jobs Africa (2026): leads MERL plan, data quality, evaluation design, donor reporting. |
| **Senior Coordinator, MERL** | *(Recruiting)* | Senior Coordinator, MERL (24-mo fixed term) | — | — | Supports MERL Specialist: data analysis, research protocols, DHIS2/ODK/KoboToolbox, visualizations. Band MWI-2 ($23–32k). |
| **Senior Technical Coordinator (HSS)** | **Mathias Mathews Mndala** | Senior Technical Coordinator (Feb 2023–present) | [linkedin.com/in/mathias-mathews-mndala-9934a788](https://www.linkedin.com/in/mathias-mathews-mndala-9934a788) | — | BIRCH project oversight, IMCI coordination, budgeting, MoH liaison. Operations background. |
| **Senior Operations Manager** | **Charity Solomon** | Senior Operations Manager (Malawi) | [linkedin.com/in/charity-solomon-a79b27200](https://www.linkedin.com/in/charity-solomon-a79b27200) | — | Procurement, vendor management, duty exemptions, compliance, budgeting, NetSuite. Key for vendor onboarding. |
| **Advisor, Health Financing** | *(Recruiting)* | Advisor, Health Financing (embedded in MoH DPPD) | — | — | Band MWI-3 ($28–44k). Costed operational plans, resource mapping, Global Fund/USAID/Gavi funding cycles, private sector engagement. |
| **Finance & Ops Consultant (ACHIEVE)** | *(Recruiting)* | Finance and Operations Consultant — ACHIEVE Project | — | — | Disbursements, donor financial reporting, procurement (purchase requests, bid evaluations, contracts), NetSuite, GAAP, Malawi Finance Regulations. |

**Global / Cross-Cutting Leads (relevant to Malawi):**
- **Paul C. K.** — Senior Manager, Global Digital Health (oversees multi-country digital health, standardizes MEL, manages budgets, represents LMH at GDHF). [LinkedIn](https://www.linkedin.com/in/dr-paul-c-k-13418171)
- **Victoria Munthali Chiumia** — Manager, Community Health, Partnerships & Quality (Malawi). Author of FY26 six-month report; leads financing advocacy.

---

## 2. Current Reporting Pain Points (USAID, Global Fund, Other Donors)

| Pain Point | Evidence | Donor / Context |
|------------|----------|-----------------|
| **Paper-based reporting burden** | CHWs spend ~10 hrs/month aggregating paper reports; reports often lost, don't reach decision-makers, incomplete picture of community health challenges. | USAID (ICH), Global Fund, MoH |
| **Data gaps & misplaced reports** | "Patient records and supply needs reported by frontline health workers won't get lost due to misplaced paperwork" — iCHIS rationale. | Global Fund (BIRCH), USAID |
| **Duplicate data entry across systems** | Multiple digital health systems (DHIS2, eHIN, iCHIS, CommCare, OpenSRP, cStock) lack interoperability → siloed data, duplicate entry, unrealized investment benefits. | GIZ, Gates Foundation, GAVI, Global Fund, USAID, UNICEF |
| **Donor-specific reporting fragmentation** | 9+ external donors each with separate budgets, priorities, decision processes (FY 2017/18 RM Round 5). MoH Resource Mapping (RM) exercise created to harmonize. | All bilateral/multilateral donors |
| **Misaligned fiscal years** | Most donors use different fiscal years from GoM (Jul–Jun); RM allows donor FY but aligns to GoM FY assuming even distribution — may not reflect actual projections. | USAID (Oct–Sep), Global Fund (Jan–Dec), Gates, GAVI, etc. |
| **Inadequate M&E capacity at MoH** | HDC partners (GIZ, Data4Health, Gates, USAID, CDC) seconded staff to MoH HIS unit; still insufficient for forthcoming M&E/HIS Strategy. | USAID, CDC, Gates, GIZ, Global Fund |
| **Data quality assurance gaps** | LMH partnering with Central M&E Division to develop comprehensive iCHIS data quality assurance process (as of 2025). | Global Fund, USAID |
| **Reporting not linked to budget execution** | Budget evaluation results don't inform next budget; HIV epi model hasn't influenced funding levels; programme-based budgeting has indicator/funding mismatch. | MoF, Global Fund, PEPFAR, GAVI |
| **Limited district-level partner budget visibility** | District Health Offices validate national RM estimates with district-level census of partner commitments; partners rarely contribute to unified district planning templates. | All implementing partners |

---

## 3. Existing Technology Stack

| System / Tool | Purpose | Owner / Lead | Status | Integration Notes |
|---------------|---------|--------------|--------|-------------------|
| **iCHIS (integrated Community Health Information System)** | Point-of-care CHW application: registers, disease mgmt, immunization, child case mgmt, supervision, reporting, surveillance, supply chain. Built on **DHIS2 Tracker** (Android app). | MoH (owner) — Univ. Malawi Chancellor College (technical lead) — LMH (product manager) | Deployed in 14 districts (Mar 2025); 1,416 CHWs trained in LMH-led districts; 11 modules developed. | Syncs with DHIS2 central server when online. Interoperability focus: HL7 FHIR, DHIS2 data model, OpenHIE profiles. |
| **DHIS2 (District Health Information Software 2)** | National HMIS platform; aggregate & individual-level data, mobile/offline collection via Android app. Core dev by HISP (Univ. Oslo). | MoH CMED / Digital Health Division | National scale; reconfigured with programme-specific dashboards (primary healthcare, UHC, core indicators). | iCHIS feeds into DHIS2. MaHIS (Malawi Health Information System) conceptualized as integrated national HIS. |
| **MaHIS (Malawi Healthcare Information System)** | National integrated HIS vision; eRegister (lightweight EMR) in Ntcheu district extended to 3 facilities. | MoH Digital Health Division / GIZ / m4h / Compelling Works | Conceptualized; eRegister launched in Ntcheu. | **Key integration target:** iCHIS ↔ MaHIS roadmap under ACHIEVE project (API/middleware: OpenHIM, Mirth Connect, custom API layer). |
| **eHIN (Electronic Health Information Network)** | Mobile commodity tracking: medicines from central warehouse to end-user, stock levels, resupply needs. | MoH / UNDP / Norad / Gov. Japan / SDG-AF | 5,000 health workers trained across 2,000 service points; target 8,500 points. | Separate from iCHIS/DHIS2; supply chain focus. |
| **CommCare** | Used by some implementing partners (e.g., D-tree, Partners In Health) for community-level case management. | Various IPs | Sub-national scale. | Listed in Health Data Ecosystem Mapping as sub-national system; interoperability gap noted. |
| **OpenMRS / OpenSRP / ODK / KoboToolbox** | Facility EMR (OpenMRS), community registers (OpenSRP), survey/data collection (ODK/Kobo). | Various (MoH, IPs, researchers) | Sub-national / project-specific. | DHIS2 interoperability via OpenHIE profiles; MERL job reqs cite ODK/Kobo & DHIS2 proficiency. |
| **NetSuite** | Financial management (LMH global). | LMH Finance | In use. | Finance consultant role requires NetSuite experience. |
| **m-mama** | Maternal emergency transport system (digital dispatch). | LMH / MoH / partners | Pilot/scale phase in Balaka, others. | Sustainable financing model development under ACHIEVE Objective 3. |

**Interoperability Architecture (per ACHIEVE consultant ToR):**
- Point-to-point API integration
- Interface engine / middleware: **OpenHIM, Mirth Connect, custom API layer**
- File-based exchange (CSV, XML, JSON) as fallback
- Data standards: **HL7 FHIR, DHIS2 data model, OpenHIE profiles**
- Auth: tokens, OAuth, API keys, RBAC
- Encryption: in-transit & at-rest
- Compliance: Malawi Data Protection Act, donor requirements (USAID, Global Fund, Gavi, World Bank)

---

## 4. Procurement Process for Vendors

| Step | Description | Authority / Owner | Notes |
|------|-------------|-------------------|-------|
| **1. Purchase Request (PR)** | Initiated by program/ops team; specifies need, specs, qty, budget code. | Program Lead / Senior Operations Manager | Charity Solomon (Sr Ops Mgr) oversees PR process. |
| **2. Bid Solicitation / Tender** | For goods/services above threshold: RFQ (3+ quotes) or RFP/tender. LMH follows **Malawi Finance Regulations**, **US Federal regulations** (for USG-funded), **LMH Finance Policy**, **GAAP**. | Senior Finance Manager + Operations | ACHIEVE consultant ToR: "Support preparation of purchase requests, bid evaluations, and contracts." |
| **3. Bid Evaluation** | Technical + financial evaluation committee; conflict-of-interest declarations. | Evaluation Committee (tech + finance + ops) | Duty exemptions secured on ~90% of imports (Charity Solomon achievement). |
| **4. Contract Award** | Approved per LMH approval matrix/thresholds. Deputy Country Director is authorized co-signatory in Malawi. | Country Director / Deputy Country Director | Thresholds defined in LMH approval matrix. |
| **5. Contract Management & Payment** | Milestone-based payments; advance accounts liquidated timely. NetSuite for PO/Invoice matching. | Finance & Operations Consultant / Senior Finance Manager | Donor compliance: USAID, Global Fund, Gavi, World Bank reporting standards. |
| **6. Asset Management** | Tablets/hardware for iCHIS: procurement, deployment, tracking, maintenance. | Senior Coordinator, Digital Health (facilitates procurement of iCHIS tablets/accessories) | Asset management part of iCHIS deployment SOPs. |

**Key Procurement Contacts:**
- **Charity Solomon**, Senior Operations Manager — procurement strategy, vendor mgmt, duty exemptions
- **Senior Finance Manager** (Malawi) — financial compliance, donor reporting
- **Finance & Operations Consultant (ACHIEVE)** — project-level procurement execution
- **Deputy Country Director (Susan Wallani)** — co-signatory, approval authority

**Vendor Registration:** New vendors require due diligence (tax compliance, banking, capacity). LMH registered as INGO in Malawi (Charity Solomon led registration in 3 months).

---

## 5. Existing Relationships & Warm Introduction Paths

| Path | Contact / Organization | Relationship Strength | How to Leverage |
|------|------------------------|---------------------|-----------------|
| **MoH Digital Health Division** | **Kennedy Kanyimbo**, Chief Digital Health Officer (kennedykanyimbo@gmail.com) | **Direct** — LMH seconded staff (Tasokwa, Lulu) sit in DHD; co-lead iCHIS. | Request intro via Tasokwa Nkhonjera (tnkhonjera@lastmilehealth.org). |
| **MoH Community Health Services Section (CHSS)** | **Doreen Namagetsi Ali**, Deputy Director Preventive Health Services – Community Health | **Strong** — BIRCH project collaboration; quoted on BIRCH impact. | LMH BIRCH team (Mathias Mndala, Program Consultant) works daily with CHSS. |
| **MoH Central M&E Division (CMED)** | **Samuel Gama**, Primary Healthcare Officer M&E (sgamah@gmail.com) | **Strong** — iCHIS data custodian; LMH partners on data review sessions (9 sessions, 120+ leaders). | Lulu Hagos (khagos@lastmilehealth.org) coordinates. |
| **University of Malawi (Chancellor College)** | Computer Science Dept — technical lead for iCHIS development | **Institutional** — MoU with MoH; LMH product manager role. | Daniel Chaweza (Digital Health Specialist) works closely with UNIMA dev team. |
| **Global Fund (Geneva & Country Team)** | BIRCH project: LMH is **lead implementer** across 11 countries ($7M TA stream). | **Deep** — LMH manages BIRCH funding; Malawi is direct implementation country. | Paul C. K. (Global Digital Health) & Tasokwa engage GF at global/regional level. |
| **USAID Malawi** | ACHIEVE project (Pact prime, LMH sub); ONSE Health Activity (historical). | **Active** — ACHIEVE: $3-4k/mo consultant role; LMH leads iCHIS integration in Balaka. | Digital Health Consultant reports to Daniel Chaweza; coordinates with MoH DHD. |
| **GIZ / Malawi German Health Programme** | MaHIS / eRegister consortium (m4h, Compelling Works, Cooper Smith). | **Collaborative** — LMH partner in iCHIS ecosystem; shared MoH Digital Health Division. | Tasokwa / Lulu attend Digital Health TWGs with GIZ. |
| **UNICEF Malawi** | iCHIS partner (tablets, training); eHIN supporter. | **Operational** — Joint deployment in districts. | LMH engages UNICEF at district & national coordination meetings. |
| **mHub (Lilongwe)** | Malawi's first tech/innovation hub; 30-40 staff; Digital Malawi project implementer. | **Ecosystem** — No direct LMH partnership found, but shared MoH Digital Health Division stakeholders. | mHub CEO Elijah Mkandawire; could facilitate local dev talent, hackathons, user testing. |
| **Africa Frontline First / Community Health Impact Coalition** | LMH co-founded CHIC; AFF Catalytic Fund (~$100M) hosted by Global Fund. | **Strategic** — LMH CEO Lisha McCormick on board; Malawi eligible for AFF funds. | Victoria Munthali Chiumia leads financing advocacy; connects to AFF. |
| **Tony Blair Institute (TBI)** | Supported Malawi National Digital Health Governance Framework (2025-2030). | **MoH-aligned** — Works with MoH Quality Management Directorate / Digital Health Division. | Intro via MoH DHD (Kennedy Kanyimbo) or GIZ. |
| **Bill & Melinda Gates Foundation** | Kuunika Project (DHIS2 support); co-funder of ICH Partnership (Frontline Health Project). | **Funder** — Historical grant to LMH (2017, $1.75M for evidence collection). | Paul C. K. presents at GDHF (Gates-funded); LMH has ongoing GF engagement. |

**Optimal Warm Introduction Sequence:**
1. **Tasokwa Nkhonjera** (tnkhonjera@lastmilehealth.org) → **Kennedy Kanyimbo** (MoH DHD) & **Doreen Ali** (MoH CHSS)
2. **Daniel Chaweza** → **Univ. Malawi CS Dept** (iCHIS dev team) & **ACHIEVE project tech leads**
3. **Charity Solomon** → **Procurement / vendor onboarding** (if selling hardware/software/services)
4. **Victoria Munthali Chiumia** → **Health Financing / Global Fund / AFF** strategy
5. **Paul C. K.** → **Global digital health strategy, cross-country scaling, donor forums (GDHF)**

---

## 6. Budget Cycle Timing

### Malawi Government Fiscal Year
- **FY = July 1 – June 30** (confirmed by Ministry of Finance, International Budget Partnership)
- **Budget formulation:** Starts ~January (pre-budget consultations); Executive Budget Proposal submitted to Parliament by **May** (ideally 2+ months before FY start)
- **Budget enactment:** Parliament debates/approves **by June 30** (ideally before Jul 1)
- **Mid-Year Budget Review:** ~January (FY2025-26 Mid-Year Budget referenced in 2026-27 Budget Policy Statement)
- **Resource Mapping (RM) Exercise:** Annual; Round 7 in progress (2023). Data collection ~May–Apr; preliminary report ~April; feeds into national budgeting.

### Donor Fiscal Years (misaligned with GoM)
| Donor | Fiscal Year | Implication for LMH Malawi |
|-------|-------------|----------------------------|
| **Government of Malawi** | Jul 1 – Jun 30 | Primary planning cycle; RM aligns to this. |
| **USAID** | Oct 1 – Sep 30 | ACHIEVE, ONSE, PEPFAR funds follow USG FY. Reporting quarters: Oct-Dec, Jan-Mar, Apr-Jun, Jul-Sep. |
| **Global Fund** | Jan 1 – Dec 31 | BIRCH (2023), GC7 (2024-2026), CS&R matching fund. Grant-making aligns to calendar year. |
| **Gavi** | Jan 1 – Dec 31 | HSS/immunization funding; co-financing obligations tracked in RM. |
| **Gates Foundation** | Calendar year | Grant cycles vary; Kuunika (DHIS2) was multi-year. |
| **GIZ / BMZ** | Calendar year | MGHP (Malawi German Health Programme) funds MaHIS/eRegister. |
| **World Bank** | Jul 1 – Jun 30 (IDA) | Health financing strategy support; DPPD embedded advisor. |

### LMH Internal Planning Cycle
- **Annual Work Plans:** Developed with MoH aligned to GoM FY (Jul–Jun). Deputy Country Director oversees "design of annual work plans that align with strategic objectives, overall resources available, and detailed budgets."
- **BIRCH Project (Global Fund TA):** Jan–Dec 2023 (Year 1); BIRCH 2.0 2024+ (Health Financing Consultant 4-6 mo).
- **ACHIEVE Project (US Dept of State / Pact):** Consultant mid-Aug 2026 – Sep 30, 2026 (short-term).
- **Quarterly Reporting:** LMH produces quarterly reports (e.g., FY23 Q2, FY26 Six-Month Jan). Aligns to donor requirements.

### Key Budget Milestones for Engagement
| Month | Activity | Relevance to Vendor/Partner Engagement |
|-------|----------|----------------------------------------|
| **Jan–Mar** | RM data collection; MoH pre-budget consultations; Global Fund grant-making (TRP review) | Position solutions for RM inclusion; respond to GF TRP queries via LMH BIRCH team. |
| **Apr–May** | Executive Budget Proposal finalized; submitted to Parliament | Advocate for iCHIS/MaHIS integration line items in MoH budget. |
| **Jun** | Budget enactment; GoM FY ends | Confirm approved allocations for digital health, CHW support. |
| **Jul** | **GoM FY starts** — new budgets active | **Best time to initiate procurement** for FY-aligned contracts. |
| **Jul–Sep** | USAID FY ends Sep 30; new awards often start Oct 1 | ACHIEVE/ONSE follow-on proposals; align to USAID FY. |
| **Oct–Dec** | Global Fund calendar year planning; concept notes for next cycle | Engage BIRCH/Health Financing team for GC8 / AFF Catalytic Fund positioning. |
| **Jan** | Mid-Year Budget Review; RM Round kickoff | Course-correct; insert new priorities / vendor solutions. |

---

## 7. Optimal Entry Point — Recommendation

### Primary Entry Point: **Tasokwa Nkhonjera (Director, Digital Health / iCHIS Product Manager)**
- **Why:** Holds dual role — LMH Digital Health lead + MoH DHD seconded Product Manager for iCHIS. Controls iCHIS roadmap, partner engagement, resource mobilization, grant management (Global Fund BIRCH, USAID ACHIEVE). Direct line to MoH Digital Health Division (Kennedy Kanyimbo) and CHSS (Doreen Ali).
- **Approach:** Email intro referencing iCHIS-MaHIS integration roadmap (ACHEIVE Strategic Objective 1), DHIS2/FHIR interoperability, or CHW digital literacy/training gaps. CC Daniel Chaweza (technical lead) and Lulu Hagos (deployment lead).

### Secondary Entry Points (by objective):
| Objective | Best Contact | Rationale |
|-----------|--------------|-----------|
| **Sell hardware/tablets for iCHIS** | Charity Solomon (Sr Ops Mgr) + Senior Coordinator Digital Health | Procurement authority; manages iCHIS tablet procurement, duty exemptions. |
| **Propose MERL / data quality tools** | MERL Specialist (when hired) / Victoria Munthali Chiumia | MERL owns data quality assurance process; Victoria oversees financing advocacy & reporting. |
| **Health financing / costing models** | Advisor Health Financing (when hired) / Mathias Mndala (BIRCH) | Embedded in MoH DPPD; develops costed operational plans, resource mapping. |
| **MaHIS-iCHIS integration middleware** | Daniel Chaweza (Digital Health Specialist) + ACHIEVE Consultant (mid-Aug 2026) | Directly managing the integration roadmap consultancy (OpenHIM/Mirth/FHIR). |
| **Global Fund / AFF Catalytic Fund positioning** | Paul C. K. (Global Digital Health) / Victoria Munthali Chiumia | Global strategy, cross-country learning, donor forum access (GDHF, WHA). |
| **Local dev capacity / hackathons / user testing** | mHub (Elijah Mkandawire) via Tasokwa intro | Malawi tech ecosystem; digital literacy training for CHWs; potential co-creation. |

### Timing Recommendation
**Engage now (Sep 2026)** to align with:
- **GoM FY 2026-27** (started Jul 2026) — budgets active, procurement windows open
- **ACHEIVE consultant engagement** (mid-Aug – Sep 30, 2026) — integration roadmap being defined
- **Global Fund GC7 / BIRCH 2.0** implementation — financing streams flowing
- **Pre-GC8 / AFF Catalytic Fund** concept development (2027+)

---

## 8. Key Citations (Source Map)

| # | Source | Key Claims |
|---|--------|------------|
| 1 | Last Mile Health Malawi page (2024-07-08) | Country program overview, iCHIS partnership with MoH since 2019 |
| 2 | iCHIS Case Study PDF (2024-10) | iCHIS architecture, partners, deployment stats (14 districts, 1,416 CHWs), contacts (Tasokwa, Lulu, Samuel Gama, Kennedy Kanyimbo) |
| 3 | "Strengthening community health systems through technology: Malawi launches iCHIS" (2022-12-05) | Paper-based pain points (10 hrs/mo reporting), CHW quotes, Dalitso Baloyi quote |
| 4 | "Going Digital at the Last Mile in Malawi" (2021-08-18) | Presidential endorsement, paper-based challenges (drug stockouts, lost reports) |
| 5 | "Stronger systems, better care: Training Malawi's CHWs in iCHIS" (2023-10-26) | 1,740 CHWs trained across 9 districts (14.5% of workforce), Robson Kayira quote |
| 6 | "How strong financing is driving resilience..." (2026-02-09) | Global Fund BIRCH, costed operational plan, resource mapping, $240M funding gap |
| 7 | "Strong financing for strong community health: LMH serves as lead implementer of Global Fund's Project BIRCH" (2023-10-20) | BIRCH $7M TA stream, 11 countries, LMH lead implementer, Africa Frontline First Catalytic Fund $100M |
| 8 | ACHIEVE Digital Health Consultant ToR (2026) | MaHIS-iCHIS integration roadmap, OpenHIM/Mirth/FHIR, donor budgeting (Gavi, GF, USAID, WB), reporting to Daniel Chaweza |
| 9 | BIRCH Program Consultant / Health Financing Consultant ToRs (2023, 2026) | Global Fund financing cycles, costed operational plans, resource mapping, MoH DPPD embedding |
| 10 | Finance & Operations Consultant (ACHIEVE) ToR | Procurement process (PR, bid eval, contracts), NetSuite, GAAP, Malawi Finance Regs, donor compliance |
| 11 | Deputy Country Director job posting (2026-01) | Role scope: programs, ops, MERL, business dev, co-signatory authority, Band MWI-4 ($70-89k) |
| 12 | MERL Specialist / Senior Coordinator MERL job postings (2026) | MERL structure, DHIS2/ODK/Kobo requirements, donor reporting, Band MWI-2/3 |
| 13 | Charity Solomon LinkedIn | Procurement leadership, duty exemptions (90% imports), ING registration, NetSuite |
| 14 | Dalitso Baloyi LinkedIn | Country Director since Sep 2021, GDHF participation |
| 15 | Tasokwa Nkhonjera LinkedIn | Digital Health Director (Jul 2023–Sep 2024), Senior Manager prior, iCHIS Product Manager secondment, grant mgmt |
| 16 | Daniel Chaweza LinkedIn | Digital Health Specialist Jul 2023–present, iCHIS end-to-end, software engineer/data scientist |
| 17 | Susan Wallani LinkedIn | Deputy Country Director Apr 2026–present, USAID/Global Fund/GIZ experience |
| 18 | Mathias Mndala LinkedIn | Senior Technical Coordinator Feb 2023–present, IMCI, budgeting, proposal writing |
| 19 | Malawi Health Data Ecosystem Mapping (BMZ/GIZ, 2024) | DHIS2, iCHIS, eHIN, CommCare, OpenSRP, cStock landscape; donors (Gates, Gavi, GF, NORAD, UNICEF, USAID); interoperability gaps |
| 20 | Malawi National Digital Health Governance Framework 2025-2030 (TBI/World Bank) | Governance framework, Digital Health Division leadership, stakeholder coordination |
| 21 | Malawi FY budget docs (MoF 2026-27) | FY Jul-Jun, K1.02T health allocation, US$744M USG financing, program-based budgeting |
| 22 | Health Sector Resource Mapping in Malawi (GFF 2023) | RM process (7 rounds), 177 orgs/yr, US$15B tracked, district validation, donor FY misalignment |
| 23 | National Health Financing Strategy 2023-2030 | "One plan, one budget, one M&E framework", MTEF not used in budget design, budget evaluation gaps |
| 24 | mHub LinkedIn / website | Malawi's first tech hub, 30-40 staff, Digital Malawi implementer, Lilongwe-based |
| 25 | Gates Foundation grant database | LMH grant 2017: $1.75M for evidence collection (USAID/UNICEF ICH Partnership) |
| 26 | LMH FY26 Six-Month Report (Jan 2026) | 3,159 CHWs trained on iCHIS since 2021, 45% active data entry, $240M funding unlocked via AFF |

---

## 9. Quick-Reference Contact Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAST MILE HEALTH MALAWI — DECISION-MAKER QUICK REFERENCE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ COUNTRY DIRECTOR          │ Dalitso Baloyi          │ LinkedIn (search)     │
│ DEPUTY COUNTRY DIRECTOR   │ Susan Wallani           │ LinkedIn (search)     │
│ DIGITAL HEALTH LEAD       │ Tasokwa Nkhonjera       │ tnkhonjera@lastmile.. │
│ DIGITAL HEALTH SR MGR     │ Kidest Lulu Hagos       │ khagos@lastmilehealth.│
│ DIGITAL HEALTH SPECIALIST │ Daniel Chaweza          │ LinkedIn (search)     │
│ SR OPS / PROCUREMENT      │ Charity Solomon         │ LinkedIn (search)     │
│ BIRCH / HSS TECH LEAD     │ Mathias Mndala          │ LinkedIn (search)     │
│ FINANCING ADVISOR (MoH)   │ [Recruiting - Band MWI-3]│ Via Victoria Chiumia  │
│ MERL LEAD                 │ [Recruiting - Band MWI-2]│ Via Dir. of Programs  │
│ GLOBAL DIGITAL HEALTH     │ Paul C. K.              │ LinkedIn (search)     │
│ PARTNERSHIPS & QUALITY    │ Victoria Munthali Chiumia│ LMH Malawi reports    │
├─────────────────────────────────────────────────────────────────────────────┤
│ MoH DIGITAL HEALTH DIR    │ Kennedy Kanyimbo        │ kennedykanyimbo@...   │
│ MoH CHSS DEPUTY DIR       │ Doreen Namagetsi Ali    │ (via LMH BIRCH team)  │
│ MoH CMED M&E OFFICER      │ Samuel Gama             │ sgamah@gmail.com      │
│ UNIV MALAWI CS DEPT       │ iCHIS Technical Lead    │ (via Daniel Chaweza)  │
│ GLOBAL FUND BIRCH         │ LMH = Lead Implementer  │ Paul C. K. / Tasokwa  │
│ USAID ACHIEVE PRIME       │ Pact                    │ LMH = Balaka sub      │
│ TECH HUB ECOSYSTEM        │ mHub (Elijah Mkandawire)│ Lilongwe              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*End of Report*