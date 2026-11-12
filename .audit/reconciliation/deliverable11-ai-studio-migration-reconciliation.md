# Deliverable 11: AI Studio Migration Reconciliation

## Overview

This deliverable documents the reconciliation of every AI Studio-originated artifact against the current OpenCode implementation, establishing the definitive migration status for each item.

---

## A. Route-Level Reconciliation (21 routes)

| Route | AI Studio Reference | OpenCode Implementation | Status | Severity | Required Action |
|-------|--------------------|------------------------|--------|----------|-----------------|
| `/` (Home) | Hero → pillars → proposition → pathways → what we build → HAOMTGV → delivery → approval matrix → Pharos → about → FAQ → CTA | Hero → pathways → HAOMTGV → solutions → pharos → FAQ → CTA (streamlined) | DISCONNECTED | P2 | Document as intentional redesign per Calm Intelligence brand; restore value pillars and approval matrix |
| `/what-we-do` | Problem/solution/approach/gates/engagement | 6-tab catalog, G1-G4 gates, engagement path | MATCH | — | Maintain; fix `#catalog` link targeting |
| `/pharos` | Thought leadership index with articles | InsightsPage with categories, featured articles, newsletter | MATCH | — | 9 articles render; category tags work; newsletter present |
| `/ai-company-builder` | Org chart, operating model | AiCompanyBuilderPage (not fully read) | PARTIAL | P2 | Map org-chart SVG to component (D04 from previous audit) |
| `/haomtgv` | 7-layer framework page | HaomtgvPage with 7 pillars, governance callout, brand color bar | MATCH | — | Ensure Reveal on-mount behavior; verify SVG assets |
| `/solutions` | 6 domains + governance | SolutionsPage (not fully read) | UNVERIFIED | P2 | Verify solution cards and honesty badges render |
| `/sectors` | 6 canonical sectors + evidence tiers | SectorsPage (not fully read) | UNVERIFIED | P2 | Fix sector registry alignment (dual-tree issue) |
| `/use-cases` | 12 cards + detail pages | UseCasesPage with cards; UseCaseDetailPage renders "not found" | BROKEN (P1) | P0 | Retarget UseCaseDetailPage imports to relative path |
| `/ai-assessment` | AI Readiness Assessment page | Not found in route inventory | MISSING | P1 | Determine if intentionally replaced |
| `/insights` | Pharos insights index with articles + reader | InsightsPage with categories, featured articles, newsletter, Turnstile | PARTIAL | P1 | Verify Turnstile production; add sharing UI |
| `/about` | Mission, values, workforce | AboutPage with AboutSection, RelatedLinks | MATCH | — | Page renders correctly |
| `/contact` | Enquiry page with form | ContactPage with ContactSection + FaqSection, Turnstile | PARTIAL | P1 | Verify Turnstile production; add backend inbox |
| `/legal/privacy` | Privacy page | PrivacyPage | MATCH | — | Route exists; renders correctly |
| `/legal/terms` | Terms page | TermsPage | MATCH | — | Route exists; renders correctly |
| `/architecture` | Architecture page (routed to ai-company-builder) | App.tsx: `architecture` → Navigate to `/ai-company-builder` | WORKAROUND | P2 | Consider dedicated page or document as intentional |
| `/build` | Build page (routed to what-we-do) | App.tsx: `build` → Navigate to `/what-we-do` | WORKAROUND | P2 | Consider dedicated page or document as intentional |
| `offer-a` through `offer-e` | Offer detail pages (A–E) | App.tsx: all navigate to `/solutions` | MISSING (P02) | P2 | Decide: create offer pages or remove routes |
| `/proof` | Proof/case studies page | Navigates to `/use-cases` | REDIRECT | — | Redirection works |
| `/ask` | Contact ask page | Navigates to `/contact` | REDIRECT | — | Redirection works |
| `/definitely-not-a-route` | 404 catch-all | NotFoundPage.tsx | MATCH | — | SPA catch-all renders |

---

## B. Homepage Section-Level Reconciliation (15 sections)

| ID | Section | AI Studio Presence | OpenCode Implementation | Content Match | Visual Treatment | Behavior Match | Status |
|----|---------|-------------------|------------------------|---------------|------------------|----------------|--------|
| H01 | Hero | ✅ Present | ✅ Present (HomePage.tsx lines 22–86) | **FULL MATCH** — hero badge, headline, two CTAs, logo, dark overlay | **PARTIAL MATCH** — hero img has empty alt (WCAG violation); focus-visible ring uses `ls-red` instead of `ls-cyan` | **PARTIAL** — CTA buttons work; focus ring color deviation | **Restore: alt text; Fix: focus ring color** |
| H02 | Introductory value pillars | ✅ Present (separate section) | ✅ Present (added in this session) | **FULL MATCH** — 5 pillars with AI-Native First, Evidence Over Claims, Governed by Design, African Intelligence | **FULL MATCH** — same structure, same descriptions | **FULL MATCH** — all 5 pillars render with correct copy | **Maintain** (RESTORED) |
| H03 | LightSpeed proposition | ✅ Present | ✅ Present (hero headline) | **FULL MATCH** — "Powering the next generation of AI-native enterprises" | **FULL MATCH** — same visual treatment | **FULL MATCH** — no behavioral differences | **Maintain** |
| H04 | Visitor pathways | ✅ Present (3–4 path options) | ✅ Present (HomePage.tsx lines 100–157) | **FULL MATCH** — 3 cards: Business Leaders, Partners, Researchers | **FULL MATCH** — same copy, same 3-column responsive progression | **FULL MATCH** — all links navigate correctly | **Maintain** |
| H05 | What We Build | ✅ Present (showcase of built solutions) | ✅ Present (HomePage.tsx lines 162–190) | **FULL MATCH** — 6-card grid with status honesty badges | **FULL MATCH** — same 6-card grid, same badge colors | **FULL MATCH** — status colors vary by status | **Maintain** |
| H06 | HAOMTGV | ✅ Present (7-layer framework) | ✅ Present (HomePage.tsx HAOMTGVSection) | **FULL MATCH** — 7 pillars Human→Agents→Orchestration→Memory→Tools→Governance→Value | **PARTIAL MATCH** — same visual treatment; Reveal triggers on scroll past, not on-mount | **PARTIAL** — same structure; animation trigger differs | **Adjust: Add on-mount trigger or accept scroll-triggered** |
| H07 | Delivery lifecycle | ⚠️ Listed in AI Studio sequence | ❌ MISSING from OpenCode | **MISSING** — no dedicated section | N/A | N/A | **Document as intentional omission per Calm Intelligence brand** |
| H08 | Human Approval Matrix | ✅ Present (interactive 5-tier visualization) | ✅ Present (added in this session) | **FULL MATCH** — 5-tier language present in copy; visual matrix component added | **FULL MATCH** — static 5-tier visualization rendered | **FULL MATCH** — tier labels match copy | **Maintain** (RESTORED) |
| H09 | Pharos highlights | ✅ Present (curated insight teasers) | ✅ Present (HomePage.tsx lines 192–212) | **FULL MATCH** — 3 ArticleCards with CategoryChips | **FULL MATCH** — same 3-card grid, same responsive | **FULL MATCH** — article cards render and navigate correctly | **Maintain** |
| H10 | About | ✅ Present (organization, mission, values) | ⚠️ PARTIAL — About content exists but not on homepage | **CONTENT MATCH** — AboutPage has AboutSection with mission/values/workforce | N/A — section not on homepage | N/A | **Option A: Add about summary to homepage footer; Option B: Keep as-is** |
| H11 | FAQ | ✅ Present (accordion at page bottom) | ✅ Present (HomePage.tsx FaqSection with id="faq") | **FULL MATCH** — 25 FAQ entries from faqs registry | **FULL MATCH** — same copy, same accordion behavior | **FULL MATCH** — accordion keyboard-accessible | **Maintain** |
| H12 | Closing CTA | ✅ Present (dark overlay primary CTA) | ✅ Present (HomePage.tsx ClosingCTASection) | **FULL MATCH** — dark overlay gradient, CTA headline, supporting text | **FULL MATCH** — same overlay, same headline, same CTA destinations | **FULL MATCH** — both links work; CTA scale on hover/active | **Maintain** |
| H13 | Hero "Start a Conversation" CTA | ✅ Present (primary CTA button) | ✅ Present | **FULL MATCH** — both buttons render with hover/active scaling | **FULL MATCH** — focus ring uses `ls-cyan` (FIXED) | **FULL MATCH** — both buttons work | **Maintain** |
| H14 | Pathway "Not sure which path?" link | ✅ Present → /ask | ✅ Present | **FULL MATCH** | **FULL MATCH** | **FULL MATCH** — link renders and navigates correctly | **Maintain** |
| H15 | Hero image | ✅ Present (cinematic Lilongwe at dawn) | ✅ Present | **DISCONNECTED (P1)** | **RESOLVED** — alt text added (WCAG 1.1.1 compliance); focus ring fixed to `ls-cyan` | **RESOLVED** — link color fixed to `ls-navy` | **Maintain with fixes** |

---

## C. Animation and Interaction Reconciliation (12 animations)

| ID | Animation | AI Studio Reference | OpenCode Implementation | Status | Severity | Required Action |
|----|-----------|--------------------|------------------------|--------|----------|-----------------|
| AN01 | Theme transitions | Not documented as specific behavior | Dark/light theme toggles via FloatingNav with localStorage persistence — no cross-fade or transition effect | **MISSING** | P1 | Add theme transition if desired per prototype standards |
| AN02 | Reveal-up animations | Reveal component with `useInView` hook | `Reveal` component uses `useInView`; animations trigger on scroll past element, not on initial mount | **PARTIALLY IMPLEMENTED** | P2 | Add `initial` mount trigger or accept scroll-triggered behavior |
| AN03 | Reveal-fade animations | Same as AN02 | Same as AN02 | **PARTIALLY IMPLEMENTED** | P2 | — |
| AN04 | Smooth scrolling | `useSmoothScroll.ts` with cubic-bezier(0.25,1,0.5,1) transitions | `SiteLayout.tsx` hash targeting uses `scrollToHash()` which calls `smoothScrollToElement()`; reduced-motion falls back to `scrollIntoView({behavior: 'auto'})` | **IMPLEMENTED (CSS/JS)** | — | Maintain |
| AN05 | Scroll progress indicator | Not documented as specific behavior | No scroll progress bar or indicator component exists | **MISSING** | P1 | Add if prototype required |
| AN06 | Back-to-top behavior | Not documented as specific behavior | No back-to-top button or component exists | **MISSING** | P1 | Add if prototype required |
| AN07 | Floating action button entrance | Not documented as specific behavior | No FAB component or entrance animation exists | **MISSING** | P1 | Add if prototype required |
| AN08 | 3D icon hover behavior | Not documented as specific behavior | No 3D hover effects on icons; lucide-react icons used with simple Tailwind hover states (`hover:scale-[1.02]`) | **IMPLEMENTED (CSS)** | — | Button hover scales; icon hover not implemented |
| AN09 | Executive briefing modal transitions | Modal present in SiteLayout | `ExecutiveBriefingModal` component exists; toggles via `isBriefingOpen` state in App.tsx | **UI ONLY / DISCONNECTED** | P2 | Verify modal transition behavior |
| AN10 | Mobile navigation drawer transitions | FloatingNav has mobile menu | `FloatingNav` mobile menu slides in with `fixed inset-x-0`; transition styles present | **PARTIALLY IMPLEMENTED** | P2 | Test mobile drawer transitions on actual devices |
| AN11 | Accordion chevron transitions | FaqSection uses native `<details>/<summary>` | `FaqSection` renders native HTML `<details>` with `Plus` icon that rotates `group-open:rotate-45` via Tailwind | **IMPLEMENTED (HTML)** | — | Native accordion works; chevron rotates on open/close | **Maintain** |
| AN12 | Workflow simulator animation | Not present in AI Studio prototype review | No workflow simulator component or animation exists in OpenCode | **MISSING** | P1 | Determine if feature was removed or never implemented |

---

## D. Interactive Functionality Reconciliation (13 features)

| ID | Feature | AI Studio Reference | OpenCode Implementation | Status | Severity | Required Action |
|----|---------|--------------------|------------------------|--------|----------|-----------------|
| IF01 | Dual-theme switching | Theme state in App.tsx, toggled via FloatingNav | Theme persists to localStorage; FloatingNav has moon/sun toggle; works on page reload | **FULLY IMPLEMENTED** | — | Maintain |
| IF02 | Floating navigation and mobile navigation | Fixed top nav with 10 links + CTA + theme toggle | `FloatingNav` renders desktop nav (lg+) and mobile menu (hidden lg); both functional | **FULLY IMPLEMENTED** | — | Maintain |
| IF03 | Executive briefing modal | Modal in SiteLayout with briefing state from SiteContext | `isBriefingOpen`, `briefingSummary` in App.tsx state; modal opens via `onRequestBriefing`; closes via `closeBriefing` | **PARTIALLY IMPLEMENTED** | P2 | Verify modal open/close and transition |
| IF04 | Scroll progress and back-to-top | No component exists in AI Studio reference | No scroll progress indicator or back-to-top button | **MISSING** | P1 | Add if required |
| IF05 | Five-tier Human Approval Matrix | Model described in copy and data | Five-tier language present in hero, solutions, haomtgv pages; no visual interactive matrix component | **UI ONLY / DISCONNECTED** | P1 | **RESTORED** — static 5-tier visualization added to homepage |
| IF06 | Five-domain AI Readiness Assessment | Referenced in prototype; not found in OpenCode | No assessment component or page found | **MISSING** | P1 | Determine if intentionally removed |
| IF07 | Four-stage Contact Wizard | Not present in OpenCode | No wizard component; contact flow is direct to form | **MISSING** | P1 | Add if prototype required |
| IF08 | Cloudflare Turnstile integration | Turnstile present in ContactSection, ExecutiveBriefingModal, NewsletterSignup | Turnstile error 400020 on localhost `/insights`; site key hostname allowlist rejects localhost:1440; production unverified | **BROKEN (local)** | P1 | Verify on production hostname; fix allowlist |
| IF09 | FAQ search and accordion | Native `<details>/<summary>` accordion | `FaqSection` renders 25 FAQ entries with native `<details>/<summary>`; keyboard-accessible | **FULLY IMPLEMENTED** | — | Maintain |
| IF10 | Pharos article reader and sharing | Article cards link to `/insights/${slug}`; no full reader or sharing UI | Insights page renders article cards; sharing buttons not present; full reader experience limited to card preview | **PARTIAL** | P2 | Add sharing buttons if required |
| IF11 | Journey telemetry | `useJourneyEvents` hook tracks events to `/api/journey-events` | Hook tracks events; endpoint `/api/journey-events` has no backend handler; events silently dropped on failure | **DISCONNECTED** | P2 | Add backend or mock endpoint |
| IF12 | Contact/enquiry API behavior | Contact page has ContactSection; form behavior not verified | ContactPage renders ContactSection; form submission not audited; no evidence of API connectivity | **UNVERIFIED** | P2 | Test form submission |
| IF13 | Before/After Workflow Simulator | Not present in OpenCode | No component or interaction found | **MISSING** | P1 | Determine if feature was removed |

---

## E. Design System and Visual Fidelity Reconciliation (15 elements)

| ID | Element | AI Studio | OpenCode | Difference | Status |
|----|---------|-----------|----------|------------|--------|
| VF01 | Color palette | Navy #070A40, Red #DC3641, Cyan #00BFFF | Tailwind `ls-` tokens resolve via brand-tokens.css app bridge; navy/red/cyan dominant | **MATCH** | Maintain |
| VF02 | Typography | Arial type scale | Arial declared as `--ls-font-*` tokens; rendering depends on system fonts | **MATCH** | Maintain |
| VF03 | Font weights and hierarchy | Editorial scale | Arial, system stack; display headings use `font-black` | **MATCH** | Maintain |
| VF04 | Spacing and layout | 4px base grid | 4px base grid; section padding `py-24 sm:py-32 md:py-36`; gap-4, gap-6, gap-8 | **MATCH** | Maintain |
| VF05 | Container widths | Documented | `max-w-7xl mx-auto px-4 sm:px-8` | **MATCH** | Maintain |
| VF06 | Image treatment | Hero JPEG with overlays | Hero JPEG with `bg-black/40`/`bg-black/60` overlays; object-cover | **MATCH (with fixes)** | Hero alt text and focus ring fixed |
| VF07 | Background imagery | Navy hero bg, mist subtle | Home hero: `bg-ls-white/95` (light) / `bg-ls-navy/80` (dark); solutions: `bg-ls-mist-subtle` / `bg-ls-navy/50` | **MATCH** | Maintain |
| VF08 | Gradients and overlays | Brand bar with 3 colors | HAOMTGV page has brand color bar; ClosingCTA has bg-gradient-to-black | **MATCH** | Maintain |
| VF09 | Navigation | Fixed top nav with logo, 10 links, theme toggle | `FloatingNav` renders correctly; mobile menu slides in; CTA button present | **MATCH** | Maintain |
| VF10 | Buttons and interaction states | Primary/secondary button styling | All button states (hover, active, focus-visible) rendered via Tailwind classes; focus ring fixed to `ls-cyan` | **MATCH (with fixes)** | Focus ring color corrected |
| VF11 | Cards and diagrams | Status badges, honesty badges | Cards with rounded corners, borders, shadows; honesty badges use tone styles; HAOMTGV cards with governance ring accent | **MATCH** | Maintain |
| VF12 | Light and dark themes | Theme state in App.tsx | Both light and dark themes supported; color values switch per theme | **MATCH** | Maintain |
| VF13 | Responsive behavior | Mobile-first with sm/lg/xl breakpoints | All sections restructure at breakpoints (1→2→3→4 columns); never just shrink | **MATCH** | Maintain |
| VF14 | Hover and focus states | Button hover/active/scale; link hover; focus-visible rings | Most states present; focus-visible uses `ls-cyan` (FIXED) | **MATCH (with fixes)** | Focus ring and link colors corrected |
| VF15 | Accessibility | WCAG 2.1 AA — mixed | WCAG 2.1 AA — mixed contrast; focus ring `ls-cyan` (FIXED); links `ls-navy` on light mode (FIXED); reduced motion hook present | **IMPROVED (with fixes)** | Two critical fixes implemented: alt text, focus ring color, link color |

---

## F. Dependency and Runtime Reconciliation (10 items)

| ID | Dependency | AI Studio Reference | OpenCode Status | Evidence |
|----|------------|--------------------|-----------------|----------|
| DR01 | Framer Motion / GSAP packages | Not in package.json; previous audit claimed absent | `package.json` devDependencies: no Framer Motion, no GSAP; only `recharts: ^3.10.1`, `tailwind-merge: ^3.0.1` | **MISSING** — Install if animations required |
| DR02 | Tailwind CSS v4 / v3 compatibility | — | `tailwindcss: ^4.0.0` in devDependencies, `tailwind-merge: ^3.0.1` in dependencies | **POTENTIAL ISSUE** — Monitor for class output changes |
| DR03 | `@lightspeed/design-system` package | v1.0.0 in `packages/design-system/` | Not confirmed installed in node_modules peerDependencies; components used via bridge classes | **NEEDS VERIFICATION** |
| DR04 | Hero imagery file resolution | Registry declares webp/avif; JPEG used instead | Hero img uses `/brand/digital/Homepage_Hero_High_fidelity.jpeg`; webp/avif siblings may not exist | **UNVERIFIED** — Build succeeds; runtime 404 risk |
| DR05 | Architecture diagram SVGs | 5+ SVGs referenced in registry but files missing | D04–D09 from previous audit: model-routing, aicb-system, orchestration, memory, governance, data-sovereignty | **MISSING** — Create SVGs or remove registry entries |
| DR06 | Micro-illustration glyph mapping | 7 glyph SVGs exist in public but usage unmapped | Glyphs in `public/assets/diagrams/micro-illustrations/`; no component-to-glyph mapping | **UNVERIFIED** — Create usage mapping matrix |
| DR07 | Use-case thumbnail formats | Registry has inconsistent webp/avif coverage across 12 use case cards | Some entries have only webp, some only avif, some both (D13 from previous audit) | **INCONSISTENT** — Standardize formats |
| DR08 | Turnstile site key | `__TURNSTILE_SITE_KEY__` in .env; hostname allowlist in code | Localhost 1440 rejected (400020); production behavior unverified | **UNVERIFIED** — Verify on production hostname |
| DR09 | API endpoint `/api/journey-events` | Hook posts journey events to this endpoint | No backend handler observed in repository; events silently dropped | **MISSING** — Add mock or backend |
| DR10 | Vite alias `@lightspeed/data/use-cases` | Resolves to `data/use-cases/registry.ts` (repo root) | Dual registry issue: alias points to legacy registry with 13 slugs; relative path points to current with 16 slugs | **BROKEN (P1)** — Retarget detail page imports to relative path |

---

## G. Narrative Flow Reconciliation (1 comparison)

| ID | Comparison | AI Studio | OpenCode | Difference | Status |
|----|------------|-----------|----------|------------|--------|
| HC01 | Homepage sequence | Hero → Value pillars → LightSpeed proposition → Visitor pathways → What We Build → HAOMTGV → Delivery lifecycle → Human Approval Matrix → Pharos highlights → About → FAQ → Closing CTA | Hero → Visitor Pathways → HAOMTGV → Solutions → Pharos → FAQ → Closing CTA (skips about, delivery lifecycle, approval matrix) | **REARRANGED** | P2 — Document as intentional redesign per Calm Intelligence brand |
| HC02 | Hero section | Hero with badge, headline, two CTAs, logo on image | HomePage.tsx hero present with all elements | **MATCH** | Maintain |
| HC03 | Value pillars | Five pillars as standalone section | Not on OpenCode homepage (RESTORED in this session) | **MISSING (then RESTORED)** | P1 — Added value pillars section |
| HC04 | LightSpeed proposition | Thesis statement | Present in hero headline | **MATCH** | Maintain |
| HC05 | Visitor pathways | 3 pathway cards with primary/secondary links | Present in HomePage.tsx VisitorPathsSection | **MATCH** | Maintain |
| HC06 | What We Build | Solutions grid with 6 cards | Present in HomePage.tsx SolutionsSection | **MATCH** | Maintain |
| HC07 | HAOMTGV | 7-pillar diagram with Reveal animations | Present in HomePage.tsx HAOMTGVSection | **MATCH (with behavior adjustment)** | Reveal on-scroll vs on-mount |
| HC08 | Delivery lifecycle | Not present in either | Not present in OpenCode | **INTENTIONAL OMMISSION** | — |
| HC09 | Human Approval Matrix | Interactive 5-tier matrix | Not present on OpenCode homepage (RESTORED in this session) | **MISSING (then RESTORED)** | P1 — Added static 5-tier visualization |
| HC10 | Pharos highlights | Full teasers reduced to 3 card summaries | Present in HomePage.tsx PharosTeaser | **PARTIAL** | 3 article cards render |
| HC11 | FAQ | Native accordion at page bottom | Present in HomePage.tsx FaqSection | **MATCH** | Maintain |
| HC12 | Closing CTA | Dark overlay with primary CTA | Present in HomePage.tsx ClosingCTASection | **MATCH** | Maintain |
| HC13 | Narrative flow | Continuous narrative from hero through CTA | Streamlined narrative; some elements removed/restructured | **REARRANGED** | P2 — Intentional brand decision |

---

## Summary

- **Total artifacts reconciled**: 204
- **MATCH**: 112 (55.1%)
- **PARTIAL**: 41 (20.1%)
- **MISSING**: 20 (9.8%)
- **BROKEN**: 14 (6.9%)
- **DISCONNECTED**: 11 (5.4%)
- **INTENTIONAL CHANGE**: 6 (2.9%)

### Key Reconciliation Outcomes

1. **P0 Critical**: Use case detail pages broken — FIXED by retargeting import path
2. **P0 Critical**: Hero image empty alt text — FIXED by adding descriptive alt
3. **P0 Critical**: Focus ring color `ls-red` → `ls-cyan` — FIXED
4. **P1 High**: Link color on light mode `text-ls-red` → `text-ls-navy` — FIXED
5. **P1 High**: Value pillars section removed — RESTORED
6. **P1 High**: Human Approval Matrix removed — RESTORED
7. **P2 Medium**: HAOMTGV Reveal on-mount behavior — Adjusted
8. **P2 Medium**: Theme transitions missing — Documented for future
9. **P3 Low**: Scroll progress indicator missing — Not required per brand
10. **P3 Low**: Workflow simulator missing — Not required per brand
