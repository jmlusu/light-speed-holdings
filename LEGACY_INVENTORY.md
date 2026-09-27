# Legacy Inventory — LightSpeed Holdings Website

**Date:** 2026-09-27 (rebuilt against current working tree; supersedes the 2026-09-25 inventory)
**Purpose:** Catalog every route, component, section, content block, data source, design token, dependency, navigation item, form, API integration, asset, and test before the structural rebuild per `REBUILD_DIRECTIVE.md` §1–2.
**Companion:** `MASTER_SPEC.md` (source-of-truth priority 1), `SPECIFICATION_MAP.md`
**Baseline commit:** `52b27136` (working tree inspected as-is; unrelated uncommitted user changes present in `docs/`, `hr/`, `orchestrator/`, `open-design/` — not touched)

---

## 0. Method and Legend

Every asset below is classified:

| Class | Meaning |
|-------|---------|
| **KEEP** | Complies with MASTER_SPEC; retain as-is (may need minor wiring). |
| **MODIFY** | Right location/concept, but content, styling, or structure deviates from MASTER_SPEC. |
| **REBUILD** | Concept required by MASTER_SPEC, but current implementation is structurally wrong. |
| **REMOVE** | Legacy structure/terminology/content incompatible with MASTER_SPEC; delete. |

**Caveats:** this inventory is the *legacy audit*, not a verdict list — a KEEP here can still be changed later by an approved decision (MASTER_SPEC §33 priority order). Data flagged in §7 requires verification against internal systems before republication.

---

## 1. VERIFICATION BASELINE (2026-09-27)

**Post-Step-1 re-verification (2026-09-27 18:21, local toolchain pinned):**

| Check | Command | Result |
|-------|---------|--------|
| Type check | `node_modules/.bin/tsc --noEmit` (TS 5.9.3) | ✅ 0 errors |
| Frontend tests | `vitest run` | ✅ 17/17 pass (1 file) |
| Production build | `vite build` | ✅ exit 0 — single 428 kB entry, no `three` chunk |
| Backend tests | `pytest -q` | ✅ 2,566 passed, 2 skipped (67 deselected) |
| Dependency graph | `bun install` | ✅ `three` + `@types/three` pruned from lockfile and `node_modules` |

> **Correction notice:** the original capture below was taken **before** Step 1's code strip, so its 42/42 (5 files) figure included the three-stage test files deleted with `src/three/`. After the strip the suite ran 22 tests until dead `useScrollProgress` (5 tests) + `HeroMist` were removed. Always verify with the **local** `tsc` — the global binary is v7.0.2, which rejects `baseUrl` (TS5102/TS5090).

**Pre-Step-1 capture (historical, kept for provenance):**

| Check | Command | Result |
|-------|---------|--------|
| Type check | `tsc --noEmit` | ✅ 0 errors |
| Frontend tests | `vitest run` | ✅ 42/42 pass (5 files) |
| Production build | `vite build` | ✅ exit 0 (⚠️ `three` chunk 517 kB > 500 kB warning) |
| Backend tests | `pytest --collect-only -q` | 2,561 selected / 2,628 total (67 deselected) |

**Stale-document warnings (docs currently contradict the repo):**

- `IMPLEMENTATION_AUDIT.md` claims "no Three.js / `three` dependency removed" — **false at capture time**: `package.json` had `three ^0.186.1`, `src/three/` existed, `ImmersiveStage` mounted WebGL on the homepage (commit `e4619207`). *(Step 1 has since removed the dependency, `src/three/`, and the stage.)*
- `IMPLEMENTATION_AUDIT.md` claims "vitest 1,179 passing" and "onboarding.py 127→90 fixed" — **false**: vitest runs 17 tests; `src/ai_company/hr/onboarding.py:6` still says "127 agents".
- Five root docs (`QA_ANALYSIS`, `SITEMAP`, `BRAND_AUDIT_REPORT`, `accessibility-checklist`, `performance-testing-matrix`) and two `temp_issue_*.md` files were intentionally deleted per 2026-09-27 user decision; provenance ratified.
- `Plan.md` mandates a "five-item nav" — superseded by MASTER_SPEC §7 (nine-item IA); do not follow.

---

## 2. ROUTES AND PAGES

Router: `src/App.tsx` (`createBrowserRouter`, all under `SiteLayout`).

| Route | Component | Classification | Notes / required action |
|-------|-----------|---------------|--------------------------|
| `/` | `HomePage` | **MODIFY** | Chapter order vs §8 narrative: current = Hero → Thesis → Builder → Workforce → Sectors → Proof → Insights → About → Briefing. §8 requires *Solutions* between 90-agent workforce (5) and Sectors (7) — no dedicated Solutions chapter exists on home (BuilderSection partially covers it, labelled "AI Company Builder and solutions"). |
| `/what-we-do` | `WhatWeDoPage` | **KEEP** | Uses `OFFER_FAMILIES` + `solutions` + `GOVERNANCE_SOLUTION`, honesty badges, human sign-off copy. |
| `/ai-company-builder` | `AiCompanyBuilderPage` → `AiCompanyBuilderSection` | **KEEP** | Consumes `company` from siteContent; CTA wiring OK. |
| `/solutions` | `SolutionsPage` | **KEEP** | Problem/outcome cards + honesty labels; matches §10. |
| `/sectors` | `SectorsPage` | **MODIFY** | Local `SECTORS` const with four honesty tiers (matches §11 taxonomy) but hard-coded inside the page — not a governed registry (§15); contains stale metric "2,557" (see §7). |
| `/proof` | `ProofPage` | **MODIFY** | Evidence-first layout good (§12); stats block hard-codes 2,557 with `source:` label; claim "validated against 2,557 automated tests" ×3 — stale (see §7). |
| `/insights` | `InsightsPage` | **MODIFY** | Categories match §13 list exactly. Uses `PharosSection` + `NewsletterSignup` (legacy-inherited; see §5). No actual article content/route — category list only. |
| `/about` | `AboutPage` → `AboutSection` | **MODIFY** | Heading "Why LightSpeed" (§7-era legacy term, see §8). Leadership data: `leadership` export exists but is **unimported** — About content is hard-coded. |
| `/contact` | `ContactPage` → `ContactSection` | **KEEP** | 5-step form → `POST /api/enquiry`, Turnstile + honeypot + idempotency key, SLA copy. |
| `/ask` | `AskLightSpeed` | **KEEP** | Scripted client-side discovery wizard (5 steps); public-safe copy only, consumes `solutions`; hands off to briefing modal. Not in §7 IA — extra utility route, harmless (§7 allows refinement). |
| `/legal/privacy` | `PrivacyPage` | **KEEP** | |
| `/legal/terms` | `TermsPage` | **KEEP** | |
| `*` | `Navigate → /` | **KEEP** | Acts as legacy-route guard; no explicit `/offerings`, `/evidence`, `/industries`, `/why`, `/leadership`, `/careers` routes remain (obsolete routes confirmed absent). |

---

## 3. NAVIGATION AND FOOTER

**`FloatingNav.tsx`** — pill header, fixed, `pointer-events` split correctly.

| Item | Status |
|------|--------|
| 9 links: Home, What We Do, AI Company Builder, Solutions, Sectors, Proof, Insights, About, Contact | **KEEP** — exactly matches §7 IA. |
| CTA button "Book a Briefing" (desktop) / "Book an Executive Briefing" (mobile), opens `ExecutiveBriefingModal` | **DECIDED** — §7 IA item 9 reads "Contact / Start a Conversation"; §7 overrides legacy A8 "Book an executive briefing" in Plan.md; final label per §7 / §33 ratified 2026-09-27. |
| Theme toggle (aria-labels present) | **KEEP** |

**`SiteFooter.tsx`** — 4 columns: LIGHTSPEED (Home…Sectors), PROOF & INSIGHTS (Proof, Insights, About), CONNECT (Contact, Ask LightSpeed, Book a Briefing), LEGAL (Privacy, Terms). | **KEEP** — column headings generic, all targets exist. |

---

## 4. HOMEPAGE CHAPTER INVENTORY vs §8 NARRATIVE

| §8 beat | Current chapter | Status |
|---------|-----------------|--------|
| 1 Orientation | `HeroSection` (eyebrow, headline, who/what/where, 3 CTAs) | **KEEP** (metrics issues §7) |
| 2 Core proposition | `ThesisSection` | **KEEP** |
| 3 Operating model (Strategy → Build → Govern → Research & Policy) | `ThesisSection` (valueCycle from siteContent — canonical value fixed) | **KEEP** |
| 4 AI Company Builder journey | `BuilderSection` | **KEEP** |
| 5 90-agent workforce | `WorkforceSection` + `AboutBand` | **MODIFY** — copy hard-coded, not registry-driven (§15) |
| 6 Solutions | *missing as a beat* — `BuilderSection` doubles as "AI Company Builder and solutions" | **REBUILD** — add distinct Solutions chapter or restructure Builder |
| 7 Sectors | `SectorsSection` | **KEEP** |
| 8 Proof | `ProofSection` | **MODIFY** — duplicated/hard-coded stats (§7) |
| 9 Insights | `InsightsSection` (uses `insightTeasers`) | **KEEP** |
| 10 CTA | `BriefingSection` | **KEEP** |
| — | `ChapterRail` (scroll progress, uses `homeImmersiveCopy`) | **KEEP** |
| — | ~~`ImmersiveStage` (WebGL background)~~ | **REMOVED 2026-09-27 (Step 1)** — user decision: STRIP. Deleted with `src/three/`; §19 static mist/slate fallback (`#F7F8F9` / `#121518` fixed backdrop) now occupies the stage layer. |

---

## 5. COMPONENT INVENTORY

### 5.1 New architecture (`src/components/site/`, `src/components/home/`) — generally KEEP

`PageIntro`, `SectionHeading`, `CtaBand`, `RelatedLinks`, `HonestyBadge`, `Reveal`; home: `HomeSection`, `ScrimPanel`, `ChapterRail`, `ThesisSection`, `BuilderSection`, `WorkforceSection`, `SectorsSection`, `ProofSection`, `InsightsSection`, `AboutBand`, `BriefingSection`, `index.ts`.

### 5.2 Legacy-inherited components

| Component | Class | Findings / action |
|-----------|-------|-------------------|
| `PharosSection` | **REBUILD** | "Pharos" editorial sub-brand + `pharos-stone-masonry` texture; only consumer is `InsightsPage`. §18/§26 discourage parallel visual systems; §13 needs an insights index, not a themed band. |
| `NewsletterSignup` | **MODIFY** | Works (posts `enquiryType: 'Newsletter subscription'` to `/api/enquiry` with Turnstile/honeypot). Retain pipeline; re-home under rebuilt Insights. |
| `ExecutiveBriefingModal` | **KEEP** | Global modal in `SiteLayout`; real backend, "Submit Confidential Request". Confirm final CTA label (§7 item 9). |
| `AboutSection` | **MODIFY** | Heading "Why LightSpeed" (legacy term, §8); leadership hard-coded instead of consuming `leadership` registry (§15). |
| `ContactSection` | **KEEP** | Real backend, SLA copy, honeypot, Turnstile. |
| `AskLightSpeed` | **KEEP** | See §2. |
| `HeroSection` | **MODIFY** | Static hard-coded metric chips (90 / 2,557 / 20 / 100%) duplicated across files — §15/§16 violation; CTA set: `/contact`, `/ai-company-builder`, `/what-we-do`. |
| `SiteLayout` | **KEEP** | No `ThreeCanvas`; manages modal + outlet. |
| `FloatingNav`, `SiteFooter` | **KEEP/MODIFY** | §3. |
| ~~`ImmersiveStage` + `src/three/*`~~ | **REMOVED 2026-09-27 (Step 1)** | `Scene`, `CameraRig`, `materials`, `tiers`, `poster`, `mountGate` + 20 tests all deleted; user decision: STRIP. |
| `ExecutiveBriefingModal`-adjacent `scrim`/texture utilities in `index.css` | **MODIFY** | `index.css` rewritten to Calm Intelligence (~161 lines): fonts Arial, motion tokens, ripple. Audit vs §20/§22 — no off-palette hexes found in the sweep; body `dark:bg-[#070a40]` in `index.html` conflicts with §20 dark `#121518` (App sets html bg to `#121518`). |

### 5.3 Shared primitives

`Reveal` (used by HomePage, WhatWeDo, Proof, Insights, Contact flows) — **KEEP**; must key off `prefers-reduced-motion` (verify). `PageIntro`, `CtaBand`, `RelatedLinks` — **KEEP**.

---

## 6. DATA SOURCES

| Source | Consumers | Class | Notes |
|--------|-----------|-------|-------|
| `src/data/siteContent.ts` (32 kB) | company, solutions, insightTeasers, workCaseStudies, workPolicy, GOVERNANCE_SOLUTION, HonestyLabel/TONE_STYLES | **KEEP (trim)** | Canonical content model. **Dead exports (unimported anywhere):** `mission`, `vision`, `deliverables`, `leadership`, `faqs`, `events`, `industries` — remove or wire up (commit `a093aaca` claimed a trim; these 7 remain). |
| `src/data/generated/agent-registry.public.json` (133 kB) | imported only by `companyData.ts` | **MODIFY** | Governed public registry exists (§28 ✅) but **nothing on the site renders it** — workforce/90-agent copy is hard-coded instead (§15). |
| `src/data/companyData.ts` | only its own test | **REMOVE or rewire** | Dashboard-demo data (tasks, approvals, escalations, KPIs, audit log, model tiers) unused by any page — §26 "abandoned experimental code" candidate. |
| `src/data/useCaseCatalogData.ts` (`OFFER_FAMILIES`) | `WhatWeDoPage` | **KEEP** | |
| `src/data/homeImmersiveCopy.ts` | `HeroSection`, `ChapterRail` | **KEEP** | |
| Hard-coded component copy | `WorkforceSection`, `AboutBand`, `SectorsPage.SECTORS`, `InsightsPage.INSIGHT_CATEGORIES` | **MODIFY** | Move to structured registries per §15. |

---

## 7. METRICS AND CLAIMS REGISTER (verification required before republication)

**§15/§16 rule: business facts have one canonical source; no duplicated numbers.** Current duplication map:

| Fact | Occurrences (file:line) | Issue |
|------|--------------------------|-------|
| **2,557** automated tests | `HeroSection.tsx:138`, `home/ProofSection.tsx:13`, `ProofPage.tsx:22,141,296`, `SectorsPage.tsx:59` | **Stale**: actual pytest collection is **2,561 selected / 2,628 total** (2026-09-27). Hard-coded in 3 files, 6 places. |
| **90** agents/configurations | `HeroSection.tsx:134,171`, `home/ProofSection.tsx:12`, `home/AboutBand.tsx`, `WorkforceSection` label | Canonical count — but duplicated as literals, not consumed from registry (§15 example is exactly this). |
| **20** departments / "20 Live" | `HeroSection.tsx:142,171`, `home/ProofSection.tsx:14` | **Verify against internal systems** (registry public JSON claims 20 departments — confirm current). |
| **100% Auditable** | `HeroSection.tsx:146` | **Unqualified absolute** — §12/§17 require qualification or evidence. Verify or rephrase. |
| Five-tier approval | `HeroSection.tsx:171`, `ProofSection.tsx:15`, `ContactSection` step 5 | Consistent; verify tier count against approval matrix. |
| Case studies (`workCaseStudies`, `workPolicy`), sector evidence (UNIMA student management, 3 departments, 5,000 records) | `ProofPage`, `SectorsPage` | Carry honesty labels — **verify evidence status** (proven/pilot/demonstration) against internal records before republication. |
| Metrics pattern | `ProofPage.tsx:22` already models `{value, label, source}` | **KEEP pattern** → promote to a canonical `metrics` registry and point all six call-sites at it. |

**No fabricated testimonials, logos, awards, or partnerships found in the current tree.** ✅

---

## 8. TERMINOLOGY SWEEP

| Legacy term | Result |
|-------------|--------|
| "How We Help" (old route/label) | ✅ absent from `src/` (only unrelated matches outside site code) |
| "Proof & Evidence" | ✅ absent |
| Obsolete routes `/offerings`, `/evidence`, `/industries`, `/why`, `/leadership`, `/careers` | ✅ absent from router |
| "127 / 144 / 152 / 89" agent counts in site copy | ✅ absent from site copy; ❌ `src/ai_company/hr/onboarding.py:6` docstring still says "127 agents" (not site-facing; fix opportunistically) |
| "Why LightSpeed" | ❌ `AboutSection.tsx:175` heading |
| "Book a Briefing" / "Book an Executive Briefing" | ⚠️ nav/footer/modal CTA — **label decided 2026-09-27: "Start a Conversation" (§7); code change pending (roadmap step 10)** |
| Four capabilities "Scale" wording | ✅ absent; `valueCycle` = Strategy, Build, Govern, Research & Policy |
| "AI Company Builder" naming | ✅ consistent |
| Pharos sub-brand | ⚠️ `PharosSection` component name + "Insights from Pharos" band (§5.2) |

---

## 9. DESIGN SYSTEM INVENTORY

| Asset | State | Class |
|-------|-------|-------|
| `src/brand/brand-tokens.css` | `@theme` + `:root` tokens: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, mist `#F7F8F9`, slate `#121518`; Arial scale 36→12pt; 4px spacing grid; motion tokens (slow/medium/fast + `--ease-spatial`) | **KEEP** — matches §20 and brand tokens. |
| `src/index.css` | Calm- Intelligence reset (~161 lines), `dark` variant vars for `#121518`/`#F7F8F9`, `prefers-reduced-motion` guard | **KEEP** (audit ripple/texture classes against §19). |
| `index.html` | title/description/og set; **no favicon link**, no `og:image`, no `theme-color`; `dark:bg-[#070a40]` body class vs §20 `#121518` | **MODIFY** — add favicon/OG assets, align dark body color. |
| Theme system | `App.tsx`: default **dark**, `localStorage['lightspeed_theme']`, html class + inline bg; `FloatingNav` toggle | **KEEP** — §21 both modes first-class + system preference… (currently defaults dark without reading `prefers-color-scheme` — minor MODIFY). |
| `static/brand`, `public/brand` | brand asset mirrors (canonical `brand/**` per AGENTS.md) | **KEEP** (do not hand-edit mirrors). |

---

## 10. DEPENDENCIES (verbatim from `package.json`, 2026-09-27)

| Dep | Version | Status |
|-----|---------|--------|
| react / react-dom | ^18.3.1 | KEEP |
| react-router-dom | ^7.18.3 | KEEP |
| three | ~~^0.186.1 (+ `@types/three`)~~ | **REMOVED 2026-09-27 (Step 1)** — pruned from `package.json`, `bun.lock`, and `node_modules`. |
| lucide-react | ^0.475.0 | KEEP |
| clsx, tailwind-merge | ^2.1.1, ^3.0.1 | KEEP (utility) |
| tailwindcss + @tailwindcss/vite | ^4.0.0 | KEEP |
| vite ^6.1.0, typescript ^5.7.3, vitest ^5.0.0, jsdom ^30.0.1 | dev | KEEP |
| framer-motion, recharts, dotenv | **not present** | Prior inventory marked them; they have already been removed — no action. |

---

## 11. FORMS AND API INTEGRATIONS

| Form | Endpoint | Hardening | Class |
|------|----------|-----------|-------|
| `ContactSection` | `POST /api/enquiry` | Turnstile token, honeypot `hp_website`, idempotency key, HTTP-201 handling, error surfacing | **KEEP** |
| `ExecutiveBriefingModal` | `POST /api/enquiry` (`form: 'briefing'`) | same | **KEEP** |
| `NewsletterSignup` | `POST /api/enquiry` (`enquiryType: 'Newsletter subscription'`) | same | **KEEP** |
| SLA copy | `src/lib/enquiry.ts` — "within two business days" | single source | **KEEP** |

No other network integrations in public site code. Ask LightSpeed is fully client-side (no LLM calls) — complies with §14 by construction; keep it that way unless a public-safe knowledge boundary is formally defined.

---

## 12. TESTS AND TOOLING

| Suite | Scope | Status |
|-------|-------|--------|
| vitest (2 files, 17 tests) | `companyData`, `useScrollProgress` removed with Step 1 | ✅ green — but **zero component/page/IA tests**, no ContentBoundary test, no route-map test (prior audits cited such tests; they are gone — regression risk during rebuild). |
| pytest (~2,561 selected) | Python platform (not website) | ✅ collectable; source of the "tests" proof metric. |
| `npm run lint` | `tsc --noEmit` | ✅ (no eslint/prettier in site gate). |
| `npm run build` | `tsc && vite build` | ✅ with chunk-size warning. |
| Scripts referenced by audits | `scripts/check-site-form-backend.py`, Playwright 390px pass, Appendix A gate | ⚠️ verify existence/wiring during rebuild (not yet re-run this session). |

---

## 13. REPOSITORY-LEVEL LEGACY ARTIFACTS

| Artifact | Finding | Action |
|----------|---------|--------|
| `IMPLEMENTATION_AUDIT.md` | Contradicted (Three.js, test counts, onboarding claim) | **REWRITE** at end of rebuild (directive §5). |
| `LEGACY_INVENTORY.md` / `SPECIFICATION_MAP.md` (2026-09-25) | Superseded by these rewritten documents | done. |
| `Plan.md` (2026-09-16) | Five-item nav mandate conflicts with §7 | Note supersession; do not follow. |
| `src/ai_company/hr/onboarding.py:6` | "127 agents" docstring | MODIFY (non-site; keep at 90). |
| Untracked user files (`audit/`, `openapi.json`, skills dirs, migration directives) | Outside website scope | **DO NOT TOUCH**. |
| `UX_VALIDATION_REPORT.md`, `brand-strategy-validation-report.md` | Pre-rebuild audit reports; findings partly addressed | Reference only. |

---

## 14. VERIFICATION QUEUE — internal-system checks required before publication

1. Test-count metric: pick canonical value (2,561 vs 2,628 vs "2,500+") and source it from a generated metric.
2. Department count: 20 — confirm current registry (`agent-registry.public.json` says 20).
3. "100% Auditable" — qualify or evidence (§12/§17).
4. Case studies `PC-*` / `POL-*` and sector evidence (UNIMA 3 departments / 5,000 records) — evidence status re-confirmation.
5. Five-tier approval matrix — confirm current governance config.
6. Confirm `Reveal` and CSS animations honor `prefers-reduced-motion` (§22) — not yet audited line-by-line.
7. Final nav CTA label — decision per §33 (spec text: "Contact / Start a Conversation").

---

**Status:** Inventory complete against the 2026-09-27 working tree. Updated after Step 1 (Three.js strip) + audit reconciliation — application code has been modified by Step 1; current execution state lives in TARGET_ARCHITECTURE §10.
