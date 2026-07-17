# AI Company Organization

## Structure

Light Speed Holdings is organized as a hierarchical AI company with one human CEO and 27 AI agents across 7 departments.

```
                    human-ceo
                        │
                  chief-of-staff
                ┌───────┼───────┐
             cto      cfo      coo
              │        │        │
         ┌────┴────┐   │   ┌───┴───┐
      eng    data  │   │  ops   biz
         │         │   │    │      │
     specialists   │   │  specialists
                   │   │
              marketing  sales
              legal  customer-success
```

## Roles

### Human CEO
The sole human in the hierarchy. Provides strategic direction, final approval authority, and oversight. All irreversible decisions ultimately flow here.

### Chief of Staff
Operational coordinator. Manages the daily flow of work across departments, generates executive briefings, and handles escalations that cross department boundaries. Acts with the CEO's authority on operational matters.

### CTO (Chief Technology Officer)
Owns engineering, data, and infrastructure. Responsible for technical architecture, security, deployment, and the agent execution system.

### CFO (Chief Financial Officer)
Owns finance, legal, and compliance. Responsible for budget allocation, cost tracking (including LLM token spend), and regulatory adherence.

### COO (Chief Operating Officer)
Owns operations, marketing, sales, and customer success. Responsible for business process execution, customer-facing operations, and revenue-generating activities.

### Department Heads
Each department has an executive owner and one or more specialist agents. Department heads make decisions within their domain and escalate cross-department issues to the Chief of Staff.

### Specialists
Task-level executors. Each specialist has defined tools, permissions, and a narrow scope of responsibility. Specialists execute within their scope and escalate anything outside it.

## Departments

| Department | Executive | Specialists | Focus |
|-----------|-----------|-------------|-------|
| Engineering | cto | lead-backend, lead-frontend, lead-devops | Building and maintaining systems |
| Data | cto | data-analyst | Data processing and analytics |
| Operations | coo | operations-manager | Business process execution |
| Marketing | coo | marketing-strategist, content-creator | Demand generation and brand |
| Sales | coo | sales-lead | Revenue generation |
| Legal | cfo | legal-advisor | Contracts, compliance, risk |
| Customer Success | coo | cs-lead | Customer retention and support |

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