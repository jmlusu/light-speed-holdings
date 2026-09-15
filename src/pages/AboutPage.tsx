import React from 'react';
import { AboutSection } from '../components/AboutSection';

interface AboutPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const AboutPage: React.FC<AboutPageProps> = ({ theme, onRequestBriefing }) => {
  return (
    <AboutSection
      theme={theme}
      onOpenContactModal={(intent) => onRequestBriefing(intent)}
    />
  );
};

export default AboutPage;
