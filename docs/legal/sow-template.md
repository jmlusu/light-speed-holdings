# Statement of Work (SOW) Template
## — Per-Engagement Scope Document —

> Each SOW is issued under the Master Service Agreement (msa-template.md).
> Variables in `{{brackets}}` are replaced per engagement.

---

**STATEMENT OF WORK**

| Field | Value |
|-------|-------|
| **SOW ID** | SOW-{{sow_id}} |
| **Client** | {{client_name}} |
| **Offer** | {{offer_name}} ({{offer_letter}}) |
| **SOW Date** | {{swo_date}} |
| **Project Start** | {{project_start_date}} |
| **Delivery Date** | {{delivery_date}} |
| **Project Manager** | {{project_manager_agent}} |
| **Lead Agent** | {{lead_agent}} |
| **Supporting Agents** | {{supporting_agents}} |

---

## 1. OBJECTIVE

{{objective_description}}

## 2. SCOPE OF WORK

### 2.1 Deliverables
{{deliverables_list}}

### 2.2 Milestones
| Milestone | Due Date | Approval Gate |
|-----------|----------|---------------|
| Kickoff complete | {{kickoff_date}} | Client sign-off |
| Draft review 1 | {{draft_date}} | human_ceo review gate |
| Final delivery | {{delivery_date}} | Client acceptance |

### 2.3 Out of Scope
{{out_of_scope}}

## 3. TIMELINE AND DELIVERY

| Phase | Activity | Owner Agent | Duration |
|-------|----------|-------------|----------|
| 1 | Brief intake → inbox.json task | human_ceo | 1 day |
| 2 | Scoping & proposal | {{lead_agent}} | 1–2 days |
| 3 | Build (agent execution) | Specialist agents | {{build_duration}} |
| 4 | Human review gate | human_ceo | 1 day |
| 5 | QA & delivery | qa_lead + support_agent | 1 day |

**Total estimated turnaround:** {{total_turnaround}} days

## 4. INVESTMENT

| Component | Currency | Amount |
|-----------|----------|--------|
| Upfront deposit (50%) | {{currency}} | {{deposit_amount}} |
| Balance on delivery (50%) | {{currency}} | {{balance_amount}} |
| Ad spend (if applicable) | — | Pass-through |
| Third-party fees | — | Pass-through |

**Total project fee:** {{total_amount}} {{currency}}

**50% deposit required before work begins. Balance due on delivery.**

## 5. APPROVAL GATE REQUIREMENTS

Before any SOW can be activated in the delivery pipeline:

1. Client Onboarding Policy gates G1–G4 must pass (see policy POL-CL-001)
2. For Offer B & C only: `malawi_offers.yaml` governance check must pass
3. human_ceo explicitly approves the task in `inbox.json` with `requires_approval=True`

## 6. ACCEPTANCE CRITERIA

{{acceptance_criteria}}

## 7. REVISION POLICY

Two (2) rounds of revisions included. Additional revisions billed at
MWK 60,000 (≈ $35)/hour. Express delivery (≤50% of standard turnaround) = +40%.

---

**Approvals:**

| Client | Service Provider |
|--------|-----------------|
| Signature: ________________ Date: ____ | Signature: ________________ Date: ____ |
| Name: ________________ | Name: ________________ |
| Title: ________________ | Title: ________________ |
