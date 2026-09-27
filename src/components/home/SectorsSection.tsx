import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { HonestyBadge } from '../site/HonestyBadge';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';

interface SectorsSectionProps {
  theme: 'light' | 'dark';
}

const SECTORS = [
  { title: 'Government & Public Sector', desc: 'Digital services, compliance automation, and data-driven policy for ministries and agencies.', status: { label: 'Proven in-house', tone: 'proven' as const } },
  { title: 'Development & Donors', desc: 'Donor reporting, M&E pipelines, and compliance workflows for UNDP and development partners.', status: { label: 'In pilot', tone: 'pilot' as const } },
  { title: 'Financial Services', desc: 'Risk classification, audit trails, and regulatory reporting for banks and microfinance.', status: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
  { title: 'Health', desc: 'Data pipelines, reporting automation, and decision support for clinics and health systems.', status: { label: 'Concept', tone: 'development' as const } },
  { title: 'Agriculture & Energy', desc: 'Supply-chain intelligence, climate-data pipelines, and operational dashboards for rural economies.', status: { label: 'Concept', tone: 'development' as const } },
  { title: 'SMEs & Entrepreneurs', desc: 'Mobile-first digital presence, automation, and AI tooling priced for the local market.', status: { label: 'Fieldable in 2026', tone: 'fieldable' as const } },
  { title: 'Technology Companies', desc: 'AI-native operating models, agentic workflows, and governance frameworks for tech firms.', status: { label: 'In development', tone: 'development' as const } },
];

/** Chapter 04 — sector coverage with honesty status labels. */
export const SectorsSection: React.FC<SectorsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="sectors" label="Where we apply it" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="SECTORS"
        title="Where We Apply It"
        lead="Only claim sector experience where evidence exists. Each area is labeled with its honest status — proven, pilot, fieldable, or emerging."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {SECTORS.map((sector, idx) => (
          <Reveal key={sector.title} delay={(idx % 3) * 0.06}>
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
                {sector.desc}
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
