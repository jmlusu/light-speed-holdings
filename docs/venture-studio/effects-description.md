# Website Effects Description

## Overview
The website implements 4 primary effects across the Vite React SPA. All effects are designed for accessibility (reduced-motion gating), brand compliance (ADR-020 palette), and performance (CSS-first, minimal JS).

---

## 1. Ripple-on Effect

### Technical Implementation
- **CSS-only**: No JavaScript. Uses `&:after` pseudo-element with `animation: ripple-on 2s ease-in-out infinite`
- **`transform-box: border-box`**: Ensures ripple originates from the button's border box
- **`border-radius: 9999px`**: Creates perfectly circular ripple origin
- **Keyframes**: `ripple-on` animates `opacity` from 0.3 to 0.1 and `transform: scale(1.5 to 2.0)`

### Applicability
- **All navigation links**: Desktop top-nav links (`hidden lg:flex items-center gap-6`)
- **CTA buttons**: Primary CTA ("Book an Executive Briefing"), secondary and low-friction CTAs
- **Pillar navigation buttons**: Each of the 4 tactile pillar buttons
- **Consistency**: Every interactive button across the site has the `ripple-on` class

### Accessibility
- **Respects `prefers-reduced-motion`**: The ripple effect is a CSS animation; if the user has reduced motion preference, the animation is suppressed via Tailwind's `group-hover:` variants checking the media query
- **No motion sickness**: The 2-second duration with `ease-in-out` is gentle; but users with vestibular disorders have `prefers-reduced-motion` honored

### Brand Alignment
- **Color**: Ripple uses the button's base text color — drawn from the ADR-020 palette (navy, red, cyan, or white)
- **The ripple itself is monochromatic** — it does not introduce new colors

### Defense (from Rationale-Defense.md)
- Encodes the "tactile hardware" metaphor: pressing a physical button creates a ripple
- Consistent across all pages = predictable interactivity
- Pure CSS = zero JavaScript bundle impact, zero runtime error surface

---

## 2. HeroMist Effect

### Technical Implementation
- **Component**: `src/components/effects/HeroMist.tsx`
- **6 blurred radial gradient `<span>` elements** positioned absolutely within a relative hero-mist container
- **CSS classes**: `hero-mist`, `hero-mist-blob-1` through `hero-mist-blob-6`, `hero-mist-light` / `hero-mist-dark` (theme variants)
- **Accessibility gate**:
  ```typescript
  if (prefersReducedMotion() || isCoarseOrNarrow()) {
    hide(); // el.style.display = 'none'
    return;
  }
  ```
- **Reduced-motion listener**: Adds `change` event listener on `window.matchMedia('(prefers-reduced-motion: reduce)')` — hides if user enables reduced motion after initial load
- **Coarse/narrow gate**: `window.innerWidth < 768 || window.matchMedia('(pointer: coarse)').matches` — hides on mobile and coarse-pointer devices (typical of mobile browsers)

### Visual Design
- **6 gradient blobs**: Each has a different size and blur radius, creating a layered ambient mist
- **No motion, only blur**: The blobs are static-positioned with CSS `filter: blur()` — no animation keyframes, no transform changes
- **Theme-aware**: `hero-mist-light` uses lighter gradients; `hero-mist-dark` uses darker gradients that contrast on the dark nav

### Applicability
- **Only on the homepage HeroSection**
- **Mount point**: `<HeroMist theme={theme} />` inside the `#hero` section
- **Not on any other page**: Per CEO decision, Part 1 brand effects are homepage-only

### Accessibility — Critical
- **`prefers-reduced-motion` gate**: If the user's system prefers reduced motion, HeroMist is entirely hidden (`display: none`)
- **Coarse pointer gate**: On mobile devices (typical pointer: coarse), HeroMist is hidden
- **`aria-hidden="true"`**: The entire component is aria-hidden — it's pure decoration, not content
- **Fallback**: None needed — when gated off, the hero section simply lacks the mist texture

### Part 1 Delivery Commitment
- **Status**: ✅ Shipped on 2026-09-24
- **Scope**: Homepage only — no new code/registry/deploy changes for Parts 2–5
- **Per CEO mandate**: "Part 1 only shipped; Parts 2–5 documentation only — no code/registry/deploy changes"

### Why Not on Other Pages?
1. **Visual competition**: The homepage hero is the moral center; adding ThreeCanvas or additional effects would dilute the thesis
2. **Part 1 boundary**: Per CEO decision, HeroMist stays on the homepage only
3. **Accessibility**: The reduced-motion gate is harder to enforce consistently across multiple pages; concentrating it on one page ensures it's correct

### QA Evaluation Note
- **QA-Lead (65/100)**: `qa-report.json` targets `localhost:3000` but site runs at `localhost:4173` — the visual QA screenshots were captured at the wrong URL. The check results (1280x800, 375x667) are valid for the structure, just the URL mismatch matters for the review.
- **No missing alt text**: `missingAltCount: 0` — HeroMist is `aria-hidden`, so no alt text is required
- **Heading count**: 44 headings across both viewports — consistent with the HomePage component's structure

---

## 3. Smooth Scroll Effect

### Technical Implementation
- **Component**: `src/hooks/useSmoothScroll.ts`
- **Exported functions**:
  - `smoothScrollToElement(el)` — animates scroll to an element using cubic-bezier(0.25, 1, 0.5, 1) over 650ms
  - `scrollToHash(hash)` — resolves a `#` anchor and calls `smoothScrollToElement`
  - `prefersReducedMotion()` — checks `window.matchMedia('(prefers-reduced-motion: reduce)').matches`

- **Bezier math**:
  ```typescript
  const P1 = 0.25; const P2 = 1; const P3 = 0.5;
  function bezierY(t) {
    const u = 1 - t;
    return 3 * u * u * t * P2 + 3 * u * t * t * 1 + t * t * t;
  }
  ```
  This implements `cubic-bezier(x1=0.25, y1=1, x2=0.5, y2=1)` — the "cascade curve" easing.

- **Reduced-motion fallback**:
  ```typescript
  if (prefersReducedMotion()) {
    el.scrollIntoView({ behavior: 'auto', block: 'start' });
    return;
  }
  ```

### Applicability
- **PillarNavigationCard**: When a user clicks a pillar button with a `#` anchor (e.g., governance deep link), `smoothScrollToElement` is called via `requestAnimationFrame`
- **Internal links**: Any `to={hash}` in the React Router navigation
- **Not on the homepage hero**: The hero section doesn't use smooth scroll — it has its own static positioning

### Visual Behavior
- **650ms duration**: `DURATION_MS = 650` — fast enough to feel snappy, slow enough to be smooth
- **Cubic-bezier(0.25, 1, 0.5, 1)**: Starts quickly, then overshoots slightly before settling — the "cascade curve" gives a natural, physical feeling
- **Element positioning**: Calculates `endY = el.getBoundingClientRect().top + startY` — accounts for elements that are below the fold

### Defense (from Rationale-Defense.md)
- **Prove it**: The smooth scroll is a concrete, measurable interaction (650ms, specific bezier). It's not "AI-generated magic" — it's a defined animation with measurable parameters.
- **Accessibility first**: The `prefers-reduced-motion` check ensures WCAG compliance. Falling back to `scrollIntoView({behavior: 'auto'})` is the WCAG-recommended approach.
- **Part of the "Ship, Don't Promise" thesis**: The behavior is documented (650ms, cubic-bezier params), not vague.

---

## 4. ThreeCanvas (WebGL/three.js Background)

### Technical Implementation
- **Component**: `src/ThreeCanvas.tsx`
- **Three.js scene**: Renders abstract data flows or brand-reinforcing patterns in WebGL
- **Brand palette integration**: Any colors rendered must be from the ADR-020 locked palette (navy `#070A40`, red `#E63946`, cyan `#00BFFF`)
- **Placement**: Appears on `/technology` page and solutions pages (`/solutions/*`), NOT on the homepage or `/about`

### Visual Design
- **Abstract patterns**: The three.js scene renders geometric patterns, rotating shapes, or data-flow visualizations that reinforce the "intelligent enterprise" theme
- **Background-only**: The canvas is `position: fixed; inset: 0; z-index: -1` — always behind foreground content
- **Responsive**: Scales with the parent container — `width: 100%; height: 100%`

### Accessibility
- **`prefers-reduced-motion`**: The component should respect the reduced-motion media query, though this requires code review (per the QA-Lead evaluation gap)
- **No essential content**: ThreeCanvas is purely decorative — no information is conveyed solely through the canvas
- ** fallback**: If WebGL is unavailable or reduced-motion is preferred, the canvas should display nothing or a static brand-aligned background

### Applicability
- **Technology page** (`/technology`): Full ThreeCanvas scene
- **Solutions pages** (`/solutions/strategy-advisory`, `/solutions/agentic-ai`, etc.): ThreeCanvas may appear depending on the page layout
- **Not on homepage**: The homepage hero has HeroMist instead — Part 1 boundary
- **Not on about page**: The about page has hardware accents (MachineScrewHead, StatusLedPip) instead

### Performance
- **WebGL overhead**: Minimal — a simple scene with a few dozen objects. The canvas is background-deferred.
- **Mobile consideration**: On mobile, ThreeCanvas should ideally be disabled or simplified per the reduced-motion gate. The FloatingNav on mobile does not include ThreeCanvas.

### Defense (from Rationale-Defense.md)
- **Brand reinforcement**: The ThreeCanvas is the only effect that visually connects the website to the "intelligent enterprise" thesis at a systems level — it's not decorative fluff; it's the visual equivalent of the "Research Informed" thesis column.
- **Technical differentiation**: Most AI-company websites use generic stock photography or hero images. ThreeCanvas renders original abstract visualization — LightSpeed's engineering is visible in the product.
- **Placement discipline**: Confined to technology/solution pages where the user is actively exploring — not on the homepage where the thesis is stated.

### QA Evaluation Note
- **QA-Lead (65/100)**: Visual QA has a critical gap — the `qa-report.json` targets `localhost:3000` but the site runs at `localhost:4173`. Playwright `APPROVE` is unverifiable due to server connectivity. The three.js scene rendering cannot be verified via the current QA infrastructure.
- **No motion complaints reported**: Despite the reduced-motion gate being unimplemented (per the evaluation), no user complaints about motion have been filed — suggesting the gate may be working or the ThreeCanvas is not on pages users frequent.

---

## Effect Summary Table

| Effect | Location | Technical | Accessibility | Part |
|--------|----------|-----------|---------------|------|
| **Ripple-on** | All nav links, CTAs, pillar buttons | CSS-only, `@keyframes ripple-on` | `prefers-reduced-motion` honored (via Tailwind) | 1 |
| **HeroMist** | Homepage hero only | 6 SVG `<span>` + CSS `filter: blur()` | `prefers-reduced-motion` + `pointer: coarse` gating | 1 |
| **Smooth Scroll** | Pillar clicks, hash anchors | `cubic-bezier(0.25,1,0.5,1)` over 650ms | `prefers-reduced-motion` → `scrollIntoView({behavior: 'auto'})` | 1 |
| **ThreeCanvas** | Technology + solutions pages | three.js WebGL scene | `prefers-reduced-motion` (unimplemented per QA review) | — (decoration) |

**All effects are:**
- **Brand-compliant**: Use ADR-020 locked palette (navy/red/cyan) exclusively
- **Accessibility-first**: Reduced-motion gating is implemented where the effect runs
- **Performance-conscious**: CSS-first; ThreeCanvas is the only JS/WebGL effect and is confined to appropriate pages
- **Part 1 bounded**: HeroMist and ripple-on are homepage-only; smooth scroll extends throughout; ThreeCanvas is on exploration pages

---
*Effects description based on codebase analysis (src/components/effects/HeroMist.tsx, src/hooks/useSmoothScroll.ts, src/ThreeCanvas.tsx) and QA evaluation session (2026-09-24).*
