/**
 * Heading Component
 *
 * Semantic heading with design system typography
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6 | 'display';

export interface HeadingProps extends React.HTMLAttributes<HTMLHeadingElement> {
  level: HeadingLevel;
  as?: React.ElementType;
}

export const Heading = React.forwardRef<HTMLHeadingElement, HeadingProps>(
  (
    {
      level,
      as,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const Component = as || `h${level}` as React.ElementType;

    const levelStyles: Record<HeadingLevel, React.CSSProperties> = {
      display: tokens.typography.styles.displayXl,
      1: tokens.typography.styles.titleXl,
      2: tokens.typography.styles.titleLg,
      3: tokens.typography.styles.titleMd,
      4: tokens.typography.styles.titleSm,
      5: tokens.typography.styles.subtitle,
      6: tokens.typography.styles.body,
    };

    const isDark = document.documentElement.classList.contains('dark');
    const colorTokens = tokens.colors;

    const combinedStyle: React.CSSProperties = {
      ...levelStyles[level],
      color: isDark ? colorTokens.dark.textPrimary : colorTokens.light.textPrimary,
      margin: 0,
      ...style,
    };

    return (
      <Component
        ref={ref}
        className={className}
        style={combinedStyle}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

Heading.displayName = 'Heading';

export default Heading;
