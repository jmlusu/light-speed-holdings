import React, { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Sun, Moon } from 'lucide-react';
import { PRIMARY_CTA_LABEL, PRIMARY_CTA_TO } from '../data/ctas';

interface FloatingNavProps {
  onRequestBriefing?: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

export const NAV_LINKS = [
  { name: 'Home', href: '/' },
  { name: 'What We Do', href: '/what-we-do' },
  { name: 'Pharos', href: '/insights' },
  { name: 'Who We Are', href: '/about' },
] as const;

const isActivePath = (pathname: string, href: string): boolean =>
  href === '/' ? pathname === '/' : pathname === href || pathname.startsWith(`${href}/`);

export const FloatingNav: React.FC<FloatingNavProps> = ({
  theme = 'dark',
  onToggleTheme,
}) => {
  const isLight = theme === 'light';
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { pathname } = useLocation();
  const toggleRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mobileMenuOpen) return;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMobileMenuOpen(false);
        toggleRef.current?.focus();
        return;
      }
      if (event.key !== 'Tab') return;

      const panel = panelRef.current;
      if (!panel) return;
      const focusables = Array.from(
        panel.querySelectorAll<HTMLElement>('a[href], button:not([disabled])'),
      );
      if (focusables.length === 0) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      const active = document.activeElement as HTMLElement | null;
      const inside = active ? panel.contains(active) : false;

      if (event.shiftKey) {
        if (!inside || active === first) {
          event.preventDefault();
          last.focus();
        }
      } else if (!inside || active === last) {
        event.preventDefault();
        first.focus();
      }
    };

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [mobileMenuOpen]);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 w-full pointer-events-none">
        {/* Transparent Glassmorphism Navigation Bar */}
        <div className={`w-full backdrop-blur-xl border-b transition-all duration-300 pointer-events-auto ${
          isLight
            ? 'bg-white/50 border-slate-200/60 text-ls-navy shadow-[0_4px_30px_rgba(7,10,64,0.06)]'
            : 'bg-[#070A40]/45 border-white/10 text-white shadow-[0_8px_32px_rgba(0,0,0,0.5)]'
        }`}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center">
              <Link
                to="/"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 group cursor-pointer border-b border-transparent"
                aria-label="LightSpeed Holdings Limited™ Home"
              >
                <img
                  src="/brand/logo/logo-favicon-transparent.png"
                  alt="LightSpeed Holdings Limited™"
                  className="w-7 h-7 object-contain shrink-0 filter drop-shadow-[0_0_8px_rgba(0,191,255,0.4)]"
                  data-ls-image-type="brand-mark"
                />
                <span className={`font-extrabold tracking-widest text-xs sm:text-sm uppercase font-sans ${
                  isLight ? 'text-ls-navy' : 'text-white'
                }`}>
                  LIGHTSPEED <span className="text-ls-cyan">HOLDINGS</span>
                </span>
              </Link>
            </div>

            {/* Desktop Navigation Links */}
            <nav aria-label="Primary" className="hidden lg:flex items-center gap-8 text-xs font-bold tracking-widest uppercase font-sans">
              {NAV_LINKS.map((link) => {
                const active = isActivePath(pathname, link.href);
                return (
                  <Link
                    key={link.name}
                    to={link.href}
                    onClick={() => setMobileMenuOpen(false)}
                    aria-current={active ? 'page' : undefined}
                    className={`relative py-1 transition-all cursor-pointer border-b-2 ${
                      active
                        ? 'border-ls-cyan text-ls-cyan font-extrabold'
                        : isLight
                        ? 'border-transparent text-slate-700 hover:text-ls-red hover:border-ls-red/50'
                        : 'border-transparent text-white/85 hover:text-ls-cyan hover:border-ls-cyan/50'
                    }`}
                  >
                    {link.name}
                  </Link>
                );
              })}
            </nav>

            {/* Actions: Theme Toggle + Pill Capsule Action Button */}
            <div className="flex items-center gap-3">
              {onToggleTheme && (
                <button
                  type="button"
                  onClick={onToggleTheme}
                  className={`w-8 h-8 rounded-full border transition-all cursor-pointer flex items-center justify-center backdrop-blur-md ${
                    isLight
                      ? 'border-slate-300/80 bg-slate-200/50 text-ls-navy hover:bg-ls-navy hover:text-white'
                      : 'border-white/25 bg-white/10 text-white hover:bg-ls-cyan hover:text-ls-navy'
                  }`}
                  title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
                  aria-label={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
                >
                  {theme === 'light' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
                </button>
              )}

              <Link
                to={PRIMARY_CTA_TO}
                onClick={() => setMobileMenuOpen(false)}
                className={`px-5 py-2.5 font-black text-xs tracking-widest transition-all duration-300 cursor-pointer flex items-center justify-center gap-1.5 rounded-full uppercase active:scale-95 text-[#9CA3AF] ${
                  isLight
                    ? 'bg-ls-navy hover:bg-ls-red hover:text-white shadow-md shadow-ls-navy/20 border border-ls-navy/20'
                    : 'bg-[#070A40] border border-white/20 hover:border-ls-cyan hover:text-ls-cyan shadow-[0_0_22px_rgba(0,191,255,0.25)]'
                }`}
              >
                <span className="font-black tracking-widest text-[#9CA3AF]">{PRIMARY_CTA_LABEL}</span>
              </Link>

              <button
                ref={toggleRef}
                type="button"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className={`lg:hidden w-8 h-8 rounded-lg flex items-center justify-center border transition-all cursor-pointer ${
                  isLight
                    ? 'border-slate-300 bg-slate-200/60 text-ls-navy hover:bg-ls-navy hover:text-white'
                    : 'border-white/20 bg-white/10 text-white hover:bg-ls-cyan hover:text-ls-navy'
                }`}
                aria-label="Toggle navigation menu"
                aria-expanded={mobileMenuOpen}
                aria-controls="mobile-nav"
              >
                {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Dropdown */}
      {mobileMenuOpen && (
        <div className={`fixed inset-x-0 top-[76px] z-40 lg:hidden pointer-events-auto border-b-2 p-5 shadow-2xl backdrop-blur-xl transition-all ${
          isLight
            ? 'bg-white/95 text-ls-navy border-slate-300 shadow-[0_12px_30px_rgba(7,10,64,0.15)]'
            : 'bg-[#070A40] text-white border-ls-cyan shadow-[0_12px_30px_rgba(0,0,0,0.8)]'
        }`}>
          <div id="mobile-nav" ref={panelRef} className="max-w-7xl mx-auto flex flex-col space-y-2">
            <nav aria-label="Primary mobile" className="flex flex-col space-y-1">
              {NAV_LINKS.map((link) => {
                const active = isActivePath(pathname, link.href);
                return (
                  <Link
                    key={link.name}
                    to={link.href}
                    onClick={() => setMobileMenuOpen(false)}
                    aria-current={active ? 'page' : undefined}
                    className={`px-4 py-3 text-sm font-bold tracking-wider uppercase transition-colors border-l-2 rounded-r-lg ${
                      active
                        ? isLight
                          ? 'border-ls-red bg-red-50 text-ls-red font-extrabold'
                          : 'border-ls-red bg-white/10 text-ls-cyan'
                        : isLight
                          ? 'border-transparent text-ls-navy hover:bg-slate-100 hover:text-ls-red'
                          : 'border-transparent text-white hover:border-ls-cyan hover:bg-white/5 hover:text-ls-cyan'
                    }`}
                  >
                    {link.name}
                  </Link>
                );
              })}
              <div className={`pt-3 mt-2 border-t ${isLight ? 'border-slate-200' : 'border-white/15'}`}>
                <Link
                  to={PRIMARY_CTA_TO}
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full justify-center px-4 py-3 font-bold text-xs tracking-widest transition-colors cursor-pointer flex items-center gap-1.5 bg-ls-red text-white hover:bg-ls-red/90 border border-ls-red uppercase text-center rounded-xl shadow-md"
                >
                  <span>{PRIMARY_CTA_LABEL}</span>
                </Link>
              </div>
            </nav>
          </div>
        </div>
      )}
    </>
  );
};

export default FloatingNav;
