# 00 — Current State and Preservation Audit

**Repository:** `C:\Users\jmlus\light-speed-holdings`
**Audit date:** 2026-11-13
**Author:** OpenCode agent (recovery mission continuation)
**Baseline HEAD:** `86d10e709c50424eb7109283ff7e7019a1a51bc2` (`chore: add urllib.error import for proper exception handling`)

This document records the state of the repository **before** this session's implementation work and the preservation risks that affect the AI Studio recovery mission. Every value below was read from the live repository in this session; nothing is inferred.

---

## 1. Git state at session start

| Item | Value | Evidence |
|---|---|---|
| Branch | `main` | `git rev-parse --abbrev-ref HEAD` |
| HEAD commit | `86d10e709c50424eb7109283ff7e7019a1a51bc2` | `git rev-parse HEAD` |
| Upstream | `origin/main` | `git rev-parse --abbrev-ref --symbolic-full-name @{u}` |
| Ahead / behind | `0 / 0` | `git rev-list --left-right --count HEAD...origin/main` |
| Working tree | clean | `git status --porcelain=v1` returned no lines |

The working tree was clean at the start of this session. All changes described in `06-complete-implementation-change-register.md` were made by this session and remain **uncommitted** (no commit, merge, or push was performed — see §6).

---

## 2. Prior recovery lineage (PR #584)

The first AI Studio recovery was already merged before this session.

| Item | Value |
|---|---|
| PR | **#584** — "Recovery/ai studio artifacts" |
| State | `MERGED` |
| Merged at | `2026-11-12T17:36:11Z` |
| Merge commit | `3ac92723595279e933495d02f130f13867fdc166` |
| Head branch | `recovery/ai-studio-artifacts` (branch no longer exists on the remote) |
| Open PRs now | none (`gh pr list --state open` returned empty) |

Recovery commits in the history:

```
0b9f406d  recovery: restore AI Studio AssessmentWizard and BeforeAfterWorkflow components; add audit deliverable 19
19b0b727  recovery: fix JSX syntax and asset paths in AssessmentWizard and BeforeAfterWorkflow
9d74f05c  Merge branch 'main' into recovery/ai-studio-artifacts
3ac92723  Recovery/ai studio artifacts (#584)
c4d1862a  Merge branch 'recovery/ai-studio-artifacts'
```

### 2.1 Conflict-resolution review

- Merge commits present: `9d74f05c`, `c4d1862a`, `0c738891`, `d51970ed`, `37594245`.
- Conflict-marker scan across `src/**/*.{ts,tsx}` (`^<<<<<<<`, `^>>>>>>>`, `^=======$`) returned **0 matches**.
- The PR #584 merge body explicitly records that it "resolves a leftover merge-conflict marker in an archived change summary" — i.e. a conflict marker existed in an archive file and was cleared. No conflict marker survives in source today.

### 2.2 Hook / bypass review

- Git hooks present and active: `commit-msg`, `post-commit`, `pre-commit` (`.git/hooks/`).
- No recovery commit message contains a `--no-verify` or bypass note; the five recovery commits above carry ordinary conventional-commit subjects.
- **Conclusion:** no evidence of a hook bypass was found. (Absence of evidence is reported as such — no bypass is claimed or denied beyond what the messages and hook state show.)

---

## 3. Remote CI state (main, distinct from local)

`gh run list --branch main` for HEAD `86d10e70`:

| Workflow | Event | Conclusion |
|---|---|---|
| **CI** | push | **success** |
| **Site Build + Principles Gate** | push | **success** |
| Verify Vite Dev Server | push | **failure** |
| Monitoring & Alerts | schedule | success |
| Autonomous Orchestrator | schedule | success |
| Vercel Preview Retry | status | skipped |

**`Verify Vite Dev Server` is red on `main`** and has been red on every recent push (`9b0e7155`, `0c738891`, `86d10e70`). Root cause (from the run log): the workflow runs `pnpm install`, but `pnpm` is not present on the `windows-latest` runner — `The term 'pnpm' is not recognized`. The workflow additionally hard-codes a developer-machine path (`C:\Users\jmlus\light-speed-holdings\scripts\dev\start-dev.ps1`) and a Unix-only redirect (`curl --output /dev/null`). This is a **pre-existing CI hygiene defect, unrelated to the AI Studio recovery**; it is recorded as an outstanding item in `07-outstanding-items-and-exclusions-register.md` (O-01).

The `CI` and `Site Build + Principles Gate` workflows — the two that gate `main` — are green at `86d10e70`.

---

## 4. The AI Studio reference export and its preservation risk

| Item | Value |
|---|---|
| Reference path | `_staging/lsh-prototype/` |
| Gitignored? | **Yes** — `.gitignore:256` = `_staging/` |
| Tracked files under `_staging/` | **0** (`git ls-files _staging` returned nothing) |
| Staging source files | **241** under `_staging/lsh-prototype/src/` |
| Staging AGENTS.md | Declares `lsh-prototype` a "constrained, read-mostly sandbox"; canonical source of truth is the main repo |

**Preservation risk (high):** the only functional reference for the AI Studio prototype is **local-only and untracked**. If this workstation's `_staging/` directory is deleted, the prototype can never again be diffed against the implementation. This is a genuine, documented risk — not a defect to "fix" silently, and not something this session altered.

---

## 5. Secret / artifact review of tracked files

| File | Tracked | Content | Assessment |
|---|---|---|---|
| `storageState.json` | yes | 209 bytes; `cookies: []`; one origin `http://localhost:1440` with `lightspeed_theme: dark` | **No credentials, tokens, or session cookies.** Only a theme preference. Low risk. |
| `.env` | no (gitignored, `.gitignore:4`) | — | Correctly excluded |
| `.env.example`, `.env.staging.example` | yes (allowlisted, `.gitignore:6–7`) | placeholders only | Correct |
| `scripts/deploy/rotate-secrets.py` | yes | deployment tooling | Not a secret |

A tracked-path scan for `storageState`, `.pem`, `.key`, `credentials`, `secret`, `token`, `.sqlite`, `.db` found no committed secret material (matches are code/test/doc filenames, not credentials). See `03-security-and-repository-hygiene.md` for the full table.

---

## 6. Files at risk / boundary conditions for this mission

| # | Risk | Status |
|---|---|---|
| R-1 | `_staging/` is gitignored → prototype reference is local-only | Open, documented (O-10) |
| R-2 | `Verify Vite Dev Server` CI workflow is red on main | Open, pre-existing (O-01) |
| R-3 | Sector taxonomy has three divergent vocabularies | **User exclusion** — not to be changed |
| R-4 | Workflow-simulator card keyboard navigation gap | **User exclusion** — not to be changed |
| R-5 | `/api/journey-events` endpoint does not exist (telemetry POST 404s) | Open, backend out of scope (O-04) |
| R-6 | Cloudflare Turnstile challenge never settles on localhost → `networkidle` never reached on `/insights` | Open, deployment config (O-05) |

---

## 7. Non-actions (explicit)

- No commit, merge, push, PR, rebase, or force-push was performed this session.
- No `--no-verify`, no hook bypass, no history rewrite.
- No file was deleted.
- The two user exclusions (sector taxonomy, workflow-simulator keyboard nav) were left untouched.

---

## 8. Session working-tree delta (after implementation, still uncommitted)

```
 M src/App.tsx                   |  4 ++++   (add /faq + /faqs routes)
 M src/components/SiteLayout.tsx |  3 +++    (mount BackToTop)
 M src/pages/HomePage.tsx        | 43 +---    (replace inline matrix approximation with real component)
?? src/components/HumanApprovalMatrix.tsx
?? src/components/BackToTop.tsx
?? src/components/FaqCardList.tsx
?? src/pages/FaqPage.tsx
?? scripts/recovery-verify.mjs
?? scripts/recovery-verify-focused.mjs
?? docs/recovery/               (this deliverable set)
```

Full detail in `06-complete-implementation-change-register.md`.
