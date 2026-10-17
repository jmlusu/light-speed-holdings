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
    componentTrends: {},
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
        const res = await fetch('/api/v1/org-health');
        if (!res.ok) throw new Error('Failed to load org health');
        this.orgHealth = await res.json();
        await this.loadComponentTrends();
      } catch (e) {
        this.error = e.message;
        console.error('Failed to load org health:', e);
      } finally {
        this.loading = false;
        this.$nextTick(() => this.renderAllGauges());
      }
    },

    async loadComponentTrends() {
      if (!this.orgHealth || !this.orgHealth.components) return;
      const promises = this.orgHealth.components.map(async (comp) => {
        try {
          const res = await fetch(
            `/api/v1/org-health/components/trend?component=${comp.name}&limit=30`
          );
          if (res.ok) {
            const data = await res.json();
            if (data && data.length > 0) {
              this.componentTrends[comp.name] = data.map((d) => d.score);
            }
          }
        } catch (e) {
          console.warn(`Failed to load trend for ${comp.name}:`, e);
        }
      });
      await Promise.allSettled(promises);
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
        task_success_rate: 'Task Success',
        agent_utilization: 'Agent Util.',
        cost_efficiency: 'Cost Eff.',
        error_rate: 'Error Rate',
        task_throughput: 'Throughput',
        escalation_rate: 'Escalation',
        security_posture: 'Security',
        strategic_alignment: 'Strategic',
      };
      return labels[name] || name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },

    getComponentDescription(name) {
      const descs = {
        task_success_rate: 'Ratio of completed tasks to total tasks (30d)',
        agent_utilization: 'Active agents vs registered agents (30d)',
        cost_efficiency: 'Budget utilization vs spend',
        error_rate: 'Error/exception rate across operations (inverted)',
        task_throughput: 'Tasks completed per day normalized to target',
        escalation_rate: 'Escalation rate across tasks (inverted)',
        security_posture: 'Audit trail health and compliance indicators',
        strategic_alignment: 'Tasks mapped to active goals and departments',
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

      // Component sparklines with real trend data
      if (this.orgHealth.components) {
        for (const comp of this.orgHealth.components) {
          if (comp.value !== null) {
            const trendData = this.componentTrends[comp.name] || null;
            this.renderSparkline('spark-' + comp.name, trendData);
            this.renderSparkline('spark-b-' + comp.name, trendData);
            this.renderSparkline('spark-d-' + comp.name, trendData);
            this.renderSparkline('spark-detail-' + comp.name, trendData);
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
      if (!canvas) return;

      if (!data || data.length === 0) {
        canvas.style.display = 'none';
        const parent = canvas.parentNode;
        if (parent && !parent.querySelector('.sparkline-placeholder')) {
          const placeholder = document.createElement('span');
          placeholder.className = 'sparkline-placeholder text-xs text-slate-500 italic flex items-center justify-center h-full w-full';
          placeholder.textContent = 'No history';
          parent.appendChild(placeholder);
        }
        return;
      }

      if (typeof Chart === 'undefined') return;

      // Remove any existing placeholder
      const parent = canvas.parentNode;
      if (parent) {
        const existing = parent.querySelector('.sparkline-placeholder');
        if (existing) existing.remove();
      }
      canvas.style.display = '';

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
