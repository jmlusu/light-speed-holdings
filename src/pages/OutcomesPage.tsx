import React from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { PageIntro } from '../components/site/PageIntro';
import { outcomeCategories } from '../data/siteContent';

interface OutcomesPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /outcomes — What changes for clients. We talk about outcomes,
 * not activities. Every category describes specific, measurable shifts.
 */
export const OutcomesPage: React.FC<OutcomesPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="OUTCOMES"
        title="What Changes"
        lead="We talk about outcomes, not activities."
      />

      <section
        id="outcomes"
        aria-labelledby="outcomes-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4 border-t"
      >
        <SectionHeading
          theme={theme}
          eyebrow="MEASURABLE IMPACT"
          title="What Actually Changes"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {outcomeCategories.map((category, idx) => (
            <Reveal key={category.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border h-full ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <h3 className="font-display font-bold text-lg sm:text-xl tracking-tight">
                  {category.title}
                </h3>
                <ul className="mt-5 space-y-2.5">
                  {category.items.map((item, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm leading-relaxed">
                      <span
                        className="mt-1 w-1.5 h-1.5 rounded-full bg-ls-red flex-shrink-0"
                        aria-hidden="true"
                      />
                      <span className={isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}>
                        {item}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default OutcomesPage;
