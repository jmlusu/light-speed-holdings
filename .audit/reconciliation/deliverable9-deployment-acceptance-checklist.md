# Deliverable 9: Deployment Acceptance Checklist

This checklist covers all routes, features, and visual elements for production readiness verification. It should be completed before any public launch.

## ✅ Routes Verification

| Route | Status | Evidence | Notes |
|---|---|---|---|
| `/` (Home) | ✅ | HomePage renders; all sections present; routing verified | Verify hero, pathways, HAOMTGV, solutions, pharos, FAQ, closing CTA all render |
| `/what-we-do` | ✅ | WhatWeDoPage renders; 6-tab catalog; G1-G4 gates; engagement path | Verify tab switching works; "View Service Catalog" → /what-we-do anchor |
| `/pharos` | ✅ | InsightsPage renders; 9 articles; categories; newsletter | Verify article cards render; Turnstile on insights (verify production) |
| `/ai-company-builder` | ✅ | AiCompanyBuilderPage renders; route exists | Verify org chart or content present; architecture SVGs may be missing (see asset checklist) |
| `/haomtgv` | ✅ | HaomtgvPage renders; 7 pillars; governance callout | Verify Reveal animations (on-scroll or on-mount per decision) |
| `/solutions` | ✅ | SolutionsPage renders; 6 domains + governance | Verify solution cards and honesty badges render |
| `/sectors` | ✅ | SectorsPage renders; sector cards | Verify sector badges and icons render; sector registry dual-tree issue noted |
| `/use-cases` | ✅ | UseCasesPage renders; 16 use case cards | **P0-01 must be fixed first:** all 16 detail pages must render titles, not "not found" |
| `/use-cases/<slug>` | ⚠️ | **P0-01 blocking:** detail pages currently render "Use case not found" | **Must fix before launch** — verify specific slug renders correct H1 |
| `/ai-assessment` | ⚠️ | Route not in App.tsx; no component found | Decision: create route or remove; verify if intentionally replaced |
| `/insights` | ✅ | InsightsPage renders; 9 featured articles; categories; newsletter; Turnstile | **P0-04 must verify:** Turnstile on localhost returns 400020; production unverified |
| `/insights/<slug>` | ✅ | InsightArticlePage renders; article content; evidence boundaries | Verify article renders; non-claims correctly labeled |
| `/about` | ✅ | AboutPage renders; AboutSection; RelatedLinks | Verify about content; tagline may or may not be on homepage |
| `/contact` | ⚠️ | ContactPage renders; ContactSection; FaqSection; Turnstile | **P0-04 must verify:** Turnstile 400020 on localhost; production unverified; form submission |
| `/legal/privacy` | ✅ | PrivacyPage renders | Verify renders; no specific content audit |
| `/legal/terms` | ✅ | TermsPage renders | Verify renders; no specific content audit |
| `/architecture` | ✅ | Redirects to `/ai-company-builder` | Document as workaround; no dedicated page |
| `/build` | ✅ | Redirects to `/what-we-do` | Document as workaround; no dedicated page |
| `offer-a` through `offer-e` | ✅ | All redirect to `/solutions` | Document as intentional; no offer detail pages |
| `/proof` | ✅ | Redirects to `/use-cases` | Verify redirection works |
| `/ask` | ✅ | Redirects to `/contact` | Verify redirection works |
| `/definitely-not-a-route` | ✅ | NotFoundPage renders | SPA catch-all 404 |

## ✅ Homepage Composition Verification

| Section | Present | Content Match | Visual Match | Behavior | Acceptance |
|---|---|---|---|---|---|
| Hero (badge, headline, 2 CTAs, logo, image) | ✅ | ✅ | ⚠️ alt text empty (P0-02); overlay hardcoded (P3-06) | CTA focus ring red vs cyan (P1-01); link color red on light (P1-02) | Fix P0-02, P1-01, P1-02; decide on overlay |
| Value pillars | ❌ | N/A | N/A | N/A | Decide P2-03: restore, add summary, or document |
| LightSpeed proposition | ✅ | ✅ | ✅ | ✅ | Maintain |
| Visitor pathways | ✅ | ✅ | ✅ | ✅ | Maintain |
| What We Build (solutions grid) | ✅ | ✅ | ✅ | ✅ | Maintain |
| HAOMTGV (7 pillars) | ✅ | ✅ | ✅ | ⚠️ Reveal on-scroll only (P2-01) | Decide P2-01: on-mount trigger or accept |
| Delivery lifecycle | ❌ | N/A | N/A | N/A | Decide P2-04: restore or document |
| Human Approval Matrix | ❌ (static refs) | ✅ (copy) | N/A | N/A | Decide P2-02: visualize or document |
| Pharos highlights (3 article cards) | ✅ | ✅ | ✅ | ⚠️ sharing missing (P2-06) | Decide P2-06: add sharing or document |
| About section | ❌ (not on homepage) | ✅ (on /about route) | N/A | N/A | Decide P2-05: add summary or document |
| FAQ (25 entries, accordion) | ✅ | ✅ | ✅ | ✅ | Maintain |
| Closing CTA (dark overlay, primary CTA) | ✅ | ✅ | ✅ | ✅ | Maintain |

## ✅ Hero Imagery Verification

| Asset | Exists | Format | Alt Text | Runtime Verification | Acceptance |
|---|---|---|---|---|---|
| Homepage hero JPEG (`/brand/digital/Homepage_Hero_High_fidelity.jpeg`) | ✅ | JPEG (not webp/avif) | ❌ Empty `alt=""` (P0-02) — **must fix** | Image renders; no broken icon | Add alt text per P0-02; decide on webp/avif (P1-04) |
| Hero webp sibling | ❌ | Declared in registry but file missing | N/A | N/A | **P1-04:** add webp/avif or update registry |
| Hero avif sibling | ❌ | Declared in registry but file missing | N/A | N/A | **P1-04:** add webp/avif or update registry |
| Production hostname Turnstile | ⚠️ | Verified on production hostname needed | N/A | **P0-04:** must verify before launch | Load production URL; confirm Turnstile renders without 400020 |

## ✅ Fonts and Logos Verification

| Asset | Exists | Theme Variants | Alt Text | Acceptance |
|---|---|---|---|---|
| 31 logo variants (`public/brand/logo/`) | ✅ | All (light/dark/mono/og/avatar/favicon) | ✅ All have alt text descriptive | Maintain; no changes needed |
| `logo-full-v2.svg` (homepage hero) | ✅ | Light background variant | ✅ `alt="LightSpeed logo"` | Maintain |
| Favicon (`public/favicon.svg`) | ✅ | Standard | ✅ Renders in browser tab | Maintain |
| OG image (`public/logo-og.svg`/`logo-og.png`) | ✅ | Social share image | ✅ Renders in meta tags | Maintain |
| Arial font family | ✅ | System font stack | ✅ Declared in `index.css` | Maintain; rendering depends on system fonts |

## ✅ Background Images Verification

| Asset | Exists | Route | Acceptance |
|---|---|---|---|
| African map `malawi-sadc-africa.svg` | ✅ | Registry: `/`, `/about`, `/sectors`, `/insights` | Verify renders on relevant routes; usage may be in decorative elements |
| African map `sector-presence.svg` | ✅ | Registry: `/sectors`, `/about` | Verify renders on relevant routes |
| Architecture SVGs (6 missing) | ❌ | Registry references but files don't exist | **P0-03:** create 6 SVGs or remove registry entries before launch if any component references them |
| Use case thumbnails | ⚠️ | `/use-cases` route | **P1-03:** standardize formats (webp/avif) before launch; current inconsistency may cause broken thumbnails on some browsers/ devices |
| Solutions grid background (`bg-ls-mist-subtle`, `bg-ls-navy/50`) | ✅ | `/solutions` route | Renders correctly per theme |
| Hero overlay (`bg-black/40`/`bg-black/60`) | ✅ | Homepage hero | **P3-06:** document as intentional or replace with design tokens; no runtime impact observed |

## ✅ Animation Behavior Verification

| Behavior | Implemented | Trigger | Reduced-Motion | Acceptance |
|---|---|---|---|---|
| Theme switching | ✅ | FloatingNav moon/sun button; localStorage persistence | ✅ No motion involved | Maintain; verify on both themes |
| Reveal animations | ⚠️ | `useInView` hook — requires scroll past element | ✅ Hook checks `prefers-reduced-motion`; disables if true | **P2-01:** decide on-mount trigger; if accepted, verify scroll-triggered works on all pages |
| Smooth scrolling | ✅ | `useSmoothScroll.ts` cubic-bezier(0.25,1,0.5,1) on hash links | ✅ Reduced-motion falls back to `scrollIntoView({behavior: 'auto'})` | Maintain |
| Scroll progress indicator | ❌ | Not present | N/A | **Decision needed:** add if prototype had; else accept |
| Back-to-top | ❌ | Not present | N/A | **Decision needed:** add if prototype had |
| FAB entrance | ❌ | Not present | N/A | **Decision needed:** add if prototype had |
| 3D icon hover | ⚠️ | Button `hover:scale-[1.02]` only (2D); no 3D transform | ✅ No motion on reduced-preference | **Decision needed:** add 3D hover if prototype had; else accept button scaling |
| Executive briefing modal | ⚠️ | Opens/closes via `onRequestBriefing`/`closeBriefing` | ⚠️ Transition unverified | **P2-07:** inspect modal; add transition if prototype had; or document |
| Mobile drawer | ⚠️ | Opens/closes via hamburger button | ⚠️ No slide transition (instant state change) | **P2-08:** add `transition-transform duration-300` for slide motion |
| Accordion chevron | ✅ | Native `<details>/<summary>` with `group-open:rotate-45` | ✅ Native `<details>` respects `prefers-reduced-motion` per browser | Maintain |
| Workflow simulator | ❌ | Not present | N/A | **Decision needed:** add if prototype had; else accept |
| Reduced-motion | ✅ | `useInView` hook + global CSS media query | ✅ Fully respected — all Reveal disabled on reduce | Maintain |

## ✅ Interactive Features Verification

| Feature | Status | Test Required | Acceptance |
|---|---|---|---|
| Dual-theme switching | ✅ | Toggle theme via FloatingNav; verify localStorage persistence; reload page | Maintain |
| Floating nav (desktop + mobile) | ✅ | Toggle viewport; verify desktop nav visible at lg+, mobile menu at handset; Escape closes menu; Tab cycles focus within panel | Maintain |
| Executive briefing modal | ⚠️ | Open from FloatingNav CTA, hero CTAs, WhatWeDoPage offers; verify open/close; verify summary state | **P2-07:** verify transition behavior |
| Scroll progress + back-to-top | ❌ | N/A | **Decision needed:** add if required |
| Five-tier approval matrix | ⚠️ | Copy references five-tier model; no visual matrix | **P2-02:** decide: visualize or document; verify no fixed agent count on homepage |
| Five-domain AI readiness assessment | ❌ | Not present | **Decision needed:** add if prototype had; else accept |
| Four-stage contact wizard | ❌ | Not present | **Decision needed:** add if prototype had; else accept |
| Cloudflare Turnstile | ⚠️ | **P0-04:** verify on production hostname; on localhost: 400020 on `/insights`; on `/contact` widget presence unreliable | **Must verify production before launch** |
| FAQ accordion | ✅ | Navigate to `/` or `/faq`; click questions; verify accordion open/close; verify chevron rotates; verify keyboard (Enter/Space activates `<summary>`) | Maintain |
| Pharos article reader | ⚠️ | Navigate to `/insights`; verify 9 article cards render with title/excerpt/read time; links to `/insights/${slug}`; **sharing buttons** | **P2-06:** decide: add sharing or document |
| Journey telemetry | ❌ | No backend `/api/journey-events`; events silently dropped | **Decision needed:** add mock/backend or disable if not required |
| Contact/enquiry API | ⚠️ | **P2-10:** submit contact form; verify success feedback; check console for errors; test on mobile | **Must test before launch** |

## ✅ Theme Switching Verification

| Check | Status | Evidence |
|---|---|---|
| Dark mode class on `document.documentElement` | ✅ | `theme === 'dark'` adds `dark` class; `localStorage.getItem('lightspeed_theme')` persists |
| Light mode visual correct | ✅ | Navy `#070A40`, Red `#E63946`/`#DC3641`, Cyan `#00BFFF` tokens render correctly |
| Theme toggle persists across reload | ✅ | `useEffect` in `App.tsx` sets `localStorage.lightspeed_theme` on every change; reload restores state |
| Reduce motion interaction | ✅ | `useInView` hook disables Reveal on `prefers-reduced-motion`; global CSS also applies |
| CTA button colors switch per theme | ✅ | Primary CTA: `bg-ls-red`/`text-ls-white` (light) or `bg-ls-red`/`text-ls-white` on dark with `shadow-ls-red/20`; secondary CTA switches similarly |

## ✅ Mobile Responsiveness Verification

| Check | Status | Routes Tested |
|---|---|---|
| Hero section on mobile (390px) | ✅ | `/` — hero `min-h-screen lg:min-h-[700px]`; full screen on mobile |
| Pathways grid on mobile | ✅ | `/` — `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`; 1→2→4 column progression |
| HAOMTGV grid on mobile | ✅ | `/haomtgv` — `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`; 1→2→3→4 progression |
| Solutions grid on mobile | ✅ | `/solutions` — `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6`; 1→2→3→6 progression |
| About section on mobile | ✅ | `/about` — `grid-cols-1 md:grid-cols-2 lg:grid-cols-4` |
| FAQ on mobile | ✅ | Native `<details>/<summary>` adapt to width; accordion items reflow |
| CTA bands on mobile | ✅ | Full width; buttons stack vertically; touch-friendly tap targets |
| Navigation on mobile | ✅ | FloatingNav hamburger opens mobile menu; menu full width; close via X or Escape |
| Form fields on `/contact` | ⚠️ | Not fully tested in this audit; verify on mobile viewport |
| Article cards on `/insights` | ✅ | `grid md:grid-cols-3 gap-5`; 1→3 column progression; responsive text scaling |

## ✅ Accessibility and Reduced Motion Verification

| Check | Status | Evidence |
|---|---|---|
| WCAG contrast (critical fixes) | ⚠️ | **P0-02:** hero alt text must be added (WCAG 1.1.1); **P1-01:** focus ring must be `ls-cyan` (WCAG 2.4.7); **P1-02:** link color `ls-navy` on light mode | Must fix P0-02 and P1-01 before launch |
| Focus ring color | ❌ | Currently `focus-visible:ring-ls-red`; must change to `focus-visible:ring-ls-cyan` (P1-01) | Fix before launch |
| Keyboard navigation | ✅ | All interactive elements tab-reachable; no `tabIndex` anomalies; Focus-visible rings present |
| Skip link | ✅ | `<a href="#main-content" className="skip-link">Skip to content</a>` present in `SiteLayout` |
| Alt text on hero | ❌ | `alt=""` — **P0-02:** must add descriptive alt (WCAG 1.1.1 critical) | Fix before launch |
| Alt text on other images | ✅ | Pathway card icons, CTA buttons, status badges all have text labels or descriptive alt |
| Reduced-motion disables animations | ✅ | `useInView` hook checks `prefers-reduced-motion`; `setInView(true)` disables Reveal | Maintain |
| No color-only information | ✅ | Badges and chips always have text labels alongside color; never rely on color alone | Maintain |
| Link purpose clear | ✅ | Link text describes destination (e.g., "Start a Conversation", "Request an AI Readiness Assessment") | Maintain |

## ✅ Console and Network Errors Verification

| Check | Status | Evidence |
|---|---|---|
| Build `npm run build` | ✅ | Exit code: 0; `dist/assets/index-BN8aXSvM.js` 496.28 kB; `index-WFtMxXoT.css` 139.91 kB; one pre-existing CSS warning |
| Lint `npm run lint` | ✅ | Exit code: 0; no lint errors |
| Test `npm run test` (vitest) | ✅ | Exit code: 0; 41 tests (companyData 17, governance 21, siteFaq 3) |
| Turnstile on production hostname | ⚠️ | **P0-04:** unverified — must load production URL (e.g., `lightspeedholdings.vercel.app`) and confirm Turnstile renders without 400020; on localhost: 400020 on `/insights` | **Must verify before launch** |
| Network errors on primary routes | ✅ | Playwright 1440×900 audits: all primary routes returned HTTP 200 with correct H1s; no console-missing-required-attribute beyond hero alt; no 404s on primary navigation |
| Hero image 404 | ⚠️ | Hero uses `/brand/digital/Homepage_Hero_High_fidelity.jpeg` which exists; if webp/avif added (P1-04), verify those files also exist at declared paths |
| SVG 404 errors (architecture) | ⚠️ | **P0-03:** 6 architecture SVGs missing; if no component references them, no runtime 404; if any component does, must fix before launch |

## ✅ Production Build and Vercel Deployment Readiness

| Check | Status | Command | Evidence |
|---|---|---|---|
| Production build succeeds | ✅ | `npm run build` | Exit code: 0; dist files generated |
| Production preview `vite preview` | ✅ | `npm run preview` (port 1440) | Port guard allows 1440; primary routes render 200 with correct H1s |
| No secrets in bundle | ✅ | Bundle secret scan (`index-BN8aXSvM.js`, 495,200 bytes): null for turnstileSecret, apiKeyLike, privateKey, dashboardKey, internalHost, athena | Confirmed clean |
| CSP/HSTS/Permissions-Policy | ⚠️ | `vercel.json` has: `nosniff`, `SAMEORIGIN`, `referrer-policy` only; no CSP, HSTS, Permissions-Policy | **Recommended (D5 previous audit):** add HSTS and baseline CSP for production; not blocking for launch per current scope |
| Vercel deployment | ⚠️ | Outside this audit scope; `vite.config.ts` hard-refuses ports 8420/8421 (dashboard ports); canonical preview port 1440 | **Verdict:** Codebase healthy for staging use; not production-complete until D1 (use-case detail fix) and D3 (Turnstile production) are resolved |
| Bundle size within limits | ✅ | 496.28 kB JS + 139.91 kB CSS | Acceptable for marketing site |
| No console errors on route load | ✅ | Primary routes load without JS errors in Playwright audits | Maintain |

## 🎯 Final Launch Readiness Assessment

### Must Fix Before Launch (P0 + P1 critical)

- [ ] **P0-01:** Use case detail pages fix — all 16 `/use-cases/<slug>` render correct H1, not "Use case not found"
- [ ] **P0-02:** Hero image alt text — add descriptive alt; WCAG 1.1.1 compliance
- [ ] **P0-03:** 6 architecture SVG files — create at declared paths or remove registry entries
- [ ] **P0-04:** Turnstile production verification — load production hostname; confirm no 400020 errors
- [ ] **P1-01:** Focus ring color — change `focus-visible:ring-ls-red` to `focus-visible:ring-ls-cyan` on CTA buttons
- [ ] **P1-02:** Link color on light mode — change `text-ls-red` to `text-ls-navy` per design system §155

### Should Fix Before Launch (P1 visual/functional)

- [ ] **P1-03:** Use case thumbnail format standardization — ensure all 12 cards support webp and avif
- [ ] **P1-04:** Hero format alignment — add webp/avif files at `public/assets/hero/` or update registry to match JPEG usage

### Should Fix (P2 — product decisions)

- [ ] **P2-01:** Reveal on-mount trigger decision — restore entrance animations or accept scroll-triggered-only
- [ ] **P2-02:** Human Approval Matrix visualization — create interactive matrix or document as intentional
- [ ] **P2-03:** Value pillars on homepage — add standalone section, footer summary, or document as intentional
- [ ] **P2-04:** Delivery lifecycle section — restore or document as intentional omission
- [ ] **P2-05:** About section on homepage — add tagline/summary or document as IA decision
- [ ] **P2-06:** Pharos sharing UI — add sharing buttons or document as not required
- [ ] **P2-07:** Executive briefing modal transition — inspect and add transition if prototype had; or document
- [ ] **P2-08:** Mobile drawer slide transition — add `transition-transform duration-300` to FloatingNav mobile menu
- [ ] **P2-09:** Five-tier approval matrix visual — create visualization or document per Calm Intelligence brand (no fixed agent count)
- [ ] **P2-10:** Contact API behavior — test form submission; verify success feedback; no console errors

### Acceptable as-Is (P3 — minor differences or documented)

- [ ] **P3-01 through P3-10:** All P3 items resolved per acceptance criteria (monitoring, documentation, or minor adjustments)

### Final Verification Checklist (run before launch)

- [ ] `npm run build` — exit code 0
- [ ] `npm run lint` — exit code 0
- [ ] `npm run test` (vitest) — exit code 0, all 41 tests pass
- [ ] Primary routes (/, /what-we-do, /pharos, /ai-company-builder, /haomtgv, /solutions, /sectors, /about, /contact, /legal/privacy, /legal/terms) — all return HTTP 200 with correct H1
- [ ] Homepage: all 13 sections present or documented as intentional; hero alt text non-empty; focus ring cyan; links navy on light
- [ ] No new console errors introduced by changes
- [ ] Turnstile verified on production hostname (no 400020)
- [ ] Mobile responsiveness verified on primary routes (390×844 and 1440×900 viewports)
- [ ] Accessibility audit: no WCAG 1.1.1 or 2.4.7 violations remaining

---

**Deplyoment Readiness Signal:**

**LAUNCH READY** — if all "Must Fix Before Launch" items are complete and final verification checklist passes.

**LAUNCH DEFERRED** — if any "Must Fix Before Launch" items remain incomplete, or if P0-04 (Turnstile production) cannot be verified.

**PRODUCTION DEFERRED** — if critical navigation (P0-01) or compliance (P0-02, P1-01, P1-02) blockers are present.

*This checklist must be completed before any public launch. No source code modifications were made during this read-only audit; all items identified for fix require implementation in a subsequent phase.*
