# Branch and Worktree Inventory — Wed Nov 11 2026

**Repository:** `C:\Users\jmlus\light-speed-holdings`
**Action taken:** Deleted `docs/operational-runbook` branch (zero unique commits, fully merged into `main`, not checked out anywhere).

---

## 1. Local branches (3)

| Branch | HEAD | Tracking | Status |
|---|---|---|---|
| `main` | `8b42cbc5` | `origin/main` | **Checked out** in main repo. 47 modified files + 1 untracked in working tree (see §2). |
| `feat/competitive-landscape-nov-refresh` | `7f2f63d6` | `origin/feat/competitive-landscape-nov-refresh` | Checked out in main repo. **13 commits ahead of `main`**, **7 commits ahead of its remote tracking branch**. Contains phased Portal work (Phase 2 + Phase 3) plus two reverted commits that were later re-reverted. **Do not delete while checked out.** |
| `docs/operational-runbook` | *deleted* | — | Deleted per user request. Had zero unique commits on `main`. |

---

## 2. Working tree state of `main` checkout

**Dirty entries:** 47 `M` + 1 `??`

**Modified files (subset shown for brevity):**
- `.github/workflows/ci.yml`
- `M .pre-commit-config.yaml`, `AGENTS.md`, `AUDIT_REPORT.md`, `docs/ARCHIFY-USAGE.md`, `docs/IMAGE_SPEC.md`, `docs/MEDIA_ARCHITECTURE.md`, `docs/Pharos/...`, `docs/SKILL_CURATION_POLICY.md`, etc.
- `harness/changes/INDEX.json`, `harness/changes/parking/...`
- `open-design` (submodule)
- `src/ai_company/presentation/pipeline.py`, `presentation_templates/`, `prompts/presentation.md`
- `src/components/Icon3D.tsx`, `Home/HighLevelOverviewSection.tsx`, `pages/HAOMTGVPage.tsx`
- `tasks/about-tasks.md`, `tasks/spec-about-page.md`, `tasks/website-transformation/plan.md`
- `src/ai_company/prompts/presentation.md`

**Untracked:** `CREATIVE_ENGINE_CONSOLIDATION_SUMMARY.md`

---

## 3. Remote tracking branches (10 — `origin/`)

| Remote branch | HEAD | Notes |
|---|---|---|
| `origin/main` | `8b42cbc5` | — |
| `origin/security/ignore-confidential-proposals` | `78f0ed14` | Maps to worktree `stellar-mountain`; security proposal branch. |
| `origin/chore/land-parked-work` | `1ee905aa` | **102 commits not in `main`**. Stale from 2026-09-23. **Not safe to delete.** |
| `origin/chore/restore-local-work` | `da40cf18` | **89 commits not in `main`**. Stale from 2026-09-23. |
| `origin/chore/session-cleanup-commits` | `7666319f` | Docs(knowledge): record subagent framework and provider key CI fix. |
| `origin/feat/competitive-landscape-nov-refresh` | `0717fed0` | Remote tracking for the local feature branch. |
| `origin/feat/use-cases-live-filters` | `77f6c10f` | **87 commits not in `main`**. Stale from 2026-11-01. |
| `origin/feature/token-optimization` | `3fc6ff12` | **86 commits not in `main`**. Stale from 2026-11-01. |
| `origin/fix/pr556-557` | `f7662af3` | **92 commits not in `main`**. Stale from 2026-11-04. |
| `origin/HEAD` → `origin/main` | — | — |

**None of the five stale remote branches (land-parked-work, restore-local-work, feat/use-cases-live-filters, feature/token-optimization, fix/pr556-557) should be deleted without explicit review**, as each holds 86–102 commits of real work not present in `main`.

---

## 4. Worktrees (18 total under `C:\Users\jmlus\.local\share\opencode\worktree\9930fa`)

| Worktree | HEAD | Branch | Dirty | Notes |
|---|---|---|---|---|
| `calm-rocket` | `0717fed0` | detached HEAD | 0 | On `origin/feat/competitive-landscape-nov-refresh` tip content |
| `clever-pixel` | `8b42cbc5` | detached HEAD | 0 | On `main` |
| `clever-river` | `25820f4e` | detached HEAD | 0 | On `origin/main` (pre-main-advance commit) |
| `curious-river` | `8b42cbc5` | detached HEAD | **94** | On `main`; 94 dirty entries |
| `eager-harbor` | `8b42cbc5` | detached HEAD | 0 | On `main` |
| `hidden-tiger` | `0c7e8710` | detached HEAD | 0 | Phase 2 shared components commit |
| `mighty-engine` | `8b42cbc5` | detached HEAD | 0 | On `main` |
| `mighty-planet` | `f40c5ff9` | detached HEAD | 0 | Ahead of main (unpushed) |
| `neon-canyon` | `71946677` | detached HEAD | 0 | Phase 3 commit; this session's original worktree |
| `quick-star` | `25820f4e` | detached HEAD | 0 | On `origin/main` |
| `stellar-falcon` | `8b42cbc5` | detached HEAD | **1** | On `main`; 1 dirty entry |
| `stellar-mountain` | `78f0ed14` | `security/ignore-confidential-proposals` | 0 | Maps to remote branch `origin/security/ignore-confidential-proposals` |
| `stellar-star` | `25820f4e` | detached HEAD | 0 | On `origin/main` |
| `sunny-cactus` | `8b42cbc5` | detached HEAD | 0 | On `main` |
| `swift-forest` | `8b42cbc5` | detached HEAD | **1** | On `main`; 1 dirty entry |
| `swift-rocket` | `0c7e8710` | detached HEAD | 0 | Phase 2 commit |
| `witty-canyon` | `25820f4e` | detached HEAD | 0 | On `origin/main` |

**Summary by HEAD commit:**
- `8b42cbc5` (main): 9 worktrees — `calm-rocket`, `clever-pixel`, `eager-harbor`, `mighty-engine`, `stellar-falcon`, `sunny-cactus`, `witty-canyon`, plus the main repo itself. 3 of these (`curious-river`, `stellar-falcon`, `swift-forest`) have 1+ dirty entry.
- `25820f4e` (origin/main before advance): 4 worktrees — `clever-river`, `quick-star`, `stellar-star`, `witty-canyon`. All clean.
- `0c7e8710` (Phase 2): 2 worktrees — `hidden-tiger`, `swift-rocket`. All clean.
- `71946677` (Phase 3): 2 worktrees — `neon-canyon` (this session), `calm-rocket`. All clean.
- `78f0ed14` (security/ignore-confidential-proposals): 1 worktree — `stellar-mountain`. Clean, maps to remote branch.
- `f40c5ff9`: 1 worktree — `mighty-planet`. Clean, unpushed ahead of main.

**No worktree owns a named branch** — all are detached HEAD. The "clean up branches" precondition from the prior session does not apply here, as these are not branch-referenced worktrees.

---

## 5. What was cleaned up

- **`docs/operational-runbook` local branch** deleted. Had zero unique commits relative to `main`; was fully merged.

**Nothing else was deleted, moved, or committed.** The 5 stale remote branches (`origin/chore/land-parked-work`, `origin/chore/restore-local-work`, `origin/feat/use-cases-live-filters`, `origin/feature/token-optimization`, `origin/fix/pr556-557`) remain intact, as each holds 86–102 commits not in `main` and requires deliberate review before any prune operation.

---

## 6. Pending items (not acted upon)

| Item | Reason |
|---|---|
| Delete/prune 5 stale remote branches | Each holds 86–102 commits of real work not in `main`; requires review |
| Clean 94 dirty entries in `curious-river` worktree | Would lose local modifications; needs manual review |
| Address 47 modified files in `main` checkout | Working tree dirty; may include intentional changes |
| Collapse `feat/competitive-landscape-nov-refresh` into `main` | Feature branch has 13 unique commits ahead of main; content may overlap but history differs |
