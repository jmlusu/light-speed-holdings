import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Sun, Moon } from 'lucide-react';
import { PRIMARY_CTA_LABEL } from '../data/ctas';
import Logo from '@/components/site/Logo.tsx';

interface FloatingNavProps {
  onRequestBriefing: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

const NAV_LINKS = [
  { name: 'Home', href: '/' },
  { name: 'AI Company Builder', href: '/ai-company-builder' },
  { name: 'Solutions', href: '/solutions' },
  { name: 'Use Cases', href: '/use-cases' },
  { name: 'Sectors', href: '/sectors' },
  { name: 'Insights', href: '/insights' },
  { name: 'About', href: '/about' },
  { name: 'Contact', href: '/contact' },
];

export const FloatingNav: React.FC<FloatingNavProps> = ({
  onRequestBriefing,
  theme = 'dark',
  onToggleTheme,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [showGovernance, setShowGovernance] = useState(false);
  const isLight = theme === 'light';

  return (
    <header className="fixed top-4 sm:top-6 left-0 right-0 z-50 flex justify-center px-3 sm:px-4 pointer-events-none">
      <div className="w-full max-w-6xl pointer-events-auto">
        <div
          className={`flex items-center justify-between px-4 sm:px-6 py-2.5 rounded-full transition-all duration-300 shadow-xl backdrop-blur-xl border ${
            isLight
              ? 'bg-ls-white/95 border-ls-grey-dark/30 text-ls-navy shadow-lg'
              : 'bg-ls-navy/95 border-ls-white/15 text-ls-white shadow-2xl'
          }`}
        >
          <div className="flex items-center gap-3">
            <Link to="/" onClick={() => setMobileMenuOpen(false)} className="flex items-center gap-2.5 group cursor-pointer">
              <Logo size={32} showText theme={theme} instance="first" />
            </Link>
          </div>

          <nav className="hidden lg:flex items-center gap-4 text-xs font-body font-bold tracking-wider">
            {NAV_LINKS.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`ripple-on transition-colors cursor-pointer py-1 px-2 rounded-md ${
                  isLight ? 'text-ls-navy/80 hover:bg-ls-navy/5 hover:text-ls-red' : 'text-ls-white/80 hover:bg-ls-white/5 hover:text-ls-red'
                }`}
              >
                {link.name}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2.5">
            {onToggleTheme && (
              <button
                type="button"
                onClick={onToggleTheme}
                className={`p-2 rounded-full transition-all cursor-pointer flex items-center justify-center ${
                  isLight ? 'hover:bg-ls-navy/10 text-ls-navy' : 'hover:bg-ls-white/10 text-ls-white'
                }`}
                title={isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
                aria-label={isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
              >
                {isLight ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
              </button>
            )}
            <button
              onClick={() => {
                window.location.hash = window.location.hash ? window.location.hash.replace(/^#/, '') : '#governance';
                if (window.location.hash === '#governance') {
                  setShowGovernance(true);
                } else {
                  setShowGovernance(false);
                }
              }}
              className={`p-2 rounded-full transition-all cursor-pointer flex items-center justify-center ${
                isLight ? 'hover:bg-ls-navy/10 text-ls-navy' : 'hover:bg-ls-white/10 text-ls-white'
              }`}
              title="Governance framework"
              aria-label="Governance framework"
            >
              <Sun className="w-4 h-4" />
            </button>
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onRequestBriefing(PRIMARY_CTA_LABEL);
              }}
              className="ripple-on flex items-center gap-2 px-4 py-2 rounded-full font-bold text-xs tracking-wider transition-all cursor-pointer shadow-md bg-ls-red hover:bg-ls-red/90 text-ls-white shadow-ls-red/25 border-t border-ls-white/20 active:scale-95"
            >
              <span>{PRIMARY_CTA_LABEL}</span>
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`lg:hidden p-2 rounded-full ${
                isLight ? 'hover:bg-ls-navy/10 text-ls-navy' : 'hover:bg-ls-white/10 text-ls-white'
              }`}
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>
    </header>
    {showGovernance && (
      <div
        className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm flex items-center justify-center p-6"
        onClick={() => setShowGovernance(false)}
      >
        <div className="bg-ls-navy/95 rounded-lg p-8 max-w-2xl w-full border-ls-white/10 shadow-2xl">
          <h2 className="text-ls-navy text-2xl font-bold mb-6">HAOMTGV Governance Framework</h2>
          <p className="text-ls-white/80 mb-8">
            The HAOMTGV framework is a 7-layer governance model for AI-native organizations.
          </p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3>H - Human CEOs</h3>
              <p className="text-ls-white/60 text-sm">Human-led strategy and oversight</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: Who owns the final decision for each agent action? Proof: 5-tier HITL approval matrix with SHA-256 audit trails (CLAIM: registry.metrics)</p>
            </div>
            <div>
              <h3>A - Agents</h3>
              <p className="text-ls-white/60 text-sm">90 specialized AI agents</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: What canonical tools can each agent use? Proof: 7-tool vocabulary (read only: read, edit, bash, task, webfetch, code-structure, jq)</p>
            </div>
            <div>
              <h3>O - Operating Model</h3>
              <p className="text-ls-white/60 text-sm">5-tier HITL approval matrix</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: How are the 4 governance gates (G1–G4) enforced? Proof: Every engagement clears Contract, DPA, Compliance, Security before work begins (CLAIM: registry.solutions)</p>
            </div>
            <div>
              <h3>M - Memory</h3>
              <p className="text-ls-white/60 text-sm">Shared semantic memory system</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: How is cross-agent memory persisted and queried? Proof: SQLite trajectory database with structured evidence logs</p>
            </div>
            <div>
              <h3>T - Tools</h3>
              <p className="text-ls-white/60 text-sm">Canonical 7-tool vocabulary</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: Which of the 7 canonical tools are permitted per agent tier? Proof: AgentRegistry validates only approved tools; code-structure and jq for JSON filtering</p>
            </div>
            <div>
              <h3>G - Governance</h3>
              <p className="text-ls-white/60 text-sm">5-tier HITL + RBAC dashboard</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: What are the 5 HITL gates and 4 governance gates (G1–G4)? Proof: ApprovalGate runs expiry sweep, transitions expired PENDING to EXPIRED (CLAIM: registry.agents)</p>
            </div>
            <div>
              <h3>V - Visuals</h3>
              <p className="text-ls-white/60 text-sm">Micro-illustrations & Type K glyphs</p>
              <p className="text-ls-xs text-ls-white/40 mt-2">Design Q: How are brand tokens (navy #070A40, red #DC3641, cyan #00BFFF) enforced? Proof: ls-artifact-qa visual QA + brand guidelines compliance</p>
            </div>
          </div>
          <button
            onClick={() => setShowGovernance(false)}
            className="mt-6 w-full py-3 rounded-full bg-ls-red text-ls-white font-bold hover:bg-ls-red/90 transition-all"
          >
            Close Governance Framework
          </button>
        </div>
      </div>
    )}
   );
};

export default FloatingNav;
