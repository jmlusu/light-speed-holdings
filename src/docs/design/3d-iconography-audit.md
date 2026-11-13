# Regipedia & LightSpeed 3D Iconography Audit

**Document Version:** 1.0.0
**Status:** Completed Audit & Taxonomy
**Scope:** Application-wide icon audit across all pages, navigation, components, forms, and interactive states.

---

## 1. Overview & Audit Objectives

This document performs a comprehensive icon inventory of the application to transition from legacy flat icons to a unified **3D Blue-Glass & Metallic-Gold Iconography System**.

### Primary Goals:
1. Map every functional and illustrative icon across all routes and components.
2. Categorize icons into **High-Priority Illustrative 3D Assets** vs **Functional Utility Icons** (which remain crisp inline glyphs for usability).
3. Establish semantic identifier mappings for the centralized `<Icon3D />` registry.

---

## 2. Comprehensive Application Icon Inventory

| ID | Location / Route | Component | Current Icon / Element | Semantic Category | Proposed 3D Asset | Priority | Replacement Strategy |
|---|---|---|---|---|---|---|---|
| **ICO-01** | Global Navigation | `FloatingNav.tsx` | Logo Emblem / Brand Mark | `brand-emblem` | 3D Blue-Glass Lighthouse & Gold Shield | High | Replace with 3D glass-gold emblem |
| **ICO-02** | Global Header | `FloatingNav.tsx` | Sun / Moon Theme Toggle | `theme-toggle` | Utility Glyph | Functional | Retain crisp utility icon with gold hover glow |
| **ICO-03** | Global Header | `FloatingNav.tsx` | Menu / X Mobile Nav | `mobile-menu` | Utility Glyph | Functional | Retain responsive utility toggle |
| **ICO-04** | Home (`/`) | `IntroductionSection.tsx` | Brain Icon | `intelligence` / `ai-native` | 3D Blue Glass Brain with Metallic Gold Neural Core | High | Replace with `<Icon3D name="intelligence" />` |
| **ICO-05** | Home (`/`) | `IntroductionSection.tsx` | ShieldCheck Icon | `evidence` / `compliance` | 3D Blue Glass Shield with Gold Checkmark | High | Replace with `<Icon3D name="security" />` |
| **ICO-06** | Home (`/`) | `IntroductionSection.tsx` | Landmark Icon | `governance` / `finance` | 3D Blue Glass Columns with Gold Pediment | High | Replace with `<Icon3D name="governance" />` |
| **ICO-07** | Home (`/`) | `IntroductionSection.tsx` | Africa Map Icon | `geography` / `sectors` | 3D Glass Continent Map with Gold Node Points | High | Replace with `<Icon3D name="location" />` |
| **ICO-08** | Home (`/`) | `LightSpeedProposition.tsx` | Brain (Dimension 1) | `intelligence` | 3D Blue Glass Brain with Gold Synapse Bevels | High | Replace with `<Icon3D name="intelligence" />` |
| **ICO-09** | Home (`/`) | `LightSpeedProposition.tsx` | GitBranch (Dimension 2) | `orchestration` | 3D Blue Glass Routing Nodes with Gold Flow Rays | High | Replace with `<Icon3D name="orchestration" />` |
| **ICO-10** | Home (`/`) | `LightSpeedProposition.tsx` | ShieldCheck (Dimension 3) | `governance` | 3D Blue Glass Sovereign Shield with Gold Crest | High | Replace with `<Icon3D name="governance" />` |
| **ICO-11** | Home (`/`) | `HAOMTGVSection.tsx` | Human, Agents, Orchestration, Memory, Tools, Gov, Value | `haomtgv-framework` | 7 Specialized 3D Glass & Gold Layer Icons | High | Replace all 7 layer badges with `<Icon3D />` |
| **ICO-12** | Home (`/`) | `HumanApprovalMatrix.tsx` | Tier 1 to Tier 5 Gate Icons | `approval-matrix` | 3D Bounded Approval Gates (Blue Glass & Gold Seals) | High | Replace gate badges with 3D icons |
| **ICO-13** | Home (`/`) | `WhatWeBuildGrid.tsx` | Enterprise Platform Icons | `solutions` / `categories` | 3D Glass Cube & Gold Module Icons | High | Replace with 3D solution cards |
| **ICO-14** | Home (`/`) | `GovernanceSecuritySection.tsx` | Lock, FileCheck, Shield, Key | `security` / `compliance` | 3D Glass Vault, Gold Key & Immutable Ledger | High | Replace with `<Icon3D name="security" />` |
| **ICO-15** | What We Do (`/what-we-do`) | `WhatWeDoPage.tsx` | Capability & Sector Cards | `capabilities` | 3D Glass & Gold Enterprise Capability Badges | High | Replace with `<Icon3D />` registry |
| **ICO-16** | AI Assessment (`/ai-assessment`) | `AiAssessmentPage.tsx` | Readiness Wizard Steps | `assessment` / `verification` | 3D Glass Meter & Gold Gauge Icons | High | Replace step indicators |
| **ICO-17** | Pharos Insights (`/insights`) | `InsightsPage.tsx` | BookOpen, Shield, Download | `reports` / `documents` | 3D Glass Whitepaper & Gold Seal | High | Replace paper cards with 3D icons |
| **ICO-18** | About (`/about`) | `AboutPage.tsx` | History, Mission, Values | `organization` | 3D Glass Globe & Gold Compass | High | Replace value cards with 3D icons |
| **ICO-19** | Contact (`/contact`) | `ContactPage.tsx` | Mail, Phone, MapPin, Send | `support` / `contact` | 3D Blue Glass Envelope with Gold Seal & Cyan Ray | High | Replace hero contact cards |
| **ICO-20** | Modal Overlays | `ExecutiveBriefingModal.tsx` | Briefing Form Controls | `notifications` | 3D Blue Glass Briefing Badge with Gold Clapper | High | Replace modal header graphic |

---

## 3. Retained Utility Icons (Functional Glyph Policy)

To preserve usability and responsiveness, small inline UI glyphs are classified as **Functional Utilities**. They maintain clean outline SVG rendering while incorporating cyan and gold hover highlights:
- Table column sort arrows (`ArrowUpDown`)
- Accordion open/close chevrons (`ChevronDown`, `ChevronUp`)
- Modal dismiss controls (`X`)
- Form validation inline badges (`CheckCircle2`, `AlertTriangle`)
- Pagination controls (`ChevronLeft`, `ChevronRight`)

---

## 4. Summary & Implementation Roadmap

All **20 core application icon contexts** have been mapped to 15 semantic 3D icon identifiers in the `<Icon3D />` registry. The centralized component will provide transparent background rendering, responsive scaling, theme adaptability, and accessible descriptions.
