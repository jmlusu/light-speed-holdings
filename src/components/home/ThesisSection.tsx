import React from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { company } from '../../data/siteContent';
import { HomeSection } from './HomeSection';

interface ThesisSectionProps {
  theme: 'light' | 'dark';
}

const THESIS_COLUMNS = [
  {
    num: '01',
    title: 'Prove It in Malawi',
    body: 'Real clients, real constraints, real infrastructure. The proof is a shipped website, a donor report that used to take weeks, a dashboard that replaced forty-page PDFs — not a press release.',
  },
  {
    num: '02',
    title: 'Ship, Don\u2019t Promise',
    body: 'Every claim on this site is labeled Proven in-house, In pilot, Fieldable, or In development — and the tests that gate our own work are published. We never blur the two.',
  },
  {
    num: '03',
    title: 'Governed by Design',
    body: 'Five-tier human approval, immutable audit trails, and regional compliance are the architecture of the workforce, not bolt-ons. Trust is what scales.',
  },
  {
    num: '04',
    title: 'Research Informed',
    body: 'Pharos turns engineering into public intellectual work. The SADC Agentic AI Governance Framework and Malawi\u2019s National AI Strategy consultation position LightSpeed as a source of policy, not just product.',
  },
];

export const ThesisSection: React.FC<ThesisSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="thesis" label="The LightSpeed thesis" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="THE LIGHTSPEED THESIS"
        title="Malawi First. Prove It. Then the World."
        lead="Intelligent automation is not a privilege of rich countries. We win trust with real engagements, published case studies, and compliant, secure delivery — in Malawi first, where the constraints are real."
      />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {THESIS_COLUMNS.map((col, idx) => (
          <Reveal key={col.num} delay={idx * 0.08}>
            <div className={`rounded-3xl p-6 sm:p-7 border h-full ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
            }`}>
              <span className="font-body text-2xl font-black text-ls-red">{col.num}</span>
              <h3 className="mt-2 font-display font-bold text-base sm:text-lg tracking-tight">{col.title}</h3>
              <p className={`mt-2 text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                {col.body}
              </p>
            </div>
          </Reveal>
        ))}
      </div>
      <p className={`mt-8 text-center font-body text-xs font-bold tracking-widest ${
        isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
      }`}>
        <span className="text-ls-red">NORTH STAR // </span>
        {company.northStar.toUpperCase()}
      </p>
    </HomeSection>
  );
};

export default ThesisSection;
