# LightSpeed External Web App — Post-Implementation Audit

**Auditor role:** Independent pre-handover verification (no code changes, no redesign)
**Date:** 2026-10-13
**Verdict:** **Ready with Conditions** — see §16. Do not treat as production-ready until P1 is fixed.

---

## 1. Executive Summary

The external Vite/React site (repo-root `src/`, not `src/ai_company/`) builds, lints, and tests green on `main` at `449a6df3`. Primary routes render correct H1s, the homepage H-A-O-M-T-G-V chapter structure is intact, no secrets appear in the production bundle, and Insights articles are published with honest evidence boundaries.

One **P1 functional defect** blocks full readiness: every use-case **detail** route (`/use-cases/<slug>`) renders "Use case not found" because a Vite alias sends `@lightspeed/data/use-cases` to a second, stale registry under repo-root `data/`. Home and index cards link with slugs from `src/data/registries/use-case-registry.json`; the detail page resolves against the wrong list.

One **P2 UX defect**: the hero "scroll to chapter 01" link targets `#operating-model`, but the actual section id is `haomtgv`.

Turnstile (Cloudflare) returns error **400020** on `/insights` under `vite preview` on localhost. A site key is present in `.env` and hostname-restricted; this is treated as a local-environment limitation, not a missing-key defect, but production behaviour is **unverified**.

Security headers on Vercel are minimal (nosniff / SAMEORIGIN / referrer-policy only) — no CSP, HSTS, or Permissions-Policy. Bundle secret scan found no API keys, private keys, or dashboard keys.

---

## 2. Scope and Method

| In scope | Out of scope |
|----------|----------------|
| Repo inspection of `main` @ `449a6df3` | Redesign, layout changes, new features |
| `npm run lint`, `npm run test`, `npm run build` | Deploying or pushing to origin |
| `vite preview` on port **1440** (canonical preview port) | Claiming production CDN/header behaviour beyond `vercel.json` |
| Playwright scripted audits of 13 primary + 16 use-case + 9 insight routes | Python pytest suite execution (file count only) |
| Bundle secret/leakage text scan of built JS | |
| Static source verification of claims, registries, Turnstile wiring | |

**Artifacts (gitignored `.tmp/`):**

- `.tmp/audit-browser.cjs`, `.tmp/browser-report.json`, `.tmp/shots/`
- `.tmp/audit-browser-2.cjs`, `.tmp/browser-report-2.json`, `.tmp/shots2/`

**Application boundary respected:** Vite/React app uses 1440 (preview) / 1441 (dev). CEO Dashboard ports 8420/8421 were not bound. `vite.config.ts` hard-refuses 8420/8421.

---

## 3. Baseline

| Item | Value |
|------|--------|
| Branch | `main` (tracks `origin/main`) |
| HEAD | `449a6df3` — `content(unslop): remove em-dashes and AI vocabulary from marketing site copy (#457)` |
| Commit time | 2026-10-13 11:21:24 +0200 |
| Tracked working tree | Clean |
| Untracked files present | Planning decks, brand PNGs, bug-fix notes, `validate-company-name.py`, etc. — not part of the audited build |
| Package | `lightspeed-holdings` v1.0.0 |
| ECL active change | None (`harness/changes/active/` contains only `.gitkeep`) |
| Recent site commits | `d652e335` (#451 HAOMTGV homepage), `90654ac9` (#455 SHA-256 phrasing), `449a6df3` (#457 unslop) |

---

## 4. Verification Commands

| Command | Result | Evidence |
|---------|--------|----------|
| `npm run lint` | **PASS** | tsc clean (script is `tsc --noEmit`) |
| `npm run test` | **PASS** — 41 tests | companyData 17, governance 21, siteFaq 3; vitest |
| `npm run build` | **PASS** (~13.5s) | `dist/assets/index-BN8aXSvM.js` 496.28 kB; `index-WFtMxXoT.css` 139.91 kB; one pre-existing CSS warning |
| `npm run preview` (port 1440) | Running for browser audits | Port guard allows 1440 |
| Recursive root greps | Timeouts | Used targeted `Select-String` / `node -e` instead |

---

## 5. Routing and Navigation

Primary routes (Playwright, 1440×900): all returned HTTP **200** with correct H1s:

| Route | H1 |
|-------|-----|
| `/` | The AI-native company builder that ships. |
| `/use-cases` | What Can LightSpeed Actually Do? |
| `/sectors` | Sectors We Serve — With the Evidence to Back It |
| `/insights` | Evidence, Research & the Agentic AI Canon |
| `/about` | About LightSpeed |
| `/contact` | Tell Us Where You Are |
| `/solutions` | Solutions Built for the Work to Be Done |
| `/ai-company-builder` | Build Governed AI Companies |
| `/what-we-do` | Enterprise AI Systems Built for Real Constraints |
| `/proof` → `/use-cases` | Redirect works |
| `/ask` → `/contact` | Redirect works |
| `/definitely-not-a-route` | Page not found (SPA catch-all) |

Homepage section ids present and non-empty: `hero`, `paths`, `haomtgv`, `solutions`, `ai-company-builder`, `workforce`, `use-cases`, `insights`, `about`, `faq`, `briefing`. Fixed nav present. Zero negative-z visible elements. Skip-link `#main-content` present.

---

## 6. Homepage / Hero

- `src/components/HeroSection.tsx` uses `homeImmersiveCopy` + `liveTestCount` from `src/data/metrics.ts`.
- Claim grid: 90 agent configurations, `{liveTestCount}` regression tests, 20 departments, 100% auditable.
- H-A-O-M-T-G-V section id is `haomtgv` (`HAOMTGVSection.tsx:80`).
- **Defect (P2):** `HeroSection.tsx:155` is `href="#operating-model"`. No element has `id="operating-model"`. Only other text match is a comment in `src/data/capabilities.ts:2`. ChapterRail correctly links `#${chapter.id}` → `#haomtgv`.
- Right-hand ScrimPanel copy markets the five-tier approval / auditable decision story — intentional product language, not internal leakage.

---

## 7. Use Cases — P1 Defect (Confirmed Root Cause)

### Symptom

All 16 detail routes tested (`uc-js-bar`, `uc-meta`, `ws-01`…`ws-03`, pilots, `fow-01`…`fow-08`) render **HTTP 200** with H1 **"Use case not found"**. Example: `.tmp/browser-report-2.json` → `useCases[0] = { slug: "uc-js-bar", h1: "Use case not found", notFound: true }`. `/use-cases/ai-company-builder` (legacy slug from root registry) also 404s on the detail page in run 1.

### Cause

Two registries exist; Vite picks the wrong one at bundle time:

| Specifier | `tsconfig` paths | `vite.config.ts` resolve.alias | Entries |
|-----------|------------------|--------------------------------|---------|
| `@lightspeed/data/use-cases` | `src/data/use-cases/*` | **`data/use-cases/registry.ts` (repo root)** | 13 legacy slugs (`compliance-automation`, `agricultural-coordination`, …) |
| relative `../data/use-cases/registry` | — | n/a | 16 current slugs (`uc-js-bar`, …) from `src/data/registries/use-case-registry.json` |

- Index/home import the **relative** path and link `/use-cases/${uc.id}` (`UseCasesSection.tsx:9,54`; `UseCasesPage.tsx:23,318`).
- Detail page imports the **alias** (`src/pages/UseCaseDetailPage.tsx:15–18`) → root `data/use-cases/registry.ts` (different ids, `sector: string[]` with short ids like `fintech`).
- Result: every card link is a guaranteed miss.

**Related:** root `data/sectors` short ids (`healthcare`, `research`, …) do not match `src/data/registries/sector-registry.json` long ids (`healthcare-public-health`, `research-universities`, …). Even after slugs align, sector badge lookup via the alias would still fall back.

**Minimal fix direction (not applied in this audit):** point `UseCaseDetailPage` at the relative `src/data/use-cases` imports (same as `UseCasesPage`), or change the Vite alias to the `src/data` tree — then re-verify all 16 slugs.

---

## 8. Sectors

- `/sectors` H1 and layout OK; no horizontal overflow at 1440 and 390.
- `src` sector ids (10): `financial-services`, `healthcare-public-health`, `agriculture-agritech`, `education-academia`, `government-public-sector`, `regulators-standards-institutions`, `research-universities`, `smes-private-enterprise`, `development-nonprofit-organizations`, `technology-digital-businesses`.
- Rendered sector anchors captured in browser-report-2 (`other.sectorAnchors`).
- Cross-registry id skew documented in §7 — do not consume root `data/sectors` from site UI without remapping.

---

## 9. Insights / Pharos

- Index H1 correct; **9 articles** render with 639–1587 words each (run 2).
- Slugs and publish dates (from `src/data/insights.ts`):

| Slug | publishedAt |
|------|-------------|
| `open-source-cost-architecture` | 2026-10-12 |
| `dual-economy-ai-pricing` | 2026-10-12 |
| `five-tier-approval-matrix` | 2026-10-12 |
| `inside-a-90-agent-company` | 2026-10-12 |
| `offline-first-ai-for-africa` | 2026-10-12 |
| `evidence-ladder-honest-claims` | 2026-10-12 |
| `sadc-ai-opportunity` | 2026-09-30 |
| `agentic-ai-african-governments` | 2026-09-27 |
| `digital-to-ai-native-transformation` | 2026-09-24 |

- Content includes explicit non-claims (no fabricated TAM/savings/revenue); SADC framework described as own proposal, not adopted standard. Alignment with evidence ladder is **positive**.
- Each article page recorded a 400 from `challenges.cloudflare.com` (see §10) — body content still rendered fully.

---

## 10. Contact, Newsletter, Turnstile

**Wiring:** `src/hooks/useTurnstile.ts` injects Cloudflare `api.js`; site key from `__TURNSTILE_SITE_KEY__` (vite define, pattern-checked). Mount points:

- `ContactSection.tsx` (contact page)
- `ExecutiveBriefingModal.tsx`
- `NewsletterSignup.tsx` (insights index — `InsightsPage.tsx:152`)

**Local evidence:**

- `.env` contains `VITE_TURNSTILE_SITE_KEY=4AAAAA***` (redacted), `TURNSTILE_SECRET_KEY`, `TURNSTILE_HOSTNAMES=jmlusu***`.
- Built with that env present (`.env` mtime 2026-10-12; `dist` 2026-10-13).
- `/insights`: pageerror `Uncaught TurnstileError: [Cloudflare Turnstile] Error: 400020` + resource 400 from challenges.cloudflare.com.
- `/contact`: no Turnstile pageerror in run 2; widget presence not reliably counted (siteKey gate at `ContactSection.tsx:404`).
- Newsletter submit disabled when `siteKey && !turnstileToken` (`NewsletterSignup.tsx:185`).

**Assessment:** 400020 is consistent with hostname allowlist rejecting `localhost:1440`, not with a missing/empty key (empty key would skip render entirely). **Production Turnstile behaviour is unverified** — must be re-checked on the real hostname before launch.

---

## 11. Legal Pages

- `/legal/privacy` and `/legal/terms` returned 200 in run 2.
- Full legal copy not line-audited beyond route reachability and H1 presence; treat wording as **not independently reviewed**.

---

## 12. Content, Claims, Metrics

**Claims registry** (`src/data/registries/claims-registry.json`): 24 claims. Classifications observed: `PROVEN_IN_HOUSE` 14, `PILOT` 3, `VERIFIED` 2, `DEMONSTRATION` 2, `FIELDABLE` 1, `LIVE` 1, `HISTORICAL` 1. No `UNVERIFIED (DO NOT PUBLISH)` rows in the current count.

**Hero test count:** `src/data/metrics.ts` exports `liveTestCount = 2566` as a **hard-coded constant**, with comment that it was verified after a strip step. `legacyPytestCount = 2557` is separate. Frontend vitest suite is **41 tests**, not 2566. Repo contains **192** `test_*.py` files under `tests/` (count only; suite not executed). The 2,566 figure is therefore a **frozen marketing constant referring to the Python platform suite**, not a live measurement from this audit. Public copy presents it as "Passing" without a timestamp caveat.

**Company / FAQ / capabilities** covered by green unit tests (`companyData.test.ts`, `siteFaq.test.tsx`, `governance.test.ts`).

**Insights honesty text** (e.g. dual-economy pricing article) correctly labels offer language vs revenue — consistent with AGENTS.md evidence policy.

---

## 13. Security and Leakage

### Response headers (local `vite preview`)

Observed: `content-type`, `content-encoding`, `cache-control: no-cache`, `etag`, `vary: Origin`. Local preview does **not** apply Vercel headers.

### `vercel.json` (deployed header plan)

| Header | Value |
|--------|--------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `SAMEORIGIN` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| CSP | **Absent** |
| HSTS | **Absent** |
| Permissions-Policy | **Absent** |

### Bundle scan (`index-BN8aXSvM.js`, 495,200 bytes)

| Pattern class | Result |
|---------------|--------|
| turnstileSecret / apiKeyLike / privateKey / dashboardKey / internalHost / athena | **null** |
| "CEO dashboard" | Found once — inside public narrative copy for the inside-a-90-agent-company insight ("story arc … to a CEO dashboard"), not a URL or credential |

### Rendered-text leakage (home + key pages)

| Term | Pages | Assessment |
|------|-------|------------|
| "approval gate" / "Approval Gate" | `/`, `/insights`, `/solutions`, `/what-we-do` | Intentional five-tier governance product language |
| "inbox.json" / "company-registry" | Absent | Clean |
| Internal filesystem paths | Absent from scanned renders | Clean |

**Conclusion:** No credential or internal-path leak in the built SPA. Narrative references to internal concepts are branded product copy. Header hardening (CSP/HSTS) remains a production follow-up on Vercel, not in local preview.

---

## 14. Accessibility, Responsive, Motion

| Check | Result |
|-------|--------|
| Horizontal overflow 1440×900 | 0 on all primary routes |
| Horizontal overflow 390×844 | 0 |
| Fixed nav | Present, non-shifting |
| Heading order | H1 correct; H2/H3/H4 hierarchy present (`browser-report-2.json` → `other.headingOrder`) |
| `imgMissingAlt` | 1: `http://localhost:1440/logo-full-v2.svg` |
| Reduced-motion audit | Initial "invisible elements" (6) were **false positives** (ChapterRail hover pills: `aria-hidden`, `opacity-0`, `pointer-events-none`) — retracted |
| Theme toggle | Works |
| Skip link | Present |

---

## 15. Defect Register

| ID | Sev | Defect | Evidence | Status |
|----|-----|--------|----------|--------|
| **D1** | **P1** | All 16 `/use-cases/<slug>` detail pages show "Use case not found" | Dual registry + `vite.config.ts` alias; `UseCaseDetailPage.tsx:15`; browser-report-2 | **Open — must fix before launch** |
| **D2** | P2 | Hero link `#operating-model` has no target (id is `haomtgv`) | `HeroSection.tsx:155`; `HAOMTGVSection.tsx:80` | **Open** |
| **D3** | P2 | Turnstile 400020 on `/insights` under localhost preview | Browser-report-2 pageerror; hostname allowlist | **Open — verify on prod hostname** |
| **D4** | P3 | `logo-full-v2.svg` missing alt text | browser-report-2 imgMissingAlt | Open |
| **D5** | P3 | No CSP / HSTS / Permissions-Policy in `vercel.json` | vercel.json headers array | Open |
| **D6** | P3 | Root `data/` vs `src/data/` registry divergence (sectors, solutions, use-cases) | Alias + dual file trees | Open (root cause of D1; track as structural) |
| **D7** | Info | `liveTestCount = 2566` is hard-coded, not live-measured; frontend suite is 41 tests | `metrics.ts`; package.json scripts | Documented; optional honesty footnote on hero |

False leads closed: reduced-motion "invisibility", empty Turnstile key, Athena/dashboard port misuse, secret leakage, broken primary nav, SPA 404 catch-all.

---

## 16. Verdict and Conditions

### Verdict: **Ready with Conditions**

The codebase is healthy for independent review and staging use: lint/test/build green, no secrets in the bundle, primary IA and Pharos insights intact, honesty-led content. It is **not** Ready for Independent Review as "production-complete" until D1 is fixed and production Turnstile is verified.

### Conditions before "Ready for Independent Review" / public launch

1. **D1 (blocking):** Fix use-case detail data source so all 16 registry slugs resolve; re-run the 16-route Playwright probe; confirm H1 is the use-case title, not "Use case not found".
2. **D2:** Change hero href to `#haomtgv` (or rename the section id) and click-verify.
3. **D3:** Load `/insights` and `/contact` on the production hostname; confirm Turnstile renders and 400020 does not occur; confirm submit gating matches design.
4. **D4:** Add `alt` to `logo-full-v2.svg`.
5. **D5 (recommended):** Add HSTS (and a baseline CSP) to production headers; re-verify with a live response dump.

### Unverified / residual risk

- Production Vercel deployment state and real response headers (only `vercel.json` was read).
- Python pytest total (192 files counted; suite not run) — 2,566 claim not re-derived here.
- Legal page full copy accuracy.
- Visual QA against the untracked blueprint `brand/digital/LightSpeed Homepage Structure Blueprint.png` (present on disk, not formally diffed).
- Email send path behind Turnstile (server/edge function not exercised).

### Recommended next engineering slice

Small PR on a branch (main is protected): retarget `UseCaseDetailPage` imports + hero anchor + alt text; add a vitest or Playwright smoke that fails if detail page H1 equals "Use case not found"; then re-audit D1–D4 only.
