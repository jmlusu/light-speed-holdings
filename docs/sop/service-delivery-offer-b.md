# Service Delivery SOP — Offer B: Business Process Automation / Chatbots

**Document ID:** SOP-SVC-B-001
**Department:** Sales / Technology (shared)
**Owner:** solutions_engineer
**Classification:** Internal — RESTRICTED (client data handling)
**Last Updated:** 2026-08-12
**Offer Code:** B — Business Process Automation (WhatsApp chatbots, AI document generation)

---

## 1. Purpose

Defines the delivery process for Offer B client engagements: WhatsApp customer service
chatbots, AI document/report generators, form/survey automation, and custom internal
dashboards. Due to client data handling requirements, this offer requires enhanced
governance gates.

> **BLOCKED STATUS:** Offer B is currently BLOCKED per `config/company/malawi_offers.yaml`.
> Client onboarding requires board-ratified governance policies (see client-onboarding-policy.md §3).

## 2. Scope

Applies to all client engagements tagged `offer-b` in `.opencode/inbox.json`.

## 3. Roles & Agent Assignment

| Role | Agent | Responsibility |
|------|-------|----------------|
| Engagement Lead | human_ceo | Final approval, data handling sign-off |
| Solution Design | solutions_engineer | Architecture, WhatsApp API setup |
| Conversation Design | conversation_designer | Bot flows, NLU training data |
| Backend Integration | backend_engineer | API endpoints, database |
| Integration | integration_engineer | WhatsApp Business API, CRM, payment gateways |
| Support | support_agent | Client training, handoff, 30-day support |
| Data Protection | data_privacy_officer | Data handling protocol enforcement |
| Security Review | ciso | WhatsApp API security, data isolation |

## 4. Delivery Pipeline

```
1. Client Brief → 2. Data Assessment → 3. Consent & DPA → 4. Intake Task → 5. Build
   → 6. Review → 7. QA → 8. Deliver → 9. Handoff
```

### Step-by-step

1. **Client Brief** — `client` CLI sub-app creates client record + SOW.
2. **Data Assessment** — `data_privacy_officer` classifies data sensitivity (PII/Non-PII).
   `ciso` reviews WhatsApp API security requirements.
3. **Consent & DPA** — Client signs GDPR/donor addendum. Cross-border LLM transfer consent obtained.
4. **Intake Task** — `human_ceo` creates inbox.json task tagged `offer-b`, `client-<id>`,
   `data_level=<classified>`, `requires_approval=True`.
5. **Build** — `integration_engineer` sets up WhatsApp Business API; `conversation_designer`
   designs flows; `backend_engineer` builds webhook endpoints.
6. **Review** — `human_ceo` reviews bot flows + security posture.
7. **QA** — `qa_engineer` tests: WhatsApp message flow, handoff trigger, analytics dashboard,
   data isolation between clients.
8. **Deliver** — Client receives bot credentials + training docs + 30-day support window.
9. **Handoff** — `support_agent` provides client training. `data_privacy_officer` schedules
   30-day data deletion unless extended retention signed.

## 5. Pricing & Payment

| Deliverable | Client Type | Price |
|-------------|-------------|-------|
| B1 — WhatsApp Chatbot | SME (MWK) | MWK 1,500,000 setup + MWK 100,000/mo |
| B1 — WhatsApp Chatbot | NGO (USD) | $850 setup + $100/mo |
| B2 — AI Document Generator | SME | MWK 1,200,000 |
| B3 — Form/Survey Automation | SME | MWK 900,000 |
| B4 — Custom Dashboard | SME | MWK 2,500,000 |

**Payment:** 50% upfront, 50% on delivery. WhatsApp API fees: ~$0.005–0.015 per message.

## 6. Data Handling Protocol

- All client conversations are processed via LLM provider APIs. Client must sign
  cross-border data transfer consent (Addendum §3).
- `integration_engineer` configures end-to-end encryption for data at rest.
- `data_privacy_officer` enforces 30-day post-delivery deletion (configurable).
- Client-isolated agent hierarchies prevent data leakage between clients.

## 7. Blocking Conditions (Must Clear Before Activation)

- [ ] client_onboarding_offer_b approval matrix entry passes
- [ ] service_level_liability_cap.status = "ratified" in malawi_offers.yaml
- [ ] Data Processing Agreement template available (legal_owner)
- [ ] WhatsApp Business API reviewed by ciso
- [ ] Client Onboarding Policy G1–G4 gates pass

## 8. Post-Delivery

- 30-day support window. `support_agent` handles questions.
- `audit_trail_owner` logs all data access during engagement.
- Postmortem: `data_privacy_officer` confirms data deletion; `support_agent` logs feedback.
