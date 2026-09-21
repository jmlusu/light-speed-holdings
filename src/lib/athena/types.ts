export type JobSource =
  | 'linkedin'
  | 'indeed'
  | 'glassdoor'
  | 'company_career'
  | 'malawi_jobs'
  | 'malawi_work'
  | 'jobs_malawi'
  | 'upwork'
  | 'toptal'
  | 'freelancer'
  | 'guru'
  | 'people_per_hour'
  | 'remote_ok'
  | 'we_work_remotely'
  | 'remote_co'
  | 'other';

export type JobType =
  | 'full_time'
  | 'part_time'
  | 'contract'
  | 'consultancy'
  | 'freelance'
  | 'internship'
  | 'temporary';

export type JobStatus =
  | 'new'
  | 'fetched'
  | 'matched'
  | 'scored'
  | 'applied'
  | 'interview'
  | 'offer'
  | 'rejected'
  | 'archived';

export type ApplicationStatus =
  | 'pending'
  | 'submitted'
  | 'confirmed'
  | 'failed'
  | 'withdrawn';

export type MatchTier =
  | 'excellent'
  | 'good'
  | 'fair'
  | 'poor';

export interface SalaryRange {
  min?: number;
  max?: number;
  currency: string;
  period: 'yearly' | 'monthly' | 'hourly';
}

export interface SkillTag {
  name: string;
  level?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  category?: 'technical' | 'soft' | 'language' | 'other';
  matched?: boolean;
  importance?: 'required' | 'preferred' | 'nice-to-have';
}

export interface Skill {
  name: string;
  level?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  years_experience?: number;
  category?: 'technical' | 'soft' | 'language' | 'other';
}

export interface Experience {
  id: string;
  title: string;
  company: string;
  location?: string;
  start_date: string;
  end_date?: string;
  current: boolean;
  description: string;
  achievements: string[];
  skills_used: string[];
}

export interface Education {
  id: string;
  institution: string;
  degree: string;
  field_of_study: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  gpa?: number;
  honors: string[];
}

export interface Document {
  id: string;
  name: string;
  type: 'resume' | 'cover_letter' | 'certification' | 'portfolio' | 'other';
  file_path: string;
  mime_type: string;
  size_bytes: number;
  uploaded_at: string;
  parsed_content?: Record<string, unknown>;
}

export interface JobPreferences {
  keywords: string[];
  excluded_keywords: string[];
  locations: string[];
  job_types: JobType[];
  min_salary?: number;
  preferred_sources: JobSource[];
  remote_only: boolean;
  visa_sponsorship_required: boolean;
}

export interface Job {
  id: string;
  source: JobSource;
  source_job_id?: string;
  title: string;
  company: string;
  location: string;
  job_type: JobType;
  description: string;
  requirements: string[];
  responsibilities: string[];
  keywords: string[];
  salary_range?: SalaryRange;
  posted_date?: string;
  expiry_date?: string;
  application_url: string;
  apply_email?: string;
  contact_person?: string;
  company_website?: string;
  company_size?: string;
  company_industry?: string;
  benefits: string[];
  ats_score?: number;
  match_score?: number;
  match_tier?: MatchTier;
  status: JobStatus;
  scraped_at: string;
  updated_at: string;
  metadata: Record<string, unknown>;
}

export interface Application {
  id: string;
  job_id: string;
  user_profile_id: string;
  resume_id: string;
  cover_letter_id?: string;
  tailored_resume_path?: string;
  tailored_cover_letter_path?: string;
  ats_score: number;
  match_score: number;
  status: ApplicationStatus;
  submitted_at?: string;
  confirmed_at?: string;
  receipt_data: Record<string, unknown>;
  follow_up_dates: string[];
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  location?: string;
  linkedin_url?: string;
  portfolio_url?: string;
  github_url?: string;
  headline: string;
  summary: string;
  skills: Skill[];
  experience: Experience[];
  education: Education[];
  certifications: string[];
  languages: string[];
  preferences: JobPreferences;
  documents: Document[];
  resume_base?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface ScrapeJob {
  id: string;
  source: JobSource;
  query: string;
  location?: string;
  job_type?: JobType;
  max_results: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  jobs_found: number;
  jobs_new: number;
  jobs_updated: number;
  error?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface ATSScoreResponse {
  job_id: string;
  profile_id: string;
  keyword_match: number;
  semantic_similarity: number;
  experience_relevance: number;
  education_match: number;
  overall: number;
  details: Record<string, unknown>;
  tier: string;
  should_auto_apply: boolean;
  should_flag_for_review: boolean;
}

export interface PipelineStatsResponse {
  total_jobs: number;
  new: number;
  fetched: number;
  matched: number;
  scored: number;
  applied: number;
  interview: number;
  offer: number;
  rejected: number;
  by_source: Record<string, number>;
  by_type: Record<string, number>;
  avg_ats_score: number;
  avg_match_score: number;
}

export interface JobListResponse {
  jobs: Job[];
  total: number;
  limit: number;
  offset: number;
}

export interface ApplicationListResponse {
  applications: Application[];
  total: number;
}

export interface MatchJobsResponse {
  matches: Array<{
    job: Job;
    match_score: number;
    match_tier?: MatchTier;
  }>;
  total: number;
}

export interface JobFilter {
  status?: JobStatus;
  source?: JobSource;
  job_type?: JobType;
  location?: string;
  min_ats_score?: number;
  max_ats_score?: number;
  min_match_score?: number;
  max_match_score?: number;
  search?: string;
  limit?: number;
  offset?: number;
}

// UI-specific types
export interface JobCardProps {
  job: Job;
  onClick: () => void;
  matchScore?: number;
  matchTier?: MatchTier;
}

export interface PipelineColumnProps {
  status: JobStatus;
  title: string;
  jobs: Job[];
  onJobClick: (job: Job) => void;
  onDragStart?: (job: Job) => void;
  onDragOver?: (e: React.DragEvent, status: JobStatus) => void;
  onDrop?: (e: React.DragEvent, status: JobStatus) => void;
}

export interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'stable';
  icon?: React.ReactNode;
  accentColor?: 'orange' | 'red' | 'cyan' | 'navy' | 'emerald' | 'blue' | 'purple' | 'amber';
  className?: string;
}
