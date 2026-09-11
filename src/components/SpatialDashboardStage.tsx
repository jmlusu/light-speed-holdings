import React, { useState, useEffect } from 'react';
import {
  Sun,
  Moon,
  Bell,
  Search,
  Lock,
  Unlock,
  Cpu,
  Zap,
  ShieldCheck,
  Server,
  Clock,
  Video,
  Settings,
  ChevronDown,
  Plus,
  RotateCcw,
  ExternalLink,
  ChevronRight,
  Activity,
  Layers,
  Database,
  Terminal,
  Radio,
  FileCheck,
  Binary
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface SpatialDashboardStageProps {
  theme?: 'light' | 'dark';
  onToggleTheme?: () => void;
  onOpenConsole: () => void;
  onOpenTemplates: () => void;
  onNavigateSection?: (sectionId: string) => void;
}

export const SpatialDashboardStage: React.FC<SpatialDashboardStageProps> = ({
  theme = 'dark',
  onToggleTheme,
  onOpenConsole,
  onOpenTemplates,
  onNavigateSection
}) => {
  // Live Sovereign Epoch & UTC Clock
  const [timeStr, setTimeStr] = useState('14:30');
  const [dateStr, setDateStr] = useState('17 July, 2026');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = String(now.getUTCHours()).padStart(2, '0');
      const mins = String(now.getUTCMinutes()).padStart(2, '0');
      setTimeStr(`${hours}:${mins} UTC`);

      const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'long', year: 'numeric' };
      setDateStr(now.toLocaleDateString('en-GB', options));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Sovereign Subsystem Security & Enforcement States
  const [hitlSweepLocked, setHitlSweepLocked] = useState(true);
  const [airGapSecured, setAirGapSecured] = useState(true);
  const [consensusArbiterActive, setConsensusArbiterActive] = useState(true);
  const [auditLedgerActive, setAuditLedgerActive] = useState(true);

  // Model Inference & Compute Allocation State
  const [contextDepth, setContextDepth] = useState<'32k' | '128k' | '1M'>('128k');
  const [computeEfficiency, setComputeEfficiency] = useState<number>(85);
  const [inferenceMode, setInferenceMode] = useState<'deterministic' | 'balanced' | 'autonomous'>('deterministic');

  // Agent Concurrency & Cluster Governor State
  const [concurrencySlots, setConcurrencySlots] = useState<number>(24);
  const [governorLocked, setGovernorLocked] = useState(true);
  const [speculativeExecution, setSpeculativeExecution] = useState(true);
  const [autoLoadBalance, setAutoLoadBalance] = useState(true);
  const [clusterOnline, setClusterOnline] = useState(true);

  // Active Enterprise Cluster / Department Enclave
  const [activeCluster, setActiveCluster] = useState<string>('governance');

  // Search input state
  const [searchTerm, setSearchTerm] = useState('');

  // Notifications state
  const [showNotificationToast, setShowNotificationToast] = useState(false);
  const navigate = useNavigate();

  const clusters = [
    { id: 'governance', name: 'Executive Governance', subtitle: 'Fiduciary Enclave', to: '/' },
    { id: 'engineering', name: 'Autonomous Systems', subtitle: 'Agent Mesh', to: '/capabilities' },
    { id: 'finance', name: 'Capital Architecture', subtitle: 'Settlement Engine', to: '/capabilities/offerings' },
    { id: 'compliance', name: 'Regulatory Watchtower', subtitle: 'Audit Mesh', to: '/capabilities/diagnostic' },
    { id: 'edge', name: 'Global Edge Compute', subtitle: 'Sovereign Nodes', to: '/insights' }
  ];

  const handleClusterSelect = (clusterId: string, to: string) => {
    setActiveCluster(clusterId);
    if (onNavigateSection) {
      onNavigateSection(clusterId);
    } else {
      navigate(to);
    }
  };

  const handleSectionNav = (sectionId: string, to: string) => {
    if (onNavigateSection) {
      onNavigateSection(sectionId);
    } else {
      navigate(to);
    }
  };

  const isLight = theme === 'light';

  return (
    <div className="w-full max-w-6xl mx-auto px-2 sm:px-4 py-6 transition-all duration-300">

      {/* 1. TOP FLOATING CONTROL PILL BAR */}
      <div className={`mb-6 p-2 sm:p-2.5 rounded-full flex flex-wrap items-center justify-between gap-3 ${
        isLight ? 'glass-pill-light' : 'glass-pill-dark'
      }`}>

        {/* User profile & Sovereign Executive Status */}
        <div className="flex items-center gap-3 pl-2">
          <div className="relative w-9 h-9 sm:w-10 sm:h-10 rounded-full overflow-hidden p-0.5 bg-gradient-to-tr from-orange-500 to-amber-400 shadow-sm">
            <img
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
              alt="Albert - Executive Director"
              className="w-full h-full object-cover rounded-full"
              referrerPolicy="no-referrer"
            />
            <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-500 border-2 border-zinc-900 rounded-full" />
          </div>
          <div>
            <div className={`text-xs sm:text-sm font-bold tracking-tight ${isLight ? 'text-slate-800' : 'text-zinc-100'}`}>
              Executive Officer • Enclave Primary
            </div>
            <div className={`text-[10px] hidden sm:block font-mono ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
              LightSpeed Holdings • 144 Sovereign Agents Synced
            </div>
          </div>
        </div>

        {/* Center Search Capsule */}
        <div className="flex-1 max-w-sm mx-2">
          <div className={`relative flex items-center rounded-full px-3.5 py-1.5 transition-all ${
            isLight
              ? 'bg-white/80 border border-slate-200/80 focus-within:border-orange-400/80 focus-within:bg-white shadow-inner'
              : 'bg-zinc-850/80 border border-zinc-700/60 focus-within:border-orange-500/80 focus-within:bg-zinc-800 shadow-inner'
          }`}>
            <Search className={`w-3.5 h-3.5 mr-2 ${isLight ? 'text-slate-400' : 'text-zinc-400'}`} />
            <input
              type="text"
              placeholder="Search agent IDs, tasks, or policy gates..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className={`w-full bg-transparent text-xs outline-none ${
                isLight ? 'text-slate-800 placeholder-slate-400' : 'text-zinc-100 placeholder-zinc-500'
              }`}
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                className={`text-[10px] px-1.5 py-0.5 rounded-full ${isLight ? 'text-slate-400 hover:text-slate-700' : 'text-zinc-400 hover:text-white'}`}
              >
                ✕
              </button>
            )}
          </div>
        </div>

        {/* Right Action: Light / Dark Toggle & Notification Bell */}
        <div className="flex items-center gap-2 pr-1">
          {/* Light / Dark Mode Toggle Capsule */}
          <div className={`flex items-center p-1 rounded-full border ${
            isLight
              ? 'bg-black/[0.04] border-black/[0.06]'
              : 'bg-white/[0.06] border-white/[0.08]'
          }`}>
            <button
              onClick={() => theme !== 'light' && onToggleTheme?.()}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                isLight
                  ? 'bg-white text-slate-800 shadow-sm'
                  : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <span className="w-4 h-4 rounded-full bg-gradient-to-tr from-amber-400 to-amber-500 flex items-center justify-center text-white shadow-xs">
                <Sun className="w-2.5 h-2.5 text-white" />
              </span>
              <span>Light</span>
            </button>
            <button
              onClick={() => theme !== 'dark' && onToggleTheme?.()}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                !isLight
                  ? 'bg-zinc-800 text-white shadow-sm'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <Moon className="w-3 h-3 text-orange-400" />
              <span>Dark</span>
            </button>
          </div>

          {/* Notification Bell Circle */}
          <button
            onClick={() => setShowNotificationToast(!showNotificationToast)}
            className={`relative w-9 h-9 rounded-full flex items-center justify-center border transition-all cursor-pointer ${
              isLight
                ? 'bg-white/80 border-slate-200/80 text-slate-700 hover:bg-white shadow-sm'
                : 'bg-zinc-800/80 border-zinc-700 text-zinc-200 hover:bg-zinc-700'
            }`}
            title="Enterprise Telemetry Alerts"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-orange-500 rounded-full animate-pulse shadow-sm shadow-orange-500" />
          </button>
        </div>
      </div>

      {/* Notification Toast Dropdown */}
      {showNotificationToast && (
        <div className={`max-w-md ml-auto mb-4 p-3 rounded-2xl border text-xs shadow-xl animate-in fade-in slide-in-from-top-2 ${
          isLight ? 'glass-card-light text-slate-800' : 'glass-card-dark text-zinc-200'
        }`}>
          <div className="flex items-center justify-between font-bold pb-2 border-b border-black/5 dark:border-white/5">
            <span>Sovereign Enclave Alerts (2 New)</span>
            <button onClick={() => setShowNotificationToast(false)} className="text-[11px] text-slate-400 hover:text-slate-700">Dismiss</button>
          </div>
          <div className="space-y-2 pt-2">
            <div className="flex items-start gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 mt-1" />
              <div>
                <div className="font-semibold font-mono">Autonomous Fleet Mesh Registry-Verified</div>
                <div className="text-[11px] text-slate-500 dark:text-zinc-400">All 144 agent cards verified against company-registry.yaml schema.</div>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="w-2 h-2 rounded-full bg-orange-500 mt-1" />
              <div>
                <div className="font-semibold font-mono">HITL Expiry Cadence Sweep Completed</div>
                <div className="text-[11px] text-slate-500 dark:text-zinc-400">Zero orphaned approval tickets; deterministic governance loop sustained.</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 2. MAIN SPATIAL GRID LAYOUT (Vertical dock on left + Main Frosted Window) */}
      <div className="flex flex-col lg:flex-row items-start gap-5">

        {/* LEFT VERTICAL CAPSULE DOCK */}
        <div className={`hidden lg:flex flex-col items-center gap-4 py-5 px-3 rounded-full shrink-0 transition-all ${
          isLight ? 'glass-pill-light' : 'glass-pill-dark'
        }`}>
          <button
            onClick={() => handleSectionNav('hero', '/')}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              activeCluster === 'governance'
                ? 'bg-orange-500 text-white shadow-md shadow-orange-500/40'
                : isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="Core Executive Enclave"
          >
            <ShieldCheck className="w-4 h-4" />
          </button>

          <button
            onClick={() => handleSectionNav('capabilities', '/capabilities')}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="System Capabilities"
          >
            <Zap className="w-4 h-4" />
          </button>

          <button
            onClick={() => handleSectionNav('workforce', '/capabilities')}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              activeCluster === 'engineering'
                ? 'bg-orange-500 text-white shadow-md shadow-orange-500/40'
                : isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="Autonomous Fleet Mesh"
          >
            <Server className="w-4 h-4" />
          </button>

          <button
            onClick={() => setShowNotificationToast(!showNotificationToast)}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="Enclave Alerts"
          >
            <Bell className="w-4 h-4" />
          </button>

          <button
            onClick={() => handleSectionNav('system', '/capabilities/offerings')}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="Sovereign Architecture Timeline"
          >
            <Clock className="w-4 h-4" />
          </button>

          <button
            onClick={() => handleSectionNav('insights', '/insights')}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="Live Telemetry Monitor"
          >
            <Radio className="w-4 h-4" />
          </button>

          <div className={`w-5 h-[1px] ${isLight ? 'bg-slate-300/60' : 'bg-zinc-700/60'}`} />

          <button
            onClick={onOpenConsole}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isLight ? 'text-slate-600 hover:bg-black/5' : 'text-zinc-400 hover:bg-white/10'
            }`}
            title="Enter CEO Command Console"
          >
            <Terminal className="w-4 h-4 text-orange-400" />
          </button>

          <button
            onClick={() => window.scrollBy({ top: 400, behavior: 'smooth' })}
            className={`w-8 h-8 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isLight ? 'text-slate-400 hover:text-slate-800' : 'text-zinc-500 hover:text-white'
            }`}
            title="Scroll Down"
          >
            <ChevronDown className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* CENTER FROSTED GLASS WINDOW */}
        <div className={`flex-1 w-full rounded-[32px] sm:rounded-[40px] p-4 sm:p-7 relative overflow-hidden transition-all duration-300 ${
          isLight ? 'glass-window-light' : 'glass-window-dark'
        }`}>

          {/* Subtle inner warm room ambient highlight */}
          <div className="absolute top-0 right-0 w-96 h-96 rounded-full bg-orange-500/10 filter blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 w-80 h-80 rounded-full bg-amber-400/10 filter blur-3xl pointer-events-none" />

          {/* GRID OF SOVEREIGN ENTERPRISE AI WIDGETS */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-4 sm:gap-5 relative z-10">

            {/* ROW 1 - LEFT: Epoch Clock & Consensus Heartbeat Widget */}
            <div className={`md:col-span-4 p-5 rounded-3xl relative overflow-hidden transition-all ${
              isLight ? 'glass-card-light' : 'glass-card-dark'
            }`}>
              <div className="flex justify-between items-start">
                <div>
                  <div className={`text-[11px] font-mono tracking-wider font-semibold ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                    EPOCH • {dateStr}
                  </div>
                  <div className="flex items-baseline gap-2 mt-2">
                    <span className={`text-2xl sm:text-3xl font-black font-mono tracking-tight ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {timeStr}
                    </span>
                    <span className="text-xs font-mono font-bold text-emerald-500 bg-emerald-500/10 px-1.5 py-0.5 rounded-sm">
                      Registry-Verified
                    </span>
                  </div>
                </div>

                {/* 3D-styled Sovereign Neural Enclave Chip Graphic */}
                <div className="relative w-16 h-16 shrink-0 flex items-center justify-center">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-zinc-900 to-zinc-800 border border-orange-500/40 flex items-center justify-center shadow-lg shadow-orange-500/20">
                    <Cpu className="w-6 h-6 text-orange-400" />
                  </div>
                  {/* Surrounding Conduit Dots */}
                  <span className="absolute top-1 right-2 w-1.5 h-1.5 rounded-full bg-orange-400 animate-ping" />
                  <span className="absolute bottom-1 left-2 w-1.5 h-1.5 rounded-full bg-emerald-400" />
                </div>
              </div>

              {/* Status footer pill */}
              <div className="mt-4 pt-3 border-t border-black/5 dark:border-white/5 flex items-center justify-between text-[11px]">
                <span className={`flex items-center gap-1.5 ${isLight ? 'text-slate-600' : 'text-zinc-300'}`}>
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Consensus: Deterministic</span>
                </span>
                <span className="font-mono text-orange-400 font-bold">144 Subagents</span>
              </div>
            </div>

            {/* ROW 1 - CENTER: Fiduciary Verification & Zero-Drift Score */}
            <div className={`md:col-span-4 p-5 rounded-3xl flex flex-col justify-between transition-all ${
              isLight ? 'glass-card-light' : 'glass-card-dark'
            }`}>
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-orange-500/10 flex items-center justify-center text-orange-500">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <span className={`text-xs font-bold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
                  Fiduciary Verification
                </span>
              </div>

              {/* Radial Donut Gauge */}
              <div className="flex items-center justify-center gap-4 my-2">
                <div className="relative w-20 h-20 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <path
                      className={isLight ? 'text-slate-200' : 'text-zinc-700'}
                      strokeWidth="3.2"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className="text-orange-500 transition-all duration-700"
                      strokeDasharray="100, 100"
                      strokeWidth="3.4"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="w-4 h-4 rounded-full bg-orange-500/20 border border-orange-500 flex items-center justify-center">
                      <span className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                    </span>
                  </div>
                </div>

                <div>
                  <div className={`text-2xl font-extrabold font-mono tracking-tight ${isLight ? 'text-slate-900' : 'text-white'}`}>
                    144
                  </div>
                  <div className={`text-[11px] font-mono ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                    Registry-Verified
                  </div>
                </div>
              </div>

              <div className={`text-[11px] text-center font-mono ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                Deterministic schema verification active
              </div>
            </div>

            {/* ROW 1 - RIGHT: Compute Allocation & Token Throughput */}
            <div className={`md:col-span-4 p-5 rounded-3xl flex flex-col justify-between transition-all ${
              isLight ? 'glass-card-light' : 'glass-card-dark'
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-full bg-orange-500/10 flex items-center justify-center text-orange-500">
                    <Binary className="w-4 h-4" />
                  </div>
                  <span className={`text-xs font-bold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
                    Token Ingestion
                  </span>
                </div>
                <span className={`text-xs font-bold font-mono ${isLight ? 'text-slate-700' : 'text-orange-400'}`}>
                  2,373 TESTS
                </span>
              </div>

              {/* Monthly Bar Columns */}
              <div className="flex items-end justify-between gap-2 pt-4 pb-1 h-24">
                {[
                  { month: 'Jan', height: '42%' },
                  { month: 'Feb', height: '62%' },
                  { month: 'Mar', height: '54%' },
                  { month: 'Apr', height: '92%', active: true, tag: 'Peak' },
                  { month: 'May', height: '78%' },
                  { month: 'Jun', height: '84%' },
                ].map((col, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end group">
                    {col.active && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-orange-500 text-white shadow-xs">
                        {col.tag}
                      </span>
                    )}
                    <div
                      className={`w-full max-w-[14px] rounded-full transition-all duration-300 ${
                        col.active
                          ? 'bg-gradient-to-t from-orange-600 to-amber-400 shadow-sm shadow-orange-500/50'
                          : isLight ? 'bg-slate-200 group-hover:bg-slate-300' : 'bg-zinc-700/80 group-hover:bg-zinc-600'
                      }`}
                      style={{ height: col.height }}
                    />
                    <span className={`text-[10px] font-mono ${
                      col.active ? 'font-bold text-orange-400' : isLight ? 'text-slate-400' : 'text-zinc-500'
                    }`}>
                      {col.month}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* ROW 2 - LEFT: 4 Sovereign Subsystem Toggles (Replacing smart home appliances) */}
            <div className="md:col-span-4 grid grid-cols-2 gap-3.5">

              {/* Subsystem 1: HITL Governance Sweep */}
              <div className={`p-4 rounded-3xl flex flex-col justify-between transition-all ${
                isLight ? 'glass-card-light' : 'glass-card-dark'
              }`}>
                <div>
                  <div className={`text-xs font-bold leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-100'}`}>
                    HITL Sweep
                  </div>
                  <div className={`text-[10px] font-mono ${isLight ? 'text-slate-400' : 'text-zinc-400'}`}>
                    Governance Gate
                  </div>
                </div>

                <div className="my-2 flex justify-center">
                  <div className="w-10 h-10 rounded-xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center">
                    <FileCheck className="w-5 h-5 text-orange-400" />
                  </div>
                </div>

                <button
                  onClick={() => setHitlSweepLocked(!hitlSweepLocked)}
                  className={`w-full py-1.5 px-3 rounded-full flex items-center justify-between text-[11px] font-bold transition-all cursor-pointer ${
                    hitlSweepLocked
                      ? 'bg-orange-500 text-white shadow-xs'
                      : isLight ? 'bg-slate-100 text-slate-700' : 'bg-zinc-800 text-zinc-300'
                  }`}
                >
                  <span className="w-4 h-4 rounded-full bg-white text-orange-600 flex items-center justify-center shadow-xs">
                    {hitlSweepLocked ? <Lock className="w-2.5 h-2.5" /> : <Unlock className="w-2.5 h-2.5" />}
                  </span>
                  <span>{hitlSweepLocked ? 'Enforced' : 'Standby'}</span>
                </button>
              </div>

              {/* Subsystem 2: Enclave Air-Gap Isolation */}
              <div className={`p-4 rounded-3xl flex flex-col justify-between transition-all ${
                isLight ? 'glass-card-light' : 'glass-card-dark'
              }`}>
                <div>
                  <div className={`text-xs font-bold leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-100'}`}>
                    Air-Gap Isolation
                  </div>
                  <div className={`text-[10px] font-mono ${isLight ? 'text-slate-400' : 'text-zinc-400'}`}>
                    Zero Exfiltration
                  </div>
                </div>

                <div className="my-2 flex justify-center">
                  <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                    <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  </div>
                </div>

                <button
                  onClick={() => setAirGapSecured(!airGapSecured)}
                  className={`w-full py-1.5 px-3 rounded-full flex items-center justify-between text-[11px] font-bold transition-all cursor-pointer ${
                    airGapSecured
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : isLight ? 'bg-slate-100 text-slate-700' : 'bg-zinc-800 text-zinc-300'
                  }`}
                >
                  <span className="w-4 h-4 rounded-full bg-white text-emerald-700 flex items-center justify-center shadow-xs">
                    {airGapSecured ? <Lock className="w-2.5 h-2.5" /> : <Unlock className="w-2.5 h-2.5" />}
                  </span>
                  <span>{airGapSecured ? 'Air-Gapped' : 'Bridge'}</span>
                </button>
              </div>

              {/* Subsystem 3: Consensus Arbiter */}
              <div className={`p-4 rounded-3xl flex flex-col justify-between transition-all ${
                isLight ? 'glass-card-light' : 'glass-card-dark'
              }`}>
                <div>
                  <div className={`text-xs font-bold leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-100'}`}>
                    Consensus Arbiter
                  </div>
                  <div className={`text-[10px] font-mono ${isLight ? 'text-slate-400' : 'text-zinc-400'}`}>
                    Byzantine Guard
                  </div>
                </div>

                <div className="my-2 flex justify-center">
                  <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
                    <Activity className="w-5 h-5 text-cyan-400" />
                  </div>
                </div>

                <button
                  onClick={() => setConsensusArbiterActive(!consensusArbiterActive)}
                  className={`w-full py-1.5 px-3 rounded-full flex items-center justify-between text-[11px] font-bold transition-all cursor-pointer ${
                    consensusArbiterActive
                      ? 'bg-cyan-600 text-white shadow-xs'
                      : isLight ? 'bg-slate-100 text-slate-700' : 'bg-zinc-800 text-zinc-300'
                  }`}
                >
                  <span className="w-4 h-4 rounded-full bg-white text-cyan-700 flex items-center justify-center shadow-xs">
                    {consensusArbiterActive ? <Lock className="w-2.5 h-2.5" /> : <Unlock className="w-2.5 h-2.5" />}
                  </span>
                  <span>{consensusArbiterActive ? 'Active' : 'Bypass'}</span>
                </button>
              </div>

              {/* Subsystem 4: Audit Trail Ledger */}
              <div className={`p-4 rounded-3xl flex flex-col justify-between transition-all ${
                isLight ? 'glass-card-light' : 'glass-card-dark'
              }`}>
                <div>
                  <div className={`text-xs font-bold leading-tight ${isLight ? 'text-slate-800' : 'text-zinc-100'}`}>
                    Audit Ledger
                  </div>
                  <div className={`text-[10px] font-mono ${isLight ? 'text-slate-400' : 'text-zinc-400'}`}>
                    Immutable Lineage
                  </div>
                </div>

                <div className="my-2 flex justify-center">
                  <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center">
                    <Database className="w-5 h-5 text-amber-400" />
                  </div>
                </div>

                <button
                  onClick={() => setAuditLedgerActive(!auditLedgerActive)}
                  className={`w-full py-1.5 px-3 rounded-full flex items-center justify-between text-[11px] font-bold transition-all cursor-pointer ${
                    auditLedgerActive
                      ? 'bg-amber-500 text-white shadow-xs'
                      : isLight ? 'bg-slate-100 text-slate-700' : 'bg-zinc-800 text-zinc-300'
                  }`}
                >
                  <span className="w-4 h-4 rounded-full bg-white text-amber-700 flex items-center justify-center shadow-xs">
                    {auditLedgerActive ? <Lock className="w-2.5 h-2.5" /> : <Unlock className="w-2.5 h-2.5" />}
                  </span>
                  <span>{auditLedgerActive ? 'Logging' : 'Paused'}</span>
                </button>
              </div>
            </div>

            {/* ROW 2 - CENTER: Cognitive Inference Depth & Precision Arc */}
            <div className={`md:col-span-4 p-5 rounded-3xl flex flex-col justify-between transition-all ${
              isLight ? 'glass-card-light' : 'glass-card-dark'
            }`}>
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-7 h-7 rounded-full bg-orange-500/10 flex items-center justify-center text-orange-500">
                    <Layers className="w-4 h-4" />
                  </div>
                  <span className={`text-xs font-bold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
                    Context Window & Precision
                  </span>
                </div>

                {/* Context Window Selector Pills */}
                <div className="flex items-center justify-between gap-1.5">
                  {(['32k', '128k', '1M'] as const).map((ctx) => (
                    <button
                      key={ctx}
                      onClick={() => setContextDepth(ctx)}
                      className={`flex-1 py-1.5 rounded-full text-xs font-mono font-bold transition-all cursor-pointer ${
                        contextDepth === ctx
                          ? 'bg-orange-500 text-white shadow-md shadow-orange-500/30'
                          : isLight ? 'bg-slate-100 text-slate-600 hover:bg-slate-200' : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700'
                      }`}
                    >
                      {ctx}
                    </button>
                  ))}
                </div>
              </div>

              {/* Radial Arc Efficiency Dial */}
              <div className="relative flex flex-col items-center justify-center my-3">
                <div className="relative w-36 h-36 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke={isLight ? '#e2e8f0' : '#27272a'}
                      strokeWidth="8"
                      fill="none"
                      strokeDasharray="251.2"
                      strokeDashoffset="62.8"
                      strokeLinecap="round"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="url(#orangeDialGradient)"
                      strokeWidth="8.5"
                      fill="none"
                      strokeDasharray="251.2"
                      strokeDashoffset={251.2 - (251.2 * 0.75 * (computeEfficiency / 100))}
                      strokeLinecap="round"
                      className="transition-all duration-300"
                    />
                    <defs>
                      <linearGradient id="orangeDialGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#f97316" />
                        <stop offset="100%" stopColor="#fbbf24" />
                      </linearGradient>
                    </defs>
                  </svg>

                  {/* Centered Stat */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                    <span className={`text-2xl font-black font-mono tracking-tight ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {computeEfficiency}%
                    </span>
                    <span className={`text-[10px] font-mono ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                      Compute Yield
                    </span>
                  </div>
                </div>

                {/* Min / Max Interactive Steppers */}
                <div className="w-full flex items-center justify-between px-4 -mt-2">
                  <button
                    onClick={() => setComputeEfficiency(Math.max(40, computeEfficiency - 5))}
                    className={`flex items-center gap-1 text-[11px] font-bold px-2 py-1 rounded-full transition-all cursor-pointer ${
                      isLight ? 'text-slate-600 hover:bg-slate-200' : 'text-zinc-300 hover:bg-zinc-700'
                    }`}
                  >
                    <span>Eco</span>
                    <span className="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 flex items-center justify-center text-xs">-</span>
                  </button>

                  <button
                    onClick={() => setComputeEfficiency(Math.min(100, computeEfficiency + 5))}
                    className={`flex items-center gap-1 text-[11px] font-bold px-2 py-1 rounded-full transition-all cursor-pointer ${
                      isLight ? 'text-slate-600 hover:bg-slate-200' : 'text-zinc-300 hover:bg-zinc-700'
                    }`}
                  >
                    <span className="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 flex items-center justify-center text-xs">+</span>
                    <span>Max</span>
                  </button>
                </div>
              </div>

              {/* Mode Pills */}
              <div className="flex items-center justify-center gap-2 pt-2 border-t border-black/5 dark:border-white/5">
                {(['deterministic', 'balanced', 'autonomous'] as const).map((m) => (
                  <button
                    key={m}
                    onClick={() => setInferenceMode(m)}
                    className={`capitalize text-xs font-mono font-semibold px-2.5 py-1 rounded-full transition-all cursor-pointer ${
                      inferenceMode === m
                        ? 'bg-orange-500 text-white shadow-xs'
                        : isLight ? 'text-slate-500 hover:text-slate-800' : 'text-zinc-400 hover:text-white'
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
            </div>

            {/* ROW 2 - RIGHT: Agent Concurrency & Cluster Governor Dial */}
            <div className={`md:col-span-4 p-5 rounded-3xl flex flex-col justify-between transition-all ${
              isLight ? 'glass-card-light' : 'glass-card-dark'
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-full bg-orange-500/10 flex items-center justify-center text-orange-500">
                    <Activity className="w-4 h-4" />
                  </div>
                  <span className={`text-xs font-bold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
                    Concurrency Governor
                  </span>
                </div>

                <button
                  onClick={() => setGovernorLocked(!governorLocked)}
                  className={`py-1 px-2.5 rounded-full flex items-center gap-1.5 text-[11px] font-bold transition-all cursor-pointer ${
                    governorLocked
                      ? 'bg-orange-500 text-white shadow-xs'
                      : isLight ? 'bg-slate-100 text-slate-700' : 'bg-zinc-700 text-zinc-200'
                  }`}
                >
                  <Lock className="w-2.5 h-2.5" />
                  <span>{governorLocked ? 'Locked' : 'Free'}</span>
                </button>
              </div>

              {/* Circular Concurrency Slots Dial */}
              <div className="relative flex flex-col items-center justify-center my-2">
                <div className="relative w-36 h-36 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="38"
                      stroke={isLight ? '#e2e8f0' : '#27272a'}
                      strokeWidth="6"
                      fill="none"
                      strokeDasharray="238.7"
                      strokeDashoffset="40"
                      strokeLinecap="round"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="38"
                      stroke="#f97316"
                      strokeWidth="7"
                      fill="none"
                      strokeDasharray="238.7"
                      strokeDashoffset={238.7 - (238.7 * 0.7 * ((concurrencySlots - 8) / 56))}
                      strokeLinecap="round"
                      className="transition-all duration-300"
                    />
                  </svg>

                  {/* Center Node Icon */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <div className="w-11 h-11 rounded-2xl bg-orange-500/10 border border-orange-500/30 flex items-center justify-center shadow-inner">
                      <Terminal className="w-5 h-5 text-orange-400" />
                    </div>
                  </div>

                  {/* Slots Readout */}
                  <div className="absolute -top-1 right-2 text-right">
                    <span className={`text-xl font-black font-mono ${isLight ? 'text-slate-900' : 'text-white'}`}>
                      {concurrencySlots}
                    </span>
                    <span className="text-[10px] font-mono block text-orange-400">PIPELINES</span>
                  </div>
                </div>

                {/* Min / Max Range Markers */}
                <div className="w-full flex items-center justify-between px-6 -mt-1 text-xs font-mono font-semibold text-zinc-500">
                  <span>8</span>
                  <span className="text-[10px] text-zinc-400">CONCURRENT LIMIT</span>
                  <span>64</span>
                </div>
              </div>

              {/* Mode Controls */}
              <div className="flex items-center justify-between px-2 pt-2 border-t border-black/5 dark:border-white/5">
                <button
                  onClick={() => setSpeculativeExecution(!speculativeExecution)}
                  className={`flex items-center gap-1.5 text-xs font-mono transition-colors cursor-pointer ${
                    speculativeExecution ? 'text-orange-400 font-bold' : 'text-zinc-500'
                  }`}
                >
                  <Zap className="w-3.5 h-3.5" />
                  <span>Speculative</span>
                </button>

                <button
                  onClick={() => setAutoLoadBalance(!autoLoadBalance)}
                  className={`flex items-center gap-1.5 text-xs font-mono transition-colors cursor-pointer ${
                    autoLoadBalance ? 'text-emerald-400 font-bold' : 'text-zinc-500'
                  }`}
                >
                  <span>Auto-Balance</span>
                </button>

                {/* Cluster Online Toggle */}
                <button
                  onClick={() => setClusterOnline(!clusterOnline)}
                  className={`w-11 h-6 rounded-full p-0.5 transition-colors cursor-pointer ${
                    clusterOnline ? 'bg-orange-600' : isLight ? 'bg-slate-300' : 'bg-zinc-700'
                  }`}
                  title="Cluster Master Power"
                >
                  <div className={`w-5 h-5 rounded-full bg-white shadow-md transform transition-transform ${
                    clusterOnline ? 'translate-x-5' : 'translate-x-0'
                  }`} />
                </button>
              </div>

              {/* Bottom Telemetry Card */}
              <div className={`mt-3 p-2.5 rounded-2xl flex items-center justify-between text-xs transition-all ${
                isLight ? 'bg-white/60 border border-slate-200/60' : 'bg-zinc-800/60 border border-zinc-700/60'
              }`}>
                <div>
                  <div className={`font-mono font-bold ${isLight ? 'text-slate-900' : 'text-white'}`}>
                    2,373
                  </div>
                  <div className={`text-[10px] flex items-center gap-1 font-mono ${isLight ? 'text-slate-500' : 'text-zinc-400'}`}>
                    <Zap className="w-2.5 h-2.5 text-orange-400" />
                    <span>Verified Regression Tests</span>
                  </div>
                </div>
                <ChevronRight className={`w-4 h-4 ${isLight ? 'text-slate-400' : 'text-zinc-400'}`} />
              </div>
            </div>
          </div>

          {/* 3. BOTTOM FLOATING ENTERPRISE DEPARTMENT ENCLAVE SELECTOR */}
          <div className="mt-7 pt-4 flex flex-wrap items-center justify-center gap-2">
            <div className={`p-1.5 rounded-full flex flex-wrap items-center gap-1.5 border shadow-sm ${
              isLight ? 'bg-white/80 border-slate-200/80' : 'bg-zinc-850/80 border-zinc-700'
            }`}>
              {clusters.map((cl) => (
                <button
                  key={cl.id}
                  onClick={() => handleClusterSelect(cl.id, cl.to)}
                  className={`px-4 py-2 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                    activeCluster === cl.id
                      ? isLight
                        ? 'bg-slate-900 text-white shadow-md'
                        : 'bg-orange-500 text-white shadow-md shadow-orange-500/40'
                      : isLight
                        ? 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                        : 'text-zinc-400 hover:text-white hover:bg-zinc-700/60'
                  }`}
                >
                  <span>{cl.name}</span>
                  <span className="hidden sm:inline opacity-70 text-[10px] ml-1">({cl.subtitle})</span>
                </button>
              ))}

              <button
                onClick={onOpenTemplates}
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-all cursor-pointer ${
                  isLight ? 'text-slate-600 hover:bg-slate-100' : 'text-zinc-400 hover:bg-zinc-700'
                }`}
                title="Explore Client Website Templates"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>
          </div>

        </div>
      </div>

      {/* 4. FLOATING BOTTOM ACTIONS */}
      <div className="mt-5 flex items-center justify-between px-2">
        <button
          onClick={onOpenConsole}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-bold transition-all shadow-md cursor-pointer ${
            isLight
              ? 'glass-pill-light text-slate-800 hover:bg-white'
              : 'glass-pill-dark text-white hover:bg-zinc-800'
          }`}
        >
          <Terminal className="w-3.5 h-3.5 text-orange-400" />
          <span>Launch CEO Command Console (144 Active Agents)</span>
        </button>

        <button
          onClick={onOpenTemplates}
          className={`hidden sm:flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium transition-all cursor-pointer ${
            isLight
              ? 'bg-white/60 text-slate-700 hover:bg-white border border-slate-200/60'
              : 'bg-zinc-800/60 text-zinc-300 hover:bg-zinc-800 border border-zinc-700/60'
          }`}
        >
          <ExternalLink className="w-3.5 h-3.5 text-orange-400" />
          <span>Client Website Templates</span>
        </button>

        <button
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className={`w-11 h-11 rounded-full flex items-center justify-center border shadow-md transition-all cursor-pointer ${
            isLight
              ? 'glass-pill-light text-slate-800 hover:bg-white'
              : 'glass-pill-dark text-white hover:bg-zinc-800'
          }`}
          title="Return to Hero"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

    </div>
  );
};
