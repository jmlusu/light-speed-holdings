import React, { useState } from 'react';
import { 
  KanbanSquare, 
  Plus, 
  Clock, 
  ArrowRight, 
  AlertCircle, 
  CheckCircle, 
  User, 
  AlertTriangle,
  FileText
} from 'lucide-react';
import { TaskItem, TaskStatus, TaskPriority, Agent } from '../types';

interface TaskKanbanProps {
  tasks: TaskItem[];
  agents: Agent[];
  onUpdateTaskStatus: (taskId: string, newStatus: TaskStatus) => void;
  onOpenNewTaskModal: () => void;
  onSelectTask: (task: TaskItem) => void;
}

export const TaskKanban: React.FC<TaskKanbanProps> = ({
  tasks,
  agents,
  onUpdateTaskStatus,
  onOpenNewTaskModal,
  onSelectTask
}) => {
  const columns: { id: TaskStatus; label: string; color: string; border: string; bg: string }[] = [
    { id: 'pending', label: 'Backlog / Pending', color: 'text-slate-300', border: 'border-slate-700', bg: 'bg-slate-900/40' },
    { id: 'in_progress', label: 'In Progress', color: 'text-cyan-400', border: 'border-cyan-500/40', bg: 'bg-cyan-950/20' },
    { id: 'review', label: 'Under Review / Gate', color: 'text-amber-400', border: 'border-amber-500/40', bg: 'bg-amber-950/20' },
    { id: 'completed', label: 'Completed', color: 'text-emerald-400', border: 'border-emerald-500/40', bg: 'bg-emerald-950/20' },
    { id: 'escalated', label: 'Escalated to Human', color: 'text-rose-400', border: 'border-rose-500/40', bg: 'bg-rose-950/20' }
  ];

  const getPriorityBadge = (priority: TaskPriority) => {
    switch (priority) {
      case 'P0':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">P0 URGENT</span>;
      case 'P1':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">P1 HIGH</span>;
      case 'P2':
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300 border border-blue-500/40">P2 NORMAL</span>;
      default:
        return <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-slate-800 text-slate-400">P3 LOW</span>;
    }
  };

  const getNextStatus = (current: TaskStatus): TaskStatus | null => {
    if (current === 'pending') return 'in_progress';
    if (current === 'in_progress') return 'review';
    if (current === 'review') return 'completed';
    return null;
  };

  return (
    <div className="space-y-5">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 bg-[#0b102f] border border-[#1b2554] p-4 rounded-2xl shadow-md">
        <div>
          <h2 className="text-base font-bold text-white tracking-wider font-display flex items-center gap-2">
            <KanbanSquare className="w-4 h-4 text-[#00bfff]" />
            Agent Task Distribution Pipeline
          </h2>
          <p className="text-justify text-xs text-slate-400">
            Real-time execution status of tasks dispatched through the orchestrator inbox (.opencode/inbox.json)
          </p>
        </div>

        <button
          onClick={onOpenNewTaskModal}
          className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-gradient-to-r from-[#00bfff] to-[#0099cc] hover:from-[#33ccff] hover:to-[#00bfff] text-[#070a40] font-bold text-xs shadow-md shadow-[#00bfff]/20 transition-all cursor-pointer self-start md:self-auto"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Dispatch New Task</span>
        </button>
      </div>

      {/* Kanban Board Columns */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 overflow-x-auto">
        {columns.map((col) => {
          const colTasks = tasks.filter(t => t.status === col.id);
          return (
            <div
              key={col.id}
              className={`rounded-2xl border ${col.border} ${col.bg} p-3.5 flex flex-col min-h-[500px] shadow-md`}
            >
              {/* Column Header */}
              <div className="flex items-center justify-between pb-3 border-b border-[#1b2554] mb-3">
                <span className={`text-xs font-bold tracking-wider ${col.color}`}>
                  {col.label}
                </span>
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-[#0a0f2b] text-slate-300 border border-[#1a234d]">
                  {colTasks.length}
                </span>
              </div>

              {/* Tasks in Column */}
              <div className="space-y-3 flex-1 overflow-y-auto">
                {colTasks.map((task) => {
                  const nextStatus = getNextStatus(task.status);
                  return (
                    <div
                      key={task.id}
                      className="bg-[#0e163b] hover:bg-[#131d4b] border border-[#1e2a58] hover:border-[#00bfff]/50 rounded-xl p-3 shadow transition-all flex flex-col justify-between group"
                    >
                      <div>
                        <div className="flex items-center justify-between gap-1 mb-1.5">
                          <span className="text-[10px] font-mono text-slate-400 font-semibold">{task.id}</span>
                          {getPriorityBadge(task.priority)}
                        </div>

                        <h4 
                          onClick={() => onSelectTask(task)}
                          className="text-xs font-bold text-white group-hover:text-[#00bfff] transition-colors line-clamp-2 cursor-pointer"
                        >
                          {task.title}
                        </h4>

                        <p className="text-justify text-[11px] text-slate-300 mt-1 line-clamp-2 leading-relaxed">
                          {task.instruction}
                        </p>

                        {task.result && (
                          <div className="mt-2 p-1.5 rounded bg-emerald-950/30 border border-emerald-500/30 text-[10px] text-emerald-300 leading-snug">
                            <strong>Output:</strong> {task.result}
                          </div>
                        )}

                        <div className="mt-2.5 pt-2 border-t border-[#18234e] flex items-center justify-between text-[10px] text-slate-400">
                          <span className="truncate max-w-[120px]">
                            To: <strong className="text-slate-200 font-mono">@{task.receiver_id}</strong>
                          </span>
                          <span className="px-1.5 py-0.2 rounded bg-[#0a0f2b] text-slate-400">
                            {task.department}
                          </span>
                        </div>
                      </div>

                      {/* Action buttons */}
                      <div className="flex items-center gap-1.5 mt-3 pt-2 border-t border-[#18234e]">
                        {nextStatus && (
                          <button
                            onClick={() => onUpdateTaskStatus(task.id, nextStatus)}
                            className="flex-1 py-1 px-2 rounded-lg bg-[#141e48] hover:bg-[#1a2862] text-[10px] font-semibold text-[#00bfff] border border-[#00bfff]/30 transition-colors flex items-center justify-center gap-1 cursor-pointer"
                          >
                            <span>Advance</span>
                            <ArrowRight className="w-2.5 h-2.5" />
                          </button>
                        )}

                        {task.status !== 'escalated' && task.status !== 'completed' && (
                          <button
                            onClick={() => onUpdateTaskStatus(task.id, 'escalated')}
                            className="py-1 px-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-[10px] font-semibold text-rose-300 border border-rose-500/30 transition-colors cursor-pointer"
                            title="Escalate to Human CEO"
                          >
                            <AlertTriangle className="w-3 h-3" />
                          </button>
                        )}

                        <button
                          onClick={() => onSelectTask(task)}
                          className="py-1 px-2 rounded-lg bg-[#12193e] hover:bg-[#192354] text-[10px] text-slate-300 transition-colors cursor-pointer"
                          title="Inspect task JSON"
                        >
                          <FileText className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  );
                })}

                {colTasks.length === 0 && (
                  <div className="h-32 flex items-center justify-center text-slate-500 text-[11px] border border-dashed border-slate-800 rounded-xl">
                    No tasks in {col.label.toLowerCase()}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
