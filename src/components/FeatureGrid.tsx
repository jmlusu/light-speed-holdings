import React from 'react';
import { FileText, GitMerge, Server } from 'lucide-react';
import { FeatureCard } from './FeatureCard';
import '../../brand/tokens/brand-tokens.css';

const features = [
  {
    title: 'Registry (YAML)',
    icon: <FileText width={32} height={32} aria-hidden="true" />,
    body: 'Single source of truth for all agents: id, name, tools, permissions. Version-controlled, reviewable, auditable.',
    href: '/docs/registry',
  },
  {
    title: 'Generator (Jinja2)',
    icon: <GitMerge width={32} height={32} aria-hidden="true" />,
    body: 'Renders OpenCode-native markdown agents from registry. Deterministic, type-safe, zero runtime surprises.',
    badge: 'Open Source',
    href: '/docs/generator',
  },
  {
    title: 'Orchestrator (MessageBus)',
    icon: <Server width={32} height={32} aria-hidden="true" />,
    body: 'JSON-based task queue at .opencode/inbox.json. Executor loop with HITL approval gates, audit logging, dead-letter handling.',
    href: '/docs/orchestrator',
  },
];

interface FeatureGridProps {
  className?: string;
}

export const FeatureGrid: React.FC<FeatureGridProps> = ({ className = '' }) => {
  return (
    <section
      className={`ls-feature-grid ${className}`}
      aria-labelledby="features-title"
      style={{
        padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
        backgroundColor: 'var(--color-grey-light, #F2F2F2)',
      } as React.CSSProperties}
    >
      <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' } as React.CSSProperties}>
        <header className="ls-feature-grid__header" style={{ textAlign: 'center', marginBottom: 'var(--spacing-64, 64px)' } as React.CSSProperties}>
          <h2
            id="features-title"
            className="ls-feature-grid__title"
            style={{
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-title-xl, 32pt)',
              lineHeight: 1.2,
              color: 'var(--color-navy, #070A40)',
              margin: '0 0 var(--spacing-16, 16px)',
            } as React.CSSProperties}
          >
            Three Pillars of Agentic Governance
          </h2>
          <p
            className="ls-feature-grid__subtitle"
            style={{
              fontFamily: 'var(--font-body, Arial)',
              fontWeight: 400,
              fontSize: 'var(--size-body-lg, 16pt)',
              lineHeight: 1.6,
              color: 'var(--color-grey-dark, #6B7280)',
              margin: 0,
              maxWidth: '600px',
              marginLeft: 'auto',
              marginRight: 'auto',
            } as React.CSSProperties}
          >
            Registry → Generator → Orchestrator: the three primitives that make agent hierarchies production-ready
          </p>
        </header>

        <div
          className="ls-feature-grid__grid"
          role="list"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 'var(--spacing-32, 32px)',
          } as React.CSSProperties}
        >
          {features.map((feature, index) => (
            <FeatureCard
              key={feature.title}
              title={feature.title}
              icon={feature.icon}
              body={feature.body}
              badge={feature.badge}
              href={feature.href}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeatureGrid;
