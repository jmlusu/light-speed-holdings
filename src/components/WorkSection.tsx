import React, { useState } from 'react';
import { 
  Building2, 
  Landmark, 
  Globe2, 
  CheckCircle2, 
  ArrowRight, 
  Cpu, 
  Layers,
  Sparkles
} from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';
import executiveLeadershipStory from '../assets/images/executive_leadership_story_1789250993517.jpg';

interface WorkSectionProps {
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const WorkSection: React.FC<WorkSectionProps> = ({
  onOpenContactModal,
  theme = 'dark'
}) => {
  const [selectedCase, setSelectedCase] = useState<number>(0);
  const isLight = theme === 'light';

  const caseStudies = [
    {
      id: 'case-1',
      title: 'National AI Policy Consultation & Sovereign Strategy',
      clientSector: 'Government & E-Government Department / SADC Region',
      challenge: 'The Department needed a structured, auditable consultation framework to evaluate national AI risk tiering, Chichewa language preservation, and SADC digital model laws.',
      discovery: 'Traditional legal consulting took 6–9 months with minimal technical validation of agentic tool-use risks.',
      strategy: 'Deploy the Pharos Policy Track—a hybrid human-in-the-loop consultation engine evaluating risk tiers (Tier 1 Auto to Tier 5 Executive Signature).',
      architecture: 'Sub-agent swarm utilizing Chichewa/English translation layers, regulatory graph indexing, and automated policy diff generation.',
      builtLayer: 'Interactive Policy Consultation Portal & Risk Tiering Matrix.',
      results: 'Delivered national consultation submission draft in 14 days with 100% auditable evidence logs and SADC alignment.',
      technology: ['OpenCode Sub-Agents', 'Chichewa NLP Model', 'PostgreSQL Policy Graph'],
      metrics: '14-Day Delivery // 100% Audit Precision'
    },
    {
      id: 'case-2',
      title: 'Sub-Second Cross-Border Mobile Money Settlement Audit',
      clientSector: 'Financial Services & Mobile Network Operators (Airtel / TNM)',
      challenge: 'Cross-border trade transactions between Malawi, Zambia, and Mozambique suffered from reconciliation delays exceeding 48 hours.',
      discovery: 'Manual ledger reconciliation between disparate mobile money wallets and custom border databases was creating severe liquidity bottlenecks.',
      strategy: 'Engineer an automated FinTech Settlement Guard agent to audit and reconcile synthetic settlement batches in under 30 seconds.',
      architecture: 'Asynchronous event bus monitoring mobile money APIs, automated fraud anomaly detection, and instant MWK/USD conversion ledgers.',
      builtLayer: 'Real-Time FinTech Reconciliation Engine & Border Liquidity Guard.',
      results: 'Reduced average settlement audit latency from 48 hours to 14.2 seconds while maintaining zero ledger discrepancies.',
      technology: ['Airtel/TNM API Hooks', 'Event Bus Message Queue', 'Zero-Trust Security'],
      metrics: '48hr → 14.2s Latency Collapse'
    },
    {
      id: 'case-3',
      title: 'Chichewa Agronomy Voice Advisory for Shire Valley Cooperatives',
      clientSector: 'Agriculture & Development Donor Organizations',
      challenge: 'Rural smallholder maize farmers lacked real-time, localized agronomy advice during unseasonal rainfall shifts caused by climate variations.',
      discovery: 'Standard text-based apps failed due to low literacy and internet connectivity gaps in remote farming communities.',
      strategy: 'Build a low-bandwidth Chichewa voice advisory agent broadcasting localized soil moisture telemetry and weather updates via mobile audio.',
      architecture: 'Satellite weather stream ingestion, automated Chichewa voice synthesis engine, and cooperative SMS/IVR dispatch system.',
      builtLayer: 'AgriTech Voice Advisory & Food Sovereignty Agent.',
      results: 'Reached over 25,000 smallholder farmers in 3 districts with timely crop management guidance.',
      technology: ['Agri-Telemetry Stream', 'Chichewa Voice Gen', 'IVR Telecom Bridge'],
      metrics: '25k+ Smallholders Active'
    }
  ];

  const currentCase = caseStudies[selectedCase];

  return (
    <section id="work" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto font-sans">
      
      {/* Title & Classification */}
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            PROVEN TRACK RECORD // EMPIRICAL OPERATIONAL RIGS
          </span>
        </div>
        <h2 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Case Records & Proof</span>
        </h2>
        <p className={`text-base leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Measurable, sovereign deployments across governance, fintech reconciliation, and community agriculture infrastructure.
        </p>
      </div>

      {/* Case Study Selector + Telemetry Chassis */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-12">
        
        {/* Selector Tabs */}
        <div className="lg:col-span-4 space-y-3">
          {caseStudies.map((cs, idx) => {
            const isSelected = selectedCase === idx;
            return (
              <button
                key={cs.id}
                onClick={() => setSelectedCase(idx)}
                className={`w-full p-4 rounded-2xl text-left transition-all border relative overflow-hidden ${
                  isSelected
                    ? isLight
                      ? 'chassis-milled-light border-amber-500 text-slate-900 shadow-md ring-1 ring-amber-500/50'
                      : 'chassis-milled-dark border-amber-500/60 text-zinc-100 shadow-lg shadow-amber-500/10 ring-1 ring-amber-500/30'
                    : isLight
                      ? 'bg-slate-100/90 border-slate-300 text-slate-700 hover:bg-slate-200/80'
                      : 'bg-zinc-900/60 border-zinc-800 text-zinc-300 hover:bg-zinc-800/80'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] font-mono text-amber-500 font-bold uppercase tracking-wider">
                    {cs.clientSector}
                  </span>
                  <StatusLedPip status={isSelected ? 'emerald' : 'off'} isLight={isLight} />
                </div>
                <h3 className="font-bold text-sm leading-snug">{cs.title}</h3>
                <div className="mt-2.5 flex items-center justify-between pt-2 border-t border-zinc-800/40 text-[10px] font-mono text-emerald-500">
                  <span>{cs.metrics}</span>
                  <ArrowRight className={`w-3.5 h-3.5 transition-transform ${isSelected ? 'translate-x-1' : 'opacity-40'}`} />
                </div>
              </button>
            );
          })}
        </div>

        {/* Detailed Case Flight Deck */}
        <div className={`lg:col-span-8 p-6 sm:p-8 rounded-3xl border relative overflow-hidden space-y-6 ${
          isLight ? 'chassis-milled-light' : 'chassis-milled-dark'
        }`}>
          <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
          <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
          <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
          <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-800 pb-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <StatusLedPip status="emerald" isLight={isLight} />
                <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-amber-500">
                  {currentCase.clientSector}
                </span>
              </div>
              <h3 className={`text-2xl font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                {currentCase.title}
              </h3>
            </div>
            <AcousticVentGrille cols={5} rows={2} isLight={isLight} />
          </div>

          {/* Strategic Case Study Visual Banner */}
          <div className="relative rounded-2xl overflow-hidden border border-zinc-800 aspect-[21/9] sm:aspect-[3/1]">
            <img 
              src={executiveLeadershipStory}
              alt={currentCase.title}
              className="w-full h-full object-cover brightness-[0.75] contrast-[1.1]"
              referrerPolicy="no-referrer"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent p-4 sm:p-6 flex flex-col justify-end">
              <span className="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-widest">[ PROOF CASE STUDY // METRICS INFOGRAPHIC ]</span>
              <h4 className="text-sm sm:text-base font-bold font-mono text-white">{currentCase.metrics}</h4>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Challenge */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <div className="flex items-center gap-2 mb-1 text-rose-500 font-mono font-bold uppercase">
                <StatusLedPip status="crimson" isLight={isLight} />
                <span>The Challenge</span>
              </div>
              <p className={`leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{currentCase.challenge}</p>
            </div>

            {/* Discovery */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <div className="flex items-center gap-2 mb-1 text-amber-500 font-mono font-bold uppercase">
                <StatusLedPip status="amber" isLight={isLight} />
                <span>The Discovery</span>
              </div>
              <p className={`leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{currentCase.discovery}</p>
            </div>

            {/* Strategy & Architecture */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
            }`}>
              <div className="flex items-center gap-2 mb-1 text-amber-500 font-mono font-bold uppercase">
                <Cpu className="w-3.5 h-3.5 text-amber-500" />
                <span>Strategy & Architecture</span>
              </div>
              <p className={`leading-relaxed ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>{currentCase.strategy}</p>
            </div>

            {/* Measured Results */}
            <div className={`p-4 rounded-2xl border ${
              isLight ? 'bg-emerald-50 border-emerald-300' : 'bg-zinc-950 border-emerald-500/40'
            }`}>
              <div className="flex items-center gap-2 mb-1 text-emerald-500 font-mono font-bold uppercase">
                <StatusLedPip status="emerald" isLight={isLight} />
                <span>Verified Result Telemetry</span>
              </div>
              <p className={`font-semibold leading-relaxed ${isLight ? 'text-emerald-950' : 'text-emerald-200'}`}>{currentCase.results}</p>
            </div>
          </div>

          <div className={`pt-4 border-t flex flex-wrap items-center justify-between gap-4 ${
            isLight ? 'border-slate-300' : 'border-zinc-800'
          }`}>
            <div className="flex flex-wrap gap-2">
              {currentCase.technology.map((tech, i) => (
                <span key={i} className={`px-3 py-1 rounded-lg border text-[11px] font-mono ${
                  isLight ? 'flight-deck-well-light text-slate-800' : 'flight-deck-well-dark text-zinc-300'
                }`}>
                  {tech}
                </span>
              ))}
            </div>

            <button
              onClick={() => onOpenContactModal(`Inquire about ${currentCase.title}`)}
              className="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 active:scale-95"
            >
              Request Technical Rig Specs
            </button>
          </div>
        </div>

      </div>

    </section>
  );
};
