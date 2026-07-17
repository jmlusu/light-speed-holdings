---
raci_id: RACI-HIRING-001
title: AI Agent Hiring Workflow RACI
department: hr
owner: chief_of_staff
version: 1.0
effective_date: 2026-07-17
---

# AI Agent Hiring Workflow RACI

## Overview

Defines responsibility assignment for the end-to-end process of adding a new AI agent to the company hierarchy.

## Legend

| Code | Role | Meaning |
|------|------|---------|
| **R** | Responsible | Does the work |
| **A** | Accountable | Owns the outcome; sole signer |
| **C** | Consulted | Provides input before decision |
| **I** | Informed | Notified after decision |

## RACI Matrix

| Activity | hr_agent | chief_of_staff | cto | lead_engineer | department_head | human_operator |
|----------|----------|----------------|-----|---------------|-----------------|----------------|
| Identify staffing need | R | A | C | C | R | I |
| Define agent role & permissions | R | C | A | C | R | I |
| Write agent configuration | R | C | I | R | C | I |
| Review configuration for security | C | C | A | R | I | I |
| Validate against registry | R | I | I | R | I | I |
| Generate agent files | I | I | I | R | I | I |
| Run test suite | I | I | I | R | I | I |
| Approve for deployment | I | A | C | I | I | R |
| Deploy to production | I | I | I | R | I | C |
| Verify post-deploy | R | A | I | R | I | I |
| Update department roster | R | I | I | I | C | I |
| Close hiring ticket | R | A | I | I | I | I |

## Notes

- The human operator has final approval authority (gate) for all agent deployments
- CTO is accountable for security review; cannot be delegated
- Lead Engineer is responsible for technical implementation (config + generation)
- HR Agent owns the workflow end-to-end but is not accountable for technical decisions

## Escalation Rules

| Condition | Escalate To | Authority |
|-----------|-------------|-----------|
| Configuration rejected by security | cto | Full authority on security matters |
| Deployment fails CI | lead_engineer | Technical decision-making |
| Agent conflicts with existing role | department_head | Department-level approval |
| Human operator unavailable > 24h | chief_of_staff | Interim deployment authority |

---

*RACI Owner: chief_of_staff*
*Version: 1.0*
*Last Updated: 2026-07-17*
