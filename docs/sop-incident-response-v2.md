---
sop_id: SOP-INCIDENT-002
title: Incident Response Procedure v2
department: engineering
owner: cto
version: 2.0
effective_date: 2026-07-20
last_reviewed: 2026-07-20
status: active
---

# Incident Response Procedure v2

## 1. Purpose

Establish a comprehensive process for detecting, triaging, containing, resolving, and learning from incidents affecting AI agent operations. This v2 procedure adds automated detection, structured communication, and postmortem-driven learning.

## 2. Scope

Applies to all agent failures, task timeouts, approval gate breaches, model provider outages, budget violations, and security incidents.

## 3. Definitions

| Term | Definition |
|------|------------|
| Incident | Any unplanned interruption or degradation of agent service |
| Severity | Impact level: SEV-1 (critical), SEV-2 (high), SEV-3 (medium), SEV-4 (low) |
| Escalation | Routing an issue to a higher-authority agent or human |
| Postmortem | Blameless analysis of root cause and prevention |
| MTTR | Mean Time To Resolution |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Detecting Agent | First to notice anomaly; creates alert |
| Chief of Staff | Triage and initial response coordination |
| CTO | Technical decision-making for SEV-1/SEV-2 |
| CFO | Budget-related incidents |
| Human Operator | Final approval and postmortem review |

## 5. Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|--------------|---------|
| SEV-1 | Complete system outage, data loss, security breach | Immediate | MessageBus failure, all agents unresponsive |
| SEV-2 | Major feature degraded, budget exceeded | 30 minutes | HITL gate timeout, cost tracker failure |
| SEV-3 | Minor issue, workaround available | 4 hours | Dashboard display bug, non-critical CLI error |
| SEV-4 | Cosmetic, informational | 1 week | Typo in help text, minor formatting issue |

## 6. Procedure

### Step 1: Detection & Alert

**Automated detection:**
- Doctor checks detect component failures
- CostTracker detects budget violations
- HITL gate detects timeout conditions
- Health check endpoint fails

**Manual detection:**
- Human operator notices anomaly
- Agent reports error via MessageBus

**Command:**
```bash
ai-company orchestrator tick
ai-company doctor run
```

**Expected Result:** Anomaly appears in pending escalations list or doctor report.

### Step 2: Triage

Chief of Staff evaluates severity:

**Severity assessment matrix:**

| Criteria | SEV-4 | SEV-3 | SEV-2 | SEV-1 |
|----------|-------|-------|-------|-------|
| Tasks affected | <5 | 5-20 | 20-50 | >50 |
| Agents affected | 1 | 2-3 | 4-6 | >6 |
| Duration | <5m | 5-30m | 30m-2h | >2h |
| Data impact | None | None | Potential | Confirmed |
| Budget impact | None | <$50 | $50-$200 | >$200 |

**Command:**
```bash
ai-company orchestrator escalation pending
```

**Expected Result:** Severity assigned, escalation rule matched, response team notified.

### Step 3: Contain

**For SEV-1 (Critical):**
1. Immediately halt affected agents
2. Route all pending approvals to human gate
3. Isolate affected agent from task queue
4. Notify CTO and Human Operator immediately

**Command:**
```bash
ai-company orchestrator escalation pending
```

**For SEV-2 (High):**
1. Pause affected scheduled tasks
2. Route pending approvals to human gate
3. Switch to fallback LLM provider if needed

**For SEV-3/SEV-4:**
1. Document the issue
2. Assign to appropriate agent for resolution
3. Continue normal operations

### Step 4: Resolve

Assigned agent investigates and implements fix:

**Commands:**
```bash
# Check current system state
ai-company orchestrator tick
ai-company doctor run

# Process pending tasks after fix
ai-company executor tick

# Verify system health
ai-company dashboard kpi list
```

**Expected Result:** Tasks resume processing, error rate drops, system returns to normal.

### Step 5: Verify

Run verification checklist:
- [ ] Error rate returns to baseline
- [ ] All pending tasks processed
- [ ] No new escalations triggered
- [ ] Model provider connectivity restored
- [ ] Approval gates functioning
- [ ] Budget limits still enforced
- [ ] Cost tracking operational

### Step 6: Close & Learn

Create postmortem for SEV-1 and SEV-2 incidents:

**Command:**
```bash
ai-company orchestrator postmortem create INC-{TASK_ID} \
  --title "Brief description" \
  --severity high \
  --affected-agent lead-engineer \
  --department engineering
```

**Update postmortem with findings:**
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

## 7. Communication Template

### During Incident (SEV-1/SEV-2)

```
[SEV-{LEVEL}] {INCIDENT_TITLE}

Status: {INVESTIGATING | IDENTIFIED | MONITORING | RESOLVED}
Impact: {DESCRIPTION_OF_IMPACT}
Timeline: {KEY_EVENTS}
Next Update: {TIME}
```

### Post-Incident

```
[RESOLVED] {INCIDENT_TITLE}

Duration: {START_TIME} - {END_TIME} ({TOTAL_DURATION})
Impact: {DESCRIPTION_OF_IMPACT}
Root Cause: {BRIEF_DESCRIPTION}
Resolution: {WHAT_WAS_DONE}
Prevention: {ACTION_ITEMS}
```

## 8. Escalation Path

| Condition | Action | Contact | SLA |
|-----------|--------|---------|-----|
| Task timeout > 10min | Auto-escalate | Chief of Staff | 10 min |
| 3+ consecutive failures | Escalate to human | Human Operator | 30 min |
| Provider outage | Switch provider | CTO | 15 min |
| Data loss suspected | Immediate escalation | Human Operator | Immediate |
| Budget exceeded | Pause non-critical tasks | CFO | Immediate |
| Security violation | Halt and investigate | CTO + CEO | Immediate |

## 9. Postmortem Requirements

### Required Sections

1. **Incident Summary**: What happened, when, how long
2. **Impact**: Tasks affected, agents affected, cost impact
3. **Timeline**: Key events in chronological order
4. **Root Cause**: Technical root cause analysis
5. **Resolution**: What was done to fix it
6. **Prevention**: Action items to prevent recurrence
7. **Lessons Learned**: What we learned and will change

### Postmortem Quality Criteria

- [ ] Blameless — focuses on systems, not individuals
- [ ] Actionable — each lesson has a concrete action item
- [ ] Timely — completed within 48 hours of SEV-1/SEV-2
- [ ] Reviewed — Human Operator has reviewed and approved
- [ ] Tracked — Action items are tracked to completion

## 10. Escalation Rules (Automated)

The `EscalationManager` enforces these rules automatically:

| Rule | Trigger | Escalate To | Timeout |
|------|---------|------------|---------|
| Task failure | 3 consecutive failures | Department executive | 30 min |
| Budget exceeded | CostTracker check fails | CFO | Immediate |
| HITL timeout | No human response in 30 min | Chief of Staff | 30 min |
| Security violation | Path traversal detected | CTO + CEO | Immediate |
| System outage | Health check fails | CTO | 15 min |
| Provider outage | All providers in tier failing | CTO | 15 min |

## 11. Verification Checklist

- [ ] Incident timeline documented
- [ ] Root cause identified
- [ ] Fix applied and tested
- [ ] Prevention measures defined
- [ ] Postmortem created
- [ ] Postmortem reviewed by human
- [ ] Action items tracked
- [ ] Team notified of resolution

## 12. References

- `docs/RISK-REGISTER.md` — Risk register with mitigations
- `docs/MODEL-ROUTING-POLICY.md` — Provider fallback rules
- `docs/BOARD-GOVERNANCE.md` — Escalation authority
- `docs/sop-incident-response.md` — v1 incident response procedure
- `src/ai_company/orchestrator/escalation.py` — EscalationManager
- `src/ai_company/executor/hitl_gate.py` — HITL gates

## 13. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | cto | Initial release |
| 2.0 | 2026-07-20 | cto | Added automated detection, communication templates, postmortem quality criteria |

---

*SOP Owner: cto*
*Next Review: 2026-10-20*
