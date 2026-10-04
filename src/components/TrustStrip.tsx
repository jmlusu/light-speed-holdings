import React, { useState, useEffect, useRef } from 'react';
import '../../brand/tokens/brand-tokens.css';

interface CaseStudy {
  id: string;
  client: string;
  logo: string;
  headline: string;
  metric: string;
  metricLabel: string;
  source: string;
}

const caseStudies: CaseStudy[] = [
  {
    id: 'malawi-gov',
    client: 'Malawi Government',
    logo: '/logos/malawi-gov.svg',
    headline: 'National AI Strategy consultation delivered in 6 weeks',
    metric: '40%',
    metricLabel: 'faster',
    source: 'results/malawi-ai-strategy.json',
  },
  {
    id: 'sadc-secretariat',
    client: 'SADC Secretariat',
    logo: '/logos/sadc.svg',
    headline: 'Agentic governance framework ratified',
    metric: '12',
    metricLabel: 'member states',
    source: 'results/sadc-framework.json',
  },
  {
    id: 'regional-bank',
    client: 'Regional Bank',
    logo: '/logos/regional-bank.svg',
    headline: 'Loan processing agents cut cycle time',
    metric: '60%',
    metricLabel: 'reduction',
    source: 'results/bank-loan-processing.json',
  },
];

interface TrustStripProps {
  className?: string;
}

export const TrustStrip: React.FC<TrustStripProps> = ({ className = '' }) => {
  const [scrollX, setScrollX] = useState(0);
  const [isHovering, setIsHovering] = useState(false);
  const marqueeRef = useRef<HTMLDivElement>(null);

  const logos = [
    { src: '/logos/partner-1.svg' },
    { src: '/logos/partner-2.svg' },
    { src: '/logos/partner-3.svg' },
    { src: '/logos/partner-4.svg' },
    { src: '/logos/partner-5.svg' },
    { src: '/logos/partner-1.svg' },
    { src: '/logos/partner-2.svg' },
    { src: '/logos/partner-3.svg' },
    { src: '/logos/partner-4.svg' },
    { src: '/logos/partner-5.svg' },
  ];

  useEffect(() => {
    if (isHovering) return;
    const marquee = marqueeRef.current;
    if (!marquee) return;

    let animationId: number;
    const speed = 0.5;

    const animate = () => {
      const maxScroll = marquee.scrollWidth / 2;
      setScrollX((prev) => {
        const next = prev + speed;
        return next >= maxScroll ? 0 : next;
      });
      animationId = requestAnimationFrame(animate);
    };

    animate();
    return () => cancelAnimationFrame(animationId);
  }, [isHovering]);

  return (
    <section
      className={`ls-trust-strip ${className}`}
      aria-labelledby="trust-title"
      style={{
        padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
        backgroundColor: 'var(--color-white, #FFFFFF)',
      } as React.CSSProperties}
    >
      <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' } as React.CSSProperties}>
        <header className="ls-trust-strip__header" style={{ marginBottom: 'var(--spacing-48, 48px)' } as React.CSSProperties}>
          <h2
            id="trust-title"
            className="ls-trust-strip__title"
            style={{
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-title-xl, 32pt)',
              lineHeight: 1.2,
              color: 'var(--color-navy, #070A40)',
              margin: 0,
            } as React.CSSProperties}
          >
            Trusted by Organizations Across Malawi & SADC
          </h2>
        </header>

        <div
          className="ls-trust-strip__marquee-wrapper"
          style={{
            overflow: 'hidden',
            width: '100%',
            marginBottom: 'var(--spacing-64, 64px)',
          } as React.CSSProperties}
          onMouseEnter={() => setIsHovering(true)}
          onMouseLeave={() => setIsHovering(false)}
        >
          <div
            ref={marqueeRef}
            className="ls-trust-strip__marquee"
            role="list"
            aria-label="Partner logos"
            style={{
              display: 'flex',
              gap: 'var(--spacing-64, 64px)',
              transform: `translateX(-${scrollX}px)`,
              transition: 'transform 0.1s linear',
              willChange: 'transform',
            } as React.CSSProperties}
          >
            {logos.map((logo, index) => (
              <img
                key={`${logo.src}-${index}`}
                src={logo.src}
                alt=""
                data-ls-image-type="brand-mark"
                data-ls-logo-instance="repeat"
                aria-hidden="true"
                role="listitem"
                style={{
                  height: '48px',
                  width: 'auto',
                  filter: 'grayscale(100%)',
                  opacity: 0.6,
                  transition: 'filter 0.15s ease, opacity 0.15s ease',
                  flexShrink: 0,
                } as React.CSSProperties}
                onMouseEnter={(e) => {
                  const target = e.currentTarget as HTMLElement;
                  target.style.filter = 'grayscale(0%)';
                  target.style.opacity = '1';
                }}
                onMouseLeave={(e) => {
                  const target = e.currentTarget as HTMLElement;
                  target.style.filter = 'grayscale(100%)';
                  target.style.opacity = '0.6';
                }}
                loading="lazy"
              />
            ))}
          </div>
        </div>

        <div
          className="ls-trust-strip__cases"
          role="list"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 'var(--spacing-32, 32px)',
          } as React.CSSProperties}
        >
          {caseStudies.map((study) => (
            <CaseStudyCard key={study.id} study={study} />
          ))}
        </div>
      </div>
    </section>
  );
};

const CaseStudyCard: React.FC<{ study: CaseStudy }> = ({ study }) => (
  <article
    className="ls-case-study-card"
    role="listitem"
    style={{
      backgroundColor: 'var(--color-white, #FFFFFF)',
      border: '1px solid var(--color-navy, #070A40)',
      borderRadius: 'var(--radius-medium, 8px)',
      padding: 'var(--spacing-24, 24px)',
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      minHeight: '240px',
      transition: 'box-shadow 0.2s ease, transform 0.1s ease',
    } as React.CSSProperties}
    onMouseEnter={(e) => {
      const target = e.currentTarget as HTMLElement;
      target.style.boxShadow = '0 8px 24px rgba(7, 10, 64, 0.1)';
      target.style.transform = 'translateY(-2px)';
    }}
    onMouseLeave={(e) => {
      const target = e.currentTarget as HTMLElement;
      target.style.boxShadow = 'none';
      target.style.transform = 'translateY(0)';
    }}
  >
    <div className="ls-case-study-card__logo" style={{ marginBottom: 'var(--spacing-16, 16px)' } as React.CSSProperties}>
      <img
        src={study.logo}
        alt=""
        data-ls-image-type="brand-mark"
        data-ls-logo-instance="repeat"
        aria-hidden="true"
        style={{ height: '32px', width: 'auto' } as React.CSSProperties}
        loading="lazy"
      />
    </div>
    <div
      className="ls-case-study-card__client"
      style={{
        fontFamily: 'var(--font-body, Arial)',
        fontWeight: 700,
        fontSize: 'var(--size-caption, 12pt)',
        letterSpacing: '0.08em',
        textTransform: 'uppercase',
        color: 'var(--color-grey-dark, #6B7280)',
        margin: '0 0 var(--spacing-8, 8px)',
      } as React.CSSProperties}
    >
      {study.client}
    </div>
    <h3
      className="ls-case-study-card__headline"
      style={{
        fontFamily: 'var(--font-display, Arial)',
        fontWeight: 700,
        fontSize: 'var(--size-title-sm, 18pt)',
        lineHeight: 1.3,
        color: 'var(--color-navy, #070A40)',
        margin: '0 0 var(--spacing-16, 16px)',
        flex: 1,
      } as React.CSSProperties}
    >
      {study.headline}
    </h3>
    <div className="ls-case-study-card__metric" style={{ display: 'flex', alignItems: 'baseline', gap: 'var(--spacing-8, 8px)', marginBottom: 'var(--spacing-12, 12px)' } as React.CSSProperties}>
      <span
        className="ls-case-study-card__metric-value"
        style={{
          fontFamily: 'var(--font-display, Arial)',
          fontWeight: 700,
          fontSize: 'var(--size-title-xl, 32pt)',
          lineHeight: 1,
          color: 'var(--color-red, #E63946)',
        } as React.CSSProperties}
      >
        {study.metric}
      </span>
      <span
        className="ls-case-study-card__metric-label"
        style={{
          fontFamily: 'var(--font-body, Arial)',
          fontWeight: 400,
          fontSize: 'var(--size-body, 14pt)',
          color: 'var(--color-grey-dark, #6B7280)',
        } as React.CSSProperties}
      >
        {study.metricLabel}
      </span>
    </div>
    <div
      className="ls-case-study-card__source"
      style={{
        fontFamily: 'var(--font-caption, Arial)',
        fontWeight: 400,
        fontSize: 'var(--size-caption, 12pt)',
        color: 'var(--color-grey-light-text, #9CA3AF)',
      } as React.CSSProperties}
    >
      Source: {study.source}
    </div>
  </article>
);

export default TrustStrip;
