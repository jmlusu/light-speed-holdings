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
    wsReconnectTimer: null,

    // ── Toast notifications ──────────────────────────────────
    toast: { show: false, type: 'info', title: '', message: '' },
    toastTimer: null,

    // ── Loading state (FIX: prevents layout jump on initial load)
    isLoading: true,

    // ── Scroll management (FIX: auto-scroll prevention) ──────
    _scrollLock: false,
    _pendingPoll: null,

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

    // ── Task assignment ──────────────────────────────────────
    newTask: { receiver_id: '', instruction: '', priority: 'medium', sender_id: 'human-ceo' },
    submitting: false,
    showAssignModal: false,

    // ── Drag and drop ────────────────────────────────────────
    draggedTask: null,

    // ── KPIs page ────────────────────────────────────────────
    activeKPIDept: '',
    kpiDepartments: [],
    allKPIsList: [],
    liveKPIData: null,

    // ── Costs page ───────────────────────────────────────────
    costPeriod: 'daily',
    costSummary: { total: 0, avgPerTask: 0, totalTasks: 0 },
    budgetPct: 0,
    costAlerts: [],
    agentCosts: [],

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
      this.connectWebSocket();

      // FIX: Load data, then reveal UI to prevent layout jump
      await this.loadPageData();
      this.isLoading = false;

      // FIX: Debounced polling — skip if a poll is already in-flight,
      // and batch updates to reduce reflow frequency.
      // Changed from 10s to 15s to reduce churn.
      setInterval(() => this.debouncedPoll(), 15000);
    },

    // ═══ SCROLL MANAGEMENT (FIX: auto-scroll prevention) ═════

    /**
     * Save the current scroll position before a data update that
     * may cause reflow. Called before loadPageData, WS updates,
     * and any operation that mutates visible state.
     */
    saveScrollPosition() {
      this._savedScrollY = window.scrollY;
      this._savedScrollX = window.scrollX;
    },

    /**
     * Restore scroll position after a data update completes.
     * Uses requestAnimationFrame to wait for the browser to finish
     * layout calculations before restoring.
     */
    restoreScrollPosition() {
      if (this._savedScrollY !== undefined) {
        requestAnimationFrame(() => {
          // Only restore if the user hasn't manually scrolled during the update
          const currentY = window.scrollY;
          const diff = Math.abs(currentY - this._savedScrollY);
          // If the browser auto-scrolled more than 5px, snap back
          if (diff > 5 && diff < 200) {
            window.scrollTo(this._savedScrollX, this._savedScrollY);
          }
          this._savedScrollY = undefined;
          this._savedScrollX = undefined;
        });
      }
    },

    /**
     * Debounced poll: if a poll is already in-flight, queue the next one
     * instead of stacking parallel fetches. This prevents multiple
     * concurrent Alpine re-renders that cause layout thrashing.
     */
    async debouncedPoll() {
      if (this._pendingPoll) return; // Skip — previous poll still running
      this._pendingPoll = true;
      try {
        this.saveScrollPosition();
        await this.loadPageData();
        this.restoreScrollPosition();
      } finally {
        this._pendingPoll = false;
      }
    },

    // ═══ WEBSOCKET ═════════════════════════════════════════════

    connectWebSocket() {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/dashboard`;

      try {
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
          console.log('[WS] Connected');
          this.wsConnected = true;
        };

        this.ws.onmessage = (event) => {
          try {
            const msg = JSON.parse(event.data);
            this.handleWSMessage(msg);
          } catch (e) {
            console.warn('[WS] Failed to parse message:', e);
          }
        };

        this.ws.onclose = () => {
          console.log('[WS] Disconnected');
          this.wsConnected = false;
          // Reconnect after 3 seconds
          this.wsReconnectTimer = setTimeout(() => this.connectWebSocket(), 3000);
        };

        this.ws.onerror = (err) => {
          console.warn('[WS] Error:', err);
          this.wsConnected = false;
        };
      } catch (e) {
        console.warn('[WS] Connection failed:', e);
        this.wsReconnectTimer = setTimeout(() => this.connectWebSocket(), 5000);
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

            // Batch update: apply all KPI changes in one reactive tick
            if (msg.payload.pending_tasks !== undefined) {
              Object.assign(this.kpis, msg.payload);
            }
            this.liveKPIData = msg.payload;

            if (typeof updateChartsFromKPIs === 'function') {
              // FIX: Defer chart update to next frame to avoid layout thrashing
              requestAnimationFrame(() => {
                updateChartsFromKPIs(this.kpis, this.departments);
              });
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

        case 'task_update':
          if (msg.payload) {
            // Refresh the current paginated page — the task may have
            // moved pages due to status change, so surgical update is
            // unreliable with server-side pagination.
            if (window.location.pathname === '/tasks') {
              this.loadTasksPage();
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

    async fetchJSON(url, opts = {}) {
      try {
        const res = await fetch(url, opts);
        if (!res.ok) throw new Error(res.statusText);
        return await res.json();
      } catch (e) {
        console.warn(`[API] ${url} failed:`, e.message);
        return null;
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
        const agentsData = await this.fetchJSON('/api/agents');
        if (agentsData) this.agents = agentsData;
      } else if (path === '/kpis') {
        await this.loadKPIs();
      } else if (path === '/costs') {
        await this.loadCosts();
      } else if (path === '/escalations') {
        // FIX: Load both in parallel
        const [approvalsData, escalationsData] = await Promise.all([
          this.fetchJSON('/api/approvals'),
          this.fetchJSON('/api/escalations'),
        ]);
        if (approvalsData) this.approvals = approvalsData;
        if (escalationsData) this.escalations = escalationsData;
      }
    },

    async loadDashboard() {
      const [kpis, depts, tasks] = await Promise.all([
        this.fetchJSON('/api/dashboard'),
        this.fetchJSON('/api/departments'),
        this.fetchJSON('/api/tasks'),
      ]);

      // FIX: Batch all state updates into a single assignment window
      // to minimize Alpine.js reactive re-renders (was 3 separate re-renders,
      // now effectively 1 coordinated update)
      let needsChartUpdate = false;

      if (kpis) {
        Object.assign(this.kpis, kpis);
        needsChartUpdate = true;
      }
      if (depts) {
        this.departments = depts;
        needsChartUpdate = true;
      }
      if (tasks) this.tasks = tasks;

      // FIX: Defer chart updates to next animation frame
      if (needsChartUpdate && typeof updateChartsFromKPIs === 'function') {
        requestAnimationFrame(() => {
          updateChartsFromKPIs(this.kpis, this.departments);
        });
      }
    },

    async loadAgents() {
      const data = await this.fetchJSON('/api/agents');
      if (data) this.agents = data;
    },

    async loadTasks() {
      const data = await this.fetchJSON('/api/tasks');
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

      const data = await this.fetchJSON(`/api/tasks/paginated?${params}`);
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
      const data = await this.fetchJSON('/api/approvals');
      if (data) this.approvals = data;
    },

    async loadEscalations() {
      const data = await this.fetchJSON('/api/escalations');
      if (data) this.escalations = data;
    },

    async loadKPIs() {
      const [depts, summary] = await Promise.all([
        this.fetchJSON('/api/kpis'),
        this.fetchJSON('/api/kpis/summary'),
      ]);

      if (depts) {
        this.kpiDepartments = Object.entries(depts).map(([id, dept]) => ({
          id,
          name: dept.name || id,
          kpiCount: (dept.kpis || []).length,
          kpis: dept.kpis || [],
        }));

        if (this.kpiDepartments.length > 0 && !this.activeKPIDept) {
          this.activeKPIDept = this.kpiDepartments[0].id;
        }
      }

      if (summary) this.allKPIsList = summary;

      // Also load live KPI data
      const live = await this.fetchJSON('/api/kpis/live');
      if (live) this.liveKPIData = live;

      if (typeof initKPICharts === 'function') {
        requestAnimationFrame(() => {
          initKPICharts(this.kpiDepartments, this.liveKPIData);
        });
      }
    },

    async refreshKPIs() {
      this.saveScrollPosition();
      await this.loadKPIs();
      this.restoreScrollPosition();
      this.showToast('success', 'Refreshed', 'KPI data updated');
    },

    async loadCosts() {
      // Build cost data from tasks
      const tasks = await this.fetchJSON('/api/tasks');
      if (!tasks) return;

      const total = tasks.length;
      const completed = tasks.filter(t => t.status === 'completed').length;

      // Cost estimation (placeholder — real cost data would come from cost tracker)
      const totalCost = completed * 0.025; // Estimate $0.025 per completed task
      const avgPerTask = total > 0 ? totalCost / total : 0;

      this.costSummary = {
        total: totalCost,
        avgPerTask: avgPerTask,
        totalTasks: total,
      };

      // Budget calculation (assume $10 daily budget)
      const dailyBudget = 10;
      this.budgetPct = (totalCost / dailyBudget) * 100;

      // Per-agent cost breakdown
      const agentMap = {};
      for (const t of tasks) {
        const agent = t.receiver_id;
        if (!agentMap[agent]) {
          agentMap[agent] = { agent, tasks: 0, totalCost: 0, model: null };
        }
        agentMap[agent].tasks++;
        if (t.status === 'completed') agentMap[agent].totalCost += 0.025;
      }

      this.agentCosts = Object.values(agentMap)
        .map(a => ({ ...a, avgCost: a.tasks > 0 ? a.totalCost / a.tasks : 0 }))
        .sort((a, b) => b.totalCost - a.totalCost);

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
      await this.fetchJSON('/api/tasks', {
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
      await this.fetchJSON(`/api/approvals/${id}/approve`, { method: 'POST' });
      this.saveScrollPosition();
      await this.loadApprovals();
      this.restoreScrollPosition();
      this.showToast('success', 'Approved', 'Request has been approved');
    },

    async rejectRequest(id) {
      await this.fetchJSON(`/api/approvals/${id}/reject`, { method: 'POST' });
      this.saveScrollPosition();
      await this.loadApprovals();
      this.restoreScrollPosition();
      this.showToast('info', 'Rejected', 'Request has been rejected');
    },

    async resolveEscalation(taskId) {
      await this.fetchJSON(`/api/escalations/${taskId}/resolve`, { method: 'POST' });
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

      // Optimistically update the UI
      this.tasks = this.tasks.map(t =>
        t.id === task.id ? { ...t, status: newStatus } : t
      );

      // Persist the status change to the backend
      const res = await this.fetchJSON(`/api/tasks/${task.id}`, {
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

      this.draggedTask = null;
    },

    // ═══ TASK DELETION ════════════════════════════════════════════

    async deleteTask(taskId) {
      if (!confirm('Delete this task? This cannot be undone.')) return;

      const res = await this.fetchJSON(`/api/tasks/${taskId}`, {
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

    // ═══ HELPERS ══════════════════════════════════════════════

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

    // ═══ MOBILE GESTURES (DASH-006) ══════════════════════════════

    /**
     * Initialize touch-based gestures for mobile Kanban interactions.
     * Enables swipe-to-move on task cards when the device supports touch.
     */
    initMobileGestures() {
      if (!('ontouchstart' in window)) return;

      let startX = 0;
      let startY = 0;
      let currentCard = null;

      document.addEventListener('touchstart', (e) => {
        const card = e.target.closest('[data-task-card]');
        if (!card) return;
        currentCard = card;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
      }, { passive: true });

      document.addEventListener('touchend', (e) => {
        if (!currentCard) return;
        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;
        const deltaX = endX - startX;
        const deltaY = endY - startY;

        // Only trigger on horizontal swipes (dx > dy, minimum 50px)
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
          const taskId = currentCard.getAttribute('data-task-id');
          const dropZones = document.querySelectorAll('.kanban-drop-zone');
          for (const zone of dropZones) {
            const rect = zone.getBoundingClientRect();
            if (endX >= rect.left && endX <= rect.right && endY >= rect.top && endY <= rect.bottom) {
              const newStatus = zone.getAttribute('data-status');
              if (taskId && newStatus && typeof this.dropTask === 'function') {
                const fakeEvent = { currentTarget: zone, preventDefault: () => {} };
                this.draggedTask = this.tasks.find(t => t.id === taskId) || null;
                if (this.draggedTask) this.dropTask(fakeEvent, newStatus);
              }
              break;
            }
          }
        }
        currentCard = null;
      }, { passive: true });
    },
  };
}
