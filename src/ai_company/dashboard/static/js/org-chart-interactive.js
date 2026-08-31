/**
 * Interactive Org Chart — Alpine.js Component
 *
 * F7 prototype: clickable SVG/CSS tree with node detail panel,
 * real-time WebSocket updates, and collapsible subtrees.
 *
 * Requirements:
 * 1. Node rendering: tier-based styling, status dots, collapsible subtrees, zoom/pan
 * 2. Node detail panel: slide-in with agent identity, live status, memory state,
 *    active tool calls, recent activity feed, action buttons
 * 3. Real-time updates: WS subscription to "agents" topic, surgical node updates
 * 4. Layout: CSS flexbox top-down tree (no heavy graph library)
 *
 * Dependencies: Alpine.js, Tailwind CSS, WebSocket (from app.js dashboard())
 * Zero new dependencies.
 */
function orgChartInteractive() {
  return {
    // ── Data ──────────────────────────────────────────────────
    tree: [],
    allAgents: [],
    agentMap: {},          // name → agent summary (quick lookup)
    selectedNode: null,
    detailPanelOpen: false,

    // ── Zoom / Pan ────────────────────────────────────────────
    zoom: 100,
    panX: 0,
    panY: 0,
    _isPanning: false,
    _panStart: { x: 0, y: 0 },
    _panStartOffset: { x: 0, y: 0 },

    // ── Collapse state ────────────────────────────────────────
    collapsedNodes: new Set(),

    // ── Drag-and-drop reassignment ────────────────────────────
    draggedNode: null,
    showReassignModal: false,
    reassigningAgent: null,
    newManager: '',

    // ── Real-time state ───────────────────────────────────────
    agentStatuses: {},    // name → { status, lastSeen, activeTasks }
    activityFeed: {},     // name → [{ timestamp, event, detail }]
    activeToolCalls: {},  // name → [{ tool, startedAt, args }]
    memoryState: {},      // name → [{ timestamp, taskContext, result }]
    orgSummary: null,     // X-Org-Summary → { total_agents, avg_span_of_control, ... }
    riskFilter: 'all',    // 'all' | 'at-risk' | 'senior' | 'busy'

    // ── Loading ───────────────────────────────────────────────
    loading: true,
    error: null,

    // ── WebSocket ─────────────────────────────────────────────
    _ws: null,
    _wsReconnectTimer: null,
    _wsReconnectAttempts: 0,
    _wsMaxReconnectAttempts: 8,

    // ═══ INITIALIZATION ═══════════════════════════════════════

    async init() {
      await Promise.all([
        this.loadOrgChart(),
        this.loadAllAgents(),
      ]);
      this.buildAgentMap();
      this._autoCollapseDeep(2);
      this.connectWebSocket();
      this._setupEventDelegation();
      this._autoFitView();
    },

    _autoCollapseDeep(maxDepth) {
      const walk = (nodes, depth) => {
        if (!nodes) return;
        for (const n of nodes) {
          if (depth >= maxDepth && n.children && n.children.length > 0) {
            this.collapsedNodes.add(n.name);
          }
          walk(n.children, depth + 1);
        }
      };
      walk(this.tree, 0);
    },

    _autoFitView() {
      setTimeout(() => {
        const root = document.getElementById('org-tree-root');
        const container = document.querySelector('.org-tree-container');
        if (!root || !container) return;
        const treeW = root.scrollWidth;
        const treeH = root.scrollHeight;
        const viewW = container.clientWidth;
        const viewH = container.clientHeight;
        if (treeW > 0 && viewW > 0) {
          const scaleX = (viewW - 40) / treeW;
          const scaleY = (viewH - 40) / treeH;
          const fit = Math.min(scaleX, scaleY, 1.0);
          this.zoom = Math.max(25, Math.round(fit * 100));
        }
        container.scrollLeft = (root.scrollWidth - container.clientWidth) / 2;
        container.scrollTop = 0;
      }, 100);
    },

    _scrollToRoot() {
      setTimeout(() => {
        const container = document.querySelector('.org-tree-container');
        if (container) {
          container.scrollLeft = 0;
          container.scrollTop = 0;
        }
      }, 50);
    },

    _setupEventDelegation() {
      const container = document.getElementById('org-tree-root');
      if (!container) return;
      container.addEventListener('click', (e) => {
        // Collapse toggle
        const collapseBtn = e.target.closest('[data-collapse]');
        if (collapseBtn) {
          e.stopPropagation();
          const name = collapseBtn.getAttribute('data-collapse');
          this.toggleCollapse(name);
          return;
        }
        // Node card click — select
        const nodeEl = e.target.closest('[data-agent]');
        if (nodeEl) {
          const name = nodeEl.getAttribute('data-agent');
          const node = this.findNode(name);
          if (node) this.selectNode(node);
        }
      });
      container.addEventListener('dblclick', (e) => {
        const nodeEl = e.target.closest('[data-agent]');
        if (nodeEl) {
          const name = nodeEl.getAttribute('data-agent');
          this.toggleCollapse(name);
        }
      });
      container.addEventListener('dragstart', (e) => {
        const nodeEl = e.target.closest('[data-agent]');
        if (nodeEl) {
          const name = nodeEl.getAttribute('data-agent');
          const node = this.findNode(name);
          if (node) {
            this.draggedNode = node;
            e.dataTransfer.effectAllowed = 'move';
          }
        }
      });
      container.addEventListener('dragover', (e) => e.preventDefault());
      container.addEventListener('drop', (e) => {
        e.preventDefault();
        const targetEl = e.target.closest('[data-agent]');
        if (targetEl && this.draggedNode) {
          const targetName = targetEl.getAttribute('data-agent');
          const targetNode = this.findNode(targetName);
          if (targetNode && this.draggedNode.name !== targetName) {
            this.reassigningAgent = this.draggedNode;
            this.newManager = targetName;
            this.showReassignModal = true;
          }
        }
      });
    },

    destroy() {
      this.disconnectWebSocket();
    },

    // ═══ AUTH HELPERS ══════════════════════════════════════════

    /**
     * Fetch wrapper that includes the ADR-013 session token from the
     * parent dashboard() Alpine component. On 401, re-mints the token
     * and retries once.
     */
    async _authFetch(url, opts = {}) {
      const headers = { ...(opts.headers || {}) };
      const token = window.__dashboardSessionToken;
      if (token && !headers['X-API-Key']) {
        headers['X-API-Key'] = token;
      }
      let res = await fetch(url, { ...opts, headers });
      if (res.status === 401 && !opts._retried) {
        // Re-mint session token and retry once
        try {
          const tokRes = await fetch('/api/v1/bootstrap-token');
          if (tokRes.ok) {
            const data = await tokRes.json();
            window.__dashboardSessionToken = data.token || null;
            headers['X-API-Key'] = window.__dashboardSessionToken;
            res = await fetch(url, { ...opts, headers, _retried: true });
          }
        } catch (_) { /* retry failed */ }
      }
      return res;
    },

    // ═══ DATA LOADING ════════════════════════════════════════

    async loadOrgChart() {
      this.loading = true;
      this.error = null;
      try {
        const res = await this._authFetch('/api/v1/org-chart?include_metrics=true');
        if (res.ok) {
          this.tree = await res.json();
          const summaryHeader = res.headers.get('X-Org-Summary');
          if (summaryHeader) {
            try { this.orgSummary = JSON.parse(summaryHeader); } catch (_) { this.orgSummary = null; }
          }
          this._autoCollapseDeep(2);
          this._autoFitView();
        } else {
          this.error = `Failed to load org chart: ${res.status} ${res.statusText}`;
        }
      } catch (e) {
        console.error('[OrgChart] Failed to load tree:', e);
        this.error = 'Network error loading org chart';
      }
      this.loading = false;
    },

    async loadAllAgents() {
      try {
        const res = await this._authFetch('/api/v1/agents');
        if (res.ok) this.allAgents = await res.json();
      } catch (e) {
        console.error('[OrgChart] Failed to load agents:', e);
      }
    },

    buildAgentMap() {
      this.agentMap = {};
      for (const a of this.allAgents) {
        this.agentMap[a.name] = a;
      }
    },

    // ═══ WEBSOCKET — REAL-TIME UPDATES ═══════════════════════

    /**
     * Connect to the dashboard WebSocket and subscribe to the "agents"
     * topic. On each message, surgically update the affected node's
     * status/activity without re-rendering the full tree.
     */
    connectWebSocket() {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      let wsUrl = `${protocol}//${window.location.host}/ws/v1/dashboard`;
      // ADR-013: pass session token for WS auth
      const token = window.__dashboardSessionToken;
      if (token) {
        wsUrl += `?api_key=${encodeURIComponent(token)}`;
      }

      try {
        this._ws = new WebSocket(wsUrl);
      } catch (e) {
        console.warn('[OrgChart] WS connection failed:', e);
        this._scheduleReconnect();
        return;
      }

      this._ws.onopen = () => {
        console.log('[OrgChart] WS connected');
        this._wsReconnectAttempts = 0;
        // Subscribe to agent updates
        this._wsSend({ type: 'subscribe', topics: ['agents', 'tasks'] });
      };

      this._ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          this._handleWSMessage(msg);
        } catch (e) {
          console.warn('[OrgChart] WS parse error:', e);
        }
      };

      this._ws.onclose = () => {
        console.warn('[OrgChart] WS disconnected');
        this._scheduleReconnect();
      };

      this._ws.onerror = () => {
        // onerror always fires before onclose — no-op here
      };
    },

    disconnectWebSocket() {
      clearTimeout(this._wsReconnectTimer);
      if (this._ws) {
        try {
          this._ws.onopen = null;
          this._ws.onmessage = null;
          this._ws.onclose = null;
          this._ws.onerror = null;
          this._ws.close();
        } catch (_) { /* best-effort */ }
      }
    },

    _wsSend(data) {
      if (this._ws && this._ws.readyState === WebSocket.OPEN) {
        this._ws.send(JSON.stringify(data));
      }
    },

    _scheduleReconnect() {
      if (this._wsReconnectAttempts >= this._wsMaxReconnectAttempts) {
        console.warn('[OrgChart] WS reconnect exhausted — relying on polling');
        return;
      }
      const delay = Math.min(30000, 1000 * Math.pow(2, this._wsReconnectAttempts));
      this._wsReconnectTimer = setTimeout(() => {
        this._wsReconnectAttempts++;
        this.connectWebSocket();
      }, delay);
    },

    /**
     * Handle incoming WebSocket messages. For "agent_update" events,
     * surgically patch the affected node in the tree and update the
     * detail panel if it's showing that agent — NO full tree re-render.
     */
    _handleWSMessage(msg) {
      switch (msg.type) {
        case 'agent_update':
          this._applyAgentUpdate(msg.payload);
          break;
        case 'task_update':
          this._applyTaskUpdate(msg.payload);
          break;
        case 'connected':
          // handshake acknowledgement — ignore
          break;
        case 'pong':
          break;
        default:
          break;
      }
    },

    /**
     * Surgically update a single agent's status in the tree.
     * Updates agentStatuses, activityFeed, and activeToolCalls
     * without touching the tree structure (no Alpine re-render storm).
     */
    _applyAgentUpdate(payload) {
      if (!payload || !payload.name) return;
      const name = payload.name;

      // Update status map (triggers detail panel reactivity only)
      this.agentStatuses[name] = {
        status: payload.status || 'idle',
        lastSeen: payload.last_seen || new Date().toISOString(),
        activeTasks: payload.active_tasks || 0,
        department: payload.department,
        type: payload.type,
      };

      // Append to activity feed (keep last 5)
      if (!this.activityFeed[name]) this.activityFeed[name] = [];
      if (payload.event) {
        this.activityFeed[name].unshift({
          timestamp: payload.timestamp || new Date().toISOString(),
          event: payload.event,
          detail: payload.detail || '',
        });
        if (this.activityFeed[name].length > 5) {
          this.activityFeed[name] = this.activityFeed[name].slice(0, 5);
        }
      }

      // Update tool calls
      if (payload.active_tool_calls !== undefined) {
        this.activeToolCalls[name] = payload.active_tool_calls || [];
      }

      // Update memory state (last 5 task contexts)
      if (payload.recent_tasks) {
        this.memoryState[name] = (payload.recent_tasks || []).slice(0, 5);
      }

      // If the detail panel is showing this agent, force reactivity
      if (this.selectedNode && this.selectedNode.name === name) {
        this.selectedNode = { ...this.selectedNode };
      }
    },

    _applyTaskUpdate(payload) {
      if (!payload || !payload.assigned_to) return;
      const name = payload.assigned_to;
      // Bump activity feed for the assigned agent
      if (!this.activityFeed[name]) this.activityFeed[name] = [];
      this.activityFeed[name].unshift({
        timestamp: payload.updated_at || new Date().toISOString(),
        event: `Task ${payload.status || 'updated'}`,
        detail: payload.instruction || payload.title || '',
      });
      if (this.activityFeed[name].length > 5) {
        this.activityFeed[name] = this.activityFeed[name].slice(0, 5);
      }
    },

    // ═══ NODE RENDERING ═══════════════════════════════════════

    /**
     * Tier-based styling: maps agent type to visual tier.
     * Executive → gold, Leadership (Manager/Board) → blue,
     * Department → cyan, Specialist → slate.
     */
    getTierClass(type) {
      const t = (type || '').toLowerCase();
      if (t === 'executive') {
        return 'border-amber-400/60 bg-amber-500/[0.08] shadow-amber-500/10';
      }
      if (t === 'manager' || t === 'board' || t === 'leadership') {
        return 'border-blue-400/50 bg-blue-500/[0.08] shadow-blue-500/10';
      }
      if (t === 'department') {
        return 'border-cyan-400/50 bg-cyan-500/[0.08] shadow-cyan-500/10';
      }
      // Specialist / fallback
      return 'border-slate-400/40 bg-slate-500/[0.06] shadow-slate-500/10';
    },

    getTierBadgeClass(type) {
      const t = (type || '').toLowerCase();
      if (t === 'executive') return 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
      if (t === 'manager' || t === 'board' || t === 'leadership') return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      if (t === 'department') return 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30';
      return 'bg-slate-500/20 text-slate-300 border border-slate-500/30';
    },

    /**
     * Status dot color — maps live agent status to a colored dot.
     */
    getStatusDotClass(name) {
      const status = this.agentStatuses[name]?.status;
      if (status === 'active' || status === 'running' || status === 'in_progress') {
        return 'bg-emerald-400 shadow-emerald-400/60 animate-pulse';
      }
      if (status === 'pending' || status === 'queued') {
        return 'bg-amber-400 shadow-amber-400/50';
      }
      if (status === 'failed' || status === 'error') {
        return 'bg-red-400 shadow-red-400/50';
      }
      if (status === 'paused' || status === 'idle') {
        return 'bg-slate-400 shadow-slate-400/40';
      }
      // Default: offline / unknown
      return 'bg-slate-600 shadow-slate-600/30';
    },

    getStatusLabel(name) {
      return this.agentStatuses[name]?.status || 'offline';
    },

    // ═══ COLLAPSIBLE SUBTREES ════════════════════════════════

    isCollapsed(name) {
      return this.collapsedNodes.has(name);
    },

    toggleCollapse(name, event) {
      if (event) event.stopPropagation();
      if (this.collapsedNodes.has(name)) {
        this.collapsedNodes.delete(name);
      } else {
        this.collapsedNodes.add(name);
      }
      // Force Alpine to detect Set mutation
      this.collapsedNodes = new Set(this.collapsedNodes);
    },

    hasChildren(node) {
      return node.children && node.children.length > 0;
    },

    // ═══ ZOOM / PAN ══════════════════════════════════════════

    zoomIn() {
      this.zoom = Math.min(200, this.zoom + 15);
      this._scrollToRoot();
    },

    zoomOut() {
      this.zoom = Math.max(25, this.zoom - 15);
      this._scrollToRoot();
    },

    resetZoom() {
      this.panX = 0;
      this.panY = 0;
      this._autoFitView();
    },

    fitToView() {
      this.panX = 0;
      this.panY = 0;
      this._autoFitView();
    },

    get containerTransform() {
      return `scale(${this.zoom / 100}) translate(${this.panX}px, ${this.panY}px)`;
    },

    // Pan via mouse drag — scrolls the container
    onPanStart(event) {
      if (event.button === 1 || event.target.classList.contains('org-tree-bg')) {
        this._isPanning = true;
        this._panStart = { x: event.clientX, y: event.clientY };
        const c = event.currentTarget;
        this._panStartScroll = { x: c.scrollLeft, y: c.scrollTop };
        event.preventDefault();
      }
    },

    onPanMove(event) {
      if (!this._isPanning) return;
      const c = event.currentTarget;
      const dx = event.clientX - this._panStart.x;
      const dy = event.clientY - this._panStart.y;
      c.scrollLeft = this._panStartScroll.x - dx;
      c.scrollTop = this._panStartScroll.y - dy;
    },

    onPanEnd() {
      this._isPanning = false;
    },

    onWheelZoom(event) {
      if (event.ctrlKey || event.metaKey) {
        event.preventDefault();
        const delta = event.deltaY > 0 ? -10 : 10;
        this.zoom = Math.min(200, Math.max(25, this.zoom + delta));
      }
    },

    // ═══ NODE SELECTION & DETAIL PANEL ════════════════════════

    selectNode(node) {
      this.selectedNode = node;
      this.detailPanelOpen = true;

      // Fetch enriched data for the detail panel
      this._loadNodeDetail(node.name);
    },

    closeDetailPanel() {
      this.detailPanelOpen = false;
      // Delay clearing so exit animation can play
      setTimeout(() => { this.selectedNode = null; }, 300);
    },

    async _loadNodeDetail(name) {
      // Try to load recent tasks for memory state
      try {
        const res = await this._authFetch(`/api/v1/agents/${encodeURIComponent(name)}/tasks?limit=5`);
        if (res.ok) {
          const tasks = await res.json();
          this.memoryState[name] = (tasks || []).map(t => ({
            timestamp: t.created_at,
            taskContext: t.instruction || t.title || '',
            result: t.status || 'pending',
            taskId: t.id,
          }));
        }
      } catch (e) {
        // Agent-specific tasks endpoint may not exist yet — that's OK
      }

      // Try to load tool call history
      try {
        const res = await this._authFetch(`/api/v1/agents/${encodeURIComponent(name)}/tool-calls?limit=5`);
        if (res.ok) {
          const calls = await res.json();
          this.activeToolCalls[name] = (calls || []).map(c => ({
            tool: c.tool || c.name,
            startedAt: c.started_at || c.timestamp,
            args: c.args || c.input || {},
            status: c.status || 'completed',
          }));
        }
      } catch (e) {
        // Tool calls endpoint may not exist yet — that's OK
      }
    },

    /**
     * Pause an agent — sends a PATCH to mark it as paused.
     */
    async pauseAgent(name) {
      try {
        const res = await this._authFetch(`/api/v1/agents/${encodeURIComponent(name)}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: 'paused' }),
        });
        if (res.ok) {
          this.agentStatuses[name] = {
            ...this.agentStatuses[name],
            status: 'paused',
          };
          if (this.selectedNode?.name === name) {
            this.selectedNode = { ...this.selectedNode };
          }
          this._showToast('info', 'Agent Paused', `${name} has been paused`);
        }
      } catch (e) {
        this._showToast('error', 'Pause Failed', `Could not pause ${name}`);
      }
    },

    /**
     * View logs for an agent — navigates to the agents page with the
     * agent pre-selected.
     */
    viewLogs(name) {
      window.location.href = `/agents?agent=${encodeURIComponent(name)}`;
    },

    /**
     * Navigate to full agent details page.
     */
    viewFullDetails(name) {
      window.location.href = `/agents?agent=${encodeURIComponent(name)}`;
    },

    // ═══ DRAG-AND-DROP REASSIGNMENT ══════════════════════════

    onDragStart(event, node) {
      this.draggedNode = node;
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', node.name);
    },

    onDragOver(event) {
      event.preventDefault();
      event.dataTransfer.dropEffect = 'move';
    },

    async onDrop(event, targetNode) {
      event.preventDefault();
      if (!this.draggedNode || this.draggedNode.name === targetNode.name) return;

      this.reassigningAgent = this.draggedNode;
      this.newManager = targetNode.name;
      this.showReassignModal = true;
    },

    startReassign(agent) {
      this.reassigningAgent = agent;
      this.newManager = '';
      this.showReassignModal = true;
    },

    async confirmReassign() {
      if (!this.reassigningAgent || !this.newManager) return;

      try {
        const res = await this._authFetch(`/api/v1/agents/${this.reassigningAgent.name}/reports-to`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reports_to: this.newManager })
        });

        if (res.ok) {
          this.showReassignModal = false;
          await this.loadOrgChart();
          this.buildAgentMap();
          this._showToast('success', 'Reassigned', `${this.reassigningAgent.name} now reports to ${this.newManager}`);
        } else {
          const error = await res.json();
          this._showToast('error', 'Reassign Failed', error.detail || 'Failed to reassign agent');
        }
      } catch (e) {
        console.error('[OrgChart] Reassign error:', e);
        this._showToast('error', 'Reassign Failed', 'Network error during reassignment');
      }
    },

    // ═══ TOAST NOTIFICATION ══════════════════════════════════

    _showToast(type, title, message) {
      // Bridge to the dashboard's global showToast if available
      if (typeof showToast === 'function') {
        showToast(type, title, message);
        return;
      }
      // Fallback: simple console log
      console.log(`[OrgChart][${type}] ${title}: ${message}`);
    },

    // ═══ HELPERS ══════════════════════════════════════════════

    /**
     * Format ISO timestamp to a relative time string (e.g., "2m ago").
     */
    timeAgo(iso) {
      if (!iso) return '—';
      const diff = Date.now() - new Date(iso).getTime();
      const secs = Math.floor(diff / 1000);
      if (secs < 60) return `${secs}s ago`;
      const mins = Math.floor(secs / 60);
      if (mins < 60) return `${mins}m ago`;
      const hrs = Math.floor(mins / 60);
      if (hrs < 24) return `${hrs}h ago`;
      const days = Math.floor(hrs / 24);
      return `${days}d ago`;
    },

    /**
     * Get the agent summary from the loaded agent list.
     */
    getAgentSummary(name) {
      return this.agentMap[name] || null;
    },

    /**
     * Get children count for a node.
     */
    childCount(node) {
      return node.children?.length || 0;
    },

    /**
     * Event badge color for the activity feed.
     */
    eventBadgeClass(event) {
      if (!event) return 'bg-slate-500/20 text-slate-400';
      const e = event.toLowerCase();
      if (e.includes('completed') || e.includes('success')) return 'bg-emerald-500/20 text-emerald-400';
      if (e.includes('failed') || e.includes('error')) return 'bg-red-500/20 text-red-400';
      if (e.includes('started') || e.includes('running')) return 'bg-blue-500/20 text-blue-400';
      if (e.includes('pending') || e.includes('queued')) return 'bg-amber-500/20 text-amber-400';
      return 'bg-slate-500/20 text-slate-400';
    },

    /**
     * Tool call status badge class.
     */
    toolStatusClass(status) {
      if (status === 'completed' || status === 'success') return 'text-emerald-400';
      if (status === 'running' || status === 'in_progress') return 'text-blue-400 animate-pulse';
      if (status === 'failed' || status === 'error') return 'text-red-400';
      return 'text-slate-400';
    },

    // ═══ RECURSIVE TREE RENDERING ═════════════════════════════

    /**
     * Find a node by name in the tree (recursive search).
     */
    findNode(name) {
      function search(nodes) {
        for (const n of nodes) {
          if (n.name === name) return n;
          if (n.children) {
            const found = search(n.children);
            if (found) return found;
          }
        }
        return null;
      }
      return search(this.tree);
    },

    /**
     * Build the full org chart as a plain HTML string.
     * Uses event delegation — no Alpine directives in the output.
     */
    renderTree() {
      if (!this.tree || this.tree.length === 0) return '';
      return this.tree.map(n => this._renderNode(n, 0)).join('');
    },

    _badgeClass(type) {
      const t = (type || '').toLowerCase();
      if (t === 'executive') return 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
      if (t === 'manager' || t === 'board' || t === 'leadership') return 'bg-blue-500/20 text-blue-300 border border-blue-500/30';
      if (t === 'department') return 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30';
      return 'bg-slate-500/20 text-slate-300 border border-slate-500/30';
    },

    _nodeCardClass(name) {
      const sel = this.selectedNode && this.selectedNode.name === name;
      return 'node-card bg-jarvis-bg border rounded-lg p-3 transition-colors min-w-[140px] max-w-[200px]'
        + (sel ? ' border-cyan-400/60 shadow-[0_0_0_2px_rgba(34,211,238,0.3)]' : ' border-jarvis-border');
    },

    _toggleIcon(name) {
      return this.collapsedNodes.has(name) ? '+' : '\u2212';
    },

    _nodeRiskLevel(node) {
      const risk = node && node.risk;
      if (!risk || !risk.succession_risk) return null;
      return risk.succession_risk; // 'high' | 'medium' | 'low'
    },

    _riskStripClass(node) {
      const lvl = this._nodeRiskLevel(node);
      if (lvl === 'high') return 'bg-rose-500/70';
      if (lvl === 'medium') return 'bg-amber-500/50';
      if (lvl === 'low') return 'bg-emerald-500/40';
      return 'bg-jarvis-border';
    },

    _nodeCapacity(node) {
      const m = node && node.metrics;
      const cap = m && typeof m.capacity === 'number' ? m.capacity : null;
      return cap === null ? null : Math.max(0, Math.min(100, cap));
    },

    _capacityBarClass(cap) {
      if (cap === null) return 'bg-jarvis-border';
      if (cap >= 80) return 'bg-rose-500/80';   // overloaded
      if (cap >= 50) return 'bg-amber-500/70';  // near capacity
      return 'bg-emerald-500/60';
    },

    _riskBadgeClass(risk) {
      if (!risk) return 'bg-slate-500/20 text-slate-300';
      const lvl = risk.succession_risk;
      if (lvl === 'high') return 'bg-rose-500/20 text-rose-300 border border-rose-500/30';
      if (lvl === 'medium') return 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
      if (lvl === 'low') return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
      return 'bg-slate-500/20 text-slate-300';
    },

    _matchesRiskFilter(node) {
      const f = this.riskFilter;
      if (!f || f === 'all') return true;
      const lvl = this._nodeRiskLevel(node);
      const cap = this._nodeCapacity(node);
      if (f === 'at-risk') return lvl === 'high';
      if (f === 'senior') return lvl === 'low' && (node.risk && node.risk.tenure === 'senior');
      if (f === 'busy' || f === 'overloaded') return cap !== null && cap >= 80;
      return true;
    },

    _renderNode(node, depth) {
      const name = node.name;
      const type = node.type || 'Unknown';
      const role = node.role || '';
      const hasKids = node.children && node.children.length > 0;
      const collapsed = this.collapsedNodes.has(name);
      const badgeCls = this._badgeClass(type);
      const en = name.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
      const safeRole = role.replace(/</g, '&lt;').replace(/>/g, '&gt;');
      const cap = this._nodeCapacity(node);
      const filterDim = !this._matchesRiskFilter(node);

      let html = '<div class="org-tree-recursive-node' + (filterDim ? ' org-filter-dim' : '') + '" draggable="true"'
        + ' data-agent="' + en + '"'
        + '>'
        // Node card
        + '<div class="' + this._nodeCardClass(name) + '">'
        + '<div class="flex items-center gap-2 mb-1">'
        + '<span class="px-1.5 py-0.5 rounded text-xs ' + badgeCls + '">'
        + '<span>' + type.substring(0, 3) + '</span>'
        + '</span>'
        + '<span class="text-jarvis-text font-medium text-sm truncate">' + name + '</span>'
        + '</div>'
        + '<p class="text-xs text-jarvis-text-muted truncate">' + safeRole + '</p>'
        + (cap !== null
          ? '<div class="mt-1.5">'
            + '<div class="flex items-center justify-between text-[10px] text-jarvis-text-muted">'
            + '<span>Load</span><span>' + Math.round(cap) + '%</span>'
            + '</div>'
            + '<div class="mt-0.5 h-1 w-full rounded bg-jarvis-border overflow-hidden">'
            + '<div class="h-full rounded ' + this._capacityBarClass(cap) + '" style="width:' + cap + '%"></div>'
            + '</div>'
            + '</div>'
          : '')
        + '<div class="mt-1.5 h-0.5 w-full rounded ' + this._riskStripClass(node) + '"></div>'
        + '</div>';

      if (hasKids) {
        // Vertical connector from card down
        html += '<div style="width:1px;height:20px;background:rgba(34,211,238,0.25);margin:0 auto"></div>';
        if (!collapsed) {
          // Horizontal bus line + children
          html += '<div style="position:relative;padding-top:20px">'
            // Horizontal line spanning all children
            + '<div style="position:absolute;top:0;left:0;right:0;height:1px;background:rgba(34,211,238,0.25)"></div>'
            + '<div class="org-tree-recursive-children">'
            + node.children.map(c => '<div class="org-tree-recursive-subtree">'
              // Vertical drop from bus to child
              + '<div style="width:1px;height:20px;background:rgba(34,211,238,0.25);margin:0 auto"></div>'
              + this._renderNode(c, depth + 1)
              + '</div>').join('')
            + '</div>'
            + '</div>';
        }
        // Collapse toggle
        html += '<button class="org-tree-recursive-toggle" data-collapse="' + en + '">'
          + '<span>' + this._toggleIcon(name) + '</span>'
          + '</button>';
      }

      html += '</div>';
      return html;
    },
  };
}
