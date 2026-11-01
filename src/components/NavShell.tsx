/**
 * NavShell — Sticky dark navy navigation bar with drawer mobile menu.
 * Session 7 of the LightSpeed redesign.
 * Directive §7
 */

import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Search, Moon, Sun } from 'lucide-react';
import LogoLockup from '@/components/site/LogoLockup';

/** Canonical top-level navigation per IA decision (prompt 02). */
export const NAV_LINKS = [
  { name: 'Home', href: '/' },
  { name: 'What We Do', href: '/what-we-do' },
  { name: 'Solutions', href: '/solutions' },
  { name: 'Sectors', href: '/sectors' },
  { name: 'Use Cases', href: '/use-cases' },
  { name: 'Pharos Insights', href: '/insights' },
  { name: 'About', href: '/about' },
  { name: 'Contact', href: '/contact' },
  { name: 'Start Free', href: '/contact' },
] as const;

const isActivePath = (pathname: string, href: string): boolean =>
  href === '/' ? pathname === '/' : pathname === href || pathname.startsWith(`${href}/`);

interface NavShellProps {
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
  onRequestBriefing?: (summary?: string) => void;
}

export const NavShell: React.FC<NavShellProps> = ({
  theme = 'dark',
  onToggleTheme,
  onRequestBriefing,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { pathname } = useLocation();
  const isLight = theme === 'light';

  useEffect(() => {
    if (!mobileMenuOpen) return;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMobileMenuOpen(false);
        return;
      }
      if (event.key === 'Tab') {
        // Allow logical tab order within drawer
        return;
      }
    };

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [mobileMenuOpen]);

  const navLinkClass = isLight
    ? 'text-ls-navy/80 hover:bg-ls-navy/5 hover:text-ls-red'
    : 'text-ls-white/80 hover:bg-ls-white/5 hover:text-ls-red';

  const activeLinkClass = isLight
    ? 'text-ls-cyan hover:underline underline-offset-2 underline-ls-cyan-2'
    : 'text-ls-cyan hover:underline underline-offset-2 underline-ls-cyan-2';

  const mobileMenu = (
    <div
      className="fixed inset-x-0 top-[4.5rem] z-40 px-3 sm:px-4 lg:hidden pointer-events-none"
    >
      <div
        id="mobile-nav"
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
  );

  return (
    <React.Fragment>
      <nav
        className="fixed top-0 left-0 right-0 z-50 sticky top-0 bg-ls-navy/95 backdrop-blur-xl border-b border-ls-white/15 shadow-2xl"
      >
        <div className="w-full max-w-6xl px-4 sm:px-6 py-2.5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              to="/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2.5 group cursor-pointer"
            >
              <LogoLockup size={32} showText theme={theme} instance="first" />
            </Link>
          </div>

          <nav
            aria-label="Primary"
            className="hidden lg:flex items-center gap-2 xl:gap-4 text-[11px] xl:text-xs font-body font-bold tracking-wider"
          >
            {NAV_LINKS.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                onClick={() => setMobileMenuOpen(false)}
                aria-current={isActivePath(pathname, link.href) ? 'page' : undefined}
                className={isActivePath(pathname, link.href) ? activeLinkClass : navLinkClass}
              >
                {link.name}
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-2.5">
            {/* Right side: outline Contact pill and cyan Start Free pill */}
            <div className="flex items-center gap-1.5">
              {/* Outline Contact pill */}
              <span
                className={
                  isLight
                    ? 'inline-flex items-center rounded-full py-1 px-2 border border-ls-white/20 text-ls-white/60 text-[10px] font-bold tracking-wider'
                    : 'inline-flex items-center rounded-full py-1 px-2 border border-ls-navy/30 text-ls-navy/60 text-[10px] font-bold tracking-wider'
                }
              >
                Contact
              </span>

              {/* Cyan Start Free pill */}
              <span
                className="inline-flex items-center rounded-full py-1 px-2 bg-ls-cyan/10 text-ls-cyan text-[10px] font-bold tracking-wider"
              >
                Start Free
              </span>
            </div>

            {/* Search icon button (if search exists today) */}
            {typeof window !== 'undefined' && (
              <button
                type="button"
                onClick={() => setMobileMenuOpen(false)}
                className="p-2 rounded-full transition-colors cursor-pointer hover:bg-ls-navy/10"
                aria-label="Search"
              >
                <Search className="w-4 h-4" />
              </button>
            )}

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
      </nav>

      {mobileMenuOpen && mobileMenu}
    </React.Fragment>
  );
};

export default NavShell;
