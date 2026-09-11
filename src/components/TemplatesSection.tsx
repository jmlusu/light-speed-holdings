import React from 'react';
import { TemplatesArtifacts } from './TemplatesArtifacts';

interface TemplatesSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const TemplatesSection: React.FC<TemplatesSectionProps> = ({ theme, onRequestBriefing }) => {
  return (
    <TemplatesArtifacts
      theme={theme}
      onRequestBriefing={onRequestBriefing}
    />
  );
};
