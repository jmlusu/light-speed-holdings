import { 
  CatalogOfferFamily, 
  EnterpriseCapability, 
  CatalogIndustryVertical, 
  CatalogPlatformScenario, 
  CatalogProofPoint, 
  CatalogPolicyItem 
} from '../types';

export const CATALOG_POSITIONING = {
  company: "LightSpeed Holdings Limited™",
  location: "Lilongwe, Malawi",
  positioningLine: "The AI-native company builder for Southern Africa.",
  tagline: "ASPIRE. ACT. ACHIEVE.",
  platformDetails: "Governed 144-agent, 20-department orchestration platform (143 AI agents + 1 human CEO)",
  honestyClassification: "Nothing in this document has been delivered to paying clients. All offers are fieldable in 2026, in pilot, or in active development. Every proof point carries an explicit honesty-ladder badge. No fabricated metrics, testimonials, or client logos appear anywhere in this document."
};

export const CATALOG_METHOD = {
  title: "The AI Company Builder Platform",
  summary: "Governed multi-agent orchestration engine where 143 AI agents and 1 human CEO operate across 20 departments.",
  pipeline: "Brief → Inbox Task → Assigned Agent(s) → Human Review → Deliverable",
  governancePillars: [
    {
      title: "5-Tier Human-in-the-Loop (HITL) Approvals",
      description: "Agents execute; human CEO owns outcome. No client-facing deliverable ships without human sign-off. Approval gates block executor threads for up to 30 minutes per request."
    },
    {
      title: "4 Governance Gates (G1–G4)",
      description: "Every engagement must clear Contract (G1), Data Processing Agreement (G2), Compliance Review (G3), and Security Assessment (G4) before work begins."
    },
    {
      title: "Immutable Audit Trails",
      description: "Every action generates an append-only JSONL audit event — correlated, queryable, and never overwritten. Every approval is gated; every escalation documented."
    },
    {
      title: "Risk-Classified Agent Tiers",
      description: "5×5 likelihood × impact risk matrix mapped to 4 risk levels (low, medium, high, critical). 25 distinct actions are risk-gated in the approval matrix."
    },
    {
      title: "Board-Level Governance Cadence",
      description: "Weekly standup → bi-weekly product review → monthly management board review → quarterly strategy session → annual refresh."
    },
    {
      title: "AI Ethics Board Review",
      description: "Tier 3+ deliverables require AI Ethics Board review before delivery."
    }
  ],
  sovereignty: "Offline-first operation on local infrastructure, integrated with Malawi payment rails (Airtel Money, TNM Mpamba, PayChangu), compliant with Malawi Data Protection Act 2017/2024 and GDPR from day one. 9 LLM providers configured, including free local models via Ollama for budget-constrained deployments."
};

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
    description: 'The same 144-agent orchestration engine that runs LightSpeed Holdings can run on your infrastructure. License the AI Company Builder, get one-on-one onboarding, and operate your own governed AI workforce — self-hosted, provider-agnostic, and extensible.',
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

export const ENTERPRISE_CAPABILITIES: EnterpriseCapability[] = [
  {
    name: "Strategy & Roadmap",
    description: "Structured discovery → roadmap generation; assessment templates, ROI modeling",
    status: "In active development"
  },
  {
    name: "AI Design Sprint (5-day)",
    description: "5-day concept-to-prototype engagement: kickoff → research → prototype → demo → backlog",
    status: "In active development"
  },
  {
    name: "Forward-Deployed Engineers",
    description: "Embed AI agents within client teams as consulting capacity",
    status: "In active development"
  },
  {
    name: "Venture Co-Build",
    description: "Build AI-native ventures from scratch; equity stakes + consulting",
    status: "In active development"
  },
  {
    name: "Platform Licensing (Managed)",
    description: "Managed deployment with RBAC + client portals",
    status: "In active development"
  },
  {
    name: "Industry Accelerators",
    description: "Per-vertical agent presets, prompt packs, KPI dashboards",
    status: "In active development"
  },
  {
    name: "Client Portal / Self-Service",
    description: "Read-only client dashboard: project status, costs, deliverables",
    status: "In active development"
  }
];

export const CATALOG_INDUSTRIES: CatalogIndustryVertical[] = [
  {
    id: "agri",
    title: "Agriculture & Agritech",
    description: "Weather data, soil analysis, and mobile-money micro-loan risk assessments — agentic AI workflows helping smallholder farmers make better decisions and helping agri-businesses manage supply chains in offline-first SADC environments.",
    keyUseCases: [
      "Agentic weather + soil advisory for smallholder farmers (Ulangizi-style chatbot patterns)",
      "Mobile-money micro-loan risk assessment for agricultural cooperatives",
      "Supply chain monitoring and procurement automation for agri-businesses",
      "Chichewa-language farmer advisory agents (piloting with Ministry of Agriculture)"
    ],
    honestyBadge: "In pilot",
    honestyNote: "In pilot / Fieldable 2026. Chichewa language foundation being built via piloting initiative.",
    iconName: "Sprout"
  },
  {
    id: "health",
    title: "Public Health & M&E",
    description: "Monitor clinic supply chains, auto-generate procurement requests on Z-score anomaly detection, and produce donor-ready M&E reports from Kobo and DHIS2 data — moving field collection to boardroom reporting from weeks to hours.",
    keyUseCases: [
      "Clinic supply chain monitoring with Z-score anomaly detection and auto-procurement",
      "Donor-ready quarterly and annual M&E reports from Kobo/DHIS2 data",
      "Interactive program dashboards (mobile-friendly, NGO-grade)",
      "Citizen-query agents for public health information"
    ],
    honestyBadge: "In pilot (composing evidence)",
    honestyNote: "In pilot development composing evidence. No confirmed partnership with any named health organization has been signed.",
    iconName: "Activity"
  },
  {
    id: "fintech",
    title: "Financial Inclusion (VSLA / SACCO / Mobile Money)",
    description: "Agentic workflows over Airtel Money and TNM Mpamba rails, serving informal savings groups (VSLA/SACCO) and micro-finance institutions with automated savings tracking, mobile-money reconciliation, and credit scoring.",
    keyUseCases: [
      "Agentic workflows over Airtel Money and TNM Mpamba rails",
      "Automated savings tracking for VSLA/SACCO groups",
      "Micro-loan risk assessment for smallholder farmers",
      "Mobile-money reconciliation and reporting"
    ],
    honestyBadge: "In pilot",
    honestyNote: "In pilot (use case in active development). Development organizations working in financial inclusion are actively seeking this; no signed engagement exists.",
    iconName: "Coins"
  },
  {
    id: "sme",
    title: "SME & Services",
    description: "A 'Company-in-a-Box' lightweight agent set — Marketing, Sales, Compliance, Finance, HR — for Malawian SMEs that cannot afford a full team but need full capability. Demonstrated live at J&S StopOver Bar.",
    keyUseCases: [
      "AI-powered inventory, sales, and profitability monitoring (demonstrated at J&S StopOver Bar)",
      "Booking and guest communication automation for hospitality",
      "Lightweight agent sets for Marketing, Sales, Compliance, Finance, HR",
      "WhatsApp-native customer service for SMEs"
    ],
    honestyBadge: "Fieldable in 2026",
    honestyNote: "Fieldable 2026. J&S StopOver Bar provides live proof-of-concept.",
    iconName: "Building2"
  },
  {
    id: "gov",
    title: "Government / Public Sector",
    description: "Citizen-query agents, legislative summarization, project monitoring, and compliance reporting — built for the governance-first standards demanded by Malawi's DPA and SADC's digital transformation agenda.",
    keyUseCases: [
      "Compliance monitoring and regulatory reporting for government agencies",
      "Contract review and legal document analysis at scale",
      "Citizen-query agents for public service information",
      "Legislative summarisation and policy analysis",
      "HR and personnel management automation"
    ],
    honestyBadge: "In active development",
    honestyNote: "In active development. Governance framework mapped to Malawi DPA & SADC standards. National AI Strategy consultation draft published.",
    iconName: "Landmark"
  }
];

export const PLATFORM_SCENARIOS: CatalogPlatformScenario[] = [
  {
    id: "fow-01",
    code: "FOW-01",
    title: "Startup Acceleration",
    subtitle: "Solo Founder + Governed AI Workforce",
    description: "A solo founder operates with the functional coverage of a multi-person team: agents handle CTO, CFO, CMO, and CLO roles, with a CEO dashboard for real-time visibility. Founder sets vision; 143 agents execute operations.",
    honestyBadge: "Proven in-house",
    targetAudience: "Tech-savvy founders & solo entrepreneurs (LightSpeed itself operates as 1 human + 143 agents)."
  },
  {
    id: "fow-02",
    code: "FOW-02",
    title: "Enterprise Automation",
    subtitle: "Augment Existing Teams",
    description: "Existing teams gain specialist AI agents for compliance scanning, data pipelines, and contract review — without the 6-month hiring cycle. Adapts to organization structure via YAML configuration.",
    honestyBadge: "In active development",
    targetAudience: "SADC enterprise teams looking to automate compliance and operational bottlenecks."
  },
  {
    id: "fow-03",
    code: "FOW-03",
    title: "Consulting Firm Scale",
    subtitle: "Delivery Backbone for Professional Services",
    description: "Consulting firms sell expertise but are constrained by headcount. Agents handle research, analysis, and report generation; humans focus on client relationships and strategic advisory.",
    honestyBadge: "In active development",
    targetAudience: "Advisory, legal, and financial consulting firms across SADC."
  },
  {
    id: "fow-04",
    code: "FOW-04",
    title: "Non-Profit Operations",
    subtitle: "Full Capability with Minimal Staff",
    description: "A small non-profit gets coverage across finance, HR, compliance, M&E, and donor communications. Immutable audit trails provide the exact documentation grantmakers require. Supports local Ollama models for zero-API-cost deployment.",
    honestyBadge: "In active development",
    targetAudience: "Local NGOs, community cooperatives, and international grant recipients."
  },
  {
    id: "fow-05",
    code: "FOW-05",
    title: "Government Compliance",
    subtitle: "Authorisation-Aligned Public Sector AI",
    description: "AI agents handle compliance monitoring, contract review, and regulatory reporting. The 5-tier approval matrix aligns directly with government authorization levels and SADC digital transformation frameworks.",
    honestyBadge: "In active development",
    targetAudience: "State departments, regulatory agencies, and municipal administrations."
  },
  {
    id: "fow-06",
    code: "FOW-06",
    title: "E-Commerce Customer Success",
    subtitle: "24/7 WhatsApp Conversational Commerce",
    description: "Customer success, sales pipeline, and marketing analytics without shift-based human teams. Maintain customer context across interactions, process mobile-money checkouts, and escalate high-value issues.",
    honestyBadge: "In active development",
    targetAudience: "SADC mobile-first retailers & WhatsApp merchant networks."
  },
  {
    id: "fow-07",
    code: "FOW-07",
    title: "Healthcare Administration",
    subtitle: "Clinical Administrative Relief & Memory Encryption",
    description: "Billing compliance, patient scheduling, credentialing, and regulatory reporting — agents handle administrative burden so clinical staff focus on patients. Memory encryption and PII detection for Malawi DPA & GDPR compliance.",
    honestyBadge: "In active development",
    targetAudience: "Hospitals, private clinics, and rural health networks."
  },
  {
    id: "fow-08",
    code: "FOW-08",
    title: "Financial Services",
    subtitle: "Risk & Continuous Regulatory Compliance",
    description: "Continuous compliance monitoring, risk analysis, and audit preparation. The 5-tier approval matrix maps directly to financial services authorization levels and central bank reporting rules.",
    honestyBadge: "In active development",
    targetAudience: "Microfinance institutions, SACCOs, and regional banking providers."
  }
];

export const CATALOG_PROOF_POINTS: CatalogProofPoint[] = [
  {
    id: "proof-js-bar",
    title: "J&S StopOver Bar — Live SME Proof",
    category: "SME Proof",
    honestyBadge: "Live proof",
    badgeType: "live",
    description: "Real, non-tech SME in Malawi running agentic decision support. The system monitors inventory levels, sales velocity, cash reconciliation, procurement needs, and profitability — demonstrating that AI-native operations work in the informal economy.",
    whatItMonitorsOrProves: "Monitors inventory, sales, shortage detection, cash reconciliation, procurement triggers, and profitability tracking.",
    whyItMatters: "World's smallest AI-native bar: tangible proof that the AI Company Builder works outside a lab on a real business in a Malawian market."
  },
  {
    id: "proof-meta",
    title: "LightSpeed Holdings — The Meta Case Study",
    category: "Meta Case Study",
    honestyBadge: "Proven in-house",
    badgeType: "proven",
    description: "LightSpeed Holdings is its own first customer. The company runs on the same 144-agent, 20-department orchestration platform offered to clients. CEO directs strategy; 143 AI agents handle operations.",
    whatItMonitorsOrProves: "Proves 5-tier HITL approvals, immutable audit trails, RACI matrices, and governance controls operate daily in production.",
    whyItMatters: "Not a prototype or slide deck — an operating company that builds and relies on the exact software it licenses."
  },
  {
    id: "proof-health-pilot",
    title: "Health / M&E Clinic Supply Chain Monitoring",
    category: "Pilot in Development",
    honestyBadge: "In pilot (composing evidence)",
    badgeType: "pilot",
    description: "Agentic workflows for monitoring clinic supply chains and auto-generating procurement requests on Z-score anomaly detection.",
    whatItMonitorsOrProves: "Data collection to boardroom donor reporting accelerated from weeks to hours.",
    whyItMatters: "In pilot development composing evidence. Transparently notes no signed engagement exists yet."
  },
  {
    id: "proof-vsla-pilot",
    title: "VSLA / SACCO / Mobile Money Financial Inclusion",
    category: "Pilot in Development",
    honestyBadge: "In pilot",
    badgeType: "pilot",
    description: "Agentic workflows over Airtel Money and TNM Mpamba rails for informal savings groups and micro-finance institutions.",
    whatItMonitorsOrProves: "Automated savings tracking, mobile-money reconciliation, and smallholder farmer micro-loan risk assessment.",
    whyItMatters: "In active development targeting financial inclusion challenges across COMESA and SADC."
  },
  {
    id: "proof-chichewa-pilot",
    title: "Chichewa AI / Ministry of Agriculture Piloting",
    category: "Pilot in Development",
    honestyBadge: "In pilot",
    badgeType: "pilot",
    description: "Building the Chichewa-language foundation for farmer advisory, citizen-query, and public-service agents in Malawi's most spoken language.",
    whatItMonitorsOrProves: "Bilingual Chichewa & English natural language understanding and contextual agricultural reasoning.",
    whyItMatters: "Ensures AI capability is accessible to non-English speaking rural smallholder farmers."
  }
];

export const CATALOG_POLICIES: CatalogPolicyItem[] = [
  {
    id: "policy-national-ai",
    title: "National AI Strategy Consultation Submission",
    honestyBadge: "Published",
    summary: "Formal stakeholder submission to the Malawi Dept of E-Government / UNDP Inclusive Digital Transformation project.",
    description: "Advocates for governing actions (Agentic AI) alongside content (Generative AI). Proposes 4-tier HITL risk model, machine-readable agent identity, and data sovereignty."
  },
  {
    id: "policy-sadc-framework",
    title: "SADC Agentic AI Governance Framework",
    honestyBadge: "In active development",
    summary: "Regional operational governance standard for autonomous AI across SADC Member States.",
    description: "Authored by CEO Jack Mlusu and submitted to digital ministers, MACRA, CRASA, central banks, and regional development banks. Aligned with AU Continental AI Strategy."
  },
  {
    id: "policy-capacity-building",
    title: "University & Talent Capacity Building",
    honestyBadge: "In active development",
    summary: "Training and certification programs in partnership with Malawian universities (MUBAS, UNIMA).",
    description: "Builds a sovereign agentic-AI talent pipeline across Southern Africa so capability is developed locally rather than imported."
  }
];
