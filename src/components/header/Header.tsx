import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Logo } from '@lightspeed/design-system';
import { getPrimaryCTA } from '@lightspeed/data/ctas';
import { Menu, X, ChevronDown } from 'lucide-react';
import { useSite } from '../../site-context';

const SOLUTIONS_DROPDOWN = [
  { title: 'Workflow Collapsing', desc: 'Compress multi-step processes into instant execution', path: '/what-we-do' },
  { title: 'Agentic Automation', desc: 'Governed AI agents deployed across defined workflows', path: '/what-we-do' },
  { title: 'HAOMTGV Framework', desc: 'Explore Human, Agents, Orchestration, Memory, Tools & Governance', path: '/haomtgv' },
];

const RESEARCH_DROPDOWN = [
  { title: 'Pharos Insights', desc: 'Executive whitepapers & geostrategic analysis', path: '/insights' },
];

export const Header: React.FC = () => {
  const { theme } = useSite();
  const location = useLocation();
  const primaryCTA = getPrimaryCTA();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [solutionsOpen, setSolutionsOpen] = useState(false);
  const [researchOpen, setResearchOpen] = useState(false);

  const isDark = theme === 'dark';

  return (
    <header
      role="banner"
      className="sticky top-0 z-[100] w-full px-4 py-4 pointer-events-none"
    >
      <div className={`max-w-7xl mx-auto px-6 lg:px-10 py-3 flex items-center justify-between rounded-2xl border backdrop-blur-xl transition-all duration-300 pointer-events-auto ${
        isDark
          ? 'bg-[#0A0E27]/75 border-[#00BFFF]/20 shadow-2xl shadow-black/60'
          : 'bg-white/80 border-slate-200 shadow-xl shadow-ls-navy/5'
      }`}>

        {/* Brand Logo */}
        <Link
          to="/"
          className="header__logo shrink-0"
          aria-label="LightSpeed Holdings - Home"
        >
          <Logo variant="full" size="md" />
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center gap-8 text-xs uppercase tracking-widest font-bold" aria-label="Primary">
          <Link
            to="/"
            className={`transition-colors py-1 ${
              location.pathname === '/' ? 'text-[#00BFFF] font-bold' : 'text-ls-navy/70 dark:text-white/70 hover:text-[#00BFFF]'
            }`}
          >
            Home
          </Link>

          <Link
            to="/what-we-do"
            className={`transition-colors py-1 ${
              location.pathname === '/what-we-do' ? 'text-[#00BFFF] font-bold' : 'text-ls-navy/70 dark:text-white/70 hover:text-[#00BFFF]'
            }`}
          >
            What We Do
          </Link>

          {/* Solutions Mega Menu Dropdown */}
          <div className="relative" onMouseEnter={() => setSolutionsOpen(true)} onMouseLeave={() => setSolutionsOpen(false)}>
            <button
              onClick={() => setSolutionsOpen(!solutionsOpen)}
              className="flex items-center gap-1.5 text-ls-navy/70 dark:text-white/70 hover:text-[#00BFFF] py-1 transition-colors uppercase tracking-widest"
            >
              <span>Solutions & Architecture</span>
              <ChevronDown className="w-3.5 h-3.5" />
            </button>

            {solutionsOpen && (
              <div className="absolute top-full left-0 w-80 bg-[#0A0E27]/95 backdrop-blur-2xl rounded-xl shadow-2xl border border-[#00BFFF]/20 p-4 grid gap-3 animate-in fade-in slide-in-from-top-2 duration-200">
                {SOLUTIONS_DROPDOWN.map((item, i) => (
                  <Link
                    key={i}
                    to={item.path}
                    onClick={() => setSolutionsOpen(false)}
                    className="p-3 rounded-lg hover:bg-[#00BFFF]/10 transition-colors group block"
                  >
                    <div className="text-xs font-bold text-white group-hover:text-[#00BFFF] flex items-center justify-between uppercase tracking-wider">
                      <span>{item.title}</span>
                      <span>→</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5 normal-case font-normal">{item.desc}</p>
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* Research Mega Menu Dropdown */}
          <div className="relative" onMouseEnter={() => setResearchOpen(true)} onMouseLeave={() => setResearchOpen(false)}>
            <button
              onClick={() => setResearchOpen(!researchOpen)}
              className="flex items-center gap-1.5 text-ls-navy/70 dark:text-white/70 hover:text-[#00BFFF] py-1 transition-colors uppercase tracking-widest"
            >
              <span>Pharos Insights</span>
              <ChevronDown className="w-3.5 h-3.5" />
            </button>

            {researchOpen && (
              <div className="absolute top-full left-0 w-80 bg-[#0A0E27]/95 backdrop-blur-2xl rounded-xl shadow-2xl border border-[#00BFFF]/20 p-4 grid gap-3 animate-in fade-in slide-in-from-top-2 duration-200">
                {RESEARCH_DROPDOWN.map((item, i) => (
                  <Link
                    key={i}
                    to={item.path}
                    onClick={() => setResearchOpen(false)}
                    className="p-3 rounded-lg hover:bg-[#00BFFF]/10 transition-colors group block"
                  >
                    <div className="text-xs font-bold text-white group-hover:text-[#00BFFF] flex items-center justify-between uppercase tracking-wider">
                      <span>{item.title}</span>
                      <span>→</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5 normal-case font-normal">{item.desc}</p>
                  </Link>
                ))}
              </div>
            )}
          </div>

          <Link
            to="/about"
            className={`transition-colors py-1 ${
              location.pathname === '/about' ? 'text-[#00BFFF] font-bold' : 'text-ls-navy/70 dark:text-white/70 hover:text-[#00BFFF]'
            }`}
          >
            About
          </Link>

          <Link
            to="/contact"
            className={`transition-colors py-1 ${
              location.pathname === '/contact' ? 'text-[#00BFFF] font-bold' : 'text-ls-navy/70 dark:text-white/70 hover:text-[#00BFFF]'
            }`}
          >
            Contact
          </Link>
        </nav>

        {/* CTA Button & Mobile Toggle */}
        <div className="flex items-center gap-4">
          <Link
            to={primaryCTA.href}
            className="hidden sm:inline-flex items-center justify-center px-5 py-2.5 font-bold text-xs text-white bg-[#E63946] hover:bg-[#d62837] rounded-lg transition-colors shadow-lg shadow-red-600/30 uppercase tracking-wider"
          >
            {primaryCTA.label}
          </Link>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 text-slate-300 hover:text-white"
            aria-label="Toggle mobile menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

      </div>

      {/* Mobile Menu Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden absolute top-full left-4 right-4 mt-2 bg-white/95 dark:bg-slate-950/95 backdrop-blur-2xl shadow-2xl rounded-2xl border border-slate-200 dark:border-white/10 p-6 space-y-4 animate-in slide-in-from-top-2 duration-200 pointer-events-auto">
          <Link
            to="/"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-ls-navy/80 dark:text-slate-200 hover:text-ls-cyan"
          >
            Home
          </Link>
          <Link
            to="/what-we-do"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-ls-navy/80 dark:text-slate-200 hover:text-ls-cyan"
          >
            What We Do
          </Link>
          <Link
            to="/haomtgv"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-ls-navy/80 dark:text-slate-200 hover:text-ls-cyan"
          >
            HAOMTGV Framework
          </Link>
          <Link
            to="/insights"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-ls-navy/80 dark:text-slate-200 hover:text-ls-cyan"
          >
            Pharos Insights
          </Link>
          <Link
            to="/about"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-ls-navy/80 dark:text-slate-200 hover:text-ls-cyan"
          >
            About
          </Link>
          <Link
            to="/contact"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-ls-navy/80 dark:text-slate-200 hover:text-ls-cyan"
          >
            Contact
          </Link>

          <div className="pt-4">
            <Link
              to={primaryCTA.href}
              onClick={() => setMobileMenuOpen(false)}
              className="w-full py-3 bg-ls-red text-white rounded-xl font-bold text-sm block text-center shadow-lg shadow-ls-red/30"
            >
              {primaryCTA.label}
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
