import React from 'react';
import { HeroSection } from '../components/HeroSection';
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
    {/* MASTER_SPEC §19 static fallback: mist/slate backdrop occupies the same
        fixed negative-z layer the WebGL stage used to paint. */}
    <div className="fixed inset-0 z-[-1] pointer-events-none bg-[#F7F8F9] dark:bg-[#121518]" aria-hidden="true" />

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
