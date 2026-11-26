import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ShieldCheck } from 'lucide-react';

import { OperatingModelOverview } from '../components/whatwedo/OperatingModelOverview';
import { SixCapabilitiesSection } from '../components/whatwedo/SixCapabilitiesSection';
import { IntegratedCapabilityMap } from '../components/whatwedo/IntegratedCapabilityMap';
import { DeliveryLifecycleSection } from '../components/whatwedo/DeliveryLifecycleSection';
import { BeforeAfterWorkflow } from '../components/BeforeAfterWorkflow';
import { DistinctCTA } from '../components/DistinctCTA';


interface WhatWeDoPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const WhatWeDoPage: React.FC<WhatWeDoPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';

  return (
    <div className={`min-h-screen ${isLight ? 'bg-[#F7F8F9] text-ls-navy' : 'bg-[#0A0D14] text-white'}`}>
      <main id="main-content" className="relative z-10 w-full">

        {/* 2. OPERATING MODEL OVERVIEW (HAOMTGV) */}
        <OperatingModelOverview theme={theme} />
        <div className="section-divider-navy" />

        {/* 3. SIX CAPABILITY AREAS */}
        <SixCapabilitiesSection theme={theme} />
        <div className="section-divider-cyan" />

        {/* WORKFLOW COLLAPSING ARCHITECTURE (BEFORE / AFTER WORKFLOW) */}
        <BeforeAfterWorkflow theme={theme} />
        <div className="section-divider-navy" />

        {/* 4. INTEGRATED CAPABILITY MAP */}
        <IntegratedCapabilityMap theme={theme} />
        <div className="section-divider-navy" />

        {/* 5. DELIVERY APPROACH */}
        <DeliveryLifecycleSection theme={theme} />
        <div className="section-divider-cyan" />

        {/* 6. ENGAGEMENT CTA */}
        <DistinctCTA
          theme={theme}
          title="Ready to Transform Your Operating Model?"
          subtitle="Speak with LightSpeed to assess workflow readiness and design a governed HAOMTGV architecture for your organisation."
          primaryActionText="Contact Us"
          primaryActionHref="/contact"
          secondaryActionText="EXPLORE PHAROS"
          secondaryActionHref="/insights"
        />


      </main>
    </div>
  );
};

export default WhatWeDoPage;
