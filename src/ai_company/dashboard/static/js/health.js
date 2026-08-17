/* ═══════════════════════════════════════════════════════════════
   Health Monitor — Alpine.js component for org health monitoring
   ═══════════════════════════════════════════════════════════════ */

function healthMonitor() {
  return {
    orgHealth: null,
    trend: [],
    anomalies: [],
    loading: true,
    autoRefresh: true,
    trendRange: '24h',
    _refreshTimer: null,
    _trendChart: null,

    async init() {
      await this.loadHealth();
      await this.loadTrend();
      await this.loadAnomalies();

      this.loading = false;

      if (this.autoRefresh) {
        this.startAutoRefresh();
      }
    },

    async loadHealth() {
      try {
        const res = await fetch('/api/v1/org-health');
        if (res.ok) {
          this.orgHealth = await res.json();
        }
      } catch (e) {
        console.error('Failed to load health:', e);
      }
    },

    async loadTrend() {
      try {
        const limit = this.trendRange === '6h' ? 6 : this.trendRange === '24h' ? 24 : 168;
        const res = await fetch(`/api/v1/org-health/trend?limit=${limit}`);
        if (res.ok) {
          this.trend = await res.json();
          this.$nextTick(() => this.renderTrendChart());
        }
      } catch (e) {
        console.error('Failed to load trend:', e);
      }
    },

    async loadAnomalies() {
      try {
        const res = await fetch('/api/v1/org-health/anomalies');
        if (res.ok) {
          this.anomalies = await res.json();
        }
      } catch (e) {
        console.error('Failed to load anomalies:', e);
      }
    },

    renderTrendChart() {
      const canvas = document.getElementById('health-trend-chart');
      if (!canvas || this.trend.length === 0 || typeof Chart === 'undefined') return;

      const ctx = canvas.getContext('2d');

      if (this._trendChart) {
        this._trendChart.destroy();
      }

      const labels = this.trend.map(t => {
        if (!t.timestamp) return '';
        const d = new Date(t.timestamp);
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      });
      const data = this.trend.map(t => t.score ?? 0);

      this._trendChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Org Health Score',
            data,
            borderColor: '#22c55e',
            backgroundColor: 'rgba(34, 197, 94, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
            pointHoverRadius: 5,
            borderWidth: 2,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(7, 11, 20, 0.9)',
              borderColor: 'rgba(34, 211, 238, 0.2)',
              borderWidth: 1,
              titleColor: '#e2e8f0',
              bodyColor: '#94a3b8',
              padding: 10,
              cornerRadius: 8,
            }
          },
          scales: {
            y: {
              min: 0,
              max: 100,
              grid: { color: 'rgba(255,255,255,0.06)' },
              ticks: { color: '#64748b', font: { size: 10 } },
            },
            x: {
              grid: { display: false },
              ticks: { color: '#64748b', font: { size: 10 }, maxRotation: 0 },
            }
          },
          interaction: {
            intersect: false,
            mode: 'index',
          },
        }
      });
    },

    startAutoRefresh() {
      this.stopAutoRefresh();
      this._refreshTimer = setInterval(async () => {
        await this.loadHealth();
        await this.loadAnomalies();
      }, 60000); // 60s
    },

    stopAutoRefresh() {
      if (this._refreshTimer) {
        clearInterval(this._refreshTimer);
        this._refreshTimer = null;
      }
    },

    toggleAutoRefresh() {
      this.autoRefresh = !this.autoRefresh;
      if (this.autoRefresh) {
        this.startAutoRefresh();
      } else {
        this.stopAutoRefresh();
      }
    },

    formatComponentName(name) {
      return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },

    getChangeClass(comp) {
      if (!comp) return 'text-jarvis-muted';
      // Determine color based on value ranges
      if (comp.value >= 80) return 'text-emerald-400';
      if (comp.value >= 50) return 'text-amber-400';
      return 'text-red-400';
    },

    getChangeText(comp) {
      if (!comp) return '';
      if (comp.value >= 80) return 'Healthy';
      if (comp.value >= 50) return 'Fair';
      return 'At Risk';
    },

    getAnomalyClass(severity) {
      const classes = {
        critical: 'bg-red-500/10 border border-red-500/20 text-red-400',
        warning: 'bg-amber-500/10 border border-amber-500/20 text-amber-400',
        info: 'bg-blue-500/10 border border-blue-500/20 text-blue-400',
      };
      return classes[severity] || classes.info;
    },

    getAnomalyIcon(severity) {
      const icons = {
        critical: '\u{1F534}',
        warning: '\u26A0\uFE0F',
        info: '\u{1F4CA}',
      };
      return icons[severity] || '\u{1F4CA}';
    },

    formatTime(isoString) {
      if (!isoString) return '--';
      const date = new Date(isoString);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);

      if (diffMins < 1) return 'just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },

    getHealthBandClass(band) {
      return {
        green: 'text-emerald-400',
        amber: 'text-amber-400',
        red: 'text-red-400',
      }[band] || 'text-slate-400';
    },

    getHealthScoreColor(score) {
      if (score >= 80) return '#22c55e';
      if (score >= 50) return '#f59e0b';
      return '#ef4444';
    },
  };
}
