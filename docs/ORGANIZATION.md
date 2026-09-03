# AI Company Organization

## Structure

Light Speed Holdings is organized as a hierarchical AI company with one human CEO and 142 AI agents across 20 departments (143 registry entries in `company-registry.yaml`, including the human CEO).

```
                     human-ceo
                        │
                  chief-of-staff
        ┌───────┬───────┼────────┬────────┐
        │       │       │        │        │
       cto    coo      caio     cmo      cpo
        │       │       │        │        │
     (Tech)  (Ops)   (AI R&D)  (Mktg)  (Product)
        │
     consulting-lead   customer-success   hr   sales   cio   legal
```

Full org chart and per-department breakdown: `company/org-chart.md` and `docs/AGENT-REGISTRY-TABLE.md`.

## Roles

### Human CEO
The sole human in the hierarchy. Provides strategic direction, final approval authority, and oversight. All irreversible decisions ultimately flow here. Oversight body: the Board of Directors (7 board agents).

### Chief of Staff
Operational coordinator. Manages the daily flow of work across departments, generates executive briefings, and handles escalations that cross department boundaries. Acts with the CEO's authority on operational matters.

### CTO (Chief Technology Officer)
Owns engineering, data, and infrastructure. Responsible for technical architecture, security, deployment, and the agent execution system.

### CFO (Chief Financial Officer)
Owns finance. Responsible for budget allocation, cost tracking (including LLM token spend), and financial forecasting.

### COO (Chief Operating Officer)
Owns operations. Responsible for business process execution, workflows, and internal processes.

### CAIO (Chief AI Officer)
Owns AI research, model selection, and prompt engineering strategy.

### Executive Cabinet
The full executive layer (19 executives across 14 operating departments plus the Executive office): CEO, Chief of Staff, CEO Advisor, CTO, CFO, COO, CAIO, CMO, CPO, CSO, CISO, CDO, CIO, CLO, HR, Sales, Customer Success, Consulting, and the Legal Advisor. See `company-registry.yaml` for `reports_to` chains.

### Department Heads
Each department has an executive owner and one or more specialist agents. Department heads make decisions within their domain and escalate cross-department issues to the Chief of Staff.

### Specialists
Task-level executors. Each specialist has defined tools, permissions, and a narrow scope of responsibility. Specialists execute within their scope and escalate anything outside it.

## Departments

| Department | Executive | Example Specialists | Focus |
|-----------|-----------|---------------------|-------|
| Technology (27) | `cto` | `lead-backend`, `lead-frontend`, `devops-lead`, `software-architect` | Building and maintaining systems |
| AI Research (13) | `caio` | `ml-engineer`, `prompt-engineer`, `red-team-engineer`, `mlops-engineer` | Model strategy and research |
| Operations (11) | `coo` | `workflow-owner`, `orchestration-owner`, `capacity-planner`, `vendor-manager` | Business process execution |
| Security (11) | `ciso` | `security-architect`, `penetration-testing-lead`, `soc2-audit-readiness-analyst` | Security and hardening |
| Product (9) | `cpo` | `product-owner`, `product-designer`, `ux-research-lead` | Product vision and delivery |
| Marketing (9) | `cmo` | `content-creator`, `brand-strategist`, `growth-hacker` | Demand generation and brand |
| Board (7) | `board-chair` | `board-strategy`, `board-finance`, `board-technology` | Governance oversight |
| People (6) | `hr` | `hr-owner`, `recruiter`, `learning-development-lead` | Workforce and culture |
| Sales (6) | `sales` | `sales-owner`, `solutions-engineer`, `business-developer` | Revenue generation |
| Executive (5) | `human-ceo`, `chief-of-staff`, `ceo-advisor` | `internal-comms-lead`, `ai-ethics-board-chair` | CEO and coordination |
| Data (5) | `cdo` | `data-engineer`, `business-intelligence-engineer`, `data-scientist` | Data processing and analytics |
| Legal (5) | `clo`, `legal` | `legal-owner`, `data-privacy-officer`, `compliance-officer` | Contracts, compliance, risk |
| QA (5) | `qa-lead` (reports to `cto`) | `qa-engineer`, `test-engineering-lead`, `release-manager` | Quality assurance |
| Strategy (4) | `cso` | `market-analyst`, `head-of-competitive-intelligence` | Corporate strategy |
| Consulting (4) | `consulting-lead` | `opportunity-identifier`, `workflow-mapper`, `interview-agent` | Client consulting |
| Finance (3) | `cfo` | `financial-analyst`, `investor-relations-lead` | Financials and fundraising |
| Customer Success (3) | `customer-success` | `support-agent`, `customer-success-owner` | Customer retention and support |
| IT (1) | `cio` | — | IT infrastructure |
| Business Development (1) | `head-of-business-development` (reports to `chief-of-staff`) | — | Partnerships and growth |

Counts in parentheses are live registry headcounts; `docs/AGENT-REGISTRY-TABLE.md` is the generator-maintained reference that stays in sync.

## Decision Authority

| Decision Type | Authority Level | Example |
|--------------|----------------|---------|
| Task execution | Specialist (self) | Writing code, drafting content |
| Tool selection | Department Head | Choosing a library or framework |
| Budget allocation | CFO | Spending > $100 on services |
| Architecture changes | CTO + Chief of Staff | Changing data models, adding services |
| Hiring/firing agents | Human CEO | Adding or removing agents from the hierarchy |
| Security exceptions | Human CEO | Granting elevated permissions |

## Communication Patterns

- **Downward:** Tasks flow from CEO → Chief of Staff → Executives → Specialists
- **Upward:** Escalations flow from Specialists → Executives → Chief of Staff → CEO
- **Lateral:** Cross-department coordination goes through Chief of Staff, not direct agent-to-agent

## Adding New Agents

See `docs/raci-hiring.md` for the full RACI matrix. Summary:
1. Department head identifies the need
2. CTO reviews configuration for security
3. Lead Engineer generates agent files
4. Human Operator approves deployment
5. HR Agent updates roster
