# Social-Card & Favicon Bundle Spec (Ticket #380)

**Generated**: 2026-10-01  
**Base**: LightSpeed Holdings Brand Design System  
**Compliance**: `ls-design-system` enforced; `ls-artifact-qa` gate required

---

## 1. Social Card Specification

### 1.1 Dimensions
- **Open Graph image**: 1200 × 630 px (minimum) — primary sharing preview
- **Twitter Card summary large image**: 1200 × 628 px — X/Twitter preview
- **Canvas**: 1200 px wide × 630 px high; 4 px base grid throughout

### 1.2 Color Palette (Brand Tokens, `brand/tokens/brand-tokens.json`)
| Token | Hex | Usage | Coverage per Brand Rules |
|-------|-----|---------|--------------------------|
| Navy | `#070A40` | Primary background, dominant surface | ~80% of visible canvas |
| Red | `#E63946` | Accent — CTAs, highlights, signal waves | ~10% of visible canvas |
| Cyan | `#00BFFF` | Accent — shield base, links on dark, taglines on navy | ~10% of visible canvas |
| White | `#FFFFFF` | Text on navy, clean backgrounds | As needed for contrast |

### 1.3 Logo Usage
- **Primary logo variant for social cards**: **Icon-only logo** — **MANDATORY**
  - Source: `static/brand/logos/icononly/icononly.png` (canonical); mirror at `static/brand/logos/icononly/`
  - Clear space: 1× "L" height on all sides (per brand guidelines §4)
  - Minimum display width: 40 px at 1200×630 canvas scale
  - Position: top-left, aligned to 4px grid, 32 px margin from top and left edges
  - Transparent PNG — renders correctly on navy background
- **Logo usage rules** (never break):
  1. Never recreate the logo — always use official assets
  2. Never stretch, rotate, distort, or recolor the logo
  3. Clear space = 1× "L" height on all sides
  4. Vector (SVG/PDF/EPS) for print; transparent PNG on dark backgrounds
  5. `™` on first mention: "LightSpeed Holdings Limited™"
  6. Tagline spelled exactly: "ASPIRE. ACT. ACHIEVE."

### 1.4 Typography
- **Typeface**: Arial, sans-serif stack (web-safe)
- **Type scale (pt)**:
  - 32 title-xl (primary heading)
  - 24 title-lg (secondary heading)
  - 18 body (body text)
  - 14 body-sm (small body)
- **Hierarchy on social card** (1200 × 630 px canvas):
  - **Line 1** (32pt title-xl, white `#FFFFFF`): "LightSpeed Holdings Limited™"
  - **Line 2** (18pt body, white `#FFFFFF`): Tagline "ASPIRE. ACT. ACHIEVE."
  - **Line 3** (14pt body, navy `#070A40` or cyan `#00BFFF` accent): Brief descriptive text, max 20 words
- **Text color rules**:
  - White on navy background (#070A40)
  - Navy on cyan accents
  - White on red CTA buttons

### 1.5 Layout & Grid (4px base unit, 1200 × 630 px canvas)
- **Overall structure** (4 px grid throughout):
  - Top margin: 32 px (8 grid units)
  - **Logo area**: 40 px wide × 40 px tall (10 × 10 grid units), positioned at (32, 32) from top-left
  - **Title area**: 32 px below logo bottom, full width, no gutter needed for single-line title
  - **Tagline area**: 24 px below title, centered, 48 px from left/right edges (12 grid units each side)
  - **Description text**: below tagline, left-aligned, max 60 characters per line, line-height 1.5, 4 px line spacing
  - Bottom margin: 32 px (8 grid units)
- **Grid alignment**: All major elements aligned to 4 px grid; spacing between elements follows 4/8/12/16/24/32/48 px scale (per brand guidelines §5)
- **White space**: Deliberate negative space; no element touches another without ≥8 px margin

### 1.6 Copy Voice (per Company Voice Guidelines, `brand/guidelines/brand-guidelines.md`)
- **No emojis** (per company voice §6)
- **No hype** (per company voice §6)
- **Evidence-led** (per company voice §6)
- **Builder register** tone
- **First mention of company name**: "LightSpeed Holdings Limited™" (with ™, per guidelines §2)
- **Tagline**: "ASPIRE. ACT. ACHIEVE." — spelled exactly, per guidelines §2
- **Every claim must have a source** (registry, results, published Pharos artifact). Never invent stats.
- **Hashtags**: focused set of 3–5; if included, use light font size at bottom of card, desaturated if on navy

### 1.7 CTA (Call to Action)
- For the specification document: **n/a** (this is a spec, not a publishable asset)
- If rendered as actual social media asset: single primary CTA, visually distinct (red `#E63946` accent on navy background), positioned at bottom-right, 48 px from right and bottom edges, 32 px minimum width, white text on red background

### 1.8 Brand Compliance Checklist (pre-QA)
- [ ] Navy `#070A40` is the dominant background color (~80% coverage)
- [ ] Red `#E63946` used as accent only (~10% coverage)
- [ ] Cyan `#00BFFF` used as accent only (~10% coverage)
- [ ] White `#FFFFFF` used for text on navy background
- [ ] Icon-only logo from `static/brand/logos/icononly/` (never recreated)
- [ ] Clear space respected (1× "L" height on all sides)
- [ ] Arial type scale used exclusively
- [ ] Type sizes from brand scale only (no invented sizes)
- [ ] "LightSpeed Holdings Limited™" on first mention with ™
- [ ] Tagline "ASPIRE. ACT. ACHIEVE." exact spelling
- [ ] 4px grid alignment throughout
- [ ] No off-palette colors
- [ ] No invented type sizes
- [ ] No logo distortion or recreation

---

## 2. Favicon Specification

### 2.1 Required Favicon Assets
| Asset | Size(s) | Format | Transparency | Usage |
|-------|---------|--------|--------------|-------|
| `favicon.ico` | 16×16, 32×32, 48×48 | ICO container | Mixed (some transparent) | Standard browser tab icon |
| `favicon.png` | 32×32 | PNG | Yes | Modern browser support |
| `apple-touch-icon.png` | 180×180 | PNG | Yes | iOS Safari home screen |
| `android-chrome-192x192.png` | 192×192 | PNG | Yes | Android Chrome |
| `android-chrome-512x512.png` | 512×512 | PNG | Yes | Android Chrome (high-DPI) |

### 2.2 Color Treatment
- All favicon assets use **navy `#070A40`** as primary color
- **Icon-only logo** from `static/brand/logos/icononly/` scaled and cropped to each size
- No red or cyan coloring at these sizes (details lose clarity below 32 px)
- If any color is visible at 16 px, limit to navy only for maximum recognizability
- Transparent background where supported (all listed formats)

### 2.3 Favicon Implementation (HTML)
```html
<!-- Standard favicon -->
<link rel="icon" href="/favicon.ico" type="image/x-icon">

<!-- PNG favicon for modern browsers -->
<link rel="icon" href="/favicon.png" type="image/png">

<!-- Apple touch icon -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<!-- Android Chrome -->
<link rel="icon" sizes="192x192" href="/android-chrome-192x192.png">
<link rel="icon" sizes="512x512" href="/android-chrome-512x512.png">
```

### 2.3 Brand Compliance Checklist (favicon)
- [ ] All favicon assets use navy `#070A40` as primary color
- [ ] Icon-only logo from `static/brand/logos/icononly/` is the visual element
- [ ] No off-palette colors (red/cyan excluded at small sizes for clarity)
- [ ] Transparent background where format supports it
- [ ] All five asset types listed above are present
- [ ] File names follow convention: `favicon.ico`, `favicon.png`, `apple-touch-icon.png`, `android-chrome-192x192.png`, `android-chrome-512x512.png`
- [ ] URLs are absolute or properly rooted for the deployment domain

---

## 3. Production Chain

```
ls-creative-director (brief intake)
    ↓
ls-design-system (brand tokens, logo rules, color palette, type scale — MANDATORY first)
    ↓
ls-social-media-design (social card visual generation per spec above)
    ↓
brand-extract (favicon generation, og:image, twitter:image metadata extraction)
    ↓
ls-artifact-qa (full QA: visual/brand/UX/accessibility/content — runs LAST)
    ↓
Generator: company-registry.yaml → Jinja2 template → .opencode/agents/*.md + company/*.yaml
```

---

## 4. QA Checklist (ls-artifact-qa)

See `ls-artifact-qa` skill for full five-pass checklist. Key highlights for this spec:

### Visual QA
- [ ] Horizontal overflow: 0 px at 1280 px viewport
- [ ] Spacing consistent with 4 px grid scale
- [ ] Hierarchy: one dominant element (navy background); reading order obvious
- [ ] Balance: navy dominant, red/cyan accents as specified
- [ ] Whitespace: deliberate negative space, not wall of content
- [ ] Alignment: all elements grid-aligned to 4 px

### Brand QA
- [ ] Palette: navy #070A40 / red #E63946 / cyan #00BFFF / white ONLY
- [ ] Logo: official icon-only from `static/brand/logos/icononly/`
- [ ] Type: Arial scale only, sizes from brand palette
- [ ] "LightSpeed Holdings Limited™" on first mention with ™
- [ ] Tagline "ASPIRE. ACT. ACHIEVE." exact spelling
- [ ] No off-palette colors, no invented type sizes

### UX QA
- [ ] CTA clarity (if applicable): one primary action visible
- [ ] No horizontal scroll at 375 px viewport
- [ ] Tap targets ≥ 44 px where interactive elements exist
- [ ] Responsive: layout graceful at mobile dimensions

### Accessibility QA
- [ ] Contrast: body text ≥ 4.5:1 (white on navy passes); headings ≥ 3:1
- [ ] Alt text: descriptive for icon-only logo (deploy via og:image `alt` attribute)
- [ ] Semantic heading order: h1 → h2 → h3, no skips
- [ ] Color not the only signal (labels accompany any color coding)

### Content QA
- [ ] Claims/citations traceable — no invented statistics
- [ ] Names/spelling: "LIGHTSPEED HOLDINGS LIMITED", tagline exact
- [ ] Grammar/typos: clean
- [ ] Voice: builder register, no emojis, no hype, no generic AI commentary

---

## 5. Generated Artifacts

Upon full stack execution (brief → design → QA → generator), the following will be produced:

1. **`.opencode/agents/*.md`** — OpenCode-compatible agent cards (mode: subagent, permission: blocks)
2. **`company/*.yaml`** — Generated from `company-registry.yaml` registry
3. **`brand/digital/social-card.png`** — 1200×630 px social card (PNG, navy background, icon-only logo, Arial type, 4px grid)
4. **`brand/digital/favicon/**`** — All five favicon assets (ico, png, apple-touch, android-chrome)
5. **`reports/qa-audit-<date>.md`** — ls-artifact-qa verdict report (APPROVE or FIX)
6. **`imagery/og-image.png`** and **`imagery/twitter-image.png`** — Open Graph and Twitter Card images

---

*This spec enforces LightSpeed Holdings brand design system (v1.0.1) across all social and browser touchpoints. Non-compliant artifacts will be rejected by ls-artifact-qa and returned for FIX → RENDER AGAIN → APPROVE loop.*