import React from 'react';
import '../../brand/tokens/brand-tokens.css';

interface HeroProps {
  className?: string;
}

const nodes = [
  { id: 'yaml', label: 'company-registry.yaml', sub: 'Source of Truth', color: 'var(--color-navy, #070A40)', textColor: 'var(--color-white, #FFFFFF)', x: 50, y: 100 },
  { id: 'gen', label: 'AgentGenerator', sub: 'Reads YAML → Renders agent.md.j2', color: 'var(--color-cyan, #00BFFF)', textColor: 'var(--color-navy, #070A40)', x: 50, y: 220 },
  { id: 'md', label: '.opencode/agents/*.md', sub: 'OpenCode-native', color: 'var(--color-white, #FFFFFF)', textColor: 'var(--color-navy, #070A40)', border: '2px solid var(--color-navy, #070A40)', x: 180, y: 340 },
  { id: 'yamlOut', label: 'company/*.yaml', sub: 'Deployed config', color: 'var(--color-white, #FFFFFF)', textColor: 'var(--color-navy, #070A40)', border: '2px solid var(--color-navy, #070A40)', x: 320, y: 340 },
  { id: 'bus', label: 'MessageBus', sub: '.opencode/inbox.json', color: 'var(--color-grey-light, #F2F2F2)', textColor: 'var(--color-navy, #070A40)', border: '1px solid var(--color-grey-dark, #6B7280)', x: 250, y: 460 },
  { id: 'exec', label: 'Executor Loop', sub: 'Task → Agent → Result', color: 'var(--color-grey-light, #F2F2F2)', textColor: 'var(--color-navy, #070A40)', border: '1px solid var(--color-grey-dark, #6B7280)', x: 250, y: 580 },
  { id: 'gate', label: 'ApprovalGate', sub: 'HITL + Expiry Sweep', color: 'var(--color-red, #E63946)', textColor: 'var(--color-white, #FFFFFF)', x: 250, y: 700 },
  { id: 'audit', label: 'AuditLog', sub: 'Escalation Events', color: 'var(--color-grey-light, #F2F2F2)', textColor: 'var(--color-navy, #070A40)', border: '1px solid var(--color-grey-dark, #6B7280)', x: 100, y: 820 },
  { id: 'dlq', label: 'Dead Letter Queue', sub: 'Failed Tasks', color: 'var(--color-grey-light, #F2F2F2)', textColor: 'var(--color-red, #E63946)', border: '2px solid var(--color-red, #E63946)', x: 400, y: 820 },
];

const edges = [
  { from: 'yaml', to: 'gen' },
  { from: 'gen', to: 'md' },
  { from: 'gen', to: 'yamlOut' },
  { from: 'md', to: 'bus' },
  { from: 'yamlOut', to: 'bus' },
  { from: 'bus', to: 'exec' },
  { from: 'exec', to: 'gate' },
  { from: 'gate', to: 'audit' },
  { from: 'exec', to: 'dlq', dashed: true },
];

const getNodeStyle = (node: typeof nodes[0]): React.CSSProperties => ({
  position: 'absolute',
  left: `${node.x}px`,
  top: `${node.y}px`,
  transform: 'translateX(-50%)',
  backgroundColor: node.color,
  color: node.textColor,
  border: node.border || 'none',
  borderRadius: 'var(--radius-medium, 8px)',
  padding: 'var(--spacing-12, 12px) var(--spacing-16, 16px)',
  minWidth: '180px',
  textAlign: 'center',
  fontFamily: 'var(--font-body, Arial)',
  fontSize: 'var(--size-body-sm, 13pt)',
  lineHeight: 1.3,
  boxShadow: '0 4px 12px rgba(7, 10, 64, 0.15)',
  zIndex: 10,
});

export const Hero: React.FC<HeroProps> = ({ className = '' }) => {
  return (
    <section
      className={`ls-hero ${className}`}
      aria-labelledby="hero-title"
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: 'var(--spacing-96, 96px)',
        alignItems: 'center',
        padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
        maxWidth: 'var(--layout-web-max-width, 1200px)',
        margin: '0 auto',
        minHeight: '600px',
        backgroundColor: 'var(--color-white, #FFFFFF)',
      } as React.CSSProperties}
    >
      <div className="ls-hero__content" style={{ maxWidth: '540px' } as React.CSSProperties}>
        <h1
          id="hero-title"
          className="ls-hero__headline"
          style={{
            fontFamily: 'var(--font-display, Arial)',
            fontWeight: 700,
            fontSize: 'var(--size-display-xl, 36pt)',
            lineHeight: 1.1,
            color: 'var(--color-navy, #070A40)',
            marginBottom: 'var(--spacing-24, 24px)',
            letterSpacing: '-0.02em',
          } as React.CSSProperties}
        >
          Build Your Agent Company
        </h1>
        <p
          className="ls-hero__subhead"
          style={{
            fontFamily: 'var(--font-body, Arial)',
            fontWeight: 400,
            fontSize: 'var(--size-title-sm, 18pt)',
            lineHeight: 1.5,
            color: 'var(--color-grey-dark, #6B7280)',
            marginBottom: 'var(--spacing-32, 32px)',
          } as React.CSSProperties}
        >
          YAML-defined. Type-safe. Auditable. Deploy hierarchies of AI agents with governance built in.
        </p>
        <div className="ls-hero__cta-group" style={{ display: 'flex', gap: 'var(--spacing-16, 16px)', flexWrap: 'wrap' } as React.CSSProperties}>
          <a
            href="/build"
            className="ls-btn ls-btn--primary"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 'var(--spacing-12, 12px) var(--spacing-24, 24px)',
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-subtitle, 16pt)',
              color: 'var(--color-white, #FFFFFF)',
              backgroundColor: 'var(--color-navy, #070A40)',
              borderRadius: 'var(--radius-medium, 8px)',
              textDecoration: 'none',
              transition: 'background-color 0.2s ease, transform 0.1s ease',
              border: 'none',
              cursor: 'pointer',
            } as React.CSSProperties}
            onMouseEnter={(e) => {
              const target = e.currentTarget as HTMLElement;
              target.style.backgroundColor = 'var(--color-red, #E63946)';
              target.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              const target = e.currentTarget as HTMLElement;
              target.style.backgroundColor = 'var(--color-navy, #070A40)';
              target.style.transform = 'translateY(0)';
            }}
          >
            Start Free →
          </a>
          <a
            href="/architecture"
            className="ls-btn ls-btn--secondary"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 'var(--spacing-12, 12px) var(--spacing-24, 24px)',
              fontFamily: 'var(--font-body, Arial)',
              fontWeight: 400,
              fontSize: 'var(--size-subtitle, 16pt)',
              color: 'var(--color-cyan, #00BFFF)',
              backgroundColor: 'transparent',
              border: '2px solid var(--color-cyan, #00BFFF)',
              borderRadius: 'var(--radius-medium, 8px)',
              textDecoration: 'none',
              transition: 'background-color 0.2s ease, color 0.2s ease',
              cursor: 'pointer',
            } as React.CSSProperties}
            onMouseEnter={(e) => {
              const target = e.currentTarget as HTMLElement;
              target.style.backgroundColor = 'var(--color-cyan, #00BFFF)';
              target.style.color = 'var(--color-navy, #070A40)';
            }}
            onMouseLeave={(e) => {
              const target = e.currentTarget as HTMLElement;
              target.style.backgroundColor = 'transparent';
              target.style.color = 'var(--color-cyan, #00BFFF)';
            }}
          >
            View Architecture
          </a>
        </div>
      </div>

      <div
        className="ls-hero__diagram"
        role="img"
        aria-label="LightSpeed Agent Company Architecture: Registry Layer (YAML) → Generator Layer (Jinja2) → Output Layer (OpenCode Agents) → Runtime Layer (MessageBus) → Governance Layer (ApprovalGate)"
        style={{
          backgroundColor: 'var(--color-grey-light, #F2F2F2)',
          border: '1px solid var(--color-grey-light-text, #9CA3AF)',
          borderRadius: 'var(--radius-large, 16px)',
          padding: 'var(--spacing-48, 48px)',
          minHeight: '400px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'auto',
        } as React.CSSProperties}
      >
        <div
          className="ls-architecture-diagram"
          style={{
            position: 'relative',
            width: '100%',
            maxWidth: '600px',
            height: '920px',
            margin: '0 auto',
          } as React.CSSProperties}
        >
          <svg
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              pointerEvents: 'none',
              zIndex: 1,
            } as React.CSSProperties}
            preserveAspectRatio="none"
            viewBox="0 0 600 920"
          >
            <defs>
              <marker
                id="arrowhead"
                markerWidth={10}
                markerHeight={7}
                refX={9}
                refY={3.5}
                orient="auto"
              >
                <polygon points="0 0, 10 3.5, 0 7" fill="var(--color-grey-dark, #6B7280)" />
              </marker>
            </defs>
            {edges.map((edge, i) => {
              const fromNode = nodes.find(n => n.id === edge.from)!;
              const toNode = nodes.find(n => n.id === edge.to)!;
              const fromX = fromNode.x;
              const fromY = fromNode.y + 60;
              const toX = toNode.x;
              const toY = toNode.y;
              const midY = (fromY + toY) / 2;
              return (
                <g key={i}>
                  <path
                    d={`M${fromX} ${fromY} C${fromX} ${midY} ${toX} ${midY} ${toX} ${toY}`}
                    stroke="var(--color-grey-dark, #6B7280)"
                    strokeWidth={edge.dashed ? 1.5 : 2}
                    strokeDasharray={edge.dashed ? '8,4' : 'none'}
                    fill="none"
                    markerEnd="url(#arrowhead)"
                  />
                </g>
              );
            })}
          </svg>

          {nodes.map(node => (
            <div key={node.id} style={getNodeStyle(node)}>
              <div style={{ fontWeight: 700, marginBottom: 'var(--spacing-4, 4px)', fontSize: 'var(--size-body, 14pt)' } as React.CSSProperties}>
                {node.label}
              </div>
              <div style={{ fontSize: 'var(--size-caption, 12pt)', opacity: 0.8 } as React.CSSProperties}>
                {node.sub}
              </div>
            </div>
          ))}

          <div
            className="ls-diagram-legend"
            style={{
              position: 'absolute',
              bottom: 'var(--spacing-24, 24px)',
              left: '50%',
              transform: 'translateX(-50%)',
              display: 'flex',
              flexWrap: 'wrap',
              gap: 'var(--spacing-16, 16px) var(--spacing-32, 32px)',
              justifyContent: 'center',
              fontSize: 'var(--size-caption, 12pt)',
              color: 'var(--color-grey-dark, #6B7280)',
              fontFamily: 'var(--font-body, Arial)',
            } as React.CSSProperties}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
              <span style={{ width: '12px', height: '12px', borderRadius: '4px', background: 'var(--color-navy, #070A40)' } as React.CSSProperties}></span>
              Registry Layer
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
              <span style={{ width: '12px', height: '12px', borderRadius: '4px', background: 'var(--color-cyan, #00BFFF)' } as React.CSSProperties}></span>
              Generator Layer
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
              <span style={{ width: '12px', height: '12px', borderRadius: '4px', background: 'var(--color-white, #FFFFFF)', border: '1px solid var(--color-navy, #070A40)' } as React.CSSProperties}></span>
              Output Layer
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
              <span style={{ width: '12px', height: '12px', borderRadius: '4px', background: 'var(--color-grey-light, #F2F2F2)', border: '1px solid var(--color-grey-dark, #6B7280)' } as React.CSSProperties}></span>
              Runtime Layer
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
              <span style={{ width: '12px', height: '12px', borderRadius: '4px', background: 'var(--color-red, #E63946)' } as React.CSSProperties}></span>
              Governance Layer
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-8, 8px)' } as React.CSSProperties}>
              <span style={{ width: '12px', height: '12px', borderRadius: '4px', background: 'var(--color-grey-light, #F2F2F2)', border: '2px solid var(--color-red, #E63946)' } as React.CSSProperties}></span>
              Dead Letter Queue
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
