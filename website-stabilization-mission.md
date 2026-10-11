# Website Stabilization Mission — Execution Plan

Mission source (verbatim): `C:\Users\jmlus\AppData\Local\Temp\opencode\mission.txt` (2110 lines).
Evidence baseline: `reports/website-capability-audit-2026-10-07.md`.
Scope: external website only (`src/`, `api/`, `public/`, `index.html`, `vercel.json`, website tests/config/docs). Never touch `src/ai_company/`, CEO Dashboard, Athena, Python systems.

**CEO decisions locked:**
1. `/use-cases` → **activate with link fix** (convert imports, remove/replace dead `View Details` detail links, wire nav + sitemap + tests; no new detail page).
2. The 5 legacy routes → **hard 404** (no new redirects; existing 4 unrelated redirects in vercel.json stay).

---

## Verified ground truth (Phase A complete)

- **Route tree (`src/App.tsx`)**: 19 routes — `index, what-we-do, ai-company-builder, solutions, sectors, proof, insights, insights/:slug, about, contact, ask, legal/privacy, legal/terms` (retain) + `architecture, build, offer-b, offer-c, offer-e` (remove) + `*` → `<Navigate to="/" replace />` (replace with real 404).
- **Alias divergence (Req N)**: `vite.config.ts` maps 12 `@lightspeed/data/*` → gitignored `./data/*`; `tsconfig.json` maps the same 12 → `src/data/*` (different files for metrics/capabilities/insights/faqs/claims/media). Exactly 4 importer files, all orphaned: `cta/CTA.tsx`, `header/Header.tsx`, `footer/Footer.tsx`, `pages/UseCasesPage.tsx`. Root `data/` exists locally but is gitignored (`.gitignore:89`) → must not remain load-bearing.
- **`@lightspeed/design-system`** aliases are identical in vite + tsconfig and target tracked `packages/design-system/` → **keep**.
- **Orphan clusters (no live importers, verified)**: `PageShell` → imports `Header`+`Footer`; `CTA` standalone; `Index.tsx` → imports `Hero/FeatureGrid/KPIBand/TrustStrip/Playground`. Live equivalents are `SiteLayout`/`FloatingNav`/`SiteFooter`/`HeroSection`.
- **Legacy components** imported only by the 5 legacy pages + orphan `Index.tsx`: `Hero, FeatureGrid, KPIBand, TrustStrip, Playground`.
- **Newsletter (Option B)**: `components/NewsletterSignup.tsx` rendered in `InsightsPage.tsx:152` + `InsightArticlePage.tsx:237`; telemetry events `newsletter_started/completed` in `hooks/useJourneyEvents.ts:18-19`. No `api/newsletter` file (check submit target during work).
- **`api/`**: `enquiry.ts`, `journey-events.ts`, `ping-edge.ts`, `ping-nodejs.js`, `ping.ts`.
- **"Executive Briefing"**: modal `ExecutiveBriefingModal` rendered by `SiteLayout.tsx:55`, state lives in `App.tsx` (`requestBriefing`). Keep feature; **reword all public copy** to approved CTA language + fix dialog a11y (filename/internal identifiers are not public-facing).
- **§17 readiness**: all `UseCasesPage` imports resolve to tracked `src/data/{use-cases,sectors,solutions}/registry.ts` (exports verified) + `packages/design-system` (tracked) + `src/layouts/PageContainer.tsx` (exists).
- **`packages/`**: `design-system` (keep), `data-use-cases` (3rd registry copy — investigate consumers; delete if orphan per §18).
- **tsconfig**: `include: ["src"]` — orphan files still type-check, which is why CI passes today.
- **Gates**: `npm run lint` / `npm run build` = `tsc --noEmit`; `npm run test` = `vitest run` (live: 38 = governance 21 + companyData 17); `python scripts/test/check-site-form-backend.py`; CI = `.github/workflows/{ci.yml, site-principles-gate.yml}` (bun). Playwright in devDeps but **no root config**.
- **Live CTA truth**: `src/data/ctas.ts` (tracked) vs orphan `src/data/ctas/registry.ts` + `src/data/registries/cta-registry.json`.
- **`.env.example` S-7 duplicate claim stale** (single `TURNSTILE_HOSTNAMES` at L32) — report as not-reproducible.

---

## Track partition (disjoint file ownership — no two agents edit the same file)

### Track 1 — Routing, deletion, alias divergence, registries (me, sequential, first)
Owns: `src/App.tsx`, `vite.config.ts`, `tsconfig.json`, `src/pages/UseCasesPage.tsx`, `src/pages/NotFoundPage.tsx` (new), files listed under **Delete**, §18 registry files.

1. **Baseline first**: record `git status` (exclude pre-existing unrelated modified files), run `npm run lint && npm run test && npm run build && python scripts/test/check-site-form-backend.py` to capture pre-existing pass/fail state.
2. `App.tsx`: remove 5 legacy imports/`withSite` wrappers/routes; add `use-cases` route; replace catch-all `*` with `<NotFoundPage />` (Req F real 404 — unknown routes must show a real not-found page with nav home, not a silent redirect).
3. **New** `src/pages/NotFoundPage.tsx` (SiteLayout-consistent, branded, links to active routes).
4. `UseCasesPage.tsx`: convert 3 alias imports → relative (`../data/use-cases/registry` etc.); remove/replace dead `View Details → /use-cases/:slug` links (no detail page exists) with honest working links (contact/CTA per `src/data/ctas.ts`); verify filters, empty states, headings.
5. **Delete** (after re-verifying zero live importers):
   - pages: `Architecture, Build, OfferB, OfferC, OfferE, Index` (orphan; must go once its legacy components go)
   - components: `Hero, FeatureGrid, KPIBand, TrustStrip, Playground` + orphan cluster `layouts/PageShell`, `components/header/Header`, `components/footer/Footer`, `components/cta/CTA`
6. **Alias removal**: delete all 12 `@lightspeed/data/*` entries from `vite.config.ts` **and** `tsconfig.json` paths (keep `@/*` + `@lightspeed/design-system{,/tokens}`). Root `data/` dir left in place (untracked) — noted as out-of-scope in report.
7. **§18 registry determination** (5-step per registry: canonical source → active consumers → obsolete → migration → delete/deprecate): sectors (3 tracked variants: `sectors.ts`, `sector-registry.ts`, `sectors/registry.ts`), ctas (`ctas.ts` live vs `ctas/registry.ts` + `registries/cta-registry.json` orphan), faqs (`faqs.ts` vs `registries/faq-registry.json`), claims/metrics (tsconfig points at `registries/claims-registry.json` — verify consumers), `packages/data-use-cases` (delete if no consumers). Never delete merely because unused — document rationale for each.
8. **No vercel.json edits here** (owned by Track 4).

### Track 2 — Content truth & integrity tests (subagent, parallel)
Owns: `src/data/{metrics.ts, siteContent.ts, faqs.ts, useCaseCatalogData.ts, ctas.ts, ...}`, `src/data/registries/*` (canonical files only), `src/__tests__/*`, `ProofPage.tsx`, `AiCompanyBuilderSection.tsx`, plus rendered-copy passes on live pages/sections (HeroSection, home sections, AskLightSpeed, SiteFooter, ContactSection...).
- Req B: canonical public-truth mechanism; approved sources for agents/claims/metrics/sectors/FAQs/capabilities/proof/geo; `AVAILABLE|IN PILOT|DEMONSTRATED|DELIVERED|RESEARCH` classifications; hard-coded metrics eliminated.
- §6 corrections: **90 total = 89 AI + 1 Human CEO** everywhere (no 37/91/"90 AI agents + 1 human"); test-count resolution = live gate is `vitest run` = 38 → publish one supported value from one source **or remove** the claim (mission rule: don't pick the impressive number); remove/quarantine "40% faster", "60% reduction", SADC "ratified", `PARTNER 01–05`, `results/*.json`, "Executive Briefing"/"Schedule an Executive Walkthrough" rendered copy (incl. `ProofPage.tsx:61,64`); CTA copy must agree with canonical `ctas.ts`.
- **Fix the architectural weakness**: governance/integrity tests must validate *rendered/public content* (import what pages render / scan built strings), not just the registry. Add production content-integrity tests failing on: stale counts, banned claims, banned CTAs, nonexistent evidence refs, placeholder case studies, values bypassing the registry.
- Do not edit files owned by other tracks (no `App.tsx`, no `UseCasesPage.tsx`, no `index.html`, no `vercel.json`).

### Track 3 — Newsletter removal, forms, Turnstile (subagent, parallel)
Owns: `NewsletterSignup.tsx` (delete), `InsightsPage.tsx`, `InsightArticlePage.tsx` (remove usage + `newsletter` copy/anchors), `useJourneyEvents.ts` (remove newsletter event types), `api/journey-events.ts` (only if it whitelists those events), `hooks/useTurnstile.ts`, `api/enquiry.ts`, `ContactSection.tsx`, `ContactPage.tsx`, form components.
- Option B full removal: UI, CTAs, forms, API action, copy, double-opt-in claims, telemetry, success states (then re-run form guard).
- Turnstile (Req K): keep server verification, hostnames allowlist, honeypot strengths; add missing `error-callback` (`useTurnstile.ts:41-45`) → **visible error/retry state**, never silently stuck; S1 fail-open, S2 spoofable IP, S3 unbounded buffers; diagnose 110200 (Cloudflare Hostname Management missing origin — document exact dashboard steps as CEO action); production browser verification → see Phase 5.
- Do NOT edit `ExecutiveBriefingModal`/`SiteLayout`/`App.tsx` (modal rewording stays with content-truth copy pass + dialog a11y with Track 5 — **decision: Track 5 owns `ExecutiveBriefingModal.tsx` + `SiteLayout.tsx`**, Track 2 owns any *CTA strings* inside them by handing exact string changes to Track 5 at dispatch to avoid dual writers; alternatively Track 2 does reword first, Track 5 applies a11y after — sequence: Track 2 → Track 5 for these two files).

### Track 4 — SEO, metadata, robots/sitemap, security headers (subagent, parallel)
Owns: `index.html`, `vercel.json`, `public/robots.txt` (new), `public/sitemap.xml` (new), new `src/config/site.ts` (`SITE_ORIGIN = https://lightspeedholdings.vercel.app` single configurable base per Req A), new per-page metadata hook (no new deps — small `usePageMeta` effect; check package.json first for an existing head library).
- `index.html`: canonical, robots meta, theme-color, og:url, absolute og:image (`https://lightspeedholdings.vercel.app/og-default.png`), twitter cards, JSON-LD where justified; zero legacy `.com` domain refs.
- `robots.txt` + `sitemap.xml` generated from the **final active route list** (given upfront): `/`, `/what-we-do`, `/ai-company-builder`, `/solutions`, `/sectors`, `/proof`, `/insights`, `/about`, `/contact`, `/ask`, `/use-cases`, `/legal/privacy`, `/legal/terms` (insight article slugs optional/added from registry).
- `vercel.json` (sole owner): existing 4 redirects kept; **no** new legacy redirects (hard 404 decision); missing static asset → real 404 not SPA shell (test with a bogus `.js`/`.png` URL strategy per §25); security headers: CSP, HSTS, plus keep existing 3; preserve SPA fallback for client routes.
- Doc inputs for Phase 4: record final metadata/sitemap/header design for handoff.

### Track 5 — Accessibility + automated a11y (subagent, parallel, starts after Track 2 finishes rewording in the 2 shared files)
Owns: `FloatingNav.tsx` (aria-expanded, ≥44×44 touch targets, desktop aria-label), `ExecutiveBriefingModal.tsx` + `SiteLayout.tsx` (dialog role/aria-modal/Escape/focus trap; remove `focus:outline-none` on main), `AiCompanyBuilderSection.tsx` **only after Track 2 completes** (dangling `aria-labelledby:55,80,104`), honeypot `aria-hidden`/`inert`, duplicate landmarks/duplicate headings sweep, contrast: derived AA-compliant darker variants of brand hues for small text (`#E63946` 4.17:1, `#00BFFF` 2.12:1) — **no invented brand colors**; keep skip link/focus-visible/reduced-motion/labelled forms/role=alert.
- Automated a11y coverage (§25): Playwright-based assertions (focus order, aria presence, touch-target size, contrast spot-checks via computed styles) — avoid new heavy deps (axe) unless already present; check `package.json` first.

### Shared-file sequencing rule
`AiCompanyBuilderSection.tsx`, `ExecutiveBriefingModal.tsx`, `SiteLayout.tsx` are the only cross-track files → strictly serialized: Track 2 (reword) → Track 5 (a11y). All other files single-owner.

---

## Phases

- **Phase 0** — Baseline gates + git status inventory (done as Track 1 step 1).
- **Phase 1** — Track 1 (me): routes, 404, deletions, alias removal, §18 registries, `/use-cases` activation. Verify: `tsc` + vitest + build green after this phase.
- **Phase 2** — Dispatch Tracks 2, 3, 4 in parallel (file-disjoint, final route list embedded in prompts); then Track 5 after Track 2's shared files land. Each agent gets: mission.txt line ranges (A=218, B=300, C=586, D=646, E=716, F=750, G=786, H=828, I=878, J=910, K=972, L=1052, M=1100, N=1160, O=1228, P=1270, §23=1424-1558, §24=1564, §25=1770, §26=1934, §27=1984), forbidden lists (banned claims, out-of-boundary paths), and the exact other-track file lists.
- **Phase 3 — E2E/smoke (Req P)** (me): root `playwright.config.ts` + `tests/e2e/*.spec.ts` covering §23 verify list: every active route 200/renders, nav + footer links resolve, 404 behavior, `/robots.txt`, `/sitemap.xml`, metadata (title/description/canonical/og:url/og:image absolute), critical assets, mobile/desktop layouts, dark/light themes, contact form (validation + mocked `/api/enquiry` success/error + Turnstile failure visible), no console/network uncaught errors, content-integrity spot checks (no banned strings, no newsletter remnants, no legacy route links). Run against `vite preview`. Wire CI job (extend `ci.yml`; playwright already in devDeps — verify, no lockfile churn if possible).
- **Phase 4 — §22 docs alignment**: `docs/architecture/ROUTE_MIGRATION_V2.md` (removed/retained routes + rationale), `docs/WEBSITE_ARCHITECTURE.md` (+ fix `:493` domain ref), `docs/content-architecture/sitemap.yaml`, imagery specs (`docs/website-imagery-spec.md`, `docs/IMAGE_SPEC.md:448`), README (exact targets per mission §22). Out-of-boundary docs (ADRs, `docs/marketing/*`, `docs/legal/*`, AGENTS.md, `.opencode/*`) → report-only.
- **Phase 5 — Gates + §24 searches + verification**:
  - `npm run lint`, `npm run test`, `npm run build`, `python scripts/test/check-site-form-backend.py`, `npx playwright test`.
  - §24 exact searches with expected results: legacy `.com` domain → 0 production refs; `/build /architecture /offer-b /offer-c /offer-e` → no active route/nav ref; `newsletter|double opt-in|unsubscribe|subscription|subscriber` → no feature/misleading promise (agent-mission JSON mentions of "the newsletter" reviewed & classified, not feature refs); `Executive Briefing` → 0 public-facing; `37 agents|37 Agents|91 agents|90 AI agents|143 agents` → no contradiction; `40% faster|60% reduction|PARTNER 01–05|ratified` → every hit reviewed, none unsupported.
  - Production verification: browser test contact/Turnstile on currently deployed site (Playwright vs live URL) per Req K manual sequence; robots/sitemap/404/metadata re-verify **after deploy** (changes not committed per §26 — deploy requires CEO instruction) → drives `COMPLETE WITH CONDITIONS` status + next-step item.
- **Phase 6 — §26 inventory** (changed/deleted/added files, routes removed/retained, canonical registries, claims changed, tests added/executed, production results, risks, intentionally-not-changed incl. `Index`/`PageShell` rationale, root `data/` dir, out-of-boundary docs) + **§27 CEO report** in exact structure (`STATUS / EXECUTIVE SUMMARY ≤150 words / BEFORE→AFTER / PUBLIC WEBSITE / CONTENT TRUTH / TEST RESULTS table / REMAINING RISKS / OUT OF SCOPE / RECOMMENDED NEXT STEP ≤5`), evidence-backed, no success claims without gate output.

## Known risks / honest constraints
1. **Turnstile 110200 hostname fix requires Cloudflare dashboard action by CEO** (I can diagnose, implement error-retry UX, document exact steps; cannot add hostname myself). Manual verification on live site will likely still fail until then → REMAINING RISKS + next step.
2. **New changes unverifiable in production until commit/deploy** (§26 forbids committing without instruction) → STATUS likely `COMPLETE WITH CONDITIONS`.
3. **Playwright/CI wiring** may need lockfile/CI-browser-install changes; if `bun install --frozen-lockfile` conflicts, fall back to running e2e as a separate non-bun job and document.
4. **Brand contrast**: AA fixes use darkened variants of existing brand hues only — flagged for CEO approval in report if any token is introduced.
5. Pre-existing unrelated modified files excluded from the change set.

## Out of scope (report only)
`src/ai_company/`, dashboard, Athena, Python systems, ADRs, `docs/marketing/*`, `docs/legal/*`, `harness/changes/parking/*`, `AGENTS.md`, `.opencode/*`, `company/*`, parked-domain DNS reclaim, root `data/` local dir deletion, orphan-but-pre-existing files not made obsolete by this work (none remain — all deletions above are §18/§19-justified).
