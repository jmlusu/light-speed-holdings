# UX → User Satisfaction: Detailed Task Breakdown

## Goal
Transform the CEO Dashboard from "buggy and unstable" (user-reported) into a polished, reliable executive tool that users trust and enjoy using.

## Current Pain Points (from `knowledge/technology/dashboard-known-issues.md`)

| ID | Issue | Severity | User Impact |
|----|-------|----------|-------------|
| DASH-001 | Scroll position lost on auto-refresh | Critical | Users lose context every 10s |
| DASH-002 | WebSocket reconnects cause UI flicker | High | "Live" indicator flickers green/red |
| DASH-003 | No loading indicators during data fetch | High | Appears unresponsive |
| DASH-004 | Failed API calls show no error | High | Users unaware of failures |
| DASH-005 | Toast notifications overlap | Medium | Important alerts buried |
| DASH-006 | Kanban drag interrupted by refresh | High | Workflow disruption |
| DASH-007 | Charts flicker on data update | Medium | Visual disruption |
| DASH-008 | No manual refresh per section | Medium | Forced full page refresh |

---

## Phase 1: Critical Fixes (Week 1-2) - "Stop the Bleeding"

### Task UX-001: Fix Scroll Position Preservation (DASH-001)
**Owner**: `frontend-engineer` | **Skill**: `bug-hunter` | **Effort**: 2 days

**Root Cause**: Alpine.js reactivity triggers full DOM re-render on data updates (`app.js:946-1014`)

**Current Implementation** (partial fix exists in `app.js:309-377`):
```javascript
saveScrollPosition() {
  this._savedScroll = window.scrollY;
}
restoreScrollPosition() {
  if (this._savedScroll !== null) {
    this._pendingRestoreRaf = requestAnimationFrame(() => {
      window.scrollTo(0, this._savedScroll);
      this._savedScroll = null;
    });
  }
}
```

**Gaps to Fix**:
- [ ] Save position **before** `Promise.all` in `loadDashboard()` (currently saves after)
- [ ] Restore **after** DOM updates complete (use `nextTick` or `requestAnimationFrame`)
- [ ] Handle edge case: user manually scrolling during refresh → don't fight them (`_onScroll` listener exists but needs tuning)
- [ ] Test with: KPI cards, Task table, Kanban board, Charts, Org chart

**Verification**:
- E2E test: Scroll to bottom, wait for auto-refresh, verify position retained
- Manual test: Drag Kanban card during refresh → card doesn't jump

---

### Task UX-002: Add Loading State Management (DASH-003)
**Owner**: `frontend-engineer` | **Skill**: `bug-hunter` | **Effort**: 2 days

**Current State**: `isLoading: true` only on initial load (`app.js:18`)

**Required Loading States**:
```javascript
loading: {
  dashboard: false,    // Full dashboard refresh
  tasks: false,        // Task list/table
  agents: false,       // Agent list
  kpis: false,         // KPI cards/charts
  costs: false,        // Cost widgets
  approvals: false,    // Approval queue
  escalations: false,  // Escalation list
  orgChart: false,     // Org chart render
  reports: false,      // Reports view
  taskFlow: false      // Task flow view
}
```

**UI Components Needed**:
- **KPI Cards**: Subtle pulse animation overlay (see `dashboard-known-issues.md:203-223`)
- **Task Table**: Skeleton loading rows (shimmer effect)
- **Charts**: Circular spinner centered on canvas
- **Agent List**: Skeleton cards
- **Kanban**: Column-level skeleton during drag

**Implementation**:
- [ ] Add `loading` object to Alpine.js state
- [ ] Set `loading.section = true` before fetch, `false` after (success or error)
- [ ] Add skeleton HTML templates in `base.html` or component partials
- [ ] Disable interactive elements (buttons, drag) while `loading.section === true`

---

### Task UX-003: Implement Error Feedback UI (DASH-004)
**Owner**: `frontend-engineer` | **Skill**: `bug-hunter` | **Effort**: 2 days

**Current State**: `fetchJSON()` catches errors but only logs to console and sets `apiStatus` banner (`app.js:693-739`)

**Required Error UI** (per `dashboard-known-issues.md:103-136`):
- **Connection Error**: Red banner, fixed top, auto-dismiss on reconnect
- **API Error**: Yellow banner inline, manual dismiss + retry button
- **Rate Limit**: Orange banner, auto-dismiss after 60s
- **Data Stale**: Blue info banner, subtle, manual dismiss

**Implementation**:
- [ ] Extend `errors` object in Alpine.js: `errors: { dashboard: null, tasks: null, agents: null, kpis: null, ... }`
- [ ] Modify `fetchJSON()` to populate `errors[section]` on failure, clear on success
- [ ] Add error banner components to each section in templates
- [ ] Add "Retry" button that calls section-specific reload function
- [ ] Add "Last updated" timestamp per section

---

### Task UX-004: WebSocket Connection Resilience (DASH-002)
**Owner**: `dashboard-owner` | **Skill**: `bug-hunter` + `performance-optimizer` | **Effort**: 3 days

**Current State** (`app.js:37-43`, `ws.py:18-100`):
- Basic reconnection: 3s fixed interval, max 8 attempts
- No exponential backoff
- No connection quality indicator
- Silent failures

**Required Improvements**:
- [ ] Exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s, 30s, 30s (cap at 30s)
- [ ] Jitter: `delay * (0.5 + Math.random())` to prevent thundering herd
- [ ] Connection quality states: `connected` | `reconnecting` | `degraded` | `offline`
- [ ] Visual indicator in header (see `dashboard-known-issues.md:263-294`)
- [ ] Manual "Reconnect" button when offline
- [ ] WebSocket ping/pong every 15s to detect stale connections
- [ ] Fallback to polling if WebSocket fails 3x consecutively

---

## Phase 2: Polish & Delight (Week 3-4) - "Make it Feel Good"

### Task UX-005: Fix Toast Notification Spam (DASH-005)
**Owner**: `frontend-engineer` | **Effort**: 1 day

**Current State**: Single toast, no queue (`app.js:14-15`)

**Required**:
- [ ] Toast queue (max 3 visible)
- [ ] Auto-stack with slide animation
- [ ] Persist critical toasts until dismissed
- [ ] Group similar toasts: "3 new tasks assigned" vs 3 separate toasts

---

### Task UX-006: Pause Polling During Drag Operations (DASH-006)
**Owner**: `frontend-engineer` | **Effort**: 1 day

**Root Cause**: Auto-refresh (15s) triggers re-render during Kanban drag

**Solution**:
```javascript
// In kanban-board.js or app.js
onDragStart() {
  this._pollPaused = true;
  clearTimeout(this._pollTimer);
}
onDragEnd() {
  this._pollPaused = false;
  this.schedulePoll(); // Resume with fresh interval
}
```

---

### Task UX-007: Eliminate Chart Flicker (DASH-007)
**Owner**: `frontend-engineer` | **Skill**: `performance-optimizer` | **Effort**: 2 days

**Current State**: Charts redraw on every KPI update (`app.js:1009-1013` schedules `scheduleKPICharts()`)

**Solution**:
- [ ] Coalesce chart updates: single `requestAnimationFrame` per frame (already partially in `app.js:46-48`)
- [ ] Use Chart.js `update('none')` for animations off, or `update('resize')` for smooth transitions
- [ ] Only update datasets that actually changed (diff previous vs new)
- [ ] Add `prefers-reduced-motion` respect (already in CSS per STATUS.md)

---

### Task UX-008: Add Manual Refresh Per Section (DASH-008)
**Owner**: `frontend-engineer` | **Effort**: 1 day

**UI**: Refresh icon button in each section header
**Behavior**: Calls section-specific load function (e.g., `loadDashboard()`, `loadTasksPage()`, `loadAgents()`)
**Visual**: Spinner on button during fetch, toast on completion

---

## Phase 3: Advanced UX (Week 5-6) - "Executive Grade"

### Task UX-009: Keyboard Shortcuts & Command Palette
**Owner**: `frontend-engineer` | **Effort**: 2 days
- `Cmd+K` → Command palette (search tasks, agents, navigate)
- `Cmd+R` → Refresh current section
- `Esc` → Close modals/dropdowns
- Arrow keys for Kanban navigation

### Task UX-010: Responsive Design & Mobile Usability
**Owner**: `frontend-engineer` | **Effort**: 3 days
- Dashboard usable on tablet (horizontal scroll for tables)
- Touch-friendly Kanban drag
- Collapsible sidebar on mobile
- Test viewports: 375px, 768px, 1024px, 1440px

### Task UX-011: Accessibility (WCAG 2.1 AA)
**Owner**: `frontend-engineer` | **Effort**: 2 days
- Semantic HTML landmarks
- ARIA labels for interactive elements
- Focus management for modals
- Color contrast ratios
- Screen reader announcements for live updates

### Task UX-012: User Feedback Collection
**Owner**: `ux-research-lead` + `frontend-engineer` | **Effort**: 2 days
- Implement feedback modal (see `dashboard-known-issues.md:298-380`)
- `/api/feedback` endpoint (see `dashboard-known-issues.md:384-414`)
- Auto-collect context: URL, WS status, recent errors, timestamp

---

## Success Metrics & KPIs

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Scroll position retention | 0% | 100% | E2E test + user testing |
| Error visibility (UI) | 0% | 100% | Analytics on banner shows |
| Connection uptime | ~95% | 99%+ | WS logs |
| Toast overlap incidents | Frequent | 0 | User reports |
| Chart flicker reports | Frequent | 0 | User reports |
| Task completion rate | Baseline | +20% | Analytics |
| User satisfaction (NPS) | Low | >50 | Quarterly survey |
| Support tickets (dashboard) | High | <5/month | Ticket tracking |

---

## Dependencies & Blockers

| Task | Depends On | Blocks |
|------|------------|--------|
| UX-001 | None | UX-006, UX-007 |
| UX-002 | None | UX-003 |
| UX-003 | UX-002 | None |
| UX-004 | `ws.py` changes | UX-012 (connection quality) |
| UX-005 | None | None |
| UX-006 | UX-001 | None |
| UX-007 | UX-001 | None |
| UX-008 | UX-002, UX-003 | None |
| UX-009-012 | Phase 1 complete | None |

---

## Definition of Done per Task

- [ ] Code implemented and reviewed (5-axis review)
- [ ] Unit tests added/updated
- [ ] E2E test added (Playwright)
- [ ] Manual verification on staging
- [ ] Documentation updated (`dashboard-known-issues.md` status column)
- [ ] Deployed to staging, verified by `ux-research-lead`