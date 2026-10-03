import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { HonestyBadge } from '../site/HonestyBadge';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { sectors } from '../../data/sector-registry';

interface SectorsSectionProps {
  theme: 'light' | 'dark';
}

/** Chapter 07 — sector coverage with honesty status labels. */
export const SectorsSection: React.FC<SectorsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="sectors" label="Where we apply it" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="SECTORS"
        title="Where We Apply It"
        lead="Only claim sector experience where evidence exists. Each area carries one of four evidence tiers: proven experience, current capability, demonstration, or future opportunity."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {sectors.map((sector, idx) => (
          <Reveal key={sector.id} delay={(idx % 3) * 0.06}>
            <Link to="/sectors" className={`ripple-on rounded-3xl p-5 border transition-all group ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
            }`}>
              <div className="flex items-start justify-between gap-3 mb-2">
                <h3 className={`font-display font-bold text-sm sm:text-base tracking-tight group-hover:text-ls-red transition-colors ${
                  isLight ? 'text-ls-navy' : 'text-ls-white'
                }`}>
                  {sector.title}
                </h3>
                <HonestyBadge label={sector.status} />
              </div>
              <p className={`text-xs leading-relaxed ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                {sector.description}
              </p>
            </Link>
          </Reveal>
        ))}
      </div>
      <div className="mt-8 text-center">
        <Link
          to="/sectors"
          className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
        >
          EXPLORE ALL SECTORS →
        </Link>
      </div>
    </HomeSection>
  );
};

export default SectorsSection;
