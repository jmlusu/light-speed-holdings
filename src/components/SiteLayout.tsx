import React, { useEffect, useRef } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { FloatingNav } from './FloatingNav';
import { SiteFooter } from './SiteFooter';
import { ExecutiveBriefingModal } from './ExecutiveBriefingModal';
import { useSite } from '../site-context';

export const SiteLayout: React.FC = () => {
  const { pathname } = useLocation();
  const { theme, onToggleTheme, onRequestBriefing, isBriefingOpen, briefingSummary, closeBriefing } = useSite();

  const lastPathnameRef = useRef(pathname);

  useEffect(() => {
    document.title = `LIGHTSPEED HOLDINGS | ${pathname === '/' ? 'AI-Native Company Builder' : pathname.replace('/', '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}`;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, left: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });

    if (lastPathnameRef.current === pathname) return;
    lastPathnameRef.current = pathname;
    const main = document.getElementById('main-content');
    if (main) {
      main.focus({ preventScroll: true });
    }
  }, [pathname]);

  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to content
      </a>

      <FloatingNav
        onRequestBriefing={onRequestBriefing}
        theme={theme}
        onToggleTheme={onToggleTheme}
      />

      <main id="main-content" tabIndex={-1} className="pt-20 focus:outline-none">
        <Outlet />
      </main>

      <SiteFooter theme={theme} />

      <ExecutiveBriefingModal
        isOpen={isBriefingOpen}
        onClose={closeBriefing}
        prefillSummary={briefingSummary}
        theme={theme}
      />
    </>
  );
};

export default SiteLayout;
