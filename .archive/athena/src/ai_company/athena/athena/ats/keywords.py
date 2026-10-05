"""ATS Keyword extraction and management."""

import re
from collections import Counter
from typing import Any, Dict, List, Optional

# Industry-specific keyword dictionaries
INDUSTRY_KEYWORDS = {
    "software_engineering": {
        "languages": [
            "python",
            "javascript",
            "typescript",
            "java",
            "c++",
            "c#",
            "go",
            "rust",
            "ruby",
            "php",
            "swift",
            "kotlin",
        ],
        "frameworks": [
            "react",
            "vue",
            "angular",
            "node",
            "django",
            "flask",
            "fastapi",
            "spring",
            "express",
            "nextjs",
            "nuxt",
        ],
        "databases": [
            "sql",
            "postgresql",
            "mysql",
            "mongodb",
            "redis",
            "elasticsearch",
            "cassandra",
            "dynamodb",
        ],
        "cloud": ["aws", "azure", "gcp", "cloud", "serverless", "lambda", "ec2", "s3", "rds"],
        "devops": [
            "docker",
            "kubernetes",
            "terraform",
            "ansible",
            "ci/cd",
            "jenkins",
            "github actions",
            "gitlab",
        ],
        "tools": ["git", "jira", "confluence", "vs code", "intellij", "postman", "swagger"],
    },
    "data_science": {
        "languages": ["python", "r", "sql", "julia", "scala"],
        "ml": [
            "machine learning",
            "deep learning",
            "nlp",
            "computer vision",
            "reinforcement learning",
        ],
        "frameworks": [
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "keras",
            "xgboost",
            "lightgbm",
            "hugging face",
        ],
        "data": ["pandas", "numpy", "spark", "hadoop", "kafka", "airflow", "dbt", "snowflake"],
        "visualization": ["tableau", "power bi", "matplotlib", "seaborn", "plotly", "looker"],
    },
    "project_management": {
        "methodologies": ["agile", "scrum", "kanban", "waterfall", "safe", "lean", "six sigma"],
        "tools": ["jira", "asana", "trello", "monday", "notion", "ms project", "smartsheet"],
        "skills": [
            "planning",
            "scheduling",
            "risk management",
            "stakeholder management",
            "budgeting",
        ],
    },
    "marketing": {
        "digital": ["seo", "sem", "ppc", "google ads", "facebook ads", "analytics", "ga4", "gtm"],
        "content": [
            "copywriting",
            "content strategy",
            "blogging",
            "social media",
            "email marketing",
        ],
        "tools": ["hubspot", "mailchimp", "salesforce", "marketo", "pardot", "klaviyo"],
    },
    "finance": {
        "accounting": ["gaap", "ifrs", "financial reporting", "audit", "tax", "bookkeeping"],
        "analysis": [
            "financial modeling",
            "forecasting",
            "valuation",
            "excel",
            "power bi",
            "tableau",
        ],
        "tools": ["quickbooks", "xero", "netsuite", "sap", "oracle", "hyperion"],
    },
}


def extract_keywords_from_text(text: str, industry: Optional[str] = None) -> List[str]:
    """Extract keywords from text, optionally filtered by industry."""
    text_lower = text.lower()
    keywords = set()

    # Use industry-specific keywords if provided
    if industry and industry in INDUSTRY_KEYWORDS:
        for _category, terms in INDUSTRY_KEYWORDS[industry].items():
            for term in terms:
                if term in text_lower:
                    keywords.add(term)
    else:
        # Use all industries
        for ind_keywords in INDUSTRY_KEYWORDS.values():
            for _category, terms in ind_keywords.items():
                for term in terms:
                    if term in text_lower:
                        keywords.add(term)

    # Extract capitalized terms (technologies, proper nouns)
    capitalized = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
    for term in capitalized:
        if len(term) > 2:
            keywords.add(term.lower())

    # Extract hyphenated terms
    hyphenated = re.findall(r"\b\w+(?:-\w+)+\b", text_lower)
    keywords.update(hyphenated)

    # Extract acronyms (3+ uppercase letters)
    acronyms = re.findall(r"\b[A-Z]{3,}\b", text)
    keywords.update([a.lower() for a in acronyms])

    return sorted(list(keywords))


def get_keyword_frequency(texts: List[str], industry: Optional[str] = None) -> Dict[str, int]:
    """Get frequency count of keywords across multiple texts."""
    all_keywords = []
    for text in texts:
        all_keywords.extend(extract_keywords_from_text(text, industry))
    return dict(Counter(all_keywords))


def suggest_keywords_for_job(job_title: str, job_description: str) -> List[str]:
    """Suggest relevant keywords for a job posting."""
    combined = f"{job_title} {job_description}"
    return extract_keywords_from_text(combined)


def compare_keywords(keywords1: List[str], keywords2: List[str]) -> Dict[str, Any]:
    """Compare two keyword lists."""
    set1 = set(keywords1)
    set2 = set(keywords2)

    return {
        "common": sorted(list(set1 & set2)),
        "only_in_first": sorted(list(set1 - set2)),
        "only_in_second": sorted(list(set2 - set1)),
        "jaccard_similarity": len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0,
    }
