import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { CTAS } from '../../data/ctas';
import { HomeSection } from './HomeSection';

/** Chapter 07 — Closing CTA: dark overlay, primary CTA, response-time statement. */
export const ClosingCTASection: React.FC<{ theme: 'light' | 'dark' }> = ({ theme }) => {
  const isLight = theme === 'light';
  const ctaLabel = CTAS.primary.label;

  return (
    <HomeSection id="closing-cta" label="Closing CTA" theme={theme} scrim={false}>
      <section className="relative py-24 sm:py-32 px-4 sm:px-8 lg:px-10 max-w-7xl mx-auto bg-[url('/hero-background.jpg')] bg-no-repeat bg-center bg-black/60 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/60 to-transparent opacity-90 sm:opacity-95" />

        <div className="relative flex flex-col sm:flex-row items-center justify-center text-center gap-4 sm:gap-0 sm:w-full">

          <div className="w-full sm:w-full sm:max-w-2xl text-center sm:text-left">
            <h2 className={`text-3xl sm:text-5xl md:text-6xl lg:text-[3.5rem] font-black tracking-tight leading-[1.02] ${isLight ? 'text-ls-white' : 'text-ls-white'}`}>
              Ready to Turn Your Vision Into an AI-Native Reality?
            </h2>

            <p className={`mt-4 text-lg sm:text-xl md:text-2xl font-semibold leading-relaxed ${isLight ? 'text-ls-white/90' : 'text-ls-white/80'}`}>
              Share a brief of up to 500 words. We will assess feasibility, outline governance, and tell you plainly what it takes to start.
            </p>
          </div>

          <div className="w-full sm:w-auto flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              to={CTAS.primary.to}
              className={`ripple-on inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-ls-red hover:bg-[#d62837] text-ls-white shadow-lg shadow-ls-red/30 hover:shadow-ls-red/50 transition-all cursor-pointer active:scale-[0.98]`}
            >
              <span>{ctaLabel}</span>
              <span aria-hidden="true">→</span>
            </Link>

            <Link
              to="/what-we-do"
              className={`px-5 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs cursor-pointer active:scale-[0.98] ${isLight
                  ? 'border-ls-red text-ls-red bg-transparent hover:bg-ls-red/10 shadow-xs'
                  : 'border-ls-cyan text-ls-cyan bg-transparent hover:bg-ls-cyan/10 hover:border-ls-cyan shadow-sm shadow-ls-cyan/20'}
                }`}
            >
              <span>How It Works</span>
            </Link>
          </div>
        </div>
      </section>
    </HomeSection>
  );
};

export default ClosingCTASection;
