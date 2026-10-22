# LightSpeed External Website — Final Handover Report

**Date:** 2026-10-13
**Auditor role:** Independent pre-handover verification (no code changes, no redesign, no deploy)
**Baseline:** `main` @ `9e031b64` (`copy: humanizer pass on marketing site content (#462)`), tracks `origin/main`
**Audience:** Human CEO + external reviewer (ChatGPT)

---

## A. Executive Summary

The external Vite/React site (repo-root `src/`, not `src/ai_company/`) is **healthy for independent review** — lint, unit tests, and production build all pass green on `main`. Content honesty, primary IA structure, insights archive, and secret hygiene are solid.

It is **not production-ready**. One P1 functional defect remains open: every use-case **detail** page renders "Use case not found" because a Vite alias resolves against a second, stale registry under repo-root `data/`. Live Playwright screenshots on `vite dev` (port 1441) confirm the failure for `uc-js-bar` and the dual-registry root cause is re-verified programmatically (zero slug overlap).

Secondary gaps against the approved SPEC: primary nav shows 6 of 8 required items (What We Do, Use Cases, Sectors missing from FloatingNav); AI Venture Studio has no route, nav entry, or sitemap URL despite existing as strategy docs; security headers on Vercel remain minimal (no CSP/HSTS).

| Verdict | Rating |
|---------|--------|
| **Ready for Independent Review** | **Yes — with conditions** (D1 fixed or explicitly deferred with owner) |
| **Ready for Production Release** | **No** (D1 blocking; D3 production Turnstile unverified) |

---

## B. Scope and Method

| In scope | Out of scope |
|----------|----------------|
| Repo inspection of `main` @ `9e031b64` | Redesign, layout changes, new features |
| `npm run lint`, `npm run test`, `npm run build` | Deploying or pushing to origin |
| `vite dev` on port **1441** (canonical dev port); Playwright screenshots | Claiming production CDN/header behaviour beyond `vercel.json` |
| Static source verification of claims, registries, Turnstile wiring, nav | Python pytest full suite execution (collect-only used) |
| Comparison against `docs/website/SPEC.md` success criteria | Email send path behind Turnstile (edge function not exercised) |
| Prior audit `docs/website/audit-2026-10-13-post-implementation.md` (base `449a6df3`) | Visual QA against untracked brand blueprint PNGs |

**Application boundary respected:** Vite/React uses 1441 (dev) / 1440 (preview). CEO Dashboard ports 8420/8421 were not bound. `vite.config.ts` hard-refuses 8420/8421.

**Baseline hygiene observation:** concurrent agent activity produced untracked planning files during this audit window (e.g. `ai_venture_studio_client_presentation*.md`, brand PNGs). These are not part of the audited tracked build.

---

## C. Baseline and Recent History

| Item | Value |
|------|--------|
| Branch | `main` (tracks `origin/main`) |
| HEAD | `9e031b64` |
| Working tree | Clean tracked state; untracked docs/PNGs present |
| Package | `lightspeed-holdings` v1.0.0 |
| ECL active change | None |

**Site commits since prior audit base `449a6df3`:**

| Commit | PR | Summary |
|--------|-----|---------|
| `2d2800fc` | #458 | Remove legacy marketing site pages and components |
| `6a6708b3` | #459 | Retire useCaseCatalogData, token mirrors, legacyPytestCount; reword Proof labels |
| `e5b353b2` | #460 | Unslop cleanup across site copy and registries |
| `8509b9cf` | #461 | Mark brand tokens canonical-only in skill asset table |
| `9e031b64` | #462 | Humanizer pass on marketing site content |

---

## D. Verification Commands

| Command | Result | Notes |
|---------|--------|-------|
| `npm run lint` | **PASS** | Script is `tsc --noEmit`; clean |
| `npm run test` | **PASS** — 41 tests | vitest: companyData 17, governance 21, siteFaq 3 |
| `npm run test -- --coverage` | **BLOCKED** | Missing dependency `@vitest/coverage-v8` — not installed; installing it would be a package change outside audit scope |
| `npm run build` | **PASS** (~11.8s) | One benign warning: `[esbuild css minify] "file" is not a known CSS property` |
| `uv run pytest --collect-only -q` | **2586/2653 collected** | Matches hard-coded `liveTestCount = 2586` |
| Playwright screenshots (dev 1441) | Captured | Home desktop, home mobile 375×667, `/use-cases/uc-js-bar` |
| `public/sitemap.xml` | 21 routes | No per-use-case detail URLs |

---

## E. Routing, Navigation, and SPEC Compliance

### Live routes (App.tsx)

Primary routes present and wired: `/`, `/what-we-do`, `/ai-company-builder`, `/solutions`, `/sectors`, `/sectors/:slug`, `/use-cases`, **`/use-cases/:slug`**, `/ai-assessment`, `/insights`, `/insights/:slug`, `/about`, `/contact`, `/legal/privacy`, `/legal/terms`, plus redirects (`/architecture` → builder, `/proof` → use-cases, `/ask` → contact, offer-a…e → solutions).

### Nav inventory (live)

| Surface | Items | SPEC 8-item? |
|---------|-------|--------------|
| **FloatingNav** (used by SiteLayout — the live chrome) | Home, AI Company Builder, Solutions, Insights, About, Contact | **No — missing What We Do, Use Cases, Sectors** |
| **Header.tsx** (defined but not mounted by SiteLayout) | Full 8-item: Home, What We Do, AI Company Builder, Solutions, Use Cases, Sectors, Insights, About | Yes (component only) |
| **SiteFooter** | Home, What We Do, AI Company Builder, Solutions, Insights, About, FAQ, Contact, Ask, Primary CTA, Legal | Partial — no Use Cases / Sectors |

**Finding N1 (P2):** SPEC success criterion "eight-item primary navigation is intact" is **not met on the live chrome**. FloatingNav is the only nav rendered; Header.tsx with the correct 8-item list is unused by SiteLayout. Mobile screenshot confirms hamburger collapses to 3 logo-adjacent controls + CTA.

### AI Venture Studio

| Check | Result |
|-------|--------|
| Route in App.tsx | **Absent** |
| Nav link (FloatingNav / Footer / Header) | **Absent** |
| Sitemap URL | **Absent** |
| `src/` history (`git log -S`) | Never existed in site sources |
| Strategy docs | Present under `docs/venture-studio/` (older parallel IA: `/work`, `/evidence`, `/why`, `/industries/*` — does not match current SPEC) |
| SPEC.md 8-item nav | Does **not** include Venture Studio |
| Solutions registry | Four offers: AI Company Builder, Digital Presence, Business Process Automation, Enterprise Deployment — no Venture Studio entry |

**Finding V1 (scope discrepancy):** Brief treats Venture Studio as a "core engagement pillar." Current SPEC and implementation exclude it entirely. Either (a) SPEC is authoritative and the brief is outdated, or (b) the brief requires a SPEC amendment and a new page slice. This report does **not** invent a route; it flags the conflict for CEO decision.

---

## F. Use Cases — P1 Defect (Re-confirmed Live)

### Symptom (live evidence)

Playwright navigation to `http://localhost:1441/use-cases/uc-js-bar` renders:

> **Use case not found**
> We couldn't find a use case matching "uc-js-bar". It may have moved, or the link may be out of date.

Screenshot: `C:\Users\jmlus\AppData\Local\Temp\ls-ucdetail.png`. Prior audit browser-report-2 recorded the same for all 16 slugs.

### Root cause (programmatic re-verification)

| Registry | Slugs / IDs | Consumer |
|----------|-------------|----------|
| Root `data/use-cases/registry.ts` (Vite alias target for `@lightspeed/data/use-cases`) | 13 legacy: `compliance-automation`, `agricultural-coordination`, `donor-reporting`, `data-cleaning`, `sme-operations`, `customer-service`, `market-intelligence`, `research-synthesis`, `regulatory-monitoring`, `university-research-support`, `policy-analysis`, `executive-ai-readiness`, `audit-trail-generation` | `UseCaseDetailPage.tsx:15` |
| `src/data/use-cases/registry.ts` → `src/data/registries/use-case-registry.json` | 16 current: `uc-js-bar`, `uc-meta`, `ws-01`…`ws-03`, pilots, `fow-01`…`fow-08` | `UseCasesPage.tsx` (listing) |

**Slug overlap: NONE.** Every listing-page card navigates to `/use-cases/${id}` from the src registry; the detail page resolves against the root registry and misses every time. Sitemap omits detail URLs, so SEO impact is limited; in-app navigation impact is total for detail pages.

**Related:** root `data/sectors` short ids do not match `src/data/registries/sector-registry.json` long ids — same dual-tree hazard (D6).

**Minimal fix direction (not applied):** point `UseCaseDetailPage` at the relative `src/data/use-cases` imports (same as `UseCasesPage`), or change the Vite alias to the `src/data` tree — then re-probe all 16 slugs.

---

## G. Homepage, Brand, Metrics

| Item | Evidence |
|------|----------|
| Hero H1 | "The AI-native company builder **that ships.**" — live screenshot |
| Scrim panel | "90 agents, 20 departments, five-tier human approval" |
| Chapter rail | 01–06 present |
| **D2 (hero CTA target)** | **FIXED** — `HeroSection.tsx` uses `href="#haomtgv"`; matches `HAOMTGVSection` id |
| **D4 (logo alt)** | **FIXED** — `Logo.tsx` sets `alt="LightSpeed Holdings Limited"` on first instance; repeats `alt=""` + `aria-hidden`. Static HTML spot-check: all three full pages (`public/infographics/inside-the-90-agent-company.html`, `open-source-stack.html`, `public/visuals/graduated-autonomy-ladder.html`) have `alt="LightSpeed Holdings Limited"`. Catalog/insights asset HTMLs under `public/assets/**` are text-only placeholders (no `<img>`). |
| `metrics.agentCount` | 90 (WorkforceSection) |
| `metrics.departments` | 20 (WorkforceSection) |
| `metrics.testCount` | **Stale: 17** — actual vitest suite is **41** |
| `liveTestCount` | **2586** — matches today's `pytest --collect-only` (2586/2653). Hard-coded constant, not live-measured; comment documents verification date 2026-10-13 |
| FAQ count | **28** evidence-controlled questions (SPEC requires ≥22) — PASS |
| Brand tokens | Navy/cyan/red system visible; tokens centralized per SPEC |

---

## H. Insights and Content Honesty

- 9 articles with publish dates 2026-09-24 → 2026-10-12; sitemap lists all 9 detail URLs.
- Claims registry: 24 claims, no `UNVERIFIED (DO NOT PUBLISH)` rows.
- Insights copy retains non-claims and evidence-ladder language; dual-economy article correctly separates offer language from revenue.
- Humanizer/unslop passes (#457, #460, #462) landed on marketing copy.

---

## I. Contact, Newsletter, Turnstile

| Mount point | File |
|-------------|------|
| Contact form | `ContactSection.tsx` |
| Executive briefing modal | `ExecutiveBriefingModal.tsx` |
| Newsletter (insights) | `NewsletterSignup.tsx` |

`useTurnstile.ts` pattern-checks site key (`SITE_KEY_RE`), injects Cloudflare `api.js`, and refuses malformed keys so a bad `.env` line never reaches the widget. Vite config mirrors the same regex on `VITE_TURNSTILE_SITE_KEY`.

**Finding D3 (open):** Prior audit observed Cloudflare error **400020** under `vite preview` on localhost — consistent with hostname allowlist rejecting localhost, not a missing key. **Production behaviour unverified.** Must be re-checked on the real hostname before launch.

---

## J. Security

### `vercel.json` headers (deployed plan)

| Header | Value |
|--------|--------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `SAMEORIGIN` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| CSP | **Absent** |
| HSTS | **Absent** |
| Permissions-Policy | **Absent** |

**Finding D5 (open):** Baseline hardening only. Recommend HSTS + a conservative CSP as production follow-up; re-verify with a live response dump after deploy.

### Bundle and leakage

Prior audit bundle scan (same build family): no secrets, no private keys, no dashboard keys, no internal filesystem paths. "CEO dashboard" appears once as public narrative copy only. Internal dashboard FastAPI remains on 8420/8421 and is hard-refused by the Vite port guard — not part of this SPA.

`dist/` (433 files, `index.html` present) contains no studio.html / dashboard template artifacts.

---

## K. Defect Register (current)

| ID | Sev | Defect | Status this audit |
|----|-----|--------|-------------------|
| **D1** | **P1** | All `/use-cases/<slug>` detail pages → "Use case not found" (dual registry, zero overlap) | **OPEN — live screenshot + programmatic proof** |
| **D2** | P2 | Hero CTA target wrong | **FIXED** (`#haomtgv`) |
| **D3** | P2 | Turnstile 400020 on localhost; prod unverified | **OPEN — verify on prod hostname** |
| **D4** | P3 | Logo missing alt | **FIXED** in `Logo.tsx` + static HTML |
| **D5** | P3 | No CSP / HSTS / Permissions-Policy | **OPEN** |
| **D6** | P3 | Root `data/` vs `src/data/` dual registries (structural root of D1) | **OPEN** |
| **D7** | Info | `liveTestCount` hard-coded (now 2586); `metrics.testCount` stale at 17 vs vitest 41 | Documented |
| **N1** | P2 | Live FloatingNav has 6 of SPEC 8 items (missing What We Do, Use Cases, Sectors) | **OPEN** |
| **V1** | Scope | AI Venture Studio absent from site; brief vs SPEC conflict | **OPEN — CEO decision** |
| **T1** | Info | Build CSS minify warning (`"file" is not a known CSS property`) | Benign |

---

## L. Final Readiness Assessment

### Ready for Independent Review: **YES — with conditions**

The codebase is reviewable: green lint/test/build, no secrets in the bundle, honesty-led content, intact primary routes, working theme/nav/CTA chrome, FAQ ≥22, mobile layout acceptable.

**Conditions:**

1. Reviewer must be told D1 is open (use-case details broken) or D1 must be fixed first.
2. N1 disclosed (nav is 6-item, not SPEC 8-item).
3. V1 disclosed (Venture Studio is strategy-docs only; no route).
4. D3 production Turnstile unverified.

### Ready for Production Release: **NO**

Blocking:

1. **D1** — every use-case detail page is a guaranteed miss.
2. **D3** — production Turnstile must be verified on the real hostname.
3. **N1** — SPEC eight-item nav criterion unmet on the live chrome (or SPEC must be amended by CEO).
4. **D5** — recommended hardening (HSTS/CSP) before public launch.

### Unverified / residual risk

- Live Vercel deployment headers (only `vercel.json` was read).
- Legal page full copy accuracy (routes reach 200; wording not line-audited).
- Email send path behind Turnstile (edge function not exercised).
- Visual QA against untracked brand blueprint PNGs.
- Code coverage percentage (`@vitest/coverage-v8` not installed; would require a package change).

### Recommended next engineering slice (priority order)

1. **Fix D1:** Align `UseCaseDetailPage` imports with `UseCasesPage` (relative `src/data/use-cases`); re-probe all 16 slugs until H1 is the use-case title.
2. **Fix N1:** Either mount the 8-item Header, or extend FloatingNav NAV_LINKS to match SPEC (add What We Do, Use Cases, Sectors — Contact can remain as CTA).
3. **Resolve V1:** CEO decision — keep Venture Studio out (update brief) or add route + nav + content (SPEC amendment).
4. **Verify D3** on production hostname; document result.
5. **Harden D5** (HSTS + baseline CSP) and re-dump live headers.
6. **Refresh D7:** update `metrics.testCount` to 41; keep `liveTestCount` refresh cadence documented.

---

## Evidence Package

| Artifact | Path / location |
|----------|-----------------|
| Baseline commit | `9e031b64` on `main` |
| Home desktop screenshot | `C:\Users\jmlus\AppData\Local\Temp\ls-home.png` |
| Home mobile (375×667) | `C:\Users\jmlus\AppData\Local\Temp\ls-home-mobile.png` |
| Use-case detail miss screenshot | `C:\Users\jmlus\AppData\Local\Temp\ls-ucdetail.png` |
| Prior audit (base `449a6df3`) | `docs/website/audit-2026-10-13-post-implementation.md` |
| Approved SPEC | `docs/website/SPEC.md` |
| Dual registries | `data/use-cases/registry.ts` vs `src/data/use-cases/registry.ts` |
| Vite aliases | `vite.config.ts` |
| Live nav | `src/components/FloatingNav.tsx` |
| Unused 8-item Header | `src/components/header/Header.tsx` |
| Route table | `src/App.tsx` |
| Metrics | `src/data/metrics.ts` |
| Turnstile hook | `src/hooks/useTurnstile.ts` |
| Deploy headers | `vercel.json` |
| Sitemap | `public/sitemap.xml` |
| Venture Studio strategy (not shipped) | `docs/venture-studio/` |

---

*End of report. No code was modified; no deploy was performed; no tests were weakened.*
