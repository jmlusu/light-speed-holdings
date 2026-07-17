---
raci_id: RACI-ESCALATION-001
title: Escalation Handling RACI
department: operations
owner: chief_of_staff
version: 1.0
effective_date: 2026-07-17
---

# Escalation Handling RACI

## Overview

Defines responsibility assignment for handling escalations when tasks fail, timeouts occur, or situations exceed an agent's authority.

## RACI Matrix

| Activity | detecting_agent | department_exec | chief_of_staff | cto | human_operator |
|----------|-----------------|-----------------|----------------|-----|----------------|
| Detect anomaly | R | I | I | I | I |
| Create escalation event | R | I | I | I | I |
| Initial triage | C | R | A | I | I |
| Assign severity level | C | R | A | I | I |
| Contain the incident | I | R | C | C | I |
| Investigate root cause | I | R | C | C | I |
| Implement fix | I | R | I | A | I |
| Verify resolution | R | A | I | C | I |
| Create postmortem | C | R | A | I | I |
| Approve postmortem | I | C | I | I | R |
| Update escalation rules | I | C | R | A | I |
| Close escalation | I | R | A | I | I |

## Notes

- Detecting Agent is responsible for raising the alert but not for resolution
- Department Executive owns resolution within their domain
- Chief of Staff is accountable for triage and cross-department coordination
- CTO is accountable for technical fixes
- Human Operator approves postmortems and policy changes to escalation rules

## Escalation Severity Matrix

| Severity | Criteria | Approver | SLA |
|----------|----------|----------|-----|
| Low | < 5 tasks, < 5 min | Department Executive | 1 hour |
| Medium | 5-20 tasks, 5-30 min | Chief of Staff | 30 min |
| High | 20-50 tasks, 30m-2h | CTO | 15 min |
| Critical | > 50 tasks, > 2h | Human Operator | Immediate |

## Escalation Rules

| Condition | Escalate To | Authority |
|-----------|-------------|-----------|
| Task timeout > 10 min | Chief of Staff | Auto-escalation |
| 3+ consecutive failures | Human Operator | Mandatory human review |
| Provider outage | CTO | Switch provider |
| Data loss suspected | Human Operator | Immediate escalation |
| Budget exceeded | CFO | Freeze non-essential spend |

---

*RACI Owner: chief_of_staff*
*Version: 1.0*
