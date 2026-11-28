import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { BigImageSection } from '../components/site/BigImageSection';
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
      'LightSpeed Holdings Limited, Lilongwe, Malawi, operates this website. \u201cLightSpeed\u201d, \u201cwe\u201d, and \u201cus\u201d mean LightSpeed Holdings Limited.',
    ],
  },
  {
    heading: '2. Our Services',
    paragraphs: [
      'We provide websites, automation, reporting, digital marketing, data and analytics, agentic AI systems, and the AI Company Builder licence. We agree scope, price, and deliverables in writing for each engagement. This website does not itself create a binding offer.',
    ],
  },
  {
    heading: '3. Honesty & Claims',
    paragraphs: [
      'We do not invent client logos, testimonials, headcount figures, or ROI numbers. Published numbers must come from our verified operational record.',
    ],
  },
  {
    heading: '4. Payments & Invoicing',
    paragraphs: [
      'Local SMEs pay in Malawi Kwacha (MWK) through Airtel Money, TNM Mpamba, or bank transfer. We generally invoice NGO and international clients in USD on net-15 terms with 50% upfront. Cost descriptions on this site include the actual production cost of the deliverable. We publish unit economics alongside prices.',
    ],
  },
  {
    heading: '5. No Lock-In',
    paragraphs: [
      'You own your website, data, dashboards, and agents after delivery. We do not lock you into proprietary formats. If you leave, we help you take your assets with you.',
    ],
  },
  {
    heading: '6. Confidentiality & Security',
    paragraphs: [
      'We keep client information confidential by default. Our systems enforce least-privilege access, append-only SHA-256 sealed audit records, and human approval for consequential actions. We protect client data and disclose problems when they occur.',
    ],
  },
  {
    heading: '7. Intellectual Property',
    paragraphs: [
      'You own deliverables produced for you once you pay in full. LightSpeed Holdings Limited retains ownership of the underlying platform, templates, and agent orchestration engine. Where applicable, we license these to you, including under the AI Company Builder licence; we do not sell them.',
    ],
  },
  {
    heading: '8. Limitation of Liability',
    paragraphs: [
      'To the fullest extent permitted by Malawi law, our aggregate liability for an engagement is limited to the fees paid for that engagement. These terms do not limit liability that cannot be limited by law.',
    ],
  },
  {
    heading: '9. Governing Law',
    paragraphs: [
      'Malawi law governs these terms and any engagement governed by them. The courts of Malawi have jurisdiction over disputes.',
    ],
  },
];

/**
 * /legal/terms - service terms for the site and engagements.
 */
export const TermsPage: React.FC<TermsPageProps> = ({ theme }) => {
  const isLight = theme === 'light';

    {/*
     * AGENT TEAM NARRATIVE - TermsPage
     * Content fidelity governed by:
     *   - legal-owner     | Terms of Service, liability limits, and regulatory compliance
     *   - content-writer  | clear, plain-language translation of legal obligations
     * Last audited: 2026-10-18
     */}
  return (
    <>
      <BigImageSection theme={theme} src="/assets/aistudio/BeforeAfterSectorBackground_d538f2ff.jpg" alt="Terms" caption="Clear terms. Clear delivery." />
      <PageIntro
        theme={theme}
        eyebrow="LEGAL // TERMS"
        title="Terms of Service"
        lead="Last updated: September 2026. We deliver what we agree, label our claims, and respect your ownership of your data."
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
            LightSpeed Holdings Limited, Lilongwe, Malawi. Send questions about these terms through the contact page; a person will respond.
          </p>
        </div>
      </section>

      <CtaBand theme={theme} />
    </>
  );
};

export default TermsPage;
