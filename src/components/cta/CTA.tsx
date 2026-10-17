/**
 * CTA Components
 *
 * Canonical CTA system with primary, secondary, and contextual variants
 * Directive §34
 */

import React from 'react';
import { ctasRegistry, canonicalCTALabels } from '@lightspeed/data/ctas';
import { tokens } from '@lightspeed/design-system/tokens';

interface CTAButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'contextual';
  size?: 'sm' | 'md' | 'lg';
  href?: string;
  children: React.ReactNode;
}

export const CTAButton = React.forwardRef<HTMLButtonElement | HTMLAnchorElement, CTAButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      href,
      children,
      className = '',
      style,
      disabled,
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
      borderRadius: tokens.radius.small,
      border: 'none',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.6 : 1,
      transition: 'all 200ms ease',
      textDecoration: 'none',
      width: 'auto',
    };

    const sizeStyles: Record<string, React.CSSProperties> = {
      sm: {
        padding: `${tokens.spacing[1]} ${tokens.spacing[3]}`,
        fontSize: tokens.typography.fontSize.bodySm,
      },
      md: {
        padding: `${tokens.spacing[2]} ${tokens.spacing[4]}`,
        fontSize: tokens.typography.fontSize.body,
      },
      lg: {
        padding: `${tokens.spacing[3]} ${tokens.spacing[6]}`,
        fontSize: tokens.typography.fontSize.bodyLg,
      },
    };

    const variantStyles: Record<string, React.CSSProperties> = {
      primary: {
        backgroundColor: colorTokens.cta.primary.background,
        color: colorTokens.cta.primary.text,
        boxShadow: `0 4px 14px ${colorTokens.cta.primary.shadow}`,
      },
      secondary: {
        backgroundColor: 'transparent',
        color: isDark ? colorTokens.white : colorTokens.navy,
        border: `2px solid ${isDark ? colorTokens.white : colorTokens.navy}`,
      },
      contextual: {
        backgroundColor: 'transparent',
        color: isDark ? colorTokens.cyan : colorTokens.navy,
        textDecoration: 'underline',
        textUnderlineOffset: '2px',
        padding: 0,
      },
    };

    const hoverStyles: Record<string, React.CSSProperties> = {
      primary: {
        backgroundColor: colorTokens.cta.primary.hover,
      },
      secondary: {
        backgroundColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(7,10,64,0.05)',
      },
    };

    const Component = href ? 'a' : 'button';
    const combinedStyle: React.CSSProperties = {
      ...baseStyles,
      ...sizeStyles[size],
      ...variantStyles[variant],
      ...style,
    };

    const commonProps = {
      className,
      style: combinedStyle,
      onMouseEnter: (e: React.MouseEvent<HTMLElement>) => {
        if (!disabled) {
          Object.assign(e.currentTarget.style, hoverStyles[variant]);
        }
      },
      onMouseLeave: (e: React.MouseEvent<HTMLElement>) => {
        if (!disabled) {
          Object.assign(e.currentTarget.style, variantStyles[variant]);
        }
      },
      ...props,
    };

    if (href) {
      return (
        <a
          {...(commonProps as unknown as React.AnchorHTMLAttributes<HTMLAnchorElement>)}
          ref={ref as React.Ref<HTMLAnchorElement>}
          href={href}
        >
          {children}
        </a>
      );
    }

    return (
      <button {...commonProps} ref={ref as React.Ref<HTMLButtonElement>}>
        {children}
      </button>
    );
  }
);

CTAButton.displayName = 'CTAButton';

/**
 * Primary CTA — Global primary action
 */
export const PrimaryCTA: React.FC<{ children?: React.ReactNode; href?: string; onClick?: () => void }> = ({
  children,
  href = '/contact',
  onClick,
}) => {
  const primaryCTA = ctasRegistry.find(c => c.id === 'cta-primary');
  return (
    <CTAButton variant="primary" href={href} onClick={onClick}>
      {children || primaryCTA?.label || canonicalCTALabels.primary}
    </CTAButton>
  );
};

/**
 * Secondary CTA — Global secondary action
 */
export const SecondaryCTA: React.FC<{ children?: React.ReactNode; href?: string; onClick?: () => void }> = ({
  children,
  href = '/ai-assessment',
  onClick,
}) => {
  const secondaryCTA = ctasRegistry.find(c => c.id === 'cta-secondary');
  return (
    <CTAButton variant="secondary" href={href} onClick={onClick}>
      {children || secondaryCTA?.label || canonicalCTALabels.secondary}
    </CTAButton>
  );
};

/**
 * Contextual CTA — Page-specific actions
 */
export const ContextualCTA: React.FC<{ id: string; href?: string; onClick?: () => void }> = ({
  id,
  href,
  onClick,
}) => {
  const cta = ctasRegistry.find(c => c.id === id);
  if (!cta) return null;

  return (
    <CTAButton variant={cta.variant as 'primary' | 'secondary' | 'contextual'} href={href || cta.href} onClick={onClick}>
      {cta.label}
    </CTAButton>
  );
};

/**
 * CTA Band — Full-width CTA section for page endings
 */
export interface CTABandProps {
  title: string;
  text?: string;
  primaryCTA?: { label: string; href: string };
  secondaryCTA?: { label: string; href: string };
  theme?: 'light' | 'dark';
}

export const CTABand: React.FC<CTABandProps> = ({
  title,
  text,
  primaryCTA,
  secondaryCTA,
  theme,
}) => {
  const isDark = theme === 'dark' || document.documentElement.classList.contains('dark');
  const colorTokens = tokens.colors;

  const bandStyle: React.CSSProperties = {
    padding: `${tokens.spacing[16]} ${tokens.spacing[12]}`,
    backgroundColor: isDark ? colorTokens.navy : colorTokens.navy,
    color: colorTokens.white,
    textAlign: 'center',
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: '720px',
    margin: '0 auto',
  };

  const titleStyle: React.CSSProperties = {
    fontFamily: tokens.typography.fontFamily.sans,
    fontWeight: tokens.typography.fontWeight.bold,
    fontSize: tokens.typography.fontSize.titleMd,
    margin: `0 0 ${tokens.spacing[4]}`,
    lineHeight: 1.2,
  };

  const textStyle: React.CSSProperties = {
    fontFamily: tokens.typography.fontFamily.sans,
    fontSize: tokens.typography.fontSize.bodyLg,
    lineHeight: 1.6,
    color: colorTokens.grey[300],
    margin: `0 0 ${tokens.spacing[8]}`,
  };

  const ctaGroupStyle: React.CSSProperties = {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: tokens.spacing[4],
  };

  return (
    <section style={bandStyle} aria-labelledby="cta-band-title">
      <div style={containerStyle}>
        <h2 id="cta-band-title" style={titleStyle}>{title}</h2>
        {text && <p style={textStyle}>{text}</p>}
        <div style={ctaGroupStyle}>
          {primaryCTA && (
            <CTAButton variant="primary" href={primaryCTA.href} size="lg">
              {primaryCTA.label}
            </CTAButton>
          )}
          {secondaryCTA && (
            <CTAButton variant="secondary" href={secondaryCTA.href} size="lg">
              {secondaryCTA.label}
            </CTAButton>
          )}
        </div>
      </div>
    </section>
  );
};

export default CTAButton;
