import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Brain, Bot, GitBranch, HardDrive, Wrench, ShieldCheck, TrendingUp } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useInView } from '../hooks/useInView';
import { Reveal } from '../components/Reveal';
import { SiteLayout } from '../layouts/SiteLayout';
import { ArrowRight } from 'lucide-react';

interface FrameworkPageProps {
  theme: 'light' | 'dark';
}

interface LayerDef {
  id: string;
  letter: string;
  title: string;
  description: string;
}

const LAYERS: LayerDef[] = [
  {
    id: 'human',
    letter: 'H',
    title: 'H - Human Purpose & Authority',
    description:
      'People set intent, own outcomes, and hold final decision authority. Agents propose; humans decide what ships. The human is not a checkpoint at the end but the source of direction present at every layer.',
  },
  {
    id: 'agents',
    letter: 'A',
    title: 'A - Specialized Agents',
    description:
      'Agents are specialized AI roles with explicit scopes, tools, and approval thresholds. Not a single general-purpose bot. Each agent operates within a bounded context with a well-defined purpose, capabilities, and accountability boundary.',
  },
  {
    id: 'orchestration',
    letter: 'O',
    title: 'O - Deterministic Orchestration',
    description:
      'Orchestration is the deterministic routing of tasks, data, and decisions across workflows so multi-step work stays auditable end to end. Unlike probabilistic pipelines, deterministic orchestration ensures every step is traceable.',
  },
  {
    id: 'memory',
    letter: 'M',
    title: 'M - Persistent Memory',
    description:
      'Memory is persistent contextual state across long-running work, so agents recall before they act, not from a blank slate. Without memory, each interaction starts fresh, losing context and accumulated knowledge.',
  },
  {
    id: 'tools',
    letter: 'T',
    title: 'T - Isolated Tools',
    description:
      'Tools are isolated execution environments for APIs, data, and actions: the only way agents touch the outside world. Isolation ensures agent actions are contained, side effects are bounded, and failures do not cascade.',
  },
  {
    id: 'governance',
    letter: 'G',
    title: 'G - Five-Tier Governance',
    description:
      'Governance is a control layer woven through the model: five-tier human approval, append-only audit receipts, and risk-classified actions. Governance is not a final checkpoint but an integral layer — authority runs through every decision.',
  },
  {
    id: 'value',
    letter: 'V',
    title: 'V - Measured Value',
    description:
      'Value is measured business outcomes (cost, latency, quality, and adoption) fed back into strategy, not vanity metrics. Value metrics close the loop, ensuring the agentic model delivers real business results and continuously improves.',
  },
];

const FunnelDiagram: React.FC = () => {
  const totalWidth = 360;
  const stageWidth = totalWidth / 4;

  return (
    <svg
      width={totalWidth}
      height={180}
      viewBox="0 0 360 180"
      className="ls-funnel-diagram"
      aria-label="The Venture Build Process funnel diagram"
    >
      <path
        fill="none"
        stroke="currentColor"
        strokeWidth={2}
        d="M 20 160 C 100 20, 260 20, 340 160 L 340 20 C 260 140, 100 140, 20 20 Z"
      />
      <line
        x1={20}
        y1={40}
        x2={20}
        y2={160}
        stroke="currentColor"
        strokeWidth={1}
        opacity={0.5}
      />
      <line
        x1={100}
        y1={40}
        x2={100}
        y2={160}
        stroke="currentColor"
        strokeWidth={1}
        opacity={0.5}
      />
      <line
        x1={260}
        y1={40}
        x2={260}
        y2={160}
        stroke="currentColor"
        strokeWidth={1}
        opacity={0.5}
      />
      <line
        x1={340}
        y1={40}
        x2={340}
        y2={160}
        stroke="currentColor"
        strokeWidth={1}
        opacity={0.5}
      />
      <circle cx={90} cy={100} r={8} fill="currentColor" />
      <text
        x={90}
        y={125}
        textAnchor="middle"
        fontFamily="sans-serif"
        fontSize={10}
        fill="currentColor"
      >
        Opportunity ID
      </text>
      <circle cx={190} cy={100} r={8} fill="currentColor" />
      <text
        x={190}
        y={125}
        textAnchor="middle"
        fontFamily="sans-serif"
        fontSize={10}
        fill="currentColor"
      >
        Venture Concept
      </text>
      <circle cx={310} cy={100} r={8} fill="currentColor" />
      <text
        x={310}
        y={125}
        textAnchor="middle"
        fontFamily="sans-serif"
        fontSize={10}
        fill="currentColor"
      >
        AI Architecture
      </text>
      <text
        x={180}
        y={170}
        textAnchor="middle"
        fontFamily="sans-serif"
        fontSize={9}
        fill="currentColor"
        opacity={0.7}
      >
        The Venture Build Process
      </text>
    </svg>
  );
};

/**
 * TabBar component with 7 tabs for H-A-O-M-T-G-V.
 * Keyboard accessible: arrow keys, Home, End.
 * URL hash deep-links support.
 */
const TabBar: React.FC<{
  activeTab: string;
  onTabChange: (tab: string) => void;
  theme: 'light' | 'dark';
}> = ({ activeTab, onTabChange, theme }) => {
  const isDark = theme === 'dark';

  return (
    <div
      className={`flex gap-2 rounded-lg p-1 overflow-x-auto scroll-snap-type-x mandatory scroll-snap-align start ${isDark
        ? 'bg-ls-navy/50 border border-ls-white/10'
        : 'bg-ls-white/95 border border-ls-grey-dark'}`}
      role="tablist"
      aria-label="HAOMTGV framework tabs"
    >
      {LAYERS.map((layer) => (
        <button
          key={layer.id}
          role="tab"
          aria-controls={`panel-${layer.id}`}
          aria-selected={activeTab === layer.id}
          className={`flex-1 rounded-md text-sm font-body font-bold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ls-cyan ${activeTab === layer.id
            ? isDark
              ? 'text-ls-white bg-ls-cyan/20'
              : 'text-ls-cyan bg-ls-grey-light'
            : isDark
              ? 'text-ls-grey-light-text'
              : 'text-ls-grey-dark'}`}
          onClick={() => onTabChange(layer.id)}
          onKeyDown={(e) => {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
              e.preventDefault();
              const nextIdx =
                LAYERS.findIndex((l) => l.id === activeTab) + 1;
              const nextTab = nextIdx < LAYERS.length ? LAYERS[nextIdx].id : LAYERS[0].id;
              onTabChange(nextTab);
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
              e.preventDefault();
              const prevIdx = LAYERS.findIndex((l) => l.id === activeTab) - 1;
              const prevTab =
                prevIdx >= 0 ? LAYERS[prevIdx].id : LAYERS[LAYERS.length - 1].id;
              onTabChange(prevTab);
            } else if (e.key === 'Home') {
              e.preventDefault();
              onTabChange('human');
            } else if (e.key === 'End') {
              e.preventDefault();
              onTabChange('value');
            }
          }}
        >
          {layer.letter}
        </button>
      ))}
    </div>
  );
};

const FrameworkPage: React.FC<FrameworkPageProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const cardBase = isLight
    ? 'bg-ls-white/95 border-ls-grey-dark text-ls-navy shadow-md'
    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white shadow-xl';

  const location = useLocation();
  const navigate = useNavigate();

  // Determine active tab from URL hash, default to 'human' if no hash or invalid hash
  const activeTab = React.useMemo(() => {
    const hash = location.hash.replace('#', '');
    // Validate hash against known layer IDs
    if (hash && LAYERS.some((l) => l.id === hash)) {
      return hash;
    }
    return 'human';
  }, [location.hash]);

  // Update URL when tab changes, keeping hash in sync
  React.useEffect(() => {
    navigate(`#${activeTab}`, { replace: true });
  }, [activeTab, navigate]);

  return (
    <SiteLayout theme={theme}>
      <section
        className={`relative overflow-hidden border-b ${isLight ? 'bg-ls-navy text-ls-white' : 'bg-ls-navy text-ls-white'}`}
        aria-label="H-A-O-M-T-G-V: The Agentic Governance Constitution"
      >
        <div aria-hidden="true" className="absolute top-0 left-0 right-0 h-1 flex">
          {['#070A40', '#E63946', '#00BFFF'].map((color) => (
            <div key={color} className="flex-1" style={{ backgroundColor: color }} />
          ))}
        </div>
        <div className="max-w-4xl mx-auto px-6 py-20 sm:py-28 text-center space-y-6">
          <span className="text-xs font-body font-bold tracking-widest text-ls-red">
            OPERATING FRAMEWORK
          </span>
          <h1
            id="haomtgv-constitution-title"
            className="text-4xl sm:text-6xl font-black tracking-[0.2em] font-display text-ls-cyan"
          >
            H-A-O-M-T-G-V: The Agentic Governance Constitution
          </h1>
          <p
            className="text-sm sm:text-lg leading-relaxed text-ls-grey-light-text max-w-2xl mx-auto"
          >
            A seven-layer control model where human authority runs through every layer
            and governance (G) is integral, not a checkpoint. Not a linear pipeline; a
            working model of AI-native operations.
          </p>
          <Link
            to="/framework/#governance"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-ls-red text-ls-white font-bold text-sm tracking-wide hover:brightness-110 transition-all"
          >
            Explore the Framework
            <span aria-hidden="true" className="w-4 h-4">
              <svg
                width={16}
                height={16}
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                  d="M5 12h8l2-5h-8l-2 5z"
                />
              </svg>
            </span>
          </Link>
          <div className="inline-flex items-center gap-2 mt-4">
            <span
              className="text-sm font-body text-ls-grey-light-text bg-ls-navy/20 rounded-full px-3 py-1"
            >
              90 operating roles (89 AI agents + 1 Human CEO)
            </span>
          </div>
        </div>
      </section>

      <section
        className={`py-16 sm:py-24 ${isLight ? 'bg-ls-white' : 'bg-ls-navy-dark'}`}
        aria-label="HAOMTGV Seven Layers Elaboration"
      >
        <div className="max-w-6xl mx-auto px-6">
          <h2
            className={`text-xl sm:text-2xl font-black font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'}`}
          >
            H-A-O-M-T-G-V: The Seven Layers
          </h2>
          <div className="mt-8 space-y-6">
            {LAYERS.map((layer) => (
              <div
                key={layer.id}
                className={`bg-ls-navy/5 ${isLight ? 'border-ls-grey-dark' : 'border-ls-white/15'} rounded-xl p-6`}
              >
                <h3
                  className={`text-lg font-black font-display ${isLight ? 'text-ls-navy' : 'text-ls-white'} mb-3`}
                >
                  {layer.title}
                </h3>
                <p
                  className={`text-ls-grey-dark/70 ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'} leading-relaxed`}
                >
                  {layer.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="mt-12 flex justify-center space-x-3">
        <Link
          to="/framework/whitepaper"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-ls-cyan text-ls-navy font-bold text-sm tracking-wide hover:opacity-90 transition-all"
        >
          Download the H-A-O-M-T-G-V Whitepaper
          <svg
            width={16}
            height={16}
            viewBox="0 0 24 24"
            className="w-4 h-4"
            aria-hidden="true"
          >
            <path
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              d="M5 12h8l2-5h-8l-2 5z"
            />
          </svg>
        </Link>
        <span className="text-sm font-body text-ls-grey-light-text">
          Pharos article available
        </span>
      </div>
    </SiteLayout>
  );
};

export default FrameworkPage;