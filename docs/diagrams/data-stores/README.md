# Data Stores Diagrams

Comprehensive diagrams for all databases and file stores in the Light Speed Holdings AI Company Builder.

## Diagrams

1. **[overview.mmd](overview.mmd)** - High-level view of all databases and file stores, showing storage abstractions (FileStore, Database) and their relationships
2. **[schema-ai_company.mmd](schema-ai_company.mmd)** - ERD of `data/ai_company.db` showing all tables, fields, and relationships
3. **[file-stores.mmd](file-stores.mmd)** - Detailed view of all file-based stores (JSON, JSONL, YAML) organized by type
4. **[data-flow.mmd](data-flow.mmd)** - Sequence diagram showing data flow between components and stores

## Database Summary

- **Main SQLite DB**: `data/ai_company.db` (Schema v5) with 11 tables + 2 FTS5 indexes
- **SQLite-backed stores**: TaskStore, AuditStore, EscalationStore, KPIPipeline, CostAnalytics, AgentPerformanceAnalytics
- **File stores**: JSONL audit trails, JSON workflow instances, Athena JSONL data, configuration YAML/JSON files

## File Store Characteristics

- **FileStore** (`src/ai_company/store/file_store.py`): Atomic writes, cross-platform file locking, automatic backups (`.bak`), corruption quarantine/recovery
- **AthenaStore** (`src/ai_company/athena/store.py`): File-backed JSONL with per-file locking

All Mermaid diagrams can be viewed in GitHub, VS Code (with Mermaid extension), or at [mermaid.live](https://mermaid.live/).
```
