# Dashboard Known Issues & Support Recommendations

**Document Type:** Support Knowledge Base  
**Last Updated:** 2026-07-22  
**Severity:** High (User-Reported Instability)  
**Affected Component:** CEO Dashboard (FastAPI + Alpine.js + WebSocket)

---

## Executive Summary

Users have reported the CEO Dashboard as "buggy and unstable" with specific complaints about auto-scrolling issues. This document compiles known issues, identifies critical pain points, and provides actionable recommendations for improving user experience and stability.

---

## 1. Compiled User Complaints

### 1.1 Auto-Scrolling Issues (Primary Complaint)

| Issue | Description | Impact |
|-------|-------------|--------|
| **Scroll position loss** | Dashboard scrolls to top when data auto-refreshes (every 10 seconds) | Users lose context when reviewing data |
| **Kanban board jumping** | Task columns jump during drag-and-drop operations | Interrupts workflow, causes misplaced tasks |
| **Table re-render** | Recent Tasks table scrolls to top on update | Users lose place in task lists |
| **Chart redraw flicker** | Charts briefly disappear and re-render on data update | Visual disruption, appears unstable |

### 1.2 Connection Stability Issues

| Issue | Description | Impact |
|-------|-------------|--------|
| **WebSocket disconnects** | Connection drops and reconnects every few minutes | "Live" indicator flickers between green/red |
| **Silent failures** | API fetch failures log only to browser console | Users see no feedback when data fails to load |
| **Reconnect loops** | Multiple rapid reconnect attempts cause UI instability | Dashboard appears to "freeze" briefly |

### 1.3 Data Loading Issues

| Issue | Description | Impact |
|-------|-------------|--------|
| **No loading indicators** | Users don't know when data is being fetched | Appears unresponsive during loading |
| **Stale data display** | Dashboard shows old data without indication | Users make decisions based on outdated information |
| **Missing error feedback** | Failed API calls show no user-facing error | Users assume data is current when it's not |

### 1.4 UI/UX Issues

| Issue | Description | Impact |
|-------|-------------|--------|
| **Toast notification spam** | Multiple rapid toast notifications overlap | Important alerts get buried |
| **Modal interruption** | Assign Task modal appears during auto-refresh | Disrupts user workflow |
| **No manual refresh** | Users cannot manually refresh specific sections | Forced to refresh entire page |

---

## 2. Critical Pain Points Identified

### Priority 1: Scroll Position Preservation
- **Root Cause:** Alpine.js reactivity triggers full DOM re-render on data updates
- **User Impact:** HIGH - Directly affects daily workflow
- **Frequency:** Every 10 seconds (polling interval) + WebSocket broadcasts

### Priority 2: Error Visibility
- **Root Cause:** `fetchJSON()` in `app.js` catches errors but only logs to console
- **User Impact:** HIGH - Users unaware of failures
- **Example Code:**
  ```javascript
  async fetchJSON(url, opts = {}) {
    try {
      const res = await fetch(url, opts);
      if (!res.ok) throw new Error(res.statusText);
      return await res.json();
    } catch (e) {
      console.warn(`[API] ${url} failed:`, e.message);  // Silent failure
      return null;
    }
  }
  ```

### Priority 3: Loading State Management
- **Root Cause:** No loading state tracking in Alpine.js data model
- **User Impact:** MEDIUM - Users cannot distinguish "loading" from "no data"
- **Missing State Variables:**
  ```javascript
  loading: {
    dashboard: false,
    tasks: false,
    agents: false,
    kpis: false,
  }
  ```

### Priority 4: Connection Resilience
- **Root Cause:** Basic reconnection logic without exponential backoff
- **User Impact:** MEDIUM - Connection indicators flicker
- **Current Implementation:**
  ```javascript
  ws.onclose = () => {
    this.wsConnected = false;
    this.wsReconnectTimer = setTimeout(() => this.connectWebSocket(), 3000);
  };
  ```

---

## 3. Recommended Error Messages & Feedback Mechanisms

### 3.1 User-Facing Error Messages

| Error Type | Message | Severity | Action |
|------------|---------|----------|--------|
| **Connection Lost** | "Connection to dashboard server lost. Attempting to reconnect..." | Warning | Auto-retry with countdown |
| **API Failure** | "Unable to load [section]. Please try again." | Error | Retry button |
| **Rate Limited** | "Too many requests. Please wait a moment before retrying." | Warning | Auto-retry after 60s |
| **Data Stale** | "Data may be outdated. Last updated: [timestamp]" | Info | Refresh button |
| **WebSocket Error** | "Real-time updates temporarily unavailable. Polling for updates." | Info | Auto-fallback to polling |

### 3.2 Error Message Template

```html
<!-- Error Banner Component -->
<div x-show="errors.dashboard" 
     class="bg-red-950/50 border border-red-800 rounded-lg p-4 mb-4">
  <div class="flex items-center gap-3">
    <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/>
    </svg>
    <div class="flex-1">
      <p class="text-sm font-medium text-red-200" x-text="errors.dashboard"></p>
      <p class="text-xs text-red-300/70 mt-1">Last successful update: <span x-text="lastUpdated.dashboard"></span></p>
    </div>
    <button @click="refreshSection('dashboard')" 
            class="bg-red-800 hover:bg-red-700 text-white px-3 py-1.5 rounded text-xs font-medium transition-colors">
      Retry
    </button>
  </div>
</div>
```

### 3.3 Feedback Mechanism Design

```javascript
// Add to Alpine.js dashboard() function
feedback: {
  show: false,
  type: 'bug',  // bug, feature, general
  message: '',
  email: '',
  submitting: false,
  submitted: false,
},

async submitFeedback() {
  this.feedback.submitting = true;
  
  // Collect context automatically
  const context = {
    type: this.feedback.type,
    message: this.feedback.message,
    email: this.feedback.email,
    url: window.location.href,
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    wsConnected: this.wsConnected,
    lastErrors: this.recentErrors,
  };
  
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(context),
    });
    this.feedback.submitted = true;
    setTimeout(() => {
      this.feedback.show = false;
      this.feedback.submitted = false;
      this.feedback.message = '';
    }, 3000);
  } catch (e) {
    // Store locally if server unavailable
    const stored = JSON.parse(localStorage.getItem('pendingFeedback') || '[]');
    stored.push(context);
    localStorage.setItem('pendingFeedback', JSON.stringify(stored));
    this.feedback.submitted = true;
  }
  
  this.feedback.submitting = false;
}
```

---

## 4. Communication Recommendations

### 4.1 Loading Spinners

| Section | Spinner Type | Location |
|---------|--------------|----------|
| **KPI Cards** | Subtle pulse animation | Overlay on card |
| **Task Table** | Skeleton loading rows | Replace table rows |
| **Charts** | Circular spinner | Center of canvas |
| **Agent List** | Skeleton cards | Replace agent cards |

**Implementation Example:**
```html
<!-- KPI Card with Loading State -->
<div class="kpi-card bg-surface-900/80 rounded-xl border border-surface-700/50 p-4 relative">
  <!-- Loading Overlay -->
  <div x-show="loading.dashboard" class="absolute inset-0 bg-surface-900/80 rounded-xl flex items-center justify-center z-10">
    <div class="animate-spin w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full"></div>
  </div>
  
  <!-- Card Content -->
  <div class="flex items-center gap-2 mb-2">
    <div class="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center">
      <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
    </div>
    <span class="text-xs text-surface-500">Pending</span>
  </div>
  <div class="text-3xl font-bold text-amber-400" x-text="kpis.pending_tasks">0</div>
</div>
```

### 4.2 Error Banners

| Banner Type | Style | Dismissal |
|-------------|-------|-----------|
| **Connection Error** | Red banner, fixed top | Auto-dismiss on reconnect |
| **API Error** | Yellow banner, inline | Manual dismiss + retry |
| **Rate Limit** | Orange banner, temporary | Auto-dismiss after 60s |
| **Data Stale** | Blue info banner, subtle | Manual dismiss |

### 4.3 Retry Buttons

| Location | Button Style | Behavior |
|----------|--------------|----------|
| **Section Header** | "Refresh" icon button | Reloads specific section |
| **Error Banner** | "Retry" button | Attempts failed request again |
| **Empty State** | "Load Data" button | Fetches initial data |

**Retry Logic:**
```javascript
async fetchWithRetry(url, opts = {}, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url, opts);
      if (res.status === 429) {
        // Rate limited - wait longer
        await new Promise(r => setTimeout(r, 60000));
        continue;
      }
      if (!res.ok) throw new Error(res.statusText);
      return await res.json();
    } catch (e) {
      if (i === retries - 1) throw e;
      await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
    }
  }
}
```

### 4.4 Connection Status Indicator

**Current Implementation:** Small green/red dot in header  
**Recommended Enhancement:**

```html
<!-- Enhanced Connection Status -->
<div class="flex items-center gap-2">
  <template x-if="wsConnected">
    <div class="flex items-center gap-2 text-emerald-400">
      <span class="relative flex h-2 w-2">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
      </span>
      <span class="text-xs font-medium">Live</span>
    </div>
  </template>
  <template x-if="!wsConnected && !wsReconnecting">
    <div class="flex items-center gap-2 text-amber-400">
      <span class="w-2 h-2 rounded-full bg-amber-500"></span>
      <span class="text-xs font-medium">Offline</span>
      <button @click="connectWebSocket()" class="text-xs underline hover:text-amber-300">Reconnect</button>
    </div>
  </template>
  <template x-if="!wsConnected && wsReconnecting">
    <div class="flex items-center gap-2 text-blue-400">
      <div class="animate-spin w-3 h-3 border border-blue-400 border-t-transparent rounded-full"></div>
      <span class="text-xs font-medium">Reconnecting...</span>
    </div>
  </template>
</div>
```

---

## 5. Feedback Collection Mechanism

### 5.1 Feedback Button Placement

```html
<!-- Footer Feedback Button -->
<footer class="border-t border-surface-800 mt-8 py-4 px-6">
  <div class="flex items-center justify-between">
    <p class="text-xs text-surface-600">Light Speed Holdings — AI Company Builder v0.1.0</p>
    <button @click="feedback.show = true" 
            class="flex items-center gap-1.5 text-xs text-surface-500 hover:text-surface-300 transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      Report Issue
    </button>
  </div>
</footer>

<!-- Feedback Modal -->
<div x-show="feedback.show" x-transition class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
  <div class="bg-surface-900 rounded-2xl shadow-2xl border border-surface-700/50 w-full max-w-md p-6">
    <div x-show="!feedback.submitted">
      <h3 class="text-lg font-semibold text-surface-100 mb-4">Report an Issue</h3>
      
      <div class="space-y-4">
        <div>
          <label class="block text-xs text-surface-500 mb-1.5">Issue Type</label>
          <select x-model="feedback.type" class="w-full bg-surface-800 border border-surface-700 rounded-lg px-3 py-2 text-sm text-surface-200">
            <option value="bug">Bug Report</option>
            <option value="feature">Feature Request</option>
            <option value="general">General Feedback</option>
          </select>
        </div>
        
        <div>
          <label class="block text-xs text-surface-500 mb-1.5">Description</label>
          <textarea x-model="feedback.message" rows="4" placeholder="What happened? What did you expect?"
                    class="w-full bg-surface-800 border border-surface-700 rounded-lg px-3 py-2 text-sm text-surface-200 placeholder-surface-500 resize-none"></textarea>
        </div>
        
        <div>
          <label class="block text-xs text-surface-500 mb-1.5">Email (optional)</label>
          <input type="email" x-model="feedback.email" placeholder="For follow-up"
                 class="w-full bg-surface-800 border border-surface-700 rounded-lg px-3 py-2 text-sm text-surface-200 placeholder-surface-500">
        </div>
        
        <div class="text-xs text-surface-600 bg-surface-800/50 rounded-lg p-3">
          <p class="font-medium text-surface-400 mb-1">Automatically collected:</p>
          <ul class="space-y-1">
            <li>• Page URL and current section</li>
            <li>• Browser and device information</li>
            <li>• Connection status and recent errors</li>
            <li>• Timestamp of issue</li>
          </ul>
        </div>
      </div>
      
      <div class="flex gap-3 mt-6">
        <button @click="feedback.show = false" class="flex-1 bg-surface-800 text-surface-300 px-4 py-2 rounded-lg text-sm font-medium hover:bg-surface-700 transition-colors">
          Cancel
        </button>
        <button @click="submitFeedback()" :disabled="feedback.submitting || !feedback.message"
                class="flex-1 bg-brand-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-brand-500 transition-colors disabled:opacity-50">
          <span x-show="!feedback.submitting">Submit</span>
          <span x-show="feedback.submitting">Submitting...</span>
        </button>
      </div>
    </div>
    
    <div x-show="feedback.submitted" class="text-center py-4">
      <div class="w-12 h-12 bg-emerald-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
      </div>
      <p class="text-surface-200 font-medium">Thank you for your feedback!</p>
      <p class="text-sm text-surface-500 mt-1">We'll review your report and follow up if needed.</p>
    </div>
  </div>
</div>
```

### 5.2 Feedback Storage Endpoint

```python
# Add to src/ai_company/dashboard/api.py

from pydantic import BaseModel

class FeedbackSubmission(BaseModel):
    type: str  # bug, feature, general
    message: str
    email: str | None = None
    url: str
    timestamp: str
    userAgent: str
    wsConnected: bool
    lastErrors: list[dict] = []

@router.post("/api/feedback")
async def submit_feedback(feedback: FeedbackSubmission) -> dict:
    """Store user feedback for review."""
    # Store to file or database
    feedback_dir = Path("dashboard/feedback")
    feedback_dir.mkdir(exist_ok=True)
    
    feedback_file = feedback_dir / f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(feedback_file, "w") as f:
        json.dump(feedback.model_dump(), f, indent=2)
    
    logger.info(f"Feedback received: {feedback.type} - {feedback.message[:50]}...")
    
    return {"status": "success", "id": feedback_file.stem}
```

---

## 6. Known Issues Documentation

### 6.1 Issue Registry

| ID | Issue | Status | Workaround | Fix ETA |
|----|-------|--------|------------|---------|
| DASH-001 | Scroll position lost on auto-refresh | Open | Manually scroll back | Sprint 4 |
| DASH-002 | WebSocket reconnects cause UI flicker | Open | None - visual only | Sprint 4 |
| DASH-003 | No loading indicators during data fetch | Open | Wait for data to appear | Sprint 4 |
| DASH-004 | Failed API calls show no error | Open | Check browser console | Sprint 4 |
| DASH-005 | Toast notifications overlap | Open | Wait for auto-dismiss | Sprint 4 |
| DASH-006 | Kanban drag interrupted by refresh | Open | Complete drag quickly | Sprint 4 |
| DASH-007 | Charts flicker on data update | Open | None - visual only | Sprint 4 |
| DASH-008 | No manual refresh per section | Open | Refresh entire page | Sprint 4 |

### 6.2 User Workarounds

| Issue | Workaround |
|-------|------------|
| **Auto-scroll** | Avoid scrolling while data is updating (every 10 seconds) |
| **Connection drops** | Click "Reconnect" button in header when offline |
| **Missing data** | Refresh entire page (F5 or Ctrl+R) |
| **Stale data** | Wait for next auto-refresh cycle (10 seconds) |
| **Modal interruption** | Complete actions quickly before next refresh |

### 6.3 Related Documentation

- [CEO Dashboard Architecture Analysis](../../docs/CEO_DASHBOARD_ARCHITECTURE_ANALYSIS.md)
- [Executive Dashboard V1 Strategic Plan](../../docs/EXECUTIVE_DASHBOARD_V1_STRATEGIC_PLAN.md)
- [System Architecture](../../docs/ARCHITECTURE.md)

---

## 7. Immediate Recommendations

### For Support Team

1. **Acknowledge the issue** - Auto-scrolling is a known bug, not user error
2. **Share workarounds** - Provide the table in Section 6.2 to affected users
3. **Collect examples** - Use feedback mechanism to gather specific reproduction steps
4. **Set expectations** - Fix is planned for Sprint 4 (Quality & Completeness)

### For Development Team

1. **Priority 1:** Implement scroll position preservation
   - Save scroll position before data update
   - Restore after DOM re-render
   - Use `requestAnimationFrame` for smooth restoration

2. **Priority 2:** Add loading state management
   - Add `loading` state object to Alpine.js
   - Show spinners during fetch operations
   - Disable interactive elements while loading

3. **Priority 3:** Implement error feedback UI
   - Add error state object to Alpine.js
   - Show error banners with retry buttons
   - Log errors to feedback system

4. **Priority 4:** Improve connection resilience
   - Implement exponential backoff for reconnection
   - Add connection quality indicator
   - Provide manual reconnect option

---

## 8. Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| **Scroll position retention** | 0% | 100% | User testing |
| **Error visibility** | 0% (console only) | 100% (UI shown) | Analytics |
| **Connection uptime** | ~95% | 99%+ | WebSocket logs |
| **User satisfaction** | Low (reported buggy) | High | Feedback score |
| **Support tickets** | High | Low | Ticket volume |

---

## 9. Appendix: Technical Root Cause Analysis

### Auto-Scroll Root Cause

The auto-scroll issue stems from Alpine.js reactivity causing full DOM re-render when data updates:

```javascript
// Current: Full data replacement triggers re-render
async loadDashboard() {
  const [kpis, depts, tasks] = await Promise.all([...]);
  if (kpis) Object.assign(this.kpis, kpis);  // Triggers re-render
  if (depts) this.departments = depts;        // Triggers re-render
  if (tasks) this.tasks = tasks;              // Triggers re-render
}
```

**Solution:** Use targeted updates and preserve scroll position:

```javascript
async loadDashboard() {
  // Save scroll position
  const scrollPos = window.scrollY;
  
  const [kpis, depts, tasks] = await Promise.all([...]);
  
  // Update data (triggers re-render)
  if (kpis) Object.assign(this.kpis, kpis);
  if (depts) this.departments = depts;
  if (tasks) this.tasks = tasks;
  
  // Restore scroll position after DOM update
  requestAnimationFrame(() => {
    window.scrollTo(0, scrollPos);
  });
}
```

### Silent Failure Root Cause

The `fetchJSON()` function catches all errors and only logs to console:

```javascript
async fetchJSON(url, opts = {}) {
  try {
    // ... fetch logic
  } catch (e) {
    console.warn(`[API] ${url} failed:`, e.message);  // Silent
    return null;  // User sees nothing
  }
}
```

**Solution:** Track errors and expose to UI:

```javascript
errors: {
  dashboard: null,
  tasks: null,
  agents: null,
},

async fetchJSON(url, opts = {}) {
  const section = this.getSectionFromUrl(url);
  try {
    const res = await fetch(url, opts);
    if (!res.ok) throw new Error(res.statusText);
    this.errors[section] = null;  // Clear error on success
    return await res.json();
  } catch (e) {
    console.warn(`[API] ${url} failed:`, e.message);
    this.errors[section] = `Failed to load data: ${e.message}`;
    return null;
  }
}
```

---

**Document Owner:** Support Team  
**Next Review:** After Sprint 4 completion  
**Distribution:** Support, Engineering, Product
