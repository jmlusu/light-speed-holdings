---
name: ls-design-system
description: "The LightSpeed Holdings brand design system. MUST be loaded before any creative production work (websites, decks, documents, social media, ads, diagrams, infographics). Enforces brand tokens (navy #070A40 / red #DC3641 / cyan #00BFFF, Arial type scale, 4px spacing grid), logo rules, template usage, and the imagery policy (AI imagery permitted on non-person surfaces; generated people and avatars prohibited). Referenced by every ls-* creative skill. Trigger on: 'use the LightSpeed brand', 'design system', 'brand tokens', 'on-brand', 'match our branding', 'make it look like LightSpeed'."
---

# LightSpeed Design System

The single source of truth for creating on-brand LightSpeed Holdings artifacts.

## When To Use

- ANY creative or visual production, regardless of artifact type
- Checking brand compliance of an existing artifact
- Before invoking `ls-creative-director`, `ls-frontend-design`, `ls-presentation-design`, `ls-document-design`, `ls-social-media-design`, `ls-brand-advertising`, `ls-diagramming`, `ls-visual-storytelling`
- The **first** thing you load for creative work — never create visual output without it

## Canonical References

**Canonical source of truth is `brand/**` (repo root).** `static/brand/**` and
`public/brand/**` are runtime mirrors — never hand-edit assets there, and never
read old versions from them for new work. See `brand/CANONICAL_SOURCES.md`.
Run `pwsh scripts/build/sync-brand.ps1` after changing a canonical asset so mirrors
pick it up.

| Asset | Canonical path | Mirror copy |
|-------|----------------|-------------|
| Brand tokens (JSON) | `brand/tokens/brand-tokens.json` | **canonical-only — not mirrored** (deleted 2026-10-13; loaded once via `src/index.css`) |
| Brand tokens (CSS) | `brand/tokens/brand-tokens.css` | **canonical-only — not mirrored** (deleted 2026-10-13; loaded once via `src/index.css`) |
| Brand guidelines (this system) | `brand/guidelines/brand-guidelines.md` | `static/brand/guidelines/brand-guidelines.md` |
| Quick reference | `brand/CANONICAL_SOURCES.md` | `static/brand/BRAND_GUIDELINES.md` |
| Logo system | `brand/logo/**` | `static/brand/logo/**` |
| Print masters | `brand/print/**` | `static/brand/print/**` |
| Digital/social covers | `brand/digital/**` | `static/brand/digital/**` |
| Pre-built templates | `static/brand/templates/**` | mirror-only (no canonical) |
| Template generators | `static/brand/templates/generate-*.py` | mirror-only (no canonical) |

## Core Tokens (Memorize These)

### Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#070A40` | Primary surfaces, headlines, slide rails, logo text |
| Red | `#DC3641` | Accent — CTAs, highlights, signal waves, key results (WCAG AA value; not `#E63946`) |
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

1. **Never recreate the logo** — always use official files in `brand/logo/` (canonical; mirrors at `static/brand/logo/` and `public/brand/logo/`).
2. Never stretch, rotate, distort, or recolor the logo.
3. Clear space = 1× "L" height on all sides.
4. Vector (SVG/PDF/EPS) for print; transparent PNG on dark backgrounds.
5. `™` on first mention: "LightSpeed Holdings Limited™".
6. Tagline spelled exactly: **ASPIRE. ACT. ACHIEVE.**

Select the variant by background, then take the `.svg` sibling for print:

| When | Use (all in `brand/logo/`) |
|------|----------------------------|
| Headers, covers, light/white backgrounds | `logo-full.png` |
| Dark or navy backgrounds | `logo-light-bg.png` |
| Darker textured backgrounds | `logo-dark-bg.png` |
| Square crops, social avatars, round placements | `logo-avatar.png` |
| Bare speed-mark where the wordmark is already present | `logo-mark.png` |
| Single-colour, embossing, one-colour print | `logo-mark-mono.png` |
| Browser tabs, small favicons | `logo-favicon.png` |
| Social/OG share cards (1200×630) | `logo-og.png` |

The variants are not interchangeable across backgrounds. Opaque bases are tuned to a canvas:
`logo-full` for light/white, `logo-light-bg` for dark/navy, `logo-dark-bg` for darker textures.
`-transparent` twins inherit the artwork's ink, so `logo-full-transparent`, `logo-og-transparent`
and `logo-dark-bg-transparent` are white and usable on dark only;
`logo-light-bg-transparent` and `logo-mark-mono-transparent` are navy and usable on light only;
`logo-mark-transparent`, `logo-avatar-transparent`, `logo-favicon-transparent` and
`logo-no-background` are mark-only and work on both. Full table, transparent variants and the
clear-space rule live in `brand/guidelines/brand-guidelines.md` § 3.

## Imagery Policy (Never Break)

Governed by [`docs/adr/027-ai-generated-imagery-policy.md`](../../../docs/adr/027-ai-generated-imagery-policy.md).

1. **AI-generated imagery is permitted** on every non-person surface — hero backdrops, infrastructure, product surfaces, environment and geometry, abstract data, textures, conceptual illustration — in any artifact: website, dashboard, deck, video, document, social, ad, diagram, infographic.
2. **Generated people, faces, figures and avatars are prohibited.** No synthetic person, no invented persona icon. Human imagery is only real, consented, commissioned photography holding a model or property release.
3. **Using the official `icononly` logo as a profile avatar is a logo use, not generated imagery** — permitted, and the only sanctioned avatar substitute.
4. **Vendors** must be allow-listed in `docs/APPROVED-VENDORS.md`; prompts are subject to the third-party transmission ban in `docs/SKILL_CURATION_POLICY.md`.
5. **Palette gate differs by asset class.** Flat graphic output (diagram, brand-mark, vector, flat illustration) must pass exact-match `--tolerance 3`. Continuous-tone output (generated photographic/raster illustration) is checked for brand-token presence and dominant-colour compliance — navy dominant, red/cyan as accents.
6. **Provenance is recorded** — generated rasters are typed `illustration` with `generated: true`, never `screenshot`. Raw model output is not an asset until post-processed to the palette.
7. **Composition** follows §Art Direction: authentic African context, no stereotypical poverty imagery, no stock-photo smiles, no posed headshot grids, cyan/red as light and signal only.

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
- [ ] Logo is an official asset (path under `brand/logo/`)
- [ ] Type sizes are on the brand scale
- [ ] Spacing follows the 4px base scale
- [ ] Template used where one exists
- [ ] Imagery policy respected — no generated people or avatars; vendors allow-listed; provenance recorded
- [ ] `™` on first mention; tagline correct
