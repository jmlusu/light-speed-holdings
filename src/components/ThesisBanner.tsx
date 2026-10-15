import React from 'react';
import { ArrowRight } from 'lucide-react';

interface ThesisBannerProps {
  theme: 'light' | 'dark';
}

export const ThesisBanner: React.FC<ThesisBannerProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <div className={`rounded-3xl border px-6 sm:px-10 py-8 text-center relative overflow-hidden ${isLight ? 'chassis-milled-light' : 'chassis-milled-dark'}`}>

      <p className="text-[11px] font-body font-bold tracking-[0.35em] text-ls-red uppercase mb-3">
        Our Thesis
      </p>
      <p className="text-2xl sm:text-4xl font-black font-display tracking-tight text-ls-cyan">
        ASPIRE. ACT. ACHIEVE.
      </p>
      <p className={isLight ? 'text-xs sm:text-sm mt-3 max-w-xl mx-auto leading-relaxed text-ls-grey-dark' : 'text-xs sm:text-sm mt-3 max-w-xl mx-auto leading-relaxed text-ls-grey-light-text'>
        Ambition without execution is theatre. We aspire with intent, act with governed speed, and measure what we achieve.
      </p>
    </div>
  );
};
