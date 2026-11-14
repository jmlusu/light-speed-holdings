import React, { useState } from 'react';
import { Sparkles, Shield, Cpu, Users, Zap, CheckCircle2, ArrowRight, Layers, Activity } from 'lucide-react';
import { Link } from 'react-router-dom';

interface StrategicHeroVisualProps {
  theme: 'light' | 'dark';
}

export const StrategicHeroVisual: React.FC<StrategicHeroVisualProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [activeTab, setActiveTab] = useState<'architecture' | 'fleet' | 'governance'>('architecture');

  return (
    <div className={`relative rounded-3xl p-6 sm:p-8 overflow-hidden transition-all duration-300 shadow-2xl ${
      isLight
        ? 'bg-gradient-to-br from-ls-white via-ls-grey-light to-ls-white shadow-ls-navy/10'
        : 'bg-gradient-to-br from-ls-navy/95 via-ls-navy to-[#040625] shadow-ls-cyan/20'
    }`}>
      {/* Topographic background SVG pattern */}
      <div className="absolute inset-0 opacity-15 pointer-events-none" aria-hidden="true">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" fill="none">
          <path d="M-100 100C100 50 300 200 500 100C700 0 900 150 1100 50" stroke={isLight ? '#070A40' : '#00BFFF'} strokeWidth="1.5" />
          <path d="M-100 220C120 170 320 320 520 220C720 120 920 270 1120 170" stroke={isLight ? '#DC3641' : '#DC3641'} strokeWidth="1" strokeDasharray="4 4" />
          <path d="M-100 340C80 290 280 440 480 340C680 240 880 390 1080 290" stroke={isLight ? '#070A40' : '#00BFFF'} strokeWidth="1.5" />
          <path d="M-100 460C140 410 340 560 540 460C740 360 940 510 1140 410" stroke={isLight ? '#DC3641' : '#DC3641'} strokeWidth="1.5" />
        </svg>
      </div>

      {/* Header Badge & Controls */}
      <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-ls-red animate-pulse shadow-xs shadow-ls-red" />
          <div>
            <span className={`font-body text-[10px] font-bold tracking-widest uppercase block ${isLight ? 'text-ls-grey-dark' : 'text-ls-cyan'}`}>
              LIGHTSPEED HOLDINGS LIMITED™ // STRATEGIC ENGINE
            </span>
            <h3 className={`font-display font-extrabold text-lg sm:text-xl tracking-tight ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>
              AI-Native Company Builder & Orchestration Map
            </h3>
          </div>
        </div>

        <div className={`inline-flex p-1 rounded-full text-xs font-body font-bold ${isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-ls-navy text-ls-grey-light-text'}`}>
          <button
            type="button"
            onClick={() => setActiveTab('architecture')}
            className={`px-3 py-1.5 rounded-full transition-all cursor-pointer ${activeTab === 'architecture' ? 'bg-ls-red text-ls-white shadow-xs' : 'hover:text-ls-white'}`}
          >
            H-A-O-M-T-G-V
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('fleet')}
            className={`px-3 py-1.5 rounded-full transition-all cursor-pointer ${activeTab === 'fleet' ? 'bg-ls-red text-ls-white shadow-xs' : 'hover:text-ls-white'}`}
          >
            90-Role Fleet
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('governance')}
            className={`px-3 py-1.5 rounded-full transition-all cursor-pointer ${activeTab === 'governance' ? 'bg-ls-red text-ls-white shadow-xs' : 'hover:text-ls-white'}`}
          >
            Governance
          </button>
        </div>
      </div>

      {/* Tab Content 1: H-A-O-M-T-G-V Architecture */}
      {activeTab === 'architecture' && (
        <div className="relative z-10 space-y-4 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {/* Human Card */}
            <div className={`p-4 rounded-2xl transition-all ${isLight ? 'bg-ls-white shadow-xs' : 'bg-ls-navy/90 shadow-sm shadow-ls-cyan/10'}`}>
              <div className="flex items-center gap-2 mb-2">
                <div className="w-7 h-7 rounded-lg bg-ls-red/10 flex items-center justify-center text-ls-red font-bold text-xs">
                  01
                </div>
                <div>
                  <span className={`text-[10px] font-body font-bold tracking-widest uppercase ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Top Authority</span>
                  <h4 className={`font-display font-bold text-sm ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Human Command</h4>
                </div>
              </div>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-navy/80 font-medium' : 'text-ls-grey-light-text'}`}>
                Operational intent, contextual values, and 5-tier final approval authority retained by the Human CEO.
              </p>
            </div>

            {/* Agents Card */}
            <div className={`p-4 rounded-2xl transition-all ${isLight ? 'bg-ls-white shadow-xs' : 'bg-ls-navy/90 shadow-sm'}`}>
              <div className="flex items-center gap-2 mb-2">
                <div className="w-7 h-7 rounded-lg bg-ls-cyan/10 flex items-center justify-center text-ls-cyan font-bold text-xs">
                  02
                </div>
                <div>
                  <span className={`text-[10px] font-body font-bold tracking-widest uppercase ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Specialized Units</span>
                  <h4 className={`font-display font-bold text-sm ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>89 AI Agent Fleet</h4>
                </div>
              </div>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-navy/80 font-medium' : 'text-ls-grey-light-text'}`}>
                Scoped execution across 20 operating departments: strategy, engineering, data, compliance, and growth.
              </p>
            </div>

            {/* Orchestration & Governance Card */}
            <div className={`p-4 rounded-2xl transition-all ${isLight ? 'bg-ls-white shadow-xs' : 'bg-ls-navy/90 shadow-sm shadow-ls-red/10'}`}>
              <div className="flex items-center gap-2 mb-2">
                <div className="w-7 h-7 rounded-lg bg-ls-red/10 flex items-center justify-center text-ls-red font-bold text-xs">
                  03
                </div>
                <div>
                  <span className={`text-[10px] font-body font-bold tracking-widest uppercase ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Rules & Audit</span>
                  <h4 className={`font-display font-bold text-sm ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Governed Value</h4>
                </div>
              </div>
              <p className={`text-xs leading-relaxed ${isLight ? 'text-ls-navy/80 font-medium' : 'text-ls-grey-light-text'}`}>
                Deterministic routing, append-only memory stores, verified tool usage, and measurable business outcomes.
              </p>
            </div>
          </div>

          <div className={`p-4 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 ${
            isLight ? 'bg-ls-white/90' : 'bg-ls-navy/70'
          }`}>
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-ls-cyan animate-pulse" />
              <div>
                <span className={`text-xs font-bold block ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Active Systemic Pipeline</span>
                <span className={`text-[11px] ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Opportunity → Design → Build → Deploy → Govern → Measure</span>
              </div>
            </div>
            <Link
              to="/what-we-do"
              className="px-4 py-2 rounded-full font-bold text-xs tracking-widest bg-ls-red hover:bg-[#d62837] text-ls-white transition-all shadow-xs inline-flex items-center gap-2"
            >
              <span>Explore Full Architecture</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      )}

      {/* Tab Content 2: 90-Role Fleet */}
      {activeTab === 'fleet' && (
        <div className="relative z-10 space-y-4 animate-fade-in">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { role: 'Executive Leadership', count: '4 Agents', status: 'Active' },
              { role: 'Engineering & DevOps', count: '18 Agents', status: 'Active' },
              { role: 'Strategy & Research', count: '14 Agents', status: 'Active' },
              { role: 'Governance & Security', count: '12 Agents', status: 'Active' },
              { role: 'Product & Design', count: '12 Agents', status: 'Active' },
              { role: 'Commercial & Growth', count: '15 Agents', status: 'Active' },
              { role: 'Operations & Legal', count: '14 Agents', status: 'Active' },
              { role: 'Human CEO', count: '1 Human', status: 'Supreme' },
            ].map((item) => (
              <div key={item.role} className={`p-3.5 rounded-xl ${isLight ? 'bg-ls-white' : 'bg-ls-navy/80'}`}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-body font-bold text-ls-red tracking-wider uppercase">{item.status}</span>
                  <Cpu className="w-3.5 h-3.5 text-ls-cyan" />
                </div>
                <h4 className={`font-display font-bold text-xs mb-0.5 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>{item.role}</h4>
                <span className={`text-[11px] font-bold ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>{item.count}</span>
              </div>
            ))}
          </div>
          <p className={`text-[11px] italic text-center ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
            Every agent operates under strict scoped tool access, automated regression testing, and transparent logging.
          </p>
        </div>
      )}

      {/* Tab Content 3: Governance */}
      {activeTab === 'governance' && (
        <div className="relative z-10 space-y-3 animate-fade-in">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className={`p-4 rounded-xl ${isLight ? 'bg-ls-white' : 'bg-ls-navy/80'}`}>
              <Shield className="w-5 h-5 text-ls-red mb-2" />
              <h4 className={`font-display font-bold text-sm mb-1 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Five-Tier Approval</h4>
              <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Escalation thresholds ranging from automated validation to human executive sign-off.</p>
            </div>
            <div className={`p-4 rounded-xl ${isLight ? 'bg-ls-white' : 'bg-ls-navy/80'}`}>
              <CheckCircle2 className="w-5 h-5 text-ls-cyan mb-2" />
              <h4 className={`font-display font-bold text-sm mb-1 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Append-Only Audits</h4>
              <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Immutable records of all agent decisions, prompt trails, and state modifications.</p>
            </div>
            <div className={`p-4 rounded-xl ${isLight ? 'bg-ls-white' : 'bg-ls-navy/80'}`}>
              <Zap className="w-5 h-5 text-ls-red mb-2" />
              <h4 className={`font-display font-bold text-sm mb-1 ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}>Resource Aware</h4>
              <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>Optimized token consumption, local compute capability, and sustainable operation.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StrategicHeroVisual;
