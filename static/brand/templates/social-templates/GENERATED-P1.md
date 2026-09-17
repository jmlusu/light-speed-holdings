# P1 Foundational Social Post Templates — Generated Set (Ticket #311)

Six foundational P1 social post templates, generated from the brand system
(tokens + official logo) with **real LightSpeed copy** sourced from
`docs/Pharos/positioning.md` and the brand tokens. No lorem ipsum.

- **Generator**: `static/brand/templates/generate-post-templates.py` (Pillow-only, no API keys)
- **Outputs**: `static/brand/social/templates/*.png` (canonical file names below)
- **Spec source**: `static/brand/templates/social-templates/TEMPLATE_SPECS.md`

> See also: [P2/P3 Secondary Social Post Templates](GENERATED-P2-P3.md) (Ticket #316) — the generator now emits all 12 types (#1–6 here, #7–12 there).

## Templates

| # | Canonical file | Dims | Surface | Slots exposed |
|---|----------------|------|---------|---------------|
| 1 | `linkedin-carousel-cover.png` | 1080×1080 | navy | `title`, `subtitle`, `tagline` |
| 2 | `youtube-thumbnail.png` | 1280×720 | navy (subtle gradient) | `badge`, `title`, `tagline` |
| 3 | `reels-shorts-cover.png` | 1080×1920 | navy | `hook`, `tagline` |
| 4 | `quote-card.png` | 1080×1080 | navy | `quote`, `author`, `role`, `tagline` |
| 5 | `stat-card.png` | 1080×1080 | white | `number`, `label`, `context`, `source`, `tagline` |
| 6 | `thread-header.png` | 1200×675 | navy | `title`, `subtitle`, `part`, `tagline` |

## Regeneration

```powershell
# All six templates
uv run python static/brand/templates/generate-post-templates.py

# Self-QA after generating (dimensions + dominant brand fills)
uv run python static/brand/templates/generate-post-templates.py --verify

# One template with copy injection
uv run python static/brand/templates/generate-post-templates.py `
  --template quote-card `
  --slots '{"quote": "New quote", "author": "Jane Doe"}'

# Slots for several templates from a JSON file
# {"stat-card": {"number": "20"}, "thread-header": {"part": "3/8"}}
uv run python static/brand/templates/generate-post-templates.py --json params.json
```

`--slots` requires `--template`. `--outdir` overrides the default output
directory. No source change is required to swap copy — every text field is a
slot.

## Design decisions (documented)

- **1pt:1px rasterization** for the type scale (Canva/Figma grids render to
  pixels on these grids).
- **48px brand rail**: on navy surfaces the rail edge is marked by a 4px cyan
  accent line (`_rail_on_navy`); on the white stat card the rail is a solid
  navy 48px block (`_rail_on_white`). Content sits at a 64px inset (48px rail +
  16px gap).
- **YouTube overlay safety**: title confined to the left content column;
  play button centered at (900, 360) r=32 — clear of the right-180px and
  bottom-90px overlay zones.
- **Reels/Shorts**: hook in the top 15%; cyan-bordered "video frame" preview
  panel in the middle; tagline placed **below the panel** (y=1428) and above
  y=1440 per spec; red 3px progress indicator at the very bottom.
- **Thread header**: red THREAD indicator bar; part counter top-right;
  subtitle y computed from the *actual* wrapped title height (16px rhythm for
  both 1- and 2-line titles).
- **Logos**: canonical `brand/logos/**` resolved first, then the
  `static/brand/logos/**` mirror (same pattern as `generate-social-assets.py`).
  Icon logo on navy surfaces; full logo on the white stat card.
- No emojis in on-image copy (brand rule).

## QA results (final)

`uv run python static/brand/templates/generate-post-templates.py --verify`:

| file | dims | dominant fill | on-brand % | result |
|------|------|---------------|-----------|--------|
| linkedin-carousel-cover.png | (1080, 1080) | #070A40 | 98.7 | OK |
| youtube-thumbnail.png | (1280, 720) | #06083A | 98.6 | OK |
| reels-shorts-cover.png | (1080, 1920) | #070A40 | 97.2 | OK |
| quote-card.png | (1080, 1080) | #070A40 | 98.7 | OK |
| stat-card.png | (1080, 1080) | #FFFFFF | 99.0 | OK |
| thread-header.png | (1200, 675) | #070A40 | 97.6 | OK |

Layout probe (text-wrap metrics using the same Pillow fonts): 18/18 checks
PASS — no overflow, no safe-zone violations, no block overlaps.

Exact-token palette gate (`.agents/skills/ls-visual-storytelling/scripts/
check_brand_palette.py --tolerance 3`): 5/6 PASS (≥ 98.3%). The
`youtube-thumbnail.png` gradient is exempted by design: the 1280×720 spec
requires a subtle navy gradient, and the exact-token checker counts every
blended pixel as off-palette (98.50% "off" is the gradient, not a brand
violation). The dominant fill (#06083A) sits within distance 6 of navy and
98.6% of pixels fall within distance 48 of a brand token.
