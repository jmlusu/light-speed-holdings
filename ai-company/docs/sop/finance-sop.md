# Finance Standard Operating Procedure

**Document ID:** SOP-FIN-001
**Department:** Finance
**Owner:** Chief Financial Officer (CFO)
**Classification:** Internal
**Last Updated:** July 2026

---

## 1. Purpose

This Standard Operating Procedure establishes the processes for budget management, LLM cost tracking, spend optimization, and financial reporting within Light Speed Holdings' AI Company Builder. It ensures responsible use of resources while maintaining visibility into all AI-related expenditures.

## 2. Scope

This SOP applies to all financial activities including:

- LLM token usage tracking and cost attribution (`CostTracker`)
- Daily and per-task budget enforcement
- Model routing cost optimization (`ModelRouter` tier selection)
- Dashboard KPI collection and reporting
- Department budget allocation and monitoring
- Vendor cost management (LLM providers: OpenAI, Anthropic, DeepSeek, Ollama)
- Financial reporting to the board and human operator

## 3. Roles and Responsibilities

| Role | Agent/Person | Responsibilities |
|------|-------------|-----------------|
| CFO | Department executive | Budget ownership, financial reporting, spend approval |
| Finance Lead | Specialist | Daily cost monitoring, report generation, variance analysis |
| CTO | `cto` | Technical cost optimization, model tier selection |
| CAIO | `caio` | Model evaluation, cost-benefit analysis of LLM providers |
| CEO / Founder | Human operator | Final budget approval, strategic spending decisions |

## 4. Budget Management

### 4.1 Budget Structure

The organization's budget is defined in the `Budget` model (`src/ai_company/models/models.py`):

```python
class Budget(BaseModel):
    fiscal_year: int = 2024
    total_budget: float = 0
    currency: str = "USD"
    departments: list[DepartmentBudget] = Field(default_factory=list)
    contingency: Contingency = Field(default_factory=Contingency)
```

Each department has an allocated budget:

```python
class DepartmentBudget(BaseModel):
    name: str
    budget: float = 0
    headcount: int = 0
    priorities: list[str] = Field(default_factory=list)
```

### 4.2 Budget Allocation Process

1. **Quarterly planning**: CFO proposes department budgets based on strategic priorities
2. **Review**: Board reviews and approves budget allocations
3. **Distribution**: Budgets are loaded into the system and enforced via `CostTracker`
4. **Monitoring**: Daily spend is tracked against allocated budgets
5. **Adjustment**: Mid-quarter reallocation requires CFO + CEO approval

### 4.3 Contingency Fund

The contingency fund covers unexpected expenses:

- **Default allocation**: 5% of total budget
- **Approval threshold**: Contingency spending requires CFO approval
- **Usage tracking**: All contingency expenditures must be logged with justification

## 5. LLM Cost Tracking

### 5.1 CostTracker Overview

The `CostTracker` class (`src/ai_company/llm/cost_tracker.py`) is the central mechanism for tracking LLM expenditures:

```python
from ai_company.llm.cost_tracker import CostTracker

tracker = CostTracker(
    results_dir="results",
    daily_budget_usd=50.00,    # Maximum daily spend
    task_budget_usd=5.00,      # Maximum per-task spend
)
```

### 5.2 How Cost Tracking Works

**Every LLM call is recorded** with the following data:

| Field | Description |
|-------|-------------|
| `timestamp` | ISO datetime of the call |
| `model` | Model identifier (e.g., `gpt-4o`, `claude-3-5-sonnet`) |
| `provider` | Provider identifier (e.g., `openai`, `anthropic`, `ollama`) |
| `agent_name` | Name of the agent making the call |
| `task_id` | ID of the task being executed |
| `prompt_tokens` | Number of input tokens |
| `completion_tokens` | Number of output tokens |
| `cost_usd` | Calculated cost in USD |
| `iteration` | Loop iteration number (for multi-turn agentic loops) |

**Cost calculation** uses per-model pricing (per 1M tokens):

| Model | Input Cost | Output Cost |
|-------|-----------|------------|
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| claude-3-5-sonnet | $3.00 | $15.00 |
| claude-3-5-haiku | $0.80 | $4.00 |
| deepseek-chat | $0.14 | $0.28 |
| ollama/llama3.1:8b | $0.00 | $0.00 |

### 5.3 Budget Enforcement

The `AgentLoop` checks budgets before each LLM iteration:

```python
# In AgentLoop.run():
if self.cost_tracker and task_id:
    allowed, reason = self.cost_tracker.check_budget(task_id)
    if not allowed:
        last_error = f"Budget exceeded: {reason}"
        break
```

Budget enforcement rules:

1. **Daily budget**: Sum of all costs for the current day must not exceed `daily_budget_usd`
2. **Task budget**: Sum of all costs for a specific task must not exceed `task_budget_usd`
3. **Breach response**: When a budget is exceeded, the `AgentLoop` terminates immediately
4. **No override**: Budget limits cannot be bypassed by AI agents; only human operators can adjust them

### 5.4 Cost Log Format

All cost records are persisted to `results/cost_log.jsonl`:

```json
{
  "timestamp": "2026-07-19T10:30:00.000000",
  "model": "gpt-4o",
  "provider": "openai",
  "agent_name": "lead_dev",
  "task_id": "task-abc123",
  "prompt_tokens": 1500,
  "completion_tokens": 800,
  "cost_usd": 0.01175,
  "iteration": 2,
  "metadata": {}
}
```

## 6. Cost Optimization

### 6.1 Model Routing Strategy

The `ModelRouter` (`src/ai_company/model_router.py`) optimizes costs by routing tasks to the most cost-effective model:

**Routing priority:**

1. **Per-agent override**: Agent registry specifies an exact model
2. **Context rules**: Escalation/approval contexts route to higher-tier models
3. **Agent type + priority rules**: Matched from `company/models.yaml` routing rules
4. **Fallback**: Default to "standard" tier

**Tier structure:**

| Tier | Models | Cost Profile | Use Case |
|------|--------|-------------|----------|
| `budget` | Ollama (llama3.1:8b, codellama:13b) | Free | Simple tasks, drafts, low-priority |
| `standard` | GPT-4o-mini, Claude 3.5 Haiku | Low | General tasks, code review, analysis |
| `premium` | GPT-4o, Claude 3.5 Sonnet | Medium | Complex reasoning, architecture, critical decisions |
| `override` | Per-agent specified | Varies | Specialized needs |

### 6.2 Cost Reduction Strategies

1. **Use budget tier for non-critical tasks**: Draft generation, formatting, simple queries
2. **Batch similar tasks**: Reduce context window usage by grouping related work
3. **Optimize prompts**: Shorter, more specific prompts reduce token counts
4. **Leverage local models**: Ollama models have zero marginal cost
5. **Monitor cost-per-task**: Identify agents/tasks with abnormally high costs
6. **Set aggressive task budgets**: Prevent runaway agentic loops from consuming excessive tokens

### 6.3 Cost Anomaly Detection

The Finance Lead monitors for cost anomalies:

| Anomaly Type | Threshold | Action |
|-------------|-----------|--------|
| Daily spend > 2x average | > 200% of 7-day average | Alert CFO |
| Single task cost > $5.00 | > task_budget_usd | Review agent configuration |
| Model downgrade needed | High-cost model on simple task | Adjust routing rules |
| Agent loop runaway | > 10 iterations on single task | Review LoopConfig.max_iterations |

## 7. Financial Reporting

### 7.1 Daily Cost Summary

The `CostTracker.get_daily_summary()` method provides:

```python
summary = tracker.get_daily_summary()
# Returns:
{
    "date": "2026-07-19",
    "total_cost_usd": 12.45,
    "total_prompt_tokens": 150000,
    "total_completion_tokens": 45000,
    "call_count": 87,
    "by_model": {
        "gpt-4o": {"cost_usd": 8.20, "calls": 32},
        "gpt-4o-mini": {"cost_usd": 3.10, "calls": 45},
        "llama3.1:8b": {"cost_usd": 0.0, "calls": 10}
    }
}
```

### 7.2 Task Cost Summary

Per-task cost tracking via `CostTracker.get_task_summary()`:

```python
summary = tracker.get_task_summary("task-abc123")
# Returns:
{
    "task_id": "task-abc123",
    "total_cost_usd": 0.045,
    "total_prompt_tokens": 12000,
    "total_completion_tokens": 3500,
    "call_count": 6,
    "max_iteration": 3
}
```

### 7.3 Dashboard KPIs

The CEO Dashboard (`src/ai_company/dashboard/`) provides real-time financial visibility:

- **Total daily spend**: Real-time aggregation of cost_log.jsonl
- **Budget utilization**: Percentage of daily/task budgets consumed
- **Cost by department**: Attribution of LLM costs to departments
- **Cost trend**: 7-day and 30-day spend trends
- **Model distribution**: Breakdown of spend by LLM model

### 7.4 Monthly Financial Report

The Finance Lead produces a monthly report containing:

1. **Total LLM spend** by model, provider, and department
2. **Budget vs. actual** variance analysis
3. **Cost optimization recommendations** based on usage patterns
4. **ROI analysis**: Cost per task completed, cost per unit of value delivered
5. **Forecast**: Projected spend for next month based on current trends

## 8. Vendor Management

### 8.1 LLM Provider Contracts

| Provider | Models | Pricing Model | Optimization |
|----------|--------|--------------|-------------|
| OpenAI | GPT-4o, GPT-4o-mini, o1 | Per-token | Use GPT-4o-mini for non-critical |
| Anthropic | Claude 3.5 Sonnet, Haiku | Per-token | Use Haiku for drafts |
| DeepSeek | deepseek-chat, deepseek-coder | Per-token | Cost-effective alternative |
| Ollama | Llama3.1, CodeLlama, Qwen | Self-hosted (free) | Maximize local usage |

### 8.2 Vendor Review Cadence

| Review | Frequency | Owner | Focus |
|--------|-----------|-------|-------|
| Cost benchmarking | Monthly | Finance Lead | Compare provider pricing |
| Model evaluation | Quarterly | CAIO | Performance vs. cost analysis |
| Contract review | Annually | CFO | Terms, volume discounts |
| Provider health check | Weekly | CTO | Uptime, latency, availability |

## 9. Escalation Procedures

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Daily budget exceeded | CFO | Immediate |
| Single task cost > $10 | CFO | 4 hours |
| Vendor pricing change | CFO + CAIO | 24 hours |
| Budget reallocation request | CFO + CEO | 48 hours |
| Cost anomaly detected | Finance Lead -> CFO | 4 hours |
| Quarterly budget review | Board | Per schedule |

## 10. Key Performance Indicators

| KPI | Target | Frequency | Owner |
|-----|--------|-----------|-------|
| Daily LLM spend | < $50/day | Daily | Finance Lead |
| Cost per task | < $0.50 | Weekly | Finance Lead |
| Budget utilization | 80-95% | Monthly | CFO |
| Cost optimization savings | > 10% QoQ | Quarterly | CAIO |
| Local model usage | > 30% of tasks | Monthly | CTO |
| Report accuracy | 100% | Monthly | Finance Lead |

## 11. Compliance Requirements

- All cost records in `results/cost_log.jsonl` must be retained for 90 days
- Budget changes require documented approval from CFO
- Cost logs must not be manually edited or deleted
- Monthly financial reports must be archived in `reports/`
- Vendor contracts must be stored in `docs/legal/`
- All LLM API keys must be stored in environment variables, never in source code

## 12. Related Documents

- `src/ai_company/llm/cost_tracker.py` - Cost tracking implementation
- `src/ai_company/model_router.py` - Model routing and cost optimization
- `src/ai_company/dashboard/kpis/finance.py` - Finance KPI collector
- `docs/MODEL-ROUTING-POLICY.md` - Detailed routing configuration
- `company/models.yaml` - Model and tier configuration (runtime)

---

*This document is maintained by the Finance department. Updates require CFO approval.*
