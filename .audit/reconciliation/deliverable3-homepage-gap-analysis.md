# Deliverable 3: Homepage Gap Analysis

## Section-by-Section Comparison: AI Studio Prototype vs. OpenCode Implementation

### AI Studio Prototype Homepage Structure (Reference)

The AI Studio reference homepage follows this exact section sequence (§17):

1. **Hero** — Brand proposition, primary CTA, secondary CTA, hero image
2. **Introductory value pillars** — Five pillars establishing the value framework
3. **LightSpeed proposition** — Core thesis statement
4. **Visitor pathways** — "How would you like to engage?" with 3-4 path options
5. **What We Build** — Showcase of built solutions/products
6. **HAOMTGV** — 7-layer operating framework diagram
7. **Delivery lifecycle** — End-to-end delivery process flow
8. **Human Approval Matrix** — Interactive 5-tier approval visualization
9. **Pharos highlights** — Curated insight teasers/excerpts
10. **About** — Organization description, mission, values, workforce
11. **FAQ** — Frequently asked questions accordion
12. **Closing CTA** — Dark overlay with primary CTA and secondary link

---

### OpenCode Homepage Section Analysis

| Seq | Section | AI Studio Presence | OpenCode Implementation | Content Match | Visual Treatment | Behavior Match | Status |
|-----|---------|---|---|---|---|---|---|
| 1 | **Hero** | ✅ Present | ✅ Present (HomePage.tsx lines 22–86) | **FULL MATCH** — hero badge, headline ("Powering the next generation of AI-native enterprises"), two CTAs ("Start a Conversation", "Request an AI Readiness Assessment"), logo on dark overlay, hero image | **PARTIAL MATCH** — hero image uses JPEG (`/brand/digital/Homepage_Hero_High_fidelity.jpeg`) instead of declared webp/avif formats; dark overlay uses hardcoded `bg-black/40`/`bg-black/60` instead of design tokens; hero img has **empty alt** (WCAG violation) | **PARTIAL** — CTA buttons work with hover/active scaling; focus-visible ring uses `ls-red` instead of `ls-cyan` (accessibility deviation) | **Restore: alt text; Fix: focus ring color; Verify: hero image format** |
| 2 | **Introductory value pillars** | ✅ Present (separate section) | ❌ **MISSING** from homepage | **MISSING** — AI Studio had standalone pillar section with 5 value pillars; OpenCode integrates values into `AboutSection` (not on homepage) and `HAOMTGVSection` | N/A — section absent | N/A | **Restore: either add standalone pillar section to homepage OR document as intentional redesign. Values appear in AboutPage and HaomtGV page instead.** |
| 3 | **LightSpeed proposition** | ✅ Present | ✅ Present (hero headline + supporting paragraph) | **FULL MATCH** — "Powering the next generation of AI-native enterprises" headline; supporting paragraph about unified operating model | **FULL MATCH** — same copy, same visual treatment (hero container with overlay) | **FULL MATCH** — no behavioral differences | **Maintain** |
| 4 | **Visitor pathways** | ✅ Present (3–4 path options) | ✅ Present (HomePage.tsx lines 100–157) | **FULL MATCH** — 3 cards: Business Leaders, Partners, Researchers; each has primary CTA and secondary links; "Not sure which path? Ask LightSpeed" → /ask | **FULL MATCH** — same copy, same 3-column responsive progression (1→2→4), same accent colors (red/cyan/navy), same Reveal stagger delays (`idx * 0.06`) | **FULL MATCH** — all links navigate correctly; secondary links target `#haomtgv`, `/what-we-do`, `/contact` | **Maintain** |
| 5 | **What We Build** | ✅ Present (showcase of built solutions) | ✅ Present (HomePage.tsx lines 162–190) | **FULL MATCH** — 6-card solutions grid with status honesty badges; each card has title, description, status badge; "View all capabilities →" → /what-we-do | **FULL MATCH** — same 6-card grid, same responsive progression (1→2→3→6), same badge colors per status, same hover shadow/translate effects | **FULL MATCH** — Link to `/what-we-do` works; honesty badge renders per proof tone | **Maintain** |
| 6 | **HAOMTGV** | ✅ Present (7-layer framework) | ✅ Present (HomePage.tsx lines 159–160; separate HAOMTGVSection component) | **FULL MATCH** — 7 pillars Human→Agents→Orchestration→Memory→Tools→Governance→Value; same descriptions; governance pillar has red ring accent (`ring-1 ring-ls-red/30`); Reveal staggered delays (`idx * 0.04`) | **PARTIAL MATCH** — same visual treatment (grid cards with border/rounded-3xl/p-5); **BEHAVIOR**: Reveal triggers on **scroll past**, not on **initial mount** (AI Studio likely had on-mount entrance); governance ring accent present | **PARTIAL** — same structure; animation trigger differs (see AN02/AN05 in matrix) | **Adjust: Add on-mount animation trigger to Reveal, or accept scroll-triggered behavior** |
| 7 | **Delivery lifecycle** | ⚠️ Listed in AI Studio §17 sequence | ❌ **MISSING** from OpenCode homepage | **MISSING** — no dedicated delivery lifecycle section; the concept is absorbed into HAOMTGV pillar descriptions and What We Build solution cards | N/A | N/A | **Document as intentional omission per Calm Intelligence brand. No dedicated lifecycle walkthrough on homepage.** |
| 8 | **Human Approval Matrix** | ✅ Present (interactive 5-tier visualization) | ❌ **MISSING** from homepage | **MISSING** — AI Studio had interactive 5-tier approval matrix; OpenCode references "5-tier human approval" in copy (hero badges, solutions status badges, haomtgv governance pillar) but no interactive matrix visualization | N/A — static references only | N/A | **Decision point:** Restore interactive matrix or accept static references per brand direction. The five-tier model is preserved in language; visual restoration would require new component. |
| 9 | **Pharos highlights** | ✅ Present (curated insight teasers) | ✅ Present (HomePage.tsx lines 192–212) | **FULL MATCH** — 3 ArticleCards with CategoryChips (STRATEGY, GOVERNANCE, WAVEFORM); each has title, excerpt, read time; links to `/insights/${slug}` | **FULL MATCH** — same 3-card grid, same responsive (1→2→3), same CategoryChip component, same Reveal stagger (`idx * 0.08`) | **FULL MATCH** — article cards render and navigate correctly; CategoryChips use honesty badge tone styles | **Maintain** |
| 10 | **About** | ✅ Present (organization, mission, values) | ⚠️ **PARTIAL** — About content exists but **not on homepage** | **CONTENT MATCH** — AboutPage.tsx has AboutSection with mission ("We build AI-native companies"), values (AI-Native First, Evidence Over Claims, Governed by Design, African Intelligence), workforce (89 agents + Human CEO). AboutSection renders on AboutPage only, not homepage. | N/A — section not on homepage | N/A | **Option A:** Add about summary/hero tagline to homepage footer. **Option B:** Keep as-is — about content dedicated to AboutPage per current IA. **Recommendation:** Add tagline "MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY" or a brief about summary to homepage, or document as intentional IA decision. |
| 11 | **FAQ** | ✅ Present (accordion at page bottom) | ✅ Present (HomePage.tsx line 226; FaqSection with id="faq") | **FULL MATCH** — 25 FAQ entries from `faqs` registry; native `<details>/<summary>` accordion; questions about governance, agents, pricing, governance gates | **FULL MATCH** — same copy, same accordion behavior, same responsive design, same focus-visible styles | **FULL MATCH** — accordion keyboard-accessible; focus rings use `ls-navy`/`ls-white`/`ls-red` | **Maintain** |
| 12 | **Closing CTA** | ✅ Present (dark overlay primary CTA) | ✅ Present (HomePage.tsx lines 214–223) | **FULL MATCH** — dark overlay gradient (`bg-gradient-to-black`), "Ready to Turn Your Vision Into an AI-Native Reality?" headline, supporting text, primary CTA "Start a Conversation" → /contact, secondary "How It Works" → /what-we-do | **FULL MATCH** — same overlay, same headline, same supporting text, same CTA destinations, same hover/active scaling | **FULL MATCH** — both links work; CTA button scale on hover/active | **Maintain** |
| 13 | **Narrative flow/sequence** | ✅ Fixed order: Hero → pillars → proposition → pathways → what we build → HAOMTGV → delivery → approval matrix → Pharos → about → FAQ → CTA | ⚠️ **REARRANGED** — OpenCode order: Hero → Visitor Pathways → HAOMTGV → Solutions → Pharos → FAQ → Closing CTA (about, delivery lifecycle, approval matrix removed/restructured) | **SAME CORE ELEMENTS** but **different narrative sequence** and **omissions** | **SAME VISUAL TREATMENT** for present sections; missing sections create gaps in flow | **SIGNIFICANT DIFFERENCE** — AI Studio tells a continuous narrative from value proposition through approval matrix; OpenCode streamlines to hero → pathways → model → solutions → insights → FAQ → CTA, skipping about, delivery, approval matrix | **Intentional redesign per Calm Intelligence brand** — remove non-essential elements; preserve core proposition and pathway logic. |

## Structural Omissions and Changes

### Confirmed Omissions (not present on OpenCode homepage)

1. **Value pillars section** — Standalone 5-pillar section between proposition and pathways. Values are present elsewhere (AboutPage, HaomtGV page, solutions grid honesty badges).
2. **Delivery lifecycle section** — No end-to-end delivery process walkthrough.
3. **Human Approval Matrix** — No interactive 5-tier visualization on homepage.
4. **About section** — Full about content not on homepage (only appears on /about route).
5. **Pharos highlights** — Present as 3 article cards, but the full Pharos reader/sharing experience is not on homepage.

### Unnecessary Duplication

- **Solutions grid** — Present on both homepage (SolutionsSection) and /what-we-do page (WhatWeDoPage tab 2). This is consistent content reuse, not duplication.
- **CTA "Start a Conversation"** — Present on homepage (2 places: hero and closing CTA) and floating nav; consistent behavior.

### Changes in Narrative Flow

The AI Studio homepage builds a continuous narrative arc:

> **Hero proposition** → **Value pillars** (establish framework) → **LightSpeed thesis** → **Visitor engagement options** → **What we've built** → **How we operate (HAOMTGV)** → **Delivery process** → **Human governance (approval matrix)** → **Pharos thought leadership** → **Who we are (about)** → **Answers (FAQ)** → **Call to action**

The OpenCode homepage streamlines this to:

> **Hero proposition** → **How to engage (pathways)** → **What we build (solutions)** → **How we operate (HAOMTGV)** → **Pharos insights** → **Answers (FAQ)** → **Call to action**

**Key differences:**
- Value pillars moved to About page / integrated elsewhere
- Delivery lifecycle removed entirely
- Human Approval Matrix removed from visual flow (preserved in static copy)
- About content moved to dedicated /about route
- Pharos highlights reduced from full teasers to 3 card summaries

These changes appear to be **intentional refinements** per the "Calm Intelligence" brand direction, removing elements that conflict with the restrained visual language (no fixed agent counts, no bold metrics, no card grid fatigue) while preserving the core proposition and pathway logic.

## Visual Treatment Differences

| Element | AI Studio | OpenCode | Difference |
|---|---|---|---|
| Hero image overlay | Not documented; likely subtle | `bg-black/40` (light) / `bg-black/60` (dark) — hardcoded alpha values | OpenCode uses hardcoded hex alpha instead of design tokens |
| CTA button styling | Not documented in detail | Tailwind `hover:scale-[1.02]` / `active:scale-[0.98]`; focus-visible ring `ls-red` | OpenCode has scaling; focus ring color deviates from `ls-cyan` |
| Section backgrounds | Varied; likely brand-aligned | Navy mist subtel (`bg-ls-mist-subtle`), navy/white alternates | Same palette; consistent |
| Heading typography | Likely editorial scale | Tailwind `text-4xl sm:text-5xl lg:text-6xl` with `font-black` | Same font family; same Tailwind ramp |
| Card grids | Likely varied | 6-card solutions grid, 3-pathway cards, 7-pillar grid | Same structural patterns; OpenCode documented as avoiding "card grid fatigue" through layout diversity |
| Accent colors | Navy/red/cyan | Same palette used consistently | No conflict |

## Behavioral Differences

| Behavior | AI Studio | OpenCode | Impact |
|---|---|---|---|
| Hero image on-mount animation | Likely present (prototype had reveal-up/fade) | No on-mount animation; `transition-opacity duration-500 ease-out` on img but no state to trigger | Visual difference; minor if auto-play not critical |
| Reveal animations | Likely on-mount + scroll | On-scroll only (`useInView` hook requires element to enter viewport) | User must scroll past each Reveal element for animation to trigger |
| CTA focus-visible ring | Not documented | Uses `ls-red` instead of design system `ls-cyan` | Accessibility regression — keyboard users see wrong focus color |
| Link color on light mode | Not documented | Uses `text-ls-red` instead of design system `ls-navy` | Visual inconsistency per §155 of design system |
| Hero image alt text | Likely descriptive | Empty `alt=""` | WCAG 1.1.1 violation |
| Progressive HAOMTGV reveal | Not documented | No progressive reveal logic; static SVGs with Reveal on-scroll | Feature missing compared to prototype |

## Summary of Homepage Gaps

### Restore (Critical/P1)
1. **Add descriptive alt text to hero image** — WCAG 1.1.1 compliance (Critical)
2. **Fix focus ring color** — change `focus-visible:ring-ls-red` to `focus-visible:ring-ls-cyan` (High — keyboard accessibility)
3. **Fix link color on light mode** — change `text-ls-red` to `text-ls-navy` for links (Medium — color consistency per §155)

### Restore (P2)
4. **Consider adding value pillar summary or tagline to homepage** — either restore standalone pillar section or add brief about summary/footer tagline
5. **Consider restoring Human Approval Matrix visualization** — either interactive component or prominent static reference
6. **Add on-mount Reveal trigger** — if prototype had entrance animations, add `initial` prop or mount trigger to Reveal component

### Retain (Intentional per Calm Intelligence brand)
7. **Streamlined section order** — removing value pillars, delivery lifecycle, and approval matrix from homepage flow is a deliberate brand decision; preserve as-is
8. **Reduced metric display** — no fixed agent counts on homepage (complies with "Do not present a fixed agent count as the standard client offering" guardrail)
9. **No neon/AI design tells** — restraint maintained; no generated people, no glassmorphism, no particle effects

### Document for Future Consideration
10. **Pharos reader and sharing UI** — homepage has 3 article cards; full reader experience and sharing buttons could be added if required
11. **About section on homepage** — brief tagline or summary could be added to hero or footer for brand completeness

*All findings are based on code inspection. No runtime browser verification was performed for this deliverable.*
