# Customer Success Standard Operating Procedure

**Document ID:** SOP-CS-001
**Department:** Customer Success
**Owner:** Customer Success Executive
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the processes for customer onboarding, retention, expansion, and satisfaction measurement within Light Speed Holdings' AI Company Builder. It ensures that every customer achieves their desired outcomes while maximizing the lifetime value of each relationship.

## 2. Scope

This SOP applies to all post-sale customer activities including:

- Customer onboarding and implementation support
- Technical support and issue resolution
- Customer health monitoring and satisfaction measurement
- Retention and churn prevention
- Expansion and upsell identification
- Customer feedback collection and action
- Knowledge base and documentation maintenance
- Community building and advocacy

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| Customer Success Lead | Executive | Strategy, retention targets, escalation management |
| Customer Success Manager | Specialist | Day-to-day customer relationships, health monitoring |
| Technical Support Engineer | Specialist | Issue resolution, technical guidance |
| Content Creator | Specialist | Knowledge base, tutorials, onboarding materials |
| CTO | `cto` | Technical escalation resolution, product feedback |
| CEO / Founder | Human operator | Strategic customer relationships, churn decisions |

## 4. Customer Onboarding

### 4.1 Onboarding Workflow

| Phase | Duration | Activities | Deliverable |
|-------|----------|-----------|-------------|
| Welcome | Day 1 | Welcome email, access provisioning, introduction call | Onboarding plan |
| Setup | Days 2-3 | Installation, configuration, first agent creation | Working installation |
| Training | Days 4-7 | Feature walkthrough, best practices, Q&A sessions | Training completion |
| Go-live | Days 8-14 | First real tasks, monitoring, optimization | Production usage |
| Review | Day 30 | 30-day review, health assessment, next steps | Health score |

### 4.2 Onboarding Checklist

For each new customer:

- [ ] Welcome email sent with getting started guide
- [ ] Installation verified (CLI, Docker, or cloud)
- [ ] First agent hierarchy created and tested
- [ ] LLM provider configured and tested
- [ ] Budget limits set via `CostTracker` configuration
- [ ] HITL gates configured for the customer's approval workflow
- [ ] Dashboard access provisioned and verified
- [ ] Customer success manager assigned
- [ ] 30-day review meeting scheduled
- [ ] Customer goals and success criteria documented

### 4.3 Onboarding Automation

The onboarding process can be partially automated:

1. **Automated welcome**: Triggered when a new customer signs up
2. **Guided setup**: CLI wizard for initial configuration
3. **Health monitoring**: Automated checks via the `Doctor` system
4. **Milestone tracking**: Automated notifications when onboarding milestones are reached

## 5. Customer Health Monitoring

### 5.1 Health Score Model

Each customer receives a health score based on:

| Factor | Weight | Measurement | Source |
|--------|--------|-------------|--------|
| Product usage | 30% | Active agents, tasks executed per week | MessageBus |
| Feature adoption | 20% | Features used vs. available | Usage analytics |
| Support tickets | 15% | Volume and severity of tickets | Support system |
| Engagement | 15% | Meetings attended, content consumed | CRM |
| Expansion signals | 10% | New use cases, team growth | Customer feedback |
| Payment history | 10% | On-time payments, plan upgrades | Billing |

### 5.2 Health Score Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy | Continue standard engagement, identify expansion |
| 60-79 | Needs attention | Proactive outreach, address gaps |
| 40-59 | At risk | Escalate to CS Lead, create intervention plan |
| 0-39 | Critical | Immediate intervention, executive involvement |

### 5.3 Automated Health Checks

The `Doctor` system (`ai-company doctor run`) can be run against customer deployments:

```bash
ai-company doctor run --customer <customer_id>
```

This checks:
- System health and availability
- Agent responsiveness
- LLM provider connectivity
- Cost tracker status
- HITL gate functionality

## 6. Retention

### 6.1 Churn Prevention

Proactive retention activities:

| Risk Signal | Intervention | Owner | SLA |
|------------|-------------|-------|-----|
| Usage declining > 30% | Outreach call + training offer | CSM | 48 hours |
| Support ticket escalation | Technical resolution + follow-up | Support Engineer | 4 hours |
| Negative feedback | Escalation to CS Lead + remediation plan | CS Lead | 24 hours |
| Payment failure | Billing support + account review | CS Lead | 24 hours |
| Competitor evaluation | Executive engagement + value reinforcement | CEO | 24 hours |

### 6.2 Retention Workflow

1. **Detect**: Automated health monitoring identifies risk signals
2. **Diagnose**: CSM investigates the root cause through customer interaction
3. **Intervene**: Execute the appropriate retention action
4. **Follow up**: Confirm the issue is resolved and the customer is satisfied
5. **Document**: Record the outcome and update the customer health score

### 6.3 Save Playbooks

| Scenario | Playbook |
|----------|---------|
| Price sensitivity | Offer usage-based pricing, demonstrate ROI |
| Feature gap | Create a roadmap, provide workaround, escalate to product |
| Support frustration | Apologize, expedite resolution, assign senior engineer |
| Champion departure | Identify new champion, provide re-onboarding |
| Competitor switching | Executive engagement, case study, POC extension |

## 7. Renewal Cycle

### 7.1 Renewal Workflow

Renewals are managed proactively, beginning 60 days before term end:

1. **Flag**: Automated health check identifies contracts within the 60-day window
2. **Assess**: `cs_lead` reviews the customer's health score (Section 5) and expansion signals (Section 7.1)
3. **Engage**: CSM schedules a renewal conversation; surface value delivered and expansion options
4. **Quote**: `cs_lead` issues a renewal quote; pricing changes route to `cfo`
5. **Handoff**: On agreement, `cs_lead` notifies `clo` for contract renewal per `docs/sop/legal-sop.md`
6. **Close**: Updated contract executed; health score reset to "Healthy" baseline

### 7.2 Renewal Risk Handling

| Health Score | Renewal Risk | Action |
|--------------|--------------|--------|
| 80-100 | Low | Standard renewal outreach |
| 60-79 | Medium | Value-review meeting + expansion offer |
| 40-59 | High | Executive engagement (`ceo`) + save playbook (Section 6.3) |
| 0-39 | Critical | Immediate intervention, possible concession approval via `cfo` |

## 8. Expansion

### 7.1 Expansion Signals

| Signal | Evidence | Opportunity |
|--------|----------|-------------|
| Team growth | New agents added to hierarchy | Upgrade plan |
| Usage increase | Tasks per week > 2x baseline | Higher tier |
| New use cases | Customer exploring new departments | Cross-sell |
| Positive feedback | NPS > 8, testimonials offered | Case study + referral |
| Budget increase | Customer mentions expanded budget | Enterprise features |

### 7.2 Expansion Workflow

1. **Identify**: CSM flags expansion signal during health review
2. **Qualify**: Confirm the need and budget with the customer
3. **Propose**: Present relevant expansion options (plan upgrade, new features)
4. **Close**: Work with Sales to execute the expansion deal
5. **Implement**: Ensure smooth transition to expanded usage
6. **Measure**: Track the customer's expanded value realization

### 7.3 Upsell Opportunities

| Current Tier | Upsell Option | Trigger |
|-------------|---------------|---------|
| Starter | Professional | Team > 3 people, need cloud LLM |
| Professional | Enterprise | Need unlimited agents, priority support |
| Any | Custom integration | Specific workflow requirements |
| Any | Training package | Complex implementation needs |

## 9. Support

### 9.1 Support Channels

| Channel | Response SLA | Resolution SLA | Use Case |
|---------|-------------|---------------|----------|
| Email | 4 hours | 24 hours | General questions, non-urgent issues |
| In-app chat | 1 hour | 8 hours | Quick questions, guidance |
| Phone/video | 30 minutes | 1 hour | Urgent issues, complex discussions |
| Emergency hotline | 15 minutes | 4 hours | SEV-1 outages only |

### 9.2 Issue Classification

| Severity | Definition | Response | Resolution |
|----------|-----------|----------|-----------|
| SEV-1 | Complete system failure | 15 minutes | 4 hours |
| SEV-2 | Major feature broken | 1 hour | 8 hours |
| SEV-3 | Minor issue, workaround available | 4 hours | 24 hours |
| SEV-4 | Cosmetic, informational | 24 hours | 1 week |

### 9.3 Support Escalation

```
Support Engineer -> CS Lead -> CTO -> CEO
     (15 min)      (1 hr)    (4 hr)  (immediate)
```

## 10. Feedback Collection

### 10.1 Feedback Channels

| Channel | Frequency | Metric | Action |
|---------|-----------|--------|--------|
| NPS survey | Quarterly | Net Promoter Score | Track trends, follow up on detractors |
| CSAT survey | Per interaction | Customer Satisfaction | Improve support quality |
| Feature requests | Continuous | Request count and priority | Inform product roadmap |
| Churn survey | Per churn | Churn reasons | Improve retention |

### 10.2 Feedback Loop

1. **Collect**: Gather feedback through surveys, support tickets, and conversations
2. **Analyze**: Identify patterns and prioritize themes
3. **Act**: Assign action items to appropriate teams
4. **Communicate**: Close the loop with customers on actions taken
5. **Measure**: Track impact of changes on satisfaction and retention

## 11. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Customer churn risk > 50% | CS Lead + CEO | 24 hours |
| SEV-1 support ticket | CTO | Immediate |
| Contract dispute | Legal + CS Lead | 4 hours |
| Customer data breach | CTO + Legal + CEO | Immediate |
| Refund request > $1,000 | CFO + CS Lead | 48 hours |
| Negative public review | Marketing Lead + CS Lead | 4 hours |

## 12. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Net Promoter Score (NPS) | > 50 | Quarterly | CS Lead |
| Customer retention rate | > 90% | Monthly | CS Lead |
| Time to value (onboarding) | < 14 days | Per customer | CSM |
| Support resolution time | < 24 hours (avg) | Weekly | Support Lead |
| Customer health score | > 70 (avg) | Monthly | CS Lead |
| Expansion revenue | > 20% of MRR | Monthly | CS Lead |
| Churn rate | < 5% monthly | Monthly | CS Lead |

## 13. Compliance Requirements

- Customer data must be handled per the Privacy Policy
- Support interactions must be logged and retained for 1 year
- Customer health scores must be updated at least monthly
- Churn surveys must be conducted for every churned customer
- Customer feedback must be anonymized before sharing with external parties
- Refund and credit decisions must be documented and approved

## 14. Related Documents

- `docs/legal/privacy-policy.md` - Customer data handling
- `docs/legal/terms-of-service.md` - Service commitments
- `docs/sop/sales-sop.md` - Pre-sale process alignment
- `docs/USER-GUIDE.md` - Customer-facing documentation
- `src/ai_company/dashboard/kpis/customer_success.py` - CS KPI collector
- `src/ai_company/doctor/` - Health check system

---

*This document is maintained by the Customer Success department. Updates require CS Lead approval.*
