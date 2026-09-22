import React from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { PageIntro } from '../components/site/PageIntro';
import { deliverables } from '../data/siteContent';

interface DeliverablesPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /deliverables — What clients actually receive. Every engagement
 * produces tangible deliverables, grouped by engagement type.
 */
export const DeliverablesPage: React.FC<DeliverablesPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="DELIVERABLES"
        title="What You Actually Receive"
        lead="Clients need to understand what they get. Every engagement produces tangible deliverables."
      />

      <section
        id="deliverables"
        aria-labelledby="deliverables-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4 border-t"
      >
        <SectionHeading
          theme={theme}
          eyebrow="ENGAGEMENT TYPES"
          title="Tangible Outputs by Engagement"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {deliverables.map((group, idx) => (
            <Reveal key={group.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border h-full ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl" aria-hidden="true">{group.icon}</span>
                  <div>
                    <h3 className="font-display font-bold text-lg sm:text-xl tracking-tight">
                      {group.engagement}
                    </h3>
                  </div>
                </div>
                <ul className="mt-5 space-y-2.5">
                  {group.deliverables.map((item, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm leading-relaxed">
                      <span
                        className={`mt-1 w-1.5 h-1.5 rounded-full flex-shrink-0 ${
                          isLight ? 'bg-ls-red' : 'bg-ls-red'
                        }`}
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

export default DeliverablesPage;
