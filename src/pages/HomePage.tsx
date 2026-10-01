import React from 'react';
import { HeroSection } from '../components/HeroSection';
import {
  ChapterRail,
  OperatingModelSection,
  AICompanyBuilderSection,
  WorkforceSection,
  SolutionsSection,
  SectorsSection,
  ProofSection,
  InsightsSection,
  AboutSection,
  BriefingSection,
  VisitorPathsSection,
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
      {/* 1. Orientation + 2. Core Proposition */}
      <HeroSection theme={theme} onRequestBriefing={onRequestBriefing} />
      {/* §8 Routing: three major visitor pathways */}
      <VisitorPathsSection theme={theme} />
      {/* 3. Operating Model: Strategy → Build → Govern → Research & Policy */}
      <OperatingModelSection theme={theme} />
      {/* 4. AI Company Builder: Opportunity → Design → Build → Deploy → Govern → Measure */}
      <AICompanyBuilderSection theme={theme} />
      {/* 5. 90-Agent Workforce */}
      <WorkforceSection theme={theme} />
      {/* 6. Solutions: Practical Business Outcomes */}
      <SolutionsSection theme={theme} />
      {/* 7. Sectors: Where We Apply It */}
      <SectorsSection theme={theme} />
      {/* 8. Proof: Verified Operating Metrics */}
      <ProofSection theme={theme} />
      {/* 9. Insights: Pharos Thought Leadership */}
      <InsightsSection theme={theme} />
      {/* 10. About: Mission, Values, What We Promise Whom */}
      <AboutSection theme={theme} />
      {/* CTA: Start a Conversation */}
      <BriefingSection theme={theme} />
    </div>
  </div>
);

export default HomePage;
