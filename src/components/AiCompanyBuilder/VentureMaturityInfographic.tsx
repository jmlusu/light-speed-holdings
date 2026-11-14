import React from 'react';
import { Reveal } from '../Reveal';

interface VentureMaturityInfographicProps {
  theme: 'light' | 'dark';
}

export const VentureMaturityInfographic: React.FC<VentureMaturityInfographicProps> = ({ theme }) => {
  const isLight = theme === 'light';

  return (
    <Reveal>
      <div className={`rounded-3xl p-4 shadow-xl ${
        isLight ? 'bg-ls-white/95' : 'bg-ls-navy/80 shadow-black/40'
      }`}>
        <img
          src="/assets/aistudio/AI_Venture_Studio_Lifecycle_Pipeline_30708830.png"
          alt="AI Venture Studio Lifecycle Pipeline"
          className="w-full h-auto rounded-2xl"
        />
      </div>
    </Reveal>
  );
};

export default VentureMaturityInfographic;
