import React, { useEffect, useState } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { Shield, Menu, X, Sun, Moon, ArrowRight, ChevronDown } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface FloatingNavProps {
  onRequestBriefing: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

// Grouped nav: Capabilities exposes the hub + two deep-dive sub-pages so every
// route is reachable directly from the bar without bloating the top level.
interface SimpleLink { name: string; to: string }
interface GroupLink { name: string; children: SimpleLink[] }
type NavEntry = SimpleLink | GroupLink;

const navLinks: NavEntry[] = [
  {
    name: 'Capabilities',
    children: [
      { name: 'Overview', to: '/capabilities' },
      { name: 'Core Offerings', to: '/capabilities/offerings' },
      { name: 'Diagnostic', to: '/capabilities/diagnostic' },
    ],
  },
  { name: 'Industries', to: '/industries' },
  { name: 'Evidence', to: '/evidence' },
  { name: 'Engagement', to: '/engagement' },
  { name: 'Authority', to: '/about' },
  { name: 'Pharos', to: '/insights' },
  { name: 'Contact', to: '/contact' },
];

function isGroup(entry: NavEntry): entry is GroupLink {
  return 'children' in entry;
}

const NAV_BASE = 'transition-colors cursor-pointer py-1 px-1.5 rounded-md hover:bg-black/5 dark:hover:bg-white/5';
const NAV_ACTIVE = 'text-ls-red';
const NAV_IDLE = 'hover:text-ls-red';
const MOBILE_BASE = 'px-3 py-2 rounded-xl text-xs font-bold tracking-wider transition-colors';
const MOBILE_ACTIVE = 'bg-ls-red text-white';
const MOBILE_IDLE_LIGHT = 'text-slate-800 hover:bg-ls-red hover:text-ls-red';
const MOBILE_IDLE_DARK = 'text-zinc-200 hover:bg-ls-red/10 hover:text-ls-red';
const MOBILE_CHILD_BASE = 'ml-3 pl-3 border-l text-[10px]';

export const FloatingNav: React.FC<FloatingNavProps> = ({
  onRequestBriefing,
  theme = 'dark',
  onToggleTheme
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const isLight = theme === 'light';
  const { pathname } = useLocation();
  const capabilitiesActive = pathname === '/capabilities' || pathname.startsWith('/capabilities/');

  useEffect(() => {
    if (!mobileMenuOpen) return;
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setMobileMenuOpen(false);
    };
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', onKeyDown);
    return () => {
      document.body.style.overflow = prevOverflow;
      window.removeEventListener('keydown', onKeyDown);
    };
  }, [mobileMenuOpen]);

  return (
    <header className="fixed top-4 sm:top-6 left-0 right-0 z-50 flex justify-center px-3 sm:px-4 pointer-events-none">
      <div className="w-full max-w-6xl pointer-events-auto">
        <div className={`flex items-center justify-between px-4 sm:px-6 py-2 sm:py-2.5 rounded-full transition-all duration-300 ${
          isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-100'
        }`}>

          {/* Brand Logo */}
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-2.5 group cursor-pointer">
              <div className="w-8 h-8 rounded-full border border-white/30 bg-ls-red flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-all">
                <Shield className="w-4 h-4" />
              </div>
              <div className="flex flex-col">
                <span className={`text-xs font-black tracking-widest font-sans flex items-center gap-1.5 ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                  LightSpeed™
                  <span className="inline-block w-1.5 h-1.5 rounded-full bg-ls-red shadow-[0_0_6px_rgba(230,57,70,0.9)] animate-pulse" />
                </span>
                <span className="text-[9px] font-mono tracking-wider hidden sm:inline font-bold text-[#2D3748]">
                  MALAWI-ROOTED • GLOBAL CAPABILITY
                </span>
              </div>
            </Link>

            <div className="hidden md:block pl-2 border-l border-black/15 dark:border-white/10">
              <AcousticVentGrille variant="cluster" isLight={isLight} />
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className={`hidden lg:flex items-center gap-4 text-[11px] font-mono font-bold tracking-wider ${
            isLight ? 'text-slate-700' : 'text-zinc-300'
          }`}>
            {navLinks.map((entry) => {
              if (!isGroup(entry)) {
                return (
                  <NavLink
                    key={entry.name}
                    to={entry.to}
                    className={({ isActive }) =>
                      `relative ${NAV_BASE} ${isActive ? NAV_ACTIVE : NAV_IDLE}`
                    }
                  >
                    {({ isActive }) => (
                      <>
                        {entry.name}
                        {isActive && (
                          <span aria-hidden="true" className="absolute left-1.5 right-1.5 -bottom-0.5 h-0.5 rounded-full bg-ls-red shadow-[0_0_6px_rgba(230,57,70,0.8)]" />
                        )}
                      </>
                    )}
                  </NavLink>
                );
              }

              // Group dropdown: trigger (Link to hub) + hover/focus panel
              return (
                <div key={entry.name} className="relative group">
                  <Link
                    to={entry.children[0].to}
                    className={`relative flex items-center gap-1 ${NAV_BASE} ${
                      capabilitiesActive ? NAV_ACTIVE : NAV_IDLE
                    }`}
                  >
                    {entry.name}
                    <ChevronDown className="w-3 h-3 transition-transform group-focus-within:rotate-180" aria-hidden="true" />
                    {capabilitiesActive && (
                      <span aria-hidden="true" className="absolute left-1.5 right-1.5 -bottom-0.5 h-0.5 rounded-full bg-ls-red shadow-[0_0_6px_rgba(230,57,70,0.8)]" />
                    )}
                  </Link>
                  <div className="absolute top-full left-0 pt-2 z-50 invisible opacity-0 group-hover:visible group-hover:opacity-100 focus-within:visible focus-within:opacity-100 transition-opacity duration-150 pointer-events-none group-hover:pointer-events-auto group-focus-within:pointer-events-auto">
                    <div className={`min-w-[200px] p-2 rounded-2xl border shadow-2xl ${
                      isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-100'
                    }`}>
                      {entry.children.map((child) => (
                        <NavLink
                          key={child.to}
                          to={child.to}
                          className={({ isActive }) =>
                            `block px-3 py-2 rounded-xl text-[11px] font-bold tracking-wider transition-colors ${
                              isActive
                                ? 'bg-ls-red text-white'
                                : isLight
                                  ? 'text-slate-800 hover:bg-ls-red/10 hover:text-ls-red'
                                  : 'text-zinc-200 hover:bg-ls-red/10 hover:text-ls-red'
                            }`
                          }
                        >
                          {child.name}
                        </NavLink>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </nav>

          {/* Right Actions */}
          <div className="flex items-center gap-2.5">
            {onToggleTheme && (
              <button
                type="button"
                onClick={onToggleTheme}
                className={`p-2 rounded-full transition-all cursor-pointer flex items-center justify-center ${
                  isLight ? 'tactile-concave-btn-light text-slate-800' : 'tactile-concave-btn-dark text-ls-cyan'
                }`}
                title={isLight ? 'Switch to Dark Studio Mode' : 'Switch to Anodized Light Mode'}
              >
                {isLight ? <Moon className="w-3.5 h-3.5" /> : <Sun className="w-3.5 h-3.5" />}
              </button>
            )}

            <button
              onClick={() => onRequestBriefing()}
              className="flex items-center gap-2 px-4 py-2 rounded-full font-bold text-xs tracking-wider transition-all cursor-pointer shadow-md bg-ls-red hover:bg-ls-red text-white shadow-ls-red/25 border-t border-white/30 active:scale-95"
            >
              <span>Request Briefing</span>
              <ArrowRight className="w-3 h-3" />
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`lg:hidden p-2 rounded-full ${
                isLight ? 'tactile-concave-btn-light text-slate-800' : 'tactile-concave-btn-dark text-zinc-200'
              }`}
              aria-expanded={mobileMenuOpen}
              aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
            >
              {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </button>
          </div>

        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className={`mt-2 p-5 rounded-3xl border shadow-2xl lg:hidden flex flex-col gap-3 animate-in fade-in slide-in-from-top-2 ${
            isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-100'
          }`}>
            <div className={`flex flex-col gap-1 pb-3 border-b ${isLight ? 'border-slate-300' : 'border-white/10'}`}>
              {navLinks.map((entry) => {
                if (!isGroup(entry)) {
                  return (
                    <NavLink
                      key={entry.name}
                      to={entry.to}
                      onClick={() => setMobileMenuOpen(false)}
                      className={({ isActive }) =>
                        `${MOBILE_BASE} ${isActive ? MOBILE_ACTIVE : isLight ? MOBILE_IDLE_LIGHT : MOBILE_IDLE_DARK}`
                      }
                    >
                      {entry.name}
                    </NavLink>
                  );
                }

                // Group header + children
                return (
                  <div key={entry.name}>
                    <div className={`px-3 py-1.5 text-[10px] font-mono font-bold tracking-widest ${
                      isLight ? 'text-zinc-500' : 'text-zinc-500'
                    }`}>
                      {entry.name}
                    </div>
                    {entry.children.map((child) => (
                      <NavLink
                        key={child.to}
                        to={child.to}
                        onClick={() => setMobileMenuOpen(false)}
                        className={({ isActive }) =>
                          `${MOBILE_BASE} ${MOBILE_CHILD_BASE} ${isActive ? MOBILE_ACTIVE : isLight ? MOBILE_IDLE_LIGHT : MOBILE_IDLE_DARK}`
                        }
                      >
                        {child.name}
                      </NavLink>
                    ))}
                  </div>
                );
              })}
            </div>
            <button
              onClick={() => { setMobileMenuOpen(false); onRequestBriefing(); }}
              className="w-full py-3 rounded-full font-bold text-xs tracking-widest bg-ls-red text-white flex items-center justify-center gap-2 shadow-md"
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
