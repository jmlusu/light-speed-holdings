# 01 — Previous Recovery Verification

**Date:** 2026-11-13
**Purpose:** Independently re-verify the recovery work that was already merged (PR #584) before continuing. No prior claim is repeated here unless this session reproduced it.

---

## 1. What was previously claimed

`.audit/reconciliation/deliverable19-session-recovery-and-verification.md` claimed two recoveries:

- **R-01** — `AssessmentWizard` restored into `src/components/`, `AiAssessmentPage.tsx` rewired to render it inline.
- **R-02** — `BeforeAfterWorkflow` restored into `src/components/`, mounted in `WhatWeDoPage.tsx`.

It also claimed a clean gate run: `tsc` exit 0, `vitest` 16 files / 145 tests passed, `vite build` success.

---

## 2. Independent re-verification (this session)

### R-01 — AssessmentWizard

| Check | Result | Evidence |
|---|---|---|
| Repo file exists | yes | `src/components/AssessmentWizard.tsx` |
| Byte-identical to staging source | **yes** | SHA256 `769722518B58F7E446530E21B89CC4E90662F00707854815E04AA838767991AC` on both `src/components/AssessmentWizard.tsx` and `_staging/lsh-prototype/src/components/AssessmentWizard.tsx` |
| Wired into the page | yes | `src/pages/AiAssessmentPage.tsx:16` imports it; `:37` renders `<AssessmentWizard theme={theme} onRequestBriefing={onRequestBriefing} />` |
| Renders at runtime | yes | Playwright `/ai-assessment` → `h1 = "AI Readiness Assessment Wizard"`, `#main-content` present, HTTP 200 |

**Verdict: VERIFIED.** The wizard is present, unmodified from the prototype, wired, and renders.

### R-02 — BeforeAfterWorkflow

| Check | Result | Evidence |
|---|---|---|
| Repo file exists | yes | `src/components/BeforeAfterWorkflow.tsx` |
| Size | 829 lines (repo) vs 834 lines (staging) | `Measure-Object -Line` on both |
| Mounted | yes | imported in `src/pages/WhatWeDoPage.tsx` |
| Renders at runtime | yes | Playwright `/what-we-do` → HTTP 200, `h1 = "Enterprise AI Systems Built for Real Constraints"` |

**Verdict: VERIFIED (with known, documented divergence).** The component is present and mounted. It is **not** byte-identical to the prototype: the repo copy carries the deliberate asset-path remaps documented as D-07 in deliverable19 (prototype referenced staging-only image paths that do not exist in this repo). This divergence is intentional and previously recorded — not a new defect.

### Prior gate claim

| Gate | Prior claim | This session (independent re-run) | Match |
|---|---|---|---|
| `npx tsc --noEmit --pretty false` | exit 0 | **exit 0** | ✅ |
| `npx vitest run` | 16 files / 145 tests passed | **16 files / 145 tests passed** | ✅ |
| `npx vite build` | success | **success** (1715 modules) | ✅ |

**Verdict: VERIFIED.** The prior gate results reproduce exactly.

---

## 3. Prior claims corrected against evidence

These are statements in the earlier `.audit/reconciliation/` set that this session found to be inaccurate. They are recorded so the ledger is not built on them.

| ID | Prior claim | Where | Correction (this session) |
|---|---|---|---|
| C-1 | "FAQ … Same **25 FAQ entries** from faqs registry" | `deliverable14-page-and-component-parity.md` (P01, P09) | The rendered registry holds **6** entries, not 25. `src/data/faqs.ts` contains one interface field (`id`/`registryId`) plus **6** array objects; a raw `registryId:` text match returns 7 because line 25 is the type declaration. (This session's own first pass also mis-stated "7" by counting that same declaration — corrected here.) The separate canonical file `src/data/registries/faq-registry.json` holds **28** entries, of which only 6 are surfaced. |
| C-2 | "6 architecture SVGs: MISSING → CREATED in `public/assets/diagrams/`" | `deliverable14` key findings | `deliverable19` already recorded this as **not reproducible**; this session confirms no source references `/assets/architecture*`. Treated as superseded. |
| C-3 | "Value pillars … **5-pillar** section" | `deliverable14` (P01) | The repo `VALUES` in `src/data/homeCopy.ts` drives **4** pillars, rendered as "Our Value Framework". |
| C-4 | "`FaqSection` … `src/components/FaqSection.tsx`" | `deliverable14` (component table) | Actual path is `src/components/site/FaqSection.tsx`. |

None of these corrections change the recovery outcome; they matter only because the reconciliation ledger (`02-…`) must not inherit inflated counts.

---

## 4. Net assessment of the prior recovery

- Both claimed recoveries are **real, present, wired, and rendering**.
- The prior gate numbers reproduce.
- The prior *narrative* documents (deliverable14 in particular) contain stale/incorrect counts (FAQ entries, pillar count, some paths). Those are documentation defects, not functional defects.
- PR #584 is merged; `main` carries the recovery.

**Conclusion:** the prior recovery is trustworthy at the artifact level and was continued rather than restarted. The remaining recoverable gaps are addressed in `02-…` and implemented per `06-…`.
