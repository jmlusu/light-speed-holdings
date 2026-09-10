import React, { useState, useEffect } from 'react';
import { ThreeCanvas } from './components/ThreeCanvas';
import { FloatingNav } from './components/FloatingNav';
import { CorporateLanding } from './components/CorporateLanding';
import { ExecutiveBriefingModal } from './components/ExecutiveBriefingModal';
import { AgentModal } from './components/AgentModal';

import { agentsList } from './data/companyData';
import { Agent } from './types';

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

  return (
    <div className={`min-h-screen relative font-sans transition-colors duration-500 overflow-x-hidden ${
      theme === 'light' 
        ? 'spatial-ambient-light text-slate-800' 
        : 'spatial-ambient-dark text-zinc-100'
    }`}>
      <ThreeCanvas theme={theme} />

      <FloatingNav
        onRequestBriefing={handleRequestBriefing}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <CorporateLanding
        onRequestBriefing={handleRequestBriefing}
        onSelectAgentForModal={setSelectedAgent}
        agentsList={agentsList}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <ExecutiveBriefingModal
        isOpen={isBriefingModalOpen}
        onClose={() => setIsBriefingModalOpen(false)}
        prefillSummary={briefingSummary}
        theme={theme}
      />

      {selectedAgent && (
        <AgentModal
          agent={selectedAgent}
          onClose={() => setSelectedAgent(null)}
          onDispatchTask={() => {
            setSelectedAgent(null);
            handleRequestBriefing(`Inquiry regarding specialist agent capability: ${selectedAgent.name} (${selectedAgent.role})`);
          }}
        />
      )}
    </div>
  );
};

export default App;
