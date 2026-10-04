import React from 'react';
import '../../brand/tokens/brand-tokens.css';

interface FeatureCardProps {
  title: string;
  icon: React.ReactNode;
  body: string;
  badge?: string;
  href: string;
  className?: string;
}

export const FeatureCard: React.FC<FeatureCardProps> = ({
  title,
  icon,
  body,
  badge,
  href,
  className = '',
}) => {
  return (
    <article
      className={`ls-feature-card ${className}`}
      style={{
        backgroundColor: 'var(--color-white, #FFFFFF)',
        border: '1px solid var(--color-grey-light-text, #9CA3AF)',
        borderRadius: 'var(--radius-medium, 8px)',
        padding: 'var(--spacing-32, 32px)',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        minHeight: '280px',
        transition: 'box-shadow 0.2s ease, border-color 0.2s ease, transform 0.1s ease',
      } as React.CSSProperties}
      onMouseEnter={(e) => {
        const target = e.currentTarget as HTMLElement;
        target.style.boxShadow = '0 12px 32px rgba(7, 10, 64, 0.12)';
        target.style.borderColor = 'var(--color-cyan, #00BFFF)';
        target.style.transform = 'translateY(-4px)';
      }}
      onMouseLeave={(e) => {
        const target = e.currentTarget as HTMLElement;
        target.style.boxShadow = 'none';
        target.style.borderColor = 'var(--color-grey-light-text, #9CA3AF)';
        target.style.transform = 'translateY(0)';
      }}
    >
      <div
        className="ls-feature-card__icon"
        style={{
          color: 'var(--color-navy, #070A40)',
          marginBottom: 'var(--spacing-16, 16px)',
          display: 'flex',
          alignItems: 'center',
        } as React.CSSProperties}
      >
        {icon}
      </div>
      <div className="ls-feature-card__header" style={{ marginBottom: 'var(--spacing-12, 12px)' } as React.CSSProperties}>
        {badge && (
          <span
            className="ls-badge"
            style={{
              display: 'inline-block',
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-caption, 12pt)',
              color: 'var(--color-white, #FFFFFF)',
              backgroundColor: 'var(--color-red, #E63946)',
              padding: 'var(--spacing-4, 4px) var(--spacing-8, 8px)',
              borderRadius: 'var(--radius-small, 4px)',
              marginBottom: 'var(--spacing-8, 8px)',
            } as React.CSSProperties}
          >
            {badge}
          </span>
        )}
        <h3
          className="ls-feature-card__title"
          style={{
            fontFamily: 'var(--font-display, Arial)',
            fontWeight: 700,
            fontSize: 'var(--size-title-md, 24pt)',
            lineHeight: 1.2,
            color: 'var(--color-navy, #070A40)',
            margin: 0,
          } as React.CSSProperties}
        >
          {title}
        </h3>
      </div>
      <p
        className="ls-feature-card__body"
        style={{
          fontFamily: 'var(--font-body, Arial)',
          fontWeight: 400,
          fontSize: 'var(--size-body, 14pt)',
          lineHeight: 1.6,
          color: 'var(--color-grey-dark, #6B7280)',
          margin: 0,
          marginBottom: 'var(--spacing-24, 24px)',
          flex: 1,
        } as React.CSSProperties}
      >
        {body}
      </p>
      <a
        href={href}
        className="ls-feature-card__link"
        style={{
          fontFamily: 'var(--font-body, Arial)',
          fontWeight: 400,
          fontSize: 'var(--size-body, 14pt)',
          color: 'var(--color-cyan, #00BFFF)',
          textDecoration: 'none',
          display: 'inline-flex',
          alignItems: 'center',
          gap: 'var(--spacing-8, 8px)',
          transition: 'color 0.2s ease, gap 0.2s ease',
        } as React.CSSProperties}
        onMouseEnter={(e) => {
          const target = e.currentTarget as HTMLElement;
          target.style.color = 'var(--color-navy, #070A40)';
          target.style.gap = 'var(--spacing-12, 12px)';
        }}
        onMouseLeave={(e) => {
          const target = e.currentTarget as HTMLElement;
          target.style.color = 'var(--color-cyan, #00BFFF)';
          target.style.gap = 'var(--spacing-8, 8px)';
        }}
      >
        Learn more
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0 } as React.CSSProperties}>
          <path d="M5 12h14M12 5l7 7-7 7" />
        </svg>
      </a>
    </article>
  );
};

export default FeatureCard;
