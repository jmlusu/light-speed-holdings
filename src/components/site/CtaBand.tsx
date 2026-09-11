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
}

/**
 * Closing CTA band used at the bottom of interior pages. Default copy points
 * at the "Start a Conversation" entry; override per page when a specific CTA
 * (e.g. "Explore AI Company Builder") carries more weight.
 */
export const CtaBand: React.FC<CtaBandProps> = ({
  theme,
  title = 'Start a Conversation',
  text = 'Tell us where your organisation is today — we will be honest about whether we can help, and exactly what it takes to start.',
  ctaLabel = 'Start a Conversation',
  ctaTo = '/contact',
  id,
}) => {
  const isLight = theme === 'light';
  return (
    <section
      id={id}
      aria-label="Call to action"
      className={`px-4 sm:px-8 pt-16 sm:pt-20 pb-24 sm:pb-28 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}
    >
      <Reveal>
        <div
          className={`relative overflow-hidden rounded-3xl p-8 sm:p-12 text-center ${
            isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-100'
          }`}
        >
          {/* Hardware Hex Corner Fasteners */}
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />

          <div className="max-w-2xl mx-auto space-y-5">
            <span className="text-xs font-mono font-bold tracking-widest text-ls-red">
              THE NEXT STEP
            </span>
            <h2 className="text-2xl sm:text-4xl font-black tracking-tight font-display">{title}</h2>
            <p className={`text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              {text}
            </p>
            <Link
              to={ctaTo}
              className="inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:brightness-110"
            >
              {ctaLabel}
              <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </Reveal>
    </section>
  );
};

export default CtaBand;
