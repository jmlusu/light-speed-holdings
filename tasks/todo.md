# Implementation Task List: Concurrent-Session Conflict & Overwrite Protection (P0)

> Full detail: `tasks/plan.md`

## Resolved decisions (locked in)
- Q1: ownership enforcement = **hard-reject** (foreign active claim → `locked`/`busy`; claimant always allowed)
- Q2: `session_id` = **root task** of the delegation lineage
- Q3: `bash` writes = **audit-only for P0**

## Phase 1: Process-safe audit trail
- [ ] Task 1: Make `AuditWriter` cross-process safe + restore append-only SQLite mirror
- [ ] (Verify) Multi-process audit append test passes, no event loss

## Phase 2: Guarded write primitive + ToolRunner
- [ ] Task 2: Add guarded `repo_write` / `RepoWriter` primitive (lock + CAS + hashes)
- [ ] Task 3: Route `ToolRunner._read`/`_write` through it (CAS 409 + hard-reject foreign claim, hash audit; `bash` audit-only)

## Phase 3: Centralise generator + CLI writers
- [ ] Task 4: Route `generator.py` bare writes through the primitive
- [ ] Task 5: Route CLI stores (`cli/*.py`) through the primitive

## Checkpoint: After Tasks 1-5
- [ ] `ruff check src/` + `mypy src/` + `pytest` clean
- [ ] `AgentGenerator().generate_all()` valid
- [ ] Manual: stale-digest second write returns 409; foreign-claim write returns `locked`

## Phase 4: File ownership / lease (hard-reject)
- [ ] Task 6a: Add `claimed_files` field + CAS-safe claim/release on MessageBus; `session_id` = root task
- [ ] Task 6b: ToolRunner ownership enforcement (hard-reject foreign-claim writes)

## Phase 5: Audit integrity + validation
- [ ] Task 7: Extend `AuditEvent` with `session_id` (root task)/session events + content digests
- [ ] Task 8: Drift / integrity sweep to surface unrecorded overwrites

## Checkpoint: Complete
- [ ] All acceptance criteria met, full verification green
- [ ] Manual two-session simulation: second writer hard-blocked or provable via audit
