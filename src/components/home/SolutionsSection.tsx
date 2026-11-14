import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { HonestyBadge } from '../site/HonestyBadge';
import { Reveal } from '../Reveal';
import { solutions, GOVERNANCE_SOLUTION } from '../../data/siteContent';
import { HomeSection } from './HomeSection';

interface SolutionsSectionProps {
  theme: 'light' | 'dark';
}

/** Six-card home catalog: five registry solutions + the governance card. */
const homeSolutions = [
  ...solutions.map((s) => ({ ...s, to: '/contact' })),
  { ...GOVERNANCE_SOLUTION, slug: 'governance' },
];

export const SolutionsSection: React.FC<SolutionsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection
      id="solutions"
      label="Solutions"
      theme={theme}
      variant="primary"
    >
      <SectionHeading
        theme={theme}
        eyebrow="SOLUTIONS"
        title="Six Domains, One Governed Stack"
        lead="Every solution answers: what problem it solves, who it's for, what changes, what LightSpeed builds, and what evidence exists. Each carries its own honesty status."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {homeSolutions.map((sol, idx) => (
          <Reveal key={sol.slug} delay={(idx % 3) * 0.06}>
            <Link
              to={sol.to}
              className="ripple-on rounded-3xl overflow-hidden transition-all h-full flex flex-col group shadow-none hover:-translate-y-0.5 bg-transparent border-none"
            >
              {sol.image && (
                <div className="h-40 overflow-hidden relative">
                  <img
                    src={sol.image}
                    alt={sol.title}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                  />
                  <div className={`absolute inset-0 bg-gradient-to-t ${isLight ? 'from-ls-white' : 'from-[#070A40]/90'} to-transparent`} />
                </div>
              )}
              <div className="p-6 flex flex-col flex-1 justify-between">
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <span className="font-body text-[10px] font-bold tracking-widest text-[#DC3641]">{sol.eyebrow}</span>
                    <HonestyBadge label={sol.proof} />
                  </div>
                  <h3 className={`font-display font-bold text-base tracking-tight transition-colors ${isLight ? 'text-ls-navy group-hover:text-[#DC3641]' : 'text-white group-hover:text-[#00BFFF]'}`}>
                    {sol.title}
                  </h3>
                  <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'}`}>
                    {sol.oneLiner}
                  </p>
                </div>
                <div className="pt-4 mt-4 flex items-center justify-between">
                  <span className={`text-[10px] font-body font-bold tracking-widest transition-colors ${isLight ? 'text-ls-navy group-hover:text-[#DC3641]' : 'text-[#00BFFF] group-hover:text-[#DC3641]'}`}>EXPLORE</span>
                  <ArrowRight className="w-3.5 h-3.5 text-[#DC3641] transition-transform group-hover:translate-x-1" aria-hidden="true" />
                </div>
              </div>
            </Link>
          </Reveal>
        ))}
      </div>
      <div className="mt-8 text-center">
        <Link
          to="/what-we-do"
          className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-[#00BFFF]'}`}
        >
          VIEW ALL CAPABILITIES & CATALOG →
        </Link>
      </div>
    </HomeSection>
  );
};

export default SolutionsSection;
