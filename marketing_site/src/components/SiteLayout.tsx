import React, { useEffect, useRef } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { FloatingNav } from './FloatingNav';
import { SiteFooter } from './SiteFooter';
import { ExecutiveBriefingModal } from './ExecutiveBriefingModal';
import { useSite } from '../site-context';
import { trackJourneyEvent, stageForRoute } from '../hooks/useJourneyEvents';
import { scrollToHash } from '../hooks/useSmoothScroll';
import { getInsightArticle } from '../data/insights';
import { applyPageMeta } from '../lib/seo';

export const SiteLayout: React.FC = () => {
  const { pathname, hash } = useLocation();
  const { theme, onToggleTheme, onRequestBriefing, isBriefingOpen, briefingSummary, closeBriefing } = useSite();

  const lastPathnameRef = useRef(pathname);

  useEffect(() => {
    trackJourneyEvent({
      eventType: 'page_view',
      route: pathname,
      journeyStage: stageForRoute(pathname),
    });
  }, [pathname]);

  useEffect(() => {
    const articleMatch = pathname.match(/^\/insights\/([^/]+)\/?$/);
    const article = articleMatch ? getInsightArticle(articleMatch[1]) : undefined;

    if (article?.seo) {
      applyPageMeta({
        title: article.seo.title,
        description: article.seo.description,
        type: 'article',
        url: window.location.origin + pathname,
      });
    } else {
      document.title = `LIGHTSPEED HOLDINGS | ${pathname === '/' ? 'AI-Native Company Builder' : pathname.replace('/', '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}`;
    }

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (hash) {
      // Hash target exists after commit (same-page section or mounted route content).
      const el = document.getElementById(hash.slice(1));
      if (el) {
        scrollToHash(hash);
      }
      // No element found: keep current position rather than jumping to top.
    } else {
      window.scrollTo({ top: 0, left: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    }

    if (lastPathnameRef.current === pathname) return;
    lastPathnameRef.current = pathname;
    const main = document.getElementById('main-content');
    if (main) {
      main.focus({ preventScroll: true });
    }
  }, [pathname, hash]);

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
