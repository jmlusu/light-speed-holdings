import React from 'react';
import { HeroSection } from '../components/HeroSection';
import {
  ChapterRail,
  HAOMTGVSection,
  AICompanyBuilderSection,
  WorkforceSection,
  SolutionsSection,
  UseCasesSection,
  InsightsSection,
  AboutSection,
  BriefingSection,
  VisitorPathsSection,
} from '../components/home';
import { FaqSection } from '../components/site/FaqSection';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => (
  <div className="relative">
    {/* MASTER_SPEC §19 static fallback: mist/slate backdrop in a zero-z layer;
        content uses z-10 so it stacks above the fixed bg. */}
    <div className="fixed inset-0 z-0 pointer-events-none bg-[#F7F8F9] dark:bg-[#121518]" aria-hidden="true" />

    <ChapterRail theme={theme} />

    <div className="relative z-10 lg:pl-16">
      {/* 1. Orientation + 2. Core Proposition */}
      <HeroSection theme={theme} onRequestBriefing={onRequestBriefing} />
      {/* §8 Routing: three major visitor pathways */}
      <VisitorPathsSection theme={theme} />
      {/* 3. H-A-O-M-T-G-V operating philosophy */}
      <HAOMTGVSection theme={theme} />
      {/* 4. Solutions: Practical Business Outcomes */}
      <SolutionsSection theme={theme} />
      {/* 5. AI Company Builder: Opportunity → Design → Build → Deploy → Govern → Measure */}
      <AICompanyBuilderSection theme={theme} />
      {/* 6. 90-Agent Workforce */}
      <WorkforceSection theme={theme} />
      {/* 7. Sectors + Use Cases (combined, evidence-status vocabulary) */}
      <UseCasesSection theme={theme} />
      {/* 8. Insights: Pharos thought leadership */}
      <InsightsSection theme={theme} />
      {/* 9. About: Mission, Values, What We Promise Whom */}
      <AboutSection theme={theme} />
      {/* 10. FAQ: Straight answers (footer link target /#faq) */}
      <FaqSection theme={theme} id="faq" />
      {/* CTA: Start a Conversation */}
      <BriefingSection theme={theme} />
    </div>
  </div>
);

export default HomePage;
