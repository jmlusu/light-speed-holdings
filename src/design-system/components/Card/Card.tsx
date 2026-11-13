/**
 * Card Component
 *
 * Canonical card with default, elevated, and interactive variants
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'interactive';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  (
    {
      variant = 'default',
      padding = 'md',
      hover = false,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const isDark = document.documentElement.classList.contains('dark');
    const colorTokens = tokens.colors;

    const variantStyles: Record<string, React.CSSProperties> = {
      default: {
        backgroundColor: 'transparent',
        border: '1px solid rgba(255,255,255,0.06)',
        boxShadow: 'none',
      },
      elevated: {
        backgroundColor: 'transparent',
        border: '1px solid rgba(255,255,255,0.06)',
        boxShadow: 'none',
      },
      interactive: {
        backgroundColor: 'transparent',
        border: '1px solid rgba(255,255,255,0.06)',
        boxShadow: 'none',
        transition: 'all 200ms ease',
        cursor: 'pointer',
      },
    };

    const paddingStyles: Record<string, React.CSSProperties> = {
      none: { padding: 0 },
      sm: { padding: tokens.spacing[4] },
      md: { padding: tokens.spacing[6] },
      lg: { padding: tokens.spacing[8] },
    };

    const hoverStyles: React.CSSProperties = hover ? {
      transform: 'translateY(-2px)',
    } : {};

    const combinedStyle: React.CSSProperties = {
      borderRadius: tokens.radius.large,
      ...variantStyles[variant],
      ...paddingStyles[padding],
      ...hoverStyles,
      ...style,
    };

    return (
      <div
        ref={ref}
        className={className}
        style={combinedStyle}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export default Card;
