# Sales Standard Operating Procedure

**Document ID:** SOP-SALES-001
**Department:** Sales
**Owner:** Sales Executive
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the processes for pipeline management, customer acquisition, revenue tracking, and deal execution within Light Speed Holdings' AI Company Builder. It ensures a structured, repeatable approach to revenue generation that scales with the organization.

## 2. Scope

This SOP applies to all sales activities including:

- Lead generation and qualification
- Pipeline management and stage progression
- Customer acquisition workflows
- Demo and proof-of-concept execution
- Deal closing and contract negotiation
- Revenue tracking and forecasting
- Customer expansion and upsell
- Competitive intelligence gathering

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| Sales Lead | Executive | Strategy, pipeline oversight, deal approval |
| Sales Development Rep | Specialist | Outbound prospecting, lead qualification |
| Account Executive | Specialist | Demo delivery, negotiation, closing |
| Content Creator | Specialist | Sales enablement materials, case studies |
| CFO | Department executive | Pricing approval, contract terms |
| CEO / Founder | Human operator | Strategic account relationships, final deal approval |

## 4. Lead Generation

### 4.1 Lead Sources

| Source | Type | Quality | Volume |
|--------|------|---------|--------|
| GitHub repository | Inbound | High | Medium |
| Documentation site | Inbound | High | High |
| Social media | Mixed | Medium | High |
| Conference/meetup | Outbound | High | Low |
| Referral | Inbound | Very High | Low |
| Content marketing | Inbound | Medium | High |

### 4.2 Lead Qualification

Leads are qualified using the BANT framework:

| Criterion | Question | Threshold |
|-----------|----------|-----------|
| **Budget** | Can they afford the tool? | > $100/month |
| **Authority** | Are they a decision-maker? | Yes or champion identified |
| **Need** | Do they have AI agent orchestration needs? | Clear use case identified |
| **Timeline** | When are they looking to implement? | Within 90 days |

### 4.3 Lead Scoring

| Score | Criteria | Action |
|-------|----------|--------|
| Hot (8-10) | BANT qualified, actively evaluating | Immediate outreach |
| Warm (5-7) | Some criteria met, interest expressed | Nurture sequence |
| Cold (1-4) | Early stage, no clear need | Marketing nurture |

## 5. Pipeline Management

### 5.1 Pipeline Stages

| Stage | Description | SLA | Exit Criteria |
|-------|-------------|-----|--------------|
| Prospecting | Initial research and outreach | 3 days | First contact made |
| Qualification | BANT assessment | 5 days | Lead scored and qualified |
| Discovery | Needs analysis and requirements gathering | 7 days | Requirements documented |
| Demo | Product demonstration | 5 days | Demo completed, feedback collected |
| Proposal | Pricing and terms proposal | 5 days | Proposal delivered |
| Negotiation | Terms discussion and refinement | 10 days | Terms agreed |
| Closed Won | Deal signed and onboarded | 3 days | Contract signed |
| Closed Lost | Deal lost or disqualified | N/A | Loss reason documented |

### 5.2 Task-Based Pipeline

All pipeline activities are managed through the `MessageBus`:

1. Sales Lead creates a task for the appropriate sales agent
2. Task includes the prospect's details, stage, and required actions
3. Sales agent executes the action and updates the task status
4. Task completion triggers the next stage in the pipeline

```python
from ai_company.models.task import Task, TaskStatus, TaskPriority

task = Task(
    id="sales-001",
    name="Qualify lead: Acme Corp",
    description="Complete BANT qualification for Acme Corp",
    sender_id="sales_lead",
    receiver_id="sdr_1",
    priority=TaskPriority.HIGH,
    status=TaskStatus.PENDING,
)
```

### 5.3 Pipeline Review

| Review | Frequency | Attendees | Focus |
|--------|-----------|-----------|-------|
| Pipeline standup | Daily | Sales team | Active deals, blockers |
| Weekly pipeline review | Weekly | Sales Lead + CFO | Forecast, stage progression |
| Monthly business review | Monthly | CEO + Sales Lead | Revenue vs. target, strategy |

## 6. Customer Acquisition

### 6.1 Demo Process

**Pre-demo:**

1. Review the prospect's requirements from the Discovery stage
2. Prepare a customized demo script highlighting relevant features
3. Test the demo environment (ensure LLM providers are available)
4. Prepare ROI calculations based on the prospect's use case

**Demo execution:**

1. **Introduction** (5 min): Company overview, prospect's goals
2. **Architecture overview** (10 min): How AI Company Builder works (MessageBus, AgentLoop, ModelRouter)
3. **Live demo** (20 min): Show the agent hierarchy, task delegation, HITL gates
4. **Cost analysis** (5 min): Demonstrate CostTracker, budget enforcement, model routing
5. **Q&A** (10 min): Address questions, discuss implementation timeline

**Post-demo:**

1. Send follow-up email with demo recording and relevant documentation
2. Update the pipeline stage based on prospect feedback
3. Schedule next steps within 48 hours

### 6.2 Proof of Concept (POC)

For complex deals, offer a structured POC:

| Phase | Duration | Activities |
|-------|----------|-----------|
| Setup | 3 days | Install tool, configure agents, integrate with prospect's workflow |
| Execution | 14 days | Run real tasks, measure performance, track costs |
| Evaluation | 3 days | Review results, present findings, recommend next steps |
| Decision | 7 days | Prospect evaluates, makes go/no-go decision |

### 6.3 Pricing

Pricing is based on the value delivered:

| Tier | Target Customer | Price Range | Features |
|------|----------------|-------------|----------|
| Starter | Individual developers | Free / $49/mo | Basic agent hierarchy, 5 agents, local models |
| Professional | Small teams | $199/mo | Full features, cloud LLM support, 20 agents |
| Enterprise | Organizations | Custom | Unlimited agents, priority support, custom integrations |

*Note: Pricing requires CFO and CEO approval before any public commitment.*

## 7. Revenue Tracking

### 7.1 Revenue Model

Revenue is tracked through the `Dashboard` KPI system:

- **Monthly Recurring Revenue (MRR)**: Subscription revenue
- **Annual Recurring Revenue (ARR)**: MRR x 12
- **Customer Acquisition Cost (CAC)**: Total sales + marketing spend / new customers
- **Customer Lifetime Value (CLV)**: Average revenue per customer x average lifetime
- **Churn Rate**: Customers lost / total customers per period

### 7.2 Revenue Dashboard

The CEO Dashboard provides real-time revenue visibility:

- MRR and ARR trends
- Pipeline value by stage
- Win/loss ratio
- Average deal size
- Sales cycle length
- Revenue by customer segment

### 7.3 Forecasting

Sales forecasting uses a weighted pipeline approach:

| Stage | Weight | Rationale |
|-------|--------|-----------|
| Prospecting | 10% | Early stage, high uncertainty |
| Qualification | 20% | Qualified but not yet committed |
| Discovery | 40% | Requirements understood, solution fit confirmed |
| Demo | 60% | Product demonstrated, positive feedback |
| Proposal | 80% | Pricing delivered, serious consideration |
| Negotiation | 90% | Terms being finalized |
| Closed Won | 100% | Deal signed |

## 8. Competitive Intelligence

### 8.1 Competitor Monitoring

| Competitor | Focus Area | Differentiation |
|-----------|-----------|----------------|
| CrewAI | Multi-agent orchestration | AI-native company structure, cost tracking |
| AutoGen | Agent conversation | HITL gates, budget enforcement |
| LangGraph | Agent workflows | Complete organizational hierarchy |
| Custom scripts | DIY solutions | Production-ready, enterprise features |

### 8.2 Win/Loss Analysis

Every closed deal (won or lost) must be analyzed:

1. **Win reasons**: What drove the decision?
2. **Loss reasons**: Why did we lose? (Price, features, timing, competitor)
3. **Competitive intel**: What did the prospect say about alternatives?
4. **Action items**: What should we change to improve win rate?

## 9. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Deal value > $10,000 | Sales Lead + CFO | 24 hours |
| Pricing exception requested | CFO + CEO | 48 hours |
| Legal/contract issue | Legal department | 24 hours |
| Technical blocker for POC | CTO | 4 hours |
| Competitive threat identified | Sales Lead + CEO | 24 hours |
| Customer complaint | Sales Lead + Customer Success | Immediate |

## 10. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Pipeline value | > $50,000 | Weekly | Sales Lead |
| Win rate | > 25% | Monthly | Sales Lead |
| Average deal size | > $2,000 | Monthly | Sales Lead |
| Sales cycle length | < 30 days | Monthly | Sales Lead |
| Demo-to-close rate | > 40% | Monthly | Account Executive |
| MRR growth | > 15% MoM | Monthly | CFO |
| Customer acquisition cost | < $500 | Quarterly | CFO |

## 11. Compliance Requirements

- All sales commitments must be documented in the MessageBus
- Pricing changes require CFO approval
- Contract terms must be reviewed by Legal
- Revenue recognition must follow accounting standards
- Customer data must be handled per the Privacy Policy
- Demo environments must not expose other customers' data

## 12. Related Documents

- `docs/legal/terms-of-service.md` - Standard Terms of Service
- `docs/legal/privacy-policy.md` - Privacy Policy
- `docs/sop/customer-success-sop.md` - Post-sale customer success
- `src/ai_company/dashboard/kpis/sales.py` - Sales KPI collector
- `docs/COMPANY-CONSTITUTION.md` - Company values and positioning

---

*This document is maintained by the Sales department. Updates require Sales Lead approval.*
