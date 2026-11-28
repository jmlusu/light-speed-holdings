import React from 'react';
import { HeroSection } from '../components/HeroSection';
import { BigImageSection } from '../components/site/BigImageSection';
import { WhatWeBuildGrid } from '../components/home/WhatWeBuildGrid';
import { HAOMTGVSection } from '../components/home/HAOMTGVSection';
import { IntentToExecutionLifecycle } from '../components/home/IntentToExecutionLifecycle';
import { InsightsSection } from '../components/home/InsightsSection';
import { AboutSection } from '../components/home/AboutSection';
import { FaqSection } from '../components/site/FaqSection';
import { DistinctCTA } from '../components/DistinctCTA';

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

        {/* Sequence 2 - BIG IMAGERY / MISSION */}
        <BigImageSection
          theme={theme}
          src="/assets/images/identity_triptych_foundations_1793818127924.avif"
          alt="LightSpeed mission and vision"
          caption="ASPIRE. ACT. ACHIEVE. — building AI-native companies from Malawi to Africa."
        />

        {/* Sequence 5 - COMMERCIAL SOLUTIONS OVERVIEW */}
        <WhatWeBuildGrid theme={theme} />

        {/* Sequence 6 - TECHNICAL GOVERNANCE (Technical sequence grouping starts) */}
        <HAOMTGVSection theme={theme} />
        <IntentToExecutionLifecycle theme={theme} />

        {/* Sequence 8 - WORKFORCE REGISTRY */}
        {/* Sequence 8 - WORKFORCE REGISTRY REMOVED */}

        {/* Sequence 9 - PHAROS HIGHLIGHTS */}
        <InsightsSection theme={theme} />

        {/* Sequence 10 - WHO WE ARE */}
        <AboutSection theme={theme} />

        {/* Sequence 11 - FAQ */}
        <FaqSection theme={theme} id="faq" />

        {/* Final CTA */}
        <DistinctCTA theme={theme} />
      </main>
    </div>
  );
};

export default HomePage;
