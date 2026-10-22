# MVP Launch Readiness Report — 2026-10-13

**Site:** lightspeedholdings.vercel.app
**Branch:** `chore/remove-legacy-marketing-site-pages` @ `52aca095` (+ working-tree changes below)
**Audit baseline:** `docs/website/audit-2026-10-13-post-implementation.md` (commit `449a6df3`)
**Scope:** CEO MVP realignment — defer Use Cases & Sectors, fix P0–P6, no rebuild, no registry migration.

---

## Executive verdict

**READY FOR STAGING, NOT PRODUCTION**

Local gates are green (tsc, vitest 41/41, Vite production build, link/route smoke). Production Turnstile hostname allowlist and live response headers have not been verified against a deployed URL. Launch production only after the two external checks in §Verification gaps.

---

## Defect dispositions (P1–P6 + audit D1–D7)

| ID | Sev | Finding | Status | What was done |
|----|-----|---------|--------|---------------|
| **D1 / P1** | **P1** | Dual registry + `@lightspeed/data/use-cases` alias; `/use-cases/<slug>` detail pages broken | **DEFERRED BY CEO DIRECTIVE** | Routes removed from `App.tsx`. Index `/use-cases` and `/sectors` → `<Navigate to="/solutions" replace />` + permanent Vercel redirects. Slug paths fall through SPA `*` → `NotFoundPage`. Root `data/` vs `src/data/` divergence **not** fixed. |
| **D2 / P2** | P2 | Hero `#operating-model` had no target (id is `haomtgv`) | **FIXED** | `HeroSection.tsx:155` → `href="#haomtgv"`. `VisitorPathsSection.tsx:45` path-2 → `to: '#haomtgv'`. Target id confirmed at `HAOMTGVSection.tsx:80`. |
| **D3 / P4** | P3 | Turnstile error `400020` on localhost | **OPEN — external** | Expected on localhost (hostname not in Cloudflare allowlist). Production Turnstile **NOT VERIFIED** — no production URL checked this session. |
| **D4 / P3** | P3 | `logo-full-v2.svg` missing alt | **FIXED** | `Logo.tsx:25` always sets `alt` — first instance `alt="LightSpeed Holdings Limited"`, subsequent `alt=""` (WCAG decorative). Static HTML assets already correct. No raw `<img>` without `alt` for this asset in active `src/`. |
| **D5 / P5** | P3 | No CSP / HSTS / Permissions-Policy in `vercel.json` | **FIXED (config)** | Added `Strict-Transport-Security` (max-age=63072000; includeSubDomains; preload), `Permissions-Policy` (camera/mic/geo/payment/usb denied), baseline `Content-Security-Policy` allowing self + Cloudflare Turnstile (`challenges.cloudflare.com`) for script/connect/frame. **Live response headers NOT VERIFIED** until next production deploy. |
| **D6** | structural | Root `data/` vs `src/data/` registry divergence | **DEFERRED BY CEO DIRECTIVE** | Same root cause as D1; out of MVP scope. |
| **D7 / P6** | Info | Hard-coded `liveTestCount = 2566` vs actual suite | **FIXED** | `uv run pytest --collect-only -q` → **2586 collected** (67 deselected). Updated `metrics.ts` (`liveTestCount = 2586`), `metrics-registry.json`, `claims-registry.json` (`lastVerified: 2026-10-13`), `sector-registry.json` honesty note. Hero renders `liveTestCount.toLocaleString` → "2,586 Passing". |

---

## P1 surface area (IA deferral)

**Active nav / footer**
- `FloatingNav.tsx` — `Use Cases` and `Sectors` removed from `NAV_LINKS`.
- `SiteFooter.tsx` — sector links removed; heading → `INSIGHTS & ABOUT`.
- `HomePage.tsx` — `UseCasesSection` import + JSX removed; comments renumbered.

**Routes (`App.tsx`)**
- Retained: `/`, `/what-we-do`, `/ai-company-builder`, `/solutions`, `/ai-assessment`, `/insights`, `/insights/:slug`, `/about`, `/contact`, `/legal/privacy`, `/legal/terms`, `*` NotFound.
- Redirects: `/use-cases` → `/solutions`; `/sectors` → `/solutions`; `/proof` → `/insights`; `/ask` → `/contact`; legacy offers → `/solutions`.

**Vercel edge redirects (`vercel.json`)**
- `/use-cases` → `/solutions` (permanent)
- `/sectors` → `/solutions` (permanent)
- `/work`, `/evidence` → `/insights` (updated from dead `/proof`)
- Slug variants intentionally **not** edge-rewritten — SPA NotFound handles them.

**Content / data**
- `homeImmersiveCopy.ts` — use-cases chapter dropped; remaining chapters 01–05.
- `VisitorPathsSection.tsx` — path-3 → Solutions/Contact.
- Related-links purged on About, AiCompanyBuilder, Insights, Solutions, WhatWeDo, InsightArticle pages.
- Sector chips → plain text on Solutions / WhatWeDo / InsightArticle.
- `usePageMeta.ts` — `/sectors`, `/use-cases` meta removed.
- `useJourneyEvents.ts` — `/sectors` dropped from journey array.
- `sitemap.xml` — both URLs removed.
- `robots.txt` — both `Allow` lines removed.

**Intentionally untouched (dead code, not in router)**
- `Header.tsx`, `Footer.tsx`, `PageShell.tsx`, `AskLightSpeed.tsx`, `UseCasesSection.tsx`, `SectorsPage.tsx`, `SectorDetailPage.tsx`, `UseCasesPage.tsx`, `UseCaseDetailPage.tsx`.
- CTA registry JSON still lists `EXPLORE USE CASES` → `/use-cases` (stale string only; no live route).
- Barrel `home/index.ts` no longer exports `UseCasesSection`.

---

## Verification (this session)

| Check | Result |
|-------|--------|
| `npm run lint` (tsc --noEmit) | **PASS** (clean) |
| `npm run test` (vitest) | **PASS** — 3 files, **41/41** |
| `npm run build` | **PASS** — 1686 modules; dist written (pre-existing CSS minify warning on `[file:line]` utility only) |
| Python suite collect | **2586** collected, 67 deselected (`uv run pytest --collect-only -q`) |
| Preview smoke (`npm run preview`, :1440) | All primary + deferred paths return HTTP 200 SPA shell |
| Link/route scan (active `src/`) | No live nav/footer links to `/use-cases` or `/sectors`; remaining hits are dead code + tests + registry data only |
| Bundle secret scan | Clean — `index-*.js`, `vendor-react-*.js`, `vendor-ui-*.js` (no private keys / AWS / GitHub / OpenAI-style secrets) |
| Browser visual/a11y re-probe | **NOT VERIFIED** this session (no Playwright run); prior audit 2026-10-13 remains last full browser report |

---

## Verification gaps (must close before production launch)

1. **Turnstile on production hostname** — load `/contact`, `/insights` (briefing modal), newsletter; confirm widget renders, no `400020`, submit gating matches design.
2. **Live response headers** — after deploy, `curl -I https://lightspeedholdings.vercel.app/` must show HSTS, CSP, Permissions-Policy, nosniff, X-Frame-Options, Referrer-Policy.
3. **SPA client redirects on production** — `/use-cases` → `/solutions`, `/sectors` → `/solutions`, `/proof` → `/insights` (edge redirects cover the index paths; slug paths must show NotFound, not blank).
4. **Optional a11y re-probe** — prior audit's single `imgMissingAlt` should re-check as 0 given Logo.tsx alt handling.

---

## Residual / deferred risk

- Dual registry (`data/` vs `src/data/`) remains a structural landmine for any future use-case work (D6 / P1 root cause). Revisit outside MVP.
- CSP includes `'unsafe-inline'` for script and style (Vite/Turnstile practical baseline). Tighten after production smoke if no inline-script dependency is found.
- CTA registry still names deferred routes; harmless today (string only).
- Python suite size can drift; hero figure is pinned to the 2026-10-13 collect (2586) and will go stale unless re-collected on release.

---

## Recommendation

**READY FOR STAGING, NOT PRODUCTION.**

Ship to a staging/preview deploy now. Promote to production after (1) Turnstile succeeds on the real hostname and (2) security headers appear in live responses. No further code work is required for MVP scope unless the production checks fail.

---

*Report generated 2026-10-13 from local verification. Evidence limited to this session's tool output; no production deploy was performed.*
