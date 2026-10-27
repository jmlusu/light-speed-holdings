import React from 'react';
import { SectionHeading } from '../site/SectionHeading';
import { Reveal } from '../Reveal';
import { HomeSection } from './HomeSection';

interface HighLevelOverviewSectionProps {
  theme: 'light' | 'dark';
}

/**
 * Chapter 02.5 — High Level Overview:
 * Inserted between Introduction (Thesis) and HAOMTGV (7-layer framework).
 * Bridges the thesis narrative into the operating model.
 *
 * Brand compliance (Sec. 9 brand-guidelines.md):
 - Navy: #070A40 (headlines, rail, primary surfaces)
 - Red: #E63946 (accents, CTAs, key highlights)
 - Cyan: #00BFFF (links on dark, taglines on navy)
 - Arial type scale: displayXL 36pt → caption 12pt
 - 4px spacing grid base unit
 - 80/10/10 color rule (navy dominant, red/cyan accents)
 - Tagline "ASPIRE. ACT. ACHIEVE." on first mention with ™
 */
export const HighLevelOverviewSection: React.FC<HighLevelOverviewSectionProps> = ({ theme }) => {
  const isLight = theme === 'light';

  const OVERVIEW_ITEMS = [
    {
      title: 'Orchestrated Agentic Platform',
      description:
        '89 AI agents + 1 Human CEO across 20 departments — a unified system for building, governing, and scaling AI-native operations.',
    },
    {
      title: 'Build & Govern',
      description:
        'Governed sandboxes with automated regression, 5-tier human approval gates, and SHA-256 append-only audit trails for every agent action.',
    },
    {
      title: 'Scale with Assurance',
      description:
        'Phased production rollouts, real-time KPI collectors, and continuous compliance monitoring so growth stays auditable and controllable.',
    },
    {
      title: 'Thesis in Practice',
      description:
        'LightSpeed\'s thesis — "Human Direction. Intelligent Execution. Measurable Value." — becomes the HAOMTGV operating framework in practice.',
    },
  ];

  return (
    <HomeSection
      id="high-level-overview"
      label="High Level Overview"
      theme={theme}
    >
      <SectionHeading
        theme={theme}
        eyebrow="AI COMPANY BUILDER"
        title="From Thesis to Operating Model"
        lead="LightSpeed Holdings™ does not position itself as a technology company that happens to use AI. We build governed operating models where human intent, agent execution, and measurable value are architecture, not afterthought."
      />

      <div className="space-y-12">
        {/* Overview items grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {OVERVIEW_ITEMS.map((item, idx) => (
            <Reveal key={item.title} delay={idx * 0.04}>
              <article
                className={`h-full rounded-3xl p-5 border flex flex-col gap-3 ${
                  isLight
                    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl'}
                ${item.title === 'Thesis in Practice' ? 'ring-1 ring-ls-red/30' : ''}`}
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-3">
                    <span
                      aria-hidden="true"
                      className="flex w-10 h-10 items-center justify-center rounded-full border border-ls-red/40 bg-ls-red/10 font-display font-black text-ls-red text-lg"
                    >
                      {idx + 1}
                    </span>
                    <h3 className="font-display font-bold text-base tracking-tight">{item.title}</h3>
                  </div>
                </div>
                <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                  {item.description}
                </p>
              </article>
            </Reveal>
          ))}
        </div>

        {/* Transition to HAOMTGV */}
        <div className="pt-8 border-t" style={{ borderColor: isLight ? '#E5E7EB' : '#1F2937' }}>
<p className={`text-sm leading-relaxed ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              The HAOMTGV operating philosophy (Chapter 03) translates this overview into
              a 7-layer control model: Human → Agents → Orchestration → Memory → Tools →
              Governance → Value. Governance (G) is the integral control layer that turns
              the thesis into an enforceable, auditable system at scale. ASPIRE. ACT. ACHIEVE.
            </p>
        </div>
      </div>
    </HomeSection>
  );
};

export default HighLevelOverviewSection;
