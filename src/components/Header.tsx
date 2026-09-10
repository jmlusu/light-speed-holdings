import React from 'react';
import { Shield, Activity, Bell, Search, Cpu, CheckCircle2, AlertTriangle } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  onSearchChange: (query: string) => void;
  searchQuery: string;
  pendingApprovalsCount: number;
  openEscalationsCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  onSearchChange,
  searchQuery,
  pendingApprovalsCount,
  openEscalationsCount
}) => {
  const [time, setTime] = React.useState<string>(new Date().toLocaleTimeString());

  React.useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="sticky top-0 z-30 bg-[#070a24]/90 backdrop-blur-md border-b border-[#172044] px-4 lg:px-8 py-3.5">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        {/* Brand identity */}
        <div className="flex items-center gap-3.5">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-lg bg-gradient-to-br from-[#00bfff]/20 to-[#070a40] border border-[#00bfff]/40 shadow-sm shadow-[#00bfff]/20">
            <Shield className="w-5 h-5 text-[#00bfff]" />
            <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#00bfff] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#00bfff]"></span>
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-bold tracking-wider text-white font-display">
                LightSpeed HOLDINGS
              </h1>
              <span className="px-1.5 py-0.5 text-[10px] font-semibold tracking-wider text-[#00bfff] bg-[#00bfff]/10 rounded border border-[#00bfff]/30">
                CEO Console
              </span>
            </div>
            <p className="text-justify text-xs text-slate-400 font-medium">
              Autonomous AI Agent Company Orchestrator • 144 Agents Fleet
            </p>
          </div>
        </div>

        {/* Center Search */}
        <div className="flex-1 max-w-md mx-auto w-full">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search 144 agents, departments, tasks, SOPs..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="w-full bg-[#0d1430] border border-[#1e2a58] rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#00bfff] focus:ring-1 focus:ring-[#00bfff] transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => onSearchChange('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[11px] text-slate-400 hover:text-white"
              >
                Clear
              </button>
            )}
          </div>
        </div>

        {/* Right Status Indicators */}
        <div className="flex items-center gap-3">
          {/* Health status pill */}
          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-[#0d1430] border border-[#1e2a58] text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="text-slate-300 font-mono text-[11px] font-medium">SYSTEM HEALTHY</span>
            <span className="text-slate-500 text-[10px]">|</span>
            <span className="text-slate-400 font-mono text-[11px]">{time}</span>
          </div>

          {/* Pending Alerts / Badges */}
          <div className="flex items-center gap-2">
            {pendingApprovalsCount > 0 && (
              <div
                title={`${pendingApprovalsCount} Pending Approvals`}
                className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-medium"
              >
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>{pendingApprovalsCount} Approvals</span>
              </div>
            )}

            {openEscalationsCount > 0 && (
              <div
                title={`${openEscalationsCount} Open Escalations`}
                className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-medium"
              >
                <Activity className="w-3.5 h-3.5" />
                <span>{openEscalationsCount} Escalations</span>
              </div>
            )}
          </div>

          {/* User profile / CEO */}
          <div className="flex items-center gap-2 pl-2 border-l border-[#1e2a58]">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#e63946] to-[#00bfff] p-[1.5px]">
              <div className="w-full h-full rounded-full bg-[#070a24] flex items-center justify-center font-bold text-xs text-white">
                CEO
              </div>
            </div>
            <div className="hidden lg:block text-left">
              <div className="text-xs font-semibold text-white leading-tight">Jack Mlusu</div>
              <div className="text-[10px] text-[#00bfff] leading-tight">Human CEO & Founder</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
