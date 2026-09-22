import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ATSGauge } from '@/components/athena/ATSGauge';
import { AreaChart } from '@/components/athena/AreaChart';
import { SkillTags, SkillComparison } from '@/components/athena/SkillTags';
import { cn, formatSalary, formatDate, getJobTypeLabel, getJobSourceLabel, getMatchTierColor, getMatchTierLabel } from '@/lib/athena/utils';
import { getJob, getATSScore } from '@/lib/athena/api';
import type { Job, MatchTier, SkillTag } from '@/lib/athena/types';
import { ChevronDown, ChevronLeft, Download, Upload, FileText, Flag, Share2, ExternalLink, Check, X, Sparkles, Brain, Loader2 } from 'lucide-react';

export const JobDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [atsScore, setAtsScore] = useState<{
    keyword_match: number;
    semantic_similarity: number;
    experience_relevance: number;
    education_match: number;
    overall: number;
    tier: string;
    should_auto_apply: boolean;
    should_flag_for_review: boolean;
    details: Record<string, unknown>;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    loadJobDetail();
  }, [id]);

  const loadJobDetail = async () => {
    if (!id) return;
    setLoading(true);
    try {
      const [jobData, atsData] = await Promise.all([
        getJob(id),
        getATSScore(id, 'current-user-profile-id'),
      ]);
      setJob(jobData);
      setAtsScore(atsData);
    } catch (error) {
      console.error('Failed to load job detail:', error);
      navigate('/athena/jobs');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-12 h-12 animate-spin text-ls-red" aria-hidden="true" />
          <p className="font-body text-ls-grey-dark">Loading job details...</p>
        </div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <p className="font-body text-ls-grey-dark">Job not found</p>
          <button onClick={() => navigate('/athena/jobs')} className="mt-4 px-4 py-2 bg-ls-red text-ls-white rounded-lg">
            Back to Jobs
          </button>
        </div>
      </div>
    );
  }

  // Mock skill data for demonstration
  const jobSkills: SkillTag[] = [
    { name: 'React', level: 'advanced', category: 'technical', matched: true, importance: 'required' },
    { name: 'TypeScript', level: 'advanced', category: 'technical', matched: true, importance: 'required' },
    { name: 'Node.js', level: 'intermediate', category: 'technical', matched: true, importance: 'preferred' },
    { name: 'PostgreSQL', level: 'intermediate', category: 'technical', matched: false, importance: 'preferred' },
    { name: 'AWS', level: 'beginner', category: 'technical', matched: false, importance: 'nice-to-have' },
    { name: 'GraphQL', level: 'beginner', category: 'technical', matched: false, importance: 'nice-to-have' },
    { name: 'Communication', level: 'advanced', category: 'soft', matched: true, importance: 'required' },
    { name: 'Problem Solving', level: 'expert', category: 'soft', matched: true, importance: 'required' },
  ];

  const userSkills = ['React', 'TypeScript', 'Node.js', 'Communication', 'Problem Solving'];
  const matchingSkills = jobSkills.filter(s => userSkills.includes(s.name));
  const missingSkills = jobSkills.filter(s => !userSkills.includes(s.name));

  const handleAction = async (action: string) => {
    setActionLoading(action);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setActionLoading(null);
    // Would trigger actual API calls here
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header with back button */}
      <div className="mb-6 sm:mb-8">
        <div className="flex items-center gap-4 mb-4">
          <button
            onClick={() => navigate('/athena/jobs')}
            className="p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors"
            aria-label="Back to job list"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <div className="flex-1">
            <h1 className="font-display font-black text-2xl sm:text-3xl text-ls-navy">{job.title}</h1>
            <p className="font-body text-sm text-ls-grey-dark mt-1">{job.company} • {job.location}</p>
          </div>
          <div className="flex items-center gap-3">
            <ATSGauge score={job.ats_score || 0} size={70} strokeWidth={6} showLabel tier={job.match_tier} />
            <a
              href={job.application_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-5 py-2.5 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors flex items-center gap-2"
            >
              <ExternalLink className="w-4 h-4" />
              Apply
            </a>
          </div>
        </div>

        {/* Meta badges */}
        <div className="flex flex-wrap items-center gap-3">
          <span className={cn('px-3 py-1.5 rounded-full text-[10px] font-bold tracking-wider border', getMatchTierColor(job.match_tier))}>
            {getMatchTierLabel(job.match_tier)}
          </span>
          <span className="px-3 py-1.5 rounded-full bg-ls-grey-light text-ls-grey-dark text-[10px] font-bold tracking-wider border border-ls-grey-dark/30">
            {getJobSourceLabel(job.source)}
          </span>
          <span className="px-3 py-1.5 rounded-full bg-ls-grey-light text-ls-grey-dark text-[10px] font-bold tracking-wider border border-ls-grey-dark/30">
            {getJobTypeLabel(job.job_type)}
          </span>
          <span className="px-3 py-1.5 rounded-full bg-ls-grey-light text-ls-grey-dark text-[10px] font-bold tracking-wider border border-ls-grey-dark/30">
            {formatSalary(job.salary_range)}
          </span>
          <span className="px-3 py-1.5 rounded-full bg-ls-grey-light text-ls-grey-dark text-[10px] font-bold tracking-wider border border-ls-grey-dark/30">
            Posted {formatDate(job.posted_date)}
          </span>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col lg:flex-row gap-6">
        {/* Left Column - Job Details */}
        <div className="flex-1 lg:w-2/3 space-y-6">
          {/* Description */}
          <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6">
            <h2 className="font-display font-bold text-lg text-ls-navy mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-ls-red" />
              Description
            </h2>
            <div className="prose prose-sm text-ls-grey-dark max-w-none whitespace-pre-wrap">
              {job.description}
            </div>
          </section>

          {/* Requirements & Responsibilities */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {job.requirements.length > 0 && (
              <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6">
                <h2 className="font-display font-bold text-lg text-ls-navy mb-4 flex items-center gap-2">
                  <Check className="w-5 h-5 text-emerald-600" />
                  Requirements
                </h2>
                <ul className="space-y-3">
                  {job.requirements.map((req, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-ls-grey-dark p-3 rounded-lg bg-ls-grey-light/50">
                      <Check className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                      <span>{req}</span>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {job.responsibilities.length > 0 && (
              <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6">
                <h2 className="font-display font-bold text-lg text-ls-navy mb-4 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-ls-cyan" />
                  Responsibilities
                </h2>
                <ul className="space-y-3">
                  {job.responsibilities.map((resp, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-ls-grey-dark p-3 rounded-lg bg-ls-grey-light/50">
                      <Sparkles className="w-4 h-4 text-ls-cyan flex-shrink-0 mt-0.5" />
                      <span>{resp}</span>
                    </li>
                  ))}
                </ul>
              </section>
            )}
          </div>

          {/* Benefits */}
          {job.benefits.length > 0 && (
            <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6">
              <h2 className="font-display font-bold text-lg text-ls-navy mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-amber-500" />
                Benefits
              </h2>
              <div className="flex flex-wrap gap-2">
                {job.benefits.map((benefit, i) => (
                  <span key={i} className="px-3 py-1.5 rounded-lg bg-ls-grey-light text-ls-grey-dark text-sm font-medium border border-ls-grey-dark/30">
                    {benefit}
                  </span>
                ))}
              </div>
            </section>
          )}

          {/* Company Info */}
          <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6">
            <h2 className="font-display font-bold text-lg text-ls-navy mb-4 flex items-center gap-2">
              <Brain className="w-5 h-5 text-ls-cyan" />
              Company Information
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
              {job.company_website && (
                <a href={job.company_website} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 text-ls-cyan hover:text-ls-red">
                  <ExternalLink className="w-4 h-4" />
                  <span>Company Website</span>
                </a>
              )}
              {job.company_size && (
                <div className="flex items-center gap-2 text-ls-grey-dark">
                  <span className="font-bold text-ls-navy">Size:</span>
                  <span>{job.company_size}</span>
                </div>
              )}
              {job.company_industry && (
                <div className="flex items-center gap-2 text-ls-grey-dark">
                  <span className="font-bold text-ls-navy">Industry:</span>
                  <span>{job.company_industry}</span>
                </div>
              )}
              {job.contact_person && (
                <div className="flex items-center gap-2 text-ls-grey-dark">
                  <span className="font-bold text-ls-navy">Contact:</span>
                  <span>{job.contact_person}</span>
                </div>
              )}
              {job.apply_email && (
                <a href={`mailto:${job.apply_email}`} className="flex items-center gap-2 text-ls-cyan hover:text-ls-red">
                  <ExternalLink className="w-4 h-4" />
                  <span>Email: {job.apply_email}</span>
                </a>
              )}
            </div>
          </section>
        </div>

        {/* Right Column - ATS Score & Skills */}
        <div className="lg:w-1/3 space-y-6">
          {/* ATS Score Card */}
          <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6 sticky top-24">
            <h2 className="font-display font-bold text-lg text-ls-navy mb-4 flex items-center gap-2">
              <Award className="w-5 h-5 text-ls-red" />
              ATS Analysis
            </h2>

            {/* Circular Gauge */}
            <div className="flex justify-center mb-6">
              <ATSGauge
                score={job.ats_score || 0}
                size={140}
                strokeWidth={14}
                tier={job.match_tier}
                showLabel={true}
              />
            </div>

            {/* Tier & Recommendation */}
            <div className="text-center mb-6 p-4 rounded-lg bg-ls-grey-light/50">
              <p className="font-body text-sm text-ls-grey-dark mb-1">Match Tier</p>
              <p className="font-display font-bold text-2xl" style={{ color: getMatchTierColor(job.match_tier).replace('border-', '').replace('text-', '') }}>
                {getMatchTierLabel(job.match_tier)}
              </p>
              {atsScore && (
                <p className="font-body text-xs text-ls-grey-dark mt-2">
                  {atsScore.should_auto_apply ? '✓ Strong candidate — consider auto-apply' :
                   atsScore.should_flag_for_review ? '⚠ Review required before applying' :
                   'Consider tailoring resume'}
                </p>
              )}
            </div>

            {/* Detailed Breakdown */}
            {atsScore && (
              <div className="space-y-3 mb-6">
                {[
                  { label: 'Keyword Match', value: atsScore.keyword_match, color: '#FF6B35' },
                  { label: 'Semantic Similarity', value: atsScore.semantic_similarity, color: '#E63946' },
                  { label: 'Experience Relevance', value: atsScore.experience_relevance, color: '#00BFFF' },
                  { label: 'Education Match', value: atsScore.education_match, color: '#10B981' },
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
            )}

            {/* Additional Details */}
            {atsScore?.details && Object.keys(atsScore.details).length > 0 && (
              <details className="group">
                <summary className="font-body text-sm text-ls-cyan hover:text-ls-red cursor-pointer flex items-center justify-between">
                  <span>View detailed breakdown</span>
                  <ChevronDown className="w-4 h-4 transition-transform group-open:rotate-180" />
                </summary>
                <div className="mt-3 p-3 bg-ls-grey-light/50 rounded-lg text-xs text-ls-grey-dark space-y-1">
                  {Object.entries(atsScore.details).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="font-medium">{key.replace(/_/g, ' ')}</span>
                      <span>{String(value)}</span>
                    </div>
                  ))}
                </div>
              </details>
            )}
          </section>

          {/* Skills Analysis */}
          <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6 sticky top-24" style={{ top: '320px' }}>
            <SkillComparison
              matchingSkills={matchingSkills}
              missingSkills={missingSkills}
            />
          </section>

          {/* Quick Actions */}
          <section className="bg-ls-white rounded-xl border border-ls-grey-dark/30 p-6 sticky top-24" style={{ top: '580px' }}>
            <h2 className="font-display font-bold text-lg text-ls-navy mb-4">Actions</h2>
            <div className="space-y-2">
              <button
                onClick={() => handleAction('apply')}
                disabled={actionLoading === 'apply'}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors disabled:opacity-50"
              >
                {actionLoading === 'apply' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
                {actionLoading === 'apply' ? 'Applying...' : 'Apply Now'}
              </button>
              <button
                onClick={() => handleAction('tailor')}
                disabled={actionLoading === 'tailor'}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors disabled:opacity-50"
              >
                {actionLoading === 'tailor' ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileText className="w-4 h-4" />}
                {actionLoading === 'tailor' ? 'Tailoring...' : 'Tailor Resume'}
              </button>
              <button
                onClick={() => handleAction('cover')}
                disabled={actionLoading === 'cover'}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors disabled:opacity-50"
              >
                {actionLoading === 'cover' ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileText className="w-4 h-4" />}
                {actionLoading === 'cover' ? 'Generating...' : 'Generate Cover Letter'}
              </button>
              <button
                onClick={() => handleAction('flag')}
                disabled={actionLoading === 'flag'}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors disabled:opacity-50"
              >
                {actionLoading === 'flag' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Flag className="w-4 h-4" />}
                {actionLoading === 'flag' ? 'Flagging...' : 'Flag for Review'}
              </button>
              <button
                onClick={() => handleAction('share')}
                disabled={actionLoading === 'share'}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-bold text-sm hover:border-ls-red hover:text-ls-red transition-colors disabled:opacity-50"
              >
                {actionLoading === 'share' ? <Loader2 className="w-4 h-4 animate-spin" /> : <Share2 className="w-4 h-4" />}
                {actionLoading === 'share' ? 'Sharing...' : 'Share Job'}
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

// Need to import Award
import { Award } from 'lucide-react';

export default JobDetail;
