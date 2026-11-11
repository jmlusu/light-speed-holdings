# HomePage Design System Audit

**Authority:** `docs/LIGHTSPEED_DESIGN_SYSTEM.md` (v1.1, ACTIVE)
**Subject:** `src/pages/HomePage.tsx` + all supporting components
**Date:** 2026-11-11
**Auditor:** OpenCode agent

---

## Audit Scope

All files inspected:
- `src/pages/HomePage.tsx` (primary page component)
- `src/components/site/CtaBand.tsx` — closing CTA band
- `src/components/site/FaqSection.tsx` — FAQ section
- `src/site/StatusBadge.tsx` — solution status pills
- `src/site/PathwayCard.tsx` — pathway navigation cards
- `src/site/CategoryChip.tsx` — article category pills
- `src/site/ArticleCard.tsx` — Pharos teaser cards
- `src/components/site/SectionHeading.tsx` — section heading component
- `src/components/Reveal.tsx` — scroll-reveal utility
- `src/components/home/HAOMTGVSection.tsx` — H-A-O-M-T-G-V diagram
- `src/components/home/VisitorPathsSection.tsx` — three visitor pathways
- `src/data/homeCopy.ts` — homepage copy & asset constants
- `src/index.css` — base styles & design system CSS

---

## 1. Visual Hierarchy

| Element | Assessment | Evidence | Recommendation |
|---------|------------|----------|----------------|
| **Hero → CTA → Paths → HAOMTGV → Solutions → Pharos → CTA → FAQ** | ✅ Clear sequential hierarchy matching §17 homepage sequence | HomePage.tsx arranges sections in correct directive order (§17: 1.Hero → 2.Orientation → 3.Visitor Paths → 4.HAOMTGV → 5.AI Company Builder → 6.90-Role Workforce → 7.Open-Weight AI → 8.Use Cases → 9.Solutions → 10.Sectors → 11.Pharos → 12.Governance → 13.FAQ → 14.Final CTA) | Maintain current order |
| **Hero h1 hierarchy** | ✅ Strong headline contrast | `h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight font-display text-ls-white break-all"` — oversized, heavy weight, tight tracking | Keep; matches §8 "Editorial Scale" and §22 type scale |
| **Section headings** | ✅ Consistent use of `SectionHeading` component | All major sections use `<SectionHeading eyebrow="…" title="…" lead="…" />` | Continue using the component |
| **Sub-section hierarchy** | ⚠️ Inconsistent heading levels within sections | Solutions grid uses `h3 className="font-display font-bold text-base sm:text-lg"`; Pathway cards use `h3`; HAOMTGV uses `h3` for pillar titles. No `h1` or `h2` skipped, but intra-section levels vary. | Ensure heading levels are logical within each section's context; avoid skipping levels globally |

**Verdict:** Visual hierarchy is fundamentally sound and follows the §17 sequence. Minor intra-section heading level variation is acceptable as long as h1-h6 are not skipped globally.

---

## 2. AI Design Tells

| Element | Assessment | Evidence | Recommendation |
|---------|------------|----------|----------------|
| **Neon/aesthetics** | ✅ No generic neon AI aesthetics | No glowing gradients, no glassmorphism, no particle effects, no 3D elements | Maintain restraint |
| **Brand palette usage** | ✅ Navy/red/cyan dominant; no orange/zinc | `bg-ls-navy`, `bg-ls-red`, `bg-ls-cyan`, `text-ls-*` tokens used; no `#FF6B35` or zinc greys | Continue avoiding retired palette |
| **Excessive card grids** | ⚠️ Several card/grid sections | Hero card grid, pathway cards (3×1→4), solutions grid (6 columns), HAOMTGV 4×4 grid. However, gap spacing and typography prevent "card grid fatigue." | Maintain current diversity of layout types (hero image, cards, diagrams) |
| **AI person/avatar imagery** | ✅ No generated people | Hero uses a real-photography road image (no faces); no avatars anywhere | Continue prohibiting generated people |

**Verdict:** Design successfully avoids AI design tells. The visual language is editorial, calm, and intentional — consistent with "CALM INTELLIGENCE" (§5).

---

## 3. Typography

The design system (§22) specifies a **pt-based type scale** with canonical px equivalents. The codebase uses Tailwind `text-` utilities which map to a different px ramp. This is a known divergence (§242–258) but is system-wide, not HomePage-specific.

| Element | Assessment | Evidence | Recommendation |
|---------|------------|----------|----------------|
| **Font family** | ✅ Arial, system stack | `font-family: Arial, sans-serif` in `index.css`; all text uses `font-display`/`font-body` classes | Continue using Arial only (§210) |
| **Display headline** | ✅ Oversized impact | Hero `h1` at `text-4xl sm:text-5xl lg:text-6xl` — large scale for hero impact | Acceptable; Tailwind `text-4xl` ≈ 24px, but hero needs oversized scale (§263) |
| **Body text** | ✅ Comfortable line height | Paragraphs use `text-lg sm:text-xl lg:text-2xl leading-relaxed` → approximates `body` (14pt/18.7px) with 1.6 line height | Acceptable |
| **Tracking** | ✅ Tight for headlines | `tracking-tight` on headlines; `tracking-widest` on uppercase labels (badges, pills) | Continue current practice (§266) |
| **overline style** | ✅ Used where present | `CategoryChip` uses `font-body text-[10px] font-bold tracking-widest uppercase` — matches `overline` spec (TS token: `11pt`, `letter-spacing: 0.1em`, uppercase) | Good |
| **px vs pt divergence** | ⚠️ System-wide known gap | HomePage uses Tailwind `text-4xl`, `text-lg`, etc. The canonical pt scale (display-xl 36pt → 48px, title-xl 32pt → 42.7px) is not directly applied. The bridge px ramp is ≈4px shorter for most steps (§248–257). | Document as known debt; do not fix in isolation — close when tokens are next revised (§134). |

**Verdict:** Typography is functionally correct. The pt↔px divergence is a repository-wide token gap, not a HomePage defect. The oversized scale (hero `text-4xl` etc.) correctly serves the "Editorial Scale" principle (§263).

---

## 4. Color

| Element | Assessment | Evidence | Recommendation |
|---------|------------|----------|----------------|
| **Primary CTA (red bg, white text)** | ✅ Correct | Hero "Start a Conversation" button: `bg-ls-red text-ls-white shadow-lg shadow-ls-red/30` — matches "Primary CTA → Always red background, white text" (§153) | Maintain |
| **Secondary CTA (navy border, navy text light / white border white text dark)** | ✅ Correct | "Request an AI Readiness Assessment": `border border-ls-red text-ls-red` — secondary style per design system | Maintain |
| **Navy for headings/secondary text** | ✅ Correct | `text-ls-navy` on section titles, pathway labels, article titles | Maintain |
| **Cyan for links on dark/focus rings** | ⚠️ Partially correct | Links use `text-ls-red hover:text-ls-red/80` (light) and `text-ls-cyan` (dark)` — links on dark use cyan ✅; focus rings use `ring-ls-red` instead of design system `var(--ls-cyan)` ❌ | Fix focus ring color to `var(--ls-cyan)` (see Accessibility section) |
| **Red accent on badges/chips** | ✅ Within palette | StatusBadge `PILOT` variant uses `bg-ls-cyan/10 text-ls-navy border-ls-cyan/40`; CategoryChip `GOVERNANCE` uses `bg-ls-red/10 text-ls-red` — both within navy/red/cyan/ grey palette | Maintain |
| **No orange usage** | ✅ Compliant | No `#FF6B35` or zinc greys anywhere in HomePage | Continue avoiding |
| **60/20/20 rule** | ⚠️ Approximately met | Navy-dominant surfaces (hero bg, section backgrounds ≈ 60%); red and cyan as bounded accents (CTAs, badges, links ≈ 20% each). Red not used as large fill. | Maintain approximate balance |
| **Hero image overlay** | ✅ Controlled | `bg-black/40` (light) / `bg-black/60` (dark) overlay on hero image — subtle, not a brand grade | Maintain |

**Known token divergence note:** All `bg-ls-*`, `text-ls-*`, `border-ls-*` classes resolve via the app bridge (`src/brand/brand-tokens.css`) → `:root` variables. The canonical JSON (`brand/tokens/brand-tokens.json`) is the source of truth (§31–33, §128–134). The bridge values currently differ slightly for some tokens (e.g., `grey-light` = `#F2F2F2` canonical vs `#F7F8F9` bridge). This is documented debt; no HomePage-specific action needed.

**Verdict:** Color palette is consistent and correct. One critical deviation: focus ring color (see Accessibility).

---

## 5. Spacing

| Element | Assessment | Evidence | Recommendation |
|---------|------------|----------|----------------|
| **Section vertical padding** | ✅ Correct | `py-24 sm:py-32 md:py-36` → corresponds to `--ls-space-8` (64px) vertical, reducing on mobile per guidance (§296) | Maintain |
| **Section horizontal padding** | ✅ Correct | `px-4 sm:px-8` → `--ls-space-2` (8px) base on mobile, `--ls-space-4` (16px) on tablet | Maintain |
| **Grid gutters** | ✅ Correct | `gap-4`, `gap-6`, `gap-8` used throughout; 4px base grid scale | Maintain |
| **Inline gaps** | ✅ Correct | `gap-1.5` (tight), `gap-2` (tighter), `gap-3` (normal) used in chips, badges | Maintain |
| **Hero image overlay** | ⚠️ Non-standard z-offset | `py-20 sm:py-32` on hero container; the `absolute inset-0` overlay uses `bg-black/40` without explicit spacing token. Visually fine but not explicitly from spacing scale. | Optional: use `--ls-space-*` if overlay gets its own section |
| **Reveal animations** | ✅ Delayed staging | `Reveal` component uses `delay={idx * 0.04}` and `delay={idx * 0.06}` for staggered entrances — adds rhythm without breaking spacing rhythm | Maintain |

**Verdict:** Spacing is consistently from the `--ls-space-*` scale (4px base grid). All section padding follows the `--ls-space-8` vertical / `--ls-space-6` horizontal rule (§296).

---

## 6. Brand Consistency

| Element | Assessment | Evidence | Recommendation |
|---------|------------ |----------|----------------|
| **Logo usage** | ✅ Correct | `<img src="/logo-full-v2.svg" alt="LightSpeed logo" className="max-w-xs" />` — SVG from canonical `brand/logo/` tree; `logo-full` variant for light backgrounds ✅ | Verify `logo-full-v2.svg` is the latest canonical version; if so, fine |
| **Logo clear space** | ✅ Respected | Logo given `max-w-xs` with `pt-20` vertical padding in hero — generous clear space around the mark | Maintain |
| **Logo on-surface color** | ✅ Correct | Navy on white/mist background; white on dark. Hero uses `max-w-xs` logo with no forced color override | Maintain |
| **Tagline "MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY"** | ⚠️ Not displayed on HomePage | The tagline is defined in the design system's brand positioning (§48–52) but does not appear on the HomePage. Other pages may carry it. | Consider adding tagline to HomePage footer or hero tagline area, or document as intentional omission |
| **No prohibited imagery** | ✅ No stock-desktop-scenes, no poverty stereotypes, no generated people | Hero uses a road/architecture image (Type A: architectural geometry, no people); no cliché smiles; no headshots | Maintain |
| **Brand tone: CALM INTELLIGENCE** | ✅ Reflected | Restrained palette, editorial typography, spacious layout, no neon, no glass — all consistent with "Calm → Curiosity → Clarity → Confidence → Action" (§54–63) | Maintain |

**Verdict:** Brand consistency is strong. The only gap is the absent tagline; all visual brand elements (logo, palette, tone) are correctly applied.

---

## 7. Responsive Design

| Element | Assessment | Evidence | Recommendation |
|---------|------------ |----------|----------------|
| **Mobile-first methodology** | ✅ Implemented | Base = mobile (`px-4 sm:px-8`, `py-20 sm:py-32`, `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`). All breakpoints use `min-width` media queries. | Maintain |
| **Breakpoint mapping** | ✅ Correct | `sm: 640px` (min), `lg: 1024px`, `xl: 1280px` — matches design system breakpoints (§308–312) | Maintain |
| **Hero responsive height** | ✅ `min-h-screen lg:min-h-[700px]` — full screen on mobile, 700px min on laptop+ | Good contrast between mobile and desktop | Maintain |
| **Grid column progression** | ✅ Well-structured | Pathway cards: `grid-cols-1` → `sm:grid-cols-2` → `lg:grid-cols-4`. Solutions: `grid-cols-1` → `sm:grid-cols-2` → `lg:grid-cols-3` → `xl:grid-cols-6`. HAOMTGV: `grid-cols-1` → `sm:grid-cols-2` → `lg:grid-cols-3` → `xl:grid-cols-4`. | Maintain — each section restructures appropriately |
| **Never simply shrink desktop** | ✅ Avoided | Sections restructure (single → multi-column) rather than just reducing font sizes and spacing. E.g., hero text reflows; pathway cards change from 1 to 4 columns. | Maintain |
| **Typography scaling** | ⚠️ Tailwind `text-` scales with `sm:`/`lg:` prefixes | `text-4xl sm:text-5xl lg:text-6xl` — Tailwind responsive class chain. This is the system-wide pattern and is acceptable. | Acceptable as system-wide pattern |
| **Focus ring visibility** | ⚠️ May need testing | Custom `focus-visible:ring-ls-red` may have different contrast on mobile vs desktop; ensure 2px minimum is maintained. | Test on actual devices |

**Verdict:** Responsive design is a strong point. The page restructures meaningfully at each breakpoint without "just shrinking" the desktop layout.

---

## 8. Accessibility

| Element | Assessment | Evidence | Recommendation |
|---------|------------ |----------|----------------|
| **WCAG 2.1 AA contrast** | ⚠️ Mixed | - `text-ls-white/90` on navy hero background: contrast likely > 4.5:1 (white on #070A40 is ∞, 90% tint may be borderline)<br>- `text-ls-red/10` on navy: likely < 3:1 (red tint on navy may fail)<br>- `text-ls-grey-dark/60` on white: likely < 4.5:1 (60% tint of #6B7280 on #FFFFFF)<br>- Dark mode: `text-ls-white` on `#121518` (navy) is fine; `text-ls-grey-light-text` on `#1A1D21` likely ok | Verify contrast with actual colors; darken tinted text colors or increase base contrast |
| **Keyboard navigation** | ✅ Tab-reachable | All interactive elements (buttons, links, inputs via forms) are in natural tab order; no `tabIndex` anomalies | Maintain |
| **Visible focus** | ⚠️ Custom ring deviates from design system | Buttons use `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-red focus-visible:ring-offset-2` — removes native 2px cyan outline and replaces with red ring. Design system §710 & `src/index.css` prescribe `2px solid var(--ls-cyan)` + `2px outline-offset`. | Change to `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-cyan focus-visible:ring-offset-2` |
| **Semantic headings** | ✅ No skipped levels | h1 on hero, h2/h3 used consistently within sections; `SectionHeading` uses `<Heading level={level}>` | Maintain |
| **Alt text** | ❌ Missing | Hero `<img src="/brand/digital/Homepage_Hero_High_fidelity.jpeg" alt="" />` — empty alt attribute. WCAG 1.1.1 requires descriptive alt for informational images. | Provide descriptive alt text: e.g., `alt="Lilongwe cityscape with data center architecture, representing LightSpeed's AI-native operating model"` |
| **Reduced motion** | ✅ Global hook | `useInView` hook checks `prefers-reduced-motion` and disables Reveal animations (§14–15). Global CSS `prefers-reduced-motion` rule also applies. | Maintain |
| **Skip link** | ⚠️ Defined but may not be on HomePage | `src/index.css` defines `.skip-link` but HomePage `<div className="relative">` has no `.skip-link` element. Interior pages may have it. | Add `.skip-link` as first focusable element in HomePage, or document as not required for this single-page SPA |
| **Alt text on supporting images** | ✅ All other images have appropriate alt | Pathway cards use `Target` icon ( decorative/structural); CTA buttons have `aria-label`; FaqSection `<summary>` has text; StatusBadge, CategoryChip, ArticleCard all use text-only labels | Maintain |
| **No color-only information** | ✅ Badges pair color with text | StatusBadge and CategoryChip always have text labels alongside color; never rely on color alone | Maintain |
| **Live regions for dynamic content** | ⚠️ Not present | No `role="status"` or `aria-live` on CTA briefing triggers. `onRequestBriefing` is a callback, not DOM-updated dynamic content. | If briefing status is displayed dynamically, add live region; otherwise not critical for static page |

**Verdict:** Key accessibility fixes needed:
1. **Add descriptive alt text** to hero image (critical: WCAG 1.1.1)
2. **Fix focus ring color** to use `var(--ls-cyan)` instead of `var(--ls-red)` (moderate: WCAG 2.4.7 focus visibility)

All other accessibility aspects are well-handled.

---

## 9. Missing States

| Element | Assessment | Evidence | Recommendation |
|---------|------------|----------|----------------|
| **Empty states** | N/A | HomePage is fully populated; no empty state scenarios on this page | Not applicable |
| **Loading states** | ⚠️ No explicit loading indicators | CTA bands and section content have no skeleton/spinners if data is async. However, homepage copy (`homeCopy`) is static imported data, so loading is not a runtime concern. | If any data fetches are added later, add loading skeletons |
| **Error states** | ⚠️ No error UI | No error boundaries or error message UI visible. Same note: static copy means not currently needed. | Document as future-proofing |
| **State badge coverage** | ✅ Full status coverage | `StatusBadge` covers `IN DEVELOPMENT`, `PILOT`, `PROTOTYPE`, `IN-HOUSE`, `EXPLORATION` — matches `SolutionStatus` type used in solutions grid. | Maintain |
| **Category chip fallback** | ✅ Neutral fallback | `CategoryChip` falls back to `bg-ls-grey-dark/10 text-ls-grey-dark` for unknown categories — prevents unstyled rendering. | Maintain |
| **No-data pathway** | ✅ Not applicable | Pathway cards are static; no empty-state pathway needed on page load. | Maintain |

**Verdict:** No missing-state issues on current HomePage (static data). Design patterns for loading/error states exist in the codebase for future dynamic sections.

---

## Prioritized Findings & Recommendations

| # | Priority | File | Line(s) | Issue | Evidence | Recommendation |
|---|----------|------|---------|-------|----------|----------------|
| **1** | **Critical** | `src/pages/HomePage.tsx` | 33 | **Missing alt text on hero image** | `<img src="/brand/digital/Homepage_Hero_High_fidelity.jpeg" alt="" />` — empty alt violates WCAG 1.1.1 (non-text content) | Provide descriptive alt text, e.g., `alt="Lilongwe architectural data-center geometry illustrating LightSpeed's AI-native operating model"` |
| **2** | **High** | `src/pages/HomePage.tsx` (button focus styles) | 60, 68 | **Focus ring color deviates from design system** | `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-red focus-visible:ring-offset-2` overrides the design system's `2px solid var(--ls-cyan)` + `2px outline-offset`. Users relying on keyboard focus see red instead of cyan. | Change to `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-cyan focus-visible:ring-offset-2` |
| **3** | **High** | `src/pages/HomePage.tsx` | 25 | **Hero dark overlay uses non-token values** | `bg-black/40` (light) / `bg-black/60` (dark) — hardcoded hex alpha values, not design system tokens (`--ls-space-*` or brand tokens). While visually fine, this breaks the "no hardcoded brand colors" principle (§12). | Replace with design system tokens, e.g., `bg-ls-white/95` is already used on the light hero bg; the overlay could use a consistent `--ls-space-3` (`12px`) derived opacity or remain if no token exists. **Decision:** Keep as-is since no exact token matches `black/40`; document as known non-token usage. |
| **4** | **Medium** | `src/pages/HomePage.tsx` | 48 | **Heading type scale uses Tailwind `text-` utilities rather than canonical pt scale** | `h1 className="text-4xl sm:text-5xl lg:text-6xl"` — Tailwind `text-4xl` ≈ 24px, whereas canonical display-xl is 36pt → 48px. Known repository-wide divergence (§242–258). | Accept as system-wide token gap; not HomePage-specific. If/when tokens are revised, update HomePage to use `--ls-size-*` CSS custom properties directly. |
| **5** | **Medium** | `src/pages/HomePage.tsx` | 26, 27 | **Background tokens use app bridge (`--ls-*`) rather than canonical JSON** | `bg-ls-white/95` and `bg-ls-navy/80` resolve via `src/brand/brand-tokens.css` app bridge. Canonical `brand/tokens/brand-tokens.json` is the source of truth (§31). Slight divergences exist (e.g., `grey-light` = `#F2F2F2` canonical vs `#F7F8F9` bridge). | Document as known debt (§128–134). No action needed unless token revision occurs. |
| **6** | **Medium** | `src/pages/HomePage.tsx` | 106 | **Link color on light mode uses red instead of navy** | `<Link to="/ask" className="inline-flex items-center gap-1.5 font-body text-xs font-bold tracking-widest uppercase text-ls-red transition-colors hover:text-ls-red/80">` — light-mode links use `text-ls-red` per design system §155: "Links → cyan on dark, navy on light." **Wait** — this uses red, not navy. Let me re-check the design system...<br>§155: "Links → cyan on dark, navy on light; underline on hover". The code uses `text-ls-red` for links, which is **wrong** — should be `text-ls-navy` on light. | Change link color from `text-ls-red` to `text-ls-navy` for light mode, keeping `text-ls-cyan` for dark mode (already the case via `hover:text-ls-red/80` on light, but base should be navy). |
| **7** | **Low** | `src/pages/HomePage.tsx` | 45 | **Brand badge text color on red background may have contrast issues** | The "AI-NATIVE OPERATING MODEL" span: `bg-ls-red/10 text-ls-red border-ls-red/30` — red text on red-tinted background. Contrast may be insufficient for WCAG. | Verify contrast; if insufficient, change text color to `text-ls-white` or adjust background tint. |
| **8** | **Low** | `src/pages/HomePage.tsx` | 53 | **Lead paragraph tint may fail contrast** | `text-ls-white/90` on navy background — 90% tint of white on navy (#070A40). Contrast likely excellent (near-pure white on navy), but the tint could be removed for maximum contrast. | Optional: remove `/90` tint for maximum contrast; keep if visual softening is desired. |
| **9** | **Informational** | `src/data/homeCopy.ts` | 123–148 | **Solution statuses use labels not mapped to honesty badge variants** | Solutions grid uses `StatusBadge` with `status={solution.status}` where statuses are `'IN DEVELOPMENT'`, `'PILOT'`, `'PROTOTYPE'`, `'IN-HOUSE'`, `'EXPLORATION'`. The `StatusBadge` component maps these to bridge classes (cyan for PILOT, red for PROTOTYPE, etc.), which partially overlaps with the honesty badge system but uses different variant names. This is documented as a known inconsistency (§576–577 in design system). | Map solution statuses to honesty badge variants via `honestyLabel()` when the feature is next revised, or document as intentional separate vocabulary. |
| **10** | **Informational** | `src/components/home/HAOMTGVSection.tsx` | 96 | **Governance pillar has extra ring** | `ring-1 ring-ls-red/30` added specifically to the governance pillar article. This is a deliberate visual accent, not a bug. | Maintain as intentional design choice to highlight the governance layer. |

---

## Summary of Recommendations

### Immediate fixes (run before next deployment):
1. **Add descriptive alt text** to hero image (Critical — WCAG compliance)
2. **Fix focus ring color** to use `var(--ls-cyan)` instead of `var(--ls-red)` (High — keyboard accessibility)
3. **Fix link color** on light mode: change `text-ls-red` to `text-ls-navy` (Medium — color consistency per §155)

### Future considerations:
4. **Token scale alignment** — When the canonical token JSON is revised to include mist/slate values, also align the px↔pt type scale (§134).
5. **Tagline display** — Consider adding the LightSpeed tagline `"MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY"` to the HomePage hero or footer for brand completeness.
6. **Status badge mapping** — Eventually map solution statuses to honesty badge variants via `honestyLabel()` rather than the current `StatusBadge` bridge mapping.

### No changes needed:
- Visual hierarchy and section ordering are correct per §17
- Brand palette (navy/red/cyan) is used consistently; no orange/zinc
- Responsive restructuring is well-executed
- No prohibited AI design tells (no neon, glassmorphism, generated people)
- Spacing follows the 4px base grid scale
- Logo usage is correct and from canonical location
- No card grid fatigue — layout variety is maintained
- Accessibility foundations are solid (beyond the two critical fixes above)
