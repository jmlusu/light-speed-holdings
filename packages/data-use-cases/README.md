# @lightspeed/data-use-cases

LightSpeed Holdings Use Cases Data Package — Registry, filters, and types for use case explorer.

## Ported from AI Studio lsh-prototype (Phase 1 — Lightspeed Portal Migration)

This package was migrated from the Google AI Studio project `lsh-prototype` into the `open-design` monorepo as part of Phase 1 of the Lightspeed Portal migration.

### Ported Data Registries

The following registries have been ported from `_staging/lsh-prototype/src/data/` to `src/`:

| File | Description |
|------|-------------|
| `capabilities.ts` | Four operating-model capabilities: strategy, build, govern, research-policy |
| `faqs.ts` | Frequently asked questions with evidence grounding per MASTER_SPEC §15 |
| `governance.ts` | Content governance registry with 5-tier HITL approval matrix (§17) |
| `insights.ts` | Pharos thought-leadership articles (CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §16) |
| `metrics.ts` | Canonical metrics: agentCount (90), testCount (109), departments (20), fiveTier, sectorStats, liveTestCount (2684) |
| `registries/claims-registry.json` | Canonical claims registry per Directive §23 with VERIFIED/PROVEN_IN_HOUSE/PILOT/DEMONSTRATION/FIELDABLE/FUTURE/HISTORICAL/UNVERIFIED classifications |
| `registries/media-registry.json` | Registry of every image the public site renders, with origin, licence and disclosure status |
| `shipped/company.ts` | Company identity: LightSpeed Holdings Limited, 90-role model, humanAuthorityStatement, roleBreakdown |
| `shipped/ctas.ts` | Canonical CTAs registry with 24 primary/secondary/contextual CTAs and canonical label mapping |
| `registry/sectors.ts` | Sector registry from sector-registry.json (6 sectors: agriculture, financial-services, government, government-public-sector, health, technology-companies) |
| `registry/solutions.ts` | Solution registry from solution-registry.json (13 solutions with capabilities, useCases, CTA) |
| `registry/use-cases.ts` | Use case registry from use-case-registry.json (35+ use cases with status, problem/solution categories, sectors) |

### Usage

```typescript
// Import the full registry
import { useCasesRegistry } from '@lightspeed/data-use-cases';

// Import specific ported registries
import { lightSpeedCapabilities, lightSpeedFaqs, lightSpeedMetrics } from '@lightspeed/data-use-cases';

// Use filter functions
import { getFeaturedUseCases, getUseCasesByStatus, searchUseCases } from '@lightspeed/data-use-cases';

// Type access
import type { Capability, Faq, GovernedClaim, InsightArticle, Metrics, CompanyIdentity, CTA, Sector, Solution, UseCase } from '@lightspeed/data-use-cases';
```

### Package API

**Exports (re-exported from `src/index.ts`):**

- **Types**: `UseCase`, `UseCaseStatus`, `ProblemCategory`, `SolutionCategory`, `UseCaseFilterFn`
- **Registry**: `useCasesRegistry`, `USE_CASE_COUNT`, `VALID_SECTOR_IDS`
- **Filters**: `getUseCasesByStatus`, `getUseCasesBySector`, `getUseCasesBySolution`, `getUseCasesByProblemCategory`, `getFeaturedUseCases`, `getAllUseCases`, `searchUseCases`, `getAvailableStatuses`, `getAvailableProblemCategories`, `getAvailableSolutionCategories`, `getAvailableSectors`, `applyFilters`, `UseCaseFilters`
- **Ported data**: `lightSpeedCapabilities`, `lightSpeedCapabilityTitles`, `lightSpeedFaqs`, `lightSpeedFaqEvidence`, `lightSpeedFaq`, `lightSpeedContentClaims`, `lightSpeedRequiresEvidence`, `lightSpeedIsPubliclyVisible`, `lightSpeedInsightArticles`, `lightSpeedMetrics`, `lightSpeedLiveTestCount`, `lightSpeedCompanyIdentity`, `lightSpeedHumanAuthorityStatement`, `lightSpeedHumanAuthorityStatementFull`, `lightSpeedRoleBreakdown`, `lightSpeedCTARegistry`, `lightSpeedCanonicalCTALabels`, `lightSpeedGetPrimaryCTA`, `lightSpeedGetSecondaryCTA`, `lightSpeedSectorsRegistry`, `lightSpeedSolutionsRegistry`

### Design Token Merge

Color conflicts between AI Studio source and existing LightSpeed design-system target values were resolved by keeping the target (canonical) values per Directive §7 (append-only merge). All canonical brand tokens (navy `#070A40`, red `#E63946`, cyan `#00BFFF`) remain unchanged.

The new `lightSpeedBrand` palette is available from the design-system package:
```typescript
import { lightSpeedBrand } from '@lightspeed/design-system/src/tokens';
```

### Related Packages

- `@lightspeed/design-system` — Design tokens, components, and utilities
- `@lightspeed/design-system` — Design tokens, components, and utilities
