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
  heroEyebrow: 'LIGHTSPEED HOLDINGS // MALAWI FIRST',
  heroTitle: 'The AI-native company builder',
  heroTitleAccent: 'that ships.',
  heroLead:
    'Agentic AI systems built and operated from Malawi for organizations across SADC. 90 agents, 20 departments, five-tier human approval.',
  heroCta: CTAS.primary.label,
  chapters: [
    { id: 'operating-model', num: '01', label: 'Operating Model' },
    { id: 'ai-company-builder', num: '02', label: 'AI Builder' },
    { id: 'workforce', num: '03', label: 'Workforce' },
    { id: 'sectors', num: '04', label: 'Sectors' },
    { id: 'proof', num: '05', label: 'Proof' },
    { id: 'insights', num: '06', label: 'Insights' },
    { id: 'briefing', num: '07', label: 'Briefing' },
  ],
  scrimHint: 'Every claim is labeled. Every number is auditable.',
};
