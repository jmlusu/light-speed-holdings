# CorporateLanding.tsx Component Split Plan

## Current State

`CorporateLanding.tsx` is **1,823 lines** containing 11 section components, 5 data arrays, form state, and navigation state — all in a single function component.

## Goals

- Every extracted component under **300 lines**
- Flat component hierarchy (max 2 levels deep from orchestrator)
- Minimal props drilling — `theme` and `onRequestBriefing` threaded through; shared state stays in the orchestrator
- Data arrays co-located with the section that consumes them (no shared data file unless cross-section)
- Zero behavioral changes — pixel-for-pixel identical output

---

## New Component Hierarchy

```
CorporateLanding (orchestrator, ~80 lines)
├── HeroSection (~250 lines)
│   └── PillarNavigationCard (~85 lines)
├── OperatingModelSection (~12 lines)
├── CoreOfferingsSection (~100 lines)
│   ├── OfferingDetailCard (~230 lines)
│   └── SynergyMatrix (~150 lines)
├── StrategyChasmSection (~90 lines)
├── SectorExpertiseSection (~130 lines)
├── DiagnosticSection (~12 lines)
├── TemplatesSection (~10 lines)
├── PharosSection (~155 lines)
├── EngagementSection (~135 lines)
├── FaqSection (~75 lines)
├── ContactSection (~210 lines)
└── SiteFooter (~20 lines)
```

**Total: 16 files** (1 orchestrator + 15 leaf/section components)

---

## Shared State Strategy

| State | Current Owner | New Owner | Rationale |
|-------|---------------|-----------|-----------|
| `activePillar` / `setActivePillar` | CorporateLanding | **CorporateLanding** (orchestrator) | Shared between `HeroSection` (PillarNavigationCard) and `CoreOfferingsSection` (tabs + detail + nav). Cross-section state. |
| `selectedSynergy` / `setSelectedSynergy` | CorporateLanding | **CoreOfferingsSection** | Used only within Section 03. |
| `selectedIndustry` / `setSelectedIndustry` | CorporateLanding | **SectorExpertiseSection** | Used only within Section 05. |
| `contactSubmitted` / `contactFormData` / `handleContactSubmit` | CorporateLanding | **ContactSection** | Used only within Section 11. |
| `isLight` | Computed from `theme` | Each component computes locally | `const isLight = theme === 'light'` — trivial, avoids prop drilling a derived value. |

---

## Props Interface (Shared Types)

```typescript
// src/types/landing.ts

export interface SectionProps {
  theme: 'light' | 'dark';
}

export interface ActionSectionProps extends SectionProps {
  onRequestBriefing: (summary?: string) => void;
}

export interface PillarNavProps extends ActionSectionProps {
  activePillar: number;
  onSelectPillar: (idx: number) => void;
}
```

---

## Component Specifications

### 1. CorporateLanding (Orchestrator)

| | |
|---|---|
| **File** | `src/components/CorporateLanding.tsx` (overwrite existing) |
| **Source lines** | Wrapper from lines 1–76 (interface + return shell) + lines 330–335 (outer `<div>`) + lines 1821–1823 (closing) |
| **Estimated size** | ~80 lines |
| **State owned** | `activePillar`, `setActivePillar` |
| **Props** | `onRequestBriefing`, `onSelectAgentForModal`, `agentsList`, `theme`, `onToggleTheme` (all from parent — same interface today) |
| **Children** | All 15 section/leaf components, rendered sequentially |
| **Behavior** | Pure orchestrator. No JSX beyond the outer `<div>` wrapper and child component invocations. |

```tsx
// Pseudocode structure
export const CorporateLanding: React.FC<CorporateLandingProps> = ({
  onRequestBriefing, onSelectAgentForModal, agentsList, theme = 'dark', onToggleTheme
}) => {
  const [activePillar, setActivePillar] = useState(0);

  return (
    <div className={...}>
      <HeroSection theme={theme} onRequestBriefing={onRequestBriefing}
        activePillar={activePillar} onSelectPillar={setActivePillar} />
      <OperatingModelSection theme={theme} onRequestBriefing={onRequestBriefing} />
      <CoreOfferingsSection theme={theme} onRequestBriefing={onRequestBriefing}
        activePillar={activePillar} onSelectPillar={setActivePillar} />
      <StrategyChasmSection theme={theme} />
      <SectorExpertiseSection theme={theme} />
      <DiagnosticSection theme={theme} onRequestBriefing={onRequestBriefing} />
      <TemplatesSection theme={theme} onRequestBriefing={onRequestBriefing} />
      <PharosSection theme={theme} onRequestBriefing={onRequestBriefing} />
      <EngagementSection theme={theme} onRequestBriefing={onRequestBriefing} />
      <FaqSection theme={theme} />
      <ContactSection theme={theme} />
      <SiteFooter theme={theme} />
    </div>
  );
};
```

**Note:** `onSelectAgentForModal` and `agentsList` are passed to `CorporateLanding` but **never used** in any section. They remain in the interface for backward compatibility but are not threaded further. If they are used in a future section, the orchestrator passes them through.

---

### 2. HeroSection

| | |
|---|---|
| **File** | `src/components/HeroSection.tsx` |
| **Source lines** | 336–568 (SECTION 01: HERO) |
| **Estimated size** | ~250 lines |
| **Props** | `theme`, `onRequestBriefing`, `activePillar`, `onSelectPillar` |
| **Data owned** | None (all static JSX) |
| **Imports** | `ArrowRight`, `Sparkles` from lucide-react; `PillarNavigationCard` |

Extracts the hero left column (eyebrow, headline, divider, proposition, 3 advantage cards, action buttons, metric strip) and renders `<PillarNavigationCard>` for the right column.

The 3 advantage cards and metric strip are inline JSX (not data-driven), so they stay as JSX within this component.

---

### 3. PillarNavigationCard

| | |
|---|---|
| **File** | `src/components/PillarNavigationCard.tsx` |
| **Source lines** | 486–567 (hero right column: hardware chassis card) |
| **Estimated size** | ~85 lines |
| **Props** | `theme`, `onRequestBriefing`, `activePillar`, `onSelectPillar` |
| **Data owned** | The 4 pillar definition array (lines 514–519) — moves inside as a `const PILLARS` |
| **Imports** | `ArrowRight` from lucide-react; `AcousticVentGrille` from `TactileHardwareElements` |

The 4-element pillar array (`{ num, title, desc, tag, idx }`) is co-located here because it is **only** used by this card's button list. It is not referenced by any other component.

---

### 4. OperatingModelSection

| | |
|---|---|
| **File** | `src/components/OperatingModelSection.tsx` |
| **Source lines** | 570–576 (SECTION 02) |
| **Estimated size** | ~12 lines |
| **Props** | `theme`, `onRequestBriefing` |
| **Data owned** | None |

Thin wrapper: `<section>` tag + `<InteractiveOperatingModel>`.

---

### 5. CoreOfferingsSection

| | |
|---|---|
| **File** | `src/components/CoreOfferingsSection.tsx` |
| **Source lines** | 578–646 (section header + tab switcher) + 874–1013 (synergy matrix header + comparative table) |
| **Estimated size** | ~100 lines |
| **Props** | `theme`, `onRequestBriefing`, `activePillar`, `onSelectPillar` |
| **State owned** | `selectedSynergy`, `setSelectedSynergy` |
| **Data owned** | `coreCapabilities` array (lines 77–158) — passed down to `OfferingDetailCard` and used locally for tab buttons |
| **Children** | `<OfferingDetailCard>`, `<SynergyMatrix>` |

This component contains:
- Section heading and eyebrow (lines 582–597)
- Tab switcher grid using `coreCapabilities` (lines 600–646)
- Synergy matrix header + comparative table (lines 874–877 intro, 967–1013 table)
- Renders `<OfferingDetailCard>` and `<SynergyMatrix>` as children

The `coreCapabilities` array is defined in this file and passed as a prop to `OfferingDetailCard` (which only needs one element) and used locally for the tab buttons.

---

### 6. OfferingDetailCard

| | |
|---|---|
| **File** | `src/components/OfferingDetailCard.tsx` |
| **Source lines** | 648–872 (active core offering deep-dive view) |
| **Estimated size** | ~230 lines |
| **Props** | `theme`, `onRequestBriefing`, `offering` (single capability object), `activePillar`, `totalPillars`, `onSelectPillar` |
| **Data owned** | None (receives `offering` from parent) |
| **Imports** | `ArrowRight`, `CheckCircle2`, `GitMerge`, `Clock`, `ArrowUpRight`, `ArrowDownRight` from lucide-react; `AcousticVentGrille` |

This is the large hardware-chassis card showing the active offering's eyebrow, title, description, input/output contracts, upstream/downstream lineage, deliverables list, benchmark metric, suite nav, and engagement CTA.

**Props detail:**
```typescript
interface OfferingDetailCardProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
  offering: CoreCapability;  // single item from coreCapabilities
  activePillar: number;
  totalPillars: number;
  onSelectPillar: (idx: number) => void;
}
```

The `CoreCapability` type is:
```typescript
interface CoreCapability {
  id: string;
  title: string;
  shortTitle: string;
  eyebrow: string;
  tagline: string;
  desc: string;
  metrics: string;
  inputContract: string;
  outputContract: string;
  upstreamSource: string;
  downstreamTarget: string;
  governance: string;
  deliverables: string[];
}
```

---

### 7. SynergyMatrix

| | |
|---|---|
| **File** | `src/components/SynergyMatrix.tsx` |
| **Source lines** | 874–966 (synergy pair selector + active synergy detail) |
| **Estimated size** | ~95 lines |
| **Props** | `theme`, `selectedSynergy`, `onSelectSynergy` |
| **Data owned** | `synergyPairs` record (lines 160–200) — moved here |
| **Imports** | `RefreshCw`, `Activity` from lucide-react |

The `synergyPairs` data is **only** consumed by this component. It moves in as a module-level `const`.

**Props detail:**
```typescript
interface SynergyMatrixProps {
  theme: 'light' | 'dark';
  selectedSynergy: string;
  onSelectSynergy: (key: string) => void;
}
```

---

### 8. StrategyChasmSection

| | |
|---|---|
| **File** | `src/components/StrategyChasmSection.tsx` |
| **Source lines** | 1017–1106 (SECTION 04: THE STRATEGY-EXECUTION CHASM) |
| **Estimated size** | ~90 lines |
| **Props** | `theme` |
| **Data owned** | None — 3 failure trap cards are static JSX |

The 3 failure trap cards (Slide Trap, Silo Tax, Toy Playground) are pure static content with no data arrays. They render as inline JSX.

---

### 9. SectorExpertiseSection

| | |
|---|---|
| **File** | `src/components/SectorExpertiseSection.tsx` |
| **Source lines** | 1108–1224 (SECTION 05: SECTOR EXPERTISE) |
| **Estimated size** | ~130 lines |
| **Props** | `theme` |
| **State owned** | `selectedIndustry`, `setSelectedIndustry` |
| **Data owned** | `industriesData` (lines 202–253) and `caseStudies` (lines 255–277) — both moved here |
| **Imports** | `CheckCircle2` from lucide-react |

Both data arrays are consumed **only** within this section. They co-locate here as module-level constants.

---

### 10. DiagnosticSection

| | |
|---|---|
| **File** | `src/components/DiagnosticSection.tsx` |
| **Source lines** | 1226–1234 (SECTION 06) |
| **Estimated size** | ~12 lines |
| **Props** | `theme`, `onRequestBriefing` |
| **Data owned** | None |

Thin wrapper: `<section>` tag + `<TransformationDiagnostic>`.

---

### 11. TemplatesSection

| | |
|---|---|
| **File** | `src/components/TemplatesSection.tsx` |
| **Source lines** | 1236–1240 (SECTION 07) |
| **Estimated size** | ~10 lines |
| **Props** | `theme`, `onRequestBriefing` |
| **Data owned** | None |

Thin wrapper: `<TemplatesArtifacts>` (which already handles its own `<section>` tag).

---

### 12. PharosSection

| | |
|---|---|
| **File** | `src/components/PharosSection.tsx` |
| **Source lines** | 1242–1391 (SECTION 08: PHAROS // THOUGHT LEADERSHIP) |
| **Estimated size** | ~155 lines |
| **Props** | `theme`, `onRequestBriefing` |
| **Data owned** | `whitepapers` (lines 279–328) — moved here |
| **Imports** | `Download` from lucide-react |

The `whitepapers` array is consumed **only** by this section. It co-locates here as a module-level constant.

---

### 13. EngagementSection

| | |
|---|---|
| **File** | `src/components/EngagementSection.tsx` |
| **Source lines** | 1393–1526 (SECTION 09: ENGAGEMENT MODELS) |
| **Estimated size** | ~135 lines |
| **Props** | `theme`, `onRequestBriefing` |
| **Data owned** | None — 3 engagement phase cards are static JSX |

The 3 phase cards (Sprint, Pilot, Enterprise) are pure static content with no data arrays. They render as inline JSX.

---

### 14. FaqSection

| | |
|---|---|
| **File** | `src/components/FaqSection.tsx` |
| **Source lines** | 1528–1595 (SECTION 10: FREQUENTLY ASKED QUESTIONS) |
| **Estimated size** | ~75 lines |
| **Props** | `theme` |
| **Data owned** | FAQ items array (lines 1549–1582) — moved here as a module-level `const FAQ_ITEMS` |

---

### 15. ContactSection

| | |
|---|---|
| **File** | `src/components/ContactSection.tsx` |
| **Source lines** | 1597–1801 (SECTION 11: CONTACT / EXECUTIVE BRIEFING INTAKE) |
| **Estimated size** | ~210 lines |
| **Props** | `theme` |
| **State owned** | `contactSubmitted`, `contactFormData`, `setContactFormData`, `handleContactSubmit` |
| **Data owned** | None |
| **Imports** | `ShieldCheck`, `Clock`, `Globe2`, `Send`, `CheckCircle2` from lucide-react; `AcousticVentGrille` from `TactileHardwareElements` |

This component owns the full contact form lifecycle: initial form render, field state management, submit handler, and success state. The `onRequestBriefing` callback is **not** needed here (the form uses its own submission flow, not the briefing modal).

**Correction:** Looking again, the contact form does NOT call `onRequestBriefing`. It sets `contactSubmitted = true`. So `onRequestBriefing` is not needed as a prop.

---

### 16. SiteFooter

| | |
|---|---|
| **File** | `src/components/SiteFooter.tsx` |
| **Source lines** | 1803–1819 (FOOTER) |
| **Estimated size** | ~20 lines |
| **Props** | `theme` |
| **Data owned** | None |

---

## Data Migration Summary

| Data Array | Current Location (lines) | New Location | Consumed By |
|------------|-------------------------|--------------|-------------|
| `coreCapabilities` | Lines 77–158 (CorporateLanding) | `CoreOfferingsSection.tsx` (module-level const) | `CoreOfferingsSection` (tab buttons), `OfferingDetailCard` (via prop) |
| `synergyPairs` | Lines 160–200 (CorporateLanding) | `SynergyMatrix.tsx` (module-level const) | `SynergyMatrix` only |
| `industriesData` | Lines 202–253 (CorporateLanding) | `SectorExpertiseSection.tsx` (module-level const) | `SectorExpertiseSection` only |
| `caseStudies` | Lines 255–277 (CorporateLanding) | `SectorExpertiseSection.tsx` (module-level const) | `SectorExpertiseSection` only |
| `whitepapers` | Lines 279–328 (CorporateLanding) | `PharosSection.tsx` (module-level const) | `PharosSection` only |
| FAQ items | Lines 1549–1582 (inline in JSX) | `FaqSection.tsx` (module-level const `FAQ_ITEMS`) | `FaqSection` only |
| Pillar definitions | Lines 514–519 (inline in JSX) | `PillarNavigationCard.tsx` (module-level const `PILLARS`) | `PillarNavigationCard` only |

---

## What Changes in App.tsx

**Nothing.** `App.tsx` imports and renders `<CorporateLanding>` with the same props interface. The split is entirely internal to the `CorporateLanding` module boundary. `App.tsx` continues to:

```tsx
import { CorporateLanding } from './components/CorporateLanding';

<CorporateLanding
  onRequestBriefing={handleRequestBriefing}
  onSelectAgentForModal={setSelectedAgent}
  agentsList={agentsList}
  theme={theme}
  onToggleTheme={toggleTheme}
/>
```

The `CorporateLandingProps` interface remains identical. No downstream breaking changes.

---

## Import Map (New Files)

Each new file needs these lucide-react imports (subset, not all icons):

| Component | lucide-react imports |
|-----------|---------------------|
| `HeroSection` | `ArrowRight`, `Sparkles` |
| `PillarNavigationCard` | `ArrowRight` |
| `CoreOfferingsSection` | `Network` |
| `OfferingDetailCard` | `ArrowRight`, `CheckCircle2`, `GitMerge`, `Clock`, `ArrowUpRight`, `ArrowDownRight` |
| `SynergyMatrix` | `RefreshCw`, `Activity` |
| `StrategyChasmSection` | (none — all icons are inline SVG or none used) |
| `SectorExpertiseSection` | `CheckCircle2` |
| `PharosSection` | `Download` |
| `EngagementSection` | `Check` |
| `ContactSection` | `ShieldCheck`, `Clock`, `Globe2`, `Send`, `CheckCircle2` |
| `SiteFooter` | (none) |

---

## Implementation Order

Recommended order for incremental extraction (each step produces a working build):

| Step | Action | Risk |
|------|--------|------|
| 1 | Create `SiteFooter.tsx`, `OperatingModelSection.tsx`, `DiagnosticSection.tsx`, `TemplatesSection.tsx` (thin wrappers — lowest risk, immediate line count reduction) | Near zero |
| 2 | Create `StrategyChasmSection.tsx`, `FaqSection.tsx` (self-contained, no shared state) | Low |
| 3 | Create `EngagementSection.tsx` (self-contained, no shared state) | Low |
| 4 | Create `SectorExpertiseSection.tsx` (absorbs `selectedIndustry` state + `industriesData` + `caseStudies`) | Low |
| 5 | Create `PharosSection.tsx` (absorbs `whitepapers` data) | Low |
| 6 | Create `ContactSection.tsx` (absorbs form state) | Low |
| 7 | Create `PillarNavigationCard.tsx` (extract hero right column) | Medium |
| 8 | Create `HeroSection.tsx` (uses PillarNavigationCard) | Medium |
| 9 | Create `OfferingDetailCard.tsx` (large extraction, most complex JSX) | Medium |
| 10 | Create `SynergyMatrix.tsx` (absorbs `synergyPairs` + `selectedSynergy` state) | Medium |
| 11 | Create `CoreOfferingsSection.tsx` (orchestrates tabs + OfferingDetailCard + SynergyMatrix, absorbs `coreCapabilities`) | Medium |
| 12 | Rewrite `CorporateLanding.tsx` as thin orchestrator | Medium — final integration step |

**Verification after each step:**
```bash
npx tsc --noEmit        # type check
npx vite build          # production build
npx vite preview        # visual regression check
```

---

## Line Count Budget

| Component | Estimated Lines | Under 300? |
|-----------|----------------|------------|
| CorporateLanding (orchestrator) | ~80 | Yes |
| HeroSection | ~250 | Yes |
| PillarNavigationCard | ~85 | Yes |
| OperatingModelSection | ~12 | Yes |
| CoreOfferingsSection | ~100 | Yes |
| OfferingDetailCard | ~230 | Yes |
| SynergyMatrix | ~95 | Yes |
| StrategyChasmSection | ~90 | Yes |
| SectorExpertiseSection | ~130 | Yes |
| DiagnosticSection | ~12 | Yes |
| TemplatesSection | ~10 | Yes |
| PharosSection | ~155 | Yes |
| EngagementSection | ~135 | Yes |
| FaqSection | ~75 | Yes |
| ContactSection | ~210 | Yes |
| SiteFooter | ~20 | Yes |
| **Total** | **~1,689** | All pass |

The total is slightly less than 1,823 because some boilerplate (state declarations, imports shared across sections) is eliminated by co-locating state and data.
