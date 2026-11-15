import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { Reveal } from '../Reveal';
import { CTAS } from '../../data/ctas';
import { trackJourneyEvent } from '../../hooks/useJourneyEvents';

interface CtaBandProps {
  theme: 'light' | 'dark';
  title?: string;
  text?: string;
  ctaLabel?: string;
  ctaTo?: string;
  id?: string;
  onRequestBriefing?: (summary?: string) => void;
  ctaLevel?: 'primary' | 'secondary' | 'lowFriction';
}

/**
 * Closing CTA band used at the bottom of interior pages. Default copy points
 * at the "Start a Conversation" entry; override per page when a specific CTA
 * (e.g. "Explore AI Company Builder") carries more weight.
 */
export const CtaBand: React.FC<CtaBandProps> = ({
  theme,
  title = CTAS.primary.label,
  text = 'Tell us where your organisation is today. We will be honest about whether we can help, and exactly what it takes to start.',
  ctaLabel = CTAS.primary.label,
  ctaTo = CTAS.primary.to,
  id,
  onRequestBriefing,
  ctaLevel = 'primary',
}) => {
  const isLight = theme === 'light';
  const ctaClasses = {
    primary:
      'btn-milled btn-milled-primary inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase text-ls-white cursor-pointer',
    secondary:
      'btn-milled btn-milled-secondary inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase cursor-pointer',
    lowFriction:
      'btn-milled inline-flex items-center justify-center gap-2.5 px-6 py-2.5 rounded-full font-bold text-xs tracking-wider text-ls-cyan bg-ls-cyan/10 hover:bg-ls-cyan/20 cursor-pointer',
  }[ctaLevel];

  const trackCta = (): void => {
    trackJourneyEvent({
      eventType: 'cta_clicked',
      cta: ctaLabel,
      journeyStage: 'intent',
      metadata: onRequestBriefing ? { target: 'briefing' } : { to: ctaTo },
    });
  };

  return (
    <section
      id={id}
      aria-label="Call to action"
      className={`px-6 lg:px-12 pt-16 sm:pt-20 pb-24 sm:pb-28 max-w-7xl mx-auto w-full`}
    >
      <Reveal>
        <div
          className={`relative overflow-hidden rounded-3xl p-8 sm:p-14 text-center shadow-2xl ${
            isLight
              ? 'bg-ls-white text-ls-navy'
              : 'bg-ls-navy text-ls-white'
          }`}
        >
          {/* Subtle Architectural Visual Overlay */}
          <div className="absolute inset-0 pointer-events-none select-none opacity-20 dark:opacity-25 z-0">
            <img
              src="/src/assets/images/pharos_cta_pure_1793817814419.jpg"
              alt="Architectural visualization of research-to-enterprise bridge"
              className="w-full h-full object-cover object-center filter saturate-110"
              loading="lazy"
            />
            <div className={`absolute inset-0 ${
              isLight
                ? 'bg-gradient-to-t from-white via-white/85 to-white/95'
                : 'bg-gradient-to-t from-[#070A40] via-[#070A40]/80 to-[#070A40]/90'
            }`} />
          </div>

          <div className="max-w-2xl mx-auto space-y-5 relative z-10">
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
                  onClick={() => {
                    trackCta();
                    onRequestBriefing(ctaLabel);
                  }}
                  className={ctaClasses}
                >
                  {ctaLabel}
                  <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
                </button>
              ) : (
                <Link
                  to={ctaTo}
                  className={ctaClasses}
                  onClick={trackCta}
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
