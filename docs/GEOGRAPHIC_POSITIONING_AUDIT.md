# Geographic Positioning Audit & Classification

## Classification Categories (per Directive §25)
1. **BASE** — Where LightSpeed is headquartered (Malawi/Lilongwe)
2. **EXPERIENCE** — Where current work/experiments are concentrated (Malawi, Southern Africa)
3. **FOCUS** — Principal market opportunity (Africa)
4. **REACH** — Where willing/able to work (Africa and beyond)
5. **SPECIFIC CONTEXT** — Factually useful geographic detail (e.g., "Malawi Data Protection Act", "Airtel Money")
6. **UNSUPPORTED / NEEDS REVIEW** — Creates geographic ceiling or overclaims

---

## Audit Results by File

### 1. src/data/siteContent.ts

| Line | Current Text | Classification | Issue |
|------|--------------|----------------|-------|
| 40 | `location: 'Lilongwe, Malawi'` | BASE | ✓ Keep - legal identity |
| 45 | `in Malawi, across SADC, and beyond` | EXPERIENCE + REACH | ⚠ "SADC" as boundary; should be "Africa and beyond" |
| 60-62 | `insightCategories`: 'African AI', 'Malawi technology', 'SADC technology' | FOCUS / SPECIFIC CONTEXT | ⚠ "SADC technology" as category creates ceiling; prefer "African technology" |
| 69-70 | `insightTeasers`: "The SADC AI Opportunity", "What Agentic AI Means for African Governments" | SPECIFIC CONTEXT | ✓ Keep - specific policy work |
| 111 | "built for Southern Africa" | FOCUS | ✗ Creates ceiling; should be "built for African operating realities" |
| 115 | "Southern Africa-first digital presence" | FOCUS | ✗ Creates ceiling |
| 117 | "Mobile-first websites and e-commerce built for Southern Africa" | FOCUS | ✗ Creates ceiling |
| 119 | "across Malawi and SADC" | EXPERIENCE | ⚠ Limit to "Malawi" or "African markets" |
| 121 | "African market" | FOCUS | ✓ Keep |
| 130 | "Selling online in Southern Africa" | SPECIFIC CONTEXT | ⚠ Regional context OK for payment rails |
| 131 | "Malawian and SADC SMEs" | EXPERIENCE | ⚠ Limit to "Malawian and African SMEs" |
| 280 | "Malawi Central Bank Compliance Automation" | SPECIFIC CONTEXT | ✓ Keep - specific case study |
| 292 | "SADC Agricultural Cooperative Digital Platform" | SPECIFIC CONTEXT | ✓ Keep - specific regional project |
| 293 | "across Malawi and Mozambique" | EXPERIENCE | ✓ Keep - factual |
| 304 | "University of Malawi Student Management System" | SPECIFIC CONTEXT | ✓ Keep |
| 320 | "Malawi Data Protection Act" | SPECIFIC CONTEXT | ✓ Keep - legal fact |
| 332 | "Malawi payment rails" | SPECIFIC CONTEXT | ✓ Keep - factual |

### 2. src/data/homeImmersiveCopy.ts

| Line | Current Text | Classification | Issue |
|------|--------------|----------------|-------|
| 24 | "Agentic AI systems built and operated from Malawi" | BASE | ⚠ Leads with Malawi; directive prefers "based in Malawi, building for Africa" |

### 3. src/data/faqs.ts

| Line | Current Text | Classification | Issue |
|------|--------------|----------------|-------|
| 28 | "Malawi Data Protection Act 2017/2024" | SPECIFIC CONTEXT | ✓ Keep - legal fact |
| 94 | "across Malawi, SADC, and Africa" | FOCUS | ✗ Creates ceiling; should be "across Africa and beyond" |

### 4. src/data/registries/faq-registry.json

| ID | Current Text | Classification | Issue |
|----|--------------|----------------|-------|
| faq-01 | "based in Lilongwe, Malawi... across Malawi, Africa. Positioning: The AI-native company builder for Africa." | BASE + FOCUS | ✓ Compliant per directive §25 |
| faq-18 | "targets 10 sectors across Malawi, SADC, and Africa" | FOCUS | ✗ Creates ceiling; should be "across Africa" |

### 5. src/data/registries/sector-registry.json

| Sector | region Array | Classification | Issue |
|--------|-------------|----------------|-------|
| financial-services | ["Malawi", "SADC"] | EXPERIENCE | ⚠ Should include "Africa" as primary |
| healthcare-public-health | ["Malawi", "SADC"] | EXPERIENCE | ⚠ Should include "Africa" |
| agriculture-agritech | ["Malawi", "Mozambique", "SADC"] | EXPERIENCE | ✓ Factual - specific countries |
| education-academia | ["Malawi", "SADC"] | EXPERIENCE | ⚠ Should include "Africa" |
| government-public-sector | ["Malawi", "SADC"] | EXPERIENCE | ⚠ Should include "Africa" |
| regulators-standards-institutions | ["Malawi", "SADC", "Africa"] | EXPERIENCE + FOCUS | ✓ Good |
| research-universities | ["Malawi", "SADC", "Africa"] | EXPERIENCE + FOCUS | ✓ Good |
| smes-private-enterprise | ["Malawi", "SADC"] | EXPERIENCE | ⚠ Should include "Africa" |
| development-nonprofit-organizations | ["Malawi", "SADC", "Global"] | EXPERIENCE + REACH | ✓ Good |
| technology-digital-businesses | ["Malawi", "SADC", "Global"] | EXPERIENCE + REACH | ✓ Good |

### 6. src/data/registries/solution-registry.json

| Solution | Issue |
|----------|-------|
| digital-transformation (line 77) | "built for African operating realities" — ✓ Compliant |
| intelligent-automation (line 38) | "Mobile-Money Integration (Airtel Money, TNM Mpamba)" — ✓ Keep factual |
| strategy-executive-advisory (line 116) | "SADC AI Governance Framework Advisory" — ✓ Specific context |
| research-applied-ai (line 153) | "SADC Technology & Digital Transformation Studies" — ⚠ Category name |

### 7. src/data/registries/use-case-registry.json

| Use Case | Current Text | Issue |
|----------|--------------|-------|
| fow-02 (line 161) | "SADC enterprise teams can automate immediately" | ⚠ Should be "African enterprise teams" |
| fow-03 (line 177) | "consulting firms across SADC can scale" | ⚠ Should be "across Africa" |
| fow-06 (line 225) | "SADC mobile-first retailers" | ⚠ Should be "African mobile-first retailers" |

### 8. src/data/capabilities.ts

| Line | Current Text | Issue |
|------|--------------|-------|
| 34 | "AI adoption in Malawi, SADC, and Africa" | ⚠ Should be "Africa" |

### 9. src/data/insights.ts

| Line | Current Text | Issue |
|------|--------------|-------|
| 30 | "The SADC AI Opportunity" | ✓ Specific policy work |
| 33 | category: "SADC technology" | ⚠ Category ceiling; prefer "African technology" |
| 41 | "The SADC region is drafting..." | ✓ Factual policy context |
| 46 | "SADC Agentic AI Governance Framework" | ✓ Specific framework name |
| 88 | "What Agentic AI Means for African Governments" | ✓ Good - "African" |
| 106 | "Malawi Data Protection Act 2024" | ✓ Legal fact |
| 129 | "advisory work on Malawi's National AI Strategy" | ✓ Factual experience |
| 168 | "headquartered in Lilongwe" | ✓ BASE - legal fact |
| 173 | "A real, non-tech SME in Malawi" | ✓ Factual experience |

### 10. src/pages/Index.tsx (Footer)

| Line | Current Text | Issue |
|------|--------------|-------|
| 111 | "ASPIRE. ACT. ACHIEVE." only | ⚠ Missing geographic positioning per directive §19 |

### 11. src/pages/WhatWeDoPage.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 33 | "organizations in Malawi, across SADC, and beyond" | ✗ Creates ceiling; should be "across Africa and beyond" |
| 67 | "African enterprises..." | ✓ Good |
| 150 | "Malawi Data Protection Act" | ✓ Legal fact |

### 12. src/pages/SectorsPage.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 49 | "Five sectors across Malawi and SADC" | ✗ Creates ceiling; should be "across Africa" |

### 13. src/components/AboutSection.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 122 | "African enterprise landscape" | ✓ Good |
| 125 | "Operating across Malawi, the SADC economic community, and Pan-African trade corridors" | ⚠ "SADC" as boundary; should be "Africa" |
| 146 | "across Malawi and SADC" | ✗ Ceiling; should be "across Africa" |
| 180 | "SADC regulatory alignment" | ✓ Specific context |

### 14. src/components/ContactSection.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 164 | "Offices in Malawi and African markets" | ✓ Compliant — Lilongwe HQ verified |

### 15. src/components/HeroSection.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 20 | "We know Malawi's institutions..." | ✓ EXPERIENCE - factual |
| 23 | "Regional SADC" | ⚠ Category ceiling; should be "Regional Africa" |
| 28 | "Global Standards" / "international firms" | ✓ REACH - capability claim |
| 56 | "MALAWI-ROOTED, SADC-FOCUSED, GLOBAL CAPABILITY" | ✗ Ceiling tagline; should be "MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY" |

### 16. src/components/home/AboutSection.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 27-28 | "African Intelligence... SADC governance frameworks, Malawi AI Strategy" | ✓ Mixed - "African Intelligence" good, specific policy context OK |

### 17. src/components/home/InsightsSection.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 21 | "from Malawi's National AI Strategy consultation to the SADC governance framework" | ✓ Factual experience |

### 18. src/components/TrustStrip.tsx

| Line | Current Text | Issue |
|------|--------------|-------|
| 17 | "Malawi Government" | ✓ SPECIFIC CONTEXT - if verified |
| 26 | "SADC Secretariat" | ⚠ UNSUPPORTED - unless verified |
| 110 | "Trusted by Organizations Across Malawi & SADC" | ✗ Ceiling; should be "Africa" |

### 19. index.html (SEO)

| Line | Current Text | Issue |
|------|--------------|-------|
| 7 | "across Malawi, SADC, and Africa" | ✗ Ceiling in meta description |
| 9 | Same in og:description | ✗ Ceiling in Open Graph |

### 20. Legal Pages (Preserve Lilongwe)

| File | Lines | Status |
|------|-------|--------|
| TermsPage.tsx | 14, 56, 62, 100 | ✓ KEEP - Legal requirement |
| PrivacyPage.tsx | 28, 34, 47, 80 | ✓ KEEP - Legal requirement |

### 21. useCaseCatalogData.ts

| Line | Current Text | Issue |
|------|--------------|-------|
| 12 | "Lilongwe, Malawi" | ✓ BASE |
| 13 | "The AI-native company builder for Africa" | ✓ Compliant per directive §25 |
| 49 | "Malawi payment rails... Malawi Data Protection Act" | ✓ SPECIFIC CONTEXT |
| 58 | "Every business in Malawi deserves..." | ✓ EXPERIENCE - factual |
| 210 | "Reach Malawian customers..." | ✓ EXPERIENCE - factual |

### 22. agent-registry.public.json (Generated - do not edit directly)

Contains multiple references to "Malawi and the SADC region" in agent missions — these are generated from source files; fix sources.

---

## Summary of Required Changes

### High Priority (Creates Geographic Ceiling)
1. **Hero/Positioning statements**: Replace "Southern Africa" with "Africa" or "African operating realities"
2. **Footer**: Add "Based in Malawi | Working across Africa and beyond"
3. **SEO metadata**: Update meta description and og:description
4. **Sector region arrays**: Add "Africa" as primary, keep specific countries for factual accuracy
5. **ContactSection**: Remove unsupported "Offices in Southern Africa"
5. **HeroSection tagline**: "MALAWI-ROOTED, SADC-FOCUSED, GLOBAL CAPABILITY" → "MALAWI-BASED, AFRICA-FOCUSED, GLOBAL CAPABILITY"

### Medium Priority (Category/Label Ceilings)
6. **insightCategories**: "SADC technology" → "African technology"
7. **Solution descriptions**: "Southern Africa" → "African operating realities"
8. **Use case businessValue**: "SADC" → "Africa"
9. **SectorsPage lead**: "Malawi and SADC" → "Africa"

### Low Priority (Factual - Keep or Refine)
10. **Legal pages**: Keep Lilongwe/Malawi references
11. **Specific case studies**: Keep Malawi/Mozambique/SADC as factual experience
12. **Payment rails / Data Protection Act**: Keep as factual context
13. **Policy work references**: Keep SADC/AU as specific policy context

### Preserve (Do Not Change)
- All honesty badge classifications (PROVEN IN-HOUSE, PILOT, etc.)
- "AI executes. Humans decide."
- Human CEO / human accountability model
- Canonical registry numbers (90 agents, 20 departments)
- Zero-Cloud Boundary / offline-first architecture claims
- Malawi Data Protection Act compliance claims
