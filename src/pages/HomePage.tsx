import React from 'react';
import { HeroSection } from '../components/HeroSection';
import { ImmersiveStage } from '../components/ImmersiveStage';
import {
  ChapterRail,
  ThesisSection,
  BuilderSection,
  WorkforceSection,
  SectorsSection,
  ProofSection,
  InsightsSection,
  AboutBand,
  BriefingSection,
} from '../components/home';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => (
  <div className="relative">
    {/* Contract A: stage mounts first, behind everything. The opaque fixed
        canvas (alpha: false) would paint above the non-positioned site footer
        at z-0, so the containment div holds it in a negative stacking context
        that still sits over the propagated body background. pointer-events
        stay on the DOM layer. */}
    <div className="fixed inset-0 z-[-1] pointer-events-none" aria-hidden="true">
      <ImmersiveStage theme={theme} />
    </div>

    <ChapterRail theme={theme} />

    <div className="relative z-10 lg:pl-16">
      <HeroSection theme={theme} onRequestBriefing={onRequestBriefing} />
      <ThesisSection theme={theme} />
      <BuilderSection theme={theme} />
      <WorkforceSection theme={theme} />
      <SectorsSection theme={theme} />
      <ProofSection theme={theme} />
      <InsightsSection theme={theme} />
      <AboutBand theme={theme} />
      <BriefingSection theme={theme} />
    </div>
  </div>
);

export default HomePage;
