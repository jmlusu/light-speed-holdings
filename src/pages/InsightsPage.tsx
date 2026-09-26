import React from 'react';
import { PharosSection } from '../components/PharosSection';
import { NewsletterSignup } from '../components/NewsletterSignup';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { SectionHeading } from '../components/site/SectionHeading';
import { Reveal } from '../components/Reveal';

interface InsightsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

const INSIGHT_CATEGORIES = [
  'Agentic AI',
  'AI Company Building',
  'AI governance',
  'AI policy',
  'Data architecture',
  'Digital transformation',
  'African AI',
  'Malawi technology',
  'SADC technology',
  'Market intelligence',
  'Operating models',
  'AI implementation',
];

export const InsightsPage: React.FC<InsightsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <section
        aria-labelledby="insights-heading"
        className={`px-4 sm:px-8 pt-16 sm:pt-20 pb-2 max-w-7xl mx-auto w-full ${
          isLight ? 'text-ls-navy' : 'text-ls-white'
        }`}
      >
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-body text-[11px] tracking-widest">
            <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
            <span>INSIGHTS // PHAROS</span>
          </div>
          <h1
            id="insights-heading"
            className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}
          >
            Evidence, Research &amp; the Agentic AI Canon
          </h1>
          <p
            className={`max-w-2xl text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}
          >
            Original research and executive briefings on AI strategy, data residency, and
            governance — written for boards, not engineers, and grounded in production systems.
          </p>
        </div>
      </section>

      {/* §13 content categories */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-2" aria-label="Insight categories">
        <SectionHeading
          theme={theme}
          eyebrow="TOPICS"
          title="What We Write About"
          lead="Short posts and deeper reports across the full agentic AI canon — from operating models to SADC policy."
        />
        <Reveal>
          <ul className="flex flex-wrap gap-2.5">
            {INSIGHT_CATEGORIES.map((cat) => (
              <li
                key={cat}
                className={`px-3.5 py-1.5 rounded-full border font-body text-[11px] font-bold tracking-wider ${
                  isLight
                    ? 'border-ls-grey-dark/40 bg-ls-white text-ls-navy'
                    : 'border-ls-white/15 bg-ls-navy/80 text-ls-white'
                }`}
              >
                {cat}
              </li>
            ))}
          </ul>
        </Reveal>
      </section>

      <PharosSection theme={theme} onRequestBriefing={onRequestBriefing} />

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/proof', label: 'Proof' },
          { to: '/what-we-do', label: 'What We Do' },
          { to: '/sectors', label: 'Sectors' },
        ]}
      />

      <NewsletterSignup theme={theme} id="newsletter" />
    </>
  );
};

export default InsightsPage;
