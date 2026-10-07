# LIGHTSPEED CLEANUP — PHASE RECORDS & ROLLBACK RUNBOOK

**Prepared:** 2026-10-07 · **Status:** P1-2 closed (runbook added; §1 reconstruction signed off as an after-the-fact record — see §6)
**Governing process:** `docs/directives/LIGHTSPEED PHASED APPROVAL & ROLLBACK PROTOCOL.md`
**Companion evidence:** `CLEANUP_STATUS_REPORT.md`, `CLEANUP_EVIDENCE.json`, `CLEANUP_FILE_MANIFEST.txt`, `CLEANUP_STATUS_SUMMARY.md`

> **Provenance disclaimer — read first.** No contemporaneous approval records, phase-completion
> records, or change manifests were produced during the 2026-10-06 → 2026-10-07 cleanup
> (`CLEANUP_STATUS_REPORT.md` §1: "NOT FOUND anywhere in tree"). Everything in §1 below is a
> **retrospective reconstruction from git evidence** (tags, commit subjects, diffs, timestamps),
> captured on 2026-10-07. It records what *is verifiable*; it is **not** a substitute for
> approval paperwork that was never written, and no phase should be read as "approved" on the
> strength of this table alone. §2 onward (the rollback procedures) is actionable as written.
>
> **After-the-fact sign-off (2026-10-07, Human CEO).** The Human CEO has signed the §1 table as
> an *after-the-fact* record, closing the phase-approval sub-item of P1-2. This sign-off
> **ratifies the reconstruction**, it does not convert it into contemporaneous approval: the
> phases were still executed without prior authorisation records, and that fact is not erased.
> Going forward (P1-2 condition b), every phase must carry a contemporaneous approval record
> written *before* the phase begins.

**Standing policy for future phases (D4, adopted 2026-10-07):**

> Phase approvals, validation evidence, and rollback checkpoints must be captured
> contemporaneously and must not be reconstructed as historical facts after the event.

This policy applies to every phase after c11. It does not alter §1 above, which remains a
labelled retrospective reconstruction, and it does not create or imply any approval record for
the 2026-10-06 → 2026-10-07 cleanup itself.

---

## 1. Phase records (reconstructed from git)

**Signed off as an after-the-fact record by the Human CEO on 2026-10-07** (see the provenance
disclaimer above for what this sign-off does and does not establish).

**Tag inventory:** 14 tags — 12 `cleanup/*` (c0–c11) + 2 `backup/*`. All 14 are present and
resolvable; no tag points at a missing object.

**Range:** `cleanup/c0-baseline` (`048627ad`, 4187 tracked files) → HEAD (`c40decf0`, 3708
tracked files) = **754 files changed, +7359 / −71486**.

| Phase | Tag object | Target commit | Created (+0200) | Scope (per commit subject/tag message) | Rollback action |
|---|---|---|---|---|---|
| **c0 — baseline** | commit | `048627adef73f2d887a338ba88aca139ca312b7e` | 2026-10-05 23:40 | Pre-cleanup baseline: tsconfig paths + wrapper module types. 4187 tracked files. | **Rollback target of last resort** — restores the pre-cleanup repository |
| **c1 — secrets** | commit | `d107ba44ec6834a38fdf0682764250d873016f69` | 2026-10-06 21:43 | Secrets hardening: `.env.example` personal path + duplicates, `.gitignore` for QA/logs, untrack QA artifacts and runtime logs | `git revert d107ba44` — **do not do this lightly**: re-exposes tracked artifacts; requires CEO/CISO sign-off per §9.2 |
| **c2 — caches** | commit | `aaef778e5fbe7c01bbe08bff26d00baaa4316f8a` | 2026-10-06 23:14 | Purge caches and generated artifacts | `git revert aaef778e` (re-adds regenerable cache files only) |
| **c3 — root moves** | commit | `87dae04ab46fbea35d991d6e4d87e4a96973e938` | 2026-10-06 23:17 | Move root clutter into `docs/`, `reports/`, `scripts/` (141 renames) | `git revert 87dae04a` — large, reverses renames; prefer single-path restore (§3.4) |
| **c4 — scripts** | commit | `0690a16783b337fe44eb3e06349a7d4bb4a6adfe` | 2026-10-06 23:38 | Repair repo-root resolution after the scripts consolidation | `git revert 0690a167` — revert **only** if c3 is also reverted, else it breaks |
| **c5 — consolidation** | commit | `6b39ea44f6e4b323f448c9f6ffb52abc25eb970f` | 2026-10-06 23:40 | Archive superseded branding landing page | `git revert 6b39ea44` |
| **c6 — generated** | commit | `db06a21933fb0d9033a6b5aa4877bcb7abe405f4` | 2026-10-06 23:44 | Move backup output **outside** the repo (`scripts/deploy/backup.ps1` → `~/.lightspeed/backups`) | `git revert db06a219` — does **not** restore already-moved backup files (see §5) |
| **c7 — large tools** | commit | `c3d2002d6596d7e01157e6c8796d0c80ec7274fc` | 2026-10-06 23:46 | Remove retired `scroll-craft` corpus (~1 GB) | `git revert c3d2002d` — restores ~1 GB; confirm disk headroom first |
| **c8 — docs** | commit | `c3ec018497c3e7b074d2628bda6cb6c7ae4e879e` | 2026-10-06 23:49 | Post-cleanup documentation | `git revert c3ec0184` |
| **c9 — validated** | commit | `bbe174c4beedce7b8049a80ce404f34527645eac` | 2026-10-07 00:10 | Close the `repository-sanitization` ECL change | `git revert bbe174c4` (bookkeeping only) |
| **c10 — decommission** | commit | `b57c96fdf169d89ef82b9d4e7c0710c43db1b156` | 2026-10-07 01:05 | Close the `decommission-followups` ECL change | `git revert b57c96fd` (bookkeeping only) |
| **c11 — landing** | tag `7fdcd5f20faf1f78cf76213199b36481239c4800` | `526f33d54fa431f4e4a2712c3226781c81999cac` | 2026-10-07 03:34 | P0-1 landing: 97 cleanup-owned files (58 `.archive/athena/**` deletions, 20 brand/positioning/src modifications, 19 evidence notes) | `git revert 526f33d5` — restores the archived athena content and the pre-review brand baseline |

**Phase-range reverts (ordered, newest first):** reverting c11 alone leaves c1–c10 in place.
A full cleanup rollback is §3.2, not a loop over this table.

**Companion commits landing after c11 (not part of the tagged cleanup phases):**
`a1bdf5b5` (README LS-MEM fix) · `1f9944cf` (untrack live runtime state) · `552c6cb8`
(remove dated registry backup) · `93ade052` (docs health totals) · `16c69940` (P1-1 tool-vocabulary
normalization) · `98c1a535` (CI script paths) · `fdceab26` (archify IR regen). These are ordinary
commits on `feat/athena-archive-and-design-system` and are reverted individually if needed.

### 1.1 Backup tags (untouched by this document)

| Tag | Target | Created (+0200) | Protects |
|---|---|---|---|
| `backup/pre-strip-bulk-tag` | `22b7d0e2b1397dc74a37306968e5c3839c4d8063` | 2026-09-23 16:50 | State before the bulk-tag strip |
| `backup/pre-history-purge-one-skill` | `1f3120d290dbed143133a99a1fc30556a87048ac` | 2026-09-24 01:36 | State before the one-skill history purge |

**Never** move, delete, or re-point these tags.

---

## 2. Pre-rollback capture (mandatory)

Every rollback starts by recording the state you are about to leave. Do this from the repo root
(`C:\Users\jmlus\light-speed-holdings`):

```powershell
git status --short                     | Tee-Object pre-rollback-status.txt
git diff                               | Tee-Object pre-rollback.patch
git diff --cached                      | Tee-Object pre-rollback-staged.patch
git log --oneline -20                  | Tee-Object pre-rollback-log.txt
```

Save these **outside** the repository (e.g. `%TEMP%\lightspeed-rollback\`) so the capture itself
does not alter the tree you are about to roll back.

- Do **not** use `git stash` to park state: stashes are hidden state and are invisible to
  `git status`, which is exactly the failure mode this cleanup already documented.
- Do **not** amend, force-push, or rewrite history at any point. `526f33d5` carries a cosmetic
  BOM in its commit subject; it is recorded as-is and must not be "fixed" by amending, because
  amending would rewrite every commit after it.
- Do **not** push any rollback branch to a remote until the CEO has signed off.

---

## 3. Rollback procedures

### 3.1 Check out a phase (inspection only — no history change)

Use this to *inspect* a phase. It creates a branch, so nothing is lost.

```powershell
git switch -c inspect/c7 cleanup/c7-large-tools
git status --short          # expect: clean
git switch feat/athena-archive-and-design-system
git branch -d inspect/c7
```

### 3.2 Full rollback to a phase tag

```powershell
# 1. Capture current state first (§2)
# 2. Create the rollback branch — never detach HEAD on a shared branch
git switch -c rollback/c6-generated cleanup/c6-generated

# 3. Verify before going further
git status --short                       # clean
uv run ruff check src/
uv run mypy src/
uv run pytest -q
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
git status --short                       # generator must produce no diff
```

Promotion back onto the working branch, **only with CEO approval**:

```powershell
git switch feat/athena-archive-and-design-system
git merge --no-ff rollback/c6-generated     # NO --force, NO rebase onto rewritten history
```

### 3.3 Revert a single phase commit

```powershell
git revert --no-commit 526f33d5          # c11; use plain `git revert <sha>` to commit immediately
git status --short                       # review the reversal
uv run pytest -q
git revert --abort                       # if the review fails
```

Caveats:

- `c4-scripts` (`0690a167`) is a fix *for* `c3-root-moves` (`87dae04a`). Reverting either one
  without the other leaves the scripts tree inconsistent.
- `c1-secrets` (`d107ba44`) must not be reverted without CEO/CISO approval — it re-tracks QA
  artifacts and runtime logs that the cleanup untracked on purpose.

### 3.4 Restore one path from a phase tag (preferred for small rollbacks)

```powershell
git checkout cleanup/c0-baseline -- brand/tokens/brand-tokens.json
git commit -m "rollback: restore brand-tokens.json from cleanup/c0-baseline"
```

This is the lowest-risk rollback and the one to reach for first.

### 3.5 Submodule state (P0-3)

```powershell
git submodule init            # registers open-design in .git/config (local only, not a commit)
git submodule status          # expect: " 6fd2f60802232e0fdb29121a6b3e745d2fe9ff42 open-design (6fd2f60)"
git submodule update --init open-design    # populates the working content (fresh clones need this)
```

Rollback of P0-3 is unnecessary: the fix was config-only (`git submodule init`), it created no
commit, and the gitlink `6fd2f60` was already in HEAD before this session.

### 3.6 Post-rollback verification gate

A rollback is not complete until **all** of these pass and `git status --short` shows only the
state you intend:

```powershell
uv run ruff check src/
uv run mypy src/
uv run pytest -q
uv run python -c "from ai_company.generator import AgentGenerator; AgentGenerator().generate_all()"
pwsh scripts/maintenance/lint-ecl.ps1
git status --short
```

Note: `uv run pytest -q` rewrites `hr/onboarding_requests.yaml` timestamps (see §5). Discard that
diff with `git checkout -- hr/onboarding_requests.yaml` before judging tree cleanliness.

---

## 4. Rollback authority

| Action | Authority |
|---|---|
| Inspect a tag / create an `inspect/*` branch | Agent, no approval |
| Restore one path from a tag | Agent, with evidence in the change record |
| Revert a single non-secrets phase commit | CEO sign-off recorded in the change report |
| Full rollback to a phase tag (§3.2) | CEO sign-off **and** a written rollback record |
| Revert `c1-secrets` / touch `docs/APPROVED-VENDORS.md` | CEO **and** CISO (Jack Mlusu, Human CEO — `AGENTS.md` §9.2) |
| Push any rollback branch, force-push, amend, or rewrite history | **Prohibited** without explicit written CEO instruction |

---

## 5. What rollback does NOT restore

These are outside git and are silently unrecoverable through any procedure above:

1. **`.env` / `.env.local`** — untracked by design; rollback does not recreate or undo them.
2. **Runtime state** — `hr/onboarding_requests.yaml`, `orchestrator/approvals.yaml`,
   `orchestrator/memory-index.yaml`, `.opencode/inbox.json`. Note `approvals.yaml` and
   `memory-index.yaml` were *untracked* by `1f9944cf`; reverting that commit re-adds whatever
   content exists at the time, not the content that existed when it was untracked.
3. **Content already deleted outside the repo** — `c6-generated` moved backups to
   `~/.lightspeed/backups`; reverting the commit restores the *script path*, not prior backup files.
4. **Submodule working content on a fresh clone** — requires `git submodule update --init` (§3.5).
5. **External systems** — CI runs, Resend contacts/broadcasts, GitHub issues and labels, and any
   third-party state are never affected by, or restored by, a git rollback.
6. **The prior cleanup tags themselves** — `cleanup/c0`…`c11` and `backup/*` are immutable. A
   rollback creates new commits or new branches; it never re-points an existing tag.

---

## 6. Closure of P1-2

The original P1-2 finding was "**no phase approval records / manifests / rollback runbook**"
(`CLEANUP_STATUS_REPORT.md` §9, row P1-2). Status after this document:

| Sub-item | Status | Note |
|---|---|---|
| Rollback runbook | **CLOSED** | §2–§5 above, executable as written |
| Change manifest | **CLOSED** (pre-existing) | `CLEANUP_FILE_MANIFEST.txt` already covered this |
| Phase approval records | **CLOSED** — signed as an after-the-fact reconstruction (2026-10-07, Human CEO) | §1 signed off above. The reconstruction was never contemporaneous approval and the sign-off does not make it so; it accepts the gap for this cleanup and imposes option (b) going forward — every future phase must have an approval record written *before* it starts. |

Recorded as **P1-2 CLOSED** in `POST_CLEANUP_VERIFICATION_REPORT.md`.

---

## 7. Rollback drill (last verified)

| Check | Result | When |
|---|---|---|
| All 14 tags resolve to objects | PASS | 2026-10-07 |
| `cleanup/c11-landing` peels to `526f33d54fa431f4e4a2712c3226781c81999cac` | PASS | 2026-10-07 |
| `inspect/*` branch created and deleted cleanly | PASS | 2026-10-07 (this document's author) |
| `git diff cleanup/c0-baseline..HEAD --stat` reconstructible | PASS — 754 files, +7359/−71486 | 2026-10-07 |
| Post-rollback gate (`ruff`/`mypy`/`pytest`/generator/`lint-ecl`) | NOT RUN — no rollback performed | — |

The drill in this table confirms the *tag chain and diff are intact*, i.e. rollback is
theoretically possible. It does **not** claim a rollback has been executed end-to-end; §3.6 must
be run for that, and the final row is deliberately marked NOT RUN.
