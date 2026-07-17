# Company Decision Framework

Every significant decision must follow this framework. It ensures consistency, traceability, and accountability across all levels of the organization.

## When to Use This Framework

Use this framework when the decision:
- Affects more than one department
- Involves spending over $100 or equivalent token budget
- Is irreversible or difficult to undo
- Touches security, permissions, or data access
- Sets a precedent for future decisions

For small, reversible decisions within a single specialist's scope, document the choice in the task result — no formal framework needed.

## The 10-Step Framework

### 1. Problem Statement
One sentence. What is broken, missing, or suboptimal?

> *Example: "The orchestrator runs on-demand only, requiring manual triggering every 6 hours."*

### 2. Root Cause
Why does this problem exist? What is the underlying reason, not just the symptom?

> *Example: "No scheduling infrastructure was implemented during the orchestration milestone."*

### 3. Alternatives Considered
List at least two options, including "do nothing." For each, state the tradeoff.

| Option | Approach | Tradeoff |
|--------|----------|----------|
| A | GitHub Action with cron schedule | Simple, free, but limited to 6h intervals |
| B | Long-running daemon process | More flexible, but requires hosting |
| C | Do nothing (manual trigger) | No cost, but unsustainable at scale |

### 4. Recommendation
State the recommended option clearly. Explain why it wins over the alternatives.

> *Example: "Option A — GitHub Action. It is the simplest path that meets the requirement, requires no infrastructure, and can be upgraded to Option B later."*

### 5. Risks
What could go wrong? For each risk, state the likelihood and mitigation.

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| GitHub Actions outage | Low | Medium | Manual trigger as fallback |
| Cron misconfiguration | Medium | Low | Test in staging first |

### 6. Costs
What does this cost? Include token budget, compute, human time, and opportunity cost.

> *Example: "Zero ongoing cost. 2 hours of implementation time."*

### 7. Benefits
What do we gain? Quantify where possible.

> *Example: "Eliminates 4 manual triggers per day. Saves ~10 minutes of human time daily."*

### 8. Timeline
When will this be done? What are the milestones?

| Milestone | Target |
|-----------|--------|
| Implementation | Day 1 |
| Testing | Day 1 |
| Deployment | Day 2 |

### 9. Dependencies
What must be true before this can proceed? What does this block?

> *Example: "Requires orchestrator tick command (already implemented). Blocks nothing."*

### 10. Next Actions
Concrete, owned, time-bound steps.

| Action | Owner | Due |
|--------|-------|-----|
| Create `autonomous.yml` workflow | cto | Day 1 |
| Test cron schedule in fork | cto | Day 1 |
| Update STATUS.md | chief-of-staff | Day 2 |

## Decision Records

Every decision using this framework should be saved as a decision record in the memory engine:

```bash
ai-company memory add --type semantic --content "Decision: [title]. Recommendation: [option]. Rationale: [brief reason]."
```

## Approval Matrix

Decisions are classified by scope and require corresponding approval:

| Scope | Approver | Examples |
|-------|----------|---------|
| Task-level | Self (specialist) | Code style, file organization |
| Department-level | Executive | Tool selection, workflow changes |
| Cross-department | Chief of Staff | Architecture changes, new integrations |
| Business-critical | Human CEO | Budget, security, public-facing changes |