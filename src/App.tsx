import React, { useState, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { SiteLayout } from './components/SiteLayout';

import { Agent } from './types';

// Code-split each route so non-home pages load on demand (kills the 1MB bundle).
const HomePage = React.lazy(() => import('./pages/HomePage'));
const AboutPage = React.lazy(() => import('./pages/AboutPage'));
const SolutionsPage = React.lazy(() => import('./pages/SolutionsPage'));
const SolutionDetailPage = React.lazy(() => import('./pages/SolutionDetailPage'));
const IndustriesPage = React.lazy(() => import('./pages/IndustriesPage'));
const IndustryDetailPage = React.lazy(() => import('./pages/IndustryDetailPage'));
const AiCompanyBuilderPage = React.lazy(() => import('./pages/AiCompanyBuilderPage'));
const TechnologyPage = React.lazy(() => import('./pages/TechnologyPage'));
const WorkPage = React.lazy(() => import('./pages/WorkPage'));
const InsightsPage = React.lazy(() => import('./pages/InsightsPage'));
const ContactPage = React.lazy(() => import('./pages/ContactPage'));
const PrivacyPage = React.lazy(() => import('./pages/PrivacyPage'));
const TermsPage = React.lazy(() => import('./pages/TermsPage'));

const RouteFallback: React.FC = () => (
  <div
    role="status"
    aria-label="Loading page"
    className="flex min-h-[50vh] items-center justify-center"
  >
    <div className="h-8 w-8 animate-spin rounded-full border-2 border-ls-red border-t-transparent" />
  </div>
);

export const App: React.FC = () => {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    const saved = localStorage.getItem('ls_theme');
    return (saved === 'dark' || saved === 'light') ? saved : 'dark';
  });

  const toggleTheme = () => {
    setTheme(prev => {
      const next = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem('ls_theme', next);
      return next;
    });
  };

  const [isBriefingModalOpen, setIsBriefingModalOpen] = useState(false);
  const [briefingSummary, setBriefingSummary] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  const handleRequestBriefing = (summary?: string) => {
    setBriefingSummary(summary || '');
    setIsBriefingModalOpen(true);
  };

  const handleDispatchTask = (agent: Agent) => {
    setSelectedAgent(null);
    handleRequestBriefing(`Inquiry regarding specialist agent capability: ${agent.name} (${agent.role})`);
  };

  return (
    <div className={`min-h-screen relative font-sans transition-colors duration-500 overflow-x-hidden ${
      theme === 'light'
        ? 'spatial-ambient-light text-slate-800'
        : 'spatial-ambient-dark text-zinc-100'
    }`}>
      <Routes>
        <Route
          element={
            <SiteLayout
              theme={theme}
              onToggleTheme={toggleTheme}
              onRequestBriefing={handleRequestBriefing}
              isBriefingModalOpen={isBriefingModalOpen}
              briefingSummary={briefingSummary}
              onCloseBriefingModal={() => setIsBriefingModalOpen(false)}
              selectedAgent={selectedAgent}
              onCloseAgentModal={() => setSelectedAgent(null)}
              onDispatchTask={handleDispatchTask}
            />
          }
        >
          {/* Legacy aliases — replaced with the new sitemap destinations */}
          <Route path="/home" element={<Navigate to="/" replace />} />
          <Route path="/capabilities/*" element={<Navigate to="/solutions" replace />} />
          <Route path="/capabilities/diagnostic" element={<Navigate to="/solutions/strategy-advisory" replace />} />
          <Route path="/evidence" element={<Navigate to="/work" replace />} />
          <Route path="/engagement" element={<Navigate to="/contact" replace />} />

          <Route
            path="/"
            element={
              <Suspense fallback={<RouteFallback />}>
                <HomePage
                  theme={theme}
                  onRequestBriefing={handleRequestBriefing}
                />
              </Suspense>
            }
          />
          <Route
            path="/about"
            element={
              <Suspense fallback={<RouteFallback />}>
                <AboutPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/solutions"
            element={
              <Suspense fallback={<RouteFallback />}>
                <SolutionsPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/solutions/:slug"
            element={
              <Suspense fallback={<RouteFallback />}>
                <SolutionDetailPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/industries"
            element={
              <Suspense fallback={<RouteFallback />}>
                <IndustriesPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/industries/:slug"
            element={
              <Suspense fallback={<RouteFallback />}>
                <IndustryDetailPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/ai-company-builder"
            element={
              <Suspense fallback={<RouteFallback />}>
                <AiCompanyBuilderPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/technology"
            element={
              <Suspense fallback={<RouteFallback />}>
                <TechnologyPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/work"
            element={
              <Suspense fallback={<RouteFallback />}>
                <WorkPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/insights"
            element={
              <Suspense fallback={<RouteFallback />}>
                <InsightsPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/contact"
            element={
              <Suspense fallback={<RouteFallback />}>
                <ContactPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/legal/privacy"
            element={
              <Suspense fallback={<RouteFallback />}>
                <PrivacyPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/legal/terms"
            element={
              <Suspense fallback={<RouteFallback />}>
                <TermsPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
        </Route>
      </Routes>
    </div>
  );
};

export default App;
