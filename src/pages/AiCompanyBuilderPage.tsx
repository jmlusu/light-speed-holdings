import React from 'react';
import { AiCompanyBuilderSection } from '../components/AiCompanyBuilderSection';
import { PublicAgentRegistry } from '../components/PublicAgentRegistry';
import { RelatedLinks } from '../components/site/RelatedLinks';

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
      <RelatedLinks
        theme={theme}
        links={[
          { to: '/proof#metrics', label: 'Proof' },
          { to: '/insights', label: 'Insights' },
          { to: '/solutions', label: 'Solutions' },
        ]}
      />
    </>
  );
};

export default AiCompanyBuilderPage;
