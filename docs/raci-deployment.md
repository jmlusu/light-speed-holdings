---
raci_id: RACI-DEPLOY-001
title: Agent Deployment RACI
department: engineering
owner: cto
version: 1.0
effective_date: 2026-07-17
---

# Agent Deployment RACI

## Overview

Defines responsibility assignment for deploying agent configuration changes to production.

## RACI Matrix

| Activity | lead_engineer | cto | chief_of_staff | hr_agent | human_operator |
|----------|---------------|-----|----------------|----------|----------------|
| Prepare configuration changes | R | C | I | I | I |
| Validate against registry | R | I | I | I | I |
| Security review | C | A | I | I | I |
| Generate agent files | R | I | I | I | I |
| Run test suite | R | A | I | I | I |
| Approve for deployment | I | C | A | I | R |
| Deploy to production | R | I | I | I | I |
| Verify post-deploy | R | A | I | I | I |
| Update documentation | R | I | I | C | I |
| Close deployment ticket | R | I | A | I | I |

## Notes

- Lead Engineer owns technical execution end-to-end
- CTO is accountable for security review (cannot be delegated)
- Human Operator has final approval gate for all production deployments
- Chief of Staff is accountable for cross-department coordination

## Escalation Rules

| Condition | Escalate To | Authority |
|-----------|-------------|-----------|
| Tests fail after deploy | cto | Technical decision-making |
| Security review rejected | cto | Full authority on security |
| Deployment blocked by approval | chief_of_staff | Interim authority |
| Human operator unavailable | chief_of_staff | 24h interim deployment authority |

---

*RACI Owner: cto*
*Version: 1.0*
