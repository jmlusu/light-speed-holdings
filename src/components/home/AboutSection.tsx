import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { company } from '../../data/siteContent';

interface AboutSectionProps {
  theme: 'light' | 'dark';
}

const VALUES = [
  {
    title: 'AI-Native First',
    description: 'We build AI-native companies where constraints are real — infrastructure gaps, talent development, regulatory evolution — then scale.',
  },
  {
    title: 'Evidence Over Claims',
    description: 'Every public statement is labeled: Proven in-house, In pilot, Fieldable, or In development. No blurring the line.',
  },
  {
    title: 'Governed by Design',
    description: 'Five-tier human approval, immutable audit trails, and regional compliance are architecture, not bolt-ons.',
  },
  {
    title: 'African Intelligence',
    description: 'Pharos turns our engineering into public intellectual work — SADC governance frameworks, Malawi AI Strategy, regional policy.',
  },
];

export const AboutSection: React.FC<AboutSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="about" label="About LightSpeed" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="ABOUT LIGHTSPEED"
        title="One Human CEO. 90 AI Agents."
        lead={company.thesis || 'We are the AI-native company we sell — governed, audited, and holding every claim to its evidence.'}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {VALUES.map((val, idx) => (
          <Reveal key={val.title} delay={idx * 0.08}>
            <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
            }`}>
              <span className="font-body text-[10px] font-bold tracking-widest text-ls-red uppercase">{val.title}</span>
              <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                {val.description}
              </p>
            </div>
          </Reveal>
        ))}
      </div>
      <div className="mt-10 pt-8 border-t" style={{ borderColor: isLight ? '#E5E7EB' : '#1F2937' }}>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h3 className="font-display font-bold text-lg sm:text-xl tracking-tight">Read the Mission, the Values, and What We Promise Whom.</h3>
            <p className={`mt-2 text-sm ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              Transparency is a feature. Our governance model, agent registry, and public commitments are documented.
            </p>
          </div>
          <Link
            to="/about"
            className="ripple-on inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase border border-ls-red/40 bg-ls-red/10 text-ls-red transition-all cursor-pointer hover:brightness-110 shrink-0"
          >
            About LightSpeed
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </HomeSection>
  );
};

export default AboutSection;
