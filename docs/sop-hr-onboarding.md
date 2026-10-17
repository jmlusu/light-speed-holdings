---
sop_id: SOP-HR-001
title: Agent Onboarding Procedure
department: hr
owner: chief_of_staff
version: 1.0
effective_date: 2026-07-17
last_reviewed: 2026-07-17
status: active
---

# Agent Onboarding Procedure

## 1. Purpose

Define the standard process for adding a new AI agent to the company hierarchy, from identification of need through deployment and verification.

## 2. Scope

Applies to all new agent additions, including new specialists, department heads, and executive roles.

## 3. Definitions

| Term | Definition |
|------|------------|
| Requesting Party | Department head or executive identifying the staffing need |
| Configuration | Agent entry in `company/agent-registry.json` |
| Onboarding | End-to-end process from need identification to active deployment |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Requesting Party | Identifies need, defines role requirements |
| HR Agent | Owns the onboarding workflow end-to-end |
| CTO | Reviews configuration for security and permissions |
| Lead Engineer | Generates agent files and validates output |
| Human Operator | Final approval gate before deployment |

## 5. Procedure

### Step 1: Identify Staffing Need

Department head documents the need:
- What work needs to be done?
- Why can't existing agents handle it?
- What tools and permissions are required?

**Expected Result:** Written staffing request with role description.

### Step 2: Define Agent Role

HR Agent creates the agent configuration:
- Unique snake_case ID
- Role title and description
- Department assignment
- Reporting hierarchy
- Tool list
- Permission set

**Expected Result:** Draft agent entry for `company/agent-registry.json`.

### Step 3: Security Review

CTO reviews the configuration:
- Permissions are least-privilege
- No unnecessary tool access
- Reporting hierarchy is valid
- No conflicts with existing roles

**Expected Result:** Security sign-off or required changes.

### Step 4: Validate and Generate

Lead Engineer validates configuration and regenerates agent files:

**Command:**
```bash
ai-company generate --dry-run    # Validate first
ai-company generate              # Generate files
```

**Expected Result:** New agent `.md` file in `.opencode/agents/`.

### Step 5: Run Tests

Verify no regressions:

**Command:**
```bash
pytest && ruff check src/ && mypy src/
```

**Expected Result:** All checks pass.

### Step 6: Human Approval

Submit to human operator for final sign-off.

**Command:**
```bash
ai-company orchestrator approval pending
```

**Expected Result:** Human operator approves the new agent.

### Step 7: Verify Deployment

Post-deployment verification:

**Command:**
```bash
ai-company agents list
```

**Expected Result:** New agent appears in the agent list.

### Step 8: Update Documentation

Update organizational documentation:

- Add agent to `docs/ORGANIZATION.md`
- Update `company/departments.yaml` if department assignment changed
- Update relevant RACI matrices if role has approval authority

## 6. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Configuration rejected by security | Revise and resubmit | CTO |
| Tests fail after generation | Debug and fix | Lead Engineer |
| Human operator unavailable > 24h | Escalate to Chief of Staff | chief-of-staff |

## 7. Verification Checklist

- [ ] Staffing need documented
- [ ] Agent configuration written
- [ ] Security review completed
- [ ] Agent files generated
- [ ] Tests pass
- [ ] Human operator approved
- [ ] Agent verified in list
- [ ] Roster updated

## 8. References

- `company/agent-registry.json` — Agent registry
- `docs/raci-hiring.md` — RACI matrix for hiring
- `docs/BOARD-GOVERNANCE.md` — Governance authority

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | chief_of_staff | Initial release |

---

*SOP Owner: chief_of_staff*
*Next Review: 2026-10-17*
