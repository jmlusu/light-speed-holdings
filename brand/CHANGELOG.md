# Brand Asset Changelog

All notable changes to LightSpeed Holdings brand assets are documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-08-27

### Added
- **Logo Suite** — Full logo, icon-only, text-only, grayscale variants (18 files)
  - Full logo: PNG, JPG, transparent, no-buffer variants
  - Icon only: PNG, transparent, no-buffer variants
  - Text only: PNG, no-buffer variants
  - Grayscale: PNG, transparent, no-buffer variants
  - Print vectors: SVG, PDF, EPS (standard and transparent)
- **Business Cards** — Design 1 (navy geometric pattern)
  - Front: SVG, PNG, PDF, JPG, EPS
  - Back: SVG, PNG, PDF, JPG, EPS
- **Letterheads** — 2 designs
  - Letterhead 1 (navy header bar): SVG, PDF
  - Letterhead 2: SVG, PDF
- **Email Signatures** — 2 designs
  - Signature 1: PNG, PDF
  - Signature 2 (recommended): SVG, PNG, PDF
- **Social Media** — Facebook Cover Page 3: SVG, PDF
- **Brand Guidelines** — Quick reference at `static/brand/BRAND_GUIDELINES.md`
- **Investor Readiness Plan** — Full document at `docs/INVESTOR_BRAND_READINESS_PLAN.md`
- **Brand Adoption Roadmap** — Full plan at `docs/BRAND_ADOPTION_ROADMAP.md`
- **Investor Templates**
  - Pitch deck (13 slides): `static/brand/templates/pitch-deck.pptx`
  - Board meeting (9 slides): `static/brand/templates/board-meeting.pptx`
  - One-pager: `static/brand/templates/one-pager.html`
  - Investor update email: `static/brand/templates/investor-update-email.html`
  - Email signature: `static/brand/templates/email-signature.html`
- **Logo Swaps**
  - `static/index.html` — "LS" placeholder → `icononly.png`
  - `static/mobile.html` — "LS" placeholder → `icononly.png`
- **Brand Directory** — `brand/` at repo root (canonical source of truth)
  - `brand/logos/`, `brand/print/`, `brand/digital/`, `brand/tokens/`, `brand/guidelines/`

### Brand Identity
- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **Primary Color:** Dark Navy `#070A40`
- **Accent — Red:** `#E63946`
- **Accent — Cyan:** `#00BFFF`
- **Neutral — Light Grey:** `#F2F2F2`

---

## [1.1.0] - 2026-08-28

### Added / Updated
- **Pitch deck** (`generate-pitch-deck.py` → `pitch-deck.pptx`) — populated with real content
  - KPI: 135 agents / 19 departments / 5 flagship offers / 8 recurring products
  - Milestones: Jul 2026 bootstrap, Aug 2026 Blueprint adoption ($500K capital guidance), 183 tests
  - Pricing: SaaS $49/$149/$299 + Managed AI Workforce (MWK)
  - Financials: $120K/$300K/$600K ARR targets — **pending CFO validation** (DIR-CEO-2026-001 §6.2)
  - Raising $500K Seed; contact Jack Mlusu, jmlusu@gmail.com, +265 (0) 980 016 004
- **Board meeting deck** (`generate-board-meeting.py` → `board-meeting.pptx`) — populated
  - Cover date Aug 27, 2026; next meeting Sep 15, 2026 — Q3 Strategy Pivot Review
  - 3 real decisions: ratify first client pilots, SaaS $49–$299 band, Y1 $120K ARR target
- **One-pager** (`one-pager.html`) — real metrics/mission/solution; logo → relative `../logos/fulllogo/fulllogo.png`
- **Investor update email** (`investor-update-email.html`) — real highlights/metrics/outlook
- **Email signatures** — CEO pre-filled; image URLs updated to `lightspeedholdings.com/brand/...` (must be hosted before send)

### Pending
- CFO sign-off on revenue projections (blocking 2.7)
- Host brand assets at `lightspeedholdings.com/brand/` so email/signature images resolve (blocking 2.5)
- Team member details for remaining signature/template placeholders

---

## [1.2.0] - 2026-09-06

### Added
- **Business Cards** — Design 1 fully integrated (10 files: front/back × SVG, PNG, PDF, JPG, EPS)
  - Canonical location: `brand/print/business-cards/` + runtime: `static/brand/print/business-cards/`
- **Letterhead 2** — SVG and PNG variants added (PDF existed)
  - Canonical: `brand/print/letterhead/letterhead-2.svg/png` + runtime: `static/brand/print/`
- **Letterhead 1 PNG** — Added to both canonical and runtime (PDF/SVG existed)
- **Email Signature 2** — PDF variant added (SVG/PNG existed)
- **Canonical directory structure** — Implemented per `brand/README.md`:
  - `brand/logos/fulllogo/vector/` — logo print vectors
  - `brand/print/letterhead/` — both letterhead designs
  - `brand/print/business-cards/` — business card package
  - `brand/print/email-signatures/` — both signature designs
  - `brand/digital/social/` — Facebook cover

### Updated
- **Logo print vectors** — Refreshed SVG/EPS files from approved artifacts:
  - `print.svg`, `print_transparent.svg`, `print.eps`, `print_transparent.eps` (PDFs unchanged)
- **Letterhead 1 SVG** — Updated from approved artifact
- **Email Signature 2 SVG** — Updated from approved artifact
- **Facebook Cover 3 SVG** — Updated from approved artifact; fixed filename typo ("Holding" → "Holdings")

### Removed
- **Source artifacts folder** — `brand/LightSpeed Holdings Limited Branding artifacts/` deleted after sync
  - Extracted subfolders and ZIPs removed
- **Legacy static folder** — `static/brand/LightSpeed Holdings Limited Brand/` (contained duplicate ZIPs)

### Brand Identity
- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **Primary Color:** Dark Navy `#070A40`
- **Accent — Red:** `#E63946`
- **Accent — Cyan:** `#00BFFF`
- **Neutral — Light Grey:** `#F2F2F2`

---

## [1.3.0] - 2026-09-06

### Added
- **Alternative Full Logo Variants** — 3 new logo variants (Logo1, Logo2, Logo3) with full format support:
  - Each variant: PNG, JPG, SVG, SVG (transparent), PDF, PDF (transparent), EPS, EPS (transparent) — 8 files × 3 = 24 files
  - Canonical location: `brand/logos/fulllogo/` + runtime: `static/brand/logos/fulllogo/`
  - Source PNGs uploaded as `Logo1.png`, `Logo2.png`, `Logo3.png` (RGBA, transparent backgrounds)
  - All derived formats generated programmatically (SVG with embedded base64, PDF via fpdf2, EPS wrapper)

### Updated
- **Brand documentation** — Updated `brand/README.md`, `static/brand/README.md`, `brand/guidelines/brand-guidelines.md`, `static/brand/BRAND_GUIDELINES.md` with new logo variant tables
- **Logo variant tables** — Added Logo1/2/3 entries with use cases (alternative layouts, presentations)

### Brand Identity
- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **Primary Color:** Dark Navy `#070A40`
- **Accent — Red:** `#E63946`
- **Accent — Cyan:** `#00BFFF`
- **Neutral — Light Grey:** `#F2F2F2`

---

## [1.4.0] - 2026-09-06

### Restored
- **Original Logo Suite** — Restored 18 original approved logo files from git history (commit c928d71):
  - Full logo (6): PNG, JPG, no-buffer variants, transparent, transparent no-buffer
  - Icon only (4): PNG, no-buffer, transparent, transparent no-buffer
  - Text only (2): PNG, no-buffer
  - Grayscale (4): PNG, no-buffer, transparent, transparent no-buffer
  - Print vectors (6): SVG, PDF, EPS (standard and transparent)

### Added
- **Complete canonical directory** — All logo variants now in `brand/logos/` matching `static/brand/logos/`:
  - `brand/logos/fulllogo/` — 30 files (6 original + 3 variants × 8 formats)
  - `brand/logos/fulllogo/vector/` — 6 print vector files
  - `brand/logos/icononly/` — 4 variants
  - `brand/logos/grayscale/` — 4 variants
  - `brand/logos/textonly/` — 2 variants

### Updated
- **All brand documentation** fully synchronized:
  - `brand/README.md` — Complete directory structure with all variants
  - `static/brand/README.md` — Complete inventory (already current)
  - `brand/guidelines/brand-guidelines.md` — Full 22-row logo variants table
  - `static/brand/BRAND_GUIDELINES.md` — Full 22-row logo variants table
- **Verification** — All 30+ logo files SHA256-matched between canonical and runtime

### Brand Identity
- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **Primary Color:** Dark Navy `#070A40`
- **Accent — Red:** `#E63946`
- **Accent — Cyan:** `#00BFFF`
- **Neutral — Light Grey:** `#F2F2F2`

---

## [1.5.0] - 2026-09-06

### Changed
- **Primary Logo Promotion** — Logo1 promoted to primary brand logo:
  - Previous primary logo archived as `fulllogo_legacy.*` (6 files: PNG, JPG, no-buffer, transparent, transparent no-buffer)
  - Logo1 (531×381 RGBA) copied to `fulllogo.*` as new primary across all 6 variants
  - Both canonical (`brand/logos/fulllogo/`) and runtime (`static/brand/logos/fulllogo/`) updated

### Updated
- **Logo variant tables** in all documentation:
  - `brand/README.md` — Directory structure updated, Logo1 removed from alternatives, legacy noted
  - `static/brand/README.md` — Same updates
  - `brand/guidelines/brand-guidelines.md` — 20-row variants table (removed Variant 1, added Legacy)
  - `static/brand/BRAND_GUIDELINES.md` — 20-row variants table (same)
- **Usage guidance** — Primary logo now references Logo1 design

### Brand Identity
- **Tagline:** ASPIRE. ACT. ACHIEVE.
- **Primary Color:** Dark Navy `#070A40`
- **Accent — Red:** `#E63946`
- **Accent — Cyan:** `#00BFFF`
- **Neutral — Light Grey:** `#F2F2F2`

---

*This changelog is maintained by the Brand Strategist and Chief of Staff.*
