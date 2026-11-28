import React from 'react';
import { AboutSection } from '../components/AboutSection';
import { BigImageSection } from '../components/site/BigImageSection';
import { ImageCarousel } from '../components/site/ImageCarousel';
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
     *   - hr-owner       | 90-role workforce roster and organizational culture
     * Last audited: 2026-10-18
     */}
  return (
    <>
      <BigImageSection
        theme={theme}
        src="/assets/images/philosophy_triptych_clean_1793818099752.avif"
        alt="LightSpeed philosophy"
        caption="Human direction. Intelligent execution. Measurable value."
      />
      <AboutSection
        theme={theme}
        onOpenContactModal={(intent) => onRequestBriefing(intent)}
      />
      <ImageCarousel
        theme={theme}
        images={[
          { src: '/assets/aistudio/who_we_are_background_df66900f.jpg', alt: 'Who we are', caption: 'Who we are.' },
          { src: '/assets/aistudio/HAOMTGV_Closed-Loop_AI_Pipeline_c8fb13d6.png', alt: 'Closed loop pipeline', caption: 'Closed-loop AI pipeline.' },
        ]}
      />
      <RelatedLinks
        theme={theme}
        links={[
          { to: '/what-we-do', label: 'What We Do' },
          { to: '/insights', label: 'Pharos' },
          { to: '/contact', label: 'Contact' },
        ]}
      />
    </>
  );
};

export default AboutPage;
