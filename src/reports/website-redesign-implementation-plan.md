# Website Redesign Implementation Plan: LightSpeed Holdings

**Audit Date**: November 3, 2026
**Auditor**: Lead Product Designer & Senior Frontend Architect

---

## 1. Primary Website Destinations & Architecture

The website enforces four primary navigation destinations in exact sequence:

1. **Home (`/`)**: 12-stage narrative introducing LightSpeed's identity, HAOMTGV architecture, Calm Intelligence, visitor paths, practice area carousel, 5-tier approval matrix, searchable 90-agent registry, applications, research briefs, company overview, FAQ, and engagement CTAs.
2. **What We Do (`/what-we-do`)**: 6 capability areas, commercial offer families A–E, honesty status badges (*Fieldable in 2026*, *In Active Development*), dual-currency MWK/USD pricing notes, and G1–G4 governance gates.
3. **Pharos (`/insights` & `/insights/:slug`)**: Executive research hub with foundational whitepapers, policy briefs, and canonical essays with full reader modal and article pages.
4. **Who We Are (`/about`)**: Verified company identity, approved mission and vision, founder bio (Founder & CEO Jack Mlusu), and operating principles.

**Persistent CTA**: `ENGAGE LIGHTSPEED` (`/contact`) in header across all viewports.

---

## 2. Phase-by-Phase Execution Sequence

### Phase 0: Audit & Specification (Complete)
- Delivered 5 comprehensive audit reports in `reports/` and `src/reports/`.
- Verified 4 primary destinations, HAOMTGV framework, 90-agent workforce registry, and 5-tier governance matrix.

### Phase 1: Shared Component & Navigation Verification
- Verified 4-destination top bar contract in `FloatingNav.tsx`.
- Verified persistent CTA `ENGAGE LIGHTSPEED` and dual-theme logo switching (`logo-light-bg.svg` vs `logo-dark-bg.svg`).

### Phase 2: Home Page Narrative & Interactive Visuals
- Verified HAOMTGV section directly after Hero.
- Verified Calm Intelligence Architecture impact image section.
- Verified 5-Tier Human Approval Matrix component with interactive tier filtering (Tiers 0–4).
- Verified Public Agent Registry displaying all 90 operating roles (89 AI agents + 1 Human CEO).

### Phase 3: What We Do & Practice Areas
- Verified 6 key capability areas and commercial offer families A–E with honesty status badges and dual-currency MWK/USD pricing notes.

### Phase 4: Pharos Research Platform
- Verified Pharos research hub, whitepaper spotlight, topic filters, and article reader modal (`PharosReaderModal.tsx`).

### Phase 5: Who We Are & Brand Compliance
- Verified `AboutPage.tsx` and `AboutSection.tsx` with mission, vision, values, founder bio, and operating principles.

---

## 3. Acceptance Criteria & Quality Gates

1. **Compilation**: `compile_applet` and `lint_applet` pass with 0 errors.
2. **Theme Consistency**: Both Light Mode and Dark Mode render with high text contrast (WCAG 2.2 AA) and smooth transitions.
3. **Brand Compliance**: Authoritative Red `#E63946`, Deep Navy `#070A40`, Cyan `#00BFFF`, Arial typography.
4. **No Fabricated Data**: All numbers (90 operating roles), claims, and articles are backed by repository registries.
