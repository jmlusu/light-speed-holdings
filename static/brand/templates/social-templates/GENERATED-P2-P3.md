# P2/P3 Secondary Social Post Templates — Generated Set (Ticket #316)

Six P2/P3 secondary social template types, generated from the brand system
(tokens + official logo) with **real LightSpeed copy** grounded in
`docs/Pharos/positioning.md` (the 7-layer framework, the Four Reservations:
Trust-by-Engineering series, and the Africa/Malawi/SADC positioning). These
extend the P1 generator from Ticket #311; all twelve templates share one
generator, one slot registry, and one verify command. No lorem ipsum.

- **Generator**: `static/brand/templates/generate-post-templates.py` (Pillow-only, no API keys)
- **Outputs**: `static/brand/social/templates/*.png` (canonical file names below)
- **Spec source**: `static/brand/templates/social-templates/TEMPLATE_SPECS.md`
- **P1 set**: see [GENERATED-P1.md](GENERATED-P1.md) (Ticket #311)

The generator now produces all **12** templates (P1 #1–6 + P2/P3 #7–12). The
registry drives `--verify` iteration, so the new types are covered by the same
self-QA as the P1 set.

## Templates (P2/P3)

| # | Canonical file | Dims | Surface | Slots exposed |
|---|----------------|------|---------|---------------|
| 7 | `lower-third-video-overlay.png` | 1920×360 | navy @ 90% (RGBA) | `name`, `role`, `tagline` |
| 8 | `hook-card.png` | 1080×1920 | navy | `number`, `hook`, `teaser`, `tagline` |
| 9 | `end-screen-cta.png` | 1920×1080 | navy | `headline`, `subtext`, `emailPlaceholder`, `cta`, `tagline` |
| 10 | `chapter-marker.png` | 1920×180 | navy @ 95% (RGBA) | `number`, `title`, `timestamp`, `tagline` |
| 11 | `facebook-group-cover.png` | 1640×856 | navy | `group`, `tagline`, `description`, `cta` |
| 12 | `email-newsletter-header.png` | 600×200 | navy | `publication`, `issue`, `tagline` |

## Regeneration

```powershell
# All twelve templates (P1 + P2/P3)
uv run python static/brand/templates/generate-post-templates.py

# Self-QA after generating (dimensions + dominant brand fills)
uv run python static/brand/templates/generate-post-templates.py --verify

# One P2/P3 template with copy injection
uv run python static/brand/templates/generate-post-templates.py `
  --template lower-third-video-overlay `
  --slots '{"name": "Jane Doe", "role": "Head of AI"}'

# Slots for several templates from a JSON file
# {"email-newsletter-header": {"issue": "Issue #02"}, "hook-card": {"number": "8"}}
uv run python static/brand/templates/generate-post-templates.py --json params.json
```

`--slots` requires `--template`. `--outdir` overrides the default output
directory. No source change is required to swap copy — every text field is a
slot.

## Design decisions (documented)

- **Lower-third video overlay (1920×360 RGBA)**: navy at **90% opacity**
  (alpha 230) so video editors can composite the bar straight over footage —
  the RGB values stay on-token, so QA still counts the surface as navy.
  Content group (name → red 4px accent line → role → tagline) is vertically
  centered on y=180; the icon logo sits right-center. Long-form/YouTube style.
- **Hook card (1080×1920)**: the red ring around the hero number is the static
  render of the spec's motion "pulse ring" (1.5s ease-in-out) anchored upper-
  middle. Hook is limited to 2 centered lines (title-lg white); the teaser
  ("Watch for the governance layer institutions actually trust.") sits below.
  Tailored for short-form first-3-seconds attention; icon logo top-right;
  tagline in the bottom clear zone (y=1856, above the 64px UI margin).
- **End-screen CTA (1920×1080)**: headline + subtext + email-capture visual
  (input field mock with cyan focus line, red "Subscribe Free" button) live in
  the left content column; a red arrow points at the CTA button; full logo +
  tagline bottom-center. Static mock, swap via slots for real campaign runs.
- **Chapter marker (1920×180 RGBA)**: navy at **95% opacity** (alpha 242);
  60%-cyan progress bar near the bottom (2px) with the red chapter circle
  (32px) at the left; timestamp + tagline right-aligned. Video/talk cut-in.
- **Facebook group cover (1640×856)**: centered stack — group name, tagline,
  description, full logo, red pill CTA — keeps all content clear of FB's
  bottom member-count UI.
- **Email newsletter header (600×200)**: the web layout's `navyRail` 4px token
  is rendered as a 4px **cyan** line at the left edge (the rail signal on a
  navy surface; a 4px navy line would be invisible). Full logo at 140px wide
  (≥ 120px min), publication + issue to its right, tagline right-aligned.
- **Exact-palette snap for small canvases**: the 600×200 header is small
  enough that anti-aliased logo/text edges would exceed the 3% exact-token QA
  tolerance (the source fulllogo itself carries ~970 blend colors).
  `_snap_to_palette` snaps every visible pixel to its nearest brand token
  after rendering — visually identical (every blend is an average of two
  tokens) and the gate reports 100% on-palette. Only the email header applies
  this pass; the larger P2/P3 canvases stay under tolerance natively.
- **Logos**: canonical `brand/logos/**` resolved first, then the
  `static/brand/logos/**` mirror. Icon logo on the lower-third + hook card;
  full logo on end-screen CTA / FB group cover / email header. New `_paste_logo`
  positions: `center-right` (lower-third, vertically centered) and `center`
  (bottom-center end-screen logo).
- **Type keys**: `generate_*` for P2/P3 use the full scale
  (`displayXl`, `titleLg`, `titleMd`); `_resolve_tokens` now guarantees them
  alongside the P1 aliases.
- No emojis in on-image copy (brand rule).

## QA results (final)

`uv run python static/brand/templates/generate-post-templates.py --verify`:

| file | dims | dominant fill | on-brand % | result |
|------|------|---------------|-----------|--------|
| lower-third-video-overlay.png | (1920, 360) | #070A40 | 99.0 | OK |
| hook-card.png | (1080, 1920) | #070A40 | 99.3 | OK |
| end-screen-cta.png | (1920, 1080) | #070A40 | 98.1 | OK |
| chapter-marker.png | (1920, 180) | #070A40 | 99.0 | OK |
| facebook-group-cover.png | (1640, 856) | #070A40 | 99.2 | OK |
| email-newsletter-header.png | (600, 200) | #070A40 | 96.9 | OK |

All 12 templates (P1 + P2/P3): VERDICT PASS.

Exact-token palette gate (`.agents/skills/ls-visual-storytelling/scripts/
check_brand_palette.py --tolerance 3`):

| file | on-palette | result |
|------|------------|--------|
| lower-third-video-overlay.png | 99.65% | PASS |
| hook-card.png | 99.74% | PASS |
| end-screen-cta.png | 98.97% | PASS |
| chapter-marker.png | 99.63% | PASS |
| facebook-group-cover.png | 99.04% | PASS |
| email-newsletter-header.png | 100.00% | PASS (snap applied) |
