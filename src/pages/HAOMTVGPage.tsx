import React from 'react';
import { SectionHeading } from '../components/site/SectionHeading';
import { Reveal } from '../components/Reveal';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { HaomtgvBlueprintHero } from '../components/haomtgv/HaomtgvBlueprintHero';
import { HAOMTGV_LAYERS } from '../components/haomtgv/layers';

interface HaomtgvPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

const BRAND_BAR = ['#070A40', '#E63946', '#00BFFF'];

export const HaomtgvPage: React.FC<HaomtgvPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const cardBase = isLight
    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl';

    {/*
     * AGENT TEAM NARRATIVE - HAOMTVGPage (7-Layer Framework)
     * Content fidelity governed by:
     *   - orchestration-owner | MessageBus task queue, agent coordination
     *   - governance-owner    | 5-tier approval matrix, H-A-O-M-T-G-V compliance
     *   - registry-owner      | canonical pillar data, company-registry.yaml mapping
     * Last audited: 2026-10-18
     */}
  return (
    <>
      {/* Hero */}
      <HaomtgvBlueprintHero />

      {/* 7-layer grid */}
      <section className={`py-16 sm:py-24 ${isLight ? 'bg-ls-white' : 'bg-ls-navy-dark'}`}>
        <div className="max-w-6xl mx-auto px-6">
          <SectionHeading
            theme={theme}
            eyebrow="THE SEVEN LAYERS"
            title="How the Model Works"
            lead="Each layer has a distinct role. Human direction is present at every layer — not saved for the end."
          />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {HAOMTGV_LAYERS.map((pillar, idx) => (
              <Reveal key={pillar.id} delay={idx * 0.04}>
                <article
                  className={`h-full rounded-3xl p-5 border flex flex-col gap-3 transition-transform hover:-translate-y-1 duration-300 ${cardBase} ${
                    pillar.id === 'governance' ? 'ring-1 ring-ls-red/30' : ''
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <span
                        aria-hidden="true"
                        className="flex w-10 h-10 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red text-lg"
                      >
                        {pillar.letter}
                      </span>
                      <h3 className="font-display font-bold text-base tracking-tight">
                        {pillar.title}
                      </h3>
                    </div>
                    <pillar.Icon className="w-4 h-4 text-ls-cyan" aria-hidden="true" />
                  </div>
                  <p
                    className={`text-xs leading-relaxed ${
                      isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                    }`}
                  >
                    {pillar.description}
                  </p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Governance callout */}
      <section className={`py-16 ${isLight ? 'bg-ls-navy/5' : 'bg-ls-navy-dark'}`}>
        <div className="max-w-3xl mx-auto px-6 text-center space-y-4">
          <h2
            className={`text-xl sm:text-2xl font-black font-display ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}
          >
            Governance Runs Through Every Layer
          </h2>
          <p
            className={`text-sm leading-relaxed ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}
          >
            Human direction is not a checkpoint at the end. It is present at
            every layer. Governance (G) is how that authority stays enforceable
            when agents act at scale.
          </p>
        </div>
      </section>

      {/* Brand color bar */}
      <div aria-hidden="true" className="h-1 flex">
        {BRAND_BAR.map((color) => (
          <div key={color} className="flex-1" style={{ backgroundColor: color }} />
        ))}
      </div>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/ai-company-builder', label: 'AI Company Builder' },
          { to: '/solutions', label: 'Solutions' },
          { to: '/insights', label: 'Insights' },
        ]}
      />
    </>
  );
};

export default HaomtgvPage;
