# Client Onboarding Approval Policy

**Policy ID:** POL-CL-001
**Owner:** human_ceo
**Approved by:** Board of Directors (ratified 2026-08-12)
**Classification:** Internal — Confidential
**Effective Date:** 2026-08-12
**Status:** ACTIVE

---

## 1. Purpose

Establishes mandatory governance gates that must pass before ANY client work begins for external paying clients. This policy exists because Light Speed Holdings delivers services through AI agents that process client data and LLM provider APIs.

## 2. Policy Statement

No client-facing deliverable may be produced, and no task may be created in `.opencode/inbox.json` for a client engagement, until ALL four gates below have passed:

| Gate | Owner | Action Required | Evidence Location |
|------|-------|-----------------|-------------------|
| G1: Signed Contract | `legal_owner` | MSA signed by both parties | `legal/clients/<client_id>/contract.signed` |
| G2: Data Processing Agreement | `data_privacy_officer` | DPA executed, data classification recorded | `legal/clients/<client_id>/dpa.yaml` |
| G3: Compliance Risk Assessment | `compliance_officer` | Risk assessment logged, GDPR/Act 2017 checked | `legal/clients/<client_id>/risk-assessment.md` |
| G4: Security Review | `ciso` | Security review logged, threat model recorded | `legal/clients/<client_id>/security-review.md` |

The `ApprovalGate` (orchestrator/approval.py) enforces G1–G4 as a composite pre-condition. Tasks tagged `client_work` with `requires_approval=True` will remain in `PENDING` with status `BLOCKED_GATES` until all four gates are satisfied.

## 3. Offer-Specific Blocking

Based on `config/company/malawi_offers.yaml`:

| Offer | Risk Level | Governance State | Reason |
|-------|-----------|------------------|--------|
| **Offer A** (Digital Presence) | medium | **approved** | Low data sensitivity; standard gates suffice |
| **Offer B** (BPA/Chatbots) | critical | **blocked** | WhatsApp customer data; cross-border LLM transfer; client_onboarding_offer_b approval requires `[clo, ciso, data_privacy_officer, human_ceo, board_chair]` |
| **Offer C** (Data & Reporting) | critical | **blocked** | NGO donor data; professional liability; donor_data_handling approval requires `[ciso, cdo, data_privacy_officer, human_ceo]` |
| **Offer D** (Digital Marketing) | low | **approved** | Minimal PII; standard gates suffice |
| **Offer E** (Platform Licensing) | high | **approved** | No client data handling; product license only |

Offers B and C remain **BLOCKED** until `service_level_liability_cap.status` transitions to `ratified` in `malawi_offers.yaml`.

## 4. Data Handling Protocol

All client data is classified at onboarding (Gate G2):

- **PII**: Personal identifiers, contact info, donor lists. Must trigger encryption-at-rest, access logging via `audit_trail_owner`, and 30-day post-delivery deletion unless client signs extended retention.
- **Non-PII**: Aggregated reports, anonymized KPIs. Standard retention applies.
- **Donor data** (Offer C only): Treated as **Tier-1 sensitive** — requires explicit consent for cross-border transfer to LLM provider APIs. Client must sign a waiver acknowledging AI processing.

## 5. Review Cycle

This policy is reviewed quarterly by the Board Risk Committee. Any failure of a governance gate (e.g., a task created without G1–G4 passing) is treated as a **security incident** and triggers `incident_response_lead` escalation.

## 6. Enforcement

The `client_intake` service (`src/ai_company/services/client_intake.py`) implements the gate check. If any gate is missing, `ClientIntakeService.create_client_engagement()` raises `GovernanceGateError` and writes the failure to the audit trail.
