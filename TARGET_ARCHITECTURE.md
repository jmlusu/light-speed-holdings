# Target Architecture — LightSpeed Holdings Website

**Generated:** 2026-09-27 after completing LEGACY_INVENTORY.md and SPECIFICATION_MAP.md
**Source of truth:** MASTER_SPEC.md (priority 1 per REBUILD_DIRECTIVE §2)
**User decisions incorporated:**
- Three.js immersive stage: **STRIPPED** (user confirmed §25/§31 cleanup)
- Primary nav CTA: **Start a Conversation** (matches §7 item 9; label refinement permitted per §7/§33)

---

## 1. INFORMATION ARCHITECTURE

Per `MASTER_SPEC.md` §7 item 9 and §8, the public IA (9 sections + contact) is the structural backbone. All routes derive from this.

| Section | Route | Primary CTA / Label | Notes |
|---|---|---|---|
| 1 Home | `/` | “Start a Conversation” (nav); *Hero CTA: “Request an Executive Briefing”* (section-internal) | No Three.js immersive stage. Hero mist/slate visual only. |
| 2 What We Do | `/what-we-do` | CTA card → `/contact` or `/ai-company-builder` | |
| 3 AI Company Builder | `/ai-company-builder` | CTA → `/contact` / `/ask` | Consumes `company` from siteContent. |
| 4 Solutions | `/solutions` | Problem/outcome cards (5-question framing) | New beat per §8 #6 (previously shared Builder space). |
| 5 Sectors | `/sectors` | Sector evidence cards (PROVEN/CURRENT/DEMO/FUTURE) | Evidence re-verified; `2,557` metric replaced with governed source. |
| 6 Proof | `/proof` | Evidence cards with honesty labels; *no “100% Auditable”* absolute | Metrics canonicalized from metrics registry (§16). |
| 7 Insights | `/insights` | Article/category listing; *no PharosSection/stone texture* | Calm Intelligence only (§19). |
| 8 About | `/about` | “One Human CEO. 90 AI Agents.” (AboutBand) | Agent count from registry (§15). |
| 9 Contact / Start a Conversation | `/contact` | 5-step form → `POST /api/enquiry` (SLA “within two business days”) | CTA label matches spec; BriefingModal kept as contact flow. |
| — Legal | `/legal/privacy`, `/legal/terms` | — | |

**Catch-all**: `*` → `/` (legacy guard; obsolete routes `/offerings`, `/evidence`, `/industries`, `/why`, `/leadership`, `/careers` removed).

---

## 2. ROUTE MAP (derived from MASTER_SPEC §8 narrative + §7 IA)

| Route | Component | Page Kind | Narrative Beat |
|---|---|---|---|
| `/` | `HomePage` | Chaptered homepage (§8 beats 1–10) | 1. Orientation → 10. CTA |
| `/what-we-do` | `WhatWeDoPage` | Problem/outcome page | §10 Solutions content |
| `/ai-company-builder` | `AiCompanyBuilderPage` → `AiCompanyBuilderSection` | Builder journey page | §4 + §5 |
| `/solutions` | `SolutionsPage` | Dedicated solutions page | §10 distinct page |
| `/sectors` | `SectorsPage` | Sector evidence page | §11 |
| `/proof` | `ProofPage` | Evidence page | §12 |
| `/insights` | `InsightsPage` | Insights listing page | §13 |
| `/about` | `AboutPage` → `AboutSection` | About page | §8 #10 CTA + leadership |
| `/contact` | `ContactPage` → `ContactSection` | Contact form page | §14 + SLA |
| `/ask` | `AskLightSpeed` | Wizard page | §14 client-side only |
| `/legal/privacy` | `PrivacyPage` | Static | |
| `/legal/terms` | `TermsPage` | Static | |

**Component-to-page mapping (post-rebuild):**

| Component | Target page(s) | KEEP/MODIFY/REBUILD/REMOVE |
|---|---|---|
| `ImmersiveStage.tsx` + `src/three/` | **REMOVE** (user decision) | — |
| `HeroSection.tsx` | Home `HeroSection` beat 1 | **MODIFY** — metrics registry wired; “100% Auditable” qualified; `homeImmersiveCopy` data retained; no WebGL canvas |
| `ThesisSection` | Home beat 2 + AI Company Builder pages | **KEEP** (valueCycle retained) |
| `BuilderSection` | Home beat 4 + `/ai-company-builder` | **KEEP** |
| `WorkforceSection` | Home beat 5 + `AboutBand` | **REBUILD** — registry-driven copy from `agent-registry.public.json`; 90-agent canonical; departments from same |
| `SectorsSection` | Home beat 7 + `/sectors` | **MODIFY** — evidence tiers from governed registry; stale metrics removed |
| `ProofSection` | Home beat 8 + `/proof` | **MODIFY** — metrics from canonical registry; no unqualified absolutes |
| `InsightsSection` | Home beat 9 + `/insights` | **MODIFY** — calm design only (no Pharos texture) |
| `AboutBand` | Home beat 10 + `/about` | **REMOVE** — replaced by `AboutSection` data consumption from registry |
| `BriefingSection` | Home beat 10 CTA + `/contact` CTA | **KEEP** (label “Start a Conversation” in nav; briefing modal stays as contact flow) |
| `ChapterRail` | Homewide scroll + chapter nav | **KEEP** — chapter labels from `homeImmersiveCopy` (no immersive dependency) |
| `PharosSection` | **REMOVE** (user decision: parallel visual system folded into Calm Intelligence) | — |
| `NewsletterSignup` | `/insights` footer / `/contact` side | **KEEP** — posts `enquiryType: 'Newsletter subscription'` to `/api/enquiry` |
| `ExecutiveBriefingModal` | Global in `SiteLayout`; contact flow from nav/footer CTA | **KEEP** |
| `FloatingNav` | Global nav (9 links + CTA) | **MODIFY** — primary CTA = “Start a Conversation”; secondary “Book a Briefing” retained for backward compat but nav label leads to modal |
| `SiteFooter` | Global footer (4 columns) | **KEEP** |
| `SiteLayout` | Global layout + modal outlet | **KEEP** |
| `Reveal`, `PageIntro`, `SectionHeading`, `CtaBand`, `RelatedLinks` | Shared primitives | **KEEP** |
| `HonestyBadge` | Throughout (Proof, Solutions, Sectors) | **KEEP** |
| `ContactSection` | `/contact` | **KEEP** |
| CTA → `/api/enquiry` pipeline | All three forms | **KEEP** |

---

## 3. CONTENT / DATA MODEL (post-rebuild)

**Canonical registries** (each exported as JSON; consumed via typed hooks or server-rendered values):

| Registry | Source file | Governed fields | Consumers |
|---|---|---|---|
| `siteContent` | `src/data/siteContent.ts` | company, solutions, insightTeasers, workCaseStudies, workPolicy, GOVERNANCE_SOLUTION, HonestyLabel/TONE_STYLES | All pages (KPI: all 7 dead exports removed) |
| `agentRegistry` | `src/data/generated/agent-registry.public.json` | 90 agents, 20 departments, 5-tier approval, per-department metadata | `WorkforceSection`, `AboutBand` (REBUILT to consume) |
| `metrics` | **NEW** — canonical metrics registry | agentCount (90), testCount (verified), departments (20), five-tier, sectorStats, caseStudyMeta | Home `HeroSection`, `ProofSection`, `ProofPage`, `SectorsPage` (replace 6 duplicated call-sites) |
| `solutions` | `siteContent.solutions` | 5-question per solution, honesty labels | `SolutionsPage`, `WhatWeDoPage` |
| `insightCategories` | `src/data/useCaseCatalogData.ts` (`OFFER_FAMILIES`) | 12 categories | `InsightsPage` |
| `sectors` | **NEW** — sector registry (PROVEN/CURRENT/DEMO/FUTURE tiers + evidence refs) | Sector data, evidence status | `SectorsPage` (replaces hard-coded `SECTORS` const) |
| `caseStudies` | `siteContent.workCaseStudies` + `siteContent.workPolicy` | Brief case metadata, source, evidence status | `ProofPage` |

**Removed/dead entries (post-rebuild cleanup):**

- 7 dead `siteContent` exports: `mission`, `vision`, `deliverables`, `leadership`, `faqs`, `events`, `industries` — **REMOVE** from file; if still needed, they belong in a content audit branch, not the public site.
- `companyData.ts` — **REMOVE** or **rewire** (consumed only by its own test; §26 abandoned experimental code).
- `PharosSection.tsx` — **REMOVE** (parallel visual system incompatible with Calm Intelligence §19/§26).
- `AboutSection` heading “Why LightSpeed” — **MODIFY** to remove legacy term (or reword per approved decision).
- `AboutBand` component — **REMOVE** (replaced by `AboutSection` consuming `agentRegistry`).
- `SectorsPage` hard-coded `SECTORS` const — **REMOVE**; sector data from new sector registry.
- `ProofPage` hard-coded stats (2,557 ×3, 90 Configurations, 20 Live, 100% Auditable) — **REBUILD** via metrics registry.
- `HeroSection` hard-coded chips (90 Configurations / 2,557 Passing / 20 Live / 100% Auditable) — **REBUILD** via metrics registry.
- `index.html` dark body `bg-[#070a40]` — **MODIFY** to `#121518`; add favicon/OG/theme-color.
- `onboarding.py:6` “127 agents” — **MODIFY** to “90 agents”.
- All `IMPLEMENTATION_AUDIT.md` claims contradicted by repo — **REWRITE** at rebuild completion.

---

## 4. DESIGN TOKENS (Calm Intelligence, unchanged from inventory §9)

- Light: `#F7F8F9` (mist), Dark: `#121518` (deep mineral), Navy: `#070A40`, Red: `#E63946`, Cyan: `#00BFFF`
- Font: Arial, scale 36→12pt; 4px spacing grid
- Motion: “Slow to the eye. Fast to the mind.” — restraint; `prefers-reduced-motion` respected; no decorative animation
- No neon/cyberpunk/noisy gradients/excessive glassmorphism

---

## 5. PUBLIC / INTERNAL BOUNDARY

- **No private prompts, credentials, internal endpoints, or secrets in public code** (§14/§27/§28 by construction).
- `agent-registry.public.json` is the *only* agent data published to the site; all other agent internals remain in `companyData.ts` (which itself will be **REMOVED** or heavily gated).
- `AskLightSpeed` is fully client-side; no LLM/backend calls in public bundle.
- Honesty labels + `TONE_STYLES` govern claim qualification; no fabricated testimonials/logos/awards.

---

## 6. AGENT REGISTRY BOUNDARY

- Canonical count = **90** AI agents (one source of truth: `agent-registry.public.json`).
- 20 departments (same source).
- Five-tier human approval visible but governed by internal approval matrix (not rendered on public site beyond the “five-tier” label).
- No agent prompts, credentials, or endpoint URLs exposed.

---

## 7. ANIMATION / MOTION SYSTEM (post-Three.js strip)

With the immersive stage removed, the animation system is lighter:

- **`prefers-reduced-motion`**: respected globally — no scroll-reveal, no chapter rail motion, no Hero motion beyond initial paint.
- **Gentle scroll reveals**: `Reveal` primitive honored; if motion is permitted, sections fade/slide in on view. If reduced motion is preferred, instant appearance.
- **ChapterRail** (scroll progress indicator): static CSS-only indicator (no JavaScript animation). Click-to-nav only.
- **Hero eyepiece/intro**: static mist/stone treatment; no WebGL layer.
- **All other motion**: same as current `index.css` transitions (`--transition-*` tokens); audit line-by-line for reduced-motion compliance after rebuild.

---

## 8. RESPONSIVE STRATEGY

- Mobile-first: hamburger menu in `FloatingNav`; grid stacks (`grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4`).
- All 12 routes tested at 390px (Plan.md verification baseline). Not yet run this session — verify before launch.
- Touch targets: minimum 44px hit area; no reliance on hover-only states.

---

## 9. TEST COVERAGE POST-REBUILD (target)

The rebuild does NOT automatically inherit the existing 42 vitest tests. New target:

| Test category | Target count | Evidence |
|---|---|---|
| Unit tests (vitest) | 17 tests (2 files, post-Step 1); existing code unchanged, deleted test files removed | new: route-map test, metrics-registry integration, content-state test |
| Accessibility tests | 0 (no automated suite) + manual audit | §24 |
| Route integrity | 1 integration test per route (9 + legal + ask) | New: confirms each route resolves and renders expected content |
| Build validation | `tsc --noEmit` 0, `vite build` with chunk warning < 5 warnings | Continuous |
| Performance regression | No >500 kB non-three chunks; three.js chunk only if retained | If Three.js stripped, no chunk warning |

---

## 10. IMPLEMENTATION ROADMAP (ordered, per REBUILD_DIRECTIVE §21)

The following order respects dependency chains:

| # | Action | Blocks | Spec ref |
|---|---|---|---|
| 1 | **Strip Three.js** + `ImmersiveStage` + `src/three/`; update `HomePage` to hero static mist/slate; remove ImmersiveStage import from `App.tsx`/`HomePage.tsx` | None (first) | §25, §31 |
| 2 | **Trim 7 dead siteContent exports** from `siteContent.ts`; update all imports | #1 (removes unused import errors) | §15, §31 |
| 3 | **Build canonical metrics registry** + update all 6 metric call-sites (Hero, ProofSection, ProofPage, SectorsPage) to consume it | None independent | §15, §16 |
| 4 | **Rewrite WorkforceSection + AboutBand** to consume `agentRegistry` (90 agents, 20 depts) | #3 (metrics pattern) | §5, §15 |
| 5 | **Add Solutions beat** as distinct `/solutions` page + restructure BuilderSection/home beat 4 | #2 (siteContent still has solutions data) | §8 #6, §10 |
| 6 | **Rewrite SectorsPage** to consume sector registry; remove hard-coded `SECTORS` const; fix stale 2,557 metric | #3 (metrics); #4 (agent model consistent) | §11, §16 |
| 7 | **Rewrite InsightsPage** — strip PharosSection/stone texture; calm design only; add category list from `OFFER_FAMILIES` | None | §13 |
| 8 | **Rewrite AboutSection** — remove "Why LightSpeed" heading; consume `agentRegistry` for 90-agent copy | #4 | §8, §15 |
| 9 | **Fix index.html** — favicon + og:image + theme-color + dark bg `#121518`; remove `dark:bg-[#070a40]` | None | §20, §21 |
| 10 | **Nav CTA** — set primary nav label to "Start a Conversation"; keep secondary "Book a Briefing" for backward compat if desired | None (user decision) | §7, §33 |
| 11 | **a11y + 390px responsive verification** (Playwright/axe) across all routes | #10 | §22, §23, §24 |
| 12 | **New route-map vitest test** + **metrics-registry integration test** | #3 | §32 |
| 13 | **Final `IMPLEMENTATION_AUDIT.md`** (per REBUILD_DIRECTIVE §21) | All above | §21 |
| 14 | **Full `tsc --noEmit` + `vite build`** + `vitest run` + `pytest --collect-only -q` | All above | §20 |

---

**Status:** Target architecture defined per MASTER_SPEC and user decisions. **Step 1 executed 2026-09-27:** Three.js / `ImmersiveStage` / `src/three/` stripped; hero static mist/slate fallback added (§19: `#F7F8F9` / `#121518` fixed backdrop); lockfile reconciled (`bun install` prunes `three` + `@types/three`); dead remnants removed (`useScrollProgress`, `HeroMist`, vite three `manualChunks`). Re-verified 18:21: tsc 0 errors · vitest 17/17 · build exit 0. Nav CTA decision recorded as "Start a Conversation" — **implementation pending (Step 10)**; `FloatingNav` still shows "Book a Briefing".