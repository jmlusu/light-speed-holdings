# User Guide

Complete reference for AI Company Builder — the Python CLI tool for creating and orchestrating AI agent hierarchies.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Agent Hierarchy](#2-agent-hierarchy)
3. [CLI Command Reference](#3-cli-command-reference)
4. [Task Management](#4-task-management)
5. [Dashboard Usage](#5-dashboard-usage)
6. [Configuration Reference](#6-configuration-reference)
7. [Common Workflows](#7-common-workflows)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Getting Started

### Prerequisites

- **Python 3.12+**
- **An LLM API key** (at least one of: OpenCode, DeepSeek, OpenAI, Anthropic, or Ollama running locally)
- **Operating System**: Windows, macOS, or Linux

### Installation

```bash
cd ai-company
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# Install in development mode
pip install -e ".[dev]"
```

### Bootstrap the Company

The bootstrap command reads your configuration files and generates all agent files, directory structures, and config outputs:

```bash
ai-company company run
```

**Output:**
- 27 agent markdown files in `.opencode/agents/`
- Config files in `.opencode/config/`
- Directory structure for memory, knowledge, projects
- Task inbox at `.opencode/inbox.json`

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--config-dir` | `config` | Path to config directory |
| `--output-dir` | `.opencode` | Output directory for generated files |
| `--dry-run` | `false` | Show what would be created without writing |

### Configure LLM Providers

Set your API keys in a `.env` file at the repo root:

```bash
OPENCODE_API_KEY=your-key
DEEPSEEK_API_KEY=your-key
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

Or configure Ollama for local inference (no API key needed). Model routing is automatic — each agent gets assigned a provider and model based on its cost tier (fast/standard/premium). See [Model Routing Policy](MODEL-ROUTING-POLICY.md) for details.

---

## 2. Agent Hierarchy

AI Company Builder uses a corporate hierarchy model where one human CEO supervises AI executives, managers, and specialists:

```
                    human-ceo
                        │
                  chief-of-staff
                ┌───────┼───────┐
             cto      cfo      coo
              │        │        │
         ┌────┴────┐   │   ┌───┴───┐
      engineering  ... │  operations ...
         │             │        │
      specialists  specialists specialists
```

### Agent Types

| Type | Description | Examples |
|------|-------------|----------|
| **Executive** | C-suite leaders with decision authority | CTO, CFO, COO, CMO |
| **Board** | Board of directors with governance oversight | Chairman, Independent Director |
| **Specialist** | Department-level workers with specific skills | Backend Engineer, Data Analyst |

### Agent Registration

All 27 agents are defined in `company/agent-registry.json`. Each entry contains:

```json
{
  "id": "lead-engineer",
  "name": "Lead Engineer",
  "role": "Lead Engineer",
  "type": "Specialist",
  "department": "engineering",
  "reportsTo": "cto",
  "tools": ["python", "git", "docker"],
  "permissions": ["read", "edit", "bash"]
}
```

### Adding a New Agent

1. Edit `company/agent-registry.json` and add a new entry
2. Regenerate agent files: `ai-company generate`
3. Verify: `ai-company agents list`

### Model Routing

Three cost tiers with automatic fallback:

| Tier | Use Case | Providers |
|------|----------|-----------|
| `fast` | Simple tasks, drafts | deepseek-chat, ollama/llama3 |
| `standard` | General work | opencode/big-pickle, gpt-4o-mini |
| `premium` | Complex reasoning | opencode/big-pickle, claude-sonnet |

Override per-agent in `company/models.yaml` under `agent_overrides`.

---

## 3. CLI Command Reference

All commands are accessed via the `ai-company` CLI entry point.

### Core Commands

#### `ai-company company run`

Bootstrap the full company from configuration files.

```bash
ai-company company run
ai-company company run --dry-run           # Preview without writing
ai-company company run --config-dir config  # Custom config path
```

#### `ai-company generate`

Regenerate all agent files from the registry.

```bash
ai-company generate
ai-company generate --registry company/agent-registry.json
```

#### `ai-company status`

Show current company status.

```bash
ai-company status
```

#### `ai-company doctor`

Run system diagnostics.

```bash
ai-company doctor           # Run diagnostics
ai-company doctor run       # Same as above
ai-company doctor check     # Run checks
ai-company doctor fix       # Auto-fix detected issues
```

The doctor checks:
- Registry validity and completeness
- Config file presence
- Template availability
- Generated agent files
- Task inbox integrity

### Agent Management

#### `ai-company agents`

Manage AI agents.

```bash
ai-company agents list                              # List all agents
ai-company agents list --type specialist             # Filter by type
ai-company agents list --department engineering      # Filter by department
```

### Orchestrator Commands

#### `ai-company orchestrator tick`

Run one orchestrator cycle — checks due tasks, pending escalations, and approval requests.

```bash
ai-company orchestrator tick
```

#### `ai-company orchestrator briefing`

Generate a daily executive briefing from the inbox and registry.

```bash
ai-company orchestrator briefing
```

#### Scheduler Subcommands

Manage recurring task schedules.

```bash
# List all scheduled tasks
ai-company orchestrator scheduler list

# Add a recurring task
ai-company orchestrator scheduler add daily-briefing \
  --name "Daily Briefing" \
  --interval 360

# Remove a scheduled task
ai-company orchestrator scheduler remove daily-briefing
```

#### Escalation Subcommands

Manage escalation rules and view pending escalations.

```bash
# List escalation rules
ai-company orchestrator escalation list

# Add an escalation rule
ai-company orchestrator escalation add timeout-rule \
  --name "Timeout Escalation" \
  --trigger "task_timeout" \
  --escalate-to chief-of-staff \
  --max-retries 3 \
  --timeout 30

# Remove an escalation rule
ai-company orchestrator escalation remove timeout-rule

# View unresolved escalations
ai-company orchestrator escalation pending
```

#### Approval Subcommands

Manage human-in-the-loop approval gates.

```bash
# List pending approvals
ai-company orchestrator approval pending

# Approve a request
ai-company orchestrator approval approve REQUEST_ID \
  --approved-by human-operator \
  --notes "Looks good"

# Reject a request
ai-company orchestrator approval reject REQUEST_ID \
  --rejected-by human-operator \
  --notes "Not ready yet"
```

#### Postmortem Subcommands

Manage incident postmortems for learning and prevention.

```bash
# List all postmortems
ai-company orchestrator postmortem list

# Create a new postmortem
ai-company orchestrator postmortem create INC-001 \
  --title "Service outage" \
  --severity high \
  --affected-agent lead-engineer \
  --department engineering

# View a specific postmortem
ai-company orchestrator postmortem show INC-001

# Update a postmortem
ai-company orchestrator postmortem update INC-001 \
  --root-cause "Memory leak in worker process" \
  --status resolved \
  --reviewed-by human-ceo

# Render to markdown
ai-company orchestrator postmortem render INC-001
```

### Executor Commands

#### `ai-company executor`

Autonomous task execution loop.

```bash
# Run one executor cycle (process all pending tasks)
ai-company executor tick

# Start continuous execution loop
ai-company executor start --poll-interval 5.0

# Execute a specific task by ID
ai-company executor run-task TASK_ID

# Show executor status and pending tasks
ai-company executor status
```

### Decision Engine

#### `ai-company decision`

Evaluate actions through the approval matrix, risk assessment, and decision trees.

```bash
# Evaluate an action
ai-company decision evaluate "deploy to production"

# Show the approval matrix
ai-company decision matrix

# Navigate the decision tree
ai-company decision tree --start root
```

### Graph Engine

#### `ai-company graph`

Query knowledge graphs — org chart, decision graph, workflow graph, knowledge graph.

```bash
# List all available graphs
ai-company graph list

# Show a specific graph's nodes and edges
ai-company graph show org_chart

# Find a path between two agents
ai-company graph path org_chart --start human-ceo --end lead-engineer
```

### Memory Engine

#### `ai-company memory`

Manage the 6-type memory store (episodic, semantic, procedural, relational, temporal, aggregate).

```bash
# List all memory entries (summary view)
ai-company memory list

# List specific memory type
ai-company memory list --memory-type episodic

# Add a memory entry
ai-company memory add \
  --memory-type semantic \
  --content "The CTO prefers Python over Go for new services" \
  --agent-id human-ceo \
  --tags "preference,tech-stack"

# Search memories
ai-company memory search --query "python" --limit 10
ai-company memory search --memory-type episodic --tags "incident"

# Consolidate a memory type into aggregate summary
ai-company memory consolidate semantic
```

### Workflow Engine

#### `ai-company workflows`

Manage and track workflow definitions.

```bash
# List all workflows
ai-company workflows list
```

### Dashboard

#### `ai-company dashboard`

Start the CEO dashboard web server.

```bash
ai-company dashboard                              # Start on port 8420
ai-company dashboard --port 9000                   # Custom port
ai-company dashboard --host 0.0.0.0                # Bind to all interfaces
ai-company dashboard --no-open                     # Don't auto-open browser
```

#### KPI Dashboard

```bash
ai-company dashboard kpi list                      # List all departments with KPIs
ai-company dashboard kpi show engineering           # Show KPIs for a department
```

### Department CLIs

Each department has its own set of commands:

```bash
# Marketing
ai-company marketing list-campaigns               # List campaigns
ai-company marketing create-campaign CAMPAIGN_ID --name "Q3 Push" --channel email
ai-company marketing launch CAMPAIGN_ID           # Launch a campaign
ai-company marketing metrics CAMPAIGN_ID          # View campaign metrics

# Sales
ai-company sales list-leads                       # List sales pipeline

# HR
ai-company hr list-agents                         # Agent workforce roster

# Legal
ai-company legal list-contracts                   # Contract management

# Customer Success
ai-company customer-success list-tickets          # Support tickets

# Board
ai-company board list                             # Board of Directors
```

### Governance Commands

#### `ai-company sop`

View Standard Operating Procedures.

```bash
ai-company sop                                    # List all SOPs
ai-company sop SOP-INCIDENT-001                   # View a specific SOP
```

#### `ai-company raci`

View RACI responsibility matrices.

```bash
ai-company raci                                   # List all RACI matrices
ai-company raci RACI-HIRING-001                   # View a specific RACI
```

---

## 4. Task Management

### Task Lifecycle

Tasks flow through the system via the JSON-based task queue at `.opencode/inbox.json`:

```
pending → in_progress → completed
         ↘ blocked
         ↘ failed
         ↘ escalated
         ↘ cancelled
```

### Creating Tasks via API

```bash
curl -X POST http://localhost:8420/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_id": "lead-engineer",
    "instruction": "Review PR #42 for the authentication module",
    "priority": "high",
    "sender_id": "human-ceo"
  }'
```

### Task Priorities

| Priority | Description |
|----------|-------------|
| `low` | Can wait, non-urgent |
| `medium` | Normal work items |
| `high` | Time-sensitive, should be handled soon |
| `critical` | Urgent, requires immediate attention |

### Task Execution

The executor processes tasks in a single pass:

```bash
ai-company executor tick
```

For continuous autonomous execution:

```bash
ai-company executor start --poll-interval 5.0
```

### Human-in-the-Loop (HITL)

Tasks requiring approval are routed through the approval gate:

1. Agent submits an action requiring approval
2. Approval request appears in `orchestrator/approvals.yaml`
3. Human approves/rejects via CLI or dashboard
4. Executor continues or aborts based on decision

---

## 5. Dashboard Usage

### Starting the Dashboard

```bash
ai-company dashboard
```

Opens `http://localhost:8420` in your browser with the CEO dashboard.

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/dashboard` | GET | KPI summary (tasks, approvals, escalations, agents) |
| `/api/kpis/live` | GET | Live KPI values from department collectors |
| `/api/agents` | GET | List all agents |
| `/api/agents/{name}` | GET | Get specific agent details |
| `/api/org-chart` | GET | Organization chart (nested tree) |
| `/api/tasks` | GET | List tasks (filterable by status, agent) |
| `/api/tasks` | POST | Create a new task |
| `/api/approvals` | GET | List pending approval requests |
| `/api/approvals/{id}/approve` | POST | Approve a request |
| `/api/approvals/{id}/reject` | POST | Reject a request |
| `/api/escalations` | GET | List open escalations |
| `/api/escalations/{id}/resolve` | POST | Resolve an escalation |
| `/api/departments` | GET | List all departments |
| `/api/departments/{name}/kpis` | GET | KPIs for a specific department |
| `/api/kpis` | GET | All department KPI definitions |
| `/api/kpis/summary` | GET | Flat summary of all KPIs |
| `/api/models` | GET | Model routing assignments |
| `/api/models/tiers` | GET | Available model tiers |
| `/api/scheduler` | GET | List scheduled tasks |

### WebSocket Protocol

Connect to `ws://localhost:8420/ws/dashboard` for live updates:

**Client → Server messages:**
```json
{"type": "ping"}
{"type": "subscribe", "topics": ["kpis", "alerts"]}
```

**Server → Client messages:**
```json
{"type": "connected", "timestamp": "...", "active_clients": 1}
{"type": "kpi_update", "timestamp": "...", "payload": {...}}
{"type": "alert", "timestamp": "...", "payload": {"category": "approval", ...}}
{"type": "pong", "timestamp": "..."}
```

### Quick Dashboard Access via cURL

```bash
# Get KPI summary
curl http://localhost:8420/api/dashboard

# List all agents
curl http://localhost:8420/api/agents

# Get org chart
curl http://localhost:8420/api/org-chart

# Create a task
curl -X POST http://localhost:8420/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"receiver_id": "cto", "instruction": "Plan Q3 tech roadmap"}'

# Approve a request
curl -X POST http://localhost:8420/api/approvals/REQ-001/approve \
  -H "Content-Type: application/json" \
  -d '{"approved_by": "human-ceo", "notes": "Approved"}'
```

---

## 6. Configuration Reference

All configuration lives in the `company/` directory.

### Configuration Files

| File | Purpose |
|------|---------|
| `company/agent-registry.json` | Single source of truth for all 27 agents |
| `company/models.yaml` | LLM provider configuration (5 providers, 3 tiers) |
| `company/departments.yaml` | 7 departments with executives and agents |
| `company/workflows.yaml` | 9 workflow definitions |
| `company/config/kpis.yaml` | Department KPI definitions (28 KPIs across 7 departments) |

### Agent Registry Schema

Each agent in `company/agent-registry.json`:

```json
{
  "id": "unique-slug",
  "name": "Human Readable Name",
  "role": "Job Title",
  "type": "Executive | Board | Specialist",
  "department": "engineering",
  "reportsTo": "parent-agent-id",
  "tools": ["tool1", "tool2"],
  "permissions": ["read", "edit", "bash"]
}
```

### Models Configuration

`company/models.yaml` defines LLM providers and routing:

```yaml
tiers:
  fast:
    description: "Simple tasks, drafts"
    providers:
      - provider: deepseek
        model: deepseek-chat
      - provider: ollama
        model: llama3
  standard:
    description: "General work"
    providers:
      - provider: opencode
        model: big-pickle
      - provider: openai
        model: gpt-4o-mini
  premium:
    description: "Complex reasoning"
    providers:
      - provider: opencode
        model: big-pickle
      - provider: anthropic
        model: claude-sonnet

agent_overrides:
  lead-engineer: premium
  cto: premium
  content-writer: standard
```

### Department Configuration

`company/departments.yaml`:

```yaml
departments:
  - name: engineering
    executive: cto
    agents:
      - lead-engineer
      - backend-engineer
      - frontend-engineer
  - name: marketing
    executive: cmo
    agents:
      - content-writer
      - growth-marketer
  # ... more departments
```

### KPI Configuration

`company/config/kpis.yaml` defines department-level KPIs:

```yaml
departments:
  engineering:
    name: Engineering
    kpis:
      - id: eng-deploy-freq
        name: Deployment Frequency
        target: 10
        unit: "per week"
        frequency: weekly
      - id: eng-cycle-time
        name: Cycle Time
        target: 2
        unit: "days"
        frequency: weekly
  # ... 7 departments, 28 KPIs total
```

---

## 7. Common Workflows

### Daily Operations

```bash
ai-company orchestrator tick          # Check what needs attention
ai-company orchestrator briefing      # Generate daily briefing
ai-company dashboard kpi list         # Review department KPIs
```

### Deploy a New Agent

```bash
ai-company agents list                         # Review current agents
# Edit company/agent-registry.json
ai-company generate                            # Regenerate files
pytest                                         # Run tests
ai-company agents list                         # Verify
```

### Incident Response

```bash
ai-company orchestrator escalation pending                    # Check escalations
ai-company orchestrator postmortem create INC-XXX \
  --title "Service outage" \
  --severity high
# Investigate and fix
ai-company orchestrator postmortem update INC-XXX \
  --root-cause "Memory leak in worker" \
  --status resolved
ai-company orchestrator postmortem render INC-XXX             # Generate report
```

### Review System Health

```bash
ai-company doctor run       # Full diagnostics
ai-company doctor fix       # Auto-fix issues
```

### Evaluate an Action

```bash
ai-company decision evaluate "deploy to production"
ai-company decision matrix        # See all approval requirements
ai-company decision tree          # Navigate decision logic
```

### Knowledge Graph Exploration

```bash
ai-company graph list                                        # Available graphs
ai-company graph show org_chart                              # View org structure
ai-company graph path org_chart --start human-ceo --end cto  # Find reporting path
```

### Memory Management

```bash
ai-company memory list                                              # Overview
ai-company memory search --query "architecture" --limit 5           # Search
ai-company memory add --memory-type semantic \
  --content "Microservices preferred over monolith" \
  --tags "architecture,preference"
ai-company memory consolidate semantic                              # Consolidate
```

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `Registry not found` | Run `ai-company company run` first |
| `ModuleNotFoundError` | Run `pip install -e ".[dev]"` |
| Dashboard won't start | Check port 8420 isn't in use: `netstat -ano \| findstr 8420` |
| Tests fail | Run `pip install -e ".[dev]"` to ensure dev deps installed |
| Agent files not generated | Run `ai-company generate` |
| `Company directory not found` | Run `ai-company company run` to bootstrap |
| Memory entries not found | Run `ai-company memory add` to create entries first |
| Postmortem already exists | Use a different incident ID or delete the existing one |
| KPI config not found | Ensure `company/config/kpis.yaml` exists |
| WebSocket connection refused | Ensure dashboard is running: `ai-company dashboard` |

### Getting Help

```bash
ai-company --help                    # General help
ai-company <command> --help          # Command-specific help
ai-company <command> <subcommand> --help  # Subcommand help
```

### Logs

The dashboard logs to stdout when running. For debugging, check:
- `orchestrator/approvals.yaml` — pending approval requests
- `orchestrator/escalation.yaml` — escalation events
- `orchestrator/scheduler.yaml` — scheduled task definitions
- `.opencode/inbox.json` — task queue
- `orchestrator/postmortems/` — incident postmortem records
