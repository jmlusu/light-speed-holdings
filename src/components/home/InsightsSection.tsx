import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { insightTeasers } from '../../data/siteContent';
import { HomeSection } from './HomeSection';

interface InsightsSectionProps {
  theme: 'light' | 'dark';
}

/** Chapter 06 — Pharos insight teasers. */
export const InsightsSection: React.FC<InsightsSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';
  return (
    <HomeSection id="insights" label="Insights from Pharos" theme={theme}>
      <SectionHeading
        theme={theme}
        eyebrow="INSIGHTS"
        title="The Agentic AI Voice of the Region"
        lead="Pharos turns LightSpeed's engineering into public intellectual work on Agentic AI Company Building, use cases, and policy — from Malawi's National AI Strategy consultation to the SADC governance framework."
      />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {insightTeasers.map((post, idx) => (
          <Reveal key={post.title} delay={idx * 0.08}>
            <Link to={post.to} className={`ripple-on rounded-3xl p-6 border transition-all h-full block group ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md hover:shadow-xl' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl hover:shadow-2xl'
            }`}>
              <span className={`font-body text-[10px] font-bold tracking-widest ${isLight ? 'text-ls-navy' : 'text-ls-cyan'}`}>
                {post.topic}
              </span>
              <h3 className={`mt-3 font-display font-bold text-base tracking-tight group-hover:text-ls-red transition-colors ${
                isLight ? 'text-ls-navy' : 'text-ls-white'
              }`}>
                {post.title}
              </h3>
              <span className={`mt-4 inline-flex items-center gap-1.5 text-[11px] font-body font-bold tracking-widest ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              } group-hover:text-ls-red`}>
                READ →
              </span>
            </Link>
          </Reveal>
        ))}
      </div>
    </HomeSection>
  );
};

export default InsightsSection;
