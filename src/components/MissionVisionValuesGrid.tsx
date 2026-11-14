import React from 'react';
import { Icon3D } from './common';

interface MissionVisionValuesGridProps {
  theme: 'light' | 'dark';
}

export const MissionVisionValuesGrid: React.FC<MissionVisionValuesGridProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

      <div className={`p-6 sm:p-7 border relative overflow-hidden space-y-3.5 transition-colors ${
        isLight ? 'bg-white border-slate-300 shadow-[4px_4px_0px_#070A40]' : 'bg-[#070A40] border-white/20 shadow-[4px_4px_0px_#00BFFF]'
      }`}>
        <div className="flex items-center shrink-0">
          <Icon3D name="target" size="md" isInteractive />
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-ls-cyan shadow-[0_0_6px_#00BFFF]" />
          <h3 className={`text-base font-bold font-sans uppercase tracking-wider ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Institutional Mission
          </h3>
        </div>
        <p className={`text-xs leading-relaxed font-sans ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
          To enable enterprises, public institutions, and growth companies across Malawi and African markets to design, build, and govern sovereign AI operating models that eliminate workflow latency and multiply human capability.
        </p>
      </div>

      <div className={`p-6 sm:p-7 border relative overflow-hidden space-y-3.5 transition-colors ${
        isLight ? 'bg-white border-slate-300 shadow-[4px_4px_0px_#070A40]' : 'bg-[#070A40] border-white/20 shadow-[4px_4px_0px_#00BFFF]'
      }`}>
        <div className="flex items-center shrink-0">
          <Icon3D name="compass" size="md" isInteractive />
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-ls-cyan shadow-[0_0_6px_#00BFFF]" />
          <h3 className={`text-base font-bold font-sans uppercase tracking-wider ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Strategic Vision
          </h3>
        </div>
        <p className={`text-xs leading-relaxed font-sans ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
          To establish LightSpeed Holdings Limited as the premier AI-Native Operator and Partner, recognized across the globe for sovereign agentic systems, regional model laws, operational execution, and category-defining AI enterprise building.
        </p>
      </div>

      <div className={`p-6 sm:p-7 border relative overflow-hidden space-y-3.5 transition-colors ${
        isLight ? 'bg-white border-slate-300 shadow-[4px_4px_0px_#070A40]' : 'bg-[#070A40] border-white/20 shadow-[4px_4px_0px_#00BFFF]'
      }`}>
        <div className="flex items-center shrink-0">
          <Icon3D name="safe" size="md" isInteractive />
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-ls-cyan shadow-[0_0_6px_#00BFFF]" />
          <h3 className={`text-base font-bold font-sans uppercase tracking-wider ${isLight ? 'text-ls-navy' : 'text-white'}`}>
            Why LightSpeed
          </h3>
        </div>
        <p className={`text-xs leading-relaxed font-sans ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
          We are not a generic software outsourcer. We provide concrete architectural proof, OpenCode agent standards, African regulatory alignment, and fiduciary execution.
        </p>
      </div>

    </div>
  );
};

export default MissionVisionValuesGrid;
