import React, { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Sun, Moon } from 'lucide-react';
import { PRIMARY_CTA_LABEL, PRIMARY_CTA_TO } from '../data/ctas';
import Logo from '@/components/site/Logo.tsx';

interface FloatingNavProps {
  /** Retained for hero and in-page briefing CTAs; the nav CTA is now a real /contact link (D2). */
  onRequestBriefing?: (summary?: string) => void;
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
}

/** SPEC §8 primary navigation: eight items, Contact lives in the CTA button. */
export const NAV_LINKS = [
  { name: 'Home', href: '/' },
  { name: 'What We Do', href: '/what-we-do' },
  { name: 'AI Company Builder', href: '/ai-company-builder' },
  { name: 'Solutions', href: '/solutions' },
  { name: 'Use Cases', href: '/use-cases' },
  { name: 'Sectors', href: '/sectors' },
  { name: 'Insights', href: '/insights' },
  { name: 'About', href: '/about' },
] as const;

const isActivePath = (pathname: string, href: string): boolean =>
  href === '/' ? pathname === '/' : pathname === href || pathname.startsWith(`${href}/`);

export const FloatingNav: React.FC<FloatingNavProps> = ({
  theme = 'dark',
  onToggleTheme,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { pathname } = useLocation();
  const isLight = theme === 'light';
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

            <nav aria-label="Primary" className="hidden lg:flex items-center gap-2 xl:gap-4 text-[11px] xl:text-xs font-body font-bold tracking-wider">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.name}
                  to={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  aria-current={isActivePath(pathname, link.href) ? 'page' : undefined}
                  className={`ripple-on transition-colors cursor-pointer py-1 px-1.5 xl:px-2 rounded-md ${
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
              <Link
                to={PRIMARY_CTA_TO}
                onClick={() => setMobileMenuOpen(false)}
                className="ripple-on flex items-center gap-2 px-3 xl:px-4 py-2 rounded-full font-bold text-[11px] xl:text-xs tracking-wider transition-all cursor-pointer shadow-md bg-ls-red hover:bg-ls-red/90 text-ls-white shadow-ls-red/25 border-t border-ls-white/20 active:scale-95"
              >
                <span>{PRIMARY_CTA_LABEL}</span>
              </Link>
              <button
                ref={toggleRef}
                type="button"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className={`lg:hidden p-2 rounded-full ${
                  isLight ? 'hover:bg-ls-navy/10 text-ls-navy' : 'hover:bg-ls-white/10 text-ls-white'
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
      {mobileMenuOpen && (
        <div className="fixed inset-x-0 top-[4.5rem] z-40 px-3 sm:px-4 lg:hidden pointer-events-none">
          <div
            id="mobile-nav"
            ref={panelRef}
            className={`w-full max-w-6xl mx-auto rounded-2xl border shadow-2xl backdrop-blur-xl pointer-events-auto overflow-hidden ${
              isLight
                ? 'bg-ls-white/95 border-ls-grey-dark/30 text-ls-navy'
                : 'bg-ls-navy/95 border-ls-white/15 text-ls-white'
            }`}
          >
            <nav aria-label="Primary mobile" className="flex flex-col py-2">
              {NAV_LINKS.map((link) => (
                <Link
                  key={link.name}
                  to={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  aria-current={isActivePath(pathname, link.href) ? 'page' : undefined}
                  className={`px-5 py-3 text-sm font-body font-bold tracking-wider transition-colors ${
                    isLight
                      ? 'text-ls-navy/90 hover:bg-ls-navy/5 hover:text-ls-red'
                      : 'text-ls-white/90 hover:bg-ls-white/5 hover:text-ls-red'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
            </nav>
          </div>
        </div>
      )}
    </>
  );
};

export default FloatingNav;
