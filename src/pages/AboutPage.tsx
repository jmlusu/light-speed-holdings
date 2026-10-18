import React from 'react';
import { AboutSection } from '../components/AboutSection';
import { RelatedLinks } from '../components/site/RelatedLinks';

interface AboutPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const AboutPage: React.FC<AboutPageProps> = ({ theme, onRequestBriefing }) => {
    {/*
     * AGENT TEAM NARRATIVE - AboutPage
     * Content fidelity governed by:
     *   - content-writer | company mission, values, and core narrative
     *   - hr-owner       | 90-agent workforce roster and organizational culture
     * Last audited: 2026-10-18
     */}
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
