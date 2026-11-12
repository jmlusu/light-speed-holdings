/**
 * AI Assessment Page
 *
 * Route: /ai-assessment  (Directive §9 / §34)
 * Interactive AI Readiness Diagnostic Wizard & Summary.
 *
 * Recovered from the AI Studio prototype (AiAssessmentPage + AssessmentWizard).
 * The 5-step wizard was replaced by a modal-trigger stub during the migration;
 * this restores the original inline diagnostic while keeping the briefing
 * request available as the wizard's exit CTA.
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
        title="AI Readiness Assessment Wizard"
        lead="A 5-step qualitative diagnostic evaluating your organization across data maturity, core infrastructure, governance alignment, talent readiness, and agentic workflow potential. Evaluate your posture in minutes."
      />

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-6 pb-20">
        <AssessmentWizard theme={theme} onRequestBriefing={onRequestBriefing} />
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default AiAssessmentPage;
