# Marketing Site Trust and Clarity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public marketing site easier to navigate and more defensible: fewer decisions on the homepage, legible honesty badges, public claims backed by evidence, honest redirects, and one canonical brand voice.

**Architecture:** Five independent workstreams share one Vite/React single-page app and one registry-driven content model. Each task is sequenced by file ownership (one task owns a file at a time), writes a failing Vitest test first, implements the smallest change that passes it, and lands as its own branch and PR. A preflight task isolates the already-uncommitted accessibility-polish changes so they are never mixed with this plan's commits.

**Tech Stack:** Vite 6, React 18, TypeScript, Tailwind 4, Vitest 5 + jsdom, @testing-library/react, React Router 7, registry JSON under `src/data/registries/`, npm scripts (`npm test`, `npm run build`, `npm run lint`).

**Spec:** `PRODUCT.md`, `DESIGN.md`, and the Source findings section below.

## Global Constraints

- Working root is `C:\Users\jmlus\light-speed-holdings` (Windows paths; PowerShell 5.1 syntax — no `head`/`tail`/`sed`/`$?`, chain with `;`).
- `main` is protected by a GitHub ruleset with 6 required checks. Work on a branch; open a PR with `gh pr create`; "done" requires green CI, otherwise report "local only".
- Never delete, overwrite, or restore files you did not create this session, including untracked ones. Stage by explicit path only — never `git add .` / `git add -A`, never `--no-verify`, never empty commits, never `git config` changes.
- Before any git/PR/CI work, read `.ai-company\constitution\16-AGENT-GUARDRAILS.md`.
- `opencode.json` carries a pre-existing modification (removal of a gbrain MCP entry) that did **not** come from this plan. It must stay unstaged and untouched in every task.
- The working tree also carries the uncommitted accessibility-polish changes from the Impeccable session (19 `src/` files). Task 0 isolates them; later tasks must not revert, stash, or overwrite them.
- Marketing site ports are dev `http://localhost:1441` and preview `http://localhost:1440`. Never bind the CEO Dashboard ports `8420`/`8421`; the Vite config has a `dashboardPortGuard`.
- The site and the CEO Dashboard are separate applications. Do not modify `src/ai_company/`, `company-registry.yaml`, or dashboard code in any task here.
- Brand is fixed: navy `#070A40`, red `#E63946`, cyan `#00BFFF`, morning mist `#F7F8F9`, deep mineral `#121518`; Arial is the only typeface; 4px spacing grid; cyan is the sole trust/status signal; navy ≤10% of a screen.
- Canonical counts are test-enforced and must not change: 90 roles = 89 agents + 1 human CEO, 20 departments, 5 governance tiers.
- Honesty badges use exactly four levels — `proven`, `pilot`, `fieldable`, `development` — with the existing `honestyLabel()` mapping. No new level, no relabelling of evidence `verified`/`unknown` as a maturity tier.
- Every claim on the public site must be registry-backed. Do not invent evidence, metrics, source anchors, or explanations (AGENTS.md §7).
- Node scripts use `npx vitest run <path>` (equivalent to `npm test -- <path>`); the full gate is `npm test` (154 tests at baseline) plus `npm run build`.

## Review Focus

Five failure modes most likely to bite a reviewer, each pinned to a test in its owning task:

1. **Dark mode or AA contrast regresssion from new badge/brand classes** — pinned by `honesty badge contrast > keeps ${tone} text at AA or better in light and dark` (Task 2) and `cyan-is-trust status palette > no green status token survives...` (Task 3).
2. **Product truth lost while simplifying the homepage** — pinned by `VisitorPathsSection: every audience, secondary destination and Ask LightSpeed copy is preserved inside the disclosure` and `InsightsSection: all eight format names, subtitles and Explore labels are preserved` (Task 1).
3. **An unsupported absolute or response-time promise returns to public copy** — pinned by `unproven public-claim regression > never reintroduces the retired 100% metric copy on public surfaces` and `... > never reintroduces an unsupported response-time promise in public copy` (Task 4).
4. **A redirect becomes two hops or loses destination SEO** — pinned by `legacy redirects are honest and single-hop > %s resolves in one hop to %s with a visible moved notice` and `... > keeps the destination SEO title (applyPageMeta) intact after the redirect` (Task 5).
5. **The canonical human-authority line is hardcoded or rendered only once** — pinned by `human authority statement > HeroSection renders the verbatim line...`, `... AboutSection renders...`, and `... both components import humanAuthorityStatement rather than hardcoding it` (Task 3).

## Team / Roster

| Workstream | Company agent (registry id) | Role in this plan |
|---|---|---|
| Preflight and whole-branch review | `qa_lead` | Owns Task 0 isolation check and final regression gate |
| Homepage clarity | `cpo` | Task 1 implementer |
| Honesty badge legibility | `culture_values_officer` | Task 2 implementer |
| Canonical brand line and status colour | `cmo` | Task 3 implementer |
| Claims evidence | `clo` | Task 4 implementer |
| Redirects and IA | `technical_documentation_lead` | Task 5 implementer |
| Every task review | `qa_lead` | Independent acceptance review before the next task unlocks |
| Whole-branch integration review | `vp_engineering` + `qa_lead` | Final verdict after all five PRs |

The runtime exposes only the built-in `general` subagent type; dispatch each role as a fresh `general` subagent primed with the role card from `.opencode/agents/<id>.md`, the task brief, and the global constraints above. Never give two tasks the same file at the same time; the ordering below is the file-ownership contract.

## Task sequence and file ownership

| Task | Owns (exclusive during its run) | Reads only |
|---|---|---|
| 0. Preflight | branch/PR for the current 19-file polish | all |
| 1. Homepage clarity | `HomeSection.tsx`, `VisitorPathsSection.tsx`, `WhatWeBuildGrid.tsx`, `InsightsSection.tsx`, `homepage-clarity.test.tsx` | `HomePage.tsx`, `SixCapabilitiesSection.tsx` |
| 2. Badges | `siteContent.ts`, `HonestyBadge.tsx`, `StatusBadge.tsx`, `CategoryChip.tsx`, `FaqCardList.tsx`, `SixCapabilitiesSection.tsx`, `brand-tokens.css`, `honestyBadge.test.tsx` | registries, `faqs.ts` |
| 3. Brand line/colour | `HeroSection.tsx`, `AboutSection.tsx` (root), `home/AboutSection.tsx`, `SiteFooter.tsx`, `HeroBanner.tsx`, `AssessmentWizard.tsx`, `BeforeAfterWorkflow.tsx`, `ContentCarousel.tsx`, `OperatingModelOverview.tsx`, `HaomtgvUnifiedArchitecture.tsx`, `HAOMTGVPage.tsx`, `brand-governance.test.tsx` | `brand-tokens.css` (verify only, owned by Task 2) |
| 4. Claims | `publicMetrics.ts`, claim/metric/FAQ registries, `enquiry.ts`, `CtaBand.tsx`, `ContactSection.tsx`, `ExecutiveBriefingModal.tsx`, `NewsletterSignup.tsx`, `AskLightSpeed.tsx`, `faqs.ts`, `public-claim-guards.test.ts`, `faq-evidence.test.ts` | `AboutSection.tsx` (Task 3 must land first) |
| 5. Redirects | `legacyRedirects.ts`, `LegacyRedirect.tsx`, `App.tsx`, `SiteLayout.tsx`, `VisitorPathsSection.tsx` (second owner, after Task 1), `legacyRedirects.test.tsx` | `InsightArticlePage.tsx` (do not edit) |

---

## Task 0: Isolate the existing accessibility polish

**Files:**
- Modify: none in content; this task only stages and commits files already modified in the working tree.
- Explicit paths: the 19 `src/` files listed by `git status --short` at plan time (all `src/` entries except `opencode.json`).

**Interfaces:**
- Consumes: the current working tree state after the Impeccable session (build green, 154 tests green, Lighthouse 1.00 on 1440).
- Produces: a clean baseline branch/PR containing only the accessibility-polish changes, so Tasks 1–5 can branch from it without mixing commits.

- [ ] **Step 1: Read the guardrails and record the baseline**

```powershell
Get-Content .ai-company/constitution/16-AGENT-GUARDRAILS.md
git status --short
git diff --check
```

Expected: `opencode.json` plus 19 `src/` files modified. If any file outside that set is modified, stop and reconcile before continuing.

- [ ] **Step 2: Branch and re-verify the baseline**

```powershell
git switch -c fix/impeccable-a11y-polish
npm test
npm run build
```

Expected: 154 tests pass; build succeeds. Do not use `git stash`, `git reset`, or `git checkout --` at any point.

- [ ] **Step 3: Stage only the polish files, by explicit path**

```powershell
git add src/brand/tokens/brand-tokens.css src/components/AboutSection.tsx src/components/BeforeAfterWorkflow.tsx src/components/DistinctCTA.tsx src/components/HeroBanner.tsx src/components/HeroSection.tsx src/components/HumanApprovalMatrix.tsx src/components/SiteLayout.tsx src/components/haomtgv/HaomtgvBlueprintHero.tsx src/components/home/AboutSection.tsx src/components/home/ClosingCTASection.tsx src/components/home/HAOMTGVVisualization.tsx src/components/home/VisitorPathsSection.tsx src/components/site/SectionHeading.tsx src/components/whatwedo/OperatingModelOverview.tsx src/components/whatwedo/SixCapabilitiesSection.tsx src/index.css src/site/CategoryChip.tsx src/site/StatusBadge.tsx
git diff --cached --stat
git status --short
```

Expected: 19 staged `src/` files; `opencode.json` still unstaged. If `opencode.json` is staged, unstage it with `git restore --staged opencode.json` (this does not modify the file).

- [ ] **Step 4: Commit and hand off**

```powershell
git commit -m "fix(site): make marketing site accessible and per-route SEO correct"
git status --short --branch
```

Expected: only `opencode.json` remains modified. Open a PR per guardrails; report CI status from `gh` output only. Tasks 1–5 branch from this commit.

---

## Task 1: Reduce homepage decision load without losing product truth

**Files:**
- Create: `src/__tests__/homepage-clarity.test.tsx`
- Modify: `src/components/home/HomeSection.tsx`, `src/components/home/VisitorPathsSection.tsx`, `src/components/home/WhatWeBuildGrid.tsx`, `src/components/home/InsightsSection.tsx`
- Reference only (do not edit): `src/pages/HomePage.tsx`, `src/components/whatwedo/SixCapabilitiesSection.tsx`

**Interfaces:**
- Consumes: local data `VISITOR_PATHS`, `CAPABILITIES`, `PHAROS_FORMATS`; shared `HomeSection`, `SectionHeading`, `Reveal`; `Link`/`MemoryRouter`; Tailwind tokens emitted from `brand-tokens.css`.
- Produces: 4 primary audience links plus one closed disclosure holding all 5 deeper links; 6 capability links with 6 unique accessible names; 1 primary research link plus one closed disclosure holding all 8 format cards; 48/64px section rhythm; 6 passing tests.

- [ ] **Step 1: Branch**

```powershell
git switch -c fix/homepage-clarity
```

- [ ] **Step 2: Write the failing test file**

Create `src/__tests__/homepage-clarity.test.tsx`:

```tsx
import { describe, it, expect } from 'vitest';
import type { ReactElement } from 'react';
import { render, screen, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { VisitorPathsSection } from '../components/home/VisitorPathsSection';
import { WhatWeBuildGrid } from '../components/home/WhatWeBuildGrid';
import { InsightsSection } from '../components/home/InsightsSection';

const renderInRouter = (ui: ReactElement) => render(<MemoryRouter>{ui}</MemoryRouter>);

describe('homepage clarity - one decision per section', () => {
  it('VisitorPathsSection: four primary path links are the only links outside the "More ways in" disclosure', () => {
    const { container } = renderInRouter(<VisitorPathsSection theme="light" />);
    const region = screen.getByRole('region', { name: /choose your path/i });
    expect(region).toHaveClass('py-12');
    expect(region).toHaveClass('lg:py-16');

    const primary = within(region).getByRole('navigation', { name: /choose one starting point/i });
    const primaryLinks = within(primary).getAllByRole('link');
    expect(primaryLinks).toHaveLength(4);
    expect(primaryLinks.map((link) => link.getAttribute('href'))).toEqual([
      '/what-we-do', '/contact', '/insights', '/haomtgv',
    ]);

    const details = container.querySelector('details');
    expect(details).not.toBeNull();
    expect(details).not.toHaveAttribute('open');
    expect(details?.querySelector('summary')).toHaveTextContent('More ways in');

    const allLinks = within(region).getAllByRole('link');
    const moreLinks = within(details as HTMLElement).getAllByRole('link');
    expect(moreLinks).toHaveLength(5);
    expect(allLinks.length - moreLinks.length).toBe(4);
  });

  it('VisitorPathsSection: every audience, secondary destination and Ask LightSpeed copy is preserved inside the disclosure', () => {
    const { container } = renderInRouter(<VisitorPathsSection theme="dark" />);
    const details = container.querySelector('details') as HTMLElement;
    for (const intent of ['Business Leaders', 'Partners', 'Researchers', 'Policy Makers']) {
      expect(screen.getByText(intent)).toBeInTheDocument();
    }
    for (const label of ['HAOMTGV Framework', 'Platform details', 'Pharos practice', 'Policy briefs']) {
      expect(within(details).getByText(new RegExp(label))).toBeInTheDocument();
    }
    expect(within(details).getByText(/Not sure which path fits\?/)).toBeInTheDocument();
    expect(within(details).getByRole('link', { name: /Ask LightSpeed/ })).toHaveAttribute('href', '/ask');
    expect(within(details).getByText(/answers from our published knowledge only/)).toBeInTheDocument();
  });

  it('WhatWeBuildGrid: six capability links have six unique accessible names', () => {
    renderInRouter(<WhatWeBuildGrid theme="dark" />);
    const links = screen.getAllByRole('link', { name: /^Explore /i });
    expect(links).toHaveLength(6);
    const names = links.map((link) => link.getAttribute('aria-label'));
    expect(new Set(names).size).toBe(6);
    expect(names).toEqual([
      'Explore AI-Native Company Building',
      'Explore Intelligent Workflow Automation',
      'Explore Agentic Systems & Orchestration',
      'Explore Enterprise AI Integration',
      'Explore Organizational Memory Systems',
      'Explore AI Governance Infrastructure',
    ]);
    links.forEach((link) => expect(link).toHaveAttribute('href', '/what-we-do'));
  });

  it('WhatWeBuildGrid: practice-area copy and 48/64px vertical rhythm are preserved', () => {
    const { container } = renderInRouter(<WhatWeBuildGrid theme="light" />);
    const section = container.querySelector('#what-we-build') as HTMLElement;
    expect(section).toHaveClass('py-12');
    expect(section).toHaveClass('lg:py-16');
    expect(screen.getByRole('heading', { level: 2, name: 'Six Capabilities. One Governed System.' })).toBeInTheDocument();
    expect(screen.getAllByText('EXPLORE CAPABILITY')).toHaveLength(6);
    expect(screen.getByText(/append-only cryptographic audit trails/)).toBeInTheDocument();
  });

  it('InsightsSection: one primary research link sits outside the "Browse all eight formats" disclosure', () => {
    const { container } = renderInRouter(<InsightsSection theme="dark" />);
    const region = screen.getByRole('region', { name: /pharos thought-leadership engine/i });
    expect(region).toHaveClass('py-12');
    expect(region).toHaveClass('lg:py-16');
    expect(within(region).getByRole('link', { name: /read the research library/i })).toHaveAttribute('href', '/insights');

    const details = container.querySelector('details') as HTMLElement;
    expect(details).not.toBeNull();
    expect(details).not.toHaveAttribute('open');
    expect(details.querySelector('summary')).toHaveTextContent('Browse all eight formats');
    const formatLinks = within(details).getAllByRole('link');
    expect(formatLinks).toHaveLength(8);
    expect(within(region).getAllByRole('link').length - formatLinks.length).toBe(1);
  });

  it('InsightsSection: all eight format names, subtitles and Explore labels are preserved', () => {
    const { container } = renderInRouter(<InsightsSection theme="light" />);
    const details = container.querySelector('details') as HTMLElement;
    const titles = [
      'Briefs', 'Field Notes', 'Research Notes', 'Policy Briefs',
      'System Maps', 'Data Stories', 'AI-Economics Analyses', 'Africa Watch Regional Monitors',
    ];
    titles.forEach((title) => expect(within(details).getByText(title)).toBeInTheDocument());
    expect(within(details).getByText(/Concise executive summaries connecting research to real-world use cases/)).toBeInTheDocument();
    expect(within(details).getByText(/First-hand operational observations and field lessons from live deployments/)).toBeInTheDocument();
    expect(within(details).getAllByText('Explore')).toHaveLength(8);
    expect(within(details).getByText('Our Eight Publication Formats')).toBeInTheDocument();
    expect(within(details).getByText('8 Publication Channels')).toBeInTheDocument();
  });
});
```

- [ ] **Step 3: Confirm red**

Run `npm test -- src/__tests__/homepage-clarity.test.tsx`. Expected: failures on the missing navigation landmark, closed disclosures, unique aria-labels, and 48/64px classes.

- [ ] **Step 4: Collapse the visitor paths**

In `src/components/home/VisitorPathsSection.tsx`, keep the four `<article>` cards but wrap them in `<nav aria-label="Choose one starting point" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">`, give each card exactly one primary `<Link to={path.primary.to}>` with the existing label and `ArrowRight`, and move every `path.secondary` link plus the `Ask LightSpeed` band into a closed `<details>` with `<summary>More ways in</summary>` and `<nav aria-label="More ways in">`. Preserve every existing string verbatim: the four audience names, `PATH {idx + 1}`, `(answers from our published knowledge only)`, and `/ask` as the Ask LightSpeed destination at this stage (Task 5 changes it to `/contact`). Keep the existing `font-body text-[10px]` path labels and the existing `bg-ls-red-cta`/`hover:bg-ls-red-ink` CTA tokens from the preflight commit.

- [ ] **Step 5: Give the six capability links unique names**

In `src/components/home/WhatWeBuildGrid.tsx`, change the section class from `py-24` to `py-12 lg:py-16`, and add `aria-label={`Explore ${cap.title}`}` to the existing `<Link to="/what-we-do">`. Keep the visible text `EXPLORE CAPABILITY` and all six titles, problems, explanations, eyebrow, and lead unchanged.

- [ ] **Step 6: Collapse the eight Pharos formats**

In `src/components/home/InsightsSection.tsx`, change `py-[100px]` to `py-12 lg:py-16`, add one primary `<Link to="/insights">Read the research library →</Link>` before the formats block, and wrap the existing eight-format grid in `<details className="mt-8"><summary>Browse all eight formats</summary>…</details>`. Do not edit any format title, subtitle, `to` value, or `Explore` label. In `src/components/home/HomeSection.tsx`, change the wrapper's `py-[100px]` to `py-12 lg:py-16` so every section built on it uses the same 48/64px rhythm.

- [ ] **Step 7: Verify**

```powershell
npm test -- src/__tests__/homepage-clarity.test.tsx
npm test -- src/__tests__/haomtgv/HAOMTGVSection.test.tsx src/__tests__/siteFaq.test.tsx
npm run build
```

Expected: all three commands green.

- [ ] **Step 8: Commit**

```powershell
git add src/components/home/HomeSection.tsx src/components/home/VisitorPathsSection.tsx src/components/home/WhatWeBuildGrid.tsx src/components/home/InsightsSection.tsx src/__tests__/homepage-clarity.test.tsx
git commit -m "fix(home): reduce homepage decision load while preserving research and capability copy"
```

## Task 2: Make honesty badges legible without changing what any badge means

**Files:**
- Create: `src/__tests__/honestyBadge.test.tsx`
- Modify: `src/brand/tokens/brand-tokens.css`, `src/data/siteContent.ts`, `src/components/site/HonestyBadge.tsx`, `src/site/StatusBadge.tsx`, `src/site/CategoryChip.tsx`, `src/components/FaqCardList.tsx`, `src/components/whatwedo/SixCapabilitiesSection.tsx`
- Run unmodified: `src/__tests__/governance.test.ts`, `src/__tests__/claims.test.ts`, `src/__tests__/faq-evidence.test.ts`, `packages/design-system/src/tokens/colors.test.ts`
- Out of scope: `src/design-system/`, `packages/design-system/src/tokens/colors.ts`, `src/design-system/components/Badge/Badge.tsx`

**Interfaces:**
- Consumes: `HonestyTone`, `HonestyLabel`, `honestyLabel()` from `siteContent.ts`; `--color-ls-*` tokens from `brand-tokens.css`; `.dark` variant from `index.css`; `faqs` from `src/data/faqs.ts` (`verified | unknown`); `SIX_CAPABILITIES[].status` strings.
- Produces: `BADGE_BASE_CLASSES`, `EVIDENCE_STATUS_CLASSES`, rewritten `TONE_STYLES` with exactly four keys; all site badges at 12px with AA ink in both themes.

- [ ] **Step 1: Branch**

```powershell
git switch -c fix/honesty-badge-legibility
```

- [ ] **Step 2: Add the two missing neutral tokens**

In `src/brand/tokens/brand-tokens.css`, inside `@theme`, after `--color-ls-grey-ink`, add:

```css
  /* AA-safe ink variants for small badge text (same hues, darker/lighter values) */
  --color-ls-grey-deep: #374151;   /* 10.4:1 on #FFFFFF — development, light */
  --color-ls-grey-soft: #D1D5DB;   /* 12.0:1 on #070A40 — fieldable, dark */
```

In `:root`, after `--ls-grey-light-text: #9CA3AF;`, add:

```css
  --ls-grey-deep: #374151;
  --ls-grey-soft: #D1D5DB;
```

- [ ] **Step 3: Replace the style table in `src/data/siteContent.ts`**

Keep `HonestyTone`, `HonestyLabel`, and the whole `honestyLabel()` function byte-for-byte. Replace only the old style table with:

```ts
export const BADGE_BASE_CLASSES =
  'inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 font-body text-xs font-bold tracking-widest uppercase';

/* One canonical tone → AA-safe brand-token class map. Hue and rank are unchanged:
   proven cyan / pilot red / fieldable grey / development graphite. */
export const TONE_STYLES: Record<HonestyTone, string> = {
  proven: 'bg-ls-cyan/10 text-ls-cyan-ink border-ls-cyan/40 dark:text-ls-cyan',
  pilot: 'bg-ls-red/10 text-ls-red-ink border-ls-red/40 dark:text-ls-red-bright',
  fieldable: 'bg-ls-grey-light-text/10 text-ls-grey-ink border-ls-grey-dark/40 dark:text-ls-grey-soft',
  development: 'bg-ls-grey-dark/10 text-ls-grey-deep border-ls-grey-dark/40 dark:text-ls-grey-light-text',
};

/* Evidence provenance is a different axis from capability maturity. Labels stay
   `verified`/`unknown` verbatim — no capability tier is implied or invented. */
export const EVIDENCE_STATUS_CLASSES: Record<'verified' | 'unknown', string> = {
  verified: 'bg-ls-cyan/10 text-ls-cyan-ink border-ls-cyan/40 dark:text-ls-cyan',
  unknown: 'bg-ls-grey-dark/10 text-ls-grey-deep border-ls-grey-dark/40 dark:text-ls-grey-light-text',
};
```

Add `BADGE_BASE_CLASSES` and `EVIDENCE_STATUS_CLASSES` to the default export object (keep `TONE_STYLES`).

- [ ] **Step 4: Consume the shared base in the badge components**

Rewrite `src/components/site/HonestyBadge.tsx`:

```tsx
import React from 'react';
import { BADGE_BASE_CLASSES, HonestyLabel, TONE_STYLES } from '../../data/siteContent';

interface HonestyBadgeProps {
  label: HonestyLabel;
  className?: string;
}

/**
 * Honesty badge: labels every claim with its evidence status. Proven (cyan) /
 * pilot (red) / fieldable (grey) / development (graphite). We never blur statuses.
 */
export const HonestyBadge: React.FC<HonestyBadgeProps> = ({ label, className }) => (
  <span className={`${BADGE_BASE_CLASSES} ${TONE_STYLES[label.tone]} ${className ?? ''}`}>
    <span aria-hidden="true" className="w-1.5 h-1.5 rounded-full bg-current opacity-70" />
    {label.label}
  </span>
);

export default HonestyBadge;
```

In both `src/site/StatusBadge.tsx` and `src/site/CategoryChip.tsx`, set the base class to:

```ts
const BASE_CLASSES =
  'inline-flex items-center rounded-full border px-2.5 py-1 font-body text-xs font-bold tracking-widest uppercase';
```

- [ ] **Step 5: Restyle FAQ evidence chips**

In `src/components/FaqCardList.tsx`, import `EVIDENCE_STATUS_CLASSES` from `../data/siteContent` and replace the green/amber ternary with:

```tsx
{faq.evidence.map((ev, i) => (
  <span
    key={i}
    className={`px-2 py-0.5 rounded border text-xs font-mono ${EVIDENCE_STATUS_CLASSES[ev.status]}`}
  >
    {ev.source} ({ev.status})
  </span>
))}
```

No label, source string, or status value changes.

- [ ] **Step 6: Unify the six capability status pills**

In `src/components/whatwedo/SixCapabilitiesSection.tsx`, add `import { honestyLabel, TONE_STYLES } from '../../data/siteContent';`, delete `statusColor: string;` from `CapabilityDetail` and all six `statusColor: '...'` entries, then replace the render with:

```tsx
<span className={`text-xs font-mono font-bold px-3 py-1 rounded-full border ${TONE_STYLES[honestyLabel(selectedCap.status).tone]}`}>
  {selectedCap.status}
</span>
```

The four displayed status strings stay verbatim.

- [ ] **Step 7: Write the failing test**

Create `src/__tests__/honestyBadge.test.tsx`:

```tsx
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { FaqCardList } from '../components/FaqCardList';
import { StatusBadge } from '../site/StatusBadge';
import { CategoryChip } from '../site/CategoryChip';
import { BADGE_BASE_CLASSES, EVIDENCE_STATUS_CLASSES, TONE_STYLES, honestyLabel } from '../data/siteContent';

const root = resolve(__dirname, '..', '..');
const css = readFileSync(resolve(root, 'src/brand/tokens/brand-tokens.css'), 'utf8');
const token = (name: string): string => {
  const match = css.match(new RegExp(`--color-ls-${name}:\\s*(#[0-9A-Fa-f]{6})\\s*;`));
  if (!match) throw new Error(`missing --color-ls-${name} in brand-tokens.css`);
  return match[1].toUpperCase();
};
const luminance = (hex: string): number => {
  const channels = [1, 3, 5].map((start) => {
    const value = parseInt(hex.slice(start, start + 2), 16) / 255;
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
};
const contrast = (fg: string, bg: string): number => {
  const a = luminance(fg), b = luminance(bg);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
};
const INK = {
  proven: { light: 'cyan-ink', dark: 'cyan' },
  pilot: { light: 'red-ink', dark: 'red-bright' },
  fieldable: { light: 'grey-ink', dark: 'grey-soft' },
  development: { light: 'grey-deep', dark: 'grey-light-text' },
} as const;
const SURFACE = { light: '#FFFFFF', dark: '#070A40' } as const;
const tones = ['proven', 'pilot', 'fieldable', 'development'] as const;

describe('honesty badge tone map', () => {
  it('keeps exactly the four canonical tones', () => {
    expect(Object.keys(TONE_STYLES).sort()).toEqual(['development', 'fieldable', 'pilot', 'proven']);
  });

  it('preserves label-to-tone mapping for every published badge string', () => {
    expect(honestyLabel('Proven in-house').tone).toBe('proven');
    expect(honestyLabel('Live proof').tone).toBe('proven');
    expect(honestyLabel('Published').tone).toBe('proven');
    expect(honestyLabel('In pilot').tone).toBe('pilot');
    expect(honestyLabel('In pilot (composing evidence)').tone).toBe('pilot');
    expect(honestyLabel('Fieldable in 2026').tone).toBe('fieldable');
    expect(honestyLabel('In active development').tone).toBe('development');
    expect(honestyLabel('Proven in-house').label).toBe('Proven in-house');
  });
});

describe('honesty badge contrast', () => {
  for (const tone of tones) {
    it(`keeps ${tone} text at AA or better in light and dark`, () => {
      expect(contrast(token(INK[tone].light), SURFACE.light)).toBeGreaterThanOrEqual(4.5);
      expect(contrast(token(INK[tone].dark), SURFACE.dark)).toBeGreaterThanOrEqual(4.5);
    });
  }
});

describe('honesty badge rendering', () => {
  it('renders every tone with the shared 12px base and its own AA ink', () => {
    const cases = [
      ['Proven in-house', 'text-ls-cyan-ink'],
      ['In pilot', 'text-ls-red-ink'],
      ['Fieldable in 2026', 'text-ls-grey-ink'],
      ['In active development', 'text-ls-grey-deep'],
    ] as const;
    for (const [label, ink] of cases) {
      const { container, unmount } = render(<HonestyBadge label={honestyLabel(label)} />);
      const badge = container.firstElementChild as HTMLElement;
      expect(badge.textContent).toContain(label);
      expect(badge).toHaveClass('text-xs');
      expect(badge).toHaveClass('border');
      expect(badge).toHaveClass(ink);
      unmount();
    }
    expect(BADGE_BASE_CLASSES).toContain('text-xs');
  });

  it('uses no green or amber classes on badge surfaces', () => {
    for (const tone of tones) expect(TONE_STYLES[tone]).not.toMatch(/emerald|green|amber|lime/);
    for (const file of ['src/components/FaqCardList.tsx', 'src/components/whatwedo/SixCapabilitiesSection.tsx']) {
      expect(readFileSync(resolve(root, file), 'utf8')).not.toMatch(/emerald|amber/);
    }
  });
});

describe('FAQ evidence chips', () => {
  it('renders verified evidence in brand cyan and unknown in brand grey', () => {
    const { container } = render(<FaqCardList theme="light" />);
    fireEvent.click(screen.getByText('What is the AI Company Builder?'));
    const verified = screen.getByText(/claim\.agent-count \(verified\)/);
    expect(verified).toHaveClass('text-ls-cyan-ink');
    expect(verified).not.toHaveClass('text-emerald-700');
    expect(EVIDENCE_STATUS_CLASSES.verified).toContain('text-ls-cyan-ink');
    expect(EVIDENCE_STATUS_CLASSES.unknown).toContain('text-ls-grey-deep');
    expect(container.querySelector('.bg-amber-50')).toBeNull();
  });

  it('keeps evidence status labels verbatim instead of reclassifying them as maturity tiers', () => {
    const faqSource = readFileSync(resolve(root, 'src/data/faqs.ts'), 'utf8');
    expect(faqSource).toContain("status: 'verified'");
    expect(faqSource).not.toMatch(/status:\s*'(proven|pilot|fieldable|development)'/);
  });
});

describe('companion badges', () => {
  it('renders StatusBadge and CategoryChip at 12px, not 10px', () => {
    const status = render(<StatusBadge status="PILOT" theme="light" />);
    const category = render(<CategoryChip category="STRATEGY" theme="light" />);
    const statusBadge = status.container.firstElementChild as HTMLElement;
    const categoryBadge = category.container.firstElementChild as HTMLElement;
    expect(statusBadge).toHaveClass('text-xs');
    expect(categoryBadge).toHaveClass('text-xs');
    expect(statusBadge.className).not.toContain('text-[10px]');
    expect(categoryBadge.className).not.toContain('text-[10px]');
  });
});
```

- [ ] **Step 8: Verify and commit**

```powershell
npm test -- src/__tests__/honestyBadge.test.tsx
npm test -- src/__tests__/honestyBadge.test.tsx src/__tests__/governance.test.ts src/__tests__/claims.test.ts src/__tests__/faq-evidence.test.ts
npm run build
git add src/brand/tokens/brand-tokens.css src/data/siteContent.ts src/components/site/HonestyBadge.tsx src/site/StatusBadge.tsx src/site/CategoryChip.tsx src/components/FaqCardList.tsx src/components/whatwedo/SixCapabilitiesSection.tsx src/__tests__/honestyBadge.test.tsx
git commit -m "Make honesty badges legible with AA-safe brand tokens"
```

CI remains unverified until the PR checks are green; report "local only, CI unverified" until then.

---

## Task 3: Render the canonical human-authority line and replace green status with cyan

**Files:**
- Create: `src/__tests__/brand-governance.test.tsx`
- Modify: `src/components/HeroSection.tsx`, `src/components/AboutSection.tsx`, `src/components/home/AboutSection.tsx`, `src/components/SiteFooter.tsx`, `src/components/HeroBanner.tsx`, `src/components/AssessmentWizard.tsx`, `src/components/BeforeAfterWorkflow.tsx`, `src/components/FaqCardList.tsx`, `src/components/ContentCarousel.tsx`, `src/components/whatwedo/SixCapabilitiesSection.tsx`, `src/components/whatwedo/OperatingModelOverview.tsx`, `src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx`, `src/pages/HAOMTGVPage.tsx`
- Verify only: `src/brand/tokens/brand-tokens.css` (owned by Task 2)

**Interfaces:**
- Consumes: `humanAuthorityStatement` from `src/data/shipped/company.ts` (`'AI executes. Humans decide.'`); AA ink tokens from Task 2; existing test conventions in `siteFaq.test.tsx`.
- Produces: the verbatim line on `/` and `/about` sourced from the registry; cyan-only status chips; no `#DC3641` in marketing sources; Arial-only typography in the four audited components.

- [ ] **Step 1: Branch and read guardrails**

```powershell
Get-Content .ai-company/constitution/16-AGENT-GUARDRAILS.md
git switch -c fix/canonical-line-cyan-status
git status --short
```

Do not stash, reset, or discard the pre-existing working-tree changes.

- [ ] **Step 2: Write the failing test**

Create `src/__tests__/brand-governance.test.tsx`:

```tsx
import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { MemoryRouter } from 'react-router-dom';
import { HeroSection } from '../components/HeroSection';
import { AboutSection } from '../components/AboutSection';
import { StatusBadge } from '../site/StatusBadge';
import { CategoryChip } from '../site/CategoryChip';
import { humanAuthorityStatement } from '../data/shipped/company';

afterEach(() => cleanup());

const collectSources = (dir: string): string[] =>
  readdirSync(dir).flatMap((name) => {
    const path = join(dir, name);
    return statSync(path).isDirectory() ? collectSources(path) : [path];
  });
const sourcesIn = (...dirs: string[]) =>
  dirs.flatMap(collectSources).filter((path) => /\.tsx?$/.test(path)).map((path) => ({ path, code: readFileSync(path, 'utf8') }));
const componentsAndSite = sourcesIn('src/components', 'src/site');
const pages = sourcesIn('src/pages');
const GREEN_STATUS_RE =
  /(?:bg|text|border|ring|fill|stroke|from|to|shadow)-(?:ls-)?(?:emerald|green)(?:-\d{2,4})?(?:\/\d+)?|#(?:10B981|22C55E|16A34A|34D399)\b/i;

describe('human authority statement', () => {
  it('HeroSection renders the verbatim line "AI executes. Humans decide."', () => {
    render(<MemoryRouter><HeroSection theme="dark" onRequestBriefing={() => {}} /></MemoryRouter>);
    expect(screen.getByText(humanAuthorityStatement).textContent).toBe('AI executes. Humans decide.');
  });

  it('AboutSection renders the verbatim line "AI executes. Humans decide."', () => {
    render(<MemoryRouter><AboutSection theme="dark" onOpenContactModal={() => {}} /></MemoryRouter>);
    expect(screen.getByText('AI executes. Humans decide.')).toBeTruthy();
  });

  it('both components import humanAuthorityStatement rather than hardcoding it', () => {
    for (const path of ['src/components/HeroSection.tsx', 'src/components/AboutSection.tsx']) {
      const code = readFileSync(path, 'utf8');
      expect(code).toContain("import { humanAuthorityStatement } from '../data/shipped/company';");
      expect(code).not.toContain("'AI executes. Humans decide.'");
    }
  });
});

describe('cyan-is-trust status palette', () => {
  it('no green status token survives in src/components or src/site', () => {
    expect(componentsAndSite.filter(({ code }) => GREEN_STATUS_RE.test(code)).map(({ path }) => path)).toEqual([]);
  });

  it('no green status token survives in src/pages', () => {
    expect(pages.filter(({ code }) => GREEN_STATUS_RE.test(code)).map(({ path }) => path)).toEqual([]);
  });

  it('StatusBadge and CategoryChip use cyan trust classes without green', () => {
    const { container } = render(<><StatusBadge status="PILOT" theme="light" /><StatusBadge status="IN DEVELOPMENT" theme="dark" /><CategoryChip category="STRATEGY" theme="light" /></>);
    const classes = Array.from(container.querySelectorAll('span')).map((span) => span.className).join(' ');
    expect(classes).toContain('bg-ls-cyan/10');
    expect(classes).not.toMatch(/emerald|green/i);
  });
});

describe('brand token unification', () => {
  it('brand-tokens.css defines the AA ink tokens ls-red-ink, ls-red-cta, ls-red-bright, ls-cyan-ink, ls-grey-ink', () => {
    const tokens = readFileSync('src/brand/tokens/brand-tokens.css', 'utf8');
    for (const token of [
      '--color-ls-red-ink: #C42E3A;', '--color-ls-red-cta: #D62E3B;',
      '--color-ls-red-bright: #FF7B84;', '--color-ls-cyan-ink: #00688F;',
      '--color-ls-grey-ink: #5F6673;',
    ]) expect(tokens).toContain(token);
  });

  it('no #DC3641 duplicate red survives in marketing sources or brand tokens', () => {
    const files = [...componentsAndSite, ...pages, { path: 'src/brand/tokens/brand-tokens.css', code: readFileSync('src/brand/tokens/brand-tokens.css', 'utf8') }];
    expect(files.filter(({ code }) => /#DC3641/i.test(code)).map(({ path }) => path)).toEqual([]);
  });
});

describe('Arial-only marketing typography', () => {
  it('hero, footer and about components use Arial tokens without font-mono', () => {
    for (const path of [
      'src/components/HeroSection.tsx', 'src/components/SiteFooter.tsx',
      'src/components/AboutSection.tsx', 'src/components/home/AboutSection.tsx',
    ]) expect(readFileSync(path, 'utf8')).not.toContain('font-mono');
  });
});
```

Confirm red with `npx vitest run src/__tests__/brand-governance.test.tsx`.

- [ ] **Step 3: Render the canonical line from the registry**

Add `import { humanAuthorityStatement } from '../data/shipped/company';` to `src/components/HeroSection.tsx` and `src/components/AboutSection.tsx`. In `HeroSection.tsx`, insert after the subtitle `</p>` and before the CTA row:

```tsx
        {/* Human authority — canonical statement */}
        <p className={`font-body text-sm sm:text-base font-bold tracking-wide border-l-4 pl-4 py-1 ${
          isLight ? 'border-ls-cyan-ink text-ls-navy' : 'border-ls-cyan text-white'
        }`}>
          {humanAuthorityStatement}
        </p>
```

In `src/components/AboutSection.tsx`, insert after the introduction paragraph inside the Company Introduction card with the same classes and `mt-4` prefixed.

- [ ] **Step 4: Replace green status classes (batch A)**

In `src/components/AboutSection.tsx`: replace the two `color: 'text-emerald-500 bg-emerald-500/10'` entries with `color: isLight ? 'text-ls-cyan-ink bg-ls-cyan/10' : 'text-ls-cyan bg-ls-cyan/10'`; replace `color: 'text-emerald-500'` with `color: 'text-ls-cyan'`; replace the `UserCheck` icon class with `w-4 h-4 text-ls-cyan shrink-0`. In `src/components/HeroBanner.tsx`, replace `bg-ls-emerald` with `bg-ls-cyan`. In `src/components/AssessmentWizard.tsx`, replace the `Optimized` badge/text pair with:

```ts
    Optimized: {
      badge: 'bg-ls-cyan/10 text-ls-cyan-ink dark:text-ls-cyan',
      text: 'text-ls-cyan-ink dark:text-ls-cyan',
    },
```

- [ ] **Step 5: Replace green status classes (batch B)**

In `src/components/BeforeAfterWorkflow.tsx`, replace the quantified-impact span with `font-bold text-ls-cyan font-body` and the following `<p>` with `text-ls-cyan-ink dark:text-ls-cyan font-semibold mt-0.5`. In `src/components/FaqCardList.tsx`, set the verified chip class to `isLight ? 'bg-ls-cyan/10 text-ls-cyan-ink border border-ls-cyan/30' : 'bg-ls-cyan/10 text-ls-cyan border border-ls-cyan/40'`. In `src/components/whatwedo/SixCapabilitiesSection.tsx`, replace all three `bg-emerald-500/10 text-emerald-600 border-emerald-500/20` occurrences with `bg-ls-cyan/10 text-ls-cyan-ink border-ls-cyan/30`. In `src/components/whatwedo/OperatingModelOverview.tsx`, set the first pillar color to `text-ls-cyan-ink bg-ls-cyan/10 border-ls-cyan/30` and its active ring to `ring-2 ring-ls-cyan shadow-lg shadow-ls-cyan/20`. In `src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx`, replace the two green evidence badges with `text-[10px] font-body px-2 py-0.5 rounded bg-ls-cyan/10 text-ls-cyan font-bold uppercase` and the feedback-loop label with `text-ls-cyan font-bold`. In `src/pages/HAOMTGVPage.tsx`, replace the verified badge with `text-xs font-body px-2.5 py-1 bg-ls-cyan/10 rounded ${isLight ? 'text-ls-cyan-ink' : 'text-ls-cyan'}`.

- [ ] **Step 6: Remove the duplicate red and audit typography**

In `src/components/ContentCarousel.tsx`, replace the chip class with `isLight ? 'bg-ls-red/10 text-ls-red-ink' : 'bg-ls-red/10 text-ls-red-bright'`. In `src/pages/HAOMTGVPage.tsx`, set `const BRAND_BAR = ['#070A40', '#E63946', '#00BFFF'];`. In `SiteFooter.tsx`, `AboutSection.tsx`, `home/AboutSection.tsx`, `FaqCardList.tsx`, and `HaomtgvUnifiedArchitecture.tsx`, replace every remaining `font-mono` class token with `font-body`. Do not edit the `.font-mono` telemetry rule in `src/index.css` (internal dashboard, out of scope).

- [ ] **Step 7: Verify and commit**

```powershell
npx vitest run src/__tests__/brand-governance.test.tsx
npm test
npm run build
git diff --check
git add src/components/HeroSection.tsx src/components/AboutSection.tsx src/components/home/AboutSection.tsx src/components/SiteFooter.tsx src/components/HeroBanner.tsx src/components/AssessmentWizard.tsx src/components/BeforeAfterWorkflow.tsx src/components/FaqCardList.tsx src/components/ContentCarousel.tsx src/components/whatwedo/SixCapabilitiesSection.tsx src/components/whatwedo/OperatingModelOverview.tsx src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx src/pages/HAOMTGVPage.tsx src/__tests__/brand-governance.test.tsx
git commit -m "feat(brand): render canonical human-authority line and replace green status with cyan"
```

Preview check on the marketing port only (`npm run preview` → 1440); never bind 8420/8421. Read CI status with `gh`; never search config or env for tokens.

## Task 4: Remove or ground unproven public-site claims

**Files:**
- Create: `src/data/publicMetrics.ts`, `src/__tests__/public-claim-guards.test.ts`
- Modify: `src/data/registries/claims-registry.json`, `src/data/registries/metrics-registry.json`, `src/components/AboutSection.tsx`, `src/lib/enquiry.ts`, `src/components/site/CtaBand.tsx`, `src/components/ContactSection.tsx`, `src/components/ExecutiveBriefingModal.tsx`, `src/components/NewsletterSignup.tsx`, `src/components/AskLightSpeed.tsx`, `src/data/faqs.ts`, `src/data/registries/faq-registry.json`, `src/components/BeforeAfterWorkflow.tsx`, `src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx`
- Run unmodified: `src/__tests__/metrics.test.ts`, `src/__tests__/claims.test.ts`, `src/__tests__/governance.test.ts`, `src/__tests__/siteFaq.test.tsx`; update one pin in `src/__tests__/faq-evidence.test.ts`

**Interfaces:**
- Consumes: `companyIdentity` from `src/data/shipped/company.ts`; `honestyLabel` from `siteContent.ts`; claim IDs from `claims-registry.json`; existing enquiry helpers in `src/lib/enquiry.ts`.
- Produces: `aboutMetrics: readonly PublicMetric[]` (each tile has `claimId` + badge); canonical `ENQUIRY_RESPONSE_COPY`; softened FAQ evidence (`64 verified, 8 unknown`); zero unbadged `100%` metrics and zero response-time promises.

- [ ] **Step 1: Branch and baseline**

```powershell
Get-Content .ai-company/constitution/16-AGENT-GUARDRAILS.md
git status --short
git switch -c fix/ground-public-claims
npx vitest run src/__tests__/metrics.test.ts src/__tests__/faq-evidence.test.ts src/__tests__/claims.test.ts src/__tests__/governance.test.ts
```

Verify the pre-existing `opencode.json` modification is still present and unstaged. Never `restore`, `reset --hard`, `clean`, or force-push.

- [ ] **Step 2: Create the registry-backed metric seam**

Create `src/data/publicMetrics.ts`:

```ts
import companyIdentity from './shipped/company';
import { honestyLabel, type HonestyLabel } from './siteContent';

export interface PublicMetric {
  id: string;
  value: string;
  label: string;
  /** Claim id in src/data/registries/claims-registry.json that grounds this tile. */
  claimId: string;
  badge: HonestyLabel;
}

export const aboutMetrics: readonly PublicMetric[] = [
  {
    id: 'operating-roles',
    value: String(companyIdentity.totalRoles),
    label: 'Operating Roles (89 Agents + 1 Human CEO)',
    claimId: 'claim.agent-count',
    badge: honestyLabel('Proven in-house'),
  },
  {
    id: 'haomtgv-layers',
    value: '7',
    label: 'HAOMTGV Operating Layers',
    claimId: 'claim.haomtgv-seven-layers',
    badge: honestyLabel('Proven in-house'),
  },
  {
    id: 'approval-tiers',
    value: String(companyIdentity.governanceTiers),
    label: 'Human Approval Tiers',
    claimId: 'claim.five-tier-approval',
    badge: honestyLabel('Proven in-house'),
  },
  {
    id: 'departments',
    value: String(companyIdentity.departmentCount),
    label: 'Departments',
    claimId: 'claim.department-count',
    badge: honestyLabel('Proven in-house'),
  },
];
```

Append to the `claims` array in `src/data/registries/claims-registry.json`:

```json
{
  "id": "claim.haomtgv-seven-layers",
  "text": "HAOMTGV names seven operating layers: Human, Agents, Orchestration, Memory, Tools, Governance, Value.",
  "classification": "PROVEN_IN_HOUSE",
  "evidenceRef": "src/components/home/HAOMTGVSection.tsx (seven pillars: Human, Agents, Orchestration, Memory, Tools, Governance, Value); src/data/homeImmersiveCopy.ts (haomtgv layer)",
  "owner": "cto",
  "lastVerified": "2026-11-25",
  "expiryDate": "2027-02-25"
}
```

Bump `claimCount.value` in `metrics-registry.json` from 24 to 25. Do **not** add a claim for `100% Audit Trail Coverage` — no measurement exists.

- [ ] **Step 3: Replace the unbadged About tile**

In `src/components/AboutSection.tsx`, add:

```ts
import { aboutMetrics } from '../data/publicMetrics';
import { HonestyBadge } from './site/HonestyBadge';
```

Replace the whole inline tile array with:

```tsx
<div className="grid grid-cols-2 lg:grid-cols-4 gap-4 pt-8 max-w-5xl mx-auto text-left">
  {aboutMetrics.map((metric) => (
    <div key={metric.id} className={`p-4 rounded-2xl ${isLight ? 'bg-ls-white border border-slate-200/80' : 'bg-white/5 border border-white/10'}`}>
      <div className={`text-2xl sm:text-3xl font-extrabold font-display ${isLight ? 'text-ls-navy' : 'text-white'}`}>{metric.value}</div>
      <div className={`text-[11px] sm:text-xs font-mono uppercase tracking-wider mt-1 ${mutedText}`}>{metric.label}</div>
      <HonestyBadge label={metric.badge} className="mt-2" />
    </div>
  ))}
</div>
```

Edit only this block and the imports; leave Task 3's changes in the same file untouched.

- [ ] **Step 4: Single-source non-promissory enquiry copy**

Replace the header of `src/lib/enquiry.ts` with:

```ts
/**
 * Response posture — deliberately not a response-time SLA. No published
 * measurement backs a timed response promise (AGENTS.md §7; PRODUCT.md
 * "Evidence on Hand"). Every public surface imports this one string.
 */
export const ENQUIRY_RESPONSE_COPY =
  'A person reviews every enquiry before we respond.';
```

Then: in `CtaBand.tsx` import `ENQUIRY_RESPONSE_COPY` and replace the two-business-days sentence with `{ENQUIRY_RESPONSE_COPY}`; in `ContactSection.tsx`, `ExecutiveBriefingModal.tsx`, `NewsletterSignup.tsx`, and `AskLightSpeed.tsx` replace `ENQUIRY_SLA_COPY` with `ENQUIRY_RESPONSE_COPY` and rewrite the two success messages to:
- `We have securely routed your message to the LightSpeed Holdings executive team. A person will review it and get in touch to arrange a confidential briefing.`
- `Our Senior Managing Partners have received your confidential inquiry. A person will review it before we schedule an executive diagnostic session.`

No file may retain the identifier `ENQUIRY_SLA_COPY` or any timing promise.

- [ ] **Step 5: Repair circular FAQ evidence**

In `src/data/faqs.ts`, delete ` Qualified enquiries receive a response within two business days.` from the `how-to-start` answer and set its evidence to:

```ts
      evidence: [
        { source: 'claim.no-paying-clients', status: 'verified' },
        { source: 'src/data/registries/cta-registry.json#REQUEST AN AI READINESS ASSESSMENT', status: 'verified' },
        { source: 'src/components/site/CtaBand.tsx#Tell us where your organisation stands today. We will tell you whether we can help and what you need to start.', status: 'verified' },
      ],
```

In `faq-registry.json`: delete the two-business-days sentence from `faq-25` and `faq-28`; set `faq-25` evidence to `{"source": "claim.no-paying-clients", "status": "verified"}`; set `faq-28` evidence to:

```json
{
  "source": "",
  "status": "unknown",
  "note": "No published basis exists for a response-time promise; the SLA sentence was removed. Only the E1 setup window below is sourced."
}
```

Change the description count from `(65 verified, 7 unknown)` to `(64 verified, 8 unknown)` and `lastUpdated` to `2026-11-25`. Update only the matching pin in `src/__tests__/faq-evidence.test.ts`: `expect(faqRegistry.lastUpdated).toBe('2026-11-25');`.

- [ ] **Step 6: Delete unsupported absolute percentages**

In `BeforeAfterWorkflow.tsx`: `94% less manual setup time; 100% encrypted trace logging.` → `Append-only SHA-256 audit records; no quantified impact claim.`; `100% Context Synthesis` → `Context synthesis`; `100% pre-execution policy enforcement; zero compliance surprises.` → `Policy gates check high-risk actions before execution; no quantified compliance outcome claimed.`; `100% Governed` → `Governed`. In `HaomtgvUnifiedArchitecture.tsx`: `100% Human` → `Human`; `100% Auditable` → `Auditable`; `100% Traceable` → `Traceable`.

- [ ] **Step 7: Write the regression guard**

Create `src/__tests__/public-claim-guards.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { aboutMetrics } from '../data/publicMetrics';
import { ENQUIRY_RESPONSE_COPY } from '../lib/enquiry';
import claimsRegistry from '../data/registries/claims-registry.json';

const root = process.cwd();
const read = (p: string) => readFileSync(join(root, p), 'utf8');
const claims = new Map(claimsRegistry.claims.map((c) => [c.id, c]));
const PUBLISHABLE = new Set(['VERIFIED', 'PROVEN_IN_HOUSE', 'PILOT', 'DEMONSTRATION', 'FIELDABLE', 'LIVE']);

describe('about-page metric tiles', () => {
  it('has exactly four tiles and no 100% absolute', () => {
    expect(aboutMetrics).toHaveLength(4);
    expect(aboutMetrics.map((m) => m.value)).not.toContain('100%');
    expect(aboutMetrics.map((m) => m.label).join(' ')).not.toMatch(/100%/);
    expect(aboutMetrics.map((m) => m.label)).not.toContain('Audit Trail Coverage');
  });

  it('grounds every tile in a publishable, externally sourced claim with a badge', () => {
    const failures: string[] = [];
    for (const metric of aboutMetrics) {
      const claim = claims.get(metric.claimId);
      if (!claim) { failures.push(`${metric.id}: unknown claim ${metric.claimId}`); continue; }
      if (!PUBLISHABLE.has(claim.classification)) failures.push(`${metric.id}: ${claim.classification} cannot back a live metric`);
      if (!claim.evidenceRef?.trim()) failures.push(`${metric.id}: empty evidenceRef`);
      if (claim.evidenceRef?.startsWith('src/lib/enquiry.ts#')) failures.push(`${metric.id}: circular self-reference`);
      if (!metric.badge?.label || !metric.badge?.tone) failures.push(`${metric.id}: missing honesty badge`);
    }
    expect(failures, failures.join('; ')).toEqual([]);
  });
});

describe('enquiry response copy', () => {
  it('is single-sourced and promises no response window', () => {
    expect(ENQUIRY_RESPONSE_COPY).toBe('A person reviews every enquiry before we respond.');
    expect(ENQUIRY_RESPONSE_COPY).not.toMatch(/business\s+days?|within\s+\d+|hour|week/i);
  });

  it('every public enquiry surface imports the canonical string', () => {
    for (const file of [
      'src/components/site/CtaBand.tsx', 'src/components/ContactSection.tsx',
      'src/components/ExecutiveBriefingModal.tsx', 'src/components/NewsletterSignup.tsx',
      'src/components/AskLightSpeed.tsx',
    ]) expect(read(file), `${file} must use ENQUIRY_RESPONSE_COPY`).toContain('ENQUIRY_RESPONSE_COPY');
  });
});

describe('unproven public-claim regression', () => {
  const walk = (dir: string): string[] =>
    readdirSync(dir).flatMap((entry) => {
      const full = join(dir, entry);
      if (statSync(full).isDirectory()) return walk(full);
      return /\.(ts|tsx|json)$/.test(entry) ? [full] : [];
    });
  const normalized = (p: string) => p.split(sep).join('/');

  it('never reintroduces the retired 100% metric copy on public surfaces', () => {
    const surfaces = [
      'src/components/AboutSection.tsx', 'src/components/BeforeAfterWorkflow.tsx',
      'src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx', 'src/data/publicMetrics.ts',
    ];
    const hits = surfaces.filter((f) => /100%/.test(read(f)));
    expect(hits, `unbadged 100% reintroduced in: ${hits.join(', ')}`).toEqual([]);
  });

  it('never reintroduces an unsupported response-time promise in public copy', () => {
    const banned = [
      'within two business days', 'within one business day',
      'We reply to qualified enquiries', 'ENQUIRY_SLA_COPY', '100% Audit Trail Coverage',
    ];
    const self = 'src/__tests__/public-claim-guards.test.ts';
    const violations: string[] = [];
    for (const dir of ['src/components', 'src/data', 'src/lib']) {
      for (const file of walk(join(root, dir))) {
        const rel = normalized(relative(root, file));
        if (rel === self) continue;
        const content = readFileSync(file, 'utf8');
        for (const phrase of banned) {
          if (content.toLowerCase().includes(phrase.toLowerCase())) violations.push(`${rel}: "${phrase}"`);
        }
      }
    }
    expect(violations, violations.join('\n')).toEqual([]);
  });
});
```

- [ ] **Step 8: Verify and commit**

```powershell
npx vitest run src/__tests__/public-claim-guards.test.ts src/__tests__/faq-evidence.test.ts src/__tests__/metrics.test.ts src/__tests__/claims.test.ts src/__tests__/siteFaq.test.tsx
npx vitest run
npm run build
git diff -- src/components/AboutSection.tsx src/components/BeforeAfterWorkflow.tsx
git status --short
```

If the diff shows interleaved pre-existing edits, ask the CEO whether to include those hunks or stage only this task's hunks with `git add -p`. Never discard prior work. Then:

```powershell
git add src/data/publicMetrics.ts src/data/registries/claims-registry.json src/data/registries/metrics-registry.json src/components/AboutSection.tsx src/lib/enquiry.ts src/components/site/CtaBand.tsx src/components/ContactSection.tsx src/components/ExecutiveBriefingModal.tsx src/components/NewsletterSignup.tsx src/components/AskLightSpeed.tsx src/data/faqs.ts src/data/registries/faq-registry.json src/__tests__/faq-evidence.test.ts src/components/BeforeAfterWorkflow.tsx src/components/haomtgv/HaomtgvUnifiedArchitecture.tsx src/__tests__/public-claim-guards.test.ts
git commit -m "fix(site): ground public metrics and remove unsupported response SLA"
```

---

## Task 5: Make legacy redirects honest and surface the site IA

**Files:**
- Create: `src/lib/legacyRedirects.ts`, `src/components/site/LegacyRedirect.tsx`, `src/__tests__/legacyRedirects.test.tsx`
- Modify: `src/App.tsx`, `src/components/SiteLayout.tsx`, `src/components/home/VisitorPathsSection.tsx` (second owner, after Task 1)
- Reference only: `src/pages/InsightArticlePage.tsx` (do not edit)

**Interfaces:**
- Consumes: React Router 7 (`createBrowserRouter`, `RouterProvider`, `Navigate`, `useLocation`, `Link`, `createMemoryRouter`); `SiteContext`; the existing `ROUTE_META`/`applyPageMeta` SEO block in `SiteLayout.tsx`; the real article slug `open-source-cost-architecture`.
- Produces: `LEGACY_REDIRECTS` with 19 rows; `LegacyRedirect` (single hop) plus `LegacyRedirectNotice` (`role="status"`); homepage Ask LightSpeed CTA pointing at `/contact`.

- [ ] **Step 1: Branch and record the ECL change**

```powershell
git switch -c fix/honest-legacy-redirects
.\scripts\maintenance\harness-change.ps1 new "Honest legacy redirects and visible IA"
```

Never `git add .`; include the ECL files as explicit `git add` paths at commit time.

- [ ] **Step 2: Create the redirect registry**

Create `src/lib/legacyRedirects.ts`:

```ts
export interface LegacyRedirect {
  /** Route pattern as declared in the router (no leading slash). */
  from: string;
  /** Canonical live route (single hop, V2 architecture ruling). */
  to: string;
  /** Human name shown in the "moved" notice. */
  label: string;
}

/** Every retired path and its one-hop destination. Keep in sync with App.tsx. */
export const LEGACY_REDIRECTS: readonly LegacyRedirect[] = [
  { from: 'ai-company-builder', to: '/what-we-do', label: 'AI Company Builder' },
  { from: 'solutions', to: '/what-we-do', label: 'Solutions' },
  { from: 'sectors', to: '/what-we-do', label: 'Sectors' },
  { from: 'sectors/:slug', to: '/what-we-do', label: 'Sector brief' },
  { from: 'use-cases', to: '/what-we-do', label: 'Use cases' },
  { from: 'use-cases/:slug', to: '/what-we-do', label: 'Use case' },
  { from: 'faqs', to: '/faq', label: 'FAQs' },
  { from: 'who-we-are', to: '/about', label: 'Who we are' },
  { from: 'privacy', to: '/legal/privacy', label: 'Privacy' },
  { from: 'terms', to: '/legal/terms', label: 'Terms' },
  { from: 'architecture', to: '/what-we-do', label: 'Architecture' },
  { from: 'build', to: '/what-we-do', label: 'Build' },
  { from: 'offer-a', to: '/what-we-do', label: 'Offer A' },
  { from: 'offer-b', to: '/what-we-do', label: 'Offer B' },
  { from: 'offer-c', to: '/what-we-do', label: 'Offer C' },
  { from: 'offer-d', to: '/what-we-do', label: 'Offer D' },
  { from: 'offer-e', to: '/what-we-do', label: 'Offer E' },
  { from: 'proof', to: '/what-we-do', label: 'Proof' },
  { from: 'ask', to: '/contact', label: 'Ask LightSpeed' },
];
```

- [ ] **Step 3: Create the one-hop redirect and notice**

Create `src/components/site/LegacyRedirect.tsx`:

```tsx
import React from 'react';
import { Link, Navigate, useLocation } from 'react-router-dom';

export interface LegacyRedirectProps { to: string; label: string; }
export interface LegacyRedirectNoticeProps { from: string; label?: string; to: string; }

export const LegacyRedirect: React.FC<LegacyRedirectProps> = ({ to, label }) => {
  const { pathname } = useLocation();
  return <Navigate to={to} replace state={{ legacyFrom: pathname, legacyLabel: label }} />;
};

export const LegacyRedirectNotice: React.FC<LegacyRedirectNoticeProps> = ({ from, label, to }) => (
  <div role="status" aria-live="polite" data-testid="legacy-redirect-notice"
    className="mb-6 rounded-2xl border border-ls-cyan/40 bg-ls-cyan/10 px-5 py-4 font-body text-sm text-ls-navy dark:text-white">
    <p className="font-bold">
      You followed an old link to {label ? <strong>{label}</strong> : <code>{from}</code>} ({from}). It has moved.
    </p>
    <p className="mt-1">
      This is the current home for that content:{' '}
      <Link to={to} className="font-bold underline">{to}</Link>
    </p>
  </div>
);
```

- [ ] **Step 4: Rewire the router**

In `src/App.tsx`, replace `import { createBrowserRouter, Navigate, RouterProvider }` with `import { createBrowserRouter, RouterProvider }` and add the two new imports. Replace the 19 hardcoded `Navigate` routes with:

```tsx
{ path: 'what-we-do', element: <WhatWeDoPageRoute /> },
...LEGACY_REDIRECTS.map(({ from, to, label }) => ({
  path: from,
  element: <LegacyRedirect to={to} label={label} />,
})),
{ path: 'haomtgv', element: <HaomtgvPageRoute /> },
{ path: 'ai-assessment', element: <AiAssessmentPageRoute /> },
{ path: 'faq', element: <FaqPageRoute /> },
{ path: 'insights', element: <InsightsPageRoute /> },
{ path: 'insights/:slug', element: <InsightArticlePageRoute /> },
{ path: 'about', element: <AboutPageRoute /> },
{ path: 'contact', element: <ContactPageRoute /> },
{ path: 'legal/privacy', element: <PrivacyPageRoute /> },
{ path: 'legal/terms', element: <TermsPageRoute /> },
```

Keep `{ path: '*', element: <NotFoundPage /> }` last. Do not touch `InsightArticlePage.tsx`'s unknown-slug redirect.

- [ ] **Step 5: Render the notice additively in SiteLayout**

Add `import { LegacyRedirectNotice } from './site/LegacyRedirect';`, change `const { pathname, hash } = useLocation();` to:

```tsx
const location = useLocation();
const { pathname, hash } = location;
const legacyState = location.state as { legacyFrom?: string; legacyLabel?: string } | null;
```

and insert inside `<main id="main-content">` above `<Outlet />`:

```tsx
{legacyState?.legacyFrom && (
  <LegacyRedirectNotice from={legacyState.legacyFrom} label={legacyState.legacyLabel} to={pathname} />
)}
```

Do not edit `ROUTE_META`, `NOT_FOUND_META`, or the `applyPageMeta` effect.

- [ ] **Step 6: Point the homepage CTA at its real destination**

In `src/components/home/VisitorPathsSection.tsx`, change the Ask LightSpeed link from `to="/ask"` to `to="/contact"`, keeping its label and colours.

- [ ] **Step 7: Write the failing test**

Create `src/__tests__/legacyRedirects.test.tsx`:

```tsx
/// <reference types="vitest" />
import React from 'react';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { createMemoryRouter, RouterProvider, type RouteObject } from 'react-router-dom';
import { readFileSync } from 'node:fs';
import { SiteContext } from '../site-context';
import { SiteLayout } from '../components/SiteLayout';
import { LegacyRedirect } from '../components/site/LegacyRedirect';
import { LEGACY_REDIRECTS } from '../lib/legacyRedirects';

vi.mock('../components/FloatingNav', () => ({ FloatingNav: () => <div /> }));
vi.mock('../components/ExecutiveBriefingModal', () => ({ ExecutiveBriefingModal: () => null }));
vi.mock('../components/BackToTop', () => ({ BackToTop: () => null }));

const contextValue = {
  theme: 'dark' as const,
  onToggleTheme: () => {},
  onRequestBriefing: () => {},
  isBriefingOpen: false,
  briefingSummary: '',
  closeBriefing: () => {},
};

const livePaths = [
  '/', '/what-we-do', '/haomtgv', '/ai-assessment', '/faq', '/insights',
  '/insights/open-source-cost-architecture', '/about', '/contact',
  '/legal/privacy', '/legal/terms',
];

const testRoutes: RouteObject[] = [{
  path: '/',
  element: <SiteLayout />,
  children: [
    { index: true, element: <div data-testid="live-page">Live page: /</div> },
    ...livePaths.filter((p) => p !== '/').map((p) => ({
      path: p.replace(/^\//, ''),
      element: <div data-testid="live-page">Live page: {p}</div>,
    })),
    ...LEGACY_REDIRECTS.map(({ from, to, label }) => ({
      path: from,
      element: <LegacyRedirect to={to} label={label} />,
    })),
    { path: '*', element: <div data-testid="not-found">Not found</div> },
  ],
}];

function renderAt(path: string) {
  const router = createMemoryRouter(testRoutes, { initialEntries: [path] });
  const view = render(
    <SiteContext.Provider value={contextValue}>
      <RouterProvider router={router} />
    </SiteContext.Provider>,
  );
  return { router, ...view };
}

describe('legacy redirects are honest and single-hop', () => {
  beforeEach(() => {
    cleanup();
    document.head.innerHTML = '';
    document.title = '';
  });

  it.each(LEGACY_REDIRECTS.map((r) => [r.from, r.to, r.label] as const))(
    '%s resolves in one hop to %s with a visible moved notice',
    (from, to, label) => {
      const visit = `/${from.replace(':slug', 'sample-slug')}`;
      const { router } = renderAt(visit);
      expect(router.state.location.pathname).toBe(to);
      expect((router.state.location.state as { legacyFrom?: string }).legacyFrom).toBe(visit);
      expect(screen.getByTestId('live-page')).toHaveTextContent(`Live page: ${to}`);
      const notice = screen.getByRole('status');
      expect(notice).toHaveTextContent(visit);
      expect(notice).toHaveTextContent(label);
      expect(notice).toHaveTextContent(to);
      expect(screen.getByRole('link', { name: to })).toHaveAttribute('href', to);
    },
  );

  it('keeps the destination SEO title (applyPageMeta) intact after the redirect', () => {
    renderAt('/ask');
    expect(document.title).toBe('Contact | LightSpeed Holdings Limited™');
    expect(document.querySelector('link[rel="canonical"]')).toHaveAttribute('href', expect.stringContaining('/contact'));
  });

  it('does not break /insights/:slug — a known article stays on its own URL', () => {
    const routes: RouteObject[] = [{
      path: '/',
      element: <SiteLayout />,
      children: [{ path: 'insights/:slug', element: <div data-testid="article">Article</div> }],
    }];
    const router = createMemoryRouter(routes, { initialEntries: ['/insights/open-source-cost-architecture'] });
    render(<SiteContext.Provider value={contextValue}><RouterProvider router={router} /></SiteContext.Provider>);
    expect(router.state.location.pathname).toBe('/insights/open-source-cost-architecture');
    expect(screen.getByTestId('article')).toBeInTheDocument();
    expect(screen.queryByRole('status')).toBeNull();
  });

  it('App.tsx renders LEGACY_REDIRECTS (map is wired, not orphaned)', () => {
    const app = readFileSync('src/App.tsx', 'utf8');
    expect(app).toContain('LEGACY_REDIRECTS.map(');
    expect(app).toContain('<LegacyRedirect');
    expect(app).not.toContain('<Navigate');
    for (const { from } of LEGACY_REDIRECTS) {
      expect(LEGACY_REDIRECTS.filter((r) => r.from === from)).toHaveLength(1);
    }
  });

  it('homepage "Ask LightSpeed" CTA links to canonical /contact, not /ask', () => {
    const vp = readFileSync('src/components/home/VisitorPathsSection.tsx', 'utf8');
    expect(vp).toMatch(/<Link\s+to="\/contact"[^>]*>\s*Ask LightSpeed/);
    expect(vp).not.toContain('<Link to="/ask"');
  });
});
```

- [ ] **Step 8: Verify and commit**

```powershell
npm run test -- src/__tests__/legacyRedirects.test.tsx
npm run test
npm run lint
npm run build
git diff --check
git add src/lib/legacyRedirects.ts src/components/site/LegacyRedirect.tsx src/App.tsx src/components/SiteLayout.tsx src/components/home/VisitorPathsSection.tsx src/__tests__/legacyRedirects.test.tsx
git commit -m "fix(site): make legacy redirects honest and surface canonical IA"
```

Include the ECL change files from Step 1 as explicit `git add` paths.

---

## Whole-branch close-out (qa_lead + vp_engineering)

- [ ] Run the full gate: `npm test`, `npm run build`, `npm run lint`, `git diff --check`.
- [ ] Re-run Lighthouse on dev 1441 and preview 1440; both must remain at accessibility 1.00 with zero failures.
- [ ] Re-run the Impeccable detector; the only accepted findings are the three proven false positives (blockquote `border-l-4`, `slate-950` on `cyan-500`, nav active-state `border-l-2`).
- [ ] Confirm `git status --short` shows `opencode.json` still unstaged and no file from the CEO Dashboard was touched.
- [ ] Open/verify PRs from `gh pr create` output; read CI with `gh pr checks`; report "local only" for anything not yet green on CI.

## Self-review record

- **Spec coverage:** all five CEO next steps have an owning task; brand-token unification and the accessibility baseline are covered by Task 0 + Task 3 tests.
- **Placeholder scan:** no `TBD`, `TODO`, "implement later", or "similar to Task N" remains. Full file bodies are given for new files and for all tests; edit steps on existing components are precise class-string and copy-string instructions rather than full rewritten files — the executor must read the named file before editing and preserve all surrounding copy.
- **Type consistency:** `PublicMetric`, `LegacyRedirect`, `LegacyRedirectNoticeProps`, `BADGE_BASE_CLASSES`, `TONE_STYLES`, `EVIDENCE_STATUS_CLASSES`, `ENQUIRY_RESPONSE_COPY`, and `aboutMetrics` are defined once and used with the same names in their tests.
- **Review focus:** all five failure modes in the Review Focus section are pinned by named tests in Tasks 1–5.
- **Known risk:** `honestyBadge.test.tsx` assumes the exact FAQ evidence string `claim.agent-count (verified)` renders after clicking "What is the AI Company Builder?"; if the current registry uses a different source label, update the assertion to the real rendered string before implementing, without changing the test's intent.
- **Scope note:** the five tasks are independent and each produces a testable, committable deliverable. One PR per task is recommended; do not land them as a single mixed branch.

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-11-25-marketing-site-trust-and-clarity.md`. Please review the plan.

Which execution approach would you prefer?

- **Subagent-driven** — a fresh subagent implements each task and a fresh reviewer checks it before the next task starts, then a whole-branch review at the end. Most thorough; costs a fresh context per task and per review.
- **Native** — I implement every task in this session, the way this harness runs work, then one fresh reviewer on the most capable model checks the whole branch. Cheapest and fastest; no independent review until the end.

For this plan I recommend **subagent-driven**, because six tasks touch shared files in a fixed order and a mistaken claim or redirect could damage public credibility — a fresh review gate before each handoff is worth the extra context. Does the plan capture what you want, and which approach should we use?
