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
        backgroundColor: isDark ? colorTokens.dark.bgSurface : colorTokens.light.bgSurface,
        border: `1px solid ${isDark ? colorTokens.dark.borderDefault : colorTokens.light.borderDefault}`,
        boxShadow: isDark ? tokens.shadows.dark.md : tokens.shadows.md,
      },
      elevated: {
        backgroundColor: isDark ? colorTokens.dark.bgSurfaceElevated : colorTokens.light.bgSurfaceElevated,
        border: `1px solid ${isDark ? colorTokens.dark.borderSubtle : colorTokens.light.borderSubtle}`,
        boxShadow: isDark ? tokens.shadows.dark.lg : tokens.shadows.lg,
      },
      interactive: {
        backgroundColor: isDark ? colorTokens.dark.bgSurface : colorTokens.light.bgSurface,
        border: `1px solid ${isDark ? colorTokens.dark.borderDefault : colorTokens.light.borderDefault}`,
        boxShadow: isDark ? tokens.shadows.dark.md : tokens.shadows.md,
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
      boxShadow: isDark ? tokens.shadows.dark.xl : tokens.shadows.xl,
      borderColor: tokens.colors.cyan,
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
