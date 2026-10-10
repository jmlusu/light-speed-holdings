import React, { useState, useMemo } from 'react';
import { ChevronDown, Search, Bot, ShieldCheck, FileText } from 'lucide-react';
import publicAgentsRaw from '@/data/public-agent-registry.json';
import { DEPARTMENT_ORDER, DEPARTMENT_COLORS, TYPE_BADGES, HONESTY_LABELS } from '@/data/publicAgentRegistry';
import type { PublicAgent, AgentType } from '@/data/publicAgentRegistry';
import type { HonestyTone } from '@/data/siteContent';

const publicAgents: PublicAgent[] = (publicAgentsRaw as any[]).map(a => ({
  ...a,
  type: a.type as AgentType,
  honestyStatus: a.honestyStatus as HonestyTone,
}));

interface PublicAgentRegistryProps {
  theme: 'light' | 'dark';
}

const DEPARTMENT_LABELS: Record<string, string> = {
  'Executive': 'Executive Leadership',
  'Technology': 'Technology & Engineering',
  'AI Research': 'AI Research & Safety',
  'Operations': 'Operations & Orchestration',
  'Security': 'Security & Compliance',
  'Product': 'Product & Design',
  'Marketing': 'Marketing & Developer Relations',
  'Sales': 'Sales & Business Development',
  'Finance': 'Finance & Analytics',
  'Data': 'Data & Intelligence',
  'Legal': 'Legal & Privacy',
  'People': 'People & Culture',
  'Business Development': 'Business Development',
  'QA': 'Quality Assurance',
  'Customer Success': 'Customer Success',
};

export const PublicAgentRegistry: React.FC<PublicAgentRegistryProps> = ({ theme }) => {
  const isLight = theme === 'light';
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedDepts, setExpandedDepts] = useState<string[]>(['Executive', 'Technology', 'AI Research']);
  const [viewMode, setViewMode] = useState<'cards' | 'table'>('cards');
  const [selectedAgent, setSelectedAgent] = useState<PublicAgent | null>(null);

  // Group agents by department
  const agentsByDept = useMemo(() => {
    const filtered = publicAgents.filter(agent =>
      agent.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.department.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.capabilities.some(c => c.toLowerCase().includes(searchQuery.toLowerCase()))
    );
    const grouped: Record<string, PublicAgent[]> = {};
    filtered.forEach(agent => {
      if (!grouped[agent.department]) grouped[agent.department] = [];
      grouped[agent.department].push(agent);
    });
    return grouped;
  }, [searchQuery]);

  const departmentCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    Object.entries(agentsByDept).forEach(([dept, agents]) => {
      counts[dept] = agents.length;
    });
    return counts;
  }, [agentsByDept]);

  const totalVisible = useMemo(() =>
    Object.values(agentsByDept).reduce((sum, agents) => sum + agents.length, 0),
  [agentsByDept]);

  const toggleDept = (dept: string) => {
    setExpandedDepts(prev => prev.includes(dept)
      ? prev.filter(d => d !== dept)
      : [...prev, dept]
    );
  };

  const handleAgentClick = (agent: PublicAgent) => {
    setSelectedAgent(agent);
  };

  return (
    <section id="public-agent-registry" aria-label="Public Agent Registry">
      {/* Header */}
      <div className="mb-8 sm:mb-12">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <h2 className="font-display font-black text-2xl sm:text-3xl tracking-tight">
              Public Agent Registry
            </h2>
            <p className="mt-1 text-sm opacity-70">
              {totalVisible} of 90 agents — governed, auditable, human-led
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center">
            <div className="relative flex-1 max-w-xs">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 opacity-40" />
              <input
                type="search"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Search agents by role, capability, department..."
                className={`w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm outline-none focus:border-ls-red transition-colors ${
                  isLight
                    ? 'bg-ls-white border-ls-grey-dark text-ls-navy placeholder:text-ls-grey-dark'
                    : 'bg-ls-navy/80 border-ls-white/15 text-ls-white placeholder:text-ls-grey-light-text'
                }`} />
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('cards')}
                className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  viewMode === 'cards'
                    ? 'bg-ls-red text-ls-white shadow-md'
                    : isLight ? 'bg-ls-grey-light/50 text-ls-navy hover:bg-ls-grey-light' : 'bg-ls-white/5 text-ls-white hover:bg-ls-white/10'
                }`}>
                <Bot className="w-4 h-4 inline mr-1" /> Cards
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  viewMode === 'table'
                    ? 'bg-ls-red text-ls-white shadow-md'
                    : isLight ? 'bg-ls-grey-light/50 text-ls-navy hover:bg-ls-grey-light' : 'bg-ls-white/5 text-ls-white hover:bg-ls-white/10'
                }`}>
                <FileText className="w-4 h-4 inline mr-1" /> Table
              </button>
            </div>
          </div>
        </div>

        {/* Public Knowledge Boundary Notice */}
        <div className={`p-4 rounded-2xl border flex items-start gap-3 ${isLight
          ? 'bg-ls-cyan/5 border-ls-cyan/20 text-ls-grey-dark'
          : 'bg-ls-cyan/5 border-ls-cyan/20 text-ls-grey-light-text'}`} role="note">
          <ShieldCheck className="w-5 h-5 shrink-0 mt-0.5 text-ls-cyan" aria-hidden="true" />
          <div className="text-sm leading-relaxed">
            <strong className="text-ls-cyan">Public knowledge boundary.</strong> This registry displays only approved fields:
            name, role, type, department, public description, capabilities, and honesty status.
            Internal prompts, credentials, private tools, memory, orchestration logic, and security controls are not exposed.
          </div>
        </div>
      </div>

      {/* Registry Content */}
      {viewMode === 'cards' ? (
        <div className="space-y-6">
          {DEPARTMENT_ORDER.map(dept => {
            const agents = agentsByDept[dept];
            if (!agents || agents.length === 0) return null;
            const isExpanded = expandedDepts.includes(dept);
            const colors = DEPARTMENT_COLORS[dept] || { light: 'bg-ls-slate/10 text-ls-slate border-ls-slate/30', dark: 'bg-ls-slate/10 text-ls-slate border-ls-slate/30' };

            return (
              <div key={dept} className="space-y-4">
                <button
                  onClick={() => toggleDept(dept)}
                  className="w-full flex items-center justify-between p-4 rounded-2xl border transition-all"
                  style={{
                    backgroundColor: isLight ? '#F7F8F9' : '#1A1D21',
                    borderColor: isLight ? '#E5E7EB' : '#2A2D31',
                  }}>
                  <div className="flex items-center gap-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wider ${isLight ? colors.light : colors.dark}`}>
                      {DEPARTMENT_LABELS[dept] || dept}
                    </span>
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold tracking-wider ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark' : 'bg-ls-white/5 text-ls-white'}`}>
                      {agents.length} agents
                    </span>
                  </div>
                  <ChevronDown className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                </button>

                {isExpanded && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mt-2 animate-slide-down">
                    {agents.map(agent => (
                      <PublicAgentCard key={agent.name} agent={agent} theme={theme} onClick={handleAgentClick} />
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left" role="table">
            <thead>
              <tr className={`border-b ${isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'}`}>
                <th className="pb-3 text-xs font-body font-bold tracking-widest uppercase opacity-60">Agent</th>
                <th className="pb-3 text-xs font-body font-bold tracking-widest uppercase opacity-60">Department</th>
                <th className="pb-3 text-xs font-body font-bold tracking-widest uppercase opacity-60">Type</th>
                <th className="pb-3 text-xs font-body font-bold tracking-widest uppercase opacity-60">Honesty</th>
                <th className="pb-3 text-xs font-body font-bold tracking-widest uppercase opacity-60">Capabilities</th>
              </tr>
            </thead>
            <tbody>
              {DEPARTMENT_ORDER.map(dept => {
                const agents = agentsByDept[dept];
                if (!agents || agents.length === 0) return null;
                return agents.map(agent => (
                  <tr key={agent.name} className={`border-b ${isLight ? 'border-ls-grey-dark/10' : 'border-ls-white/5'} hover:bg-ls-red/5 transition-colors cursor-pointer`} onClick={() => handleAgentClick(agent)}>
                    <td className="py-4">
                      <div className="font-medium">{agent.role}</div>
                      <div className="text-xs opacity-60">{agent.name}</div>
                    </td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? DEPARTMENT_COLORS[agent.department]?.light : DEPARTMENT_COLORS[agent.department]?.dark}`}>
                        {DEPARTMENT_LABELS[agent.department] || agent.department}
                      </span>
                    </td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? TYPE_BADGES[agent.type].light : TYPE_BADGES[agent.type].dark}`}>
                        {TYPE_BADGES[agent.type].label}
                      </span>
                    </td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? HONESTY_LABELS[agent.honestyStatus].light : HONESTY_LABELS[agent.honestyStatus].dark}`}>
                        {HONESTY_LABELS[agent.honestyStatus].label}
                      </span>
                    </td>
                    <td className="py-4">
                      <div className="flex flex-wrap gap-1">
                        {agent.capabilities.slice(0, 3).map((cap, i) => (
                          <span key={i} className={`px-2 py-0.5 rounded text-[10px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>
                            {cap}
                          </span>
                        ))}
                        {agent.capabilities.length > 3 && (
                          <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark' : 'bg-ls-white/5 text-ls-grey-light-text'}`}>
                            +{agent.capabilities.length - 3}
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ));
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Agent Detail Modal */}
      {selectedAgent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={() => setSelectedAgent(null)}>
          <div className="absolute inset-0 bg-black/50" />
          <div className={`relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-3xl border shadow-2xl ${isLight ? 'bg-ls-white border-ls-grey-dark' : 'bg-ls-navy border-ls-white/15'}`} onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b flex items-start justify-between">
              <div className="flex items-center gap-4">
                <Bot className="w-10 h-10 rounded-xl bg-ls-red text-ls-white flex items-center justify-center" />
                <div>
                  <h3 className="font-display font-black text-xl">{selectedAgent.role}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? TYPE_BADGES[selectedAgent.type].light : TYPE_BADGES[selectedAgent.type].dark}`}>
                      {TYPE_BADGES[selectedAgent.type].label}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? DEPARTMENT_COLORS[selectedAgent.department]?.light : DEPARTMENT_COLORS[selectedAgent.department]?.dark}`}>
                      {DEPARTMENT_LABELS[selectedAgent.department] || selectedAgent.department}
                    </span>
                  </div>
                </div>
              </div>
              <button onClick={() => setSelectedAgent(null)} className="p-2 rounded-xl hover:bg-ls-red/10 text-ls-red transition-colors">×</button>
            </div>
            <div className="p-6 space-y-6">
              <div className="space-y-2">
                <p className="text-sm leading-relaxed">{selectedAgent.description}</p>
              </div>
              <div className="pt-4 border-t">
                <h4 className="font-bold text-sm mb-3">HAOMTGV Pillar Alignment</h4>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-navy/20 text-ls-navy">H</span>
                    <span className="text-xs text-ls-white/60">Human CEOs</span>
                  </div>
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-red/20 text-ls-red">A</span>
                    <span className="text-xs text-ls-white/60">Agents</span>
                  </div>
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-navy/20 text-ls-navy">O</span>
                    <span className="text-xs text-ls-white/60">Operating Model</span>
                  </div>
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-navy/20 text-ls-navy">M</span>
                    <span className="text-xs text-ls-white/60">Memory</span>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-4">
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-navy/20 text-ls-navy">T</span>
                    <span className="text-xs text-ls-white/60">Tools</span>
                  </div>
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-navy/20 text-ls-navy">G</span>
                    <span className="text-xs text-ls-white/60">Governance</span>
                  </div>
                  <div>
                    <span className="px-2 py-1 rounded text-[9px] font-medium bg-ls-navy/20 text-ls-navy">V</span>
                    <span className="text-xs text-ls-white/60">Visuals</span>
                  </div>
                </div>
              </div>
              <div className="pt-4 border-t">
                <h4 className="font-bold text-sm mb-3">Canonical 7 Tools Only</h4>
                <div className="flex flex-wrap gap-2">
                  <span key={1} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>read</span>
                  <span key={2} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>edit</span>
                  <span key={3} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>bash</span>
                  <span key={4} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>task</span>
                  <span key={5} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>webfetch</span>
                  <span key={6} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>code-structure</span>
                  <span key={7} className={`px-2 py-1 rounded-full text-[9px] font-medium ${isLight ? 'bg-ls-grey-light/50 text-ls-grey-dark border-ls-grey-dark/20' : 'bg-ls-white/5 text-ls-grey-light-text border-ls-white/10'}`}>jq</span>
                </div>
                <p className="text-xs text-ls-white/60 mt-3">Only these 7 tools are canonical; all others are rejected at runtime.</p>
              </div>
              <div className="pt-4 border-t">
                <h4 className="font-bold text-sm mb-3">HAOMTGV Compliance</h4>
                <p className="text-sm opacity-70">
                  This agent operates within the 5-tier HITL approval matrix (G1–G4 gates enforce Contract, DPA, Compliance, Security).
                  Every action generates append-only JSONL audit events with SHA-256 seals (CLAIM: registry.agents).
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

function PublicAgentCard({ agent, theme, onClick }: { agent: PublicAgent; theme: 'light' | 'dark'; onClick: (agent: PublicAgent) => void }) {
  const isLight = theme === 'light';
  const colors = DEPARTMENT_COLORS[agent.department] || { light: 'bg-ls-slate/10 text-ls-slate border-ls-slate/30', dark: 'bg-ls-slate/10 text-ls-slate border-ls-slate/30' };
  return (
    <button
      onClick={() => onClick(agent)}
      className={`group p-4 rounded-2xl border transition-all cursor-pointer h-full flex flex-col ${isLight
        ? 'bg-ls-white/95 border-ls-grey-dark shadow-sm hover:shadow-xl hover:-translate-y-0.5 hover:border-ls-red/50'
        : 'bg-ls-navy/80 border-ls-white/15 shadow-sm hover:shadow-xl hover:-translate-y-0.5 hover:border-ls-red/50'}`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <Bot className="w-8 h-8 rounded-xl bg-ls-red text-ls-white flex items-center justify-center shrink-0" />
          <div className="min-w-0">
            <h4 className="font-display font-bold text-sm truncate">{agent.role}</h4>
            <span className="text-[10px] font-mono opacity-50">{agent.name}</span>
          </div>
        </div>
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider shrink-0 ${isLight ? TYPE_BADGES[agent.type].light : TYPE_BADGES[agent.type].dark}`}>
          {TYPE_BADGES[agent.type].label}
        </span>
      </div>
      <p className="text-xs leading-relaxed flex-1 opacity-80 mb-4">{agent.description}</p>
      <div className="flex items-center justify-between pt-3 border-t">
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? HONESTY_LABELS[agent.honestyStatus].light : HONESTY_LABELS[agent.honestyStatus].dark}`}>
          {HONESTY_LABELS[agent.honestyStatus].label}
        </span>
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider ${isLight ? DEPARTMENT_COLORS[agent.department]?.light : DEPARTMENT_COLORS[agent.department]?.dark}`}>
          {DEPARTMENT_LABELS[agent.department] || agent.department}
        </span>
      </div>
    </button>
  );
}

export default PublicAgentRegistry;
