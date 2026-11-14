/**
 * Button Component
 *
 * Canonical button with primary, secondary, ghost, and link variants
 * Directive §34 — CTA system
 */

import React from 'react';
import { tokens } from '@lightspeed/design-system/tokens';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className = '',
      disabled,
      children,
      style,
      ...props
    },
    ref
  ) => {
    const isDark = document.documentElement.classList.contains('dark');
    const colorTokens = tokens.colors;

    const baseStyles: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: tokens.spacing[2],
      fontFamily: tokens.typography.fontFamily.sans,
      fontWeight: tokens.typography.fontWeight.bold,
      borderRadius: '9999px',
      border: '1px solid transparent',
      cursor: loading || disabled ? 'not-allowed' : 'pointer',
      opacity: loading || disabled ? 0.6 : 1,
      transition: 'all 250ms cubic-bezier(0.16, 1, 0.3, 1)',
      width: fullWidth ? '100%' : 'auto',
      textDecoration: 'none',
      position: 'relative',
      overflow: 'hidden',
    };

    const sizeStyles: Record<string, React.CSSProperties> = {
      sm: {
        padding: `${tokens.spacing[2]} ${tokens.spacing[4]}`,
        fontSize: tokens.typography.fontSize.bodySm,
      },
      md: {
        padding: `${tokens.spacing[3]} ${tokens.spacing[6]}`,
        fontSize: tokens.typography.fontSize.body,
      },
      lg: {
        padding: `${tokens.spacing[4]} ${tokens.spacing[8]}`,
        fontSize: tokens.typography.fontSize.bodyLg,
      },
    };

    const variantStyles: Record<string, React.CSSProperties> = {
      primary: {
        backgroundColor: colorTokens.cta.primary.background,
        color: colorTokens.cta.primary.text,
        borderColor: 'transparent',
        boxShadow: `
          inset 0 1px 1px rgba(255, 255, 255, 0.4),
          0 4px 6px -1px rgba(0, 0, 0, 0.1),
          0 2px 4px -1px rgba(0, 0, 0, 0.06)
        `,
      },
      secondary: {
        backgroundColor: isDark ? 'rgba(7, 10, 64, 0.85)' : 'rgba(255, 255, 255, 0.95)',
        color: isDark ? colorTokens.white : colorTokens.navy,
        borderColor: 'transparent',
        boxShadow: isDark
          ? 'inset 0 1px 1px rgba(255, 255, 255, 0.2), 0 4px 12px rgba(0, 0, 0, 0.35)'
          : 'inset 0 1px 1.5px rgba(255, 255, 255, 0.9), 0 4px 12px rgba(7, 10, 64, 0.12)',
      },
      ghost: {
        backgroundColor: 'transparent',
        color: isDark ? colorTokens.white : colorTokens.navy,
        borderColor: 'transparent',
      },
      link: {
        backgroundColor: 'transparent',
        color: isDark ? colorTokens.cyan : colorTokens.navy,
        textDecoration: 'underline',
        textUnderlineOffset: '2px',
        padding: 0,
        borderColor: 'transparent',
      },
    };

    const hoverStyles: Record<string, React.CSSProperties> = {
      primary: {
        backgroundColor: colorTokens.cta.primary.hover,
        transform: 'translateY(-1.5px)',
        boxShadow: `
          inset 0 1px 2px rgba(255, 255, 255, 0.6),
          0 8px 20px -3px ${colorTokens.cta.primary.shadow},
          0 0 18px rgba(230, 57, 70, 0.45)
        `,
      },
      secondary: {
        backgroundColor: isDark ? 'rgba(255, 255, 255, 0.12)' : 'rgba(7, 10, 64, 0.08)',
        transform: 'translateY(-1.5px)',
        boxShadow: isDark
          ? 'inset 0 1px 1.5px rgba(255, 255, 255, 0.35), 0 6px 16px rgba(0, 0, 0, 0.45)'
          : 'inset 0 1px 2px rgba(255, 255, 255, 1), 0 6px 16px rgba(7, 10, 64, 0.18)',
      },
      ghost: {
        backgroundColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(7, 10, 64, 0.05)',
      },
    };

    const combinedStyle: React.CSSProperties = {
      ...baseStyles,
      ...sizeStyles[size],
      ...variantStyles[variant],
      ...style,
    };

    return (
      <button
        ref={ref}
        className={className}
        disabled={disabled || loading}
        style={combinedStyle}
        onMouseEnter={(e) => {
          if (!disabled && !loading) {
            Object.assign(e.currentTarget.style, hoverStyles[variant]);
          }
        }}
        onMouseLeave={(e) => {
          if (!disabled && !loading) {
            Object.assign(e.currentTarget.style, variantStyles[variant]);
          }
        }}
        {...props}
      >
        {loading ? (
          <>
            <svg
              className="animate-spin"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="10" strokeOpacity="0.25" />
              <path
                d="M12 2a10 10 0 0 1 10 10"
                strokeLinecap="round"
              />
            </svg>
            <span>Loading...</span>
          </>
        ) : (
          <>
            {leftIcon && <span aria-hidden="true">{leftIcon}</span>}
            {children}
            {rightIcon && <span aria-hidden="true">{rightIcon}</span>}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
