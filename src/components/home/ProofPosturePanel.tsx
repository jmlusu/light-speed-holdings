import React from 'react';
import { Link } from 'react-router-dom';
import { HonestyBadge } from '../site/HonestyBadge';
import { honestyLabel } from '../../data/siteContent';

interface ProofPosturePanelProps {
  theme: 'light' | 'dark';
}

/**
 * Small, closed disclosure that makes the already-published honest posture
 * visible earlier on / and /what-we-do. Every answer string below is copied
 * verbatim from src/data/faqs.ts; the badge label is the existing
 * "Proven in-house" honesty label. No new claim, no new number, no new CTA.
 */
const ANSWER_SNIPPETS = [
  'Not yet. Nothing has been delivered to paying clients.',
  'There is no public rate card yet.',
  'Every proof point on this site carries an explicit honesty badge.',
] as const;

export const ProofPosturePanel: React.FC<ProofPosturePanelProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <aside aria-label="Honest posture" className="w-full max-w-7xl mx-auto px-6 lg:px-12 py-4">
      <details
        className={`rounded-lg border p-4 font-body text-xs ${
          isLight ? 'border-slate-200 bg-white/70 text-ls-navy' : 'border-white/10 bg-ls-navy/40 text-white'
        }`}
      >
        <summary
          className={`cursor-pointer font-bold tracking-wide ${
            isLight ? 'text-ls-cyan-ink' : 'text-ls-cyan'
          }`}
        >
          What we have not proven yet
        </summary>

        <div className="mt-4 space-y-3">
          {ANSWER_SNIPPETS.map((snippet) => (
            <p key={snippet} className={isLight ? 'text-slate-700' : 'text-slate-300'}>
              {snippet}
            </p>
          ))}
          <div className="flex flex-wrap items-center gap-3">
            <HonestyBadge label={honestyLabel('Proven in-house')} />
            <Link
              to="/faq"
              className={`font-bold tracking-wide underline underline-offset-2 ${
                isLight ? 'text-ls-cyan-ink' : 'text-ls-cyan'
              }`}
            >
              Read the published answers
            </Link>
          </div>
        </div>
      </details>
    </aside>
  );
};

export default ProofPosturePanel;
