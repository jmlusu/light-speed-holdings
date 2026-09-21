import React, { useEffect, useState, useMemo, useCallback } from 'react';
import { Search, Filter, X, ChevronDown, Download, Upload, Plus, Loader2, FileText } from 'lucide-react';
import { JobCard } from '@/components/athena/JobCard';
import { ATSGauge, MiniATSGauge } from '@/components/athena/ATSGauge';
import { cn, formatSalary, formatDate, getJobTypeLabel, getJobSourceLabel, getMatchTierColor, getMatchTierLabel, debounce } from '@/lib/athena/utils';
import { listJobs, triggerScrape } from '@/lib/athena/api';
import type { Job, JobFilter, JobSource, JobType, JobStatus, MatchTier } from '@/lib/athena/types';

const JOB_SOURCES: JobSource[] = ['linkedin', 'indeed', 'glassdoor', 'company_career', 'malawi_jobs', 'malawi_work', 'jobs_malawi', 'remote_ok', 'we_work_remotely', 'other'];
const JOB_TYPES: JobType[] = ['full_time', 'part_time', 'contract', 'consultancy', 'freelance', 'internship', 'temporary'];
const JOB_STATUSES: JobStatus[] = ['new', 'fetched', 'matched', 'scored', 'applied', 'interview', 'offer', 'rejected', 'archived'];
const MATCH_TIERS: MatchTier[] = ['excellent', 'good', 'fair', 'poor'];

export const JobList: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [page, setPage] = useState(1);
  const pageSize = 20;

  // Filters state
  const [filters, setFilters] = useState<JobFilter>({
    search: '',
    status: undefined,
    source: undefined,
    job_type: undefined,
    location: '',
    min_ats_score: undefined,
    max_ats_score: undefined,
    min_match_score: undefined,
    max_match_score: undefined,
    limit: pageSize,
    offset: 0,
  });

  const [showFilters, setShowFilters] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  // Debounced search
  const debouncedSearch = useMemo(
    () => debounce((value: string) => {
      setFilters(prev => ({ ...prev, search: value, offset: 0 }));
      setPage(1);
    }, 300),
    []
  );

  // Load jobs
  const loadJobs = useCallback(async () => {
    setLoading(true);
    try {
      const response = await listJobs({ ...filters, offset: (page - 1) * pageSize });
      setJobs(response.jobs);
      setTotal(response.total);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  }, [filters, page]);

  useEffect(() => {
    loadJobs();
  }, [loadJobs]);

  // Handle filter changes
  const handleFilterChange = (key: keyof JobFilter, value: JobFilter[keyof JobFilter]) => {
    setFilters(prev => ({ ...prev, [key]: value, offset: 0 }));
    setPage(1);
  };

  const clearFilters = () => {
    setFilters({
      search: '',
      status: undefined,
      source: undefined,
      job_type: undefined,
      location: '',
      min_ats_score: undefined,
      max_ats_score: undefined,
      min_match_score: undefined,
      max_match_score: undefined,
      limit: pageSize,
      offset: 0,
    });
    setPage(1);
  };

  const hasActiveFilters = useMemo(() =>
    Object.entries(filters).some(([key, value]) =>
      key !== 'limit' && key !== 'offset' && value !== undefined && value !== '' && value !== null
    ), [filters]);

  const handleScrape = async () => {
    setScraping(true);
    try {
      await triggerScrape({ query: filters.search || 'software engineer', max_results: 50 });
      loadJobs();
    } catch (error) {
      console.error('Scrape failed:', error);
    } finally {
      setScraping(false);
    }
  };

  const handleJobClick = (job: Job) => {
    setSelectedJob(job);
  };

  const closeJobDetail = () => {
    setSelectedJob(null);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Page Header */}
      <div className="mb-6 sm:mb-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <h1 className="font-display font-black text-2xl sm:text-3xl text-ls-navy">Job Search</h1>
            <p className="font-body text-sm text-ls-grey-dark mt-1">
              {total} job{total !== 1 ? 's' : ''} found • Discover and match opportunities
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg border transition-all',
                showFilters
                  ? 'bg-ls-red/10 border-ls-red text-ls-red'
                  : 'border-ls-grey-dark/30 text-ls-grey-dark hover:border-ls-red hover:text-ls-red'
              )}
            >
              <Filter className="w-4 h-4" aria-hidden="true" />
              <span className="font-body font-medium text-sm">Filters</span>
              {hasActiveFilters && (
                <span className="px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-ls-red text-ls-white">
                  {Object.values(filters).filter(v => v !== undefined && v !== '' && v !== null).length}
                </span>
              )}
            </button>
            <button
              onClick={handleScrape}
              disabled={scraping}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors disabled:opacity-50"
            >
              <Loader2 className={cn('w-4 h-4', scraping && 'animate-spin')} aria-hidden="true" />
              <span className="font-body font-medium text-sm">Scrape</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark hover:border-ls-red hover:text-ls-red transition-all">
              <Download className="w-4 h-4" aria-hidden="true" />
              <span className="font-body font-medium text-sm">Export</span>
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative mb-4">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-ls-grey-light-text" aria-hidden="true" />
          <input
            type="search"
            value={filters.search}
            onChange={(e) => debouncedSearch(e.target.value)}
            placeholder="Search by title, company, description..."
            className="w-full pl-12 pr-4 py-3 bg-ls-white border border-ls-grey-dark/30 rounded-lg text-ls-navy placeholder-ls-grey-light-text focus:outline-none focus:ring-2 focus:ring-ls-red focus:border-transparent"
            aria-label="Search jobs"
          />
          {filters.search && (
            <button
              onClick={() => handleFilterChange('search', '')}
              className="absolute right-4 top-1/2 -translate-y-1/2 p-1 text-ls-grey-light-text hover:text-ls-red"
              aria-label="Clear search"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Active Filters Chips */}
        {hasActiveFilters && (
          <div className="flex flex-wrap gap-2 mb-4" role="group" aria-label="Active filters">
            {(Object.entries(filters) as [keyof JobFilter, JobFilter[keyof JobFilter]][])
              .filter(([key, value]) => key !== 'limit' && key !== 'offset' && value !== undefined && value !== '' && value !== null)
              .map(([key, value]) => (
                <span key={key} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-ls-red/10 text-ls-red text-sm font-medium">
                  {key.replace(/_/g, ' ')}: {String(value)}
                  <button
                    onClick={() => handleFilterChange(key, undefined)}
                    className="hover:text-ls-red/70"
                    aria-label={`Remove ${key} filter`}
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </span>
              ))}
            <button
              onClick={clearFilters}
              className="px-3 py-1 rounded-full text-sm font-medium text-ls-grey-dark hover:text-ls-red transition-colors"
            >
              Clear all
            </button>
          </div>
        )}

        {/* Advanced Filters Panel */}
        {showFilters && (
          <div className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-5 mb-6 animate-in slide-in-from-top-2" role="region" aria-label="Advanced filters">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="font-body text-xs font-bold tracking-wider uppercase text-ls-grey-dark block mb-1.5">Status</label>
                <select
                  value={filters.status || ''}
                  onChange={(e) => handleFilterChange('status', e.target.value || undefined)}
                  className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                >
                  <option value="">All statuses</option>
                  {JOB_STATUSES.map(s => <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>)}
                </select>
              </div>

              <div>
                <label className="font-body text-xs font-bold tracking-wider uppercase text-ls-grey-dark block mb-1.5">Source</label>
                <select
                  value={filters.source || ''}
                  onChange={(e) => handleFilterChange('source', e.target.value as JobSource || undefined)}
                  className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                >
                  <option value="">All sources</option>
                  {JOB_SOURCES.map(s => <option key={s} value={s}>{getJobSourceLabel(s)}</option>)}
                </select>
              </div>

              <div>
                <label className="font-body text-xs font-bold tracking-wider uppercase text-ls-grey-dark block mb-1.5">Job Type</label>
                <select
                  value={filters.job_type || ''}
                  onChange={(e) => handleFilterChange('job_type', e.target.value as JobType || undefined)}
                  className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                >
                  <option value="">All types</option>
                  {JOB_TYPES.map(t => <option key={t} value={t}>{getJobTypeLabel(t)}</option>)}
                </select>
              </div>

              <div>
                <label className="font-body text-xs font-bold tracking-wider uppercase text-ls-grey-dark block mb-1.5">Location</label>
                <input
                  type="text"
                  value={filters.location}
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                  placeholder="e.g., Lilongwe, Remote"
                  className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy placeholder-ls-grey-light-text focus:outline-none focus:ring-2 focus:ring-ls-red"
                />
              </div>

              <div className="lg:col-span-2">
                <label className="font-body text-xs font-bold tracking-wider uppercase text-ls-grey-dark block mb-1.5">ATS Score Range</label>
                <div className="flex items-center gap-3">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={filters.min_ats_score || ''}
                    onChange={(e) => handleFilterChange('min_ats_score', e.target.value ? parseInt(e.target.value) : undefined)}
                    placeholder="Min"
                    className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                    aria-label="Minimum ATS score"
                  />
                  <span className="text-ls-grey-light-text">–</span>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={filters.max_ats_score || ''}
                    onChange={(e) => handleFilterChange('max_ats_score', e.target.value ? parseInt(e.target.value) : undefined)}
                    placeholder="Max"
                    className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                    aria-label="Maximum ATS score"
                  />
                </div>
              </div>

              <div className="lg:col-span-2">
                <label className="font-body text-xs font-bold tracking-wider uppercase text-ls-grey-dark block mb-1.5">Match Score Range</label>
                <div className="flex items-center gap-3">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={filters.min_match_score || ''}
                    onChange={(e) => handleFilterChange('min_match_score', e.target.value ? parseInt(e.target.value) : undefined)}
                    placeholder="Min"
                    className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                    aria-label="Minimum match score"
                  />
                  <span className="text-ls-grey-light-text">–</span>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={filters.max_match_score || ''}
                    onChange={(e) => handleFilterChange('max_match_score', e.target.value ? parseInt(e.target.value) : undefined)}
                    placeholder="Max"
                    className="w-full px-3 py-2 border border-ls-grey-dark/30 rounded-lg bg-ls-white text-sm text-ls-navy focus:outline-none focus:ring-2 focus:ring-ls-red"
                    aria-label="Maximum match score"
                  />
                </div>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-ls-grey-dark/30 flex justify-end">
              <button onClick={clearFilters} className="px-4 py-2 text-sm font-medium text-ls-grey-dark hover:text-ls-red transition-colors">
                Clear all filters
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Job Results */}
      <div className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-ls-red" aria-hidden="true" />
            <span className="ml-3 font-body text-ls-grey-dark">Loading jobs...</span>
          </div>
        ) : jobs.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
            <div className="w-16 h-16 rounded-full bg-ls-grey-light flex items-center justify-center mb-4">
              <Search className="w-8 h-8 text-ls-grey-light-text" aria-hidden="true" />
            </div>
            <h3 className="font-display font-bold text-lg text-ls-navy mb-2">No jobs found</h3>
            <p className="font-body text-sm text-ls-grey-dark max-w-sm">
              Try adjusting your filters or search terms, or scrape for new jobs.
            </p>
            <button
              onClick={handleScrape}
              disabled={scraping}
              className="mt-4 px-6 py-2.5 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors"
            >
              Scrape for jobs
            </button>
          </div>
        ) : (
          <>
            {/* Results Header */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4 pb-3 border-b border-ls-grey-dark/30">
              <p className="font-body text-sm text-ls-grey-dark">
                Showing <span className="font-bold text-ls-navy">{((page - 1) * pageSize) + 1}</span>–
                <span className="font-bold text-ls-navy">{Math.min(page * pageSize, total)}</span>
                of <span className="font-bold text-ls-navy">{total.toLocaleString()}</span> jobs
              </p>
              <div className="flex items-center gap-2">
                <select
                  value={pageSize}
                  onChange={(e) => { /* pageSize change would need state */ }}
                  className="px-3 py-1.5 border border-ls-grey-dark/30 rounded-lg text-sm text-ls-navy bg-ls-white focus:outline-none focus:ring-2 focus:ring-ls-red"
                  aria-label="Items per page"
                >
                  <option value={20}>20 per page</option>
                  <option value={50}>50 per page</option>
                  <option value={100}>100 per page</option>
                </select>
              </div>
            </div>

            {/* Job Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" role="list" aria-label="Job listings">
              {jobs.map((job) => (
                <JobCard
                  key={job.id}
                  job={job}
                  onClick={() => handleJobClick(job)}
                  matchScore={job.match_score}
                  matchTier={job.match_tier}
                />
              ))}
            </div>

            {/* Pagination */}
            {total > pageSize && (
              <nav className="mt-6 flex items-center justify-center gap-2" aria-label="Pagination">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="p-2 rounded-lg border border-ls-grey-dark/30 text-ls-grey-dark hover:border-ls-red hover:text-ls-red disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                  aria-label="Previous page"
                >
                  <ChevronDown className="w-5 h-5 rotate-180" />
                </button>
                <span className="font-body text-sm text-ls-grey-dark px-3">
                  Page {page} of {Math.ceil(total / pageSize)}
                </span>
                <button
                  onClick={() => setPage(p => Math.min(Math.ceil(total / pageSize), p + 1))}
                  disabled={page >= Math.ceil(total / pageSize)}
                  className="p-2 rounded-lg border border-ls-grey-dark/30 text-ls-grey-dark hover:border-ls-red hover:text-ls-red disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                  aria-label="Next page"
                >
                  <ChevronDown className="w-5 h-5" />
                </button>
              </nav>
            )}
          </>
        )}
      </div>

      {/* Job Detail Modal */}
      {selectedJob && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 animate-in fade-in" role="dialog" aria-modal="true" aria-labelledby="job-detail-title">
          <div className="bg-ls-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col animate-in zoom-in-95 slide-in-from-bottom-2">
            {/* Modal Header */}
            <div className="flex items-start justify-between p-5 border-b border-ls-grey-dark/30 sticky top-0 bg-ls-white z-10">
              <div className="flex-1 mr-4 min-w-0">
                <div className="flex items-center gap-2 mb-2 flex-wrap">
                  <span className="font-display font-bold text-lg text-ls-navy truncate">{selectedJob.company}</span>
                  <span className={cn('px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wider border', getMatchTierColor(selectedJob.match_tier))}>
                    {getMatchTierLabel(selectedJob.match_tier)}
                  </span>
                </div>
                <h2 id="job-detail-title" className="font-display font-bold text-xl text-ls-navy">{selectedJob.title}</h2>
                <div className="flex flex-wrap items-center gap-4 mt-2 text-sm text-ls-grey-dark">
                  <span className="flex items-center gap-1.5"><MapPin className="w-4 h-4" /> {selectedJob.location}</span>
                  <span className="flex items-center gap-1.5"><Briefcase className="w-4 h-4" /> {getJobTypeLabel(selectedJob.job_type)}</span>
                  <span className="flex items-center gap-1.5"><DollarSign className="w-4 h-4" /> {formatSalary(selectedJob.salary_range)}</span>
                  <span className="flex items-center gap-1.5"><Clock className="w-4 h-4" /> {formatDate(selectedJob.posted_date)}</span>
                </div>
              </div>
              <div className="flex items-center gap-3 flex-shrink-0">
                <ATSGauge score={selectedJob.ats_score || 0} size={60} strokeWidth={6} showLabel tier={selectedJob.match_tier} />
                <button onClick={closeJobDetail} className="p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors" aria-label="Close job detail">
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="flex-1 overflow-y-auto p-5 space-y-6">
              {/* Description */}
              <section>
                <h3 className="font-display font-bold text-base text-ls-navy mb-3">Description</h3>
                <div className="prose prose-sm text-ls-grey-dark max-w-none">
                  <p className="whitespace-pre-wrap">{selectedJob.description}</p>
                </div>
              </section>

              {/* Requirements & Responsibilities */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {selectedJob.requirements.length > 0 && (
                  <section>
                    <h3 className="font-display font-bold text-base text-ls-navy mb-3 flex items-center gap-2">
                      <ChevronDown className="w-4 h-4 text-ls-red" />
                      Requirements
                    </h3>
                    <ul className="space-y-2">
                      {selectedJob.requirements.map((req, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-ls-grey-dark">
                          <span className="w-1.5 h-1.5 rounded-full bg-ls-red mt-1.5 flex-shrink-0" />
                          {req}
                        </li>
                      ))}
                    </ul>
                  </section>
                )}

                {selectedJob.responsibilities.length > 0 && (
                  <section>
                    <h3 className="font-display font-bold text-base text-ls-navy mb-3 flex items-center gap-2">
                      <ChevronDown className="w-4 h-4 text-ls-cyan" />
                      Responsibilities
                    </h3>
                    <ul className="space-y-2">
                      {selectedJob.responsibilities.map((resp, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-ls-grey-dark">
                          <span className="w-1.5 h-1.5 rounded-full bg-ls-cyan mt-1.5 flex-shrink-0" />
                          {resp}
                        </li>
                      ))}
                    </ul>
                  </section>
                )}
              </div>

              {/* ATS Score Breakdown */}
              {selectedJob.ats_score !== undefined && (
                <section>
                  <h3 className="font-display font-bold text-base text-ls-navy mb-3">ATS Score Breakdown</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <ATSGauge score={selectedJob.ats_score} size={80} tier={selectedJob.match_tier} label="Overall" />
                    <div className="md:col-span-3 space-y-3">
                      {[
                        { label: 'Keyword Match', value: 85, color: '#FF6B35' },
                        { label: 'Semantic Similarity', value: 78, color: '#E63946' },
                        { label: 'Experience Relevance', value: 82, color: '#00BFFF' },
                        { label: 'Education Match', value: 75, color: '#10B981' },
                      ].map((item) => (
                        <div key={item.label} className="flex items-center gap-3">
                          <span className="w-36 font-body text-sm text-ls-grey-dark">{item.label}</span>
                          <div className="flex-1 h-2 bg-ls-grey-light rounded-full overflow-hidden">
                            <div className="h-full rounded-full transition-all duration-500" style={{ width: `${item.value}%`, backgroundColor: item.color }} />
                          </div>
                          <span className="w-10 text-right font-display font-bold text-sm text-ls-navy">{item.value}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </section>
              )}

              {/* Actions */}
              <div className="flex flex-wrap gap-3 pt-4 border-t border-ls-grey-dark/30">
                <a
                  href={selectedJob.application_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors"
                >
                  <Upload className="w-4 h-4" />
                  Apply Now
                </a>
                <button className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-6 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors">
                  <Download className="w-4 h-4" />
                  Tailor Resume
                </button>
                <button className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-6 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors">
                  <FileText className="w-4 h-4" />
                  Cover Letter
                </button>
                <button className="flex-1 sm:flex-none flex items-center justify-center gap-2 px-6 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors">
                  <ChevronDown className="w-4 h-4" />
                  Flag
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Need to import MapPin, Briefcase, DollarSign, Clock, ChevronDown
import { MapPin, Briefcase, DollarSign, Clock } from 'lucide-react';

export default JobList;
