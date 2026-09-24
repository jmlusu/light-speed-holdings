import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Shield, Menu, X, Sun, Moon, ArrowRight } from 'lucide-react';

interface FloatingNavProps {
  onRequestBriefing: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export const FloatingNav: React.FC<FloatingNavProps> = ({
  onRequestBriefing,
  theme = 'dark',
  onToggleTheme,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const isLight = theme === 'light';

  const navLinks = [
    { name: 'What We Do', href: '/what-we-do' },
    { name: 'Proof', href: '/proof' },
    { name: 'Technology', href: '/technology' },
    { name: 'Ask LightSpeed', href: '/ask' },
    { name: 'Insights', href: '/insights' },
    { name: 'About', href: '/about' },
  ];

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
          {/* Brand Logo & Editorial Wordmark */}
          <div className="flex items-center gap-3">
            <Link
              to="/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2.5 group cursor-pointer"
            >
              <div className="w-8 h-8 rounded-full border border-ls-white/30 bg-ls-red flex items-center justify-center text-ls-white shadow-md group-hover:scale-105 transition-all">
                <Shield className="w-4 h-4" />
              </div>
              <div className="flex flex-col">
                <span
                  className={`text-xs font-black tracking-widest font-sans flex items-center gap-1.5 ${
                    isLight ? 'text-ls-navy' : 'text-ls-white'
                  }`}
                >
                  LightSpeed
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-ls-red shadow-[0_0_6px_rgba(230,57,70,0.9)] animate-pulse" />
                </span>
                <span
                  className={`text-[9px] font-body tracking-wider hidden sm:inline font-bold ${
                    isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
                  }`}
                >
                  MALAWI &amp; SADC AI SYSTEMS
                </span>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation Links */}
          <nav
            className={`hidden lg:flex items-center gap-6 text-xs font-body font-bold tracking-wider ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}
          >
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                className={`ripple-on transition-colors cursor-pointer py-1 px-2 rounded-md hover:text-ls-red ${
                  isLight ? 'text-ls-navy/80 hover:bg-ls-navy/5' : 'text-ls-white/80 hover:bg-ls-white/5'
                }`}
              >
                {link.name}
              </Link>
            ))}
          </nav>

          {/* Right-aligned Actions & Briefing Conversion Pill */}
          <div className="flex items-center gap-2.5">
            {/* Theme Toggle Button */}
            {onToggleTheme && (
              <button
                type="button"
                onClick={onToggleTheme}
                className={`p-2 rounded-full transition-all cursor-pointer flex items-center justify-center ${
                  isLight
                    ? 'hover:bg-ls-navy/10 text-ls-navy'
                    : 'hover:bg-ls-white/10 text-ls-white'
                }`}
                title={isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
                aria-label={isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
              >
                {isLight ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
              </button>
            )}

            {/* Executive Conversion Action: Singular Primary CTA */}
            <button
              onClick={() => onRequestBriefing('Book an Executive Briefing')}
              className="ripple-on flex items-center gap-2 px-4 sm:px-5 py-2 rounded-full font-bold text-xs tracking-wider transition-all cursor-pointer shadow-md bg-ls-red hover:bg-ls-red/90 text-ls-white shadow-ls-red/25 border-t border-ls-white/20 active:scale-95"
            >
              <span>Book an Executive Briefing</span>
              <ArrowRight className="w-3.5 h-3.5 text-ls-white" />
            </button>

            {/* Mobile Hamburger Toggle */}
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

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div
            className={`mt-2 p-5 rounded-3xl border shadow-2xl lg:hidden flex flex-col gap-2 animate-in fade-in slide-in-from-top-2 ${
              isLight
                ? 'bg-ls-white/95 border-ls-grey-dark/30 text-ls-navy'
                : 'bg-ls-navy/95 border-ls-white/15 text-ls-white'
            }`}
          >
            <div
              className={`flex flex-col gap-1 pb-3 border-b ${
                isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'
              }`}
            >
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  to={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`ripple-on px-3 py-2.5 rounded-xl text-xs font-bold tracking-wider transition-colors ${
                    isLight
                      ? 'text-ls-navy hover:bg-ls-navy/5 hover:text-ls-red'
                      : 'text-ls-white hover:bg-ls-white/5 hover:text-ls-red'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onRequestBriefing('Book an Executive Briefing');
              }}
              className="ripple-on w-full py-3 rounded-full font-bold text-xs tracking-widest bg-ls-red text-ls-white flex items-center justify-center gap-2 shadow-md hover:bg-ls-red/90 transition-all"
            >
              <span>Book an Executive Briefing</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default FloatingNav;
