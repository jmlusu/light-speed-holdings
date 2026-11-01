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
 * Blue gradient band with logo, heading with cyan final word, sub line,
 * and crimson pill button with arrow.
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
  const onNavy = isDark ? '#FFFFFF' : '#070A40';
  const onCyan = '#00BFFF';
  const crimson = '#DC3641';

  const bandStyle: React.CSSProperties = {
    padding: `${tokens.spacing[16]} ${tokens.spacing[12]}`,
    background: isDark ? 'linear-gradient(135deg, #00BFFF 0%, #070A40 100%)' : 'linear-gradient(135deg, #00BFFF 0%, #070A40 100%)',
    color: onNavy,
    textAlign: 'center',
    position: 'relative',
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: '720px',
    margin: '0 auto',
    position: 'relative',
    zIndex: 1,
  };

  const titleStyle: React.CSSProperties = {
    fontFamily: tokens.typography.fontFamily.sans,
    fontWeight: tokens.typography.fontWeight.bold,
    fontSize: tokens.typography.fontSize.titleMd,
    margin: `0 0 ${tokens.spacing[4]}`,
    lineHeight: 1.2,
    display: 'inline-block',
  };

  const textStyle: React.CSSProperties = {
    fontFamily: tokens.typography.fontFamily.sans,
    fontSize: tokens.typography.fontSize.bodyLg,
    lineHeight: 1.6,
    color: isDark ? 'rgba(255,255,255,0.8)' : 'rgba(255,255,255,0.7)',
    margin: `0 0 ${tokens.spacing[8]}`,
  };

  const ctaGroupStyle: React.CSSProperties = {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: tokens.spacing[4],
    marginTop: tokens.spacing[6],
  };

  // Extract the final word of the title to style it cyan
  const titleWords = title.trim().split(/\s+/);
  const lastWord = titleWords[titleWords.length - 1];
  const restWords = titleWords.slice(0, -1);

  return (
    <section style={bandStyle} aria-labelledby="cta-band-title">
      <div style={containerStyle}>
        <h2 id="cta-band-title" style={titleStyle}>
          {restWords.length > 0
            ? <span>{restWords.join(' ')} </span>
            : ''}
          <span style={{ color: onCyan, fontWeight: 700 }}>{lastWord}</span>
        </h2>
        {text && <p style={textStyle}>{text}</p>}
        <div style={ctaGroupStyle}>
          {primaryCTA && (
            <CTAButton
              variant="primary"
              href={primaryCTA.href}
              size="lg"
              style={{
                backgroundColor: crimson,
                color: 'white',
                boxShadow: '0 4px 14px rgba(220,54,65,0.15)',
              }}
            >
              {primaryCTA.label}
              <svg
                width="12"
                height="12"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="2.5"
                style={{ transform: 'rotate(45deg)' }}
              >
                <path d="M5 12l6 6 6-6" />
              </svg>
            </CTAButton>
          )}
          {secondaryCTA && (
            <CTAButton
              variant="secondary"
              href={secondaryCTA.href}
              size="lg"
              style={{
                backgroundColor: 'transparent',
                color: onCyan,
                border: '2px solid onCyan',
              }}
            >
              {secondaryCTA.label}
            </CTAButton>
          )}
        </div>
      </div>
    </section>
  );
};

export default CTAButton;
