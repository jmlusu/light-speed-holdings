import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';
import { metrics } from '../../data/metrics';

interface WorkforceSectionProps {
  theme: 'light' | 'dark';
}

/** Chapter 03 - the agentic operating model (specialized agents, human direction). */
export const WorkforceSection: React.FC<WorkforceSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="workforce" label="The agentic operating model" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="THE AGENTIC OPERATING MODEL"
        title="Specialized AI. Human Direction. Governed Execution."
        lead="LightSpeed operates through a governed digital workforce: 90 agents across 20 departments, each with explicit role definitions and approval thresholds. Human direction, audited execution."
      />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { value: String(metrics.agentCount), label: 'Agents' },
          { value: String(metrics.departments), label: 'Departments' },
          { value: String(metrics.fiveTier), label: 'Approval tiers' },
          { value: String(metrics.caseStudyMeta), label: 'Case studies' },
        ].map((stat, idx) => (
          <Reveal key={stat.label} delay={idx * 0.04}>
            <div className={`rounded-2xl p-5 border text-center ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md' : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'
            }`}>
              <span className="font-body text-2xl sm:text-3xl font-black text-ls-cyan">{stat.value}</span>
              <p className="mt-2 text-[10px] font-body font-bold tracking-widest uppercase opacity-70">{stat.label}</p>
            </div>
          </Reveal>
        ))}
      </div>
      <p className={`mt-6 text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
        Specialized roles, not a single general-purpose bot. Each agent has a job, a scope, and a human who can overrule it. Browse the registry to see who does what.
      </p>
      <div className="mt-4 text-center">
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
