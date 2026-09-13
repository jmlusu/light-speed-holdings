import React, { useState } from 'react';
import { 
  Landmark, 
  Globe2, 
  Building2, 
  Sparkles, 
  Lock, 
  Brain, 
  Layers, 
  Handshake, 
  ShoppingBag,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Zap,
  ShieldAlert
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';
import agritechSadc from '../assets/images/agritech_sadc_1789078246558.jpg';
import fintechHubSadc from '../assets/images/fintech_hub_sadc_1789078259804.jpg';
import solarGridSadc from '../assets/images/solar_grid_sadc_1789078270848.jpg';

interface IndustriesSectionProps {
  initialIndustry?: string;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const IndustriesSection: React.FC<IndustriesSectionProps> = ({
  initialIndustry = 'government',
  onOpenContactModal,
  theme = 'dark'
}) => {
  const [selectedIndustry, setSelectedIndustry] = useState<string>(initialIndustry);
  const isLight = theme === 'light';

  const industriesList = [
    {
      id: 'government',
      name: 'Government & Public Sector',
      icon: Landmark,
      problem: 'Bureaucratic friction, manual document processing, and lack of sovereign AI governance frameworks.',
      opportunity: 'Automate public consultation workflows, digitize civil registries, and deploy Chichewa/English civic AI agents.',
      solution: 'Pharos Policy & Sovereign Governance Rigs + E-Government Workflow Automation.',
      useCases: ['National AI Strategy Consultation', 'Customs Tariff Automated Verification', 'Civic Portal Multilingual Agents']
    },
    {
      id: 'development',
      name: 'Development & Donor Organisations',
      icon: Globe2,
      problem: 'High administrative overhead in field data collection, M&E reporting, and localized community advisory.',
      opportunity: 'Automated impact telemetry, Chichewa/Swahili audio survey analysis, and real-time grant monitoring.',
      solution: 'Donor M&E Agent Swarms & Rural Community Advisory Engines.',
      useCases: ['Automated Beneficiary Verification', 'Chichewa Voice Field Surveys', 'Grant SLA Audit Loggers']
    },
    {
      id: 'financial-services',
      name: 'Financial Services & Banking',
      icon: Building2,
      problem: 'Slow cross-border SADC settlements, high fraud rates in mobile money, and manual credit scoring.',
      opportunity: 'Sub-30s settlement reconciliation, real-time fraud monitoring, and automated micro-loan underwriting.',
      solution: 'FinTech & Airtel/TNM Settlement Guard + AI Credit Intelligence.',
      useCases: ['Cross-Border SADC Trade Settlement Audit', 'Mobile Money Fraud Anomaly Detection', 'Algorithmic Credit Scoring']
    },
    {
      id: 'telecom',
      name: 'Telecommunications',
      icon: Sparkles,
      problem: 'High customer churn, expensive call center operations, and network outage triage latency.',
      opportunity: 'Automated network anomaly triage and 24/7 AI customer care swarms in local languages.',
      solution: 'Telecom Network Telemetry & Conversational Agent Swarms.',
      useCases: ['Localized Voice/Text Customer Agents', 'Tower Outage Predictive Triage', 'SIM Activation Automated Audit']
    },
    {
      id: 'healthcare',
      name: 'Healthcare & Life Sciences',
      icon: Lock,
      problem: 'Shortage of clinical specialists, supply chain stockouts in rural clinics, and paper-based medical records.',
      opportunity: 'AI triage assistants, automated pharmaceutical inventory replenishment, and digital patient intake.',
      solution: 'HealthTech Sovereign Assistant & Rural Medical Inventory Agent.',
      useCases: ['Pharmaceutical Stockout Early Warning', 'Chichewa Symptom Intake Triage', 'District Hospital Records Digitization']
    },
    {
      id: 'agriculture',
      name: 'Agriculture & Value Chains',
      icon: Brain,
      problem: 'Climate instability, poor soil telemetry, and middleman price exploitation of smallholder farmers.',
      opportunity: 'Hyper-local weather telemetry, Chichewa agronomy advice, and transparent market price intelligence.',
      solution: 'AgriTech Sovereignty & Smallholder Advisor Agent.',
      useCases: ['Soil Telemetry Crop Recommendations', 'Chichewa Weather Advisory Broadcasts', 'Cooperative Supply Chain Routing']
    },
    {
      id: 'energy',
      name: 'Energy & Utilities',
      icon: Layers,
      problem: 'Grid load shedding, unmonitored solar mini-grids, and delayed billing reconciliation.',
      opportunity: 'Predictive grid load balancing, automated solar meter auditing, and smart tariff billing.',
      solution: 'Smart Grid Telemetry & Utility Settlement Engine.',
      useCases: ['Solar Mini-Grid Anomaly Detection', 'Prepaid Token Reconciliation Audit', 'Load Shedding Optimization']
    },
    {
      id: 'retail',
      name: 'Retail & Consumer Goods',
      icon: ShoppingBag,
      problem: 'Inventory shrinkage, stockouts across informal markets, and manual supplier ordering.',
      opportunity: 'Automated reordering agents, demand forecasting, and localized trade intelligence.',
      solution: 'FMCG Demand Intelligence & Supply Chain Agent.',
      useCases: ['Informal Market Demand Forecasting', 'Automated Supplier Reordering', 'Price Elasticity Analytics']
    },
    {
      id: 'growth',
      name: 'SMEs & Growth Companies',
      icon: Handshake,
      problem: 'Inability to scale headcount, limited access to executive advisory, and manual back-office tasks.',
      opportunity: 'Instant deployment of an AI Operating Model providing synthetic CFO, COO, and marketing sub-agents.',
      solution: 'AI Company Builder Package for High-Growth Enterprises.',
      useCases: ['Synthetic Executive Team', 'Automated Invoice & Tax Filing', 'AI Lead Generation Engine']
    }
  ];

  const currentInd = industriesList.find(i => i.id === selectedIndustry) || industriesList[0];

  return (
    <section id="industries" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">
      
      {/* Title & Classification */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            VERTICAL DOMAIN MATRICES // SECTOR ADAPTATION
          </span>
        </div>
        <h2 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Industry Matrices</span>
        </h2>
        <p className={`text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Mapping sector-specific business bottlenecks directly to autonomous AI capabilities, verifiable telemetry, and sovereign African deployments.
        </p>
      </div>

      {/* Grid selector + detail layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Industry Sector Selector */}
        <div className="lg:col-span-5 grid grid-cols-1 gap-2.5">
          {industriesList.map((ind) => {
            const Icon = ind.icon;
            const isSelected = ind.id === selectedIndustry;
            return (
              <button
                key={ind.id}
                onClick={() => setSelectedIndustry(ind.id)}
                className={`p-3.5 rounded-2xl text-left transition-all flex items-center justify-between border relative overflow-hidden ${
                  isSelected
                    ? isLight
                      ? 'chassis-milled-light border-amber-500 text-slate-900 shadow-md ring-1 ring-amber-500/50'
                      : 'chassis-milled-dark border-amber-500/60 text-zinc-100 shadow-lg shadow-amber-500/10 ring-1 ring-amber-500/30'
                    : isLight
                      ? 'bg-slate-100/90 border-slate-300 text-slate-700 hover:bg-slate-200/80'
                      : 'bg-zinc-900/60 border-zinc-800 text-zinc-300 hover:bg-zinc-800/80'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-xl transition-colors ${
                    isSelected 
                      ? 'bg-amber-500 text-slate-950 shadow-sm shadow-amber-500/30' 
                      : isLight 
                        ? 'bg-slate-200 text-amber-600' 
                        : 'bg-zinc-800 text-amber-400'
                  }`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex items-center gap-2">
                    <StatusLedPip status={isSelected ? 'emerald' : 'off'} isLight={isLight} />
                    <span className="text-xs font-mono font-bold uppercase tracking-wider">{ind.name}</span>
                  </div>
                </div>
                <ArrowRight className={`w-3.5 h-3.5 transition-transform ${
                  isSelected ? 'text-amber-500 translate-x-0.5' : isLight ? 'text-slate-400' : 'text-zinc-600'
                }`} />
              </button>
            );
          })}
        </div>

        {/* Selected Sector Detail Chassis */}
        <div className={`lg:col-span-7 p-6 sm:p-8 rounded-3xl border relative overflow-hidden transition-colors space-y-6 ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>
          <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
          <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
          <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
          <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-800 pb-4">
            <div className="flex items-center gap-3.5">
              <div className="p-3 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/30">
                <currentInd.icon className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-0.5">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="text-xs font-mono text-amber-500 font-extrabold uppercase tracking-wider">SECTOR SPECIFICATION</span>
                </div>
                <h3 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>{currentInd.name}</h3>
              </div>
            </div>
            <AcousticVentGrille cols={4} rows={2} isLight={isLight} />
          </div>

          {/* Sector Strategic Photography & Infographic Visual Banner */}
          <div className="relative rounded-2xl overflow-hidden mb-6 border border-zinc-800 aspect-[21/9] sm:aspect-[3/1]">
            <img 
              src={
                selectedIndustry === 'agriculture' ? agritechSadc :
                (selectedIndustry === 'financial-services' || selectedIndustry === 'telecom') ? fintechHubSadc :
                solarGridSadc
              }
              alt={currentInd.name}
              className="w-full h-full object-cover brightness-[0.75] contrast-[1.1]"
              referrerPolicy="no-referrer"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-4 sm:p-6 flex flex-col justify-end">
              <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ FIELD TELEMETRY & DOMAIN INFOGRAPHIC ]</span>
              <h4 className="text-sm sm:text-base font-bold font-mono text-white">{currentInd.name} Architecture</h4>
            </div>
          </div>

          <div className="space-y-4 text-xs">
            {/* Bottleneck */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <div className="flex items-center gap-2 mb-1.5 text-rose-500 font-mono font-bold uppercase">
                <StatusLedPip status="crimson" isLight={isLight} />
                <span>Sector Bottleneck & Vulnerability</span>
              </div>
              <p className={`leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{currentInd.problem}</p>
            </div>

            {/* AI Opportunity */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <div className="flex items-center gap-2 mb-1.5 text-emerald-500 font-mono font-bold uppercase">
                <StatusLedPip status="emerald" isLight={isLight} />
                <span>Autonomous Opportunity & Efficiency</span>
              </div>
              <p className={`leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{currentInd.opportunity}</p>
            </div>

            {/* Lightspeed Solution */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'bg-amber-50 border-amber-300' : 'bg-zinc-950 border-amber-500/40'
            }`}>
              <div className="flex items-center gap-2 mb-1.5 text-amber-500 font-mono font-bold uppercase">
                <Zap className="w-3.5 h-3.5 text-amber-500" />
                <span>LightSpeed Engineered Solution</span>
              </div>
              <p className={`font-semibold leading-relaxed ${isLight ? 'text-slate-900' : 'text-amber-200'}`}>{currentInd.solution}</p>
            </div>
          </div>

          {/* Deployment Use Cases */}
          <div>
            <h4 className="text-xs font-mono text-amber-500 uppercase font-bold mb-3 tracking-wider">VERIFIED DEPLOYMENT RIGS</h4>
            <div className="space-y-2">
              {currentInd.useCases.map((uc, i) => (
                <div key={i} className={`flex items-center gap-2.5 text-xs p-3 rounded-xl border ${
                  isLight ? 'flight-deck-well-light text-slate-800' : 'flight-deck-well-dark text-zinc-200'
                }`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span className="font-mono">{uc}</span>
                </div>
              ))}
            </div>
          </div>

          <div className={`pt-4 border-t flex justify-end ${isLight ? 'border-slate-300' : 'border-zinc-800'}`}>
            <button
              onClick={() => onOpenContactModal(`Discuss Solutions for ${currentInd.name}`)}
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 active:scale-95"
            >
              <span>Explore {currentInd.name} Deployment</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>

    </section>
  );
};
