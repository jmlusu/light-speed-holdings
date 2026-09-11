import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Boxes, Building2, ArrowRight } from 'lucide-react';
import { CoreOfferingsSection } from '../components/CoreOfferingsSection';

interface OfferingsPageProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

/* ────────────────────────────────────────────────────────────────────────────
   CLIENT SERVICE CATALOG DATA
   Source: docs/client-facing/USE-CASE-CATALOG.md (Offer A–E + Enterprise line)
   ──────────────────────────────────────────────────────────────────────────── */

type BadgeTone = 'fieldable' | 'development' | 'blocked';

interface BadgePill {
  label: string;
  tone: BadgeTone;
}

interface DeliverableRow {
  id: string;
  name: string;
  description: string;
  priceMWK: string;
  priceUSD: string;
  turnaround: string;
}

interface OfferFamily {
  code: string;
  eyebrow: string;
  title: string;
  narrative: string;
  badges: BadgePill[];
  rows: DeliverableRow[];
  targetClients: string;
  governanceNote: string;
  pricingNote?: string;
}

interface EnterpriseRow {
  capability: string;
  description: string;
  status: string;
}

const BADGE_STYLES: Record<BadgeTone, string> = {
  fieldable: 'bg-ls-cyan/10 text-ls-cyan border-ls-cyan/30',
  development: 'bg-slate-400/10 text-slate-400 border-slate-400/30',
  blocked: 'bg-red-500/10 text-ls-red border-ls-red/30',
};

const serviceFamilies: OfferFamily[] = [
  {
    code: 'A',
    eyebrow: 'OFFER A // DIGITAL PRESENCE',
    title: 'Digital Presence',
    narrative:
      'Every business in Malawi deserves a digital front door. LightSpeed builds mobile-first websites, e-commerce stores, and brand identities — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one. From MWK 150,000 (~$85) for a Google Business listing to a full online store with 20 products, we design for the way Malawi actually transacts.',
    badges: [{ label: 'FIELDABLE IN 2026', tone: 'fieldable' }],
    rows: [
      {
        id: 'A1',
        name: 'A1 — Business Website',
        description: 'Up to 5 pages, mobile-first, contact form, WhatsApp button, hosting setup, 30 days support',
        priceMWK: 'MWK 800,000',
        priceUSD: '~$450',
        turnaround: '5–10 days'
      },
      {
        id: 'A2',
        name: 'A2 — E-commerce / Online Store',
        description: 'Product catalog, Airtel Money / Mpamba checkout, order notifications, 20 products',
        priceMWK: 'MWK 1,800,000',
        priceUSD: '~$1,000',
        turnaround: '10–15 days'
      },
      {
        id: 'A3',
        name: 'A3 — Brand Identity',
        description: 'Logo, color system, fonts, social media kit, letterhead',
        priceMWK: 'MWK 500,000',
        priceUSD: '~$280',
        turnaround: '3–5 days'
      },
      {
        id: 'A4',
        name: 'A4 — Google Business + Listings',
        description: 'Map listing, business info management, review setup',
        priceMWK: 'MWK 150,000',
        priceUSD: '~$85',
        turnaround: '2–3 days'
      }
    ],
    targetClients: 'Local SMEs, schools, clinics, hotels/lodges, agri-businesses, churches, real estate.',
    governanceNote: 'Low-risk commodity service. Minimal PII; standard gates suffice.'
  },
  {
    code: 'B',
    eyebrow: 'OFFER B // BUSINESS PROCESS AUTOMATION',
    title: 'Business Process Automation',
    narrative:
      'Your customers are already on WhatsApp. LightSpeed builds WhatsApp-native assistants that handle FAQs, take orders, process bookings, and hand off to a human when the conversation gets complex. Integrated with Airtel Money and TNM Mpamba for instant mobile-money checkout — no app download required.',
    badges: [
      { label: 'IN ACTIVE DEVELOPMENT', tone: 'development' },
      { label: 'BLOCKED — DO NOT SELL', tone: 'blocked' }
    ],
    rows: [
      {
        id: 'B1',
        name: 'B1 — WhatsApp Customer Chatbot',
        description: 'FAQ + order/service automation, handoff to human, analytics dashboard',
        priceMWK: 'MWK 1,500,000',
        priceUSD: '~$850',
        turnaround: '7–14 days'
      },
      {
        id: 'B2',
        name: 'B2 — AI Document/Report Generator',
        description: 'Template-driven report generation (donor reports, payroll letters, certificates)',
        priceMWK: 'MWK 1,200,000',
        priceUSD: '~$680',
        turnaround: '7–14 days'
      },
      {
        id: 'B3',
        name: 'B3 — Form + Survey Automation',
        description: 'Kobo/Google-Forms-to-spreadsheet pipeline, auto-alerts, summary dashboards',
        priceMWK: 'MWK 900,000',
        priceUSD: '~$500',
        turnaround: '5–10 days'
      },
      {
        id: 'B4',
        name: 'B4 — Internal Tool / Dashboard',
        description: 'Custom web dashboard for stock, sales, students, patients, or members',
        priceMWK: 'MWK 2,500,000',
        priceUSD: '~$1,400',
        turnaround: '10–20 days'
      }
    ],
    targetClients: 'SMEs, clinics, schools, cooperatives, transport companies.',
    governanceNote:
      'BLOCKED — delivery awaits completion of the G1–G4 security review and liability cap ratification. Sales opening when governance gates clear.',
    pricingNote: 'B1 requires MWK 100,000/mo recurring hosting.'
  },
  {
    code: 'C',
    eyebrow: 'OFFER C // DATA, ANALYTICS & DONOR REPORTING',
    title: 'Data, Analytics & Donor Reporting',
    narrative:
      'NGOs and development programmes spend weeks turning Kobo and DHIS2 data into donor-ready reports. LightSpeed automates that pipeline: clean the data, generate narrative reports against donor templates, and build interactive dashboards your field team can access on a phone. All hosted in-region, all compliant with Malawi\u2019s Data Protection Act.',
    badges: [
      { label: 'IN ACTIVE DEVELOPMENT', tone: 'development' },
      { label: 'BLOCKED — DO NOT SELL', tone: 'blocked' }
    ],
    rows: [
      {
        id: 'C1',
        name: 'C1 — Data Cleaning & Analysis',
        description: 'Clean dataset + insights report (Excel/PDF)',
        priceMWK: 'MWK 700,000',
        priceUSD: '~$400',
        turnaround: '3–7 days'
      },
      {
        id: 'C2',
        name: 'C2 — Donor/Project Reports',
        description: 'Narrative + data-visualized quarterly/annual reports compliant with donor templates',
        priceMWK: 'MWK 1,000,000',
        priceUSD: '~$550',
        turnaround: '5–10 days'
      },
      {
        id: 'C3',
        name: 'C3 — Interactive Dashboard',
        description: 'Live web dashboard for program KPIs (mobile-friendly, NGO-grade)',
        priceMWK: 'MWK 2,000,000',
        priceUSD: '~$1,100',
        turnaround: '10–15 days'
      },
      {
        id: 'C4',
        name: 'C4 — Survey Design + Analysis',
        description: 'Questionnaire design, data collection setup, analysis, recommendations',
        priceMWK: 'MWK 1,300,000',
        priceUSD: '~$720',
        turnaround: '7–14 days'
      }
    ],
    targetClients: 'NGOs, development programmes, UN agencies, cooperatives, research organizations.',
    governanceNote:
      'BLOCKED — donor data treated as Tier-1 sensitive; requires explicit cross-border consent workflow and professional liability cap before any client engagement.'
  },
  {
    code: 'D',
    eyebrow: 'OFFER D // DIGITAL MARKETING',
    title: 'Digital Marketing',
    narrative:
      'Reach Malawian customers where they already are — Facebook, WhatsApp, Google — with localised content, community management, and ad campaigns. LightSpeed handles the content calendar, the posting, and the optimisation so you can run the business.',
    badges: [{ label: 'FIELDABLE IN 2026', tone: 'fieldable' }],
    rows: [
      {
        id: 'D1',
        name: 'D1 — Social Media Management',
        description: 'Content calendar, 12 posts/month, community management',
        priceMWK: 'MWK 350,000/mo',
        priceUSD: '~$200/mo',
        turnaround: 'Ongoing retainer'
      },
      {
        id: 'D2',
        name: 'D2 — Content Pack',
        description: '10 blog articles + 20 social captions',
        priceMWK: 'MWK 600,000',
        priceUSD: '~$340',
        turnaround: '5–10 days'
      },
      {
        id: 'D3',
        name: 'D3 — Google/Facebook Ads Setup',
        description: 'Campaign setup, pixel, tracking, 2-week optimization',
        priceMWK: 'MWK 700,000',
        priceUSD: '~$400',
        turnaround: '3–5 days'
      }
    ],
    targetClients: 'SMEs, local businesses, lodges, clinics, cooperatives.',
    governanceNote: 'Low-risk commodity service. Minimal PII; standard gates suffice.',
    pricingNote: 'Ad spend excluded from all pricing.'
  },
  {
    code: 'E',
    eyebrow: 'OFFER E // PLATFORM LICENSING',
    title: 'Platform Licensing',
    narrative:
      'The same 144-agent orchestration engine that runs LightSpeed Holdings can run on your infrastructure. License the AI Company Builder, get one-on-one onboarding, and operate your own governed AI workforce — self-hosted, provider-agnostic, and extensible. For agencies: white-label agent teams for your clients.',
    badges: [{ label: 'FIELDABLE IN 2026 — PROVEN IN-HOUSE', tone: 'fieldable' }],
    rows: [
      {
        id: 'E1',
        name: 'E1 — AI Company Builder License',
        description: 'One-on-one onboarding, your own governed AI company running on your laptop/VPS',
        priceMWK: 'MWK 3,500,000',
        priceUSD: '~$2,000',
        turnaround: '1–2 weeks setup'
      },
      {
        id: 'E2',
        name: 'E2 — Agent Setup for Agencies',
        description: "White-label: we stand up agent teams for your agency's clients",
        priceMWK: 'Contact for quote',
        priceUSD: '—',
        turnaround: '—'
      }
    ],
    targetClients: 'Tech-savvy founders, local agencies, diaspora entrepreneurs, developers.',
    governanceNote: 'No client data handling; product license only. No G1–G4 blocking.',
    pricingNote:
      'E1 is a one-off license fee plus a recurring support retainer of MWK 350,000/mo (~$200/mo). E2 in active development with no public pricing.'
  }
];

const enterpriseLine: EnterpriseRow[] = [
  {
    capability: 'Strategy & Roadmap',
    description: 'Structured discovery → roadmap generation; assessment templates, ROI modeling',
    status: 'In active development'
  },
  {
    capability: 'AI Design Sprint (5-day)',
    description: '5-day concept-to-prototype engagement: kickoff → research → prototype → demo → backlog',
    status: 'In active development'
  },
  {
    capability: 'Forward-Deployed Engineers',
    description: 'Embed AI agents within client teams as consulting capacity',
    status: 'In active development'
  },
  {
    capability: 'Venture Co-Build',
    description: 'Build AI-native ventures from scratch; equity stakes + consulting',
    status: 'In active development'
  },
  {
    capability: 'Platform Licensing (Managed Hosting)',
    description: 'Managed deployment with RBAC + client portals',
    status: 'In active development'
  },
  {
    capability: 'Industry Accelerators',
    description: 'Per-vertical agent presets, prompt packs, KPI dashboards',
    status: 'In active development'
  },
  {
    capability: 'Client Portal / Self-Service',
    description: 'Read-only client dashboard: project status, costs, deliverables',
    status: 'In active development'
  }
];

/* ── Shared render helpers (same file — no new component files) ── */

const renderEyebrow = (label: string, icon: React.ReactNode) => (
  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
    {icon}
    <span>{label}</span>
  </div>
);

const renderBadgePills = (badges: BadgePill[]) => (
  <div className="flex flex-wrap items-center gap-2">
    {badges.map((pill) => (
      <span
        key={pill.label}
        className={`inline-flex items-center px-2.5 py-1 rounded-full border font-mono text-[10px] font-bold tracking-wider ${BADGE_STYLES[pill.tone]}`}
      >
        {pill.label}
      </span>
    ))}
  </div>
);

interface OffersTableProps {
  theme: 'light' | 'dark';
  rows: DeliverableRow[];
}

const OffersTable: React.FC<OffersTableProps> = ({ theme, rows }) => {
  const isLight = theme === 'light';
  return (
    <div className="mt-6">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse min-w-[640px]">
          <thead>
            <tr className={`border-b ${isLight ? 'border-slate-300 bg-slate-100/80 text-slate-800' : 'border-white/10 bg-zinc-900/50 text-zinc-300'}`}>
              <th className="p-3 font-mono font-bold">Deliverable</th>
              <th className="p-3 font-mono font-bold">Description</th>
              <th className="p-3 font-mono font-bold whitespace-nowrap">Price (MWK)</th>
              <th className="p-3 font-mono font-bold whitespace-nowrap">~USD</th>
              <th className="p-3 font-mono font-bold whitespace-nowrap">Turnaround</th>
            </tr>
          </thead>
          <tbody className={`divide-y ${isLight ? 'divide-slate-200 text-slate-700' : 'divide-white/10 text-zinc-300'}`}>
            {rows.map((row) => (
              <tr key={row.id} className={isLight ? 'hover:bg-slate-50' : 'hover:bg-white/[0.02]'}>
                <td className="p-3 font-bold font-mono whitespace-nowrap">{row.name}</td>
                <td className="p-3">{row.description}</td>
                <td className="p-3 font-mono font-bold whitespace-nowrap text-ls-red">{row.priceMWK}</td>
                <td className="p-3 font-mono whitespace-nowrap">{row.priceUSD}</td>
                <td className="p-3 font-mono whitespace-nowrap">{row.turnaround}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className={`mt-2 text-right text-[10px] font-mono tracking-wider ${isLight ? 'text-slate-400' : 'text-zinc-500'}`}>
        SCROLL HORIZONTALLY ON MOBILE →
      </div>
    </div>
  );
};

/**
 * Core Offerings page. Owns the activePillar state plus the ?offering=N
 * deep link that used to live on the (now hub) Capabilities page.
 *
 * Page order: intro → client service catalog (Offer A–E) → enterprise
 * transformation line → internal Four Connected Core Offerings architecture
 * → CTA band.
 */
export const OfferingsPage: React.FC<OfferingsPageProps> = ({ theme, onRequestBriefing }) => {
  const isLight = theme === 'light';
  const [searchParams] = useSearchParams();
  const initialPillar = Number(searchParams.get('offering'));
  const [activePillar, setActivePillar] = useState(
    Number.isFinite(initialPillar) && initialPillar >= 0 && initialPillar <= 3 ? initialPillar : 0
  );

  const handleSelectPillar = (idx: number) => {
    setActivePillar(idx);
    const url = new URL(window.location.href);
    url.searchParams.set('offering', String(idx));
    window.history.replaceState(null, '', url.toString());
  };

  return (
    <>
      {/* Page Intro */}
      <header className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-16 sm:pt-24 pb-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
          <Boxes className="w-3.5 h-3.5" />
          <span>INTEGRATED ARCHITECTURE</span>
        </div>
        <h1 className={`mt-4 text-3xl sm:text-5xl font-black tracking-tight font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
          Four Connected Core Offerings
        </h1>
        <p className={`mt-4 max-w-2xl text-sm sm:text-base leading-relaxed ${isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'}`}>
          Strategy compiles into private knowledge graphs, structured AI teams, and audited core execution. Explore each offering's contracts, lineage, and deliverables below.
        </p>
      </header>

      {/* ================================================================
          NEW SECTION 1 — FIVE CLIENT OFFER FAMILIES (A–E)
          ================================================================ */}
      <section className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="max-w-3xl mb-12 space-y-3">
          {renderEyebrow('CLIENT SERVICE CATALOG', <Boxes className="w-3.5 h-3.5" />)}
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Five Offer Families, One Governed Backbone
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Nothing has been delivered to paying clients yet. Everything below is honest-badged: fieldable in 2026, in active development, or blocked pending governance gates.
          </p>
        </div>

        <div className="space-y-12">
          {serviceFamilies.map((offer) => (
            <div
              key={offer.code}
              className={`relative overflow-hidden rounded-3xl p-6 sm:p-8 ${
                isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
              }`}
            >
              {/* Corner screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
                <span className="font-mono text-[11px] tracking-widest text-ls-red font-bold">
                  {offer.eyebrow}
                </span>
                {renderBadgePills(offer.badges)}
              </div>

              <h3 className={`text-xl sm:text-2xl font-black tracking-tight font-display ${
                isLight ? 'text-slate-900' : 'text-white'
              }`}>
                {offer.title}
              </h3>

              <p className={`mt-3 max-w-3xl text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
              }`}>
                {offer.narrative}
              </p>

              <OffersTable theme={theme} rows={offer.rows} />

              <div className={`mt-4 space-y-1.5 text-xs leading-relaxed ${
                isLight ? 'text-slate-600' : 'text-zinc-400'
              }`}>
                <p>
                  <span className="font-mono font-bold text-ls-cyan">TARGET CLIENTS // </span>
                  {offer.targetClients}
                </p>
                <p>
                  <span className="font-mono font-bold text-ls-red">GOVERNANCE // </span>
                  {offer.governanceNote}
                </p>
                {offer.pricingNote && (
                  <p>
                    <span className={`font-mono font-bold ${isLight ? 'text-slate-500' : 'text-zinc-500'}`}>PRICING // </span>
                    {offer.pricingNote}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ================================================================
          NEW SECTION 2 — ENTERPRISE TRANSFORMATION LINE
          ================================================================ */}
      <section className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="max-w-3xl mb-10 space-y-3">
          {renderEyebrow('ENTERPRISE CONSULTANCY', <Building2 className="w-3.5 h-3.5" />)}
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            The Enterprise Transformation Line
          </h2>
          <p className={`text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            For organizations that need more than a productized deliverable. These services are in active development — modules are being built, not yet production-ready — and are included for completeness.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse min-w-[560px]">
            <thead>
              <tr className={`border-b ${isLight ? 'border-slate-300 bg-slate-100/80 text-slate-800' : 'border-white/10 bg-zinc-900/50 text-zinc-300'}`}>
                <th className="p-3 font-mono font-bold">Capability</th>
                <th className="p-3 font-mono font-bold">Description</th>
                <th className="p-3 font-mono font-bold">Status</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${isLight ? 'divide-slate-200 text-slate-700' : 'divide-white/10 text-zinc-300'}`}>
              {enterpriseLine.map((row) => (
                <tr key={row.capability} className={isLight ? 'hover:bg-slate-50' : 'hover:bg-white/[0.02]'}>
                  <td className="p-3 font-bold font-mono whitespace-nowrap">{row.capability}</td>
                  <td className="p-3">{row.description}</td>
                  <td className="p-3 font-mono font-bold whitespace-nowrap text-slate-400">{row.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className={`mt-2 text-right text-[10px] font-mono tracking-wider ${isLight ? 'text-slate-400' : 'text-zinc-500'}`}>
          SCROLL HORIZONTALLY ON MOBILE →
        </div>

        <p className={`mt-4 text-xs font-mono tracking-wider font-bold ${
          isLight ? 'text-slate-500' : 'text-slate-400'
        }`}>
          HONESTY NOTE // Enterprise line: in active development — modules not yet built.
        </p>
      </section>

      {/* Existing architecture model (internal operating model) */}
      <CoreOfferingsSection
        theme={theme}
        onRequestBriefing={onRequestBriefing}
        activePillar={activePillar}
        onSelectPillar={handleSelectPillar}
      />

      {/* ================================================================
          NEW CTA BAND — BOOK A DISCOVERY CALL
          ================================================================ */}
      <section className={`px-4 sm:px-8 py-24 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className={`relative overflow-hidden rounded-3xl p-8 sm:p-12 text-center ${
          isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
        }`}>
          {/* Corner screws */}
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

          <div className="max-w-2xl mx-auto space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-ls-red/30 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest">
              <span className="w-2 h-2 rounded-full bg-ls-red shadow-sm shadow-ls-red/80 animate-pulse" />
              <span>COMMENCE TRANSFORMATION</span>
            </div>
            <h2 className={`text-3xl sm:text-4xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              The Conversation Starts with a Discovery Call
            </h2>
            <p className={`text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Whether you are an enterprise lead in Lilongwe, an NGO programme manager in Blantyre, a diaspora entrepreneur in Johannesburg, or a policymaker in Lusaka — we will map your challenge to the right offer, the right governance posture, and the right price point, in MWK or USD.
            </p>
            <div className="pt-2">
              <button
                onClick={() => onRequestBriefing()}
                className="inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-white shadow-lg shadow-ls-red/30 transition-all cursor-pointer hover:brightness-110"
              >
                Book a Discovery Call
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default OfferingsPage;
