function commandCenter() {
  return {
    kpis: {},
    agents: [],
    approvals: [],
    activity: [],
    healthServices: [],
    routingDecisions: [],
    connections: [],
    departments: [],
    modelUsage: {},
    security: {},
    governance: {},
    stateCounts: [],
    _pollTimer: null,

    async init() {
      await this.fetchAll();
      this.buildDepartmentLayout();
      this._pollTimer = setInterval(() => this.fetchAll(), 15000);
    },

    async fetchAll() {
      try {
        const [dashRes, agentRes, approvalRes, healthRes, modelRes, costRes] = await Promise.allSettled([
          fetch('/api/v1/dashboard').then(r => r.json()),
          fetch('/api/v1/agents').then(r => r.json()),
          fetch('/api/v1/approvals').then(r => r.json()),
          fetch('/api/v1/health').then(r => r.json()),
          fetch('/api/v1/models').then(r => r.json()),
          fetch('/api/v1/costs').then(r => r.json()),
        ]);

        if (dashRes.status === 'fulfilled') {
          const d = dashRes.value;
          this.kpis = {
            company_health: d.company_health || 'Good',
            health_trend: d.health_trend || 0,
            revenue: d.revenue || 0,
            burn_rate: d.burn_rate || 0,
            runway_months: d.runway_months || 0,
            mrr: d.mrr || 0,
            active_agents: d.active_agents || 0,
            utilization: d.utilization || 0,
            tasks_completed: d.tasks_completed || 0,
            tokens_used: d.tokens_used || 0,
            uptime_seconds: d.uptime_seconds || 0,
            active_workflows: d.active_workflows || 0,
          };
          this.security = d.security || { threat_level: 'low', blocked_count: 0 };
          this.governance = d.governance || { compliance_pct: 100, pending_approvals: 0 };
        }

        if (agentRes.status === 'fulfilled') {
          const raw = Array.isArray(agentRes.value) ? agentRes.value : (agentRes.value.agents || []);
          this.agents = raw.map(a => ({
            id: a.id,
            name: a.name || a.id,
            tier: a.tier || a.type || 'specialist',
            model: a.model || '—',
            tokens: a.tokens_used || 0,
            task: a.current_task || '',
            state: this.mapState(a.status || a.state || 'offline'),
            department: a.department || '',
          }));
          this.computeStateCounts();
        }

        if (approvalRes.status === 'fulfilled') {
          const raw = Array.isArray(approvalRes.value) ? approvalRes.value : (approvalRes.value.approvals || []);
          this.approvals = raw.map(a => ({
            id: a.id,
            title: a.title || a.description || 'Untitled',
            agent: a.agent || a.requester || '—',
            tier: a.tier || 1,
            time_ago: a.time_ago || a.created_at || '',
          }));
        }

        if (healthRes.status === 'fulfilled') {
          const h = healthRes.value;
          this.healthServices = Object.entries(h).map(([name, val]) => ({
            name: name.replace(/_/g, ' '),
            status: typeof val === 'string' ? val : (val.status || 'healthy'),
          }));
        } else {
          this.healthServices = [
            { name: 'API', status: 'healthy' },
            { name: 'Queue', status: 'healthy' },
            { name: 'LLM', status: 'degraded' },
            { name: 'Storage', status: 'healthy' },
          ];
        }

        if (modelRes.status === 'fulfilled') {
          const models = modelRes.value;
          const total = models.reduce((s, m) => s + (m.requests || 0), 0) || 1;
          this.modelUsage = {};
          models.forEach(m => {
            const provider = m.provider || 'unknown';
            if (!this.modelUsage[provider]) this.modelUsage[provider] = { pct: 0 };
            this.modelUsage[provider].pct += Math.round(((m.requests || 0) / total) * 100);
          });
        }

        if (costRes.status === 'fulfilled') {
          this.buildRoutingDecisions();
        }

        this.buildActivity();
      } catch (e) {
        console.warn('Command Center fetch error:', e);
      }
    },

    mapState(s) {
      const map = {
        active: 'executing', busy: 'thinking', idle: 'online',
        waiting: 'waiting', blocked: 'blocked', escalated: 'escalated',
        offline: 'offline', running: 'executing', completed: 'online',
        delegated: 'delegating', thinking: 'thinking',
      };
      return map[s] || 'offline';
    },

    computeStateCounts() {
      const counts = {};
      this.agents.forEach(a => {
        const st = a.state || 'offline';
        counts[st] = (counts[st] || 0) + 1;
      });
      this.stateCounts = Object.entries(counts)
        .map(([state, count]) => ({ state, count }))
        .sort((a, b) => b.count - a.count);
    },

    buildDepartmentLayout() {
      const depts = {};
      this.agents.forEach(a => {
        const d = a.department || 'Unassigned';
        if (!depts[d]) depts[d] = { name: d, agents: 0, states: {} };
        depts[d].agents++;
        depts[d].states[a.state] = (depts[d].states[a.state] || 0) + 1;
      });

      const names = Object.keys(depts);
      const count = names.length || 1;
      const positions = [
        { x: 20, y: 100 }, { x: 20, y: 220 }, { x: 20, y: 340 },
        { x: 620, y: 100 }, { x: 620, y: 220 }, { x: 620, y: 340 },
        { x: 300, y: 10 }, { x: 300, y: 420 },
        { x: 140, y: 10 }, { x: 460, y: 420 },
      ];

      this.departments = names.slice(0, 10).map((name, i) => {
        const info = depts[name];
        const dominantState = Object.entries(info.states).sort((a, b) => b[1] - a[1])[0];
        return {
          id: name,
          name: name,
          agents: info.agents,
          state: dominantState ? dominantState[0] : 'offline',
          x: positions[i] ? positions[i].x : 20,
          y: positions[i] ? positions[i].y : 100 + i * 80,
        };
      });

      this.buildConnections();
    },

    buildConnections() {
      const svgW = 800, svgH = 500;
      const cx = svgW / 2, cy = svgH / 2;
      this.connections = this.departments.map((dept, i) => ({
        id: dept.id,
        x1: cx,
        y1: cy,
        x2: dept.x + 60,
        y2: dept.y + 20,
        active: dept.state === 'executing' || dept.state === 'thinking',
      }));
    },

    buildRoutingDecisions() {
      this.routingDecisions = this.agents.slice(0, 6).map(a => ({
        id: a.id,
        agent: a.name,
        model: a.model || '—',
      }));
    },

    buildActivity() {
      const events = [];
      this.agents.forEach(a => {
        if (a.task) {
          events.push({
            id: a.id + '-task',
            message: a.name + ' — ' + a.task,
            severity: a.state === 'escalated' ? 'critical' : a.state === 'blocked' ? 'warning' : 'info',
            state: a.state,
            time_ago: 'now',
          });
        }
      });
      this.approvals.forEach(a => {
        if (a.tier >= 4) {
          events.push({
            id: a.id + '-approval',
            message: 'Decision required: ' + a.title,
            severity: a.tier === 5 ? 'critical' : 'warning',
            state: 'escalated',
            time_ago: a.time_ago,
          });
        }
      });
      this.activity = events.slice(0, 20);
    },

    formatNumber(n) {
      if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
      if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
      return String(n);
    },

    async approveItem(id) {
      try {
        await fetch('/api/v1/approvals/' + id + '/approve', { method: 'POST' });
        this.approvals = this.approvals.filter(a => a.id !== id);
        this.buildActivity();
      } catch (e) { console.warn('Approve failed:', e); }
    },

    async rejectItem(id) {
      try {
        await fetch('/api/v1/approvals/' + id + '/reject', { method: 'POST' });
        this.approvals = this.approvals.filter(a => a.id !== id);
        this.buildActivity();
      } catch (e) { console.warn('Reject failed:', e); }
    },

    destroy() {
      if (this._pollTimer) clearInterval(this._pollTimer);
    },
  };
}
