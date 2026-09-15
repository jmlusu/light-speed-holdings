import React from 'react';
import { X, Shield, Cpu, Terminal, CheckCircle2, Award, Zap, ArrowRight, UserCheck } from 'lucide-react';
import { Agent } from '../types';

interface AgentModalProps {
  agent: Agent | null;
  onClose: () => void;
  onDispatchTask?: (agent: Agent) => void;
  theme?: 'light' | 'dark';
}

export const AgentModal: React.FC<AgentModalProps> = ({
  agent,
  onClose,
  onDispatchTask,
  theme = 'dark'
}) => {
  if (!agent) return null;
  const isLight = theme === 'light';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div
        className={`relative w-full max-w-2xl rounded-2xl border p-6 sm:p-8 shadow-2xl max-h-[90vh] overflow-y-auto ${
          isLight
            ? 'bg-white border-slate-200 text-slate-900 shadow-amber-500/10'
            : 'bg-[#070a40] border-slate-800 text-slate-100 shadow-amber-500/20'
        }`}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-full transition-colors ${
            isLight
              ? 'bg-slate-100 hover:bg-slate-200 text-slate-600'
              : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
          }`}
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-start gap-4 mb-6">
          <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-500 shrink-0">
            <Cpu className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2.5 py-0.5 text-xs font-semibold rounded-full uppercase tracking-wider ${
                agent.type === 'Executive'
                  ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                  : agent.type === 'Board'
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
              }`}>
                {agent.type} Agent
              </span>
              <span className="text-xs text-slate-500 font-mono">{agent.department}</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight">{agent.name}</h2>
            <p className="text-amber-500 font-medium text-sm">{agent.role}</p>
          </div>
        </div>

        {/* Description */}
        <div className={`p-4 rounded-xl border mb-6 text-sm leading-relaxed ${
          isLight ? 'bg-slate-50 border-slate-200 text-slate-700' : 'bg-slate-900/60 border-slate-800 text-slate-300'
        }`}>
          {agent.description}
        </div>

        {/* Governance & Permission */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-slate-900/40 border-slate-800'}`}>
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-slate-400 mb-1">
              <Shield className="w-3.5 h-3.5 text-amber-500" />
              Permission Tier
            </div>
            <div className="font-semibold text-sm">{agent.permission}</div>
          </div>
          <div className={`p-4 rounded-xl border ${isLight ? 'bg-slate-50 border-slate-200' : 'bg-slate-900/40 border-slate-800'}`}>
            <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-slate-400 mb-1">
              <UserCheck className="w-3.5 h-3.5 text-emerald-500" />
              Reports To
            </div>
            <div className="font-semibold text-sm">{agent.reportsTo}</div>
          </div>
        </div>

        {/* Responsibilities */}
        {agent.responsibilities && agent.responsibilities.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
              <Award className="w-4 h-4 text-amber-500" /> Core Responsibilities
            </h3>
            <ul className="space-y-2">
              {agent.responsibilities.map((resp, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-sm text-slate-300">
                  <CheckCircle2 className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  <span>{resp}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Tools */}
        {agent.tools && agent.tools.length > 0 && (
          <div className="mb-8">
            <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
              <Terminal className="w-4 h-4 text-amber-500" /> Authorized Toolset
            </h3>
            <div className="flex flex-wrap gap-2">
              {agent.tools.map((tool, idx) => (
                <span
                  key={idx}
                  className={`px-3 py-1 rounded-lg text-xs font-mono border ${
                    isLight
                      ? 'bg-slate-100 border-slate-200 text-slate-700'
                      : 'bg-slate-800/80 border-slate-700 text-slate-300'
                  }`}
                >
                  {tool}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Action button */}
        <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
          <button
            onClick={onClose}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
              isLight ? 'bg-slate-100 hover:bg-slate-200 text-slate-700' : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
            }`}
          >
            Close
          </button>
          {onDispatchTask && (
            <button
              onClick={() => {
                onDispatchTask(agent);
                onClose();
              }}
              className="flex items-center gap-2 px-5 py-2 rounded-xl text-sm font-medium bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold transition-all shadow-lg shadow-amber-500/20"
            >
              <Zap className="w-4 h-4" />
              Dispatch Task to {agent.name}
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
