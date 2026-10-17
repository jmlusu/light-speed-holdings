import React from 'react';
import { kpis } from '../../data/kpis';

interface KPISectionProps {
  theme: 'light' | 'dark';
}

export const KPISection: React.FC<KPISectionProps> = ({ theme }) => {
  const isDark = theme === 'dark';
  const sectionBg = isDark ? 'bg-[#0A1128] text-white' : 'bg-[#F7F8F9] text-[#0A1128]';
  const cardBg = isDark ? 'bg-white/5 border-white/10' : 'bg-white border-slate-200';

  return (
    <section className={`py-16 sm:py-24 ${sectionBg}`} aria-labelledby="kpi-heading">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-bold tracking-[0.2em] text-ls-cyan uppercase">
            Operational Metrics
          </p>
          <h2 id="kpi-heading" className="mt-3 text-3xl font-black font-display sm:text-4xl">
            Measurable Outcomes, Governed Execution
          </h2>
          <p className="mt-4 text-lg opacity-80">
            Every agent action and engagement is tracked against strict operational KPIs, ensuring velocity never compromises governance.
          </p>
        </div>
        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {kpis.map((kpi) => (
            <div
              key={kpi.label}
              className={`p-6 rounded-lg border ${cardBg} transition-all hover:shadow-md`}
            >
              <p className="text-xs font-bold uppercase tracking-wider opacity-70">
                {kpi.label}
              </p>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-3xl font-black font-display">{kpi.value}</span>
                {kpi.delta && (
                  <span className="text-sm font-bold text-ls-cyan">{kpi.delta}</span>
                )}
              </div>
              {kpi.description && (
                <p className="mt-3 text-sm opacity-80 leading-relaxed">
                  {kpi.description}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default KPISection;
