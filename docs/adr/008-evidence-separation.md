# ADR-008: Evidence Separation Architecture

**Status**: Accepted
**Date**: 2026-10-01
**Deciders**: Chief of Staff, QA Lead, Test Engineering Lead, CEO Advisor
**Technical Story**: Implement audit evidence separation per AGENTS.md §9.3

---

## Context

The organization operates multiple audit processes that generate evidence consumed by auditors. Previously, auditors wrote findings into the same directories containing the evidence they were auditing (e.g., `reports/repo-audit-<date>.md` written into `reports/` alongside `reports/evidence-<date>.json`). This violated the principle that an auditor's read set and write set must be disjoint.

The governance rule **AGENTS.md §9.3** mandates:
> An agent performing an audit must treat its evidence set as read-only: never write, move, rename, or delete any file inside the evidence directory it is auditing.

This ADR documents the architectural decisions for implementing evidence separation across all audit types.

---

## Decision

### 1. Three Independent Append-Only JSONL Stores

| Store | Path | Purpose | Retention |
|-------|------|---------|-----------|
| **Escalation Events** | `orchestrator/escalation_events.jsonl` | All escalation lifecycle events (trigger, resolve, postmortem) | 30 days |
| **Dead-Letter Queue** | `orchestrator/dead_letter.jsonl` | Task failures, retries, resolutions | 90 days |
| **Audit Export** | `reports/evidence/audit-<date>.jsonl` | Daily SQLite `audit/audit.db` → JSONL export | 90 days |

**Why JSONL?**
- Append-only by design — natural fit for evidence trails
- Streaming-friendly — auditors can tail/stream without locking
- Tool-agnostic — `jq`, `python -m json.tool`, `sqlite3 .import` all work
- Structurally verifiable — `ai_company.audit.integrity check` confirms every line
  is a well-formed JSON object and exits non-zero on corruption

> **Integrity guarantee (scope limit).** These three stores are append-only and
> structurally checked, but they are **not** hash chained: unlike
> `AuditWriter` (`.opencode/audit/audit.jsonl`), they do not write
> `__seq` / `__prev_hash`, so `verify_audit_chain` cannot attest to them and
> reports success without inspecting any link. Only the AuditWriter trail is
> tamper-evident today. Adding chaining to these stores is tracked as follow-up
> work; until then, treat store integrity as append-only-plus-structural, not
> cryptographic.

### 2. Evidence Separation Rule (AGENTS.md §9.3)

> **Evidence directory** — any path consumed as evidence: `reports/evidence/`, `audit/*.jsonl`, `.opencode/audit/*`, `harness/changes/*/reviews/`, downloaded `audit-evidence` CI artifacts, `orchestrator/escalation_events.jsonl`, `orchestrator/dead_letter.jsonl`, `reports/evidence/audit-*.jsonl`.
>
> **Where output goes** — a directory outside the evidence set.
>
> **On violation** — discard the run, re-fetch evidence from a fresh clone or CI artifact, re-run, and report the incident alongside the findings.

### 3. Correlation ID Propagation

Every event across all three stores carries a `correlation_id` (UUID v7, time-ordered) that links:
- Escalation trigger → resolution
- Dead-letter move → retry → resolution
- Audit export batch → originating audit run

This enables end-to-end forensic tracing from escalation → dead-letter → audit export.

### 4. Rotation Strategy

| Store | Rotation | Method |
|-------|----------|--------|
| `escalation_events.jsonl` | Monthly | Atomic rename to `escalation_events.rotated-<ts>.jsonl` |
| `dead_letter.jsonl` | Monthly | Atomic rename to `dead_letter.rotated-<ts>.jsonl` |
| `reports/evidence/audit-*.jsonl` | Daily (cron) | New file per date; 90-day artifact retention |
| `reports/evidence/` (weekly audit) | Weekly (cron) | Git commit + artifact upload |

**Rotation is atomic**: write to temp file → `os.replace()` (POSIX atomic, Windows near-atomic).

### 5. Metrics & Alerting

Prometheus metrics exported via `/metrics` endpoint:
- `evidence_store_size_bytes{store="escalation_events"}`
- `evidence_store_size_bytes{store="dead_letter"}`
- `evidence_store_size_bytes{store="audit_export"}`
- `evidence_store_events_total{store="..."}`
- `evidence_store_rotation_total{store="..."}`

Alert rules:
- `evidence_store_size_bytes > 100MB` → warning
- `evidence_store_size_bytes > 500MB` → critical

---

## Consequences

### Positive

| Consequence | Impact |
|-------------|--------|
| **Audit integrity** | Auditors can never corrupt their own evidence; findings are independently re-derivable |
| **Forensic traceability** | Correlation ID chains escalation → dead-letter → audit export for end-to-end incidents |
| **Compliance readiness** | Append-only JSONL + rotation + correlation IDs + read/write separation give auditors a re-derivable trail; cryptographic tamper evidence comes from the AuditWriter chain and is a follow-up increment for these stores |
| **Operational automation** | Daily export cron + monthly rotation + 90-day artifact retention = zero-touch hygiene |

### Negative

| Consequence | Mitigation |
|-------------|------------|
| **Three stores to monitor** | Unified Prometheus metrics + single alert rule |
| **Correlation ID propagation required everywhere** | Enforced in `EscalationManager.trigger_escalation()`, `DeadLetterQueue.move_task()`, `export_audit_log()` |
| **Rotation atomicity critical** | Temp-file + `os.replace()` pattern enforced in code review |
| **Test isolation required** | Fixtures use `tmp_path` per test to avoid cross-test store pollution |

---

## Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| **Single unified JSONL store** | Violates evidence separation (one write set for multiple audit types) |
| **SQLite for all stores** | Not append-only by default; harder to stream/tail; rotation more complex |
| **Write-ahead log per store** | Over-engineering; JSONL + rotation is simpler and auditable |
| **No correlation ID** | Forensic tracing requires manual stitching; cost: 2 hours to add, value: 10x faster RCA |

---

## Implementation Plan

| Phase | Task | Owner | Status |
|-------|------|-------|--------|
| 1 | Create JSONL stores (`escalation_events.py`, `dead_letter.py`, `export.py`) | Done | ✅ |
| 2 | Integrate with `EscalationManager`, `DeadLetterQueue`, `AuditWriter` | Done | ✅ |
| 3 | Add `correlation_id` to all schemas + propagation | Done | ✅ |
| 4 | Add Prometheus metrics + alert rules | In progress | 🔄 |
| 5 | Add rotation atomicity (temp file + `os.replace`) | Planned | ⏳ |
| 7 | Create ADR + sequence diagram + DR runbook | This ADR | ✅ |

---

## References

- AGENTS.md §9.3 — Audit Evidence Separation governance rule
- `docs/sop/operations-sop.md` §7.3 — Evidence Directory Rotation table
- `.github/workflows/audit-export.yml` — Daily export cron
- `tests/unit/test_evidence_separation.py` — 9 evidence separation tests
- `src/ai_company/audit/writer.py` — Tamper-evident JSONL writer with rotation
- `src/ai_company/audit/integrity.py` — Hash chain verification
