import React from 'react';
import { InteractiveOperatingModel } from './InteractiveOperatingModel';

interface OperatingModelSectionProps {
  theme: 'light' | 'dark';
  onRequestBriefing: (summary?: string) => void;
}

export const OperatingModelSection: React.FC<OperatingModelSectionProps> = ({ theme, onRequestBriefing }) => {
  return (
    <section id="operating-model" className="py-24 px-4 sm:px-8 max-w-7xl mx-auto w-full relative z-10">
      <InteractiveOperatingModel
        theme={theme}
        onRequestBriefing={onRequestBriefing}
      />
    </section>
  );
};
