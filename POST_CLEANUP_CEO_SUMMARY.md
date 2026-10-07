# Post-Cleanup Verification — CEO Summary

**Date:** 2026-10-07
**Report HEAD:** `4bb64572` · **Baseline:** `cleanup/c0-baseline` = `048627ad` (4187 tracked files)
**Branch:** `feat/athena-archive-and-design-system` (in sync with origin)
**Predecessor audit:** `repo-audit/cleanup-status/CLEANUP_STATUS_REPORT.md` — 72/100, READY WITH CONDITIONS
**Full evidence:** [`POST_CLEANUP_VERIFICATION_REPORT.md`](POST_CLEANUP_VERIFICATION_REPORT.md) · [`POST_CLEANUP_EVIDENCE.json`](POST_CLEANUP_EVIDENCE.json)

---

## Verdict

> **READY WITH CONDITIONS — conditions narrowed from three open-ended items to one specific, testable fix.**

| # | Condition (predecessor audit) | Status |
|---|---|---|
| P0-1 | Working tree dirty at audit time | **OPEN — narrowed to 1 cause** |
| P0-2 | Full pytest not verified | **CLOSED** — 4 runs, 5 failures proven PRE-EXISTING, 0 real failures at HEAD |
| P0-3 | `open-design` submodule uninitialized | **CLOSED** — config-only fix |

| # | P1 finding | Status |
|---|---|---|
| P1-1 | Registry tool-vocabulary drift | **CLOSED** — 145/145 normalized, 0 residual, 0 card diffs |
| P1-2 | Phase approval records / runbook | **PARTIAL** — runbook landed; approval records cannot be fabricated |
| P1-3 | Brand/positioning edits uncommitted | **CLOSED** — landed, tagline consistent |
| P1-4 | "57× openai.yaml duplication" | **CLOSED — RETAIN** (zero duplication; the wording was wrong) |

**Scale:** 751 files changed · +6,372 / −71,486 · tracked files **4187 → 3705 (−482, −11.5%)**

---

## What was actually done

1. **P0-1 landing (`526f33d5`)** — committed the 97 cleanup-owned files that were sitting dirty in the working tree (+2,150/−13,524). Foreign changes were checked and **none** leaked into the commit.
2. **P1-1 (`16c69940`)** — normalized all 145 legacy tool names in `company-registry.yaml` to the canonical 7 (`write`→`edit` ×83, `execute`→`bash` ×49, `web_search`→`webfetch` ×11, `delegate`→`task` ×2). Regenerated all agents: **0 files changed, 0 diffs** — proving no permission surface moved.
3. **P1-2 (`56a42b27`)** — added `repo-audit/cleanup-status/CLEANUP_ROLLBACK_RUNBOOK.md` (234 lines): c0–c11 phase table, rollback procedures, authority matrix, and an honest provenance disclaimer. **Drill actually executed and passed** (branched to `cleanup/c7-large-tools`, verified, deleted the branch cleanly).
4. **Evidence capture** — four full pytest runs plus the command-derived proofs below.

**No push, no amend, no force-push, no stash, no history rewrite, no tag movement, no hand-edited agent cards.**

---

## The three P0s

### P0-2 · Full pytest verified — 5 failures are PRE-EXISTING ✅

Five tests in `tests/test_scraper_inventory.py` fail because `company/athena/*.jsonl` do not exist. Five independent proofs:

1. Root-cause commit `d2fa83aa` (2026-10-05 23:25) is an **ancestor of the baseline tag** → pre-dates cleanup. Exit 0.
2. `.gitignore:170 company/athena/` → the data **can never exist** in any clone; none on disk.
3. Last commit touching the test = `3e36b00c` (2026-09-28, pre-cleanup).
4. **Restore-and-rerun:** restoring the three files BOM-free → all 5 pass → restores deleted.
5. **Identical failure set across 3 independent runs.**

**Post-cleanup state (run 4, at `4bb64572`):** `1 failed, 2510 passed, 2 skipped` — and that single failure is a **documented flake**:

- `test_endpoint_response_time_p95` — timing assertion (`assert p95 < 200`)
- The project's own health gate **already excludes it by design** (`scripts/health_check.py:61`)
- Absent from runs 1–3; re-run in isolation **3/3 passed**

> **Suite real-failure count at report HEAD: 0.**

### P0-3 · Submodule initialized ✅
`git submodule status` → `6fd2f60 open-design`. **Config-only** (`git submodule init`); no commit. Fresh clones still need `git submodule update --init open-design` (in the runbook).

### P0-1 · Tree still dirty — but down to ONE cause ⚠️
The two original causes were: (a) cleanup-owned changes uncommitted, (b) test-suite residue.

- **(a) is discharged** by `526f33d5`.
- **(b) remains:** pytest rewrites `hr/onboarding_requests.yaml` on **every run** because `src/ai_company/orchestrator/hr.py:16` uses a CWD-relative path and `onboarding.py:280/283` rewrites the file. Only timestamps change.
- **The concurrent session's foreign changes have all landed** — nothing else blocks cleanliness.

**→ One action left. See D1 below.**

---

## Two things you should be told plainly

### 1. Someone deleted the failing tests — and the root cause is now untested
While this report was being written, the concurrent session committed:

```
4bb64572  test: drop scraper inventory tests missed by Athena archive
          tests/test_scraper_inventory.py | 176 lines deleted
```

This change **did not produce it and did not sweep it** (pathspec-scoped commits throughout). But you should know what it means:

> The 5 failures disappeared because **the tests were removed, not because the bug was fixed.** The fixture gap is now *untested* rather than *failing*.

It's a legitimate, candidly-messaged CI-unblocking move. It is recorded rather than left implicit — see **D3**.

### 2. Phase approval records genuinely do not exist
`CLEANUP_STATUS_REPORT.md` §1 already recorded them as "NOT FOUND anywhere in tree." They **cannot be closed by reconstruction** — creating them now would be fabricating evidence. The runbook is explicitly a *retrospective* reconstruction with a provenance disclaimer. See **D4**.

---

## Decisions required

| ID | Owner | Decision | Status |
|---|---|---|---|
| **D1** | Engineering | Stop pytest rewriting `hr/onboarding_requests.yaml` — temp path under pytest, or untrack it (already done for `approvals.yaml`/`memory-index.yaml` in `1f9944cf`). | **OPEN — sole remaining action** |
| **D3** | CEO | Note that the scraper-inventory tests were removed as a CI unblock, not fixed. Decide: reintroduce with a fixture, or formally retire the coverage. | **OPEN — noting** |
| **D4** | CEO | Sign the git-derived phase reconstruction as an after-the-fact record, **or** accept the gap and require contemporaneous records going forward. | **OPEN** |

---

## Recommendation

**Sign off on:** P0-2 (CLOSED), P0-3 (CLOSED), P1-1 (CLOSED), P1-3 (CLOSED), P1-4 (CLOSED — retain), and the P1-2 runbook.

**Hold open:** P0-1 (one action, D1) · P1-2 phase-approval records (D4).

**Do not treat** the deletion of `tests/test_scraper_inventory.py` as a fix (D3).

### Honest statement of limits

- Test results are reproduced, not memorised — raw logs preserved.
- 5 failures proven pre-existing from git evidence, **not** labelled as such by assertion.
- Skip-count drift (1 → 2) could not be attributed and is reported as an **open micro-observation**, not waved away.
- Cosmetic BOM in `526f33d5`'s subject line is **documented, not repaired** — repairing would rewrite 5 later shared, pushed commits.
- The rollback drill was executed and verified; the destructive end-to-end rollback was **not** run (needs your authority).

**Overall: READY WITH CONDITIONS.** Improvement over the predecessor's 72/100 — three open-ended conditions became one specific fix.
