/* ═══════════════════════════════════════════════════════════════
   Light Speed Holdings — CEO Dashboard
   Alpine.js application + WebSocket connection
   ═══════════════════════════════════════════════════════════════ */

function dashboard() {
  return {
    // ── Connection state ─────────────────────────────────────
    wsConnected: false,
    wsClients: 0,
    ws: null,

    // ── Toast notifications ──────────────────────────────────
    toast: { show: false, type: 'info', title: '', message: '' },
    toastTimer: null,

    // ── Loading state (FIX: prevents layout jump on initial load)
    isLoading: true,

    // ── Scroll management (FIX: auto-scroll prevention) ──────
    // _scrollLock is bound to body.scroll-locked in base.html. It stays
    // false by design: we prevent scroll jumps with save/restore guards
    // below instead of locking the page (overflow:hidden can itself reset
    // scroll position when content height changes).
    _scrollLock: false,
    _savedScroll: null,
    _pendingRestoreRaf: null,
    _scrollGuardActive: false,

    // ── Polling state ─────────────────────────────────────────
    _pollTimer: null,
    _pollInFlight: false,
    _pollQueued: false,
    _pollIntervalMs: 15000,

    // ── WebSocket hardening state ─────────────────────────────
    _wsDisposed: false,
    _wsReconnectAttempts: 0,
    _wsMaxReconnectAttempts: 8,
    _wsReconnectTimer: null,
    _wsReconnectScheduled: false,
    _wsKeepaliveTimer: null,
    _wsProbeTimer: null,

    // ── Chart update coalescing (FIX: avoid double redraw per frame) ──
    _kpiChartsRaf: null,
    _kpiChartsPending: false,
    _latestKpis: null,
    _latestDepartments: null,

    // ── API error surfacing (FIX: silent failures) ────────────
    apiStatus: { show: false, message: '' },
    _apiErrorKey: '',

    // ── ADR-013: Browser session token ───────────────────────
    _sessionToken: null,
    _tokenRefreshTimer: null,

    // ── PWA / Offline sync (Issue #41) ──────────────────────
    swInstallable: false,
    swUpdateAvailable: false,
    offlineQueueCount: 0,
    syncStatus: '',

    // ── Data ─────────────────────────────────────────────────
    kpis: {
      pending_tasks: 0,
      in_progress_tasks: 0,
      completed_tasks: 0,
      failed_tasks: 0,
      escalated_tasks: 0,
      pending_approvals: 0,
      open_escalations: 0,
      total_agents: 0,
      scheduled_tasks: 0,
      uptime_seconds: 0,
    },
    tasks: [],
    agents: [],
    approvals: [],
    escalations: [],
    departments: [],
    tiers: [],
    modelRoutes: [],
    orgChart: [],

    // ── CEO Hero Section ──────────────────────────────────────
    orgHealth: null,
    orgHealthLoading: true,
    heroVariant: 'B',
    heroExpanded: null,
    expandedComponent: null,
    _heroGauges: {},

    // ── Task assignment ──────────────────────────────────────
    newTask: { receiver_id: '', instruction: '', priority: 'medium', sender_id: 'human-ceo' },
    submitting: false,
    showAssignModal: false,

    // ── Drag and drop ────────────────────────────────────────
    draggedTask: null,

    // ── Task detail slide-out ────────────────────────────────
    selectedTask: null,
    taskDetailOpen: false,
    taskDecomposition: null,
    taskDecomposing: false,

    // ── KPIs page ────────────────────────────────────────────
    activeKPIDept: '',
    kpiDepartments: [],
    allKPIsList: [],
    liveKPIData: null,
    companyKPIs: [],
    companyKPISummary: null,

    // ── Costs page ───────────────────────────────────────────
    costPeriod: 'daily',
    costSummary: { total: 0, avgPerTask: 0, totalTasks: 0 },
    budgetPct: 0,
    costAlerts: [],
    agentCosts: [],

    // ── Approval edit (F3) ───────────────────────────────────
    editingApproval: null,   // id of approval being edited, or null
    editRisk: '',            // draft risk level
    editCost: '',            // draft cost estimate

    // ── Escalation notifications (F6) ────────────────────────
    escalationNotifications: [],  // real-time toast list from WS
    _escNotifId: 0,

    // ── Task pagination ──────────────────────────────────────
    taskPage: 1,
    taskPageSize: 20,
    taskTotal: 0,
    taskTotalPages: 0,
    taskCountsByStatus: {},

    // ── Task filters ─────────────────────────────────────────
    taskFilterPriority: '',
    taskFilterDepartment: '',
    taskFilterAgent: '',
    taskFilterStatus: '',

    // ── Task sort ────────────────────────────────────────────
    taskSortBy: 'created_at',
    taskSortDir: 'desc',

    // ── Agent search ─────────────────────────────────────────
    agentSearch: '',
    agentDeptFilter: '',
    selectedAgent: null,

    // ═══ INITIALIZATION ═══════════════════════════════════════

    async init() {
      // FIX: Scroll guard listener — if a scroll event fires while no data
      // update is in flight, the user is scrolling; cancel any pending
      // restore so we never fight the user (AC-SCROLL-03).
      window.addEventListener('scroll', () => this._onScroll(), { passive: true });

      // FIX: Pause polling + timers when the tab is hidden, resume on return.
      document.addEventListener('visibilitychange', () => this._onVisibilityChange());
      window.addEventListener('beforeunload', () => this.destroy());

      // PWA (Issue #41): listen for SW lifecycle and offline-sync events.
      window.addEventListener('sw-installable', (e) => { this.swInstallable = e.detail; });
      window.addEventListener('sw-update-available', () => { this.swUpdateAvailable = true; });
      window.addEventListener('sw-sync-complete', () => { this._refreshOfflineQueueCount(); });
      window.addEventListener('offline-sync-toast', (e) => {
        const d = e.detail || {};
        this.showToast(d.type || 'info', d.title || 'Sync', d.message || '');
      });
      window.addEventListener('online', () => { this._refreshOfflineQueueCount(); });
      window.addEventListener('offline', () => { this._refreshOfflineQueueCount(); });

      // ADR-013: Fetch bootstrap session token before any data loading.
      await this._fetchSessionToken();

      // Load hero variant preference from localStorage
      const savedVariant = localStorage.getItem('heroVariant');
      if (savedVariant && ['A', 'B', 'D'].includes(savedVariant)) {
        this.heroVariant = savedVariant;
      }

      this.connectWebSocket();

      // FIX: Load data, then reveal UI to prevent layout jump
      await this.loadPageData();
      this.isLoading = false;

      // Load org health data for the hero section
      this.loadOrgHealth();

      // FIX: Debounced polling — skip if a poll is already in-flight and
      // queue exactly one trailing poll instead of stacking parallel
      // fetches. Cadence adapts to WebSocket health (30s while WS is live,
      // 15s when WS is down) so polling acts as a fallback without
      // double-fetching alongside WS pushes.
      this._applyPollingCadence();
      this._startPolling();
    },

    /**
     * Cleanup on page unload — clears every timer/interval so nothing
     * keeps firing (and reconnecting) after the page is gone.
     */
    destroy() {
      this._wsDisposed = true;
      this._pausePolling();
      clearTimeout(this._wsReconnectTimer);
      clearTimeout(this._wsProbeTimer);
      clearInterval(this._wsKeepaliveTimer);
      clearTimeout(this._tokenRefreshTimer);
      this._cancelPendingRestore();
      if (this._kpiChartsRaf) cancelAnimationFrame(this._kpiChartsRaf);
      if (this.ws) {
        try {
          this.ws.onopen = null;
          this.ws.onmessage = null;
          this.ws.onclose = null;
          this.ws.onerror = null;
          this.ws.close();
        } catch (e) {
          // best-effort — socket may already be gone
        }
      }
    },

    _startPolling() {
      if (this._pollTimer) return;
      this._pollTimer = setInterval(() => this.debouncedPoll(), this._pollIntervalMs);
    },

    _pausePolling() {
      if (this._pollTimer) {
        clearInterval(this._pollTimer);
        this._pollTimer = null;
      }
    },

    _onVisibilityChange() {
      if (document.hidden) {
        this._pausePolling();
      } else {
        this._startPolling();
        // Refresh once when the tab becomes visible again — the data may
        // be stale from the hidden period. debouncedPoll dedupes so this
        // never double-fetches with an in-flight poll.
        this.debouncedPoll();
      }
    },

    _applyPollingCadence() {
      // WS up → 30s safety-net polling (WS pushes are the live path).
      // WS down → 15s polling (polling becomes the live path / fallback).
      this._pollIntervalMs = this.wsConnected ? 30000 : 15000;
      if (this._pollTimer) {
        clearInterval(this._pollTimer);
        this._pollTimer = setInterval(() => this.debouncedPoll(), this._pollIntervalMs);
      }
    },

    // ═══ SCROLL MANAGEMENT (FIX: auto-scroll prevention) ═════

    /**
     * Save the current scroll position before a data update that may cause
     * reflow. Called before loadPageData, WS updates, and any operation
     * that mutates visible state. Any previously scheduled restore is
     * cancelled so an older restore can never fight a newer update.
     */
    saveScrollPosition() {
      this._savedScroll = { x: window.scrollX, y: window.scrollY };
      this._scrollGuardActive = true;
      this._cancelPendingRestore();
    },

    /**
     * Restore scroll position after a data update completes.
     *
     * The restore runs on the next animation frame — after the browser has
     * finished layout. If the user scrolled after the update finished (a
     * scroll event fired while no update was in flight), the scroll guard
     * cancels this restore so we never override user-initiated scrolling.
     * Snap-back is exact (no 5px/200px magic-number window): the scroll
     * listener is what protects against fighting the user.
     */
    restoreScrollPosition() {
      const saved = this._savedScroll;
      if (!saved) return;
      this._savedScroll = null;
      this._scrollGuardActive = false;
      this._cancelPendingRestore();
      this._pendingRestoreRaf = requestAnimationFrame(() => {
        this._pendingRestoreRaf = null;
        const diff = Math.abs(window.scrollY - saved.y);
        if (diff > 1) {
          window.scrollTo(saved.x, saved.y);
        }
      });
    },

    _cancelPendingRestore() {
      if (this._pendingRestoreRaf) {
        cancelAnimationFrame(this._pendingRestoreRaf);
        this._pendingRestoreRaf = null;
      }
    },

    /**
     * Scroll-event guard. A scroll that fires while no update is in flight
     * means the user moved the page (or browser back/forward restoration) —
     * cancel any pending restore so we never yank the viewport back.
     * Scrolls that fire DURING an update (_scrollGuardActive) are the
     * browser's auto-scroll from DOM mutation; those are ignored here and
     * corrected by restoreScrollPosition().
     */
    _onScroll() {
      if (this._pendingRestoreRaf && !this._scrollGuardActive) {
        this._cancelPendingRestore();
      }
    },

    /**
     * Debounced poll: if a poll is already in-flight, queue exactly one
     * trailing poll (instead of stacking parallel fetches or silently
     * dropping the update). This prevents multiple concurrent Alpine
     * re-renders that cause layout thrashing.
     */
    async debouncedPoll() {
      if (this._pollInFlight) {
        this._pollQueued = true;
        return;
      }
      this._pollInFlight = true;
      this._pollQueued = false;
      try {
        this.saveScrollPosition();
        await this.loadPageData();
        this.restoreScrollPosition();
      } catch (e) {
        console.warn('[Poll] loadPageData failed:', e);
      } finally {
        this._pollInFlight = false;
        if (this._pollQueued && !document.hidden) {
          this._pollQueued = false;
          this.debouncedPoll();
        }
      }
    },

    // ═══ ADR-013: SESSION TOKEN ═════════════════════════════════

    /**
     * Fetch a short-lived, IP-bound session token from the bootstrap
     * endpoint (ADR-013). The token is held in memory only — nothing
     * persists across tabs or restarts. On 401/WS-1008, the client
     * transparently re-mints via this method.
     */
    async _fetchSessionToken() {
      try {
        const res = await fetch('/api/v1/bootstrap-token');
        if (res.ok) {
          const data = await res.json();
          this._sessionToken = data.token || null;
        }
      } catch (e) {
        console.warn('[Token] Bootstrap fetch failed:', e);
      }
    },

    /**
     * Re-mint the session token (called on 401 or WS close-1008).
     * Transparent to the caller — if the re-mint fails, the token
     * stays stale and the next request will also fail.
     */
    async _refreshSessionToken() {
      await this._fetchSessionToken();
    },

    // ═══ WEBSOCKET ═════════════════════════════════════════════

    /**
     * Establish the single dashboard WebSocket connection.
     *
     * FIX (hardening):
     * - Single connection: never opens a duplicate while one is OPEN or
     *   CONNECTING (prevents the double-connect reconnect loop).
     * - Reconnect uses exponential backoff with jitter, capped at 30s.
     * - After _wsMaxReconnectAttempts consecutive failures the rapid
     *   reconnect loop STOPS; a slow 60s recovery probe keeps the page
     *   able to pick the socket back up if the server restarts.
     * - Application-level keepalive ping keeps half-open sockets honest.
     * - Polling is the automatic fallback while WS is down (see
     *   _applyPollingCadence) — no second fetch loop is started.
     */
    connectWebSocket() {
      if (this._wsDisposed) return;
      // Single connection — never stack a second socket on a live one.
      if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
        return;
      }

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      let wsUrl = `${protocol}//${window.location.host}/ws/v1/dashboard`;
      // ADR-013: use the session token (fetched from /api/v1/bootstrap-token)
      // instead of the never-populated window.DASHBOARD_API_KEY.
      if (this._sessionToken) {
        wsUrl += `?api_key=${encodeURIComponent(this._sessionToken)}`;
      }

      let ws;
      try {
        ws = new WebSocket(wsUrl);
      } catch (e) {
        // Constructor failure is rare, but never throw into the UI.
        console.warn('[WS] Connection failed:', e);
        this.wsConnected = false;
        this._scheduleReconnect();
        return;
      }
      this.ws = ws;

      ws.onopen = () => {
        console.log('[WS] Connected');
        this.wsConnected = true;
        this._wsReconnectAttempts = 0;
        if (this._wsProbeTimer) {
          clearTimeout(this._wsProbeTimer);
          this._wsProbeTimer = null;
        }
        this._startKeepalive();
        this._applyPollingCadence();
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          this.handleWSMessage(msg);
        } catch (e) {
          console.warn('[WS] Failed to parse message:', e);
        }
      };

      ws.onclose = (event) => {
        console.warn('[WS] Disconnected');
        this.wsConnected = false;
        this._stopKeepalive();
        this._applyPollingCadence();
        // ADR-013: re-mint session token on close-1008 (auth failure)
        if (event && event.code === 1008) {
          this._refreshSessionToken().then(() => this._scheduleReconnect());
        } else {
          this._scheduleReconnect();
        }
        // FIX: Fallback to polling — refresh data immediately since WS
        // pushes were the live path. debouncedPoll dedupes, so this never
        // double-fetches with an in-flight poll.
        if (!document.hidden && !this._wsDisposed) {
          this.debouncedPoll();
        }
      };

      ws.onerror = () => {
        // onerror is always followed by onclose — only mark offline here;
        // reconnect is scheduled in onclose to avoid double scheduling.
        this.wsConnected = false;
      };
    },

    /**
     * Schedule the next reconnect attempt with exponential backoff.
     * Guarded by _wsReconnectScheduled so overlapping onclose/catch/error
     * paths can never schedule two timers (the double-reconnect loop).
     */
    _scheduleReconnect() {
      if (this._wsReconnectScheduled || this._wsDisposed) return;
      this._wsReconnectScheduled = true;
      clearTimeout(this._wsReconnectTimer);

      if (this._wsReconnectAttempts >= this._wsMaxReconnectAttempts) {
        // Stop the rapid reconnect loop. Keep a slow recovery probe so the
        // page can pick the socket back up after a long server outage.
        console.warn(
          `[WS] Reconnect attempts exhausted (${this._wsReconnectAttempts}); ` +
            'falling back to polling. Probing every 60s.'
        );
        this._wsReconnectScheduled = false;
        this._wsProbeTimer = setTimeout(() => {
          this._wsProbeTimer = null;
          this._wsReconnectAttempts = 0;
          this._wsReconnectScheduled = false;
          this.connectWebSocket();
        }, 60000);
        return;
      }

      const baseDelay = Math.min(30000, 1000 * Math.pow(2, this._wsReconnectAttempts));
      const jitter = Math.round(baseDelay * (0.5 + Math.random() * 0.5));
      this._wsReconnectTimer = setTimeout(() => {
        this._wsReconnectScheduled = false;
        this._wsReconnectAttempts += 1;
        this.connectWebSocket();
      }, jitter);
    },

    _startKeepalive() {
      this._stopKeepalive();
      this._wsKeepaliveTimer = setInterval(() => {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          try {
            this.ws.send(JSON.stringify({ type: 'ping' }));
          } catch (e) {
            console.warn('[WS] Keepalive send failed:', e);
          }
        }
      }, 25000);
    },

    _stopKeepalive() {
      if (this._wsKeepaliveTimer) {
        clearInterval(this._wsKeepaliveTimer);
        this._wsKeepaliveTimer = null;
      }
    },

    handleWSMessage(msg) {
      switch (msg.type) {
        case 'connected':
          this.wsClients = msg.active_clients || 0;
          break;

        case 'kpi_update':
          if (msg.payload) {
            // FIX: Save scroll position before WS-triggered update
            this.saveScrollPosition();

            // FIX (dedup): merge only fields that actually changed. Poll
            // responses and WS pushes carry the same KPI snapshot (the
            // /api/v1/dashboard endpoint broadcasts exactly what it returns),
            // so without a change check every poll cycle would trigger a
            // redundant second reactive mutation + chart redraw.
            const merged = this._mergeKPIPayload(msg.payload);

            // Live KPI snapshots (from /api/v1/kpis/live) carry a
            // `departments` key rather than task counters. Only apply them
            // on the KPIs page, and only when they actually change.
            if (msg.payload.departments && window.location.pathname === '/kpis') {
              this.liveKPIData = msg.payload;
              this.mergeLiveKPIValues();
              if (typeof initKPICharts === 'function') {
                initKPICharts(this.kpiDepartments, this.liveKPIData);
              }
            } else if (merged.chartRelevantChanged) {
              // FIX: Coalesce chart updates into one redraw per frame
              this.scheduleKPICharts();
            }

            this.restoreScrollPosition();
          }
          break;

        case 'alert':
          if (msg.payload) {
            const cat = msg.payload.category || 'info';
            this.showToast(
              cat === 'escalation' ? 'warning' : 'info',
              cat.charAt(0).toUpperCase() + cat.slice(1),
              msg.payload.reason || msg.payload.action || 'New alert received'
            );
          }
          break;

        case 'escalation':
          if (msg.payload) {
            // F6: push a dedicated non-blocking notification
            this._pushEscalationNotif(msg.payload);
            // Also refresh the escalation list so the table stays in sync
            if (window.location.pathname === '/escalations') {
              this.loadEscalations();
            }
          }
          break;

        case 'task_update':
          if (msg.payload) {
            // FIX: Save scroll before any task-list mutation so the
            // kanban/table re-render never jumps the viewport.
            this.saveScrollPosition();

            // Refresh the current paginated page — the task may have
            // moved pages due to status change, so surgical update is
            // unreliable with server-side pagination.
            if (window.location.pathname === '/tasks') {
              this.loadTasksPage().finally(() => this.restoreScrollPosition());
            } else {
              // Fallback for dashboard home: do a lightweight local update
              const updatedTask = msg.payload;
              const event = msg.event || 'updated';
              if (event === 'deleted') {
                this.tasks = this.tasks.filter(t => t.id !== updatedTask.id);
              } else {
                const idx = this.tasks.findIndex(t => t.id === updatedTask.id);
                if (idx >= 0) {
                  this.tasks[idx] = { ...this.tasks[idx], ...updatedTask };
                } else {
                  this.tasks.push(updatedTask);
                }
              }
              this.tasks = [...this.tasks];
              this.restoreScrollPosition();
            }
          }
          break;

        case 'pong':
          // Keepalive response
          break;

        default:
          // Unknown message type — ignore
          break;
      }
    },

    // ═══ DATA LOADING ═════════════════════════════════════════

    /**
     * Fetch + JSON with timeout and non-intrusive error surfacing.
     *
     * FIX (silent failures): a failed/timed-out request now sets a small
     * apiStatus banner (see base.html) instead of silently returning null.
     * - 429  → friendly "Too many requests" message (AC-ERR-05)
     * - 401  → session expired message (AC-ERR-05 E-05, no hard redirect)
     * - 5xx/network/timeout → "showing last known data" (AC-ERR-04)
     * The banner auto-clears on the next successful request, and errors are
     * deduped by message so Alpine only re-renders the banner once.
     */
    async fetchJSON(url, opts = {}) {
      const controller = new AbortController();
      const timeoutMs = opts.timeout || 15000;
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        // ADR-013: send the session token as X-API-Key on all REST calls.
        const headers = { ...(opts.headers || {}) };
        if (this._sessionToken && !headers['X-API-Key']) {
          headers['X-API-Key'] = this._sessionToken;
        }
        const res = await fetch(url, { ...opts, headers, signal: controller.signal });
        if (res.status === 429) {
          this._setApiError('Too many requests — retrying shortly');
          return null;
        }
        if (res.status === 401) {
          // ADR-013: transparently re-mint token and retry once.
          if (!opts._retried) {
            clearTimeout(timer);
            await this._refreshSessionToken();
            return this.fetchJSON(url, { ...opts, _retried: true });
          }
          this._setApiError('Session expired — refresh the page to reconnect');
          return null;
        }
        if (!res.ok) {
          this._setApiError(`Request failed (${res.status}) — showing last known data`);
          return null;
        }
        this._clearApiError();
        return await res.json();
      } catch (e) {
        if (e && e.name === 'AbortError') {
          this._setApiError('Request timed out — retrying automatically');
        } else {
          this._setApiError('Cannot reach server — showing last known data');
        }
        return null;
      } finally {
        clearTimeout(timer);
      }
    },

    _setApiError(message) {
      if (this._apiErrorKey === message) return; // dedupe — avoid banner churn
      this._apiErrorKey = message;
      this.apiStatus = { show: true, message };
    },

    _clearApiError() {
      if (this._apiErrorKey) {
        this._apiErrorKey = '';
        this.apiStatus = { show: false, message: '' };
      }
    },

    dismissApiError() {
      this._apiErrorKey = '';
      this.apiStatus = { show: false, message: '' };
    },

    // ── PWA / Offline sync helpers (Issue #41) ─────────────

    async _refreshOfflineQueueCount() {
      if (window.jarvisOfflineSync) {
        try {
          const actions = await window.jarvisOfflineSync.getQueuedActions();
          this.offlineQueueCount = actions.length;
          this.syncStatus = navigator.onLine ? 'online' : 'offline';
        } catch (_e) {
          // IndexedDB may not be available.
        }
      }
    },

    async installPWA() {
      if (window.jarvisInstall) {
        const outcome = await window.jarvisInstall();
        if (outcome === 'accepted') {
          this.showToast('success', 'Installed', 'J.A.R.V.I.S. added to home screen.');
        }
        this.swInstallable = false;
      }
    },

    async loadPageData() {
      const path = window.location.pathname;

      if (path === '/' || path === '') {
        await this.loadDashboard();
      } else if (path === '/agents') {
        await this.loadAgents();
      } else if (path === '/tasks') {
        await this.loadTasksPage();
        const agentsData = await this.fetchJSON('/api/v1/agents');
        if (agentsData) this.agents = agentsData;
      } else if (path === '/kpis') {
        await this.loadKPIs();
      } else if (path === '/costs') {
        await this.loadCosts();
      } else if (path === '/escalations') {
        // FIX: Load both in parallel
        const [approvalsData, escalationsData] = await Promise.all([
          this.fetchJSON('/api/v1/approvals'),
          this.fetchJSON('/api/v1/escalations'),
        ]);
        if (approvalsData) this.approvals = approvalsData;
        if (escalationsData) this.escalations = escalationsData;
      }
    },

    async loadDashboard() {
      const [kpis, depts, tasks, costs] = await Promise.all([
        this.fetchJSON('/api/v1/dashboard'),
        this.fetchJSON('/api/v1/departments'),
        this.fetchJSON('/api/v1/tasks'),
        this.fetchJSON('/api/v1/costs/summary'),  // F8: cost widget
      ]);

      // FIX: Batch all state updates into a single assignment window
      // to minimize Alpine.js reactive re-renders (was 3 separate re-renders,
      // now effectively 1 coordinated update). Additionally, only assign
      // when the payload actually changed — identical poll payloads no
      // longer trigger x-text/x-for re-evaluation (REG-05/REG-06).
      let needsChartUpdate = false;

      if (kpis) {
        const merged = this._mergeKPIPayload(kpis);
        if (merged.chartRelevantChanged) needsChartUpdate = true;
      }
      if (depts && JSON.stringify(depts) !== JSON.stringify(this.departments)) {
        this.departments = depts;
        needsChartUpdate = true;
      }
      if (tasks && JSON.stringify(tasks) !== JSON.stringify(this.tasks)) {
        this.tasks = tasks;
      }

      // FIX: Defer chart updates to next animation frame, coalescing any
      // updates already scheduled this frame into a single redraw.
      if (needsChartUpdate) {
        this.scheduleKPICharts();
      }
    },

    async loadAgents() {
      const data = await this.fetchJSON('/api/v1/agents');
      if (data) this.agents = data;
    },

    async loadTasks() {
      const data = await this.fetchJSON('/api/v1/tasks');
      if (data) this.tasks = data;
    },

    async loadTasksPage() {
      const params = new URLSearchParams({
        page: this.taskPage,
        page_size: this.taskPageSize,
        sort_by: this.taskSortBy,
        sort_dir: this.taskSortDir,
      });
      if (this.taskFilterPriority) params.set('priority', this.taskFilterPriority);
      if (this.taskFilterDepartment) params.set('department', this.taskFilterDepartment);
      if (this.taskFilterAgent) params.set('agent', this.taskFilterAgent);
      if (this.taskFilterStatus) params.set('status', this.taskFilterStatus);

      const data = await this.fetchJSON(`/api/v1/tasks/paginated?${params}`);
      if (data) {
        this.tasks = data.items;
        this.taskTotal = data.total;
        this.taskTotalPages = data.total_pages;
        this.taskCountsByStatus = data.counts_by_status;
      }
    },

    goToPage(page) {
      if (page < 1 || page > this.taskTotalPages) return;
      this.taskPage = page;
      this.loadTasksPage();
    },

    setTaskPageSize(size) {
      this.taskPageSize = size;
      this.taskPage = 1;
      this.loadTasksPage();
    },

    clearTaskFilters() {
      this.taskFilterPriority = '';
      this.taskFilterDepartment = '';
      this.taskFilterAgent = '';
      this.taskFilterStatus = '';
      this.taskPage = 1;
      this.loadTasksPage();
    },

    toggleTaskSort(field) {
      if (this.taskSortBy === field) {
        this.taskSortDir = this.taskSortDir === 'asc' ? 'desc' : 'asc';
      } else {
        this.taskSortBy = field;
        this.taskSortDir = 'desc';
      }
      this.taskPage = 1;
      this.loadTasksPage();
    },

    async loadApprovals() {
      const data = await this.fetchJSON('/api/v1/approvals');
      if (data) this.approvals = data;
    },

    async loadEscalations() {
      const data = await this.fetchJSON('/api/v1/escalations');
      if (data) this.escalations = data;
    },

    async loadKPIs() {
      const [depts, summary, company] = await Promise.all([
        this.fetchJSON('/api/v1/kpis'),
        this.fetchJSON('/api/v1/kpis/summary'),
        this.fetchJSON('/api/v1/company-kpis'),
      ]);

      // FIX: only assign state that actually changed — identical poll
      // payloads no longer churn the KPI cards/charts on the /kpis page.
      let needsKPIChartUpdate = false;

      if (depts) {
        const next = Object.entries(depts).map(([id, dept]) => ({
          id,
          name: dept.name || id,
          kpiCount: (dept.kpis || []).length,
          kpis: dept.kpis || [],
        }));
        if (JSON.stringify(next) !== JSON.stringify(this.kpiDepartments)) {
          this.kpiDepartments = next;
          needsKPIChartUpdate = true;

          if (this.kpiDepartments.length > 0 && !this.activeKPIDept) {
            this.activeKPIDept = this.kpiDepartments[0].id;
          }
        }
      }

      if (summary && JSON.stringify(summary) !== JSON.stringify(this.allKPIsList)) {
        this.allKPIsList = summary;
      }

      // Company-level KPIs (Sprint 3, item 2) — loaded before chart renders.
      if (company) {
        const nextKPIs = company.kpis || [];
        const nextSummary = company.summary || null;
        if (
          JSON.stringify(nextKPIs) !== JSON.stringify(this.companyKPIs) ||
          JSON.stringify(nextSummary) !== JSON.stringify(this.companyKPISummary)
        ) {
          this.companyKPIs = nextKPIs;
          this.companyKPISummary = nextSummary;
          needsKPIChartUpdate = true;
        }
      } else if (this.companyKPIs.length) {
        this.companyKPIs = [];
        this.companyKPISummary = null;
        needsKPIChartUpdate = true;
      }

      // Also load live KPI data
      const live = await this.fetchJSON('/api/v1/kpis/live');
      if (live && JSON.stringify(live) !== JSON.stringify(this.liveKPIData)) {
        this.liveKPIData = live;
        needsKPIChartUpdate = true;
      }

      // FIX: /api/v1/kpis returns definitions only (no current/status).
      // Overlay live values so department KPI cards show real data
      // instead of "undefined". Only re-merge when something changed —
      // mutating the same values would still re-render the cards.
      if (needsKPIChartUpdate) {
        this.mergeLiveKPIValues();

        if (typeof initKPICharts === 'function') {
          requestAnimationFrame(() => {
            initKPICharts(this.kpiDepartments, this.liveKPIData);
          });
        }

        if (typeof initCompanyKPICharts === 'function') {
          requestAnimationFrame(() => {
            initCompanyKPICharts(this.companyKPIs);
          });
        }
      }
    },

    /**
     * FIX: Overlay live telemetry values onto department KPI definitions.
     * /api/v1/kpis returns definitions only, so cards previously rendered
     * "undefined" for current/status. The live snapshot
     * (liveKPIData.departments[deptId].kpis) is keyed by the same ids as
     * the definitions, each value {current, target, unit, status}.
     * Defensive: live data may be null or missing departments; only fields
     * the live payload actually provides are copied.
     */
    mergeLiveKPIValues() {
      const live = this.liveKPIData;
      if (!live || !live.departments) return;

      this.kpiDepartments.forEach(dept => {
        const liveDept = live.departments[dept.id];
        if (!liveDept || !liveDept.kpis) return;
        (dept.kpis || []).forEach(kpi => {
          const liveKpi = liveDept.kpis[kpi.id];
          if (!liveKpi) return;
          if (liveKpi.current !== undefined) kpi.current = liveKpi.current;
          if (liveKpi.target !== undefined) kpi.target = liveKpi.target;
          if (liveKpi.unit !== undefined) kpi.unit = liveKpi.unit;
          if (liveKpi.status !== undefined) kpi.status = liveKpi.status;
        });
      });
    },

    async refreshKPIs() {
      this.saveScrollPosition();
      await this.loadKPIs();
      this.restoreScrollPosition();
      this.showToast('success', 'Refreshed', 'KPI data updated');
    },

    async loadCosts() {
      // Real cost data from the API — no client-side fabrication.
      const summary = await this.fetchJSON('/api/v1/costs/summary');
      if (!summary) return;

      this.costSummary = {
        total: summary.total_spent ?? 0,
        avgPerTask: summary.avg_cost_per_task ?? 0,
        totalTasks: summary.total_tasks ?? 0,
        costTrend: summary.cost_trend ?? [],
      };

      this.budgetPct = summary.budget_utilization ?? 0;

      // Per-agent cost breakdown (calls == audit LLM calls per agent)
      this.agentCosts = (summary.per_agent_costs ?? []).map(a => ({
        agent: a.agent,
        tasks: a.calls,
        totalCost: a.total_cost,
        avgCost: a.avg_cost_per_call ?? (a.calls > 0 ? a.total_cost / a.calls : 0),
        model: null,
      }));

      // Alerts
      this.costAlerts = [];
      if (this.budgetPct > 90) {
        this.costAlerts.push({
          id: 'budget-critical',
          severity: 'critical',
          message: `Budget usage at ${this.budgetPct.toFixed(1)}% — approaching limit`,
          timestamp: new Date().toISOString(),
        });
      } else if (this.budgetPct > 70) {
        this.costAlerts.push({
          id: 'budget-warning',
          severity: 'warning',
          message: `Budget usage at ${this.budgetPct.toFixed(1)}% — monitor closely`,
          timestamp: new Date().toISOString(),
        });
      }

      if (typeof initCostCharts === 'function') {
        requestAnimationFrame(() => {
          initCostCharts(this.costSummary, this.agentCosts, this.costPeriod);
        });
      }
    },

    // ═══ TASK ACTIONS ═════════════════════════════════════════

    async assignTask() {
      if (!this.newTask.receiver_id || !this.newTask.instruction) return;
      this.submitting = true;
      await this.fetchJSON('/api/v1/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.newTask),
      });
      this.newTask = { receiver_id: '', instruction: '', priority: 'medium', sender_id: 'human-ceo' };
      this.submitting = false;
      this.showAssignModal = false;
      this.saveScrollPosition();
      if (window.location.pathname === '/tasks') {
        await this.loadTasksPage();
      } else {
        await this.loadTasks();
      }
      this.restoreScrollPosition();
      this.showToast('success', 'Task Assigned', 'New task has been created');
    },

    async approveRequest(id) {
      await this.fetchJSON(`/api/v1/approvals/${id}/approve`, { method: 'POST' });
      this.saveScrollPosition();
      await this.loadApprovals();
      this.restoreScrollPosition();
      this.showToast('success', 'Approved', 'Request has been approved');
    },

    async rejectRequest(id) {
      await this.fetchJSON(`/api/v1/approvals/${id}/reject`, { method: 'POST' });
      this.saveScrollPosition();
      await this.loadApprovals();
      this.restoreScrollPosition();
      this.showToast('info', 'Rejected', 'Request has been rejected');
    },

    async saveApprovalEdit(id) {
      const body = {};
      if (this.editRisk !== '') body.risk_level = this.editRisk || null;
      if (this.editCost !== '') body.cost_estimate = this.editCost !== '' ? Number(this.editCost) : null;
      await this.fetchJSON(`/api/v1/approvals/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      this.editingApproval = null;
      await this.loadApprovals();
      this.showToast('success', 'Updated', 'Approval details saved');
    },

    // ═══ ESCALATION NOTIFICATIONS (F6) ══════════════════════════

    _pushEscalationNotif(payload) {
      const nid = ++this._escNotifId;
      const notif = {
        _nid: nid,
        task_id: payload.task_id || '',
        from_agent: payload.from_agent || '',
        to_agent: payload.to_agent || '',
        reason: payload.reason || payload.rule_id || 'Escalation triggered',
        visible: true,
      };
      // Prepend so newest appear at top
      this.escalationNotifications.unshift(notif);
      // Keep max 5 visible at once
      if (this.escalationNotifications.length > 5) {
        this.escalationNotifications = this.escalationNotifications.slice(0, 5);
      }
      // Auto-dismiss after 30s
      setTimeout(() => this.dismissEscalationNotif(nid), 30000);
    },

    dismissEscalationNotif(nid) {
      const idx = this.escalationNotifications.findIndex(n => n._nid === nid);
      if (idx !== -1) {
        this.escalationNotifications[idx].visible = false;
        // Remove from array after transition
        setTimeout(() => {
          this.escalationNotifications = this.escalationNotifications.filter(n => n._nid !== nid);
        }, 250);
      }
    },

    async resolveEscalation(taskId) {
      await this.fetchJSON(`/api/v1/escalations/${taskId}/resolve`, { method: 'POST' });
      this.saveScrollPosition();
      await this.loadEscalations();
      this.restoreScrollPosition();
      this.showToast('success', 'Resolved', 'Escalation has been resolved');
    },

    // ═══ DRAG & DROP ═════════════════════════════════════════

    dragTask(event, task) {
      this.draggedTask = task;
      event.dataTransfer.effectAllowed = 'move';
      event.target.classList.add('dragging');
    },

    dragEnd() {
      this.draggedTask = null;
      document.querySelectorAll('.dragging').forEach(el => el.classList.remove('dragging'));
      document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
    },

    dragOverColumn(event, column) {
      event.currentTarget.classList.add('drag-over');
    },

    async dropTask(event, newStatus) {
      event.currentTarget.classList.remove('drag-over');
      if (!this.draggedTask || this.draggedTask.status === newStatus) return;

      const task = this.draggedTask;
      const oldStatus = task.status;

      // FIX: Guard scroll across the optimistic update + reconcile — the
      // kanban x-for re-renders twice and must not jump the viewport.
      this.saveScrollPosition();

      // Optimistically update the UI
      this.tasks = this.tasks.map(t =>
        t.id === task.id ? { ...t, status: newStatus } : t
      );

      // Persist the status change to the backend
      const res = await this.fetchJSON(`/api/v1/tasks/${task.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });

      if (res && res.id) {
        // Reconcile with server response (in case of extra fields like updated_at)
        if (window.location.pathname === '/tasks') {
          await this.loadTasksPage();
        } else {
          this.tasks = this.tasks.map(t =>
            t.id === res.id ? res : t
          );
        }
        this.showToast('success', 'Task Moved', `Task moved from ${oldStatus} to ${newStatus}`);
      } else {
        // Revert optimistic update on failure
        this.tasks = this.tasks.map(t =>
          t.id === task.id ? { ...t, status: oldStatus } : t
        );
        this.showToast('warning', 'Move Failed', 'Could not persist status change');
      }

      this.restoreScrollPosition();
      this.draggedTask = null;
    },

    // ═══ TASK DELETION ════════════════════════════════════════════

    async deleteTask(taskId) {
      if (!confirm('Delete this task? This cannot be undone.')) return;

      // FIX: Guard scroll across the list mutation / reload.
      this.saveScrollPosition();

      const res = await this.fetchJSON(`/api/v1/tasks/${taskId}`, {
        method: 'DELETE',
      });

      if (res && res.ok) {
        if (window.location.pathname === '/tasks') {
          await this.loadTasksPage();
        } else {
          this.tasks = this.tasks.filter(t => t.id !== taskId);
        }
        this.showToast('success', 'Task Deleted', 'Task has been removed');
      } else {
        this.showToast('warning', 'Delete Failed', 'Could not delete task');
      }

      this.restoreScrollPosition();
    },

    // ═══ TASK DETAIL SLIDE-OUT ═════════════════════════════════

    async openTaskDetail(task) {
      this.selectedTask = task;
      this.taskDetailOpen = true;
      this.taskDecomposition = null;

      // Fetch decomposition if available
      try {
        const res = await this.fetchJSON(`/api/v1/tasks/${task.id}/subtasks`);
        if (res && res.subtasks) {
          this.taskDecomposition = res;
        }
      } catch (e) {
        // No decomposition yet — that's fine
      }
    },

    async decomposeTask(taskId) {
      if (!taskId) return;
      this.taskDecomposing = true;
      try {
        const res = await this.fetchJSON(`/api/v1/tasks/${taskId}/decompose`, {
          method: 'POST',
        });
        if (res) {
          this.taskDecomposition = res;
          this.showToast('success', 'Task Decomposed', 'Task broken down into subtasks');
        }
      } catch (e) {
        this.showToast('error', 'Decompose Failed', 'Could not decompose task');
      }
      this.taskDecomposing = false;
    },

    closeTaskDetail() {
      this.taskDetailOpen = false;
      this.selectedTask = null;
      this.taskDecomposition = null;
    },

    getSubtaskStatusClass(status) {
      const classes = {
        completed: 'bg-emerald-500/20 text-emerald-400',
        in_progress: 'bg-blue-500/20 text-blue-400',
        pending: 'bg-white/[0.06] text-jarvis-muted',
      };
      return classes[status] || classes.pending;
    },

    async reassignTask(taskId) {
      this.showToast('info', 'Reassign', 'Reassignment feature coming soon');
    },

    async escalateTask(taskId) {
      if (!taskId) return;
      try {
        const res = await this.fetchJSON(`/api/v1/tasks/${taskId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: 'escalated' }),
        });
        if (res && res.id) {
          this.showToast('warning', 'Task Escalated', 'Task has been escalated');
          this.closeTaskDetail();
          if (window.location.pathname === '/tasks') {
            this.saveScrollPosition();
            await this.loadTasksPage();
            this.restoreScrollPosition();
          }
        }
      } catch (e) {
        this.showToast('error', 'Escalate Failed', 'Could not escalate task');
      }
    },

    // ═══ COMPUTED ═════════════════════════════════════════════

    get kanbanTasks() {
      return {
        pending: this.tasks.filter(t => t.status === 'pending'),
        in_progress: this.tasks.filter(t => t.status === 'in_progress'),
        completed: this.tasks.filter(t => t.status === 'completed'),
        failed: this.tasks.filter(t => t.status === 'failed'),
        escalated: this.tasks.filter(t => t.status === 'escalated'),
      };
    },

    get kanbanCounts() {
      return {
        pending: this.taskCountsByStatus.pending || 0,
        in_progress: this.taskCountsByStatus.in_progress || 0,
        completed: this.taskCountsByStatus.completed || 0,
        failed: this.taskCountsByStatus.failed || 0,
        escalated: this.taskCountsByStatus.escalated || 0,
      };
    },

    get filteredAgents() {
      return this.agents.filter(a => {
        const matchSearch = !this.agentSearch ||
          a.role.toLowerCase().includes(this.agentSearch.toLowerCase()) ||
          a.name.toLowerCase().includes(this.agentSearch.toLowerCase());
        const matchDept = !this.agentDeptFilter || a.department === this.agentDeptFilter;
        return matchSearch && matchDept;
      });
    },

    get uniqueDepartments() {
      return [...new Set(this.agents.map(a => a.department).filter(Boolean))].sort();
    },

    get currentKPIDept() {
      return this.kpiDepartments.find(d => d.id === this.activeKPIDept);
    },

    get companyKPISummaryText() {
      const s = this.companyKPISummary;
      if (!s) return '';
      return `${s.total || 0} KPIs · ${s.on_track || 0} on track · ${s.below_target || 0} below target`;
    },

    // ═══ HELPERS ══════════════════════════════════════════════

    /**
     * FIX: Merge a KPI payload into this.kpis, returning which parts
     * actually changed. Poll responses and WS pushes can deliver the same
     * snapshot back-to-back; mutating Alpine state for unchanged values is
     * what triggers the redundant re-renders behind scroll jumps.
     *
     * @returns {{stateChanged: boolean, chartRelevantChanged: boolean}}
     */
    _mergeKPIPayload(payload) {
      let stateChanged = false;
      let chartRelevantChanged = false;
      const chartKeys = [
        'pending_tasks',
        'in_progress_tasks',
        'completed_tasks',
        'failed_tasks',
        'escalated_tasks',
      ];

      for (const key of Object.keys(payload || {})) {
        if (key === 'departments' || payload[key] === undefined) continue;
        if (payload[key] !== this.kpis[key]) {
          this.kpis[key] = payload[key];
          stateChanged = true;
          if (chartKeys.includes(key)) chartRelevantChanged = true;
        }
      }
      return { stateChanged, chartRelevantChanged };
    },

    /**
     * FIX: Coalesce KPI chart updates into at most one redraw per
     * animation frame. Multiple callers (poll, WS push, refreshKPIs) can
     * request chart updates in the same frame; without coalescing the
     * canvas redraws repeatedly, which is wasted work and layout churn.
     */
    scheduleKPICharts() {
      if (typeof updateChartsFromKPIs !== 'function') return;
      this._kpiChartsPending = true;
      this._latestKpis = this.kpis;
      this._latestDepartments = this.departments;
      if (this._kpiChartsRaf) return; // one scheduled redraw per frame is enough
      this._kpiChartsRaf = requestAnimationFrame(() => {
        this._kpiChartsRaf = null;
        if (this._kpiChartsPending) {
          this._kpiChartsPending = false;
          updateChartsFromKPIs(this._latestKpis, this._latestDepartments);
        }
      });
    },

    showToast(type, title, message) {
      this.toast = { show: true, type, title, message };
      clearTimeout(this.toastTimer);
      this.toastTimer = setTimeout(() => { this.toast.show = false; }, 5000);
    },

    formatTime(iso) {
      if (!iso) return '';
      const d = new Date(iso);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },

    formatUptime(secs) {
      if (!secs) return '0s';
      const h = Math.floor(secs / 3600);
      const m = Math.floor((secs % 3600) / 60);
      const s = Math.floor(secs % 60);
      if (h > 24) {
        const d = Math.floor(h / 24);
        return `${d}d ${h % 24}h`;
      }
      if (h > 0) return `${h}h ${m}m`;
      if (m > 0) return `${m}m ${s}s`;
      return `${s}s`;
    },

    priorityClass(p) {
      return {
        low:      'bg-surface-700/50 text-surface-400',
        medium:   'bg-blue-500/10 text-blue-400',
        high:     'bg-amber-500/10 text-amber-400',
        critical: 'bg-red-500/10 text-red-400',
      }[p] || 'bg-surface-700/50 text-surface-400';
    },

    statusClass(s) {
      return {
        pending:     'bg-amber-500/10 text-amber-400',
        in_progress: 'bg-blue-500/10 text-blue-400',
        completed:   'bg-emerald-500/10 text-emerald-400',
        failed:      'bg-red-500/10 text-red-400',
        escalated:   'bg-red-500/15 text-red-300',
        cancelled:   'bg-surface-700/50 text-surface-500',
      }[s] || 'bg-surface-700/50 text-surface-400';
    },

    agentTypeBadge(type) {
      return {
        Executive: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
        Manager:   'bg-blue-500/10 text-blue-400 border-blue-500/20',
        Specialist:'bg-brand-500/10 text-brand-400 border-brand-500/20',
        Human:     'bg-amber-500/10 text-amber-400 border-amber-500/20',
      }[type] || 'bg-surface-700/50 text-surface-400 border-surface-600';
    },

    // Status badge classes for company-level KPI cards. Follows the
    // existing KPI badge conventions: emerald for on-track, amber for
    // below-target, gray for informational (fallback).
    companyKPIStatusClass(status) {
      return {
        on_track:     'bg-emerald-500/10 text-emerald-400',
        below_target: 'bg-amber-500/10 text-amber-400',
        info:         'bg-surface-700/50 text-surface-400',
      }[status] || 'bg-surface-700/50 text-surface-400';
    },

    formatCompactCurrency(value) {
      if (value === null || value === undefined || value === '') return '—';
      const abs = Math.abs(value);
      const sign = value < 0 ? '-' : '';
      if (abs >= 1e9) return `${sign}$${(value / 1e9).toFixed(1).replace(/\.0$/, '')}B`;
      if (abs >= 1e6) return `${sign}$${(value / 1e6).toFixed(1).replace(/\.0$/, '')}M`;
      if (abs >= 1e3) return `${sign}$${(value / 1e3).toFixed(1).replace(/\.0$/, '')}K`;
      return `${sign}$${Math.round(value)}`;
    },

    formatKPIValue(value, unit) {
      if (value === null || value === undefined || value === '') return '—';
      if (typeof value !== 'number') return value;
      if (unit === 'usd') return this.formatCompactCurrency(value);
      if (unit === 'percent') return `${Math.round(value)}%`;
      return value.toLocaleString();
    },

    // ═══ CEO HERO METHODS ══════════════════════════════════════

    async loadOrgHealth() {
      this.orgHealthLoading = true;
      try {
        const res = await this.fetchJSON('/api/v1/org-health');
        if (res) {
          this.orgHealth = res;
          this.$nextTick(() => this.renderHeroGauges());
        }
      } catch (e) {
        console.error('Failed to load org health:', e);
      } finally {
        this.orgHealthLoading = false;
      }
    },

    setHeroVariant(v) {
      this.heroVariant = v;
      this.expandedComponent = null;
      localStorage.setItem('heroVariant', v);
      this.$nextTick(() => this.renderHeroGauges());
    },

    getBandTextClass(band) {
      return {
        green: 'text-emerald-400',
        amber: 'text-amber-400',
        red: 'text-red-400',
      }[band] || 'text-slate-400';
    },

    getBandClass(band) {
      return {
        green: 'bg-emerald-500',
        amber: 'bg-amber-500',
        red: 'bg-red-500',
      }[band] || 'bg-slate-500';
    },

    getComponentLabel(name) {
      const labels = {
        task_success_rate: 'Task Success Rate',
        agent_utilization: 'Agent Utilization',
        cost_efficiency: 'Cost Efficiency',
        error_rate: 'Error Rate (Inverted)',
      };
      return labels[name] || name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },

    getComponentDescription(name) {
      const descs = {
        task_success_rate: 'Ratio of completed tasks to total tasks (30d)',
        agent_utilization: 'Active agents vs registered agents (30d)',
        cost_efficiency: 'Budget utilization vs spend',
        error_rate: 'Error/exception rate across operations (inverted)',
      };
      return descs[name] || '';
    },

    toggleComponent(comp) {
      this.expandedComponent = this.expandedComponent === comp ? null : comp;
      this.$nextTick(() => this.renderHeroGauges());
    },

    renderHeroGauges() {
      if (!this.orgHealth || typeof Chart === 'undefined') return;

      // Render the appropriate gauge based on variant
      if (this.heroVariant === 'A') {
        this._renderRadialGauge('heroGauge', this.orgHealth.score, this.orgHealth.band, 256);
      } else if (this.heroVariant === 'B') {
        this._renderRadialGauge('heroGaugeB', this.orgHealth.score, this.orgHealth.band, 192);
      } else if (this.heroVariant === 'D') {
        this._renderRadialGauge('heroGaugeD', this.orgHealth.score, this.orgHealth.band, 256);
      }

      // Render sparklines for component cards
      if (this.orgHealth.components) {
        for (const comp of this.orgHealth.components) {
          this._renderSparkline('spark-' + comp.name, this._generateTrendData(comp.value));
          this._renderSparkline('spark-b-' + comp.name, this._generateTrendData(comp.value));
          // D variant: overview cards + detail view sparklines
          this._renderSparkline('spark-d-' + comp.name, this._generateTrendData(comp.value));
          if (this.expandedComponent === comp.name) {
            this._renderSparkline('spark-detail-' + comp.name, this._generateTrendData(comp.value));
          }
        }
      }
    },

    _renderRadialGauge(canvasId, score, band, size) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || typeof Chart === 'undefined') return;

      const ctx = canvas.getContext('2d');
      const bandColors = {
        green: '#34d399',
        amber: '#fbbf24',
        red: '#f87171',
      };
      const color = bandColors[band] || '#64748b';

      // Destroy existing chart
      if (this._heroGauges[canvasId]) {
        this._heroGauges[canvasId].destroy();
      }

      this._heroGauges[canvasId] = new Chart(ctx, {
        type: 'doughnut',
        data: {
          datasets: [{
            data: [score, 100 - score],
            backgroundColor: [color, 'rgba(255,255,255,0.06)'],
            borderWidth: 0,
            circumference: 180,
            rotation: 270,
          }]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          cutout: '75%',
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
          },
          animation: {
            animateRotate: true,
            animateScale: true,
            duration: 1000,
            easing: 'easeOutQuart',
          },
        },
      });
    },

    _renderSparkline(canvasId, data) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || typeof Chart === 'undefined') return;

      const ctx = canvas.getContext('2d');

      if (this._heroGauges[canvasId]) {
        this._heroGauges[canvasId].destroy();
      }

      this._heroGauges[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map((_, i) => i),
          datasets: [{
            data: data,
            borderColor: '#22d3ee',
            borderWidth: 2,
            pointRadius: 0,
            fill: true,
            backgroundColor: 'rgba(34, 211, 238, 0.1)',
            tension: 0.4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: { enabled: false } },
          scales: { x: { display: false }, y: { display: false } },
          elements: { point: { radius: 0 } },
          animation: { duration: 500 },
        },
      });
    },

    _generateTrendData(currentValue) {
      // Generate 20 pseudo-random points trending toward currentValue
      const points = [];
      let val = currentValue * (0.7 + Math.random() * 0.3);
      for (let i = 0; i < 20; i++) {
        val += (currentValue - val) * 0.1 + (Math.random() - 0.5) * 5;
        val = Math.max(0, Math.min(100, val));
        points.push(val);
      }
      return points;
    },
  };
}
