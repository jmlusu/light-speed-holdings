import React from 'react';
import { BigImageSection } from '../components/site/BigImageSection';
import { ShieldCheck } from 'lucide-react';
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
      'When you use the contact form or ask a question, we collect the information you provide: your name, title, organisation, email address, and inquiry context.',
      'We do not collect payment card details on this site. We agree payment separately through your chosen method: Airtel Money, TNM Mpamba, bank transfer, or international transfer for USD invoices.',
    ],
  },
  {
    heading: '2. How We Use It',
    paragraphs: [
      'We use your information to respond to your inquiry, prepare a proposal, deliver agreed services, and meet legal obligations. We do not sell your data. We do not use it for unrelated marketing without your consent.',
    ],
  },
  {
    heading: '3. How We Store & Protect It',
    paragraphs: [
      'We store personal data with encryption at rest, limit access to people who need it for their work, and record actions on an audit trail.',
      'For donor-funded and international partners, we apply GDPR-comparable protection and document consent for cross-border data flows. For work inside Malawi, we use the Malawi Data Protection Act, 2024 as the default legal baseline.',
    ],
  },
  {
    heading: '4. Your Rights',
    paragraphs: [
      'Under the Malawi Data Protection Act, 2024, you may request access to, correction of, or deletion of your personal data. Send your request through the contact page. We will respond within the timeframes required by law.',
      'We retain inquiry data only as long as needed to serve you and meet legal and audit obligations. We then delete it.',
    ],
  },
  {
    heading: '5. Cookies & Analytics',
    paragraphs: [
      'This site uses functional local storage for your dark or light theme preference. We do not run third-party ad trackers or sell advertising profiles.',
    ],
  },
];

/**
 * /legal/privacy - data protection notice. Aligned to the Malawi Data
 * Protection Act 2017 and our GDPR-comparable posture for donor data.
 */
export const PrivacyPage: React.FC<PrivacyPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

    {/*
     * AGENT TEAM NARRATIVE - PrivacyPage
     * Content fidelity governed by:
     *   - legal-owner        | GDPR, Malawi DPA, and international privacy regulations
     *   - data-privacy-owner | data handling policies, cookie consent, and user rights
     * Last audited: 2026-10-18
     */}
  return (
    <>
      <BigImageSection theme={theme} src="/assets/images/val_prop_bg_night_1793997847272.avif" alt="Privacy" caption="Your data, governed." />
      <PageIntro
        theme={theme}
        eyebrow="LEGAL // PRIVACY"
        title="Privacy Policy"
        lead="Last updated: September 2026. This policy explains what we collect, why we collect it, and your rights over your data."
      />

      <section className="px-6 lg:px-12 max-w-4xl mx-auto w-full pt-10 pb-16">
        <div className="longform-contrast-layer rounded-3xl p-6 sm:p-10 lg:p-12 space-y-10">
          {/* Legal Counsel Disclaimer Box */}
          <div className={`p-4 sm:p-5 rounded-2xl flex items-start gap-3.5 ${
            isLight
              ? 'bg-cyan-50/80 text-ls-navy border border-cyan-200/70'
              : 'bg-cyan-950/40 text-slate-100 border border-cyan-500/20 shadow-md'
          }`}>
            <ShieldCheck className="w-5 h-5 text-ls-cyan shrink-0 mt-0.5" aria-hidden="true" />
            <p className="text-xs sm:text-sm leading-relaxed font-medium">
              <strong className="font-bold text-ls-red">Disclaimer: </strong>
              This page describes LightSpeed Holdings Limited's general digital operating baseline. Executed Master Services Agreements (MSAs) and Statements of Work (SOWs), reviewed by qualified legal counsel, govern bespoke client engagements, enterprise licences, and specific project deliverables.
            </p>
          </div>

          <div className="space-y-10">
            {SECTIONS.map((section) => (
              <div key={section.heading}>
                <h2 className={`font-display font-bold text-lg sm:text-xl tracking-tight mb-3 ${
                  isLight ? 'text-ls-navy' : 'text-white'
                }`}>
                  {section.heading}
                </h2>
                <div className="space-y-3">
                  {section.paragraphs.map((p) => (
                    <p key={p} className={`text-sm sm:text-base leading-relaxed ${
                      isLight ? 'text-slate-800' : 'text-slate-100'
                    }`}>
                      {p}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <p className={`text-xs leading-relaxed pt-6 border-t ${
            isLight ? 'border-slate-200 text-slate-500' : 'border-white/10 text-slate-400'
          }`}>
            LightSpeed Holdings Limited, Lilongwe, Malawi. Send questions about this policy through the contact page; a person will respond.
          </p>
        </div>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default PrivacyPage;
