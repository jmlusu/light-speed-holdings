/* ═══════════════════════════════════════════════════════════════
   Light Speed Holdings — CEO Dashboard
   Chart.js integration for KPIs, costs, and analytics
   ═══════════════════════════════════════════════════════════════ */

// ── Chart.js Global Defaults ────────────────────────────────
if (typeof Chart !== 'undefined') {
  Chart.defaults.color = '#94a3b8';
  Chart.defaults.borderColor = 'rgba(51, 65, 85, 0.3)';
  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
  Chart.defaults.font.size = 12;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
  Chart.defaults.plugins.legend.labels.padding = 16;
  Chart.defaults.animation.duration = 600;
  Chart.defaults.responsive = true;
  Chart.defaults.maintainAspectRatio = false;
}

// ── Color Palette ───────────────────────────────────────────
const COLORS = {
  amber:   { bg: 'rgba(251, 191, 36, 0.15)', border: '#fbbf24', point: '#fbbf24' },
  blue:    { bg: 'rgba(59, 130, 246, 0.15)', border: '#3b82f6', point: '#3b82f6' },
  emerald: { bg: 'rgba(16, 185, 129, 0.15)', border: '#10b981', point: '#10b981' },
  red:     { bg: 'rgba(239, 68, 68, 0.15)', border: '#ef4444', point: '#ef4444' },
  purple:  { bg: 'rgba(168, 85, 247, 0.15)', border: '#a855f7', point: '#a855f7' },
  brand:   { bg: 'rgba(14, 165, 233, 0.15)', border: '#0ea5e9', point: '#0ea5e9' },
  slate:   { bg: 'rgba(100, 116, 139, 0.15)', border: '#64748b', point: '#64748b' },
  cyan:    { bg: 'rgba(6, 182, 212, 0.15)', border: '#06b6d4', point: '#06b6d4' },
};

const CHART_COLORS = Object.values(COLORS);

// ── Chart Instances ─────────────────────────────────────────
const chartInstances = {};

function destroyChart(id) {
  if (chartInstances[id]) {
    chartInstances[id].destroy();
    delete chartInstances[id];
  }
}

// ═══ DASHBOARD CHARTS ════════════════════════════════════════

function updateChartsFromKPIs(kpis, departments) {
  // ── Task Status Doughnut ───────────────────────────────────
  const taskCtx = document.getElementById('taskStatusChart');
  if (taskCtx) {
    destroyChart('taskStatus');
    chartInstances['taskStatus'] = new Chart(taskCtx, {
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
          hoverOffset: 8,
        }],
      },
      options: {
        cutout: '65%',
        plugins: {
          legend: { position: 'bottom', labels: { padding: 12, font: { size: 11 } } },
        },
      },
    });
  }

  // ── Department Load Bar Chart ──────────────────────────────
  const deptCtx = document.getElementById('departmentChart');
  if (deptCtx && departments && departments.length > 0) {
    destroyChart('department');
    chartInstances['department'] = new Chart(deptCtx, {
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
        },
        scales: {
          x: { grid: { display: false }, ticks: { stepSize: 1 } },
          y: { grid: { display: false } },
        },
      },
    });
  }
}

// ═══ KPI CHARTS ══════════════════════════════════════════════

function initKPICharts(kpiDepartments, liveKPIData) {
  if (!kpiDepartments || kpiDepartments.length === 0) return;

  // ── KPI Comparison Radar Chart ─────────────────────────────
  const radarCtx = document.getElementById('kpiComparisonChart');
  if (radarCtx) {
    destroyChart('kpiComparison');

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

    chartInstances['kpiComparison'] = new Chart(radarCtx, {
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
    });
  }

  // ── KPI Target vs Current Bar Chart ────────────────────────
  const barCtx = document.getElementById('kpiTargetChart');
  if (barCtx) {
    destroyChart('kpiTarget');

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

    chartInstances['kpiTarget'] = new Chart(barCtx, {
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
    });
  }
}

// ═══ COST CHARTS ═════════════════════════════════════════════

function initCostCharts(costSummary, agentCosts, period) {
  // ── Cost Trend Line Chart ──────────────────────────────────
  const trendCtx = document.getElementById('costTrendChart');
  if (trendCtx) {
    destroyChart('costTrend');

    // Generate mock trend data (in production, this would come from history)
    const labels = [];
    const data = [];
    const now = new Date();
    const points = period === 'daily' ? 24 : period === 'weekly' ? 7 : 30;

    for (let i = points - 1; i >= 0; i--) {
      const d = new Date(now);
      if (period === 'daily') {
        d.setHours(d.getHours() - i);
        labels.push(d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
      } else if (period === 'weekly') {
        d.setDate(d.getDate() - i);
        labels.push(d.toLocaleDateString([], { weekday: 'short' }));
      } else {
        d.setDate(d.getDate() - i);
        labels.push(d.toLocaleDateString([], { month: 'short', day: 'numeric' }));
      }
      data.push(+(Math.random() * 0.1 + 0.01).toFixed(4));
    }

    chartInstances['costTrend'] = new Chart(trendCtx, {
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
    });
  }

  // ── Cost per Agent Bar Chart ───────────────────────────────
  const agentCtx = document.getElementById('costAgentChart');
  if (agentCtx && agentCosts && agentCosts.length > 0) {
    destroyChart('costAgent');

    const topAgents = agentCosts.slice(0, 10);

    chartInstances['costAgent'] = new Chart(agentCtx, {
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
    });
  }
}
