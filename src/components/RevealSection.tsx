import React, { createContext, useContext } from 'react';
import { useSectionReveal } from '../hooks/useSectionReveal';

interface RevealSectionContextValue {
  isVisible: boolean;
  getRevealClass: (
    type?: 'up' | 'fade' | 'scale',
    delayIndex?: 1 | 2 | 3 | 4 | 5 | 6,
    additional?: string
  ) => string;
}

const RevealSectionContext = createContext<RevealSectionContextValue>({
  isVisible: true,
  getRevealClass: (type = 'up', delayIndex, additional = '') =>
    `${type === 'fade' ? 'reveal-fade' : 'reveal-up'} is-visible ${
      delayIndex ? `delay-${delayIndex}` : ''
    } ${additional}`.trim(),
});

export const useRevealContext = () => useContext(RevealSectionContext);

export interface RevealSectionProps extends React.HTMLAttributes<HTMLElement> {
  as?: 'section' | 'div' | 'article' | 'header';
  threshold?: number;
  rootMargin?: string;
  triggerOnce?: boolean;
  immediate?: boolean;
  children: React.ReactNode;
}

/**
 * Container component that attaches an IntersectionObserver to orchestrate
 * staged entry animations for child elements carrying 'reveal-up' and 'reveal-fade'.
 */
export const RevealSection: React.FC<RevealSectionProps> = ({
  as: Component = 'section',
  threshold = 0.12,
  rootMargin = '0px 0px -40px 0px',
  triggerOnce = true,
  immediate = false,
  className = '',
  children,
  ...rest
}) => {
  const { ref, isVisible, getRevealClass } = useSectionReveal<HTMLElement>({
    threshold,
    rootMargin,
    triggerOnce,
    immediate,
  });

  return (
    <RevealSectionContext.Provider value={{ isVisible, getRevealClass }}>
      <Component ref={ref as React.Ref<HTMLElement> as unknown as React.Ref<never>} className={className} {...rest}>
        {children}
      </Component>
    </RevealSectionContext.Provider>
  );
};

export interface RevealItemProps extends React.HTMLAttributes<HTMLElement> {
  as?: string;
  variant?: 'up' | 'fade' | 'scale';
  delay?: 1 | 2 | 3 | 4 | 5 | 6;
  children: React.ReactNode;
}

/**
 * Child element that animates into view using 'reveal-up' or 'reveal-fade'
 * once its parent RevealSection or intersection observer activates.
 */
export const RevealItem: React.FC<RevealItemProps> = ({
  as: Component = 'div',
  variant = 'up',
  delay,
  className = '',
  children,
  ...rest
}) => {
  const { isVisible } = useRevealContext();
  const base = variant === 'fade' ? 'reveal-fade' : variant === 'scale' ? 'reveal-scale' : 'reveal-up';
  const visible = isVisible ? 'is-visible' : '';
  const delayClass = delay ? `delay-${delay}` : '';

  return React.createElement(
    Component,
    {
      className: `${base} ${visible} ${delayClass} ${className}`.trim(),
      ...rest,
    },
    children
  );
};

export default RevealSection;
