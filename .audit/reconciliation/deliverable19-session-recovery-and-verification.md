# Deliverable 19 — Session Recovery and Verification Record

**Date:** 2026-11-12
**Baseline HEAD:** `d51970ed` — Merge remote-tracking branch 'origin/main' into chore/nov-2026-consolidation
**Scope:** Recover remaining lost AI Studio artifacts, verify prior claims independently, produce the 13-section audit report.
**Commits made:** None. **Deploys:** None. **Destructive git operations:** None.

---

## 1. Verification performed (this session)

| Command | Result |
|---|---|
| `npx tsc --noEmit --pretty false` | Exit 0 — no type errors |
| `npx vitest run` | 16 files / 145 tests — **145 passed, 0 failed** |
| `npx vite build` | Success — 1708 modules, built in 40.11s |

Baseline before this session's edits: `vitest` reported **1 failed / 144 passed** (`media-registry.test.ts`) only after the recovery below introduced unregistered asset paths; it was green before. The failure was caused by the recovery itself and was fixed (see D-07).

---

## 2. Recoveries completed

### R-01 — AI Readiness Assessment Wizard (restored)
- **Lost:** `src/pages/AiAssessmentPage.tsx` had been reduced to a modal-trigger stub. The AI Studio original rendered a five-step diagnostic (`AssessmentWizard`) covering data maturity, core infrastructure, governance alignment, talent readiness, and agentic workflow potential.
- **Evidence:** `_staging/lsh-prototype/src/pages/AiAssessmentPage.tsx:11,32` imports and mounts `AssessmentWizard`; `_staging/.../components/AssessmentWizard.tsx` (615 lines) was intact.
- **Action:** copied `AssessmentWizard.tsx` verbatim into `src/components/`; rewrote `src/pages/AiAssessmentPage.tsx` to render the wizard inline and removed the duplicate on-mount modal open.
- **Dependency check:** imports only `react`, `lucide-react`, `./Reveal` — all present in main.

### R-02 — Before/After Workflow Simulator (restored)
- **Lost:** `BeforeAfterWorkflow` (890 lines) existed only in staging. Main `WhatWeDoPage` had no equivalent section.
- **Evidence:** `_staging/lsh-prototype/src/pages/WhatWeDoPage.tsx:9,35` — mounted between the capabilities section and the integrated capability map.
- **Action:** copied `BeforeAfterWorkflow.tsx` into `src/components/`; mounted in `src/pages/WhatWeDoPage.tsx` as section `3b`, between "LightSpeed's Approach" and "Commercial Catalog" — the same relative position it held in staging.
- **Dependency check:** imports only `react`, `lucide-react`.

---

## 3. Defects

| ID | Description | Severity | Status |
|---|---|---|---|
| D-01 | `AiAssessmentPage` lost its 5-step readiness diagnostic; replaced by a modal stub | High | Fixed (R-01) |
| D-02 | `BeforeAfterWorkflow` simulator absent from main; WhatWeDoPage lost the section | High | Fixed (R-02) |
| D-03 | Three divergent sector vocabularies: canonical JSON (10 ids), `sector-registry.ts` (6 ids), `sectors.ts` (9 ids) | Medium | Not fixed — needs product decision |
| D-04 | `sectors.ts` legacy 9-sector registry has no `.tsx` importer but is still exercised by `governance.test.ts` | Low | Not fixed |
| D-05 | Orphaned `ClosingCTASection.tsx` references `/hero-background.jpg`, registered `kind: missing`; build emits an unresolved-asset warning | Low | Not fixed — documented placeholder, dead component |
| D-06 | `AiAssessmentPage` auto-opened the briefing modal on mount, duplicating the page's purpose | Low | Fixed (R-01) |
| D-07 | Recovered `BeforeAfterWorkflow` referenced two staging-only image paths plus an unregistered logo path | High | Fixed — remapped to registered assets |
| D-08 | `useJourneyEvents` posts to `/api/journey-events`, which does not exist | Medium | Not fixed — backend out of scope |
| D-09 | Turnstile returns error `400020` on localhost (hostname not allowlisted) | Medium | Not fixed — deployment configuration |
| D-10 | `offer-a`…`offer-e` all redirect to `/solutions` | Low | Not fixed — product decision |

### D-03 detail (verified, not assumed)
| Source | Count | IDs |
|---|---|---|
| `src/data/registries/sector-registry.json` | 10 | financial-services, healthcare-public-health, agriculture-agritech, education-academia, government-public-sector, regulators-standards-institutions, research-universities, smes-private-enterprise, development-nonprofit-organizations, technology-digital-businesses |
| `src/data/sector-registry.ts` | 6 | financial-services, healthcare, agriculture, education, government, academia-research |
| `src/data/sectors.ts` | 9 | government-public-sector, development-donors, health, financial-services, agriculture, energy, telecommunications, smes-entrepreneurs, technology-companies |

**Impact assessment (corrected):** This is **not** a broken-link defect. Every `/sectors/:id` link is generated from `sector-registry.ts` and resolved by `SectorDetailPage` against the same file, so navigation resolves. The real impact is IA inconsistency: `UseCasesPage` builds its sector filter from the 10-id JSON registry, while `/sectors` publishes 6 pages. Only `financial-services` is identical across sources.

### D-07 detail
The copied component referenced:
- `/src/assets/images/before_after_sector_bg_daytime_1793890712154.jpg` (staging source path, absent)
- `/assets/aistudio/BeforeAfterSectorBackground_d538f2ff.jpg` (staging public path, absent)
- `/brand/logo/logo-favicon-transparent.png` (file exists, but not in the pinned 14-asset registry)

Fixed by remapping to `/brand/digital/Homepage_Hero_High_fidelity.jpeg` (registered `photograph`, file present) and `/logo-icon-v2.svg` (registered `logo`). The media registry's pinned count of 14 was left untouched.

---

## 4. Claims corrected against evidence

- **"Six architecture SVGs referenced but missing."** Not reproducible. No source references `/assets/architecture*`, and `public/assets/architecture` does not exist. The media-registry suite (which fails on any unregistered reference or any non-`missing` entry without a file) passes. Recorded as not a current defect.
- **"HomePage.tsx and homeCopy.ts modified this session."** They contain the recovered Value Pillars and Five-Tier Approval Matrix, but `git status` shows no working-tree diff: the changes are committed at HEAD via `4fd45815` (2026-11-12 10:00:48), which is an ancestor of `d51970ed`. They are reported as verified-present-and-committed, not as working-tree modifications.
- **"FAQ page missing."** The standalone `/faq` route from AI Studio is absent, but the FAQ capability is not: `FaqSection` renders from `src/data/faqs.ts` on both `HomePage` (`id="faq"`) and `ContactPage`, and the footer targets `/#faq`. No 404 is reachable. Not recorded as a defect.

---

## 5. Files touched this session

**Created**
- `src/components/AssessmentWizard.tsx`
- `src/components/BeforeAfterWorkflow.tsx`
- `.audit/reconciliation/deliverable19-session-recovery-and-verification.md`

**Modified**
- `src/pages/AiAssessmentPage.tsx`
- `src/pages/WhatWeDoPage.tsx`
- `src/components/BeforeAfterWorkflow.tsx` (post-copy asset remap)

**Pre-existing working-tree state (not mine, left untouched)**
- Staged: `packages/data-use-cases/src/insights.ts`, `src/data/insights.ts`, `src/data/pharos.ts`, `src/data/registries/faq-registry.json`, `src/pages/PharosPage.tsx`
- Unstaged/untracked: `AGENTS.md`, `data/orchestrator/cost_tracker.json`, `docs/STATUS.md`, `harness/changes/active/summary.md`, `tests/test_subagent_framework.py`, `commit-out.txt`, `merge-out.txt`, `pr-body.md`, `push-out.txt`

---

## 6. Conclusion

Both genuinely lost interactive artifacts identified by the prototype diff are recovered and verified by a clean typecheck, a fully green test suite, and a successful production build. Remaining open items are outside the frontend recovery scope: a sector-taxonomy product decision, a missing backend endpoint, and deployment-level Turnstile/hostname configuration.

---

## 7. Addendum — independent review findings

Two independent reviewers (`qa-lead`, `senior-frontend-engineer`) were run after the first green build. QA returned PASS on all three gates. The frontend review found further real defects in the recovered components, which were then fixed and re-verified.

| ID | Description | Severity | Status |
|---|---|---|---|
| D-11 | `AssessmentWizard` used `btn-milled` / `btn-milled-primary` / `btn-milled-secondary`, which have **no CSS definition anywhere in the repo** and carried no colour utilities — Back/Next/Retake/Request-Briefing rendered as uncoloured text | High | Fixed — primary buttons now use the repo idiom `bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90`; secondary buttons use a bordered navy/white treatment |
| D-12 | `bg-ls-grey-light/50` used in the progress track and unselected radio dot; `--color-ls-grey-light` is not a defined token (only `--color-ls-grey-light-text`), so both rendered transparent | Medium | Fixed — remapped to `bg-ls-grey-light-text/30` |
| D-13 | Modal lacked `role`/`aria-modal`; close button was icon-only with no accessible name; decorative background image carried a redundant `alt` | Medium | Fixed — added `role="dialog"`, `aria-modal="true"`, `aria-label`, button `type`/`aria-label`, and `alt=""` + `aria-hidden` on the scrim |

### Not fixed after review (with rationale)
- **Keyboard access to the 10 interactive workflow cards** (`BeforeAfterWorkflow.tsx:439,676`): they are `<div onClick>` with no `role`, `tabIndex`, or key handler, so the inspector is mouse-only. Fixing this requires restructuring each card into a `role="button"` with key handling; the component is prototype-inherited and this is a larger refactor than the recovery itself. Non-blocking, but a genuine a11y gap on `/what-we-do`.
- **Escape-to-close / focus trap** on the same modal: needs an added effect and focus management; deferred with the item above.
- **Light-theme contrast** (`text-[#00BFFF]` on white ≈2.0:1): prototype-inherited palette choice used across the recovered component; changing it diverges from the AI Studio visual reference and should be decided with brand sign-off.
- **Colour drift** `#E63946` vs brand token `#DC3641`: intentional-looking in the prototype; normalising it changes the recovered visual. Left for brand review.
- **Second build warning** `[file\:line]` CSS property: confirmed by QA to originate from third-party Open Design preview CSS bundled into the stylesheet, not from `src/`. Cosmetic.

### Final gate results (after fixes)
| Gate | Result |
|---|---|
| `npx tsc --noEmit` | Exit 0 |
| `npx vitest run` | 16/16 files, 145/145 tests passed |
| `npx vite build` | Success, 27.43s |
