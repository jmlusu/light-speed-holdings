# opencode.db — P0 Containment Runbook (F-01 → F-09)

**Date:** 2026-11-08 · **Owners:** ciso (F-01/F-03/F-04/F-05/F-06),
devsecops-lead (F-09), cio (F-02) · **Approver:** Human CEO (CISO of record)

All steps are outside-workspace operations. **Do not execute any step
without a fresh snapshot** (`opencode-snapshot.ps1`) and, where the step
mutates the DB, a maintenance window with OpenCode closed. Rollbacks are
noted per step; global rule: no rollback re-exposes data.

## F-01 — ACL lockdown

Verified 2026-11-08 (read-only): `icacls` on
`C:\Users\jmlus\.local\share\opencode` still shows the orphaned
`S-1-5-21-…-1003 (I)(OI)(CI)(RX)` ACE. Remove it, break inheritance, and
re-assert owner-only on the directory, `opencode.db*`, `auth.json`,
`mcp-auth.json` (see `opencode-db-security-fix-2026-11-08.md` §4).
Verify with `icacls`; no `…-1003` line anywhere.

## F-02 — Encryption at rest

Decision pending (CEO + CIO, Open Question 3): BitLocker (preferred,
whole-volume) vs EFS on the data directory. Status verified 2026-11-08:
`cipher /c opencode.db` → `U` (unencrypted); `manage-bde` is not
permitted in this session (access denied) so volume status is **unknown**.
Rollback warning: decrypting requires a compensating control and
re-encryption within 24 h or CEO escalation.

## F-03 — `.bak` disposition

38,533,844,992 B (2026-11-01). Restore-test to a scratch location (or
record a formal CEO waiver) before deletion. Preferred end state:
delete after the WAL checkpoint proves v2 stable; alternative:
encrypted cold archive. Script: `opencode-db-bak-disposition.ps1`
(dry-run default).

## F-04 — Credential rotation

Treat all 22 `credential` rows as plaintext until vendor docs prove
otherwise (P0-T3 determination: **cannot verify encryption from
available evidence** — no value-level list is produced, by design).
Rotate provider-side (never SQL UPDATE on the live DB), then replace via
the supported UI/CLI; rotate every `.env` value reachable via `read`/
`bash` (309 reads baseline); log fingerprints only (last-4 + SHA-256
prefix, never values). Rotation is irreversible; never revert to an old
key.

## F-09 — WAL checkpoint + VACUUM

Maintenance window only: snapshot → `PRAGMA wal_checkpoint(TRUNCATE)`
(busy must be 0) → `VACUUM` (needs ~DB-size free space; freelist is
~8 MB so vacuum alone reclaims little — archive live rows first, F-10).
Scripts: `opencode-wal-checkpoint.ps1` (dry-run default),
`opencode-db-maintenance.ps1`.

## Maintenance window (4 h booked, 1 h buffer)

`Get-PSDrive` free > 12 GB → snapshot → checkpoint → orphan sweep
(`sweep-orphaned-tool-calls.ps1 -Apply`) → temp sweep
(`sweep-temp-opencode.ps1 -Apply`) → project GC dry-run → VACUUM
decision → reopen + smoke test. Abort = restore from the pre-fix
snapshot; verify `integrity_check = ok` + counts match the pre-window
snapshot.
