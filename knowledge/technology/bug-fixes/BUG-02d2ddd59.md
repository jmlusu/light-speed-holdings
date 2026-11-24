# fix: repoint production image URLs to published AVIF assets

**ID:** BUG-02d2ddd59
**Date:** 2026-11-23
**Resolved:** resolved
**Commit:** 02d2ddd591de261e0f1267885f52bc61c79908ac
**Issue:** (none - conventional-commit fix: without an issue reference)

## Original Issue Body

(No linked issue. The engineer should link or file one.)

## Root Cause (filled by the resolving engineer)

Recorded in the commit message: The previous commit misdiagnosed the cause as CSP. The header is report-only, so it cannot block images, and relaxing img-src broke the pinned security-header contract. Real cause: 38 quoted /src/assets/images/*.jpg literals that Vite copies verbatim into the bundle (paths that do not exist under public/), with the ...

_Source: commit 02d2ddd591de261e0f1267885f52bc61c79908ac message (verbatim excerpt)._

## Fix (filled by the resolving engineer)

The previous commit misdiagnosed the cause as CSP. The header is report-only, so it cannot block images, and relaxing img-src broke the pinned security-header contract. Real cause: 38 quoted /src/assets/images/*.jpg literals that Vite copies verbatim into the bundle (paths that do not exist under public/), with the SPA rewrite masking each 404 as 200 text/html. Repoint them to the registered /assets/images/*.avif variants, restore the CSP, and turn the vacuous media guard into a real no-bundled-literal assertion. Also refresh stale copy expectations from the marketing rewrite and add the new insight to the sitemap.

_Source: commit 02d2ddd591de261e0f1267885f52bc61c79908ac message (verbatim)._

## Files Changed

knowledge/technology/bug-fixes/BUG-eea7fe4fc.md
public/sitemap.xml
src/__tests__/footer-disclosure.test.tsx
src/__tests__/haomtgv/HaomtgvGlyphGallery.test.tsx
src/__tests__/haomtgv/HaomtgvPage.test.tsx
src/__tests__/media-registry.test.ts
src/__tests__/nav/FloatingNav.test.tsx
src/__tests__/sitemap.test.ts
src/components/AboutSection.tsx
src/components/BeforeAfterWorkflow.tsx
src/components/HeroSection.tsx
src/components/SiteFooter.tsx
src/components/home/IntentToExecutionLifecycle.tsx
src/components/home/LightSpeedProposition.tsx
src/components/home/VisitorPathsSection.tsx
src/components/home/WhatWeBuildGrid.tsx
src/components/site/CtaBand.tsx
src/components/whatwedo/SixCapabilitiesSection.tsx
src/data/siteContent.ts
src/pages/InsightArticlePage.tsx
src/pages/InsightsPage.tsx
src/pages/_tests__/WhatWeDoPage.test.tsx
vercel.json

_Source: GitHub commit 02d2ddd591de261e0f1267885f52bc61c79908ac file list, filtered to text/source files._

## Diagnostic Commands

Not recorded in the commit message.

## Verification

Not recorded in the commit message.

Commit is present in the current origin/main history; CI was not re-run for this record.

## Link an Issue

If this is a tracked bug, add Closes #N to a future commit or
file an issue and link it so the record becomes issue-backed.
