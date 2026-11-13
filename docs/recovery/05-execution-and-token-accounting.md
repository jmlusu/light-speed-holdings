# 05 — Execution and Token Accounting

**Date:** 2026-11-13
**Purpose:** Record the commands actually executed for this recovery, their outcomes, and an honest accounting of execution cost. Nothing here is estimated as if it were measured.

---

## 1. Execution log (commands + exit codes)

### 1.1 State capture

| # | Command | Purpose | Exit |
|---|---|---|---|
| 1 | `git status --short` | confirm clean tree / list delta | 0 |
| 2 | `git rev-parse --abbrev-ref HEAD` → `main` | branch | 0 |
| 3 | `git rev-parse HEAD` → `86d10e709c50424eb7109283ff7e7019a1a51bc2` | baseline | 0 |
| 4 | `git log --oneline -5` | confirm PR #584 lineage | 0 |
| 5 | `gh run list --branch main --limit 8 --json name,conclusion,event,headSha` | remote CI status | 0 |
| 6 | `gh pr list --state open` | confirm no open PRs | 0 |

### 1.2 Reconciliation scans

| # | Command | Purpose | Exit |
|---|---|---|---|
| 7 | `git ls-files _staging` | prove `_staging/` is untracked | 0 |
| 8 | `Select-String .gitignore -Pattern _staging` → line 256 | confirm ignore rule | 0 |
| 9 | staging-vs-repo path diff (241 prototype files) | produce the absent-file list | 0 |
| 10 | reference-grep per absent file | classify DEAD vs functional | 0 |
| 11 | `git ls-files` filtered on `secret|token|credential|.pem|.key|.sqlite|.db|storageState|.env` | secret scan | 0 |

### 1.3 Implementation + integrity

| # | Command | Purpose | Exit |
|---|---|---|---|
| 12 | copy 4 files from `_staging/lsh-prototype/src/` → repo `src/` | restore | 0 |
| 13 | `Get-FileHash <file> -Algorithm SHA256` ×8 | prove byte-identity (repo vs staging) | 0 |
| 14 | edits to `src/App.tsx`, `src/components/SiteLayout.tsx`, `src/pages/HomePage.tsx` | wiring | 0 |
| 15 | `git diff --stat` | quantify the change | 0 |

### 1.4 Gates (re-run this session)

| # | Command | Result | Exit |
|---|---|---|---|
| 16 | `npx tsc --noEmit --pretty false` | no diagnostics | **0** |
| 17 | `npx vitest run` | 16 files / 145 tests passed | **0** |
| 18 | `npx vite build` | built in 30.94 s | **0** |

### 1.5 Runtime verification

| # | Command | Purpose | Exit |
|---|---|---|---|
| 19 | `node scripts/recovery-verify.mjs` | 27-route matrix + interactions → `verification-run.json` | 0 |
| 20 | `node scripts/recovery-verify-focused.mjs` | `/insights`, BackToTop, matrix → `verification-focused.json` | 0 |
| 21 | inline Playwright FAQ count | resolve the 6-vs-7 card question | 0 |

**No command failed.** No command was run with `--no-verify`, no push/merge/rebase was executed, and no destructive git operation was issued.

---

## 2. Files produced by execution

| Artifact | Kind | Size / count |
|---|---|---|
| `docs/recovery/00…08` | deliverables | 9 markdown docs |
| `docs/recovery/screenshots/*.png` | runtime evidence | 33 PNGs |
| `docs/recovery/verification-run.json` | machine evidence | 10,834 bytes |
| `docs/recovery/verification-focused.json` | machine evidence | 909 bytes |
| `docs/recovery/_staging-absent-src.txt` | scan evidence | 5,639 bytes / 117 lines |
| `scripts/recovery-verify.mjs` | verification harness | 146 lines |
| `scripts/recovery-verify-focused.mjs` | verification harness | 52 lines |

---

## 3. Token accounting — honest statement

**Precise token counts are not measurable from inside this session.** The agent runtime does not expose per-turn input/output token usage or dollar cost to the agent, and no billing API was queried. Any exact figure would be fabricated. What *can* be stated truthfully:

| Metric | Value | Basis |
|---|---|---|
| Session type | single continued session (resumed from a checkpoint) | conversation record |
| Shell command groups executed | ~21 | §1 |
| Gate runs | 3 (tsc, vitest, build) | §1.4 |
| Playwright runs | 3 | §1.5 |
| Longest single command | `npx vite build` ≈ 31 s; `npx vitest run` ≈ 18 s | measured wall time |
| Screenshots written | 33 | filesystem |

**Cost proxies (not token counts):** the work is dominated by (a) reading the 241-file staging tree for reconciliation and (b) three full gate runs. The heaviest token consumers were the reconciliation scans (many small file reads/greps) and this deliverable set (9 long markdown documents).

To obtain a true token/cost figure, the operator should consult the provider dashboard for the model `opencode/big-pickle` over the session window; that data is outside the agent's reach and is **not** reproduced here.

---

## 4. Reproducibility

Everything in §1 is deterministic and re-runnable:

```pwsh
npx tsc --noEmit --pretty false
npx vitest run
npx vite build
node scripts/recovery-verify.mjs
node scripts/recovery-verify-focused.mjs
```

`recovery-verify.mjs` expects a preview server on `http://localhost:1440` (`npx vite preview --port 1440`). It writes JSON + PNGs into `docs/recovery/`.
