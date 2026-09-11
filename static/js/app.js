function dashboard() {
  return {
    activeTab: 'dashboard',
    connected: false,
    submitting: false,
    taskFilter: 'all',
    selectedAgent: null,

    tabs: [
      { id: 'dashboard', label: 'Dashboard' },
      { id: 'org',        label: 'Org Chart' },
      { id: 'tasks',      label: 'Tasks' },
      { id: 'approvals',  label: 'Approvals & Escalations' },
      { id: 'models',     label: 'Models' },
    ],

    kpis: {
      pending_tasks: 0,
      completed_tasks: 0,
      open_escalations: 0,
      pending_approvals: 0,
      total_agents: 0,
      uptime_seconds: 0,
    },
    taskStatusBars: [],
    departments: [],
    orgChart: [],
    agents: [],
    tasks: [],
    approvals: [],
    escalations: [],
    tiers: [],
    modelRoutes: [],

    newTask: { receiver_id: '', instruction: '', priority: 'medium' },

    async fetchJSON(url, opts = {}) {
      try {
        const res = await fetch(url, opts);
        if (!res.ok) throw new Error(res.statusText);
        this.connected = true;
        return await res.json();
      } catch (e) {
        this.connected = false;
        return null;
      }
    },

    async init() {
      await this.loadTab('dashboard');
      setInterval(() => this.loadTab(this.activeTab), 5000);
    },

    async loadTab(tab) {
      switch (tab) {
        case 'dashboard':
          await this.loadDashboard();
          break;
        case 'org':
          await Promise.all([this.loadOrgChart(), this.loadAgents()]);
          break;
        case 'tasks':
          await Promise.all([this.loadTasks(), this.loadAgents()]);
          break;
        case 'approvals':
          await Promise.all([this.loadApprovals(), this.loadEscalations()]);
          break;
        case 'models':
          await this.loadModels();
          break;
      }
    },

    async loadDashboard() {
      const [kpis, depts, tasks] = await Promise.all([
        this.fetchJSON('/api/dashboard'),
        this.fetchJSON('/api/departments'),
        this.fetchJSON('/api/tasks'),
      ]);
      if (!kpis) return;

      this.kpis = kpis;

      const counts = [
        { label: 'pending',     count: kpis.pending_tasks },
        { label: 'in_progress', count: kpis.in_progress_tasks },
        { label: 'completed',   count: kpis.completed_tasks },
        { label: 'failed',      count: kpis.failed_tasks },
        { label: 'escalated',   count: kpis.escalated_tasks },
      ];
      const max = Math.max(...counts.map(c => c.count), 1);
      const colors = {
        pending: 'bg-amber-400',
        in_progress: 'bg-blue-500',
        completed: 'bg-green-500',
        failed: 'bg-red-400',
        escalated: 'bg-red-600',
      };
      this.taskStatusBars = counts.map(c => ({
        label: c.label,
        count: c.count,
        pct: Math.round((c.count / max) * 100),
        color: colors[c.label] || 'bg-gray-400',
      }));

      this.departments = depts || [];
      this.tasks = tasks || [];
    },

    async loadOrgChart() {
      const data = await this.fetchJSON('/api/org-chart');
      if (data) this.orgChart = data;
    },

    async loadAgents() {
      const data = await this.fetchJSON('/api/agents');
      if (data) this.agents = data;
    },

    async loadTasks() {
      const url = this.taskFilter === 'all'
        ? '/api/tasks'
        : `/api/tasks?status=${this.taskFilter}`;
      const data = await this.fetchJSON(url);
      if (data) this.tasks = data;
    },

    async loadApprovals() {
      const data = await this.fetchJSON('/api/approvals/pending');
      if (data) this.approvals = data;
    },

    async loadEscalations() {
      const data = await this.fetchJSON('/api/escalations/pending');
      if (data) this.escalations = data;
    },

    async loadModels() {
      const [routes, tiers] = await Promise.all([
        this.fetchJSON('/api/models'),
        this.fetchJSON('/api/models/tiers'),
      ]);
      if (routes) this.modelRoutes = routes;
      if (tiers) this.tiers = tiers;
    },

    async assignTask() {
      if (!this.newTask.receiver_id || !this.newTask.instruction) return;
      this.submitting = true;
      await this.fetchJSON('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.newTask),
      });
      this.newTask = { receiver_id: '', instruction: '', priority: 'medium' };
      this.submitting = false;
      await this.loadTasks();
    },

    async approveRequest(id) {
      await this.fetchJSON(`/api/approvals/${id}/approve`, { method: 'POST' });
      await this.loadApprovals();
    },

    async rejectRequest(id) {
      await this.fetchJSON(`/api/approvals/${id}/reject`, { method: 'POST' });
      await this.loadApprovals();
    },

    async resolveEscalation(taskId) {
      await this.fetchJSON(`/api/escalations/${taskId}/resolve`, { method: 'POST' });
      await this.loadEscalations();
    },

    deptPct(total) {
      const max = Math.max(...this.departments.map(d => d.total_agents), 1);
      return Math.round((total / max) * 100);
    },

    renderOrgNode(node, depth) {
      const indent = depth * 24;
      const color = depth === 0 ? 'border-brand-500 bg-brand-50' :
                    depth === 1 ? 'border-blue-400 bg-blue-50' :
                    'border-gray-300 bg-gray-50';
      const click = `@click="selectedAgent = agents.find(a => a.name === '${node.name}') || ${JSON.stringify(JSON.stringify(node)).replace(/"/g, '&quot;')}"`;
      let html = `<div class="ml-[${indent}px] mb-2 border-l-4 ${color} pl-3 py-1 rounded-r-lg cursor-pointer hover:shadow-sm transition-shadow" ${click}>`;
      html += `<span class="text-sm font-medium">${node.role}</span>`;
      html += `<span class="text-xs text-gray-400 ml-2 font-mono">${node.name}</span>`;
      if (node.children && node.children.length) {
        html += `<span class="text-xs text-gray-400 ml-2">(${node.children.length} reports)</span>`;
      }
      html += `</div>`;
      if (node.children) {
        for (const child of node.children) {
          html += this.renderOrgNode(child, depth + 1);
        }
      }
      return html;
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
      if (h > 0) return `${h}h ${m}m`;
      if (m > 0) return `${m}m ${s}s`;
      return `${s}s`;
    },

    priorityClass(p) {
      return {
        low:      'bg-gray-100 text-gray-600',
        medium:   'bg-blue-100 text-blue-700',
        high:     'bg-amber-100 text-amber-700',
        critical: 'bg-red-100 text-red-700',
      }[p] || 'bg-gray-100 text-gray-600';
    },

    statusClass(s) {
      return {
        pending:     'bg-amber-100 text-amber-700',
        in_progress: 'bg-blue-100 text-blue-700',
        completed:   'bg-green-100 text-green-700',
        failed:      'bg-red-100 text-red-700',
        escalated:   'bg-red-200 text-red-800',
        cancelled:   'bg-gray-100 text-gray-500',
      }[s] || 'bg-gray-100 text-gray-600';
    },

    tierBadgeClass(tier) {
      return {
        fast:     'bg-gray-100 text-gray-700',
        standard: 'bg-blue-100 text-blue-700',
        premium:  'bg-purple-100 text-purple-700',
      }[tier] || 'bg-gray-100 text-gray-700';
    },
  };
}
