# opencode.db — Blob-storage migration design (P2-T5)

**Date:** 2026-11-08 · **Owner:** cto (review: cto + ciso) · **Status:** DESIGN ONLY

144 inline-base64 `file` parts (57 sessions) inflate `part.data` JSON;
`blob`/`blob_ref` are empty. New attachments must go to `blob`/`blob_ref`
at write time with only the content hash in `part.data`; dedup is then
free (same image twice = one `blob` row, hash PK).

## Decisions before implementation

1. **Backfill vs new-only.** Recommended: new-only + cold archive of
   the 144 historical payloads (byte-length assertion
   `blob.bytes == decoded length` on the snapshot clone first).
   In-place backfill of live `part.data` needs a versioned migration +
   audit note (never a silent rewrite).
2. **Binary fidelity.** `blob.data` is `BLOB`; backup/restore tooling
   must preserve binary — verify the `.backup` round-trip on a clone.
3. **Privacy.** Blobs still retain bytes; moving them out of
   `part.data` removes them from text scans but not from the corpus.
   Retention (F-10) still applies.

## Acceptance (when scheduled)

- Reader/writer gap tests pass for new data; `SELECT COUNT(*) FROM blob`
  equals distinct-hash count (≤144 for history); zero remaining inline
  payloads; `PRAGMA integrity_check = ok`.
- Blocked on the P3-T1 v2 decision (which schema's writers own blobs).
