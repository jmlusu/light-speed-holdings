---
sop_id: SOP-INCIDENT-001
title: Incident Response Procedure
department: engineering
owner: cto
version: 1.0
effective_date: 2026-07-17
last_reviewed: 2026-07-17
status: active
---

# Incident Response Procedure

## 1. Purpose

Establish a consistent process for detecting, triaging, resolving, and learning from incidents affecting AI agent operations.

## 2. Scope

Applies to all agent failures, task timeouts, approval gate breaches, and model provider outages.

## 3. Definitions

| Term | Definition |
|------|------------|
| Incident | Any unplanned interruption or degradation of agent service |
| Severity | Impact level: low, medium, high, critical |
| Escalation | Routing an issue to a higher-authority agent or human |
| Postmortem | Blameless analysis of root cause and prevention |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Detecting Agent | First to notice anomaly; creates alert |
| Chief of Staff | Triage and initial response |
| CTO | Technical decision-making for high/critical |
| Human Operator | Final approval and postmortem review |

## 5. Procedure

### Step 1: Detection & Alert

Agent detects anomaly (task failure, timeout, error rate spike).

**Command:**
```bash
ai-company orchestrator tick
```

**Expected Result:** Anomaly appears in pending escalations list.

### Step 2: Triage

Chief of Staff evaluates severity using the matrix:

| Criteria | Low | Medium | High | Critical |
|----------|-----|--------|------|----------|
| Tasks affected | <5 | 5-20 | 20-50 | >50 |
| Agents affected | 1 | 2-3 | 4-6 | >6 |
| Duration | <5m | 5-30m | 30m-2h | >2h |

**Expected Result:** Severity assigned, escalation rule matched.

### Step 3: Contain

If severity is high or critical:
- Pause affected scheduled tasks
- Route pending approvals to human gate
- Isolate affected agent from task queue

**Command:**
```bash
ai-company orchestrator escalation pending
```

**Expected Result:** Escalation events visible with clear ownership.

### Step 4: Resolve

Assigned agent investigates and implements fix.

**Command:**
```bash
ai-company executor tick
```

**Expected Result:** Tasks resume processing, error rate drops.

### Step 5: Verify

Run verification checklist:
- [ ] Error rate returns to baseline
- [ ] All pending tasks processed
- [ ] No new escalations triggered
- [ ] Model provider connectivity restored
- [ ] Approval gates functioning

### Step 6: Close & Learn

Create postmortem for medium+ severity incidents.

**Command:**
```bash
ai-company orchestrator postmortem create INC-{TASK_ID} \
  --title "Brief description" \
  --severity high \
  --affected-agent lead-engineer \
  --department engineering
```

**Update with findings:**
```bash
ai-company orchestrator postmortem update INC-{TASK_ID} \
  --root-cause "Root cause description" \
  --status resolved \
  --reviewed-by human-ceo
```

**Render to markdown:**
```bash
ai-company orchestrator postmortem render INC-{TASK_ID}
```

**Expected Result:** Postmortem created, updated, and rendered for review.

## 6. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Task timeout > 10min | Auto-escalate | Chief of Staff |
| 3+ consecutive failures | Escalate to human | Human Operator |
| Provider outage | Switch provider | CTO |
| Data loss suspected | Immediate escalation | Human Operator |

## 7. Verification Checklist

- [ ] Incident timeline documented
- [ ] Root cause identified
- [ ] Fix applied and tested
- [ ] Prevention measures defined
- [ ] Postmortem reviewed by human

## 8. References

- `docs/RISK-REGISTER.md` — Risk register with mitigations
- `docs/MODEL-ROUTING-POLICY.md` — Provider fallback rules
- `docs/BOARD-GOVERNANCE.md` — Escalation authority

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | cto | Initial release |

---

*SOP Owner: cto*
*Next Review: 2026-10-17*
