# LightSpeed Holdings — Brand Adoption Roadmap

**Owner:** Chief of Staff
**Sponsor:** CEO (Human)
**Created:** 2026-08-27
**Status:** ACTIVE
**Tagline:** ASPIRE. ACT. ACHIEVE.

---

## Executive Summary

This roadmap tracks the organization-wide adoption of official LightSpeed Holdings Limited branding materials. The CEO has uploaded professional brand assets (logos, business cards, letterheads, email signatures, social media covers) that must be deployed across all public-facing and operational touchpoints while preserving the J.A.R.V.I.S. theme for the CEO Dashboard.

**Key Principle:** The J.A.R.V.I.S. theme (control-plane-theme.css, jarvis-* tokens) remains untouched for the CEO Dashboard — it is a specialized internal UI, not public-facing brand.

---

## Current State

| Surface | Status | Brand Applied |
|---------|--------|---------------|
| CEO Dashboard | Live | J.A.R.V.I.S. (preserved) |
| Mobile Dashboard | Live | ⚠️ "LS" placeholder — **SWAPPED to icononly.png** |
| Landing Page (index.html) | Live | ⚠️ "LS" placeholder — **SWAPPED to icononly.png** |
| Email Signatures | Not deployed | ✅ Template ready |
| Business Cards | Designed | ✅ Assets in `static/brand/print/` |
| Letterheads | Designed | ✅ Assets in `static/brand/print/` |
| Social Media | Designed | ✅ Assets in `static/brand/social/` |
| Pitch Deck | Not created | ✅ Template generated |
| Board Meeting Deck | Not created | ✅ Template generated |
| One-Pager | Not created | ✅ Template generated |
| Investor Update Email | Not created | ✅ Template generated |

---

## Roadmap Phases

### Phase 1: Foundation ✅ COMPLETE
**Duration:** Day 1 (August 27, 2026)

| # | Task | Status | Owner |
|---|------|--------|-------|
| 1.1 | Upload brand assets to `Branding landing page/` | ✅ Done | CEO |
| 1.2 | Organize assets into `static/brand/` directory | ✅ Done | IR Lead |
| 1.3 | Create `BRAND_GUIDELINES.md` quick reference | ✅ Done | IR Lead |
| 1.4 | Create `INVESTOR_BRAND_READINESS_PLAN.md` | ✅ Done | IR Lead |
| 1.5 | Swap "LS" logo in `static/index.html` → icononly.png | ✅ Done | Engineering |
| 1.6 | Swap "LS" logo in `static/mobile.html` → icononly.png | ✅ Done | Engineering |
| 1.7 | Generate pitch deck template (13 slides) | ✅ Done | IR Lead |
| 1.8 | Generate board meeting template (9 slides) | ✅ Done | IR Lead |
| 1.9 | Create one-pager HTML template | ✅ Done | IR Lead |
| 1.10 | Create investor update email HTML template | ✅ Done | IR Lead |
| 1.11 | Create email signature HTML template | ✅ Done | IR Lead |
| 1.12 | Create brand adoption roadmap | ✅ Done | Chief of Staff |

### Phase 2: Content Population 🔄 IN PROGRESS
**Duration:** Week 1-2 (September 1-12, 2026)

| # | Task | Status | Owner | Dependencies |
|---|------|--------|-------|--------------|
| 2.1 | Replace `[placeholder]` text in pitch deck with real content | ✅ Done | CEO + CMO | 1.7 |
| 2.2 | Replace `[placeholder]` text in board meeting deck | ✅ Done | CEO | 1.8 |
| 2.3 | Replace `[placeholder]` text in one-pager | ✅ Done | CMO | 1.9 |
| 2.4 | Replace `[placeholder]` text in investor update email | ✅ Done | IR Lead | 1.10 |
| 2.5 | Update image URLs from `your-domain.com` to actual domain | ⚠️ Partial — assets must be hosted on `lightspeedholdings.com/brand/...` before sending | Engineering | — |
| 2.6 | Add team member details to templates (names, titles, contacts) | 🔲 TODO — CEO pre-filled; other exec placeholders await details | HR + CEO | 2.1-2.4 |
| 2.7 | Add financial projections to pitch deck | ⚠️ Partial — targets added ($120K/$300K/$600K ARR); pending CFO validation & sign-off | CFO | 2.1 |
| 2.8 | Add real KPI metrics to traction slide | ✅ Done — 135 agents, 19 departments, 5 offers, 8 products | CFO + CMO | 2.1 |
| 2.9 | Extract exact brand colors from SVG assets | 🔲 TODO | Brand Strategist | — |
| 2.10 | Identify typography used in brand assets | 🔲 TODO | Brand Strategist | — |

### Phase 3: Deployment 📋 PLANNED
**Duration:** Week 2-3 (September 8-19, 2026)

| # | Task | Status | Owner | Dependencies |
|---|------|--------|-------|--------------|
| 3.1 | Deploy Email Signature 2 org-wide (HTML for all team members) | 🔲 TODO | IT + CMO | 1.11 |
| 3.2 | Order business cards for executives (500 qty) | 🔲 TODO | CFO | — |
| 3.3 | Order letterheads (500 qty) | 🔲 TODO | CFO | — |
| 3.4 | Create `brand-tokens.css` with official color palette | 🔲 TODO | Product Designer | 2.9 |
| 3.5 | Update `static/manifest.json` theme color to brand navy | 🔲 TODO | Engineering | 2.9 |
| 3.6 | Generate favicon from official icononly mark | 🔲 TODO | Engineering | — |
| 3.7 | Update `static/css/mobile.css` brand color variables | 🔲 TODO | Engineering | 2.9 |
| 3.8 | Create LinkedIn company page assets (profile + banner) | ✅ Done | Content Creator | — |
| 3.9 | Create Twitter/X profile assets (profile + header) | ✅ Done | Content Creator | — |
| 3.10 | Create GitHub organization logo from official assets | 🔲 TODO | Engineering | — |

### Phase 4: Integration 📋 PLANNED
**Duration:** Week 3-4 (September 15-26, 2026)

| # | Task | Status | Owner | Dependencies |
|---|------|--------|-------|--------------|
| 4.1 | Create `brand/` directory at repo root (canonical source of truth) | 🔲 TODO | Engineering | — |
| 4.2 | Create `brand/guidelines/brand-guidelines.md` (full document) | 🔲 TODO | Brand Strategist | 2.9, 2.10 |
| 4.3 | Create `brand/tokens/brand-tokens.json` (design tokens) | 🔲 TODO | Product Designer | 2.9 |
| 4.4 | Import brand assets to `brand/logos/`, `brand/print/`, etc. | 🔲 TODO | Engineering | 4.1 |
| 4.5 | Create symlink from `static/brand/` → `brand/` (or copy in CI) | 🔲 TODO | DevOps | 4.1, 4.4 |
| 4.6 | Update Marketing SOP to reference `brand/` paths | 🔲 TODO | CMO | 4.1 |
| 4.7 | Create press kit ZIP with all brand assets | 🔲 TODO | IR Lead | 4.4 |
| 4.8 | Upload press kit to website | 🔲 TODO | Engineering | 4.7 |
| 4.9 | Create CLI ASCII logo from official wordmark | 🔲 TODO | Engineering | — |
| 4.10 | Add brand headers to key documentation files | 🔲 TODO | Technical Writer | 4.2 |

### Phase 5: Governance & Verification 📋 PLANNED
**Duration:** Week 4-5 (September 22 - October 3, 2026)

| # | Task | Status | Owner | Dependencies |
|---|------|--------|-------|--------------|
| 5.1 | Cross-surface visual audit (all touchpoints) | 🔲 TODO | Brand Strategist | All |
| 5.2 | J.A.R.V.I.S. regression check (dashboard untouched) | 🔲 TODO | CTO | All |
| 5.3 | Create `brand/CHANGELOG.md` | 🔲 TODO | Brand Strategist | 4.1 |
| 5.4 | Brief all executives on brand usage (30-min session) | 🔲 TODO | CMO | 4.2 |
| 5.5 | CEO final sign-off on brand rollout | 🔲 TODO | CEO | 5.1, 5.2 |
| 5.6 | Internal announcement (all-hands / email) | 🔲 TODO | CMO | 5.5 |
| 5.7 | Schedule quarterly brand audit (Q4: January 2027) | 🔲 TODO | Brand Strategist | 5.5 |
| 5.8 | Confirm trademark registration status with Legal | 🔲 TODO | CLO | — |

### Phase 6: Extended Brand System 📋 FUTURE
**Duration:** Ongoing (Q4 2026 - Q1 2027)

| # | Task | Status | Owner | Dependencies |
|---|------|--------|-------|--------------|
| 6.1 | Create illustration style guide | 🔲 TODO | Content Creator | 4.2 |
| 6.2 | Create iconography system (UI icons, feature icons) | 🔲 TODO | Product Designer | 4.2 |
| 6.3 | Create photography guidelines | 🔲 TODO | CMO | 4.2 |
| 6.4 | Create motion/animation principles | 🔲 TODO | Product Designer | 4.2 |
| 6.5 | Create co-branding templates for partners | 🔲 TODO | Brand Strategist | 4.2 |
| 6.6 | Create conference/event banner templates | 🔲 TODO | Content Creator | 4.4 |
| 6.7 | Create swag/merchandise templates | 🔲 TODO | Content Creator | 4.4 |
| 6.8 | Build brand asset management portal (optional) | 🔲 TODO | Engineering | 4.1 |

---

## Asset Inventory

### Logos (`static/brand/logos/`)
| Variant | Files | Primary Use |
|---------|-------|-------------|
| Full Logo | 6 raster + 6 vector | Headers, covers, presentations |
| Icon Only | 4 PNG | Avatars, favicons, small spaces |
| Text Only | 2 PNG | Horizontal headers, footers |
| Grayscale | 4 PNG | B&W print, legal documents |

### Print Materials (`static/brand/print/`)
| Asset | Files | Use |
|-------|-------|-----|
| Letterhead 1 | SVG, PDF | Standard correspondence (navy header bar) |
| Letterhead 2 | SVG, PDF | Alternative design |
| Email Signature 1 | PNG | Simple design |
| Email Signature 2 | SVG, PNG | Recommended — navy border frame |

### Social Media (`static/brand/social/`)
| Asset | Files | Use |
|-------|-------|-----|
| Facebook Cover 3 | SVG, PDF | Facebook/LinkedIn cover photo |

### Templates (`static/brand/templates/`)
| Asset | File | Status |
|-------|------|--------|
| Pitch Deck | `pitch-deck.pptx` | ✅ Generated (13 slides) |
| Board Meeting | `board-meeting.pptx` | ✅ Generated (9 slides) |
| One-Pager | `one-pager.html` | ✅ Created |
| Investor Update Email | `investor-update-email.html` | ✅ Created |
| Email Signature | `email-signature.html` | ✅ Created |

---

## Brand Identity

| Element | Value |
|---------|-------|
| **Company Name** | LIGHTSPEED HOLDINGS LIMITED |
| **Tagline** | ASPIRE. ACT. ACHIEVE. |
| **Primary Color** | Dark Navy `#070A40` |
| **Accent — Red** | `#E63946` |
| **Accent — Cyan** | `#00BFFF` |
| **Neutral — Light Grey** | `#F2F2F2` |
| **Neutral — White** | `#FFFFFF` |
| **Logo Symbol** | Lighthouse/shield emblem with signal waves |

---

## RACI Matrix

| Activity | CEO | CMO | Brand Strat | IR Lead | Product Design | Engineering | CFO | CLO |
|----------|-----|-----|-------------|---------|----------------|-------------|-----|-----|
| Brand vision & direction | **A** | R | C | C | — | — | — | — |
| Logo/color/typography specs | I | C | **R** | C | C | — | — | — |
| Asset organization | I | I | C | **R** | — | C | — | — |
| Template creation | I | C | C | **R** | C | — | — | — |
| Dashboard integration | I | — | C | — | C | **R** | — | — |
| CLI branding | I | — | C | — | C | **R** | — | — |
| Print orders | I | C | — | C | — | — | **R** | — |
| Legal/trademark review | A | — | — | — | — | — | — | **R** |
| Social media deployment | I | **A** | C | C | — | C | — | — |
| Final sign-off | **R** | C | C | C | — | — | — | — |

**R** = Responsible | **A** = Accountable | **C** = Consulted | **I** = Informed

---

## Escalation Matrix

| Condition | Escalate To | SLA |
|-----------|------------|-----|
| Brand violation on public surface | CMO → Chief of Staff | Immediate |
| J.A.R.V.I.S. theme regression | CTO → Chief of Staff → CEO | Immediate |
| Asset not available in required format | Brand Strategist → CMO | 24 hours |
| Budget overrun on print/distribution | CFO → CEO | 24 hours |
| Legal/trademark concern | CLO → CEO | Immediate |
| Stakeholder disagreement on asset selection | CMO decides; CEO if unresolved | 48 hours |

---

## Risk Register

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|------------|------------|
| R1 | J.A.R.V.I.S. theme contamination into public brand | Critical | Medium | Namespace isolation; CI gate on control-plane-theme.css |
| R2 | Inconsistent brand usage across surfaces | High | Medium | Single guidelines doc + quarterly audit |
| R3 | Missing asset formats for specific use cases | Medium | Low | Complete asset catalog in Phase 1; adapt as needed |
| R4 | Print vendor delays | Medium | Low | Order early in Phase 3; digital assets launch independently |
| R5 | Trademark not registered | High | Unknown | Confirm status with Legal immediately |
| R6 | Old "LS" placeholder still visible somewhere | Medium | High | Phase 1 logo swap complete; verify after deployment |
| R7 | Team members use personal email signatures | Medium | High | Deploy org-wide HTML signature; IT enforcement |
| R8 | Scope creep ("let's redesign the dashboard too") | High | Medium | CEO constraint explicit: J.A.R.V.I.S. stays |

---

## Success Criteria

| Metric | Target | Measured By |
|--------|--------|-------------|
| All public surfaces use official branding | 100% | Brand Strategist audit |
| J.A.R.V.I.S. theme untouched | 0 changes to control-plane-theme.css | Git diff check |
| Brand guidelines document complete | Published to brand/guidelines/ | Brand Strategist |
| Print assets ordered | Business cards + letterhead in production | CFO confirmation |
| Time to complete | ≤ 5 weeks | Chief of Staff tracking |
| Budget adherence | Within approved budget | CFO tracking |
| Executive briefing completed | All execs briefed on brand usage | CMO confirmation |

---

## Quick Reference

### Logo Usage
| Context | Variant | Format |
|---------|---------|--------|
| Website header | fulllogo_transparent | SVG/PNG |
| Favicon | icononly | PNG (32x32) |
| CLI --help | icononly_nobuffer or ASCII | PNG/text |
| Email signature | Per signature template | PNG |
| Business cards | Design 1 (pre-designed) | SVG/PDF/EPS |
| Letterhead | Letterhead 1 (navy header bar) | SVG/PDF |
| Social profile | icononly_transparent | PNG (400x400) |
| Social cover | Facebook Cover 3 | SVG/PDF |
| Investor decks | fulllogo_transparent | PNG/SVG |
| Legal documents | grayscale | PNG |

### Minimum Sizes
| Variant | Print | Screen |
|---------|-------|--------|
| Full Logo | 30mm wide | 120px wide |
| Icon Only | 12mm wide | 32px wide |

### Clear Space
Minimum clear space = height of the "L" in "LIGHTSPEED" on all sides.

---

*Document maintained by Chief of Staff. Updates require CEO approval.*
*Next review: End of Phase 5 (October 3, 2026)*
