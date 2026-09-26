import React from 'react';
import { AiCompanyBuilderSection } from '../components/AiCompanyBuilderSection';

interface AiCompanyBuilderPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const AiCompanyBuilderPage: React.FC<AiCompanyBuilderPageProps> = ({ theme, onRequestBriefing }) => {
  return (
    <AiCompanyBuilderSection
      theme={theme}
      onRequestBriefing={onRequestBriefing}
    />
  );
};

export default AiCompanyBuilderPage;
