import React from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { CtaBand } from '../components/site/CtaBand';

interface PrivacyPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const SECTIONS: { heading: string; paragraphs: string[] }[] = [
  {
    heading: '1. What We Collect',
    paragraphs: [
      'When you use the contact form or ask us questions, we collect the information you provide: your name, title, organisation, email address, and the context of your inquiry.',
      'We do not collect payment card details on this site. Payment, when it happens, is agreed separately on the rails you specify — Airtel Money, TNM Mpamba, bank transfer, or international transfer for USD invoices.',
    ],
  },
  {
    heading: '2. How We Use It',
    paragraphs: [
      'We use the information solely to respond to your inquiry, prepare a proposal, deliver agreed services, and comply with our legal obligations. We do not sell your data to third parties, and we do not use it for unrelated marketing without your consent.',
    ],
  },
  {
    heading: '3. How We Store & Protect It',
    paragraphs: [
      'Personal data is stored with encryption at rest, access is limited to the people who need it to do their job, and every action is recorded on an audit trail.',
      'For donor-funded and international partners we apply a GDPR-comparable level of protection and documented consent for cross-border data flows. For all work inside Malawi we treat the Malawi Data Protection Act 2017 as the default baseline.',
    ],
  },
  {
    heading: '4. Your Rights',
    paragraphs: [
      'Under the Malawi Data Protection Act 2017 you may request access to, correction of, or deletion of your personal data. To exercise any of these rights, send a message through the contact page and we will respond within the timeframes the law requires.',
      'We retain inquiry data only as long as needed to serve you and to meet legal and audit obligations. After that, it is deleted.',
    ],
  },
  {
    heading: '5. Cookies & Analytics',
    paragraphs: [
      'This site uses functional local storage for theme preference (dark/light mode). We do not run third-party ad trackers or sell advertising profiles.',
    ],
  },
];

/**
 * /legal/privacy — data protection notice. Aligned to the Malawi Data
 * Protection Act 2017 and our GDPR-comparable posture for donor data.
 */
export const PrivacyPage: React.FC<PrivacyPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="LEGAL // PRIVACY"
        title="Privacy Policy"
        lead="Last updated: September 2026. This page explains what we collect, why, and the rights you hold over your data. It is written to be read — not to be indexed."
      />

      <section className={`px-4 sm:px-8 max-w-3xl mx-auto w-full pt-12 pb-4 ${
        isLight ? 'text-slate-700' : 'text-zinc-300'
      }`}>
        {SECTIONS.map((section) => (
          <div key={section.heading} className="mb-10">
            <h2 className={`font-display font-bold text-lg sm:text-xl tracking-tight ${
              isLight ? 'text-slate-900' : 'text-zinc-100'
            }`}>
              {section.heading}
            </h2>
            {section.paragraphs.map((p) => (
              <p key={p} className="mt-3 text-sm leading-relaxed">
                {p}
              </p>
            ))}
          </div>
        ))}
        <p className="text-xs leading-relaxed opacity-70">
          LightSpeed Holdings Limited, Lilongwe, Malawi. Questions about this policy reach a human through the contact page.
        </p>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default PrivacyPage;
