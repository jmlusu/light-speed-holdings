import React, { useState } from 'react';
import { ShieldCheck, FileText, Lock, Globe2, Eye, CheckCircle2 } from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille, 
  ChassisPanel 
} from './TactileHardwareElements';

interface LegalSectionProps {
  initialTab?: 'privacy' | 'terms' | 'cookies' | 'ai-principles' | 'accessibility';
  theme?: 'light' | 'dark';
}

export const LegalSection: React.FC<LegalSectionProps> = ({
  initialTab = 'privacy',
  theme = 'dark'
}) => {
  const [activeLegalTab, setActiveLegalTab] = useState<'privacy' | 'terms' | 'cookies' | 'ai-principles' | 'accessibility'>(initialTab);
  const isLight = theme === 'light';

  const tabs: Array<{ id: 'privacy' | 'terms' | 'cookies' | 'ai-principles' | 'accessibility'; label: string }> = [
    { id: 'privacy', label: 'Privacy Policy' },
    { id: 'terms', label: 'Terms of Use' },
    { id: 'cookies', label: 'Cookie Policy' },
    { id: 'ai-principles', label: 'AI Principles & Ethics' },
    { id: 'accessibility', label: 'Accessibility Statement' }
  ];

  return (
    <section id="legal" className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12 font-sans">
      
      {/* Title & Classification */}
      <div className="text-center max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold uppercase tracking-wider mb-4 border select-none">
          <StatusLedPip status="emerald" isLight={isLight} />
          <span className={`text-[10px] font-mono tracking-widest ${isLight ? 'text-slate-800' : 'text-zinc-300'}`}>
            FIDUCIARY & COMPLIANCE ARCHIVE // SADC REGULATORY REGISTER
          </span>
        </div>
        <h1 className={`text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-display mb-4 leading-normal sm:leading-tight break-words ${
          isLight ? 'text-slate-900' : 'text-zinc-100'
        }`}>
          <span className="inline-block pb-1.5 text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">Legal Statements</span>
        </h1>
        <p className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
          Consistently registered and operated as LightSpeed Holdings Limited (Malawi & SADC Region).
        </p>
      </div>

      {/* Hardware Selector Tabs */}
      <div className="flex flex-wrap justify-center gap-2">
        <div className={`p-1.5 rounded-2xl border inline-flex flex-wrap gap-2 ${
          isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
        }`}>
          {tabs.map((tab) => {
            const isActive = activeLegalTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveLegalTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase transition-all ${
                  isActive
                    ? 'bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20'
                    : isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <StatusLedPip status={isActive ? 'emerald' : 'off'} isLight={isLight} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Legal Chassis Panel */}
      <div className={`p-8 sm:p-10 rounded-3xl border relative overflow-hidden text-xs leading-relaxed space-y-5 max-w-4xl mx-auto transition-all ${
        isLight ? 'chassis-milled-light text-slate-800' : 'chassis-milled-dark text-zinc-300'
      }`}>
        <MachineScrewHead isLight={isLight} className="absolute top-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute top-3 right-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 left-3" />
        <MachineScrewHead isLight={isLight} className="absolute bottom-3 right-3" />

        <div className="flex items-center justify-between border-b border-zinc-800/80 pb-4">
          <div className="flex items-center gap-2">
            <StatusLedPip status="emerald" isLight={isLight} />
            <span className="font-mono text-amber-500 font-extrabold uppercase tracking-wider text-[11px]">
              REGULATORY REGISTER ID: LSH-MW-2026-LAW
            </span>
          </div>
          <AcousticVentGrille cols={4} rows={2} isLight={isLight} />
        </div>

        {activeLegalTab === 'privacy' && (
          <div className="space-y-3">
            <h2 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              Data Sovereignty & Privacy Policy
            </h2>
            <p>
              LightSpeed Holdings Limited is committed to defending sovereign data governance and institutional privacy across Malawi, SADC member states, and Pan-African corridors. We operate on a strict zero-retention model for raw client documents processed via sovereign AI proxy pipelines.
            </p>
            <p>
              All agentic inference calls utilize private tenant isolation with zero cross-model training on client data. Telemetry logs are encrypted at rest using AES-256 and HMAC-SHA256 authenticated transmission.
            </p>
          </div>
        )}

        {activeLegalTab === 'terms' && (
          <div className="space-y-3">
            <h2 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              Terms of Institutional Engagement
            </h2>
            <p>
              All proprietary architecture specifications, OpenCode agent templates, and sovereign AI consultation frameworks presented on this platform are the exclusive intellectual property of LightSpeed Holdings Limited.
            </p>
            <p>
              Authorized partners and clients receive non-exclusive, auditable operational deployment licenses under bilateral enterprise service level agreements (SLAs).
            </p>
          </div>
        )}

        {activeLegalTab === 'cookies' && (
          <div className="space-y-3">
            <h2 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              Cookie & Telemetry Policy
            </h2>
            <p>
              We employ strictly essential operational session storage to preserve interface state (such as Dark Command Deck vs. Light Clean Lab mode and interactive assessment calibrations).
            </p>
            <p>
              We strictly forbid third-party cross-site advertising pixels or tracking scripts on our infrastructure.
            </p>
          </div>
        )}

        {activeLegalTab === 'ai-principles' && (
          <div className="space-y-4">
            <h2 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              Responsible AI & Sovereign Ethics Charter
            </h2>
            <div className="space-y-2">
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <p><strong>1. Human-in-the-Loop (HITL) Veto Power:</strong> Critical automated operations require explicit human executive cryptographic signatures prior to execution.</p>
              </div>
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <p><strong>2. Linguistic & Regional Sovereignty:</strong> Preserving Chichewa, regional African dialects, and local cultural context in all trained models and voice advisory agents.</p>
              </div>
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                <p><strong>3. Cryptographic Auditability:</strong> 100% auditable evidence trails for every sub-agent action, tool execution, and database mutation.</p>
              </div>
            </div>
          </div>
        )}

        {activeLegalTab === 'accessibility' && (
          <div className="space-y-3">
            <h2 className={`text-lg font-bold font-display ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
              Accessibility & Usability Standard
            </h2>
            <p>
              LightSpeed Holdings Limited builds hardware-grade web applications complying rigorously with WCAG 2.1 AA contrast standards, keyboard navigation, and screen reader semantic tagging.
            </p>
            <p>
              High-contrast physical tactile cues, clear typography step scales, and reduced motion options ensure complete usability across all environments.
            </p>
          </div>
        )}

        <div className={`pt-4 border-t flex items-center justify-between font-mono text-[10px] ${
          isLight ? 'border-slate-300 text-slate-500' : 'border-zinc-800 text-zinc-500'
        }`}>
          <span>GOVERNANCE AUTHORITY: SADC COMPLIANCE REGISTRY</span>
          <span className="text-emerald-500 font-bold">VERIFIED SECURE</span>
        </div>
      </div>

    </section>
  );
};
