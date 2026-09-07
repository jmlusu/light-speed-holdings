export const services = [
  {
    id: 'agentic-company-building',
    title: 'Agentic AI Company Building',
    description: 'We architect multi-agent systems that run as self-contained AI-native enterprises — 144 agents orchestrating operations, governance, and growth on our own platform.',
    icon: 'agentic-building',
    slug: '/services/agentic-company-building',
    status: 'proven-in-house' as const,
  },
  {
    id: 'offer-a-brand-websites',
    title: 'Offer A — Brand Systems & Websites',
    description: 'Complete brand identity and web presence for organisations ready to lead. Strategy, design system, and production-ready Next.js/Astro sites.',
    icon: 'offer-a',
    slug: '/services/offer-a-brand-websites',
    status: 'fieldable-2026' as const,
  },
  {
    id: 'offer-b-whatsapp-assistants',
    title: 'Offer B — WhatsApp & Mobile Assistants',
    description: 'NLU-powered conversational agents on WhatsApp with local payment rails (Airtel Money, TNM Mpamba, PayChangu) — built for how people actually transact.',
    icon: 'offer-b',
    slug: '/services/offer-b-whatsapp-assistants',
    status: 'in-pilot' as const,
  },
  {
    id: 'offer-c-ngo-monitoring',
    title: 'Offer C — NGO Monitoring & Evaluation',
    description: 'Offline-first M&E platforms using KoboToolbox, DHIS2, and custom field agents. Designed for low-connectivity environments and data sovereignty.',
    icon: 'offer-c',
    slug: '/services/offer-c-ngo-monitoring',
    status: 'in-development' as const,
  },
  {
    id: 'governed-deployment',
    title: 'Governed Deployment Platform',
    description: 'Malawi DPA 2017/2024 + GDPR-aligned by default. 5-tier approvals, audit trails, human-in-the-loop gates — the infrastructure others retrofit.',
    icon: 'governance',
    slug: '/services/governed-deployment',
    status: 'proven-in-house' as const,
  },
]

export const industries = [
  {
    id: 'agriculture-agritech',
    title: 'Agriculture & Agritech',
    description: 'Chichewa AI Initiative with Ministry of Agriculture: 3.5M farmers targeted, 10K-farmer Mo9 pilot, MACRA IVR *384#, 50 Malawian ML engineers.',
    slug: '/industries/agriculture-agritech',
    icon: 'agriculture',
    stat: { label: 'Farmers targeted', value: '3.5M', suffix: '+' },
  },
  {
    id: 'public-health-me',
    title: 'Public Health & M&E',
    description: 'Offline-first monitoring for VSLA/SACCO health programmes. KoboToolbox + DHIS2 integration, field-agent workflows, informed-consent workflows.',
    slug: '/industries/public-health-me',
    icon: 'health',
    stat: { label: 'Field agents', value: '500', suffix: '+' },
  },
  {
    id: 'financial-inclusion',
    title: 'Financial Inclusion (VSLA/SACCO)',
    description: 'Digital transformation for village savings groups and cooperatives. Agent-based onboarding, mobile money integration, audit-ready ledgers.',
    slug: '/industries/financial-inclusion',
    icon: 'financial',
    stat: { label: 'Groups digitised', value: '1,200', suffix: '+' },
  },
  {
    id: 'sme-services',
    title: 'SME & Services',
    description: 'J&S StopOver Bar — the world\'s smallest AI-native bar. Real SME proof: automated inventory, WhatsApp ordering, Airtel/TNM payments.',
    slug: '/industries/sme-services',
    icon: 'sme',
    stat: { label: 'Revenue uplift', value: '27%', suffix: '' },
  },
  {
    id: 'government-public-sector',
    title: 'Government & Public Sector',
    description: 'Co-developing sovereign AI infrastructure with Ministry of Agriculture, MACRA, and UNDP Malawi. Policy-to-code pipelines, procurement-ready.',
    slug: '/industries/government-public-sector',
    icon: 'government',
    stat: { label: 'Institutional partners', value: '8', suffix: '' },
  },
]

export const partners = [
  { id: 'undp', name: 'UNDP Malawi', logo: 'undp', url: 'https://malawi.un.org/' },
  { id: 'world-bank', name: 'World Bank Malawi', logo: 'world-bank', url: 'https://www.worldbank.org/en/country/malawi' },
  { id: 'minag', name: 'Ministry of Agriculture', logo: 'minag', url: 'https://www.agriculture.gov.mw/' },
  { id: 'macra', name: 'MACRA', logo: 'macra', url: 'https://www.macra.mw/' },
  { id: 'ictam', name: 'ICTAM', logo: 'ictam', url: 'https://ictam.mw/' },
  { id: 'mhub', name: 'mHub', logo: 'mhub', url: 'https://mhubmw.com/' },
  { id: 'comesa', name: 'COMESA/IDEA', logo: 'comesa', url: 'https://comesa.int/' },
  { id: 'mubas', name: 'MUBAS', logo: 'mubas', url: 'https://mubas.ac.mw/' },
  { id: 'unima', name: 'UNIMA', logo: 'unima', url: 'https://www.unima.ac.mw/' },
]

export const caseStudies = [
  {
    id: 'chichewa-ai',
    title: 'Chichewa AI Initiative',
    client: 'Ministry of Agriculture, Malawi',
    industry: 'Agriculture & Agritech',
    status: 'in-pilot' as const,
    description: 'Digital Malawi P173456 ($100M IDA). Chichewa-language IVR (*384#) for 3.5M farmers. 10,000-farmer Mo9 pilot. 50 Malawian ML engineers trained.',
    slug: '/proof/chichewa-ai',
  },
  {
    id: 'js-stopover',
    title: 'J&S StopOver Bar',
    client: 'J&S StopOver (SME)',
    industry: 'SME & Services',
    status: 'proven-in-house' as const,
    description: 'World\'s smallest AI-native bar. Automated inventory, WhatsApp ordering, Airtel Money/TNM Mpamba payments. Live proof of Offer B stack.',
    slug: '/proof/js-stopover',
  },
  {
    id: 'vsla-sacco-digitisation',
    title: 'VSLA/SACCO Digitisation',
    client: 'NGO Consortium (pilot)',
    industry: 'Financial Inclusion',
    status: 'in-pilot' as const,
    description: '1,200+ savings groups digitised. Offline-first KoboToolbox collection, DHIS2 reporting, mobile money disbursement. Audit-ready by design.',
    slug: '/proof/vsla-sacco-digitisation',
  },
]

export const insights = [
  {
    id: 'state-of-agentic-ai-malawi',
    title: 'State of Agentic AI in Malawi',
    excerpt: 'The first comprehensive landscape review of agentic AI adoption, governance gaps, and talent pipelines in Malawi — produced by Pharos, our thought-leadership arm.',
    date: '15 August 2026',
    slug: '/insights/state-of-agentic-ai-malawi',
  },
  {
    id: 'sadc-agentic-ai-framework',
    title: 'SADC Agentic AI Governance Framework',
    excerpt: 'A regional framework for sovereign, interoperable agentic AI deployment across SADC member states — submitted to SADC Secretariat and UNDP.',
    date: '1 August 2026',
    slug: '/insights/sadc-agentic-ai-framework',
  },
  {
    id: 'h-a-o-m-t-g-v-framework',
    title: 'The H-A-O-M-T-G-V Framework',
    excerpt: 'Human-AI Orchestration, Oversight, Memory, Tool-use, Governance, Verification — our 7-pillar framework for building governed agentic enterprises.',
    date: '20 July 2026',
    slug: '/insights/h-a-o-m-t-g-v-framework',
  },
]