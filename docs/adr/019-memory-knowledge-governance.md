# ADR-019: Memory Knowledge Governance

**Status:** Accepted
**Date:** 2026-09-10
**Deciders:** Memory Owner, Knowledge Manager
**Technical Domain:** Memory / Continuous Learning

## Context

The continuous-learning pipeline (tickets #222-228) captures memory
automatically with no human review gate, but there are no rules governing
**what gets captured, how long it is retained, and how stale or
contradicted knowledge is prevented from polluting agent context**.

`MemoryStore` already has `prune(max_age_days, max_entries_per_type)` and
`consolidate_all()` (dedup, digest, aggregate), but the eligibility,
retention, staleness, conflict, and curator-override policies were implicit
or missing. Ticket #229 asks for an explicit policy layer.

Standing preference that constrains the design: **fully automatic capture
(no human review gate)**. Governance must therefore refine *what is stored
and retired*, not gate capture behind human approval.

## Decision

Add a data-first policy layer (`src/ai_company/memory/governance.py`,
default `MemoryGovernance`) consulted by the engine, encoding six rules:

### 1. Capture rules (what qualifies as knowledge)
- **Hard veto** — content matching the constitutional blocklist
  (`CONSTITUTIONAL_BLOCKLIST`) is never persisted. This is the only
  capture-time rejection.
- **Soft flag** — content shorter than `MIN_KNOWLEDGE_LENGTH` (40 chars)
  or carrying extraction-noise markers is persisted but flagged
  (`metadata.flagged = True`) so downstream tools can de-prioritise it.
- Everything else is captured automatically (no human gate).

### 2. Retention rules (TTL per memory type)
- `episodic`: 90 days (retired early because consolidation digests it into
  knowledge).
- `semantic` / `procedural`: 3650 days (knowledge lives until contradicted
  or superseded, not until the clock expires).
- `relational`: 730, `temporal`: 365, `aggregate`: 10950 (long-lived
  summaries).
- TTLs live in `MemoryGovernance.retention_ttl_days` and are overridable
  per deployment. `prune()` remains the enforcement point; `is_expired()`
  provides the predicate.

### 3. Staleness detection
- An entry never recalled within `staleness_days` (default 180) is marked
  `metadata.status = stale` during consolidation
  (`_flag_stale_entries`). Stale entries are kept (not deleted) so
  curators can review, but are labelled for de-prioritisation.

### 4. Conflict resolution
- When a new statement contradicts existing knowledge, newest wins by
  default; the loser is marked `status = superseded`.
- **Pinned entries win over newer ones** — a curator's explicit pin is the
  tie-breaker.
- Superseded and vetoed entries are excluded from `recall()` / `search()`
  so they cannot pollute agent context.

### 5. Human / curator override
- `knowledge_manager` can pin an entry (`store.pin(id)` / integration
  `pin_memory(id)`): pinned entries are exempt from age pruning, the
  per-type cap, and episodic digestion.
- Unpin restores normal lifecycle treatment.
- This is an explicit curator action, not a capture review gate.

### 6. Constitutional AI alignment
- `CONSTITUTIONAL_BLOCKLIST` is a small, explicit, human-reviewable list
  aligned with `ai_development_constitution/`. `is_constitutionally_blocked`
  drives the capture veto in rule 1.

## Alternatives Considered

### No policy layer (status quo)
- Memory grows unbounded, stale/superseded facts pollute context, curator
  has no way to preserve important memories.
- Rejected: ticket #229 exists precisely because this is broken.

### Human approval gate on every capture
- Guarantees quality but violates the standing "fully automatic capture"
  preference and would throttle the pipeline.
- Rejected: capture stays automatic; the veto+flag model achieves the same
  quality goals without blocking.

### Delete stale entries automatically
- Avoids stale-pollution but destroys possibly-recoverable knowledge with
  no review.
- Rejected: flag-then-review keeps the option of curator recovery.

### Scalar TTL for all types
- Simpler model, but episodic (digestible) and semantic (long-lived)
  memories have fundamentally different lifecycles.
- Rejected: per-type TTLs reflect how the pipeline actually consumes each
  type.

## Consequences

- `MemoryStore` constructor accepts an optional `governance`; defaults keep
  current behaviour for existing callers.
- New curator API: `MemoryStore.pin/unpin` + integration `pin_memory` /
  `unpin_memory` / `governance_summary`.
- `prune()` and `_digest_episodic()` skip pinned entries; `consolidate_all`
  now reports `stale_flagged` in its summary.
- `recall()` / `search()` exclude vetoed and superseded entries.
- Capture-time cost is a linear substring scan over a small blocklist —
  negligible.
- Policy is data-first: deployments override TTLs/blocklist in config
  without code changes.
