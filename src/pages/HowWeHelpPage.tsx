import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { TONE_STYLES } from '../data/siteContent';
import { clientProblems, engagementModels } from '../data/siteContent';

interface HowWeHelpPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /how-we-help — Combined page that surfaces the client problem finder
 * ("You may be here because...") alongside the engagement models.
 * Every card carries its honesty status — proven, pilot, fieldable, or development.
 */
export const HowWeHelpPage: React.FC<HowWeHelpPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="HOW WE HELP"
        title="You May Be Here Because..."
        lead="Recognize yourself. Every page on this site starts with a problem — and every problem has a path to a solution."
      />

      {/* ── Client Problems ──────────────────────────── */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-8" id="problems">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {clientProblems.map((problem, idx) => (
            <Reveal key={problem.id} delay={idx * 0.06}>
              <Link
                to={problem.to}
                className={`relative rounded-3xl p-6 sm:p-7 border transition-all h-full flex flex-col justify-between group ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">
                      {problem.trigger}
                    </span>
                    <HonestyBadge label={problem.proof} />
                  </div>
                  <h3 className={`text-lg font-bold tracking-tight font-display ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    {problem.heading}
                  </h3>
                  <p className={`text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
                  }`}>
                    {problem.subtext}
                  </p>
                </div>
                <div className={`pt-5 mt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`text-[11px] font-body font-bold tracking-widest group-hover:text-ls-red transition-colors ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    {problem.solution}
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ── Engagement Models ────────────────────────── */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full py-16 sm:py-20 border-t" id="engagement">
        <SectionHeading
          theme={theme}
          eyebrow="ENGAGEMENT MODELS"
          title="How You Can Work With Us"
          lead="Not every engagement requires a large consulting project. Choose the model that fits your needs."
        />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {engagementModels.map((model, idx) => (
            <Reveal key={model.id} delay={idx * 0.06}>
              <div
                className={`relative rounded-3xl p-6 sm:p-7 border transition-all h-full flex flex-col ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
                }`}
              >
                <div className="space-y-4 flex-1">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className={`text-lg font-bold tracking-tight font-display ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}>
                      {model.name}
                    </h3>
                    <HonestyBadge label={model.proof} />
                  </div>
                  <p className={`text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
                  }`}>
                    {model.description}
                  </p>
                  <div className="pt-2">
                    <span className={`text-[11px] font-body font-bold tracking-widest ${
                      isLight ? 'text-ls-red' : 'text-ls-red'
                    }`}>
                      Typical duration: {model.typicalDuration}
                    </span>
                  </div>
                  <ul className="space-y-1.5">
                    {model.deliverables.map((deliverable) => (
                      <li key={deliverable} className={`flex items-start gap-2 text-xs sm:text-sm leading-relaxed ${
                        isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
                      }`}>
                        <span className="text-ls-red font-body font-black" aria-hidden="true">✓</span>
                        {deliverable}
                      </li>
                    ))}
                  </ul>
                  <div className="pt-3">
                    <span className={`text-[11px] font-body font-medium ${
                      isLight ? 'text-ls-grey-dark/70' : 'text-ls-grey-light-text/70'
                    }`}>
                      Best for: {model.bestFor}
                    </span>
                  </div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default HowWeHelpPage;
