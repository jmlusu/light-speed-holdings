import React, { useEffect, useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { TrendingUp, TrendingDown, Minus, Target, Users, DollarSign, Clock, Award, RefreshCw, Download, FileText } from 'lucide-react';
import { MetricCard, MetricCardLarge, StatCounter } from '@/components/athena/MetricCard';
import { AreaChart, MountainAreaChart, CircularGaugeChart } from '@/components/athena/AreaChart';
import { JobCard } from '@/components/athena/JobCard';
import { PipelineColumn } from '@/components/athena/PipelineColumn';
import { ATSGauge, MiniATSGauge } from '@/components/athena/ATSGauge';
import { cn, formatRelativeTime, groupBy, sortBy } from '@/lib/athena/utils';
import { listJobs, getPipelineStats, getScrapingStats, triggerScrape } from '@/lib/athena/api';
import type { Job, JobStatus, PipelineStatsResponse } from '@/lib/athena/types';

const PIPELINE_STAGES: Array<{ status: JobStatus; title: string; order: number }> = [
  { status: 'new', title: 'New', order: 1 },
  { status: 'fetched', title: 'Fetched', order: 2 },
  { status: 'matched', title: 'Matched', order: 3 },
  { status: 'scored', title: 'Scored', order: 4 },
  { status: 'applied', title: 'Applied', order: 5 },
  { status: 'interview', title: 'Interview', order: 6 },
  { status: 'offer', title: 'Offer', order: 7 },
];

export const AthenaDashboard: React.FC = () => {
  const location = useLocation();
  const [stats, setStats] = useState<PipelineStatsResponse | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [recentJobs, setRecentJobs] = useState<Job[]>([]);
  const [atsDistribution, setAtsDistribution] = useState<Array<{ range: string; count: number }>>([]);
  const [matchTierDistribution, setMatchTierDistribution] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [draggedJob, setDraggedJob] = useState<Job | null>(null);
  const metricsContainerRef = useRef<HTMLDivElement>(null);
  const filtersContainerRef = useRef<HTMLDivElement>(null);

  // Load data on mount
  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [statsData, jobsData, scrapeData] = await Promise.all([
        getPipelineStats(),
        listJobs({ limit: 100 }),
        getScrapingStats(),
      ]);

      setStats(statsData);
      setJobs(jobsData.jobs);
      setRecentJobs(jobsData.jobs.slice(0, 5));

      // Calculate ATS score distribution
      const atsScores = jobsData.jobs.filter(j => j.ats_score !== undefined).map(j => j.ats_score!);
      if (atsScores.length > 0) {
        const distribution = calculateATSDistribution(atsScores);
        setAtsDistribution(distribution);
      }

      // Calculate match tier distribution
      const tierDist: Record<string, number> = {};
      jobsData.jobs.forEach(job => {
        if (job.match_tier) {
          tierDist[job.match_tier] = (tierDist[job.match_tier] || 0) + 1;
        }
      });
      setMatchTierDistribution(tierDist);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateATSDistribution = (scores: number[]): Array<{ range: string; count: number }> => {
    const bins = 10;
    const min = Math.min(...scores);
    const max = Math.max(...scores);
    const binSize = Math.max(1, (max - min) / bins);

    const distribution: Array<{ range: string; count: number }> = [];
    for (let i = 0; i < bins; i++) {
      const binMin = Math.floor(min + i * binSize);
      const binMax = Math.floor(min + (i + 1) * binSize);
      const count = scores.filter(s => s >= binMin && s < binMax).length;
      distribution.push({ range: `${binMin}-${binMax}`, count });
    }
    return distribution;
  };

  const handleDragStart = (job: Job) => {
    setDraggedJob(job);
  };

  const handleDragOver = (e: React.DragEvent, targetStatus: JobStatus) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = async (e: React.DragEvent, targetStatus: JobStatus) => {
    e.preventDefault();
    if (!draggedJob) return;

    if (draggedJob.status !== targetStatus) {
      try {
        // Update job status via API
        // await updateJob(draggedJob.id, { status: targetStatus });

        // Optimistic update
        setJobs(prev => prev.map(job =>
          job.id === draggedJob.id ? { ...job, status: targetStatus } : job
        ));

        // Reload stats
        const newStats = await getPipelineStats();
        setStats(newStats);
      } catch (error) {
        console.error('Failed to update job status:', error);
      }
    }
    setDraggedJob(null);
  };

  const handleJobClick = (job: Job) => {
    // Navigate to job detail - would use a modal or navigate to /athena/jobs/:id
    console.log('Job clicked:', job);
  };

  const handleScrape = async () => {
    setScraping(true);
    try {
      await triggerScrape({ query: 'software engineer', max_results: 50 });
      // Reload data after scrape
      await loadDashboardData();
    } catch (error) {
      console.error('Scrape failed:', error);
    } finally {
      setScraping(false);
    }
  };

  // Inject metrics into right sidebar
  useEffect(() => {
    if (metricsContainerRef.current && stats) {
      metricsContainerRef.current.innerHTML = '';
      // In a real app, this would render React components into the container
      // For now, we'll use the main content area for metrics
    }
  }, [stats]);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-ls-red/30 border-t-ls-red rounded-full animate-spin" aria-hidden="true" />
          <p className="font-body text-ls-grey-dark">Loading Athena dashboard...</p>
        </div>
      </div>
    );
  }

  // Group jobs by status for pipeline
  const jobsByStatus = groupBy(jobs, 'status');

  return (
    <div className="h-full flex flex-col">
      {/* Dashboard Header */}
      <div className="mb-6 sm:mb-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <h1 className="font-display font-black text-2xl sm:text-3xl text-ls-navy">Pipeline Dashboard</h1>
            <p className="font-body text-sm text-ls-grey-dark mt-1">
              Track your job applications from discovery to offer
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleScrape}
              disabled={scraping}
              className="flex items-center gap-2 px-4 py-2 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark hover:border-ls-red hover:text-ls-red transition-all disabled:opacity-50"
            >
              <RefreshCw className={cn('w-4 h-4', scraping && 'animate-spin')} aria-hidden="true" />
              <span className="font-body font-medium text-sm">Scrape Jobs</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors">
              <Download className="w-4 h-4" aria-hidden="true" />
              <span>Export</span>
            </button>
          </div>
        </div>

        {/* Key Metrics Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6" role="region" aria-label="Key metrics">
          <MetricCardLarge
            title="Total Jobs"
            value={stats?.total_jobs || 0}
            subtitle="in pipeline"
            description="All discovered positions"
            trend={stats && stats.total_jobs > 0 ? 'up' : 'stable'}
            trendValue={stats ? `+${stats.new} new` : undefined}
            icon={<Target className="w-6 h-6" />}
            accentColor="navy"
          />
          <MetricCardLarge
            title="Avg ATS Score"
            value={stats ? Math.round(stats.avg_ats_score) : 0}
            subtitle="%"
            description="Keyword + semantic match"
            trend={stats && stats.avg_ats_score > 70 ? 'up' : 'down'}
            trendValue={stats ? `${Math.round(stats.avg_ats_score)}%` : undefined}
            icon={<Award className="w-6 h-6" />}
            accentColor="orange"
          />
          <MetricCardLarge
            title="Applications"
            value={stats ? stats.applied + stats.interview + stats.offer : 0}
            subtitle="active"
            description="Submitted + interviewing"
            trend="up"
            icon={<FileText className="w-6 h-6" />}
            accentColor="cyan"
          />
          <MetricCardLarge
            title="Offers"
            value={stats?.offer || 0}
            subtitle="received"
            description="Pending decisions"
            trend={stats && stats.offer > 0 ? 'up' : 'stable'}
            icon={<Award className="w-6 h-6" />}
            accentColor="emerald"
          />
        </div>
      </div>

      {/* Main Content: Pipeline Board + Right Sidebar Content */}
      <div className="flex-1 flex flex-col lg:flex-row gap-6 min-h-0">
        {/* Pipeline Kanban Board */}
        <div className="flex-1 min-w-0 lg:max-w-[calc(100%-320px)]">
          <div className="bg-ls-white rounded-xl border border-ls-grey-dark/30 overflow-hidden">
            {/* Pipeline Header */}
            <div className="px-4 py-3 border-b border-ls-grey-dark/30 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <h2 className="font-display font-bold text-lg text-ls-navy">Job Pipeline</h2>
              <div className="flex items-center gap-2 text-xs text-ls-grey-dark">
                {stats && (
                  <>
                    <span className="px-2 py-0.5 rounded bg-ls-cyan/20 text-ls-cyan font-bold">New: {stats.new}</span>
                    <span className="px-2 py-0.5 rounded bg-orange/20 text-orange-700 font-bold">Scored: {stats.scored}</span>
                    <span className="px-2 py-0.5 rounded bg-ls-red/20 text-ls-red font-bold">Applied: {stats.applied}</span>
                    <span className="px-2 py-0.5 rounded bg-emerald/20 text-emerald-700 font-bold">Offers: {stats.offer}</span>
                  </>
                )}
              </div>
            </div>

            {/* Pipeline Columns */}
            <div className="overflow-x-auto pb-4" role="region" aria-label="Job pipeline kanban board">
              <div className="flex gap-4 min-w-max p-4" style={{ minWidth: PIPELINE_STAGES.length * 340 }}>
                {PIPELINE_STAGES.map((stage) => (
                  <PipelineColumn
                    key={stage.status}
                    status={stage.status}
                    title={stage.title}
                    jobs={jobsByStatus[stage.status] || []}
                    onJobClick={handleJobClick}
                    onDragStart={handleDragStart}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Sidebar Content Area (mirrored in main content for desktop) */}
        <div className="lg:w-80 flex-shrink-0 hidden lg:block">
          <div className="space-y-6">
            {/* ATS Score Distribution */}
            <div className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-bold text-base text-ls-navy">ATS Score Distribution</h3>
              </div>
              <MountainAreaChart
                data={atsDistribution}
                height={200}
                colors={['#FF6B35', '#E63946', '#00BFFF']}
              />
              <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded" style={{ background: 'linear-gradient(90deg, #FF6B35, #E63946)' }} />
                  <span className="font-body text-ls-grey-dark">High Match</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded bg-ls-cyan/60" />
                  <span className="font-body text-ls-grey-dark">Low Match</span>
                </div>
              </div>
            </div>

            {/* Match Tier Breakdown */}
            <div className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-5">
              <h3 className="font-display font-bold text-base text-ls-navy mb-4">Match Tier Breakdown</h3>
              <div className="space-y-3">
                {([
                  { tier: 'excellent', label: 'Excellent (90+)', color: '#10B981' },
                  { tier: 'good', label: 'Good (80-89)', color: '#3B82F6' },
                  { tier: 'fair', label: 'Fair (70-79)', color: '#F59E0B' },
                  { tier: 'poor', label: 'Poor (<70)', color: '#EF4444' },
                ]).map(({ tier, label, color }) => {
                  const count = matchTierDistribution[tier] || 0;
                  const total = Object.values(matchTierDistribution).reduce((a, b) => a + b, 0) || 1;
                  const percentage = Math.round((count / total) * 100);
                  return (
                    <div key={tier} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-body text-ls-grey-dark flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
                          {label}
                        </span>
                        <span className="font-display font-bold text-ls-navy">{count} ({percentage}%)</span>
                      </div>
                      <div className="h-1.5 bg-ls-grey-light rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all duration-500"
                          style={{ width: `${percentage}%`, backgroundColor: color }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-5">
              <h3 className="font-display font-bold text-base text-ls-navy mb-4">Quick Stats</h3>
              <div className="space-y-3">
                <StatCounter
                  value={stats?.by_source ? Object.values(stats.by_source).reduce((a, b) => a + b, 0) : 0}
                  label="Sources Tracked"
                  format="plain"
                  accentColor="cyan"
                />
                <StatCounter
                  value={stats?.by_type ? Object.keys(stats.by_type).length : 0}
                  label="Job Types"
                  format="plain"
                  accentColor="purple"
                />
                <StatCounter
                  value={stats?.total_jobs || 0}
                  label="Total Tracked"
                  format="comma"
                  accentColor="navy"
                />
              </div>
            </div>

            {/* Recent Scrapes */}
            <div className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-bold text-base text-ls-navy">Recent Scrapes</h3>
                <button onClick={handleScrape} disabled={scraping} className="text-xs text-ls-cyan hover:text-ls-red font-bold">
                  {scraping ? 'Scraping...' : 'Run Scrape'}
                </button>
              </div>
              <div className="space-y-2 text-sm">
                <p className="font-body text-ls-grey-dark">Last scrape: {formatRelativeTime(new Date().toISOString())}</p>
                <p className="font-body text-ls-grey-dark">Jobs found: {stats?.new || 0} new</p>
                <p className="font-body text-ls-grey-dark">Avg match: {stats ? Math.round(stats.avg_match_score) : 0}%</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AthenaDashboard;
