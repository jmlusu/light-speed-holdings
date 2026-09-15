import React from 'react';
import { PageIntro } from '../components/site/PageIntro';
import { CtaBand } from '../components/site/CtaBand';

interface TermsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

const SECTIONS: { heading: string; paragraphs: string[] }[] = [
  {
    heading: '1. Who We Are',
    paragraphs: [
      'This website is operated by LightSpeed Holdings Limited, Lilongwe, Malawi. References to \u201cLightSpeed\u201d, \u201cwe\u201d, or \u201cus\u201d mean LightSpeed Holdings Limited.',
    ],
  },
  {
    heading: '2. Our Services',
    paragraphs: [
      'We provide websites, automation, reporting, digital marketing, data and analytics, agentic AI systems, and the AI Company Builder license. Scope, price, and deliverables are agreed in writing per engagement — nothing on this website is itself an offer that binds either party.',
    ],
  },
  {
    heading: '3. Honesty & Claims',
    paragraphs: [
      'We label every claim with its evidence status: Proven in-house, In pilot, Fieldable, or In development. Please treat statuses precisely as they read — we do, and we expect the same in return. If a marketing statement ever overstates what we can prove, tell us; that is a bug we will fix.',
    ],
  },
  {
    heading: '4. Payments & Invoicing',
    paragraphs: [
      'Local SMEs pay in Malawi Kwacha (MWK) via Airtel Money, TNM Mpamba, or bank transfer. NGO and international clients are invoiced in USD, generally net-15 with a 50% upfront payment. Every description of cost on this site includes what the deliverable actually costs to produce — we publish unit economics, not just prices.',
    ],
  },
  {
    heading: '5. No Lock-In',
    paragraphs: [
      'Your website, data, dashboards, and agents are yours after delivery. We do not lock you into proprietary formats, and we help you take your assets with you if you leave.',
    ],
  },
  {
    heading: '6. Confidentiality & Security',
    paragraphs: [
      'We apply a strict non-disclosure posture to client information by default. Our systems enforce least-privilege access, immutable audit trails, and human approval on consequential actions. We treat client data as if it were our own, and we are transparent the moment something goes wrong.',
    ],
  },
  {
    heading: '7. Intellectual Property',
    paragraphs: [
      'Deliverables produced for you belong to you once paid in full. Our underlying platform, templates, and agent orchestration engine remain the property of LightSpeed Holdings Limited and are licensed to you where applicable (for example, under the AI Company Builder license), not sold.',
    ],
  },
  {
    heading: '8. Limitation of Liability',
    paragraphs: [
      'To the fullest extent permitted by the laws of Malawi, our aggregate liability for any engagement is limited to the fees paid for that engagement. Nothing in these terms limits liability that cannot be limited by law.',
    ],
  },
  {
    heading: '9. Governing Law',
    paragraphs: [
      'These terms and any engagement governed by them are subject to the laws of the Republic of Malawi, and any disputes are subject to the jurisdiction of the courts of Malawi.',
    ],
  },
];

/**
 * /legal/terms — service terms for the site and engagements.
 */
export const TermsPage: React.FC<TermsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <>
      <PageIntro
        theme={theme}
        eyebrow="LEGAL // TERMS"
        title="Terms of Service"
        lead="Last updated: September 2026. The short version: we ship what we promise, we are transparent about every claim, and your data is yours."
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
          LightSpeed Holdings Limited, Lilongwe, Malawi. Questions about these terms reach a human through the contact page.
        </p>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default TermsPage;
