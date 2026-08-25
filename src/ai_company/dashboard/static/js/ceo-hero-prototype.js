/* CEO Dashboard Hero Prototype — 3 variants switchable via ?variant=
 *
 * Variants:
 *   A: Gauge Hero (large radial) + 4 KPI cards below
 *   B: Horizontal: Gauge left, KPI cards in 2x2 grid right
 *   D: Drill-down: Click gauge → expands to component breakdown
 *
 * Run: Open /mission-control?variant=A (or B, D)
 * Switcher bar appears at bottom in development mode.
 */

function ceoHeroPrototype() {
  return {
    /* State */
    variant: 'A',
    orgHealth: null,
    loading: true,
    error: null,
    expandedComponent: null,
    showSwitcher: false,
    _gauges: {},

    /* Variant definitions */
    variants: [
      { key: 'A', name: 'Gauge Hero' },
      { key: 'B', name: 'Horizontal Split' },
      { key: 'D', name: 'Drill-down' },
    ],

    /* Init */
    async init() {
      this.variant = this.getVariantFromUrl() || 'A';
      this.showSwitcher = this.isDevMode();
      await this.loadOrgHealth();
      this.$nextTick(() => this.renderAllGauges());
    },

    getVariantFromUrl() {
      const params = new URLSearchParams(window.location.search);
      return params.get('variant');
    },

    isDevMode() {
      return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    },

    async loadOrgHealth() {
      this.loading = true;
      try {
        const res = await fetch('/api/v1/kpis/org-health');
        if (!res.ok) throw new Error('Failed to load org health');
        this.orgHealth = await res.json();
      } catch (e) {
        this.error = e.message;
        console.error('Failed to load org health:', e);
      } finally {
        this.loading = false;
        this.$nextTick(() => this.renderAllGauges());
      }
    },

    setVariant(key) {
      this.variant = key;
      this.expandedComponent = null;
      const url = new URL(window.location);
      url.searchParams.set('variant', key);
      window.history.replaceState({}, '', url);
      this.$nextTick(() => this.renderAllGauges());
    },

    nextVariant() {
      const idx = this.variants.findIndex(v => v.key === this.variant);
      const next = this.variants[(idx + 1) % this.variants.length];
      this.setVariant(next.key);
    },

    prevVariant() {
      const idx = this.variants.findIndex(v => v.key === this.variant);
      const prev = this.variants[(idx - 1 + this.variants.length) % this.variants.length];
      this.setVariant(prev.key);
    },

    toggleComponent(comp) {
      this.expandedComponent = this.expandedComponent === comp ? null : comp;
      this.$nextTick(() => this.renderAllGauges());
    },

    getBandClass(band) {
      return {
        green: 'bg-emerald-500',
        amber: 'bg-amber-500',
        red: 'bg-red-500',
      }[band] || 'bg-slate-500';
    },

    getBandTextClass(band) {
      return {
        green: 'text-emerald-400',
        amber: 'text-amber-400',
        red: 'text-red-400',
      }[band] || 'text-slate-400';
    },

    formatScore(score) {
      return typeof score === 'number' ? score.toFixed(0) : '—';
    },

    handleKeydown(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowRight') this.nextVariant();
      if (e.key === 'ArrowLeft') this.prevVariant();
    },

    getComponentLabel(name) {
      const labels = {
        task_success_rate: 'Task Success Rate',
        agent_utilization: 'Agent Utilization',
        cost_efficiency: 'Cost Efficiency',
        error_rate: 'Error Rate (Inverted)',
      };
      return labels[name] || name;
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

    /* Gauge rendering */
    async renderAllGauges() {
      if (!this.orgHealth) return;

      // Main hero gauge
      this.renderRadialGauge('heroGauge', this.orgHealth.score, this.orgHealth.band, 256);
      this.renderRadialGauge('heroGaugeB', this.orgHealth.score, this.orgHealth.band, 192);
      this.renderRadialGauge('heroGaugeD', this.orgHealth.score, this.orgHealth.band, 256);

      // Component sparklines
      if (this.orgHealth.components) {
        for (const comp of this.orgHealth.components) {
          if (comp.value !== null) {
            const trendData = await this.fetchComponentTrend(comp.name);
            const trend = trendData || this.generateTrendData(comp.value);
            this.renderSparkline('spark-' + comp.name, trend);
            this.renderSparkline('spark-b-' + comp.name, trend);
            this.renderSparkline('spark-d-' + comp.name, trend);
            this.renderSparkline('spark-detail-' + comp.name, trend);
          }
        }
      }
    },

    renderRadialGauge(canvasId, score, band, size) {
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
      if (this._gauges[canvasId]) {
        this._gauges[canvasId].destroy();
      }

      this._gauges[canvasId] = new Chart(ctx, {
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

    renderSparkline(canvasId, data) {
      const canvas = document.getElementById(canvasId);
      if (!canvas || typeof Chart === 'undefined') return;

      const ctx = canvas.getContext('2d');

      if (this._gauges[canvasId]) {
        this._gauges[canvasId].destroy();
      }

      this._gauges[canvasId] = new Chart(ctx, {
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

    generateTrendData(currentValue) {
      // Generate 20 pseudo-random points trending toward currentValue
      // NOTE: This is a fallback only. Prefer fetching real history from
      // /api/v1/org-health/trend for live sparklines.
      const points = [];
      let val = currentValue * (0.7 + Math.random() * 0.3);
      for (let i = 0; i < 20; i++) {
        val += (currentValue - val) * 0.1 + (Math.random() - 0.5) * 5;
        val = Math.max(0, Math.min(100, val));
        points.push(val);
      }
      return points;
    },

    async fetchComponentTrend(compName) {
      try {
        const resp = await fetch('/api/v1/org-health/trend?limit=20');
        if (!resp.ok) return null;
        const data = await resp.json();
        if (!data || !Array.isArray(data) || data.length === 0) return null;
        const values = data
          .map(entry => entry.components?.find(c => c.name === compName)?.value)
          .filter(v => v !== null && v !== undefined && !isNaN(v));
        return values.length >= 3 ? values.slice(-20) : null;
      } catch {
        return null;
      }
    },
  };
}

/* Floating prototype switcher bar */
function prototypeSwitcher() {
  return {
    variants: [],
    current: 'A',
    visible: false,

    init() {
      this.variants = [
        { key: 'A', name: 'Gauge Hero' },
        { key: 'B', name: 'Horizontal Split' },
        { key: 'D', name: 'Drill-down' },
      ];
      this.current = this.getVariantFromUrl() || 'A';
      this.visible = this.isDevMode();

      document.addEventListener('keydown', (e) => this.handleKeydown(e));

      // Listen for variant changes from main component
      window.addEventListener('variant-change', (e) => {
        this.current = e.detail.variant;
      });
    },

    getVariantFromUrl() {
      const params = new URLSearchParams(window.location.search);
      return params.get('variant');
    },

    isDevMode() {
      return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    },

    setVariant(key) {
      this.current = key;
      const url = new URL(window.location);
      url.searchParams.set('variant', key);
      window.history.replaceState({}, '', url);
      window.dispatchEvent(new CustomEvent('variant-change', { detail: { variant: key } }));
    },

    nextVariant() {
      const idx = this.variants.findIndex(v => v.key === this.current);
      this.setVariant(this.variants[(idx + 1) % this.variants.length].key);
    },

    prevVariant() {
      const idx = this.variants.findIndex(v => v.key === this.current);
      this.setVariant(this.variants[(idx - 1 + this.variants.length) % this.variants.length].key);
    },

    handleKeydown(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowRight') this.nextVariant();
      if (e.key === 'ArrowLeft') this.prevVariant();
    },
  };
}
