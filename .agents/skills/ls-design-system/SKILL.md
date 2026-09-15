---
name: ls-design-system
description: "The LightSpeed Holdings brand design system. MUST be loaded before any creative production work (websites, decks, documents, social media, ads, diagrams, infographics). Enforces brand tokens (navy #070A40 / red #E63946 / cyan #00BFFF, Arial type scale, 4px spacing grid), logo rules, and template usage so every artifact is on-brand. Referenced by every ls-* creative skill. Trigger on: 'use the LightSpeed brand', 'design system', 'brand tokens', 'on-brand', 'match our branding', 'make it look like LightSpeed'."
---

# LightSpeed Design System

The single source of truth for creating on-brand LightSpeed Holdings artifacts.

## When To Use

- ANY creative or visual production, regardless of artifact type
- Checking brand compliance of an existing artifact
- Before invoking `ls-creative-director`, `ls-frontend-design`, `ls-presentation-design`, `ls-document-design`, `ls-social-media-design`, `ls-brand-advertising`, `ls-diagramming`, `ls-visual-storytelling`
- The **first** thing you load for creative work — never create visual output without it

## Canonical References

| Asset | Path |
|-------|------|
| Brand tokens (JSON) | `brand/tokens/brand-tokens.json` |
| Brand tokens (CSS) | `brand/tokens/brand-tokens.css` |
| Brand guidelines (this system) | `brand/guidelines/brand-guidelines.md` |
| Quick reference | `static/brand/BRAND_GUIDELINES.md` |
| Logo suite | `static/brand/logos/**` |
| Pre-built templates | `static/brand/templates/**` |
| Template generators | `static/brand/templates/generate-*.py` |

## Core Tokens (Memorize These)

### Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#070A40` | Primary surfaces, headlines, slide rails, logo text |
| Red | `#E63946` | Accent — CTAs, highlights, signal waves, key results |
| Cyan | `#00BFFF` | Accent — shield base, links on dark, taglines on navy |
| Light Grey | `#F2F2F2` | Backgrounds, cards, callouts |
| White | `#FFFFFF` | Clean backgrounds, text on navy |
| Dark Grey | `#6B7280` | Secondary text, captions |
| Light Text Grey | `#9CA3AF` | Tertiary text on dark surfaces |

~80% navy / 10% red / 10% cyan on brand-dominant surfaces. Accents are accents — never let them overpower navy.

### Typography

- Display/headings: **Arial 700**. Body: **Arial 400**.
- Type scale (pt): 36 display-xl, 32 title-xl, 28 title-lg, 24 title-md, 18 title-sm, 16 subtitle/body-lg, 14 body, 13 body-sm, 12 caption.
- Do not invent sizes outside the scale.

### Spacing & Grid

- Base unit 4px; scale: 4/8/12/16/24/32/48/64/96.
- Web: 12-col grid, 24px gutter, 48px margin, max width 1200px.
- Slides: 10in × 7.5in; navy left rail 0.15in on content slides.
- Radius: 4px small / 8px medium / 16px large.

## Logo Rules (Never Break)

1. **Never recreate the logo** — always use official files in `static/brand/logos/`.
2. Never stretch, rotate, distort, or recolor the logo.
3. Clear space = 1× "L" height on all sides.
4. Vector (SVG/PDF/EPS) for print; transparent PNG on dark backgrounds.
5. `™` on first mention: "LightSpeed Holdings Limited™".
6. Tagline spelled exactly: **ASPIRE. ACT. ACHIEVE.**

| When | Use |
|------|-----|
| Headers/covers/light backgrounds | `logos/fulllogo/fulllogo.png` |
| Dark backgrounds/overlays | `logos/fulllogo/fulllogo_transparent.png` |
| Avatars/favicons/small spaces | `logos/icononly/icononly.png` |
| Print | `logos/fulllogo/vector/print.svg` (or PDF/EPS) |
| Legal/B&W | `logos/grayscale/grayscale.png` |

## Pre-Built Templates (Prefer Over Building From Scratch)

For decks, documents, and social assets, start from the branded templates in `static/brand/templates/`:

| Template | Generator |
|----------|-----------|
| Pitch deck (13 slides) | `generate-pitch-deck.py` |
| Board meeting (9 slides) | `generate-board-meeting.py` |
| Social assets | `generate-social-assets.py` |
| One-pager / investor update / email signatures | `.html` files |

Pattern used by the generators: white slides with a navy left rail, navy section titles (28pt bold), red accent divider under cover titles, cyan taglines on navy covers.

## Dashboard Exception

The CEO Dashboard (`src/ai_company/dashboard/`) uses the J.A.R.V.I.S. theme with the "LS" placeholder. It is **internal** and NOT public-facing brand — do NOT rebrand it. This is the only sanctioned off-brand surface.

## Workflow

1. Load `brand/tokens/brand-tokens.json` (authoritative) — or read `brand/guidelines/brand-guidelines.md` for the human-readable rules.
2. Decide which branded template/generator to start from, if any.
3. Produce the artifact using the tokens above — no off-palette colors, no invented type sizes, no recreated logo.
4. Hand the artifact to `ls-artifact-qa` for brand + visual QA before delivery.

## On-Brand Confidence Check

- [ ] Colors resolve to `brand-tokens.json` values only
- [ ] Logo is an official asset (path under `static/brand/logos/`)
- [ ] Type sizes are on the brand scale
- [ ] Spacing follows the 4px base scale
- [ ] Template used where one exists
- [ ] `™` on first mention; tagline correct
