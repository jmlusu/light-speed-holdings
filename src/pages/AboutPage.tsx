import React from 'react';
import { AboutSection } from '../components/AboutSection';
import { RelatedLinks } from '../components/site/RelatedLinks';

interface AboutPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const AboutPage: React.FC<AboutPageProps> = ({ theme, onRequestBriefing }) => {
  return (
    <>
      <AboutSection
        theme={theme}
        onOpenContactModal={(intent) => onRequestBriefing(intent)}
      />
      <RelatedLinks
        theme={theme}
        links={[
          { to: '/use-cases', label: 'Use Cases' },
          { to: '/insights', label: 'Insights' },
          { to: '/contact', label: 'Contact' },
        ]}
      />
    </>
  );
};

export default AboutPage;
