import React from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { PageIntro } from '../components/site/PageIntro';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { RelatedLinks } from '../components/site/RelatedLinks';
import {
  securityTopics,
  responsibleAi,
  trustEvidence,
  honestyPolicy,
} from '../data/siteContent';

interface TrustPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /trust — Security and trust for serious institutional clients.
 * Covers Responsible AI governance, operational trust evidence, and
 * Security & Trust fundamentals. Evidence cards carry honesty status.
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

      {/* Trust evidence — operational controls only */}
      <section
        id="trust-evidence"
        aria-labelledby="trust-evidence-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4"
      >
        <SectionHeading
          theme={theme}
          eyebrow="EVIDENCE"
          title="Controls We Actually Run"
          lead="No invented certification logos. These are the operational controls on every engagement — each with its honesty status."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trustEvidence.map((item, idx) => (
            <Reveal key={item.id} delay={(idx % 3) * 0.06}>
              <div
                className={`rounded-3xl p-6 sm:p-7 border h-full ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <h3 className="font-display font-bold text-lg tracking-tight">
                    {item.title}
                  </h3>
                  <HonestyBadge label={item.proof} />
                </div>
                <p
                  className={`mt-3 text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  {item.description}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* Honesty policy */}
      <section
        id="honesty-policy"
        aria-labelledby="honesty-policy-heading"
        className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 sm:pt-16 pb-4 border-t"
      >
        <Reveal>
          <div
            className={`rounded-3xl p-6 sm:p-8 border ${
              isLight
                ? 'bg-ls-white/95 border-ls-grey-dark shadow-md'
                : 'bg-ls-navy/80 border-ls-white/15 shadow-xl'
            }`}
          >
            <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">
              HONESTY POLICY
            </span>
            <ul
              className={`mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-3 text-sm leading-relaxed ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}
            >
              {honestyPolicy.map((point) => (
                <li key={point} className="flex items-start gap-2">
                  <span
                    className="mt-0.5 shrink-0 w-4 h-4 rounded-full bg-ls-cyan/15 text-ls-cyan flex items-center justify-center text-[10px] font-black"
                    aria-hidden="true"
                  >
                    ✓
                  </span>
                  {point}
                </li>
              ))}
            </ul>
          </div>
        </Reveal>
      </section>

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
                <h3 className="font-display font-bold text-lg tracking-tight">
                  {topic.title}
                </h3>
                <p
                  className={`mt-3 text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
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
                <h3 className="font-display font-bold text-lg tracking-tight">
                  {topic.title}
                </h3>
                <p
                  className={`mt-3 text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  {topic.description}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/technology#governance', label: 'Technology' },
          { to: '/leadership', label: 'Leadership' },
          { to: '/faq', label: 'FAQ' },
          { to: '/evidence', label: 'Evidence' },
        ]}
      />

      <CtaBand theme={theme} onRequestBriefing={onRequestBriefing} />
    </>
  );
};

export default TrustPage;
