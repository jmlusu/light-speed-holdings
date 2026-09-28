import React from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';
import { sectors, sectorTierLegend } from '../data/sectors';

interface SectorsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/**
 * /sectors per MASTER_SPEC §11: useful without becoming a generic industry
 * list. Nine sectors from the canonical registry, each carrying one of four
 * evidence tiers — only claim sector experience where evidence exists.
 */
export const SectorsPage: React.FC<SectorsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="SECTORS"
        title="Sectors We Serve — With the Evidence to Back It"
        lead="Nine sectors across Malawi and SADC. Every sector card carries an evidence tier: proven experience, current capability, demonstration, or future opportunity. We only claim what we can show."
      />

      {/* Evidence tier legend */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-2">
        <SectionHeading
          theme={theme}
          eyebrow="HOW TO READ THIS PAGE"
          title="Four Evidence Tiers"
          lead="Sector claims are graded the same way as every other claim on this site."
        />
        <Reveal>
          <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4`}>
            {sectorTierLegend.map(({ tier, desc }) => (
              <div
                key={tier.label}
                className={`rounded-2xl p-5 border ${isLight ? 'bg-ls-white border-ls-grey-dark/60 shadow-sm' : 'bg-ls-navy border-ls-white/10 shadow-lg'}`}
              >
                <HonestyBadge label={tier} />
                <p className={`mt-3 text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </Reveal>
      </section>

      {/* Sector cards */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {sectors.map((sector, idx) => (
            <Reveal key={sector.id} delay={(idx % 3) * 0.06}>
              <div
                className={`rounded-3xl p-6 border h-full flex flex-col gap-4 ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <h3
                    className={`font-display font-bold text-lg tracking-tight ${
                      isLight ? 'text-ls-navy' : 'text-ls-white'
                    }`}
                  >
                    {sector.title}
                  </h3>
                  <HonestyBadge label={sector.status} />
                </div>
                <p
                  className={`text-sm leading-relaxed ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  {sector.evidence}
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

export default SectorsPage;
