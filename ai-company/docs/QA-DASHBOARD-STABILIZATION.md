# Dashboard Stabilization — QA Test Plan

> **Author:** QA Lead  
> **Date:** 2026-07-22  
> **Status:** Active  
> **Priority:** P0 — Blocking user experience  
> **Scope:** CEO Dashboard scroll instability, data loading, error handling, responsive design

---

## 1. Executive Summary

The CEO Dashboard exhibits unstable auto-scrolling behavior that degrades usability. After analyzing the full stack — FastAPI backend, Alpine.js frontend, WebSocket real-time updates, Chart.js rendering, and Jinja2 templates — this plan identifies root causes, defines acceptance criteria, and establishes a regression test suite to prevent recurrence.

### Key Findings from Code Review

| Area | Observation | Risk |
|------|-------------|------|
| **Polling** | `setInterval(() => this.loadPageData(), 10000)` fires every 10s | **HIGH** — Each cycle mutates Alpine.js state, triggering DOM re-renders |
| **Chart re-creation** | `updateChartsFromKPIs()` calls `destroyChart()` + `new Chart()` on every update | **HIGH** — Canvas resize/layout shift causes scroll position jumps |
| **WebSocket handler** | `Object.assign(this.kpis, msg.payload)` triggers reactive updates | **MEDIUM** — Additional state mutation path compounds re-render frequency |
| **CSS `scroll-behavior`** | `html { scroll-behavior: smooth; }` in `style.css` | **LOW** — Can mask or amplify unintended scroll events |
| **No scroll guards** | No `scrollRestoration`, no position save/restore, no debounce | **HIGH** — Nothing prevents scroll jump on data mutation |
| **Alpine.js reactivity** | `x-text`, `x-for`, `:class` bindings re-render on every state change | **MEDIUM** — Multiple template re-evaluations per update cycle |

---

## 2. Auto-Scroll Bug Analysis

### 2.1 Reproduction Steps

**Step 1: Start the dashboard**
```powershell
cd C:\Users\jmlus\light-speed-holdings\ai-company
ai-company dashboard --no-open
```

**Step 2: Open browser to `http://localhost:8420`**

**Step 3: Scroll down to the "Recent Tasks" table** (bottom of the dashboard page)

**Step 4: Wait 10–20 seconds** — observe that the page scrolls back to the top

**Step 5: Alternatively, force a data mutation:**
1. Open browser DevTools Console
2. Run: `document.querySelector('[x-data]').__x.$data.kpis.pending_tasks = 99`
3. Observe scroll position jump

**Step 6: WebSocket-triggered variant:**
1. Open two browser tabs to the dashboard
2. In tab 1, scroll down
3. In tab 2, assign a new task via the Tasks page
4. Tab 1 receives WebSocket update → scroll jumps

### 2.2 Root Cause Chain

```
10s polling interval fires
  → loadPageData() → loadDashboard()
    → fetchJSON('/api/dashboard') returns
      → Object.assign(this.kpis, kpis)     ← Alpine.js detects mutation
        → All x-text bindings re-evaluate
          → Template re-renders
            → Chart.js destroy/recreate    ← Canvas layout shift
              → Browser recalculates layout
                → Scroll position jumps to top (or nearest recalculation point)
```

### 2.3 Contributing Factors

1. **Chart.js destruction cycle**: `destroyChart()` removes the canvas element, then `new Chart()` recreates it. This changes page height, forcing the browser to recalculate scroll position.

2. **No `window.scrollY` preservation**: After DOM mutations, the browser may reset scroll position, especially when elements are removed/reinserted.

3. **Alpine.js `x-for` template re-rendering**: The `template x-for="t in tasks.slice(0, 10)"` re-evaluates the entire loop on every `this.tasks` mutation, causing DOM churn.

4. **Simultaneous update paths**: Both 10s polling AND WebSocket messages mutate the same state, creating overlapping update storms.

---

## 3. Acceptance Criteria — What Does "Stable" Look Like?

### 3.1 Scroll Behavior (P0)

| ID | Criterion | Measurement |
|----|-----------|-------------|
| AC-SCROLL-01 | Page scroll position is preserved after KPI polling update | Scroll position delta ≤ 0px after 5 consecutive poll cycles |
| AC-SCROLL-02 | Page scroll position is preserved after WebSocket push | Scroll position delta ≤ 0px after receiving WS message |
| AC-SCROLL-03 | User-initiated scroll is never overridden by system | Manual scroll down → wait 60s → position unchanged |
| AC-SCROLL-04 | Tab navigation preserves scroll state on return | Navigate away → return → scroll position restored |
| AC-SCROLL-05 | No visual "jump" or "flicker" during data updates | 0 reported visual artifacts in 5-minute observation |
| AC-SCROLL-06 | Charts re-render without layout shift | Chart container height variance ≤ 1px across updates |

### 3.2 Data Loading (P0)

| ID | Criterion | Measurement |
|----|-----------|-------------|
| AC-DATA-01 | KPI cards display correct values within 2s of page load | First meaningful paint ≤ 2s |
| AC-DATA-02 | Task list populates within 3s | Table rows visible ≤ 3s |
| AC-DATA-03 | WebSocket connects within 5s | `wsConnected === true` ≤ 5s |
| AC-DATA-04 | WebSocket auto-reconnects after disconnect | Reconnection ≤ 5s after server restart |
| AC-DATA-05 | 10s polling does not cause data flicker | No visible value flicker during poll cycle |
| AC-DATA-06 | Concurrent poll + WS update does not duplicate data | Task list length ≤ expected count |

### 3.3 Error Handling (P1)

| ID | Criterion | Measurement |
|----|-----------|-------------|
| AC-ERR-01 | API failure shows toast notification | Error toast within 3s of failed fetch |
| AC-ERR-02 | WebSocket disconnect shows "Offline" badge | Badge updates within 1s of disconnect |
| AC-ERR-03 | Empty states display helpful message | "No tasks yet" message when task list is empty |
| AC-ERR-04 | Network timeout does not crash the page | Page remains functional after 30s timeout |
| AC-ERR-05 | Rate limit (429) shows user-friendly message | Toast: "Too many requests" within 2s |

### 3.4 Responsive Design (P1)

| ID | Criterion | Measurement |
|----|-----------|-------------|
| AC-RESP-01 | Dashboard renders correctly at 320px width | No horizontal overflow, all content accessible |
| AC-RESP-02 | Dashboard renders correctly at 768px width | 2-column KPI grid, stacked charts |
| AC-RESP-03 | Dashboard renders correctly at 1440px width | 6-column KPI grid, side-by-side charts |
| AC-RESP-04 | Touch interactions work on mobile (≤768px) | Kanban drag-and-drop functional on touch |
| AC-RESP-05 | Navigation tabs are scrollable on narrow screens | Horizontal scroll on tab bar at 320px |

### 3.5 Cross-Browser (P2)

| ID | Criterion | Measurement |
|----|-----------|-------------|
| AC-BROWSER-01 | Chrome 120+ — all features functional | No console errors, all interactions work |
| AC-BROWSER-02 | Firefox 120+ — all features functional | No console errors, all interactions work |
| AC-BROWSER-03 | Edge 120+ — all features functional | No console errors, all interactions work |
| AC-BROWSER-04 | Safari 17+ — all features functional | No console errors, all interactions work |
| AC-BROWSER-05 | WebSocket works across all browsers | Connection established, messages received |

---

## 4. Test Scenarios

### 4.1 Scroll Behavior Tests

| # | Scenario | Priority | Type |
|---|----------|----------|------|
| S-01 | Initial page load scroll position is at top (0,0) | P0 | Automated |
| S-02 | Scroll to bottom → wait 30s → position unchanged | P0 | Automated |
| S-03 | Scroll to bottom → trigger KPI update → position unchanged | P0 | Automated |
| S-04 | Scroll to bottom → WebSocket push received → position unchanged | P0 | Automated |
| S-05 | Rapid scroll up/down during polling cycle → no jump | P0 | Manual |
| S-06 | Navigate to Tasks tab → scroll → return to Dashboard → scroll restored | P1 | Automated |
| S-07 | Open modal → close → scroll position preserved | P1 | Automated |
| S-08 | Browser back/forward → scroll position restored | P1 | Manual |
| S-09 | Chart resize (window resize) → no scroll jump | P1 | Automated |
| S-10 | Multiple rapid WebSocket messages → stable scroll | P1 | Automated |

### 4.2 Data Loading Tests

| # | Scenario | Priority | Type |
|---|----------|----------|------|
| D-01 | KPI cards show correct values on first load | P0 | Automated |
| D-02 | Task table populates with correct data | P0 | Automated |
| D-03 | Polling updates KPI values without page disruption | P0 | Automated |
| D-04 | WebSocket KPI update applies without re-fetch | P0 | Automated |
| D-05 | Empty task list shows "No tasks yet" message | P1 | Automated |
| D-06 | API error shows toast notification | P1 | Automated |
| D-07 | WebSocket disconnect → reconnect cycle works | P1 | Automated |
| D-08 | Stale data not displayed after server restart | P2 | Manual |

### 4.3 Error Handling Tests

| # | Scenario | Priority | Type |
|---|----------|----------|------|
| E-01 | API server down → error toast displayed | P1 | Automated |
| E-02 | WebSocket server down → "Offline" badge shown | P1 | Automated |
| E-03 | Malformed WebSocket message → no crash | P1 | Automated |
| E-04 | 429 rate limit → user-friendly message | P2 | Automated |
| E-05 | 401 unauthorized → redirect to health check | P2 | Manual |
| E-06 | Invalid task creation → validation error shown | P2 | Automated |

### 4.4 Responsive Design Tests

| # | Scenario | Priority | Type |
|---|----------|----------|------|
| R-01 | 320px viewport — single column, no overflow | P1 | Automated |
| R-02 | 768px viewport — 2-col KPI, stacked charts | P1 | Automated |
| R-03 | 1440px viewport — 6-col KPI, side-by-side charts | P1 | Automated |
| R-04 | Resize from 1440 → 320 → 1440 — layout adapts | P1 | Automated |
| R-05 | Mobile touch — kanban drag works | P2 | Manual |
| R-06 | Tab navigation scrollable on narrow screens | P2 | Manual |

### 4.5 Cross-Browser Tests

| # | Scenario | Priority | Type |
|---|----------|----------|------|
| B-01 | Chrome — full smoke test | P1 | Automated |
| B-02 | Firefox — full smoke test | P1 | Automated |
| B-03 | Edge — full smoke test | P2 | Automated |
| B-04 | Safari — full smoke test | P2 | Manual |
| B-05 | WebSocket — connection + message flow | P1 | Automated |

---

## 5. Regression Test Cases for Scroll Issues

These tests specifically prevent future scroll regressions:

| # | Regression Test | Assertion | Priority |
|---|----------------|-----------|----------|
| REG-01 | `scrollY` stable after 5 poll cycles | `Math.abs(scrollY_after - scrollY_before) === 0` | P0 |
| REG-02 | `scrollY` stable after WS `kpi_update` | `Math.abs(scrollY_after - scrollY_before) === 0` | P0 |
| REG-03 | `scrollY` stable after `loadDashboard()` | `Math.abs(scrollY_after - scrollY_before) === 0` | P0 |
| REG-04 | Chart canvas height stable after re-render | `canvas.offsetHeight === previous.offsetHeight` | P0 |
| REG-05 | No DOM element count change during update | `document.querySelectorAll('*').length === previous` | P1 |
| REG-06 | `document.body.scrollHeight` stable after update | `Math.abs(body.scrollHeight - previous) ≤ 1` | P1 |
| REG-07 | `performance.now()` layout recalc count ≤ 1 per update | `PerformanceObserver` entry count ≤ 1 | P2 |
| REG-08 | Tab switching + scroll → return preserves position | `scrollY === saved_scrollY` | P1 |
| REG-09 | Modal open/close → scroll preserved | `scrollY === saved_scrollY` | P1 |
| REG-10 | Rapid polling (1s interval) → scroll stable | `Math.abs(scrollY_after - scrollY_before) === 0` | P1 |

---

## 6. Architecture Diagram Validation Checklist

Before any stabilization fix is merged, verify:

| # | Check | Status |
|---|-------|--------|
| 1 | `base.html` header is `sticky top-0` — does NOT cause scroll issues | [ ] |
| 2 | `style.css` `scroll-behavior: smooth` does NOT interfere with programmatic scroll | [ ] |
| 3 | `app.js` `init()` — `setInterval` is properly cleaned up on page unload | [ ] |
| 4 | `app.js` `connectWebSocket()` — reconnect timer is cleaned up properly | [ ] |
| 5 | `app.js` `loadPageData()` — does NOT trigger full page re-render | [ ] |
| 6 | `charts.js` `destroyChart()` — removes chart WITHOUT affecting page layout | [ ] |
| 7 | `charts.js` `updateChartsFromKPIs()` — updates chart data without destroy/recreate | [ ] |
| 8 | `ws.py` — broadcast does NOT flood clients with duplicate messages | [ ] |
| 9 | `api.py` — `/api/dashboard` response does NOT include unnecessary data causing large payloads | [ ] |
| 10 | `index.html` — KPI cards use `x-text` binding (reactive) NOT full template re-render | [ ] |
| 11 | `index.html` — Recent Tasks table uses `x-for` with proper `:key` | [ ] |
| 12 | Alpine.js `x-init` does NOT trigger multiple simultaneous data loads | [ ] |
| 13 | WebSocket and polling do NOT update same state simultaneously without debouncing | [ ] |
| 14 | Chart.js `responsive: true` + `maintainAspectRatio: false` — canvas does NOT resize on content change | [ ] |
| 15 | Tailwind CDN config does NOT inject scripts that cause layout shifts | [ ] |

---

## 7. Recommended Testing Tools & Environment

### 7.1 Frontend E2E Testing (NEW — Critical Gap)

| Tool | Purpose | Why |
|------|---------|-----|
| **Playwright** | Browser automation, screenshot comparison, scroll position testing | Best cross-browser support, built-in assertion library, handles SPAs well |
| **Playwright Test** | Test runner with parallel execution | Integrated with CI, trace viewer for debugging |

**Why Playwright over Cypress:** Playwright supports multi-tab testing (needed for WebSocket sync tests), has better cross-browser coverage (Chromium, Firefox, WebKit), and doesn't require a running dev server for test isolation.

### 7.2 Backend Testing (EXISTING — Extend)

| Tool | Purpose | Status |
|------|---------|--------|
| **pytest** | Unit/integration tests | ✅ Already in use |
| **FastAPI TestClient** | API endpoint testing | ✅ Already in use |
| **pytest-asyncio** | Async WebSocket tests | ✅ Already in use |

### 7.3 Performance & Visual Testing (NEW)

| Tool | Purpose | Why |
|------|---------|-----|
| **Playwright screenshot comparison** | Visual regression | Detect layout shifts automatically |
| **Lighthouse CI** | Performance auditing | Catch performance regressions in CI |
| **Web Vitals** | Core Web Vitals monitoring | CLS (Cumulative Layout Shift) directly measures scroll-related jank |

### 7.4 Environment Setup

```powershell
# Install Playwright
cd C:\Users\jmlus\light-speed-holdings\ai-company
pip install playwright pytest-playwright
playwright install chromium firefox webkit

# Run dashboard for testing
ai-company dashboard --port 9420 --no-open

# Run existing backend tests
pytest tests/unit/test_dashboard*.py -v

# Run new E2E tests (once created)
pytest tests/e2e/ -v --browser chromium
```

### 7.5 CI Integration

```yaml
# Add to .github/workflows/test.yml
- name: Dashboard E2E Tests
  run: |
    pip install playwright pytest-playwright
    playwright install --with-deps chromium
    ai-company dashboard --port 9420 &
    sleep 5
    pytest tests/e2e/ -v --browser chromium
```

---

## 8. Test Execution Priority

### Phase 1: Immediate (Before Fix)
1. Create Playwright E2E test harness
2. Write scroll regression tests (REG-01 through REG-03)
3. Write chart stability test (REG-04)
4. Run existing backend tests to establish baseline

### Phase 2: During Fix
1. Implement scroll position preservation
2. Optimize Chart.js update strategy (update data, don't recreate)
3. Add debouncing to polling/WebSocket update paths
4. Run Phase 1 tests continuously

### Phase 3: After Fix
1. Run full regression suite (REG-01 through REG-10)
2. Run cross-browser smoke tests (B-01 through B-04)
3. Run responsive design tests (R-01 through R-06)
4. Run visual regression screenshots
5. Performance audit with Lighthouse

### Phase 4: Ongoing
1. Add scroll stability test to CI pipeline
2. Monitor CLS (Cumulative Layout Shift) in production
3. Monthly cross-browser smoke test
4. Quarterly accessibility audit

---

## 9. Exit Criteria

The dashboard stabilization is **complete** when:

- [ ] All P0 acceptance criteria (AC-SCROLL-01 through AC-SCROLL-06) pass
- [ ] All P0 regression tests (REG-01 through REG-04) pass
- [ ] No auto-scroll reported by users for 2 consecutive sprints
- [ ] CLS score ≤ 0.1 (Lighthouse)
- [ ] Chart re-render does not cause layout shift
- [ ] WebSocket + polling concurrent updates are debounced
- [ ] E2E tests are integrated into CI pipeline
- [ ] Cross-browser smoke tests pass on Chrome, Firefox, Edge

---

## 10. Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Chart.js destroy/recreate strategy change breaks other views | Medium | High | Create chart lifecycle unit tests before refactoring |
| Alpine.js upgrade changes reactivity model | Medium | Low | Pin Alpine.js version, test before upgrade |
| WebSocket message frequency increase overwhelms frontend | High | Medium | Add message deduplication + throttle in `handleWSMessage` |
| Polling interval change affects data freshness perception | Low | Medium | A/B test interval, survey users |
| Cross-browser CSS differences cause layout shifts | Medium | Medium | Use Playwright visual comparison across browsers |

---

## Appendix: File Inventory

| File | Role | Scroll Risk |
|------|------|-------------|
| `src/ai_company/dashboard/app.py` | FastAPI app, routes, middleware | Low |
| `src/ai_company/dashboard/api.py` | REST API endpoints | Low |
| `src/ai_company/dashboard/ws.py` | WebSocket handler + broadcast | Medium — message frequency |
| `src/ai_company/dashboard/static/js/app.js` | Alpine.js app + WS client | **HIGH** — polling + state mutation |
| `src/ai_company/dashboard/static/js/charts.js` | Chart.js integration | **HIGH** — destroy/recreate cycle |
| `src/ai_company/dashboard/static/css/style.css` | Styles | Low — `scroll-behavior: smooth` |
| `src/ai_company/dashboard/templates/base.html` | Base layout | Low — sticky header only |
| `src/ai_company/dashboard/templates/index.html` | Dashboard home | Medium — KPI cards + table |
| `src/ai_company/dashboard/templates/tasks.html` | Task kanban | Medium — drag/drop |
| `src/ai_company/dashboard/templates/agents.html` | Agent grid + modal | Low |
| `src/ai_company/dashboard/templates/escalations.html` | Approvals/escalations | Low |
