import React, { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { Shield, Menu, X, Sun, Moon, ArrowRight, ChevronDown } from 'lucide-react';
import { AcousticVentGrille } from './TactileHardwareElements';

interface FloatingNavProps {
  onRequestBriefing: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

// Primary site navigation per the Lightspeed sitemap. Solutions and Industries
// expose their hub + deep-dive sub-pages via dropdowns so every route is
// reachable directly from the bar without bloating the top level.
interface SimpleLink { name: string; to: string }
interface GroupLink { name: string; children: SimpleLink[] }
type NavEntry = SimpleLink | GroupLink;

const navLinks: NavEntry[] = [
  {
    name: 'Solutions',
    children: [
      { name: 'Overview', to: '/solutions' },
      { name: 'Agentic AI', to: '/solutions/agentic-ai' },
      { name: 'Digital Transformation', to: '/solutions/digital-transformation' },
      { name: 'Data & Intelligence', to: '/solutions/data-intelligence' },
      { name: 'Intelligent Automation', to: '/solutions/automation' },
      { name: 'Strategy & Advisory', to: '/solutions/strategy-advisory' },
      { name: 'AI Governance & Policy', to: '/technology#governance' },
    ],
  },
  {
    name: 'Industries',
    children: [
      { name: 'Overview', to: '/industries' },
      { name: 'Government', to: '/industries/government' },
      { name: 'Development & Donor', to: '/industries/development' },
      { name: 'Financial Services', to: '/industries/financial-services' },
      { name: 'Healthcare', to: '/industries/healthcare' },
      { name: 'Agriculture', to: '/industries/agriculture' },
    ],
  },
  { name: 'AI Company Builder', to: '/ai-company-builder' },
  { name: 'Technology', to: '/technology' },
  { name: 'Work', to: '/work' },
  { name: 'Insights', to: '/insights' },
  { name: 'About', to: '/about' },
];

const GROUP_PREFIXES: Record<string, string> = {
  Solutions: '/solutions',
  Industries: '/industries',
};

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
  const [scrolled, setScrolled] = useState(false);
  const scrolledRef = useRef(false);
  const progressRef = useRef<HTMLDivElement>(null);
  const isLight = theme === 'light';
  const { pathname } = useLocation();

  const groupActive = (entry: NavEntry) => {
    if (!isGroup(entry)) return false;
    const prefix = GROUP_PREFIXES[entry.name];
    return prefix ? pathname === prefix || pathname.startsWith(`${prefix}/`) : false;
  };

  // Shrink the pill once the page is scrolled and paint a scroll-progress bar
  // along its bottom edge. Progress updates write straight to the DOM (ref) so
  // continuous scroll doesn't cause re-renders; only the threshold flip does.
  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY;
      const pastThreshold = y > 24;
      if (pastThreshold !== scrolledRef.current) {
        scrolledRef.current = pastThreshold;
        setScrolled(pastThreshold);
      }
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const bar = progressRef.current;
      if (bar) {
        bar.style.transform = `scaleX(${max > 0 ? Math.min(Math.max(y / max, 0), 1) : 0})`;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

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
        <div className={`relative flex items-center justify-between px-4 sm:px-6 rounded-full transition-all duration-300 ${
          scrolled ? 'py-1.5 sm:py-2 shadow-2xl' : 'py-2 sm:py-2.5'
        } ${
          isLight ? 'hardware-chassis-light text-slate-800' : 'hardware-chassis-dark text-zinc-100'
        }`}>

          {/* Scroll progress bar */}
          <div
            ref={progressRef}
            aria-hidden="true"
            className="absolute bottom-0.5 left-2 right-2 h-0.5 origin-left scale-x-0 rounded-full bg-ls-cyan/80"
          />

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
                  LIGHTSPEED HOLDINGS LIMITED
                </span>
              </div>
            </Link>

            <div className="hidden md:block pl-2 border-l border-black/15 dark:border-white/10">
              <AcousticVentGrille variant="cluster" isLight={isLight} />
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className={`hidden lg:flex items-center gap-2.5 xl:gap-3.5 text-[11px] font-mono font-bold tracking-wider ${
            isLight ? 'text-slate-700' : 'text-zinc-300'
          }`}>
            {navLinks.map((entry) => {
              if (!isGroup(entry)) {
                return (
                  <NavLink
                    key={entry.name}
                    to={entry.to}
                    className={({ isActive }) =>
                      `relative shrink-0 ${NAV_BASE} ${isActive ? NAV_ACTIVE : NAV_IDLE}`
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
              const active = groupActive(entry);
              return (
                <div key={entry.name} className="relative group shrink-0">
                  <Link
                    to={entry.children[0].to}
                    className={`relative flex items-center gap-1 ${NAV_BASE} ${
                      active ? NAV_ACTIVE : NAV_IDLE
                    }`}
                  >
                    {entry.name}
                    <ChevronDown className="w-3 h-3 transition-transform group-focus-within:rotate-180" aria-hidden="true" />
                    {active && (
                      <span aria-hidden="true" className="absolute left-1.5 right-1.5 -bottom-0.5 h-0.5 rounded-full bg-ls-red shadow-[0_0_6px_rgba(230,57,70,0.8)]" />
                    )}
                  </Link>
                  <div className="absolute top-full left-0 pt-2 z-50 invisible opacity-0 group-hover:visible group-hover:opacity-100 focus-within:visible focus-within:opacity-100 transition-opacity duration-150 pointer-events-none group-hover:pointer-events-auto group-focus-within:pointer-events-auto">
                    <div className={`min-w-[220px] p-2 rounded-2xl border shadow-2xl ${
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

            <Link
              to="/contact"
              className="flex items-center gap-2 px-4 py-2 rounded-full font-bold text-xs tracking-wider transition-all cursor-pointer shadow-md bg-ls-red hover:bg-ls-red text-white shadow-ls-red/25 border-t border-white/30 active:scale-95"
            >
              <span>Start a Conversation</span>
              <ArrowRight className="w-3 h-3" />
            </Link>

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
            <Link
              to="/contact"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full py-3 rounded-full font-bold text-xs tracking-widest bg-ls-red text-white flex items-center justify-center gap-2 shadow-md"
            >
              <span>Start a Conversation</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};

export default FloatingNav;
