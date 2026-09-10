import React from 'react';
import { 
  LayoutDashboard, 
  Users, 
  GitFork, 
  KanbanSquare, 
  LineChart, 
  BadgePercent, 
  ShieldAlert, 
  Compass
} from 'lucide-react';

interface NavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  pendingApprovalsCount: number;
  openEscalationsCount: number;
  totalAgentsCount: number;
  totalTasksCount: number;
}

export const Navigation: React.FC<NavigationProps> = ({
  activeTab,
  onTabChange,
  pendingApprovalsCount,
  openEscalationsCount,
  totalAgentsCount,
  totalTasksCount
}) => {
  const navItems = [
    { id: 'command', label: 'Command Center', icon: LayoutDashboard },
    { id: 'org_chart', label: 'Org Chart', icon: GitFork },
    { id: 'roster', label: 'Agent Roster', icon: Users, badge: totalAgentsCount },
    { id: 'kanban', label: 'Tasks Kanban', icon: KanbanSquare, badge: totalTasksCount },
    { id: 'kpis', label: 'KPIs & Analytics', icon: LineChart },
    { id: 'finance', label: 'Finance & Costs', icon: BadgePercent },
    { 
      id: 'approvals', 
      label: 'Approvals & Gates', 
      icon: ShieldAlert, 
      alertCount: pendingApprovalsCount + openEscalationsCount 
    },
    { id: 'mission', label: 'Mission & Brand', icon: Compass }
  ];

  return (
    <nav className="bg-[#090e2b] border-b border-[#172044] px-4 lg:px-8 py-2 overflow-x-auto scrollbar-none">
      <div className="flex items-center space-x-1 sm:space-x-2 min-w-max">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all cursor-pointer whitespace-nowrap ${
                isActive
                  ? 'bg-gradient-to-r from-[#00bfff]/20 to-[#070a40] text-[#00bfff] border border-[#00bfff]/50 shadow-sm shadow-[#00bfff]/10'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#12193e] border border-transparent'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-[#00bfff]' : 'text-slate-400'}`} />
              <span>{item.label}</span>

              {item.badge !== undefined && (
                <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isActive ? 'bg-[#00bfff]/20 text-[#00bfff]' : 'bg-slate-800 text-slate-400'
                }`}>
                  {item.badge}
                </span>
              )}

              {item.alertCount !== undefined && item.alertCount > 0 && (
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-rose-500/20 text-rose-300 font-bold border border-rose-500/40">
                  {item.alertCount}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};
