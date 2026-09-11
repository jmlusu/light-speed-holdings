import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { Reveal } from '../components/Reveal';
import { industries } from '../data/siteContent';

interface IndustriesPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /industries hub. Five verticals where the same governed agentic stack is
 * applied to real, named problems. Honesty statuses differentiate live proof
 * from targeted use cases.
 */
export const IndustriesPage: React.FC<IndustriesPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="WHO WE SERVE"
        title="Industries Where Agentry Works"
        lead="The same governed agentic stack applies across five verticals — government, development & donor organisations, financial services, healthcare, and agriculture. We lead with the problem in each industry, not the technology."
      />

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {industries.map((ind, idx) => (
            <Reveal key={ind.slug} delay={idx * 0.06}>
              <Link
                to={`/industries/${ind.slug}`}
                className={`relative rounded-3xl p-6 sm:p-7 border transition-all h-full flex flex-col justify-between group ${
                  isLight
                    ? 'bg-white/95 border-slate-300 shadow-md hover:shadow-xl hover:-translate-y-0.5'
                    : 'bg-zinc-950/80 border-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-mono text-[10px] font-bold tracking-widest text-ls-red">
                      INDUSTRY
                    </span>
                    <HonestyBadge label={ind.proof} />
                  </div>
                  <h3 className={`text-xl font-bold tracking-tight font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {ind.title}
                  </h3>
                  <p className={`text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
                  }`}>
                    {ind.problem}
                  </p>
                </div>
                <div className={`pt-5 mt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-slate-200' : 'border-white/10'
                }`}>
                  <span className={`text-[11px] font-mono font-bold tracking-widest group-hover:text-ls-red transition-colors ${
                    isLight ? 'text-slate-500' : 'text-zinc-400'
                  }`}>
                    EXPLORE
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      <section className={`px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-20 pb-4 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <SectionHeading
          theme={theme}
          eyebrow="HOW INDUSTRIES ARE CHOSEN"
          title="Real Constraints, Real Problems"
          lead="We did not start from a generic industry list. These five verticals come from where agentic AI demonstrably moves the needle in the SADC economy: compliance-heavy institutions, donor-funded programmes, mobile-money rails, offline-first supply chains, and smallholder agriculture."
        />
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default IndustriesPage;
