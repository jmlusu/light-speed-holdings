import React, { useEffect } from 'react';
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
  '/': 'LIGHTSPEED HOLDINGS — From Strategy to Intelligent Execution',
  '/home': 'LIGHTSPEED HOLDINGS — From Strategy to Intelligent Execution',
  '/about': 'About | LIGHTSPEED HOLDINGS',
  '/capabilities': 'Overview | LIGHTSPEED HOLDINGS',
  '/capabilities/offerings': 'Core Offerings | LIGHTSPEED HOLDINGS',
  '/capabilities/diagnostic': 'AI Diagnostic | LIGHTSPEED HOLDINGS',
  '/industries': 'Industries | LIGHTSPEED HOLDINGS',
  '/evidence': 'Evidence | LIGHTSPEED HOLDINGS',
  '/insights': 'Insights | LIGHTSPEED HOLDINGS',
  '/engagement': 'Engagement | LIGHTSPEED HOLDINGS',
  '/contact': 'Contact | LIGHTSPEED HOLDINGS',
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

  // On route change: update the document title, scroll to top, and move
  // focus to the main landmark for assistive tech. Respect reduced motion.
  useEffect(() => {
    document.title = ROUTE_TITLES[pathname] ?? 'LIGHTSPEED HOLDINGS';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, left: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });

    const main = document.getElementById('main-content');
    if (main) {
      main.focus({ preventScroll: true });
    }
  }, [pathname]);

  return (
    <>
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
