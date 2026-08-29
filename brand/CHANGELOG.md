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

*This changelog is maintained by the Brand Strategist and Chief of Staff.*
