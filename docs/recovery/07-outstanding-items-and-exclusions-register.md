# 07 — Outstanding Items and Exclusions Register

**Date:** 2026-11-13
**Purpose:** list everything that is **not** closed, plus the two items the user directed must be left alone. Nothing here was silently "fixed".

Legend — **Type:** `DEFECT` (something is wrong) · `GAP` (missing functionality) · `EXCLUSION` (user-directed no-change) · `RISK` (future hazard) · `PENDING` (blocked on authorization) · `DOC` (documentation defect).
**Severity:** High / Medium / Low.

---

## 1. Outstanding items

| ID | Type | Severity | Item | Evidence | Recommended action | Status |
|---|---|---|---|---|---|---|
| **O-01** | DEFECT | Medium | `Verify Vite Dev Server` CI workflow is red on every push | `.github/workflows/verify-vite.yml` runs `pnpm install` (pnpm absent on runner), hard-codes `C:\Users\jmlus\…\start-dev.ps1`, uses `/dev/null` | Rewrite the workflow to use the repo's actual package manager and a portable dev-server start; or disable it until fixed | **Open** (pre-existing, non-gating) |
| **O-04** | GAP | Low | `/api/journey-events` returns 404 | `verification-run.json` → `failedRequests: net::ERR_ABORTED http://localhost:1440/api/journey-events` | Implement the telemetry endpoint in the backend, or make the client tolerant when it is absent | **Open** (backend out of recovery scope) |
| **O-05** | DEFECT | Low | Cloudflare Turnstile challenge never settles on localhost; blocks `networkidle` | `net::ERR_NAME_NOT_RESOLVED https://brunhild.challenges.cloudflare.com/...`; CSP blocks `data:,` connect | Expected in local dev; ensure the production deployment supplies the Turnstile keys/domains. Page renders regardless | **Open** (deployment config) |
| **O-06** | GAP | Low | Prototype `components/home/IntentToExecutionLifecycle.tsx` has **no repo equivalent** | `02-…` §2.3; staging HomePage references it | Decide whether the "Intent → Execution" lifecycle deserves a repo section; the concept is covered textually in `HAOMTGTVSection`/`/haomtgv` | **Open** (deliberate non-restore) |
| **O-10** | RISK | High | The AI Studio reference (`_staging/lsh-prototype/`) is **gitignored and untracked** (0 tracked files) | `git ls-files _staging` → 0; `.gitignore:256` | Archive the prototype into the tracked tree or an external durable store, or the reconciliation can never be re-verified | **Open** (needs authorization) |
| **H-01** | RISK | Low | `storageState.json` is tracked | 209 bytes; `cookies: []`; only `lightspeed_theme: dark` | Keep, or untrack if it ever holds session cookies | **Open** (low) |
| **P-01** | PENDING | High | Remote CI has **not** evaluated this session's changes | `gh run list` shows runs only for `86d10e70`; nothing was committed/pushed | Commit on a branch, open a PR, and let `CI` + `Site Build + Principles Gate` run — **only with explicit authorization** | **Blocked on authorization** |
| **P-02** | PENDING | Medium | Implementation is uncommitted | `git status` shows 3 modified + new files | Same as P-01 | **Blocked on authorization** |
| **DOC-01** | DOC | Low | Prior audit set `.audit/reconciliation/deliverable14-…` contains stale counts | FAQ count, pillar count, component paths — see `01-…` §3 | Correct or supersede the prior deliverable; do not build on its numbers | **Open** (documentation) |

---

## 2. User-directed exclusions (do **not** change)

| ID | Exclusion | What the divergence is | Directive |
|---|---|---|---|
| **X-01** | Sector taxonomy | Three divergent sector vocabularies exist between prototype and repo | **Leave unchanged** — explicitly out of scope |
| **X-02** | Workflow-simulator card keyboard navigation | The prototype/repo workflow-simulator cards lack full keyboard navigation | **Leave unchanged** — explicitly out of scope |

These are recorded so a future reader does not mistake them for overlooked defects. They were verified to be *unchanged* by this session.

---

## 3. Reconciliation leftovers (classified, not outstanding defects)

The `02-…` ledger accounts for the 117 prototype files absent from the repo:

| Category | Count | Why it is not an outstanding item |
|---|---|---|
| Media (`assets/images/**`) | 62 | Prototype-only bundled images; the repo has a larger, registry-backed media set (288 public assets) |
| Prototype in-tree design system | 26 | **Superseded** by the `packages/design-system` package |
| Prototype docs/reports (markdown) | 10 | Non-functional documentation artifacts |
| Functional components — REPLACED | 9 | Equivalent implementation exists in the repo |
| Functional components — DEAD | 8 | Prototype itself never referenced them (0 refs) |
| Functional — OMITTED | 1 | `IntentToExecutionLifecycle` → **O-06** |
| RELOCATED | 1 | `brand/tokens/brand-tokens.css` present at repo path |

**Net functional gap: 1** (O-06), plus the two exclusions.

---

## 4. Acceptance-criteria status

| Criterion | Status |
|---|---|
| Recovery scope identified from the prototype | ✅ complete (`02-…`) |
| Recoverable losses restored verbatim | ✅ 4 components (`06-…`) |
| Gates green locally | ✅ tsc/vitest/build (`04-…` §1) |
| All routes verified | ✅ 27 routes (`04-…` §2) |
| Interactions verified | ✅ matrix / back-to-top / FAQ / theme (`04-…` §3) |
| Screenshots captured inside repo | ✅ 33 PNGs (`04-…` §4) |
| Remote CI green | ❌ `Verify Vite Dev Server` red (pre-existing) **and** new code not yet pushed (P-01) |
| Changes committed / PR opened | ❌ intentionally not done (P-02) |

The two ❌ rows are the reason the mission is **PARTIAL**, not COMPLETE (see `08-…`).
