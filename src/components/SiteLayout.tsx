import React, { useEffect, useRef } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { ThreeCanvas } from './ThreeCanvas';
import { FloatingNav } from './FloatingNav';
import { SiteFooter } from './SiteFooter';
import { ExecutiveBriefingModal } from './ExecutiveBriefingModal';
import { AgentModal } from './AgentModal';
import { Agent } from '../types';

interface SiteLayoutProps {
  theme: 'light' | 'dark';
  onToggleTheme: () => void;
  onRequestBriefing: (summary?: string) => void;
  isBriefingModalOpen: boolean;
  briefingSummary: string;
  onCloseBriefingModal: () => void;
  selectedAgent: Agent | null;
  onCloseAgentModal: () => void;
  onDispatchTask: (agent: Agent) => void;
}

const ROUTE_TITLES: Record<string, string> = {
  '/': 'LIGHTSPEED HOLDINGS — Build the Intelligent Enterprise',
  '/about': 'About | LIGHTSPEED HOLDINGS',
  '/solutions': 'Solutions | LIGHTSPEED HOLDINGS',
  '/solutions/agentic-ai': 'Agentic AI | LIGHTSPEED HOLDINGS',
  '/solutions/digital-transformation': 'Digital Transformation | LIGHTSPEED HOLDINGS',
  '/solutions/data-intelligence': 'Data & Intelligence | LIGHTSPEED HOLDINGS',
  '/solutions/automation': 'Intelligent Automation | LIGHTSPEED HOLDINGS',
  '/solutions/strategy-advisory': 'Strategy & Advisory | LIGHTSPEED HOLDINGS',
  '/industries': 'Industries | LIGHTSPEED HOLDINGS',
  '/industries/government': 'Government | LIGHTSPEED HOLDINGS',
  '/industries/development': 'Development & Donor | LIGHTSPEED HOLDINGS',
  '/industries/financial-services': 'Financial Services | LIGHTSPEED HOLDINGS',
  '/industries/healthcare': 'Healthcare | LIGHTSPEED HOLDINGS',
  '/industries/agriculture': 'Agriculture | LIGHTSPEED HOLDINGS',
  '/ai-company-builder': 'AI Company Builder | LIGHTSPEED HOLDINGS',
  '/technology': 'Technology | LIGHTSPEED HOLDINGS',
  '/work': 'Work & Proof | LIGHTSPEED HOLDINGS',
  '/insights': 'Insights | LIGHTSPEED HOLDINGS',
  '/contact': 'Start a Conversation | LIGHTSPEED HOLDINGS',
  '/legal/privacy': 'Privacy Policy | LIGHTSPEED HOLDINGS',
  '/legal/terms': 'Terms of Service | LIGHTSPEED HOLDINGS',
};

/**
 * Shared site shell rendered once for every routed page.
 * Owns the ambient canvas, fixed nav, footer, and the always-mounted modals;
 * routed page content flows through <Outlet/>.
 * App.tsx remains the state owner and passes state down via props.
 */
export const SiteLayout: React.FC<SiteLayoutProps> = ({
  theme,
  onToggleTheme,
  onRequestBriefing,
  isBriefingModalOpen,
  briefingSummary,
  onCloseBriefingModal,
  selectedAgent,
  onCloseAgentModal,
  onDispatchTask,
}) => {
  const { pathname } = useLocation();
  // Skip focus management for the pathname we mounted on. Tracked by value
  // (not a boolean) so React 18 StrictMode's double effect-invocation can't
  // trip it: both mount passes see the same pathname and return early, while
  // any real route change reliably moves focus to the main landmark. Leaving
  // focus on <body> at load also means a keyboard user's first Tab reaches
  // the skip link (and then the nav) instead of jumping past both.
  const lastPathnameRef = useRef(pathname);

  useEffect(() => {
    document.title = ROUTE_TITLES[pathname] ?? 'LIGHTSPEED HOLDINGS';

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

      <ThreeCanvas theme={theme} />

      <FloatingNav
        onRequestBriefing={onRequestBriefing}
        theme={theme}
        onToggleTheme={onToggleTheme}
      />

      {/* pt-20 clears the fixed FloatingNav; tabIndex keeps focus() valid for a11y */}
      <main id="main-content" tabIndex={-1} className="pt-20 focus:outline-none">
        <Outlet />
      </main>

      <SiteFooter theme={theme} />

      {/* Modals stay mounted across route changes */}
      <ExecutiveBriefingModal
        isOpen={isBriefingModalOpen}
        onClose={onCloseBriefingModal}
        prefillSummary={briefingSummary}
        theme={theme}
      />

      {selectedAgent && (
        <AgentModal
          agent={selectedAgent}
          onClose={onCloseAgentModal}
          onDispatchTask={onDispatchTask}
        />
      )}
    </>
  );
};

export default SiteLayout;
