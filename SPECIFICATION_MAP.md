# Specification-to-Code Map — LightSpeed Holdings

**Date:** 2026-09-27 (rebuilt against current working tree; supersedes the 2026-09-25 map)
**Purpose:** Map every major `MASTER_SPEC.md` requirement → current implementation status → required action. Companion to `LEGACY_INVENTORY.md` (evidence catalogue) per `REBUILD_DIRECTIVE.md` §2.
**Baseline:** commit `52b27136`; verification baseline in `LEGACY_INVENTORY.md` §1 (re-verified post-Step-1 at 18:21: tsc ✅ 0 / vitest ✅ 17/17 / build ✅ / pytest 2,566 passed).

**Status legend:** ✅ COMPLIANT · 🟡 PARTIAL · ❌ NOT COMPLIANT · ⭕ NOT IMPLEMENTED · 🅰️ DECISION REQUIRED
**Action legend:** KEEP · MODIFY · REBUILD · REMOVE · ADD

---

## 1. STRATEGY AND IDENTITY

### §1 Purpose / §2 Brand Position

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| LightSpeed Holdings Limited, AI-native operator & partner | `index.html` title/meta; `company` in `siteContent.ts`; footer | ✅ | KEEP |
| Brand line ASPIRE. ACT. ACHIEVE. | `company.tagline` (siteContent) | ✅ | KEEP |
| Positioning: AI-native company **builder** and operating platform | Hero + Thesis sections; hero line "builds and operates agentic AI systems from Malawi" | ✅ | KEEP |
| Geographic ambition Malawi → SADC → Africa | Hero line + meta description; footer | ✅ | KEEP |

### §3 Core Operating Model

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Four capabilities Strategy → Build → Govern → **Research & Policy** | `siteContent.valueCycle` (fixed; previously "Scale") consumed by `ThesisSection` | ✅ | KEEP |
| Connected system, not four unrelated categories | ThesisSection renders valueCycle as a cycle | ✅ | KEEP |
| Capabilities coherent everywhere (§32) | `ContactSection` 5-step micro-copy uses Strategy/Build/Govern vocabulary | ✅ | KEEP |

### §4 AI Company Builder / §5 90-agent model / §6 Human + AI

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Journey Opportunity → Design → Build → Deploy → Govern → Measure | `AiCompanyBuilderSection` + home `BuilderSection` stages | 🟡 | Audit stage labels vs §4 wording; MODIFY copy if divergent |
| 90-agent canonical count, consistent | Hard-coded in Hero (×2), ProofSection, AboutBand, Workforce label — not registry-driven | 🟡 | REBUILD → single canonical source (`LEGACY_INVENTORY` §7) |
| Human governance visible (sign-off, 5-tier gates) | Home ProofSection "5-Tier", WhatWeDo human sign-off copy, hero "five-tier human approval" | ✅ | KEEP |
| AI shown as operating capability, not leadership replacement (§29) | AboutBand "One Human CEO. 90 AI Agents."; WhatWeDo sign-off statement | ✅ | KEEP |

---

## 2. INFORMATION ARCHITECTURE AND HOMEPAGE

### §7 Public IA (9 sections)

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| 9 top-level sections: Home, What We Do, AI Company Builder, Solutions, Sectors, Proof, Insights, About, Contact | Router (`App.tsx`) + `FloatingNav` 9 links + footer columns — all 12 routes resolve | ✅ | KEEP |
| Contact / "Start a Conversation" CTA | Nav CTA "Book a Briefing" (+ mobile "Book an Executive Briefing"); footer "Book a Briefing" | 🟡 | MODIFY — confirm final label per §33 |
| Obsolete routes gone | No `/offerings`, `/evidence`, `/industries`, `/why`, `/leadership`, `/careers`; `*` → `/` | ✅ | KEEP |
| `/ask` (§14) extra route | Present, client-side wizard | ✅ | KEEP |

### §8 Homepage narrative sequence (10 beats)

| Beat | Current chapter | Status | Action |
|---|---|---|---|
| 1 Orientation (who/what/who for/why AI-native) | `HeroSection` | ✅ | KEEP |
| 2 Core proposition | `ThesisSection` | ✅ | KEEP |
| 3 Operating model cycle | `ThesisSection` (valueCycle) | ✅ | KEEP |
| 4 Builder journey | `BuilderSection` | ✅ | KEEP |
| 5 90-agent workforce | `WorkforceSection` | 🟡 | MODIFY (registry-driven copy) |
| 6 **Solutions** | *missing as distinct beat* (Builder doubles as "…and solutions") | ❌ | REBUILD — add Solutions chapter between 5 and 7 |
| 7 Sectors | `SectorsSection` | ✅ | KEEP |
| 8 Proof | `ProofSection` | 🟡 | MODIFY (metrics §16) |
| 9 Insights | `InsightsSection` (`insightTeasers`) | ✅ | KEEP |
| 10 CTA | `BriefingSection` | ✅ | KEEP |
| Chapter navigation | `ChapterRail` + scroll progress | ✅ | KEEP |

### §9 Progressive disclosure (6 layers)

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Layer 1 Executive → Layer 6 Technical, stoppable at any layer | Home beats (1–2) → WhatWeDo/Solutions (3) → Builder (3–4) → Proof (5) → Ask/docs (6); `RelatedLinks` cross-links | 🟡 | MODIFY — verify Layer 4 (architecture) exists as its own stop; document layer map in content model |

---

## 3. CONTENT AREAS

### §10 Solutions

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Problem/outcome framing, 5 questions per solution, no generic consulting language | `solutions` in siteContent; `SolutionsPage` + `WhatWeDoPage` + `BuilderSection` consume it | ✅ | KEEP (verify each card answers the 5 questions — content review) |
| Honesty labels where evidence lacking | `HonestyBadge` + `TONE_STYLES` | ✅ | KEEP |

### §11 Sectors

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Useful sector pages, evidence-only claims, four-tier distinction | `SectorsPage` with PROVEN/CURRENT/DEMO/FUTURE tiers | 🟡 | MODIFY — move `SECTORS` to governed registry; fix stale "2,557" (§16) |

### §12 Proof

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| No manufactured testimonials/logos/awards/outcomes | None found in tree | ✅ | KEEP |
| Evidence types with labels where unavailable | `ProofPage` uses workCaseStudies/workPolicy + honesty tiers; evidence `source:` field pattern | 🟡 | MODIFY — verify evidence status (inventory §7 queue), qualify absolutes |
| Unqualified absolutes prohibited | "100% Auditable" (Hero) | ❌ | MODIFY — qualify or evidence |

### §13 Insights

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Categories list (12) | `INSIGHT_CATEGORIES` matches spec exactly | ✅ | KEEP |
| Short posts + deeper articles/reports | **No article content or article route**; insights = teaser cards + `PharosSection` band + newsletter | ⭕ | ADD — content model + article rendering (or approved scope decision) |
| Coherent experience | `PharosSection` parallel visual identity | ❌ | REBUILD — fold into Calm Intelligence system |

### §14 Ask LightSpeed

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Public-safe knowledge boundary; no secrets/prompts/internal info | Fully client-side scripted wizard; copy + `solutions` data only | ✅ | KEEP (maintain client-side-only posture) |
| Distinguish public vs internal knowledge | Not implemented (no internal layer exists to expose) | ✅ | KEEP by construction |

---

## 4. DATA, METRICS, GOVERNANCE

### §15 Data and content architecture

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Structured registries for services/solutions/sectors/case studies/insights/metrics/agents/leadership/FAQs/CTAs | Partial: `siteContent.ts` (solutions, case studies, teasers, FAQ array), `useCaseCatalogData`, `agent-registry.public.json` | 🟡 | REBUILD — consolidate into typed registries; metrics + leadership + sectors registries missing |
| Canonical facts consumed, not duplicated | Agent count/test count duplicated as literals in 6 places; leadership `export` unimported; `companyData.ts` consumed only by its test | ❌ | REBUILD — wire views to canonical sources; delete dead exports (7 found) or use them |
| Same number once | 2,557 in 3 files × 6 call-sites | ❌ | REBUILD — see §16 |

### §16 Dynamic metrics

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Metrics as governed data, propagate from canonical source | Hard-coded in `HeroSection`, `ProofSection`, `ProofPage`, `SectorsPage` | ❌ | ADD — canonical `metrics` registry + generate from verified sources |
| No duplicated numbers | 6 call-sites (inventory §7) | ❌ | REBUILD |
| Never animated counters to look authoritative | No count-up animations found on stats | ✅ | KEEP |
| Correct current values | 2,557 vs actual 2,561/2,628 | ❌ | MODIFY — verify + propagate (verification queue #1) |

### §17 Content governance

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Claim source/owner; states Draft→Published | `ProofPage` `source:` field only; no state model | 🟡 | ADD — content-state metadata in registries |
| Claims on clients/finance/outcomes need evidence | Honesty labels cover most; "100% Auditable" unqualified; case studies need re-verification | 🟡 | MODIFY (verification queue #3–4) |

---

## 5. DESIGN, MOTION, RESPONSIVE, A11Y, PERFORMANCE

### §18 Design language: Calm Intelligence

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Calm, premium, spacious, technically sophisticated; not loud/cyberpunk/generic-SaaS | `index.css` Calm-Intelligence system; `site/` primitives; soft borders/radius on panels | ✅ | KEEP |
| Typography Arial scale | `brand-tokens.css` Arial tokens; `font-display/body/caption` used | ✅ | KEEP |

### §19 Visual world / §20 Color system / §21 Modes

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Natural/architectural metaphors, no neon/glassmorphism-everywhere | Stone/mist/scrim motifs in home sections; textures confined (mostly) | 🟡 | MODIFY — audit `pharos-stone-masonry` + texture layers (§31 cleanup vs approved design) |
| Light `#F7F8F9`, dark `#121518`, brand navy/red/cyan accents | `brand-tokens.css` exact values; index.css dark vars `#121518` | ✅ | KEEP |
| — | `index.html` body `dark:bg-[#070a40]` (navy) conflicts with `#121518` | ❌ | MODIFY — align to `#121518` |
| Both modes first-class, tuned independently; respect system preference + control | Explicit toggle ✅, per-mode classes throughout; **defaults dark without `prefers-color-scheme`** | 🟡 | MODIFY — read system preference on first visit |

### §22 Motion

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Slow/fluid/restrained; "Slow to the eye. Fast to the mind." | CSS transitions (`--transition-*`), `Reveal` scroll reveals, ChapterRail progress | ✅ | KEEP |
| `prefers-reduced-motion` respected; complete experience without decorative animation | `index.css` guard (reduced-motion block); Three.js/`useScrollProgress` paths removed with Step 1 — static §19 fallback needs no motion | 🟡 | MODIFY — line-by-line audit of `Reveal`/CSS keyframes (verification queue #6) |
| Do not animate every element | Sections reveal on scroll only | ✅ | KEEP |

### §23 Responsive

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Desktop/laptop/tablet/mobile; reconsider nav/density/grids/typography per breakpoint | Mobile hamburger menu in `FloatingNav`; grids collapse (`grid-cols-2 lg:grid-cols-4`, etc.) | 🟡 | MODIFY — verify 390px pass (Plan.md verification standard) across all 12 routes; not yet run this session |

### §24 Accessibility

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Semantic HTML, keyboard, visible focus, contrast, labels, alt, forms, reduced motion, headings | `aria-labelledby`/`aria-label` patterns, `aria-hidden` on decorative layers, labelled form fields, `HonestyBadge` text | 🟡 | MODIFY — no automated a11y suite (no axe/Playwright a11y tests); heading-hierarchy + focus-order audit pending |
| Form accessibility | Labels/for + error surfacing in Contact/Briefing/Newsletter | 🟡 | MODIFY — verify error `aria-live` announcements |

### §25 Performance

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Fast despite sophisticated visuals; lazy loading; minimal JS | Route-level code split via router; Three.js removed with Step 1 — single 428 kB JS bundle, no separate three chunk | ✅ | KEEP — no chunk >500 kB warning remains |
| Heavy tech only where materially improving | Three.js removed with Step 1 (user decision: STRIP, 2026-09-27) — §25 caution now satisfied; §19 static fallback | ✅ | DECIDED 2026-09-27: STRIP — see ADR-037 (supersedes ADR-036) |

### §26 Technical architecture

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Modular components, typed interfaces, centralized tokens, predictable routing, testable logic | `site/`+`home/` primitives, TS everywhere, `brand-tokens.css`, declarative router, 17 unit tests (2 files, post-Step 1) | ✅ | KEEP |
| Avoid giant pages, duplicated constants, abandoned code, legacy compat layers | Duplicated metrics (§16); `companyData.ts` unused; 7 dead exports; `PharosSection` parallel system | ❌ | REBUILD — cleanup pass |

---

## 6. BOUNDARIES, REGISTRY, CONTROL

### §27 Public vs internal boundary

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Only Public info in public experience; no internal architecture exposed | Public site ships no internal prompts/endpoints; Ask LightSpeed client-side; agent data via `agent-registry.public.json` | ✅ | KEEP — re-verify after each content change |

### §28 Agent registry

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Governed registry with approved fields only; no prompts/credentials/endpoints | `src/data/generated/agent-registry.public.json` (generated, 133 kB) | ✅ | KEEP |
| Registry actually drives public views | Only imported by `companyData.ts` (itself unused) | ❌ | REBUILD — render workforce/agent views from registry |

### §29 Executive / human control

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Decision rights understandable; human sign-off visible | "One Human CEO. 90 AI Agents.", sign-off statements, 5-tier gates, "Submit Confidential Request" flow | ✅ | KEEP |

### §30 Architecture documentation

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| ADRs, diagrams, content-model + boundary + deployment + registry docs | `docs/architecture/adr/` (001-037); Three.js decision recorded as **ADR-037** (supersedes ADR-036); this map + inventory provide content-model/boundary docs | 🟡 | MODIFY — add content-model doc when registries are consolidated |

---

## 7. MIGRATION AND ACCEPTANCE

### §31 Migration principle

| Requirement | Current implementation | Status | Action |
|---|---|---|---|
| Prioritize IA → content model → brand → components → boundary → perf → a11y → cleanup; don't preserve legacy code | IA ✅ done; content model/brand mostly done; cleanup outstanding (Pharos, dead exports, `companyData`, duplicated metrics) | 🟡 | REBUILD — remaining cleanup items are the active backlog |

### §32 Acceptance criteria checklist

| Criterion | Status | Evidence / gap |
|---|---|---|
| IA matches specification | ✅ | 9 routes + legal + ask, nav matches §7 |
| Legacy structure removed where incompatible | 🟡 | Obsolete routes gone; Pharos band, dead exports, hard-coded metrics remain |
| Positions as AI-native company builder | ✅ | Hero/Thesis/meta |
| Four capabilities coherent | ✅ | valueCycle |
| 90-agent model represented consistently | 🟡 | Consistent number, but duplicated literals not registry-driven |
| Human governance clear | ✅ | §29 evidence |
| Public/internal boundary enforced | ✅ | §27/§28 evidence |
| Progressive disclosure used | 🟡 | Layer 4 (architecture) stop not explicit |
| Light + dark both intentional | 🟡 | System-preference default + `index.html` bg mismatch |
| Calm Intelligence visible | ✅ | tokens + CSS |
| Accessibility implemented | 🟡 | Partial; no automated gate |
| Performance protected | 🟡 | Lazy three.js; chunk warning open |
| Claims evidence-based | 🟡 | Honesty system good; "100% Auditable" + stale 2,557 to fix |
| Content structured and governed | 🟡 | Registries partial; no state model |
| Responsive | 🟡 | Designed for it; 390px verification not run this session |
| No unnecessary legacy architecture | 🟡 | Cleanup backlog above |

### §33 Source-of-truth rule

Enforced: MASTER_SPEC > brand tokens > approved decisions > tech constraints > existing code. Conflicts noted: `Plan.md` five-item nav (superseded), prior audit "no Three.js" (contradicted), Three.js retention (**decided 2026-09-27: STRIP** — user override; see TARGET_ARCHITECTURE §1).

---

## 8. ACTION BACKLOG (ordered for the rebuild)

| # | Action | Spec refs | Inventory ref |
|---|---|---|---|
| 1 | ~~Decide Three.js retain-vs-remove~~ **DECIDED 2026-09-27: STRIP** (user override) — Step 1 executed; ADR still to be written per §31 | §25, §31, §33 | §5.2, §10 |
| 2 | Canonical `metrics` registry; fix 2,557 → verified value; remove 6 duplicated call-sites | §15, §16 | §7 |
| 3 | Qualify "100% Auditable"; re-verify case-study/sector evidence | §12, §17 | §7, §14 |
| 4 | Add homepage Solutions beat (§8 #6) | §8 | §4 |
| 5 | Registry-drive 90-agent/workforce copy; render agent views from `agent-registry.public.json`; drop `companyData.ts` or rewire | §5, §15, §28 | §6 |
| 6 | Trim/rebuild: 7 dead siteContent exports, `PharosSection` → Calm Intelligence, AboutSection "Why LightSpeed" heading | §26, §31 | §5.2, §6, §8 |
| 7 | Insights: article content model + route (or approved scope note) | §13 | §2 |
| 8 | `index.html`: favicon, og:image, theme-color, dark bg `#121518`; system-preference theme default | §20, §21, SEO | §9 |
| 9 | ~~Confirm nav CTA label~~ **DECIDED 2026-09-27: "Start a Conversation"** (spec-faithful §7) — code change pending in FloatingNav | §7, §33 | §3 |
| 10 | a11y + 390px responsive verification pass (Playwright/axe); reduced-motion audit | §23, §24, §22 | §12, §14 |
| 11 | Re-add IA/regression tests (route map, content boundary) lost since prior audits | §26, §32 | §12 |
| 12 | Fix `onboarding.py` "127 agents" docstring; rewrite `IMPLEMENTATION_AUDIT.md` at close | §5, directive §5 | §13 |

---

**Status:** Specification map complete against the 2026-09-27 working tree. Updated after Step 1 (Three.js strip) + audit reconciliation; application code modified by Step 1 — see TARGET_ARCHITECTURE §10 roadmap for execution state.
