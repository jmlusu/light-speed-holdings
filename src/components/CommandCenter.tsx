import React from 'react';
import { 
  Activity, 
  Users, 
  Cpu, 
  DollarSign, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  Send, 
  Sparkles, 
  Zap, 
  TrendingUp, 
  ShieldCheck, 
  ArrowUpRight, 
  Play,
  RotateCcw
} from 'lucide-react';
import { TaskItem, ApprovalRequest, EscalationItem, AuditEntry, KPIDefinition } from '../types';

interface CommandCenterProps {
  agentsCount: number;
  departmentsCount: number;
  tasks: TaskItem[];
  approvals: ApprovalRequest[];
  escalations: EscalationItem[];
  kpis: KPIDefinition[];
  auditLogs: AuditEntry[];
  onOpenNewTaskModal: () => void;
  onNavigateTab: (tab: string) => void;
  onTriggerAudit: () => void;
}

export const CommandCenter: React.FC<CommandCenterProps> = ({
  agentsCount,
  departmentsCount,
  tasks,
  approvals,
  escalations,
  kpis,
  auditLogs,
  onOpenNewTaskModal,
  onNavigateTab,
  onTriggerAudit
}) => {
  const [auditRunning, setAuditRunning] = React.useState(false);
  const [selectedAuditFilter, setSelectedAuditFilter] = React.useState<string>('all');

  const pendingApprovals = approvals.filter(a => a.status === 'pending');
  const openEscalations = escalations.filter(e => e.status !== 'resolved');
  const inProgressTasks = tasks.filter(t => t.status === 'in_progress');
  const completedTasks = tasks.filter(t => t.status === 'completed');

  const orgHealthKPI = kpis.find(k => k.id === 'org_health_composite') || {
    current: 94.2,
    target: 90.0,
    status: 'good'
  };

  const filteredLogs = selectedAuditFilter === 'all'
    ? auditLogs
    : auditLogs.filter(l => l.category === selectedAuditFilter);

  const handleRunAudit = () => {
    setAuditRunning(true);
    setTimeout(() => {
      onTriggerAudit();
      setAuditRunning(false);
    }, 1200);
  };

  // Calculate SVG circle properties for Org Health gauge
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (orgHealthKPI.current / 100) * circumference;

  return (
    <div className="space-y-6">
      {/* Top Banner: Quick Summary & Action Bar */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 bg-gradient-to-r from-[#0d1435] via-[#0b102b] to-[#070a24] p-5 rounded-2xl border border-[#1e2a58] shadow-lg shadow-black/40">
        <div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              Autonomous Orchestrator Live
            </span>
            <span className="text-xs text-slate-400">Cadence: 6-Hour Ticks</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1.5 tracking-tight font-display">
            Executive Command Console • LightSpeed Holdings
          </h2>
          <p className="text-justify text-xs text-slate-300 max-w-2xl mt-0.5">
            144 registered AI agents actively fulfilling operational, engineering, and market expansion mandates under constitutional human-in-the-loop oversight.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={onOpenNewTaskModal}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-gradient-to-r from-[#00bfff] to-[#0099cc] hover:from-[#33ccff] hover:to-[#00bfff] text-[#070a40] font-bold text-xs shadow-md shadow-[#00bfff]/20 transition-all cursor-pointer"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Dispatch Task</span>
          </button>

          <button
            onClick={handleRunAudit}
            disabled={auditRunning}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#141d45] hover:bg-[#1a2558] border border-[#233370] text-slate-200 font-semibold text-xs transition-all cursor-pointer disabled:opacity-50"
          >
            <RotateCcw className={`w-3.5 h-3.5 ${auditRunning ? 'animate-spin text-[#00bfff]' : ''}`} />
            <span>{auditRunning ? 'Auditing Telemetry...' : 'Trigger Health Audit'}</span>
          </button>

          <button
            onClick={() => onNavigateTab('approvals')}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#e63946]/10 hover:bg-[#e63946]/20 border border-[#e63946]/30 text-[#ff6b77] font-semibold text-xs transition-all cursor-pointer"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Review Gates ({pendingApprovals.length})</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Org Health Hero Gauge & Core Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Org Health Circular Hero Gauge */}
        <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 flex flex-col justify-between shadow-md relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[#00bfff]/5 rounded-full blur-2xl pointer-events-none"></div>
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 tracking-wider">Org Health Score</span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
              OPTIMAL
            </span>
          </div>

          <div className="flex items-center justify-center my-2">
            <div className="relative flex items-center justify-center">
              <svg className="w-32 h-32 transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r={radius}
                  className="text-slate-800/80 stroke-current"
                  strokeWidth="10"
                  fill="transparent"
                />
                <circle
                  cx="64"
                  cy="64"
                  r={radius}
                  className="text-[#00bfff] stroke-current transition-all duration-1000 ease-out"
                  strokeWidth="10"
                  strokeDasharray={circumference}
                  strokeDashoffset={strokeDashoffset}
                  strokeLinecap="round"
                  fill="transparent"
                />
              </svg>
              <div className="absolute flex flex-col items-center justify-center text-center">
                <span className="text-2xl font-black text-white tracking-tight">{orgHealthKPI.current}</span>
                <span className="text-[10px] text-slate-400 font-medium">TARGET 90.0</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-1 text-[11px] pt-2 border-t border-[#1a234d] text-slate-300">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Success Rate:</span>
              <span className="font-semibold text-emerald-400">97.4%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Availability:</span>
              <span className="font-semibold text-[#00bfff]">99.8%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Cost Effic.:</span>
              <span className="font-semibold text-slate-200">91.5%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Escalations:</span>
              <span className="font-semibold text-amber-400">2.1%</span>
            </div>
          </div>
        </div>

        {/* Card 2: Active Agents Fleet */}
        <div 
          onClick={() => onNavigateTab('roster')}
          className="bg-[#0b102f] border border-[#1b2554] hover:border-[#00bfff]/50 rounded-2xl p-5 flex flex-col justify-between shadow-md cursor-pointer transition-all group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 tracking-wider">Autonomous Fleet</span>
            <Users className="w-4 h-4 text-[#00bfff] group-hover:scale-110 transition-transform" />
          </div>
          <div className="my-3">
            <div className="text-3xl font-extrabold text-white tracking-tight">{agentsCount}</div>
            <p className="text-justify text-xs text-slate-400 mt-0.5">
              Agents configured in <span className="text-[#00bfff] font-medium">{departmentsCount} Departments</span>
            </p>
          </div>
          <div className="space-y-1.5 pt-2 border-t border-[#1a234d] text-xs">
            <div className="flex justify-between text-slate-400">
              <span>Executives & C-Suite:</span>
              <span className="text-slate-200 font-semibold">18</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Specialists & Engineers:</span>
              <span className="text-slate-200 font-semibold">112</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Governance & Board:</span>
              <span className="text-slate-200 font-semibold">14</span>
            </div>
          </div>
        </div>

        {/* Card 3: Tasks Pipeline */}
        <div 
          onClick={() => onNavigateTab('kanban')}
          className="bg-[#0b102f] border border-[#1b2554] hover:border-[#00bfff]/50 rounded-2xl p-5 flex flex-col justify-between shadow-md cursor-pointer transition-all group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 tracking-wider">Tasks Pipeline</span>
            <Cpu className="w-4 h-4 text-emerald-400 group-hover:scale-110 transition-transform" />
          </div>
          <div className="my-3">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white tracking-tight">{tasks.length}</span>
              <span className="text-xs text-emerald-400 font-semibold flex items-center">
                <TrendingUp className="w-3.5 h-3.5 mr-0.5" /> Active
              </span>
            </div>
            <p className="text-justify text-xs text-slate-400 mt-0.5">
              {inProgressTasks.length} in progress • {completedTasks.length} completed today
            </p>
          </div>
          <div className="space-y-1.5 pt-2 border-t border-[#1a234d] text-xs">
            <div className="flex justify-between text-slate-400">
              <span>In Progress:</span>
              <span className="text-emerald-400 font-semibold">{inProgressTasks.length}</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Review / Gate:</span>
              <span className="text-amber-400 font-semibold">{tasks.filter(t => t.status === 'review').length}</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Escalated:</span>
              <span className="text-rose-400 font-semibold">{tasks.filter(t => t.status === 'escalated').length}</span>
            </div>
          </div>
        </div>

        {/* Card 4: Financial Burn & Model Efficiency */}
        <div 
          onClick={() => onNavigateTab('finance')}
          className="bg-[#0b102f] border border-[#1b2554] hover:border-[#00bfff]/50 rounded-2xl p-5 flex flex-col justify-between shadow-md cursor-pointer transition-all group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 tracking-wider">LLM Cost & Budget</span>
            <DollarSign className="w-4 h-4 text-amber-400 group-hover:scale-110 transition-transform" />
          </div>
          <div className="my-3">
            <div className="text-3xl font-extrabold text-white tracking-tight">$117.64</div>
            <p className="text-justify text-xs text-slate-400 mt-0.5">
              Annual Cap: <span className="text-slate-200 font-medium">$15,000,000</span>
            </p>
          </div>
          <div className="space-y-1.5 pt-2 border-t border-[#1a234d] text-xs">
            <div className="flex justify-between text-slate-400">
              <span>Avg Cost / Task:</span>
              <span className="text-emerald-400 font-semibold">$0.038 (Target &lt;$0.05)</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Tokens Processed:</span>
              <span className="text-slate-200 font-semibold">270.4M</span>
            </div>
            <div className="flex justify-between text-slate-400">
              <span>Model Routing Savings:</span>
              <span className="text-[#00bfff] font-semibold">22% vs Single Tier</span>
            </div>
          </div>
        </div>
      </div>

      {/* Middle Row: Executive Briefing & Approvals/Escalations Snapshot */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Executive AI Briefing */}
        <div className="lg:col-span-2 bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md">
          <div className="flex items-center justify-between pb-3 border-b border-[#1a234d]">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#00bfff]" />
              <h3 className="text-sm font-bold text-white tracking-wider font-display">
                Executive Morning Briefing • Chief of Staff Summary
              </h3>
            </div>
            <span className="text-[11px] font-mono text-slate-400">Generated for Human CEO</span>
          </div>

          <div className="mt-4 space-y-3 text-xs text-slate-300 leading-relaxed">
            <div className="p-3 bg-[#0e163b] rounded-xl border border-[#1e2a58]">
              <div className="font-semibold text-white flex items-center gap-1.5 mb-1">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                Technology & SADC Governance Deliverables
              </div>
              <p>
                Agentic Policy Analyst and Thought Leadership Lead finalized Section 4 of the SADC Agentic AI Framework. Lead Backend resolved model tier routing latency, cutting average task duration by 14%.
              </p>
            </div>

            <div className="p-3 bg-[#0e163b] rounded-xl border border-[#1e2a58]">
              <div className="font-semibold text-white flex items-center gap-1.5 mb-1">
                <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                Key Attention Items (2 Pending Approvals)
              </div>
              <p>
                CAIO submitted a Tier 5 CEO capital allocation request ($14,200) for Chichewa dialect multi-GPU fine-tuning dataset compute. Consulting Lead requested World Bank Open Data Gateway API whitelisting.
              </p>
            </div>

            <div className="p-3 bg-[#0e163b] rounded-xl border border-[#1e2a58]">
              <div className="font-semibold text-white flex items-center gap-1.5 mb-1">
                <span className="w-2 h-2 rounded-full bg-[#00bfff]"></span>
                Workforce Health & Orchestrator SLA
              </div>
              <p>
                All 144 agent specs are compliant with the 7 canonical OpenCode tools. Zero critical security breaches detected in recent git commits or prompt injections.
              </p>
            </div>
          </div>
        </div>

        {/* High Priority Escalation & Approvals Card */}
        <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-[#1a234d]">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-rose-400" />
                <h3 className="text-sm font-bold text-white tracking-wider font-display">
                  Safety Gates & HITL
                </h3>
              </div>
              <span className="text-xs text-rose-400 font-semibold">{pendingApprovals.length + openEscalations.length} Actionable</span>
            </div>

            <div className="mt-4 space-y-3">
              {pendingApprovals.map((req) => (
                <div key={req.id} className="p-2.5 rounded-lg bg-[#111942] border border-amber-500/30 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-amber-300">{req.tier}</span>
                    <span className="text-[10px] text-slate-400">{req.id}</span>
                  </div>
                  <div className="text-white font-medium mt-1 line-clamp-1">{req.title}</div>
                  <div className="text-slate-400 text-[11px] mt-0.5">By {req.requested_by} • Approver: {req.approver_role}</div>
                </div>
              ))}

              {openEscalations.map((esc) => (
                <div key={esc.id} className="p-2.5 rounded-lg bg-[#111942] border border-rose-500/30 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-rose-400 tracking-wider text-[10px]">{esc.level} Escalation</span>
                    <span className="text-[10px] text-slate-400">{esc.id}</span>
                  </div>
                  <div className="text-white font-medium mt-1 line-clamp-1">{esc.title}</div>
                  <div className="text-slate-400 text-[11px] mt-0.5">Agent: {esc.agent_id} • {esc.department}</div>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => onNavigateTab('approvals')}
            className="w-full mt-4 py-2 px-3 bg-[#131d47] hover:bg-[#1a265e] text-slate-200 border border-[#233370] rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer"
          >
            <span>Open Decision Matrix & Gates</span>
            <ArrowUpRight className="w-3.5 h-3.5 text-[#00bfff]" />
          </button>
        </div>
      </div>

      {/* Bottom Row: Real-time Telemetry & Audit Stream */}
      <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#1a234d]">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white tracking-wider font-display">
              Live Audit Log & Telemetry Stream
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
              JSONL MessageBus
            </span>
          </div>

          {/* Category filter pills */}
          <div className="flex items-center gap-1.5 text-xs">
            {['all', 'orchestrator', 'approval', 'escalation', 'security'].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedAuditFilter(cat)}
                className={`px-2.5 py-1 rounded-md capitalize text-[11px] font-medium transition-all cursor-pointer ${
                  selectedAuditFilter === cat
                    ? 'bg-[#00bfff] text-[#070a40] font-bold'
                    : 'bg-[#10173d] text-slate-400 hover:text-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-4 space-y-2 max-h-64 overflow-y-auto pr-1">
          {filteredLogs.map((log) => (
            <div
              key={log.id}
              className="flex items-start justify-between p-2.5 rounded-lg bg-[#0e1538] hover:bg-[#131c48] border border-[#182350] text-xs transition-colors"
            >
              <div className="flex items-start gap-3">
                <span className="text-[10px] font-mono text-slate-500 mt-0.5">
                  {new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </span>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-white font-mono">{log.actor}</span>
                    <span className="px-1.5 py-0.2 text-[9px] font-bold tracking-wider rounded bg-slate-800 text-[#00bfff] border border-[#00bfff]/20">
                      {log.action}
                    </span>
                  </div>
                  <p className="text-justify text-slate-300 text-[11px] mt-0.5">{log.details}</p>
                </div>
              </div>
              <span className="text-[10px] text-slate-500 font-mono capitalize">{log.category}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
