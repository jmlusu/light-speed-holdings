/* ═══════════════════════════════════════════════════════════════
   PROTOTYPE — Command Center (throwaway)
   Alpine.js component wiring real dashboard APIs
   ═══════════════════════════════════════════════════════════════ */

function commandCenter() {
  return {
    // ── Variant switching ────────────────────────────────────
    variant: new URLSearchParams(window.location.search).get('variant') || 'B',
    variantNames: { A: 'The Bridge', B: 'The War Room', C: 'The Cockpit' },
    variants: ['A', 'B', 'C'],

    // ── Command bar ──────────────────────────────────────────
    showCommandBar: true,
    commandQuery: '',

    // ── Data ─────────────────────────────────────────────────
    companyHealth: 0,
    metrics: {
      totalAgents: 0,
      activeTasks: 0,
      pendingApprovals: 0,
      openEscalations: 0,
      completedTasks: 0,
      uptimeSeconds: 0,
    },
    briefItems: [],
    workforce: [],
    modelTelemetry: [],
    activityStream: [],

    // ── Polling ──────────────────────────────────────────────
    _pollTimer: null,
    _activityPollTimer: null,

    // ── State mapping ────────────────────────────────────────
    stateMap: {
      active:    'online',
      online:    'online',
      thinking:  'thinking',
      executing: 'executing',
      delegating:'delegating',
      waiting:   'waiting',
      blocked:   'blocked',
      escalated: 'escalated',
      idle:      'online',
      offline:   'offline',
    },

    // ── Agent tier mapping (from registry) ───────────────────
    tierMap: {
      executive:  1,
      leadership: 2,
      department: 3,
      specialist: 4,
      individual: 4,
    },

    async init() {
      await this.fetchData();
      this._pollTimer = setInterval(() => this.fetchData(), 15000);

      // Activity stream polls more frequently for live feel
      this.fetchActivity();
      this._activityPollTimer = setInterval(() => this.fetchActivity(), 5000);

      // Keyboard shortcuts
      this._bindKeyboard();

      // Update URL on variant change
      this.$watch('variant', (v) => {
        const url = new URL(window.location);
        url.searchParams.set('variant', v);
        window.history.replaceState({}, '', url);
      });
    },

    // ── Keyboard shortcuts ───────────────────────────────────
    _bindKeyboard() {
      document.addEventListener('keydown', (e) => {
        const mod = e.metaKey || e.ctrlKey;

        // Cmd/Ctrl+K — toggle command bar
        if (mod && e.key === 'k') {
          e.preventDefault();
          this.showCommandBar = !this.showCommandBar;
          if (this.showCommandBar) {
            this.$nextTick(() => this.$refs.commandInput?.focus());
          }
          return;
        }

        // Cmd/Ctrl+1/2/3 — switch variants
        if (mod && ['1', '2', '3'].includes(e.key)) {
          e.preventDefault();
          this.variant = this.variants[parseInt(e.key) - 1];
          return;
        }

        // Escape — close command bar
        if (e.key === 'Escape' && this.showCommandBar) {
          this.showCommandBar = false;
        }
      });
    },

    // ── Data fetching ────────────────────────────────────────
    async fetchData() {
      try {
        const [briefingRes, agentsRes, telemetryRes] = await Promise.all([
          fetch('/api/v1/briefing').then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/api/v1/agents').then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/api/v1/models/telemetry').then(r => r.ok ? r.json() : null).catch(() => null),
        ]);

        // Executive Briefing
        if (briefingRes) {
          this.briefItems = briefingRes.items || [];
          this.companyHealth = briefingRes.company_health || 85;
          const pipeline = briefingRes.task_pipeline || {};
          this.metrics.activeTasks = (pipeline.in_progress || 0) + (pipeline.pending || 0);
          this.metrics.completedTasks = pipeline.completed || 0;
          this.metrics.openEscalations = briefingRes.summary?.high_priority || 0;
        }

        // Agent workforce with state mapping
        if (agentsRes && Array.isArray(agentsRes)) {
          this.metrics.totalAgents = agentsRes.length;
          this.workforce = agentsRes.slice(0, 30).map(a => {
            const rawState = (a.status || 'idle').toLowerCase();
            return {
              id: a.id || a.name || 'unknown',
              name: a.name || a.id || 'unknown',
              role: a.department || a.type || 'agent',
              model: a.model || 'default',
              status: rawState,
              state: this.stateMap[rawState] || 'offline',
              tier: this.tierMap[a.type] || 4,
            };
          });
        }

        // Model telemetry (read-only observability)
        if (telemetryRes && Array.isArray(telemetryRes)) {
          this.modelTelemetry = telemetryRes;
        }

        // Uptime from ceo-dashboard fallback
        if (!this.metrics.uptimeSeconds) {
          try {
            const ceoRes = await fetch('/api/v1/ceo-dashboard').then(r => r.ok ? r.json() : null).catch(() => null);
            if (ceoRes) {
              this.metrics.uptimeSeconds = ceoRes.uptime_seconds || 0;
            }
          } catch { /* ignore */ }
        }

      } catch (err) {
        console.error('Command Center fetch error:', err);
      }
    },

    async fetchActivity() {
      try {
        // Pull recent activity from briefing items (task updates, alerts, escalations)
        const [tasksRes, alertsRes] = await Promise.all([
          fetch('/api/v1/briefing').then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/api/v1/approvals/pending').then(r => r.ok ? r.json() : null).catch(() => null),
        ]);

        const items = [];

        if (tasksRes && tasksRes.items) {
          tasksRes.items.forEach(item => {
            items.push({
              type: item.category || 'info',
              text: item.title || item.description || '',
              source: item.source || '',
              time: item.timestamp || new Date().toISOString(),
            });
          });
        }

        if (alertsRes && Array.isArray(alertsRes)) {
          alertsRes.slice(0, 5).forEach(req => {
            items.push({
              type: 'alert',
              text: `Approval needed: ${req.title || req.description || 'Unknown request'}`,
              source: req.requester || 'System',
              time: req.created_at || new Date().toISOString(),
            });
          });
        }

        // Deduplicate by text and keep most recent 12
        const seen = new Set();
        this.activityStream = items
          .filter(item => {
            if (seen.has(item.text)) return false;
            seen.add(item.text);
            return true;
          })
          .slice(0, 12);

      } catch (err) {
        console.warn('Activity stream fetch error:', err);
      }
    },

    // ── Variant navigation ───────────────────────────────────
    prevVariant() {
      const idx = this.variants.indexOf(this.variant);
      this.variant = this.variants[(idx - 1 + this.variants.length) % this.variants.length];
    },

    nextVariant() {
      const idx = this.variants.indexOf(this.variant);
      this.variant = this.variants[(idx + 1) % this.variants.length];
    },

    // ── Formatting helpers ───────────────────────────────────
    formatUptime(seconds) {
      if (!seconds) return '0m';
      const h = Math.floor(seconds / 3600);
      const m = Math.floor((seconds % 3600) / 60);
      return h > 0 ? `${h}h ${m}m` : `${m}m`;
    },

    formatTime(timestamp) {
      if (!timestamp) return '';
      try {
        const d = new Date(timestamp);
        const now = new Date();
        const diff = Math.floor((now - d) / 1000);
        if (diff < 60) return 'just now';
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        return d.toLocaleDateString();
      } catch {
        return '';
      }
    },

    stateClass(agent) {
      return 'state-' + (agent.state || 'offline');
    },

    agentRowClass(agent) {
      return 'cc-agent-row jarvis-state jarvis-state-' + (agent.state || 'offline');
    },

    tierClass(agent) {
      return 'jarvis-tier-' + (agent.tier || 4);
    },

    activityClass(item) {
      const map = {
        task: 'cc-activity-task',
        alert: 'cc-activity-alert',
        escalation: 'cc-activity-escalation',
        info: 'cc-activity-info',
      };
      return map[item.type] || 'cc-activity-info';
    },

    activityDotColor(item) {
      const map = {
        task: 'bg-jarvis-cyan',
        alert: 'bg-red-400',
        escalation: 'bg-orange-400',
        info: 'bg-purple-400',
      };
      return map[item.type] || 'bg-jarvis-muted';
    },

    modelBarColor(model) {
      if (!model.success_rate) return 'bg-jarvis-muted';
      if (model.success_rate >= 0.95) return 'bg-emerald-400';
      if (model.success_rate >= 0.8) return 'bg-amber-400';
      return 'bg-red-400';
    },
  };
}
