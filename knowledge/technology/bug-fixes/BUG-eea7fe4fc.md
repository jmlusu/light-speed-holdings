# fix: restore marketing images in production and refresh site copy

**ID:** BUG-eea7fe4fc
**Date:** 2026-11-23
**Resolved:** resolved
**Commit:** eea7fe4fc25e054d80635ac4b97fde8f7e85a5ea
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

Marketing images did not render on the production Vite/React site deployed to Vercel.

## Root Cause (filled by the resolving engineer)

Commit eea7fe4fc misdiagnosed the cause as the CSP `img-src` directive in
`vercel.json` and relaxed it to `img-src 'self' data: https:`. That was wrong on
two counts:

1. The header is `Content-Security-Policy-Report-Only`, so it cannot block any
   resource.
2. `src/__tests__/security-headers.test.ts` deliberately pins
   `img-src 'self' data:`; the change broke that contract and the
   Site Build + Principles Gate in CI.

The actual cause: 38 string literals across 13 source files still referenced
`/src/assets/images/*.jpg`. Vite only rewrites real ES imports and CSS `url()`
tokens - quoted strings in JSX/data objects are copied verbatim into the
production bundle, where those paths do not exist under `public/`. The SPA
catch-all rewrite in `vercel.json` (`/(.*)` -> `/index.html`) then returned
`200 text/html` for each image request, so browsers received HTML instead of an
image. The same defect had been fixed previously and was reintroduced by the
prototype redesign reset.

Live evidence at diagnosis: `/src/assets/images/hero_cinematic_landscape_day.jpg`
returned `200 text/html`, while `/assets/images/hero_cinematic_landscape_day.avif`
returned `200 image/avif`.

## Fix (filled by the resolving engineer)

- Reverted the ineffective `https:` addition to the report-only CSP in
  `vercel.json`.
- Repointed all 38 `/src/assets/images/*.jpg` literals to the published
  `/assets/images/*.avif` variants that already exist under `public/` and are
  registered in `src/data/registries/media-registry.json`.
- Replaced the vacuous media-registry guard (which only checked that bundled
  references existed on disk) with an assertion that no `/src/assets/**`
  image literal exists at all.
- Refreshed stale test expectations for the intentional marketing-copy rewrite
  (CTA label "Contact Us", new HAOMTGV/footer/glyph copy) and added the new
  `why-we-built-90-agents` insight to `public/sitemap.xml`.

## Files Changed

- `vercel.json`
- `public/sitemap.xml`
- `src/components/{AboutSection,BeforeAfterWorkflow,HeroSection,SiteFooter}.tsx`
- `src/components/home/{IntentToExecutionLifecycle,LightSpeedProposition,VisitorPathsSection,WhatWeBuildGrid}.tsx`
- `src/components/site/CtaBand.tsx`
- `src/components/whatwedo/SixCapabilitiesSection.tsx`
- `src/data/siteContent.ts`
- `src/pages/{InsightArticlePage,InsightsPage}.tsx`
- `src/__tests__/{footer-disclosure,media-registry,sitemap,security-headers}.test.ts*`
- `src/__tests__/haomtgv/{HaomtgvGlyphGallery,HaomtgvPage}.test.tsx`
- `src/__tests__/nav/FloatingNav.test.tsx`
- `src/pages/_tests__/WhatWeDoPage.test.tsx`

## Diagnostic Commands

- `gh pr checks 603`
- `gh run view 45261360223 --log-failed`
- `npx vitest run <affected test files>`
- `npm run build`
- `npm test`
- `Select-String -Path dist/assets/*.js -Pattern '/src/assets/images/' -SimpleMatch`

## Verification

- Local: `npm run build` passed; `npm test` passed (17 files, 154 tests).
- Built JS bundle contains no `/src/assets/images/` literals.
- CI: PR #603 checks re-running after the corrective commit.
