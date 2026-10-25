import { CTAS } from './ctas';

export interface ImmersiveChapter {
  id: string;
  num: string;
  label: string;
}

export interface HomeImmersiveCopy {
  heroEyebrow: string;
  heroTitle: string;
  heroTitleAccent: string;
  heroLead: string;
  heroCta: string;
  chapters: ImmersiveChapter[];
  scrimHint: string;
}

export const homeImmersiveCopy: HomeImmersiveCopy = {
  heroEyebrow: 'LIGHTSPEED HOLDINGS // AI-NATIVE COMPANY BUILDER',
  heroTitle: 'The AI-native company builder',
  heroTitleAccent: 'that ships.',
  heroLead:
    'Agentic AI systems based in Malawi, building for Africa. 89 AI agents + 1 Human CEO, 20 departments, five-tier human approval.',
  heroCta: CTAS.primary.label,
  chapters: [
    { id: 'haomtgv', num: '01', label: 'HAOMTGV' },
    { id: 'ai-company-builder', num: '02', label: 'AI Builder' },
    { id: 'workforce', num: '03', label: 'Workforce' },
    { id: 'use-cases', num: '04', label: 'Use Cases' },
    { id: 'insights', num: '05', label: 'Insights' },
    { id: 'briefing', num: '06', label: 'Briefing' },
  ],
  scrimHint: 'Every claim is labeled. Every number is auditable.',
};
