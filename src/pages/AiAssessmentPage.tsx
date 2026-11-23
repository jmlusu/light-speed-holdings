/**
 * AI Assessment Page
 *
 * Route: /ai-assessment  (Directive §9 / §34)
 * Interactive AI Readiness Diagnostic Wizard & Summary.
 */

import React from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { CtaBand } from '../components/site/CtaBand';
import { AssessmentWizard } from '../components/AssessmentWizard';

interface AiAssessmentPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const AiAssessmentPage: React.FC<AiAssessmentPageProps> = ({
  theme,
  onRequestBriefing,
}) => {
  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="AI READINESS DIAGNOSTIC"
        title="AI Readiness Assessment"
        lead="Check your organisation across five domains: data maturity, infrastructure, governance, talent, and agentic workflow potential. The qualitative assessment takes minutes."
      />

      <section className="px-6 lg:px-12 max-w-7xl mx-auto w-full pt-6 pb-20">
        <AssessmentWizard theme={theme} onRequestBriefing={onRequestBriefing} />
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default AiAssessmentPage;
