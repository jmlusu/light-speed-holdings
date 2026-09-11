import React from 'react';
import { Globe2 } from 'lucide-react';
import { SectorExpertiseSection } from '../components/SectorExpertiseSection';

interface IndustriesPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const IndustriesPage: React.FC<IndustriesPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <Globe2 className="w-3.5 h-3.5" />
          <span>SECTOR EXPERTISE</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
          Industry-Grade Delivery Across SADC
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
          Built for regulated African environments where data sovereignty is non-negotiable and operational failure has real-world consequences. Seven sector verticals — all positioned honestly. None of these sectors represents a paid client deployment; they are pilot, fieldable, or in active development.
        </p>
      </header>

      <SectorExpertiseSection theme={theme} />
    </>
  );
};

export default IndustriesPage;
