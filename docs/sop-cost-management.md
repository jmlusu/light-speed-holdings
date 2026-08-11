---
sop_id: SOP-COST-001
title: Cost Management Procedure
department: finance
owner: cfo
version: 1.0
effective_date: 2026-07-20
last_reviewed: 2026-07-20
status: active
---

# Cost Management Procedure

## 1. Purpose

Define the standard process for monitoring, controlling, and optimizing LLM API costs across all AI agents and departments. Ensure responsible spending while maintaining operational effectiveness.

## 2. Scope

Applies to all LLM API expenditures including:
- Per-task token usage and cost attribution
- Daily and per-task budget enforcement
- Model routing cost optimization
- Department budget allocation and monitoring
- Cost anomaly detection and response

## 3. Definitions

| Term | Definition |
|------|------------|
| CostTracker | System component that records every LLM API call with cost data |
| ModelRouter | System that selects the most cost-effective model for each task |
| Token Budget | Allocated LLM API spending per agent/department per period |
| Cost Anomaly | Unusual spending pattern that deviates significantly from baseline |

## 4. Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| CFO | Budget ownership, final approval on spending changes |
| Finance Lead | Daily cost monitoring, anomaly detection, reporting |
| CTO | Technical cost optimization, model tier selection |
| Human Operator | Approve budget changes exceeding executive authority |

## 5. Procedure

### Step 1: Monitor Daily Spend

Review cost data via the dashboard or CLI:

**Command:**
```bash
ai-company dashboard kpi show finance
```

Or check the cost log directly:

**Command:**
```bash
tail -20 results/cost_log.jsonl | python -m json.tool
```

**Expected Result:** Daily spend is below the configured budget limit (default: $50/day).

### Step 2: Review Cost by Model

Identify which models are consuming the most budget:

**Command:**
```bash
curl http://localhost:8420/api/kpis/live | python -m json.tool
```

**Expected Result:** Cost distribution is reasonable across models. No single model consumes >60% of daily budget without justification.

### Step 3: Check Budget Utilization

Verify budget status across departments:

**Command:**
```bash
ai-company dashboard kpi list
```

**Expected Result:** All departments are within budget thresholds.

### Step 4: Detect Anomalies

Look for cost anomalies:

| Anomaly Type | Threshold | Action |
|-------------|-----------|--------|
| Daily spend > 2x average | > 200% of 7-day average | Alert CFO immediately |
| Single task cost > $5.00 | > task_budget_usd | Review agent configuration |
| Model downgrade needed | High-cost model on simple task | Adjust routing rules |
| Agent loop runaway | > 10 iterations on single task | Review LoopConfig.max_iterations |

**Command:**
```bash
# Check recent high-cost tasks
grep '"cost_usd"' results/cost_log.jsonl | python -c "
import sys, json
records = [json.loads(line) for line in sys.stdin]
high_cost = [r for r in records if r.get('cost_usd', 0) > 1.0]
for r in sorted(high_cost, key=lambda x: x['cost_usd'], reverse=True)[:10]:
    print(f\"{r['cost_usd']:.4f} | {r['model']} | {r['agent_name']} | {r['task_id']}\")
"
```

**Expected Result:** No unexpected high-cost tasks.

### Step 5: Optimize Model Routing

Adjust model routing to reduce costs:

**Check current routing:**
```bash
ai-company models list
```

**Check available tiers:**
```bash
ai-company models tiers
```

**Optimization actions:**
1. Route simple tasks to `fast` tier (Ollama/DeepSeek)
2. Use `standard` tier for general work
3. Reserve `premium` tier for complex reasoning only
4. Set per-agent overrides in `company/models.yaml` under `agent_overrides`

### Step 6: Adjust Budget Limits

If budget limits need adjustment:

**Daily budget:**
```python
# In company/models.yaml or via CostTracker configuration
daily_budget_usd: 50.00  # Adjust as needed
task_budget_usd: 5.00    # Adjust as needed
```

**Escalation for budget changes:**

| Amount | Approver | SLA |
|--------|----------|-----|
| < $50/day increase | CFO | 4 hours |
| $50-$200/day increase | CFO + CEO | 24 hours |
| > $200/day increase | CEO + Board | 48 hours |

### Step 7: Report and Document

Generate cost reports for stakeholders:

**Daily:**
- Total LLM spend by model, provider, and department
- Budget utilization percentage
- Any anomalies detected and resolved

**Monthly:**
- Cost optimization recommendations
- ROI analysis (cost per task completed)
- Forecast for next month
- Provider comparison (cost vs. quality)

## 6. Cost Optimization Strategies

| Strategy | Expected Savings | Implementation |
|----------|-----------------|----------------|
| Use Ollama for drafts | 100% on affected tasks | Route simple tasks to fast tier |
| Batch similar tasks | 10-20% | Group related work in single context |
| Optimize prompts | 15-30% | Shorter, more specific prompts |
| Use DeepSeek for non-critical | 80% vs. GPT-4o | Route to deepseek-chat |
| Set aggressive task budgets | Prevents runaway loops | Configure task_budget_usd |
| Monitor cost-per-task | Identifies waste | Review cost_log.jsonl regularly |

## 7. Escalation Path

| Condition | Action | Contact |
|-----------|--------|---------|
| Daily budget exceeded | Pause non-critical tasks | CFO |
| Single task cost > $10 | Review and adjust | CFO |
| Cost anomaly detected | Investigate immediately | Finance Lead → CFO |
| Budget reallocation needed | Submit request | CFO + CEO |
| Provider pricing change | Evaluate alternatives | CFO + CTO |

## 8. Verification Checklist

- [ ] Daily spend is within budget limits
- [ ] No cost anomalies detected
- [ ] Model routing is optimized
- [ ] Budget limits are appropriate for current workload
- [ ] Cost logs are being recorded correctly
- [ ] Monthly report generated and reviewed
- [ ] Optimization recommendations implemented

## 9. References

- `src/ai_company/llm/cost_tracker.py` — CostTracker implementation
- `src/ai_company/model_router.py` — Model routing logic
- `company/models.yaml` — Provider and tier configuration
- `results/cost_log.jsonl` — Cost tracking records
- `docs/MODEL-ROUTING-POLICY.md` — Routing policy documentation
- `docs/sop-budget-approval.md` — Budget approval procedure

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-20 | cfo | Initial release |

---

*SOP Owner: cfo*
*Next Review: 2026-10-20*
