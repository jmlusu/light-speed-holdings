"""Test the ETL pipelines end-to-end."""

from ai_company.data.database import Database
from ai_company.data.etl.pipelines.kpi_snapshot import CostAggregationPipeline, AgentPerformancePipeline
from pathlib import Path
import tempfile
import shutil
from datetime import datetime, timezone, timedelta

# Test with a temporary database
tmpdir = Path(tempfile.mkdtemp())
try:
    db_path = tmpdir / 'test.db'
    db = Database(str(db_path))
    db.init_schema()
    
    # Insert some test cost records
    now = datetime.now(timezone.utc)
    for i in range(5):
        ts = (now - timedelta(days=i)).isoformat()
        db.execute(
            '''INSERT INTO cost_records (timestamp, model, provider, agent_name, task_id, prompt_tokens, completion_tokens, cost_usd, iteration, metadata)
               VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (ts, 'gpt-4o', 'openai', 'engineer', f'task-{i}', 100, 50, 0.01 * (i+1), 1, '{}')
        )
    db.commit()
    
    # Insert some test tasks and audit events
    for i in range(3):
        ts = (now - timedelta(hours=i)).isoformat()
        db.execute(
            '''INSERT INTO tasks (id, sender_id, receiver_id, status, created_at, completed_at, raw_json)
               VALUES (?,?,?,?,?,?,?)''',
            (f'task-{i}', 'alice', 'bob', 'completed' if i < 2 else 'failed', ts, ts, '{}')
        )
        meta = '{"cost": 0.01}'
        db.execute(
            '''INSERT INTO audit_events (event_id, timestamp, event_type, agent_id, task_id, tool, args, result, metadata, severity)
               VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (f'audit-{i}', ts, 'tool_call', 'bob', f'task-{i}', 'read', '{}', '{}', meta, 'info')
        )
    db.commit()
    
    # Test CostAggregationPipeline
    print('=== Testing CostAggregationPipeline ===')
    cost_pipeline = CostAggregationPipeline(db, period='daily')
    result = cost_pipeline.run()
    print(f'Success: {result.success}')
    print(f'Extracted: {result.extraction.record_count if result.extraction else 0}')
    print(f'Transformed: {result.transformation.output_count if result.transformation else 0}')
    print(f'Loaded: {result.load.loaded_count if result.load else 0}')
    print(f'Load target: {result.load.target if result.load else None}')
    print(f'Errors: {result.errors}')
    
    # Verify data in cost_aggregations table
    rows = db.fetchall('SELECT * FROM cost_aggregations')
    print(f'Cost aggregation rows in DB: {len(rows)}')
    for row in rows:
        print(f'  Period: {row["period"]}, Key: {row["period_key"]}, Cost: {row["total_cost_usd"]}')
    
    # Test AgentPerformancePipeline
    print()
    print('=== Testing AgentPerformancePipeline ===')
    agent_pipeline = AgentPerformancePipeline(db, days=30)
    result = agent_pipeline.run()
    print(f'Success: {result.success}')
    print(f'Extracted: {result.extraction.record_count if result.extraction else 0}')
    print(f'Transformed: {result.transformation.output_count if result.transformation else 0}')
    print(f'Loaded: {result.load.loaded_count if result.load else 0}')
    print(f'Load target: {result.load.target if result.load else None}')
    print(f'Errors: {result.errors}')
    
    # Verify data in agent_performance_metrics table
    rows = db.fetchall('SELECT * FROM agent_performance_metrics')
    print(f'Agent performance rows in DB: {len(rows)}')
    for row in rows:
        print(f'  Agent: {row["agent_id"]}, Completed: {row["tasks_completed"]}, Rate: {row["completion_rate_pct"]}%')
    
    print()
    print('All tests passed!')
finally:
    db.close()
    shutil.rmtree(tmpdir, ignore_errors=True)