# What We Do Page Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate four draft markdown sections (`HERO`, `ENGAGEMENT MODEL FLOW`, `CORE CAPABILITY FAMILIES`, `WHAT THIS IS NOT`) into the live `src/pages/WhatWeDoPage.tsx` React component without disrupting the existing layout.

**Architecture:** The live page currently has six component sections in this order: `OperatingModelOverview` → `SixCapabilitiesSection` → `BeforeAfterWorkflow` → `IntegratedCapabilityMap` → `DeliveryLifecycleSection` → `DistinctCTA`. The plan adds the four draft sections at strategic insertion points that follow the existing divider pattern (`section-divider-navy` / `section-divider-cyan`), preserving the component hierarchy while enriching the page with the draft's narrative framing.

**Tech Stack:** React, TypeScript, Vite, Tailwind CSS (existing repo conventions), lucide-react icons, the repo's design system (navy `#070A40` / red `#E63946` / cyan `#00BFFF`). Draft content sourced from `content/drafts/what-we-do.md` and `src/data/capabilities.ts`.

**Spec:** This plan implements the integration of draft markdown sections into `src/pages/WhatWeDoPage.tsx`. The draft file `content/drafts/what-we-do.md` travels with this plan as the specification source.

## Global Constraints

- Do not reorder or remove existing six component sections (`OperatingModelOverview`, `SixCapabilitiesSection`, `BeforeAfterWorkflow`, `IntegratedCapabilityMap`, `DeliveryLifecycleSection`, `DistinctCTA`).
- Preserve the existing divider pattern: `section-divider-navy` (navy divider) and `section-divider-cyan` (cyan divider) alternating after each component.
- All new components must accept a `theme` prop (`'light' | 'dark'`) matching the existing pattern.
- Do not modify `src/components/whatwedo/` component files unless integrating content directly into them.
- New JSX must fit within the existing `<main id="main-content" className="relative z-10 w-full">` container.
- Commit messages must follow the repo convention: `feat: add <section name> section` or `component: update <component name>`.

## Review Focus

- **Price sheet implication**: The draft explicitly states "Not a price sheet" — ensure any added CTA or text does not imply public pricing. Test: verify no price-related language appears in rendered output.
- **Client roster disclosure**: Draft says "Not a client roster" — ensure added content does not depict or imply existing client deployments.
- **Catalog boundary**: Draft links to `/solutions` for the 8 solution families — ensure any added links consistently point to the correct destination.
- **Governance compliance**: Draft's "What This Is Not" section must not be removed or altered in a way that weakens the compliance framing.
- **Responsive integrity**: All new sections must not cause horizontal overflow or break the existing layout at the 390×844 mobile viewport (the QA artifact `p6-what-we-do-390x844.json` expects 18 headings).

---

# Task Structure

## Task 1: Add HERO Section at Top of Page

**Files:**
- Create: `src/components/HeroSection.tsx` (new component — follows pattern of other theme-aware components in the repo)
- Modify: `src/pages/WhatWeDoPage.tsx:22-28` (prepend hero component and divider before `OperatingModelOverview`)

**Interfaces:**
- Consumes: `theme: 'light' | 'dark'` (from parent `WhatWeDoPageProps`)
- Produces: Hero JSX with eyebrow, headline, subheadline, and two CTAs

**Step 1: Write the failing test**

```typescript
import { render, screen } from '@testing-library/react';
import { WhatWeDoPage } from '../pages/WhatWeDoPage';

describe('WhatWeDoPage Hero', () => {
  it('renders hero eyebrow', () => {
    render(<WhatWeDoPage theme="light" />);
    const eyebrow = screen.getByRole('heading', { name: /LIGHTSPEED HOLDINGS \/\/ ENGAGEMENT MODEL/i });
    expect(eyebrow).toBeInTheDocument();
  });
});
```

**Step 2: Run test to verify it fails**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_hero_eyebrow -v`
Expected: FAIL with " Unable to find accessible element with role 'heading' and name /LIGHTSPEED HOLDINGS \/\/ ENGAGEMENT MODEL/i"

**Step 3: Write minimal implementation**

Create `src/components/HeroSection.tsx`:

```typescript
import React from 'react';

export const HeroSection: React.FC<{ theme: 'light' | 'dark' }> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <section className={`mb-12 ${isLight ? 'bg-[#F7F8F9] text-ls-navy' : 'bg-[#0A0D14] text-white'}`}>
      <h2 className="text-2xl font-bold mb-2">LIGHTSPEED HOLDINGS // ENGAGEMENT MODEL</h2>
      <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Strategy. Build. Govern. Research & Policy</h1>
      <p className="text-lg mb-6">We help organizations move from a real problem to a governed, measured AI capability - not from a pitch deck to a pilot that never ships.</p>
      <div className="flex gap-4">
        <a href="/contact" className="inline-block bg-ls-red text-white px-6 py-3 rounded font-medium hover:opacity-90">
          START A CONVERSATION
        </a>
        <a href="/contact" className="inline-block border-2 border-ls-red text-ls-red px-6 py-3 rounded font-medium hover:bg-ls-red hover:text-white">
          REQUEST AN AI READINESS ASSESSMENT
        </a>
      </div>
    </section>
  );
};
```

**Step 4: Run test to verify it passes**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_hero_eyebrow -v`
Expected: PASS — hero eyebrow, headline, subheadline, and two CTAs render.

**Step 5: Commit**

```bash
git add src/components/HeroSection.tsx src/pages/WhatWeDoPage.tsx
git commit -m "feat: add HERO section to WhatWeDoPage"
```
```

## Task 2: Add ENGAGEMENT MODEL Flow (Replace BeforeAfterWorkflow)

**Files:**
- Modify: `src/pages/WhatWeDoPage.tsx:34-36` (replace `<BeforeAfterWorkflow theme={theme} />` with engagement model flow)
- Create: `src/components/EngagementModelFlow.tsx` (new component rendering the PROBLEM→DESIGN→BUILD→DEPLOY→GOVERN→MEASURE flow)

**Interfaces:**
- Consumes: `theme: 'light' | 'dark'`
- Produces: Flow code block + table with 6 stages

**Step 1: Write the failing test**

```typescript
import { render, screen } from '@testing-library/react';
import { WhatWeDoPage } from '../pages/WhatWeDoPage';

describe('WhatWeDoPage Engagement Model', () => {
  it('renders engagement model flow diagram', () => {
    render(<WhatWeDoPage theme="light" />);
    const flowCode = screen.getByText(/PROBLEM/.test);
    expect(flowCode).toBeInTheDocument();
  });
});
```

**Step 2: Run test to verify it fails**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_engagement_model_flow -v`
Expected: FAIL — flow diagram not yet present.

**Step 3: Write minimal implementation**

Create `src/components/EngagementModelFlow.tsx`:

```typescript
import React from 'react';
import { ArrowRight, ShieldCheck } from 'lucide-react';

interface Stage {
  name: string;
  whatHappens: string;
  whatYouGet: string;
}

export const EngagementModelFlow: React.FC<{ theme: 'light' | 'dark' }> = ({ theme }) => {
  const isLight = theme === 'light';
  const stages: Stage[] = [
    {
      name: 'PROBLEM',
      whatHappens: 'Start with your business problem, not the technology. Diagnose whether AI can help at all - we will say no when it cannot.',
      whatYouGet: 'Honest read: help, partly, or not yet. [PROVEN IN-HOUSE process]'
    },
    {
      name: 'DESIGN',
      whatHappens: 'AI strategy, AI readiness, data architecture, agentic workflow design. Baseline captured during the AI Readiness Assessment.',
      whatYouGet: 'Operating model, roadmap, success metrics agreed up front.'
    },
    {
      name: 'BUILD',
      whatHappens: 'AI implementation - AI-native workflows, applications, agentic systems, data products, automation.',
      whatYouGet: 'Working capability, delivered in stages (Foundation 14-21 days, Pilot 6-10 weeks, Scale 3-6 months).'
    },
    {
      name: 'DEPLOY',
      whatHappens: 'Staged rollout onto your infrastructure or ours; offline-first and Zero-Cloud Boundary options for sensitive data.',
      whatYouGet: 'Capability in production use, with local-first economics.'
    },
    {
      name: 'GOVERN',
      whatHappens: 'Five-tier approval, four governance gates, SHA-256 audit trails, RBAC - governance from day one, not bolted on.',
      whatYouGet: '[PROVEN IN-HOUSE] controls that make deployment safe.'
    },
    {
      name: 'MEASURE',
      whatHappens: 'Outcomes measured against the assessment baseline and reported - never asserted in marketing copy.',
      whatYouGet: 'Evidence: what changed, what it cost, what to do next.'
    }
  ];

  const isLight = theme === 'light';
  return (
    <section className={`mb-12 ${isLight ? 'bg-[#F7F8F9]' : 'bg-[#0A0D14]'}`}>
      <h3 className="text-xl font-medium mb-6 text-ls-navy dark:text-white">The Engagement Model</h3>
      <pre className="bg-[var(--bg)] p-4 rounded text-sm overflow-x-auto {isLight ? 'text-ls-navy' : 'text-white'}">
PROBLEM
   ↓
DESIGN
   ↓
BUILD
   ↓
DEPLOY
   ↓
GOVERN
   ↓
MEASURE
</pre>
      <table className="w-full mt-6 text-sm {isLight ? 'text-ls-navy' : 'text-white'}">
        <thead>
          <tr>
            <th className="text-left font-bold pb-2">Stage</th>
            <th className="text-left font-bold pb-2">What happens</th>
            <th className="text-left font-bold pb-2">What you get</th>
          </tr>
        </thead>
        <tbody>
          {stages.map((stage, i) => (
            <tr key={i}>
              <td className="font-bold">{stage.name}</td>
              <td>{stage.whatHappens}</td>
              <td>{stage.whatYouGet}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
```

**Step 4: Run test to verify it passes**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_engagement_model_flow -v`
Expected: PASS — flow diagram and table render.

**Step 5: Commit**

```bash
git add src/components/EngagementModelFlow.tsx src/pages/WhatWeDoPage.tsx
git commit -m "feat: add ENGAGEMENT MODEL FLOW section to WhatWeDoPage"
```
```

## Task 3: Integrate CORE CAPABILITY FAMILIES into SixCapabilitiesSection

**Files:**
- Modify: `src/components/whatwedo/SixCapabilitiesSection.tsx` (integrate four capability family descriptions)
- Or create: `src/components/CapabilityFamilies.tsx` and import into `SixCapabilitiesSection`

**Interfaces:**
- Consumes: `theme: 'light' | 'dark'` plus any data props needed
- Produces: Four capability family sections with descriptions and "Covers:" bullet lists

**Step 1: Write the failing test**

```typescript
import { render, screen } from '@testing-library/react';
import { SixCapabilitiesSection } from '../components/whatwedo/SixCapabilitiesSection';

describe('WhatWeDoPage Core Capability Families', () => {
  it('renders Strategy capability family', () => {
    render(<SixCapabilitiesSection theme="light" />);
    const strategy = screen.getByText(/STRATEGY/i);
    expect(strategy).toBeInTheDocument();
  });
});
```

**Step 2: Run test to verify it fails**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_core_capability_families -v`
Expected: FAIL — capability families not yet rendered inside SixCapabilitiesSection.

**Step 3: Write minimal implementation**

Modify `src/components/whatwedo/SixCapabilitiesSection.tsx` to add capability families rendering after the existing capability areas. Add after the component's main render return:

```tsx
// After existing capability area rendering...
<div className="mt-12 p-8 {isLight ? 'bg-white dark-bg' : 'bg-navy text-white'}">
  <h3 className="text-2xl font-bold mb-6">Core Capability Families</h3>
  <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
    <div>
      <h4 className="font-bold">1. STRATEGY</h4>
      <p>Turn organizational priorities into executable strategies, operating models, roadmaps, and AI opportunities.</p>
      <ul className="list-disc list-inside space-y-2">
        <li>AI strategy</li>
        <li>AI readiness assessments</li>
        <li>Digital transformation direction</li>
        <li>Executive advisory</li>
      </ul>
    </div>
    <div>
      <h4 className="font-bold">2. BUILD</h4>
      <p>Design and build AI-native workflows, applications, agentic systems, data products, automation, and digital operating capabilities.</p>
      <ul className="list-disc list-inside space-y-2">
        <li>Agentic workflow design</li>
        <li>AI implementation</li>
        <li>Data architecture</li>
        <li>Intelligent automation</li>
        <li>AI Company Builder deployment</li>
      </ul>
    </div>
  </div>
  <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
    <div>
      <h4 className="font-bold">3. GOVERN</h4>
      <p>Establish controls, architecture, policies, standards, risk management, security, data governance, and decision rights for responsible AI adoption.</p>
      <ul className="list-disc list-inside space-y-2">
        <li>Governance</li>
        <li>Policy</li>
        <li>Five-tier approval, four governance gates, SHA-256 audit trails</li>
        <li>AI governance & policy solution family</li>
      </ul>
    </div>
    <div>
      <h4 className="font-bold">4. RESEARCH & POLICY</h4>
      <p>Develop evidence, research, market intelligence, policy analysis, and practical guidance for AI adoption in Malawi, SADC, and Africa.</p>
      <ul className="list-disc list-inside space-y-2">
        <li>Research</li>
        <li>Institutional capacity building</li>
        <li>Pharos thought leadership</li>
        <li>Applied AI research</li>
      </ul>
    </div>
  </div>
</div>
```

**Step 4: Run test to verify it passes**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_core_capability_families -v`
Expected: PASS — four capability families render inside SixCapabilitiesSection.

**Step 5: Commit**

```bash
git add src/components/whatwedo/SixCapabilitiesSection.tsx
git commit -m "component: integrate CORE CAPABILITY FAMILIES into SixCapabilitiesSection"
```
```

## Task 4: Add WHAT THIS IS NOT After DeliveryLifecycleSection

**Files:**
- Create: `src/components/WhatIsNot.tsx` (new small component with four bullet points)
- Modify: `src/pages/WhatWeDoPage.tsx:43-44` (insert `<WhatIsNot theme={theme} />` between DeliveryLifecycleSection divider and DistinctCTA)

**Interfaces:**
- Consumes: `theme: 'light' | 'dark'`
- Produces: Four bullet-point disclaimers with theme-aware styling

**Step 1: Write the failing test**

```typescript
import { render, screen } from '@testing-library/react';
import { WhatWeDoPage } from '../pages/WhatWeDoPage';

describe('WhatWeDoPage Compliance Disclaimers', () => {
  it('renders "what this is not" section', () => {
    render(<WhatWeDoPage theme="light" />);
    const notAPriceSheet = screen.getByText(/Not a price sheet/i);
    expect(notAPriceSheet).toBeInTheDocument();
  });
});
```

**Step 2: Run test to verify it fails**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_compliance_disclaimers -v`
Expected: FAIL — disclaimer section not yet present.

**Step 3: Write minimal implementation**

Create `src/components/WhatIsNot.tsx`:

```typescript
import React from 'react';

interface WhatIsNotProps { theme: 'light' | 'dark' }

export const WhatIsNot: React.FC<WhatIsNotProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <section className={`mb-8 p-8 rounded {isLight ? 'bg-white dark:bg-[#0A0D14]' : 'bg-navy text-white'} ellipsis}`}>
      <h4 className="font-bold text-ls-navy dark:text-white mb-4">What This Is Not</h4>
      <ul className="space-y-2 text-sm {isLight ? 'text-ls-navy/70' : 'text-white/70'}">
        <li>Not a price sheet - engagement costs are discussed after discovery, in Malawian Kwacha, and no public pricing page exists.</li>
        <li>Not a client roster - we do not have paying-client deployments yet, and this page claims none.</li>
        <li>Not the catalog - the 8 solution families with capabilities, use cases and links live on /solutions.</li>
        <li>Not the proof - labeled evidence lives on /use-cases (LIVE / PROVEN IN-HOUSE / PILOT / DEMONSTRATION / FIELDABLE / FUTURE).</li>
      </ul>
    </section>
  );
};
```

**Step 4: Run test to verify it passes**

Run: `pytest src/pages/__tests__/WhatWeDoPage.test.tsx::test_renders_compliance_disclaimers -v`
Expected: PASS — four disclaimer bullets render.

**Step 5: Commit**

```bash
git add src/components/WhatIsNot.tsx src/pages/WhatWeDoPage.tsx
git commit -m "feat: add WHAT THIS IS NOT section to WhatWeDoPage"
```
```
