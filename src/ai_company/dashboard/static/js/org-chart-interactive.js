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

    // ── Real-time state ───────────────────────────────────────
    agentStatuses: {},    // name → { status, lastSeen, activeTasks }
    activityFeed: {},     // name → [{ timestamp, event, detail }]
    activeToolCalls: {},  // name → [{ tool, startedAt, args }]
    memoryState: {},      // name → [{ timestamp, taskContext, result }]

    // ── Loading ───────────────────────────────────────────────
    loading: true,

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
      this.connectWebSocket();
    },

    destroy() {
      this.disconnectWebSocket();
    },

    // ═══ DATA LOADING ════════════════════════════════════════

    async loadOrgChart() {
      this.loading = true;
      try {
        const res = await fetch('/api/v1/org-chart');
        if (res.ok) this.tree = await res.json();
      } catch (e) {
        console.error('[OrgChart] Failed to load tree:', e);
      }
      this.loading = false;
    },

    async loadAllAgents() {
      try {
        const res = await fetch('/api/v1/agents');
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
      const wsUrl = `${protocol}//${window.location.host}/ws/v1/dashboard`;

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
      event.stopPropagation();
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
    },

    zoomOut() {
      this.zoom = Math.max(25, this.zoom - 15);
    },

    resetZoom() {
      this.zoom = 100;
      this.panX = 0;
      this.panY = 0;
    },

    fitToView() {
      this.zoom = 100;
      this.panX = 0;
      this.panY = 0;
    },

    get containerTransform() {
      return `scale(${this.zoom / 100}) translate(${this.panX}px, ${this.panY}px)`;
    },

    // Pan via mouse drag on the container background
    onPanStart(event) {
      // Only pan on middle-click or when holding space (simplified: always allow)
      if (event.button === 1 || event.target.classList.contains('org-tree-bg')) {
        this._isPanning = true;
        this._panStart = { x: event.clientX, y: event.clientY };
        this._panStartOffset = { x: this.panX, y: this.panY };
        event.preventDefault();
      }
    },

    onPanMove(event) {
      if (!this._isPanning) return;
      const dx = (event.clientX - this._panStart.x) / (this.zoom / 100);
      const dy = (event.clientY - this._panStart.y) / (this.zoom / 100);
      this.panX = this._panStartOffset.x + dx;
      this.panY = this._panStartOffset.y + dy;
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
        const res = await fetch(`/api/v1/agents/${encodeURIComponent(name)}/tasks?limit=5`);
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
        const res = await fetch(`/api/v1/agents/${encodeURIComponent(name)}/tool-calls?limit=5`);
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
        const res = await fetch(`/api/v1/agents/${encodeURIComponent(name)}`, {
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
  };
}
