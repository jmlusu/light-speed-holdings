# ADR — opencode.db schema duality: v2 vs v1 (P3-T1, DRAFT)

**Date:** 2026-11-08 · **Decider:** CTO (ADR required) · **Status:** DRAFT — no decision recorded

## Context

`session_part = 0` while `session_message = 9,284`; `blob`/`blob_ref = 0`
while 144 `file` parts carry inline base64; `job`/`schedule`/`session_inbox`
are 0 while `event_sequence = 3,530`. Every consumer joins both schemas.
v2 writers for parts/blobs/scheduling/events are either missing or
deliberately deferred.

## Options

- **A. Complete v2.** Recorder populates `session_part` from the same
  payloads (with the 64 KB cap + blob indirection), then readers cut over.
  Scope: writers + gap tests; consumer joins removed one at a time.
- **B. Freeze v1 as canonical.** Document `message`/`part` as authoritative,
  deprecate `session_part`; dual-schema query burden acknowledged as the
  cost of stability.

## Consequences until decided

Retention/VACUUM (P3-T4), project GC (P3-T3), orphan sweeper (P3-T2),
and blob migration (P2-T5) must all operate schema-agnostically (both
tables) — no silent continued ambiguity. Snapshot re-audits must report
both schemas explicitly.

## Decision

**Pending.** Owner: CTO. Recorded decisions must list follow-through
scope (tables, backfill-or-new-only, consumer joins).
