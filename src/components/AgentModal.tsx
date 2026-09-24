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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ls-navy/80 backdrop-blur-md animate-fade-in">
      <div
        className={`relative w-full max-w-2xl rounded-2xl border p-6 sm:p-8 shadow-2xl max-h-[90vh] overflow-y-auto ${
          isLight
            ? 'bg-ls-white border-ls-grey-dark text-ls-navy shadow-ls-red/10'
            : 'bg-[#070a40] border-ls-white text-ls-white shadow-ls-red/20'
        }`}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-full transition-colors ${
            isLight
              ? 'bg-ls-grey-light hover:bg-ls-grey-light text-ls-grey-dark'
              : 'bg-ls-navy hover:bg-ls-navy text-ls-grey-light-text'
          }`}
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-start gap-4 mb-6">
          <div className="p-3.5 rounded-xl bg-ls-red/10 border border-ls-red/30 text-ls-red shrink-0">
            <Cpu className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2.5 py-0.5 text-xs font-semibold rounded-full uppercase tracking-wider ${
                agent.type === 'Executive'
                  ? 'bg-ls-red/20 text-ls-red/40 border border-ls-red/30'
                  : agent.type === 'Board'
                  ? 'bg-ls-cyan/20 text-ls-cyan/80 border border-ls-cyan/30'
                  : 'bg-ls-red/20 text-ls-red/40 border border-ls-red/30'
              }`}>
                {agent.type} Agent
              </span>
              <span className="text-xs text-ls-grey-dark font-body">{agent.department}</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight">{agent.name}</h2>
            <p className="text-ls-red font-medium text-sm">{agent.role}</p>
          </div>
        </div>

        {/* Description */}
        <div className={`p-4 rounded-xl border mb-6 text-sm leading-relaxed ${
          isLight ? 'bg-ls-grey-light border-ls-grey-dark text-ls-grey-dark' : 'bg-ls-navy/60 border-ls-white text-ls-grey-light-text'
        }`}>
          {agent.description}
        </div>

        {/* Governance */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy/40 border-ls-white'}`}>
            <div className="flex items-center gap-2 text-xs font-body uppercase tracking-wider text-ls-grey-light-text mb-1">
              <Shield className="w-3.5 h-3.5 text-ls-red" />
              Agent Type
            </div>
            <div className="font-semibold text-sm">{agent.type}</div>
          </div>
          <div className={`p-4 rounded-xl border ${isLight ? 'bg-ls-grey-light border-ls-grey-dark' : 'bg-ls-navy/40 border-ls-white'}`}>
            <div className="flex items-center gap-2 text-xs font-body uppercase tracking-wider text-ls-grey-light-text mb-1">
              <UserCheck className="w-3.5 h-3.5 text-ls-cyan" />
              Reports To
            </div>
            <div className="font-semibold text-sm">{agent.reportsTo}</div>
          </div>
        </div>

        {/* Responsibilities */}
        {agent.responsibilities && agent.responsibilities.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xs font-body uppercase tracking-wider text-ls-grey-light-text mb-3 flex items-center gap-2">
              <Award className="w-4 h-4 text-ls-red" /> Core Responsibilities
            </h3>
            <ul className="space-y-2">
              {agent.responsibilities.map((resp, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-sm text-ls-grey-light-text">
                  <CheckCircle2 className="w-4 h-4 text-ls-red shrink-0 mt-0.5" />
                  <span>{resp}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Tools */}
        {agent.tools && agent.tools.length > 0 && (
          <div className="mb-8">
            <h3 className="text-xs font-body uppercase tracking-wider text-ls-grey-light-text mb-3 flex items-center gap-2">
              <Terminal className="w-4 h-4 text-ls-red" /> Authorized Toolset
            </h3>
            <div className="flex flex-wrap gap-2">
              {agent.tools.map((tool, idx) => (
                <span
                  key={idx}
                  className={`px-3 py-1 rounded-lg text-xs font-body border ${
                    isLight
                      ? 'bg-ls-grey-light border-ls-grey-dark text-ls-grey-dark'
                      : 'bg-ls-navy/80 border-ls-white text-ls-grey-light-text'
                  }`}
                >
                  {tool}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Action button */}
        <div className="flex justify-end gap-3 pt-4 border-t border-ls-white">
          <button
            onClick={onClose}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
              isLight ? 'bg-ls-grey-light hover:bg-ls-grey-light text-ls-grey-dark' : 'bg-ls-navy hover:bg-ls-navy text-ls-grey-light-text'
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
              className="flex items-center gap-2 px-5 py-2 rounded-xl text-sm font-medium bg-ls-red hover:bg-ls-red/85 text-ls-navy font-bold transition-all shadow-lg shadow-ls-red/20"
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
