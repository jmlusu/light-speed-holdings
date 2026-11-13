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
  heroEyebrow: 'AI-NATIVE OPERATING MODEL',
  heroTitle: "Human Direction.",
  heroTitleAccent: 'Intelligent Execution.',
  heroLead:
    'LightSpeed Holdings is building an AI-native operating model that brings human judgment together with coordinated AI, clear governance and a focus on practical outcomes.',
  heroCta: 'WHAT WE DO',
  chapters: [
    { id: 'haomtgv', num: '01', label: 'HAOMTGV' },
    { id: 'paths', num: '02', label: 'Choose Path' },
    { id: 'solutions', num: '03', label: 'Solutions' },
    { id: 'insights', num: '04', label: 'Insights' },
    { id: 'about', num: '05', label: 'About' },
  ],
  scrimHint: 'Every claim is labeled. Every number is auditable.',
};
