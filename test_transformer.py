from datetime import datetime, timedelta, timezone

from ai_company.data.etl.transformers.kpi_transformer import CostAggregationTransformer

transformer = CostAggregationTransformer(period="daily")
now = datetime.now(timezone.utc)
records = []
for i in range(5):
    ts = (now - timedelta(days=i)).isoformat()
    records.append(
        {
            "timestamp": ts,
            "model": "gpt-4o",
            "provider": "openai",
            "agent_name": "engineer",
            "task_id": f"task-{i}",
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "cost_usd": 0.01 * (i + 1),
            "iteration": 1,
            "metadata": "{}",
        }
    )

result = transformer.transform(records)
print("Output records:")
for r in result.records:
    print(
        f"  period={r.get('period')}, period_key={r.get('period_key')}, period_type={r.get('period_type')}"
    )
