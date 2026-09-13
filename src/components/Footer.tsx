import React from 'react';
import { Shield, Sparkles, ArrowUpRight, Globe2, Radio, Terminal } from 'lucide-react';
import { 
  StatusLedPip, 
  MachineScrewHead, 
  AcousticVentGrille 
} from './TactileHardwareElements';

interface FooterProps {
  onNavigate: (route: string) => void;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
}

export const Footer: React.FC<FooterProps> = ({
  onNavigate,
  onOpenContactModal,
  theme = 'dark'
}) => {
  const isLight = theme === 'light';

  return (
    <footer className={`border-t pt-14 pb-12 px-4 sm:px-6 lg:px-8 font-sans transition-colors relative overflow-hidden ${
      isLight 
        ? 'bg-[#f4f5f8] border-slate-300 text-slate-700' 
        : 'bg-[#06080e] border-zinc-800 text-zinc-300'
    }`}>
      <MachineScrewHead isLight={isLight} className="absolute top-3 left-4" />
      <MachineScrewHead isLight={isLight} className="absolute top-3 right-4" />

      <div className="max-w-7xl mx-auto space-y-12">
        
        {/* Brand Hardware Header & Command Tagline */}
        <div className={`flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b ${
          isLight ? 'border-slate-300' : 'border-zinc-800'
        }`}>
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <img 
                src="/static/brand/logos/icononly/icononly_transparent_nobuffer.png" 
                alt="LightSpeed Holdings Limited" 
                className="h-10 sm:h-12 w-auto object-contain shrink-0"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = '/brand/logos/icononly/icononly_transparent_nobuffer.png';
                }}
              />
              <div>
                <div className="flex items-center gap-2">
                  <StatusLedPip status="emerald" isLight={isLight} />
                  <span className="font-extrabold font-display text-lg sm:text-xl tracking-tight bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600 bg-clip-text text-transparent">
                    LightSpeed Holdings Limited
                  </span>
                </div>
                <p className={`text-[11px] font-mono mt-0.5 tracking-wider uppercase ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                  AI-NATIVE OPERATOR &amp; PARTNER // INSTITUTIONAL COMMAND
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <AcousticVentGrille cols={6} rows={2} isLight={isLight} />
            <button
              onClick={() => onOpenContactModal('Start a Conversation')}
              className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-extrabold font-mono text-xs uppercase tracking-wider transition-all shadow-lg shadow-amber-500/20 flex items-center gap-2 active:scale-95"
            >
              <span>Engage Command Desk</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Multi-Column Sitemap Layout */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 text-xs">
          
          {/* Solutions */}
          <div className="space-y-3">
            <div className="flex items-center gap-1.5">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h4 className="font-mono font-bold text-amber-500 uppercase tracking-wider text-[11px]">Solutions</h4>
            </div>
            <ul className={`space-y-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              <li><button onClick={() => onNavigate('solutions')} className="hover:text-amber-500 transition-colors">Agentic AI Systems</button></li>
              <li><button onClick={() => onNavigate('solutions')} className="hover:text-amber-500 transition-colors">Digital Transformation</button></li>
              <li><button onClick={() => onNavigate('solutions')} className="hover:text-amber-500 transition-colors">Data & Intelligence</button></li>
              <li><button onClick={() => onNavigate('solutions')} className="hover:text-amber-500 transition-colors">Intelligent Automation</button></li>
              <li><button onClick={() => onNavigate('solutions')} className="hover:text-amber-500 transition-colors">Strategy & Advisory</button></li>
              <li><button onClick={() => onNavigate('solutions')} className="hover:text-amber-500 transition-colors">AI Policy & Governance</button></li>
            </ul>
          </div>

          {/* Industries */}
          <div className="space-y-3">
            <div className="flex items-center gap-1.5">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h4 className="font-mono font-bold text-amber-500 uppercase tracking-wider text-[11px]">Industries</h4>
            </div>
            <ul className={`space-y-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">Government & Public</button></li>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">Development & Donors</button></li>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">Financial Services</button></li>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">Telecommunications</button></li>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">Healthcare Sciences</button></li>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">Agriculture AgriTech</button></li>
              <li><button onClick={() => onNavigate('industries')} className="hover:text-amber-500 transition-colors">SMEs & Growth Co.</button></li>
            </ul>
          </div>

          {/* AI Company Builder */}
          <div className="space-y-3">
            <div className="flex items-center gap-1.5">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h4 className="font-mono font-bold text-amber-500 uppercase tracking-wider text-[11px]">Builder Rigs</h4>
            </div>
            <ul className={`space-y-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              <li><button onClick={() => onNavigate('ai-company-builder')} className="hover:text-amber-500 transition-colors">AI Operating Model</button></li>
              <li><button onClick={() => onNavigate('ai-company-builder')} className="hover:text-amber-500 transition-colors">Agent Workforce</button></li>
              <li><button onClick={() => onNavigate('ai-company-builder')} className="hover:text-amber-500 transition-colors">Workflow Collapse</button></li>
              <li><button onClick={() => onNavigate('ai-company-builder')} className="hover:text-amber-500 transition-colors">AI Product Factory</button></li>
              <li><button onClick={() => onNavigate('ai-company-builder')} className="hover:text-amber-500 transition-colors">HITL Governance</button></li>
            </ul>
          </div>

          {/* Technology & Work */}
          <div className="space-y-3">
            <div className="flex items-center gap-1.5">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h4 className="font-mono font-bold text-amber-500 uppercase tracking-wider text-[11px]">Tech & Proof</h4>
            </div>
            <ul className={`space-y-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              <li><button onClick={() => onNavigate('technology')} className="hover:text-amber-500 transition-colors">Sovereign Architecture</button></li>
              <li><button onClick={() => onNavigate('technology')} className="hover:text-amber-500 transition-colors">OpenCode Spec Cards</button></li>
              <li><button onClick={() => onNavigate('technology')} className="hover:text-amber-500 transition-colors">Live Benchmarks</button></li>
              <li><button onClick={() => onNavigate('work')} className="hover:text-amber-500 transition-colors">Case Studies</button></li>
            </ul>
          </div>

          {/* Pharos // The Sovereign Beacon */}
          <div className="space-y-3">
            <div className="flex items-center gap-1.5">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h4 className="font-mono font-bold text-amber-500 uppercase tracking-wider text-[11px]">Pharos</h4>
            </div>
            <ul className={`space-y-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              <li><button onClick={() => onNavigate('pharos')} className="hover:text-amber-500 transition-colors">Alexandria Beacon &amp; Lore</button></li>
              <li><button onClick={() => onNavigate('pharos')} className="hover:text-amber-500 transition-colors">Sovereign Treatises</button></li>
              <li><button onClick={() => onNavigate('pharos')} className="hover:text-amber-500 transition-colors">SADC Research Reports</button></li>
              <li><button onClick={() => onNavigate('resources')} className="hover:text-amber-500 transition-colors">AI Readiness Assessment</button></li>
            </ul>
          </div>

          {/* Company & Legal */}
          <div className="space-y-3">
            <div className="flex items-center gap-1.5">
              <StatusLedPip status="emerald" isLight={isLight} />
              <h4 className="font-mono font-bold text-amber-500 uppercase tracking-wider text-[11px]">Governance</h4>
            </div>
            <ul className={`space-y-2 ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              <li><button onClick={() => onNavigate('about')} className="hover:text-amber-500 transition-colors">Institutional Thesis</button></li>
              <li><button onClick={() => onNavigate('about')} className="hover:text-amber-500 transition-colors">Board & Fiduciary</button></li>
              <li><button onClick={() => onNavigate('legal')} className="hover:text-amber-500 transition-colors">Zero-Trust Privacy</button></li>
              <li><button onClick={() => onNavigate('legal')} className="hover:text-amber-500 transition-colors">Terms of Operations</button></li>
              <li><button onClick={() => onNavigate('legal')} className="hover:text-amber-500 transition-colors">AI Ethics Rig</button></li>
            </ul>
          </div>

        </div>

        {/* Bottom Hardware Telemetry & Copyright Bar */}
        <div className={`pt-8 border-t flex flex-col sm:flex-row items-center justify-between text-xs font-mono gap-4 ${
          isLight ? 'border-slate-300 text-slate-600' : 'border-zinc-800 text-zinc-500'
        }`}>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse"></span>
            <span>© 2026 LightSpeed Holdings Limited • REPUBLIC OF MALAWI • ENCRYPTED SOVEREIGN CORE</span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={() => onNavigate('legal')} className="hover:text-amber-500">PRIVACY PROTOCOL</button>
            <span>•</span>
            <button onClick={() => onNavigate('legal')} className="hover:text-amber-500">TERMS OF SERVICE</button>
            <span>•</span>
            <button onClick={() => onNavigate('legal')} className="hover:text-amber-500">ACCESSIBILITY AA</button>
          </div>
        </div>

      </div>
    </footer>
  );
};
