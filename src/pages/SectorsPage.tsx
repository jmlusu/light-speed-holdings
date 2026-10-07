import React, { useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { Reveal } from '../components/Reveal';
import { sectors, sectorTierLegend } from '../data/sector-registry';
import { solutions } from '../data/siteContent';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface SectorsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

/** Resolve a solution slug to its display title (falls back to the slug). */
const solutionTitle = (slug: string): string =>
  solutions.find((s) => s.slug === slug)?.title ?? slug;

/**
 * /sectors per CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §12: five canonical
 * sectors from `sector-registry.ts`, each carrying one of four evidence
 * tiers — only claim sector experience where evidence exists. Each card
 * cross-links onward to the solutions that serve it (no dead ends).
 */
export const SectorsPage: React.FC<SectorsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const { hash } = useLocation();

  useEffect(() => {
    const id = hash.replace('#', '');
    if (!id) return;
    trackJourneyEvent({
      eventType: 'sector_view',
      sector: id,
      journeyStage: 'exploration',
      route: '/sectors',
    });
  }, [hash]);

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="SECTORS"
        title="Sectors We Serve — With the Evidence to Back It"
        lead="Five sectors across Malawi and Africa. Every sector card carries an evidence tier: proven experience, current capability, demonstration, or future opportunity. We only claim what we can show — and every card links to the solutions that serve it."
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
                id={sector.id}
                className={`rounded-3xl p-6 border h-full flex flex-col gap-4 scroll-mt-28 ${
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
                  {sector.description}
                </p>
                <p
                  className={`text-xs leading-relaxed ${
                    isLight ? 'text-ls-grey-dark/90' : 'text-ls-grey-light-text/90'
                  }`}
                >
                  <span className="font-body font-bold tracking-widest text-ls-red text-[9px]">
                    EVIDENCE{' '}
                  </span>
                  {sector.evidence}
                </p>
                {sector.region && sector.region.length > 0 && (
                  <p
                    className={`font-body text-[10px] font-bold tracking-widest uppercase ${
                      isLight ? 'text-ls-grey-dark/80' : 'text-ls-grey-light-text/80'
                    }`}
                  >
                    {sector.region.join(' · ')}
                  </p>
                )}
                {sector.relevantSolutions && sector.relevantSolutions.length > 0 && (
                  <div
                    className={`mt-auto pt-4 border-t flex flex-wrap items-center gap-2 ${
                      isLight ? 'border-ls-grey-dark/60' : 'border-ls-white/10'
                    }`}
                  >
                    <span
                      className={`font-body text-[9px] font-bold tracking-widest ${
                        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                      }`}
                    >
                      SOLUTIONS FOR THIS SECTOR
                    </span>
                    {sector.relevantSolutions.map((slug) => (
                      <Link
                        key={slug}
                        to={`/solutions#${slug}`}
                        className={`font-body text-[10px] font-bold px-2.5 py-1 rounded-full border transition-colors hover:border-ls-red hover:text-ls-red ${
                          isLight
                            ? 'border-ls-grey-dark/70 text-ls-navy'
                            : 'border-ls-white/25 text-ls-white'
                        }`}
                      >
                        {solutionTitle(slug)}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/proof', label: 'Proof' },
          { to: '/solutions', label: 'Solutions' },
          { to: '/insights', label: 'Insights' },
        ]}
      />

      <CtaBand theme={theme} />
    </>
  );
};

export default SectorsPage;
