import React from 'react';
import '../../brand/tokens/brand-tokens.css';

export const Architecture: React.FC = () => {
  return (
    <>
      <header
        className="ls-page-header"
        style={{
          backgroundColor: 'var(--color-navy, #070A40)',
          color: 'var(--color-white, #FFFFFF)',
          padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
          textAlign: 'center',
        }}
      >
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h1
            className="ls-page-header__title"
            style={{
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-display-xl, 36pt)',
              lineHeight: 1.1,
              margin: '0 0 var(--spacing-16, 16px)',
              letterSpacing: '-0.02em',
            }}
          >
            System Architecture
          </h1>
          <p
            className="ls-page-header__subtitle"
            style={{
              fontFamily: 'var(--font-body, Arial)',
              fontWeight: 400,
              fontSize: 'var(--size-body-lg, 16pt)',
              lineHeight: 1.6,
              color: 'var(--color-cyan, #00BFFF)',
              margin: 0,
            }}
          >
            How LightSpeed turns YAML into governed, auditable agent hierarchies
          </p>
        </div>
      </header>

      <main style={{ padding: 'var(--spacing-64, 64px) var(--spacing-48, 48px)' }}>
        <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' }}>
          <section
            className="ls-architecture__overview"
            style={{ marginBottom: 'var(--spacing-64, 64px)' }}
          >
            <h2
              style={{
                fontFamily: 'var(--font-display, Arial)',
                fontWeight: 700,
                fontSize: 'var(--size-title-lg, 28pt)',
                color: 'var(--color-navy, #070A40)',
                margin: '0 0 var(--spacing-24, 24px)',
              }}
            >
              Five-Layer Architecture
            </h2>
            <p
              style={{
                fontFamily: 'var(--font-body, Arial)',
                fontWeight: 400,
                fontSize: 'var(--size-body-lg, 16pt)',
                lineHeight: 1.7,
                color: 'var(--color-grey-dark, #6B7280)',
                margin: 0,
                maxWidth: '800px',
              }}
            >
              LightSpeed follows a strict separation of concerns across five layers.
              The Registry is the single source of truth. The Generator renders
              OpenCode-native agents deterministically. The Output layer produces
              deployable artifacts. The Runtime layer orchestrates execution via
              a message bus. The Governance layer enforces HITL approval gates,
              audit logging, and expiry sweeps — built in, not bolted on.
            </p>
          </section>

          <section className="ls-architecture__diagram" aria-label="Architecture diagram">
            <div
              style={{
                border: '1px solid var(--color-grey-light-text, #9CA3AF)',
                borderRadius: 'var(--radius-large, 16px)',
                overflow: 'hidden',
                backgroundColor: 'var(--color-white, #FFFFFF)',
              }}
            >
              <iframe
                src="/docs/assets/architecture.html"
                title="LightSpeed Agent Company Architecture Diagram"
                style={{
                  width: '100%',
                  height: '900px',
                  border: 'none',
                  display: 'block',
                }}
                sandbox="allow-scripts allow-same-origin"
                loading="lazy"
              />
            </div>
            <p
              style={{
                fontFamily: 'var(--font-caption, Arial)',
                fontSize: 'var(--size-caption, 12pt)',
                color: 'var(--color-grey-light-text, #9CA3AF)',
                marginTop: 'var(--spacing-16, 16px)',
                textAlign: 'center',
              }}
            >
              Interactive diagram — toggle dark/light mode, hover nodes for details.
              <a
                href="/docs/assets/architecture.html"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: 'var(--color-cyan, #00BFFF)', textDecoration: 'none', marginLeft: 'var(--spacing-8, 8px)' }}
              >
                Open fullscreen →
              </a>
            </p>
          </section>

          <section className="ls-architecture__layers" style={{ marginTop: 'var(--spacing-64, 64px)' }}>
            <h2
              style={{
                fontFamily: 'var(--font-display, Arial)',
                fontWeight: 700,
                fontSize: 'var(--size-title-lg, 28pt)',
                color: 'var(--color-navy, #070A40)',
                margin: '0 0 var(--spacing-32, 32px)',
              }}
            >
              Layer Details
            </h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: 'var(--spacing-24, 24px)',
              }}
            >
              {[
                {
                  title: '1. Registry Layer',
                  color: 'var(--color-navy, #070A40)',
                  items: [
                    'company-registry.yaml — single source of truth',
                    'All agents: id, name, tools, permissions',
                    'Version-controlled, reviewable, auditable',
                    'Pydantic models: Executive, Specialist, Department, Company',
                  ],
                },
                {
                  title: '2. Generator Layer',
                  color: 'var(--color-cyan, #00BFFF)',
                  items: [
                    'AgentGenerator reads YAML',
                    'Renders agent.md.j2 (Jinja2 template)',
                    'Deterministic, type-safe output',
                    'Zero runtime surprises',
                  ],
                },
                {
                  title: '3. Output Layer',
                  color: 'var(--color-white, #FFFFFF)',
                  border: '2px solid var(--color-navy, #070A40)',
                  items: [
                    '.opencode/agents/*.md — OpenCode-native',
                    'company/*.yaml — deployed config',
                    'mode: subagent + permission blocks',
                    'Canonical 7 tools only',
                  ],
                },
                {
                  title: '4. Runtime Layer',
                  color: 'var(--color-grey-light, #F2F2F2)',
                  items: [
                    'MessageBus — JSON task queue',
                    '.opencode/inbox.json — inbox',
                    'Executor loop: Task → Agent → Result',
                    'Concurrency-safe file locking',
                  ],
                },
                {
                  title: '5. Governance Layer',
                  color: 'var(--color-red, #E63946)',
                  textColor: 'var(--color-white, #FFFFFF)',
                  items: [
                    'ApprovalGate — HITL approval matrix',
                    'Expiry sweep: PENDING → EXPIRED',
                    'AuditLog — escalation events',
                    'Dead Letter Queue — failed tasks',
                  ],
                },
              ].map((layer, index) => (
                <article
                  key={layer.title}
                  className="ls-architecture__layer"
                  style={{
                    backgroundColor: layer.color,
                    color: layer.textColor || 'var(--color-navy, #070A40)',
                    border: layer.border || '1px solid var(--color-grey-light-text, #9CA3AF)',
                    borderRadius: 'var(--radius-medium, 8px)',
                    padding: 'var(--spacing-24, 24px)',
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <h3
                    style={{
                      fontFamily: 'var(--font-display, Arial)',
                      fontWeight: 700,
                      fontSize: 'var(--size-title-md, 24pt)',
                      margin: '0 0 var(--spacing-16, 16px)',
                    }}
                  >
                    {layer.title}
                  </h3>
                  <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 'var(--spacing-8, 8px)' }}>
                    {layer.items.map((item, i) => (
                      <li key={i} style={{ fontFamily: 'var(--font-body, Arial)', fontSize: 'var(--size-body, 14pt)', lineHeight: 1.5, display: 'flex', alignItems: 'flex-start', gap: 'var(--spacing-8, 8px)' }}>
                        <span style={{ flexShrink: 0, width: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'currentColor', marginTop: '6px' }}></span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </article>
              ))}
            </div>
          </section>

          <section className="ls-architecture__files" style={{ marginTop: 'var(--spacing-64, 64px)' }}>
            <h2
              style={{
                fontFamily: 'var(--font-display, Arial)',
                fontWeight: 700,
                fontSize: 'var(--size-title-lg, 28pt)',
                color: 'var(--color-navy, #070A40)',
                margin: '0 0 var(--spacing-24, 24px)',
              }}
            >
              Key Files
            </h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                gap: 'var(--spacing-24, 24px)',
              }}
            >
              {[
                { path: 'company-registry.yaml', desc: 'Agent registry (source of truth)', layer: 'Registry' },
                { path: 'src/ai_company/generator.py', desc: 'AgentGenerator — reads YAML, renders templates', layer: 'Generator' },
                { path: 'templates/agents/agent.md.j2', desc: 'Jinja2 template for OpenCode agents', layer: 'Generator' },
                { path: '.opencode/agents/*.md', desc: 'Generated OpenCode-native agent files', layer: 'Output' },
                { path: 'company/*.yaml', desc: 'Deployed company configuration', layer: 'Output' },
                { path: 'src/ai_company/orchestrator/message_bus.py', desc: 'MessageBus — JSON task queue', layer: 'Runtime' },
                { path: 'src/ai_company/orchestrator/executor.py', desc: 'Executor loop with governance hooks', layer: 'Runtime' },
                { path: 'src/ai_company/governance/approval_gate.py', desc: 'ApprovalGate — HITL + expiry sweep', layer: 'Governance' },
                { path: 'src/ai_company/security/rbac.py', desc: 'RBAC for dashboard API keys', layer: 'Governance' },
              ].map((file, index) => (
                <article
                  key={file.path}
                  className="ls-architecture__file"
                  style={{
                    backgroundColor: 'var(--color-white, #FFFFFF)',
                    border: '1px solid var(--color-grey-light-text, #9CA3AF)',
                    borderRadius: 'var(--radius-medium, 8px)',
                    padding: 'var(--spacing-16, 16px) var(--spacing-20, 20px)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 'var(--spacing-8, 8px)',
                  }}
                >
                  <code
                    style={{
                      fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Menlo, monospace',
                      fontSize: 'var(--size-body-sm, 13pt)',
                      color: 'var(--color-navy, #070A40)',
                      backgroundColor: 'var(--color-grey-light, #F2F2F2)',
                      padding: 'var(--spacing-4, 4px) var(--spacing-8, 8px)',
                      borderRadius: 'var(--radius-small, 4px)',
                      alignSelf: 'flex-start',
                    }}
                  >
                    {file.path}
                  </code>
                  <span
                    style={{
                      fontFamily: 'var(--font-body, Arial)',
                      fontSize: 'var(--size-body-sm, 13pt)',
                      color: 'var(--color-grey-dark, #6B7280)',
                      flex: 1,
                    }}
                  >
                    {file.desc}
                  </span>
                  <span
                    style={{
                      fontFamily: 'var(--font-display, Arial)',
                      fontWeight: 700,
                      fontSize: 'var(--size-caption, 12pt)',
                      color: 'var(--color-cyan, #00BFFF)',
                      backgroundColor: 'rgba(0, 191, 255, 0.1)',
                      padding: 'var(--spacing-4, 4px) var(--spacing-8, 8px)',
                      borderRadius: 'var(--radius-small, 4px)',
                      alignSelf: 'flex-start',
                    }}
                  >
                    {file.layer}
                  </span>
                </article>
              ))}
            </div>
          </section>
        </div>
      </main>

      <footer
        style={{
          backgroundColor: 'var(--color-navy, #070A40)',
          color: 'var(--color-white, #FFFFFF)',
          padding: 'var(--spacing-48, 48px)',
          textAlign: 'center',
        }}
      >
        <p style={{ fontFamily: 'var(--font-caption, Arial)', fontSize: 'var(--size-caption, 12pt)', color: 'var(--color-grey-light-text, #9CA3AF)', margin: 0 }}>
          LightSpeed Holdings Limited™ &copy; {new Date().getFullYear()} — <a href="/" style={{ color: 'var(--color-cyan, #00BFFF)' }}>lightspeedholdings.com</a>
        </p>
      </footer>
    </>
  );
};

export default Architecture;
