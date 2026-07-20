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

    // ── Agent search ─────────────────────────────────────────
    agentSearch: '',
    agentDeptFilter: '',
    selectedAgent: null,

    // ═══ INITIALIZATION ═══════════════════════════════════════

    async init() {
      this.connectWebSocket();
      await this.loadPageData();
      // Poll for updates every 10 seconds
      setInterval(() => this.loadPageData(), 10000);
    },

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
            // Update main KPIs if the payload has the expected shape
            if (msg.payload.pending_tasks !== undefined) {
              Object.assign(this.kpis, msg.payload);
            }
            // Update live KPI data for charts
            this.liveKPIData = msg.payload;
            if (typeof updateChartsFromKPIs === 'function') {
              updateChartsFromKPIs(this.kpis, this.departments);
            }
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
        await this.loadTasks();
        await this.loadAgents();
      } else if (path === '/kpis') {
        await this.loadKPIs();
      } else if (path === '/costs') {
        await this.loadCosts();
      } else if (path === '/escalations') {
        await this.loadApprovals();
        await this.loadEscalations();
      }
    },

    async loadDashboard() {
      const [kpis, depts, tasks] = await Promise.all([
        this.fetchJSON('/api/dashboard'),
        this.fetchJSON('/api/departments'),
        this.fetchJSON('/api/tasks'),
      ]);
      if (kpis) Object.assign(this.kpis, kpis);
      if (depts) this.departments = depts;
      if (tasks) this.tasks = tasks;

      if (typeof updateChartsFromKPIs === 'function') {
        updateChartsFromKPIs(this.kpis, this.departments);
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
        initKPICharts(this.kpiDepartments, this.liveKPIData);
      }
    },

    async refreshKPIs() {
      await this.loadKPIs();
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
        initCostCharts(this.costSummary, this.agentCosts, this.costPeriod);
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
      await this.loadTasks();
      this.showToast('success', 'Task Assigned', 'New task has been created');
    },

    async approveRequest(id) {
      await this.fetchJSON(`/api/approvals/${id}/approve`, { method: 'POST' });
      await this.loadApprovals();
      this.showToast('success', 'Approved', 'Request has been approved');
    },

    async rejectRequest(id) {
      await this.fetchJSON(`/api/approvals/${id}/reject`, { method: 'POST' });
      await this.loadApprovals();
      this.showToast('info', 'Rejected', 'Request has been rejected');
    },

    async resolveEscalation(taskId) {
      await this.fetchJSON(`/api/escalations/${taskId}/resolve`, { method: 'POST' });
      await this.loadEscalations();
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

      // Update task status via API (if endpoint exists)
      // For now, we optimistically update the UI
      const task = this.draggedTask;
      const oldStatus = task.status;

      // Move in local state
      this.tasks = this.tasks.map(t =>
        t.id === task.id ? { ...t, status: newStatus } : t
      );

      this.showToast('info', 'Task Moved', `Task moved from ${oldStatus} to ${newStatus}`);
      this.draggedTask = null;
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
  };
}
