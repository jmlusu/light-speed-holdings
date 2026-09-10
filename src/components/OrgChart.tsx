import React, { useState, useMemo } from 'react';
import { 
  GitFork, 
  Users, 
  ChevronDown, 
  ChevronRight, 
  Search, 
  Shield, 
  Cpu, 
  Terminal, 
  ExternalLink,
  Layers
} from 'lucide-react';
import { Agent, Department } from '../types';

interface OrgChartProps {
  agents: Agent[];
  departments: Department[];
  onSelectAgent: (agent: Agent) => void;
}

interface TreeNode {
  agent: Agent;
  children: TreeNode[];
}

export const OrgChart: React.FC<OrgChartProps> = ({ agents, departments, onSelectAgent }) => {
  const [search, setSearch] = useState('');
  const [selectedDept, setSelectedDept] = useState('all');
  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>({
    'human-ceo': true,
    'chief-of-staff': true,
    'cto': true,
    'cfo': true,
    'coo': true
  });

  const toggleExpand = (agentName: string) => {
    setExpandedNodes(prev => ({
      ...prev,
      [agentName]: !prev[agentName]
    }));
  };

  const expandAll = () => {
    const all: Record<string, boolean> = {};
    agents.forEach(a => { all[a.name] = true; });
    setExpandedNodes(all);
  };

  const collapseAll = () => {
    setExpandedNodes({ 'human-ceo': true });
  };

  // Build the hierarchical tree
  const tree = useMemo(() => {
    const agentMap = new Map<string, TreeNode>();

    // Add CEO stub if not explicitly in agents
    const ceoAgent: Agent = agents.find(a => a.name === 'human-ceo') || {
      name: 'human-ceo',
      role: 'Human Chief Executive Officer',
      type: 'Executive',
      department: 'Executive',
      reportsTo: 'board',
      description: 'Founder and Human CEO providing executive stewardship, strategic mandates, and constitutional governance.',
      responsibilities: ['Overall company vision', 'Constitutional oversight', 'Capital allocation', 'Final HITL approval'],
      tools: ['read', 'edit', 'bash', 'delegate'],
      permission: 'Execute'
    };

    agentMap.set('human-ceo', { agent: ceoAgent, children: [] });

    agents.forEach(a => {
      if (a.name !== 'human-ceo') {
        agentMap.set(a.name, { agent: a, children: [] });
      }
    });

    // Populate children
    agents.forEach(a => {
      if (a.name === 'human-ceo') return;
      const reportsTo = a.reportsTo || 'chief-of-staff';
      const parent = agentMap.get(reportsTo);
      const current = agentMap.get(a.name);
      if (parent && current) {
        parent.children.push(current);
      } else if (current && reportsTo === 'human-ceo') {
        const root = agentMap.get('human-ceo');
        if (root) root.children.push(current);
      }
    });

    return agentMap.get('human-ceo');
  }, [agents]);

  // Recursive Tree Node Renderer
  const renderNode = (node: TreeNode, depth: number = 0) => {
    const isExpanded = !!expandedNodes[node.agent.name];
    const hasChildren = node.children.length > 0;
    const matchesSearch = search === '' || 
      node.agent.name.toLowerCase().includes(search.toLowerCase()) || 
      node.agent.role.toLowerCase().includes(search.toLowerCase()) ||
      node.agent.department.toLowerCase().includes(search.toLowerCase());
    
    const matchesDept = selectedDept === 'all' || node.agent.department.toLowerCase() === selectedDept.toLowerCase();

    const isMatch = matchesSearch && (selectedDept === 'all' || matchesDept);

    return (
      <div key={node.agent.name} className="relative ml-4 md:ml-6 border-l-2 border-[#1e2a58] pl-3 py-1">
        <div 
          className={`flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-3 rounded-xl border transition-all ${
            isMatch 
              ? 'bg-[#0e163b] hover:bg-[#131d4d] border-[#1e2a58] hover:border-[#00bfff]/40' 
              : 'opacity-40 bg-[#090e28] border-transparent'
          }`}
        >
          <div className="flex items-center gap-2.5">
            {hasChildren ? (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleExpand(node.agent.name);
                }}
                className="w-6 h-6 flex items-center justify-center rounded bg-[#16204d] hover:bg-[#1e2a66] text-[#00bfff] transition-colors cursor-pointer"
              >
                {isExpanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
              </button>
            ) : (
              <span className="w-6 h-6 flex items-center justify-center text-slate-600">•</span>
            )}

            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="font-bold text-xs text-white hover:text-[#00bfff] transition-colors cursor-pointer" onClick={() => onSelectAgent(node.agent)}>
                  {node.agent.role}
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-300">
                  {node.agent.name}
                </span>
                <span className={`text-[9px] font-semibold px-1.5 py-0.2 rounded ${
                  node.agent.type === 'Executive' 
                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' 
                    : node.agent.type === 'Manager'
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    : node.agent.type === 'Board'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                }`}>
                  {node.agent.type}
                </span>
              </div>
              <div className="text-[11px] text-slate-400 mt-0.5 flex items-center gap-2">
                <span>Dept: <strong className="text-slate-300">{node.agent.department}</strong></span>
                {hasChildren && (
                  <span className="text-[10px] text-[#00bfff] bg-[#00bfff]/10 px-1.5 py-0.2 rounded">
                    {node.children.length} Direct Reports
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 self-end sm:self-center">
            <div className="hidden md:flex items-center gap-1">
              {node.agent.tools.slice(0, 3).map((tool, idx) => (
                <span key={idx} className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-[#070b20] text-slate-400 border border-slate-800">
                  {tool}
                </span>
              ))}
              {node.agent.tools.length > 3 && (
                <span className="text-[9px] font-mono px-1 rounded bg-[#070b20] text-slate-500">
                  +{node.agent.tools.length - 3}
                </span>
              )}
            </div>

            <button
              onClick={() => onSelectAgent(node.agent)}
              className="px-2.5 py-1 rounded-lg bg-[#141e48] hover:bg-[#1a2862] text-[11px] font-semibold text-[#00bfff] border border-[#00bfff]/30 transition-colors flex items-center gap-1 cursor-pointer"
            >
              <span>Inspect</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        </div>

        {hasChildren && isExpanded && (
          <div className="mt-1 space-y-1">
            {node.children.map(child => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-5">
      {/* Header & Filter Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#0b102f] border border-[#1b2554] p-4 rounded-2xl shadow-md">
        <div>
          <h2 className="text-base font-bold text-white tracking-wider font-display flex items-center gap-2">
            <GitFork className="w-4 h-4 text-[#00bfff]" />
            Organizational Reporting Structure
          </h2>
          <p className="text-justify text-xs text-slate-400">
            Hierarchical chain of command mapping 144 agents from Human CEO through Executive C-Suite to Specialists
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search tree..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-[#0e163b] border border-[#1e2a58] rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-[#00bfff] w-36 sm:w-48"
            />
          </div>

          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="bg-[#0e163b] border border-[#1e2a58] rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-[#00bfff]"
          >
            <option value="all">All Departments (20)</option>
            {departments.map(d => (
              <option key={d.id} value={d.name}>{d.name}</option>
            ))}
          </select>

          <button
            onClick={expandAll}
            className="px-2.5 py-1.5 rounded-lg bg-[#141e48] hover:bg-[#1a2862] text-xs text-slate-300 transition-colors cursor-pointer"
          >
            Expand All
          </button>
          <button
            onClick={collapseAll}
            className="px-2.5 py-1.5 rounded-lg bg-[#141e48] hover:bg-[#1a2862] text-xs text-slate-300 transition-colors cursor-pointer"
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* Org Tree View */}
      <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl p-4 md:p-6 shadow-md overflow-x-auto">
        {tree ? (
          renderNode(tree)
        ) : (
          <div className="text-center py-12 text-slate-400 text-sm">
            Building organizational tree...
          </div>
        )}
      </div>
    </div>
  );
};
