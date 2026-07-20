---
sop_id: SOP-FINANCE-001
title: Budget Approval Procedure
department: finance
owner: cfo
version: 1.0
effective_date: 2026-07-17
last_reviewed: 2026-07-17
status: active
---

# Budget Approval Procedure

## 1. Purpose

Define the standard process for requesting, reviewing, and approving expenditures including LLM API costs, infrastructure, and tool licenses.

## 2. Scope

Applies to all spending requests over $10 or equivalent token budget. Covers API costs, compute, third-party services, and tool subscriptions.

## 3. Definitions

| Term | Definition |
|------|------------|
| Requester | Agent or department initiating the spend request |
| Budget Owner | CFO — final authority on all expenditures |
| Token Budget | Allocated LLM API spending per department per month |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Requesting Agent | Documents need, estimates cost, submits request |
| Department Executive | Reviews and endorses department-level requests |
| CFO | Approves all requests, tracks budget utilization |
| Human Operator | Approves requests exceeding executive authority |

## 5. Procedure

### Step 1: Estimate Cost

Requester calculates the expected cost:
- LLM tokens: estimate input/output tokens × provider rate
- Compute: estimate hours × hourly rate
- Services: monthly subscription cost

**Expected Result:** Cost estimate with breakdown.

### Step 2: Check Budget

Requester verifies department has remaining budget:

**Command:**
```bash
ai-company dashboard kpi show finance
```

**Expected Result:** Budget utilization is below threshold (target: 90%).

### Step 3: Submit Request

Requester creates an approval request:

**Command:**
```bash
ai-company orchestrator approval pending
```

Or through the decision engine:

**Command:**
```bash
ai-company decision evaluate "spend $50 on API calls"
```

**Expected Result:** Approval request created with cost details.

### Step 4: Executive Review

Department executive reviews:
- Is the spend aligned with department goals?
- Is the cost estimate reasonable?
- Are there cheaper alternatives?

**Expected Result:** Executive endorses or rejects.

### Step 5: CFO Approval

CFO evaluates:
- Budget remaining for the period
- ROI justification
- Comparison to historical spend
- Compliance with spending policies

**Command:**
```bash
ai-company orchestrator approval approve REQUEST_ID --approved-by cfo --notes "Approved for Q3 marketing campaign"
```

**Expected Result:** Request approved or rejected with rationale.

### Step 6: Execute Purchase

Upon approval, the requesting agent proceeds with the expenditure.

**Expected Result:** Service provisioned or tokens allocated.

### Step 7: Record and Track

CFO records the expenditure:
- Amount
- Department
- Purpose
- Date
- Remaining budget

**Expected Result:** Budget ledger updated.

## 6. Approval Thresholds

| Amount | Approver | SLA |
|--------|----------|-----|
| < $50 | Department Executive | 4 hours |
| $50 - $500 | CFO | 24 hours |
| > $500 | Human Operator | 48 hours |
| > $5,000 | Human Operator + Board | 72 hours |

## 7. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Request pending > SLA | Auto-escalate | CFO |
| Budget exceeded | Freeze non-essential spend | Human Operator |
| Unexpected cost spike | Investigate immediately | CTO + CFO |

## 8. Verification Checklist

- [ ] Cost estimate documented
- [ ] Budget availability confirmed
- [ ] Approval request submitted
- [ ] Executive reviewed and endorsed
- [ ] CFO approved
- [ ] Expenditure recorded
- [ ] Remaining budget updated

## 9. References

- `company/config/kpis.yaml` — Budget KPI definitions
- `docs/RISK-REGISTER.md` — Financial risk items
- `docs/BOARD-GOVERNANCE.md` — Spending authority

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | cfo | Initial release |

---

*SOP Owner: cfo*
*Next Review: 2026-10-17*
