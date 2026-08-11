# Board Governance Charter — Light Speed Holdings

> Last updated: 2026-07-17

## Board Composition

| Agent | Role | Expertise | Type |
|-------|------|-----------|------|
| board-strategy | Strategy Board Advisor | Long-term strategy, partnerships, market expansion | ReviewOnly |
| board-finance | Finance Board Advisor | Financial health, budgets, investment strategy | ReviewOnly |
| board-technology | Technology Board Advisor | Architecture, AI strategy, engineering health | ReviewOnly |
| board-product | Product Board Advisor | Product vision, roadmap, competitive positioning | ReviewOnly |
| board-customer | Customer Board Advisor | Customer experience, retention, market fit | ReviewOnly |
| board-risk | Risk Board Advisor | Operational, technical, and strategic risks | ReviewOnly |

All board agents have `ReviewOnly` permission: read-only access, no bash/edit/task capabilities.

## Meeting Cadence

| Meeting | Frequency | Required Attendees | Quorum |
|---------|-----------|-------------------|--------|
| Full Board | Quarterly | All 6 board advisors + human-ceo | 4 of 6 advisors |
| Finance Committee | Monthly | board-finance, cfo, human-ceo | 2 of 3 |
| Technology Committee | Monthly | board-technology, cto, human-ceo | 2 of 3 |
| Risk Committee | Quarterly | board-risk, cfo, cto, human-ceo | 3 of 4 |

## Voting Rules

- **Simple majority**: Routine operational decisions (budget < $100K)
- **Super majority (2/3)**: Strategic decisions, new department creation, model provider changes
- **Unanimous**: Constitutional changes, human CEO replacement, company dissolution
- **Advisory only**: Board votes are advisory to human CEO; final approval always rests with human CEO

## Decision Authority

| Decision Type | Authority | Board Role |
|---------------|-----------|------------|
| Daily operations (< $10K) | Department executive | None |
| Budget allocation ($10K-$100K) | CFO + CEO | Advisory |
| Strategic initiative ($100K+) | CEO + Board | Required advisory |
| New agent deployment | CTO + CAIO | Technology committee review |
| Model provider change | CTO + CFO | Technology + Finance committee review |
| Policy change | Legal + CEO | Full board advisory |
| Constitutional change | Human CEO only | Full board must approve unanimously |

## Escalation to Board

The board is consulted (not decided) on:
1. Cross-department conflicts unresolved by chief-of-staff
2. Budget overruns > 20% of quarterly allocation
3. Security incidents affecting customer data
4. Model performance degradation below SLA
5. Strategic pivots or market repositioning

## Reporting

- Weekly: Chief of Staff provides operational summary to board Slack channel
- Monthly: CFO provides financial dashboard to Finance Committee
- Quarterly: Full board receives comprehensive company review
- Ad-hoc: Risk Committee convenes within 24 hours for critical incidents

## Amendment Process

This charter may be amended by:
1. Proposal from any board member or executive
2. Review by Legal Advisor
3. Super majority vote of full board
4. Final approval by human CEO
