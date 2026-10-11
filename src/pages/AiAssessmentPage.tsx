/**
 * AI Assessment Page
 *
 * Route: /ai-assessment  (Directive §9 / §34)
 * Thin entry that reuses ExecutiveBriefingModal — no new assessment UI.
 * Opening the nav "AI ASSESSMENT" action or hitting this URL directly
 * both surface the same briefing modal.
 */

import React, { useEffect } from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { CtaBand } from '../components/site/CtaBand';
import { Reveal } from '../components/Reveal';

interface AiAssessmentPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const AiAssessmentPage: React.FC<AiAssessmentPageProps> = ({
  theme,
  onRequestBriefing,
}) => {
  const isLight = theme === 'light';

  useEffect(() => {
    onRequestBriefing?.('REQUEST AN AI READINESS ASSESSMENT');
  }, [onRequestBriefing]);

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="AI READINESS"
        title="Request an AI Readiness Assessment"
        lead="A structured read of where your organisation stands across data, infrastructure, talent, and governance — and a prioritised roadmap to an AI-native operating model. Opening the assessment form now."
      />

      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-6 pb-20">
        <Reveal>
          <div
            className={`rounded-3xl p-8 border text-center ${
              isLight ? 'bg-ls-white/95 border-ls-grey-dark shadow-md' : 'bg-ls-navy/80 border-ls-white/15 shadow-xl'
            }`}
          >
            <p className={`text-sm leading-relaxed max-w-2xl mx-auto ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
              The assessment opens in a form. If it didn't open automatically, use the
              <span className="font-bold text-ls-red"> AI ASSESSMENT </span>
              button in the navigation, or
              <button
                type="button"
                onClick={() => onRequestBriefing?.('REQUEST AN AI READINESS ASSESSMENT')}
                className={`font-bold underline underline-offset-2 mx-1 cursor-pointer ${
                  isLight ? 'text-ls-navy hover:text-ls-red' : 'text-ls-white hover:text-ls-red'
                }`}
              >
                reopen it here
              </button>
              .
            </p>
          </div>
        </Reveal>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default AiAssessmentPage;
