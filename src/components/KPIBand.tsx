import React, { useEffect, useRef, useState } from 'react';
import '../../brand/tokens/brand-tokens.css';

interface KPIMetric {
  id: string;
  value: number;
  target: number;
  label: string;
  suffix?: string;
  prefix?: string;
  source: string;
}

const metrics: KPIMetric[] = [
  {
    id: 'agents',
    value: 0,
    target: 37,
    label: 'Agents Registered',
    source: 'company-registry.yaml',
  },
  {
    id: 'deploy-time',
    value: 0,
    target: 5,
    label: 'Deploy Time (min)',
    prefix: '<',
    source: 'Generator benchmarks',
  },
  {
    id: 'declarative',
    value: 0,
    target: 90,
    label: 'Declarative Config',
    suffix: '%',
    source: 'Architecture docs',
  },
  {
    id: 'type-coverage',
    value: 0,
    target: 100,
    label: 'Type Coverage',
    suffix: '%',
    source: 'mypy/ruff CI',
  },
];

interface KPIBandProps {
  className?: string;
}

export const KPIBand: React.FC<KPIBandProps> = ({ className = '' }) => {
  const [animatedValues, setAnimatedValues] = useState<number[]>([0, 0, 0, 0]);
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !isVisible) {
            setIsVisible(true);
            observer.disconnect();
          }
        });
      },
      { threshold: 0.3, rootMargin: '0px 0px -100px 0px' }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, [isVisible]);

  useEffect(() => {
    if (!isVisible) return;

    const duration = 1800;
    const startTime = Date.now();

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);

      setAnimatedValues(
        metrics.map((m) => {
          if (m.id === 'deploy-time') {
            return Math.max(m.target - eased * m.target, 0);
          }
          return Math.round(eased * m.target);
        })
      );

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [isVisible]);

  return (
    <section
      ref={sectionRef}
      className={`ls-kpi-band ${className}`}
      aria-label="Key performance indicators"
      style={{
        backgroundColor: 'var(--color-navy, #070A40)',
        padding: 'var(--spacing-32, 32px) var(--spacing-48, 48px)',
      } as React.CSSProperties}
    >
      <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' } as React.CSSProperties}>
        <div
          className="ls-kpi-band__grid"
          role="list"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: 'var(--spacing-32, 32px)',
            alignItems: 'center',
          } as React.CSSProperties}
        >
          {metrics.map((metric, index) => (
            <div
              key={metric.id}
              className="ls-kpi-band__item"
              role="listitem"
              style={{
                textAlign: 'center',
                position: 'relative',
              } as React.CSSProperties}
            >
              {index < metrics.length - 1 && (
                <div
                  className="ls-kpi-band__divider"
                  style={{
                    position: 'absolute',
                    right: 'calc(-1 * var(--spacing-32, 32px) / 2)',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    width: '32px',
                    height: '2px',
                    backgroundColor: 'var(--color-red, #E63946)',
                    borderRadius: '2px',
                  } as React.CSSProperties}
                  aria-hidden="true"
                />
              )}
              <div
                className="ls-kpi-band__value"
                style={{
                  fontFamily: 'var(--font-display, Arial)',
                  fontWeight: 700,
                  fontSize: 'var(--size-display-xl, 36pt)',
                  lineHeight: 1,
                  color: 'var(--color-white, #FFFFFF)',
                  marginBottom: 'var(--spacing-8, 8px)',
                  fontVariantNumeric: 'tabular-nums',
                } as React.CSSProperties}
                aria-live="polite"
              >
                {metric.prefix || ''}
                {metric.id === 'deploy-time'
                  ? animatedValues[index].toFixed(1)
                  : animatedValues[index].toLocaleString()}
                {metric.suffix || ''}
              </div>
              <div
                className="ls-kpi-band__label"
                style={{
                  fontFamily: 'var(--font-body, Arial)',
                  fontWeight: 400,
                  fontSize: 'var(--size-title-sm, 18pt)',
                  lineHeight: 1.3,
                  color: 'var(--color-cyan, #00BFFF)',
                  marginBottom: 'var(--spacing-4, 4px)',
                } as React.CSSProperties}
              >
                {metric.label}
              </div>
              <div
                className="ls-kpi-band__source"
                style={{
                  fontFamily: 'var(--font-caption, Arial)',
                  fontWeight: 400,
                  fontSize: 'var(--size-caption, 12pt)',
                  lineHeight: 1.4,
                  color: 'var(--color-grey-light-text, #9CA3AF)',
                } as React.CSSProperties}
              >
                Source: {metric.source}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default KPIBand;
