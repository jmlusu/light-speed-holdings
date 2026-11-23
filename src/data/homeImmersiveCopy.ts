/**
 * Home immersive experience copy (homepage hero, chapter rail, stage surfaces).
 */
export interface ImmersiveChapter {
  id: string;
  num: string;
  label: string;
}

export const homeImmersiveCopy = {
  hero: {
    stage: 'Governed agentic AI for real operating environments',
    headline: ['ASPIRE.', 'ACT.', 'ACHIEVE.'],
    lead:
      'LightSpeed designs governed agentic AI systems for organisations in Malawi and across SADC. We combine human authority, agent execution, and measurable operating outcomes in environments where trust, bandwidth, and accountability matter.',
    pillars: ['Human Authority', 'Agent Execution', 'Measurable Value'],
    cta: {
      primary: 'Request an AI Readiness Assessment',
      secondary: 'Explore What We Do',
    },
  },
  // Legacy/rail fields retained for existing components.
  heroEyebrow: 'AI-NATIVE OPERATING MODEL',
  heroTitle: 'Human Direction.',
  heroTitleAccent: 'Intelligent Execution.',
  heroLead:
    'LightSpeed Holdings is building an AI-native operating model that brings human judgment together with coordinated AI, clear governance and a focus on practical outcomes.',
  heroCta: 'WHAT WE DO',
  chapters: [
    { id: 'haomtgv', num: '01', label: 'HAOMTGV' },
    { id: 'paths', num: '02', label: 'Choose Path' },
    { id: 'solutions', num: '03', label: 'Solutions' },
    { id: 'insights', num: '04', label: 'Pharos' },
    { id: 'about', num: '05', label: 'About' },
  ] as ImmersiveChapter[],
  scrimHint: 'Every claim is labeled. Every number is auditable.',
} as const;

export type HomeImmersiveCopy = typeof homeImmersiveCopy;
