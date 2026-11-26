import React from 'react';

interface ApprovalMatrixWalkthroughProps {
  theme: 'light' | 'dark';
}

/**
 * ONE static worked example of the five-tier human approval mechanism.
 *
 * Every displayed string is copied verbatim from registry-backed sources:
 * - claims-registry.json: claim.five-tier-approval, claim.four-governance-gates,
 *   claim.append-only-audit-trails (classification: PROVEN_IN_HOUSE -> "Proven in-house")
 * - HAOMTGVPage.tsx APPROVAL_TIERS[3] (Tier 4): scope, riskLevel, authority
 * - HaomtgvUnifiedArchitecture.tsx: SHA-256 state receipts under human gates
 *
 * No new claim, no new number, no CTA, no interactive control.
 */
const WALKTHROUGH = [
  {
    label: 'Action request',
    value: 'Financial commitments, external partnerships, and policy changes.',
  },
  { label: 'Risk class', value: 'High' },
  { label: 'Named human gate', value: 'Executive sponsor or director.' },
  {
    label: 'SHA-256 audit receipt',
    value: 'Every agent action generates an append-only SHA-256 sealed JSONL audit trail.',
  },
] as const;

export const ApprovalMatrixWalkthrough: React.FC<ApprovalMatrixWalkthroughProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <section
      aria-label="One worked example of the five-tier human approval matrix"
      className={`rounded-xl border p-4 sm:p-5 ${
        isLight ? 'border-ls-cyan/40 bg-ls-cyan/10' : 'border-ls-cyan/40 bg-ls-cyan/5'
      }`}
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3
          className={`font-body text-xs font-bold tracking-widest uppercase ${
            isLight ? 'text-ls-cyan-ink' : 'text-ls-cyan'
          }`}
        >
          One worked example
        </h3>
      </div>

      <ol className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {WALKTHROUGH.map((step) => (
          <li key={step.label}>
            <span
              className={`block font-body text-[11px] font-bold tracking-wide uppercase ${
                isLight ? 'text-ls-cyan-ink' : 'text-ls-cyan'
              }`}
            >
              {step.label}
            </span>
            <p
              className={`mt-1 font-body text-xs leading-relaxed ${
                isLight ? 'text-slate-700' : 'text-slate-300'
              }`}
            >
              {step.value}
            </p>
          </li>
        ))}
      </ol>

      <p className={`mt-4 font-body text-[11px] ${isLight ? 'text-ls-grey-ink' : 'text-slate-400'}`}>
        claim.five-tier-approval · claim.four-governance-gates · claim.append-only-audit-trails
      </p>
    </section>
  );
};

export default ApprovalMatrixWalkthrough;
