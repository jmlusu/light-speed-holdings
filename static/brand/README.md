# LightSpeed Holdings — Static Brand Assets

**Runtime-serving copy of canonical brand assets.** Source of truth: `brand/` at repo root.

## Directory Structure

```
static/brand/
├── BRAND_GUIDELINES.md          # Quick reference for agents/developers
├── README.md                    # This file
├── logos/                       # All logo variants
│   ├── fulllogo/
│   │   ├── fulllogo.png         # Full logo (primary) — now Logo1
│   │   ├── fulllogo.jpg
│   │   ├── fulllogo_nobuffer.png
│   │   ├── fulllogo_nobuffer.jpg
│   │   ├── fulllogo_transparent.png
│   │   ├── fulllogo_transparent_nobuffer.png
│   │   ├── fulllogo_legacy.png        # Previous primary logo
│   │   ├── fulllogo_legacy.jpg
│   │   ├── fulllogo_nobuffer_legacy.png
│   │   ├── fulllogo_nobuffer_legacy.jpg
│   │   ├── fulllogo_transparent_legacy.png
│   │   ├── fulllogo_transparent_nobuffer_legacy.png
│   │   ├── Logo2.png            # Alternative full logo variant 2
│   │   ├── Logo2.jpg
│   │   ├── Logo2.svg
│   │   ├── Logo2_transparent.svg
│   │   ├── Logo2.pdf
│   │   ├── Logo2_transparent.pdf
│   │   ├── Logo2.eps
│   │   ├── Logo2_transparent.eps
│   │   ├── Logo3.png            # Alternative full logo variant 3
│   │   ├── Logo3.jpg
│   │   ├── Logo3.svg
│   │   ├── Logo3_transparent.svg
│   │   ├── Logo3.pdf
│   │   ├── Logo3_transparent.pdf
│   │   ├── Logo3.eps
│   │   ├── Logo3_transparent.eps
│   │   └── vector/
│   │       ├── print.svg              # Print vector (UPDATED)
│   │       ├── print_transparent.svg  # Print vector transparent (UPDATED)
│   │       ├── print.eps              # Print EPS (UPDATED)
│   │       ├── print_transparent.eps  # Print EPS transparent (UPDATED)
│   │       ├── print.pdf
│   │       └── print_transparent.pdf
│   ├── icononly/
│   │   ├── icononly.png
│   │   ├── icononly_transparent.png
│   │   ├── icononly_nobuffer.png
│   │   └── icononly_transparent_nobuffer.png
│   ├── textonly/
│   │   ├── textonly.png
│   │   └── textonly_nobuffer.png
│   └── grayscale/
│       ├── grayscale.png
│       ├── grayscale_transparent.png
│       ├── grayscale_nobuffer.png
│       └── grayscale_transparent_nobuffer.png
├── print/                       # Print materials
│   ├── letterhead-1.svg         # Letterhead design 1 (UPDATED)
│   ├── letterhead-1.png
│   ├── letterhead-1.pdf
│   ├── letterhead-2.svg         # Letterhead design 2 (NEW)
│   ├── letterhead-2.png         # NEW
│   ├── letterhead-2.pdf
│   ├── business-cards/          # Business card package (NEW)
│   │   ├── front_fullcolor_1024x599.svg
│   │   ├── front_fullcolor_1024x599.png
│   │   ├── front_fullcolor_1024x599.pdf
│   │   ├── front_fullcolor_1024x599.jpg
│   │   ├── front_fullcolor_1024x599.eps
│   │   ├── back_fullcolor_1024x599.svg
│   │   ├── back_fullcolor_1024x599.png
│   │   ├── back_fullcolor_1024x599.pdf
│   │   ├── back_fullcolor_1024x599.jpg
│   │   └── back_fullcolor_1024x599.eps
│   ├── email-signature-1.png
│   ├── email-signature-1.pdf
│   ├── email-signature-2.svg    # Recommended (UPDATED)
│   ├── email-signature-2.png
│   └── email-signature-2.pdf    # NEW
├── social/                      # Social media assets
│   ├── facebook-cover-3.svg     # UPDATED
│   ├── facebook-cover-3.pdf
│   ├── avatar-1024.png
│   ├── github-profile.png
│   ├── linkedin-profile.png
│   ├── linkedin-banner.png
│   ├── twitter-profile.png
│   └── twitter-header.png
└── templates/                   # Programmatic generators
    ├── pitch-deck.pptx
    ├── board-meeting.pptx
    ├── generate-pitch-deck.py
    ├── generate-board-meeting.py
    ├── generate-social-assets.py
    ├── one-pager.html
    ├── investor-update-email.html
    ├── email-signature.html
    └── email-signature-team.html
```

## Usage

| Asset Type | Primary Path | Notes |
|------------|--------------|-------|
| Logo (web) | `logos/fulllogo/fulllogo_transparent.png` | Dark backgrounds |
| Logo (print) | `logos/fulllogo/vector/print.svg` | Vector for print |
| Letterhead | `print/letterhead-1.svg` or `letterhead-2.svg` | Two designs available |
| Business Cards | `print/business-cards/` | Front/back in 5 formats each |
| Email Signature | `print/email-signature-2.svg` | Recommended default |
| Facebook Cover | `social/facebook-cover-3.svg` | 1640×624 px |

## Brand Compliance

All assets use approved palette from `brand/tokens/brand-tokens.json`:
- Navy `#070A40` (primary)
- Red `#E63946` (accent)
- Cyan `#00BFFF` (accent)
- Grey-light `#F2F2F2` (background)
- Arial font family

See `BRAND_GUIDELINES.md` for full rules.

---
*Generated from canonical `brand/` directory. Do not edit files here directly — update `brand/` and re-sync.*
