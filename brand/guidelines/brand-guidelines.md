# LightSpeed Holdings Brand Guidelines

**Version:** 1.0.1
**Source of truth:** `brand/tokens/brand-tokens.json` (machine-readable), `brand/tokens.md` (human-readable overview), `static/brand/BRAND_GUIDELINES.md` (quick reference).
**Owner:** Brand Strategist / CMO.
**Applies to:** All public-facing and operational touchpoints. Agents creating any artifact (website, deck, document, social post, ad, diagram, infographic) MUST load the `ls-design-system` skill before producing creative output.

---

## 1. Brand Identity

| Element | Value |
|---------|-------|
| **Company Name** | LIGHTSPEED HOLDINGS LIMITED |
| **Tagline** | ASPIRE. ACT. ACHIEVE. |
| **Trademark** | Use `™` on first mention: "LightSpeed Holdings Limited™" |
| **Logo Symbol** | Lighthouse/shield emblem with signal waves |

## 2. Color System

| Token | Hex | Usage |
|-------|-----|-------|
| `navy` | `#070A40` | Headlines, logo text, primary brand surfaces, slide rails |
| `red` | `#E63946` | Signal waves, accent elements, CTAs, key highlights |
| `cyan` | `#00BFFF` | Shield base, accent elements, links on dark, taglines on navy |
| `grey-light` | `#F2F2F2` | Backgrounds, cards, callout boxes |
| `white` | `#FFFFFF` | Clean backgrounds, text on navy |
| `grey-dark` | `#6B7280` | Secondary text, captions |
| `grey-light-text` | `#9CA3AF` | Tertiary text on dark surfaces |

### Color Rules
- Navy is the dominant brand color. Red and cyan are accents — use sparingly (approximately 80/10/10 navy/red/cyan on brand-dominant surfaces).
- On navy surfaces, text is white; on cyan surfaces, text is navy; on red surfaces, text is white.
- Do NOT add new colors without a documented brand decision. Off-palette colors invalidate brand compliance.

## 3. Logo Usage

**Canonical location: `brand/logo/`** (8 variants, each in SVG + PNG; runtime mirrors at `static/brand/logo/` and `public/brand/logo/`). The logo artwork uses its own palette distinct from the UI tokens (navy `#02062F`, speed gradient `#01AFFD`→`#01DFFD`, red `#FD0231`–`#FD315D`) — this is an approved exception (ADR-027). Select the variant by background:

### Variants
| Variant | File (in `brand/logo/`) | Use For |
|---------|-------------------------|---------|
| Full Logo | `logo-full.png` / `logo-full.svg` | Light/white backgrounds — headers, covers, presentations |
| Full Logo (light bg) | `logo-light-bg.png` / `.svg` | Dark or navy backgrounds — wordmark + tagline tuned for contrast |
| Full Logo (dark bg) | `logo-dark-bg.png` / `.svg` | Darker textured backgrounds |
| Mark | `logo-mark.png` / `.svg` | Bare speed-mark where the wordmark is already present |
| Mark (mono) | `logo-mark-mono.png` / `.svg` | Single-colour contexts, embossing, one-colour print |
| Avatar | `logo-avatar.png` / `.svg` | Square crops, social avatars, round placements |
| Favicon | `logo-favicon.png` / `.svg` | Browser tabs, small favicons |
| Open Graph | `logo-og.png` / `.svg` | 1200×630 social/OG share cards |

### Transparent variants
Every concept also ships transparent. The rule used: a transparent twin exists only
where the base file was opaque, so `dark-bg`, `light-bg`, `mark` and `mark-mono`
have no `-transparent.svg` — their SVGs never carried a background.

| Transparent file | Size | Wordmark colour | Usable on |
|------------------|------|-----------------|-----------|
| `logo-full-transparent.svg` / `.png` | 1254² | white | dark only |
| `logo-og-transparent.svg` / `.png` | 1200×630 | white | dark only |
| `logo-dark-bg-transparent.png` | 1254² | white | dark only |
| `logo-light-bg-transparent.png` | 1254² | navy `#070A40` | light only |
| `logo-avatar-transparent.svg` / `.png` | 1024² | mark only | light and dark |
| `logo-favicon-transparent.svg` / `.png` | 512² | mark only | light and dark |
| `logo-mark-transparent.png` | 609×388 | mark only | light and dark |
| `logo-mark-mono-transparent.png` | 609×388 | navy `#070A40` | light only |
| `logo-no-background.svg` / `.png` | 1024² | mark only | light and dark |

`logo-mark-mono-transparent.png` is navy-filled, so it disappears on a navy
background. There is no white mono mark yet; add `logo-mark-mono-white.svg` if
one is needed.

Note: the table above describes `logo-full` as being for light/white backgrounds
and `logo-light-bg` for dark or navy backgrounds. Measured from the pixels this
is the other way round — `logo-full` is a white wordmark on a navy canvas, and
`logo-light-bg` is a navy wordmark on a light canvas. The transparent-variant
table is the pixel-verified one; treat the rows above with that in mind.

### Archived Legacy Suite
The legacy lighthouse-in-shield suite (`fulllogo`, `icononly`, `textonly`, `grayscale`) is **retired** and lives only in `.archive/legacy-logo-suite-2026-10-23/`. Do not reference it in any live artifact. Style explorations are in `.archive/brand/logos/`.

### Rules
1. **Never** recreate the logo — always use official assets.
2. **Never** stretch, rotate, or distort the logo.
3. **Never** change logo colors.
4. **Always** maintain clear space — 1× "L" height on all sides.
5. **Always** use vector (SVG/PDF/EPS) for print.
6. **Always** use transparent PNGs on non-white backgrounds.
7. **Always** use `™` on first mention.

### Minimum Sizes
| Context | Full Logo | Icon Only |
|---------|-----------|-----------|
| Print | 30mm wide | 12mm wide |
| Screen | 120px wide | 32px wide |

## 4. Typography

- **Display / Headings:** Arial 700 (fallback to sans-serif stack on web).
- **Body:** Arial 400.
- **Captions / Secondary:** Arial 400, `grey-dark`.
- Use the type scale in `brand-tokens.json` (`title-xl` 32pt through `caption` 12pt). Do not invent headline sizes outside the scale.

## 5. Layout

- **Slides (PPTX):** 10in × 7.5in (4:3) unless a 16:9 brief overrides; a navy rail (0.15in) runs down the left edge of content slides (see `static/brand/templates/generate-pitch-deck.py`).
- **Web:** 12-column grid, 24px gutter, 48px margin, max content width 1200px.
- **Spacing:** base unit 4px; use the scale 4/8/12/16/24/32/48/64/96.

## 6. Voice

- Tagline voice: **ASPIRE. ACT. ACHIEVE.** — confident, builders' register, no hype.
- Public content: professional, evidence-led, no emojis, no generic AI commentary.
- Pharos thought-leadership: builder-advocate voice — lead with proof, then principle (see Pharos skills).

## 7. Templates (Pre-Built)

| Template | Path | Use For |
|----------|------|---------|
| Pitch deck (13 slides) | `static/brand/templates/pitch-deck.pptx` | Investor pitches |
| Board meeting (9 slides) | `static/brand/templates/board-meeting.pptx` | Board meetings |
| Pitch deck generator | `static/brand/templates/generate-pitch-deck.py` | Programmatic decks |
| Board generator | `static/brand/templates/generate-board-meeting.py` | Programmatic decks |
| Social assets generator | `static/brand/templates/generate-social-assets.py` | Social creatives |
| One-pager | `static/brand/templates/one-pager.html` | One-page summaries |
| Investor update email | `static/brand/templates/investor-update-email.html` | Investor comms |
| Email signature (team) | `static/brand/templates/email-signature-team.html` | Email signatures |

## 8. Exceptions

- **CEO Dashboard:** uses the internal J.A.R.V.I.S. theme with the "LS" placeholder. Internal only — do NOT rebrand the dashboard.
- **Case-by-case:** any deviation requires a documented brand decision approved by the Brand Strategist / CMO.

## 9. Compliance Checklist

- [ ] Logo from official assets, never recreated
- [ ] Logo clear space respected
- [ ] Only palette colors used
- [ ] Vector format for print, transparent PNG on dark
- [ ] `™` on first mention of company name
- [ ] Type sizes from the brand scale
- [ ] Tagline spelled exactly "ASPIRE. ACT. ACHIEVE."
