/**
 * Sector Detail Page
 *
 * Route: /sectors/:slug  (Directive §9)
 * Renders a single canonical sector from sector-registry.ts.
 * Data + component stack matches SectorsPage (local site components).
 */

import React, { useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { PageIntro } from '../components/site/PageIntro';
import { SectionHeading } from '../components/site/SectionHeading';
import { HonestyBadge } from '../components/site/HonestyBadge';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { Reveal } from '../components/Reveal';
import { getSectorById, sectorTierLegend } from '../data/sector-registry';
import { solutions } from '../data/siteContent';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

interface SectorDetailPageProps {
  theme: 'light' | 'dark';
}

const solutionTitle = (slug: string): string =>
  solutions.find((s) => s.slug === slug)?.title ?? slug;

export const SectorDetailPage: React.FC<SectorDetailPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const { slug } = useParams<{ slug: string }>();
  const sector = slug ? getSectorById(slug) : undefined;

  useEffect(() => {
    if (!sector) return;
    trackJourneyEvent({
      eventType: 'sector_view',
      sector: sector.id,
      journeyStage: 'exploration',
      route: `/sectors/${sector.id}`,
    });
  }, [sector]);

  if (!sector) {
    return (
      <>
        <PageIntro
          theme={theme}
          eyebrow="SECTORS"
          title="Sector not found"
          lead={`We couldn't find a sector matching “${slug}”. It may have moved, or the link may be out of date.`}
        />
        <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-6 pb-20">
          <Link
            to="/sectors"
            className={`inline-flex items-center gap-2 font-body text-sm font-bold px-5 py-3 rounded-full border transition-colors hover:border-ls-red hover:text-ls-red ${
              isLight ? 'border-ls-grey-dark/70 text-ls-navy' : 'border-ls-white/25 text-ls-white'
            }`}
          >
            <ArrowLeft size={16} aria-hidden="true" />
            Back to Sectors
          </Link>
        </section>
        <CtaBand theme={theme} />
      </>
    );
  }

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="SECTOR"
        title={sector.title}
        lead={sector.description}
      />

      {/* Evidence tier legend (context for this sector's badge) */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-2">
        <SectionHeading
          theme={theme}
          eyebrow="HOW TO READ THIS PAGE"
          title="Evidence Tiers"
          lead="Sector claims are graded the same way as every other claim on this site."
        />
        <Reveal>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
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

      {/* Sector detail card */}
      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-10 pb-10">
        <Reveal>
          <div
            className={`rounded-3xl p-8 border flex flex-col gap-5 ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl'
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <h2 className={`font-display font-bold text-2xl tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                {sector.title}
              </h2>
              <HonestyBadge label={sector.status} />
            </div>

            <p className={`text-base leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              {sector.description}
            </p>

            {sector.evidence && (
              <p className={`text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark/90' : 'text-ls-grey-light-text/90'}`}>
                <span className="font-body font-bold tracking-widest text-ls-red text-[9px]">EVIDENCE </span>
                {sector.evidence}
              </p>
            )}

            {sector.region && sector.region.length > 0 && (
              <p className={`font-body text-[10px] font-bold tracking-widest uppercase ${isLight ? 'text-ls-grey-dark/80' : 'text-ls-grey-light-text/80'}`}>
                {sector.region.join(' · ')}
              </p>
            )}

            {sector.relevantSolutions && sector.relevantSolutions.length > 0 && (
              <div className={`mt-auto pt-5 border-t flex flex-wrap items-center gap-2 ${isLight ? 'border-ls-grey-dark/60' : 'border-ls-white/10'}`}>
                <span className={`font-body text-[9px] font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  SOLUTIONS FOR THIS SECTOR
                </span>
                {sector.relevantSolutions.map((slug) => (
                  <Link
                    key={slug}
                    to={`/solutions#${slug}`}
                    className={`font-body text-[10px] font-bold px-2.5 py-1 rounded-full border transition-colors hover:border-ls-red hover:text-ls-red ${
                      isLight ? 'border-ls-grey-dark/70 text-ls-navy' : 'border-ls-white/25 text-ls-white'
                    }`}
                  >
                    {solutionTitle(slug)}
                  </Link>
                ))}
              </div>
            )}
          </div>
        </Reveal>
      </section>

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/sectors', label: 'All Sectors' },
          { to: '/use-cases', label: 'Use Cases' },
          { to: '/solutions', label: 'Solutions' },
        ]}
      />

      <CtaBand theme={theme} />
    </>
  );
};

export default SectorDetailPage;
