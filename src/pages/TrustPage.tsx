import React from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { PageIntro } from '../components/site/PageIntro';
import { securityTopics, responsibleAi } from '../data/siteContent';

interface TrustPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /trust — Security and trust for serious institutional clients.
 * Covers Responsible AI governance and Security & Trust fundamentals.
 */
export const TrustPage: React.FC<TrustPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="TRUST & SECURITY"
        title="Security and Trust"
        lead="For serious institutional clients."
      />

      {/* Responsible AI */}
      <section
        id="responsible-ai"
        aria-labelledby="responsible-ai-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4 border-t"
      >
        <SectionHeading
          theme={theme}
          eyebrow="RESPONSIBLE AI"
          title="Governed by Design"
          lead="Our AI operating model embeds responsibility at every layer — from human oversight to responsible deployment."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {responsibleAi.map((topic, idx) => (
            <Reveal key={topic.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <h3 className="font-display font-bold text-lg tracking-tight">{topic.title}</h3>
                <p className={`mt-3 text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {topic.description}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Security & Trust */}
      <section
        id="security-trust"
        aria-labelledby="security-trust-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4 border-t"
      >
        <SectionHeading
          theme={theme}
          eyebrow="SECURITY & TRUST"
          title="Built on Trust"
          lead="From data handling to incident management — every layer is engineered with institutional-grade rigour."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {securityTopics.map((topic, idx) => (
            <Reveal key={topic.id} delay={(idx % 2) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-8 border ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <h3 className="font-display font-bold text-lg tracking-tight">{topic.title}</h3>
                <p className={`mt-3 text-sm leading-relaxed ${
                  isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                }`}>
                  {topic.description}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default TrustPage;
