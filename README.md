# AI Company Builder

Python CLI for creating and orchestrating AI agent hierarchies. One human CEO supervises AI executives, managers, and specialists through a defined chain of command.

**Python 3.12+** | **Typer CLI** | **Pydantic models** | **FastAPI dashboard** | **WebSocket live updates**

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/light-speed-holdings/ai-company.git
uv sync --extra dev            # Creates .venv and installs project + dev deps from uv.lock

# Bootstrap the company from config (generates 144 agents)
uv run ai-company company run

# List all agents
uv run ai-company agents list

# Start the CEO dashboard (opens browser at localhost:8420)
uv run ai-company dashboard
```

### 30-Second Demo

```bash
uv run ai-company company run            # 1. Bootstrap the company
uv run ai-company agents list            # 2. See all 144 agents
uv run ai-company orchestrator tick      # 3. Check what needs attention
uv run ai-company dashboard              # 4. Open the live dashboard
```

---

## Features

### Core Capabilities

- **144 AI Agents** across 20 departments with defined reporting chains
- **30+ CLI Commands** covering orchestration, execution, memory, graphs, and more
- **5-Tier Approval System** with human-in-the-loop safety gates
- **Audit Trail** with JSONL writer, query/filter, and executor integration
- **Memory Engine** with 6 memory types (episodic, semantic, procedural, relational, temporal, aggregate)
- **Knowledge Graphs** with BFS pathfinding (org chart, decision, workflow, knowledge)
- **Workflow Engine** with 9 workflows, step tracking, and SLA monitoring
- **Data Layer** — `data/` package with task, memory, escalation, audit stores + KPI pipeline + cost analytics
- **ML Module** — `ml/` package with sentence-transformer embeddings (`EmbeddingEngine`)
- **Security Module** — `security/` package with secrets scanner, PII detector, content filter
- **FileStore** — `store/` package with atomic file I/O and platform-aware locking

### Dashboard and Monitoring

- **FastAPI REST API** with 20+ endpoints
- **WebSocket Support** for real-time KPI updates and alerts
- **Department KPIs** -- 25 KPIs in 8 KPI-enabled departments
- **LLM Streaming** with SSE/NDJSON parsing for OpenAI, Anthropic, Ollama
- **Analytics Layer** — history tracking, trend analysis, alert rules, summary rollups

### Safety and Governance

- **5-Tier Action Classification** (auto-approve, single approval, dual approval, executive approval, CEO approval)
- **Escalation Rules** with configurable timeouts and retry limits
- **Postmortem System** for incident tracking, root cause analysis, and prevention
- **SOPs and RACI Matrices** for operational governance
- **Model Routing** with 3 cost tiers (fast/standard/premium) and automatic fallback
- **Circuit Breaker** — LLM provider fail-fast after N errors
- **Dead-Letter Queue** — stale task detection and retry

### Operations

- **Autonomous Scheduling** via GitHub Actions (every 6 hours)
- **CI Pipeline** with lint, type check, test, and harness jobs
- **Release Infrastructure** with release.yml, release.ps1, and CHANGELOG.md
- **Docker Support** with health checks and volume mounts
- **Pre-commit Hooks** — ruff, mypy, bandit, trailing whitespace, YAML validation

---

## How It Works

```
                    human-ceo
                        |
                  chief-of-staff
                +-------+-------+
             cto      cfo      coo
              |        |        |
         +----+----+   |   +---+---+
      engineering  ... |  operations ...
         |             |        |
      specialists  specialists specialists
```

1. **Define** agents in `company-registry.yaml` (144 agents across 20 departments; synced to
`company/agent-registry.json`)
2. **Generate** OpenCode-compatible markdown files via Jinja2 templates
3. **Orchestrate** tasks through a scheduler, escalation rules, and approval gates
4. **Execute** tasks autonomously with LLM-based processing and human-in-the-loop safety
5. **Learn** from postmortems, memory, and decision records

---

## CLI Command Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `ai-company company run` | Bootstrap the full company from config |
| `ai-company generate` | Regenerate agent files from registry |
| `ai-company agents list` | List all registered agents |
| `ai-company status` | Show company status |
| `ai-company doctor` | Run system diagnostics |

### Orchestrator

| Command | Description |
|---------|-------------|
| `ai-company orchestrator tick` | Run one orchestrator cycle |
| `ai-company orchestrator briefing` | Generate daily executive briefing |
| `ai-company orchestrator scheduler list` | List scheduled tasks |
| `ai-company orchestrator escalation pending` | View open escalations |
| `ai-company orchestrator approval pending` | View pending approvals |
| `ai-company orchestrator postmortem list` | List incident postmortems |

### Execution and Dashboard

| Command | Description |
|---------|-------------|
| `ai-company executor tick` | Run one executor cycle |
| `ai-company executor start` | Start continuous execution loop |
| `ai-company dashboard` | Start the CEO dashboard (FastAPI) |
| `ai-company dashboard kpi list` | View department KPI definitions |

### Intelligence

| Command | Description |
|---------|-------------|
| `ai-company decision evaluate` | Evaluate an action through the decision engine |
| `ai-company decision matrix` | Show the approval matrix |
| `ai-company decision tree` | Navigate the decision tree |
| `ai-company graph list` | List knowledge graphs |
| `ai-company graph show org_chart` | View the organization chart |
| `ai-company memory list` | List memory entries |
| `ai-company memory search` | Search memory entries |
| `ai-company workflows list` | List available workflows |

### Department CLIs

```bash
ai-company marketing list-campaigns      # Marketing campaigns
ai-company sales list-leads              # Sales pipeline
ai-company hr list-agents                # Agent workforce roster
ai-company legal list-contracts          # Contract management
ai-company customer-success list-tickets # Support tickets
ai-company board list                    # Board of Directors
```

### Governance

```bash
ai-company sop                           # List Standard Operating Procedures
ai-company sop SOP-INCIDENT-001          # View a specific SOP
ai-company raci                          # List RACI matrices
ai-company raci RACI-HIRING-001          # View a specific RACI
```

See [docs/USER-GUIDE.md](docs/USER-GUIDE.md) for the complete command reference with examples.

---

## Configuration

All configuration lives in `company/`:

| File | Purpose |
|------|---------|
| `company-registry.yaml` | Single source of truth for all 144 agents |
| `company/agent-registry.json` | Generated registry (synced from `company-registry.yaml`) |
| `company/models.yaml` | LLM provider configuration (9 providers, 3 tiers) |
| `company/departments.yaml` | 20 departments with executives and agents |
| `company/config/kpis.yaml` | Department KPI definitions (25 KPIs) |

### Adding a New Agent

1. Add entry to `company-registry.yaml`:

```yaml
- id: data-analyst
  name: Data Analyst
  title: Data Analyst
  description: Analyzes data and builds reports for clients.
  type: specialist
  department: Data
  reports_to: cdo
  responsibilities:
    - Build client-facing analytics deliverables.
  guidelines: Deliver clean, reproducible analysis.
  tools: [read, edit, bash]
```

2. Sync + regenerate: `uv run ai-company sync-registry && uv run ai-company generate`
3. Verify: `uv run ai-company agents list`

### Model Routing

Three cost tiers with automatic fallback:

| Tier | Use Case | Providers |
|------|----------|-----------|
| `fast` | Simple tasks, drafts | opencode/big-pickle, gemini-3.5-flash, ollama/llama3.1 |
| `standard` | General work | opencode/big-pickle, gemini-3.5-flash, ollama, deepseek-chat, kimi-k2 |
| `premium` | Complex reasoning | opencode/big-pickle, gemini-3.1-pro, deepseek-coder, kimi-k2 |

Override per-agent in `company/models.yaml` under `routing`.

---

## Project Structure

```
ai-company/                     # Repository root
  src/ai_company/
    cli/                    # 30 Typer CLI commands (5 root + 25 sub-apps)
      main.py               # Entry point - registers all subcommands
      orchestrator.py       # Scheduler, escalation, approval, postmortem
      executor.py           # Autonomous task execution
      dashboard.py          # FastAPI dashboard + KPI views
    models/                 # 64 Pydantic models (Company, Agent, Task, etc.)
    registry/               # YAML config -> typed CompanyRegistry
    orchestrator/           # Scheduler, escalation, approval, briefing
    executor/               # LLM-based execution loop, HITL gates
    decision/               # Approval matrix, risk assessment, decision trees
    workflow/               # 9 workflows, step tracking, SLA monitoring
    memory/                 # 6 memory types with persistence
    graph/                  # Org chart, decision, workflow, knowledge graphs
    llm/                    # Multi-provider LLM client
    model_router.py         # 3-tier cost-aware model selection
    dashboard/              # FastAPI REST API + WebSocket
      api.py                # REST endpoints (20+ routes)
      ws.py                 # WebSocket handler
      models.py             # API response schemas
      kpis/                 # Department KPI collectors
    builder/                # Bootstrap engine - generates everything
  company/                  # Configuration YAMLs + generated registry
  templates/                # 9 Jinja2 templates
  tests/                    # 1856 unit + integration tests
  docs/                     # Architecture, governance, SOPs, user guide
  .github/workflows/        # CI + autonomous scheduling
  pyproject.toml            # Project metadata and dependencies
```

---

## Technical Architecture

The LightSpeed Holdings platform seamlessly combines a high-performance **React 18 + Vite** executive web application with **OpenCode automation standards** and a **Python 3.12+ Typer/FastAPI** backend orchestrator.

```
+-----------------------------------------------------------------------------------+
|                        PRESENTATION LAYER (React 18 + Vite)                       |
|  CorporateLanding | MissionControl | AgentRoster | TemplatesArtifacts | Spatial    |
+-----------------------------------------------------------------------------------+
                                        | REST API & WebSockets
+-----------------------------------------------------------------------------------+
|                     API & ORCHESTRATION LAYER (FastAPI & CLI)                     |
|  FastAPI Server (Port 8420) | WebSocket Telemetry | Typer CLI (ai-company)        |
+-----------------------------------------------------------------------------------+
                                        | OpenCode Engine
+-----------------------------------------------------------------------------------+
|                    OPENCODE AGENT RUNTIME & GOVERNANCE                            |
|  .opencode/agents/*.md | company-registry.yaml | Canonical 7-Tool Permission Gate |
+-----------------------------------------------------------------------------------+
                                        | Storage & Persistence
+-----------------------------------------------------------------------------------+
|                   DATA, MEMORY & EXECUTION INFRASTRUCTURE                         |
|  .opencode/inbox.json | JSONL Audit Logs | Memory Engine | Knowledge Graphs      |
+-----------------------------------------------------------------------------------+
```

### Integration with OpenCode Automation Standards

1. **OpenCode Agent Cards (`.opencode/agents/*.md`)**:
   - The React frontend (`src/components/AgentRoster.tsx`, `AgentModal.tsx`) visualizes OpenCode agent specifications generated from `company-registry.yaml` via Jinja2 templates (`templates/agents/agent.md.j2`).
   - Every agent is defined with OpenCode-native attributes (`mode: subagent`, `description`, `reports_to`, and granular permission blocks).

2. **Canonical 7-Tool Permission Vocabulary**:
   - Both the Python execution engine (`src/ai_company/executor/`) and the React UI enforce OpenCode's strict 7-tool permission boundaries:
     `read`, `edit`, `grep`, `list`, `bash`, `webfetch`, `task`.
   - Legacy tool aliases (`write` -> `edit`, `execute` -> `bash`, `delegate` -> `task`) are transparently normalized by the runtime.

3. **Task Queue & Inbox Synchronization**:
   - The task management board (`src/components/TaskKanban.tsx`, `TaskModal.tsx`) displays and manages tasks structured according to OpenCode's JSON task schema (`.opencode/inbox.json`).
   - Tasks progress through deterministic states (`PENDING`, `IN_PROGRESS`, `AWAITING_APPROVAL`, `COMPLETED`, `FAILED`).

4. **Human-in-the-Loop (HITL) Fiduciary Controls**:
   - The approvals management interface (`src/components/ApprovalsEscalations.tsx`) connects to OpenCode's 5-Tier decision matrix (`ApprovalGate`, `.opencode/pending_approvals.json`).
   - High-value operations or sensitive data actions require explicit cryptographic human sign-off before executing.

5. **Templates & Deliverables (`src/components/TemplatesArtifacts.tsx`)**:
   - Displays production-grade OpenCode agent YAML cards, SADC trade compliance frameworks, Policy-as-Code schemas, and DAG execution flows.
   - Developers and automation tools can ingest these templates directly into OpenCode CLI environments.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete technical specifications.

---

## Development Guide

### Prerequisites

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Python**: 3.12 or higher
- **uv**: Fast Python package installer and virtual environment manager (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)

---

### 1. Web Application Setup (React + Vite)

The web user interface is built with React 18, Vite, and Tailwind CSS.

#### Installation & Startup

```bash
# Install Node dependencies
npm install

# Start Vite development server (runs on port 3000)
npm run dev

# Build production static assets (outputs to dist/)
npm run build

# Run TypeScript type checker
npm run lint
```

#### Key React Scripts
| Script | Command | Purpose |
|--------|---------|---------|
| `dev` | `vite` | Starts dev server on `http://localhost:3000` |
| `build` | `tsc && vite build` | Compiles TypeScript and builds production distribution |
| `lint` | `tsc --noEmit` | Validates TypeScript type safety with zero code generation |
| `preview` | `vite preview` | Serves production build locally for verification |

---

### 2. Python Backend & Orchestrator Setup

The backend CLI, orchestrator engine, and FastAPI server are powered by Python 3.12.

#### Installation & Quick Start

```bash
# Create virtual environment (.venv) and install dependencies
uv sync --extra dev

# Bootstrap the 144 AI agents from company-registry.yaml
uv run ai-company company run

# Verify registered agents
uv run ai-company agents list

# Launch the FastAPI REST & WebSocket server (runs on localhost:8420)
uv run ai-company dashboard
```

#### CLI Command Reference
```bash
uv run ai-company orchestrator tick     # Run one orchestrator task cycle
uv run ai-company executor tick         # Run one execution cycle
uv run ai-company status                # View company health status
uv run ai-company doctor                # Run system diagnostics
```

---

### 3. Testing & Code Quality Verification

All source changes must pass linting, type checking, and unit/integration tests before deployment.

#### Python Checks & Tests
```bash
uv run ruff check src/                   # Lint Python source code
uv run ruff format src/                  # Format Python files
uv run mypy src/                         # Run mypy static type checking
uv run pytest                            # Run complete test suite (1856+ tests)
uv run pytest --cov=ai_company          # Run tests with coverage reporting
```

#### Convenience Makefile Targets
```bash
make help              # Show all available targets
make install           # Run uv sync --extra dev
make test              # Run pytest suite
make test-cov          # Run pytest with coverage
make lint              # Run ruff linter
make format            # Format with ruff
make typecheck         # Run mypy type checker
make all-checks        # Execute lint + typecheck + pytest
make generate          # Regenerate agent files from registry
make doctor            # Run system diagnostics
make clean             # Remove caches and build artifacts
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [User Guide](docs/USER-GUIDE.md) | Complete CLI reference, workflows, troubleshooting |
| [API Reference](docs/API-REFERENCE.md) | REST API endpoints, WebSocket protocol, data models |
| [Deployment Guide](docs/DEPLOYMENT-GUIDE.md) | Local, Docker, and production deployment |
| [Architecture](docs/ARCHITECTURE.md) | System architecture and module hierarchy |
| [Risk Register](docs/RISK-REGISTER.md) | 10 identified risks with mitigations |
| [Board Governance](docs/BOARD-GOVERNANCE.md) | Board charter, meeting cadence, voting |
| [Model Routing Policy](docs/MODEL-ROUTING-POLICY.md) | Provider tiers, fallback, cost control |
| [Incident Response SOP](docs/sop-incident-response.md) | Detection, triage, resolve, learn |
| [Deployment SOP](docs/sop-deployment.md) | Prepare, validate, generate, deploy |
| [Hiring RACI](docs/raci-hiring.md) | Responsibility matrix for adding agents |
| [Constitution](docs/COMPANY-CONSTITUTION.md) | Principles and decision order |
| [Decision Framework](docs/DECISION-FRAMEWORK.md) | 10-step decision template |

---

## Milestones Presentation

A comprehensive PowerPoint presentation showcasing all major milestones is available:

```bash
# Generate the milestones deck (Node.js)
npm install
node scripts/generate-milestones-deck.js

# Or using Python
uv sync --extra dev
uv run python scripts/generate-milestones-deck.py
```

The presentation includes 15 slides covering:
- Executive summary with key metrics
- Project timeline visualization
- All 8 major milestones
- Quality metrics and architecture overview
- Remaining work and next steps

See [README-milestones-deck.md](README-milestones-deck.md) for detailed instructions and [MILESTONES-DECK-SETUP.md](MILESTONES-DECK-SETUP.md) for a complete setup summary.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, code style, and submission guidelines.

### Quick Contribution Workflow

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USER/ai-company.git

# 2. Set up development environment
uv sync --extra dev

# 3. Create a feature branch
git checkout -b feat/my-feature

# 4. Make changes and verify
uv run ruff check src/
uv run mypy src/
uv run pytest

# 5. Commit and push
git commit -m "feat: add my feature"
git push origin feat/my-feature

# 6. Open a Pull Request
```

---

## Author

**Jack Mlusu** -- Light Speed Holdings
