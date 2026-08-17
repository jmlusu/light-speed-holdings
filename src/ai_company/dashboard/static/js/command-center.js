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

    // ── Polling ──────────────────────────────────────────────
    _pollTimer: null,

    async init() {
      await this.fetchData();
      this._pollTimer = setInterval(() => this.fetchData(), 15000);

      // Keyboard shortcut: Cmd/Ctrl+K to toggle command bar
      document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          this.showCommandBar = !this.showCommandBar;
          if (this.showCommandBar) {
            this.$nextTick(() => this.$refs.commandInput?.focus());
          }
        }
      });

      // Update URL on variant change
      this.$watch('variant', (v) => {
        const url = new URL(window.location);
        url.searchParams.set('variant', v);
        window.history.replaceState({}, '', url);
      });
    },

    async fetchData() {
      try {
        const [briefingRes, agentsRes] = await Promise.all([
          fetch('/api/v1/briefing').then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/api/v1/agents').then(r => r.ok ? r.json() : null).catch(() => null),
        ]);

        // Executive Briefing — from server-side aggregation
        if (briefingRes) {
          this.briefItems = briefingRes.items || [];
          this.companyHealth = briefingRes.company_health || 85;
          const pipeline = briefingRes.task_pipeline || {};
          this.metrics.activeTasks = (pipeline.in_progress || 0) + (pipeline.pending || 0);
          this.metrics.completedTasks = pipeline.completed || 0;
          this.metrics.openEscalations = briefingRes.summary?.high_priority || 0;
        }

        // Agent workforce
        if (agentsRes && Array.isArray(agentsRes)) {
          this.metrics.totalAgents = agentsRes.length;
          this.workforce = agentsRes.slice(0, 20).map(a => ({
            name: a.name || a.id || 'unknown',
            role: a.department || a.type || 'agent',
            model: a.model || 'default',
            status: a.status || 'idle',
          }));
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

    prevVariant() {
      const idx = this.variants.indexOf(this.variant);
      this.variant = this.variants[(idx - 1 + this.variants.length) % this.variants.length];
    },

    nextVariant() {
      const idx = this.variants.indexOf(this.variant);
      this.variant = this.variants[(idx + 1) % this.variants.length];
    },

    formatUptime(seconds) {
      if (!seconds) return '0m';
      const h = Math.floor(seconds / 3600);
      const m = Math.floor((seconds % 3600) / 60);
      return h > 0 ? `${h}h ${m}m` : `${m}m`;
    },
  };
}
