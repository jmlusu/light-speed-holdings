from datetime import datetime, timedelta, timezone

from ai_company.data.etl.transformers.kpi_transformer import AgentPerformanceTransformer

transformer = AgentPerformanceTransformer(days=30)
now = datetime.now(timezone.utc)

# Tasks
tasks = []
for i in range(3):
    ts = (now - timedelta(hours=i)).isoformat()
    tasks.append(
        {
            "id": f"task-{i}",
            "sender_id": "alice",
            "receiver_id": "bob",
            "status": "completed" if i < 2 else "failed",
            "created_at": ts,
            "completed_at": ts,
        }
    )

# Audit events
audit_events = []
for i in range(3):
    ts = (now - timedelta(hours=i)).isoformat()
    audit_events.append(
        {
            "event_id": f"audit-{i}",
            "timestamp": ts,
            "event_type": "tool_call",
            "agent_id": "bob",
            "task_id": f"task-{i}",
            "tool": "read",
            "args": "{}",
            "result": "{}",
            "metadata": '{"cost": 0.01}',
            "severity": "info",
        }
    )

combined = tasks + audit_events

result = transformer.transform(
    combined,
    tasks=tasks,
    audit_events=audit_events,
)

print("Output records:")
for r in result.records:
    print(f"  agent_id={r.get('agent_id')}")
    print(f"  period_days={r.get('period_days')}")
    print(f"  period_start={r.get('period_start')}")
    print(f"  period_end={r.get('period_end')}")
    print(f"  tasks_sent={r.get('tasks_sent')}")
    print(f"  tasks_received={r.get('tasks_received')}")
    print(f"  tasks_completed={r.get('tasks_completed')}")
    print(f"  tasks_failed={r.get('tasks_failed')}")
    print(f"  completion_rate_pct={r.get('completion_rate_pct')}")
    print(f"  error_rate_pct={r.get('error_rate_pct')}")
    print(f"  sent_by_status={r.get('sent_by_status')}")
    print(f"  received_by_status={r.get('received_by_status')}")
    print(f"  audit_events={r.get('audit_events')}")
    print(f"  tool_usage={r.get('tool_usage')}")
    print(f"  total_cost_usd={r.get('total_cost_usd')}")
    print(f"  prompt_tokens={r.get('prompt_tokens')}")
    print(f"  completion_tokens={r.get('completion_tokens')}")
    print(f"  llm_calls={r.get('llm_calls')}")
    print(f"  error_events={r.get('error_events')}")
    print(f"  computed_at={r.get('computed_at')}")
    print()

# Now test validation
from ai_company.data.etl.quality.validator import validate_records  # noqa: E402

violations = validate_records(result.records, "agent_performance")
print("Violations:")
for v in violations:
    print(f"  {v}")
