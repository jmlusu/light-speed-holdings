# Deliverable 8: Recommended Implementation Sequence

This deliverable recommends the safest implementation order for restoring the intended AI Studio experience in OpenCode while preserving the existing production architecture and approved LightSpeed brand direction.

## Implementation Priority Order

Changes are organized into 6 phases. Within each phase, tickets that are independent (no cross-dependencies) can be handled in parallel; tickets with dependencies must follow the ordered sequence.

### Phase 1: Deployment Blockers (Immediate — Fix Before Any Launch)

**Objective:** Fix critical issues that block production deployment or violate compliance.

**Order & Rationale:**
1. **P0-01: Use case detail pages** — Fixes broken navigation on `/use-cases` section. This is the highest-priority functional blocker; all 16 detail pages currently render "Use case not found." Fix by retargeting `UseCaseDetailPage` imports to relative path (same as `UseCasesPage`). **No dependencies.**

2. **P0-02: Hero image alt text** — WCAG 1.1.1 compliance critical fix. Empty alt attribute violates accessibility standards. **No dependencies.** Can fix simultaneously with P0-01.

3. **P0-03: 6 architecture SVG files** — Missing SVGs referenced in media registry create broken asset references. Create the 6 missing SVG files at declared paths, OR remove registry entries. **No dependencies.** Can fix simultaneously with P0-01/P0-02.

4. **P0-04: Turnstile production verification** — Must verify production hostname before launch to avoid 400020 errors on contact/briefing/submit flows. **No dependencies.** Can fix simultaneously with other P0 tickets.

**Phase 1 Deliverable:** All 4 P0 tickets fixed before any production deployment or public launch.

---

### Phase 2: Critical Visual Restoration (Brand-Compliance-Led)

**Objective:** Restore visual elements that affect the user experience without conflicting with "Calm Intelligence" brand guardrails.

**Order & Rationale:**
1. **P1-01: Focus ring color** — Changes `focus-visible:ring-ls-red` to `focus-visible:ring-ls-cyan` on CTA buttons. This is a keyboard accessibility fix that also aligns with the design system. **No dependencies.** Can fix simultaneously with other P1 tickets.

2. **P1-02: Link color on light mode** — Changes `text-ls-red` to `text-ls-navy` for links per design system §155. **No dependencies.** Can fix simultaneously with P1-01.

3. **P1-03: Use case thumbnail format standardization** — Standardizes all 12 use case thumbnail entries to support both webp and avif. **No dependencies.** Can fix simultaneously with P1-01/P1-02. May require adding webp/avif files to `public/assets/use-cases/`.

4. **P1-04: Hero webp/avif format** — Aligns registry with actual hero imagery. Three options: (a) add webp/avif files at `public/assets/hero/`, (b) update registry to remove webp/avif from hero-home entry, or (c) keep JPEG and document. **No dependencies.** Can fix simultaneously with other P1 tickets. Decision should be made product-first.

**Phase 2 Deliverable:** All 4 P1 tickets fixed. Visual restored without brand guardrail conflicts. Format decisions (P1-03, P1-04) should follow the format standardization principle: support both webp and avif where possible, or choose one format consistently.

---

### Phase 3: Missing or Disconnected Functionality (Product Decisions)

**Objective:** Restore features that were present in the AI Studio prototype but are missing in OpenCode. Each ticket requires a product decision.

**Order & Rationale:** These tickets are independent of each other but each requires a go/no-go decision. They can be worked on in parallel after Phase 2.

**Tickets (work in parallel after Phase 2 completion):**
- **P2-01: Reveal on-mount trigger** — Add `initial` prop or mount trigger to `Reveal` component. Decision: restore on-mount entrance animations (matching AI Studio prototype) OR accept scroll-triggered-only behavior per Calm Intelligence brand. If restoring, may depend on animation library install (Framer Motion/GSAP).

- **P2-02: Human Approval Matrix visualization** — Decision: create interactive 5-tier matrix visualization on homepage, OR document as intentional per brand. If creating interactive component, may need design resources.

- **P2-03: Value pillars on homepage** — Decision: (a) add standalone 5-pillar section between proposition and pathways, OR (b) add about summary/tagline to footer/her, OR (c) document as intentional redesign. Values already exist in AboutPage and HaomtGVSection.

- **P2-04: Delivery lifecycle section** — Decision: restore dedicated section, OR document as intentional omission. Content may be covered in HaOMGV pillars and WhatWeDoPage approach section.

- **P2-05: About section on homepage** — Decision: add about summary/tagline to homepage, OR document as intentional IA decision. Tagline "MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY" available in design system.

- **P2-06: Pharos sharing UI** — Decision: add sharing buttons (Twitter, LinkedIn, email) to insights/index/pages, OR accept that sharing is not part of current implementation.

- **P2-07: Executive briefing modal transition** — Decision: inspect `ExecutiveBriefingModal.tsx`; add Framer Motion/GSAP transition if prototype had animated modal, OR document transition behavior.

- **P2-08: Mobile drawer slide transition** — Add `transform transition` to FloatingNav mobile menu `div`. Straightforward CSS enhancement.

- **P2-09: Five-tier approval matrix visual** — Decision: create visual matrix on homepage, OR document as intentional per Calm Intelligence brand (no fixed agent count as standard offering). Must preserve guardrail: no presenting fixed agent count as standard client offering.

- **P2-10: Contact API behavior** — Test contact form end-to-end; verify API endpoint; add success/error feedback. May depend on backend deployment outside audit scope.

**Phase 3 Deliverable:** Product decisions made on all P2 tickets. Functionality restored or documented as intentional per brand direction.

---

### Phase 4: Animation and Motion Restoration

**Objective:** Restore animation behaviors from the AI Studio prototype.

**Order & Rationale:**
1. **If animation libraries installed in Phase 3** (depends on P2-01 decision): Install Framer Motion or GSAP if on-mount Reveal or modal transitions require them.

2. **P2-01 follow-up: Reveal component enhancement** — If decision was to restore on-mount animations: implement `initial` mount trigger in `Reveal` component. May use simple CSS `animation` property or Framer Motion depending on complexity.

3. **P2-07: Executive briefing modal transition** — If prototype had animated modal: add entrance/exit transition using same library as Reveal component.

4. **P2-08: Mobile drawer slide transition** — Add `transform transition duration-300` to FloatingNav mobile menu. Straightforward CSS; no animation library needed.

**Phase 4 Deliverable:** Animation behaviors restored per prototype specifications, or documented as intentional per Calm Intelligence brand. If animation libraries installed, all Reveal and modal animations use consistent library.

---

### Phase 5: Secondary Page Improvements

**Objective:** Improve existing pages and resolve minor discrepancies.

**Tickets (work in parallel, low risk):**
- **P3-01: Tailwind CSS v3/v4 monitoring** — Run build/lint; no action unless classes malfunction.
- **P3-02: Brand token divergence documentation** — Document grey-light divergence; no action unless token revision.
- **P3-03: Architecture SVG gaps documentation** — If no component references these SVGs, gap accepted as future-proofing.
- **P3-04: Micro-illustration glyph usage audit** — Search component imports; map usage or accept as unmapped but existing.
- **P3-05: Use case slug count documentation** — Document 16 vs 13 slug discrepancy; no user-visible impact.
- **P3-06: Hero overlay hardcoded values** — Document `bg-black/40`/`bg-black/60` as intentional if no tokens match; or replace with closest token.
- **P3-07: Page transition animations decision** — Add transitions using React Router or Framer Motion if prototype had them; OR accept instant navigation.
- **P3-08: Delivery lifecycle concept documentation** — Document that lifecycle is present in HAOMTGV pillars and WhatWeDoPage approach section.
- **P3-09: About tagline decision** — Add tagline to homepage footer/her, OR document as intentional IA decision.
- **P3-10: Global focus ring audit** — Audit all button focus-visible rings; change `ls-red` to `ls-cyan` where design system requires; document any intentional red usage.

**Phase 5 Deliverable:** All P3 tickets resolved. Minor improvements implemented; discrepancies documented or resolved.

---

### Phase 6: Final Responsive and Accessibility Refinement

**Objective:** Ensure the site is fully responsive and accessible.

**Tickets:**
- **Verify mobile responsiveness** across all routes after previous phases — test hero, pathways, HAOMTGV, solutions, about, insights, contact on mobile and desktop viewports.
- **Verify accessibility** — after P1-01 (focus ring), P1-02 (link color), P0-02 (alt text), run accessibility audit (axe, Lighthouse) to confirm WCAG 2.1 AA compliance.
- **Verify reduced-motion** — confirm `prefers-reduced-motion` still disables Reveal animations and no other motion-dependent interactions break.
- **Verify theme switching** — confirm dark/light toggle persists and colors switch correctly across all pages.
- **Verify responsive grid columns** — confirm all sections restructure at breakpoints (1→2→3→4 or 1→2→3 columns) without content overflow.
- **Verify console errors** — run production build; confirm no new console errors introduced by changes.

**Phase 6 Deliverable:** Site is verified for responsiveness, accessibility, and production readiness.

---

## Summary of Implementation Sequence

| Phase | Focus | Tickets | Key Dependencies |
|---|---|---|---|
| 1 | Deployment Blockers (P0) | 4 tickets (P0-01 through P0-04) | None — all independent |
| 2 | Critical Visual Restoration (P1) | 4 tickets (P1-01 through P1-04) | None — all independent; format decisions (P1-03, P1-04) should align |
| 3 | Missing/Disconnected Functionality (P2) | 10 tickets (P2-01 through P2-10) | Product decisions required each; no technical dependencies between tickets |
| 4 | Animation and Motion (P2 subset) | 4 tickets (depends on P2-01 decision) | If on-mount animations: install animation library; then implement Reveal/modal enhancements |
| 5 | Secondary Page Improvements (P3) | 10 tickets (P3-01 through P3-10) | Independent; monitoring and documentation |
| 6 | Final Refinement (P3) | 6 verification tickets | Depends on all previous phases completing; runtime verification |

**Estimated Sequence Duration:**
- Phase 1 (deployment blockers): 1–2 days
- Phase 2 (visual restoration): 1–2 days
- Phase 3 (functionality restoration): 3–5 days (product decision time)
- Phase 4 (animations): 2–3 days (if animation library installed)
- Phase 5 (secondary improvements): 2–3 days
- Phase 6 (final verification): 1–2 days

**Total Estimated Time:** 10–17 days from kickoff, depending on product decision velocity on P2 tickets.

*No implementation is authorized during this audit. This sequence is for planning a subsequent implementation phase.*
