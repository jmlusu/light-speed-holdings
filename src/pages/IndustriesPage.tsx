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
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">
                      INDUSTRY
                    </span>
                    <HonestyBadge label={ind.proof} />
                  </div>
                  <h3 className={`text-xl font-bold tracking-tight font-display ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}>
                    {ind.title}
                  </h3>
                  <p className={`text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark font-medium' : 'text-ls-grey-light-text'
                  }`}>
                    {ind.problem}
                  </p>
                </div>
                <div className={`pt-5 mt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`text-[11px] font-body font-bold tracking-widest group-hover:text-ls-red transition-colors ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
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
        isLight ? 'border-ls-grey-dark/80' : 'border-ls-grey-dark/80'
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
