# Tasks

## Format

- `- [x] T001 [US?] Action with target path and validation note`
- `[P]` means parallel-safe; `[US1]` maps to a user story when stories exist. All work below was sequenced by file ownership (no two tasks held the same file at once).

## Setup / Intake

- [x] T001 Review `spec.md`, `plan.md`, `PRODUCT.md`, `DESIGN.md` and the SDD ledger before implementation; confirm guardrails and the file-ownership contract.
- [x] T002 Preflight isolation (Task 0): stage the 19 pre-existing accessibility-polish `src/` files by explicit path and commit as `9ef4476b`; leave `opencode.json` unstaged.

## Implementation — five workstreams

- [x] T003 Task 1 homepage clarity — `src/components/home/HomeSection.tsx`, `VisitorPathsSection.tsx`, `WhatWeBuildGrid.tsx`, `InsightsSection.tsx`; new `src/__tests__/homepage-clarity.test.tsx`. Four primary paths, six unique capability-link names, one primary research link, two closed disclosures; copy preserved. Commit `76391fc8`; review APPROVE.
- [x] T004 Task 2 honesty badge legibility — `src/brand/tokens/brand-tokens.css`, `src/data/siteContent.ts`, `src/components/site/HonestyBadge.tsx`, `src/site/StatusBadge.tsx`, `src/site/CategoryChip.tsx`, `src/components/FaqCardList.tsx`, `src/components/whatwedo/SixCapabilitiesSection.tsx`; new `src/__tests__/honestyBadge.test.tsx` plus the `vitest.config.ts` alias. Commit `13c31427`; review required one fix round (Important finding: test copied JSX rather than importing `FaqCardList`), fixed in `8dc62f28`; 2 addressed, 0 open.
- [x] T005 Task 3 canonical line and cyan status — `src/components/HeroSection.tsx`, `src/components/AboutSection.tsx`, `src/components/home/AboutSection.tsx`, `src/components/SiteFooter.tsx`, `src/components/HeroBanner.tsx`, `src/components/AssessmentWizard.tsx`, `src/components/BeforeAfterWorkflow.tsx`, `src/components/ContentCarousel.tsx`, `src/components/whatwedo/OperatingModelOverview.tsx`, `src/components/whatwedo/SixCapabilitiesSection.tsx`, `src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx`, `src/pages/HAOMTGVPage.tsx`; new `src/__tests__/brand-governance.test.tsx`. Registry-sourced human-authority line, cyan-only trust palette, 24 `#DC3641` tokens removed. Commit `221d479a`; review APPROVE (24-vs-20 token count corrected in ledger).
- [x] T006 Task 4 claims evidence — `src/data/publicMetrics.ts` (new), `src/components/AboutSection.tsx`, `src/lib/enquiry.ts`, `src/components/site/CtaBand.tsx`, `src/components/ContactSection.tsx`, `src/components/ExecutiveBriefingModal.tsx`, `src/components/NewsletterSignup.tsx`, `src/components/AskLightSpeed.tsx`, `src/data/faqs.ts`, `src/data/registries/{claims,metrics,faq}-registry.json`, `src/components/BeforeAfterWorkflow.tsx`, `src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx`; new `src/__tests__/public-claim-guards.test.ts`. Registry-backed tiles, no `100%` absolute, no timing SLA. Commit `06463ab2`; review required one fix round (Important: registry-note contradiction), fixed in `1aa99c12`; 1 addressed, 0 open.
- [x] T007 Task 5 honest redirects and canonical IA — `src/lib/legacyRedirects.ts`, `src/components/site/LegacyRedirect.tsx`, `src/App.tsx`, `src/components/SiteLayout.tsx`, `src/components/home/VisitorPathsSection.tsx` (second owner, after Task 1); new `src/__tests__/legacyRedirects.test.tsx`. Single-hop redirects, visible moved notice, destination SEO preserved, Ask LightSpeed → `/contact`. Commit `a06504a1`; review APPROVE with one scoped test-contract correction accepted.

## Validation And Review

- [x] T008 Whole-branch integration review — REQUEST CHANGES, then one fix wave (`da6dd7d1`, theme-aware cyan text) and scoped re-review: 3 addressed, 0 open; whole branch APPROVED (ledger line 36 and 44).
- [x] T009 Close-out Lighthouse gate on preview 1440 — one `label-content-name-mismatch` fixed in `c3754e7d` (visible text included in capability-link accessible names); re-run 1.00/1.00/1.00, zero failures; scoped re-review clean (ledger lines 40 and 43).
- [x] T010 Run local validation gates — `npm test` 210 passed / 22 files; `npm run build` PASS (one pre-existing esbuild `file:` CSS warning); Lighthouse 1.00/1.00/1.00 zero failures; Impeccable 5 warnings triaged and accepted. All local only; CI not run.
- [x] T011 Complete the ECL records in `harness/changes/active/` — `summary.md`, `spec.md`, `tasks.md`, `reviews/review.md` filled from ledger and `git log main..HEAD`; `phase: validate`, reviews approved, validation results recorded; no archive, no staging.

## Deferred Tasks

Tracked in the SDD ledger for post-merge triage (handoff Step 3); not reopened in this change and not silently dropped:

- `qa-lead`: contrast test uses flat surfaces rather than 10% tints; jsdom `scrollTo` warnings in test output.
- `cto`: `src/design-system/components/Logo/Logo.tsx` retains three `#DC3641` values outside the current public render path; sibling cyan pillars and inspector badge in `OperatingModelOverview.tsx` still use `text-ls-cyan` on light surfaces; `InsightsSection.tsx:121` light hover class now equals its base.
- `clo`: `faq-registry.json` faq-28 answer still contains response windows while its note says no basis exists (public component renders `src/data/faqs.ts`, which no longer does).
- `cmo`: duplicate canonical enquiry sentence in the CTA band (`CtaBand.tsx` text prop plus built-in footnote).
- Pre-existing, not introduced here: esbuild `file:` CSS build warning and CRLF→LF `git diff --check` notices.
- `Task 5` duplicate `role="status"` + `aria-live="polite"` annotation is brief-mandated; retained deliberately.
