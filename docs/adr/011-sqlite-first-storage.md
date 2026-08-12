# ADR-011: SQLite-First Storage and Memory Engine

**Status:** Accepted
**Date:** 2026-08-12
**Deciders:** CTO, Wayfinder
**Technical Domain:** Storage & Memory Engine

## Context

Requirement T3 demands PostgreSQL + Redis + a vector DB with sub-50ms retrieval.
The current runtime is single-machine and file-first by design (ADR-002,
ADR-005): JSON stores (`.opencode/inbox.json`, `audit.jsonl`, `memory/`) plus a
SQLite database (`data/ai_company.db`) that is already the operational read
layer for the dashboard. The SQLite schema explicitly replaces the legacy files
("Tasks (replaces .opencode/inbox.json)", "Audit events (replaces
.opencode/audit.jsonl)"). A local cosine `VectorStore` + sentence-transformers
`EmbeddingEngine` provide best-effort semantic retrieval with no external DB.

Standing posture (wayfinder map charting Q2/Q3): single-machine-first — keep
SQLite + files as the core; PostgreSQL/Redis/vector infra opt-in via
docker-compose only where a feature truly needs it; performance metrics are
reported targets, not acceptance gates.

## Decision

1. **Canonical store: SQLite-first.** SQLite (`data/ai_company.db`) is the
   canonical operational store for tasks, audit events, memory index, and
   analytics. JSON files under `.opencode/*` and `memory/` are retained as the
   human-readable interchange + backup/source-of-truth for human-authored
   content, and are still parsed for backwards compatibility. PostgreSQL /
   Pgvector / Redis stay opt-in behind the existing `Database` / `VectorStore`
   interfaces (docker-compose), added only when a feature truly needs them.
   ADR-005 is not superseded; ADR-011 formalizes what is already de-facto true.
2. **Memory retrieval path: local cosine by default.** Semantic retrieval uses
   SQLite/file-backed entries + the in-process cosine `VectorStore`. The
   "sub-50ms retrieval" figure is a **reported target**, evidenced by a
   report-only benchmark (`tests/unit/test_memory_retrieval_perf.py`, marked
   `performance`, never a CI gate). A Pgvector/Qdrant adapter behind the
   `VectorStore` interface is the escape hatch if the local path demonstrably
   cannot hold the target under scale.
3. **`.opencode/*` migration: read-compatible, opt-in mirror.** Existing
   `.opencode/*` data is **not** force-migrated. It stays readable; new writes
   go through the store layer. An opt-in, non-destructive CLI command
   (`ai-company storage import-opencode`) mirrors legacy JSON into SQLite
   (idempotent `INSERT OR REPLACE`) for anyone who wants it consolidated.

## Consequences

- **Positive:** preserves single-machine, no-external-services posture; uses the
  SQLite layer that already exists and is exercised by the dashboard; no data
  loss or destructive migration; gives a concrete migration path without
  forcing it; T3's infra is deferred behind a measured target.
- **Negative / risk:** fan-out retrieval beyond the in-process index is not
  pre-built; if sub-50ms at very large memory volumes cannot be met by local
  cosine, a second decision (opt-in Pgvector/Qdrant) is required. SQLite and
  JSON can drift if a writer touches one and not the other; the dashboard and
  stores must keep using the same paths (data root resolution via
  `ai_company.paths`).
- **Neutral:** `.opencode/*` remains the human-readable interchange; the mirror
  command makes the split manageable for single-user operators.

## Links

- Ticket: #36 Decide the storage and memory engine (decision record)
- Map: #33 Wayfinder: mission-control dashboard spec
- ADR-002: JSON MessageBus
- ADR-005: File-based Persistence vs Database
- ADR-010: T1 Event-Bus Alignment with the File-Based MessageBus
- Evidence: `tests/unit/test_memory_retrieval_perf.py`, `src/ai_company/cli/storage.py`
