# AI Company Organization

## Structure

Light Speed Holdings is organized as a hierarchical AI company with 90 agents (one human CEO + 89 AI agents) across 20 departments.

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
The executive layer in `company-registry.yaml` (executives + department heads with `reports_to` chains): CEO, Chief of Staff, CEO Advisor, CTO, CFO, COO, CAIO, CMO, CPO, CSO, CISO, CDO, CIO, CLO, HR, Sales, Customer Success, Consulting, and the Legal Advisor. See `company-registry.yaml` for exact membership.

### Department Heads
Each department has an executive owner and one or more specialist agents. Department heads make decisions within their domain and escalate cross-department issues to the Chief of Staff.

### Specialists
Task-level executors. Each specialist has defined tools, permissions, and a narrow scope of responsibility. Specialists execute within their scope and escalate anything outside it.

## Departments

| Department | Executive | Example Specialists | Focus |
|-----------|-----------|---------------------|-------|
| Technology (13) | `cto` | `lead-backend`, `lead-frontend`, `devops-lead` | Building and maintaining systems |
| AI Research (7) | `caio` | `ml-engineer`, `prompt-engineer`, `red-team-engineer` | Model strategy and research |
| Operations (6) | `coo` | `workflow-owner`, `orchestration-owner`, `platform-reliability-engineer` | Business process execution |
| Security (7) | `ciso` | `security-architect`, `security-compliance-lead` | Security and hardening |
| Product (5) | `cpo` | `product-owner`, `product-designer`, `ux-research-lead` | Product vision and delivery |
| Marketing (9) | `cmo` | `content-creator`, `product-marketing-manager`, `growth-hacker` | Demand generation and brand |
| Board (7) | `board-chair` | `board-strategy`, `board-finance`, `board-technology` | Governance oversight |
| People (4) | `hr` | `hr-owner`, `recruiter`, `culture-values-officer` | Workforce and culture |
| Sales (3) | `sales` | `sales-owner`, `solutions-engineer` | Revenue generation |
| Executive (5) | `human-ceo`, `chief-of-staff`, `ceo-advisor` | `internal-comms-lead`, `ai-ethics-board-chair` | CEO and coordination |
| Data (3) | `cdo` | `data-engineer`, `business-intelligence-engineer` | Data processing and analytics |
| Legal (3) | `clo` | `data-privacy-officer`, `legal-owner` | Contracts, compliance, risk |
| QA (3) | `qa-lead` (reports to `cto`) | `test-engineering-lead`, `release-manager` | Quality assurance |
| Strategy (2) | `cso` | `market-analyst` | Corporate strategy |
| Consulting (1) | `consulting-lead` | — | Client consulting |
| Finance (2) | `cfo` | `financial-analyst` | Financials and fundraising |
| Customer Success (2) | `customer-success` | `customer-success-owner` | Customer retention and support |
| IT (1) | `cio` | — | IT infrastructure |
| Business Development (1) | `head-of-business-development` (reports to `chief-of-staff`) | — | Partnerships and growth |

Counts in parentheses are live registry headcounts (post-trim, 2026-09-23); `docs/AGENT-REGISTRY-TABLE.md` is the generator-maintained reference that stays in sync.

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
