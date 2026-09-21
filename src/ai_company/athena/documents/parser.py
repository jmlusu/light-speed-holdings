"""
Resume parser for Athena using k-dense-liteparse skill.

This module provides a pluggable document parser architecture that can extract
structured resume data from PDF and DOCX files, mapping to UserProfile model fields.
"""

import asyncio
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..models import Document, Education, Experience, Skill, UserProfile

logger = logging.getLogger(__name__)


@dataclass
class ParsedSection:
    """Represents a parsed section of a resume."""

    name: str
    content: str
    raw_text: str
    bbox: Optional[Tuple[float, float, float, float]] = None  # x0, y0, x1, y1


@dataclass
class ParseResult:
    """Result of parsing a resume document."""

    success: bool
    profile_data: Dict[str, Any] = field(default_factory=dict)
    sections: List[ParsedSection] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    raw_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_user_profile(self, email: str, file_path: str) -> UserProfile:
        """Convert parsed data to UserProfile model."""
        return UserProfile(
            email=email,
            full_name=self.profile_data.get("full_name", ""),
            phone=self.profile_data.get("phone"),
            location=self.profile_data.get("location"),
            linkedin_url=self.profile_data.get("linkedin_url"),
            portfolio_url=self.profile_data.get("portfolio_url"),
            github_url=self.profile_data.get("github_url"),
            headline=self.profile_data.get("headline", ""),
            summary=self.profile_data.get("summary", ""),
            skills=[Skill(**s) for s in self.profile_data.get("skills", [])],
            experience=[Experience(**e) for e in self.profile_data.get("experience", [])],
            education=[Education(**edu) for edu in self.profile_data.get("education", [])],
            certifications=self.profile_data.get("certifications", []),
            languages=self.profile_data.get("languages", []),
            resume_base=self.profile_data,
            documents=[
                Document(
                    name=Path(file_path).name,
                    type="resume",
                    file_path=file_path,
                    mime_type=self._get_mime_type(file_path),
                    size_bytes=Path(file_path).stat().st_size if Path(file_path).exists() else 0,
                    parsed_content=self.profile_data,
                )
            ],
        )

    def _get_mime_type(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        return {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
        }.get(ext, "application/octet-stream")


class DocumentParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    async def parse(self, file_path: Path) -> ParseResult:
        """Parse a document and return structured data."""
        pass

    @abstractmethod
    def supports_format(self, file_path: Path) -> bool:
        """Check if this parser supports the given file format."""
        pass

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove zero-width characters
        text = text.replace("\u200b", "").replace("\ufeff", "")
        return text.strip()

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text."""
        # Match various phone formats
        patterns = [
            r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    def _extract_urls(self, text: str) -> Dict[str, Optional[str]]:
        """Extract LinkedIn, GitHub, portfolio URLs from text."""
        urls: Dict[str, Optional[str]] = {
            "linkedin_url": None,
            "github_url": None,
            "portfolio_url": None,
        }

        linkedin_match = re.search(
            r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+", text, re.IGNORECASE
        )
        if linkedin_match:
            url = linkedin_match.group(0)
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            urls["linkedin_url"] = url

        github_match = re.search(
            r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+", text, re.IGNORECASE
        )
        if github_match:
            url = github_match.group(0)
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            urls["github_url"] = url

        # Generic portfolio/personal site
        portfolio_match = re.search(
            r"(?:https?://)?(?:www\.)?[A-Za-z0-9_-]+\.(?:com|io|dev|me|app)", text, re.IGNORECASE
        )
        if portfolio_match and not any(portfolio_match.group(0) in v for v in urls.values() if v):
            url = portfolio_match.group(0)
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            urls["portfolio_url"] = url

        return urls

    def _parse_skills(self, text: str) -> List[Dict[str, Any]]:
        """Parse skills from text."""
        skills = []
        # Common skill keywords/patterns
        skill_section = re.search(
            r"(?:skills?|technologies?|tools?|stack|competencies)[:\s]\n?(.*?)(?:\n\n|\n[A-Z]|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if skill_section:
            skill_text = skill_section.group(1)
            # Split by common delimiters
            skill_items = re.split(r"[,\n•|;]", skill_text)
            for item in skill_items:
                item = item.strip()
                if item and len(item) > 1:
                    # Try to extract level
                    level_match = re.search(
                        r"(beginner|intermediate|advanced|expert)", item, re.IGNORECASE
                    )
                    level = level_match.group(1).lower() if level_match else None
                    name = re.sub(
                        r"\s*\(?(?:beginner|intermediate|advanced|expert)\)?",
                        "",
                        item,
                        flags=re.IGNORECASE,
                    ).strip()
                    if name:
                        skills.append({"name": name, "level": level})
        return skills

    def _parse_experience(self, text: str) -> List[Dict[str, Any]]:
        """Parse work experience from text."""
        experiences = []
        # Look for experience section
        exp_section = re.search(
            r"(?:experience|employment|work history|career)[:\s]\n?(.*?)(?:\n\n|\n[A-Z][a-z]+:|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if exp_section:
            exp_text = exp_section.group(1)
            # Split by job entries (look for date patterns or company names)
            job_entries = re.split(r"\n\s*\n", exp_text)
            for entry in job_entries:
                entry = entry.strip()
                if not entry:
                    continue

                exp = self._parse_single_experience(entry)
                if exp:
                    experiences.append(exp)
        return experiences

    def _parse_single_experience(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse a single experience entry."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return None

        # First line often has title and company
        first_line = lines[0]

        # Try to extract dates
        date_pattern = (
            r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|\d{1,2}/\d{4}|\d{4}"
        )
        dates = re.findall(date_pattern, text, re.IGNORECASE)

        start_date = None
        end_date = None
        current = False

        if len(dates) >= 1:
            try:
                if re.match(r"[A-Za-z]{3}\s+\d{4}", dates[0]):
                    start_date = datetime.strptime(dates[0], "%b %Y")
                else:
                    start_date = datetime(int(dates[0]), 1, 1)
            except ValueError:
                pass
        if len(dates) >= 2:
            try:
                if re.match(r"[A-Za-z]{3}\s+\d{4}", dates[1]):
                    end_date = datetime.strptime(dates[1], "%b %Y")
                else:
                    end_date = datetime(int(dates[1]), 12, 31)
            except ValueError:
                pass
        elif "present" in text.lower() or "current" in text.lower():
            current = True

        # Extract title and company (heuristic)
        title = ""
        company = ""
        if " at " in first_line:
            parts = first_line.split(" at ", 1)
            title = parts[0].strip()
            company = parts[1].strip()
        elif " - " in first_line:
            parts = first_line.split(" - ", 1)
            title = parts[0].strip()
            company = parts[1].strip()
        else:
            title = first_line

        # Description from remaining lines
        description = "\n".join(lines[1:]) if len(lines) > 1 else ""

        # Extract skills mentioned
        skills_used = []
        skill_keywords = [
            "python",
            "java",
            "javascript",
            "react",
            "sql",
            "aws",
            "docker",
            "kubernetes",
            "git",
            "linux",
            "agile",
            "scrum",
        ]
        for kw in skill_keywords:
            if kw.lower() in text.lower():
                skills_used.append(kw)

        return {
            "title": title,
            "company": company,
            "start_date": start_date or datetime.now(),
            "end_date": end_date,
            "current": current,
            "description": description,
            "skills_used": skills_used,
            "achievements": [],
        }

    def _parse_education(self, text: str) -> List[Dict[str, Any]]:
        """Parse education from text."""
        education = []
        edu_section = re.search(
            r"(?:education|academic|degree|university|college)[:\s]\n?(.*?)(?:\n\n|\n[A-Z][a-z]+:|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if edu_section:
            edu_text = edu_section.group(1)
            entries = re.split(r"\n\s*\n", edu_text)
            for entry in entries:
                entry = entry.strip()
                if not entry:
                    continue

                # Try to extract degree, institution, field
                lines = [line.strip() for line in entry.split("\n") if line.strip()]
                if not lines:
                    continue

                institution = lines[0]
                degree = ""
                field_of_study = ""

                if len(lines) > 1:
                    degree = lines[1]
                if len(lines) > 2:
                    field_of_study = lines[2]

                # Extract dates
                dates = re.findall(r"\d{4}", entry)
                start_date = None
                end_date = None
                if dates:
                    try:
                        start_date = datetime(int(dates[0]), 1, 1)
                        if len(dates) > 1:
                            end_date = datetime(int(dates[1]), 12, 31)
                    except ValueError:
                        pass

                education.append(
                    {
                        "institution": institution,
                        "degree": degree,
                        "field_of_study": field_of_study,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )
        return education

    def _extract_profile_data(
        self, full_text: str, sections: List[ParsedSection]
    ) -> Dict[str, Any]:
        """Extract structured profile data from parsed text and sections."""
        profile: Dict[str, Any] = {}

        # Extract basic info from first part of text
        first_section = full_text[:2000] if full_text else ""

        # Name - try to extract from first lines
        name = self._extract_name(first_section)
        if name:
            profile["full_name"] = name

        # Email
        email = self._extract_email(full_text)
        if email:
            profile["email"] = email

        # Phone
        phone = self._extract_phone(full_text)
        if phone:
            profile["phone"] = phone

        # URLs
        urls = self._extract_urls(full_text)
        profile.update(urls)

        # Location - try to find in first section
        location = self._extract_location(first_section)
        if location:
            profile["location"] = location

        # Headline - first non-empty line after name
        headline = self._extract_headline(first_section, name)
        if headline:
            profile["headline"] = headline

        # Summary - look for summary/objective section
        summary = self._extract_summary(full_text)
        if summary:
            profile["summary"] = summary

        # Skills
        skills = self._parse_skills(full_text)
        if skills:
            profile["skills"] = skills

        # Experience
        experience = self._parse_experience(full_text)
        if experience:
            profile["experience"] = experience

        # Education
        education = self._parse_education(full_text)
        if education:
            profile["education"] = education

        # Certifications
        certs = self._parse_certifications(full_text)
        if certs:
            profile["certifications"] = certs

        # Languages
        languages = self._parse_languages(full_text)
        if languages:
            profile["languages"] = languages

        return profile

    def _extract_name(self, text: str) -> Optional[str]:
        """Extract person name from text."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return None
        # First non-empty line is often the name
        first_line = lines[0]
        # Skip if it looks like a header
        if len(first_line) > 50 or any(
            kw in first_line.lower() for kw in ["resume", "cv", "curriculum", "profile"]
        ):
            return None
        # Should be 2-4 words, title case
        words = first_line.split()
        if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
            return first_line
        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from text."""
        # Look for city, state/country patterns
        location_patterns = [
            r"\b[A-Z][a-z]+,\s*[A-Z]{2}\b",  # City, ST
            r"\b[A-Z][a-z]+,\s*[A-Z][a-z]+\b",  # City, Country
            r"\b(?:Remote|Hybrid|On-site)\b",
        ]
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    def _extract_headline(self, text: str, name: Optional[str]) -> Optional[str]:
        """Extract professional headline."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        start_idx = 1 if name and lines and lines[0] == name else 0
        for line in lines[start_idx : start_idx + 3]:
            if (
                len(line) > 10
                and len(line) < 200
                and not any(
                    kw in line.lower()
                    for kw in ["email", "phone", "linkedin", "github", "@", "http"]
                )
            ):
                return line
        return None

    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract summary/objective section."""
        patterns = [
            r"(?:summary|objective|profile|about)[:\s]\n?(.*?)(?:\n\n|\n[A-Z][a-z]+:|\Z)",
            r"(?:professional summary|career summary)[:\s]\n?(.*?)(?:\n\n|\n[A-Z][a-z]+:|\Z)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                summary = match.group(1).strip()
                if len(summary) > 20:
                    return summary
        return None

    def _parse_certifications(self, text: str) -> List[str]:
        """Parse certifications from text."""
        certs = []
        cert_section = re.search(
            r"(?:certifications?|licenses?|credentials?)[:\s]\n?(.*?)(?:\n\n|\n[A-Z][a-z]+:|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if cert_section:
            cert_text = cert_section.group(1)
            items = re.split(r"[\n•|;]", cert_text)
            for item in items:
                item = item.strip()
                if item and len(item) > 3:
                    certs.append(item)
        return certs

    def _parse_languages(self, text: str) -> List[str]:
        """Parse languages from text."""
        languages = []
        lang_section = re.search(
            r"(?:languages?)[:\s]\n?(.*?)(?:\n\n|\n[A-Z][a-z]+:|\Z)",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if lang_section:
            lang_text = lang_section.group(1)
            items = re.split(r"[\n,•|;]", lang_text)
            for item in items:
                item = item.strip()
                if item and len(item) > 1:
                    languages.append(item)
        return languages


class PDFParser(DocumentParser):
    """PDF parser using pdfplumber for layout-aware extraction."""

    def __init__(self) -> None:
        self._pdfplumber: Any = None
        self._try_import()

    def _try_import(self) -> None:
        try:
            import pdfplumber

            self._pdfplumber = pdfplumber
        except ImportError:
            logger.warning("pdfplumber not installed. PDF parsing will be limited.")
            self._pdfplumber = None

    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".pdf"

    async def parse(self, file_path: Path) -> ParseResult:
        if not self._pdfplumber:
            return ParseResult(
                success=False,
                errors=["pdfplumber not installed. Install with: pip install pdfplumber"],
            )

        return await asyncio.to_thread(self._parse_sync, file_path)

    def _parse_sync(self, file_path: Path) -> ParseResult:
        result = ParseResult(success=True)
        sections = []
        full_text = ""

        try:
            with self._pdfplumber.open(file_path) as pdf:
                result.metadata["page_count"] = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages):
                    # Extract text with layout info
                    text = page.extract_text() or ""
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}"

                    # Extract words with bounding boxes for layout awareness
                    words = page.extract_words() or []
                    if words:
                        # Group words into lines by y-position
                        lines = self._group_words_into_lines(words)
                        for line in lines:
                            line_text = " ".join(w["text"] for w in line)
                            if line_text.strip():
                                bbox = self._get_line_bbox(line)
                                sections.append(
                                    ParsedSection(
                                        name=f"page_{page_num + 1}",
                                        content=line_text,
                                        raw_text=line_text,
                                        bbox=bbox,
                                    )
                                )

                    # Extract tables
                    tables = page.extract_tables() or []
                    for table_idx, table in enumerate(tables):
                        table_text = self._table_to_text(table)
                        if table_text:
                            sections.append(
                                ParsedSection(
                                    name=f"page_{page_num + 1}_table_{table_idx}",
                                    content=table_text,
                                    raw_text=table_text,
                                )
                            )

            result.raw_text = full_text
            result.sections = sections
            result.profile_data = self._extract_profile_data(full_text, sections)

        except Exception as e:
            logger.exception(f"Error parsing PDF {file_path}")
            result.success = False
            result.errors.append(str(e))

        return result

    def _group_words_into_lines(
        self, words: List[Dict[str, Any]], y_tolerance: float = 3.0
    ) -> List[List[Dict[str, Any]]]:
        """Group words into lines based on y-position."""
        if not words:
            return []

        # Sort by y then x
        words = sorted(words, key=lambda w: (w.get("top", 0), w.get("x0", 0)))

        lines: List[List[Dict[str, Any]]] = []
        current_line: List[Dict[str, Any]] = [words[0]]

        for word in words[1:]:
            last_word = current_line[-1]
            if abs(word.get("top", 0) - last_word.get("top", 0)) <= y_tolerance:
                current_line.append(word)
            else:
                lines.append(current_line)
                current_line = [word]

        lines.append(current_line)
        return lines

    def _get_line_bbox(self, line: List[Dict[str, Any]]) -> Tuple[float, float, float, float]:
        """Get bounding box for a line of words."""
        x0 = min(w.get("x0", 0) for w in line)
        y0 = min(w.get("top", 0) for w in line)
        x1 = max(w.get("x1", 0) for w in line)
        y1 = max(w.get("bottom", 0) for w in line)
        return (x0, y0, x1, y1)

    def _table_to_text(self, table: List[List[Any]]) -> str:
        """Convert table to readable text."""
        rows = []
        for row in table:
            cells = [str(cell or "").strip() for cell in row]
            rows.append(" | ".join(cells))
        return "\n".join(rows)


class DOCXParser(DocumentParser):
    """DOCX parser using python-docx."""

    def supports_format(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in [".docx", ".doc"]

    async def parse(self, file_path: Path) -> ParseResult:
        return await asyncio.to_thread(self._parse_sync, file_path)

    def _parse_sync(self, file_path: Path) -> ParseResult:
        result = ParseResult(success=True)
        sections = []
        full_text = ""

        try:
            from docx import Document as DocxDocument

            doc = DocxDocument(str(file_path))

            # Extract paragraphs with style info
            for para_idx, para in enumerate(doc.paragraphs):
                text = para.text.strip()
                if text:
                    full_text += f"\n{text}"
                    sections.append(
                        ParsedSection(
                            name=f"paragraph_{para_idx}",
                            content=text,
                            raw_text=text,
                        )
                    )

            # Extract tables
            for table_idx, table in enumerate(doc.tables):
                table_text = self._table_to_text(table)
                if table_text:
                    full_text += f"\n--- Table {table_idx + 1} ---\n{table_text}"
                    sections.append(
                        ParsedSection(
                            name=f"table_{table_idx}",
                            content=table_text,
                            raw_text=table_text,
                        )
                    )

            result.raw_text = full_text
            result.sections = sections
            result.profile_data = self._extract_profile_data(full_text, sections)

        except Exception as e:
            logger.exception(f"Error parsing DOCX {file_path}")
            result.success = False
            result.errors.append(str(e))

        return result

    def _table_to_text(self, table: Any) -> str:
        """Convert docx table to text."""
        rows: List[str] = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append(" | ".join(cells))
        return "\n".join(rows)


class ResumeParser:
    """
    Main resume parser that coordinates different format parsers.

    Uses the k-dense-liteparse approach for layout-aware extraction
    with pluggable backends for different file formats.
    """

    def __init__(self) -> None:
        self.parsers: List[DocumentParser] = [
            PDFParser(),
            DOCXParser(),
        ]

    def add_parser(self, parser: DocumentParser) -> None:
        """Add a custom parser."""
        self.parsers.append(parser)

    def get_parser(self, file_path: Path) -> Optional[DocumentParser]:
        """Get the appropriate parser for a file."""
        for parser in self.parsers:
            if parser.supports_format(file_path):
                return parser
        return None

    async def parse(self, file_path: str | Path) -> ParseResult:
        """
        Parse a resume file and return structured data.

        Args:
            file_path: Path to the resume file (PDF or DOCX)

        Returns:
            ParseResult with extracted profile data
        """
        path = Path(file_path)

        if not path.exists():
            return ParseResult(
                success=False,
                errors=[f"File not found: {file_path}"],
            )

        parser = self.get_parser(path)
        if not parser:
            return ParseResult(
                success=False,
                errors=[f"Unsupported file format: {path.suffix}"],
            )

        logger.info(f"Parsing {path.name} with {parser.__class__.__name__}")
        result = await parser.parse(path)

        if not result.success:
            logger.warning(f"Parsing completed with errors: {result.errors}")

        return result

    async def parse_to_profile(
        self,
        file_path: str | Path,
        email: str,
    ) -> Tuple[Optional[UserProfile], ParseResult]:
        """
        Parse a resume and convert directly to UserProfile.

        Args:
            file_path: Path to the resume file
            email: Email address for the profile (required)

        Returns:
            Tuple of (UserProfile or None, ParseResult)
        """
        result = await self.parse(file_path)

        if not result.success and not result.profile_data:
            return None, result

        try:
            profile = result.to_user_profile(email, str(file_path))
            return profile, result
        except Exception as e:
            logger.exception("Error converting to UserProfile")
            result.success = False
            result.errors.append(f"Profile conversion error: {e}")
            return None, result


# Convenience function for simple usage
async def parse_resume(
    file_path: str | Path, email: str
) -> Tuple[Optional[UserProfile], ParseResult]:
    """Parse a resume file to UserProfile."""
    parser = ResumeParser()
    return await parser.parse_to_profile(file_path, email)


# Export
__all__ = [
    "ResumeParser",
    "DocumentParser",
    "PDFParser",
    "DOCXParser",
    "ParseResult",
    "ParsedSection",
    "parse_resume",
]
