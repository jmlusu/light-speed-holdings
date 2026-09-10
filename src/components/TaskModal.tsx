import React, { useState, useEffect } from 'react';
import { 
  X, 
  Send, 
  KanbanSquare, 
  User, 
  AlertCircle, 
  CheckCircle, 
  Layers,
  FileText
} from 'lucide-react';
import { TaskItem, TaskPriority, Agent } from '../types';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateTask: (newTask: Omit<TaskItem, 'id' | 'created_at' | 'updated_at'>) => void;
  agents: Agent[];
  preselectedAgent?: Agent | null;
  taskToInspect?: TaskItem | null;
}

export const TaskModal: React.FC<TaskModalProps> = ({
  isOpen,
  onClose,
  onCreateTask,
  agents,
  preselectedAgent,
  taskToInspect
}) => {
  if (!isOpen && !taskToInspect) return null;

  const isInspectMode = !!taskToInspect;

  const [title, setTitle] = useState('');
  const [instruction, setInstruction] = useState('');
  const [receiverId, setReceiverId] = useState(preselectedAgent?.name || 'lead-backend');
  const [priority, setPriority] = useState<TaskPriority>('P2');
  const [senderId, setSenderId] = useState('human-ceo');

  React.useEffect(() => {
    if (preselectedAgent) {
      setReceiverId(preselectedAgent.name);
    }
  }, [preselectedAgent]);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !instruction.trim()) return;

    const assignedAgent = agents.find(a => a.name === receiverId);
    const department = assignedAgent?.department || 'Technology';

    onCreateTask({
      title: title.trim(),
      instruction: instruction.trim(),
      status: 'pending',
      priority,
      sender_id: senderId,
      receiver_id: receiverId,
      department
    });

    setTitle('');
    setInstruction('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4 pt-16 sm:pt-20 overflow-y-auto">
      <div className="bg-[#0b102f] border border-[#1b2554] rounded-2xl max-w-xl w-full shadow-2xl overflow-hidden my-auto relative">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-[#1b2554] bg-[#090e2b] relative z-10">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-[#00bfff]/15 border border-[#00bfff]/30 flex items-center justify-center text-[#00bfff]">
              <KanbanSquare className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-display">
                {isInspectMode ? `Task Details (${taskToInspect?.id})` : 'Dispatch Autonomous Task'}
              </h3>
              <p className="text-justify text-xs text-slate-400">
                {isInspectMode ? 'Inspection of task payload and execution status' : 'Assigns a verified mandate to an autonomous agent'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            type="button"
            aria-label="Close modal"
            title="Close modal"
            className="relative z-50 w-9 h-9 rounded-xl bg-[#141e48] hover:bg-[#1a2862] text-slate-200 hover:text-white flex items-center justify-center transition-all cursor-pointer border border-[#1b2554] shadow-md shrink-0"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {isInspectMode ? (
          /* Inspect Mode Content */
          <div className="p-6 space-y-4 text-xs">
            <div className="flex items-center justify-between bg-[#0e163b] p-3 rounded-xl border border-[#1e2a58]">
              <div>
                <span className="text-slate-400 block text-[10px]">Status</span>
                <span className="font-bold text-white text-sm capitalize">{taskToInspect?.status}</span>
              </div>
              <div className="text-right">
                <span className="text-slate-400 block text-[10px]">Priority</span>
                <span className="font-bold text-[#00bfff] text-sm">{taskToInspect?.priority}</span>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-slate-400 mb-1">Title</h4>
              <p className="text-justify text-white text-sm font-bold bg-[#0e163b] p-3 rounded-xl border border-[#1e2a58]">
                {taskToInspect?.title}
              </p>
            </div>

            <div>
              <h4 className="font-semibold text-slate-400 mb-1">Instruction Payload</h4>
              <p className="text-justify text-slate-200 bg-[#0e163b] p-3 rounded-xl border border-[#1e2a58] leading-relaxed">
                {taskToInspect?.instruction}
              </p>
            </div>

            {taskToInspect?.result && (
              <div>
                <h4 className="font-semibold text-emerald-400 mb-1">Execution Output</h4>
                <p className="text-justify text-emerald-200 bg-emerald-950/20 p-3 rounded-xl border border-emerald-500/30 leading-relaxed">
                  {taskToInspect.result}
                </p>
              </div>
            )}

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 bg-[#0e163b] rounded-xl border border-[#1e2a58]">
                <span className="text-slate-400 block text-[10px]">Assigned Specialist</span>
                <span className="font-bold text-white font-mono">@{taskToInspect?.receiver_id}</span>
              </div>
              <div className="p-3 bg-[#0e163b] rounded-xl border border-[#1e2a58]">
                <span className="text-slate-400 block text-[10px]">Department</span>
                <span className="font-bold text-white">{taskToInspect?.department}</span>
              </div>
            </div>

            <div className="pt-2 border-t border-[#1b2554] flex justify-end">
              <button
                onClick={onClose}
                className="px-4 py-2 rounded-xl bg-[#141e48] text-slate-200 font-semibold text-xs hover:bg-[#1a2862]"
              >
                Close
              </button>
            </div>
          </div>
        ) : (
          /* Create Task Form */
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Task Title / Objective
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Implement rate limiter for external webhooks"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#00bfff]"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Assignee Agent (144 Fleet)
                </label>
                <select
                  value={receiverId}
                  onChange={(e) => setReceiverId(e.target.value)}
                  className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#00bfff]"
                >
                  {agents.map(a => (
                    <option key={a.name} value={a.name}>
                      {a.role} (@{a.name})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Priority Level
                </label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value as TaskPriority)}
                  className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#00bfff]"
                >
                  <option value="P0">P0 - Urgent (Production / Blocker)</option>
                  <option value="P1">P1 - High Priority</option>
                  <option value="P2">P2 - Normal Operations</option>
                  <option value="P3">P3 - Low / Background</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Sender Authority
              </label>
              <select
                value={senderId}
                onChange={(e) => setSenderId(e.target.value)}
                className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-[#00bfff]"
              >
                <option value="human-ceo">Human CEO (Jack Mlusu)</option>
                <option value="chief-of-staff">Chief of Staff</option>
                <option value="cto">Chief Technology Officer (CTO)</option>
                <option value="cfo">Chief Financial Officer (CFO)</option>
                <option value="coo">Chief Operating Officer (COO)</option>
                <option value="ciso">Chief Information Security Officer (CISO)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Instruction Payload & Acceptance Criteria
              </label>
              <textarea
                required
                rows={4}
                placeholder="Specify precise guidelines, constraints, and definition of done..."
                value={instruction}
                onChange={(e) => setInstruction(e.target.value)}
                className="w-full bg-[#0e163b] border border-[#1e2a58] rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#00bfff]"
              />
            </div>

            <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-[#1b2554]">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl bg-[#141e48] hover:bg-[#1a2862] text-xs font-semibold text-slate-300 transition-colors cursor-pointer"
              >
                Cancel
              </button>

              <button
                type="submit"
                className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-[#00bfff] to-[#0099cc] hover:from-[#33ccff] hover:to-[#00bfff] text-[#070a40] font-bold text-xs shadow-md shadow-[#00bfff]/20 transition-all cursor-pointer"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Dispatch to Inbox</span>
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
