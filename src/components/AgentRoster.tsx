import React, { useState, useMemo } from 'react';
import { 
  Users, 
  Search, 
  Filter, 
  Terminal, 
  Shield, 
  Briefcase, 
  ExternalLink, 
  Send,
  Layers,
  ChevronRight
} from 'lucide-react';
import { Agent, Department } from '../types';

interface AgentRosterProps {
  agents: Agent[];
  departments: Department[];
  onSelectAgent: (agent: Agent) => void;
  onDispatchToAgent: (agent: Agent) => void;
}

export const AgentRoster: React.FC<AgentRosterProps> = ({
  agents,
  departments,
  onSelectAgent,
  onDispatchToAgent
}) => {
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [toolFilter, setToolFilter] = useState<string>('all');

  const roleTypes = ['all', 'Executive', 'Specialist', 'Manager', 'Board'];
  const canonicalTools = ['all', 'read', 'edit', 'bash', 'webfetch', 'task'];

  const filteredAgents = useMemo(() => {
    return agents.filter(agent => {
      const matchesSearch = search === '' ||
        agent.name.toLowerCase().includes(search.toLowerCase()) ||
        agent.role.toLowerCase().includes(search.toLowerCase()) ||
        agent.description.toLowerCase().includes(search.toLowerCase());

      const matchesDept = deptFilter === 'all' || 
        agent.department.toLowerCase() === deptFilter.toLowerCase();

      const matchesType = typeFilter === 'all' || 
        agent.type.toLowerCase() === typeFilter.toLowerCase();

      const matchesTool = toolFilter === 'all' || 
        agent.tools.includes(toolFilter);

      return matchesSearch && matchesDept && matchesType && matchesTool;
    });
  }, [agents, search, deptFilter, typeFilter, toolFilter]);

  return (
    <div className="space-y-5">
      {/* Top Filter Bar */}
      <div className="bg-[#0b102f] border border-[#1b2554] p-4 rounded-2xl shadow-md space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-white tracking-wider font-display flex items-center gap-2">
              <Users className="w-4 h-4 text-[#00bfff]" />
              Agent Roster Directory ({agents.length} Registered)
            </h2>
            <p className="text-justify text-xs text-slate-400">
              Complete catalog of autonomous AI workers generated into OpenCode-compatible execution manifests
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Showing:</span>
            <span className="text-xs font-bold text-[#00bfff] bg-[#00bfff]/10 px-2 py-0.5 rounded border border-[#00bfff]/30">
              {filteredAgents.length} Agents
            </span>
          </div>
        </div>

        {/* Filter controls row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 pt-2 border-t border-[#18224d]">
          {/* Search box */}
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search by role, name, keyword..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#00bfff]"
            />
          </div>

          {/* Department dropdown */}
          <div>
            <select
              value={deptFilter}
              onChange={(e) => setDeptFilter(e.target.value)}
              className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-[#00bfff]"
            >
              <option value="all">All Departments ({departments.length})</option>
              {departments.map(d => (
                <option key={d.id} value={d.name}>{d.name}</option>
              ))}
            </select>
          </div>

          {/* Role Type */}
          <div>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-[#00bfff]"
            >
              <option value="all">All Hierarchy Types</option>
              <option value="Executive">Executive / C-Suite</option>
              <option value="Specialist">Specialist / Worker</option>
              <option value="Manager">Manager</option>
              <option value="Board">Board Member</option>
            </select>
          </div>

          {/* Tool filter */}
          <div>
            <select
              value={toolFilter}
              onChange={(e) => setToolFilter(e.target.value)}
              className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-[#00bfff]"
            >
              <option value="all">Any Configured Tool</option>
              {canonicalTools.filter(t => t !== 'all').map(t => (
                <option key={t} value={t}>Has '{t}' tool</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Agents Card Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredAgents.map((agent) => (
          <div
            key={agent.name}
            className="bg-[#0b102f] border border-[#1b2554] hover:border-[#00bfff]/50 rounded-2xl p-4 shadow-md flex flex-col justify-between transition-all group"
          >
            <div>
              {/* Header: Name, Department badge, Type */}
              <div className="flex items-start justify-between gap-2">
                <div>
                  <h3 
                    onClick={() => onSelectAgent(agent)}
                    className="font-bold text-sm text-white group-hover:text-[#00bfff] transition-colors cursor-pointer"
                  >
                    {agent.role}
                  </h3>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="text-[10px] font-mono text-slate-400 bg-[#070b20] px-1.5 py-0.2 rounded border border-slate-800">
                      @{agent.name}
                    </span>
                    <span className="text-[10px] text-slate-400">
                      • {agent.department}
                    </span>
                  </div>
                </div>

                <span className={`text-[9px] font-bold px-2 py-0.5 rounded tracking-wider ${
                  agent.type === 'Executive' 
                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                    : agent.type === 'Board'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    : agent.type === 'Manager'
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                }`}>
                  {agent.type}
                </span>
              </div>

              {/* Description */}
              <p className="text-justify text-xs text-slate-300 mt-2.5 line-clamp-2 leading-relaxed">
                {agent.description || 'Specialized autonomous AI agent serving under departmental guidelines.'}
              </p>

              {/* Reports line */}
              <div className="text-[11px] text-slate-400 mt-2 flex items-center justify-between">
                <span>Reports to: <strong className="text-slate-300 font-mono">@{agent.reportsTo}</strong></span>
                {agent.directReports && agent.directReports.length > 0 && (
                  <span className="text-[#00bfff] font-medium text-[10px]">
                    {agent.directReports.length} reports
                  </span>
                )}
              </div>

              {/* Configured Tools */}
              <div className="flex flex-wrap gap-1 mt-3">
                {agent.tools.map((t, idx) => (
                  <span key={idx} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-[#101738] text-slate-300 border border-[#1b2554]">
                    {t}
                  </span>
                ))}
              </div>
            </div>

            {/* Footer actions */}
            <div className="flex items-center gap-2 mt-4 pt-3 border-t border-[#18224d]">
              <button
                onClick={() => onSelectAgent(agent)}
                className="flex-1 py-1.5 px-2 bg-[#121a42] hover:bg-[#182357] text-slate-200 border border-[#233370] rounded-xl text-xs font-semibold flex items-center justify-center gap-1 transition-colors cursor-pointer"
              >
                <span>Full Card</span>
                <ExternalLink className="w-3 h-3 text-[#00bfff]" />
              </button>

              <button
                onClick={() => onDispatchToAgent(agent)}
                className="py-1.5 px-2.5 bg-[#00bfff]/15 hover:bg-[#00bfff]/25 text-[#00bfff] border border-[#00bfff]/40 rounded-xl text-xs font-semibold flex items-center justify-center gap-1 transition-colors cursor-pointer"
                title={`Assign task to ${agent.name}`}
              >
                <Send className="w-3 h-3" />
                <span>Task</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredAgents.length === 0 && (
        <div className="text-center py-16 bg-[#0b102f] border border-[#1b2554] rounded-2xl">
          <p className="text-justify text-slate-400 text-sm">No agents match your active filters.</p>
          <button
            onClick={() => { setSearch(''); setDeptFilter('all'); setTypeFilter('all'); setToolFilter('all'); }}
            className="mt-2 text-xs text-[#00bfff] hover:underline"
          >
            Reset all filters
          </button>
        </div>
      )}
    </div>
  );
};
