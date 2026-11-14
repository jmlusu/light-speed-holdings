# ADR — opencode.db schema duality: v2 vs v1 (P3-T1)

**Date:** 2026-11-08 · **Decider:** CTO (decision approved per 2026-11-08 tasking: “v2 complete”) · **Status:** APPROVED — Option A (Complete v2)

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

Option A — Complete v2 (approved). The OpenCode recorder populates `session_part`
from the same payloads (with the 64 KB cap + blob indirection), then readers
cut over. Scope: writers + gap tests; consumer joins removed one at a time.

- **Tables:** `session_part` (+ `blob`/`blob_ref` indirection for `file`
  parts, hash pointer only). v1 `part` stays authoritative until the writer
  is proven on ≥1 window's worth of new-session data.
- **Backfill-or-new-only:** **new-only.** No 670k backfill. Only sessions
  created after the upstream writer ships route to `session_part`.
- **Checkpoint:** the first new session after the upstream release must
  satisfy `SELECT COUNT(*) FROM session_part WHERE session_id = <new id> > 0`;
  only then flip the canonical flag (v1 deprecated) in a follow-up commit.
- **Ownership (upstream-owned, not a repo patch):** the
  `session`/`session_message`/`session_part` writers live in the upstream
  OpenCode application (`~/.local/share/opencode/opencode.db`), not in
  `src/ai_company/`. This repo cannot patch the upstream recorder in-tree.
  **Upstream tracking ticket for the OpenCode recorder (`session_part`
  writer) is required** — see
  `reports/opencode-db-retention-close-2026-11-08.md` §3 (not filed in this
  session: shell stalled, `gh` unreachable; ticket text recorded there and
  to be filed upstream before the checkpoint can pass).
