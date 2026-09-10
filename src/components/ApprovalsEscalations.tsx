import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  AlertTriangle, 
  FileText, 
  ArrowRight,
  ShieldCheck,
  UserCheck,
  Check,
  X
} from 'lucide-react';
import { ApprovalRequest, EscalationItem } from '../types';

interface ApprovalsEscalationsProps {
  approvals: ApprovalRequest[];
  escalations: EscalationItem[];
  onApprove: (id: string, notes?: string) => void;
  onReject: (id: string, notes?: string) => void;
  onResolveEscalation: (id: string, resolutionNotes: string) => void;
}

export const ApprovalsEscalations: React.FC<ApprovalsEscalationsProps> = ({
  approvals,
  escalations,
  onApprove,
  onReject,
  onResolveEscalation
}) => {
  const [activeTab, setActiveTab] = useState<'approvals' | 'escalations' | 'matrix'>('approvals');
  const [resolutionModalOpen, setResolutionModalOpen] = useState(false);
  const [selectedEscalationId, setSelectedEscalationId] = useState<string | null>(null);
  const [resolutionText, setResolutionText] = useState('');

  useEffect(() => {
    if (resolutionModalOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [resolutionModalOpen]);

  const pendingApprovals = approvals.filter(a => a.status === 'pending');
  const openEscalations = escalations.filter(e => e.status !== 'resolved');

  const approvalTiers = [
    { tier: 'Tier 1 (Auto)', authority: 'Automated Agent', scope: 'Read-only queries, non-destructive file formatting, internal data pipelines', limit: '$0' },
    { tier: 'Tier 2 (Single)', authority: 'Team Lead / Manager', scope: 'Routine pull requests, minor dependency updates, task re-assignment', limit: '< $500' },
    { tier: 'Tier 3 (Dual)', authority: 'Cross-Department (e.g. CISO + CTO)', scope: 'Database schema modifications, external API credentials, tool permissions elevation', limit: '< $2,500' },
    { tier: 'Tier 4 (Executive)', authority: 'C-Suite (CFO / CLO / COO)', scope: 'Contract commitments, legal disclaimers, high-concurrency jobs', limit: '< $10,000' },
    { tier: 'Tier 5 (CEO)', authority: 'Human CEO (Jack Mlusu)', scope: 'Capital expenditure > $10,000, company constitution amendments, SADC policy releases', limit: '> $10,000' }
  ];

  const handleOpenResolve = (id: string) => {
    setSelectedEscalationId(id);
    setResolutionText('');
    setResolutionModalOpen(true);
  };

  const submitResolve = () => {
    if (selectedEscalationId && resolutionText.trim()) {
      onResolveEscalation(selectedEscalationId, resolutionText.trim());
      setResolutionModalOpen(false);
      setSelectedEscalationId(null);
    }
  };

  return (
    <div className="space-y-5">
      {/* Top Header & Sub-nav */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#0b102f] border border-[#1b2554] p-4 rounded-2xl shadow-md">
        <div>
          <h2 className="text-base font-bold text-white tracking-wider font-display flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-[#e63946]" />
            Human-in-the-Loop (HITL) Safety Gates & Escalations
          </h2>
          <p className="text-justify text-xs text-slate-400">
            Enforcing constitutional guardrails, two-man rules, and executive sign-off before privileged execution
          </p>
        </div>

        <div className="flex items-center gap-1.5 bg-[#0e163b] p-1 rounded-xl border border-[#1e2a58]">
          <button
            onClick={() => setActiveTab('approvals')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeTab === 'approvals'
                ? 'bg-[#00bfff] text-[#070a40]'
                : 'text-slate-300 hover:text-white'
            }`}
          >
            Pending Approvals ({pendingApprovals.length})
          </button>
          <button
            onClick={() => setActiveTab('escalations')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeTab === 'escalations'
                ? 'bg-[#e63946] text-white'
                : 'text-slate-300 hover:text-white'
            }`}
          >
            Escalation Stream ({openEscalations.length})
          </button>
          <button
            onClick={() => setActiveTab('matrix')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeTab === 'matrix'
                ? 'bg-[#182357] text-white'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Approval Matrix
          </button>
        </div>
      </div>

      {/* Tab Content: Approvals */}
      {activeTab === 'approvals' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 gap-4">
            {approvals.map((req) => (
              <div
                key={req.id}
                className={`p-5 rounded-2xl border transition-all ${
                  req.status === 'pending'
                    ? 'bg-[#0b102f] border-amber-500/40 shadow-lg shadow-amber-500/5'
                    : req.status === 'approved'
                    ? 'bg-[#090e2b] border-emerald-500/30 opacity-75'
                    : 'bg-[#090e2b] border-rose-500/30 opacity-75'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-xs text-slate-400 font-bold">{req.id}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider ${
                        req.tier.includes('CEO')
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                          : req.tier.includes('Executive')
                          ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
                          : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                      }`}>
                        {req.tier}
                      </span>
                      {req.amount && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                          {req.amount}
                        </span>
                      )}
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        req.status === 'pending' ? 'bg-amber-400/10 text-amber-300' :
                        req.status === 'approved' ? 'bg-emerald-400/10 text-emerald-400' : 'bg-rose-400/10 text-rose-400'
                      }`}>
                        {req.status}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white mt-1.5">
                      {req.title}
                    </h3>
                    <p className="text-justify text-xs text-slate-300 mt-1 leading-relaxed">
                      {req.reason}
                    </p>

                    <div className="flex items-center gap-4 mt-3 text-xs text-slate-400">
                      <span>Requested by: <strong className="text-slate-200 font-mono">@{req.requested_by}</strong></span>
                      <span>Target Approver: <strong className="text-[#00bfff]">{req.approver_role}</strong></span>
                      <span>Created: <strong className="text-slate-300">{new Date(req.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</strong></span>
                    </div>

                    {req.notes && (
                      <div className="mt-2 text-xs text-slate-400 italic bg-[#070b20] p-2 rounded border border-slate-800">
                        Resolution Note: {req.notes}
                      </div>
                    )}
                  </div>

                  {req.status === 'pending' && (
                    <div className="flex items-center gap-2 self-end md:self-center">
                      <button
                        onClick={() => onReject(req.id)}
                        className="px-3 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
                      >
                        <XCircle className="w-4 h-4" />
                        <span>Reject</span>
                      </button>

                      <button
                        onClick={() => onApprove(req.id)}
                        className="px-4 py-2 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-bold flex items-center gap-1.5 shadow-md shadow-emerald-500/10 transition-colors cursor-pointer"
                      >
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        <span>Sign & Authorize</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab Content: Escalations */}
      {activeTab === 'escalations' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 gap-4">
            {escalations.map((esc) => (
              <div
                key={esc.id}
                className={`p-5 rounded-2xl border transition-all ${
                  esc.status !== 'resolved'
                    ? 'bg-[#0b102f] border-rose-500/40 shadow-lg shadow-rose-500/5'
                    : 'bg-[#090e2b] border-slate-800 opacity-60'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-xs text-slate-400 font-bold">{esc.id}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider ${
                        esc.level === 'critical' ? 'bg-rose-500 text-white' : 'bg-amber-500 text-black'
                      }`}>
                        {esc.level} LEVEL
                      </span>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                        {esc.department}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        esc.status === 'open' ? 'bg-rose-500/20 text-rose-300' :
                        esc.status === 'investigating' ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
                      }`}>
                        {esc.status}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white mt-1.5">
                      {esc.title}
                    </h3>
                    <p className="text-justify text-xs text-slate-300 mt-1 leading-relaxed">
                      {esc.reason}
                    </p>

                    <div className="flex items-center gap-4 mt-3 text-xs text-slate-400">
                      <span>Originating Agent: <strong className="text-slate-200 font-mono">@{esc.agent_id}</strong></span>
                      <span>Opened: <strong className="text-slate-300">{new Date(esc.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</strong></span>
                    </div>

                    {esc.resolution_notes && (
                      <div className="mt-2 text-xs text-emerald-300 bg-emerald-950/20 p-2 rounded border border-emerald-500/30">
                        <strong>Resolution:</strong> {esc.resolution_notes}
                      </div>
                    )}
                  </div>

                  {esc.status !== 'resolved' && (
                    <button
                      onClick={() => handleOpenResolve(esc.id)}
                      className="px-3.5 py-2 rounded-xl bg-gradient-to-r from-[#00bfff] to-[#0099cc] hover:from-[#33ccff] hover:to-[#00bfff] text-[#070a40] font-bold text-xs shadow-md transition-all cursor-pointer self-end md:self-center"
                    >
                      <span>Resolve Escalation</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab Content: Approval Matrix */}
      {activeTab === 'matrix' && (
        <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-5 shadow-md">
          <h3 className="text-sm font-bold text-white tracking-wider font-display mb-1">
            Constitutional 5-Tier HITL Approval Matrix
          </h3>
          <p className="text-justify text-xs text-slate-400 mb-4">
            Governing automated execution boundaries according to config/decision/approval_matrix.yaml
          </p>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-[#1b2554] text-slate-400 text-[10px]">
                <tr>
                  <th className="py-2.5 px-3">Tier</th>
                  <th className="py-2.5 px-3">Authorized Signer</th>
                  <th className="py-2.5 px-3">Permitted Execution Scope</th>
                  <th className="py-2.5 px-3 text-right">Financial Cap</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1b2554] text-slate-200">
                {approvalTiers.map((t) => (
                  <tr key={t.tier} className="hover:bg-[#0e163b]">
                    <td className="py-3 px-3 font-bold text-white whitespace-nowrap">{t.tier}</td>
                    <td className="py-3 px-3 text-[#00bfff] font-medium whitespace-nowrap">{t.authority}</td>
                    <td className="py-3 px-3 text-slate-300">{t.scope}</td>
                    <td className="py-3 px-3 text-right font-mono font-bold text-emerald-400 whitespace-nowrap">{t.limit}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Resolution Modal */}
      {resolutionModalOpen && (
        <div className="fixed inset-0 z-[1000] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 pt-16 sm:pt-20 overflow-y-auto">
          <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-4 relative">
            <div className="flex items-center justify-between pb-3 border-b border-[#1b2554] relative z-10">
              <h3 className="text-sm font-bold text-white tracking-wider font-display">
                Resolve Escalation ({selectedEscalationId})
              </h3>
              <button
                onClick={() => setResolutionModalOpen(false)}
                type="button"
                aria-label="Close modal"
                title="Close modal"
                className="relative z-50 p-2 rounded-xl bg-[#141e48] hover:bg-[#1a2862] text-slate-200 hover:text-white transition-all cursor-pointer border border-[#1b2554] shrink-0"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Resolution Notes & Corrective Actions
              </label>
              <textarea
                value={resolutionText}
                onChange={(e) => setResolutionText(e.target.value)}
                placeholder="Describe how the contention/conflict was resolved..."
                rows={4}
                className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-xl p-3 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#00bfff]"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-[#1b2554]">
              <button
                onClick={() => setResolutionModalOpen(false)}
                className="px-3 py-1.5 rounded-xl bg-[#141e48] text-xs text-slate-300 hover:bg-[#1a2862]"
              >
                Cancel
              </button>
              <button
                onClick={submitResolve}
                disabled={!resolutionText.trim()}
                className="px-4 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs disabled:opacity-50 transition-colors"
              >
                Mark Resolved
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
