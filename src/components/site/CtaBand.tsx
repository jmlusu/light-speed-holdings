import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { Reveal } from '../Reveal';

interface CtaBandProps {
  theme: 'light' | 'dark';
  title?: string;
  text?: string;
  ctaLabel?: string;
  ctaTo?: string;
  id?: string;
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * Closing CTA band used at the bottom of interior pages. Default copy points
 * at the "Start a Conversation" entry; override per page when a specific CTA
 * (e.g. "Explore AI Company Builder") carries more weight.
 */
export const CtaBand: React.FC<CtaBandProps> = ({
  theme,
  title = 'Book an Executive Briefing',
  text = 'Tell us where your organisation is today — we will be honest about whether we can help, and exactly what it takes to start.',
  ctaLabel = 'Book an Executive Briefing',
  ctaTo = '/contact',
  id,
  onRequestBriefing,
}) => {
  const isLight = theme === 'light';
  return (
    <section
      id={id}
      aria-label="Call to action"
      className={`px-4 sm:px-8 pt-16 sm:pt-20 pb-24 sm:pb-28 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-ls-grey-dark/40' : 'border-ls-white/10'
      }`}
    >
      <Reveal>
        <div
          className={`relative overflow-hidden rounded-3xl p-8 sm:p-12 text-center border shadow-xl ${
            isLight
              ? 'bg-ls-white border-ls-grey-dark/30 text-ls-navy'
              : 'bg-ls-navy border-ls-white/15 text-ls-white'
          }`}
        >
          <div className="max-w-2xl mx-auto space-y-5">
            <span className="text-xs font-body font-bold tracking-widest text-ls-red uppercase">
              THE NEXT STEP
            </span>
            <h2 className="text-2xl sm:text-4xl font-black tracking-tight font-display">{title}</h2>
            <p className={`text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
            }`}>
              {text}
            </p>
            <div className="pt-2">
              {onRequestBriefing ? (
                <button
                  type="button"
                  onClick={() => onRequestBriefing(ctaLabel)}
                  className="inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98]"
                >
                  {ctaLabel}
                  <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
                </button>
              ) : (
                <Link
                  to={ctaTo}
                  className="inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98]"
                >
                  {ctaLabel}
                  <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
                </Link>
              )}
              <p className={`text-[11px] font-body mt-3 font-medium ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                We respond to qualified enquiries within two business days.
              </p>
            </div>
          </div>
        </div>
      </Reveal>
    </section>
  );
};

export default CtaBand;
