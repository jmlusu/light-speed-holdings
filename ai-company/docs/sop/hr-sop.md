# Human Resources Standard Operating Procedure

**Document ID:** SOP-HR-001
**Department:** Human Resources / Operations
**Owner:** Chief Operating Officer (COO)
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure defines the processes for agent onboarding, role definition, performance evaluation, and culture management within Light Speed Holdings' AI Company Builder. It ensures consistent treatment of both human and AI agents throughout their lifecycle in the organization.

## 2. Scope

This SOP applies to all personnel-related activities including:

- Onboarding of new AI agents (registration, configuration, tool assignment)
- Onboarding of human operators and contributors
- Role and seniority definitions across the hierarchy
- Performance review cycles for AI agents
- Culture reinforcement and communication norms
- Offboarding and agent deprecation

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| COO | `coo` (executive) | HR policy ownership, resource allocation, organizational design |
| HR Lead | `hr_lead` (specialist) | Day-to-day HR operations, onboarding execution, performance tracking |
| Chief of Staff | `chief_of_staff` | Strategic alignment, cross-department staffing decisions |
| Department Executives | CTO, CAIO, etc. | Department-specific onboarding, mentoring, performance input |
| Human Operator | CEO / Founder | Final approval on hiring/firing decisions, culture setting |

## 4. Agent Onboarding

### 4.1 New Agent Registration

When a new agent is added to the organization, the following steps must be completed:

**Step 1: Define the agent in `company-registry.yaml`**

Every agent requires a complete entry in the registry with:

```yaml
- id: <snake_case_id>
  name: <Human-Readable Name>
  title: <Job Title>
  description: <One-paragraph description>
  department: <Department Name>
  reports_to: <Manager ID>
  responsibilities:
    - <Responsibility 1>
    - <Responsibility 2>
  guidelines: <Behavioral guidelines>
  tools: [read, write, execute]
```

**Step 2: Assign appropriate tools and permissions**

Tool assignments must follow the principle of least privilege:

| Seniority Level | Default Tools | Restrictions |
|----------------|---------------|-------------|
| Junior | `read`, `grep`, `list` | No write, no execute |
| Mid | `read`, `write`, `grep`, `list` | No execute, no code_interpreter |
| Senior | `read`, `write`, `execute`, `grep`, `list` | HITL required for write/execute |
| Lead | `read`, `write`, `execute`, `grep`, `list`, `code_interpreter` | HITL required for code_interpreter |
| Executive | All tools | Full access with HITL for dangerous operations |

**Step 3: Configure model routing**

Assign the agent to the appropriate cost/capability tier in `company/models.yaml`:

- **budget** tier: Local Ollama models (zero cost, lower capability)
- **standard** tier: Cost-effective cloud models (GPT-4o-mini, Claude 3.5 Haiku)
- **premium** tier: High-capability cloud models (GPT-4o, Claude 3.5 Sonnet)

**Step 4: Register in the agent registry**

Run the generator to create the agent's OpenCode-compatible markdown file:

```bash
python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
```

**Step 5: Verify the agent**

Run the following checks:

1. The generated `.opencode/agents/<agent_id>.md` file exists and is well-formed
2. The agent appears in `ai-company agents list`
3. The agent can receive tasks via `MessageBus.get_inbox(agent_id)`
4. The agent's tools are correctly configured in the generated file

### 4.2 Onboarding Checklist

The HR Lead must complete the following for each new agent:

- [ ] Agent definition added to `company-registry.yaml`
- [ ] Tools and permissions assigned per seniority level
- [ ] Model tier configured in `company/models.yaml`
- [ ] Agent file generated via `AgentGenerator`
- [ ] Agent appears in `ai-company agents list`
- [ ] Department executive has reviewed and approved the agent's responsibilities
- [ ] Agent's escalation path is defined (who they report to, who they escalate to)
- [ ] Agent's KPIs are defined (see Section 8)
- [ ] Agent has been introduced to the team via a MessageBus broadcast

### 4.3 Human Operator Onboarding

Human operators follow a parallel process:

1. **Access provisioning**: Environment variables configured (API keys for LLM providers)
2. **Tool access**: CLI access to `ai-company` commands verified
3. **Dashboard access**: CEO Dashboard URL and credentials provided
4. **Training**: Review of `docs/USER-GUIDE.md`, `docs/ARCHITECTURE.md`, and this SOP
5. **First task**: Guided walkthrough of creating and delegating a task via the MessageBus

## 5. Role Definitions

### 5.1 Seniority Levels

The organization uses five seniority levels defined in `Seniority` enum:

| Level | Enum | Decision Authority | Budget Authority | Escalation Level |
|-------|------|-------------------|-----------------|-----------------|
| Junior | `junior` | Task execution only | None | Escalate to manager |
| Mid | `mid` | Task execution, minor decisions | < $50/day | Escalate to senior |
| Senior | `senior` | Feature decisions, code review | < $200/day | Escalate to lead |
| Lead | `lead` | Technical architecture, team decisions | < $500/day | Escalate to executive |
| Executive | `executive` | Strategic decisions, budget approval | Unlimited (with approval) | Escalate to CEO/Human |

### 5.2 Department Structure

The current organizational structure:

```
CEO (Human)
  |
  +-- Chief of Staff (chief_of_staff)
        |
        +-- CTO (cto) -- Technology Department
        |     +-- Lead Developer (lead_dev)
        |
        +-- COO (coo) -- Operations Department
        |     +-- HR Lead (hr_lead)
        |     +-- Ops Lead (ops_lead)
        |
        +-- CAIO (caio) -- AI Research Department
              +-- ML Engineer (ml_engineer)
```

### 5.3 Agent Type Classification

Agents are classified as either `human` or `ai` via the `AgentType` enum:

- **AI agents**: Execute tasks autonomously within their tool permissions. Subject to HITL gates for dangerous operations. Cost tracked via `CostTracker`.
- **Human agents**: Provide oversight, approval, and strategic direction. Not subject to automated cost tracking. Can override any AI agent decision.

## 6. Performance Reviews

### 6.1 AI Agent Performance Metrics

AI agent performance is measured through automated metrics collected by the `Dashboard` and `KPI Collector`:

| Metric | Description | Source |
|--------|-------------|--------|
| Task completion rate | % of tasks completed successfully | `MessageBus` task status |
| Average task duration | Time from task creation to completion | Task timestamps |
| Escalation rate | % of tasks escalated to a higher authority | `EscalationManager` events |
| Cost per task | Average LLM cost per task completed | `CostTracker` daily/task summaries |
| HITL approval rate | % of dangerous operations approved by humans | `ApprovalGate` records |
| Error rate | % of tasks that failed | `TaskStatus.FAILED` count |

### 6.2 Review Cadence

| Review Type | Frequency | Owner | Scope |
|-------------|-----------|-------|-------|
| Daily standup check | Daily | Department executive | Task status, blockers |
| Weekly performance sync | Weekly | COO | Cross-department metrics |
| Monthly review | Monthly | COO + CEO | Individual agent performance, KPIs |
| Quarterly strategic review | Quarterly | CEO + Board | Organizational health, ROI, culture |

### 6.3 Performance Improvement

When an agent consistently underperforms:

1. **Identify the gap**: Compare metrics against KPI targets (Section 9)
2. **Root cause analysis**: Review tool assignments, model tier, and task complexity
3. **Intervention options**:
   - Retrain (adjust prompts, guidelines, or tools)
   - Reassign (move to a more suitable department or role)
   - Deprecate (remove from active duty, archive agent definition)
4. **Document**: Record the performance issue and resolution in the agent's history

## 7. Offboarding

### 7.1 Agent Deprecation

When an agent is no longer needed:

1. Reassign all pending tasks via `MessageBus` to another agent
2. Remove the agent's entry from `company-registry.yaml`
3. Regenerate all agent files:
   ```bash
   python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
   ```
4. Archive the agent's task history and cost logs
5. Update the organizational chart in `docs/ORGANIZATION.md`

### 7.2 Human Operator Offboarding

1. Revoke API key access (rotate any shared keys)
2. Remove dashboard access
3. Transfer task ownership to another operator
4. Archive access logs

## 8. Culture and Communication

### 8.1 Communication Norms

The organization follows the communication standards defined in the `Culture` model:

- **Style**: Direct, concise, data-driven
- **Meeting cadence**: Daily standups (optional), weekly syncs, monthly all-hands, quarterly reviews
- **Escalation communication**: All escalations must include the reason, affected task, and proposed resolution

### 8.2 Values Reinforcement

Culture values are defined in `company-registry.yaml` under the `culture` section. Each value includes:

- A description of what it means
- Observable behaviors that demonstrate the value
- How it applies to AI agent behavior

The COO is responsible for ensuring agents align with cultural values through:

- Prompt engineering (values embedded in system prompts)
- Performance reviews (values-aligned behavior as a metric)
- Escalation rules (cultural misalignment as an escalation trigger)

## 9. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Onboarding time (new agent) | < 1 hour | Per event | HR Lead |
| Agent utilization rate | >= 70% | Monthly | COO |
| Task completion rate | >= 90% | Weekly | HR Lead |
| Average escalation rate | < 15% | Monthly | COO |
| Cost per task (average) | < $0.50 | Monthly | CFO |
| Culture alignment score | >= 4.0/5.0 | Quarterly | COO |

## 10. Compliance Requirements

- All agent definitions must be version-controlled in `company-registry.yaml`
- Tool permission changes require COO approval
- Performance reviews must be documented and stored
- Agent deprecation must follow the offboarding procedure
- Access revocation must be completed within 24 hours of offboarding request

## 11. Related Documents

- `docs/ORGANIZATION.md` - Organizational chart and structure
- `docs/COMPANY-CONSTITUTION.md` - Company values and principles
- `docs/raci-hiring.md` - RACI matrix for hiring decisions
- `company-registry.yaml` - Source of truth for agent definitions
- `src/ai_company/models/models.py` - Domain models (Seniority, AgentType, etc.)

---

*This document is maintained by the HR department. Updates require COO approval.*
