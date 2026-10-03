import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';

interface WorkforceSectionProps {
  theme: 'light' | 'dark';
}

const AGENT_CATEGORIES = [
  { label: 'Strategy', count: '12' },
  { label: 'Research', count: '14' },
  { label: 'Product & Eng', count: '18' },
  { label: 'Operations', count: '11' },
  { label: 'Governance', count: '16' },
  { label: 'Content & Comms', count: '9' },
  { label: 'Finance & Legal', count: '10' },
];

/** Chapter 03 — the 90-agent workforce breakdown. */
export const WorkforceSection: React.FC<WorkforceSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="workforce" label="The 90-agent workforce" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="OPERATING MODEL"
        title="A Coordinated Workforce of 90 Agents"
        lead="LightSpeed operates through a governed digital workforce — 90 agents across 20 departments, each with explicit role definitions and approval thresholds. Human direction, audited execution."
      />
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
        {AGENT_CATEGORIES.map((cat, idx) => (
          <Reveal key={cat.label} delay={idx * 0.04}>
            <div className={`rounded-2xl p-4 border text-center ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
            }`}>
              <span className="font-body text-2xl sm:text-3xl font-black text-ls-cyan">{cat.count}</span>
              <p className="mt-2 text-[10px] font-body font-bold tracking-widest uppercase opacity-70">{cat.label}</p>
            </div>
          </Reveal>
        ))}
      </div>
      <div className="mt-6 text-center">
        <Link
          to="/ai-company-builder"
          className={`font-body text-xs font-bold tracking-widest hover:underline ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}
        >
          EXPLORE THE AGENT ARCHITECTURE →
        </Link>
      </div>
    </HomeSection>
  );
};

export default WorkforceSection;
