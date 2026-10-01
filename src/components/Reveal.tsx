import React from 'react';
import { useInView } from '../hooks/useInView';

interface RevealProps {
  delay?: number;
  className?: string;
  children: React.ReactNode;
}

export const Reveal: React.FC<RevealProps> = ({ delay = 0, className, children }) => {
  const { ref, inView } = useInView<HTMLDivElement>();

  return (
    <div
      ref={ref}
      className={`transition-all duration-700 ease-out will-change-transform ${
        inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      } ${className ?? ''}`}
      style={delay > 0 ? { transitionDelay: `${delay}s` } : undefined}
    >
      {children}
    </div>
  );
};
