# AI Company Builder

Python CLI for creating and orchestrating AI agent hierarchies. One human CEO supervises AI executives, managers, and specialists through a defined chain of command.

**Python 3.12+** | **Typer CLI** | **Pydantic models** | **Jinja2 templates**

## Quick Start

```bash
cd ai-company
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"

# Bootstrap the company from config
ai-company company run

# List all agents
ai-company agents list

# Run orchestrator tick
ai-company orchestrator tick
```

## How It Works

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

1. **Define** agents in `company/agent-registry.json` (27 agents across 7 departments)
2. **Generate** OpenCode-compatible markdown files via Jinja2 templates
3. **Orchestrate** tasks through a scheduler, escalation rules, and approval gates
4. **Execute** tasks autonomously with LLM-based processing and human-in-the-loop safety
5. **Learn** from postmortems, memory, and decision records

## CLI Commands

| Command | Description |
|---------|-------------|
| `ai-company company run` | Bootstrap the full company from config |
| `ai-company generate` | Regenerate agent files from registry |
| `ai-company agents list` | List all registered agents |
| `ai-company status` | Show company status |
| `ai-company orchestrator tick` | Run one orchestrator cycle |
| `ai-company orchestrator briefing` | Generate daily executive briefing |
| `ai-company orchestrator scheduler list` | List scheduled tasks |
| `ai-company orchestrator escalation pending` | View open escalations |
| `ai-company orchestrator postmortem list` | List incident postmortems |
| `ai-company executor tick` | Run one executor cycle |
| `ai-company dashboard` | Start the CEO dashboard (FastAPI) |
| `ai-company dashboard kpi list` | View department KPI definitions |
| `ai-company doctor` | Run system diagnostics |
| `ai-company sop` | List Standard Operating Procedures |
| `ai-company raci` | List RACI matrices |
| `ai-company decision evaluate` | Evaluate an action through the decision engine |
| `ai-company graph list` | List knowledge graphs |
| `ai-company memory list` | List memory entries |
| `ai-company workflows list` | List available workflows |

### Department CLIs

```bash
ai-company marketing list-campaigns     # Marketing campaigns
ai-company sales list-leads             # Sales pipeline
ai-company hr list-agents               # Agent workforce roster
ai-company legal list-contracts         # Contract management
ai-company customer-success list-tickets # Support tickets
ai-company board list                   # Board of Directors
```

## Configuration

All configuration lives in `company/`:

| File | Purpose |
|------|---------|
| `company/agent-registry.json` | Single source of truth for all 27 agents |
| `company/models.yaml` | LLM provider configuration (5 providers, 3 tiers) |
| `company/departments.yaml` | 7 departments with executives and agents |
| `company/workflows.yaml` | 9 workflow definitions |
| `company/config/kpis.yaml` | Department KPI definitions (28 KPIs) |

### Adding a New Agent

1. Add entry to `company/agent-registry.json`:

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

2. Regenerate: `ai-company generate`

### Model Routing

Three cost tiers with automatic fallback:

| Tier | Use Case | Providers |
|------|----------|-----------|
| `fast` | Simple tasks, drafts | deepseek-chat, ollama/llama3 |
| `standard` | General work | opencode/big-pickle, gpt-4o-mini |
| `premium` | Complex reasoning | opencode/big-pickle, claude-sonnet |

Override per-agent in `company/models.yaml` under `agent_overrides`.

## Project Structure

```
ai-company/
├── src/ai_company/
│   ├── cli/                    # 20 Typer CLI subcommands
│   │   ├── main.py             # Entry point — registers all subcommands
│   │   ├── orchestrator.py     # Scheduler, escalation, approval, postmortem
│   │   ├── executor.py         # Autonomous task execution
│   │   └── dashboard.py        # FastAPI dashboard + KPI views
│   ├── models/                 # 57 Pydantic models (Company, Agent, Task, etc.)
│   ├── registry/               # YAML config → typed CompanyRegistry
│   ├── orchestrator/           # Scheduler, escalation, approval, briefing
│   ├── executor/               # LLM-based execution loop, HITL gates
│   ├── decision/               # Approval matrix, risk assessment, decision trees
│   ├── workflow/               # 9 workflows, step tracking, SLA monitoring
│   ├── memory/                 # 6 memory types with persistence
│   ├── graph/                  # Org chart, decision, workflow, knowledge graphs
│   ├── llm/                    # Multi-provider LLM client
│   ├── model_router.py        # 3-tier cost-aware model selection
│   ├── dashboard/              # FastAPI REST API
│   └── builder.py             # Bootstrap engine — generates everything
├── company/                    # Configuration YAMLs
├── templates/                  # 14 Jinja2 templates
├── tests/                      # 183 unit tests
├── docs/                       # Architecture, governance, SOPs
├── .github/workflows/          # CI + autonomous scheduling
└── pyproject.toml              # Project metadata and dependencies
```

## Development

```bash
cd ai-company
pip install -e ".[dev]"

# Run all checks
ruff check src/                # Lint
black src/                     # Format
mypy src/                      # Type check
pytest                         # Tests
```

### Useful Commands

```bash
# Regenerate agents from registry
ai-company generate

# Run full health check
ai-company doctor

# View a specific SOP
ai-company sop SOP-INCIDENT-001

# View a RACI matrix
ai-company raci RACI-HIRING-001
```

## Testing

```bash
pytest                         # All 183 tests
pytest tests/unit/test_orchestrator.py  # Single file
pytest -v                      # Verbose output
pytest -k "postmortem"         # By name pattern
```

Tests cover: models, registry, orchestrator (scheduler, escalation, approval, postmortem), executor, dashboard API, memory, graphs, workflows, decision engine, model routing, and generation.

## Governance

| Document | Description |
|----------|-------------|
| [Risk Register](docs/RISK-REGISTER.md) | 10 identified risks with mitigations |
| [Board Governance](docs/BOARD-GOVERNANCE.md) | Board charter, meeting cadence, voting |
| [Model Routing Policy](docs/MODEL-ROUTING-POLICY.md) | Provider tiers, fallback, cost control |
| [Incident Response SOP](docs/sop-incident-response.md) | Detection → triage → resolve → learn |
| [Deployment SOP](docs/sop-deployment.md) | Prepare → validate → generate → deploy |
| [Hiring RACI](docs/raci-hiring.md) | Responsibility matrix for adding agents |
| [Constitution](docs/COMPANY-CONSTITUTION.md) | Principles and decision order |
| [Decision Framework](docs/DECISION-FRAMEWORK.md) | 10-step decision template |

## Architecture

- **Entry point:** `ai_company.cli.main:app` (Typer)
- **Task queue:** `.opencode/inbox.json` (JSON-backed)
- **Agent files:** `.opencode/agents/*.md` (OpenCode format)
- **Dashboard:** FastAPI at `localhost:8420` (auto-opens browser)
- **Autonomous:** GitHub Action runs orchestrator + executor every 6 hours

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.

## Author

**Jack Mlusu** — Light Speed Holdings
