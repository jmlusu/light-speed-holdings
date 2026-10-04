import React, { useState, useRef, useEffect } from 'react';
import '../../brand/tokens/brand-tokens.css';

interface PlaygroundProps {
  className?: string;
}

const commands = [
  {
    id: 'generate',
    prompt: 'ai-company generate',
    output: [
      { type: 'info', text: 'Reading registry: company-registry.yaml' },
      { type: 'info', text: 'Found 37 agents in registry' },
      { type: 'info', text: 'Rendering templates via Jinja2...' },
      { type: 'success', text: 'Generated .opencode/agents/ceo.md' },
      { type: 'success', text: 'Generated .opencode/agents/cto.md' },
      { type: 'success', text: 'Generated .opencode/agents/cmo.md' },
      { type: 'success', text: '... 34 more agents generated' },
      { type: 'success', text: 'Generated company/*.yaml configs' },
      { type: 'info', text: '✓ All agents written to .opencode/agents/' },
    ],
  },
  {
    id: 'validate',
    prompt: 'ai-company validate',
    output: [
      { type: 'info', text: 'Validating agent registry...' },
      { type: 'info', text: 'Checking YAML syntax...' },
      { type: 'success', text: '✓ YAML syntax valid' },
      { type: 'info', text: 'Running type checks (mypy)...' },
      { type: 'success', text: '✓ 100% type coverage' },
      { type: 'info', text: 'Checking permissions & tool vocab...' },
      { type: 'success', text: '✓ All tools canonical (read, edit, grep, list, bash, webfetch, task)' },
      { type: 'info', text: 'Validating OpenCode format...' },
      { type: 'success', text: '✓ All agents OpenCode-native' },
    ],
  },
  {
    id: 'deploy',
    prompt: 'ai-company deploy --dry-run',
    output: [
      { type: 'info', text: 'Preparing deployment (dry-run)...' },
      { type: 'info', text: 'Checking governance layer...' },
      { type: 'success', text: '✓ ApprovalGate configured (HITL + Expiry Sweep)' },
      { type: 'success', text: '✓ AuditLog enabled' },
      { type: 'success', text: '✓ Dead Letter Queue configured' },
      { type: 'info', text: 'Verifying MessageBus connectivity...' },
      { type: 'success', text: '✓ .opencode/inbox.json accessible' },
      { type: 'info', text: 'Cost estimation...' },
      { type: 'info', text: 'Estimated monthly: $47.32 (37 agents)' },
      { type: 'success', text: '✓ Dry-run complete — ready to deploy' },
    ],
  },
];

interface OutputLine {
  type: string;
  text: string;
}

const TerminalSimulator: React.FC = () => {
  const [activeCommand, setActiveCommand] = useState<string | null>(null);
  const [outputLines, setOutputLines] = useState<OutputLine[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const terminalRef = useRef<HTMLDivElement>(null);

  const runCommand = (cmd: typeof commands[0]) => {
    setActiveCommand(cmd.id);
    setOutputLines([]);
    setIsRunning(true);

    let delay = 0;
    cmd.output.forEach((line, index) => {
      delay += index === 0 ? 300 : 150 + Math.random() * 200;
      setTimeout(() => {
        setOutputLines((prev) => [...prev, line]);
        if (index === cmd.output.length - 1) {
          setIsRunning(false);
        }
      }, delay);
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.key === 'Enter' || e.key === ' ') && !isRunning) {
      const cmd = commands.find((c) => c.id === activeCommand);
      if (cmd) runCommand(cmd);
    }
  };

  return (
    <div
      className="ls-terminal"
      style={{
        backgroundColor: 'var(--color-navy, #070A40)',
        borderRadius: 'var(--radius-medium, 8px)',
        overflow: 'hidden',
        fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Menlo, monospace',
        fontSize: '14px',
        lineHeight: 1.6,
        color: 'var(--color-grey-light-text, #9CA3AF)',
        boxShadow: '0 8px 32px rgba(7, 10, 64, 0.3)',
        border: '1px solid var(--color-grey-dark, #6B7280)',
        height: '400px',
        display: 'flex',
        flexDirection: 'column',
      } as React.CSSProperties}
    >
      <div
        className="ls-terminal__header"
        style={{
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
          borderBottom: '1px solid var(--color-grey-dark, #6B7280)',
          padding: 'var(--spacing-8, 8px) var(--spacing-12, 12px)',
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-8, 8px)',
        } as React.CSSProperties}
      >
        <div style={{ display: 'flex', gap: 'var(--spacing-6, 6px)' } as React.CSSProperties}>
          <span style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#FF5F57' } as React.CSSProperties}></span>
          <span style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#FEBC2E' } as React.CSSProperties}></span>
          <span style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#28CA42' } as React.CSSProperties}></span>
        </div>
        <span style={{ fontSize: '12px', color: 'var(--color-grey-light-text, #9CA3AF)', marginLeft: 'var(--spacing-12, 12px)', flex: 1 } as React.CSSProperties}>
          λ ~/light-speed-holdings
        </span>
      </div>

      <div
        ref={terminalRef}
        className="ls-terminal__output"
        role="log"
        aria-live="polite"
        aria-label="Terminal output"
        style={{
          flex: 1,
          padding: 'var(--spacing-16, 16px)',
          overflowY: 'auto',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        } as React.CSSProperties}
      >
        {outputLines.length === 0 && !isRunning && (
          <div style={{ opacity: 0.5 } as React.CSSProperties}>
            <div>Welcome to LightSpeed Holdings CLI</div>
            <div>Press Enter on a command below to simulate</div>
          </div>
        )}
        {outputLines.map((line, index) => (
          <div
            key={index}
            className={`ls-terminal__line ls-terminal__line--${line.type}`}
            style={{
              marginBottom: 'var(--spacing-4, 4px)',
              color:
                line.type === 'success'
                  ? '#10B981'
                  : line.type === 'error'
                  ? 'var(--color-red, #E63946)'
                  : line.type === 'info'
                  ? 'var(--color-cyan, #00BFFF)'
                  : 'var(--color-grey-light-text, #9CA3AF)',
              animation: 'fadeIn 0.2s ease',
            } as React.CSSProperties}
          >
            {line.text}
          </div>
        ))}
        {isRunning && (
          <div className="ls-terminal__cursor" style={{ display: 'inline-block', animation: 'blink 1s infinite' } as React.CSSProperties}>
            █
          </div>
        )}
      </div>

      <div
        className="ls-terminal__commands"
        role="tablist"
        aria-label="Available commands"
        style={{
          display: 'flex',
          gap: 'var(--spacing-8, 8px)',
          padding: 'var(--spacing-12, 12px)',
          borderTop: '1px solid var(--color-grey-dark, #6B7280)',
          backgroundColor: 'rgba(0, 0, 0, 0.2)',
          flexWrap: 'wrap',
        } as React.CSSProperties}
      >
        {commands.map((cmd) => (
          <button
            key={cmd.id}
            role="tab"
            aria-selected={activeCommand === cmd.id}
            aria-controls={`panel-${cmd.id}`}
            id={`tab-${cmd.id}`}
            onClick={() => !isRunning && runCommand(cmd)}
            onKeyDown={handleKeyDown}
            tabIndex={activeCommand === cmd.id ? 0 : -1}
            disabled={isRunning}
            style={{
              fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Menlo, monospace',
              fontSize: '12px',
              padding: 'var(--spacing-6, 6px) var(--spacing-12, 12px)',
              borderRadius: 'var(--radius-small, 4px)',
              border: `1px solid ${
                activeCommand === cmd.id
                  ? 'var(--color-cyan, #00BFFF)'
                  : 'var(--color-grey-dark, #6B7280)'
              }`,
              backgroundColor: activeCommand === cmd.id
                ? 'rgba(0, 191, 255, 0.15)'
                : 'transparent',
              color: activeCommand === cmd.id
                ? 'var(--color-cyan, #00BFFF)'
                : 'var(--color-grey-light-text, #9CA3AF)',
              cursor: isRunning ? 'not-allowed' : 'pointer',
              transition: 'all 0.15s ease',
              opacity: isRunning && activeCommand !== cmd.id ? 0.5 : 1,
            } as React.CSSProperties}
            onMouseEnter={(e) => {
              if (!isRunning && activeCommand !== cmd.id) {
                const target = e.currentTarget as HTMLElement;
                target.style.borderColor = 'var(--color-cyan, #00BFFF)';
                target.style.color = 'var(--color-cyan, #00BFFF)';
              }
            }}
            onMouseLeave={(e) => {
              if (activeCommand !== cmd.id) {
                const target = e.currentTarget as HTMLElement;
                target.style.borderColor = 'var(--color-grey-dark, #6B7280)';
                target.style.color = 'var(--color-grey-light-text, #9CA3AF)';
              }
            }}
          >
            {cmd.prompt}
          </button>
        ))}
      </div>
    </div>
  );
};

export const Playground: React.FC<PlaygroundProps> = ({ className = '' }) => {
  return (
    <section
      className={`ls-playground ${className}`}
      aria-labelledby="playground-title"
      style={{
        padding: 'var(--spacing-96, 96px) var(--spacing-48, 48px)',
        backgroundColor: 'var(--color-white, #FFFFFF)',
      } as React.CSSProperties}
    >
      <div style={{ maxWidth: 'var(--layout-web-max-width, 1200px)', margin: '0 auto' } as React.CSSProperties}>
        <header className="ls-playground__header" style={{ marginBottom: 'var(--spacing-48, 48px)', textAlign: 'center' } as React.CSSProperties}>
          <h2
            id="playground-title"
            className="ls-playground__title"
            style={{
              fontFamily: 'var(--font-display, Arial)',
              fontWeight: 700,
              fontSize: 'var(--size-title-xl, 32pt)',
              lineHeight: 1.2,
              color: 'var(--color-navy, #070A40)',
              margin: '0 0 var(--spacing-16, 16px)',
            } as React.CSSProperties}
          >
            Try It Live
          </h2>
          <p
            className="ls-playground__subtitle"
            style={{
              fontFamily: 'var(--font-body, Arial)',
              fontWeight: 400,
              fontSize: 'var(--size-body-lg, 16pt)',
              lineHeight: 1.6,
              color: 'var(--color-grey-dark, #6B7280)',
              margin: '0 0 var(--spacing-32, 32px)',
              maxWidth: '600px',
              marginLeft: 'auto',
              marginRight: 'auto',
            } as React.CSSProperties}
          >
            The CLI is the product. See <code style={{ color: 'var(--color-navy, #070A40)', background: 'var(--color-grey-light, #F2F2F2)', padding: '2px 6px', borderRadius: '4px', fontFamily: 'inherit' }}>ai-company generate</code>, <code style={{ color: 'var(--color-navy, #070A40)', background: 'var(--color-grey-light, #F2F2F2)', padding: '2px 6px', borderRadius: '4px', fontFamily: 'inherit' }}>validate</code>, and <code style={{ color: 'var(--color-navy, #070A40)', background: 'var(--color-grey-light, #F2F2F2)', padding: '2px 6px', borderRadius: '4px', fontFamily: 'inherit' }}>deploy</code> in action.
          </p>
        </header>

        <div
          className="ls-playground__content"
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: 'var(--spacing-48, 48px)',
            alignItems: 'start',
          } as React.CSSProperties}
        >
          <div className="ls-playground__terminal">
            <TerminalSimulator />
          </div>

          <div className="ls-playground__preview">
            <h3
              className="ls-playground__preview-title"
              style={{
                fontFamily: 'var(--font-display, Arial)',
                fontWeight: 700,
                fontSize: 'var(--size-title-md, 24pt)',
                lineHeight: 1.3,
                color: 'var(--color-navy, #070A40)',
                margin: '0 0 var(--spacing-16, 16px)',
              } as React.CSSProperties}
            >
              What You'll See
            </h3>
            <div
              className="ls-playground__tree"
              style={{
                backgroundColor: 'var(--color-navy, #070A40)',
                borderRadius: 'var(--radius-medium, 8px)',
                padding: 'var(--spacing-24, 24px)',
                fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Menlo, monospace',
                fontSize: '13px',
                lineHeight: 1.8,
                color: 'var(--color-white, #FFFFFF)',
                overflowX: 'auto',
              } as React.CSSProperties}
            >
              <pre style={{ margin: 0 } as React.CSSProperties}>
{`📁 .opencode/
└── 📁 agents/
    ├── 📄 ceo.md
    ├── 📄 cto.md
    ├── 📄 cmo.md
    ├── 📄 cfo.md
    ├── 📄 ciso.md
    ├── 📄 caio.md
    ├── 📄 orchestration-owner.md
    ├── 📄 registry-owner.md
    ├── 📄 ... (37 total)
    └── 📄 approval-gate.md

📁 company/
    ├── 📄 departments.yaml
    ├── 📄 executives.yaml
    ├── 📄 specialists.yaml
    └── 📄 permissions.yaml`}
              </pre>
            </div>
            <ul
              className="ls-playground__highlights"
              style={{
                listStyle: 'none',
                padding: 0,
                margin: 'var(--spacing-24, 24px) 0 0',
                display: 'flex',
                flexDirection: 'column',
                gap: 'var(--spacing-12, 12px)',
              } as React.CSSProperties}
            >
              <li style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-12, 12px)', color: 'var(--color-grey-dark, #6B7280)' } as React.CSSProperties}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--color-cyan, #00BFFF)', flexShrink: 0 } as React.CSSProperties}></span>
                Type-safe markdown with Pydantic models
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-12, 12px)', color: 'var(--color-grey-dark, #6B7280)' } as React.CSSProperties}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--color-cyan, #00BFFF)', flexShrink: 0 } as React.CSSProperties}></span>
                Permission blocks (read, edit, grep, list, bash, webfetch, task)
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-12, 12px)', color: 'var(--color-grey-dark, #6B7280)' } as React.CSSProperties}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--color-cyan, #00BFFF)', flexShrink: 0 } as React.CSSProperties}></span>
                OpenCode-native subagent format
              </li>
            </ul>

            <div
              className="ls-playground__install"
              style={{
                marginTop: 'var(--spacing-32, 32px)',
                padding: 'var(--spacing-24, 24px)',
                backgroundColor: 'var(--color-navy, #070A40)',
                borderRadius: 'var(--radius-medium, 8px)',
                textAlign: 'center',
              } as React.CSSProperties}
            >
              <code
                style={{
                  fontFamily: '"JetBrains Mono", "Fira Code", "SF Mono", Menlo, monospace',
                  fontSize: 'var(--size-body, 14pt)',
                  color: 'var(--color-cyan, #00BFFF)',
                  display: 'block',
                  marginBottom: 'var(--spacing-16, 16px)',
                } as React.CSSProperties}
              >
                uvx ai-company
              </code>
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
                  backgroundColor: 'var(--color-red, #E63946)',
                  borderRadius: 'var(--radius-medium, 8px)',
                  textDecoration: 'none',
                  transition: 'background-color 0.2s ease, transform 0.1s ease',
                  border: 'none',
                  cursor: 'pointer',
                } as React.CSSProperties}
                onMouseEnter={(e) => {
                  const target = e.currentTarget as HTMLElement;
                  target.style.backgroundColor = '#c02d3a';
                  target.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  const target = e.currentTarget as HTMLElement;
                  target.style.backgroundColor = 'var(--color-red, #E63946)';
                  target.style.transform = 'translateY(0)';
                }}
              >
                Install & Try
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Playground;
