# Plan

## Technical Approach

This change addresses the gap between the live marketing site (`lightspeedholdings.vercel.app`) and the approved SPEC (`docs/website/SPEC.md`). The site is stable but not SPEC-complete. The work decomposes into four P0 items that must ship, three P1 items if capacity allows, and explicit P2 deferrals.

The core strategy:
1. **Fix the factual error first** (P0-1) — the 89/90 agent count contradiction is the highest-priority content honesty gap (tracks #302). A guard test prevents regression.
2. **Make orphan pages reachable** (P0-3) — `/haomtgv`, sector details, and use-case details already render; they just need links and sitemap entries.
3. **Refresh stale numbers** (P0-4) — pytest collection is 2,684 vs the published 2,586; vitest is 87 vs the published 17. Both verified today.
4. **Deliver SPEC-compliant nav** (P0-2) — the 8-item nav requires the D1/D2 decisions, so it ships last in this session to avoid rework if decisions change.

Each P0 item lands in its own PR for clean revert granularity. Branch from `origin/main` (NOT the current `feat/deck-gate` HEAD, which is 3 ahead / 2 behind).

## Impacted Modules And Files

| Module | Files | Change Type |
|---|---|---|
| Site content / claims | `src/data/siteContent.ts`, `src/data/faqs.ts`, `src/components/AiCompanyBuilderSection.tsx`, `src/pages/WhatWeDoPage.tsx`, `src/components/home/HighLevelOverviewSection.tsx`, `src/data/insights.ts`, `src/data/registries/faq-registry.json`, `src/data/registries/claims-registry.json` | Copy edit |
| Guard tests | `src/__tests__/claims.test.ts` (new), `src/__tests__/sitemap.test.ts` (new), `src/__tests__/metrics.test.ts` (new) | New test |
| Metrics / claims registry | `src/data/metrics.ts`, `src/data/registries/metrics-registry.json`, `src/data/registries/claims-registry.json` | Data update |
| Navigation | `src/components/FloatingNav.tsx`, `src/components/SiteFooter.tsx` | Component logic + a11y |
| Nav tests | `src/__tests__/nav/FloatingNav.test.tsx` (new) | New test |
| Sitemap | `public/sitemap.xml` | Regenerated |
| Page links | `src/pages/SectorsPage.tsx`, `src/components/home/HAOMTGVSection.tsx` | Add links |
| P1: FAQ | `src/data/registries/faq-registry.json`, `src/data/faqs.ts`, `src/__tests__/siteFaq.test.tsx` | Refactor + test |
| P1: Media | `data/media/registry.ts`, `src/__tests__/media-registry.test.ts` (new) | Prune + test |
| P1: Security | `vercel.json` | Headers |

## Interfaces, Data, Permissions

- **`src/data/registries/faq-registry.json`**: add optional `evidence?: string` field (claim id) to each item; update TypeScript interface in `src/data/faqs.ts` projection.
- **`src/data/metrics.ts`**: exported constants `liveTestCount`, `testCount` — consumers in `src/data/sectors.ts`, `src/data/governance.ts`, `src/data/registries/*` will pick up new values automatically.
- **`FloatingNavProps`**: `onRequestBriefing` may become unused in nav context; verify other callers (`SiteLayout.tsx`, `HomePage.tsx` hero CTAs) before removing from interface.
- **`vercel.json` headers**: additive only — `Permissions-Policy` and report-only CSP do not change existing behaviour.

No new permissions, no new API routes, no database changes.

## Spec Gaps Found From Planning

| SPEC Requirement | Current State | Gap Resolution |
|---|---|---|
| Eight-item primary navigation (Home, What We Do, AI Company Builder, Solutions, Use Cases, Sectors, Insights, About) | 6-item nav (missing What We Do, Use Cases, Sectors) | P0-2 implements 8-item nav |
| H-A-O-M-T-G-V framework explained as "90 operating roles. 89 AI agents. One Human CEO." with no contradictory claims | Live: "90 AI agents. One human CEO." | P0-1 fixes all occurrences |
| FAQ component accessible, keyboard-navigable, ≥22 evidence-controlled questions | 7 questions, no evidence field, accessibility gaps | P1-1 adds evidence field, projects from registry; a11y in P1-1 scope |
| Every use-case detail page reachable and in sitemap | Render but orphaned; sitemap omits 16 | P0-3 adds links + sitemap entries |
| Every sector detail page reachable and in sitemap | Render but orphaned; sitemap omits 6 | P0-3 adds links + sitemap entries |
| HAOMTGV page reachable and in sitemap | Renders at `/haomtgv`; orphaned; sitemap omits | P0-3 adds link + sitemap entry |
| Public numbers match verified claims | 2,586 / 17 vs actual 2,684 / 87 | P0-4 updates + guard tests |

## Risks And Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| 8 nav items overflow at 1024 px | Medium | Layout break, horizontal scroll | Measure in browser before commit; fallback: group Use Cases + Sectors under "Proof" dropdown (keeps pages reachable) |
| Editing published insight article (`insights.ts`) alters public artifact | Certain if we rewrite body | Credibility / audit trail | Add dated correction note at top; do NOT rewrite body |
| CSP breaks Turnstile silently | Medium | Contact form widget fails | Report-only CSP for one deploy; re-run contact-step-5 widget check before enforcing |
| `liveTestCount` change propagates to Sectors page evidence copy | Certain (used in `sectors.ts:126`, `governance.ts:131`) | Evidence text may read awkwardly | Verify rendered text after change; minor copy tweak if needed |
| `faq-registry.json` evidence field requires claim IDs that don't exist yet | Medium | Blocked on claim registry alignment | Map to existing `claim.agent-count`, `claim.hitl`, `claim.data-protection` etc.; create missing claims first if needed |
| Branch from `feat/deck-gate` HEAD instead of `origin/main` | Low (process guard) | PR includes unrelated deck-gate changes | Explicit gate in T000: branch from `origin/main` only |

## Verification Plan

### Pre-merge (per PR)
```powershell
npx tsc --noEmit --pretty false
npx vitest run --reporter=dot
bun run build
```

### Post-merge / post-deploy
```powershell
# Health
$r = Invoke-WebRequest -Uri "https://lightspeedholdings.vercel.app" -Method Head -UseBasicParsing; $r.StatusCode  # 200
$r = Invoke-WebRequest -Uri "https://lightspeedholdings.vercel.app/sitemap.xml" -UseBasicParsing
($r.Content -split '<loc>').Count - 1  # 44 URLs
```

### Browser verification (3 widths: 375, 1024, 1440)
- `/` — hero shows "2,684 tests collected"; claim reads "90 operating roles. 89 AI agents. One Human CEO."
- `/haomtgv` — renders, linked from homepage HAOMTGV section
- `/sectors` — 6 cards, each has "View sector →" link to `/sectors/:slug`
- `/sectors/financial-services` (or any) — renders with evidence
- `/use-cases` — 16 cards link to detail pages
- `/use-cases/uc-js-bar` (or any) — renders with real title (not "Use case not found")
- `/contact` — Turnstile widget renders at step 5, returns token
- Nav — 8 items at desktop; mobile toggle `aria-expanded`, `Esc` closes, focus trap, CTA links to `/contact`

### ECL gate
```powershell
.\scripts\maintenance\lint-ecl.ps1  # PASS
```

### Change close
```powershell
.\scripts\maintenance\harness-change.ps1 close site-claims-nav-sitemap-next-session
```
