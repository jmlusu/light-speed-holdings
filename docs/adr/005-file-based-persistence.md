# ADR-005: File-based Persistence vs Database

**Status:** Accepted
**Date:** 2026-07-17
**Deciders:** CTO, Lead Engineer
**Technical Domain:** Data Persistence

## Context

AI Company Builder needs to persist:
- Agent definitions (27 agents across 7 departments)
- Task queue (JSON-backed MessageBus)
- Approval requests and decisions
- Escalation events
- Scheduled tasks
- Postmortem records
- Memory entries (6 types)
- Knowledge graphs (4 types)
- Cost tracking logs
- Configuration (19 YAML files)

The persistence layer must:
- Work without external services (no database server)
- Be human-readable and editable
- Support the expected data volume (<1000 tasks, <100MB total)
- Be easy to backup and version control
- Integrate with Pydantic models

## Decision

We use **file-based persistence** with a mix of JSON, YAML, and JSONL formats.

## File Layout

```
company/                          # Configuration (YAML + JSON)
  agent-registry.json             # 27 agent definitions
  models.yaml                     # LLM provider config
  departments.yaml                # 7 departments
  workflows.yaml                  # 9 workflow definitions
  config/kpis.yaml                # 28 KPI definitions

orchestrator/                     # Operational state (YAML + JSON)
  inbox.json                      # Task queue (JSON array)
  approvals.yaml                  # Pending approval requests
  escalation.yaml                 # Escalation events
  scheduler.yaml                  # Scheduled recurring tasks
  postmortems/                    # Incident postmortems (YAML per incident)

memory/                           # Agent memory (JSON per type)
  episodic.json
  semantic.json
  procedural.json
  relational.json
  temporal.json
  aggregate.json

results/                          # Operational logs (JSONL)
  cost_log.jsonl                  # LLM cost tracking records

.opencode/                        # Generated outputs (Markdown + YAML)
  agents/*.md                     # 27 agent definition files
  config/*.yaml                   # Derived configuration
```

## Options Considered

### 1. File-based (JSON + YAML + JSONL) (chosen)

**Pros:**
- Zero infrastructure — works on any machine
- Human-readable — `cat`, `grep`, `jq` for debugging
- Git-friendly — diffs show exactly what changed
- Simple backup — `cp -r` covers everything
- Pydantic native — `.model_dump()` serializes directly
- Format-appropriate — JSON for structured data, YAML for config, JSONL for logs

**Cons:**
- No concurrent access without file locking
- No indexed queries (filtering done in Python)
- No referential integrity enforcement

### 2. SQLite

**Pros:**
- ACID transactions
- Concurrent read access
- SQL queries for complex filtering
- Single-file storage

**Cons:**
- Not human-readable without tools
- Schema migrations for model changes
- Harder to version control (binary file)
- Requires `sqlite3` integration

### 3. PostgreSQL

**Pros:**
- Full ACID, concurrent access
- Rich querying (JSONB, full-text search)
- Production-grade

**Cons:**
- Requires running a database server
- Connection management complexity
- Overkill for expected data volume
- Adds deployment complexity

### 4. Redis

**Pros:**
- Excellent performance
- Built-in data structures
- Atomic operations

**Cons:**
- Requires running a server
- Data not persistent by default
- Not human-readable
- Overkill for this use case

## Consequences

### Positive

- **Simplicity**: No database setup, no migrations, no connection pools
- **Debuggability**: `cat orchestrator/inbox.json | python -m json.tool` for instant inspection
- **Portability**: Entire system state is a directory tree that can be copied, backed up, or version controlled
- **Testing**: Tests use temporary directories with real files (no mocking databases)
- **Auditability**: Git history shows every change to every configuration and state file
- **Format flexibility**: JSON for API data, YAML for configuration, JSONL for append-only logs

### Negative

- **Concurrency**: Single-writer model (mitigated: orchestrator and executor run as single processes)
- **Querying**: No indexed queries (mitigated: data volume is small, Python filtering is fast enough)
- **Referential integrity**: Not enforced at the storage layer (mitigated: validated at the model layer via Pydantic)

### Mitigations

- `Pydantic` models validate data integrity on read/write
- `RegistryLoader` validates cross-references between agents, departments, and workflows
- File locking via `fcntl`/`msvcrt` available if concurrent access is ever needed
- Future migration to SQLite is straightforward — change the storage layer, keep the models

## Performance Characteristics

| Operation | Expected Volume | Latency |
|-----------|----------------|---------|
| Task queue read/write | <100 tasks | <5ms |
| Agent registry load | 27 agents | <10ms |
| Memory search | <1000 entries | <50ms |
| Cost log append | <1000 entries/day | <1ms |
| Config load (19 YAMLs) | 19 files | <100ms |

All operations are well within acceptable latency for a CLI tool with a web dashboard.

## Evidence

- Current system state: ~50 files, <10MB total
- 466 tests pass using temporary file fixtures
- Dashboard API reads state from files on each request (<50ms p99)
- `orchestrator/inbox.json` handles the expected task throughput comfortably

## References

- `src/ai_company/orchestrator/message_bus.py` — JSON-backed task queue
- `src/ai_company/memory/engine.py` — JSON-backed memory store
- `src/ai_company/llm/cost_tracker.py` — JSONL cost log
- `src/ai_company/registry/loader.py` — YAML config loading
- `docs/ARCHITECTURE.md` — Data flow and file layout
