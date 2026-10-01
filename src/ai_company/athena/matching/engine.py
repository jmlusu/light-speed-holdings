from typing import Dict, List, Optional, Tuple

from ..models import Job, MatchTier, Skill, UserProfile
from .embeddings import cosine_similarity, embedding_model


class MatchingEngine:
    """Semantic matching engine for jobs and user profiles."""

    def __init__(self) -> None:
        self.model = embedding_model

    def build_profile_text(self, profile: UserProfile) -> str:
        """Build a comprehensive text representation of user profile."""
        parts = []

        if profile.headline:
            parts.append(f"Headline: {profile.headline}")

        if profile.summary:
            parts.append(f"Summary: {profile.summary}")

        if profile.skills:
            skills_text = ", ".join([f"{s.name} ({s.level or 'unknown'})" for s in profile.skills])
            parts.append(f"Skills: {skills_text}")

        if profile.experience:
            exp_texts = []
            for exp in profile.experience:
                exp_text = f"{exp.title} at {exp.company}"
                if exp.description:
                    exp_text += f": {exp.description}"
                if exp.skills_used:
                    exp_text += f" [Skills: {', '.join(exp.skills_used)}]"
                exp_texts.append(exp_text)
            parts.append(f"Experience: {'; '.join(exp_texts)}")

        if profile.education:
            edu_texts = [
                f"{e.degree} in {e.field_of_study} from {e.institution}" for e in profile.education
            ]
            parts.append(f"Education: {'; '.join(edu_texts)}")

        if profile.certifications:
            parts.append(f"Certifications: {', '.join(profile.certifications)}")

        if profile.languages:
            parts.append(f"Languages: {', '.join(profile.languages)}")

        return "\n\n".join(parts)

    def build_job_text(self, job: Job) -> str:
        """Build a comprehensive text representation of job."""
        parts = []

        parts.append(f"Title: {job.title}")
        parts.append(f"Company: {job.company}")
        parts.append(f"Location: {job.location}")
        parts.append(f"Type: {job.job_type.value}")

        if job.description:
            parts.append(f"Description: {job.description}")

        if job.requirements:
            parts.append(f"Requirements: {'; '.join(job.requirements)}")

        if job.responsibilities:
            parts.append(f"Responsibilities: {'; '.join(job.responsibilities)}")

        if job.keywords:
            parts.append(f"Keywords: {', '.join(job.keywords)}")

        if job.benefits:
            parts.append(f"Benefits: {', '.join(job.benefits)}")

        return "\n\n".join(parts)

    def compute_match_score(self, profile: UserProfile, job: Job) -> float:
        """Compute semantic match score between profile and job (0-100)."""
        if not self.model.is_available():
            return self._keyword_match_score(profile, job)

        profile_text = self.build_profile_text(profile)
        job_text = self.build_job_text(job)

        profile_embedding = self.model.encode_single(profile_text)
        job_embedding = self.model.encode_single(job_text)

        similarity = cosine_similarity(profile_embedding, job_embedding)
        # Convert cosine similarity (-1 to 1) to 0-100 scale
        score = (similarity + 1) * 50
        return min(100, max(0, score))

    def _keyword_match_score(self, profile: UserProfile, job: Job) -> float:
        """Fallback keyword-based matching when embeddings unavailable."""
        profile_keywords = set()
        for skill in profile.skills:
            profile_keywords.add(skill.name.lower())
        for exp in profile.experience:
            for used_skill in exp.skills_used:
                profile_keywords.add(used_skill.lower())
        if profile.headline:
            profile_keywords.update(profile.headline.lower().split())
        if profile.summary:
            profile_keywords.update(profile.summary.lower().split())

        job_keywords = set()
        for kw in job.keywords:
            job_keywords.add(kw.lower())
        for req in job.requirements:
            job_keywords.update(req.lower().split())
        for resp in job.responsibilities:
            job_keywords.update(resp.lower().split())
        if job.description:
            job_keywords.update(job.description.lower().split())
        job_keywords.update(job.title.lower().split())

        if not job_keywords:
            return 0.0

        matches = profile_keywords & job_keywords
        return (len(matches) / len(job_keywords)) * 100

    def rank_jobs(
        self, profile: UserProfile, jobs: List[Job], top_k: Optional[int] = None
    ) -> List[Tuple[Job, float]]:
        """Rank jobs by match score for a profile."""
        scored_jobs = []
        for job in jobs:
            score = self.compute_match_score(profile, job)
            job.match_score = score
            job.match_tier = self._get_match_tier(score)
            scored_jobs.append((job, score))

        scored_jobs.sort(key=lambda x: x[1], reverse=True)

        if top_k:
            scored_jobs = scored_jobs[:top_k]

        return scored_jobs

    def _get_match_tier(self, score: float) -> MatchTier:
        if score >= 90:
            return MatchTier.EXCELLENT
        elif score >= 80:
            return MatchTier.GOOD
        elif score >= 70:
            return MatchTier.FAIR
        return MatchTier.POOR

    def find_matching_skills(self, profile: UserProfile, job: Job) -> Dict[str, List[str]]:
        """Find matching and missing skills between profile and job."""
        profile_skills = {s.name.lower(): s for s in profile.skills}
        for exp in profile.experience:
            for skill in exp.skills_used:
                profile_skills[skill.lower()] = Skill(name=skill)

        job_skills = set()
        for kw in job.keywords:
            job_skills.add(kw.lower())
        for req in job.requirements:
            for word in req.lower().split():
                if len(word) > 3:
                    job_skills.add(word)
        for resp in job.responsibilities:
            for word in resp.lower().split():
                if len(word) > 3:
                    job_skills.add(word)

        matching = []
        missing = []

        for job_skill in job_skills:
            if job_skill in profile_skills:
                matching.append(job_skill)
            else:
                missing.append(job_skill)

        return {
            "matching": matching[:20],
            "missing": missing[:20],
        }


# Global instance
matching_engine = MatchingEngine()
