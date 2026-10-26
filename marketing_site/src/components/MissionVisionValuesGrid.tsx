import React from 'react';
import { ArrowRight } from 'lucide-react';

interface MissionVisionValuesGridProps {
  theme: 'light' | 'dark';
}

export const MissionVisionValuesGrid: React.FC<MissionVisionValuesGridProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

      <div className={isLight ? 'p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all text-ls-grey-dark' : 'p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all text-ls-grey-light-text'}>
        <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
          <span className="w-5 h-5" />
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-ls-emerald" />
          <h3 className={isLight ? 'text-base font-bold font-display text-ls-navy' : 'text-base font-bold font-display text-ls-white'}>Institutional Mission</h3>
        </div>
        <p className={isLight ? 'text-xs leading-relaxed text-ls-grey-dark' : 'text-xs leading-relaxed text-ls-grey-light-text'}>
          To enable enterprises, public institutions, and growth companies across Malawi and African markets to design, build, and govern sovereign AI operating models that eliminate workflow latency and multiply human capability.
        </p>
      </div>

      <div className={isLight ? 'p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all text-ls-grey-dark' : 'p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all text-ls-grey-light-text'}>
        <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
          <span className="w-5 h-5" />
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-ls-emerald" />
          <h3 className={isLight ? 'text-base font-bold font-display text-ls-navy' : 'text-base font-bold font-display text-ls-white'}>Strategic Vision</h3>
        </div>
        <p className={isLight ? 'text-xs leading-relaxed text-ls-grey-dark' : 'text-xs leading-relaxed text-ls-grey-light-text'}>
          To establish LightSpeed Holdings Limited as the premier AI-Native Operator and Partner, recognized across the globe for sovereign agentic systems, regional model laws, operational execution, and category-defining AI enterprise building.
        </p>
      </div>

      <div className={isLight ? 'p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all text-ls-grey-dark' : 'p-6 sm:p-7 rounded-3xl border relative overflow-hidden space-y-3.5 transition-all text-ls-grey-light-text'}>
        <div className="p-3 rounded-2xl bg-ls-red/10 text-ls-red border border-ls-red/30 w-fit">
          <span className="w-5 h-5" />
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-ls-emerald" />
          <h3 className={isLight ? 'text-base font-bold font-display text-ls-navy' : 'text-base font-bold font-display text-ls-white'}>Why LightSpeed</h3>
        </div>
        <p className={isLight ? 'text-xs leading-relaxed text-ls-grey-dark' : 'text-xs leading-relaxed text-ls-grey-light-text'}>
          We are not a generic software outsourcer. We provide concrete architectural proof, OpenCode agent standards, African regulatory alignment, and fiduciary execution.
        </p>
      </div>

    </div>
  );
};
