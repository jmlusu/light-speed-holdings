import React from 'react';
import { Reveal } from '../Reveal';

interface HaomtgvPipelineDiagramProps {
  theme: 'light' | 'dark';
}

export const HaomtgvPipelineDiagram: React.FC<HaomtgvPipelineDiagramProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <Reveal>
      <div className={`rounded-3xl p-4 shadow-xl ${
        isLight ? 'bg-ls-white/95' : 'bg-ls-navy/80'
      }`}>
        <img
          src="/assets/aistudio/HAOMTGV_Closed-Loop_AI_Pipeline_c8fb13d6.png"
          alt="HAOMTGV Closed-Loop AI Pipeline Diagram"
          className="w-full h-auto rounded-2xl"
        />
      </div>
    </Reveal>
  );
};

export default HaomtgvPipelineDiagram;
