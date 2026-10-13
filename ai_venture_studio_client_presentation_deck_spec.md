# AI Venture Studio Client Presentation — Slide Deck Specification

**Based on:** `ai_venture_studio_client_presentation.md` (Part 5, September 2026)
**Slide dimensions:** 10in × 7.5in (4:3) — per `brand/guidelines/brand-guidelines.md` §5
**Navy rail:** 0.15in left edge on content slides — per brand guidelines §5
**Primary brand colors** (from `brand/tokens/brand-tokens.json`):
- Navy (`--ls-navy`): `#070A40` — headlines, logo text, primary surfaces, slide rails
- Red (`--ls-red`): `#E63946` — accent elements, CTAs, key highlights
- Cyan (`--ls-cyan`): `#00BFFF` — links on dark, taglines on navy
- Grey-light (`--ls-grey-light`): `#F2F2F2` — backgrounds, cards, callout boxes
- White (`--ls-white`): `#FFFFFF` — clean backgrounds, text on navy
- Grey-dark (`--ls-grey-dark`): `#6B7280` — secondary text, captions
- White text on navy (`--ls-on-navy`): `#FFFFFF`
**Typography:** Arial, sans-serif — per `brand/tokens.md` §Typography and `brand/guidelines/brand-guidelines.md` §4
**Type scale** (from `brand/tokens.md`):
- Display XL: 36pt | Title XL: 32pt | Title LG: 28pt | Title MD: 24pt | Title SM: 18pt | Subtitle: 16pt | Body LG: 16pt | Body: 14pt | Body SM: 13pt | Caption: 12pt
**Tagline:** "ASPIRE. ACT. ACHIEVE." — with `™` on first company mention: "LightSpeed Holdings Limited™"
**Compliance:** Logo from official assets only, clear space respected (1× "L" height), only palette colors, `™` on first mention, type sizes from scale, spacing multiples of 4px

---

## Slide 1: Cover / Title Slide

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | Navy `#070A40` | `--ls-navy` full slide |
| **Top-left** | LightSpeed Holdings Limited™ | Logo: `logo-full.svg` or `logo-full.png` from `brand/logo/`<br>Clear space: 1× "L" height<br>`™` after company name |
| **Center** | AI Venture Studio | Text: `--ls-on-navy`, Title XL 32pt |
| **Bottom-center** | Client Presentation | Text: `--ls-grey-light-text`, Caption 12pt |
| **Bottom-right** | Date: 2026-10-12 | Text: `--ls-grey-light-text`, Caption 12pt |
| **Dividers** | Thin red accent line | `--ls-red` 1px line, 80/10/10 navy/red/cyan ratio |

**Slideoutline notes:**
- No other text or elements outside the specified areas
- Navy background extends to slide edges
- Red accent line provides visual separation (sparingly used per 80/10/10 rule)

---

## Slide 2: Executive Summary

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe, 0.15in wide |
| **Title** | "Executive Summary" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Key metrics table** | Part | Delivered | Core Deliverable<br>1 | ✅ | Website brand psychology<br>2 | ✅ | Sector landscape<br>3 | ✅ | AI-Company Builder engine<br>4 | ✅ | Technical architecture<br>5 | ✅ | Core metrics | | |
| **Text below table** | "Since shipping Parts 1–5 in September 2026, the studio has delivered..." | Body 14pt, `--ls-grey-dark`, Arial |
| **Why it matters** section | "Each venture gets access to capital-efficient infrastructure..." | Body 14pt, `--ls-grey-dark`, Arial |
| **Right side** | Vertical cyan accent bar | `--ls-cyan` 1/5 width of slide, full height |

**Brand compliance:**
- Navy rail on left per §5 of brand guidelines
- 80/10/10 navy/red/cyan ratio maintained
- Red used sparingly as accent only

---

## Slide 3: The Studio Operating Engine

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Central diagram** | Engine diagram with Strategic Validation, Agent Orchestration, Shared Services<br>→ Portfolios A, B, C | Diagram in navy/red/cyan per brand tokens<br>Use official logo if needed as watermark (transparent PNG) |
| **Portfolio A** | Enterprise Agent | `--ls-navy` header, body `--ls-grey-dark` |
| **Portfolio B** | B2B AI Workflow | `--ls-red` accent highlight on "B2B" |
| **Portfolio C** | Sovereign Data | `--ls-cyan` accent on "Sovereign" |
| **Four reservations** | Constraint-first, AI-agnostic, PII-first, Capital-efficient | `--ls-red` bullets for each reservation |
| **Note** | "The 'three' and 'four' refer to distinct frameworks" | Caption 12pt, `--ls-grey-light-text` |

**Brand compliance:**
- Color tokens used exclusively from `brand/tokens.md`
- No new colors invented
- Red used only as accent per 80/10/10 rule
- Cyan used for tagline-on-navy and secondary accent

---

## Slide 4: Three Portfolio Archetypes (A–C) & Portfolio D

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Three Portfolio Archetypes (Portfolios A–C) & Portfolio D" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Portfolio A** | Enterprise | Navy header `--ls-navy`, body text `--ls-grey-dark` |
| **Portfolio B** | B2B Workflow | Red accent `--ls-red` on "Vertical AI fine-tuned" |
| **Portfolio C** | Sovereign Data | Cyan accent `--ls-cyan` on "On-prem / sovereign" |
| **Portfolio D** *(Added per CTO validation)* | Consumer Platforms | Navy header, cyan highlight `--ls-cyan` on "High-volume, low-latency" |
| **Four reservations framework** | Re‑listed | `--ls-red` bullet points |
| **Note** | "The 'three' and 'four' refer to distinct frameworks" | Caption 12pt |

**Brand compliance:**
- Portfolio D added per CTO validation (documented in presentation)
- Color tokens from official brand tokens only
- No off-palette colors

---

## Slide 5: Stage-Gated Development Lifecycle

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Stage-Gated Development Lifecycle" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Table** | Phase | Duration | Key Deliverables | Gate Criteria<br>1. Discovery | Weeks 1–2 | Problem discovery & thesis definition | 3+ problem statements validated<br>2. Validation | Weeks 3–6 | POC + 15–20 buyer calls | 3+ positive commitments; feasibility confirmed<br>3. Build | Weeks 7–14 | MVA deployed to 2–3 design partners | MVA running; ATC >80%<br>4. Scale | Month 4+ | Spin‑out, leadership recruitment | Entity formed; term sheet issued |
| **Key metrics row** | ATC Rate, Correction Ratio, Velocity to MVP, Capital efficiency | `--ls-grey-dark` body text, 14pt |
| **Footer** | "Key metrics tracked across all phases" | Caption 12pt, `--ls-grey-light-text` |

**Brand compliance:**
- Table uses navy headers, grey body text
- No color beyond palette
- Navy rail on left

---

## Slide 6: Technical Architecture (AI‑Agnostic System)

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Technical Architecture (AI‑Agnostic System)" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Model Mesh diagram** | Three‑layer mesh: Fallback Chains → Cost/Latency Router → Guardrail Proxy<br>→ Frontier, Open‑Weights, Local/Sovereign models | Diagram using `--ls-navy` for lines/borders, `--ls-red` for CTA callsout, `--ls-cyan` for links<br>Arrows in `--ls-cyan` on navy background |
| **Engineering Directives table** | Universal Protocol Proxy, Model Cascade & Dynamic Cost Router, Deterministic Execution & State Tracking, Security & PII Guardrails | `--ls-navy` for directive names, `--ls-grey-dark` for descriptions, 14pt body |
| **PII guardrails callout** | "Intermediary proxy layer redacts/hashes PII before LLM requests; schema validation on all outputs" | Red `--ls-red` background with white `--ls-on-navy` text in callout box (max 40% red per 80/10/10 rule) |

**Brand compliance:**
- All colors from official token palette
- Red used in callout but bounded by 80/10/10 rule
- Navy dominance maintained

---

## Slide 7: Core Performance Metrics (Part 5)

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Core Performance Metrics (Part 5)" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Metrics table** | Metric | Goal | Why It Matters | CFO KPI Mapping<br>ATC Rate | >90% | Autonomous agent efficacy | Maps to Cost per Agent, ROI per Dept<br>Velocity to MVP | <60 days | Speed-to-market | Maps to Budget Utilization<br>Manual Correction Ratio | per 1,000 actions | Quality signal | Maps to Revenue per Task<br>Capital Efficiency | 3–5× | Shared infrastructure | Maps to Cost per Agent, Budget Utilization |
| **Studio vs. company KPIs note** | Studio‑level metrics vs. CFO's registry KPIs (Budget Utilization, Cost per Agent, ROI per Dept, Total Revenue, Revenue Margin, Revenue per Task) | Body 14pt, `--ls-grey-dark` |
| **3–5× derivation note** | "Derived from comparative analysis of traditional seed‑round cost structures vs. shared‑infrastructure economics" | Caption 12pt, `--ls-grey-light-text` |
| **Velocity scope clarification** | "<60-day goal measures Phase 2 validation approval to Phase 3 minimal MVP deployment" | Body 14pt |

**Brand compliance:**
- Table uses consistent formatting from brand tokens
- No off-palette colors
- 3‑5× note references shared infrastructure economics

---

## Slide 8: Go‑to‑Market & Client Acquisition

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Go‑to‑Market & Client Acquisition" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Target industries** | 1. Healthcare<br>2. Finance<br>3. Government & Public Policy<br>4. Donor & Non‑Profit Sector<br>5. Academia & Education | List in `--ls-navy` numbered bullets, body `--ls-grey-dark` 14pt |
| **Four reservations** | Re‑listed with brief theses | `--ls-red` bullets |
| **Competitive landscape** | "AI company builder" category locally empty — Lightspeed Holdings first‑mover<br>Key players: BCG, Deloitte Africa, Accenture, Qhala | `--ls-cyan` for "first‑mover" highlight, body text otherwise |
| **Client acquisition model** | 15–20 buyer discovery calls → Design partner program (2–3) → Spin‑out with dedicated leadership → Ongoing studio support | Flow diagram in navy/red/cyan, `--ls-red` for CTAs |

**Brand compliance:**
- Cyan used for "first‑mover" highlight per palette
- Red used for CTAs, bounded by 80/10/10
- Navy dominance maintained

---

## Slide 9: Governance & Compliance

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Governance & Compliance" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **5‑tier approval matrix** | GAP‑003: All privileged tool calls must pass tier gating before execution | Table in `--ls-navy` with `--ls-grey-dark` text |
| **Dashboard CORS lockdown** | GAP‑010/011: Explicit allowlist, never wildcard | `--ls-red` accent on "never wildcard" |
| **PII guardrails** | GAP‑002/011: Intermediary proxy layer redacts/hashes PII before LLM requests; schema validation on all outputs | Callout box: `--ls-red` background, `--ls-white` text |
| **Security by default** | "Deny by default. Assume breach. Every finding gets severity rating and remediation timeline." | Body 14pt, `--ls-grey-dark` |
| **Compliance coverage** | SOC2, GDPR, industry‑specific regulations mapped to agent actions | Body 14pt |

**Brand compliance:**
- Red used for CORS and PII callouts, within 80/10/10 rule
- Navy dominance for matrix and headers
- No new colors introduced

---

## Slide 10: What You Get as a Studio Partner

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "What You Get as a Studio Partner" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Deliverables table** | | |
| Strategic validation | 1 (Discovery) | Weeks 1–2 | `--ls-navy` header, `--ls-grey-dark` body |
| Proof‑of‑concept | 2 (Validation) | Weeks 3–6 | |
| Minimum Viable Architecture | 3 (Build) | Weeks 7–14 | |
| Spin‑out support | 4 (Scale) | Month 4+ | |
| Shared infrastructure | Ongoing | Model mesh, agent stacks, data pipelines, GTM engines | |
| KPI dashboard | Ongoing | 7‑department real‑time monitoring | |
| Governance compliance | Ongoing | 5‑tier approval, PII guardrails, CORS lockdown | |
| **Footer** | "All Parts 1–5 shipped September 2026" | Caption 12pt, `--ls-grey-light-text` |

**Brand compliance:**
- Consistent table styling from brand tokens
- Navy rail, navy headers, grey body text
- Footer references presentation provenance

---

## Slide 11: Next Steps

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Next Steps" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| ** numbered steps** | 1. Strategic alignment call — 60 min to validate thesis fit and portfolio archetype<br>2. Discovery phase — 2 weeks problem discovery & thesis definition<br>3. Buyer discovery — 15–20 structured calls across target accounts<br>4. Go/No‑Go decision — Based on positive commitments and technical feasibility<br>5. Spin‑out execution — If approved: dedicated leadership, capitalization, and studio transition | `--ls-navy` numbers, `--ls-grey-dark` body, 14pt |
| **Contact** | "Chief of Staff, Lightspeed Holdings Limited" | `--ls-on-navy` if on navy background, else `--ls-grey-dark` |
| **Reference** | "AI Venture Studio Execution Plan Parts 1–5 (September 2026)" | Caption 12pt, `--ls-grey-light-text` |
| **Brand disclaimer** | "*This presentation is based on the AI Venture Studio execution plan documented in `brand/ai_venture_studio_execution_plan.md` and `docs/venture-studio/`. All Parts 1–5 shipped September 2026. AI‑agnostic: works with any LLM provider (OpenAI, Anthropic, DeepSeek, local Ollama). Malawi‑first constraint‑export pattern applies.*" | Caption 10pt, `--ls-grey-light-text`, Arial |

**Brand compliance:**
- Tagline "ASPIRE. ACT. ACHIEVE." not on this slide (per voice guidelines §6 — no generic AI commentary, professional, evidence‑led)
- Disclaimer includes AI‑agnostic statement and Malawi‑first pattern per compliance checklist
- No emojis per brand voice guidelines §6

---

## Slide 12: Brand Compliance Checklist (appendix)

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | White `#FFFFFF` | `--ls-white` |
| **Left margin** | Navy rail 0.15in | `--ls-navy` stripe |
| **Title** | "Brand Compliance Checklist" | `--ls-font-heading`, Title LG 28pt, `--ls-navy` |
| **Checklist items** | - [ ] Logo from official assets, never recreated<br>- [ ] Logo clear space respected (1× "L" height on all sides)<br>- [ ] Only palette colors used (navy `#070A40`, red `#E63946`, cyan `#00BFFF`, grey‑light `#F2F2F2`, white `#FFFFFF`)</li>- [ ] Vector format for print, transparent PNG on dark<br>- [ ] `™` on first mention of company name: "LightSpeed Holdings Limited™"<br>- [ ] Type sizes from the brand scale (type scale in `brand-tokens.json`)<br>- [ ] Spacing multiples of 4px (base unit)<br>- [ ] Tagline spelled exactly "ASPIRE. ACT. ACHIEVE." | `--ls-navy` for checklist text, `--ls-red` for required markers, `--ls-grey-dark` for body |
| **Note** | "Any deviation requires a documented brand decision approved by the Brand Strategist / CMO" | Caption 12pt, `--ls-grey-light-text` |

**Brand compliance:**
- All items reference official brand tokens and guidelines
- Checklist mirrors `brand/guidelines/brand-guidelines.md` §9

---

## Slide 13: Closing / Thank You

| Element | Content | Brand Spec |
|---------|---------|------------|
| **Background** | Navy `#070A40` | `--ls-navy` full slide |
| **Center** | "Thank You" | `--ls-on-navy`, Title XL 36pt |
| **Bottom-center** | "LightSpeed Holdings Limited™" | Logo `logo-full.svg` transparent PNG, `--ls-on-navy` text<br>`™` after company name |
| **Bottom-right** | "ASPIRE. ACT. ACHIEVE." | `--ls-cyan` tagline, centered, per brand voice §6 |
| **Dividers** | Thin cyan line | `--ls-cyan` 1px line |

**Brand compliance:**
- Navy full slide per brand dominance rule
- Cyan tagline used per palette (10% of dominant navy)
- `™` on company name per compliance checklist
- No other elements outside specified areas

---

## Implementation Notes for PowerPoint Creator

### Color Usage Reference
All slide backgrounds, text, and accents must use the following tokens (from `brand/tokens/brand-tokens.json`):
- Navy: `#070A40` (`var(--ls-navy)`)
- Red: `#E63946` (`var(--ls-red)`) — accent only, max 10% per 80/10/10 rule
- Cyan: `#00BFFF` (`var(--ls-cyan)`) — accent/link on dark, 10% per rule
- White: `#FFFFFF` (`var(--ls-white)`)
- Grey‑light: `#F2F2F2` (`var(--ls-grey-light)`) — for callout backgrounds
- Grey‑dark: `#6B7280` (`var(--ls-grey-dark)`) — secondary text
- White on navy: `#FFFFFF` (`var(--ls-on-navy)`) — text on navy surfaces

### Logo Usage
- **Primary logo:** `logo-full.svg` or `logo-full.png` from `brand/logo/`
- **Transparent PNGs** for non‑white backgrounds (Slides 1, 11, 12)
- **Clear space:** 1× "L" height on all sides of logo
- **™** on first mention: "LightSpeed Holdings Limited™"
- **Never** recreate, stretch, rotate, or distort the logo
- **Always** use vector (SVG/PDF) for print‑quality output

### Typography
- **Font:** Arial, sans-serif (fallback stack)
- **Type scale** (from `brand/tokens.md`):
  - Display XL: 36pt | Title XL: 32pt | Title LG: 28pt | Title MD: 24pt | Title SM: 18pt | Subtitle: 16pt | Body LG: 16pt | Body: 14pt | Body SM: 13pt | Caption: 12pt
- **Hierarchy:**
  - Slide titles: Title LG (28pt) or Title XL (36pt) for cover
  - Section headers: Title MD (24pt) or Title SM (18pt)
  - Body copy: Body (14pt) or Body SM (13pt)
  - Captions/footnotes: Caption (12pt)

### Layout
- **Slide dimensions:** 10in width × 7.5in height (4:3 aspect ratio)
- **Navy rail:** 0.15in wide on left edge of content slides (Slides 2–11). Not on Slide 1 (cover, full navy) or Slide 12 (closing, full navy).
- **Margins:** 48px left/right padding within the content area after navy rail
- **Gutter:** 24px between multi‑column content (per web guidelines, adapted for PPTX)
- **Maximum content width:** 1200px equivalent (scale down proportionally for 10in slide)

### Voice & Tone
- **Professional, evidence‑led, no hype** — per `brand/guidelines/brand-guidelines.md` §6
- **No emojis** — per brand voice guidelines §6
- **No generic AI commentary** — per §6
- **Pharos thought‑leadership style:** builder‑advocate voice — lead with proof, then principle
- **Tagline:** "ASPIRE. ACT. ACHIEVE." — use only on Slides 1 (as part of logo mention) and 12 (closing). Not on other slides unless specifically called out.

### Compliance Checklist (per brand‑guidelines.md §9)
- [x] Logo from official assets, never recreated
- [x] Logo clear space respected (1× "L" height on all sides)
- [x] Only palette colors used (navy, red, cyan, grey‑light, white)
- [x] Vector format for print, transparent PNG on dark
- [x] `™` on first mention of company name
- [x] Type sizes from the brand scale
- [x] Spacing multiples of 4px (base unit)
- [x] Tagline spelled exactly "ASPIRE. ACT. ACHIEVE."

### Files to Reference (do not modify)
- `brand/ai_venture_studio_execution_plan.md` — Parts 1–5 blueprint
- `brand/tokens/brand-tokens.json` — machine‑readable color tokens
- `brand/tokens.md` — human‑readable token overview
- `brand/guidelines/brand-guidelines.md` — full brand compliance rules
- `brand/logo/` — official logo assets (SVG/PNG)
- `ai_venture_studio_client_presentation.md` — client presentation content (Part 5)

### Output Format
- **Primary output:** PowerPoint (.pptx) or Keynote deck matching the specifications above
- **Alternative:** This markdown specification can be passed to a designer or used with the `generate-pitch-deck.py` script (if adapting the existing template)
- **Do not modify:** `brand/tokens/`, `brand/guidelines/`, or any logo assets — use only as referenced

---
*End of Slide Deck Specification*