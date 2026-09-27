import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

interface AboutBandProps {
  theme: 'light' | 'dark';
}

/**
 * Untracked band between chapters 06 and 07 — deliberately has NO id so the
 * chapter-rail IntersectionObserver keeps the previous chapter lit while the
 * 1% scan band passes through it.
 */
export const AboutBand: React.FC<AboutBandProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <section aria-label="About LightSpeed" className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4">
      <div className={`rounded-3xl p-8 sm:p-10 flex flex-col lg:flex-row lg:items-center gap-6 border ${
        isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
      }`}>
        <div className="flex-1 space-y-3">
          <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">ABOUT</span>
          <h2 className="text-xl sm:text-2xl font-black tracking-tight font-display">One Human CEO. 90 AI Agents.</h2>
          <p className={`text-sm leading-relaxed ${
            isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
          }`}>
            We are the AI-native company we sell — governed, audited, and holding every claim to its evidence. Read the mission, the values, and what we promise whom.
          </p>
        </div>
        <Link
          to="/about"
          className="ripple-on inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase border border-ls-red/40 bg-ls-red/10 text-ls-red transition-all cursor-pointer hover:brightness-110"
        >
          About LightSpeed
          <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
        </Link>
      </div>
    </section>
  );
};

export default AboutBand;
