import React from 'react';
import { AiCompanyBuilderSection } from '../components/AiCompanyBuilderSection';
import { PublicAgentRegistry } from '../components/PublicAgentRegistry';

interface AiCompanyBuilderPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const AiCompanyBuilderPage: React.FC<AiCompanyBuilderPageProps> = ({ theme, onRequestBriefing }) => {
  return (
    <>
      <AiCompanyBuilderSection
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />
      <PublicAgentRegistry theme={theme} />
    </>
  );
};

export default AiCompanyBuilderPage;
