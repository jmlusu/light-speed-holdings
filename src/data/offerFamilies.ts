import { CatalogOfferFamily } from '../types';

/* Commercial catalog offer families (A–E). Migrated from
   src/data/useCaseCatalogData.ts (retired 2026-10-13); sole live consumer
   is WhatWeDoPage. Content is source-backed by OFFER_FAMILIES in git history. */
export const OFFER_FAMILIES: CatalogOfferFamily[] = [
  {
    id: 'offer-a',
    letter: 'A',
    title: 'Digital Presence',
    tagline: 'Your digital front door with local mobile-money checkout built in.',
    description: 'Every business in Malawi deserves a digital front door. LightSpeed builds mobile-first websites, e-commerce stores, and brand identities — with Airtel Money, TNM Mpamba, and PayChangu checkout built in from day one. Designed for the way Malawi actually transacts.',
    honestyBadge: 'Fieldable in 2026',
    targetClients: ['Local SMEs', 'Schools & Clinics', 'Hotels & Lodges', 'Agri-businesses', 'Churches & Real Estate'],
    governanceNote: 'Low-risk commodity service. Minimal PII; standard gates suffice.',
    pricingNote: '50% upfront / 50% on delivery for all one-off projects. Excludes ad spend, hosting, domain, and gateway fees.',
    deliverables: [
      {
        id: 'A1',
        name: 'A1 — Business Website',
        description: 'Up to 5 pages, mobile-first, contact form, WhatsApp button, hosting setup, 30 days support',
        priceMwk: 'MWK 800,000',
        priceUsd: '~$450',
        turnaround: '5–10 days'
      },
      {
        id: 'A2',
        name: 'A2 — E-commerce / Online Store',
        description: 'Product catalog, Airtel Money / Mpamba checkout, order notifications, 20 products',
        priceMwk: 'MWK 1,800,000',
        priceUsd: '~$1,000',
        turnaround: '10–15 days'
      },
      {
        id: 'A3',
        name: 'A3 — Brand Identity',
        description: 'Logo, color system, fonts, social media kit, letterhead',
        priceMwk: 'MWK 500,000',
        priceUsd: '~$280',
        turnaround: '3–5 days'
      },
      {
        id: 'A4',
        name: 'A4 — Google Business + Listings',
        description: 'Map listing, business info management, review setup',
        priceMwk: 'MWK 150,000',
        priceUsd: '~$85',
        turnaround: '2–3 days'
      }
    ]
  },
  {
    id: 'offer-b',
    letter: 'B',
    title: 'Business Process Automation',
    tagline: 'WhatsApp-native assistants & automated document pipelines.',
    description: 'WhatsApp-native assistants that handle FAQs, take orders, process bookings, and hand off to humans when complex. Integrated with Airtel Money and TNM Mpamba — no app download required. Includes document/report generators, form automation, and internal dashboards.',
    honestyBadge: 'In active development',
    targetClients: ['SMEs', 'Clinics & Hospitals', 'Schools', 'Agricultural Cooperatives', 'Transport Companies'],
    governanceNote: 'BLOCKED. WhatsApp customer data and cross-border LLM transfer require G1–G4 security review completion and liability cap ratification before sales opening.',
    pricingNote: 'Pricing is to be validated with prospects. B1 requires a recurring hosting commitment (MWK 100,000/mo, ~$56/mo). Excludes ad spend and hosting fees.',
    deliverables: [
      {
        id: 'B1',
        name: 'B1 — WhatsApp Customer Chatbot',
        description: 'FAQ + order/service automation, handoff to human, analytics dashboard',
        priceMwk: 'MWK 1,500,000',
        priceUsd: '~$850',
        turnaround: '7–14 days',
        blocked: true,
        blockedReason: 'G1–G4 security review pending',
        hostingFee: 'MWK 100,000/mo (~$56/mo)'
      },
      {
        id: 'B2',
        name: 'B2 — AI Document/Report Generator',
        description: 'Template-driven report generation (donor reports, payroll letters, certificates)',
        priceMwk: 'MWK 1,200,000',
        priceUsd: '~$680',
        turnaround: '7–14 days',
        blocked: true,
        blockedReason: 'Liability cap ratification pending'
      },
      {
        id: 'B3',
        name: 'B3 — Form + Survey Automation',
        description: 'Kobo/Google-Forms-to-spreadsheet pipeline, auto-alerts, summary dashboards',
        priceMwk: 'MWK 900,000',
        priceUsd: '~$500',
        turnaround: '5–10 days',
        blocked: true,
        blockedReason: 'G2 DPA review pending'
      },
      {
        id: 'B4',
        name: 'B4 — Internal Tool / Dashboard',
        description: 'Custom web dashboard for stock, sales, students, patients, or members',
        priceMwk: 'MWK 2,500,000',
        priceUsd: '~$1,400',
        turnaround: '10–20 days',
        blocked: true,
        blockedReason: 'G4 Security assessment pending'
      }
    ]
  },
  {
    id: 'offer-c',
    letter: 'C',
    title: 'Data, Analytics & Donor Reporting',
    tagline: 'Automate donor-ready reports from Kobo and DHIS2 data in hours, not weeks.',
    description: 'NGOs and development programmes spend weeks turning Kobo and DHIS2 data into donor-ready reports. LightSpeed automates that pipeline: clean the data, generate narrative reports against donor templates, and build interactive dashboards accessible on mobile.',
    honestyBadge: 'In active development',
    targetClients: ['NGOs & INGOs', 'Development Programmes', 'UN Agencies', 'Agricultural Cooperatives', 'Research Organizations'],
    governanceNote: 'BLOCKED. Donor data is treated as Tier-1 sensitive — requires explicit cross-border consent workflow for LLM provider APIs and professional liability cap before client engagement.',
    pricingNote: 'International NGOs expect USD quotes and pay in USD. Quoted at USD figure directly with terms (50% upfront, 50% on delivery).',
    deliverables: [
      {
        id: 'C1',
        name: 'C1 — Data Cleaning & Analysis',
        description: 'Clean dataset + insights report (Excel/PDF)',
        priceMwk: 'MWK 700,000',
        priceUsd: '~$400',
        turnaround: '3–7 days',
        blocked: true,
        blockedReason: 'Donor data waiver workflow in active development'
      },
      {
        id: 'C2',
        name: 'C2 — Donor/Project Reports',
        description: 'Narrative + data-visualized quarterly/annual reports compliant with donor templates',
        priceMwk: 'MWK 1,000,000',
        priceUsd: '~$550',
        turnaround: '5–10 days',
        blocked: true,
        blockedReason: 'Tier-1 sensitive data consent workflow pending'
      },
      {
        id: 'C3',
        name: 'C3 — Interactive Dashboard',
        description: 'Live web dashboard for program KPIs (mobile-friendly, NGO-grade)',
        priceMwk: 'MWK 2,000,000',
        priceUsd: '~$1,100',
        turnaround: '10–15 days',
        blocked: true,
        blockedReason: 'G3 Compliance review pending'
      },
      {
        id: 'C4',
        name: 'C4 — Survey Design + Analysis',
        description: 'Questionnaire design, data collection setup, analysis, recommendations',
        priceMwk: 'MWK 1,300,000',
        priceUsd: '~$720',
        turnaround: '7–14 days',
        blocked: true,
        blockedReason: 'Data protection waiver pending'
      }
    ]
  },
  {
    id: 'offer-d',
    letter: 'D',
    title: 'Digital Marketing',
    tagline: 'Bilingual (Chichewa + English) content, community management & ad campaigns.',
    description: 'Reach Malawian customers where they already are — Facebook, WhatsApp, Google — with bilingual content, community management, and ad campaigns. LightSpeed handles the content calendar, posting, and optimization so you can run your business.',
    honestyBadge: 'Fieldable in 2026',
    targetClients: ['SMEs', 'Local Businesses', 'Lodges & Resorts', 'Clinics & Pharmacies', 'Cooperatives'],
    governanceNote: 'Low-risk commodity service. Minimal PII; standard gates suffice.',
    pricingNote: 'Ad spend is excluded from all pricing.',
    deliverables: [
      {
        id: 'D1',
        name: 'D1 — Social Media Management',
        description: 'Content calendar, 12 posts/month (Chichewa + English), community management',
        priceMwk: 'MWK 350,000/mo',
        priceUsd: '~$200/mo',
        turnaround: 'Ongoing retainer'
      },
      {
        id: 'D2',
        name: 'D2 — Content Pack',
        description: '10 blog articles + 20 social captions',
        priceMwk: 'MWK 600,000',
        priceUsd: '~$340',
        turnaround: '5–10 days'
      },
      {
        id: 'D3',
        name: 'D3 — Google/Facebook Ads Setup',
        description: 'Campaign setup, pixel, tracking, 2-week optimization',
        priceMwk: 'MWK 700,000',
        priceUsd: '~$400',
        turnaround: '3–5 days'
      }
    ]
  },
  {
    id: 'offer-e',
    letter: 'E',
    title: 'Platform Licensing',
    tagline: 'Run your own governed AI workforce self-hosted on your infrastructure.',
    description: 'The same 90-role orchestration engine that runs LightSpeed Holdings can run on your infrastructure. License the AI Company Builder, get one-on-one onboarding, and operate your own governed AI workforce - self-hosted, provider-agnostic, and extensible.',
    honestyBadge: 'Fieldable in 2026',
    targetClients: ['Tech-Savvy Founders', 'Local Tech Agencies', 'Diaspora Entrepreneurs', 'Software Developers'],
    governanceNote: 'No client data handling; product license only. No G1–G4 blocking.',
    pricingNote: 'E1 is a one-off license fee plus recurring support retainer of MWK 350,000/mo (~$200/mo). E2 agency setup pricing upon inquiry.',
    deliverables: [
      {
        id: 'E1',
        name: 'E1 — AI Company Builder License',
        description: 'One-on-one onboarding, your own governed AI company running on your laptop/VPS',
        priceMwk: 'MWK 3,500,000',
        priceUsd: '~$2,000',
        turnaround: '1–2 weeks setup',
        hostingFee: 'Support Retainer: MWK 350,000/mo (~$200/mo)'
      },
      {
        id: 'E2',
        name: 'E2 — Agent Setup for Agencies',
        description: 'White-label: we stand up agent teams for your agency\'s clients',
        priceMwk: 'Custom Quote',
        priceUsd: 'Custom Quote',
        turnaround: 'Project-based'
      }
    ]
  }
];
