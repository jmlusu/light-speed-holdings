/* ═══════════════════════════════════════════════════════════════
   Light Speed Holdings — CEO Dashboard
   Chart.js integration for KPIs, costs, and analytics
   ═══════════════════════════════════════════════════════════════ */

// ── CSS Token Reader ────────────────────────────────────────
const _style = typeof getComputedStyle !== 'undefined'
  ? getComputedStyle(document.documentElement)
  : null;
const _c = (v) => _style ? _style.getPropertyValue(v).trim() : '';

// ── Chart.js Global Defaults ────────────────────────────────
if (typeof Chart !== 'undefined') {
  Chart.defaults.color = _c('--jarvis-text-muted') || '#94a3b8';
  Chart.defaults.borderColor = 'rgba(34, 211, 238, 0.08)';
  Chart.defaults.font.family = _c('--jarvis-font-display') || "'Rajdhani', 'Inter', system-ui, sans-serif";
  Chart.defaults.font.size = 12;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
  Chart.defaults.plugins.legend.labels.padding = 16;

  /*
   * FIX: Reduced animation duration from 600ms to 300ms.
   * With 15-second polling, long animations overlap with the next
   * data update cycle, causing compounding layout thrashing.
   * 300ms is visually smooth but fast enough to complete before the
   * next poll arrives.
   */
  Chart.defaults.animation.duration = 300;

  Chart.defaults.responsive = true;

  /*
   * FIX: maintainAspectRatio is set to false globally (same as before),
   * but now we pair it with .chart-container CSS that provides explicit
   * height, so charts never collapse to 0px during destroy/recreate.
   */
  Chart.defaults.maintainAspectRatio = false;
}

// ── Color Palette (token-derived) ─────────────────────────
const COLORS = {
  amber:   { bg: 'rgba(251, 191, 36, 0.15)', border: '#fbbf24', point: '#fbbf24' },
  blue:    { bg: 'rgba(59, 130, 246, 0.15)', border: '#3b82f6', point: '#3b82f6' },
  emerald: { bg: 'rgba(52, 211, 153, 0.15)', border: '#34d399', point: '#34d399' },
  red:     { bg: 'rgba(248, 113, 113, 0.15)', border: '#f87171', point: '#f87171' },
  purple:  { bg: 'rgba(168, 85, 247, 0.15)', border: '#a855f7', point: '#a855f7' },
  brand:   { bg: _c('--jarvis-cyan') ? 'rgba(34, 211, 238, 0.15)' : 'rgba(14, 165, 233, 0.15)',
             border: _c('--jarvis-cyan') || '#0ea5e9',
             point: _c('--jarvis-cyan') || '#0ea5e9' },
  slate:   { bg: 'rgba(100, 116, 139, 0.15)', border: '#64748b', point: '#64748b' },
  cyan:    { bg: _c('--jarvis-cyan') ? 'rgba(34, 211, 238, 0.15)' : 'rgba(6, 182, 212, 0.15)',
             border: _c('--jarvis-cyan') || '#06b6d4',
             point: _c('--jarvis-cyan') || '#06b6d4' },
};

const CHART_COLORS = Object.values(COLORS);

// ── Chart Instances ─────────────────────────────────────────
const chartInstances = {};

/**
 * FIX: Improved destroyChart to safely clean up.
 * Chart.js instances must be destroyed before the canvas is reused,
 * otherwise they leak memory and interfere with new instances.
 * We also clear the reference immediately to prevent stale access.
 */
function destroyChart(id) {
  if (chartInstances[id]) {
    try {
      chartInstances[id].destroy();
    } catch (e) {
      console.warn(`[Chart] Error destroying ${id}:`, e);
    }
    delete chartInstances[id];
  }
}

/**
 * FIX: New helper — update chart data in-place when possible,
 * only creating a new Chart when the chart doesn't exist yet.
 * This avoids the destroy → collapse → recreate → expand cycle
 * that was the #2 cause of auto-scrolling.
 *
 * For charts that change structure (e.g., different number of datasets),
 * we still destroy/recreate, but the container prevents layout shift.
 *
 * FIX (no-op guard): if the new data is identical to the current chart
 * data we skip the redraw entirely — poll responses and WS pushes can
 * deliver the same snapshot back-to-back, and every chart.update() is
 * wasted layout work that can nudge scroll position.
 */
function updateOrCreateChart(id, ctx, config) {
  if (chartInstances[id]) {
    // Update existing chart data in-place (no destroy/recreate needed)
    const chart = chartInstances[id];
    const signature = JSON.stringify(config.data || null);
    if (chart._dataSignature === signature) {
      // Nothing changed — skip the redraw to avoid layout churn.
      return chart;
    }
    chart._dataSignature = signature;
    chart.data = config.data;
    // Merge options in case they changed
    Object.assign(chart.options, config.options || {});
    chart.update('none'); // 'none' = no animation on data update
    return chart;
  }
  // First render — create new instance
  const chart = new Chart(ctx, config);
  chart._dataSignature = JSON.stringify(config.data || null);
  chartInstances[id] = chart;
  return chart;
}

// ═══ DASHBOARD CHARTS ════════════════════════════════════════

function updateChartsFromKPIs(kpis, departments) {
  // ── Task Status Doughnut ───────────────────────────────────
  const taskCtx = document.getElementById('taskStatusChart');
  if (taskCtx) {
    const taskStatuses = ['pending', 'in_progress', 'completed', 'failed', 'escalated'];
    const config = {
      type: 'doughnut',
      data: {
        labels: ['Pending', 'In Progress', 'Completed', 'Failed', 'Escalated'],
        datasets: [{
          data: [
            kpis.pending_tasks || 0,
            kpis.in_progress_tasks || 0,
            kpis.completed_tasks || 0,
            kpis.failed_tasks || 0,
            kpis.escalated_tasks || 0,
          ],
          backgroundColor: [
            COLORS.amber.bg,
            COLORS.blue.bg,
            COLORS.emerald.bg,
            COLORS.red.bg,
            COLORS.purple.bg,
          ],
          borderColor: [
            COLORS.amber.border,
            COLORS.blue.border,
            COLORS.emerald.border,
            COLORS.red.border,
            COLORS.purple.border,
          ],
          borderWidth: 2,
          hoverOffset: 12,
        }],
      },
      options: {
        cutout: '65%',
        plugins: {
          legend: { position: 'bottom', labels: { padding: 12, font: { size: 11 } } },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                const value = ctx.parsed;
                const pct = total > 0 ? Math.round((value / total) * 100) : 0;
                return ` ${ctx.label}: ${value} task${value !== 1 ? 's' : ''} (${pct}%)`;
              }
            },
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            titleFont: { size: 12 },
            bodyFont: { size: 11 },
            padding: 8,
            cornerRadius: 6,
          },
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const idx = elements[0].index;
            const status = taskStatuses[idx];
            window.dispatchEvent(new CustomEvent('drilldown:task-status', { detail: { status } }));
          }
        },
      },
    };
    updateOrCreateChart('taskStatus', taskCtx, config);
  }

  // ── Department Load Bar Chart ──────────────────────────────
  const deptCtx = document.getElementById('departmentChart');
  if (deptCtx && departments && departments.length > 0) {
    const config = {
      type: 'bar',
      data: {
        labels: departments.map(d => d.name || d),
        datasets: [{
          label: 'Agents',
          data: departments.map(d => d.total_agents || 0),
          backgroundColor: CHART_COLORS.slice(0, departments.length).map(c => c.bg),
          borderColor: CHART_COLORS.slice(0, departments.length).map(c => c.border),
          borderWidth: 1,
          borderRadius: 6,
        }],
      },
      options: {
        indexAxis: 'y',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                const value = ctx.parsed.x;
                return ` ${ctx.label}: ${value} agent${value !== 1 ? 's' : ''}`;
              }
            },
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            titleFont: { size: 12 },
            bodyFont: { size: 11 },
            padding: 8,
            cornerRadius: 6,
          },
        },
        scales: {
          x: { grid: { display: false }, ticks: { stepSize: 1 } },
          y: { grid: { display: false } },
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const idx = elements[0].index;
            const deptName = departments[idx]?.name || departments[idx];
            window.dispatchEvent(new CustomEvent('drilldown:department', { detail: { name: deptName } }));
          }
        },
      },
    };
    updateOrCreateChart('department', deptCtx, config);
  }
}

// ═══ KPI CHARTS ══════════════════════════════════════════════

function initKPICharts(kpiDepartments, liveKPIData) {
  if (!kpiDepartments || kpiDepartments.length === 0) return;

  // ── KPI Comparison Radar Chart ─────────────────────────────
  const radarCtx = document.getElementById('kpiComparisonChart');
  if (radarCtx) {
    // Normalize KPI values to 0-100 scale for radar
    const datasets = kpiDepartments.slice(0, 4).map((dept, i) => {
      const kpis = dept.kpis || [];
      return {
        label: dept.name,
        data: kpis.map(k => {
          const val = k.current || 0;
          const target = k.target || 100;
          return Math.min((val / target) * 100, 100);
        }),
        backgroundColor: CHART_COLORS[i].bg,
        borderColor: CHART_COLORS[i].border,
        pointBackgroundColor: CHART_COLORS[i].point,
        borderWidth: 2,
      };
    });

    const allKPINames = new Set();
    kpiDepartments.forEach(dept => {
      (dept.kpis || []).forEach(k => allKPINames.add(k.name || k.id));
    });

    const config = {
      type: 'radar',
      data: {
        labels: [...allKPINames].slice(0, 8),
        datasets: datasets,
      },
      options: {
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            grid: { color: 'rgba(51, 65, 85, 0.2)' },
            angleLines: { color: 'rgba(51, 65, 85, 0.2)' },
            pointLabels: { font: { size: 10 } },
            ticks: { display: false },
          },
        },
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 10 }, padding: 8 } },
        },
      },
    };
    updateOrCreateChart('kpiComparison', radarCtx, config);
  }

  // ── KPI Target vs Current Bar Chart ────────────────────────
  const barCtx = document.getElementById('kpiTargetChart');
  if (barCtx) {
    // Flatten all KPIs across departments
    const allKPIs = [];
    kpiDepartments.forEach(dept => {
      (dept.kpis || []).forEach(k => {
        if (k.target !== null && k.target !== undefined) {
          allKPIs.push({
            name: `${dept.name}: ${(k.name || '').substring(0, 15)}`,
            current: k.current || 0,
            target: k.target || 0,
          });
        }
      });
    });

    const limited = allKPIs.slice(0, 10);

    const config = {
      type: 'bar',
      data: {
        labels: limited.map(k => k.name),
        datasets: [
          {
            label: 'Current',
            data: limited.map(k => k.current),
            backgroundColor: COLORS.brand.bg,
            borderColor: COLORS.brand.border,
            borderWidth: 1,
            borderRadius: 4,
          },
          {
            label: 'Target',
            data: limited.map(k => k.target),
            backgroundColor: COLORS.slate.bg,
            borderColor: COLORS.slate.border,
            borderWidth: 1,
            borderRadius: 4,
          },
        ],
      },
      options: {
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 10 } } },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { size: 9 }, maxRotation: 45 },
          },
          y: { grid: { color: 'rgba(51, 65, 85, 0.15)' }, beginAtZero: true },
        },
      },
    };
    updateOrCreateChart('kpiTarget', barCtx, config);
  }
}

// ═══ COMPANY KPI CHART ═══════════════════════════════════════

function initCompanyKPICharts(companyKPIs) {
  if (!companyKPIs || companyKPIs.length === 0) return;

  const ctx = document.getElementById('companyKPIChart');
  if (!ctx) return;

  const limited = companyKPIs.slice(0, 8);

  const config = {
    type: 'bar',
    data: {
      labels: limited.map(k => (k.name || k.id || '').substring(0, 20)),
      datasets: [
        {
          label: 'Current',
          data: limited.map(k => k.current || 0),
          backgroundColor: COLORS.brand.bg,
          borderColor: COLORS.brand.border,
          borderWidth: 1,
          borderRadius: 4,
        },
        {
          label: 'Target',
          data: limited.map(k => k.target || 0),
          backgroundColor: COLORS.slate.bg,
          borderColor: COLORS.slate.border,
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      plugins: {
        legend: { position: 'bottom', labels: { font: { size: 10 } } },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 9 }, maxRotation: 45 },
        },
        y: { grid: { color: 'rgba(51, 65, 85, 0.15)' }, beginAtZero: true },
      },
    },
  };
  updateOrCreateChart('companyKPI', ctx, config);
}

// ═══ COST CHARTS ═════════════════════════════════════════════

function initCostCharts(costSummary, agentCosts, period) {
  // ── Cost Trend Line Chart ──────────────────────────────────
  const trendCtx = document.getElementById('costTrendChart');
  if (trendCtx) {
    // Real cost trend from the API (costSummary.costTrend), never mock data.
    const trend = (costSummary && costSummary.costTrend) || [];
    const sorted = trend
      .slice()
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    const labels = sorted.map(p => {
      const d = new Date(p.timestamp);
      return d.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    });
    const data = sorted.map(p => p.value);

    const config = {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Cost ($)',
          data,
          borderColor: COLORS.brand.border,
          backgroundColor: COLORS.brand.bg,
          fill: true,
          tension: 0.4,
          pointRadius: 2,
          pointHoverRadius: 6,
          borderWidth: 2,
        }],
      },
      options: {
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: { grid: { display: false }, ticks: { font: { size: 10 }, maxTicksLimit: 8 } },
          y: { grid: { color: 'rgba(51, 65, 85, 0.15)' }, beginAtZero: true },
        },
      },
    };
    updateOrCreateChart('costTrend', trendCtx, config);
  }

  // ── Cost per Agent Bar Chart ───────────────────────────────
  const agentCtx = document.getElementById('costAgentChart');
  if (agentCtx && agentCosts && agentCosts.length > 0) {
    const topAgents = agentCosts.slice(0, 10);

    const config = {
      type: 'bar',
      data: {
        labels: topAgents.map(a => a.agent),
        datasets: [{
          label: 'Cost ($)',
          data: topAgents.map(a => a.totalCost),
          backgroundColor: CHART_COLORS.slice(0, topAgents.length).map(c => c.bg),
          borderColor: CHART_COLORS.slice(0, topAgents.length).map(c => c.border),
          borderWidth: 1,
          borderRadius: 6,
        }],
      },
      options: {
        indexAxis: 'y',
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: { grid: { display: false }, beginAtZero: true },
          y: { grid: { display: false }, ticks: { font: { size: 10 } } },
        },
      },
    };
    updateOrCreateChart('costAgent', agentCtx, config);
  }

  // ── F8: Mini cost trend sparkline on the main dashboard ──────
  const miniCtx = document.getElementById('costTrendMini');
  if (miniCtx) {
    const trend = (costSummary && costSummary.costTrend) || [];
    const sorted = trend
      .slice()
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    const labels = sorted.map(p => {
      const d = new Date(p.timestamp);
      return d.toLocaleString([], { hour: '2-digit', minute: '2-digit' });
    });
    const data = sorted.map(p => p.value);

    const config = {
      type: 'line',
      data: {
        labels,
        datasets: [{
          data,
          borderColor: COLORS.brand.border,
          backgroundColor: 'transparent',
          fill: false,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 1.5,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
        scales: {
          x: { display: false },
          y: { display: false, beginAtZero: true },
        },
      },
    };
    updateOrCreateChart('costTrendMini', miniCtx, config);
  }
}
