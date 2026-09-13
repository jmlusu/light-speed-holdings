import React from 'react';
import { HaomtgvGovernanceFramework } from './HaomtgvGovernanceFramework';

interface MethodFrameworkProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const MethodFramework: React.FC<MethodFrameworkProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  return (
    <section id="method" className="py-16 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10">
      <HaomtgvGovernanceFramework 
        theme={theme} 
        onOpenContactModal={onRequestBriefing} 
      />
    </section>
  );
};
