# Spec: Geographic Positioning & Market Architecture Refinement

## Objective
Refine LightSpeed Holdings' geographic and market positioning across the entire website to clearly communicate:
- **Origin**: Based in Malawi (headquartered in Lilongwe)
- **Operating Context**: Designed for African operating realities
- **Primary Market**: Africa (not limited to SADC/Southern Africa)
- **Broader Reach**: Open to appropriate opportunities beyond Africa

The website must communicate origin and focus without creating a geographic ceiling.

## Tech Stack
- React 18 + TypeScript
- Vite build system
- Tailwind CSS (via brand tokens)
- React Router for navigation
- Vitest for testing

## Commands
```bash
# Development
npm run dev

# Build
npm run build

# Test
npm test

# Lint
npm run lint

# Type check
npm run typecheck
```

## Project Structure
```
src/
├── data/
│   ├── siteContent.ts          # Main content model (company, solutions, proof, etc.)
│   ├── homeImmersiveCopy.ts    # Homepage hero/immersive copy
│   ├── faqs.ts                 # FAQ content
│   ├── ctas.ts                 # Call-to-action definitions
│   ├── sectors.ts              # Sector definitions
│   ├── capabilities.ts         # Capability definitions
│   ├── insights.ts             # Insights/Pharos content
│   └── registries/
│       ├── claims-registry.json
│       ├── solution-registry.json
│       ├── sector-registry.json
│       ├── use-case-registry.json
│       ├── faq-registry.json
│       └── cta-registry.json
├── pages/
│   ├── Index.tsx               # Homepage
│   ├── AboutPage.tsx
│   ├── WhatWeDoPage.tsx
│   ├── SectorsPage.tsx
│   └── ...
├── components/
│   ├── Hero.tsx
│   ├── AboutSection.tsx
│   └── site/                   # Reusable page components
└── index.html                  # SEO metadata
```

## Code Style
- TypeScript with explicit types
- Inline styles using CSS variables from brand tokens
- Functional React components
- lucide-react for icons
- Honesty badges on all claims

## Testing Strategy
- Unit tests for data transformations (Vitest)
- Integration tests for component rendering
- No e2e tests currently

## Boundaries
**Always:**
- Preserve honesty badge architecture (PROVEN IN-HOUSE, PILOT, FIELDABLE, etc.)
- Maintain claim verification through claims-registry.json
- Keep "AI executes. Humans decide." principle
- Preserve Human CEO / human accountability model

**Ask First:**
- Changes to claims-registry.json classifications
- New geographic claims not in existing evidence
- Changes to legal entity information

**Never:**
- Invent clients, partnerships, or countries of operation
- Claim global operations without evidence
- Claim African-wide deployment without verification
- Remove Malawi from company identity
- Make SADC the geographic ceiling
- Replace factual regional claims with vague "global" marketing language

## Success Criteria
1. Homepage hero communicates: "An AI-native company builder based in Malawi, building practical, governed agentic AI systems for organisations across Africa and beyond"
2. "The AI-native company builder for Southern Africa" replaced with "An AI-native company builder built for African operating realities"
3. All "Malawi, SADC, and Africa" constructions updated to "Africa and beyond" or appropriate hierarchy
4. Footer reads: "Based in Malawi | Working across Africa and beyond" or "Built in Malawi. Designed for Africa. Open to the world."
4. SEO metadata reflects Africa-focused positioning without overclaiming
5. All sector `region` arrays updated to reflect Africa primary market
6. FAQ answers updated per directive
7. No unsupported international client/operation claims introduced
8. All existing evidence classifications (PROVEN IN-HOUSE, PILOT, etc.) preserved
9. `npm test` passes
10. `npm run build` passes

## Open Questions
- Should "Southern Africa" be completely removed from hero/positioning or kept as "regional experience" context?
- The directive says "The word 'Southern' should not appear in the company's core positioning unless the content specifically concerns Southern Africa" - confirm this applies to hero/positioning statements only
- Should "Lilongwe" be kept in legal/contact pages but removed from marketing copy?
- Are the solution registry "region" fields used anywhere currently? (They don't exist in solution-registry.json)

## Files to Modify
Based on the audit, the following files require changes:

### Primary Content Files
1. `src/data/siteContent.ts` - company identity, heroSubline, solutions descriptions, insightCategories, proofCaseStudies
2. `src/data/homeImmersiveCopy.ts` - heroLead
3. `src/data/faqs.ts` - FAQ answers (data-protection, proven-clients, sectors)
4. `src/data/registries/faq-registry.json` - FAQ answers (faq-01, faq-18)
5. `src/data/registries/sector-registry.json` - region arrays, descriptions
6. `src/data/registries/solution-registry.json` - descriptions referencing Southern Africa
7. `src/data/registries/use-case-registry.json` - businessValue fields referencing SADC
8. `src/data/capabilities.ts` - description referencing Malawi, SADC, Africa
9. `src/data/insights.ts` - insight titles/categories

### Page Components
10. `src/pages/Index.tsx` - footer copy, logo alt text (if needed)
11. `src/pages/WhatWeDoPage.tsx` - PageIntro lead
12. `src/pages/SectorsPage.tsx` - PageIntro lead
13. `src/components/AboutSection.tsx` - Mission, Vision, operating across text
14. `src/components/Hero.tsx` - (uses homeImmersiveCopy, already covered)

### SEO/Metadata
15. `index.html` - title, meta description, og:description

### Legal/Contact (Preserve Lilongwe)
- `src/pages/TermsPage.tsx` - Keep Lilongwe (legal requirement)
- `src/pages/PrivacyPage.tsx` - Keep Lilongwe (legal requirement)
