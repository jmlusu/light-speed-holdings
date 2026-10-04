import re
from dataclasses import dataclass
from typing import Any, Dict, Set

from ..matching import matching_engine
from ..models import Job, UserProfile


@dataclass
class ATSScoreBreakdown:
    keyword_match: float
    semantic_similarity: float
    experience_relevance: float
    education_match: float
    overall: float
    details: Dict[str, Any]


class ATSScorer:
    """ATS (Applicant Tracking System) scoring engine."""

    # Common ATS keywords by category
    TECH_KEYWORDS = {
        "python",
        "javascript",
        "typescript",
        "java",
        "c++",
        "c#",
        "go",
        "rust",
        "react",
        "vue",
        "angular",
        "node",
        "django",
        "flask",
        "fastapi",
        "spring",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "elasticsearch",
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "terraform",
        "ansible",
        "git",
        "ci/cd",
        "jenkins",
        "github actions",
        "gitlab",
        "jira",
        "confluence",
        "machine learning",
        "ai",
        "llm",
        "nlp",
        "computer vision",
        "data science",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "hugging face",
    }

    SOFT_SKILLS = {
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "critical thinking",
        "adaptability",
        "time management",
        "project management",
        "agile",
        "scrum",
        "collaboration",
        "mentoring",
        "analytical",
        "creative",
        "detail oriented",
    }

    def __init__(self) -> None:
        self.matching_engine = matching_engine

    def score_resume_against_job(self, profile: UserProfile, job: Job) -> ATSScoreBreakdown:
        """Score a resume/profile against a job description."""

        # 1. Keyword Match (40% weight)
        keyword_score, keyword_details = self._compute_keyword_match(profile, job)

        # 2. Semantic Similarity (35% weight)
        semantic_score = self.matching_engine.compute_match_score(profile, job)
        semantic_details = self.matching_engine.find_matching_skills(profile, job)

        # 3. Experience Relevance (15% weight)
        experience_score, exp_details = self._compute_experience_relevance(profile, job)

        # 4. Education Match (10% weight)
        education_score, edu_details = self._compute_education_match(profile, job)

        # Weighted overall score
        overall = (
            keyword_score * 0.40
            + semantic_score * 0.35
            + experience_score * 0.15
            + education_score * 0.10
        )

        return ATSScoreBreakdown(
            keyword_match=round(keyword_score, 1),
            semantic_similarity=round(semantic_score, 1),
            experience_relevance=round(experience_score, 1),
            education_match=round(education_score, 1),
            overall=round(overall, 1),
            details={
                "keywords": keyword_details,
                "semantic": semantic_details,
                "experience": exp_details,
                "education": edu_details,
            },
        )

    def _compute_keyword_match(
        self, profile: UserProfile, job: Job
    ) -> tuple[float, Dict[str, Any]]:
        """Compute keyword-based match score."""
        # Extract keywords from job
        job_keywords = self._extract_job_keywords(job)
        if not job_keywords:
            return 0.0, {"matched": [], "missing": [], "total_job_keywords": 0}

        # Extract keywords from profile
        profile_keywords = self._extract_profile_keywords(profile)

        # Calculate matches
        matched = job_keywords & profile_keywords
        missing = job_keywords - profile_keywords

        score = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0

        return score, {
            "matched": sorted(list(matched)),
            "missing": sorted(list(missing)),
            "total_job_keywords": len(job_keywords),
            "matched_count": len(matched),
        }

    def _extract_job_keywords(self, job: Job) -> Set[str]:
        """Extract relevant keywords from job description."""
        keywords = set()

        # Explicit keywords
        for kw in job.keywords:
            keywords.add(kw.lower().strip())

        # From requirements
        for req in job.requirements:
            keywords.update(self._extract_skills_from_text(req))

        # From responsibilities
        for resp in job.responsibilities:
            keywords.update(self._extract_skills_from_text(resp))

        # From description
        if job.description:
            keywords.update(self._extract_skills_from_text(job.description))

        # From title
        keywords.update(self._extract_skills_from_text(job.title))

        # Filter out common words
        stopwords = {
            "and",
            "or",
            "the",
            "a",
            "an",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "as",
            "is",
            "be",
            "are",
            "was",
            "were",
            "has",
            "have",
            "had",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "need",
            "our",
            "you",
            "your",
            "we",
            "us",
            "their",
            "this",
            "that",
            "these",
            "those",
        }
        return {k for k in keywords if k not in stopwords and len(k) > 2}

    def _extract_profile_keywords(self, profile: UserProfile) -> Set[str]:
        """Extract keywords from user profile."""
        keywords = set()

        # From skills
        for skill in profile.skills:
            keywords.add(skill.name.lower().strip())
            if skill.category:
                keywords.add(skill.category.lower().strip())

        # From experience
        for exp in profile.experience:
            keywords.update(self._extract_skills_from_text(exp.title))
            keywords.update(self._extract_skills_from_text(exp.description))
            for used_skill in exp.skills_used:
                keywords.add(used_skill.lower().strip())

        # From headline and summary
        if profile.headline:
            keywords.update(self._extract_skills_from_text(profile.headline))
        if profile.summary:
            keywords.update(self._extract_skills_from_text(profile.summary))

        # From certifications
        for cert in profile.certifications:
            keywords.add(cert.lower().strip())

        return keywords

    def _extract_skills_from_text(self, text: str) -> Set[str]:
        """Extract potential skill keywords from text."""
        # Common skill patterns
        text_lower = text.lower()
        skills = set()

        # Known tech skills
        for tech in self.TECH_KEYWORDS:
            if tech in text_lower:
                skills.add(tech)

        # Known soft skills
        for soft in self.SOFT_SKILLS:
            if soft in text_lower:
                skills.add(soft)

        # Extract capitalized words (potential proper nouns/technologies)
        words = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
        for word in words:
            if len(word) > 2:
                skills.add(word.lower())

        # Extract hyphenated terms
        hyphenated = re.findall(r"\b\w+(?:-\w+)+\b", text_lower)
        skills.update(hyphenated)

        return skills

    def _compute_experience_relevance(
        self, profile: UserProfile, job: Job
    ) -> tuple[float, Dict[str, Any]]:
        """Compute experience relevance score."""
        if not profile.experience:
            return 0.0, {"years_experience": 0, "relevant_roles": 0}

        total_years: float = 0
        relevant_years: float = 0
        relevant_roles = 0

        job_keywords = self._extract_job_keywords(job)
        job_title_words = set(job.title.lower().split())

        for exp in profile.experience:
            # Calculate years
            if exp.end_date:
                years = (exp.end_date - exp.start_date).days / 365.25
            else:
                from datetime import datetime

                years = (datetime.utcnow() - exp.start_date).days / 365.25

            total_years += years

            # Check relevance
            exp_text = f"{exp.title} {exp.description} {' '.join(exp.skills_used)}".lower()
            exp_keywords = self._extract_skills_from_text(exp_text)

            overlap = job_keywords & exp_keywords
            title_overlap = job_title_words & set(exp.title.lower().split())

            if overlap or title_overlap:
                relevant_years += years
                relevant_roles += 1

        # Score based on relevant years (cap at 10 years for max score)
        if total_years == 0:
            return 0.0, {"years_experience": 0, "relevant_roles": 0}

        relevance_ratio = relevant_years / total_years if total_years > 0 else 0
        years_score = min(relevant_years / 10, 1.0) * 100

        return years_score, {
            "total_years": round(total_years, 1),
            "relevant_years": round(relevant_years, 1),
            "relevant_roles": relevant_roles,
            "relevance_ratio": round(relevance_ratio, 2),
        }

    def _compute_education_match(
        self, profile: UserProfile, job: Job
    ) -> tuple[float, Dict[str, Any]]:
        """Compute education match score."""
        if not profile.education:
            return 50.0, {"has_degree": False, "matching_fields": []}  # Neutral

        job_text = f"{job.title} {' '.join(job.requirements)} {' '.join(job.keywords)}".lower()

        # Check for degree requirements in job
        degree_keywords = ["bachelor", "master", "phd", "degree", "bs", "ms", "ba", "ma", "mba"]
        requires_degree = any(kw in job_text for kw in degree_keywords)

        if not requires_degree:
            return 75.0, {"has_degree": True, "degree_not_required": True}

        has_degree = len(profile.education) > 0
        if not has_degree:
            return 0.0, {"has_degree": False}

        # Check field relevance
        job_keywords = self._extract_job_keywords(job)
        matching_fields = []
        for edu in profile.education:
            field_words = set(edu.field_of_study.lower().split())
            if field_words & job_keywords:
                matching_fields.append(edu.field_of_study)

        field_score = 100 if matching_fields else 60

        return field_score, {
            "has_degree": True,
            "degrees": [f"{e.degree} in {e.field_of_study}" for e in profile.education],
            "matching_fields": matching_fields,
        }

    def get_score_tier(self, score: float) -> str:
        """Get tier label for score."""
        if score >= 90:
            return "excellent"
        elif score >= 80:
            return "good"
        elif score >= 70:
            return "fair"
        else:
            return "poor"

    def should_auto_apply(self, score: float) -> bool:
        """Determine if application should be auto-submitted."""
        return score >= 90

    def should_flag_for_review(self, score: float) -> bool:
        """Determine if application should be flagged for human review."""
        return 80 <= score < 90


# Global instance
ats_scorer = ATSScorer()
