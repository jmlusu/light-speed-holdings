import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  ArrowRight, 
  CheckCircle2, 
  Cpu, 
  Layers, 
  ShieldCheck, 
  Workflow, 
  Zap, 
  TrendingUp, 
  Building2, 
  Landmark, 
  Globe2, 
  Sparkles, 
  ChevronRight,
  ChevronDown,
  ChevronUp,
  HelpCircle,
  Search,
  BookOpen,
  FileText,
  Clock,
  Send,
  ExternalLink,
  Coins,
  Shield,
  FileCheck,
  Compass,
  Brain,
  Download,
  Check,
  Network,
  GitMerge,
  Lock,
  RefreshCw,
  Activity,
  ArrowDownRight,
  ArrowUpRight,
  Database
} from 'lucide-react';
import { Agent } from '../types';
import { InteractiveOperatingModel } from './InteractiveOperatingModel';
import { TransformationDiagnostic } from './TransformationDiagnostic';
import { TemplatesArtifacts } from './TemplatesArtifacts';
import { TactileRockerSwitch, TactileRotaryKnob, AcousticVentGrille } from './TactileHardwareElements';
import { StatusBadge } from './ui/StatusBadge';
import { SovereignConstellation } from './SovereignConstellation';
import { MethodFramework } from './MethodFramework';
import { ProofShowcase } from './ProofShowcase';
import { EcosystemCarousel } from './EcosystemCarousel';
import { SadcGovernanceFramework } from './SadcGovernanceFramework';
import { NationalAiStrategySubmission } from './NationalAiStrategySubmission';
import { UseCaseCatalogSection } from './UseCaseCatalogSection';
import heroSadcAi from '../assets/images/hero_sadc_ai_1789078232203.jpg';
import agritechSadc from '../assets/images/agritech_sadc_1789078246558.jpg';
import fintechHubSadc from '../assets/images/fintech_hub_sadc_1789078259804.jpg';
import solarGridSadc from '../assets/images/solar_grid_sadc_1789078270848.jpg';
import pharosBeaconLake from '../assets/images/pharos_beacon_lake_1789078282970.jpg';

interface CorporateLandingProps {
  onRequestBriefing: (summary?: string) => void;
  onSelectAgentForModal: (agent: Agent) => void;
  agentsList: Agent[];
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export const CorporateLanding: React.FC<CorporateLandingProps> = ({
  onRequestBriefing,
  onSelectAgentForModal,
  agentsList,
  theme = 'dark',
  onToggleTheme
}) => {
  const isLight = theme === 'light';
  const [activePillar, setActivePillar] = useState<number>(0);
  const [selectedSynergy, setSelectedSynergy] = useState<string>('strategy-intelligence');
  const [selectedIndustry, setSelectedIndustry] = useState<string>('agritech');
  const [contactSubmitted, setContactSubmitted] = useState<boolean>(false);

  // FAQ Interactive & Accessibility State
  const [faqCategory, setFaqCategory] = useState<string>('all');
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0); // First question open by default
  const [faqSearchQuery, setFaqSearchQuery] = useState<string>('');
  const [contactFormData, setContactFormData] = useState({
    name: '',
    title: '',
    organization: '',
    email: '',
    scope: 'Advisory Architecture Sprint (2 Weeks)',
    objective: '',
    timeline: 'Within 30 days'
  });

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setContactSubmitted(true);
  };

  // The 3 Productized Offer Lines + 2 Enterprise Lines (Honesty-Tagged)
  const coreCapabilities: {
    id: string;
    title: string;
    shortTitle: string;
    eyebrow: string;
    tagline: string;
    desc: string;
    metrics: string;
    inputContract: string;
    outputContract: string;
    upstreamSource: string;
    downstreamTarget: string;
    governance: string;
    tier: 'proven-in-house' | 'pilot' | 'fieldable-2026' | 'in-development';
    deliverables: string[];
  }[] = [
    {
      id: 'offer-a',
      title: 'High-Velocity Digital Presence & Brand Systems',
      shortTitle: 'Web & Brand Systems',
      eyebrow: 'PRODUCTIZED LINE A // ENTERPRISE IDENTITY',
      tagline: 'Precision Web Architectures, Design Systems & Motion Interfaces',
      desc: 'Crafting responsive, high-performance web applications, board-grade digital assets, and brand design systems tailored for Southern African corporations, institutions, and international ventures.',
      metrics: '< 1.2s Global Load & Tailwind v4 Architecture',
      inputContract: 'Corporate Identity Briefs, Regulatory Requirements & Communication Objectives',
      outputContract: 'Production Web Architectures, Interactive Showcases & Design Token Libraries',
      upstreamSource: 'Informed by institutional positioning and audience research',
      downstreamTarget: 'Directly channels high-intent inbound inquiries to Autonomous Conversational Assistants (Line B)',
      governance: 'WCAG AA / Next.js & React 19 Standards',
      tier: 'fieldable-2026',
      deliverables: [
        'Production Next.js / React Enterprise Web Scaffolds',
        'Hardware-Grade Tactile UI Component Libraries',
        'Multi-lingual Localization (English / Chichewa / Portuguese)',
        'Zero-Tracker Fast-Loading Compliance Layouts'
      ]
    },
    {
      id: 'offer-b',
      title: 'WhatsApp & Mobile Agentic Assistants',
      shortTitle: 'WhatsApp & Mobile NLU',
      eyebrow: 'PRODUCTIZED LINE B // CONVERSATIONAL RAILS',
      tagline: 'Vernacular NLU, Voice Interfaces & Airtel/TNM/PayChangu Integrations',
      desc: 'Building autonomous conversational agents that live where Malawian and SADC users actually are: WhatsApp, SMS, and low-bandwidth mobile channels. Integrated with local mobile money rails and bilingual Chichewa/English NLU.',
      metrics: 'Sub-second NLU & Native Mobile Money Handshakes',
      inputContract: 'WhatsApp User Audio/Text Prompts, Catalog Inventories & Transaction Intents',
      outputContract: 'Dispatched Airtel/TNM/PayChangu Checkout Links, Bookings & Factual Answers',
      upstreamSource: 'Grounded by private enterprise knowledge bases and verified catalogs',
      downstreamTarget: 'Pipes reconciled transactions to accounting ledgers and core ERP systems',
      governance: 'Malawi DPA 2017/2024 & WhatsApp Business API Guardrails',
      tier: 'pilot',
      deliverables: [
        'Bilingual Chichewa & English Speech-to-Text / Intent Classification',
        'Native Airtel Money, TNM Mpamba & PayChangu Payment Dispatch',
        '24/7 Autonomous Concierge, Reservations & Order Management',
        'Deterministic Escalation to Human Staff for Edge Cases'
      ]
    },
    {
      id: 'offer-c',
      title: 'NGO M&E & Fiduciary Field Telemetry',
      shortTitle: 'NGO M&E & Kobo/DHIS2',
      eyebrow: 'PRODUCTIZED LINE C // DEVELOPMENT SECTOR',
      tagline: 'Offline-First Field Data Synchronization & Donor-Grade Audit Chains',
      desc: 'Bridging remote rural field enumerators, community health workers, and agricultural extension teams with central donor reporting. Native offline caching with automated reconciliation into DHIS2 and KoboToolbox.',
      metrics: '100% Offline-Resilient Field Capture & Zero Telemetry Loss',
      inputContract: 'Raw Enumerator Surveys, GPS Geo-Pings, Multi-Modal Field Imagery',
      outputContract: 'Automated DHIS2 Datasets, Kobo Form Aggregations & Fiduciary Audit Dossiers',
      upstreamSource: 'Field devices in low-connectivity rural districts across Malawi',
      downstreamTarget: 'Dispatches synthesized impact reports directly to donor dashboards (UNDP, USAID, World Bank)',
      governance: 'GDPR / Malawi DPA / Fiduciary Anti-Diversion Protocols',
      tier: 'in-development',
      deliverables: [
        'Offline-First Progressive Web App (PWA) Enumerator Clients',
        'Automated Bi-directional DHIS2 & KoboToolbox Connectors',
        'Satellite & Drone Cross-Verification of Infrastructure Milestones',
        'Cryptographic Anti-Tamper Signatures on Beneficiary Records'
      ]
    },
    {
      id: 'enterprise-01',
      title: '144-Agent Sovereign Company Builder',
      shortTitle: '144-Agent Enterprise Builder',
      eyebrow: 'ENTERPRISE ARCHITECTURE 01 // AGENTIC SCALE',
      tagline: 'YAML-Defined Autonomous Corporate Hierarchies & Task Buses',
      desc: 'Deploying structured hierarchies of 144 specialized AI agents operating across Executive, Departmental, and Specialist tiers. Managed via single-source-of-truth registries, OpenCode-native cards, and deterministic DAG message buses.',
      metrics: '144 Discrete Agent Roles & Sub-Second Task Buses',
      inputContract: 'Corporate Mandates, Departmental Budgets & High-Level Objectives',
      outputContract: 'Executed Code Commits, Audited Spreadsheets, Strategy Briefs & Compliance Reports',
      upstreamSource: 'Boardroom directives and scheduled governance sweeps',
      downstreamTarget: 'Executes across business operations through canonical 7-tool sandboxes',
      governance: 'OpenCode Canonical 7-Tool Permission Boundaries',
      tier: 'proven-in-house',
      deliverables: [
        'OpenCode Agent Roster with Role-Bounded Permission Schemas',
        'Deterministic Task Queue & Async Message Bus (.opencode/inbox.json)',
        'Autonomous Multi-Agent Collaboration DAGs & Consensus Arbiters',
        'Continuous Model Drift Monitoring & Automated Tool Runners'
      ]
    },
    {
      id: 'enterprise-02',
      title: 'Governed Deployment & Compliance Platform',
      shortTitle: 'Governed Deployment Platform',
      eyebrow: 'ENTERPRISE ARCHITECTURE 02 // TRUST & SOVEREIGNTY',
      tagline: 'Malawi DPA 2017/2024 Translation, 5-Tier Approval Gates & On-Soil Compute',
      desc: 'An institutional governance wrapper providing air-gapped model inference, cryptographic SHA-256 audit logging, and automated policy-as-code validation. Ensures full statutory compliance without telemetry leaking overseas.',
      metrics: '100% On-Soil Residency & Cryptographic Audit Trails',
      inputContract: 'Regulatory Statutes (Malawi DPA, King IV, Basel) & Sensitive Corporate Records',
      outputContract: 'Immutable Audit Hash-Chains, Fiduciary Gate Approvals & Compliance Certifications',
      upstreamSource: 'All agent and user operations across the organizational stack',
      downstreamTarget: 'Provides statutory verification dossiers for national regulatory audits',
      governance: 'Malawi DPA 2017/2024 & ISO/IEC 42001 AI Management Standard',
      tier: 'fieldable-2026',
      deliverables: [
        '5-Tier Cryptographic Human-in-the-Loop (HITL) Gatekeeper Engine',
        'Periodic HITL Expiry Sweeper Preventing Stale Blocked States',
        'Air-Gapped Sovereign Model Runtimes with Zero Foreign Telemetry',
        'Automated Regulatory Cross-Mapping to Malawi DPA & SADC Treaties'
      ]
    }
  ];

  // Interconnected Synergy Matrix Pairs
  const synergyPairs: Record<string, {
    title: string;
    from: string;
    to: string;
    headline: string;
    mechanism: string;
    compoundImpact: string;
  }> = {
    'strategy-intelligence': {
      title: 'Strategy ↔ Intelligence',
      from: '01. Strategy',
      to: '02. Private Intelligence',
      headline: 'Policy-Governed Knowledge Synthesis',
      mechanism: 'Statutory compliance policies and corporate mandates are encoded as machine-readable schema filters, ensuring the semantic knowledge graph strictly enclaves confidential data and enforces SADC regulatory jurisdiction rules before indexing.',
      compoundImpact: '100% elimination of unauthorized data leakage across cross-border business units.'
    },
    'intelligence-systems': {
      title: 'Intelligence ↔ Autonomous Systems',
      from: '02. Private Intelligence',
      to: '03. Autonomous Systems',
      headline: 'Deterministic RAG Grounding',
      mechanism: 'Air-gapped knowledge graphs supply real-time entity linking and verified document citations to agent fleets, preventing LLM hallucinations and grounding every operational recommendation in immutable source records.',
      compoundImpact: 'Zero hallucination risk with sub-200ms factual retrieval across millions of legacy records.'
    },
    'systems-execution': {
      title: 'Autonomous Systems ↔ Execution',
      from: '03. Autonomous Systems',
      to: '04. Fiduciary & Execution',
      headline: 'Verified Autonomous Settlement',
      mechanism: 'Specialist agent hierarchies decompose complex transactions into atomic API payloads and route high-value operations through cryptographic Human-in-the-Loop (HITL) approval gates before writing to core banking or customs EDI mainframes.',
      compoundImpact: 'Reconciliation times compressed from 72 hours to 14 minutes with zero unverified writes.'
    },
    'execution-strategy': {
      title: 'Execution ↔ Strategy (Feedback Loop)',
      from: '04. Fiduciary & Execution',
      to: '01. Strategy',
      headline: 'Closed-Loop Telemetry & Adaptive Policy',
      mechanism: 'Live transaction latency, recovered revenue yield, exception rates, and agent drift telemetry are piped directly into executive dashboards, allowing board committees to adjust business policies and capital allocation dynamically.',
      compoundImpact: 'Quarterly strategy cycles converted into real-time computable operational optimization.'
    }
  };

  const industriesData: Record<string, {
    label: string;
    title: string;
    subtitle: string;
    description: string;
    citation: string;
    image: string;
    imageCaption: string;
    impact: string[];
    tier: 'pilot' | 'in-development' | 'proven-in-house' | 'fieldable-2026';
  }> = {
    agritech: {
      label: 'AGRICULTURE & AGRITECH',
      title: 'Agricultural Extension, Crop Telemetry & Smallholder NLU',
      subtitle: 'Bilingual Chichewa voice diagnostic pipelines, drone crop scouting, and cooperative aggregation.',
      description: 'Supporting commercial estates (tea, macadamia, coffee) and smallholder farmer cooperatives through localized Chichewa/English NLU, offline crop disease diagnostic tools, and automated cooperative produce aggregation.',
      citation: 'Malawi Vision 2063 Pillar 1: Agricultural Productivity & Commercialization',
      image: agritechSadc,
      imageCaption: 'Thyolo & Mulanje Agricultural Estates // IoT Crop & Soil Telemetry',
      tier: 'pilot',
      impact: [
        'Bilingual Chichewa/English pest and disease identification model running on WhatsApp.',
        'Offline-capable cooperative aggregation reducing produce grading delays.',
        'Extends extension officer reach from 1:2,500 to digital scale.'
      ]
    },
    health: {
      label: 'PUBLIC HEALTH & M&E',
      title: 'Community Health Telemetry & DHIS2 Field Synchronizers',
      subtitle: 'Offline-first clinic registries, maternal health tracking, and donor-grade telemetry.',
      description: 'Equipping rural health surveillance assistants (HSAs) with offline-first mobile data capture, automated DHIS2 / KoboToolbox synchronization, and algorithmic supply chain alerts for essential medicines.',
      citation: 'National Digital Health Strategy & SADC Health Protocol',
      image: pharosBeaconLake,
      imageCaption: 'Rural Health Center Telemetry & Solar Clinic Node // Lake Malawi Basin',
      tier: 'in-development',
      impact: [
        'Zero-data loss offline-first synchronization for remote clinic health workers.',
        'Automated drug stock-out alerts routed before regional depot depletion.',
        'Donor-compliant audit verification generated directly from raw field records.'
      ]
    },
    vsla: {
      label: 'FINANCIAL INCLUSION',
      title: 'VSLA & SACCO Autonomous Ledgers & Mobile Money',
      subtitle: 'Village savings reconciliation, automated share-outs, and credit history genesis.',
      description: 'Bridging informal village savings groups and microfinance institutions through WhatsApp voice ledger reconciliation, automated share-out math, and verifiable credit scoring on top of Airtel Money and TNM Mpamba.',
      citation: 'National Financial Inclusion Strategy & Reserve Bank of Malawi Framework',
      image: fintechHubSadc,
      imageCaption: 'Lilongwe Digital Finance Hub // Mobile Money & SACCO Micro-Reconciliation',
      tier: 'in-development',
      impact: [
        'Eliminates paper ledger disputes through voice-confirmed SMS/WhatsApp entries.',
        'Generates verifiable credit histories for unbanked micro-entrepreneurs.',
        'Direct API integration pathways for local mobile network operators.'
      ]
    },
    sme: {
      label: 'SME & COMMERCIAL SERVICES',
      title: 'Autonomous SME Operations, Concierge & PayChangu Rails',
      subtitle: 'Conversational booking, automated inventory, and instant payment settlement.',
      description: 'Transforming local hospitality (such as J&S StopOver Lodge), retail, and professional service operators into AI-streamlined businesses with automated customer response, reservation management, and PayChangu checkout links.',
      citation: 'Proven in-house across Malawian hospitality and commerce deployments',
      image: heroSadcAi,
      imageCaption: 'Commercial Operations & SME Digital Suite // Lilongwe Business District',
      tier: 'proven-in-house',
      impact: [
        '24/7 autonomous guest concierge handling reservations and inquiries.',
        'Integrated PayChangu and mobile money payment links dispatched automatically.',
        'Supplier procurement orders scheduled without manual staff overhead.'
      ]
    },
    government: {
      label: 'GOVERNMENT & PUBLIC SECTOR',
      title: 'Sovereign Compliance, Customs Auditing & Citizen Services',
      subtitle: 'Malawi DPA 2017/2024 translation, border manifest audit, and air-gapped governance.',
      description: 'Assisting statutory bodies, revenue agencies, and ministries to deploy secure on-soil AI systems that comply with national data protection laws, automate customs manifest audits, and triage citizen queries.',
      citation: 'Malawi Data Protection Act 2017/2024 & SADC Cross-Border Data Framework',
      image: solarGridSadc,
      imageCaption: 'National Data Infrastructure & Cross-Border Sovereign Compute',
      tier: 'fieldable-2026',
      impact: [
        '100% on-soil data residency ensuring zero cross-border telemetry exposure.',
        'Automated cross-examination of shipping manifests against national tariff schedules.',
        '5-tier cryptographic approval gates preventing unauthorized administrative actions.'
      ]
    }
  };

  const caseStudies = [
    {
      sector: 'COMMERCIAL BANKING',
      client: 'Regional Tier-1 Bank (Southern & Eastern Africa)',
      problem: 'Manual trade finance reconciliation took 72 hours per letter of credit, creating massive merchant bottlenecks and foreign currency exposure.',
      intervention: 'Engineered a 4-agent sovereign pipeline (Ingest, Verification, Sanction Sweep, Swift Dispatch) with verified Human-in-the-Loop approval gates.',
      outcome: 'Reduced letter of credit issuance time from 72 hours to 14 minutes with 100% compliance audit match.'
    },
    {
      sector: 'NATIONAL REVENUE AUTHORITY',
      client: 'Sovereign Taxation & Customs Service',
      problem: 'Cross-border cargo manifest discrepancies resulted in millions in uncollected tariffs and multi-day border queues.',
      intervention: 'Deployed a multimodal computer vision and manifest cross-examination system running local edge models at border control points.',
      outcome: 'Recovered $14.2M in previously missed duty within 90 days; border clearance throughput increased by 400%.'
    },
    {
      sector: 'COMMODITY LOGISTICS',
      client: 'Export Mineral Logistics Fleet (Central & Southern Africa)',
      problem: 'Fragmented warehouse receipts, volatile corridor delays, and disjointed transport fleets caused massive demurrage penalties at regional ports.',
      intervention: 'Constructed an autonomous logistics orchestration pipeline with predictive border wait times and automated clearing manifests.',
      outcome: 'Corridor transit times reduced by 3.8 days; fleet fuel consumption decreased by 18% across 400+ transport units.'
    }
  ];

  const whitepapers = [
    {
      tome: 'TOME I',
      greekNumeral: 'Α // 01',
      tag: 'EXECUTIVE DISPATCH',
      title: 'The AI-Native Enterprise: Collapsing Strategy into Real-Time Execution',
      epigraph: 'Guiding enterprise navigation past the shoals of static consulting slide decks into dynamic computable topologies.',
      desc: 'Why conventional management consulting slide decks fail to deliver, and how closed-loop cognitive topologies bridge boardroom intent with real-time operational delivery.',
      author: 'LightSpeed Advisory Practice',
      readTime: '12 min read',
      downloads: '1,420 Executive Downloads',
      focus: 'Fiduciary Strategy & Topology'
    },
    {
      tome: 'TOME II',
      greekNumeral: 'Β // 02',
      tag: 'SOVEREIGN INTELLIGENCE',
      title: 'Sovereign Data Fabrics & Regional Compliance in the SADC Corridor',
      epigraph: 'Illuminating on-soil air-gapped compute architectures that withstand regulatory and data residency storms.',
      desc: 'Architecting air-gapped, on-soil inference clusters that comply strictly with national banking acts and SADC regional data residency mandates without sacrificing LLM reasoning capabilities.',
      author: 'Systems & Infrastructure Group',
      readTime: '15 min read',
      downloads: '980 Executive Downloads',
      focus: 'On-Premises Sovereignty'
    },
    {
      tome: 'TOME III',
      greekNumeral: 'Γ // 03',
      tag: 'SYSTEMS ENGINEERING',
      title: 'Deterministic Fiduciary Controls in Multi-Agent Swarms',
      epigraph: 'Mathematical bounds and cryptographic human-in-the-loop gates preventing agentic drift and hallucination.',
      desc: 'A mathematical and architectural specification for bounding autonomous AI agents to canonical tools, rate limits, and cryptographic human-in-the-loop approval gates.',
      author: 'AI Engineering Division',
      readTime: '18 min read',
      downloads: '2,150 Technical Downloads',
      focus: 'Agentic DAG Verification'
    },
    {
      tome: 'TOME IV',
      greekNumeral: 'Δ // 04',
      tag: 'REGULATORY TREATISE',
      title: 'The Alexandria Protocol: Air-Gapped High-Assurance Compute for Central Banks',
      epigraph: 'Deterministic settlement rails and anti-money laundering verification under sovereign jurisdictional bounds.',
      desc: 'Formulating provable cryptographic audit trails for automated foreign currency issuance, letters of credit, and cross-border customs declarations.',
      author: 'Sovereign Regulatory Institute',
      readTime: '20 min read',
      downloads: '1,840 Central Bank Downloads',
      focus: 'Monetary & Fiduciary Proofs'
    }
  ];

  return (
    <div className={`relative z-10 w-full transition-colors duration-300 ${
      isLight ? 'text-slate-700 selection:bg-orange-100 selection:text-slate-900' : 'text-zinc-300 selection:bg-white/20 selection:text-white'
    }`}>

      {/* SECTION 01: HERO — STRATEGY TO INTELLIGENT EXECUTION */}
      <section id="hero" className="relative min-h-[92vh] flex flex-col justify-center pt-28 pb-16 px-4 sm:px-8 max-w-7xl mx-auto w-full">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10 w-full">
          
          {/* Left Column: Core Positioning Statement & Vision */}
          <div className="lg:col-span-7 xl:col-span-7 space-y-6 text-left">
            
            {/* Eyebrow Badge & Canonical Tagline */}
            <div className={`inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full border text-[11px] font-mono tracking-widest transition-all shadow-xs ${
              isLight 
                ? 'bg-white border-slate-300 text-slate-900 shadow-orange-500/5' 
                : 'bg-zinc-900/90 border-orange-500/40 text-zinc-300 shadow-black/40'
            }`}>
              <span className="w-2 h-2 rounded-full bg-orange-500 shadow-sm shadow-orange-500/80 animate-pulse" />
              <span className="font-bold text-orange-500">ASPIRE. ACT. ACHIEVE.</span>
              <span className="text-zinc-500">•</span>
              <span>MALAWI-ROOTED • SADC-FOCUSED</span>
            </div>

            {/* Main Headline: Canonical Positioning */}
            <h1 className={`text-4xl sm:text-6xl md:text-7xl font-black tracking-tight font-display leading-[1.04] ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              THE AI-NATIVE <br />
              <span className={isLight 
                ? 'text-transparent bg-clip-text bg-gradient-to-r from-orange-600 via-amber-600 to-slate-900'
                : 'text-transparent bg-clip-text bg-gradient-to-r from-orange-400 via-amber-400 to-amber-200'
              }>
                COMPANY BUILDER
              </span> <br />
              FOR SOUTHERN AFRICA.
            </h1>

            {/* Divider Accent Line */}
            <div className="flex items-center gap-2">
              <div className={`w-16 h-[2px] ${isLight ? 'bg-orange-500/80' : 'bg-orange-500'}`} />
              <div className="w-1.5 h-1.5 rounded-xs bg-orange-400 shadow-sm shadow-orange-400" />
            </div>

            {/* Explicit Regional Proposition Statement with Honesty Anchor */}
            <div className="space-y-3">
              <p className={`text-justify text-justify max-w-2xl text-base sm:text-lg font-bold leading-relaxed ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                Architected and piloted in Malawi; architected for the SADC region.
              </p>
              <p className={`text-justify text-justify max-w-2xl text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'
              }`}>
                LightSpeed Holdings is the SADC region's agentic-AI builder — where enterprise, government, and donor partners don't just buy AI, they co-architect governed AI systems that run on their soil, their sovereign data, and their rules.
              </p>
            </div>

            {/* Honesty Ladder Confidence Strip */}
            <div className="flex flex-wrap items-center gap-2 pt-1 max-w-2xl">
              <StatusBadge tier="proven-in-house" size="sm" />
              <StatusBadge tier="pilot" size="sm" />
              <StatusBadge tier="fieldable-2026" size="sm" />
              <StatusBadge tier="in-development" size="sm" />
            </div>

            {/* 30-60 Second Visually Understandable Regional Advantage Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 max-w-2xl">
              <motion.div 
                initial={{ opacity: 0, y: 14 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-20px' }}
                transition={{ duration: 0.4, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
                className={`p-3.5 rounded-2xl border transition-all ${
                  isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
                }`}
              >
                <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-orange-500 mb-1 font-mono">
                  <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                  Local Fluency
                </div>
                <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  Deep operational mastery of Malawi’s institutions, business realities, infrastructure, and talent environment.
                </p>
              </motion.div>

              <motion.div 
                initial={{ opacity: 0, y: 14 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-20px' }}
                transition={{ duration: 0.4, delay: 0.12, ease: [0.16, 1, 0.3, 1] }}
                className={`p-3.5 rounded-2xl border transition-all ${
                  isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
                }`}
              >
                <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-orange-500 mb-1 font-mono">
                  <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                  Regional SADC
                </div>
                <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  Solutions architected for SADC corridor dynamics, trade integration, and national regulatory nuances.
                </p>
              </motion.div>

              <motion.div 
                initial={{ opacity: 0, y: 14 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-20px' }}
                transition={{ duration: 0.4, delay: 0.19, ease: [0.16, 1, 0.3, 1] }}
                className={`p-3.5 rounded-2xl border transition-all ${
                  isLight ? 'bg-white border-slate-300 shadow-xs' : 'bg-zinc-900/80 border-slate-800'
                }`}
              >
                <div className="flex items-center gap-1.5 text-xs font-bold tracking-wide text-orange-500 mb-1 font-mono">
                  <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                  Global Standards
                </div>
                <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                  Engineering, security, air-gapped governance, and design quality standing alongside top international firms.
                </p>
              </motion.div>
            </div>

            {/* Primary Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <button
                onClick={() => onRequestBriefing('Discovery Call — Sovereign AI Transformation')}
                className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-full font-bold text-xs tracking-widest bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/30 transition-all cursor-pointer"
              >
                <div className="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center transition-transform group-hover:translate-x-0.5">
                  <ArrowRight className="w-3 h-3" />
                </div>
                <span>Book a Discovery Call</span>
              </button>

              <a
                href="#method"
                className={`px-6 py-3.5 rounded-full font-bold text-xs tracking-widest border transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                  isLight 
                    ? 'bg-slate-900 hover:bg-slate-800 text-white border-slate-900' 
                    : 'bg-zinc-900 hover:bg-zinc-800 text-white border-white/20'
                }`}
              >
                <span>Explore the Method</span>
              </a>

              <a
                href="#diagnostic"
                className={`px-5 py-3.5 rounded-full font-bold text-xs tracking-widest border backdrop-blur-xl transition-all shadow-xs flex items-center gap-2 cursor-pointer ${
                  isLight 
                    ? 'bg-white hover:bg-slate-50 text-slate-900 border-slate-300 hover:border-orange-500' 
                    : 'bg-zinc-900/80 hover:bg-zinc-800 text-zinc-300 hover:text-white border-white/15'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5 text-orange-500" />
                <span>AI Diagnostic</span>
              </a>
            </div>

            {/* 30-Second Clarity Metric Strip */}
            <div className={`pt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t max-w-2xl ${
              isLight ? 'border-slate-200' : 'border-white/15'
            }`}>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Formulation Cycle</span>
                <span className="text-sm font-bold font-mono text-orange-500">9 Months → Real-Time</span>
              </div>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Settlement Speed</span>
                <span className="text-sm font-bold font-mono text-emerald-500">14 Min Trade Rails</span>
              </div>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Recovered Duties</span>
                <span className={`text-sm font-bold font-mono ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>$14.2M in Q1</span>
              </div>
              <div>
                <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-[#2D3748]' : 'text-[#2D3748]'}`}>Governance</span>
                <span className={`text-sm font-bold font-mono ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>100% Auditable</span>
              </div>
            </div>

          </div>

          {/* Right Column: Audio/Hardware-Grade 4-Pillars Architectural Chassis Card */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.96, y: 20 }}
            whileInView={{ opacity: 1, scale: 1, y: 0 }}
            viewport={{ once: true, margin: '-20px' }}
            transition={{ duration: 0.5, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="lg:col-span-5 xl:col-span-5 flex justify-end"
          >
            <div className={`p-6 sm:p-7 rounded-3xl max-w-md w-full transition-all duration-300 relative overflow-hidden ${
              isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
            }`}>
              {/* Hardware Hex Corner Fasteners */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              {/* Chassis Header Strip with Micro Acoustic Vent */}
              <div className={`flex items-center justify-between pb-3.5 border-b ${isLight ? 'border-black/10' : 'border-white/10'}`}>
                <div className="flex items-center gap-2 pl-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)]" />
                  <span className={`font-mono text-xs font-bold tracking-wider ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                    OPERATING TOPOLOGY
                  </span>
                </div>
                <div className="flex items-center gap-2.5 pr-2">
                  <AcousticVentGrille variant="strip" isLight={isLight} />
                  <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20 font-bold">
                    LIVE CORE
                  </span>
                </div>
              </div>

              {/* The 4 Connected Pillars (Tactile Hardware Stepped Array) */}
              <div className="space-y-2 pt-4">
                {[
                  { num: '01', title: 'Strategy', desc: 'Operating model redesign & capital allocation', tag: 'Executive', idx: 0 },
                  { num: '02', title: 'Intelligence', desc: 'Private data fabrics & semantic synthesis', tag: 'Sovereign', idx: 1 },
                  { num: '03', title: 'AI-Native Systems', desc: 'Multi-agent orchestration & deterministic DAGs', tag: 'Autonomous', idx: 2 },
                  { num: '04', title: 'Execution', desc: 'Legacy core integration & instant settlement', tag: 'Production', idx: 3 }
                ].map((p, pIdx) => (
                  <motion.button 
                    key={p.num}
                    initial={{ opacity: 0, x: -8 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.35, delay: 0.15 + pIdx * 0.06, ease: [0.16, 1, 0.3, 1] }}
                    onClick={() => {
                      setActivePillar(p.idx);
                      const el = document.getElementById('capabilities');
                      if (el) el.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className={`w-full text-left p-3 rounded-2xl transition-all cursor-pointer group ${
                      activePillar === p.idx
                        ? isLight ? 'tactile-btn-active-light border-orange-500/50' : 'tactile-btn-active-dark border-orange-500/50'
                        : isLight 
                          ? 'tactile-concave-btn-light' 
                          : 'tactile-concave-btn-dark'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs mb-1">
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full transition-all ${
                          activePillar === p.idx ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="font-mono font-bold text-orange-500">{p.num}</span>
                        <span className={`font-bold font-display group-hover:text-orange-500 transition-colors ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{p.title}</span>
                      </div>
                      <span className={`text-[10px] font-mono font-semibold ${activePillar === p.idx ? 'text-orange-500' : 'text-[#2D3748]'}`}>{p.tag}</span>
                    </div>
                    <p className="text-justify text-justify text-xs leading-snug pl-6 text-[#2D3748] font-medium">
                      {p.desc}
                    </p>
                  </motion.button>
                ))}
              </div>

              {/* Card Footer */}
              <div className={`pt-4 mt-3 border-t flex items-center justify-between text-xs px-2 ${isLight ? 'border-black/10' : 'border-white/10'}`}>
                <span className="font-mono text-[10px] font-semibold text-[#2D3748]">SADC & International</span>
                <button
                  onClick={() => onRequestBriefing()}
                  className="font-mono text-[11px] font-bold text-orange-500 hover:text-orange-400 flex items-center gap-1 cursor-pointer"
                >
                  <span>Partner Briefing</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>

            </div>
          </motion.div>

        </div>
      </section>

      {/* SECTION 01B: THE AFRICAN LEAPFROG & SADC SOVEREIGN OPPORTUNITY */}
      <section className={`py-12 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10 border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <motion.div 
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-40px' }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className={`rounded-3xl p-6 sm:p-10 border relative overflow-hidden ${
            isLight ? 'bg-gradient-to-br from-white via-slate-50 to-orange-50/30 border-slate-300 shadow-xl' : 'bg-gradient-to-br from-zinc-950 via-zinc-900 to-black border-white/15 shadow-2xl'
          }`}
        >
          {/* Subtle Grid & Fasteners */}
          <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
          <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left: Cinematic Visual Console */}
            <div className="lg:col-span-7 relative group">
              <div className={`relative rounded-2xl overflow-hidden border shadow-2xl ${
                isLight ? 'border-slate-300' : 'border-white/20'
              }`}>
                <img 
                  src={heroSadcAi} 
                  alt="Modern SADC Corporate AI Command Center" 
                  referrerPolicy="no-referrer"
                  className="w-full h-72 sm:h-96 object-cover object-center group-hover:scale-102 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent pointer-events-none" />

                {/* Top Status Bar */}
                <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
                  <div className="flex items-center gap-2 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/20">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                    <span className="font-mono text-[10px] text-white font-bold tracking-wider">
                      LILONGWE // SADC REGIONAL COMMAND
                    </span>
                  </div>
                  <div className="bg-orange-500/90 text-white font-mono text-[10px] px-2.5 py-1 rounded-full font-bold shadow-md">
                    SOVEREIGN CORE
                  </div>
                </div>

                {/* Bottom Overlay Telemetry Strip */}
                <div className="absolute bottom-3 left-3 right-3 p-3.5 rounded-xl bg-black/75 backdrop-blur-md border border-white/15 text-white space-y-1.5 pointer-events-none">
                  <div className="flex items-center justify-between text-[11px] font-mono">
                    <span className="text-orange-400 font-bold">SOVEREIGN AI FABRIC</span>
                    <span className="text-emerald-400 font-semibold">100% ON-SOIL COMPLIANCE</span>
                  </div>
                  <p className="text-[11px] text-zinc-300 leading-snug font-sans">
                    Air-gapped telemetry deployed across Southern African corridors, ensuring sovereign data residency under national banking acts.
                  </p>
                </div>
              </div>
            </div>

            {/* Right: Narrative Story & The Leapfrog Thesis */}
            <div className="lg:col-span-5 space-y-5">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[11px] tracking-widest font-bold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>THE AFRICAN LEAPFROG THESIS</span>
              </div>

              <h2 className={`text-2xl sm:text-4xl font-black tracking-tight font-display leading-tight ${
                isLight ? 'text-slate-900' : 'text-white'
              }`}>
                From Malawi to SADC: <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-500">
                  Leapfrogging Legacy IT to Autonomous AI
                </span>
              </h2>

              <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${
                isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
              }`}>
                Just as Southern Africa bypassed landline telephony for mobile networks and traditional branch banking for mobile money, the region is uniquely unencumbered by decades of bloated legacy software.
              </p>

              <div className="space-y-3 pt-1">
                {[
                  {
                    title: 'Direct to Agentic Automation',
                    desc: 'Deploying autonomous agent fleets directly on private data fabrics without decades of ERP re-platforming.',
                    highlight: 'Zero Legacy Debt'
                  },
                  {
                    title: 'On-Soil Data Sovereignty',
                    desc: 'Compute and intelligence reside within national borders—protecting sensitive financial and trade telemetry.',
                    highlight: 'SADC Law Compliant'
                  },
                  {
                    title: 'Fiduciary Mathematical Certainty',
                    desc: 'Replacing speculative consulting slide decks with deterministic, auditable multi-agent execution.',
                    highlight: '100% Verifiable'
                  }
                ].map((item, i) => (
                  <div 
                    key={i}
                    className={`p-3 rounded-2xl border flex items-start gap-3 ${
                      isLight ? 'bg-white border-slate-200' : 'bg-white/[0.04] border-white/10'
                    }`}
                  >
                    <div className="w-5 h-5 rounded-full bg-orange-500/20 text-orange-500 flex items-center justify-center shrink-0 mt-0.5 font-mono text-[10px] font-bold">
                      0{i + 1}
                    </div>
                    <div className="space-y-0.5">
                      <div className="flex items-center justify-between gap-2">
                        <span className={`text-xs font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                          {item.title}
                        </span>
                        <span className="text-[10px] font-mono text-orange-500 font-bold px-1.5 py-0.2 bg-orange-500/10 rounded">
                          {item.highlight}
                        </span>
                      </div>
                      <p className={`text-justify text-justify text-[11px] leading-snug ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                        {item.desc}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="pt-2">
                <button
                  onClick={() => onRequestBriefing('SADC Leapfrog Sovereign AI Architecture')}
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-lg shadow-orange-500/25 transition-all cursor-pointer"
                >
                  <span>Request SADC Sovereign Architecture Briefing</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* SADC ECOSYSTEM DIALOGUE & STANDARDS ALIGNMENT INTERACTIVE CAROUSEL */}
      <EcosystemCarousel 
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* SOVEREIGN CONSTELLATION: INTERACTIVE TOPOLOGY & REGIONAL ARCS */}
      <section id="constellation">
        <SovereignConstellation 
          theme={theme}
          onRequestBriefing={onRequestBriefing}
        />
      </section>

      {/* METHOD: THE 144-AGENT SOVEREIGN COMPANY FRAMEWORK (H-A-O-M-T-G-V) */}
      <MethodFramework 
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* MASTER USE CASE CATALOG (OFFERS A–E, DUAL PRICING, SADC VERTICALS, FOW SCENARIOS, HONESTY BADGES) */}
      <UseCaseCatalogSection 
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* SADC AGENTIC AI GOVERNANCE FRAMEWORK (POLICY BRIEFING & EXECUTIVE SUBMISSION) */}
      <SadcGovernanceFramework 
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* NATIONAL AI STRATEGY & DIGITAL TRANSFORMATION COMMENTS (MALAWI DEPT OF E-GOVT / UNDP SUBMISSION) */}
      <NationalAiStrategySubmission 
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* SECTION 03: PRODUCTIZED & ENTERPRISE SERVICES */}
      <section id="services" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="max-w-3xl mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[11px] tracking-widest font-bold">
            <Network className="w-3.5 h-3.5" />
            <span>PRACTICAL PRODUCTIZED & ENTERPRISE OFFERINGS</span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Five Sovereign Offer Lines
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            LightSpeed does not deliver speculative slides or disconnected chatbots. We engineer a closed-loop institutional stack where brand identity, mobile vernacular channels, field telemetry, multi-agent hierarchies, and air-gapped governance unite on your soil.
          </p>
        </div>

        {/* 5 Core Offerings Tab Switcher */}
        <div className={`p-2 rounded-3xl mb-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5 ${
          isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
        }`}>
          {coreCapabilities.map((cap, idx) => (
            <motion.button
              key={cap.id}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-20px' }}
              transition={{ duration: 0.4, delay: idx * 0.05, ease: [0.16, 1, 0.3, 1] }}
              onClick={() => setActivePillar(idx)}
              className={`p-3.5 rounded-2xl text-left transition-all duration-200 cursor-pointer relative overflow-hidden group ${
                activePillar === idx
                  ? isLight 
                    ? 'tactile-btn-active-light text-slate-900 border-orange-500/50 shadow-md' 
                    : 'tactile-btn-active-dark text-white border-orange-500/50 shadow-lg'
                  : isLight 
                    ? 'tactile-btn-inactive-light text-slate-700' 
                    : 'tactile-btn-inactive-dark text-zinc-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-1.5">
                  <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    activePillar === idx ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                  }`} />
                  <span className={`text-[9px] font-mono tracking-widest font-bold px-1.5 py-0.5 rounded-md ${
                    activePillar === idx 
                      ? 'bg-orange-500/20 text-orange-500' 
                      : 'bg-black/5 text-[#2D3748]'
                  }`}>
                    {idx < 3 ? `OFFER ${String.fromCharCode(65 + idx)}` : `ENT 0${idx - 2}`}
                  </span>
                </div>
              </div>
              <span className="text-xs font-bold tracking-wide block font-display leading-tight">{cap.shortTitle}</span>
              <div className="mt-2">
                <StatusBadge tier={cap.tier} size="sm" />
              </div>
            </motion.button>
          ))}
        </div>

        {/* Active Core Offering Deep-Dive View */}
        {(() => {
          const active = coreCapabilities[activePillar];
          return (
            <motion.div 
              key={active.id}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
              className={`p-6 sm:p-10 rounded-3xl transition-all duration-300 relative overflow-hidden shadow-2xl ${
                isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
              }`}
            >
              {/* Hardware Hex Corner Screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              {/* Corner Badge with Honesty Tier */}
              <div className="absolute top-0 right-0 py-1.5 px-4 rounded-bl-2xl bg-orange-500 text-white text-[10px] font-mono font-bold tracking-wider shadow-md flex items-center gap-2">
                <span>{active.governance}</span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start pt-2">
                
                {/* Left Column: Core Description & Contracts */}
                <div className="lg:col-span-7 space-y-6">
                  <div>
                    <div className="flex flex-wrap items-center gap-2 mb-2">
                      <span className="text-xs font-mono font-bold tracking-wider text-orange-500 block">
                        {active.eyebrow}
                      </span>
                      <StatusBadge tier={active.tier} size="sm" />
                    </div>
                    <h3 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
                      isLight ? 'text-slate-900' : 'text-white'
                    }`}>
                      {active.title}
                    </h3>
                    <div className={`text-sm font-semibold mt-1 ${isLight ? 'text-slate-800' : 'text-orange-400'}`}>
                      {active.tagline}
                    </div>
                  </div>

                  <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
                    isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
                  }`}>
                    {active.desc}
                  </p>

                  {/* Inter-Offering Data Contracts Box (Recessed Hardware Well) */}
                  <div className={`p-4 rounded-2xl space-y-3 ${
                    isLight ? 'hardware-well-light' : 'hardware-well-dark'
                  }`}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <GitMerge className="w-4 h-4 text-orange-500" />
                        <span className={`text-xs font-mono font-bold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>
                          Structured Inter-Offering Contracts
                        </span>
                      </div>
                      <AcousticVentGrille variant="cluster" isLight={isLight} />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                      <div className={`p-3 rounded-xl border ${isLight ? 'bg-white/90 border-slate-300' : 'bg-zinc-950/80 border-white/10'}`}>
                        <span className={`text-[10px] font-mono font-bold block mb-1 ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                          Input Contract (Feeds In)
                        </span>
                        <p className={`text-justify text-justify font-medium leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                          {active.inputContract}
                        </p>
                      </div>

                      <div className={`p-3 rounded-xl border ${isLight ? 'bg-white/90 border-slate-300' : 'bg-zinc-950/80 border-white/10'}`}>
                        <span className={`text-[10px] font-mono font-bold block mb-1 text-emerald-500`}>
                          Output Contract (Generates)
                        </span>
                        <p className={`text-justify text-justify font-medium leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                          {active.outputContract}
                        </p>
                      </div>
                    </div>

                    {/* Upstream & Downstream Flow Lineage Grid */}
                    <div className={`pt-3 border-t grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs ${
                      isLight ? 'border-slate-200' : 'border-white/10'
                    }`}>
                      {/* Upstream Source Card */}
                      <div className={`p-3 rounded-xl border flex flex-col justify-between space-y-1.5 ${
                        isLight ? 'bg-orange-50/70 border-orange-200/80' : 'bg-orange-950/30 border-orange-500/20'
                      }`}>
                        <div className="flex items-center gap-1.5">
                          <span className="p-1 rounded-md bg-orange-500/15 text-orange-500">
                            <ArrowUpRight className="w-3.5 h-3.5" />
                          </span>
                          <span className="font-bold font-mono text-[10px] tracking-wider text-orange-500">
                            Upstream Source
                          </span>
                        </div>
                        <p className={`text-justify text-justify text-[11px] sm:text-xs leading-relaxed font-medium break-words ${
                          isLight ? 'text-slate-800' : 'text-zinc-300'
                        }`}>
                          {active.upstreamSource}
                        </p>
                      </div>

                      {/* Downstream Target Card */}
                      <div className={`p-3 rounded-xl border flex flex-col justify-between space-y-1.5 ${
                        isLight ? 'bg-emerald-50/70 border-emerald-200/80' : 'bg-emerald-950/30 border-emerald-500/20'
                      }`}>
                        <div className="flex items-center gap-1.5">
                          <span className="p-1 rounded-md bg-emerald-500/15 text-emerald-500">
                            <ArrowDownRight className="w-3.5 h-3.5" />
                          </span>
                          <span className="font-bold font-mono text-[10px] tracking-wider text-emerald-500">
                            Downstream Target
                          </span>
                        </div>
                        <p className={`text-justify text-justify text-[11px] sm:text-xs leading-relaxed font-medium break-words ${
                          isLight ? 'text-slate-800' : 'text-zinc-300'
                        }`}>
                          {active.downstreamTarget}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Deliverables List */}
                  <div>
                    <div className={`text-xs font-mono font-bold mb-3 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                      Production Deliverables & Specifications:
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                      {active.deliverables.map((item, dIdx) => (
                        <div 
                          key={dIdx} 
                          className={`flex items-center gap-2.5 p-3 rounded-xl border text-xs font-medium transition-colors ${
                            isLight ? 'bg-slate-50 border-slate-300 text-slate-800 hover:bg-slate-100' : 'border-white/15 bg-white/[0.04] text-zinc-300 hover:bg-white/[0.08]'
                          }`}
                        >
                          <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                          <span className="leading-snug">{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Right Column: Institutional Benchmarks & Engagement Model */}
                <div className="lg:col-span-5 space-y-5">
                  <div className={`p-6 rounded-2xl ${
                    isLight ? 'hardware-well-light' : 'hardware-well-dark'
                  }`}>
                    <span className={`text-xs font-mono block mb-1 font-bold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                      Target Technical Benchmark
                    </span>
                    <div className="text-xl sm:text-2xl font-black font-mono text-emerald-500">
                      {active.metrics}
                    </div>
                    <div className={`text-xs font-medium mt-2 leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      Calibrated for SADC infrastructure constraints, bandwidth optimization, and zero foreign telemetry leakage.
                    </div>
                  </div>

                  {/* Interconnected Ecosystem Nav */}
                  <div className={`p-5 rounded-2xl space-y-3 ${
                    isLight ? 'hardware-well-light' : 'hardware-well-dark'
                  }`}>
                    <div className="flex items-center justify-between text-xs font-mono font-bold">
                      <span className={isLight ? 'text-slate-900' : 'text-zinc-200'}>Offering Navigation</span>
                      <span className="text-orange-500">Line {activePillar + 1} of {coreCapabilities.length}</span>
                    </div>

                    <div className="grid grid-cols-5 gap-1.5">
                      {coreCapabilities.map((c, cIdx) => (
                        <button
                          key={c.id}
                          onClick={() => setActivePillar(cIdx)}
                          className={`h-2.5 rounded-full transition-all ${
                            activePillar === cIdx 
                              ? 'bg-orange-500 shadow-[0_0_6px_rgba(249,115,22,0.8)]' 
                              : isLight ? 'bg-slate-300 hover:bg-slate-400' : 'bg-zinc-800 hover:bg-zinc-700'
                          }`}
                          title={`Switch to: ${c.shortTitle}`}
                        />
                      ))}
                    </div>

                    <div className="flex items-center justify-between pt-2">
                      <button
                        onClick={() => setActivePillar((activePillar + coreCapabilities.length - 1) % coreCapabilities.length)}
                        className={`text-xs font-mono font-semibold hover:text-orange-500 cursor-pointer ${
                          isLight ? 'text-slate-600' : 'text-zinc-400'
                        }`}
                      >
                        ← Prev Line
                      </button>
                      <button
                        onClick={() => setActivePillar((activePillar + 1) % coreCapabilities.length)}
                        className="text-xs font-mono font-bold text-orange-500 hover:text-orange-400 cursor-pointer flex items-center gap-1"
                      >
                        <span>Next Line</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>

                  <div className="p-6 rounded-2xl bg-orange-500/10 border border-orange-500/30 space-y-3 relative overflow-hidden">
                    <div className="text-xs font-mono tracking-wider text-orange-500 font-bold flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5" />
                      <span>Commercial Engagement Protocol</span>
                    </div>
                    <div className={`text-sm font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                      2-Week Diagnostic → Co-Architected Pilot
                    </div>
                    <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      We embed directly with enterprise leadership and technical teams to audit latency, specify private cognitive topologies, and deliver verified production code with zero data leakage.
                    </p>
                    <button
                      onClick={() => onRequestBriefing(`Inquiry regarding ${active.title}: ${active.tagline}`)}
                      className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-wider flex items-center justify-center gap-2 cursor-pointer transition-all shadow-md shadow-orange-500/20 active:scale-98"
                    >
                      <span>Engage {active.shortTitle} Line</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

              </div>
            </motion.div>
          );
        })()}

        {/* INTERACTIVE CONTINUOUS CLOSED-LOOP & SYNERGY MATRIX */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-40px' }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className={`mt-12 p-8 sm:p-10 rounded-3xl border ${
            isLight ? 'bg-slate-50/80 border-slate-300' : 'bg-zinc-950/70 border-white/15'
          }`}
        >
          <div className="max-w-3xl mb-8 space-y-2">
            <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[10px] tracking-widest">
              <RefreshCw className="w-3 h-3" />
              <span>THE CLOSED-LOOP MULTIPLIER EFFECT</span>
            </div>
            <h3 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              How the Four Offerings Interconnect
            </h3>
            <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Deploying any single offering creates value, but connecting all four creates an insurmountable sovereign compounding advantage. Click any interface pair below to inspect the joint protocol:
            </p>
          </div>

          {/* Synergy Pair Selector Buttons */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
            {Object.entries(synergyPairs).map(([key, pair], sIdx) => (
              <motion.button
                key={key}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.35, delay: sIdx * 0.06, ease: [0.16, 1, 0.3, 1] }}
                onClick={() => setSelectedSynergy(key)}
                className={`p-3.5 rounded-xl border text-left transition-all cursor-pointer ${
                  selectedSynergy === key
                    ? 'bg-orange-500 text-white border-orange-400 shadow-md shadow-orange-500/20'
                    : isLight 
                      ? 'bg-white hover:bg-slate-100 text-slate-800 border-slate-300' 
                      : 'bg-zinc-900/80 hover:bg-zinc-900 text-zinc-300 border-white/15'
                }`}
              >
                <div className={`text-[10px] font-mono font-bold mb-1 ${
                  selectedSynergy === key ? 'text-orange-100' : 'text-orange-500'
                }`}>
                  {pair.title}
                </div>
                <div className="text-xs font-bold truncate">{pair.headline}</div>
              </motion.button>
            ))}
          </div>

          {/* Active Synergy Detail Card */}
          {(() => {
            const pair = synergyPairs[selectedSynergy];
            if (!pair) return null;
            return (
              <motion.div 
                key={selectedSynergy}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                className={`p-6 rounded-2xl border transition-all ${
                  isLight ? 'bg-white border-slate-300 shadow-sm' : 'bg-zinc-900/90 border-white/20'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-orange-500/20 mb-4">
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 rounded-lg bg-orange-500 text-white font-mono text-xs font-bold">
                      {pair.title}
                    </span>
                    <h4 className={`text-base font-bold font-display ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {pair.headline}
                    </h4>
                  </div>
                  <div className="flex items-center gap-2 text-xs font-mono font-semibold text-emerald-500">
                    <Activity className="w-3.5 h-3.5" />
                    <span>Real-time Integration Protocol</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
                  <div className="md:col-span-7 space-y-2">
                    <span className={`text-[11px] font-mono font-bold block ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                      Integration Mechanism & Technical Contract
                    </span>
                    <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-800 font-medium' : 'text-zinc-300'}`}>
                      {pair.mechanism}
                    </p>
                  </div>

                  <div className={`md:col-span-5 p-4 rounded-xl border ${
                    isLight ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950' : 'bg-emerald-950/20 border-emerald-500/30 text-emerald-200'
                  }`}>
                    <span className="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                      Compound Institutional Impact
                    </span>
                    <p className="text-justify text-justify text-xs font-bold leading-relaxed">
                      {pair.compoundImpact}
                    </p>
                  </div>
                </div>
              </motion.div>
            );
          })()}

          {/* Comparative Table: Point Solutions vs. Lightspeed Connected Suite */}
          <div className="mt-8 pt-8 border-t border-slate-200 dark:border-white/10">
            <div className="flex items-center justify-between mb-4">
              <span className={`text-xs font-mono font-bold tracking-wider ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                Architectural Contrast: Disconnected Point-Tools vs. Connected Sovereign Suite
              </span>
              <span className="text-[10px] font-mono text-orange-500 font-bold">
                Zero Cloud SaaS Leakage
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className={`border-b ${isLight ? 'border-slate-300 bg-slate-100/80 text-slate-800' : 'border-white/10 bg-zinc-900/50 text-zinc-300'}`}>
                    <th className="p-3 font-mono font-bold">Offering Layer</th>
                    <th className="p-3 font-mono font-bold text-rose-500">Fragmented Point Solution</th>
                    <th className="p-3 font-mono font-bold text-emerald-500">Lightspeed Connected Architecture</th>
                  </tr>
                </thead>
                <tbody className={`divide-y ${isLight ? 'divide-slate-200 text-slate-700' : 'divide-white/10 text-zinc-300'}`}>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">01. Strategy</td>
                    <td className="p-3">Static PowerPoint slide decks, 9-month review cycles, zero computable rules.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">Executable Policy-as-Code, dynamic token budgets, computable board models.</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">02. Intelligence</td>
                    <td className="p-3">Siloed data lakes, public LLM SaaS APIs risking trade secrets and residency.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">100% sovereign air-gapped knowledge graphs with cryptographic AST lineage.</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">03. Autonomous Systems</td>
                    <td className="p-3">Unbounded probabilistic chatbots prone to hallucinations and tool abuse.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">Deterministic OpenCode agent fleets bound to 7 canonical tools and strict DAGs.</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-bold font-mono text-orange-500">04. Execution & Governance</td>
                    <td className="p-3">Manual data re-entry, 72-hour paper settlement, post-facto audit trails.</td>
                    <td className="p-3 font-medium text-emerald-600 dark:text-emerald-400">Direct core API event rails, Human-in-the-Loop gates, immutable SHA-256 ledgers.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </motion.div>

      </section>

      {/* SECTION 04: THE SYSTEMIC PROBLEM — THE STRATEGY-EXECUTION CHASM */}
      <section id="problem" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
            THE STRATEGY-EXECUTION CHASM
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Why Enterprise Transformations Fail
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Institutions do not fail for lack of strategy. They fail because strategy is stranded in slide decks, data is trapped in silos, and execution requires months of bureaucratic handoffs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Failure Trap 01 */}
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-30px' }}
            transition={{ duration: 0.45, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
            className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
              isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
            }`}
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-mono font-black text-orange-500">01</span>
                <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-red-500/30 text-red-500 bg-red-500/10 font-bold">
                  THE SLIDE TRAP
                </span>
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Static Strategy Decks</h3>
              <p className="text-justify text-justify text-xs sm:text-sm leading-relaxed text-[#2D3748]">
                Conventional consultancies spend 6 months formulating 200-page slide decks. By the time the presentation is delivered, market conditions have shifted, and the strategy is already obsolete.
              </p>
            </div>
            <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[#2D3748]`}>
              <span>LATENCY: 6–9 MONTHS</span>
              <span className="text-red-500 font-bold">CODE SHIPPED: 0%</span>
            </div>
          </motion.div>

          {/* Failure Trap 02 */}
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-30px' }}
            transition={{ duration: 0.45, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
            className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
              isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
            }`}
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-mono font-black text-orange-500">02</span>
                <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-amber-500/30 text-amber-500 bg-amber-500/10 font-bold">
                  THE SILO TAX
                </span>
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Fragmented Knowledge Pools</h3>
              <p className="text-justify text-justify text-xs sm:text-sm leading-relaxed text-[#2D3748]">
                Critical business truth is locked within legacy mainframe ERPs, paper bills-of-lading, and siloed spreadsheets. Executives make multimillion-dollar decisions on information that is two weeks stale.
              </p>
            </div>
            <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[#2D3748]`}>
              <span>TRUTH CONVERGENCE: POOR</span>
              <span className="text-amber-500 font-bold">FIDUCIARY RISK: HIGH</span>
            </div>
          </motion.div>

          {/* Failure Trap 03 */}
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-30px' }}
            transition={{ duration: 0.45, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className={`p-8 rounded-3xl border transition-all flex flex-col justify-between ${
              isLight ? 'bg-white/95 border-slate-300 text-slate-900 shadow-lg' : 'bg-zinc-950/80 border-white/15 text-zinc-300 shadow-xl'
            }`}
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-mono font-black text-orange-500">03</span>
                <span className="text-[10px] font-mono tracking-widest px-2.5 py-0.5 rounded-full border border-amber-500/30 text-amber-500 bg-amber-500/10 font-bold">
                  THE TOY PLAYGROUND
                </span>
              </div>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Ungoverned Ad-Hoc AI</h3>
              <p className="text-justify text-justify text-xs sm:text-sm leading-relaxed text-[#2D3748]">
                Organizations subscribe to disjointed SaaS chatbots that generate text but have zero access to production ledgers, cannot invoke audited tools, and cannot assume fiduciary accountability.
              </p>
            </div>
            <div className={`pt-6 border-t text-xs font-mono flex justify-between font-semibold ${isLight ? 'border-slate-200' : 'border-white/10'} text-[#2D3748]`}>
              <span>BUSINESS IMPACT: 0%</span>
              <span className="text-orange-500 font-bold">COMPLIANCE: UNVERIFIED</span>
            </div>
          </motion.div>

        </div>
      </section>

      {/* SECTION 05: SECTOR EXPERTISE & REGIONAL AUTHORITY (Objective 1) */}
      <section id="authority" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div className="space-y-2 max-w-2xl">
            <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
              REGIONAL RELEVANCE & PROVEN AUTHORITY
            </span>
            <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Engineered for Regulated Scale
            </h2>
            <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Tested and deployed in demanding African and international environments—where connectivity, data sovereignty, and regulatory scrutiny cannot be compromised.
            </p>
          </div>

          <div className={`flex flex-wrap p-1.5 rounded-2xl gap-2 ${
            isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
          }`}>
            {Object.keys(industriesData).map((key) => {
              const indItem = industriesData[key];
              const isSelected = selectedIndustry === key;
              return (
                <button
                  key={key}
                  onClick={() => setSelectedIndustry(key)}
                  className={`px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wider transition-all duration-200 cursor-pointer flex items-center gap-2 ${
                    isSelected
                      ? isLight ? 'tactile-btn-active-light text-slate-900 border-orange-500/50' : 'tactile-btn-active-dark text-white border-orange-500/50'
                      : isLight 
                        ? 'tactile-btn-inactive-light text-slate-700' 
                        : 'tactile-btn-inactive-dark text-zinc-300'
                  }`}
                >
                  <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                  }`} />
                  <span>{indItem.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Selected Sector Deep-Dive Card with Realistic Visual */}
        {(() => {
          const ind = industriesData[selectedIndustry];
          return (
            <motion.div 
              key={selectedIndustry}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
              className={`p-6 sm:p-8 rounded-3xl border mb-12 relative overflow-hidden ${
                isLight ? 'bg-white/95 border-slate-300 shadow-xl text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-2xl text-zinc-300'
              }`}
            >
              {/* Corner Hardware Screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                {/* Sector Photorealistic Image */}
                <div className="lg:col-span-5 relative group">
                  <div className={`relative rounded-2xl overflow-hidden border shadow-xl ${
                    isLight ? 'border-slate-300' : 'border-white/20'
                  }`}>
                    <img 
                      src={ind.image} 
                      alt={ind.title}
                      referrerPolicy="no-referrer"
                      className="w-full h-64 sm:h-72 object-cover object-center group-hover:scale-103 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent pointer-events-none" />

                    {/* Image Top Badge */}
                    <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-full border border-white/20">
                      <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                      <span className="font-mono text-[9px] text-white font-bold tracking-wider">
                        SADC SOVEREIGN FIELD TELEMETRY
                      </span>
                    </div>

                    {/* Image Bottom Caption */}
                    <div className="absolute bottom-3 left-3 right-3 p-2.5 rounded-xl bg-black/75 backdrop-blur-md border border-white/15 text-white">
                      <p className="text-[10px] font-mono text-zinc-300">
                        {ind.imageCaption}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Sector Narrative & Impact */}
                <div className="lg:col-span-7 space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-orange-500 font-bold tracking-wider">
                      {ind.citation}
                    </span>
                    <span className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20 font-bold">
                      VERIFIED DEPLOYMENT
                    </span>
                  </div>

                  <h3 className={`text-2xl sm:text-3xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{ind.title}</h3>
                  <p className={`text-justify text-justify text-sm font-semibold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{ind.subtitle}</p>
                  <p className={`text-justify text-justify text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>{ind.description}</p>

                  <div className="space-y-2 pt-2">
                    <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                      Verified Production Impact:
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {ind.impact.map((imp, iIdx) => (
                        <div 
                          key={iIdx} 
                          className={`p-3 rounded-xl border text-xs flex items-start gap-2 font-medium ${
                            isLight ? 'bg-slate-50 border-slate-300 text-slate-800' : 'border-white/15 bg-white/[0.05] text-zinc-300'
                          }`}
                        >
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                          <span className="text-[11px] leading-tight">{imp}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })()}

        {/* Case Studies Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {caseStudies.map((cs, cIdx) => (
            <motion.div 
              key={cIdx} 
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-20px' }}
              transition={{ duration: 0.45, delay: cIdx * 0.08, ease: [0.16, 1, 0.3, 1] }}
              className={`p-6 rounded-3xl border flex flex-col justify-between space-y-4 ${
                isLight ? 'bg-slate-50 border-slate-300' : 'bg-zinc-900/70 border-white/15'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between text-[11px] font-mono">
                  <span className="text-orange-500 font-bold">{cs.sector}</span>
                  <span className={`font-semibold ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>PRODUCTION</span>
                </div>
                <div className={`text-sm font-bold ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{cs.client}</div>
                <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                  <strong className={`font-semibold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>Challenge:</strong> {cs.problem}
                </p>
                <p className={`text-justify text-justify text-xs leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                  <strong className={`font-semibold ${isLight ? 'text-slate-900' : 'text-zinc-200'}`}>LIGHTSPEED Solution:</strong> {cs.intervention}
                </p>
              </div>

              <div className="pt-3 border-t border-white/10 text-xs font-mono text-emerald-500 font-bold">
                Outcome: {cs.outcome}
              </div>
            </motion.div>
          ))}
        </div>

      </section>

      {/* SECTION: PROOF SHOWCASE (Pilots, Publications, Ecosystem) */}
      <ProofShowcase 
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* SECTION 06: INTERACTIVE AI TRANSFORMATION DIAGNOSTIC (Objective 4) */}
      <section id="diagnostic" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <TransformationDiagnostic 
          theme={theme}
          onRequestBriefing={onRequestBriefing}
        />
      </section>

      {/* SECTION 07: STANDARDIZED ARTIFACTS & DELIVERABLE TEMPLATES (With Hardware Interface Ports) */}
      <TemplatesArtifacts
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />

      {/* SECTION 08: PHAROS // THOUGHT LEADERSHIP (The Ancient Lighthouse of Alexandria on the Island of Pharos) */}
      <section id="publications" className={`py-28 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t relative overflow-hidden ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        {/* Subtle stone masonry background pattern */}
        <div className="absolute inset-0 pharos-stone-masonry pointer-events-none opacity-40" />

        {/* Pharos Header & Lighthouse Lore */}
        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-end mb-14">
          <div className="lg:col-span-8 space-y-4">
            <div className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border border-amber-500/40 bg-gradient-to-r from-amber-500/15 via-orange-500/10 to-transparent text-amber-500 font-mono text-[11px] tracking-widest shadow-sm">
              <span className="w-2 h-2 rounded-full bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,1)] animate-pulse" />
              <span>PHAROS // THE LIGHTHOUSE OF ALEXANDRIA</span>
            </div>

            <h2 className={`text-4xl sm:text-6xl font-black tracking-tight font-display leading-[1.05] ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              PHAROS <br />
              <span className={isLight 
                ? 'text-transparent bg-clip-text bg-gradient-to-r from-amber-600 via-orange-600 to-slate-900' 
                : 'text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-orange-400 to-amber-100'
              }>
                THOUGHT LEADERSHIP
              </span>
            </h2>

            <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed max-w-3xl ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Erected on the limestone bedrock of the island of Pharos in Alexandria, Egypt, the ancient Lighthouse stood as humanity's supreme beacon of guidance—projecting radiant light across treacherous maritime shoals. 
              In today's turbulent storm of AI hype, SaaS data leakages, and consulting slide paralysis, LIGHTSPEED's <strong className="text-orange-500 font-bold">PHAROS</strong> casts unyielding illumination: providing boards, central banks, and sovereign ministries with definitive mathematical, architectural, and fiduciary clarity.
            </p>
          </div>

          {/* Pharos Beacon Optical Station Telemetry Card */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: 16 }}
            whileInView={{ opacity: 1, scale: 1, y: 0 }}
            viewport={{ once: true, margin: '-20px' }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            className="lg:col-span-4"
          >
            <div className={`p-4 rounded-3xl relative overflow-hidden backdrop-blur-xl border ${
              isLight ? 'bg-white/90 border-slate-300 text-slate-800 shadow-xl' : 'bg-zinc-950/80 border-amber-500/30 text-zinc-300 shadow-2xl'
            }`}>
              {/* Pharos Beacon Image Frame */}
              <div className="relative rounded-2xl overflow-hidden mb-3 border border-amber-500/30">
                <img 
                  src={pharosBeaconLake} 
                  alt="Pharos Beacon on Lake Malawi" 
                  referrerPolicy="no-referrer"
                  className="w-full h-36 object-cover object-center"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent pointer-events-none" />
                <div className="pharos-beacon-beam" />
                <div className="absolute bottom-2 left-2.5 right-2.5 flex items-center justify-between text-[10px] font-mono text-amber-300">
                  <span className="font-bold">LAKE MALAWI // PHAROS STATION</span>
                  <span className="bg-amber-500/30 px-1.5 py-0.5 rounded border border-amber-500/50 text-amber-200">589nm EMISSION</span>
                </div>
              </div>

              <div className="relative z-10 space-y-2.5">
                <div className="flex items-center justify-between border-b border-amber-500/20 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,1)] animate-ping" />
                    <span className="font-mono text-xs font-bold tracking-wider text-amber-500">
                      OPTICAL BEACON TELEMETRY
                    </span>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">
                    RADIANT
                  </span>
                </div>

                <div className="space-y-1 text-[11px] font-mono">
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Station Lat/Lon:</span>
                    <span className="font-bold text-amber-400">13.9626° S, 33.7741° E (Lilongwe)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Optical Reach:</span>
                    <span className="font-bold text-emerald-400">SADC Regional Corridor</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[#2D3748]">Guiding Purpose:</span>
                    <span className={`font-bold ${isLight ? 'text-slate-800' : 'text-white'}`}>Sovereign Clarity</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* 4 Pharos Treatises / Tomes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10">
          {whitepapers.map((wp, wIdx) => (
            <motion.div 
              key={wIdx} 
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-40px' }}
              transition={{ duration: 0.45, delay: wIdx * 0.1, ease: [0.16, 1, 0.3, 1] }}
              className={`p-6 sm:p-7 rounded-3xl flex flex-col justify-between space-y-6 transition-all group relative overflow-hidden ${
                isLight 
                  ? 'hardware-chassis-light hover:border-amber-500 text-slate-900' 
                  : 'hardware-chassis-dark hover:border-amber-500/60 text-zinc-300'
              }`}
            >
              {/* Corner Hardware Fasteners */}
              <div className="absolute top-2.5 left-2.5 w-1.5 h-1.5 rounded-full hardware-screw" />
              <div className="absolute top-2.5 right-2.5 w-1.5 h-1.5 rounded-full hardware-screw" />

              {/* Decorative classical top gold accent rule */}
              <div className="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-transparent via-amber-500/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

              <div className="space-y-3.5 pt-1">
                {/* Tome Header & Greek Numeral */}
                <div className="flex items-center justify-between text-[11px] font-mono border-b border-black/10 dark:border-white/10 pb-2.5">
                  <span className="px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-500 border border-amber-500/30 font-bold">
                    {wp.tome}
                  </span>
                  <span className="font-semibold text-[#2D3748]">{wp.readTime}</span>
                </div>

                {/* Subtitle & Tag */}
                <div className="flex items-center justify-between text-[10px] font-mono">
                  <span className="text-orange-500 font-bold">{wp.tag}</span>
                  <span className="text-[#2D3748]">{wp.greekNumeral}</span>
                </div>

                {/* Title */}
                <h3 className={`text-base sm:text-lg font-bold tracking-tight leading-snug group-hover:text-amber-500 transition-colors ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  {wp.title}
                </h3>

                {/* Epigraph / Quote */}
                <blockquote className="text-xs italic border-l-2 pl-3 py-0.5 border-amber-400 text-[#2D3748]">
                  "{wp.epigraph}"
                </blockquote>

                {/* Detailed Description */}
                <p className="text-justify text-justify text-xs leading-relaxed text-[#2D3748]">
                  {wp.desc}
                </p>
              </div>

              {/* Treatise Footer */}
              <div className={`pt-4 border-t flex items-center justify-between text-xs ${
                isLight ? 'border-black/10' : 'border-white/10'
              }`}>
                <span className="text-[10px] font-mono font-medium text-[#2D3748]">
                  {wp.downloads}
                </span>
                <button
                  onClick={() => onRequestBriefing(`Request Pharos Treatise: ${wp.tome} - ${wp.title}`)}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-mono font-bold text-amber-500 hover:text-amber-400 cursor-pointer transition-all ${
                    isLight ? 'tactile-concave-btn-light' : 'tactile-concave-btn-dark'
                  }`}
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download Tome</span>
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* SECTION 09: COMMERCIAL CONVERSION & ENGAGEMENT MODELS (Objective 4) */}
      <section id="engagement" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <span className="text-xs font-mono font-bold tracking-widest text-orange-500">
            HOW WE ENGAGE
          </span>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Engagement Structures
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Structured engagement frameworks designed for institutional leadership, board accountability, and rapid time-to-value.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Model 01 */}
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.45, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
            className={`p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
              isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
            }`}
          >
            <div className="space-y-4">
              <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                PHASE 01 // 2 WEEKS
              </span>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Advisory Architecture Sprint</h3>
              <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                A rapid forensic audit of your organizational topology, regulatory constraints, and sovereign data availability. Deliverable is an executive blueprint with computable business rules and an ROI model.
              </p>
              <ul className={`space-y-2 text-xs font-medium pt-2 ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Cognitive Friction & Latency Audit</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Sovereign Data Residency Blueprint</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Board-Level Investment Case</span>
                </li>
              </ul>
            </div>

            <button
              onClick={() => onRequestBriefing('Advisory Architecture Sprint (2 Weeks)')}
              className="w-full py-3 rounded-full border border-orange-500/50 text-orange-500 hover:bg-orange-500 hover:text-white font-bold text-xs tracking-wider transition-colors cursor-pointer"
            >
              Initiate Architecture Sprint
            </button>
          </motion.div>

          {/* Model 02: Featured Co-Engineered Pilot */}
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.45, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
            className="p-8 rounded-3xl border-2 border-orange-500 bg-gradient-to-b from-orange-500/10 via-zinc-950 to-zinc-950 flex flex-col justify-between space-y-6 relative shadow-2xl shadow-orange-500/10"
          >
            <div className="absolute -top-3 left-8 px-3 py-1 rounded-full bg-orange-500 text-white font-mono text-[10px] font-bold tracking-widest">
              MOST COMMON COMMENCEMENT
            </div>

            <div className="space-y-4">
              <span className="text-xs font-mono text-orange-400 font-bold block">
                PHASE 02 // 90 DAYS
              </span>
              <h3 className="text-xl font-bold tracking-tight text-white">Co-Engineered Pilot</h3>
              <p className="text-justify text-justify text-xs sm:text-sm text-zinc-300 leading-relaxed font-normal">
                Co-deploying a live sovereign multi-agent pipeline alongside your internal engineers. Proving measurable business outcomes against real transaction volume before broad institutional rollout.
              </p>
              <ul className="space-y-2 text-xs text-zinc-200 font-medium pt-2">
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                  <span>Production Core API Integration</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                  <span>Human-in-the-Loop Sign-off Gates</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-400 shrink-0" />
                  <span>Verified ROI Ledgers & SLA Guarantee</span>
                </li>
              </ul>
            </div>

            <button
              onClick={() => onRequestBriefing('Co-Engineered Pilot (90 Days)')}
              className="w-full py-3.5 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest transition-all cursor-pointer shadow-md shadow-orange-500/25"
            >
              Request Pilot Consultation
            </button>
          </motion.div>

          {/* Model 03 */}
          <motion.div 
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.45, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className={`p-8 rounded-3xl border flex flex-col justify-between space-y-6 ${
              isLight ? 'bg-white/95 border-slate-300 shadow-md text-slate-900' : 'bg-zinc-950/80 border-white/15 shadow-xl text-zinc-300'
            }`}
          >
            <div className="space-y-4">
              <span className={`text-xs font-mono font-bold block ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                PHASE 03 // ENTERPRISE SCALE
              </span>
              <h3 className={`text-xl font-bold tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>Sovereign Enterprise Deployment</h3>
              <p className={`text-justify text-justify text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                Full-scale institutional transition to an AI-native operating model. Continuous agent fleets, on-premise air-gapped inference clusters, and embedded transformation partners.
              </p>
              <ul className={`space-y-2 text-xs font-medium pt-2 ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Autonomous Multi-Agent Fleet</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>Enterprise Sovereign Air-Gap Infra</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-orange-500 shrink-0" />
                  <span>24/7 Model Drift & Security Oversight</span>
                </li>
              </ul>
            </div>

            <button
              onClick={() => onRequestBriefing('Sovereign Enterprise Deployment')}
              className="w-full py-3 rounded-full border border-orange-500/50 text-orange-500 hover:bg-orange-500 hover:text-white font-bold text-xs tracking-wider transition-colors cursor-pointer"
            >
              Consult On Enterprise Scope
            </button>
          </motion.div>

        </div>
      </section>

      {/* SECTION 10: FREQUENTLY ASKED QUESTIONS */}
      <section id="faq" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[11px] tracking-widest font-bold">
            <HelpCircle className="w-3.5 h-3.5" />
            <span>EXECUTIVE CLARITY & ASSURANCE</span>
          </div>
          <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
            isLight ? 'text-slate-900' : 'text-white'
          }`}>
            Frequently Asked Questions
          </h2>
          <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
            isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
          }`}>
            Direct answers regarding LightSpeed's 4 Connected Core Offerings, sovereign data security, and the specific operational purpose of our provided templates and deliverables.
          </p>
        </div>

        {/* FAQ Controls: Category Filter Tabs & Live Search */}
        <div className="max-w-4xl mx-auto mb-10 space-y-4">
          
          {/* Live Search Bar with ARIA Labeling */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-orange-500 pointer-events-none" />
            <input
              type="text"
              role="searchbox"
              aria-label="Search Frequently Asked Questions regarding LightSpeed offerings and templates"
              placeholder="Search inquiries (e.g., core offerings, templates, OpenCode, HITL, data sovereignty)..."
              value={faqSearchQuery}
              onChange={(e) => {
                setFaqSearchQuery(e.target.value);
                setOpenFaqIndex(0); // Reset accordion expand on new search
              }}
              className={`w-full pl-11 pr-4 py-3.5 rounded-2xl border text-xs sm:text-sm font-medium outline-none focus:border-orange-500 transition-all ${
                isLight 
                  ? 'bg-white border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner focus:ring-2 focus:ring-orange-500/20' 
                  : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner focus:ring-2 focus:ring-orange-500/30'
              }`}
            />
            {faqSearchQuery && (
              <button
                type="button"
                onClick={() => setFaqSearchQuery('')}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-mono font-bold text-orange-500 hover:text-orange-400 cursor-pointer px-2 py-1 rounded-md bg-orange-500/10"
              >
                Clear
              </button>
            )}
          </div>

          {/* Category Filter Pills (Accessible Tab List) */}
          <div 
            role="tablist" 
            aria-label="Filter FAQ topics"
            className={`flex flex-wrap items-center gap-2 p-1.5 rounded-2xl ${
              isLight ? 'bg-slate-200/70' : 'bg-zinc-900/80 border border-white/10'
            }`}
          >
            {[
              { id: 'all', label: 'All Inquiries' },
              { id: 'offerings', label: 'Core Offerings' },
              { id: 'templates', label: 'Templates & Purpose' },
              { id: 'sovereignty', label: 'Sovereignty & Security' },
              { id: 'deployment', label: 'Deployment Process' }
            ].map((cat) => {
              const isActive = faqCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  type="button"
                  role="tab"
                  aria-selected={isActive}
                  onClick={() => {
                    setFaqCategory(cat.id);
                    setOpenFaqIndex(0);
                  }}
                  className={`px-3.5 py-2 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                    isActive
                      ? 'bg-orange-500 text-white shadow-md shadow-orange-500/20'
                      : isLight
                        ? 'text-slate-700 hover:text-slate-900 hover:bg-slate-300/60'
                        : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
                  }`}
                >
                  {cat.label}
                </button>
              );
            })}
          </div>

        </div>

        {/* FAQ Accordion List */}
        {(() => {
          const faqItems = [
            {
              id: 'faq-1',
              category: 'offerings',
              categoryLabel: 'Core Offerings',
              q: 'What are LightSpeed\'s 4 Connected Core Offerings, and how do they work together?',
              a: 'LightSpeed provides a closed-loop institutional operating stack comprising four connected offerings: (1) Strategy Formulation & Operating Models (computable Policy-as-Code and capital allocation), (2) Private Sovereign Intelligence (air-gapped knowledge graphs and zero-leakage RAG grounding), (3) Autonomous Systems & Orchestration (specialist AI agent fleets with deterministic DAG workflows), and (4) Fiduciary Control & Core Execution (cryptographic Human-in-the-Loop approval gates and legacy API connectors). Unlike isolated chatbots or static consulting decks, strategy directly compiles into agent execution, and real-time transaction telemetry streams back into board-level policy governance.',
              highlights: ['Policy-as-Code', 'Sovereign Knowledge Graphs', 'Deterministic Agent Fleets', 'HITL Fiduciary Gates']
            },
            {
              id: 'faq-2',
              category: 'templates',
              categoryLabel: 'Templates & Purpose',
              q: 'What is the specific purpose of the provided Templates & Artifacts in the platform?',
              a: 'The Templates & Artifacts section provides pre-engineered, board-approved structural blueprints and computable schemas that eliminate the typical 6–9 month strategy-to-execution gap. Clients use these templates as actionable starter kits for: (a) OpenCode-compatible agent YAML cards, (b) SADC regional customs EDI and trade finance compliance frameworks, (c) Fiduciary gatekeeper risk matrices, (d) Sovereign data residency rules, and (e) DAG workflow execution contracts. Each template contains production-ready JSON/YAML definitions that can be imported directly into OpenCode agent runtimes or local orchestration engines.',
              highlights: ['OpenCode-Compatible YAML', 'SADC Trade Compliance', 'Sovereign Residency Matrix', 'Production-Ready Schemas']
            },
            {
              id: 'faq-3',
              category: 'templates',
              categoryLabel: 'Templates & Purpose',
              q: 'How do LightSpeed\'s templates differ from static consulting decks or generic SaaS templates?',
              a: 'Traditional management consulting deliverables are static presentation slides with zero shipped code ("The Slide Trap"). Generic SaaS templates lack institutional governance and regulatory awareness. In contrast, LightSpeed\'s templates are executable engineering specs. They bundle statutory compliance rules (such as Basel IV, King IV, and WCO SAFE EDI standards) directly with machine-readable tool permissions, cryptographic HITL approval triggers, and audit logging parameters. They are ready to be parsed by AI agents and integrated into enterprise VPC environments immediately.',
              highlights: ['Executable Specs', '0% Slide Trap', 'Embedded Regulatory Standards', 'Machine-Readable Permissions']
            },
            {
              id: 'faq-4',
              category: 'sovereignty',
              categoryLabel: 'Sovereignty & Security',
              q: 'How does LightSpeed ensure data sovereignty and regulatory compliance across SADC corridors?',
              a: 'We engineer air-gapped, on-soil data fabrics and private LLM inference clusters aligned with national banking acts and SADC regional data residency mandates. Confidential enterprise data is indexed natively inside your secure VPC perimeter. Cross-border agent communications pass through deterministic policy-as-code filters that enforce sovereign boundaries before indexing or processing, eliminating unauthorized cross-border data exposure.',
              highlights: ['On-Soil Air-Gapped Compute', 'SADC Residency Compliance', 'In-Perimeter Knowledge Graphs', 'Zero-Leakage Policy Enclaves']
            },
            {
              id: 'faq-5',
              category: 'offerings',
              categoryLabel: 'Core Offerings',
              q: 'What role do Human-in-the-Loop (HITL) gates play in agent execution and fiduciary control?',
              a: 'HITL gates serve as cryptographic circuit breakers for autonomous agent swarms. While specialist agents handle automated data ingestion, multi-document synthesis, and draft calculations, any high-value transaction, capital disbursement, or regulatory filing must trigger an explicit HITL approval request. Human officers review verified source citations and issue a cryptographic sign-off before the action writes to core banking, customs EDI, or ERP mainframes. This eliminates hallucination risk and preserves clear fiduciary accountability.',
              highlights: ['Fiduciary Circuit Breakers', 'Cryptographic Sign-Off', 'Zero Unverified Writes', 'Immutable Audit Trails']
            },
            {
              id: 'faq-6',
              category: 'deployment',
              categoryLabel: 'Deployment Process',
              q: 'How does an organization transition from template selection to a live enterprise deployment?',
              a: 'LightSpeed follows a structured 3-phase transformation path: Phase 1 is a 2-Week Advisory Architecture Sprint where we audit cognitive latency and map template schemas to your enterprise topology. Phase 2 is a 90-Day Co-Engineered Pilot deploying live agent pipelines alongside your internal engineering team. Phase 3 scales into a full Sovereign Enterprise Deployment with 24/7 model drift oversight, continuous security monitoring, and automated policy updates.',
              highlights: ['2-Week Architecture Sprint', '90-Day Co-Engineered Pilot', 'Sovereign Enterprise Scale', '24/7 Model Drift Oversight']
            },
            {
              id: 'faq-7',
              category: 'deployment',
              categoryLabel: 'Deployment Process',
              q: 'How do LightSpeed templates integrate with OpenCode agent automation environments?',
              a: 'All agent templates and company topologies in LightSpeed are structured according to OpenCode standards. YAML templates map directly to OpenCode agent cards (.opencode/agents/*.md) with canonical tool permissions (read, edit, grep, list, bash, webfetch, task) and approval gate protocols. This allows developer and automation teams to ingest LightSpeed template definitions directly into CLI orchestrators like OpenCode or ai-company without re-architecting underlying schemas.',
              highlights: ['OpenCode Native Format', 'Canonical 7-Tool Vocabulary', 'Direct CLI Orchestration', 'Instant YAML Intake']
            },
            {
              id: 'faq-8',
              category: 'sovereignty',
              categoryLabel: 'Sovereignty & Security',
              q: 'How fast can LightSpeed connect with legacy core infrastructure (e.g. monolithic banking cores or customs EDIs)?',
              a: 'Through Offering 04 (Fiduciary Control & Core Execution), we deploy legacy core API modernization wrappers. These wrappers translate legacy protocols (COBOL, mainframes, SOAP, flat-file EDI) into reactive event streams and secure REST/gRPC endpoints without requiring high-risk core rewrites. This compresses systemic reconciliation latencies from 72 hours down to minutes.',
              highlights: ['Zero-Rewrite API Wrappers', 'Mainframe & COBOL Connectors', '72hr to 14min Compression', 'Reactive Event Streaming']
            }
          ];

          // Filter by category and search query
          const filtered = faqItems.filter(item => {
            const matchesCat = faqCategory === 'all' || item.category === faqCategory;
            const query = faqSearchQuery.toLowerCase().trim();
            const matchesSearch = !query || 
              item.q.toLowerCase().includes(query) || 
              item.a.toLowerCase().includes(query) ||
              item.categoryLabel.toLowerCase().includes(query) ||
              item.highlights.some(h => h.toLowerCase().includes(query));
            return matchesCat && matchesSearch;
          });

          if (filtered.length === 0) {
            return (
              <div className={`p-8 rounded-3xl text-center max-w-4xl mx-auto border ${
                isLight ? 'bg-white border-slate-300 text-slate-800' : 'bg-zinc-900 border-white/10 text-zinc-300'
              }`}>
                <HelpCircle className="w-8 h-8 text-orange-500 mx-auto mb-3 opacity-80" />
                <p className="text-sm font-bold mb-1">No matching inquiries found</p>
                <p className="text-xs text-[#2D3748] mb-4">Try adjusting your search terms or selecting a different category filter.</p>
                <button
                  onClick={() => { setFaqSearchQuery(''); setFaqCategory('all'); }}
                  className="px-4 py-2 rounded-xl bg-orange-500 text-white font-mono text-xs font-bold hover:bg-orange-600 transition-colors cursor-pointer"
                >
                  Reset FAQ Filters
                </button>
              </div>
            );
          }

          return (
            <div className="max-w-4xl mx-auto space-y-4" role="region" aria-live="polite">
              <div className="text-right text-[11px] font-mono font-bold text-[#2D3748] px-2 mb-2">
                Showing {filtered.length} of {faqItems.length} inquiries
              </div>

              {filtered.map((faq, idx) => {
                const isOpen = openFaqIndex === idx;
                const buttonId = `faq-btn-${faq.id}`;
                const panelId = `faq-panel-${faq.id}`;

                return (
                  <motion.div
                    key={faq.id}
                    initial={{ opacity: 0, y: 12 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: '-20px' }}
                    transition={{ duration: 0.35, delay: idx * 0.05, ease: [0.16, 1, 0.3, 1] }}
                    className={`rounded-2xl border transition-all overflow-hidden ${
                      isOpen
                        ? isLight
                          ? 'bg-white border-orange-500/60 shadow-lg ring-1 ring-orange-500/20'
                          : 'bg-zinc-950 border-orange-500/60 shadow-xl shadow-orange-500/5 ring-1 ring-orange-500/30'
                        : isLight
                          ? 'bg-white/90 border-slate-300 hover:border-slate-400 shadow-xs'
                          : 'bg-zinc-900/70 border-white/15 hover:border-white/25'
                    }`}
                  >
                    {/* Accordion Header Button */}
                    <button
                      id={buttonId}
                      type="button"
                      aria-expanded={isOpen}
                      aria-controls={panelId}
                      onClick={() => setOpenFaqIndex(isOpen ? null : idx)}
                      className={`w-full text-left p-5 sm:p-6 flex items-start justify-between gap-4 cursor-pointer focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:ring-offset-2 focus-visible:outline-none transition-colors ${
                        isOpen 
                          ? isLight ? 'bg-orange-50/40' : 'bg-orange-950/10' 
                          : ''
                      }`}
                    >
                      <div className="space-y-1.5 pr-2">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-mono font-bold tracking-wider px-2 py-0.5 rounded-md bg-orange-500/15 text-orange-500">
                            {faq.categoryLabel}
                          </span>
                        </div>
                        <h3 className={`text-base sm:text-lg font-bold tracking-tight leading-snug ${
                          isLight ? 'text-slate-900' : 'text-white'
                        }`}>
                          {faq.q}
                        </h3>
                      </div>

                      <div className={`p-2 rounded-xl shrink-0 transition-all ${
                        isOpen 
                          ? 'bg-orange-500 text-white shadow-md shadow-orange-500/30' 
                          : isLight 
                            ? 'bg-slate-200 text-slate-700' 
                            : 'bg-zinc-800 text-zinc-300'
                      }`}>
                        {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </div>
                    </button>

                    {/* Accordion Content Panel */}
                    <div
                      id={panelId}
                      role="region"
                      aria-labelledby={buttonId}
                      hidden={!isOpen}
                      className={`px-5 pb-6 sm:px-6 sm:pb-6 pt-1 border-t transition-all ${
                        isLight ? 'border-slate-200/80 text-slate-800' : 'border-white/10 text-zinc-200'
                      }`}
                    >
                      <p className="text-xs sm:text-sm leading-relaxed text-justify mb-4 font-normal">
                        {faq.a}
                      </p>

                      {/* Highlight Chips */}
                      {faq.highlights && faq.highlights.length > 0 && (
                        <div className="pt-2 border-t border-black/5 dark:border-white/10 flex flex-wrap items-center gap-1.5">
                          <span className="text-[10px] font-mono font-bold text-[#2D3748] mr-1">
                            KEY SPECIFICATIONS:
                          </span>
                          {faq.highlights.map((item, hIdx) => (
                            <span
                              key={hIdx}
                              className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${
                                isLight
                                  ? 'bg-slate-100 border-slate-300 text-slate-800'
                                  : 'bg-zinc-900 border-white/15 text-zinc-300'
                              }`}
                            >
                              ✓ {item}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                  </motion.div>
                );
              })}
            </div>
          );
        })()}

        {/* Bottom Contact CTA Box */}
        <div className={`mt-12 p-6 rounded-3xl max-w-4xl mx-auto text-center border flex flex-col sm:flex-row items-center justify-between gap-4 ${
          isLight ? 'bg-slate-100 border-slate-300 text-slate-900' : 'bg-zinc-900/90 border-white/15 text-white'
        }`}>
          <div className="text-left space-y-1">
            <h4 className="text-sm font-extrabold tracking-tight">Have a custom institutional question?</h4>
            <p className="text-xs text-[#2D3748]">Our partner engineering team conducts confidential advisory assessments.</p>
          </div>
          <button
            onClick={() => onRequestBriefing('Custom Institutional Inquiry')}
            className="px-5 py-2.5 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-mono text-xs font-bold tracking-wider transition-colors cursor-pointer shrink-0 shadow-md shadow-orange-500/20"
          >
            Request Executive Briefing →
          </button>
        </div>

      </section>

      {/* SECTION 11: CONTACT / EXECUTIVE BRIEFING INTAKE (Objective 4) */}
      <section id="contact" className={`py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t ${
        isLight ? 'border-slate-200/80' : 'border-zinc-800/80'
      }`}>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
          
          <div className="lg:col-span-5 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-orange-500/30 bg-orange-500/10 text-orange-500 font-mono text-[11px] tracking-widest font-bold">
              <span>COMMENCE TRANSFORMATION</span>
            </div>
            <h2 className={`text-3xl sm:text-5xl font-black tracking-tight font-display ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Request an Executive Briefing
            </h2>
            <p className={`text-justify text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Schedule a confidential 45-minute advisory diagnostic with our Managing Partners. We will assess your current operating latency and evaluate the feasibility of deploying sovereign AI architectures.
            </p>

            <div className={`space-y-4 pt-4 border-t ${isLight ? 'border-slate-200' : 'border-white/15'}`}>
              <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
                <span>Strict fiduciary non-disclosure agreement standard</span>
              </div>
              <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <Clock className="w-4 h-4 text-orange-500 shrink-0" />
                <span>Executive response within 12 business hours</span>
              </div>
              <div className={`flex items-center gap-3 text-xs font-medium ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
                <Globe2 className="w-4 h-4 text-amber-500 shrink-0" />
                <span>Offices in Southern Africa & International Advisory Network</span>
              </div>
            </div>
          </div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            className="lg:col-span-7"
          >
            <div className={`p-8 sm:p-10 rounded-3xl relative overflow-hidden shadow-2xl ${
              isLight ? 'hardware-chassis-light text-slate-900' : 'hardware-chassis-dark text-zinc-300'
            }`}>
              {/* Hardware Screws */}
              <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" />
              <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" />

              {/* Console Header Bar */}
              <div className="flex items-center justify-between pb-3.5 mb-6 border-b border-black/10 dark:border-white/10 px-1">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.9)]" />
                  <span className="font-mono text-xs font-bold tracking-wider">
                    BRIEFING TRANSMISSION CONSOLE
                  </span>
                </div>
                <AcousticVentGrille variant="strip" isLight={isLight} />
              </div>

              {contactSubmitted ? (
                <div className="py-12 text-center space-y-4">
                  <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-500 border border-emerald-500/40 flex items-center justify-center mx-auto shadow-[0_0_15px_rgba(16,185,129,0.3)]">
                    <CheckCircle2 className="w-8 h-8" />
                  </div>
                  <h3 className={`text-2xl font-black tracking-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                    Briefing Request Received
                  </h3>
                  <p className={`text-justify text-justify text-sm max-w-md mx-auto leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                    Thank you. A Senior Partner will review your institutional profile and contact you directly within 12 business hours.
                  </p>
                  <button
                    onClick={() => setContactSubmitted(false)}
                    className="px-6 py-2.5 rounded-xl bg-orange-500 text-white font-bold text-xs tracking-wider cursor-pointer shadow-md hover:bg-orange-600 transition-all"
                  >
                    Submit Another Inquiry
                  </button>
                </div>
              ) : (
                <form onSubmit={handleContactSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Executive Name *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Dr. K. Mlangeni"
                        value={contactFormData.name}
                        onChange={(e) => setContactFormData({ ...contactFormData, name: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Executive Title *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Chief Executive Officer"
                        value={contactFormData.title}
                        onChange={(e) => setContactFormData({ ...contactFormData, title: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Institution / Entity *
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="e.g. Reserve Bank / Standard Bank"
                        value={contactFormData.organization}
                        onChange={(e) => setContactFormData({ ...contactFormData, organization: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                    <div>
                      <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                        Official Email *
                      </label>
                      <input
                        type="email"
                        required
                        placeholder="executive@institution.com"
                        value={contactFormData.email}
                        onChange={(e) => setContactFormData({ ...contactFormData, email: e.target.value })}
                        className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                          isLight 
                            ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                            : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                        }`}
                      />
                    </div>
                  </div>

                  <div>
                    <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      Target Engagement Model
                    </label>
                    <select
                      value={contactFormData.scope}
                      onChange={(e) => setContactFormData({ ...contactFormData, scope: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors font-medium ${
                        isLight 
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 shadow-inner' 
                          : 'bg-zinc-900 border-white/20 text-white shadow-inner'
                      }`}
                    >
                      <option value="Advisory Architecture Sprint (2 Weeks)">Advisory Architecture Sprint (2 Weeks)</option>
                      <option value="Co-Engineered Pilot (90 Days)">Co-Engineered Pilot (90 Days)</option>
                      <option value="Sovereign Enterprise Deployment">Sovereign Enterprise Deployment</option>
                      <option value="Executive Boardroom Briefing">Executive Boardroom Briefing</option>
                    </select>
                  </div>

                  <div>
                    <label className={`block text-[11px] font-mono tracking-wider mb-1 font-bold ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
                      Strategic Objectives & Context
                    </label>
                    <textarea
                      rows={3}
                      placeholder="Describe your current strategic bottlenecks, regulatory constraints, or legacy IT dependencies..."
                      value={contactFormData.objective}
                      onChange={(e) => setContactFormData({ ...contactFormData, objective: e.target.value })}
                      className={`w-full px-3.5 py-2.5 rounded-xl border text-xs outline-none focus:border-orange-500 transition-colors resize-none font-medium ${
                        isLight 
                          ? 'bg-slate-100/90 border-slate-300 text-slate-900 placeholder:text-[#2D3748] shadow-inner' 
                          : 'bg-zinc-900/90 border-white/20 text-white placeholder:text-[#2D3748] shadow-inner'
                      }`}
                    />
                  </div>

                  <div className="pt-2">
                    <button
                      type="submit"
                      className="w-full py-3.5 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs tracking-widest transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-orange-500/25 active:scale-98"
                    >
                      <span>Submit Confidential Executive Request</span>
                      <Send className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </form>
              )}
            </div>
          </motion.div>

        </div>
      </section>

      {/* FOOTER: Minimalist Editorial Signoff */}
      <footer className={`py-12 px-4 sm:px-8 max-w-7xl mx-auto w-full border-t flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono ${
        isLight ? 'border-slate-200 text-slate-700' : 'border-white/15 text-zinc-300'
      }`}>
        <div>
          © {new Date().getFullYear()} LIGHTSPEED HOLDINGS LIMITED. All rights reserved. Sovereign AI Transformation.
        </div>
        <div className={`flex items-center gap-4 ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
          <a href="#operating-model" className="hover:text-orange-500 font-medium">Model</a>
          <a href="#capabilities" className="hover:text-orange-500 font-medium">Capabilities</a>
          <a href="#diagnostic" className="hover:text-orange-500 font-medium">Diagnostic</a>
          <a href="#templates" className="hover:text-orange-500 font-medium">Templates</a>
          <a href="#publications" className="hover:text-orange-500 font-medium">Publications</a>
          <a href="#faq" className="hover:text-orange-500 font-medium">FAQ</a>
          <a href="#contact" className="hover:text-orange-500 font-medium">Contact</a>
        </div>
      </footer>

    </div>
  );
};
