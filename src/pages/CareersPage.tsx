import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { careers } from '../data/siteContent';

interface CareersPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /careers — build the future with LightSpeed.
 * Career categories with title, description, and items.
 */
export const CareersPage: React.FC<CareersPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="CAREERS"
        title="Build the Future With Us"
        lead="The long-term LightSpeed vision will require people who can work alongside our AI operating model."
      />

      <section
        id="careers"
        aria-labelledby="careers-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-4"
      >
        <SectionHeading
          theme={theme}
          eyebrow="JOIN US"
          title="Career Categories"
          lead="From open positions to research fellowships, associateships, and internships — find the role that matches your expertise."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {careers.map((category, idx) => (
            <Reveal key={category.id} delay={(idx % 3) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border flex flex-col ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-black tracking-widest text-ls-red">
                    {category.id.toUpperCase()}
                  </span>
                </div>
                <h3 className="mt-4 font-display font-bold text-lg sm:text-xl tracking-tight">
                  {category.title}
                </h3>
                <p className={`mt-3 text-xs sm:text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {category.description}
                </p>
                <ul className="mt-4 space-y-2 flex-1">
                  {category.items.map((item) => (
                    <li key={item} className="flex items-center gap-2 text-xs sm:text-sm">
                      <span className="w-1.5 h-1.5 rounded-full bg-ls-red shrink-0" aria-hidden="true" />
                      <span className={isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}>
                        {item}
                      </span>
                    </li>
                  ))}
                </ul>
                <div className={`mt-auto pt-5 border-t flex items-center justify-between ${
                  isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'
                }`}>
                  <span className={`text-[11px] font-body font-bold tracking-widest ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}>
                    Explore
                  </span>
                  <ArrowRight className="w-4 h-4 text-ls-red" aria-hidden="true" />
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand
        theme={theme}
        title="Ready to Build the Future?"
        text="Whether you are looking for an open role, a research fellowship, or a partnership opportunity — LightSpeed is building something extraordinary and we want you aboard."
        ctaLabel="Explore Careers"
      />
    </>
  );
};

export default CareersPage;
