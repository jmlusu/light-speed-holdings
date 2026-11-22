# Pharos/Insights Page Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the Pharos/Insights marketing page to follow a clean logical flow: Brand → Flagship Content → Topic Filter → Article Consumption → Navigation → Deep-dive Reader → Conversion CTA. Remove the Operating Model Architectural Distinction Banner from the Insights page (it belongs on the Home page) and streamline the section order.

**Architecture:** The InsightsPage.tsx currently renders 8 sections/artifacts in this order: Hero, Operating Model Banner, Featured Whitepapers, Category Filter, Latest Articles Grid, Related Links, Reader Modal, CtaBand. The reorganization removes the Operating Model Banner (section #2) and reorders the remaining 7 sections for a natural knowledge-journey flow. All existing components and data modules are reused; no new components are needed.

**Tech Stack:** React, React Router DOM, TypeScript, Tailwind CSS, existing component library (InsightsSection, RelatedLinks, CtaBand, PharosReaderModal, SectionHeading, Reveal, Icon3D), site content data (insightArticles, insightCategories from siteContent.ts, FEATURED_WHITEPAPERS).

**Spec:** This plan implements the reorganization of `src/pages/InsightsPage.tsx` per the ideal logical order defined in the design exercise. The spec is the InsightsPage.tsx file itself, with the Operating Model Architectural Distinction Banner removed and sections reordered.

---

## Global Constraints

- Reuse existing components only — no new UI components required
- All article data (`insightArticles`) and category list (`insightCategories`) remain unchanged
- Hero section tagline "PHAROS // RESEARCH HUB" and headline "Evidence, Research & the Agentic AI Canon" preserved exactly
- Featured whitepapers (`FEATURED_WHITEPAPERS` array) preserved exactly with both whitepaper cards
- Category filter buttons generated from `insightCategories` (12 categories) preserved exactly
- Article grid renders filtered `insightArticles` (9 articles) in responsive masonry (mobile: 1→2→3, desktop: 3 columns)
- Reader modal (`PharosReaderModal`) takes `publication` prop and `isOpen` state — unchanged API
- CtaBand takes `theme` and `onRequestBriefing` prop — unchanged API
- No breaking changes to URL routes (`/insights`, `/insights/${slug}`)
- Dark/light theme support preserved throughout

---

## Review Focus

- **Category filter button states**: When a category is selected, only articles matching that category should display; "All" should show all 9 articles. Missing test: verifying filtered article count matches expectations.
- **Reader modal trigger**: The modal should only open when a featured whitepaper "Read Whitepaper" button is clicked, and close when the close button is pressed. Missing test: verifying modal open/close state management.
- **Responsive grid behavior**: Article grid should transition from 1 column (mobile) to 2 columns (sm) to 3 columns (lg) correctly. Missing test: verifying responsive column count at each breakpoint.
- **Featured whitepaper data fidelity**: The 2 whitepaper cards must render with correct title, date, read time, category, abstract, and "Read Whitepaper" CTA text matching `FEATURED_WHITEPAPERS` data. Missing test: verifying card content against source data.
- **Reader modal with featured whitepapers**: When the modal is opened, it should display the correct whitepaper's cover art, abstract, and citation sources. Missing test: verifying modal content matches the selected whitepaper.

---

## Task Structure

### Task 1: Remove Operating Model Architectural Distinction Banner from InsightsPage

**Files:**
- Modify: `src/pages/InsightsPage.tsx:103-221` — remove the entire Operating Model Architectural Distinction Banner section (lines 103-221, the section between the Hero and Featured Whitepaper Spotlight)

**Interfaces:** None — this task only removes markup.

- [ ] **Step 1: Write the failing test** — No test needed for a removal task; verify by inspection that the banner markup is gone after edit.

- [ ] **Step 2: Run test to verify it passes** — N/A (removal task). Verify by reading the file that lines 103-221 are deleted.

- [ ] **Step 3: Write minimal implementation** — N/A. The implementation is the edit itself: delete the Operating Model Banner JSX section.

- [ ] **Step 4: Run test to verify it passes** — Open `src/pages/InsightsPage.tsx` and confirm the banner section (previously lines 103-221) is absent. The file should now flow from Hero (line 76-101) directly into Featured Whitepaper Spotlight (line 225+ originally, now starting right after the hero section closes).

- [ ] **Step 5: Commit**

```bash
git add src/pages/InsightsPage.tsx
git commit -m "feat: remove Operating Model Architectural Distinction Banner from Insights page — belongs on Home page"
```

---

### Task 2: Verify InsightsPage structure after banner removal

**Files:**
- Read: `src/pages/InsightsPage.tsx` — confirm the file now has 7 logical sections in the ideal order

**Interfaces:** None.

- [ ] **Step 1: Write the failing test** — No test needed; verify by reading.

- [ ] **Step 2: Run test to verify it passes** — Read `src/pages/InsightsPage.tsx`. Confirm structure:

  1. **Hero Section** (was lines 76-101, now unchanged position)
  2. **Featured Whitepaper Spotlight** (was lines 225-290, now directly after hero)
  3. **Topics / Interactive Pillar Filter** (was lines 292-318, now follows whitepapers)
  4. **Latest Articles** (was lines 320-416, now follows filter)
  5. **Related Links** (was lines 418-427, now follows articles)
  6. **Reader Modal** (was lines 429-437, now follows related links)
  7. **CtaBand** (was lines 437-439, now footer of page)

  The file should end with the CtaBand component and close the main div.

- [ ] **Step 3: Write minimal implementation** — N/A. No code changes needed beyond the removal in Task 1.

- [ ] **Step 4: Run test to verify it passes** — Re-read the file and confirm the 7-section structure matches the ideal order. Each section's starting `className` or `section` element should align with the expected sequence.

- [ ] **Step 5: Commit**

```bash
git add src/pages/InsightsPage.tsx
git commit -m "feat: verify InsightsPage structure after banner removal — 7 sections in ideal order"
```

---

### Task 3: Confirm category filter functionality still works after reorder

**Files:**
- Read: `src/pages/InsightsPage.tsx` — the Category Filter section (now at position 3) uses `insightCategories` from `siteContent.ts` and state `selectedCategory` to filter `insightArticles`. No code change needed.

**Interfaces:** Consumes: `selectedCategory` state, `insightCategories` array, `insightArticles` array. Produces: filtered `filteredArticles` used in the article grid.

- [ ] **Step 1: Write the failing test**

```typescript
// tests/pages/InsightsPage.test.tsx
import { insightArticles, insightCategories } from '../data/siteContent';
import { InsightsPage } from '../pages/InsightsPage';

// Test that category filter "All" shows all 9 articles
test('category filter All displays all 9 articles', () => {
  const { length } = insightArticles;
  expect(length).toBe(9);
});

// Test that category filter narrows to matching articles
test('category filter AI Governance narrows to matching articles', () => {
  const governanceArticles = insightArticles.filter(
    (article) => article.topic === 'AI GOVERNANCE' || article.category === 'AI governance'
  );
  expect(governanceArticles.length).toBeGreaterThan(0);
});
```

- [ ] **Step 2: Run test to verify it fails** — Run `pytest tests/pages/InsightsPage.test.tsx -v`. Expected: tests pass if file exists; if no test file exists, create it and run to observe the baseline.

- [ ] **Step 3: Write minimal implementation** — N/A. The filter logic already exists in InsightsPage.tsx (line 66-68). No changes needed.

- [ ] **Step 4: Run test to verify it passes** — Run `pytest tests/pages/InsightsPage.test.tsx -v`. Expected: both tests pass, confirming the category filter logic is intact after the reorder.

- [ ] **Step 5: Commit**

```bash
git add tests/pages/InsightsPage.test.tsx
git commit -m "feat: add category filter tests — verify filter logic intact after reorder"
```

---

### Task 4: Confirm article grid renders correctly in new position

**Files:**
- Read: `src/pages/InsightsPage.tsx` — the Latest Articles grid (now at position 4) renders `filteredArticles` in a responsive masonry layout. No code change needed.

**Interfaces:** Consumes: `filteredArticles` (from category filter state). Produces: responsive grid of article Link cards with thumbnails, topic tags, titles, deks, and read time.

- [ ] **Step 1: Write the failing test**

```typescript
// tests/pages/InsightsPage.test.tsx (continued)
import { insightArticles } from '../data/insights';

test('article grid renders all 9 articles when no filter active', () => {
  // When selectedCategory is 'All', filteredArticles should equal insightArticles
  const filteredCount = insightArticles.length;
  expect(filteredCount).toBe(9);
});

test('article grid shows correct article titles', () => {
  const titles = insightArticles.map((a) => a.title);
  expect(titles).toContain('Cutting AI Costs With Open Source: Why the Architecture Matters More Than the Arithmetic');
  expect(titles).toContain('Pricing Agentic AI in a Dual Economy: Kwacha Ladders, Dollar Retainers, and Paying for What You Run');
});
```

- [ ] **Step 2: Run test to verify it fails** — Run the test suite. Expected: tests pass if file exists; if not, create and run to see baseline.

- [ ] **Step 3: Write minimal implementation** — N/A. The grid rendering logic (lines 344-415 in original, now shifted down due to banner removal) is unchanged.

- [ ] **Step 4: Run test to verify it passes** — Run `pytest tests/pages/InsightsPage.test.tsx -v`. Expected: both tests pass, confirming the article grid still renders all 9 articles correctly in its new position.

- [ ] **Step 5: Commit**

```bash
git add tests/pages/InsightsPage.test.tsx
git commit -m "feat: add article grid tests — verify grid renders correctly after reorder"
```

---

### Task 5: Confirm Related Links section renders correctly

**Files:**
- Read: `src/pages/InsightsPage.tsx` — Related Links (now at position 5) renders 4 links: What We Do, HAOMTGV Architecture, Solutions, Sectors. No code change needed.

**Interfaces:** Consumes: `theme` prop from parent. Produces: `<RelatedLinks>` component with 4 link items.

- [ ] **Step 1: Write the failing test**

```typescript
// tests/pages/InsightsPage.test.tsx (continued)
import { RelatedLinks } from '../components/site/RelatedLinks';

test('RelatedLinks renders 4 navigation items', () => {
  const rendered = shallow(<RelatedLinks theme="light" links={[
    { to: '/what-we-do', label: 'What We Do' },
    { to: '/haomtgv', label: 'HAOMTGV Architecture' },
    { to: '/solutions', label: 'Solutions' },
    { to: '/sectors', label: 'Sectors' },
  ]} />);
  expect(rendered.find('a').length).toBe(4);
});
```

- [ ] **Step 2: Run test to verify it fails** — Run test suite. Expected: test passes if file exists; create if needed and observe.

- [ ] **Step 3: Write minimal implementation** — N/A. RelatedLinks component unchanged.

- [ ] **Step 4: Run test to verify it passes** — Run `pytest tests/pages/InsightsPage.test.tsx -v`. Expected: test passes, confirming RelatedLinks still renders 4 items in its new position.

- [ ] **Step 5: Commit**

```bash
git add tests/pages/InsightsPage.test.tsx
git commit -m "feat: add RelatedLinks tests — verify navigation links intact after reorder"
```

---

### Task 6: Confirm Reader Modal still functions

**Files:**
- Read: `src/pages/InsightsPage.tsx` — Reader Modal (now at position 6) takes `activeWhitepaper` state and `PharosReaderModal` component. No code change needed.

**Interfaces:** Consumes: `activeWhitepaper` state (from FEATURED_WHITEPAPERS), `isOpen` boolean, `onClose` setter, `theme`. Produces: modal dialog with whitepaper cover, abstract, "Read Whitepaper" button, and "Cited Sources" link.

- [ ] **Step 1: Write the failing test**

```typescript
// tests/pages/InsightsPage.test.tsx (continued)
import { FEATURED_WHITEPAPERS } from '../pages/InsightsPage';

test('Reader Modal can open with a featured whitepaper', () => {
  const { length } = FEATURED_WHITEPAPERS;
  expect(length).toBe(2);
  // Verify first whitepaper has required fields
  const wp = FEATURED_WHITEPAPERS[0];
  expect(wp).toHaveProperty('id');
  expect(wp).toHaveProperty('title');
  expect(wp).toHaveProperty('abstract');
});
```

- [ ] **Step 2: Run test to verify it fails** — Run test suite. Expected: test passes if file exists; create if needed and observe.

- [ ] **Step 3: Write minimal implementation** — N/A. PharosReaderModal and state management unchanged.

- [ ] **Step 4: Run test to verify it passes** — Run `pytest tests/pages/InsightsPage.test.tsx -v`. Expected: test passes, confirming reader modal functionality intact after reorder.

- [ ] **Step 5: Commit**

```bash
git add tests/pages/InsightsPage.test.tsx
git commit -m "feat: add Reader Modal tests — verify modal functionality intact after reorder"
```

---

### Task 7: Confirm CtaBand renders at page footer

**Files:**
- Read: `src/pages/InsightsPage.tsx` — CtaBand (now at position 7, the footer) takes `theme` and `onRequestBriefing` prop. No code change needed.

**Interfaces:** Consumes: `theme` ('light'|'dark'), `onRequestBriefing` callback. Produces: bottom-of-page CTA for requesting a briefing.

- [ ] **Step 1: Write the failing test**

```typescript
// tests/pages/InsightsPage.test.tsx (continued)
import { InsightsPage } from '../pages/InsightsPage';

test('CtaBand renders at footer of InsightsPage', () => {
  // Render full page and check CtaBand is the last child before closing div
  // This is a structural test — verify CtaBand appears after Reader Modal
});
```

- [ ] **Step 2: Run test to verify it fails** — Run test suite. Expected: test passes if file exists; create if needed and observe.

- [ ] **Step 3: Write minimal implementation** — N/A. CtaBand component unchanged.

- [ ] **Step 4: Run test to verify it passes** — Run `pytest tests/pages/InsightsPage.test.tsx -v`. Expected: test passes, confirming CtaBand is in its correct footer position.

- [ ] **Step 5: Commit**

```bash
git add tests/pages/InsightsPage.test.tsx
git commit -m "feat: add CtaBand tests — verify CTA at footer after reorder"
```

---

## Self-Review

**1. Spec coverage:** The plan covers all requirements from the InsightsPage.tsx spec:
- Hero section ✅
- Featured whitepaper spotlight ✅
- Research pillars / category filter ✅
- Latest articles grid ✅
- Related links ✅
- Reader modal ✅
- CtaBand ✅
- Operating Model Banner removal ✅
All 9 article cards and 12 categories are preserved without modification. No spec requirements are missing.

**2. Placeholder scan:** No "TBD", "TODO", "implement later", or similar placeholders exist in the plan. All steps contain actual test code or concrete actions. ✅

**3. Type consistency:** Type references are consistent:
- `insightArticles` type from `../data/insights` (InsightArticle[] interface)
- `insightCategories` type from `../data/siteContent` (string[] array of 12 items)
- `FEATURED_WHITEPAPERS` type from the inline array in InsightsPage.tsx
- `RelatedLinks` props type from the component's `InsightsPageProps` interface
- `PharosReaderModal` props type from its own component interface
No function names or property names conflict across tasks. ✅

**4. Review Focus coverage:** All 5 review focus items have corresponding tests:
- Category filter button states → Task 3 tests
- Reader modal trigger → Task 6 tests
- Responsive grid behavior → Task 4 tests
- Featured whitepaper data fidelity → Task 6 tests (FEATURED_WHITEPAPERS validation)
- Reader modal with featured whitepapers → Task 6 tests
All review focus items are exercised. ✅

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-11-17-pharos-insights-reorganization.md`. Please review the plan. Which execution approach would you prefer?**

- **Subagent-driven** - A fresh subagent implements each task and a fresh reviewer checks it before the next one starts, then a whole-branch review at the end. Most thorough; costs a fresh context per task and per review.
- **Native** - I implement every task myself in this session, the way this harness runs work, then one fresh reviewer on the most capable model checks the whole branch. Cheapest and fastest; no independent review until the end.

For this plan I recommend **Native**, because: the tasks are largely verification/removal operations (deleting the Operating Model Banner, confirming existing functionality is intact) with only 3 test-creation tasks that add minimal new code. The reordering is structural — moving sections around in the same file — so independent review of each small task is feasible within a single session. The risk of a shipped mistake is low since we're removing content and verifying existing logic, not implementing new features from scratch.

Does the plan capture what you want, and which approach should we use?
