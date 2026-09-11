import React, { useState } from 'react';
import { Shield, Sparkles, Menu, X, ArrowUpRight, Globe, Layers, Sun, Moon, ArrowRight, FileCheck } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface FloatingNavProps {
  onRequestBriefing: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export const FloatingNav: React.FC<FloatingNavProps> = ({
  onRequestBriefing,
  theme = 'dark',
  onToggleTheme
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const isLight = theme === 'light';

  const navLinks = [
    { name: 'Model', href: '#operating-model' },
    { name: 'Core Offerings', href: '#capabilities' },
    { name: 'Diagnostic', href: '#diagnostic' },
    { name: 'Authority', href: '#authority' },
    { name: 'Pharos', href: '#publications' },
    { name: 'Templates', href: '#templates' },
    { name: 'Contact', href: '#contact' },
  ];

  const handleLinkClick = (href: string) => {
    setMobileMenuOpen(false);
    const el = document.querySelector(href);
    el?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header className="fixed top-4 sm:top-6 left-0 right-0 z-50 flex justify-center px-3 sm:px-4 pointer-events-none">
      <div className="w-full max-w-6xl pointer-events-auto">
        <div className={`flex items-center justify-between px-4 sm:px-6 py-2 sm:py-2.5 rounded-full transition-all duration-300 ${
          isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-100'
        }`}>

          {/* Brand Logo & Editorial Wordmark with Micro Acoustic Rosette */}
          <div className="flex items-center gap-3">
            <a
              href="#hero"
              onClick={(e) => {
                e.preventDefault();
                handleLinkClick('#hero');
              }}
              className="flex items-center gap-2.5 group cursor-pointer"
            >
              <div className="w-8 h-8 rounded-full border border-white/30 bg-gradient-to-tr from-orange-500 to-amber-500 flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-all">
                <Shield className="w-4 h-4" />
              </div>
              <div className="flex flex-col">
                <span className={`text-xs font-black tracking-widest font-sans flex items-center gap-1.5 ${
                  isLight ? 'text-slate-900' : 'text-zinc-100'
                }`}>
                  LightSpeed
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-orange-400 shadow-[0_0_6px_rgba(249,115,22,0.9)] animate-pulse" />
                </span>
                <span className="text-[9px] font-mono tracking-wider hidden sm:inline font-bold text-[#2D3748]">
                  MALAWI-ROOTED • GLOBAL CAPABILITY
                </span>
              </div>
            </a>

            {/* Subtle Hardware Micro-Vent Divider */}
            <div className="hidden md:block pl-2 border-l border-black/15 dark:border-white/10">
              <AcousticVentGrille variant="cluster" isLight={isLight} />
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className={`hidden lg:flex items-center gap-5 text-[11px] font-mono font-bold tracking-wider ${
            isLight ? 'text-slate-700' : 'text-zinc-300'
          }`}>
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleLinkClick(link.href);
                }}
                className={`transition-colors cursor-pointer py-1 px-1.5 rounded-md hover:bg-black/5 dark:hover:bg-white/5 ${
                  isLight ? 'hover:text-orange-600' : 'hover:text-orange-400'
                }`}
              >
                {link.name}
              </a>
            ))}
          </nav>

          {/* Right-aligned Actions & Briefing Conversion Pill */}
          <div className="flex items-center gap-2.5">
            {/* Tactile Rocker / Button for Theme Toggle */}
            {onToggleTheme && (
              <button
                type="button"
                onClick={onToggleTheme}
                className={`p-2 rounded-full transition-all cursor-pointer flex items-center justify-center ${
                  isLight
                    ? 'tactile-concave-btn-light text-slate-800'
                    : 'tactile-concave-btn-dark text-amber-400'
                }`}
                title={isLight ? 'Switch to Dark Studio Mode' : 'Switch to Anodized Light Mode'}
              >
                {isLight ? <Moon className="w-3.5 h-3.5" /> : <Sun className="w-3.5 h-3.5" />}
              </button>
            )}

            {/* Executive Conversion Action: Tactile Hardware Button */}
            <button
              onClick={() => onRequestBriefing()}
              className="flex items-center gap-2 px-4 py-2 rounded-full font-bold text-xs tracking-wider transition-all cursor-pointer shadow-md bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white shadow-orange-500/25 border-t border-white/30 active:scale-95"
            >
              <span>Request Briefing</span>
              <ArrowRight className="w-3 h-3" />
            </button>

            {/* Mobile Hamburger Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`lg:hidden p-2 rounded-full ${
                isLight ? 'tactile-concave-btn-light text-slate-800' : 'tactile-concave-btn-dark text-zinc-200'
              }`}
            >
              {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>

        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className={`mt-2 p-5 rounded-3xl border shadow-2xl lg:hidden flex flex-col gap-3 animate-in fade-in slide-in-from-top-2 ${
            isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-100'
          }`}>
            <div className={`flex flex-col gap-1 pb-3 border-b ${isLight ? 'border-slate-300' : 'border-white/10'}`}>
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  onClick={(e) => {
                    e.preventDefault();
                    handleLinkClick(link.href);
                  }}
                  className={`px-3 py-2 rounded-xl text-xs font-bold tracking-wider transition-colors ${
                    isLight
                      ? 'text-slate-800 hover:bg-orange-50 hover:text-orange-600'
                      : 'text-zinc-200 hover:bg-orange-500/10 hover:text-orange-400'
                  }`}
                >
                  {link.name}
                </a>
              ))}
            </div>
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onRequestBriefing();
              }}
              className="w-full py-3 rounded-full font-bold text-xs tracking-widest bg-gradient-to-r from-orange-500 to-amber-500 text-white flex items-center justify-center gap-2 shadow-md"
            >
              <span>Request Executive Briefing</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
