import React from 'react';

interface Stage {
  name: string;
  whatHappens: string;
  whatYouGet: string;
}

interface EngagementModelFlowProps {
  theme: 'light' | 'dark';
}

export const EngagementModelFlow: React.FC<EngagementModelFlowProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const stages: Stage[] = [
    {
      name: 'PROBLEM',
      whatHappens:
        'Start with your business problem, not the technology. Diagnose whether AI can help at all - we will say no when it cannot.',
      whatYouGet:
        'Honest read: help, partly, or not yet. [PROVEN IN-HOUSE process]',
    },
    {
      name: 'DESIGN',
      whatHappens:
        'AI strategy, AI readiness, data architecture, agentic workflow design. Baseline captured during the AI Readiness Assessment.',
      whatYouGet:
        'Operating model, roadmap, success metrics agreed up front.',
    },
    {
      name: 'BUILD',
      whatHappens:
        'AI implementation - AI-native workflows, applications, agentic systems, data products, automation.',
      whatYouGet:
        'Working capability, delivered in stages (Foundation 14-21 days, Pilot 6-10 weeks, Scale 3-6 months).',
    },
    {
      name: 'DEPLOY',
      whatHappens:
        'Staged rollout onto your infrastructure or ours; offline-first and Zero-Cloud Boundary options for sensitive data.',
      whatYouGet:
        'Capability in production use, with local-first economics.',
    },
    {
      name: 'GOVERN',
      whatHappens:
        'Five-tier approval, four governance gates, SHA-256 audit trails, RBAC - governance from day one, not bolted on.',
      whatYouGet:
        '[PROVEN IN-HOUSE] controls that make deployment safe.',
    },
    {
      name: 'MEASURE',
      whatHappens:
        'Outcomes measured against the assessment baseline and reported - never asserted in marketing copy.',
      whatYouGet:
        'Evidence: what changed, what it cost, what to do next.',
    },
  ];

  return (
    <section className={`mb-12 ${isLight ? 'bg-[#F7F8F9]' : 'bg-[#0A0D14]'}`}>
      <h3 className="text-xl font-medium mb-6 text-ls-navy dark:text-white">
        The Engagement Model
      </h3>
      <pre
        className="bg-[var(--bg)] p-4 rounded text-sm overflow-x-auto {
          isLight ? 'text-ls-navy' : 'text-white'
        }">
PROBLEM
   ↓
DESIGN
   ↓
BUILD
   ↓
DEPLOY
   ↓
GOVERN
   ↓
MEASURE
</pre>
      <table className="w-full mt-6 text-sm {
        isLight ? 'text-ls-navy' : 'text-white'
      }">
        <thead>
          <tr>
            <th className="text-left font-bold pb-2">Stage</th>
            <th className="text-left font-bold pb-2">What happens</th>
            <th className="text-left font-bold pb-2">What you get</th>
          </tr>
        </thead>
        <tbody>
          {stages.map((stage, i) => (
            <tr key={i}>
              <td className="font-bold">{stage.name}</td>
              <td>{stage.whatHappens}</td>
              <td>{stage.whatYouGet}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
