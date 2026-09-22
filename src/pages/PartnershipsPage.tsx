import React from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { PageIntro } from '../components/site/PageIntro';
import { partnerships } from '../data/siteContent';

interface PartnershipsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /partnerships — Our ecosystem of genuine relationships with
 * technology partners, research institutions, and implementation partners.
 */
export const PartnershipsPage: React.FC<PartnershipsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="OUR ECOSYSTEM"
        title="Partnerships and Ecosystem"
        lead="Genuine relationships with technology partners, research institutions, and implementation partners."
      />

      <section
        id="partnerships"
        aria-labelledby="partnerships-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4 border-t"
      >
        <SectionHeading
          theme={theme}
          eyebrow="ECO SYSTEM"
          title="Who We Work With"
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {partnerships.map((category, idx) => (
            <Reveal key={category.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border h-full ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <h3 className="font-display font-bold text-lg sm:text-xl tracking-tight">
                  {category.name}
                </h3>
                <p className={`mt-2 text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {category.description}
                </p>
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

export default PartnershipsPage;
