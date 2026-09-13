import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { HomeSection } from './components/HomeSection';
import { SolutionsSection } from './components/SolutionsSection';
import { IndustriesSection } from './components/IndustriesSection';
import { AiCompanyBuilderSection } from './components/AiCompanyBuilderSection';
import { TechnologySection } from './components/TechnologySection';
import { WorkSection } from './components/WorkSection';
import { PharosSection } from './components/InsightsResearchSection';
import { AiReadinessAssessment } from './components/AiReadinessAssessment';
import { AboutSection } from './components/AboutSection';
import { LegalSection } from './components/LegalSection';
import { ScrollToTopButton } from './components/ScrollToTopButton';
import { Footer } from './components/Footer';
import { ContactModal } from './components/ContactModal';

export const App: React.FC = () => {
  const [currentRoute, setCurrentRoute] = useState<string>('home');
  const [routeParam, setRouteParam] = useState<string | undefined>(undefined);
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('lightspeed_theme');
      if (saved === 'light' || saved === 'dark') return saved;
    }
    return 'dark';
  });
  const [isContactOpen, setIsContactOpen] = useState<boolean>(false);
  const [contactIntent, setContactIntent] = useState<string>('Start a Conversation');
  const [contactSummary, setContactSummary] = useState<string>('');

  // Persist theme and update root html class and body background
  useEffect(() => {
    localStorage.setItem('lightspeed_theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.style.backgroundColor = '#060d16';
      document.body.style.backgroundColor = '#060d16';
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.style.backgroundColor = '#edf3f8';
      document.body.style.backgroundColor = '#edf3f8';
    }
  }, [theme]);

  // Handle navigation
  const handleNavigate = (route: string, param?: string) => {
    setCurrentRoute(route);
    setRouteParam(param);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Open contact modal with prefilled context
  const handleOpenContactModal = (intent?: string, summary?: string) => {
    if (intent) setContactIntent(intent);
    if (summary) setContactSummary(summary);
    setIsContactOpen(true);
  };

  // Theme toggle
  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <div className={`min-h-screen w-full max-w-full overflow-x-hidden font-sans transition-colors duration-500 ease-in-out ${
      theme === 'dark' ? 'bg-[#060d16] text-[#f0f6fa]' : 'bg-[#edf3f8] text-[#061522]'
    }`}>
      
      {/* Navigation Header */}
      <Header
        currentRoute={currentRoute}
        onNavigate={handleNavigate}
        theme={theme}
        onToggleTheme={toggleTheme}
        onOpenContactModal={() => handleOpenContactModal('Start a Conversation')}
      />

      {/* Main Page Route View */}
      <main className="pt-2 sm:pt-4 pb-12">
        {currentRoute === 'home' && (
          <HomeSection
            onNavigate={handleNavigate}
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'solutions' && (
          <SolutionsSection
            initialSubSection={routeParam}
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'industries' && (
          <IndustriesSection
            initialIndustry={routeParam}
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'ai-company-builder' && (
          <AiCompanyBuilderSection
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'technology' && (
          <TechnologySection
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'work' && (
          <WorkSection
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {(currentRoute === 'pharos' || currentRoute === 'insights' || currentRoute === 'research') && (
          <PharosSection
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'resources' && (
          <AiReadinessAssessment
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'about' && (
          <AboutSection
            onOpenContactModal={handleOpenContactModal}
            theme={theme}
          />
        )}

        {currentRoute === 'legal' && (
          <LegalSection
            theme={theme}
          />
        )}
      </main>

      {/* Global Footer */}
      <Footer
        onNavigate={handleNavigate}
        onOpenContactModal={handleOpenContactModal}
        theme={theme}
      />

      {/* Contact Modal */}
      <ContactModal
        isOpen={isContactOpen}
        onClose={() => setIsContactOpen(false)}
        prefilledIntent={contactIntent}
        prefilledSummary={contactSummary}
        theme={theme}
      />

      {/* Global Architectural Return to Top Floating Control */}
      <ScrollToTopButton theme={theme} />

    </div>
  );
};

export default App;
