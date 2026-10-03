import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { HonestyBadge } from '../site/HonestyBadge';
import { Reveal } from '../Reveal';
import { solutions } from '../../data/siteContent';
import { HomeSection } from './HomeSection';

interface SolutionsSectionProps {
  theme: 'light' | 'dark';
}

export const SolutionsSection: React.FC<SolutionsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="solutions" label="Solutions" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="SOLUTIONS"
        title="Six Domains, One Governed Stack"
        lead="Every solution answers: what problem it solves, who it's for, what changes, what LightSpeed builds, and what evidence exists. Each carries its own honesty status."
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {solutions.map((sol, idx) => (
          <Reveal key={sol.slug} delay={(idx % 3) * 0.06}>
            <Link to="/contact" className={`ripple-on rounded-3xl p-6 border transition-all h-full flex flex-col justify-between group ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl hover:-translate-y-0.5' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl hover:-translate-y-0.5'
            }`}>
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-3">
                  <span className="font-body text-[10px] font-bold tracking-widest text-ls-red">{sol.eyebrow}</span>
                  <HonestyBadge label={sol.proof} />
                </div>
                <h3 className={`font-display font-bold text-base tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
                  {sol.title}
                </h3>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {sol.oneLiner}
                </p>
              </div>
              <div className={`pt-4 mt-4 border-t flex items-center justify-between ${isLight ? 'border-ls-grey-dark' : 'border-ls-white/10'}`}>
                <span className={`text-[10px] font-body font-bold tracking-widest group-hover:text-ls-red transition-colors ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>EXPLORE</span>
                <ArrowRight className="w-3.5 h-3.5 text-ls-red" aria-hidden="true" />
              </div>
            </Link>
          </Reveal>
        ))}
      </div>
      <div className="mt-8 text-center">
        <Link
          to="/what-we-do"
          className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
        >
          VIEW ALL CAPABILITIES & CATALOG →
        </Link>
      </div>
    </HomeSection>
  );
};

export default SolutionsSection;