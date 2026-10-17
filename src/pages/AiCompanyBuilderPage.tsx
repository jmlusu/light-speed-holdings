import React from 'react';
import { AiCompanyBuilderSection } from '../components/AiCompanyBuilderSection';
import { PublicAgentRegistry } from '../components/PublicAgentRegistry';
import { RelatedLinks } from '../components/site/RelatedLinks';

interface AiCompanyBuilderPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const AiCompanyBuilderPage: React.FC<AiCompanyBuilderPageProps> = ({ theme, onRequestBriefing }) => {
    {/*
     * AGENT TEAM NARRATIVE - AiCompanyBuilderPage
     * Content fidelity governed by:
     *   - registry-owner     | company-registry.yaml metrics, agent roster, departments
     *   - creative-director  | orchestrates the creative production stack flow
     *   - dashboard-owner    | KPI collectors, engagement metrics, conversion tracking
     * Last audited: 2026-10-18
     */}
  return (
    <>
      <AiCompanyBuilderSection
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />
      <PublicAgentRegistry theme={theme} />
      <RelatedLinks
        theme={theme}
        links={[
          { to: '/use-cases', label: 'Use Cases' },
          { to: '/insights', label: 'Insights' },
          { to: '/solutions', label: 'Solutions' },
        ]}
      />
    </>
  );
};

export default AiCompanyBuilderPage;
