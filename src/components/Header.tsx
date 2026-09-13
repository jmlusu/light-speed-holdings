import React, { useState, useEffect } from 'react';
import { 
  ChevronDown, 
  Cpu, 
  Layers, 
  Sparkles, 
  ShieldCheck, 
  Workflow, 
  Building2, 
  Globe2, 
  Bot, 
  Database, 
  Brain, 
  FileText, 
  Compass, 
  Lock, 
  Landmark, 
  Handshake, 
  Menu, 
  X,
  ArrowRight,
  Sun,
  Moon,
  Radio
} from 'lucide-react';

interface HeaderProps {
  currentRoute: string;
  onNavigate: (route: string, subSection?: string) => void;
  onOpenContactModal: (intent?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentRoute,
  onNavigate,
  onOpenContactModal,
  theme = 'dark',
  onToggleTheme
}) => {
  const [solutionsOpen, setSolutionsOpen] = useState(false);
  const [industriesOpen, setIndustriesOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isLight = theme === 'light';

  const handleLinkClick = (route: string, subSection?: string) => {
    onNavigate(route, subSection);
    setSolutionsOpen(false);
    setIndustriesOpen(false);
    setMobileMenuOpen(false);
  };

  const navItemClass = (route: string) => {
    const isActive = currentRoute === route;
    if (isLight) {
      return isActive 
        ? 'text-amber-700 font-bold neu-pressed-light shadow-inner' 
        : 'text-slate-700 hover:text-slate-900 hover:neu-pill-light';
    }
    return isActive 
      ? 'text-amber-400 font-bold neu-pressed-dark shadow-inner' 
      : 'text-slate-300 hover:text-white hover:neu-pill-dark';
  };

  return (
    <header className={`relative w-full z-40 transition-colors ${
      isLight 
        ? 'bg-[#edf3f8]/95 border-b border-[#e5b74c]/30 shadow-[0_4px_16px_rgba(6,13,22,0.06)]' 
        : 'bg-[#060d16]/95 border-b border-[#e5b74c]/25 shadow-[0_6px_20px_rgba(0,0,0,0.7)]'
    }`}>
      <div className="w-full max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-13 sm:h-14 gap-2">
          
          {/* Brand Logo */}
          <button 
            onClick={() => handleLinkClick('home')}
            className="flex items-center gap-2 sm:gap-2.5 text-left group focus:outline-none shrink-0 py-0.5 max-w-[70vw] sm:max-w-none"
          >
            <img 
              src="/static/brand/logos/icononly/icononly_transparent_nobuffer.png" 
              alt="LightSpeed Holdings Limited" 
              className="h-7 sm:h-8 xl:h-8.5 w-auto object-contain shrink-0 group-hover:scale-105 transition-transform duration-200"
              onError={(e) => {
                (e.target as HTMLImageElement).src = '/brand/logos/icononly/icononly_transparent_nobuffer.png';
              }}
            />
            <div className="flex flex-col justify-center min-w-0">
              <span className="font-extrabold text-xs sm:text-sm tracking-tight font-display truncate bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600 bg-clip-text text-transparent leading-tight">
                LightSpeed Holdings Limited
              </span>
              <p className={`text-[8px] sm:text-[8.5px] font-mono tracking-wider uppercase truncate hidden xs:block leading-none mt-0.5 ${
                isLight ? 'text-slate-500' : 'text-slate-400'
              }`}>
                AI-Native Operator &amp; Partner
              </p>
            </div>
          </button>

          {/* Desktop Navigation (Visible on xl+ screens) */}
          <nav className="hidden xl:flex items-center gap-0.5 2xl:gap-1 text-xs font-medium shrink-0">
            
            {/* Home Link */}
            <button
              onClick={() => handleLinkClick('home')}
              className={`px-2 py-1 rounded-md transition-colors whitespace-nowrap ${navItemClass('home')}`}
            >
              Home
            </button>

            {/* Solutions Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setSolutionsOpen(true)}
              onMouseLeave={() => setSolutionsOpen(false)}
            >
              <button
                onClick={() => handleLinkClick('solutions')}
                className={`px-2 py-1 rounded-md flex items-center gap-1 transition-colors whitespace-nowrap ${navItemClass('solutions')}`}
              >
                Solutions
                <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${solutionsOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Mega Menu: Solutions */}
              {solutionsOpen && (
                <div className={`absolute top-full left-0 w-[560px] max-w-[calc(100vw-2rem)] p-4 mt-1 rounded-2xl border shadow-2xl backdrop-blur-2xl grid grid-cols-2 gap-3 text-left animate-in fade-in slide-in-from-top-2 duration-150 z-50 ${
                  isLight ? 'bg-[#ffffff] border-[#e5b74c]/30 shadow-slate-300/80 text-slate-800' : 'bg-[#0f2231] border-[#e5b74c]/30 shadow-black/80 text-slate-100'
                }`}>
                  <button
                    onClick={() => handleLinkClick('solutions', 'agentic-ai')}
                    className={`p-3 rounded-xl transition-all text-left group border ${
                      isLight 
                        ? 'hover:bg-amber-50/80 border-transparent hover:border-amber-300' 
                        : 'hover:bg-slate-800/80 border-transparent hover:border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 text-amber-500 font-semibold text-sm mb-1">
                      <Bot className="w-4 h-4" />
                      Agentic AI
                    </div>
                    <p className={`text-xs leading-snug ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                      Autonomous agents, multi-agent orchestrations, and intelligent execution workflows.
                    </p>
                  </button>

                  <button
                    onClick={() => handleLinkClick('solutions', 'digital-transformation')}
                    className={`p-3 rounded-xl transition-all text-left group border ${
                      isLight 
                        ? 'hover:bg-amber-50/80 border-transparent hover:border-amber-300' 
                        : 'hover:bg-slate-800/80 border-transparent hover:border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 text-amber-500 font-semibold text-sm mb-1">
                      <Layers className="w-4 h-4" />
                      Digital Transformation
                    </div>
                    <p className={`text-xs leading-snug ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                      Enterprise architecture, cloud platforms, data engineering & modernization.
                    </p>
                  </button>

                  <button
                    onClick={() => handleLinkClick('solutions', 'data-intelligence')}
                    className={`p-3 rounded-xl transition-all text-left group border ${
                      isLight 
                        ? 'hover:bg-amber-50/80 border-transparent hover:border-amber-300' 
                        : 'hover:bg-slate-800/80 border-transparent hover:border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 text-amber-500 font-semibold text-sm mb-1">
                      <Database className="w-4 h-4" />
                      Data & Intelligence
                    </div>
                    <p className={`text-xs leading-snug ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                      Semantic fabric, market intelligence feeds, and AI decision support systems.
                    </p>
                  </button>

                  <button
                    onClick={() => handleLinkClick('solutions', 'automation')}
                    className={`p-3 rounded-xl transition-all text-left group border ${
                      isLight 
                        ? 'hover:bg-amber-50/80 border-transparent hover:border-amber-300' 
                        : 'hover:bg-slate-800/80 border-transparent hover:border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 text-amber-500 font-semibold text-sm mb-1">
                      <Workflow className="w-4 h-4" />
                      Intelligent Automation
                    </div>
                    <p className={`text-xs leading-snug ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                      Workflow collapse, automated process redesign, and SLA-bound execution.
                    </p>
                  </button>

                  <button
                    onClick={() => handleLinkClick('solutions', 'strategy-advisory')}
                    className={`p-3 rounded-xl transition-all text-left group border ${
                      isLight 
                        ? 'hover:bg-amber-50/80 border-transparent hover:border-amber-300' 
                        : 'hover:bg-slate-800/80 border-transparent hover:border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 text-amber-500 font-semibold text-sm mb-1">
                      <Compass className="w-4 h-4" />
                      Strategy & Advisory
                    </div>
                    <p className={`text-xs leading-snug ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                      Executive AI strategy, transformation roadmaps, and business model design.
                    </p>
                  </button>

                  <button
                    onClick={() => handleLinkClick('solutions', 'ai-policy-governance')}
                    className={`p-3 rounded-xl transition-all text-left group border ${
                      isLight 
                        ? 'hover:bg-amber-50/80 border-transparent hover:border-amber-300' 
                        : 'hover:bg-slate-800/80 border-transparent hover:border-amber-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 text-amber-500 font-semibold text-sm mb-1">
                      <ShieldCheck className="w-4 h-4" />
                      AI Governance & Policy
                    </div>
                    <p className={`text-xs leading-snug ${isLight ? 'text-slate-600' : 'text-slate-400'}`}>
                      Human-in-the-loop auditability, risk management, and regulatory compliance.
                    </p>
                  </button>
                </div>
              )}
            </div>

            {/* Industries Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setIndustriesOpen(true)}
              onMouseLeave={() => setIndustriesOpen(false)}
            >
              <button
                onClick={() => handleLinkClick('industries')}
                className={`px-2 py-1 rounded-md flex items-center gap-1 transition-colors whitespace-nowrap ${navItemClass('industries')}`}
              >
                Industries
                <ChevronDown className={`w-3 h-3 transition-transform duration-200 ${industriesOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Mega Menu: Industries */}
              {industriesOpen && (
                <div className={`absolute top-full left-0 w-[540px] max-w-[calc(100vw-2rem)] p-4 mt-1 rounded-2xl border shadow-2xl backdrop-blur-2xl grid grid-cols-2 gap-2 text-left animate-in fade-in slide-in-from-top-2 duration-150 z-50 ${
                  isLight ? 'bg-[#ffffff] border-[#e5b74c]/30 shadow-slate-300/80 text-slate-800' : 'bg-[#0f2231] border-[#e5b74c]/30 shadow-black/80 text-slate-100'
                }`}>
                  <button onClick={() => handleLinkClick('industries', 'government')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Landmark className="w-4 h-4 text-amber-500 shrink-0" /> Government & Public Sector
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'development')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Globe2 className="w-4 h-4 text-emerald-500 shrink-0" /> Development & Donors
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'financial-services')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Building2 className="w-4 h-4 text-cyan-500 shrink-0" /> Financial Services
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'telecom')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Sparkles className="w-4 h-4 text-purple-500 shrink-0" /> Telecommunications
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'healthcare')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Lock className="w-4 h-4 text-rose-500 shrink-0" /> Healthcare & Life Sciences
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'agriculture')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Brain className="w-4 h-4 text-amber-500 shrink-0" /> Agriculture & Value Chains
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'energy')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Layers className="w-4 h-4 text-blue-500 shrink-0" /> Energy & Utilities
                  </button>
                  <button onClick={() => handleLinkClick('industries', 'growth')} className={`p-2.5 rounded-lg text-left text-xs font-semibold flex items-center gap-2 ${isLight ? 'hover:bg-slate-100 text-slate-800 hover:text-amber-600' : 'hover:bg-slate-800/80 text-slate-200 hover:text-amber-400'}`}>
                    <Handshake className="w-4 h-4 text-indigo-500 shrink-0" /> SMEs & Growth Companies
                  </button>
                </div>
              )}
            </div>

            {/* AI Company Builder (Flagship) */}
            <button
              onClick={() => handleLinkClick('ai-company-builder')}
              className={`px-2 py-1 rounded-md transition-colors flex items-center gap-1 whitespace-nowrap ${
                currentRoute === 'ai-company-builder'
                  ? 'text-amber-500 font-bold bg-amber-500/10'
                  : 'text-amber-500 font-semibold hover:bg-amber-500/10'
              }`}
            >
              <Sparkles className="w-3 h-3 shrink-0" />
              <span className="hidden 2xl:inline">AI Company Builder</span>
              <span className="2xl:hidden">AI Builder</span>
            </button>

            {/* Technology */}
            <button
              onClick={() => handleLinkClick('technology')}
              className={`px-2 py-1 rounded-md transition-colors whitespace-nowrap ${navItemClass('technology')}`}
            >
              Technology
            </button>

            {/* Work */}
            <button
              onClick={() => handleLinkClick('work')}
              className={`px-2 py-1 rounded-md transition-colors whitespace-nowrap ${navItemClass('work')}`}
            >
              <span className="hidden 2xl:inline">Work & Proof</span>
              <span className="2xl:hidden">Work</span>
            </button>

            {/* Pharos // The Sovereign Beacon */}
            <button
              onClick={() => handleLinkClick('pharos')}
              className={`px-2 py-1 rounded-md transition-colors whitespace-nowrap ${
                currentRoute === 'pharos' || currentRoute === 'insights' || currentRoute === 'research'
                  ? (isLight ? 'text-amber-600 font-semibold bg-amber-50' : 'text-amber-400 font-semibold bg-amber-500/10')
                  : navItemClass('pharos')
              }`}
            >
              Pharos
            </button>

            {/* Resources / Readiness */}
            <button
              onClick={() => handleLinkClick('resources')}
              className={`px-2 py-1 rounded-md transition-colors whitespace-nowrap ${navItemClass('resources')}`}
            >
              Resources
            </button>

            {/* About */}
            <button
              onClick={() => handleLinkClick('about')}
              className={`px-2 py-1 rounded-md transition-colors whitespace-nowrap ${navItemClass('about')}`}
            >
              About
            </button>
          </nav>

          {/* Primary CTA & Theme Toggle */}
          <div className="hidden xl:flex items-center gap-2 shrink-0">
            
            {/* Theme Toggle Button */}
            <button
              onClick={onToggleTheme}
              title={isLight ? "Switch to Dark Mode" : "Switch to Light Mode"}
              aria-label="Toggle theme"
              className={`p-1.5 2xl:p-2 rounded-lg transition-all flex items-center gap-1 text-xs font-mono font-medium shrink-0 cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-800' : 'neu-btn-dark text-slate-200'
              }`}
            >
              {isLight ? (
                <>
                  <Moon className="w-3.5 h-3.5 text-indigo-600" />
                  <span className="hidden 2xl:inline text-[11px]">Dark</span>
                </>
              ) : (
                <>
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  <span className="hidden 2xl:inline text-[11px]">Light</span>
                </>
              )}
            </button>

            <button
              onClick={() => onOpenContactModal('Start a Conversation')}
              className="neu-btn-amber flex items-center gap-1.5 px-3 2xl:px-4 py-1.5 rounded-lg text-xs font-bold font-mono uppercase tracking-wider whitespace-nowrap shrink-0 cursor-pointer"
            >
              <span className="hidden 2xl:inline">Start a Conversation</span>
              <span className="2xl:hidden">Contact</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          {/* Mobile Actions: Theme Toggle + Menu Button */}
          <div className="xl:hidden flex items-center gap-2 shrink-0">
            <button
              onClick={onToggleTheme}
              title={isLight ? "Switch to Dark Mode" : "Switch to Light Mode"}
              aria-label="Toggle theme"
              className={`p-1.5 sm:p-2 rounded-lg transition-all cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-800' : 'neu-btn-dark text-slate-200'
              }`}
            >
              {isLight ? <Moon className="w-4 h-4 text-indigo-600" /> : <Sun className="w-4 h-4 text-amber-400" />}
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`p-1.5 sm:p-2 rounded-lg cursor-pointer ${
                isLight ? 'neu-btn-light text-slate-800' : 'neu-btn-dark text-slate-200'
              }`}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className={`xl:hidden border-t px-4 pt-4 pb-6 space-y-3 max-h-[calc(100vh-5rem)] overflow-y-auto ${
          isLight ? 'bg-white border-slate-200 text-slate-900' : 'bg-[#070a18] border-slate-800 text-slate-100'
        }`}>
          <button
            onClick={() => handleLinkClick('home')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Home
          </button>
          <button
            onClick={() => handleLinkClick('solutions')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Solutions
          </button>
          <button
            onClick={() => handleLinkClick('ai-company-builder')}
            className="block w-full text-left py-2 text-sm font-bold text-amber-500"
          >
            AI Company Builder
          </button>
          <button
            onClick={() => handleLinkClick('technology')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Technology & Proof
          </button>
          <button
            onClick={() => handleLinkClick('work')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Work & Case Studies
          </button>
          <button
            onClick={() => handleLinkClick('industries')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Industries
          </button>
          <button
            onClick={() => handleLinkClick('pharos')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Pharos: LightSpeed Insights
          </button>
          <button
            onClick={() => handleLinkClick('resources')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            Resources & AI Assessment
          </button>
          <button
            onClick={() => handleLinkClick('about')}
            className={`block w-full text-left py-2 text-sm font-semibold ${isLight ? 'text-slate-800 hover:text-amber-600' : 'text-slate-200 hover:text-amber-400'}`}
          >
            About Us
          </button>

          <div className={`pt-4 border-t flex flex-col gap-3 ${isLight ? 'border-slate-200' : 'border-slate-800'}`}>
            <button
              onClick={onToggleTheme}
              className={`w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-mono font-semibold border ${
                isLight ? 'bg-slate-100 border-slate-300 text-slate-800' : 'bg-slate-800 border-slate-700 text-slate-200'
              }`}
            >
              {isLight ? <Moon className="w-4 h-4 text-indigo-600" /> : <Sun className="w-4 h-4 text-amber-400" />}
              <span>Switch to {isLight ? 'Dark' : 'Light'} Mode</span>
            </button>

            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenContactModal('Start a Conversation');
              }}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-bold font-mono uppercase bg-amber-500 text-slate-950"
            >
              Start a Conversation
            </button>
          </div>
        </div>
      )}
    </header>
  );
};
