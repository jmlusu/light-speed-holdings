# Service Delivery SOP — Offer C: Data & Reporting Services

**Document ID:** SOP-SVC-C-001
**Department:** Data
**Owner:** cdo
**Classification:** Internal — RESTRICTED (donor data handling)
**Last Updated:** 2026-08-12
**Offer Code:** C — Data & Reporting (surveys, dashboards, donor reporting)

---

## 1. Purpose

Defines the delivery process for Offer C client engagements: data cleaning & analysis,
donor/project reports, interactive dashboards, and survey design + analysis. This is the
**differentiator** offer — NGOs pay in USD and the sector runs on reporting. Due to donor
data sensitivity and professional liability, this offer requires the highest governance
gates.

> **BLOCKED STATUS:** Offer C is currently BLOCKED per `config/company/malawi_offers.yaml`.
> Client onboarding requires board-ratified liability cap (see client-onboarding-policy.md §3).

## 2. Scope

Applies to all client engagements tagged `offer-c` in `.opencode/inbox.json`.

## 3. Roles & Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Engagement Lead | human_ceo | Final deliverable approval, liability sign-off |
| Data Strategy | cdo | Overall data handling, compliance |
| Data Engineering | data_engineer | Pipeline construction, ETL, validation |
| BI Engineering | business_intelligence_engineer | Dashboard design, visualization |
| Data Science | data_scientist | Analysis, modeling, insights |
| Survey Research | survey_researcher | Survey design, sampling, field collection |
| Data Protection | data_privacy_officer | GDPR/Act 2017 compliance, retention |
| Ethics Review | ai_ethics_board_chair | Accuracy review of donor reports (Tier 3+) |
| Security | ciso | Data isolation, encryption-at-rest |
| QA | qa_lead | Data accuracy verification, dashboard testing |

## 4. Delivery Pipeline

```
1. Client Brief → 2. Data Assessment → 3. Consent & DPA → 4. Ethics Review →
   5. Intake Task → 6. Build → 7. Accuracy Review → 8. QA → 9. Deliver
```

### Step-by-step

1. **Client Brief** — `client` CLI sub-app creates client record + SOW.
2. **Data Assessment** — `data_privacy_officer` classifies all data as PII/Non-PII/sensitive.
   `survey_researcher` assesses survey methodology requirements.
3. **Consent & DPA** — Client signs GDPR/donor addendum. Cross-border LLM transfer consent
   obtained for any analysis routed to external providers.
4. **Ethics Review** — `ai_ethics_board_chair` reviews the proposed deliverable type.
   All donor reports and dashboards are Tier 3+ → require board-level Ethics Review before delivery.
5. **Intake Task** — `human_ceo` creates inbox.json task tagged `offer-c`, `client-<id>`,
   `data_level=<classified>`, `risk_level=critical`, `requires_approval=True`.
6. **Build** — `data_engineer` constructs pipelines; `business_intelligence_engineer` builds
   dashboards; `data_scientist` performs analysis; `survey_researcher` manages field collection.
7. **Accuracy Review** — `human_ceo` + `qa_lead` verify all figures against source data.
   For donor reports: `ai_ethics_board_chair` confirms no hallucinated figures.
8. **QA** — `qa_lead` runs: data accuracy checks, dashboard responsiveness, report formatting.
9. **Deliver** — Client receives dashboard credentials + report package + 30-day support.
   `data_privacy_officer` schedules deletion of raw data after 30 days.

## 5. Pricing & Payment

| Deliverable | Price |
|-------------|-------|
| C1 — Data Cleaning & Analysis | $400 |
| C2 — Donor/Project Reports | $550 |
| C3 — Interactive Dashboard | $1,100 |
| C4 — Survey Design + Analysis | $720 |

**Payment (NGO clients):** 50% upfront via bank transfer (USD), 50% on delivery. Net 30 terms accepted for established NGOs. 1.5%/month late fee.

## 6. Professional Accuracy Standard

This is the key differentiator. Consulting firms charge $50K+ for NGO reporting. We undercut
10x by delivering through AI agents — but we must match their accuracy.

- All numbers in reports must be traceable to source data. `data_engineer` logs lineage.
- No LLM-generated figures without human verification. `human_ceo` signs off.
- `qa_lead` runs automated reconciliation: sum checks, null checks, outlier detection.
- `ai_ethics_board_chair` reviews reports that inform donor funding decisions.

## 7. Blocking Conditions (Must Clear Before Activation)

- [ ] client_onboarding_offer_c approval matrix entry passes
- [ ] service_level_liability_cap.status = "ratified" in malawi_offers.yaml
- [ ] Ethics Review of Agent Output policy covers professional accuracy
- [ ] Donor data handling approval matrix entry passes
- [ ] Client Onboarding Policy G1–G4 gates pass

## 8. Post-Delivery

- 30-day support window + data correction window (free corrections within 30 days).
- `data_privacy_officer` enforces raw data deletion after 30 days (unless extended retention signed).
- `support_agent` logs feedback; `data_scientist` archives anonymized insights to semantic memory.
- Postmortem: `cdo` reviews data quality; `human_ceo` validates client satisfaction.
