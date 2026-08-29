# LightSpeed Holdings Limited — Investor-Facing Brand Readiness Plan

**Owner:** Investor Relations Lead (reports to CFO)
**Created:** 2026-08-27
**Status:** DRAFT — Pending CFO Review
**Next Review:** Before next board meeting or fundraise kickoff

---

## Executive Summary

LightSpeed Holdings Limited has received official branding materials from the CEO. This plan maps every investor-facing touchpoint, specifies which logo variants to use, defines co-branding rules, outlines press kit contents, and provides a readiness checklist. The goal is to ensure consistent, professional brand presentation across all investor communications before the next fundraise or board meeting.

**Key Principle:** The J.A.R.V.I.S. theme (CEO Dashboard) is a specialized internal UI — it is NOT public-facing brand. All other touchpoints adopt the new official branding.

---

## 1. Brand Identity Reference

| Element | Value |
|---------|-------|
| **Company Name** | LIGHTSPEED HOLDINGS LIMITED |
| **Tagline** | ASPIRE. ACT. ACHIEVE |
| **Primary Color** | Dark Navy (#070A40) |
| **Accent Colors** | Signal Red, Cyan Blue (#00BFFF) |
| **Logo Symbol** | Lighthouse/shield emblem with signal waves |
| **Typography** | Bold, wide-spaced sans-serif (company name); lighter weight (tagline) |

### Extracted Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Navy Primary | `#070A40` | Headlines, logo text, business card backgrounds, letterhead accents |
| Red Accent | `#E63946` (approx) | Signal waves in logo, accent elements |
| Cyan Accent | `#00BFFF` (approx) | Shield base in logo, accent elements |
| Light Grey | `#F2F2F2` | Business card background, letterhead body |
| White | `#FFFFFF` | Letterhead body, email signature backgrounds |

---

## 2. Investor Touchpoint Map

Every point where an investor encounters the LightSpeed Holdings brand:

| # | Touchpoint | Current State | Required Action | Priority |
|---|------------|---------------|-----------------|----------|
| 1 | **Pitch Deck** | Does not exist | Create full deck with new branding | CRITICAL |
| 2 | **One-Pager / Executive Summary** | Does not exist | Create branded one-pager | CRITICAL |
| 3 | **Email Signatures** | No standard | Deploy Email Signature 2 (navy border) org-wide | HIGH |
| 4 | **Business Cards** | Not printed | Order Business Card Design 1 for all executives | HIGH |
| 5 | **Letterhead** | Does not exist | Deploy Letterhead 1 (navy header bar) as standard | HIGH |
| 6 | **Website / Landing Page** | `static/index.html` has "LS" placeholder | Replace with official logo; full brand refresh | HIGH |
| 7 | **Social Media Profiles** | No assets deployed | Apply Facebook Cover Page 3; create LinkedIn/Twitter equivalents | MEDIUM |
| 8 | **Press / Media Kit** | Does not exist | Create downloadable press kit | MEDIUM |
| 9 | **Board Meeting Materials** | J.A.R.V.I.S. dashboard only | Create branded board deck template | HIGH |
| 10 | **Data Room / Due Diligence** | Does not exist | Create branded data room cover page and folder structure | HIGH |
| 11 | **Legal Documents** | No letterhead | Use grayscale logo variant on legal filings | MEDIUM |
| 12 | **Investor Update Emails** | No template | Create branded email template | HIGH |
| 13 | **CLI / Developer-Facing** | "LS" text placeholder in dashboard | Keep J.A.R.V.I.S. theme (internal); do NOT rebrand | N/A |
| 14 | **Conference / Event Materials** | Does not exist | Order banners, pull-ups using vector assets | MEDIUM |

---

## 3. Asset Selection Matrix

Which logo variant to use for each investor material:

| Material | Logo Variant | Format | Background | Notes |
|----------|-------------|--------|------------|-------|
| **Pitch Deck — Cover** | `fulllogo.png` or `fulllogo_transparent.png` | PNG (high-res) | White or Navy | Full logo with icon + text; use transparent on dark backgrounds |
| **Pitch Deck — Slides** | `icononly.png` | PNG | White | Icon only for slide corners/watermarks |
| **Pitch Deck — Thank You** | `fulllogo_transparent.png` | PNG | Navy | Full logo on dark background |
| **One-Pager** | `fulllogo.png` | PNG | White | Header placement, left-aligned |
| **Email Signature** | `icononly.png` | PNG (72dpi, ~80px wide) | White | Small icon next to name block |
| **Business Card** | Pre-designed | SVG/PDF | Navy pattern | Use Design 1 as-is; do not modify layout |
| **Letterhead** | Pre-designed | SVG/PDF | White | Use Letterhead 1 as-is; navy header bar |
| **Website** | `fulllogo_transparent.png` or `print.svg` | SVG preferred | Variable | SVG for crisp rendering at all sizes |
| **Social Media — Profile** | `icononly_transparent.png` | PNG (400x400+) | Transparent | Avatar/profile picture |
| **Social Media — Cover** | Facebook Cover Page 3 (SVG) | SVG/PDF | Navy pattern | Direct use of provided asset |
| **Press Kit** | All variants | SVG + PNG | Mixed | Include all formats for media use |
| **Board Deck** | `fulllogo.png` | PNG | White | Cover slide; icon on internal slides |
| **Legal Documents** | `grayscale.png` or `grayscale_transparent.png` | PNG | White | Monochrome for B&W printing |
| **Data Room** | `fulllogo.png` | PNG | White | Cover page; folder tabs |
| **Investor Updates** | `icononly.png` | PNG | White | Email header; small and clean |
| **Event Banners** | `print.svg` or `print.pdf` | Vector | Variable | High-resolution print output |

### Vector vs Raster Decision Tree

```
Is it for screen display?
├── Yes → PNG (use transparent variants on non-white backgrounds)
└── No (print)
    ├── High-quality print → PDF or EPS
    └── Large format (banner, pull-up) → SVG or PDF
```

---

## 4. Presentation Templates

### 4.1 Pitch Deck Template

**Structure (12–15 slides):**

| Slide | Content | Branding Notes |
|-------|---------|----------------|
| 1 | Cover: Logo + Company Name + Tagline | `fulllogo_transparent.png` on navy background |
| 2 | Problem Statement | Icon-only watermark; navy headlines |
| 3 | Solution | Icon-only watermark |
| 4 | Market Opportunity | Charts use brand accent colors |
| 5 | Product / Technology | Screenshots with brand frame |
| 6 | Business Model | Clean layout; navy dividers |
| 7 | Traction / Metrics | KPI cards with brand color coding |
| 8 | Competitive Landscape | Navy headers; red for differentiation |
| 9 | Team | Photos in circular frames; navy name bars |
| 10 | Financials | Charts use brand palette |
| 11 | Funding Ask | Clear CTA; navy background option |
| 12 | Thank You / Contact | `fulllogo_transparent.png` centered on navy |

**Template Format:** `.pptx` (PowerPoint) + `.key` (Keynote) as primary; PDF export for distribution.

### 4.2 One-Pager Template

- **Size:** A4 / US Letter
- **Header:** `fulllogo.png` top-left, contact info top-right
- **Body:** Company overview, key metrics, contact details
- **Footer:** Tagline + legal entity name
- **Format:** PDF (print-ready) + editable DOCX

### 4.3 Board Meeting Template

- **Cover Slide:** `fulllogo.png` + "Board Meeting — [Date]"
- **Section Dividers:** Navy background with white text
- **Content Slides:** Clean white; icon-only watermark bottom-right
- **Appendix:** Grayscale variant for B&W printouts
- **Format:** `.pptx` with master slide branding

### 4.4 Investor Update Email Template

- **Header:** `icononly.png` (40px) + "LightSpeed Holdings Limited" text
- **Divider:** Navy horizontal rule
- **Body:** Clean sans-serif font; brand navy for headings
- **Footer:** Email signature block (matches Email Signature 2)
- **Format:** HTML email template + plain-text fallback

---

## 5. Co-Brandin g Rules

### 5.1 Logo Placement with Partners

| Scenario | Rule |
|----------|------|
| **LightSpeed + Partner (equal)** | Logos side-by-side, separated by vertical rule (`|`), same height. LightSpeed on left. |
| **LightSpeed + Partner (LightSpeed lead)** | LightSpeed logo 1.5x partner logo size. LightSpeed top/left, partner bottom/right. |
| **LightSpeed + Partner (Partner lead)** | Partner logo 1.5x LightSpeed logo size. Partner top/left, LightSpeed bottom/right. |
| **LightSpeed as sponsor** | LightSpeed logo in sponsor row, consistent with other sponsor logos. |
| **LightSpeed as client/partner** | Use `icononly` variant; respect partner's brand guidelines. |

### 5.2 Clear Space Requirements

- **Minimum clear space** around logo = height of the "L" in "LIGHTSPEED" on all sides
- **No other logos, text, or graphics** may enter this clear space
- **Exception:** Co-branding scenarios above, where a vertical rule separates logos

### 5.3 Minimum Sizes

| Variant | Print Minimum | Screen Minimum |
|---------|---------------|----------------|
| Full Logo (icon + text) | 30mm wide | 120px wide |
| Icon Only | 12mm wide | 32px wide |
| Text Only | 25mm wide | 100px wide |

### 5.4 Do Not

- Do not rotate the logo
- Do not stretch or distort proportions
- Do not change the logo colors
- Do not add effects (drop shadows, glows, gradients)
- Do not place the logo on busy photographic backgrounds without sufficient contrast
- Do not recreate the logo in any other typeface
- Do not use low-resolution versions for print

---

## 6. Press Kit Contents

A downloadable media kit for journalists, analysts, and partners. Package as a ZIP file hosted on the website.

### 6.1 Kit Structure

```
lightspeed-press-kit/
├── README.txt                    # Usage terms and contact info
├── brand-guidelines.pdf          # Summary of this document
├── logo/
│   ├── fulllogo/
│   │   ├── fulllogo.png
│   │   ├── fulllogo.jpg
│   │   ├── fulllogo_transparent.png
│   │   ├── print.svg
│   │   ├── print.pdf
│   │   └── print.eps
│   ├── icononly/
│   │   ├── icononly.png
│   │   ├── icononly_transparent.png
│   │   └── print.svg
│   ├── textonly/
│   │   ├── textonly.png
│   │   └── textonly_nobuffer.png
│   └── grayscale/
│       ├── grayscale.png
│       └── grayscale_transparent.png
├── business-card/
│   ├── front_fullcolor_1024x599.png
│   ├── front_fullcolor_1024x599.svg
│   ├── back_fullcolor_1024x599.png
│   └── back_fullcolor_1024x599.svg
├── letterhead/
│   ├── letterhead-1.svg
│   └── letterhead-2.svg
├── social-media/
│   ├── facebook-cover-3.svg
│   └── facebook-cover-3.pdf
├── executive-photos/             # CEO and leadership headshots (placeholder)
│   └── jack-mlusu-ceo.jpg
└── fact-sheet/
    └── lightspeed-holdings-fact-sheet.pdf
```

### 6.2 README.txt Template

```
LIGHTSPEED HOLDINGS LIMITED — Brand Assets
============================================

Usage: These assets are provided for editorial and media use only.
       For commercial or promotional use, please contact investor.relations@lightspeedholdings.com

Company: LightSpeed Holdings Limited
Tagline: Aspire. Act. Achieve.
Contact: Jack Mlu su, Founder & CEO
Email: jmlusu@gmail.com
Phone: +265 (0) 980 016 004
Location: Lilongwe, Malawi

When using our logo, please maintain clear space and minimum size requirements
as outlined in the included brand guidelines.
```

---

## 7. Compliance & Trademark Rules

### 7.1 Trademark Notice

- The LightSpeed Holdings name and logo are proprietary marks of LightSpeed Holdings Limited
- Use the ™ symbol on first mention in any document: "LightSpeed Holdings Limited™"
- Use the ® symbol once registered: "LightSpeed Holdings Limited®"
- **Action Item:** Confirm trademark registration status with Legal

### 7.2 Logo Usage — Mandatory Rules

| Rule | Detail |
|------|--------|
| **Always use official assets** | Never recreate, screenshot, or approximate the logo |
| **Maintain aspect ratio** | Never stretch, compress, or distort |
| **Clear space** | Minimum 1x "L" height on all sides |
| **Minimum size** | 30mm print / 120px screen (full logo); 12mm / 32px (icon) |
| **Color accuracy** | Use provided color files; do not re-color |
| **Background contrast** | Ensure sufficient contrast; use transparent variants on dark backgrounds |
| **No modifications** | No effects, no outlines, no shadows, no rotations |
| **Print specifications** | Use vector (SVG/PDF/EPS) for all print materials |
| **Digital specifications** | Use PNG for web; SVG for scalable web elements |

### 7.3 Font Usage

- **Company name** uses a proprietary bold, wide-tracked sans-serif (extracted from brand assets)
- **Tagline** uses a lighter weight of the same family
- **Do not** attempt to match or approximate this typeface; use the provided SVG/PDF assets
- For documents, use a clean sans-serif as body text (e.g., Inter, Helvetica Neue, Arial)

### 7.4 Color Compliance

| Do | Don't |
|----|-------|
| Use exact hex values from brand assets | Approximate colors from memory |
| Use grayscale variant for B&W media | Convert color logo to grayscale manually |
| Use transparent PNGs on non-white backgrounds | Place light logos on light backgrounds |
| Test contrast ratio (minimum 4.5:1 for text) | Assume accessibility compliance without testing |

---

## 8. Readiness Checklist

### Phase 1 — Immediate (Before Next Board Meeting)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1.1 | Copy all brand assets to `static/brand/` directory | IR Lead | ☐ TODO | Centralize assets for web/CLI access |
| 1.2 | Create `static/brand/BRAND_GUIDELINES.md` | IR Lead | ☐ TODO | Quick-reference for all agents and team |
| 1.3 | Build pitch deck template (12–15 slides) | IR Lead + CMO | ☐ TODO | Use `fulllogo_transparent.png` for cover |
| 1.4 | Build one-pager template | IR Lead | ☐ TODO | A4/Letter; PDF + DOCX |
| 1.5 | Build board meeting template | IR Lead | ☐ TODO | `.pptx` master with branded slides |
| 1.6 | Deploy Email Signature 2 org-wide | IR Lead + IT | ☐ TODO | HTML signature for all team members |
| 1.7 | Order business cards (Design 1) | IR Lead | ☐ TODO | For CEO, CFO, and key executives |
| 1.8 | Update `static/index.html` logo | IR Lead + Eng | ☐ TODO | Replace "LS" placeholder with `icononly.png` |

### Phase 2 — Pre-Fundraise (4–6 Weeks Before Raise)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 2.1 | Finalize pitch deck with financials | IR Lead + CFO | ☐ TODO | Complete all slides; export PDF |
| 2.2 | Create investor update email template | IR Lead | ☐ TODO | HTML + plain text |
| 2.3 | Build data room structure | IR Lead + Legal | ☐ TODO | Branded cover page; organized folders |
| 2.4 | Create press kit ZIP | IR Lead | ☐ TODO | Following structure in Section 6 |
| 2.5 | Upload press kit to website | IR Lead + Eng | ☐ TODO | Downloadable link on website |
| 2.6 | Create LinkedIn company page assets | IR Lead + CMO | ☐ TODO | Profile + banner from brand assets |
| 2.7 | Create Twitter/X profile assets | IR Lead + CMO | ☐ TODO | Profile + header from brand assets |
| 2.8 | Print letterhead (500 copies) | IR Lead | ☐ TODO | Letterhead 1 (navy header bar) |
| 2.9 | Prepare co-branding guidelines doc | IR Lead | ☐ TODO | For partner/client logo usage |
| 2.10 | Brief all executives on brand usage | IR Lead | ☐ TODO | 30-min session; distribute guidelines |

### Phase 3 — Ongoing Maintenance

| # | Task | Owner | Frequency | Notes |
|---|------|-------|-----------|-------|
| 3.1 | Review brand consistency quarterly | IR Lead | Quarterly | Audit all investor-facing materials |
| 3.2 | Update press kit with new assets | IR Lead | As needed | When new materials are created |
| 3.3 | Reprint business cards as needed | IR Lead | As needed | Keep inventory above 50 cards per exec |
| 3.4 | Update email signatures on org changes | IR Lead + IT | On hire/role change | New team members get branded signature |
| 3.5 | Trademark renewal monitoring | IR Lead + Legal | Annually | Track registration expiry dates |
| 3.6 | Brand asset version control | IR Lead | On update | Archive old versions; note changelog |

---

## 9. Asset Directory Structure (Recommended)

```
static/brand/
├── logos/
│   ├── fulllogo/
│   │   ├── fulllogo.png
│   │   ├── fulllogo.jpg
│   │   ├── fulllogo_transparent.png
│   │   ├── fulllogo_transparent_nobuffer.png
│   │   ├── fulllogo_nobuffer.png
│   │   ├── fulllogo_nobuffer.jpg
│   │   └── vector/
│   │       ├── print.svg
│   │       ├── print.pdf
│   │       ├── print.eps
│   │       ├── print_transparent.svg
│   │       ├── print_transparent.pdf
│   │       └── print_transparent.eps
│   ├── icononly/
│   │   ├── icononly.png
│   │   ├── icononly_nobuffer.png
│   │   ├── icononly_transparent.png
│   │   └── icononly_transparent_nobuffer.png
│   ├── textonly/
│   │   ├── textonly.png
│   │   └── textonly_nobuffer.png
│   └── grayscale/
│       ├── grayscale.png
│       ├── grayscale_nobuffer.png
│       ├── grayscale_transparent.png
│       └── grayscale_transparent_nobuffer.png
├── templates/
│   ├── pitch-deck.pptx
│   ├── one-pager.docx
│   ├── one-pager.pdf
│   ├── board-meeting.pptx
│   ├── investor-update-email.html
│   └── data-room-cover.pdf
├── print/
│   ├── letterhead-1.svg
│   ├── letterhead-1.pdf
│   ├── letterhead-2.svg
│   ├── letterhead-2.pdf
│   ├── business-card-front.svg
│   ├── business-card-back.svg
│   ├── email-signature-1.png
│   ├── email-signature-2.svg
│   └── email-signature-2.png
├── social/
│   ├── facebook-cover-3.svg
│   ├── facebook-cover-3.pdf
│   ├── linkedin-banner.svg        # To be created
│   └── twitter-header.svg         # To be created
├── BRAND_GUIDELINES.md
└── README.md
```

---

## 10. Brand Color Tokens (for CSS/Digital Use)

If we need to reference brand colors in CSS, email templates, or digital materials:

```css
:root {
  /* Primary */
  --ls-navy: #070A40;
  --ls-navy-light: #0D1266;
  --ls-navy-dark: #040729;

  /* Accents */
  --ls-red: #E63946;
  --ls-cyan: #00BFFF;

  /* Neutrals */
  --ls-grey: #F2F2F2;
  --ls-grey-dark: #9CA3AF;
  --ls-white: #FFFFFF;

  /* Text */
  --ls-text-primary: #070A40;
  --ls-text-secondary: #6B7280;
  --ls-text-inverse: #FFFFFF;
}
```

---

## 11. Escalation & Approval

| Decision | Approver | SLA |
|----------|----------|-----|
| New brand asset creation | CMO + CEO | 5 business days |
| Co-branding with partner | CEO + Legal | 3 business days |
| Press kit publication | CEO | 2 business days |
| Brand guideline exceptions | CFO + CEO | Immediate |
| Trademark filing/renewal | Legal + CEO | Per legal timeline |

---

## 12. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Inconsistent brand usage across materials | High | Medium | Centralized asset directory; brand guidelines; quarterly audit |
| Low-resolution logos in print materials | Medium | Medium | Enforce vector-first policy for all print |
| Co-branding misalignment with partners | High | Low | Written co-branding guidelines; approval workflow |
| Trademark not registered | High | Unknown | Confirm status with Legal immediately |
| Old "LS" placeholder still visible | Medium | High | Task 1.8 in Phase 1; verify after deployment |
| Team members use personal email signatures | Medium | High | Deploy org-wide HTML signature; IT enforcement |

---

## Appendix A: Quick Reference Card

```
╔══════════════════════════════════════════════════════════╗
║  LIGHTSPEED HOLDINGS LIMITED™                           ║
║  Aspire. Act. Achieve.                                  ║
╠══════════════════════════════════════════════════════════╣
║  LOGO:  Use fulllogo for headers; icononly for avatars  ║
║  COLOR: Navy #070A40 | Red accent | Cyan accent        ║
║  MIN:   30mm print / 120px screen (full logo)           ║
║  SPACE: 1x "L" height clear on all sides                ║
║  LEGAL: ™ on first use; ® once registered               ║
║  PRINT: Always use vector (SVG/PDF/EPS)                 ║
║  WEB:   PNG for raster; SVG for scalable elements       ║
╚══════════════════════════════════════════════════════════╝
```

---

*Prepared by Investor Relations Lead, LightSpeed Holdings Limited*
*For questions: investor.relations@lightspeedholdings.com*
