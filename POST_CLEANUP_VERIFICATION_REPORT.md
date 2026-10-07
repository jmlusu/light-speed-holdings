# POST-CLEANUP VERIFICATION REPORT

**Package:** `POST_CLEANUP_VERIFICATION_REPORT.md` · `POST_CLEANUP_EVIDENCE.json` · `POST_CLEANUP_CEO_SUMMARY.md`
**Prepared:** 2026-10-07 · **Branch:** `feat/athena-archive-and-design-system` · **Evidence HEAD:** `4bb64572`
**Final HEAD after decision closure:** `363c1aec` (+ this commit) · **Baseline:** tag `cleanup/c0-baseline` = `048627ad` (2026-10-05 23:40 +0200)
> **Note:** F1–F9 compliance corrections land in a later commit whose SHA will be restated by `FINAL_CLEANUP_SIGNOFF.md`.
**Predecessor:** `repo-audit/cleanup-status/CLEANUP_STATUS_REPORT.md` (HEAD `be7d1848`, readiness 72/100, READY WITH CONDITIONS)

**Method:** every P0/P1 condition from the 2026-10-07 cleanup audit was re-tested against the live
repository with reproducible commands. Findings are classified as CLOSED / OPEN / PRE-EXISTING /
PARTIAL **only** where git history, file contents, or a validation run supports the label —
never by inspection alone (`AGENTS.md` §9). Nothing in this report was inferred from a filename,
a doc claim, or a prior report's assertion.

---

## 1. Verdict

| ID | Condition | Verdict | Evidence |
|---|---|---|---|
| **P0-1** | Working tree dirty at audit time | **CLOSED** | Fixed at `tests/unit/test_onboarding.py` (D1); full `pytest` now leaves the tree **byte-clean** — 2511 passed / 0 failed, `hr/onboarding_requests.yaml` hash unchanged (§3.3, run 5) |
| **P0-2** | Full `pytest` not verified | **CLOSED** | Full suite run **5×**; 2585→2580 tests; 5 failures proven **PRE-EXISTING** with git-history + restore-and-rerun evidence (§4); 1 historical failure is a **documented flake** (§4.6) |
| **P0-3** | `open-design` submodule uninitialized | **CLOSED** | `git submodule init` → `git submodule status` clean at `6fd2f60` (§5) |
| **P1-1** | Registry tool-vocabulary drift | **CLOSED** | `16c69940`: 145/145 legacy lines normalized, 0 residual, 0 agent-card diffs on regenerate (§6.1) |
| **P1-2** | No phase approval records / manifests / rollback runbook | **CLOSED** | Runbook added (`56a42b27`); manifest pre-existed; §1 reconstruction **signed by the Human CEO as an after-the-fact record** on 2026-10-07 (D4, §6.2) |
| **P1-3** | Uncommitted brand-token + positioning edits | **CLOSED** | Landed in `526f33d5`; tagline verified consistent across 4 source files (§6.3) |
| **P1-4** | 57× `openai.yaml` duplication unexamined | **CLOSED** | All 57 files examined: **57 unique SHA256 = zero duplication**; retain, no action (§6.4) |

**Overall: READY — all seven conditions discharged.**
P0-2, P0-3, P1-1, P1-3 and P1-4 were already closed with evidence. P0-1 closed on run 5: the
test-suite rewrite that was the sole remaining cause is fixed at source, so a full suite run no
longer dirties the tree. P1-2 closed on the CEO's after-the-fact sign-off of the §1 reconstruction
(D4), with the standing condition that future phases carry contemporaneous approval records.
The 5 deleted scraper-inventory tests are **formally retired** (D3, §4.7) — not restored.

---

## 2. Scope and provenance

**In scope:** the three P0 conditions and four P1 findings raised by the 2026-10-07 audit, the
evidence package requested for CEO sign-off, and the three CEO decisions taken afterwards
(D1 fix `hr/`, D3 retire the deleted tests, D4 sign the reconstruction — §11).

**Deliberately out of scope** (governing decisions for this change):

- No architecture redesign; no replacement of the 5-tier permission model; no changes to the 90-agent roster.
- No history rewrite, no `git push`, no amend, no force-push, no stash created.
- No hand-editing of generated agent cards (`.opencode/agents/*.md` are generator output only).
- No edits to the audit's original evidence files, and no restore of the five deleted tests (D3 chose retirement).
- The only test edit is the D1 fixture fix in `tests/unit/test_onboarding.py` (§3.2) — one file, two
  constructor arguments, no runtime/source default changed.
- No sweeping of concurrent-session changes into this change's commits (`AGENTS.md` §7).
- No deletion or deduplication of the 57 `openai.yaml` files (P1-4 decided *examine + report only*).
- Backup and cleanup tags never moved or re-pointed.

**Governing process:** `docs/directives/LIGHTSPEED PHASED APPROVAL & ROLLBACK PROTOCOL.md`;
`AGENTS.md` §§7–9.

**Commits produced by this change:**

| Commit | Purpose |
|---|---|
| `526f33d5` | P0-1 landing of cleanup-owned Class A/B working-tree changes (97 files) |
| `16c69940` | P1-1 tool-vocabulary normalization in `company-registry.yaml` |
| `56a42b27` | P1-2 phase records + rollback runbook |
| tag `cleanup/c11-landing` | annotated tag object `7fdcd5f2` → `526f33d5`, message fixed |
| `d507c1ab` | the three root-level deliverables |
| `c40decf0` | deliverable fix-up (stale two-causes framing in §3/§3.1) |
| *(this commit)* | D1 fixture fix, D3 retirement records, D4 sign-off, decision closure |
| `363c1aec` | D4 standing policy adopted in the rollback runbook ('Standing policy for future phases (D4, adopted 2026-10-07)'); decision-closure follow-up commit |

---

## 3. P0-1 — Working tree cleanliness · **CLOSED**

Two independent causes existed when this change began. **One cleared by itself** (§3.1 — all
concurrent-session changes landed) and **one was fixed at source** (§3.2 → D1, proven clean by
run 5 in §3.3).

### 3.1 Concurrent-session changes (excluded by decision, now landed)

The repository has a second active session. Per the standing instruction *“proceed, exclude foreign
changes,”* only this change's Class A/B set was committed; the other session's changes were left
untouched throughout and subsequently landed under their own commits (`98c1a535`, `fdceab26`,
`93ade052`, `4bb64572`, …).

At the time this change's commits were made, the tree carried foreign state that was **never
swept**:

```
Staged:      deleted:    tests/test_scraper_inventory.py     ← foreign, landed in 4bb64572 (§7.1)
Unstaged:    modified:   docs/AGENT-REGISTRY-TABLE.md        ← foreign, landed
             modified:   docs/REPOSITORY_HEALTH.md           ← foreign, landed in 4bb64572
             modified:   scripts/health_check.py             ← foreign, landed in 4bb64572
             modified:   hr/onboarding_requests.yaml         ← §3.2 test residue, STILL DIRTY
```

Every commit from this change was pathspec-scoped (`git commit -F <msg> -- <paths>`) after
re-checking `git status --short`, so no foreign line entered any of its commits.

**Status after D1:** P0-1 is **CLOSED**. The sole remaining tracked modification was
`hr/onboarding_requests.yaml`, fixed at source in §3.2; run 5 (§3.3) leaves the tree byte-clean.

### 3.2 The test suite rewrites a tracked file — root cause (now fixed, D1)

`uv run pytest` used to make the tree dirty on **every** run. Root cause, established by
bisection rather than inspection:

- `src/ai_company/hr/onboarding.py:343` → `OnboardingManager.__init__(..., data_dir="hr")`,
  a CWD-relative default; `_RequestStore(data_dir)` then writes `hr/onboarding_requests.yaml`.
- `tests/unit/test_onboarding.py:55` (`manager` fixture) and `:71` (`_make_manager`) constructed
  `OnboardingManager` **without `data_dir`**, so they hit that default and rewrote the tracked
  file. (`tests/unit/test_unified_onboarding.py` already passed `data_dir=str(tmp_path)` and was
  clean — confirmed by running each file against a restored baseline.)
- Effect was timestamp-only: `created_at` / `updated_at` rewritten; content otherwise identical.
- Last committed by unrelated PR #412 (`5ab90eda`, 2026-10-04).

**Bisection evidence:** with the baseline hash recorded, the three candidate files were run
individually against a restored `hr/onboarding_requests.yaml` —
`test_dashboard_integration.py` CLEAN, `test_onboarding.py` **DIRTIES**, `test_unified_onboarding.py`
CLEAN. The two offending constructions were then given `data_dir=str(tmp_path / "hr")`.

**Fix (D1):** `tests/unit/test_onboarding.py` now passes `data_dir` at both construction sites.
No runtime/source default was changed, the file remains tracked, and no `.gitignore` entry was
added — the fix is scoped to the test that caused the write.

### 3.3 Run 5 — proof P0-1 is closed

| Run | When (local) | HEAD | Result | Time | Tree after |
|---|---|---|---|---|---|
| **5** | 2026-10-07, after D1 fix | **`c40decf0`** | **0 failed, 2511 passed, 2 skipped, 67 deselected** | **411.15 s** | **CLEAN — `hr/onboarding_requests.yaml` SHA256 unchanged** |

Run 5 is the first run in this change to exit 0 **and** leave the working tree clean. The only
path dirty afterward was `tests/unit/test_onboarding.py` itself (the fix, unstaged at run time).

---

## 4. P0-2 — Full test suite · **CLOSED · 5 failures PRE-EXISTING**

### 4.1 Runs

| Run | When (local) | HEAD | Result | Time |
|---|---|---|---|---|
| 1 | 2026-10-07 03:03→03:08 (saved: `%TEMP%\opencode\pytest-full.log`) | `be7d1848` lineage | **5 failed, 2512 passed, 1 skipped, 67 deselected** | 253.88 s |
| 2 | 2026-10-07, after `16c69940` | `16c69940` | **5 failed, 2511 passed, 2 skipped, 67 deselected** | 303.55 s |
| 3 | 2026-10-07, at this change's final HEAD | **`56a42b27`** | **5 failed, 2511 passed, 2 skipped, 67 deselected** | **311.68 s** |
| **4** | 2026-10-07 04:05, after concurrent commit `4bb64572` | **`4bb64572`** | **1 failed, 2510 passed, 2 skipped, 67 deselected** | **287.76 s** |
| **5** | 2026-10-07, after D1 fix | **`c40decf0`** | **0 failed, 2511 passed, 2 skipped, 67 deselected** | **411.15 s** |

Runs 1–3 totalled **2585** collected (5 + passed + skipped + 67 deselected), matching the audit's
figure exactly. Runs 4–5 total **2580** — exactly 5 fewer, because `4bb64572` deleted the five
scraper-inventory tests (§4.5, retired per D3 in §4.7). Exit code 1 in runs 1–4, **0 in run 5**.

### 4.2 The five failures — identical in all three runs

```
FAILED tests/test_scraper_inventory.py::test_scrape_jobs_jsonl_is_valid
FAILED tests/test_scraper_inventory.py::test_jobs_jsonl_is_valid
FAILED tests/test_scraper_inventory.py::test_user_profiles_jsonl_is_valid
FAILED tests/test_scraper_inventory.py::test_inventory_covers_all_jsonl_datasets
FAILED tests/test_scraper_inventory.py::test_scraper_script_dirs_reporting_matches_filesystem
```

All five raise `FileNotFoundError` for `company/athena/{jobs,scrape_jobs,user_profiles}.jsonl`.

### 4.3 Classification: **PRE-EXISTING** — five independent lines of evidence

1. **Root cause predates the cleanup.** The data was removed by `d2fa83aa` (*“feat: archive Athena,
   add design system, …”*, 2026-10-05 23:25 +0200), which **is an ancestor of `cleanup/c0-baseline`**
   (`git merge-base --is-ancestor d2fa83aa cleanup/c0-baseline` → exit 0). The tests were already
   broken before phase c1 began.
2. **The data can never be present.** `.gitignore:170` contains `company/athena/`, so
   `jobs.jsonl`, `scrape_jobs.jsonl` and `user_profiles.jsonl` are untracked and absent on disk —
   and would be absent in any fresh clone. The failures are structural, not incidental.
3. **No cleanup commit touched the test or its fixture.** `git log -- tests/test_scraper_inventory.py`
   last shows `3e36b00c` (2026-09-28, SCR-02) — predates c0.
4. **Restore-and-rerun proves causation.** Temporarily restoring the three `.jsonl` files (BOM-free)
   at the ignored path made **all five tests pass**; the temporary restores were then deleted and the
   directory confirmed clean. The failure is *caused by* the missing data, not by any code change.
5. **Identical set across all three runs**, including the run at report HEAD.

**Not labelled “pre-existing” on assertion alone** — every claim above is command-derived.

### 4.4 Skips

Both skips are conditional-by-design and reproduce:

| Test | Skip reason | Root cause |
|---|---|---|
| `tests/memory/test_git_safety.py:109` | `"LS-MEM package not yet created"` | `src/ai_company/lsmem` removed by `42284c54` (*refactor(memory): decommission LS-MEM engine*, 2026-10-07 00:49) — an approved cleanup-lineage commit and an ancestor of `be7d1848` |
| `tests/docs/test_doc_drift.py:223` | `"No static source file"` | Parametrized over `docs/source-of-truth.yaml`; exactly **1** claim carries `source: dynamic` (manifest last changed `5ab90eda`, 2026-10-04) |

**Open micro-observation (recorded, not resolved):** run 1 reported **1** skip, runs 2–3 report **2**.
No commit between run 1 and run 3 touched `tests/` or `docs/source-of-truth.yaml`
(`git log --since='2026-10-07 03:00' -- tests/ docs/source-of-truth.yaml` → empty), so the delta of
one parametrized/environment-conditional skip **cannot be attributed from git evidence alone**. It is
classified **non-material**: the collected total (2585), the deselect count (67) and the failure set
(5, identical) did not change. This is reported as an unexplained observation rather than waved off.

### 4.5 State change between runs 3 and 4 — the five tests were deleted, not fixed

Between run 3 and run 4 the concurrent session committed:

```
4bb64572 2026-10-07T04:02:46+02:00  LSAI Remediation Bot
test: drop scraper inventory tests missed by Athena archive
 tests/test_scraper_inventory.py | 176 ---------------------- (deleted)
 scripts/health_check.py         |  35 +++++----
 docs/REPOSITORY_HEALTH.md       |   5 +-
```

Its message is candid and correct about the history: *“The Athena archive (`d2fa83aa`) deleted
`company/athena/*.jsonl` and the Athena unit tests but missed `tests/test_scraper_inventory.py`,
leaving the required Test (ubuntu/windows) jobs red on every branch commit.”*

**Assessment:**

- The **failures are gone because the tests are gone.** The root cause — no
  `company/athena/{jobs,scrape_jobs,user_profiles}.jsonl` fixture — is **unchanged**: the commit
  adds no data, and `.gitignore:170` still excludes the directory, so the data still cannot exist
  in a clone.
- The classification in §4.3 stands: those five failures **were** pre-existing. Run 4 does not
  overturn that; it removes the observer.
- This change **did not make or stage this deletion** (§7.1) and takes no credit for it. The
  deletion resolves the *red CI* symptom, which is a legitimate goal, but it is a **test-removal
  decision, not a bug fix** — and it should be recorded as such rather than absorbed silently.
- **P0-2's evidence therefore has two valid bases:** the pre-existing classification from runs 1–3
  (file present, root cause proven), and the post-deletion state at run 4.

### 4.6 The one remaining failure in run 4 — documented flake, not a regression

```
FAILED tests/performance/test_dashboard_performance.py
       ::TestAPIPerformance::test_endpoint_response_time_p95[/api/v1/dashboard]
```

| Evidence | Result |
|---|---|
| Assertion under test | `assert p95 < 200` — a **timing** threshold (`test_dashboard_performance.py:85`) |
| Project's own health gate excludes it **by design** | `scripts/health_check.py:61` → `-k "not test_endpoint_response_time_p95"` inside `check_pytest()` |
| Did it fail in runs 1–3? | **No** — grep of both saved logs returns no occurrence |
| Re-run in isolation ×3 (10 parametrized cases each) | **3/3 passed** — `10 passed in 9.16s`, `9.60s`, `8.49s` |
| Commit `4bb64572` reference | “keeping the documented endpoint perf-flake exclusion” |

**Classification: KNOWN FLAKE.** Three independent lines of support: the project already excludes
this test from its own health check, it passed in every earlier full run, and it passed 3/3 in
isolation immediately after failing under full-suite load. It is load-sensitive, not a regression
introduced by any commit in this change or in `4bb64572`.

**Net state of the suite at report HEAD `4bb64572`: 0 real failures.**
1 failure = documented flake; 5 previous failures = removed by test deletion; root cause of the 5
remains unaddressed and is now **untested** rather than merely failing.

**Run 5 (§3.3) confirms:** `0 failed, 2511 passed` — the flake did not recur, and the suite now
exits 0.

### 4.7 D3 — the five deleted tests: **TESTS RETIRED**

`tests/test_scraper_inventory.py` (176 lines, 5 tests) was deleted by the concurrent session in
`4bb64572`. CEO decision **D3 = formally retire the coverage** (not restore it).

| Check | Result |
|---|---|
| Deleted tests | `test_scrape_jobs_jsonl_is_valid`, `test_jobs_jsonl_is_valid`, `test_user_profiles_jsonl_is_valid`, `test_inventory_covers_all_jsonl_datasets`, `test_scraper_script_dirs_reporting_matches_filesystem` |
| Why restoration was rejected | The data they assert against (`company/athena/*.jsonl`) is **gitignored** (`.gitignore:170`) and can never exist in a clone. Restoring the tests would require inventing a fixture — asserting against fabricated data tests less than it appears to. |
| Dangling references cleared | `docs/wayfinder/map2-scraper-discovery-gap-analysis.md` and `docs/superpowers/plans/2026-09-28-wayfinder-map2-scraper-discovery-gap-analysis.md` updated to state the file is retired, so no future agent is sent to run a test that no longer exists |
| Prior record | `docs/REPOSITORY_HEALTH.md:43` already records `RESOLVED 2026-10-07 — module removed` |
| Coverage gap | **Accepted, explicit:** the scraper-inventory JSONL contract (3 datasets + script-dir reporting) is now **unguarded**. If scraper work resumes, re-derive coverage against data that is actually tracked. |

`company/athena/` is gitignored (`.gitignore:170`) and absent from disk, so the five retired tests could never pass in a fresh clone — effective passing coverage for this contract is zero, and the scraper inventory remains unguarded until tracked fixtures exist.

---

## 5. P0-3 — Submodule `open-design` · **CLOSED**

```
$ git submodule init                       → exit 0
$ git submodule status
  6fd2f60802232e0fdb29121a6b3e745d2fe9ff42 open-design (6fd2f60)
```

- The gitlink `6fd2f60` was **already present in HEAD**; only `.git/config` registration was missing.
- On-disk submodule content matched `6fd2f60` exactly — no checkout, no fetch, no commit required.
- The fix is **config-only**: it creates no commit and appears in no diff.
- **Residual (documented, not a blocker):** a fresh clone still needs
  `git submodule update --init open-design`. Recorded in the rollback runbook §3.5.

---

## 6. P1 findings

### 6.1 P1-1 — Registry tool vocabulary · **CLOSED** (`16c69940`)

| Check | Result |
|---|---|
| Legacy lines in `company-registry.yaml` | **145 found → 145 replaced → 0 residual** (`write`→`edit` 83, `execute`→`bash` 49, `web_search`→`webfetch` 11, `delegate`→`task` 2) |
| Unchanged lines | 3993 — byte-identical; encoding LF, no BOM |
| Registry tool counts after | `read` 90 · `edit` 83 · `grep` 65 · `list` 65 · `bash` 50 · `webfetch` 18 · `task` 4 (**375 total, 0 legacy**) |
| **Regenerate agent cards** | `AgentGenerator().generate_all()` → exit 0, **0 changed files** under `.opencode/agents/` and `company/` |
| Generated cards | **0** legacy tool lines |
| `ruff check src/` | All checks passed |
| `mypy src/` | no issues found in **225** source files |

Zero card diffs is the decisive proof: the registry now normalizes to the canonical 7
(`AGENTS.md` §8) and the generator produced identical output, so no agent's permission surface moved.

**Follow-on (reported, deliberately not changed):** legacy tool names remain in two out-of-scope
locations — `company/registry-templates/consulting-firm/company-registry.yaml` (30 lines across 5
tracked template files, referenced only by two docs) and `hr/onboarding_requests.yaml` (2 lines,
runtime data). The template file was outside the agreed P1-1 scope (`company-registry.yaml` only).

### 6.2 P1-2 — Phase approval records / manifests / rollback runbook · **CLOSED**

New: `repo-audit/cleanup-status/CLEANUP_ROLLBACK_RUNBOOK.md` (`56a42b27`) — phase table c0–c11
reconstructed from git, rollback procedures (pre-rollback capture, tag inspection, full phase
rollback, single-phase revert, per-path restore, submodule state, post-rollback gate), rollback
authority matrix, and an explicit “what rollback does NOT restore” section.

| Sub-item | Status |
|---|---|
| Rollback runbook | **CLOSED** |
| Change manifest | **CLOSED** — `CLEANUP_FILE_MANIFEST.txt` pre-existed |
| Phase approval records | **CLOSED — signed as an after-the-fact reconstruction (D4)** |

**D4 executed 2026-10-07 (Human CEO):** the runbook's §1 reconstruction is signed off as an
after-the-fact record, choosing option (a) of the two the runbook offered. The sign-off is
recorded in the runbook's provenance disclaimer and §1 header, and §6 there now reads CLOSED.

**What the signature does and does not establish** (kept explicit so the record stays honest):

- It **does** accept the git-derived §1 table as the after-the-fact record for this cleanup,
  closing P1-2's third sub-item.
- It **does not** convert a retrospective reconstruction into contemporaneous approval. The
  cleanup phases were still executed without prior approval paperwork, and that fact stands.
- **Standing condition (option b, imposed by this decision):** every future phase must carry an
  approval record written *before* the phase begins. This is now the repo's obligation, not an
  observation.

The runbook carries this policy as the block **"Standing policy for future phases (D4, adopted
2026-10-07)"** (`CLEANUP_ROLLBACK_RUNBOOK.md`, landed in `363c1aec`).

**Tag inventory verified:** 14 tags resolve — 12 `cleanup/*` (c0–c11) + 2 `backup/*`.
`cleanup/c11-landing` = annotated tag `7fdcd5f20faf1f78cf76213199b36481239c4800` →
peeled `526f33d54fa431f4e4a2712c3226781c81999cac`, message intact (1036 bytes, newlines preserved,
no U+FEFF in the message).

### 6.3 P1-3 — Brand tokens / positioning edits · **CLOSED**

The uncommitted edits landed in `526f33d5`. The reported staleness does not reproduce — the tagline
is consistent across every source checked:

| File | Value |
|---|---|
| `brand/tokens/brand-tokens.json:6` | `"tagline": "ASPIRE. ACT. ACHIEVE."` |
| `src/data/siteContent.ts:41` | `tagline: 'ASPIRE. ACT. ACHIEVE.'` |
| `src/data/siteContent.ts:47` | `thesis: 'Aspire. Act. Achieve.'` (sentence case, intentional) |
| `docs/NARRATIVE-AND-POSITIONING.md` | consistent at L19, L33, L58, L86 |

No edit made. The original issue was uncommitted work, which the landing commit resolved.

### 6.4 P1-4 — 57× `openai.yaml` duplication · **CLOSED (report-only, RETAIN)**

| Check | Result |
|---|---|
| Files matching `.agents/skills/**/agents/openai.yaml` | **57** |
| Distinct SHA256 | **57 — zero duplication** |
| Size range | 94–363 bytes |
| Structure | `interface` 57/57; `policy` 48/57 (`allow_implicit_invocation`); optional `icon_*`, `default_prompt` |
| In-repo references (docs, `SKILL.md`, `README`, `AGENTS.md`) | **0** |
| Sibling provider variants (`claude.yaml` / `codex.yaml` / `gemini.yaml` / `agents.yaml`) | **0** |

**Finding:** the audit's word “duplicated” is a misnomer — 57 *distinct per-agent* config stubs, not
57 copies of one file. There is nothing to deduplicate. The consumer is an external spec or none
found in-repo. **Recommendation: RETAIN, no action.** Classified CLOSED because the finding was
*examined* as instructed; no file was moved or deleted.

---

## 7. Concurrency observations (material to sign-off)

### 7.1 The failing test file was deleted by the other session (landed as `4bb64572`)

While this report was being prepared the index showed, and the concurrent session then committed:

```
4bb64572  test: drop scraper inventory tests missed by Athena archive
          tests/test_scraper_inventory.py | 176 ------------------- (deleted)
```

- **Not produced by this change.** This change's commits are `526f33d5`, `16c69940`, `56a42b27` —
  none touch this file; the last commit to it before deletion was `3e36b00c` (2026-09-28).
- **Never swept.** It was left staged and untouched while staged, per `AGENTS.md` §7, and was not
  included in any commit from this change.
- **What it means:** the 5 P0-2 failures disappeared because **the test was removed, not because the
  root cause was fixed.** The gap — no `company/athena/*.jsonl` fixture and a data path excluded by
  `.gitignore:170` — is now **untested rather than failing**. This is a legitimate, candidly-messaged
  CI-unblocking move by the other session, but it changes the nature of the residue, so it is
  recorded here rather than left implicit.
- The §4.3 pre-existing evidence was captured against **HEADs where the file exists** (runs 1–3);
  run 4 documents the post-deletion state.

**Recorded for the CEO:** `tests/test_scraper_inventory.py` is now gone. If the underlying scraper
inventory ever needs coverage again, it must be reintroduced with a checked-in fixture (or an
explicit `xfail` with a written reason) — the original tests cannot pass without data that
`.gitignore` forbids from being committed.

### 7.2 Push activity — all attributed to the other session

At report time `git status -sb` shows the branch **in sync with origin** (no ahead/behind). Every
commit from this change, including `56a42b27`, is now on origin — **pushed by the concurrent
session, not by this change.** This change performed **no push, no amend, no force-push**, and
created **no stash**; the only git writes it performed were pathspec-scoped commits, a
`submodule init`, and a temporary inspect branch created and deleted during the rollback drill.

---

## 8. Validation matrix (gates at `4bb64572`; tree/test state at final HEAD `363c1aec`)

| Gate | Command | Result |
|---|---|---|
| Lint | `uv run ruff check src/` | **PASS** — All checks passed |
| Type check | `uv run mypy src/` | **PASS** — no issues in 225 source files |
| Tests (run 5) | `uv run pytest -q` | **2511 passed, 2 skipped, 0 failed, 67 deselected** (2580 total) → **PASS, exit 0** (§3.3) |
| Generator | `…AgentGenerator().generate_all()` | **PASS** — exit 0, **0 changed files** |
| Harness/docs lint | `pwsh scripts/maintenance/lint-ecl.ps1` | **PASS** — `ECL lint passed`, 0 failures / 0 warnings (22 files) |
| Registry vocabulary | residual legacy tool lines | **0** of 145 |
| Submodule | `git submodule status` | **PASS** — `6fd2f60` clean |
| Tags | 14 tags resolve; `c11` peels to `526f33d5` | **PASS** |
| Tree after full suite | `git status --short` + SHA256 of `hr/onboarding_requests.yaml` | **CLEAN** — hr file byte-identical to pre-run (§3.3) |
| Sync | `git status -sb` | **4 ahead of origin, deliberately unpushed** — push excluded by the governing protocol; recompute with `git status -sb` at application time (ahead 4 at `363c1aec`, may change) |

**Diff against baseline (measured 2026-10-07 at `c40decf0`):** `git diff --shortstat cleanup/c0-baseline..c40decf0` →
**754 files changed, 7359 insertions(+), 71486 deletions(−)** (baseline → `c40decf0`); tracked files **4187 → 3708 (−479, −11.4%)**.

---

## 9. Known artifacts and limitations

1. **Cosmetic BOM in commit `526f33d5`'s subject line** — the first character of the subject is a
   U+FEFF byte, left over from a Windows encoding mistake. It is **documented, not repaired**: amending
   is prohibited because it would rewrite every commit after it (`16c69940`, `98c1a535`, `fdceab26`,
   `56a42b27`, `4bb64572`) and the branch is shared and fully pushed. Impact: display only.
2. **Skip-count delta 1 → 2 between run 1 and runs 2–3** is unattributable from git evidence and is
   reported as an open micro-observation (§4.4).
3. **Approval records were absent — now signed as an after-the-fact reconstruction** (D4, §6.2).
   The cleanup still ran without contemporaneous approval; the signature closes the sub-item and
   imposes contemporaneous records on all future phases.
4. **P0-1 was dirty, and is now closed** (§3.2/§3.3): the test fixtures that rewrote
   `hr/onboarding_requests.yaml` now pass `data_dir` to a temp path. A full-suite run leaves the
   tree byte-clean; run 5 is the proof.
5. **The five scraper-inventory tests are retired, not restored** (D3, §4.7) — the coverage gap is
   accepted explicitly. Re-introducing it requires real tracked fixtures, not a fabricated JSONL.
6. **One documented perf flake remains in the suite** — `test_endpoint_response_time_p95`, already
   excluded by the project's own health gate (§4.6); passes 3/3 in isolation.
7. **Two out-of-scope files still carry legacy tool names** — registry template + runtime
   `hr/` data (§6.1 follow-on).
8. **Evidence separation honoured** (`AGENTS.md` §9.3): this change wrote only its own deliverables
   and the rollback runbook. It did not write into `reports/evidence/`, `audit/*.jsonl`,
   `.opencode/audit/*`, `harness/changes/*/reviews/`, or `repo-audit/cleanup-status/CLEANUP_*`
   (the audit's own evidence files are untouched).

---

## 10. Recommendation

**Sign off on all seven:** P0-1 (CLOSED — fixed at source, run 5 exits 0 with a byte-clean tree),
P0-2 (CLOSED — 5 failures PRE-EXISTING; suite now at 0 real failures), P0-3 (CLOSED), P1-1
(CLOSED), P1-2 (CLOSED — runbook + signed reconstruction), P1-3 (CLOSED), P1-4 (CLOSED — retain,
zero duplication).

**Overall readiness: READY — all three P0 conditions and all four P1 findings discharged with
evidence.** This is an improvement on the predecessor audit's 72/100 READY WITH CONDITIONS: the
three open-ended conditions are now closed with reproducible proof, not narrowed.

---

## 11. CEO decision closure (2026-10-07)

| # | Decision | Action taken | Result |
|---|---|---|---|
| **D1** | Fix the `hr/` rewrite rather than report it | `tests/unit/test_onboarding.py` passes `data_dir=str(tmp_path / "hr")` at both `OnboardingManager` construction sites; root cause established by bisection (§3.2) | **P0-1 CLOSED** — run 5: 0 failed, hr file byte-identical (§3.3) |
| **D3** | Formally retire the 5 deleted tests (not restore) | Retired in §4.7; two dangling doc references cleared so no agent is sent to run a non-existent test; coverage gap recorded explicitly | **Recorded** — gap accepted, `.gitignore:170` remains the structural cause |
| **D4** | Sign the git-derived phase reconstruction | Runbook provenance disclaimer + §1 header signed as an after-the-fact record; §6 flipped to CLOSED; contemporaneous-approval condition imposed on future phases | **P1-2 CLOSED** |

No push, no amend, no force-push, no stash, no tag re-point, no hand-edit of generated agent
cards. Every commit pathspec-scoped after re-checking `git status --short` (`AGENTS.md` §7).
