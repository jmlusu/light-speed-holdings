# Implementation Plan: Concurrent-Session Conflict & Overwrite Protection (P0)

## Overview

Protect the repo's **agent-authored files** (source, docs, generated agents, `company/*.yaml`)
from concurrent-session conflicts and silent/unauthorised overwrites, and make both the
**audit trail** and the **file write path** cross-process safe.

The investigation (audit-trail-owner / dashboard-owner / security-architect) found the system
protects its *internal state files* (inbox, approvals, memories) but treats repo files as
single-writer assets. Confirmed gaps:

- `ToolRunner._write` is a bare `path.write_text()` — no lock, no ownership, no optimistic
  concurrency (`src/ai_company/executor/tool_runner.py:573-578`).
- `generator.py` writes agents/company YAML via bare `write_text()` at
  `:93,253,419,491,511,534,555` — concurrent `generate_all()` clobbers.
- `AuditWriter` is thread-safe, *not* process-safe — cross-process lost-update race silently
  drops audit events (`src/ai_company/audit/writer.py:122,229-275,194-223`).
- `AuditEvent` has no `session_id` / `file_changed` / content hashes — cannot detect or prove
  a clobber (`src/ai_company/audit/events.py:46-93`).
- The task lease is per-task only; no `claimed_files` ownership map
  (`src/ai_company/orchestrator/message_bus.py:271-334`).

## Architecture Decisions

- **D1 — Reuse the existing `FileStore` + `file_lock` primitives.** The repo already has a
  production cross-process sidecar lock (`src/ai_company/store/file_lock.py`) and an atomic,
  lock-safe, `.bak`-backed store (`src/ai_company/store/file_store.py`). P0 does **not**
  introduce a new lock library; it funnels raw writers through these.
- **D2 — Wrap ToolRunner's write in a small `repo_write` helper.** A dedicated guarded-write
  primitive (under `store/`) that (a) acquires the sidecar lock, (b) checks ownership,
  (c) does optimistic-concurrency CAS on a content digest, (d) writes atomically with `.bak`,
  and (e) records `before_hash`/`after_hash` for the audit trail. ToolRunner, generator, and
  CLI stores all call this same primitive (closes G1/G4/G5 with one code path).
- **D3 — Optimistic concurrency (CAS) enforced at tool level, PLUS hard-reject ownership.**
  A write refuses if the on-disk content differs from a caller-supplied expected digest
  (return `409 Conflict`). In addition, a write to a file claimed by a *different active*
  task/session is **hard-rejected** (`locked`/`busy`) — not advisory. The claimant can always
  write; only another active claimant or a CAS mismatch blocks. (Decision Q1: hard-reject.)
- **D6 — Session identity = root task.** `session_id` is derived from the **root of the task
  chain** (the top-level task that spawned the delegation lineage), not a new env var or a
  daemon start token. The executor already spawns subtasks from a parent via
  `_delegate` (`tool_runner.py:775-781`); `session_id` = lineage root, `task_id` = current
  task. (Decision Q2: task root.)
- **D7 — `bash` writes are audit-only for P0.** The allowlisted `bash` tool can still write
  files but cannot be CAS'd. P0 scope: record resulting file digests in the audit result
  metadata only — no lock/ownership enforcement. A future P1+ may add write-intent parsing.
  (Decision Q3: audit-only.)
- **D4 — Process-safe audit via a sidecar lock (not O_APPEND).** Keep the atomic
  temp+rename but guard it with a cross-process `file_lock` so two processes never both
  read-then-replace. This is minimal and preserves the existing rotation logic.
- **D5 — Audit schema extended backward-compatibly.** Add optional `session_id` and a
  `file_changed` metadata key and content digests. `model_config extra=ignore` means old
  readers ignore new fields; SQLite mirror uses plain `INSERT` (already `INSERT OR REPLACE` —
  see Task 1).
- **D6 — Session identity = root task.** See note above: `_delegate` (`tool_runner.py:775-781`)
  spawns subtasks from a parent; `session_id` = lineage root, `task_id` = current task.
  Thread `session_id` (root task) and `task_id`/`agent_id` (already received per-step at
  `run_plan`, `tool_runner.py:215-226`) plus the expected-digest through to `_write`.

## Task List

### Phase 1: Process-safe audit trail (prevent silent audit loss)

- [ ] **Task 1: Make `AuditWriter` cross-process safe + restore append-only SQLite mirror**
  - [ ] Guard `write_batch`/`_rotate` (read-modify-write + rotation) with the cross-process
        `store.file_lock` sidecar (`<audit>.lock`), short timeout + stale break.
  - [ ] Change `INSERT OR REPLACE` in `src/ai_company/data/audit_store.py:44` to plain
        `INSERT` to restore append-only semantics.
  - [ ] Add a multi-*process* test (two `AuditWriter` instances / subprocesses appending)
        asserting no event loss. Keep the existing thread test.
  - Files: `src/ai_company/audit/writer.py`, `src/ai_company/data/audit_store.py`,
    `tests/unit/test_audit.py`, `tests/integration/test_audit_cross_process.py`
  - Size: Medium
  - Depends: None

### Phase 2: Guarded write primitive + ToolRunner integration

- [ ] **Task 2: Add a guarded repo-write primitive (`repo_write` / `RepoWriter`)**
  - [ ] New module `src/ai_company/store/repo_write.py` exposing `write_file(path, content, *, expected_digest=None, owner=None)` that: acquires sidecar lock, reads current content + digest, compares against `expected_digest` (409 on mismatch), writes via `atomic_write`, creates `.bak`, and returns `{before_hash, after_hash, conflict: bool}`.
  - [ ] Digest = SHA-256 of file bytes (stdlib `hashlib`).
  - [ ] `read_file(path)` returns content + digest so callers can get a version to CAS against.
  - Files: `src/ai_company/store/repo_write.py`, `tests/unit/test_repo_write.py`
  - Size: Medium
  - Depends: None

- [ ] **Task 3: Route `ToolRunner._read`/`_write` through the guarded primitive (closes G1)**
  - [ ] `_read` returns the content digest alongside content.
  - [ ] `_write` accepts an optional expected digest; on mismatch returns a
        `409 Conflict` result instead of overwriting.
  - [ ] `_write` **hard-rejects** (returns `locked`/`busy`) a write to a file claimed by a
        different active task/session; the claimant always may write (decision Q1).
        Enforcement backend wired in Task 6.
  - [ ] `_write` records `before_hash`/`after_hash`/`file_changed` into the audit event's
        `metadata`/`result`.
  - [ ] Thread `task_id`/`agent_id`+`session_id` (root task, D6) and expected-digest into
        `_write` for ownership and audit context.
  - [ ] `bash` tool: audit-only (record file digests in the result metadata; no lock or
        ownership enforcement) per decision Q3.
  - Files: `src/ai_company/executor/tool_runner.py`, `src/ai_company/audit/integration.py`
  - Size: Medium
  - Depends: Task 2

### Phase 3: Centralise generator + CLI writers (closes G4/G5)

- [ ] **Task 4: Route `generator.py` bare `write_text` calls through the guarded primitive**
  - [ ] Replace the 6 bare writes (`:93,253,419,491,511,534,555`) with `repo_write`.
  - Files: `src/ai_company/generator.py`
  - Size: Small-Medium
  - Depends: Task 2

- [ ] **Task 5: Route CLI imperative stores through the guarded primitive**
  - [ ] Replace bare writes in `src/ai_company/cli/{specialists,sales,marketing,hr,legal,consulting}.py`.
  - Files: `src/ai_company/cli/*.py`
  - Size: Medium
  - Depends: Task 2

### Checkpoint: After Tasks 1-5
- [ ] `uv run ruff check src/ && uv run mypy src/ && uv run pytest`
- [ ] `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"`
- [ ] Cross-process audit test passes (no event loss)
- [ ] Manual: two processes `repo_write` same file with stale digest → second gets 409

### Phase 4: File ownership / lease (unauthorised overwrite)

- [ ] **Task 6: Extend the task lease with `claimed_files` ownership (closes G3)**
  - [ ] Add optional `claimed_files: list[str]` to the Task model / claim flow.
  - [ ] ToolRunner `_write` registers the target file against the claiming task and
        **hard-rejects** writes to a file claimed by a *different active* task
        (`busy`/`locked`) — decision Q1; the claimant always may write.
  - [ ] `session_id` for ownership = root task of the delegation lineage (decision Q2).
  - [ ] Clear/release claims on task completion/failure.)
  - Files: `src/ai_company/models/models.py`, `src/ai_company/orchestrator/message_bus.py`,
    `src/ai_company/executor/tool_runner.py`, `src/ai_company/executor/loop.py`
  - Size: Large — **split into 6a/6b (below)**
  - Depends: Tasks 3

  *Slicing:* split Task 6 into:
  - **Task 6a**: Add `claimed_files` field + CAS-safe `claim`/`release` on MessageBus
    (wire in the executor tick); `session_id` = root task.
  - **Task 6b**: ToolRunner ownership enforcement (hard-reject foreign-claim writes;
    claimant always allowed) against the `claimed_files` registry.

### Phase 5: End-to-end audit integrity + validation

- [ ] **Task 7: Extend `AuditEvent` with `session_id` + emit session/start events + content digests**
  - [ ] Add optional `session_id` (populated from the **root task** of the delegation chain,
        decision Q2) and a `session` event family (`SESSION_START`/`SESSION_END` emitted at the
        root-task boundary).
  - [ ] Ensure `file_changed` + `before_hash`/`after_hash` are recorded on write events
        (wired from Task 3).
  - Files: `src/ai_company/audit/events.py`, `src/ai_company/audit/integration.py`
  - Size: Small-Medium
  - Depends: Task 3

- [ ] **Task 8: Drift / integrity sweep to surface unrecorded overwrites**
  - [ ] A lightweight check comparing on-disk content hashes against the audit ledger for
        tracked written files; report mismatches (aligns with doctor drift-detection role).
  - [ ] Wire as a `doctor`/governance check (best-effort).
  - Files: `src/ai_company/security/` or `src/ai_company/diagnostics/`, `tests/`
  - Size: Medium
  - Depends: Task 7

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] `uv run ruff check src/ && uv run mypy src/ && uv run pytest` clean
- [ ] Generated agents remain valid (`generate_all` + validation)
- [ ] Manual two-session simulation: second writer blocked (409 / ownership) or provable via audit
- [ ] Review with human before merging

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Windows lock robustness (`_pid_alive` always True → mtime-only stale detection) | Med | Existing heartbeat mitigates; confirm short timeout + heartbeat; add lock-contention warning surface (P2, non-P0) |
| CAS 409 could surprise single-session flows if callers don't pass expected digest | Med | Keep expected-digest optional; when absent, fall back to locked write (no CAS) but still record hashes |
| Hard ownership enforcement (Task 6) could deadlock/regress normal single-session exec | Med | The claimant always may write its own claimed files; hard-reject fires only on *foreign* active claims or CAS mismatch. Add `session_id` trace to audit to diagnose any false positives |
| Adding `session_id` to audit could break existing JSONL consumers | Low | `model_config extra=ignore`; fields optional with defaults; SQLite mirror + reader remain backward compatible |
| `generator.py` writes are fast-path and ubiquitous | Low | `repo_write` is cheap (single SHA-256 + lock); benchmark not required |
| Splitting Task 6 into 6a/6b could drift contracts | Med | Define Task model field + MessageBus API first, then ToolRunner enforcement |

## Resolved Decisions (from review)

- **Q1 — ownership enforcement: HARD-REJECT.** A write to a file claimed by a different
  active task/session is rejected (`busy`/`locked`); the claimant always may write. Not
  advisory, no config flag for P0.
- **Q2 — `session_id` source: TASK ROOT.** `session_id` = root of the task chain (top-level
  task that spawned the delegation lineage), not a new env var / daemon token.
- **Q3 — `bash` writes: AUDIT-ONLY for P0.** The allowlisted `bash` tool records resulting
  file digests in the audit result metadata only — no lock/ownership/CAS enforcement.

## Verification Commands

- `uv run ruff check src/`
- `uv run mypy src/`
- `uv run pytest`
- `python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"`
