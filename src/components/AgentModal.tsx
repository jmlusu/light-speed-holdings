import React, { useEffect } from 'react';
import { 
  X, 
  Terminal, 
  Shield, 
  Send, 
  CheckCircle, 
  Layers, 
  GitFork,
  FileCode,
  FileText
} from 'lucide-react';
import { Agent } from '../types';

interface AgentModalProps {
  agent: Agent | null;
  onClose: () => void;
  onDispatchTask: (agent: Agent) => void;
}

export const AgentModal: React.FC<AgentModalProps> = ({ agent, onClose, onDispatchTask }) => {
  useEffect(() => {
    if (agent) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [agent]);

  if (!agent) return null;

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center bg-black/80 backdrop-blur-md p-4 pt-16 sm:pt-20 overflow-y-auto">
      <div className="bg-zinc-950 border border-white/15 rounded-3xl max-w-2xl w-full shadow-2xl overflow-hidden my-auto relative">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-white/10 bg-zinc-900/80 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center font-bold text-sm text-white shadow-md shadow-orange-500/20">
              {agent.name.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white font-display">
                  {agent.role}
                </h3>
                <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded tracking-wider ${
                  agent.type === 'Executive' 
                    ? 'bg-orange-500/20 text-orange-400 border border-orange-500/40'
                    : 'bg-zinc-800 text-zinc-300 border border-white/10'
                }`}>
                  {agent.type}
                </span>
              </div>
              <p className="text-justify text-xs text-zinc-400 font-mono">
                @{agent.name} • {agent.department} Department
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            type="button"
            aria-label="Close modal"
            title="Close modal"
            className="relative z-50 w-9 h-9 rounded-full bg-zinc-900 hover:bg-zinc-800 text-zinc-200 hover:text-white flex items-center justify-center transition-all cursor-pointer border border-white/20 shadow-md shrink-0"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5 max-h-[75vh] overflow-y-auto">
          {/* Description */}
          <div>
            <h4 className="text-xs font-mono font-bold tracking-wider text-zinc-400 mb-1">
              Operational Role & Summary
            </h4>
            <p className="text-justify text-xs text-zinc-200 leading-relaxed bg-zinc-900/70 p-3.5 rounded-2xl border border-white/10">
              {agent.description || 'Specialized AI agent assigned to fulfill organizational goals.'}
            </p>
          </div>

          {/* Hierarchy & Reporting */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3.5 bg-zinc-900/70 rounded-2xl border border-white/10">
              <span className="text-[10px] text-zinc-400 block font-mono tracking-wider font-bold">Reports To</span>
              <span className="font-bold text-white font-mono mt-0.5 block">@{agent.reportsTo}</span>
            </div>
            <div className="p-3.5 bg-zinc-900/70 rounded-2xl border border-white/10">
              <span className="text-[10px] text-zinc-400 block font-mono tracking-wider font-bold">Direct Reports</span>
              <span className="font-bold text-orange-400 font-mono mt-0.5 block">
                {agent.directReports && agent.directReports.length > 0
                  ? `${agent.directReports.length} agents`
                  : 'None (Terminal Specialist)'}
              </span>
            </div>
          </div>

          {/* Configured Tools & Permissions */}
          <div>
            <h4 className="text-xs font-mono font-bold tracking-wider text-zinc-400 mb-2">
              Assigned OpenCode Canonical Tools ({agent.tools.length})
            </h4>
            <div className="flex flex-wrap gap-1.5">
              {agent.tools.map((t, idx) => (
                <span
                  key={idx}
                  className="text-xs font-mono px-2.5 py-1 rounded-xl bg-zinc-900 text-zinc-200 border border-white/15 flex items-center gap-1.5"
                >
                  <Terminal className="w-3 h-3 text-orange-400" />
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Responsibilities */}
          {agent.responsibilities && agent.responsibilities.length > 0 && (
            <div>
              <h4 className="text-xs font-mono font-bold tracking-wider text-zinc-400 mb-2">
                Core Responsibilities
              </h4>
              <ul className="space-y-1.5 text-xs text-zinc-300">
                {agent.responsibilities.map((resp, idx) => (
                  <li key={idx} className="flex items-start gap-2 bg-zinc-900/50 p-2.5 rounded-xl border border-white/5">
                    <CheckCircle className="w-3.5 h-3.5 text-orange-400 shrink-0 mt-0.5" />
                    <span>{resp}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Operational Guidelines */}
          {agent.guidelines && (
            <div>
              <h4 className="text-xs font-mono font-bold tracking-wider text-zinc-400 mb-1">
                Operational Guidelines & System Directives
              </h4>
              <p className="text-justify text-xs text-zinc-300 leading-relaxed bg-zinc-900/70 p-3.5 rounded-2xl border border-white/10">
                {agent.guidelines}
              </p>
            </div>
          )}

          {/* OpenCode Manifest Format Preview */}
          <div>
            <h4 className="text-xs font-mono font-bold tracking-wider text-zinc-400 mb-1 flex items-center gap-1.5">
              <FileCode className="w-3.5 h-3.5 text-orange-400" />
              <span>Generated OpenCode Card (.opencode/agents/{agent.name}.md)</span>
            </h4>
            <pre className="text-[11px] font-mono text-zinc-200 bg-zinc-950 p-3.5 rounded-2xl border border-white/10 overflow-x-auto leading-relaxed shadow-inner">
{`---
mode: subagent
name: ${agent.name}
description: "${agent.description}"
permission:
${agent.tools.map(t => `  ${t}: true`).join('\n')}
---
# ${agent.role} (@${agent.name})
Department: ${agent.department}
Reports To: ${agent.reportsTo}
`}
            </pre>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-white/10 bg-zinc-900/80 flex items-center justify-between">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-xs font-semibold text-zinc-300 transition-colors cursor-pointer"
          >
            Close
          </button>

          <button
            onClick={() => {
              onClose();
              onDispatchTask(agent);
            }}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-bold text-xs shadow-md shadow-orange-500/20 transition-all cursor-pointer"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Dispatch Task to @{agent.name}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
