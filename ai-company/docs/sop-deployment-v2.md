---
sop_id: SOP-DEPLOY-002
title: Agent Deployment Procedure v2
department: engineering
owner: cto
version: 2.0
effective_date: 2026-07-20
last_reviewed: 2026-07-20
status: active
---

# Agent Deployment Procedure v2

## 1. Purpose

Define the complete, end-to-end process for deploying new agents, updating agent configurations, and regenerating agent files safely. This v2 procedure incorporates lessons from v1 and adds validation, rollback, and monitoring steps.

## 2. Scope

Applies to all changes to:
- `company/agent-registry.json` — agent definitions
- `company/departments.yaml` — department assignments
- `company/models.yaml` — model routing overrides
- `templates/agents/` — Jinja2 agent templates

## 3. Definitions

| Term | Definition |
|------|------------|
| Registry | `company/agent-registry.json` — single source of truth for agents |
| Generator | CLI tool that renders agent markdown from registry |
| Bootstrap | Full company generation from configuration files |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Requesting Agent | Identifies need for new/updated agent |
| Lead Engineer | Reviews and approves configuration changes |
| CTO | Reviews security, permissions, and architecture |
| Human Operator | Final sign-off on production deployment |

## 5. Procedure

### Step 1: Identify Need

Document the requirement:
- What work needs to be done?
- Why can't existing agents handle it?
- What tools and permissions are required?
- What department does the agent belong to?

**Expected Result:** Written staffing request with role description.

### Step 2: Prepare Configuration

Edit `company/agent-registry.json` with the new agent entry:

```json
{
  "id": "new-agent-id",
  "name": "New Agent Name",
  "role": "Role Title",
  "type": "Specialist",
  "department": "engineering",
  "reportsTo": "lead-engineer",
  "tools": ["read", "write", "grep"],
  "permissions": ["read", "edit"]
}
```

**Checklist:**
- [ ] Agent ID follows snake_case convention
- [ ] Required fields present: id, name, role, type, department, reportsTo
- [ ] `reportsTo` references a valid existing agent
- [ ] Department exists in `company/departments.yaml`
- [ ] Tools are appropriate for the role (least privilege)
- [ ] Permissions follow the security matrix
- [ ] No duplicate agent IDs

### Step 3: Security Review

CTO reviews the configuration:

- Permissions are least-privilege
- No unnecessary tool access
- Reporting hierarchy is valid
- No conflicts with existing roles
- Model tier is appropriate

**Expected Result:** Security sign-off or required changes.

### Step 4: Validate Registry

Run validation to catch configuration errors:

**Command:**
```bash
ai-company generate --dry-run
```

**Expected Result:** All agents validate cleanly, no errors reported.

### Step 5: Generate Agent Files

Render agent markdown files from registry:

**Command:**
```bash
ai-company generate
```

**Expected Result:** `.opencode/agents/*.md` files updated with new agent.

### Step 6: Verify Generated Files

Check the generated output:

**Command:**
```bash
ai-company agents list
```

**Expected Result:** New agent appears in the list with correct details.

Also verify the generated file exists:

**Command:**
```bash
dir .opencode\agents\new-agent-id.md    # Windows
ls -la .opencode/agents/new-agent-id.md # Linux/macOS
```

### Step 7: Run Tests

Ensure no regressions:

**Command:**
```bash
pytest && ruff check src/ && mypy src/
```

**Expected Result:** All tests pass, no lint errors, no type errors.

### Step 8: Deploy

For CI/CD: push changes and let GitHub Actions run.

**Command:**
```bash
git add company/ .opencode/agents/
git commit -m "feat(agents): add new-agent-id to engineering"
git push
```

**Expected Result:** Changes deployed, CI passes.

### Step 9: Smoke Test

Verify agents respond after deployment:

**Command:**
```bash
ai-company agents list
ai-company doctor run
```

**Expected Result:** All agents listed, no errors in diagnostics.

### Step 10: Monitor

Watch for issues in the first hour:

- Check dashboard for task processing
- Monitor for escalation events
- Verify LLM provider connectivity

**Command:**
```bash
ai-company orchestrator tick
ai-company dashboard kpi list
```

**Expected Result:** System operating normally, no new escalations.

## 6. Rollback Procedure

If a deployment introduces issues:

1. Revert the registry change:
   ```bash
   git revert HEAD
   ```

2. Regenerate agent files:
   ```bash
   ai-company generate
   ```

3. Verify rollback:
   ```bash
   ai-company agents list
   ```

4. Run diagnostics:
   ```bash
   ai-company doctor run
   ```

5. Notify the team via MessageBus if critical.

## 7. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Registry validation fails | Fix config, do not deploy | Lead Engineer |
| Tests fail after deploy | Rollback and investigate | CTO |
| Generated files unexpected | Review template changes | Lead Engineer |
| Agent conflicts with existing roles | Review organizational structure | CTO |
| Security violation detected | Immediate rollback | CTO + CEO |

## 8. Verification Checklist

- [ ] Staffing need documented
- [ ] Agent configuration written
- [ ] Security review completed
- [ ] Registry validates cleanly
- [ ] Agent files generated
- [ ] Agent appears in agents list
- [ ] All tests pass
- [ ] Ruff clean
- [ ] Mypy clean
- [ ] CI passes on push
- [ ] Smoke test passes
- [ ] No new escalations in first hour

## 9. References

- `company/agent-registry.json` — Agent registry source of truth
- `company/departments.yaml` — Department assignments
- `company/models.yaml` — Model routing configuration
- `docs/USER-GUIDE.md` — CLI command reference
- `docs/sop-hr-onboarding.md` — Agent onboarding procedure
- `docs/raci-hiring.md` — RACI matrix for hiring decisions

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | cto | Initial release |
| 2.0 | 2026-07-20 | cto | Added security review, dry-run validation, rollback, monitoring |

---

*SOP Owner: cto*
*Next Review: 2026-10-20*
