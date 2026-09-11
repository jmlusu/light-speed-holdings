import React, { useEffect, useRef, useState } from 'react';

interface StatCounterProps {
  to: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  format?: 'plain' | 'comma';
  decimals?: number;
  className?: string;
}

const easeOutExpo = (t: number) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));

const formatValue = (value: number, format: 'plain' | 'comma', decimals: number) => {
  if (format === 'comma') {
    return value.toLocaleString('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: decimals > 0 ? decimals : 0,
    });
  }
  if (decimals > 0) {
    return value.toFixed(decimals);
  }
  return String(Math.round(value));
};

export const StatCounter: React.FC<StatCounterProps> = ({
  to,
  duration = 1200,
  prefix,
  suffix,
  format = 'plain',
  decimals = 0,
  className,
}) => {
  const ref = useRef<HTMLSpanElement | null>(null);
  const [displayValue, setDisplayValue] = useState(0);
  const startedRef = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setDisplayValue(to);
      return;
    }

    if (!('IntersectionObserver' in window)) {
      setDisplayValue(to);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries[0];
        if (!entry || !entry.isIntersecting || startedRef.current) return;
        startedRef.current = true;
        observer.disconnect();

        const start = performance.now();
        const animate = (now: number) => {
          const elapsed = Math.min((now - start) / duration, 1);
          setDisplayValue(to * easeOutExpo(elapsed));
          if (elapsed < 1) {
            requestAnimationFrame(animate);
          }
        };
        requestAnimationFrame(animate);
      },
      { threshold: 0.2 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [to, duration]);

  return (
    <span ref={ref} className={className}>
      {prefix}
      {formatValue(displayValue, format, decimals)}
      {suffix}
    </span>
  );
};
