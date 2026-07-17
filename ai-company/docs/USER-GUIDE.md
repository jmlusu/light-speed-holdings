# User Guide

Step-by-step guide to using AI Company Builder.

## Prerequisites

- Python 3.12+
- An LLM API key (at least one of: opencode, deepseek, openai, anthropic, or ollama running locally)

## 1. Install

```bash
cd ai-company
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
```

## 2. Bootstrap the Company

This generates all agent files, configs, and directory structure from the registry:

```bash
ai-company company run
```

Output:
- 27 agent markdown files in `.opencode/agents/`
- Config files in `.opencode/config/`
- Directory structure for memory, knowledge, projects

## 3. Configure LLM Providers

Set your API keys in a `.env` file at the repo root:

```
OPENCODE_API_KEY=your-key
DEEPSEEK_API_KEY=your-key
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

Or configure Ollama for local inference (no key needed).

Model routing is automatic — each agent gets assigned a provider and model based on its tier (fast/standard/premium). See `docs/MODEL-ROUTING-POLICY.md` for details.

## 4. Explore the Organization

```bash
# List all agents
ai-company agents list

# Filter by type
ai-company agents list --type specialist

# Filter by department
ai-company agents list --department engineering

# View company status
ai-company status
```

## 5. Run the Orchestrator

The orchestrator checks for due tasks, pending escalations, and approval requests:

```bash
ai-company orchestrator tick
```

This shows:
- Scheduled tasks that are due
- Unresolved escalations
- Pending approval requests

### Schedule Recurring Tasks

```bash
# List current schedules
ai-company orchestrator scheduler list

# Add a recurring task
ai-company orchestrator scheduler add daily-briefing --name "Daily Briefing" --interval 360
```

### View Escalations

```bash
# List escalation rules
ai-company orchestrator escalation list

# View pending escalations
ai-company orchestrator escalation pending
```

### Approve or Reject Requests

```bash
# List pending approvals
ai-company orchestrator approval pending

# Approve a request
ai-company orchestrator approval approve REQUEST_ID --approved-by human-operator

# Reject a request
ai-company orchestrator approval reject REQUEST_ID --rejected-by human-operator --notes "Not ready"
```

## 6. Execute Tasks

The executor picks up pending tasks and processes them using LLMs:

```bash
ai-company executor tick
```

For autonomous operation, the GitHub Action runs this every 6 hours automatically.

## 7. Use the Dashboard

Start the CEO dashboard (FastAPI web UI):

```bash
ai-company dashboard
```

Opens `http://localhost:8420` with:
- `/api/dashboard` — KPI summary
- `/api/agents` — All agents
- `/api/tasks` — Task queue
- `/api/approvals` — Pending approvals
- `/api/escalations` — Open escalations
- `/api/departments` — Department info
- `/api/models` — Model routing assignments

### View Department KPIs

```bash
# List all departments with KPIs
ai-company dashboard kpi list

# Show KPIs for a specific department
ai-company dashboard kpi show engineering
```

## 8. Add a New Agent

1. Edit `company/agent-registry.json` and add:

```json
{
  "id": "data-analyst",
  "name": "Data Analyst",
  "role": "Data Analyst",
  "type": "Specialist",
  "department": "engineering",
  "reportsTo": "lead-engineer",
  "tools": ["python", "sql", "pandas"],
  "permissions": ["read", "analyze"]
}
```

2. Regenerate:
```bash
ai-company generate
```

3. Verify:
```bash
ai-company agents list
```

## 9. Create a Postmortem

When an incident occurs:

```bash
# Create a postmortem
ai-company orchestrator postmortem create INC-001 --title "Service outage" --severity high

# View it
ai-company orchestrator postmortem show INC-001

# Update root cause
ai-company orchestrator postmortem update INC-001 --root-cause "Memory leak in worker" --status resolved

# Render to markdown
ai-company orchestrator postmortem render INC-001
```

## 10. View SOPs and RACIs

```bash
# List available SOPs
ai-company sop

# View a specific SOP
ai-company sop SOP-INCIDENT-001

# List RACI matrices
ai-company raci

# View a specific RACI
ai-company raci RACI-HIRING-001
```

## 11. Make a Decision

Use the decision engine to evaluate actions:

```bash
# Evaluate an action against the approval matrix
ai-company decision evaluate --action "deploy to production" --agent cto
```

## 12. Run Diagnostics

```bash
ai-company doctor
```

Runs system health checks on:
- Registry validity
- Config file presence
- Template availability
- Test suite status

## Common Workflows

### Daily Operations

```bash
ai-company orchestrator tick          # Check what needs attention
ai-company orchestrator briefing      # Generate daily briefing
ai-company dashboard kpi list         # Review department KPIs
```

### Deploy a New Agent

```bash
ai-company agents list                # Review current agents
# Edit company/agent-registry.json
ai-company generate                   # Regenerate files
pytest                                # Run tests
ai-company agents list                # Verify
```

### Incident Response

```bash
ai-company orchestrator escalation pending   # Check escalations
ai-company orchestrator postmortem create INC-XXX --title "..." --severity high
# Investigate and fix
ai-company orchestrator postmortem update INC-XXX --root-cause "..." --status resolved
ai-company orchestrator postmortem render INC-XXX
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Registry not found` | Run `ai-company company run` first |
| `ModuleNotFoundError` | Run `pip install -e ".[dev]"` |
| Dashboard won't start | Check port 8420 isn't in use: `netstat -ano | findstr 8420` |
| Tests fail | Run `pip install -e ".[dev]"` to ensure dev deps installed |
| Agent files not generated | Run `ai-company generate` |
