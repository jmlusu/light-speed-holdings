import React, { useState } from 'react';
import { Plus, GripVertical, Trash2, Edit, ChevronRight } from 'lucide-react';
import { JobCard } from './JobCard';
import { cn } from '@/lib/athena/utils';
import type { Job, JobStatus, PipelineColumnProps } from '@/lib/athena/types';

const STATUS_COLORS: Record<JobStatus, { bg: string; border: string; text: string }> = {
  new: { bg: 'bg-ls-cyan/10', border: 'border-ls-cyan/30', text: 'text-ls-cyan' },
  fetched: { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-700' },
  matched: { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-700' },
  scored: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-700' },
  applied: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700' },
  interview: { bg: 'bg-emerald-50', border: 'border-emerald-200', text: 'text-emerald-700' },
  offer: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700' },
  rejected: { bg: 'bg-gray-50', border: 'border-gray-200', text: 'text-gray-500' },
  archived: { bg: 'bg-slate-50', border: 'border-slate-200', text: 'text-slate-500' },
};

const STATUS_LABELS: Record<JobStatus, string> = {
  new: 'New',
  fetched: 'Fetched',
  matched: 'Matched',
  scored: 'Scored',
  applied: 'Applied',
  interview: 'Interview',
  offer: 'Offer',
  rejected: 'Rejected',
  archived: 'Archived',
};

interface PipelineColumnInternalProps extends PipelineColumnProps {
  isDraggingOver?: boolean;
}

export const PipelineColumn: React.FC<PipelineColumnInternalProps> = ({
  status,
  title,
  jobs,
  onJobClick,
  onDragStart,
  onDragOver,
  onDrop,
  isDraggingOver = false,
}) => {
  const colors = STATUS_COLORS[status];
  const label = STATUS_LABELS[status];
  const [showAddForm, setShowAddForm] = useState(false);
  const [newJobTitle, setNewJobTitle] = useState('');

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    onDragOver?.(e, status);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    onDrop?.(e, status);
  };

  const handleAddJob = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newJobTitle.trim()) return;

    // In a real app, this would call an API
    const newJob: Job = {
      id: `temp-${Date.now()}`,
      source: 'other',
      title: newJobTitle,
      company: 'New Company',
      location: 'Remote',
      job_type: 'full_time',
      description: '',
      requirements: [],
      responsibilities: [],
      keywords: [],
      application_url: '#',
      benefits: [],
      status,
      scraped_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      metadata: {},
    };

    // This would typically be handled by parent state
    console.log('Add job:', newJob);
    setNewJobTitle('');
    setShowAddForm(false);
  };

  return (
    <div
      className={cn(
        'flex flex-col min-w-[320px] max-w-[360px] flex-shrink-0',
        'bg-ls-grey-light/50 rounded-xl border-2 transition-all duration-200',
        isDraggingOver
          ? 'border-ls-red bg-ls-red/5 ring-2 ring-ls-red/20'
          : `border-${colors.border}`
      )}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      role="list"
      aria-label={`${label} column`}
    >
      {/* Column Header */}
      <div
        className={cn(
          'flex items-center justify-between px-4 py-3 rounded-t-xl border-b',
          'border-ls-grey-dark/30',
          colors.bg
        )}
      >
        <div className="flex items-center gap-3">
          <span
            className={cn(
              'px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider',
              `border ${colors.border} ${colors.text} ${colors.bg.replace('bg-', 'bg-').replace('50', '100')}`
            )}
          >
            {label}
          </span>
          <span className="font-display font-bold text-sm text-ls-navy">
            {title}
          </span>
        </div>
        <span className="font-display font-bold text-lg text-ls-grey-dark">
          {jobs.length}
        </span>
      </div>

      {/* Job Cards */}
      <div
        className="flex-1 overflow-y-auto p-3 space-y-3 min-h-[400px]"
        role="list"
      >
        {jobs.map((job, index) => (
          <div
            key={job.id}
            className="relative"
            role="listitem"
          >
            <JobCard
              job={job}
              onClick={() => onJobClick(job)}
              compact
              showActions
            />
            {/* Drag handle */}
            <div
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
              draggable
              onDragStart={(e) => onDragStart?.(job)}
              tabIndex={0}
              role="button"
              aria-label={`Drag ${job.title} to reorder`}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  onDragStart?.(job);
                }
              }}
            >
              <GripVertical className="w-4 h-4 text-ls-grey-light-text cursor-grab" aria-hidden="true" />
            </div>
          </div>
        ))}

        {/* Empty state / Add job trigger */}
        {jobs.length === 0 && !showAddForm && (
          <button
            onClick={() => setShowAddForm(true)}
            className="w-full py-8 border-2 border-dashed border-ls-grey-dark/50 rounded-lg text-ls-grey-dark hover:border-ls-red hover:text-ls-red hover:bg-ls-red/5 transition-all flex flex-col items-center gap-2"
          >
            <Plus className="w-6 h-6" aria-hidden="true" />
            <span className="font-body text-sm">Add job to {label.toLowerCase()}</span>
          </button>
        )}

        {/* Add job form */}
        {showAddForm && (
          <form onSubmit={handleAddJob} className="p-3 space-y-3 border border-ls-grey-dark/30 rounded-lg bg-ls-white">
            <input
              type="text"
              value={newJobTitle}
              onChange={(e) => setNewJobTitle(e.target.value)}
              placeholder="Job title"
              className="w-full px-3 py-2 border border-ls-grey-dark rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-ls-red focus:border-transparent"
              autoFocus
              aria-label="Job title"
            />
            <div className="flex gap-2">
              <button
                type="submit"
                className="flex-1 py-2 px-3 bg-ls-red text-ls-white font-bold text-sm rounded-lg hover:bg-ls-red/90 transition-colors"
              >
                Add
              </button>
              <button
                type="button"
                onClick={() => { setShowAddForm(false); setNewJobTitle(''); }}
                className="flex-1 py-2 px-3 border border-ls-grey-dark text-ls-grey-dark font-bold text-sm rounded-lg hover:bg-ls-grey-light transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Column footer actions */}
      <div className="px-4 py-3 border-t border-ls-grey-dark/30 flex items-center justify-between">
        <span className="font-body text-xs text-ls-grey-light-text">
          {jobs.length} job{jobs.length !== 1 ? 's' : ''}
        </span>
      </div>
    </div>
  );
};

// Column header with drag indicator
export const PipelineColumnHeader: React.FC<{
  status: JobStatus;
  title: string;
  count: number;
  onAddClick?: () => void;
}> = ({ status, title, count, onAddClick }) => {
  const colors = STATUS_COLORS[status];
  const label = STATUS_LABELS[status];

  return (
    <div className={cn('flex items-center justify-between px-4 py-3', colors.bg, 'border-b', `border-${colors.border}`)}>
      <div className="flex items-center gap-3">
        <span className={cn('px-2.5 py-1 rounded-full text-[10px] font-bold tracking-wider', `border ${colors.border} ${colors.text} ${colors.bg.replace('50', '100')}`)}>
          {label}
        </span>
        <span className="font-display font-bold text-sm text-ls-navy">{title}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="font-display font-bold text-lg text-ls-grey-dark">{count}</span>
        {onAddClick && (
          <button
            onClick={onAddClick}
            className="p-1.5 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors"
            aria-label={`Add job to ${label}`}
          >
            <Plus className="w-4 h-4" aria-hidden="true" />
          </button>
        )}
      </div>
    </div>
  );
};
