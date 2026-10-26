import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { HonestyBadge } from '../site/HonestyBadge';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { sectors } from '../../data/sector-registry';
import { useCasesRegistry } from '../../data/use-cases/registry';
import type { HonestyLabel } from '../../data/siteContent';

interface UseCasesSectionProps {
  theme: 'light' | 'dark';
}

/** Registry status → canonical honesty badge vocabulary. */
function statusToHonesty(status: string): HonestyLabel {
  const s = status.toLowerCase();
  if (s === 'live') return { label: 'LIVE', tone: 'proven' };
  if (s.includes('proven')) return { label: 'PROVEN IN-HOUSE', tone: 'proven' };
  if (s.includes('pilot')) return { label: 'IN PILOT', tone: 'pilot' };
  if (s.includes('fieldable')) return { label: 'FIELDABLE', tone: 'fieldable' };
  if (s.includes('demonstration')) return { label: 'DEMONSTRATION', tone: 'fieldable' };
  return { label: 'IN DEVELOPMENT', tone: 'development' };
}

const FEATURED_USE_CASE_IDS = ['uc-js-bar', 'uc-meta', 'ws-01', 'ws-02'];

/** Chapter 05 - sectors + use cases combined (replaces Proof). */
export const UseCasesSection: React.FC<UseCasesSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const featured = FEATURED_USE_CASE_IDS
    .map((id) => useCasesRegistry.find((uc) => uc.id === id))
    .filter((uc): uc is NonNullable<typeof uc> => Boolean(uc));

  return (
    <HomeSection id="use-cases" label="Applications and opportunities" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="APPLICATIONS & OPPORTUNITIES"
        title="Where Practical AI Can Make a Difference"
        lead="Agentic systems matter when they solve real operational problems: compliance, coordination, reporting, and the daily work that keeps institutions running. We work across sectors where African organisations face concrete constraints, from regulated financial services to rural cooperatives operating on WhatsApp and mobile money."
      />

      {/* Featured use cases with evidence status */}
      <div className="mb-10">
        <h3 className={`font-body text-[10px] font-bold tracking-widest mb-4 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
          FEATURED USE CASES
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {featured.map((uc, idx) => (
            <Reveal key={uc.id} delay={idx * 0.05}>
              <Link
                to={`/use-cases/${uc.id}`}
                className={`ripple-on h-full rounded-3xl p-5 border flex flex-col gap-3 transition-all hover:-translate-y-0.5 group ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <h4 className={`font-display font-bold text-sm tracking-tight group-hover:text-ls-red transition-colors ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                    {uc.title}
                  </h4>
                  <HonestyBadge label={statusToHonesty(uc.status)} className="shrink-0" />
                </div>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {uc.problem}
                </p>
                <span className={`mt-auto inline-flex items-center gap-1.5 text-[11px] font-body font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'} group-hover:text-ls-red`}>
                  VIEW USE CASE →
                </span>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-4 text-center">
          <Link
            to="/use-cases"
            className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
          >
            VIEW ALL USE CASES →
          </Link>
        </div>
      </div>

      {/* Sectors with evidence tiers */}
      <div>
        <h3 className={`font-body text-[10px] font-bold tracking-widest mb-4 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
          SECTORS
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {sectors.map((sector, idx) => (
            <Reveal key={sector.id} delay={(idx % 3) * 0.05}>
              <Link
                to={`/sectors#${sector.id}`}
                className={`ripple-on h-full rounded-3xl p-5 border flex flex-col gap-3 transition-all hover:-translate-y-0.5 group ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl'
                    : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">
                    {sector.region?.join(' · ') ?? 'SECTOR'}
                  </span>
                  <HonestyBadge label={sector.status} />
                </div>
                <h4 className={`font-display font-bold text-sm tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  {sector.title}
                </h4>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {sector.description}
                </p>
              </Link>
            </Reveal>
          ))}
        </div>
        <div className="mt-4 text-center">
          <Link
            to="/sectors"
            className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
          >
            VIEW ALL SECTORS &amp; EVIDENCE TIERS →
            <ArrowRight className="inline w-3.5 h-3.5 ml-1" aria-hidden="true" />
          </Link>
        </div>
      </div>

      <p className={`mt-8 text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
        Across every engagement, we focus on the same outcome: useful intelligence, clear accountability, and systems people can actually operate. Not AI for its own sake. AI for work that matters.
      </p>
    </HomeSection>
  );
};

export default UseCasesSection;
