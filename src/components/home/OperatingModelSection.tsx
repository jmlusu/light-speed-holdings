import React from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { CAPABILITIES } from '../../data/capabilities';

interface OperatingModelSectionProps {
  theme: 'light' | 'dark';
}

export const OperatingModelSection: React.FC<OperatingModelSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="operating-model" label="Our operating model" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="OPERATING MODEL"
        title="Four Capabilities, One Connected System"
        lead="Strategy, Build, Govern, and Research & Policy operate as an integrated engine — not four separate services. Each capability feeds the next in a continuous improvement loop."
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {CAPABILITIES.map((cap, idx) => (
          <Reveal key={cap.id} delay={idx * 0.08}>
            <div className={`relative rounded-3xl p-6 sm:p-7 border h-full transition-all group ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md group-hover:shadow-xl' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl group-hover:shadow-2xl'
            }`}>
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl" aria-hidden="true">{cap.icon}</span>
                <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">
                  {cap.id.toUpperCase().replace('-', ' ')}
                </span>
              </div>
              <h3 className="font-display font-bold text-base sm:text-lg tracking-tight mb-2">{cap.title}</h3>
              <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                {cap.description}
              </p>
              <div className={`absolute bottom-0 left-0 right-0 h-1.5 rounded-b-3xl ${idx % 2 === 0 ? 'bg-ls-red' : 'bg-ls-cyan'} opacity-60 group-hover:opacity-100 transition-opacity`} aria-hidden="true" />
            </div>
          </Reveal>
        ))}
      </div>
      <div className="mt-8 text-center">
        <p className={`font-body text-[10px] font-bold tracking-widest ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
          STRATEGY → BUILD → GOVERN → RESEARCH & POLICY → STRATEGY
        </p>
      </div>
    </HomeSection>
  );
};

export default OperatingModelSection;