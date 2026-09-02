# ETL Pipeline Framework

Production-grade ETL pipelines for KPI collection, transformation, and loading.

## Architecture

```
data/etl/
├── README.md                 # This file
├── __init__.py               # Package exports
├── base.py                   # Abstract base classes
├── extractors/               # Source-specific extractors
│   ├── __init__.py
│   ├── sqlite_extractor.py   # SQLite table extractors
│   ├── file_extractor.py     # Legacy file extractors
│   └── api_extractor.py      # External API extractors
├── transformers/             # Transformation logic
│   ├── __init__.py
│   ├── kpi_transformer.py    # KPI computation transforms
│   ├── cost_transformer.py   # Cost aggregation transforms
│   └── agent_transformer.py  # Agent performance transforms
├── loaders/                  # Target-specific loaders
│   ├── __init__.py
│   ├── sqlite_loader.py      # SQLite upsert/bulk load
│   └── file_loader.py        # NDJSON/JSON export
├── pipelines/                # Composed pipeline definitions
│   ├── __init__.py
│   ├── kpi_snapshot.py       # Periodic KPI snapshot pipeline
│   ├── cost_daily.py         # Daily cost aggregation pipeline
│   ├── agent_performance.py  # Agent analytics pipeline
│   └── governance.py         # Retention/governance pipeline
├── orchestration/            # Pipeline scheduling & monitoring
│   ├── __init__.py
│   ├── scheduler.py          # Cron-style scheduler
│   ├── monitor.py            # Pipeline health monitoring
│   └── dead_letter.py        # Failed record handling
└── quality/                  # Data quality checks
    ├── __init__.py
    ├── validator.py          # Schema & rule validation
    ├── profiler.py           # Data profiling
    └── alerts.py             # Quality alerting
```

## Pipeline Execution Model

Each pipeline follows the pattern:

```python
pipeline = KPISnapshotPipeline(database)
result = pipeline.run(since=last_run_timestamp, batch_size=1000, quality_check=True)
```

## Monitoring

All pipelines emit structured events to:
- `audit_events` table (for governance)
- Structured logs (for observability)
- Metrics counters (for alerting)

## Dead Letter Handling

Failed records are written to `.opencode/etl_dead_letter.jsonl` with:
- Original record
- Error message
- Stack trace
- Retry count
- Timestamp

Retry logic: exponential backoff (1m, 5m, 15m, 1h, 6h) max 5 attempts.
