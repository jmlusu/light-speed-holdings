# LightSpeed Design System

**Version:** 1.1
**Status:** ACTIVE — Single Source of Truth
**Created:** 2026-10-04 · **Last updated:** 2026-10-04
**Owner:** Creative Director / Design System Owner

---

## Purpose

This document is the **canonical design system authority** for LightSpeed Holdings (Directive §7). It defines all visual, interaction, and motion standards for the public website. No page may invent its own design language. No page should hardcode brand colors when a token exists.

**Directive Reference:** §5, §6, §7, §8, §17, §19, §20, §21, §23, §32, §33, §38, §39

**Scope note (v1.1):** This revision audits the v1.0 document against the repository, corrects drifted token names and values, and adds the sections §7 requires but v1.0 lacked: imagery, logo usage, honesty status vocabulary, breakpoints with ranges, and the token-change procedure.

---

## Token Source & Path Reconciliation

There is exactly **one machine-readable token source**:

| Layer | Path | Role |
|-------|------|------|
| **Canonical (source of truth)** | `brand/tokens/brand-tokens.json` | The only machine-readable token file. Edit this first, always. |
| Canonical CSS mirror | `brand/tokens/brand-tokens.css` | CSS `:root` projection of the JSON (colors, pt type scale, spacing, grid, radius, layout). |
| Propagation mirrors | `static/brand/`, `public/brand/` | Generated mirrors kept in sync by `scripts/build/sync-brand.ps1`. |
| App bridge | `src/brand/brand-tokens.css` | Tailwind v4 `@theme` + `:root` variables consumed by the site (adds `--ls-*` extended tokens). |
| TypeScript tokens | `packages/design-system/src/tokens/*.ts` | TS projections used by components (`colors.ts`, `typography.ts`, `spacing.ts`, `visual.ts`). |
| Documentation | **This file** | Human-readable authority; updated in the same change as any token edit. |

**Path reconciliation note:** Directive §7 refers to the token source as `src/brand/tokens/`. That path does not exist. The canonical location is **`brand/tokens/`** at repository root (see `brand/CANONICAL_SOURCES.md`). The `src/brand/` tree is an application bridge, not the source of truth.

**Terminology used in this document:**
- *canonical* — value originates in `brand/tokens/brand-tokens.json` (+ its CSS mirror)
- *mirror* — generated copy under `static/brand/` or `public/brand/`
- *bridge* — application-layer variables in `src/brand/brand-tokens.css`
- *TS token* — value in `packages/design-system/src/tokens/`

Where layers disagree, the canonical JSON wins and the divergence is recorded in [Known Token Divergences](#known-token-divergences) below.

---

## Brand Identity

### Core Positioning
- **Company:** LightSpeed Holdings Limited
- **Tagline:** MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY
- **Positioning:** "The AI-native company builder for Africa."
- **Geographic Progression:** Malawi → Africa
- **North Star:** "We build AI-native companies."

### Visual Essence: CALM INTELLIGENCE
> Calm → Curiosity → Clarity → Confidence → Action

The design system embodies:
- **Premium** — Not generic, not template-like
- **Calm** — Restrained, spacious, unhurried
- **Intelligent** — Architectural, editorial, technically sophisticated
- **Editorial** — Strong typography, generous whitespace, visual hierarchy
- **African** — Authentic context, not stereotypical
- **Credible** — Evidence-based, honest, governance-visible

### What to Avoid (Directive §5)
- Generic neon AI aesthetics
- Excessive glowing cards
- Excessive glassmorphism
- Robot imagery
- Cliché humanoid AI images
- Excessive particle effects
- Gratuitous 3D
- Every section being dark
- Every section being a card grid
- Excessive gradients

### Superseded Palette
> **SUPERSEDED — do not use.** An earlier hardware-console palette (orange `#FF6B35`-family accents, zinc greys) is retired. The current palette is navy / red / cyan / morning mist / deep mineral / white. If you find orange or zinc in old components, migrate them (Governance → Change Process).

---

## Color System

### Brand Colors (Canonical — `brand/tokens/brand-tokens.json` → `brand/tokens/brand-tokens.css`)

| Token | CSS variable | Hex | Usage |
|-------|--------------|-----|-------|
| `navy` | `--ls-navy` | `#070A40` | Headlines, logo text, primary brand surfaces, primary backgrounds |
| `red` | `--ls-red` | `#E63946` | Signal waves, accent elements, key highlights, **primary CTAs** |
| `cyan` | `--ls-cyan` | `#00BFFF` | Shield base, accent elements, links on dark, focus rings |
| `grey-light` | `--ls-grey-light` | `#F2F2F2` | Light grey neutral (borders, subtle fills) |
| `white` | `--ls-white` | `#FFFFFF` | Clean backgrounds, text on navy |
| `grey-dark` | `--ls-grey-dark` | `#6B7280` | Secondary text grey |
| `grey-light-text` | `--ls-grey-light-text` | `#9CA3AF` | Muted text grey |

**§5 palette values not yet in the canonical JSON:** Directive §5 names six core colors, but the canonical token file carries only the seven above. `morning-mist` (`#F7F8F9`) and `deep-mineral` (`#121518`) exist in the **app bridge** (`--color-ls-mist`, `--color-ls-slate`) and in `packages/design-system/src/tokens/colors.ts`, not in `brand/tokens/`. This is a known gap in the canonical file — do not invent new hex values for them; use the bridge/TS values and record the mismatch when tokens are next revised.

### On-Surface Text (canonical)

| Token | Value |
|-------|-------|
| `--ls-on-navy` | `#FFFFFF` |
| `--ls-on-red` | `#FFFFFF` |
| `--ls-on-cyan` | `#070A40` |

### Semantic Colors (source: `packages/design-system/src/tokens/colors.ts`)

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `bg-primary` | morning-mist `#F7F8F9` | deep-mineral `#121518` | Page backgrounds |
| `bg-surface` | white `#FFFFFF` | navy `#070A40` | Card/panel backgrounds |
| `bg-surface-elevated` | white `#FFFFFF` | `#1A1E24` | Elevated surfaces (modals, dropdowns) |
| `text-primary` | navy `#070A40` | white `#FFFFFF` | Primary text |
| `text-secondary` | grey-dark `#6B7280` | grey-light-text `#9CA3AF` | Secondary text |
| `text-muted` | grey-light-text `#9CA3AF` | grey-dark `#6B7280` | Muted/tertiary text |
| `border-default` | grey-200 `#E5E7EB` | grey-700 `#374151` | Default borders |
| `border-subtle` | grey-100 `#F2F2F2` | grey-800 `#1F2937` | Hairline dividers |
| `border-focus` | cyan `#00BFFF` | cyan `#00BFFF` | Focus rings |
| `border-error` | red `#E63946` | red `#E63946` | Error states |

### Known Token Divergences

The repository currently carries three token layers that do not fully agree. **Documented, not fixed here** (token files are out of scope for this documentation track). Canonical wins; record the rest as debt:

| Item | Canonical (`brand/tokens`) | App bridge (`src/brand/brand-tokens.css`) | TS tokens (`colors.ts`) | Note |
|------|---------------------------|-------------------------------------------|--------------------------|------|
| `grey-light` | `#F2F2F2` | `#F7F8F9` | `#F2F2F2` (border-subtle) | Bridge aliases grey-light to mist; footnoted in `brand/tokens.md` |
| morning-mist `#F7F8F9` | absent | `--color-ls-mist` | `bg-primary` (light) | §5 color missing from canonical JSON |
| deep-mineral `#121518` | absent | `--color-ls-slate` | `bg-primary` (dark) | §5 color missing from canonical JSON |
| light `text-primary` | n/a | `--ls-text-light: #121518` | `#070A40` (navy) | Bridge darkens light-mode text; TS/canonical use navy |
| dark elevated surface | n/a | `#1A1D21` / `#22262A` (`--ls-surface-elevated-dark` / mineral) | `#1A1E24` | Three values for one concept |
| dark borders | n/a | `#2A2D31` / `#1F2226` | `#374151` / `#1F2937` | Bridge uses bespoke greys; TS uses grey-700/800 |

> `colors.ts` header states `brand/tokens/brand-tokens.json` is the source of truth — true for intent, but the file does not yet contain mist/slate. Close this when tokens are next revised.

### Supporting Neutrals (for accessibility & hierarchy)

| Token | Hex | Usage |
|-------|-----|-------|
| `grey-50` | `#F9FAFB` | Subtle backgrounds |
| `grey-100` | `#F2F2F2` | Light grey (canonical `grey-light`) |
| `grey-200` | `#E5E7EB` | Borders, dividers |
| `grey-300` | `#D1D5DB` | Disabled borders |
| `grey-400` | `#9CA3AF` | Light text grey (canonical `grey-light-text`) |
| `grey-500` | `#6B7280` | Dark grey (canonical `grey-dark`) |
| `grey-600` | `#4B5563` | Medium text |
| `grey-700` | `#374151` | Dark text on light |
| `grey-800` | `#1F2937` | Near-black |
| `grey-900` | `#111827` | Almost black |

### Color Usage Rules

1. **Primary CTA** → Always `red` background, white text
2. **Secondary CTA** → `navy` border (light) / white border (dark), `navy` text (light) / white text (dark)
3. **Links** → `cyan` on dark, `navy` on light; underline on hover
4. **Focus Ring** → `cyan`, **2px outline, 2px offset** (actual implementation — see Accessibility)
5. **Error/Destructive** → `red`
6. **Success/Verified** → `cyan` (not green — cyan is our trust signal)
7. **Warning/Pilot** → `red` (per honesty badge system)
8. **Never use orange** as primary brand accent (Directive §5)
9. **80/10/10 rule** — navy-dominant surfaces (≈80%), red and cyan as accents (≈10% each); red never used as a large fill

### CSS Custom Properties (actual names in the codebase)

The app bridge (`src/brand/brand-tokens.css`) defines brand colors **twice**: as Tailwind v4 `@theme` entries (generating utilities) and as `:root` variables:

```css
/* @theme — generates Tailwind utilities: bg-ls-navy, text-ls-cyan, border-ls-red … */
@theme {
  --color-ls-navy: #070A40;
  --color-ls-red: #E63946;
  --color-ls-cyan: #00BFFF;
  --color-ls-mist: #F7F8F9;        /* morning mist */
  --color-ls-slate: #121518;       /* deep mineral */
  --color-ls-white: #FFFFFF;
  --color-ls-grey-dark: #6B7280;
  --color-ls-grey-light-text: #9CA3AF;
  /* extended neutrals: mist-light, alabaster #FAFAFA, mist-subtle #F0F1F3,
     slate-deep #0D1013, mineral #1A1D21, mineral-elevated #22262A, stone, water, reflection */
}

:root {
  /* Brand */
  --ls-navy: #070A40;
  --ls-red: #E63946;
  --ls-cyan: #00BFFF;
  /* RGB channels for alpha compositing */
  --ls-navy-rgb: 7, 10, 64;
  --ls-red-rgb: 230, 57, 70;
  --ls-cyan-rgb: 0, 191, 255;

  /* On-surface text */
  --ls-on-navy: #FFFFFF;
  --ls-on-red: #FFFFFF;
  --ls-on-cyan: #070A40;
}

.dark {
  /* Dark surfaces are overridden per-surface — see Surfaces */
}
```

> There is **no** `--color-navy` variable. Older notes referencing `--color-navy` / `--color-cyan` mean `--ls-navy` / `--ls-cyan` (`:root`) or `--color-ls-navy` / `--color-ls-cyan` (`@theme`).

---

## Typography

### Font Family
**Arial** — system font stack for performance and credibility (canonical `--ls-font-*`, all `Arial, sans-serif`).

```css
--ls-font-display: Arial, sans-serif;
--ls-font-heading: Arial, sans-serif;
--ls-font-body: Arial, sans-serif;
--ls-font-caption: Arial, sans-serif;
/* TS token (typography.ts) full stack: */
font-family: Arial, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif;
/* Mono (TS only): "SF Mono", "Fira Code", Monaco, monospace */
```

### Type Scale (canonical pt — `brand/tokens/brand-tokens.json` / `brand-tokens.css`, line heights from `packages/design-system/src/tokens/typography.ts`)

| Token | Size (canonical) | px equivalent | Line Height | Weight | Usage |
|-------|------------------|---------------|-------------|--------|-------|
| `display-xl` | 36pt | 48px | 1.1 | 700 | Hero headlines, cover titles |
| `title-xl` | 32pt | 42.7px | 1.15 | 700 | Major section titles |
| `title-lg` | 28pt | 37.3px | 1.2 | 700 | Section titles |
| `title-md` | 24pt | 32px | 1.25 | 700 | Subsection titles |
| `title-sm` | 18pt | 24px | 1.3 | 700 | Card titles |
| `subtitle` | 16pt | 21.3px | 1.5 | 400 | Lead paragraphs, intros |
| `body-lg` | 16pt | 21.3px | 1.6 | 400 | Body text (comfortable reading) |
| `body` | 14pt | 18.7px | 1.6 | 400 | Default body text |
| `body-sm` | 13pt | 17.3px | 1.5 | 400 | Secondary body |
| `caption` | 12pt | 16px | 1.4 | 400 | Captions, footnotes, disclaimers |
| `overline` | 11pt | 14.7px | 1.3 | 700 | Uppercase labels, badges |

- px equivalents = pt × 4/3 (1pt = 1.333px). v1.0 published wrong px values for `subtitle`, `body-lg`, `body`, `body-sm`, `caption`, and `overline` — corrected here.
- `overline` exists **only in `typography.ts`** (fontSize `11pt`, uppercase, `letter-spacing: 0.1em`); it is not in the canonical JSON/CSS. Cite `typography.ts` for it.
- Canonical CSS mirror defines the same steps as `--ls-size-display-xl … --ls-size-caption` **in pt** (e.g. `--ls-size-display-xl: 36pt`).

### Known Divergence: the px bridge

`src/brand/brand-tokens.css` defines a **px** ramp that is *not* a pt→px conversion for most steps:

| Step | Canonical (pt → px) | Bridge `--ls-size-*` (px) | Δ |
|------|---------------------|---------------------------|---|
| display-xl | 36pt → 48px | 48px | ✓ |
| title-xl | 32pt → 42.7px | 40px | −2.7 |
| title-lg | 28pt → 37.3px | 32px | −5.3 |
| title-md | 24pt → 32px | 24px | −8 |
| title-sm | 18pt → 24px | 20px | −4 |
| subtitle / body-lg | 16pt → 21.3px | 16px | −5.3 |
| body | 14pt → 18.7px | 14px | −4.7 |
| body-sm | 13pt → 17.3px | 13px | −4.3 |
| caption | 12pt → 16px | 12px | −4 |
| caption-sm (bridge only) | — | 11px | — |

**Rule:** treat the **pt scale as canonical** for brand typography; the bridge px ramp is an approximate mapping used by utility classes. Do not mix the two scales in the same view. Closing this gap is token debt, tracked above.

### Typography Rules

1. **Editorial Scale** — Use oversized typography for impact (Directive §8)
2. **Strong Hierarchy** — Clear distinction between heading levels
3. **Generous Line Height** — Minimum 1.5 for body, 1.15 for headlines
4. **Tracking** — Tight for headlines (`letter-spacing: -0.02em`), normal for body, `0.1em` for uppercase labels (TS token `letterSpacing.wider`)
5. **Uppercase Labels** — `overline` style: `text-transform: uppercase; letter-spacing: 0.1em;`
6. **No Custom Fonts** — Arial only; avoids font loading, CLS, licensing

---

## Spacing System

### Canonical Scale — `--ls-space-*` (4px base grid)

```css
--ls-space-1: 4px;
--ls-space-2: 8px;
--ls-space-3: 12px;
--ls-space-4: 16px;
--ls-space-5: 24px;
--ls-space-6: 32px;
--ls-space-7: 48px;
--ls-space-8: 64px;
--ls-space-9: 96px;
/* Bridge only (not in canonical JSON): */
--ls-space-10: 128px;
```

Scale: `[4, 8, 12, 16, 24, 32, 48, 64, 96]` from `brand/tokens/brand-tokens.json`.

> There is **no** `--spacing-6: 24px`. v1.0 documented Tailwind-style `--spacing-*` names with wrong step values (`--spacing-6: 24px` vs canonical `--ls-space-6: 32px`). Use `--ls-space-*` only. In Tailwind classes, the bridge's `@theme` spacing entries resolve `p-6` etc. — prefer explicit `--ls-space-*` in custom CSS.

### Spacing Rules
1. **Consistent Rhythm** — All spacing from the scale; no arbitrary values
2. **Section Padding** — `--ls-space-8` (64px) vertical, `--ls-space-7` (48px) horizontal
3. **Component Gaps** — `--ls-space-5` (24px) default, `--ls-space-6` (32px) loose
4. **Inline Gaps** — `--ls-space-2` (8px) tight, `--ls-space-3` (12px) normal

---

## Grid & Layout

### Breakpoints (source: `packages/design-system/src/tokens/visual.ts`)

| Name | Range | `visual.ts` value | Media query | Tailwind |
|------|-------|-------------------|-------------|----------|
| `mobile` | < 640px | `640px` (used as max) | `(max-width: 639px)` | base |
| `tablet` | 640–1023px | `640px` (min) | `(min-width: 640px) and (max-width: 1023px)` | `sm:`–`md:` |
| `laptop` | 1024–1279px | `1024px` | `(min-width: 1024px) and (max-width: 1279px)` | `lg:` |
| `desktop` | 1280–1535px | `1280px` | `(min-width: 1280px) and (max-width: 1535px)` | `xl:` |
| `large-desktop` | ≥ 1536px | `1536px` | `(min-width: 1536px)` | `2xl:` |

### Container Widths

| Context | Max Width | Padding | Source |
|---------|-----------|---------|--------|
| Web page | **1200px** (`--ls-page-max-width`) | `--ls-margin` 48px (reduce to 24px on mobile — guidance, not a token) | canonical |
| Content column | 720px | — | *recommended reading measure (guidance, not a token)* |
| Narrow column | 480px | — | *recommended reading measure (guidance, not a token)* |

### Grid System (canonical)

- **Columns:** 12 (`--ls-grid-columns`)
- **Gutter:** 24px (`--ls-gutter`)
- **Margin:** 48px (`--ls-margin`)

---

## Border Radius

| Layer | Tokens | Values |
|-------|--------|--------|
| Canonical | `--ls-radius-sm` / `-md` / `-lg` | 4px / 8px / 16px |
| Bridge adds | `--ls-radius-xl` / `-2xl` / `-full` | 24px / 32px / 9999px |
| TS token (`visual.ts`) | `small` / `medium` / `large` / `full` | 4px / 8px / 16px / 9999px |

| Token | Value | Usage |
|-------|-------|-------|
| `small` / `sm` | 4px | Buttons, badges, inputs |
| `medium` / `md` | 8px | Cards, panels |
| `large` / `lg` | 16px | Modals, major containers |
| `xl` / `2xl` (bridge) | 24px / 32px | Large feature surfaces |
| `full` | 9999px | Pills, avatars, round buttons |

---

## Shadows

Two real shadow systems exist. Use the restrained app bridge for product UI; the design-system layer additionally provides glow accents.

### Layer A — App bridge (`src/brand/brand-tokens.css`, "restrained depth")

| Token | Value | Usage |
|-------|-------|-------|
| `--ls-shadow-sm` | `0 1px 2px rgba(0,0,0,0.03)` | Subtle elevation |
| `--ls-shadow-md` | `0 4px 12px rgba(0,0,0,0.05)` | Cards, panels |
| `--ls-shadow-lg` | `0 8px 24px rgba(0,0,0,0.08)` | Elevated cards |
| `--ls-shadow-xl` | `0 16px 48px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--ls-shadow-red` | `0 8px 24px rgba(230,57,70,0.15)` | Red accent elevation |
| `--ls-shadow-cyan` | `0 8px 24px rgba(0,191,255,0.15)` | Cyan accent elevation |

### Layer B — Design system (`globals.css` / `visual.ts` → Tailwind `shadow-*`)

| Token | Value | Usage |
|-------|-------|-------|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| `shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)` | Cards, panels |
| `shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)` | Elevated cards |
| `shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)` | Modals, dropdowns |
| `--shadow-glow-cyan` | `0 0 20px rgba(0,191,255,0.3)` | Focus, active states |
| `--shadow-glow-red` | `0 0 20px rgba(230,57,70,0.3)` | Primary CTA hover |

**Dark mode:** design-system shadow base rises to `rgba(0,0,0,0.3)` (md) / `rgba(0,0,0,0.4)` (lg); glows unchanged. Prefer `--ls-shadow-*` for everyday depth — glow is an accent, not a default.

---

## Surfaces

| Surface | Light Mode | Dark Mode | Source | Usage |
|---------|------------|-----------|--------|-------|
| `page` | morning-mist `#F7F8F9` | deep-mineral `#121518` | `colors.ts` (`bg-primary`) | Full page background |
| `card` | white `#FFFFFF` | navy `#070A40` | `colors.ts` (`bg-surface`) | Standard cards |
| `card-elevated` | white + shadow `md` | `#1A1E24` + shadow `lg` | `colors.ts` (`bg-surface-elevated`) | Interactive cards |
| `card-elevated (bridge)` | `#FAFAFA` (`--ls-surface-elevated-light`) | `#1A1D21` / `#22262A` (`--ls-surface-elevated-dark` / mineral) | bridge | Site implementation |
| `panel` | `grey-50 #F9FAFB` | `#0A0C12` | *recommended — not yet a token* | Secondary panels |
| `overlay` | `rgba(18,21,24,0.6)` | `rgba(0,0,0,0.8)` | *recommended — not yet a token* | Modal backdrops |

Bridge `:root` surfaces (verified):

```css
:root {
  --ls-bg-light: #F7F8F9;
  --ls-surface-light: #FFFFFF;
  --ls-surface-elevated-light: #FAFAFA;
  --ls-text-light: #121518;
  --ls-text-secondary-light: #6B7280;
  --ls-text-muted-light: #9CA3AF;
  --ls-bg-dark: #121518;
  --ls-surface-dark: #1A1D21;
  --ls-surface-elevated-dark: #22262A;
  --ls-text-dark: #F7F8F9;
  --ls-border-dark: #2A2D31;
  --ls-border-subtle-dark: #1F2226;
}
```

---

## Borders

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `default` | grey-200 `#E5E7EB` (`colors.ts`) / bridge `#E5E7EB` | grey-700 `#374151` (`colors.ts`) / bridge `#2A2D31` | Default borders |
| `subtle` | grey-100 `#F2F2F2` | grey-800 `#1F2937` (`colors.ts`) / bridge `#1F2226` | Hairline dividers |
| `emphasis` | navy | cyan | Left-border accents |
| `focus` | cyan | cyan | Focus states (2px outline) |

See [Known Token Divergences](#known-token-divergences) for the bridge-vs-TS border mismatch.

---

## Iconography

### Icon System: Lucide React (`lucide-react ^0.475.0`)
- Consistent 24×24px base size
- Stroke width: 2px (library default; do not override per-icon)
- Rounded caps and joins
- Outline style only (no filled icons)

### Custom Brand Icons
- **Logo Mark:** Geometric "L" — two interlocking forward-moving planes, red acceleration element, cyan core (Directive §6)
- **Micro-Illustrations (Type K):** H, A, O, M, T, G, V glyphs for HAOMTGV
- **Sector Icons:** Minimal line icons per sector (not emoji)

---

## Motion System (Directive §21)

### Principles
> "Slow to the eye. Fast to the mind."

1. **Meaningful** — Motion reinforces meaning (reveal, progress, transition)
2. **Restrained** — No constant movement, no distracting particles
3. **Respectful** — Honor `prefers-reduced-motion`
4. **Performant** — CSS transforms only; no layout thrashing

### Allowed Motion Types (source: `visual.ts` / `globals.css` `--duration-*`, `--easing-*`)

| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| `reveal` | 600ms | `cubic-bezier(0.16, 1, 0.3, 1)` (`--easing-reveal`) | Scroll reveal (sections, cards) |
| `fade` | 300ms | `ease-out` | Modals, tooltips, dropdowns |
| `slide-up` | 400ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Modals, drawers, toasts |
| `scale` | 200ms | `ease-out` | Buttons, cards on hover |
| `line-draw` | 800ms | `ease-in-out` | Diagram lines, HAOMTGV connections |
| `number-count` | 1000ms | `ease-out` | Metric counters |
| `parallax` | scroll-linked | — | Hero imagery, subtle (no fixed px budget — keep subordinate to content) |

### App utility layer (`src/index.css` + bridge)

| Token / class | Value |
|---------------|-------|
| `--transition-slow` / `.transition-slow` | 500ms `cubic-bezier(0.4,0,0.2,1)` |
| `--transition-medium` / `.transition-medium` | 300ms same easing |
| `--transition-fast` / `.transition-fast` | 150ms same easing |
| `--ease-spatial` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `--ease-in-expo` | `cubic-bezier(0.7, 0, 0.84, 0)` |
| `.reveal-up` | `translateY(20px)` → 0, 600ms `var(--ease-out-expo)` |
| `.reveal-fade` | opacity fade, 500ms |
| Stagger delays | 50ms increments (`.delay-50` … `.delay-300`) |

**No animation framework.** `framer-motion` is not a dependency and has zero imports. Motion = CSS transitions/keyframes + IntersectionObserver reveals, with a `useReducedMotion` hook exported from the design system.

### Forbidden
- Constant animation loops
- Bouncing/elastic easing
- Excessive 3D transforms
- Animation that delays reading
- Particle systems

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
`visual.ts` `reducedMotion = 0.01ms` mirrors this; components use the `useReducedMotion` hook.

---

## Components

### Core Components (design system package — complete list)

The package exports **exactly these 10 components** (`packages/design-system/src/index.ts`). v1.0 listed 23 components (Input, Link, Modal, Tabs, Table, …) that do not exist — corrected.

| Component | Key props (verified) | Notes |
|-----------|----------------------|-------|
| `Badge` | `variant: 'proven'\|'pilot'\|'fieldable'\|'development'\|'neutral'`, `size?: 'sm'\|'md'` | Honesty badge — see below |
| `Button` | `variant?: 'primary'\|'secondary'\|'ghost'\|'link'`, `size?: 'sm'\|'md'\|'lg'` | States: default, hover, focus, active, disabled, loading |
| `Card` | `variant?: 'default'\|'elevated'\|'interactive'`, `padding?: 'none'\|'sm'\|'md'\|'lg'` | default, hover, focus |
| `Container` | `size?: 'default'\|'narrow'\|'wide'\|'full'`, `padding?: boolean` | Page/content widths |
| `Grid` | `columns?: 1–12`, `gap?: spacing keys \| 'component' \| 'tight'` | 12-col grid |
| `Heading` | `level: 1\|2\|3\|4\|5\|6\|'display'`, `as?` | Semantic heading hierarchy |
| `Logo` | `variant?: 'full'\|'dark'\|'light'\|'icon'\|'monochrome'`, `size?: 'sm'\|'md'\|'lg'\|'xl'` | See Logo Usage |
| `Section` | `id?`, `label?`, `theme?: 'light'\|'dark'`, `scrim?`, `narrow?`, `wide?` | Page section wrapper |
| `Stack` | `direction?: 'vertical'\|'horizontal'`, `gap?: spacing keys \| 'component'\|'tight'\|'loose'` | Flow layout |
| `Text` | `variant?: 'body'\|'lead'\|'caption'\|'overline'\|'subtitle'`, `as?` | Typographic text |

Also exported: `tokens`, `useTheme`, `useMediaQuery`, `useReducedMotion`, `cn`, `formatters`.

> Additional site UI (forms, modals, navigation, page composites) lives in `src/components/` and is **not** yet promoted into the package. Promoting it is a Governance change, not a documentation change.

### Honesty Badge Component (Critical)

```tsx
import { Badge } from '@lightspeed/design-system';

<Badge variant="proven">Proven in-house</Badge>
<Badge variant="pilot">In pilot</Badge>
<Badge variant="fieldable">Fieldable in 2026</Badge>
<Badge variant="development">In development</Badge>
```

**Visual spec** (source: `packages/design-system/src/tokens/colors.ts` `honesty` block, mirrored as `--badge-*` custom properties in `globals.css:43+`, consistent with `siteContent.ts` `TONE_STYLES` and `CLAIMS_GOVERNANCE.md`):

| Variant | Border | Background | Text |
|---------|--------|------------|------|
| `proven` | `rgba(0,191,255,0.4)` (cyan/40) | `rgba(0,191,255,0.1)` (cyan/10) | `#00BFFF` |
| `pilot` | `rgba(230,57,70,0.4)` (red/40) | `rgba(230,57,70,0.1)` (red/10) | `#E63946` |
| `fieldable` | `rgba(156,163,175,0.4)` (grey-light-text/40) | `rgba(156,163,175,0.1)` | `#9CA3AF` |
| `development` | `rgba(107,114,128,0.4)` (grey-dark/40) | `rgba(107,114,128,0.1)` | `#6B7280` |
| `neutral` | grey tokens — uncolored, for generic labels (see `Badge.tsx`) | | |

---

## Honesty Status Vocabulary (Directive §23)

Every public claim carries a status. Authoritative source: **`docs/CLAIMS_GOVERNANCE.md`** (definitions below are its § Claim Classification System; that file governs on conflict).

| Status | Label | Definition | Publish? |
|--------|-------|------------|----------|
| `VERIFIED` | **VERIFIED** | Independently confirmed by third party (auditor, client, regulator) | ✅ Yes |
| `PROVEN_IN_HOUSE` | **PROVEN IN-HOUSE** | Running in LightSpeed operations, validated by internal systems/tests | ✅ Yes |
| `PILOT` | **PILOT** | Active pilot with real users, composing evidence, no signed engagement | ✅ Yes |
| `DEMONSTRATION` | **DEMONSTRATION** | Working demo/prototype, no live users | ✅ Yes |
| `FIELDABLE` | **FIELDABLE** | Ready for deployment, awaiting client, technically complete | ✅ Yes |
| `FUTURE` | **FUTURE** | Roadmap target, no evidence yet, honestly stated | ✅ Yes |
| `HISTORICAL` | **HISTORICAL** | Was true, no longer current (archived for reference) | ⚠️ Context only |
| `UNVERIFIED_DO_NOT_PUBLISH` | **UNVERIFIED — DO NOT PUBLISH** | Cannot be verified, lacks evidence | ❌ **NO** |

**Canonical definition of PROVEN IN-HOUSE** (site FAQ, `src/data/registries/faq-registry.json` faq-23):

> "'Proven In-House' means the capability, workflow, or outcome has been verified running inside LightSpeed Holdings' own operations — not delivered to an external paying client."

### Status → Badge variant mapping

| Status | Badge variant (tone) |
|--------|----------------------|
| `VERIFIED`, `PROVEN_IN_HOUSE` | `proven` (cyan) |
| `PILOT` | `pilot` (red) |
| `DEMONSTRATION`, `FIELDABLE` | `fieldable` (grey-light-text) |
| `FUTURE`, `HISTORICAL` | `development` (grey-dark) |
| `UNVERIFIED_DO_NOT_PUBLISH` | **no badge — never published** |

Use `honestyLabel()` / `TONE_STYLES` in `src/data/siteContent.ts` to derive tone; do not hand-roll mappings.

**Known implementation inconsistencies (report-only gaps — not fixed by this document):**
1. `src/pages/UseCasesPage.tsx` derives the Badge variant by lowercasing the raw status (`.toLowerCase().replace('_','-')`): `"LIVE"` → `"live"`, `"PROVEN IN-HOUSE"` → `"proven in-house"` — invalid `BadgeVariant` values that are cast `as any`, so those badges lose their intended tone. Fix: map status → variant via `honestyLabel()`.
2. Sector experience uses its own 4-label system (`PROVEN / CURRENT / DEMONSTRATION / FUTURE`, `CLAIMS_GOVERNANCE.md` content rules) whose tones coincide with the mapping above; keep the two vocabularies distinct in copy.

---

## Logo Usage (Directive §6)

### Concept
Geometric "L" formed by two interlocking forward-moving planes, with a red acceleration element and a cyan core — light speed, forward momentum, sovereign focus.

### Files
Canonical location: **`brand/logo/`** (populated — 8 variants, SVG + PNG siblings, mirrored to `static/brand/logo/` and `public/brand/logo/` via `scripts/build/sync-brand.ps1`). The legacy `brand/logos/` tree is **DEPRECATED**: do not add files there and do not reference it in new work; style explorations are archived at `.archive/brand/logos/`.

Required variants (canonical filenames in `brand/logo/`):

| File | Purpose |
|------|---------|
| `logo-full.svg` | Full logo, light backgrounds |
| `logo-dark-bg.svg` | Full logo, dark backgrounds |
| `logo-light-bg.svg` | Full logo, light backgrounds (inverse-safe) |
| `logo-mark.svg` | Icon / mark only |
| `logo-mark-mono.svg` | Single-color reproduction |
| `logo-favicon.svg` | Favicon source |
| `logo-avatar.png` | Avatar / profile image |
| `logo-og.png` | Open Graph share card |

### Clear Space & Minimum Size
- **Clear space:** ≥ 1× the height of the "L" in LIGHTSPEED on all sides (from `brand/tokens/brand-tokens.json`)
- **Minimum full logo:** 30mm print / 120px screen
- **Minimum icon:** 12mm print / 32px screen

### Rules
1. **SVG first** — vector source for all screen uses; PNG only where a raster is required (OG, avatar)
2. **Never** recreate, rotate, recolor, outline, add effects to, or place the logo on busy imagery
3. **Never** use a different logo per page — one system, chosen variant only
4. On-surface only from the palette: white on navy/red/dark imagery; navy on white/mist
5. **™** appears at first mention per `brand/tokens.md` checklist
6. Source logos from `brand/logo/` (fallback: `brand/logos/` official suite per `brand/CANONICAL_SOURCES.md`) — never redraw

---

## Imagery & Media (Directive §8, §19, §20, §38, §39)

### Photography & Art Direction
- **Editorial scale** — imagery is compositional, not decorative filler (§8)
- **Architectural geometry** — structures, grids, data-center and civic geometry over stock desk scenes (§8)
- **Whitespace-friendly** — images support the layout; they do not fight type (§8)
- **African context, authentic** — real people, real work, contemporary settings (§8, §39)
- **No stereotypes** — *"Avoid stereotypical poverty imagery."* (Directive line 2067); no "staring at a laptop" cliché; no generic stock-photo smiles (lines 1088, §19 Type A)
- **Authentic leadership** — leadership imagery shows competence and context, not posed headshot grids (line 1278)
- **Controlled accent use** — cyan/red appear as light and signal in imagery, never as an all-over grade (§5 80/10/10)

### Diagrams & Illustration Types (Directive §19)
- **Type A** — cinematic hero imagery (African tech/business context, Lilongwe geometry, data centers)
- **Type B** — process/flow infographics (HAOMTGV, model routing, economics)
- **Type K** — micro-illustrations (H A O M T G V glyphs)
- **Type D/E** — model-routing and Africa AI economics diagrams
- Editorial diagrams are **preferred over photographs** for explaining mechanism (line 1224, §20)

### Placement Rules (§20)
- Hero imagery is Type A, full-bleed or contained per section theme
- Supporting sections use diagrams first, photography second
- Every image carries meaningful alt text (Accessibility)

### External References & Research Art Direction (§38, §39)
- External reports/books inform **art direction and argument only** — never copied imagery, never presented as LightSpeed evidence
- **Africa-first:** Malawi → SADC → Africa (§39); global imagery only where the subject is genuinely global

---

## Page-Specific Patterns

### Homepage Sequence (Directive §17)
1. Hero → 2. Orientation → 3. Visitor Paths → 4. HAOMTGV → 5. AI Company Builder → 6. 90-Role Workforce → 7. Open/Open-Weight AI → 8. Use Cases → 9. Solutions → 10. Sectors → 11. Pharos → 12. Governance → 13. FAQ → 14. Final CTA

### Section Template (actual component API)

```tsx
<Section id="section-id" label="Section Label" theme={theme}>
  <Heading level={2}>Section Title</Heading>
  <Text variant="lead">Lead paragraph</Text>
  <Container>
    <Grid columns={4} gap="component">
      {items.map(item => (
        <Card key={item.id} variant="interactive">
          {/* … */}
        </Card>
      ))}
    </Grid>
  </Container>
</Section>
```

> v1.0's template used a non-existent `SectionHeading`, invalid `gap="lg"`, and mismatched tags. The API above matches `Section`/`Heading`/`Text`/`Container`/`Grid`/`Card` props as implemented.

### HAOMTGV Diagram (Directive §3, §19 Type B)
- Vertical flow: HUMAN → AGENTS → ORCHESTRATION → MEMORY → TOOLS → GOVERNANCE → VALUE
- Feedback loops between Memory, Tools, Orchestration, Governance
- Human layer above system; Value as business outcome
- Cyan connection lines; red accent on Human; navy containers

### Model Routing Infographic (Directive §19 Type D)
```
LOCAL / OPEN-WEIGHT → LOW COST TASKS
MID-TIER → STANDARD REASONING
PREMIUM → HIGH COMPLEXITY
HUMAN → FINAL AUTHORITY
```

### Africa AI Economics (Directive §19 Type E)
- API dependency vs local inference vs open-weight vs hybrid routing
- Principle: "Use the least expensive model that can reliably do the job."
- No fabricated cost savings

---

## Accessibility (Directive §32)

### Required Standards
- **WCAG 2.1 AA** minimum
- **Keyboard Navigation** — All interactive elements reachable and operable
- **Visible Focus** — 2px cyan outline, 2px offset (actual implementation)
- **Semantic Headings** — h1-h6 hierarchy; no skipped levels
- **Contrast** — 4.5:1 normal text, 3:1 large text (AA)
- **Alt Text** — Required on all images; descriptive, not decorative
- **Reduced Motion** — Respect `prefers-reduced-motion`
- **Accessible Dialogs** — Focus trap, ARIA roles, Escape closes
- **Accessible Forms** — Labels, error announcements, validation
- **No Color-Only Information** — Icons + text for status (honesty badges pair color with text)
- **Screen Reader Status** — Live regions for dynamic content
- **Skip link** — `.skip-link` focus styles defined in `src/index.css`

### Focus Ring Implementation (actual code — `src/index.css`)

```css
:focus-visible {
  outline: 2px solid var(--ls-cyan);
  outline-offset: 2px;
}
```

> v1.0 claimed a 3px ring and showed invalid `ring:` pseudo-declarations. The shipped rule above is authoritative.

---

## Responsive Behavior (Directive §33)

### Mobile-First Methodology
```css
/* Base = mobile */
.component { padding: var(--ls-space-4); }   /* 16px */

/* Tablet up */
@media (min-width: 640px) {
  .component { padding: var(--ls-space-6); } /* 32px */
}

/* Laptop up */
@media (min-width: 1024px) {
  .component { padding: var(--ls-space-7); } /* 48px */
}

/* Desktop up */
@media (min-width: 1280px) {
  .component { padding: var(--ls-space-8); } /* 64px */
}
```

### Navigation
- **Mobile:** Hamburger menu, slide-in drawer
- **Tablet:** Condensed horizontal nav
- **Desktop+:** Full horizontal nav with CTAs

### Information Hierarchy
- Mobile: Single column, stacked sections
- Desktop: Multi-column grids, side-by-side layouts
- **Never** simply shrink desktop — restructure for mobile

---

## Implementation

### Package Structure (actual — `packages/design-system/`)

```
packages/design-system/
├── package.json
├── tsconfig.json
└── src/
    ├── index.ts                 # Public exports (barrel below)
    ├── tokens/
    │   ├── colors.ts            # Colors + honesty block (semantic, light/dark)
    │   ├── typography.ts        # pt type scale, line heights, semantic styles
    │   ├── spacing.ts           # Spacing tokens
    │   ├── visual.ts            # Shadows, radius, breakpoints, motion
    │   └── index.ts
    ├── components/              # Exactly 10: Badge, Button, Card, Container,
    │   └── …                    #   Grid, Heading, Logo, Section, Stack, Text
    ├── hooks/
    │   ├── useTheme.ts
    │   ├── useMediaQuery.ts
    │   └── useReducedMotion.ts
    ├── utils/
    │   ├── cn.ts                # class merging
    │   └── formatters.ts
    └── styles/
        └── globals.css          # --shadow-*, --duration-*, --easing-*, --badge-*, dark overrides
```

**There is no `tailwind.config.ts`** anywhere in the repo — Tailwind v4 is CSS-first (see below). v1.0's tree (23 components, `reset.css`, `utilities.css`, `motion.ts`, `breakpoints.ts` as separate files) was aspirational, not actual.

### Usage in Apps

```tsx
// src/pages/UseCasesPage.tsx (repo root, not apps/web/)
import { Badge, Button, Card, Container, Grid, Heading, Section, Stack, Text } from '@lightspeed/design-system';
```

> There is no `apps/web/` directory. Site code lives at repository root `src/` (Vite React SPA). The design system is imported as `@lightspeed/design-system`.

### Tailwind Integration (v4, CSS-first)

Entry stylesheet `src/index.css`:

```css
@import "tailwindcss";
@import "./brand/brand-tokens.css";

@custom-variant dark (&:where(.dark, .dark *));

@theme {
  --font-sans: Arial, sans-serif;
  --font-display: Arial, sans-serif;
}
```

- Brand colors enter Tailwind through `@theme` in `src/brand/brand-tokens.css` (`--color-ls-*`), yielding utilities such as `bg-ls-navy`, `text-ls-cyan`, `border-ls-red`.
- Dark mode = `.dark` class on `<html>`, activated by the `@custom-variant` above.
- Token-driven motion utilities (`.transition-slow`, `.reveal-up`, …) are plain CSS in `src/index.css`.
- **Do not** create a `tailwind.config.*` — configuration belongs in CSS (`@theme`, `@custom-variant`, `@utility`).

---

## Governance

### Change Process
1. **Propose** — Create RFC in `docs/adr/` for design system changes
2. **Review** — Creative Director + Design System Owner + Lead Frontend
3. **Approve** — CEO sign-off for brand-affecting changes
4. **Implement** — Update tokens, components, documentation
5. **Version** — Semantic versioning for `@lightspeed/design-system`
6. **Communicate** — Changelog, migration guide

### How to Change a Token
1. Edit **`brand/tokens/brand-tokens.json`** (the single machine-readable source)
2. Update the canonical CSS mirror **`brand/tokens/brand-tokens.css`**
3. Update TS projections: `packages/design-system/src/tokens/*.ts`
4. Update the app bridge **`src/brand/brand-tokens.css`** (`@theme` + `:root`)
5. Run **`pwsh scripts/build/sync-brand.ps1`** to propagate to `static/brand/` and `public/brand/` mirrors
6. Verify: **`pwsh scripts/build/sync-brand.ps1 -Verify`** — exits 1 on mirror drift; CI must stay green
7. Update **this document** (and `brand/tokens.md` if naming/notes changed) in the same change
8. Brand-affecting changes additionally require an ADR + CEO sign-off (Change Process above)

### Forbidden Without Approval
- Adding new colors to palette
- Changing type scale
- Modifying spacing scale
- Adding new component variants
- Changing motion durations/easings
- Modifying honesty badge system

---

## Quality Assurance

### Automated Checks (actual CI — no aspirational entries)
- **Token mirror drift** — `pwsh scripts/build/sync-brand.ps1 -Verify` exits 1 when `static/brand/` or `public/brand/` diverge from canonical
- **Site Build + Principles Gate** (`.github/workflows/site-principles-gate.yml`, every PR to `main`) — `bun run build` (TypeScript check + Vite build, zero TS errors) and `scripts/test/check-site-form-backend.py` (fails fake-success contact/brief forms)
- **Repository CI** (`.github/workflows/ci.yml`) — `ruff`, `mypy`, `pytest` (coverage ≥ 72%), Playwright e2e, `pwsh scripts/maintenance/lint-ecl.ps1`, security scan
- **Pre-commit hooks** — trailing-whitespace, end-of-file-fixer, check-yaml, `ruff`, `mypy`, `bandit`
- **Site test stack** — Vitest (`^5`) + Playwright (`^1.63`)

**Not configured (do not claim):** Storybook/Chromatic visual regression, axe-core CI, bundle-size monitoring. Visual QA today is `ls-artifact-qa` review + manual inspection; accessibility audits are manual/quarterly.

### Manual Review
- **Brand Review** — Creative Director reviews all new components (`ls-artifact-qa` gate on artifacts)
- **Accessibility Audit** — Quarterly full audit
- **Performance Profile** — Component render performance

---

*This document is the single source of truth for design. Canonical tokens live in `brand/tokens/`; `static/brand/` and `public/brand/` are mirrors managed by `scripts/build/sync-brand.ps1`; `src/brand/` is the application bridge. Update this document first, then propagate via the token-change procedure above.*

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-10-04 | Initial canonical design system per Directive | Creative Director |
| 1.1 | 2026-10-04 | Documentation audit: corrected type-scale px values, spacing/CSS token names (`--ls-space-*`, `--color-ls-*`), focus ring (2px), shadows (two real systems), component inventory (10 real components + verified props), package tree, Tailwind v4 CSS-first setup, and real QA/CI claims; added Token Source & Path Reconciliation, Known Token Divergences, Honesty Status Vocabulary, Logo Usage, Imagery & Media, and the token-change procedure | Technical Documentation Lead |
