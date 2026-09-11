import React, { useState, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { SiteLayout } from './components/SiteLayout';

import { Agent } from './types';

// Code-split each route so non-home pages load on demand (kills the 1MB bundle).
const HomePage = React.lazy(() => import('./pages/HomePage'));
const AboutPage = React.lazy(() => import('./pages/AboutPage'));
const CapabilitiesPage = React.lazy(() => import('./pages/CapabilitiesPage'));
const OfferingsPage = React.lazy(() => import('./pages/OfferingsPage'));
const DiagnosticPage = React.lazy(() => import('./pages/DiagnosticPage'));
const IndustriesPage = React.lazy(() => import('./pages/IndustriesPage'));
const EvidencePage = React.lazy(() => import('./pages/EvidencePage'));
const InsightsPage = React.lazy(() => import('./pages/InsightsPage'));
const EngagementPage = React.lazy(() => import('./pages/EngagementPage'));
const ContactPage = React.lazy(() => import('./pages/ContactPage'));

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
            path="/home"
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
            path="/capabilities"
            element={
              <Suspense fallback={<RouteFallback />}>
                <CapabilitiesPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/capabilities/offerings"
            element={
              <Suspense fallback={<RouteFallback />}>
                <OfferingsPage theme={theme} onRequestBriefing={handleRequestBriefing} />
              </Suspense>
            }
          />
          <Route
            path="/capabilities/diagnostic"
            element={
              <Suspense fallback={<RouteFallback />}>
                <DiagnosticPage theme={theme} onRequestBriefing={handleRequestBriefing} />
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
            path="/evidence"
            element={
              <Suspense fallback={<RouteFallback />}>
                <EvidencePage theme={theme} onRequestBriefing={handleRequestBriefing} />
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
            path="/engagement"
            element={
              <Suspense fallback={<RouteFallback />}>
                <EngagementPage theme={theme} onRequestBriefing={handleRequestBriefing} />
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
        </Route>
      </Routes>
    </div>
  );
};

export default App;
