# Marketing Redesign — Remaining Issues Tracker

Trackable plan to close the gaps listed in the session summary. Update status as items complete.

## Phase 1 — Image uniqueness & coverage (P1)
- [x] **R1** Audit all `/assets/images/*` references across `src/`. Build a duplicate/orphan report. (see `image-audit-report.md`)
- [~] **R2** Remove or replace duplicate references so each image is used exactly once. (Partial: /assets/images duplicates 16→8; remaining aistudio/diagram duplicates are intentional reuses in components — strict uniqueness blocked: only 8 unused registered assets remain, all logos/favicons)
- [x] **R3** Uniqueness/registration coverage: existing `media-registry.test.ts` already asserts no unregistered image paths; strict duplicate-count test deferred until R2 fully resolved.
- [ ] **R4** Add big imagery to remaining pages that only have a single image (HAOMTGV, Privacy, Terms) — second image or carousel.

## Phase 2 — Carousels & infographics (P1)
- [x] **R5** Add `ImageCarousel` to at least 2 more pages (What We Do, About or Insights).
- [x] **R6** Add `InfographicBlock` (mission/vision/values or page-specific) to at least 2 more pages. (Home + About)
- [ ] **R7** Add carousels/infographics to HAOMTGV, Privacy, Terms, and 404 where appropriate.

## Phase 3 — Accessibility (P1)
- [x] **R8** Replace generic alt text ("Contact", "FAQ", "Terms") with descriptive, context-specific alt text.
- [x] **R9** Verify skip link, focus-visible rings, and keyboard navigation on all new sections.
- [x] **R10** Confirm `prefers-reduced-motion` collapses animations on new components.

## Phase 4 — Responsive & dark mode (P2)
- [ ] **R11** Visual QA of big images on mobile (320–640px): crop points, height, text overlay legibility.
- [ ] **R12** Visual QA in dark mode: overlay gradients, caption contrast, carousel controls.
- [ ] **R13** Run `ls-artifact-qa` (or Playwright screenshots) across all pages in both themes.

## Phase 5 — Content copy (P2)
- [ ] **R14** Replace placeholder captions with final marketing copy (reviewed by CMO/product marketing).
- [ ] **R15** Finalize infographic labels and values against brand messaging.

## Phase 6 — Release (P0/P1)
- [ ] **R16** Confirm PR #615 CI green (Vercel preview + required checks).
- [ ] **R17** Merge to `main` only after CI green and CEO approval.
- [ ] **R18** Post-launch: capture engagement metrics (time on site, scroll depth, contact conversions).

## Tracking
- Owner: lead-frontend (implementation), qa-lead (verification), cmo (copy).
- Each item should be a separate commit/PR or grouped logically; update checkboxes here as done.
- Verification gate: `tsc --noEmit` clean + `vitest run` all green + Playwright smoke before merge.
