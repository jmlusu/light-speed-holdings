import React from 'react';
import { HeroSection } from '../components/HeroSection';
import { IntroductionSection } from '../components/home/IntroductionSection';
import { LightSpeedProposition } from '../components/home/LightSpeedProposition';
import { VisitorPathsSection } from '../components/home/VisitorPathsSection';
import { WhatWeBuildGrid } from '../components/home/WhatWeBuildGrid';
import { HAOMTGVSection } from '../components/home/HAOMTGVSection';
import { IntentToExecutionLifecycle } from '../components/home/IntentToExecutionLifecycle';
import { HumanApprovalMatrix } from '../components/HumanApprovalMatrix';

import { InsightsSection } from '../components/home/InsightsSection';
import { AboutSection } from '../components/home/AboutSection';
import { FaqSection } from '../components/site/FaqSection';
import { DistinctCTA } from '../components/DistinctCTA';
import { Footer } from '../components/footer/Footer';

interface HomePageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <div className={`relative min-h-screen ${isLight ? 'bg-[#F7F8F9] text-ls-navy' : 'bg-[#0A0D14] text-white'}`}>
      <div className={`fixed inset-0 z-0 pointer-events-none ${isLight ? 'bg-[#F7F8F9]' : 'bg-[#0A0D14]'}`} aria-hidden="true" />

      <main id="main-content" className="relative z-10 w-full">
        {/* Sequence 1 - HERO */}
        <HeroSection theme={theme} onRequestBriefing={onRequestBriefing} />

        {/* Sequence 2 - INTRODUCTION */}
        <IntroductionSection theme={theme} />

        {/* Sequence 3 - LIGHTSPEED PROPOSITION */}
        <LightSpeedProposition theme={theme} />

        {/* Sequence 4 - VISITOR PATHS */}
        <VisitorPathsSection theme={theme} />

        {/* Sequence 5 - COMMERCIAL SOLUTIONS OVERVIEW */}
        <WhatWeBuildGrid theme={theme} />

        {/* Sequence 6 - TECHNICAL GOVERNANCE (Technical sequence grouping starts) */}
        <HAOMTGVSection theme={theme} />
        <IntentToExecutionLifecycle theme={theme} />

        {/* Sequence 7 - HUMAN APPROVAL MATRIX */}
        <HumanApprovalMatrix theme={theme} />

        {/* Sequence 8 - WORKFORCE REGISTRY */}
        {/* Sequence 8 - WORKFORCE REGISTRY REMOVED */}

        {/* Sequence 9 - PHAROS HIGHLIGHTS */}
        <InsightsSection theme={theme} />

        {/* Sequence 10 - WHO WE ARE */}
        <AboutSection theme={theme} />

        {/* Sequence 11 - FAQ */}
        <FaqSection theme={theme} id="faq" />

        {/* Final CTA */}
        <DistinctCTA />

        {/* Global Footer */}
        <Footer theme={theme} />
      </main>
    </div>
  );
};

export default HomePage;
