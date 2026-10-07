/**
 * Badge Component — Honesty Badge System
 *
 * Critical component for evidence-based transparency
 * Directive §10, §23 — Honesty badges for all claims
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export type BadgeVariant = 'proven' | 'pilot' | 'fieldable' | 'development' | 'neutral';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant: BadgeVariant;
  size?: 'sm' | 'md';
  dot?: boolean;
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  (
    {
      variant,
      size = 'md',
      dot = false,
      className = '',
      children,
      style,
      ...props
    },
    ref
  ) => {
    const variantStyles: Record<BadgeVariant, React.CSSProperties> = {
      proven: {
        borderColor: tokens.colors.honesty.proven.border,
        backgroundColor: tokens.colors.honesty.proven.background,
        color: tokens.colors.honesty.proven.text,
      },
      pilot: {
        borderColor: tokens.colors.honesty.pilot.border,
        backgroundColor: tokens.colors.honesty.pilot.background,
        color: tokens.colors.honesty.pilot.text,
      },
      fieldable: {
        borderColor: tokens.colors.honesty.fieldable.border,
        backgroundColor: tokens.colors.honesty.fieldable.background,
        color: tokens.colors.honesty.fieldable.text,
      },
      development: {
        borderColor: tokens.colors.honesty.development.border,
        backgroundColor: tokens.colors.honesty.development.background,
        color: tokens.colors.honesty.development.text,
      },
      neutral: {
        borderColor: tokens.colors.grey[300],
        backgroundColor: tokens.colors.grey[100],
        color: tokens.colors.grey[600],
      },
    };

    const sizeStyles: Record<string, React.CSSProperties> = {
      sm: {
        padding: `${tokens.spacing[1]} ${tokens.spacing[2]}`,
        fontSize: tokens.typography.fontSize.caption,
      },
      md: {
        padding: `${tokens.spacing[1]} ${tokens.spacing[3]}`,
        fontSize: tokens.typography.fontSize.overline,
      },
    };

    const combinedStyle: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      gap: tokens.spacing[1],
      borderWidth: '1px',
      borderStyle: 'solid',
      borderRadius: tokens.radius.full,
      fontFamily: tokens.typography.fontFamily.sans,
      fontWeight: tokens.typography.fontWeight.bold,
      whiteSpace: 'nowrap',
      ...variantStyles[variant],
      ...sizeStyles[size],
      ...style,
    };

    return (
      <span
        ref={ref}
        className={className}
        style={combinedStyle}
        {...props}
      >
        {dot && (
          <span
            style={{
              width: size === 'sm' ? '6px' : '8px',
              height: size === 'sm' ? '6px' : '8px',
              borderRadius: '50%',
              backgroundColor: 'currentColor',
            }}
            aria-hidden="true"
          />
        )}
        {children}
      </span>
    );
  }
);

Badge.displayName = 'Badge';

export default Badge;
