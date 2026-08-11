---
sop_id: SOP-DEPLOY-001
title: Agent Deployment Procedure
department: engineering
owner: cto
version: 1.0
effective_date: 2026-07-17
last_reviewed: 2026-07-17
status: active
---

# Agent Deployment Procedure

## 1. Purpose

Define the standard process for deploying new agents, updating agent configurations, and regenerating agent files safely.

## 2. Scope

Applies to all changes to `company-registry.yaml`, `company/*.yaml`, and agent template files.

## 3. Definitions

| Term | Definition |
|------|------------|
| Registry | `company-registry.yaml` — single source of truth for agents |
| Generator | Jinja2-based tool that renders agent markdown from registry |
| Harness | Change tracking system under `harness/` directory |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| Requesting Agent | Identifies need for new/updated agent |
| Lead Engineer | Reviews and approves configuration changes |
| Generator | Renders agent files from registry |
| Human Operator | Final sign-off on production deployment |

## 5. Procedure

### Step 1: Prepare Changes

Edit `company/agent-registry.json` with agent configuration.

**Checklist:**
- [ ] Agent ID follows snake_case convention
- [ ] Required fields present: id, name, role, department, tools, permissions
- [ ] Department exists in `company/departments.yaml`
- [ ] No duplicate agent IDs

### Step 2: Validate Configuration

Run registry validation.

**Command:**
```bash
ai-company generate --dry-run
```

**Expected Result:** All agents validate cleanly, no errors reported.

### Step 3: Generate Agent Files

Render agent markdown files from registry.

**Command:**
```bash
ai-company generate
```

**Expected Result:** `.opencode/agents/*.md` files updated.

### Step 4: Verify Generated Files

Check generated files match expected output.

**Command:**
```bash
ls -la .opencode/agents/
```

**Expected Result:** All expected agent files present, no orphaned files.

### Step 5: Run Tests

Ensure no regressions.

**Command:**
```bash
cd ai-company && pytest && ruff check src/ && mypy src/
```

**Expected Result:** All tests pass, no lint errors, no type errors.

### Step 6: Deploy

For CI/CD: push changes and let GitHub Actions run.

For manual: commit and push.

**Command:**
```bash
git add company/ .opencode/agents/ && git commit -m "deploy: update agent registry" && git push
```

**Expected Result:** Changes deployed, CI passes.

### Step 7: Smoke Test

Verify agents respond after deployment.

**Command:**
```bash
ai-company agents list
```

**Expected Result:** All agents listed, no errors.

## 6. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Registry validation fails | Fix config, do not deploy | Lead Engineer |
| Tests fail after deploy | Rollback and investigate | CTO |
| Generated files unexpected | Review template changes | Lead Engineer |

## 7. Verification Checklist

- [ ] Registry validates cleanly
- [ ] Generator produces expected output
- [ ] All tests pass
- [ ] Ruff clean
- [ ] Mypy clean
- [ ] CI passes on push
- [ ] Agents listed correctly post-deploy

## 8. References

- `company-registry.yaml` — Agent registry source of truth
- `company/agent-registry.json` — Full agent metadata
- `templates/agents/agent.md.j2` — Agent template

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-17 | cto | Initial release |

---

*SOP Owner: cto*
*Next Review: 2026-10-17*
