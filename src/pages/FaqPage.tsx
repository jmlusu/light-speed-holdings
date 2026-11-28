import React, { useEffect } from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { FaqCardList } from '../components/FaqCardList';
import { CtaBand } from '../components/site/CtaBand';
import { RelatedLinks } from '../components/site/RelatedLinks';
import { BigImageSection } from '../components/site/BigImageSection';

interface FaqPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const FaqPage: React.FC<FaqPageProps> = ({ theme }) => {
  useEffect(() => {
    document.title = 'Frequently Asked Questions | LightSpeed Holdings';
  }, []);

  return (
    <>
      <BigImageSection theme={theme} src="/assets/images/pharos_ai_governance_1793514972204.avif" alt="FAQ" caption="Governance you can trust." />
      <PageIntro
        theme={theme}
        eyebrow="HONEST ANSWERS // REGISTRY §15"
        title="Frequently Asked Questions"
        lead="Get direct answers about how the platform works, including what we have not proven yet. Each answer includes its evidence citations."
      />

      <section className="px-6 lg:px-12 max-w-7xl mx-auto w-full pt-6 pb-20">
        <FaqCardList theme={theme} />
      </section>

      <CtaBand theme={theme} />

      <RelatedLinks
        theme={theme}
        links={[
          { to: '/what-we-do', label: 'What We Do' },
          { to: '/haomtgv', label: 'HAOMTGV Framework' },
          { to: '/insights', label: 'Pharos' },
          { to: '/contact', label: 'Contact Us' },
        ]}
      />
    </>
  );
};

export default FaqPage;
