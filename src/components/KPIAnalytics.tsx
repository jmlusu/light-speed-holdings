import React, { useState } from 'react';
import { 
  LineChart, 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  Target, 
  CheckCircle2, 
  AlertCircle, 
  Calendar,
  Layers
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts';
import { KPIDefinition } from '../types';

interface KPIAnalyticsProps {
  kpis: KPIDefinition[];
}

export const KPIAnalytics: React.FC<KPIAnalyticsProps> = ({ kpis }) => {
  const [selectedDept, setSelectedDept] = useState<string>('All');
  const [selectedKPIId, setSelectedKPIId] = useState<string>(kpis[0]?.id || 'org_health_composite');

  const departments = ['All', 'Executive', 'Technology', 'Finance', 'Operations', 'Customer Success'];

  const filteredKPIs = selectedDept === 'All' 
    ? kpis 
    : kpis.filter(k => k.department.toLowerCase() === selectedDept.toLowerCase());

  const activeKPI = kpis.find(k => k.id === selectedKPIId) || kpis[0];

  const getTrendIcon = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />;
      case 'down':
        return <TrendingDown className="w-3.5 h-3.5 text-rose-400" />;
      default:
        return <Minus className="w-3.5 h-3.5 text-slate-400" />;
    }
  };

  const getStatusBadge = (status: 'good' | 'amber' | 'critical' | 'info') => {
    switch (status) {
      case 'good':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">ON TRACK</span>;
      case 'amber':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">ATTENTION</span>;
      case 'critical':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">CRITICAL</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40">INFO</span>;
    }
  };

  return (
    <div className="space-y-5">
      {/* Top Header & Department Filter */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#0b102f] border border-[#1b2554] p-4 rounded-2xl shadow-md">
        <div>
          <h2 className="text-base font-bold text-white tracking-wider font-display flex items-center gap-2">
            <LineChart className="w-4 h-4 text-[#00bfff]" />
            Departmental KPI Scorecards & Velocity
          </h2>
          <p className="text-justify text-xs text-slate-400">
            Real-time telemetry aggregated from autonomous worker ticks and historical evaluation ndjson streams
          </p>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          {departments.map((dept) => (
            <button
              key={dept}
              onClick={() => setSelectedDept(dept)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer whitespace-nowrap ${
                selectedDept === dept
                  ? 'bg-[#00bfff] text-[#070a40] font-bold'
                  : 'bg-[#10173d] text-slate-400 hover:text-slate-200'
              }`}
            >
              {dept}
            </button>
          ))}
        </div>
      </div>

      {/* Main KPI Graph & Metric Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Left: Interactive Trend Chart */}
        <div className="lg:col-span-2 bg-[#0b102f] border border-[#1b2554] p-5 rounded-2xl shadow-md flex flex-col justify-between">
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-[#1b2554]">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-white font-display">
                    {activeKPI?.name}
                  </h3>
                  {getStatusBadge(activeKPI?.status || 'good')}
                </div>
                <p className="text-justify text-xs text-slate-400 mt-0.5">
                  {activeKPI?.description}
                </p>
              </div>

              <div className="flex items-baseline gap-2 self-start sm:self-center">
                <span className="text-2xl font-black text-white">
                  {activeKPI?.current} {activeKPI?.unit}
                </span>
                {activeKPI?.target && (
                  <span className="text-xs text-slate-400">
                    (Target: {activeKPI.target} {activeKPI.unit})
                  </span>
                )}
              </div>
            </div>

            {/* Chart Area */}
            <div className="h-64 sm:h-72 w-full mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={activeKPI?.history || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="kpiGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00bfff" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#00bfff" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1b2554" vertical={false} />
                  <XAxis dataKey="timestamp" stroke="#64748b" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#64748b" tick={{ fontSize: 11 }} domain={['dataMin - 1', 'dataMax + 1']} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#070b1e',
                      borderColor: '#1e2a58',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '12px'
                    }}
                    formatter={(val: any) => [`${val} ${activeKPI?.unit}`, 'Value']}
                  />
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke="#00bfff"
                    strokeWidth={2.5}
                    fillOpacity={1}
                    fill="url(#kpiGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="pt-3 border-t border-[#1b2554] flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-500" />
              Evaluation Cadence: Daily automated rolling 7-day window
            </span>
            <span className="text-[#00bfff] font-mono">
              Source: dashboard/kpi_history/{activeKPI?.department.toLowerCase()}_history.ndjson
            </span>
          </div>
        </div>

        {/* Right: KPI Selectable Cards List */}
        <div className="space-y-3">
          {filteredKPIs.map((kpi) => {
            const isSelected = kpi.id === activeKPI?.id;
            return (
              <div
                key={kpi.id}
                onClick={() => setSelectedKPIId(kpi.id)}
                className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-[#121c4b] border-[#00bfff] shadow-md shadow-[#00bfff]/10'
                    : 'bg-[#0b102f] hover:bg-[#0e163b] border-[#1b2554]'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <span className="text-[10px] font-mono text-slate-400 tracking-wider">
                      {kpi.department}
                    </span>
                    <h4 className="text-xs font-bold text-white mt-0.5">
                      {kpi.name}
                    </h4>
                  </div>
                  <div className="flex items-center gap-1">
                    {getTrendIcon(kpi.trend)}
                    {getStatusBadge(kpi.status)}
                  </div>
                </div>

                <div className="flex items-baseline justify-between mt-3">
                  <div className="text-lg font-extrabold text-white">
                    {kpi.current} <span className="text-xs font-normal text-slate-400">{kpi.unit}</span>
                  </div>
                  {kpi.target && (
                    <div className="text-[11px] text-slate-400">
                      Target: <span className="text-slate-200 font-semibold">{kpi.target} {kpi.unit}</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
