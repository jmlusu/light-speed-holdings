import React from 'react';
import { 
  BadgePercent, 
  DollarSign, 
  Cpu, 
  TrendingDown, 
  PieChart as PieIcon, 
  ShieldCheck, 
  Zap, 
  Layers
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts';
import { ModelTierConfig } from '../types';

interface FinanceCostsProps {
  modelTiers: ModelTierConfig[];
}

export const FinanceCosts: React.FC<FinanceCostsProps> = ({ modelTiers }) => {
  const totalTokens = modelTiers.reduce((acc, t) => acc + t.tokensProcessed, 0);
  const totalCost = modelTiers.reduce((acc, t) => acc + t.totalCost, 0);
  const totalRequests = modelTiers.reduce((acc, t) => acc + t.requestsCount, 0);

  const budgetCategories = [
    { name: 'Product Development', budget: 5500000, spent: 48.20, departments: 6, color: '#00bfff' },
    { name: 'Operations', budget: 4500000, spent: 34.50, departments: 6, color: '#e63946' },
    { name: 'Growth & BD', budget: 3000000, spent: 22.14, departments: 5, color: '#10b981' },
    { name: 'Infrastructure & Security', budget: 2000000, spent: 12.80, departments: 3, color: '#8b5cf6' }
  ];

  const chartData = modelTiers.map(tier => ({
    name: tier.name.split(':')[0],
    cost: tier.totalCost,
    tokens: (tier.tokensProcessed / 1000000).toFixed(1),
    requests: tier.requestsCount
  }));

  const COLORS = ['#00bfff', '#3b82f6', '#8b5cf6'];

  return (
    <div className="space-y-5">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#0b102f] border border-[#1b2554] p-4 rounded-2xl shadow-md">
        <div>
          <h2 className="text-base font-bold text-white tracking-wider font-display flex items-center gap-2">
            <BadgePercent className="w-4 h-4 text-[#00bfff]" />
            Fiscal Health, LLM Inference Spend & Model Tiers
          </h2>
          <p className="text-justify text-xs text-slate-400">
            Multi-model dynamic routing architecture enforcing cost caps and token efficiency across 144 agent cards
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3 py-1.5 rounded-lg bg-[#0e163b] border border-[#1e2a58] text-right">
            <span className="text-[10px] text-slate-400 tracking-wider block">Total Allocated Budget</span>
            <span className="text-sm font-bold text-white">$15,000,000.00</span>
          </div>
          <div className="px-3 py-1.5 rounded-lg bg-[#0e163b] border border-[#1e2a58] text-right">
            <span className="text-[10px] text-slate-400 tracking-wider block">Total LLM Spend YTD</span>
            <span className="text-sm font-bold text-emerald-400">${totalCost.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* 3 Model Routing Tiers Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {modelTiers.map((tier, idx) => (
          <div
            key={tier.tier}
            className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md flex flex-col justify-between relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-24 h-24 bg-[#00bfff]/5 rounded-full blur-xl pointer-events-none"></div>

            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white tracking-wider">
                  {tier.name}
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#131d47] text-[#00bfff] border border-[#00bfff]/30">
                  {tier.costRange}
                </span>
              </div>

              <div className="my-3">
                <div className="text-2xl font-black text-white">${tier.totalCost.toFixed(2)}</div>
                <div className="text-xs text-slate-400 mt-0.5">
                  {(tier.tokensProcessed / 1000000).toFixed(1)}M tokens processed • {tier.requestsCount.toLocaleString()} tasks
                </div>
              </div>

              <div className="space-y-1.5 pt-2 border-t border-[#18234e] text-xs">
                <span className="text-[11px] font-semibold text-slate-400 block">Primary Model Providers:</span>
                <div className="flex flex-wrap gap-1">
                  {tier.primaryProviders.map((prov, pIdx) => (
                    <span key={pIdx} className="text-[10px] px-1.5 py-0.5 rounded bg-[#070b20] text-slate-300 border border-slate-800">
                      {prov}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-4 pt-2 border-t border-[#18234e] flex items-center justify-between text-[11px] text-slate-400">
              <span>Share of total volume:</span>
              <span className="font-bold text-white">
                {((tier.tokensProcessed / totalTokens) * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Middle Row: Spend Chart & Department Budget Allocation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Spend Comparison Chart */}
        <div className="bg-[#0b102f] border border-[#1b2554] p-5 rounded-2xl shadow-md">
          <h3 className="text-sm font-bold text-white tracking-wider font-display mb-1">
            Cost by Routing Tier ($ USD)
          </h3>
          <p className="text-justify text-xs text-slate-400 mb-4">
            Tier 1 & Tier 2 handle 88.5% of autonomous volume, minimizing reliance on expensive frontier reasoning models
          </p>

          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1b2554" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#070b1e',
                    borderColor: '#1e2a58',
                    borderRadius: '8px',
                    color: '#fff',
                    fontSize: '12px'
                  }}
                  formatter={(val: any) => [`$${val}`, 'Spend']}
                />
                <Bar dataKey="cost" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Department Budget Allocation */}
        <div className="bg-[#0b102f] border border-[#1b2554] p-5 rounded-2xl shadow-md flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-white tracking-wider font-display mb-1">
              Departmental Budget Categories
            </h3>
            <p className="text-justify text-xs text-slate-400 mb-4">
              Authorized budget limits by category from company/departments.yaml
            </p>

            <div className="space-y-3">
              {budgetCategories.map((cat) => (
                <div key={cat.name} className="p-3 rounded-xl bg-[#0e163b] border border-[#1e2a58] text-xs">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-semibold text-white">{cat.name}</span>
                    <span className="font-bold text-slate-200">
                      ${(cat.budget / 1000000).toFixed(1)}M Cap
                    </span>
                  </div>

                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full" 
                      style={{ width: `${Math.min(100, (cat.spent / 100) * 100)}%`, backgroundColor: cat.color }}
                    ></div>
                  </div>

                  <div className="flex items-center justify-between mt-1 text-[11px] text-slate-400">
                    <span>{cat.departments} active departments</span>
                    <span className="text-emerald-400 font-medium">${cat.spent.toFixed(2)} spent</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#18234e] text-xs text-slate-400 flex items-center justify-between">
            <span className="flex items-center gap-1 text-emerald-400">
              <ShieldCheck className="w-3.5 h-3.5" />
              Strict budget guardrails active
            </span>
            <span className="font-mono text-[10px]">CFO Signoff Required &gt; $5,000</span>
          </div>
        </div>
      </div>
    </div>
  );
};
