"""
Athena Document Generator - Professional Resume and Cover Letter Generation.

This module provides professional 1-column resume and cover letter templates
using python-docx for .docx output and WeasyPrint for PDF generation.

Follows LightSpeed brand guidelines:
- Off-white background, dark charcoal text
- Soft orange/red (#E63946) and cyan (#00BFFF) accents
- Arial font family
- 4px spacing grid
"""

import asyncio
import io
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from docx.document import Document as DocxDocumentType

from docx import Document as DocxDocumentClass
from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from ..models import Education, Experience, Job, Skill, UserProfile

logger = logging.getLogger(__name__)

# LightSpeed Brand Colors (from brand-tokens.json)
BRAND_NAVY = RGBColor(0x07, 0x0A, 0x40)  # #070A40
BRAND_RED = RGBColor(0xE6, 0x39, 0x46)  # #E63946
BRAND_CYAN = RGBColor(0x00, 0xBF, 0xFF)  # #00BFFF
BRAND_GREY_LIGHT = RGBColor(0xF2, 0xF2, 0xF2)  # #F2F2F2
BRAND_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BRAND_GREY_DARK = RGBColor(0x6B, 0x72, 0x80)  # #6B7280
BRAND_GREY_LIGHT_TEXT = RGBColor(0x9C, 0xA3, 0xAF)  # #9CA3AF

# Font settings
FONT_FAMILY = "Arial"
FONT_SIZE_DISPLAY_XL = Pt(36)
FONT_SIZE_TITLE_XL = Pt(32)
FONT_SIZE_TITLE_LG = Pt(28)
FONT_SIZE_TITLE_MD = Pt(24)
FONT_SIZE_TITLE_SM = Pt(18)
FONT_SIZE_SUBTITLE = Pt(16)
FONT_SIZE_BODY_LG = Pt(16)
FONT_SIZE_BODY = Pt(14)
FONT_SIZE_BODY_SM = Pt(13)
FONT_SIZE_CAPTION = Pt(12)

# Spacing (4px base unit)
SPACING_0 = Pt(0)
SPACING_4 = Pt(4)
SPACING_8 = Pt(8)
SPACING_12 = Pt(12)
SPACING_16 = Pt(16)
SPACING_24 = Pt(24)
SPACING_32 = Pt(32)
SPACING_48 = Pt(48)
SPACING_64 = Pt(64)
SPACING_96 = Pt(96)

# Margins
MARGIN_LEFT = Inches(1.0)
MARGIN_RIGHT = Inches(1.0)
MARGIN_TOP = Inches(0.8)
MARGIN_BOTTOM = Inches(0.8)

# Shared defaults (immutable singletons for callable-free parameter defaults)
NO_INDENT = Inches(0)
LINE_THICKNESS_DEFAULT = Pt(1)


@dataclass
class DocumentOutput:
    """Result of document generation."""

    docx_bytes: bytes
    pdf_bytes: Optional[bytes] = None
    filename: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class DocumentGenerator:
    """
    Generates professional resume and cover letter documents.

    Supports:
    - Resume: 1-column professional template with header, summary, skills, experience, education, certifications
    - Cover Letter: 1-column professional template with header, employer address, body paragraphs
    - Output formats: DOCX (python-docx) and PDF (WeasyPrint)
    - Tailoring: Emphasize matching keywords, reorder sections based on job requirements
    """

    def __init__(self, template_dir: Optional[Path] = None) -> None:
        """Initialize the document generator."""
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # Public API
    # =========================================================================

    async def generate_resume(
        self,
        profile: UserProfile,
        job: Optional[Job] = None,
        output_format: str = "docx",
    ) -> DocumentOutput:
        """
        Generate a professional resume.

        Args:
            profile: UserProfile with all resume data
            job: Optional Job to tailor the resume for
            output_format: "docx" or "pdf" or "both"

        Returns:
            DocumentOutput with generated document(s)
        """
        logger.info(f"Generating resume for {profile.full_name}")

        # Tailor profile for job if provided
        tailored_data = self._tailor_profile_for_job(profile, job)

        # Build DOCX
        docx_bytes = await asyncio.to_thread(self._build_resume_docx, tailored_data, profile)

        output = DocumentOutput(
            docx_bytes=docx_bytes,
            filename=f"resume_{profile.full_name.replace(' ', '_')}.docx",
        )

        # Generate PDF if requested
        if output_format in ("pdf", "both"):
            try:
                output.pdf_bytes = await self._docx_to_pdf(docx_bytes)
                output.filename = output.filename.replace(".docx", ".pdf")
            except Exception as e:  # noqa: BLE001
                logger.warning(f"PDF generation failed: {e}")
                output.warnings.append(f"PDF generation failed: {e}")

        return output

    async def generate_cover_letter(
        self,
        profile: UserProfile,
        job: Job,
        output_format: str = "docx",
    ) -> DocumentOutput:
        """
        Generate a professional cover letter tailored to a specific job.

        Args:
            profile: UserProfile with user data
            job: Job to write cover letter for
            output_format: "docx" or "pdf" or "both"

        Returns:
            DocumentOutput with generated document(s)
        """
        logger.info(
            f"Generating cover letter for {profile.full_name} - {job.title} at {job.company}"
        )

        # Tailor content for job
        tailored_data = self._tailor_profile_for_job(profile, job)

        # Build DOCX
        docx_bytes = await asyncio.to_thread(
            self._build_cover_letter_docx, tailored_data, profile, job
        )

        output = DocumentOutput(
            docx_bytes=docx_bytes,
            filename=f"cover_letter_{profile.full_name.replace(' ', '_')}_{job.company.replace(' ', '_')}.docx",
        )

        # Generate PDF if requested
        if output_format in ("pdf", "both"):
            try:
                output.pdf_bytes = await self._docx_to_pdf(docx_bytes)
                output.filename = output.filename.replace(".docx", ".pdf")
            except Exception as e:  # noqa: BLE001
                logger.warning(f"PDF generation failed: {e}")
                output.warnings.append(f"PDF generation failed: {e}")

        return output

    async def generate_both(
        self,
        profile: UserProfile,
        job: Optional[Job] = None,
        output_format: str = "docx",
    ) -> Tuple[DocumentOutput, Optional[DocumentOutput]]:
        """
        Generate both resume and cover letter.

        Args:
            profile: UserProfile with all data
            job: Optional Job for tailoring
            output_format: "docx" or "pdf" or "both"

        Returns:
            Tuple of (resume_output, cover_letter_output)
        """
        resume_output = await self.generate_resume(profile, job, output_format)

        cover_letter_output = None
        if job:
            cover_letter_output = await self.generate_cover_letter(profile, job, output_format)

        return resume_output, cover_letter_output

    # =========================================================================
    # Resume Building
    # =========================================================================

    def _build_resume_docx(self, data: Dict[str, Any], profile: UserProfile) -> bytes:
        """Build resume DOCX document."""
        doc = DocxDocumentClass()

        # Configure page setup
        self._setup_document(doc)

        # Define styles
        self._define_styles(doc)

        # Build sections
        self._build_resume_header(doc, data)
        self._build_professional_summary(doc, data)
        self._build_core_skills(doc, data)
        self._build_experience(doc, data)
        self._build_education(doc, data)
        self._build_certifications(doc, data)

        # Save to bytes
        buffer = io.BytesIO()
        doc.save(buffer)
        return buffer.getvalue()

    def _build_cover_letter_docx(
        self, data: Dict[str, Any], profile: UserProfile, job: Job
    ) -> bytes:
        """Build cover letter DOCX document."""
        doc = DocxDocumentClass()

        # Configure page setup
        self._setup_document(doc)

        # Define styles
        self._define_styles(doc)

        # Build sections
        self._build_cover_letter_header(doc, data)
        self._build_employer_address(doc, job)
        self._build_salutation(doc, job)
        self._build_opening_paragraph(doc, data, job)
        self._build_body_paragraphs(doc, data, job)
        self._build_closing_paragraph(doc, data, job)
        self._build_sign_off(doc, profile)

        # Save to bytes
        buffer = io.BytesIO()
        doc.save(buffer)
        return buffer.getvalue()

    # =========================================================================
    # Document Setup & Styles
    # =========================================================================

    def _setup_document(self, doc: "DocxDocumentType") -> None:
        """Configure document page setup and default formatting."""
        section = doc.sections[0]
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.orientation = WD_ORIENT.PORTRAIT
        section.left_margin = MARGIN_LEFT
        section.right_margin = MARGIN_RIGHT
        section.top_margin = MARGIN_TOP
        section.bottom_margin = MARGIN_BOTTOM

        # Set default font for normal style
        style = doc.styles["Normal"]
        font = style.font
        font.name = FONT_FAMILY
        font.size = FONT_SIZE_BODY
        font.color.rgb = BRAND_NAVY
        style.paragraph_format.space_after = SPACING_8
        style.paragraph_format.line_spacing = 1.15

    def _define_styles(self, doc: "DocxDocumentType") -> None:
        """Define custom styles for the document."""
        # Header Name Style
        self._create_style(
            doc,
            "ResumeName",
            FONT_FAMILY,
            FONT_SIZE_DISPLAY_XL,
            BRAND_NAVY,
            bold=True,
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
        )

        # Header Contact Style
        self._create_style(
            doc,
            "ResumeContact",
            FONT_FAMILY,
            FONT_SIZE_BODY_SM,
            BRAND_GREY_DARK,
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
        )

        # Section Heading Style
        self._create_style(
            doc,
            "SectionHeading",
            FONT_FAMILY,
            FONT_SIZE_TITLE_SM,
            BRAND_NAVY,
            bold=True,
            space_before=SPACING_24,
            space_after=SPACING_12,
        )

        # Subsection Heading Style
        self._create_style(
            doc,
            "SubsectionHeading",
            FONT_FAMILY,
            FONT_SIZE_BODY_LG,
            BRAND_RED,
            bold=True,
            space_before=SPACING_16,
            space_after=SPACING_8,
        )

        # Job Title Style
        self._create_style(
            doc,
            "JobTitle",
            FONT_FAMILY,
            FONT_SIZE_BODY_LG,
            BRAND_NAVY,
            bold=True,
            space_before=SPACING_12,
            space_after=SPACING_4,
        )

        # Company/Date Style
        self._create_style(
            doc, "CompanyDate", FONT_FAMILY, FONT_SIZE_BODY, BRAND_GREY_DARK, space_after=SPACING_4
        )

        # Body Text Style
        self._create_style(
            doc, "ResumeBody", FONT_FAMILY, FONT_SIZE_BODY, BRAND_NAVY, space_after=SPACING_8
        )

        # Bullet Point Style
        self._create_style(
            doc,
            "BulletPoint",
            FONT_FAMILY,
            FONT_SIZE_BODY,
            BRAND_NAVY,
            left_indent=Inches(0.3),
            space_after=SPACING_4,
            bullet=True,
        )

        # Skill Category Style
        self._create_style(
            doc,
            "SkillCategory",
            FONT_FAMILY,
            FONT_SIZE_BODY_SM,
            BRAND_RED,
            bold=True,
            space_after=SPACING_4,
        )

        # Skill Item Style
        self._create_style(
            doc, "SkillItem", FONT_FAMILY, FONT_SIZE_BODY_SM, BRAND_NAVY, space_after=SPACING_4
        )

    def _create_style(
        self,
        doc: "DocxDocumentType",
        name: str,
        font_name: str,
        font_size: Pt,
        color: RGBColor,
        bold: bool = False,
        italic: bool = False,
        alignment: int = WD_ALIGN_PARAGRAPH.LEFT,
        space_before: Pt = SPACING_0,
        space_after: Pt = SPACING_0,
        left_indent: Inches = NO_INDENT,
        bullet: bool = False,
    ) -> None:
        """Create or update a paragraph style."""
        try:
            style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        except ValueError:
            style = doc.styles[name]

        font = style.font
        font.name = font_name
        font.size = font_size
        font.color.rgb = color
        font.bold = bold
        font.italic = italic

        pf = style.paragraph_format
        pf.alignment = alignment
        pf.space_before = space_before
        pf.space_after = space_after
        pf.left_indent = left_indent
        pf.line_spacing = 1.15

    # =========================================================================
    # Resume Sections
    # =========================================================================

    def _build_resume_header(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build resume header with name and contact info."""
        # Name
        name_para = doc.add_paragraph(data.get("full_name", ""), style="ResumeName")
        name_para.paragraph_format.space_after = SPACING_8

        # Contact info line
        contact_parts = []
        if data.get("phone"):
            contact_parts.append(data["phone"])
        if data.get("location"):
            contact_parts.append(data["location"])
        if data.get("email"):
            contact_parts.append(data["email"])
        if data.get("linkedin_url"):
            contact_parts.append("LinkedIn")
        if data.get("github_url"):
            contact_parts.append("GitHub")
        if data.get("portfolio_url"):
            contact_parts.append("Portfolio")

        contact_text = "  |  ".join(contact_parts)
        contact_para = doc.add_paragraph(contact_text, style="ResumeContact")
        contact_para.paragraph_format.space_after = SPACING_24

        # Add a subtle line
        self._add_horizontal_line(doc, BRAND_RED, thickness=Pt(2))

    def _build_professional_summary(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build professional summary section."""
        summary = data.get("summary", "")
        if not summary:
            return

        doc.add_paragraph("PROFESSIONAL SUMMARY", style="SectionHeading")
        doc.add_paragraph(summary, style="ResumeBody")

    def _build_core_skills(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build core skills section with categorized skills."""
        skills = data.get("skills", [])
        if not skills:
            return

        doc.add_paragraph("CORE SKILLS", style="SectionHeading")

        # Group skills by category
        categories: Dict[str, List[str]] = {}
        for skill in skills:
            category = skill.get("category", "Technical") or "Technical"
            if category not in categories:
                categories[category] = []
            skill_name = skill.get("name", "")
            level = skill.get("level")
            if level:
                skill_name = f"{skill_name} ({level})"
            categories[category].append(skill_name)

        # Add each category
        for category, skill_list in sorted(categories.items()):
            doc.add_paragraph(category.upper(), style="SkillCategory")
            skills_text = "  •  ".join(skill_list)
            doc.add_paragraph(skills_text, style="SkillItem")

    def _build_experience(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build experience section in reverse chronological order."""
        experiences = data.get("experience", [])
        if not experiences:
            return

        doc.add_paragraph("PROFESSIONAL EXPERIENCE", style="SectionHeading")

        # Sort by start_date descending (most recent first)
        sorted_exps = sorted(
            experiences, key=lambda x: x.get("start_date", datetime.min), reverse=True
        )

        for exp in sorted_exps:
            self._add_experience_entry(doc, exp)

    def _add_experience_entry(self, doc: "DocxDocumentType", exp: Dict[str, Any]) -> None:
        """Add a single experience entry."""
        title = exp.get("title", "")
        company = exp.get("company", "")
        location = exp.get("location", "")
        start_date = exp.get("start_date")
        end_date = exp.get("end_date")
        current = exp.get("current", False)
        description = exp.get("description", "")
        achievements = exp.get("achievements", [])

        # Title and company
        title_text = f"{title}"
        if company:
            title_text += f"  |  {company}"
        if location:
            title_text += f"  |  {location}"

        doc.add_paragraph(title_text, style="JobTitle")

        # Date range
        date_str = self._format_date_range(start_date, end_date, current)
        if date_str:
            doc.add_paragraph(date_str, style="CompanyDate")

        # Description
        if description:
            doc.add_paragraph(description, style="ResumeBody")

        # Achievements as bullets
        for achievement in achievements:
            if achievement:
                bullet = doc.add_paragraph(style="BulletPoint")
                bullet.text = achievement

    def _build_education(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build education section."""
        education = data.get("education", [])
        if not education:
            return

        doc.add_paragraph("EDUCATION", style="SectionHeading")

        for edu in education:
            institution = edu.get("institution", "")
            degree = edu.get("degree", "")
            field = edu.get("field_of_study", "")
            location = edu.get("location", "")
            start_date = edu.get("start_date")
            end_date = edu.get("end_date")
            gpa = edu.get("gpa")
            honors = edu.get("honors", [])

            # Institution and degree
            edu_text = institution
            if degree or field:
                parts = []
                if degree:
                    parts.append(degree)
                if field:
                    parts.append(field)
                edu_text += f"  —  {', '.join(parts)}"

            doc.add_paragraph(edu_text, style="JobTitle")

            # Details
            details = []
            if location:
                details.append(location)
            date_str = self._format_date_range(start_date, end_date, False)
            if date_str:
                details.append(date_str)
            if gpa:
                details.append(f"GPA: {gpa}")
            if honors:
                details.append(f"Honors: {', '.join(honors)}")

            if details:
                doc.add_paragraph("  |  ".join(details), style="CompanyDate")

    def _build_certifications(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build certifications section."""
        certifications = data.get("certifications", [])
        if not certifications:
            return

        doc.add_paragraph("CERTIFICATIONS", style="SectionHeading")

        for cert in certifications:
            if cert:
                bullet = doc.add_paragraph(style="BulletPoint")
                bullet.text = cert

    # =========================================================================
    # Cover Letter Sections
    # =========================================================================

    def _build_cover_letter_header(self, doc: "DocxDocumentType", data: Dict[str, Any]) -> None:
        """Build cover letter header matching resume."""
        # Name
        name_para = doc.add_paragraph(data.get("full_name", ""), style="ResumeName")
        name_para.paragraph_format.space_after = SPACING_4

        # Contact info
        contact_parts = []
        if data.get("phone"):
            contact_parts.append(data["phone"])
        if data.get("email"):
            contact_parts.append(data["email"])
        if data.get("location"):
            contact_parts.append(data["location"])
        if data.get("linkedin_url"):
            contact_parts.append("LinkedIn")

        contact_text = "  |  ".join(contact_parts)
        contact_para = doc.add_paragraph(contact_text, style="ResumeContact")
        contact_para.paragraph_format.space_after = SPACING_24

        # Horizontal line
        self._add_horizontal_line(doc, BRAND_RED, thickness=Pt(2))

    def _build_employer_address(self, doc: "DocxDocumentType", job: Job) -> None:
        """Build employer address block."""
        lines = []
        lines.append(job.company)
        if job.location:
            lines.append(job.location)

        for line in lines:
            para = doc.add_paragraph(line, style="ResumeBody")
            para.paragraph_format.space_after = SPACING_4

        # Date
        date_para = doc.add_paragraph(datetime.now().strftime("%B %d, %Y"), style="ResumeBody")
        date_para.paragraph_format.space_after = SPACING_24

    def _build_salutation(self, doc: "DocxDocumentType", job: Job) -> None:
        """Build salutation."""
        contact = job.contact_person or "Hiring Manager"
        salutation = f"Dear {contact},"
        para = doc.add_paragraph(salutation, style="ResumeBody")
        para.paragraph_format.space_after = SPACING_16

    def _build_opening_paragraph(
        self, doc: "DocxDocumentType", data: Dict[str, Any], job: Job
    ) -> None:
        """Build opening paragraph - position, company, hook."""
        headline = data.get("headline", "")
        summary = data.get("summary", "")

        # Hook from headline or summary
        hook = headline or (summary[:200] + "..." if len(summary) > 200 else summary)

        text = (
            f"I am writing to express my strong interest in the {job.title} position at "
            f"{job.company}. {hook}"
        )

        para = doc.add_paragraph(text, style="ResumeBody")
        para.paragraph_format.space_after = SPACING_16

    def _build_body_paragraphs(
        self, doc: "DocxDocumentType", data: Dict[str, Any], job: Job
    ) -> None:
        """Build body paragraphs matching skills to job requirements."""
        # Match skills to job requirements
        matched_skills = self._match_skills_to_job(data.get("skills", []), job)
        experiences = data.get("experience", [])

        # Paragraph 1: Key qualifications matching job
        if matched_skills:
            skills_text = ", ".join(matched_skills[:5])
            text = (
                f"My background aligns well with the requirements you've outlined. "
                f"In particular, my expertise in {skills_text} directly supports "
                f"the core needs of this role."
            )
            doc.add_paragraph(text, style="ResumeBody").paragraph_format.space_after = SPACING_12

        # Paragraph 2: Relevant experience highlights
        if experiences:
            # Get most relevant experience
            top_exp = experiences[0] if experiences else None
            if top_exp:
                title = top_exp.get("title", "")
                company = top_exp.get("company", "")
                achievements = top_exp.get("achievements", [])

                text = f"In my recent role as {title} at {company}, "
                if achievements:
                    text += f"I {achievements[0].lower()}. "
                text += (
                    f"This experience has prepared me to contribute immediately to "
                    f"{job.company}'s objectives."
                )
                doc.add_paragraph(
                    text, style="ResumeBody"
                ).paragraph_format.space_after = SPACING_12

        # Paragraph 3: Cultural fit / company knowledge
        if job.company_industry:
            text = (
                f"I have long admired {job.company}'s work in {job.company_industry} "
                f"and would welcome the opportunity to bring my skills to your team. "
                f"The values and mission of {job.company} resonate with my professional "
                f"philosophy of delivering impactful results through collaboration and innovation."
            )
            doc.add_paragraph(text, style="ResumeBody").paragraph_format.space_after = SPACING_16

    def _build_closing_paragraph(
        self, doc: "DocxDocumentType", data: Dict[str, Any], job: Job
    ) -> None:
        """Build closing paragraph with call to action."""
        text = (
            f"I would welcome the opportunity to discuss how my experience and skills "
            f"can contribute to {job.company}'s continued success. "
            f"Thank you for your time and consideration—I look forward to speaking with you."
        )
        para = doc.add_paragraph(text, style="ResumeBody")
        para.paragraph_format.space_after = SPACING_24

    def _build_sign_off(self, doc: "DocxDocumentType", profile: UserProfile) -> None:
        """Build professional sign-off."""
        doc.add_paragraph(
            "Sincerely,", style="ResumeBody"
        ).paragraph_format.space_after = SPACING_32
        doc.add_paragraph(profile.full_name, style="ResumeBody")

    # =========================================================================
    # Tailoring Logic
    # =========================================================================

    def _tailor_profile_for_job(self, profile: UserProfile, job: Optional[Job]) -> Dict[str, Any]:
        """
        Tailor profile data for a specific job.

        - Reorders skills to emphasize matching keywords
        - Highlights relevant experience
        - Adjusts summary to match job language
        """
        data: Dict[str, Any] = {
            "full_name": profile.full_name,
            "phone": profile.phone,
            "location": profile.location,
            "email": profile.email,
            "linkedin_url": str(profile.linkedin_url) if profile.linkedin_url else None,
            "github_url": str(profile.github_url) if profile.github_url else None,
            "portfolio_url": str(profile.portfolio_url) if profile.portfolio_url else None,
            "headline": profile.headline,
            "summary": profile.summary,
            "skills": [self._skill_to_dict(s) for s in profile.skills],
            "experience": [self._experience_to_dict(e) for e in profile.experience],
            "education": [self._education_to_dict(e) for e in profile.education],
            "certifications": profile.certifications,
            "languages": profile.languages,
        }

        if not job:
            return data

        # Extract job keywords
        job_keywords = set(kw.lower() for kw in job.keywords)
        job_requirements = [r.lower() for r in job.requirements]

        # Reorder skills: matching skills first
        skills = data["skills"]
        for skill in skills:
            skill_name_lower = skill["name"].lower()
            skill["_match_score"] = 0
            if skill_name_lower in job_keywords:
                skill["_match_score"] = 3
            elif any(kw in skill_name_lower for kw in job_keywords):
                skill["_match_score"] = 2
            elif any(skill_name_lower in req for req in job_requirements):
                skill["_match_score"] = 1

        skills.sort(key=lambda s: s.get("_match_score", 0), reverse=True)

        # Reorder experience: most relevant first
        experiences = data["experience"]
        for exp in experiences:
            exp["_match_score"] = 0
            exp_text = f"{exp.get('title', '')} {exp.get('description', '')} {' '.join(exp.get('skills_used', []))}".lower()
            for kw in job_keywords:
                if kw in exp_text:
                    exp["_match_score"] += 1

        experiences.sort(key=lambda e: e.get("_match_score", 0), reverse=True)

        # Adjust summary if we have a good match
        if matched_skills := [s["name"] for s in skills if s.get("_match_score", 0) > 0]:
            top_matches = matched_skills[:3]
            data["summary"] = (
                f"{profile.summary} Key strengths for this role include: {', '.join(top_matches)}."
            ).strip()

        return data

    def _match_skills_to_job(self, skills: List[Dict[str, Any]], job: Job) -> List[str]:
        """Find skills that match job requirements."""
        job_keywords = set(kw.lower() for kw in job.keywords)
        job_requirements = [r.lower() for r in job.requirements]

        matched = []
        for skill in skills:
            skill_name = skill.get("name", "").lower()
            if (
                skill_name in job_keywords
                or any(kw in skill_name for kw in job_keywords)
                or any(skill_name in req for req in job_requirements)
            ):
                matched.append(skill["name"])

        return matched

    # =========================================================================
    # Conversion Helpers
    # =========================================================================

    def _skill_to_dict(self, skill: Skill) -> Dict[str, Any]:
        """Convert Skill model to dict."""
        return {
            "name": skill.name,
            "level": skill.level,
            "years_experience": skill.years_experience,
            "category": skill.category,
        }

    def _experience_to_dict(self, exp: Experience) -> Dict[str, Any]:
        """Convert Experience model to dict."""
        return {
            "title": exp.title,
            "company": exp.company,
            "location": exp.location,
            "start_date": exp.start_date,
            "end_date": exp.end_date,
            "current": exp.current,
            "description": exp.description,
            "achievements": exp.achievements,
            "skills_used": exp.skills_used,
        }

    def _education_to_dict(self, edu: Education) -> Dict[str, Any]:
        """Convert Education model to dict."""
        return {
            "institution": edu.institution,
            "degree": edu.degree,
            "field_of_study": edu.field_of_study,
            "location": edu.location,
            "start_date": edu.start_date,
            "end_date": edu.end_date,
            "gpa": edu.gpa,
            "honors": edu.honors,
        }

    def _format_date_range(
        self, start: Optional[datetime], end: Optional[datetime], current: bool
    ) -> str:
        """Format date range for display."""
        parts = []

        if start:
            parts.append(start.strftime("%b %Y"))

        if current:
            parts.append("Present")
        elif end:
            parts.append(end.strftime("%b %Y"))

        return " — ".join(parts) if parts else ""

    def _add_horizontal_line(
        self, doc: "DocxDocumentType", color: RGBColor, thickness: Pt = LINE_THICKNESS_DEFAULT
    ) -> None:
        """Add a horizontal line to the document."""
        para = doc.add_paragraph()
        para.paragraph_format.space_before = SPACING_8
        para.paragraph_format.space_after = SPACING_8

        # Add bottom border to paragraph
        pPr = para._p.get_or_add_pPr()
        pBdr = pPr.makeelement(qn("w:pBdr"), {})
        bottom = pBdr.makeelement(
            qn("w:bottom"),
            {
                qn("w:val"): "single",
                qn("w:sz"): str(int(thickness * 8)),  # Convert Pt to eighths of a point
                qn("w:space"): "1",
                qn("w:color"): f"{color[0]:02X}{color[1]:02X}{color[2]:02X}",
            },
        )
        pBdr.append(bottom)
        pPr.append(pBdr)

    # =========================================================================
    # PDF Generation
    # =========================================================================

    async def _docx_to_pdf(self, docx_bytes: bytes) -> bytes:
        """
        Convert DOCX to PDF using WeasyPrint.

        Note: This requires WeasyPrint and its dependencies to be installed.
        For production, consider using LibreOffice headless conversion for better fidelity.
        """
        try:
            from weasyprint import CSS, HTML
        except ImportError as e:
            raise RuntimeError(f"PDF generation requires weasyprint: {e}") from e

        # Convert DOCX to HTML
        html_content = await asyncio.to_thread(self._docx_to_html, docx_bytes)

        # Add print CSS
        print_css = CSS(string=self._get_print_css())

        # Generate PDF
        html_doc = HTML(string=html_content)
        pdf_buffer = io.BytesIO()
        await asyncio.to_thread(html_doc.write_pdf, pdf_buffer, stylesheets=[print_css])

        return pdf_buffer.getvalue()

    def _docx_to_html(self, docx_bytes: bytes) -> str:
        """Convert DOCX bytes to HTML string."""
        # Use a simple conversion approach
        # In production, use mammoth or docx2html for better fidelity
        doc = DocxDocumentClass(io.BytesIO(docx_bytes))

        html_parts = ['<html><head><meta charset="utf-8"></head><body>']

        for para in doc.paragraphs:
            style_name = para.style.name if para.style else "Normal"
            text = para.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            if not text.strip():
                html_parts.append("<br>")
                continue

            # Map styles to HTML tags
            if "Heading" in style_name or "SectionHeading" in style_name:
                html_parts.append(
                    f'<h2 style="color:#070A40; margin-top:24pt; margin-bottom:12pt;">{text}</h2>'
                )
            elif "JobTitle" in style_name:
                html_parts.append(
                    f'<h3 style="color:#070A40; margin-top:12pt; margin-bottom:4pt;">{text}</h3>'
                )
            elif "CompanyDate" in style_name:
                html_parts.append(f'<p style="color:#6B7280; margin-bottom:4pt;">{text}</p>')
            elif "BulletPoint" in style_name:
                html_parts.append(f'<li style="margin-left:30px; margin-bottom:4pt;">{text}</li>')
            elif "SkillCategory" in style_name:
                html_parts.append(
                    f'<p style="color:#E63946; font-weight:bold; margin-bottom:4pt;">{text}</p>'
                )
            elif "ResumeName" in style_name:
                html_parts.append(
                    f'<h1 style="color:#070A40; text-align:center; margin-bottom:8pt;">{text}</h1>'
                )
            elif "ResumeContact" in style_name:
                html_parts.append(
                    f'<p style="color:#6B7280; text-align:center; margin-bottom:24pt;">{text}</p>'
                )
            else:
                html_parts.append(f'<p style="margin-bottom:8pt; line-height:1.15;">{text}</p>')

        html_parts.append("</body></html>")
        return "".join(html_parts)

    def _get_print_css(self) -> str:
        """Get CSS for PDF printing."""
        return f"""
        @page {{
            size: letter;
            margin: 0.8in 1in 0.8in 1in;
            @bottom-center {{
                content: counter(page);
                font-family: {FONT_FAMILY};
                font-size: 10pt;
                color: #6B7280;
            }}
        }}
        body {{
            font-family: {FONT_FAMILY}, sans-serif;
            font-size: 14pt;
            line-height: 1.15;
            color: #070A40;
        }}
        h1, h2, h3 {{
            font-family: {FONT_FAMILY}, sans-serif;
            font-weight: 700;
            color: #070A40;
        }}
        h2 {{
            border-bottom: 2px solid #E63946;
            padding-bottom: 4pt;
        }}
        ul {{ margin: 0; padding-left: 20px; }}
        li {{ margin-bottom: 4pt; }}
        """


# =========================================================================
# Convenience Functions
# =========================================================================


async def generate_resume(
    profile: UserProfile,
    job: Optional[Job] = None,
    output_format: str = "docx",
    template_dir: Optional[Path] = None,
) -> DocumentOutput:
    """Convenience function to generate a resume."""
    generator = DocumentGenerator(template_dir)
    return await generator.generate_resume(profile, job, output_format)


async def generate_cover_letter(
    profile: UserProfile,
    job: Job,
    output_format: str = "docx",
    template_dir: Optional[Path] = None,
) -> DocumentOutput:
    """Convenience function to generate a cover letter."""
    generator = DocumentGenerator(template_dir)
    return await generator.generate_cover_letter(profile, job, output_format)


async def generate_application_package(
    profile: UserProfile,
    job: Job,
    output_format: str = "docx",
    template_dir: Optional[Path] = None,
) -> Tuple[DocumentOutput, Optional[DocumentOutput]]:
    """Generate both resume and cover letter for a job application."""
    generator = DocumentGenerator(template_dir)
    return await generator.generate_both(profile, job, output_format)


# =========================================================================
# Template File Creation (for reference/base templates)
# =========================================================================


def create_base_templates(template_dir: Optional[Path] = None) -> None:
    """Create base template files for reference."""
    if template_dir is None:
        template_dir = Path(__file__).parent / "templates"
    template_dir = Path(template_dir)
    template_dir.mkdir(parents=True, exist_ok=True)

    # The templates are generated programmatically, but we can create
    # placeholder .docx files that serve as visual references
    _create_resume_template_docx(template_dir / "resume_template.docx")
    _create_cover_letter_template_docx(template_dir / "cover_letter_template.docx")


def _create_resume_template_docx(path: Path) -> None:
    """Create a base resume template DOCX for reference."""
    doc = DocxDocumentClass()
    _setup_template_doc(doc)
    _define_template_styles(doc)

    # Header
    doc.add_paragraph("[FULL NAME]", style="TemplateName")
    doc.add_paragraph(
        "[Phone]  |  [Location]  |  [Email]  |  [LinkedIn]  |  [GitHub]", style="TemplateContact"
    )

    # Horizontal rule
    _add_template_line(doc)

    # Professional Summary
    doc.add_paragraph("PROFESSIONAL SUMMARY", style="TemplateSectionHeading")
    doc.add_paragraph("[Your professional summary here...]", style="TemplateBody")

    # Core Skills
    doc.add_paragraph("CORE SKILLS", style="TemplateSectionHeading")
    doc.add_paragraph("TECHNICAL", style="TemplateSkillCategory")
    doc.add_paragraph(
        "[Skill 1]  •  [Skill 2]  •  [Skill 3]  •  [Skill 4]", style="TemplateSkillItem"
    )
    doc.add_paragraph("TOOLS & PLATFORMS", style="TemplateSkillCategory")
    doc.add_paragraph("[Tool 1]  •  [Tool 2]  •  [Tool 3]", style="TemplateSkillItem")

    # Experience
    doc.add_paragraph("PROFESSIONAL EXPERIENCE", style="TemplateSectionHeading")
    doc.add_paragraph("[Job Title]  |  [Company]  |  [Location]", style="TemplateJobTitle")
    doc.add_paragraph("[Month Year] — [Month Year / Present]", style="TemplateCompanyDate")
    doc.add_paragraph("[Role description...]", style="TemplateBody")
    bullet = doc.add_paragraph(style="TemplateBullet")
    bullet.text = "[Key achievement with metrics]"
    bullet = doc.add_paragraph(style="TemplateBullet")
    bullet.text = "[Another quantified achievement]"

    doc.add_paragraph("[Previous Job Title]  |  [Company]  |  [Location]", style="TemplateJobTitle")
    doc.add_paragraph("[Month Year] — [Month Year]", style="TemplateCompanyDate")
    doc.add_paragraph("[Role description...]", style="TemplateBody")
    bullet = doc.add_paragraph(style="TemplateBullet")
    bullet.text = "[Key achievement]"

    # Education
    doc.add_paragraph("EDUCATION", style="TemplateSectionHeading")
    doc.add_paragraph("[Degree], [Field of Study]", style="TemplateJobTitle")
    doc.add_paragraph(
        "[Institution]  |  [Location]  |  [Graduation Year]", style="TemplateCompanyDate"
    )

    # Certifications
    doc.add_paragraph("CERTIFICATIONS", style="TemplateSectionHeading")
    bullet = doc.add_paragraph(style="TemplateBullet")
    bullet.text = "[Certification Name]"

    doc.save(str(path))
    logger.info(f"Created resume template at {path}")


def _create_cover_letter_template_docx(path: Path) -> None:
    """Create a base cover letter template DOCX for reference."""
    doc = DocxDocumentClass()
    _setup_template_doc(doc)
    _define_template_styles(doc)

    # Header
    doc.add_paragraph("[YOUR FULL NAME]", style="TemplateName")
    doc.add_paragraph("[Phone]  |  [Email]  |  [Location]  |  [LinkedIn]", style="TemplateContact")
    _add_template_line(doc)

    # Date
    doc.add_paragraph("[Month Day, Year]", style="TemplateBody")
    doc.add_paragraph("", style="TemplateBody")  # spacer

    # Employer Address
    doc.add_paragraph("[Hiring Manager Name]", style="TemplateBody")
    doc.add_paragraph("[Company Name]", style="TemplateBody")
    doc.add_paragraph("[Company Address]", style="TemplateBody")
    doc.add_paragraph("", style="TemplateBody")

    # Salutation
    doc.add_paragraph("Dear [Hiring Manager Name],", style="TemplateBody")
    doc.add_paragraph("", style="TemplateBody")

    # Opening
    doc.add_paragraph(
        "I am writing to express my strong interest in the [Position Title] role at [Company Name]. "
        "[Brief hook connecting your background to the role.]",
        style="TemplateBody",
    )
    doc.add_paragraph("", style="TemplateBody")

    # Body paragraph 1 - Skills match
    doc.add_paragraph(
        "My background aligns well with the requirements you've outlined. In particular, "
        "my expertise in [Skill 1], [Skill 2], and [Skill 3] directly supports the core needs of this role.",
        style="TemplateBody",
    )
    doc.add_paragraph("", style="TemplateBody")

    # Body paragraph 2 - Experience
    doc.add_paragraph(
        "In my recent role as [Current Title] at [Current Company], I [key achievement]. "
        "This experience has prepared me to contribute immediately to [Company Name]'s objectives.",
        style="TemplateBody",
    )
    doc.add_paragraph("", style="TemplateBody")

    # Body paragraph 3 - Company fit
    doc.add_paragraph(
        "I have long admired [Company Name]'s work in [industry/field] and would welcome "
        "the opportunity to bring my skills to your team.",
        style="TemplateBody",
    )
    doc.add_paragraph("", style="TemplateBody")

    # Closing
    doc.add_paragraph(
        "I would welcome the opportunity to discuss how my experience and skills can contribute "
        "to [Company Name]'s continued success. Thank you for your time and consideration—I look "
        "forward to speaking with you.",
        style="TemplateBody",
    )
    doc.add_paragraph("", style="TemplateBody")

    # Sign-off
    doc.add_paragraph("Sincerely,", style="TemplateBody")
    doc.add_paragraph("", style="TemplateBody")
    doc.add_paragraph("[Your Full Name]", style="TemplateBody")

    doc.save(str(path))
    logger.info(f"Created cover letter template at {path}")


def _setup_template_doc(doc: "DocxDocumentType") -> None:
    """Setup template document."""
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.left_margin = MARGIN_LEFT
    section.right_margin = MARGIN_RIGHT
    section.top_margin = MARGIN_TOP
    section.bottom_margin = MARGIN_BOTTOM


def _define_template_styles(doc: "DocxDocumentType") -> None:
    """Define template styles."""
    styles_config: List[Tuple[Any, ...]] = [
        (
            "TemplateName",
            FONT_SIZE_DISPLAY_XL,
            BRAND_NAVY,
            True,
            WD_ALIGN_PARAGRAPH.CENTER,
            SPACING_4,
        ),
        (
            "TemplateContact",
            FONT_SIZE_BODY_SM,
            BRAND_GREY_DARK,
            False,
            WD_ALIGN_PARAGRAPH.CENTER,
            SPACING_24,
        ),
        (
            "TemplateSectionHeading",
            FONT_SIZE_TITLE_SM,
            BRAND_NAVY,
            True,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_24,
            SPACING_12,
        ),
        (
            "TemplateJobTitle",
            FONT_SIZE_BODY_LG,
            BRAND_NAVY,
            True,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_12,
            SPACING_4,
        ),
        (
            "TemplateCompanyDate",
            FONT_SIZE_BODY,
            BRAND_GREY_DARK,
            False,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_0,
            SPACING_4,
        ),
        (
            "TemplateBody",
            FONT_SIZE_BODY,
            BRAND_NAVY,
            False,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_0,
            SPACING_8,
        ),
        (
            "TemplateSkillCategory",
            FONT_SIZE_BODY_SM,
            BRAND_RED,
            True,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_12,
            SPACING_4,
        ),
        (
            "TemplateSkillItem",
            FONT_SIZE_BODY_SM,
            BRAND_NAVY,
            False,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_0,
            SPACING_8,
        ),
        (
            "TemplateBullet",
            FONT_SIZE_BODY,
            BRAND_NAVY,
            False,
            WD_ALIGN_PARAGRAPH.LEFT,
            SPACING_0,
            SPACING_4,
            Inches(0.3),
        ),
    ]

    for config in styles_config:
        name = config[0]
        font_size = config[1]
        color = config[2]
        bold = config[3]
        alignment = config[4]
        space_before = config[5] if len(config) > 5 else Pt(0)
        space_after = config[6] if len(config) > 6 else Pt(0)
        left_indent = config[7] if len(config) > 7 else Inches(0)

        _create_template_style(
            doc, name, font_size, color, bold, alignment, space_before, space_after, left_indent
        )


def _create_template_style(
    doc: "DocxDocumentType",
    name: str,
    font_size: Pt,
    color: RGBColor,
    bold: bool,
    alignment: int,
    space_before: Pt,
    space_after: Pt,
    left_indent: Inches,
) -> None:
    """Create a template style."""
    try:
        style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    except ValueError:
        style = doc.styles[name]

    font = style.font
    font.name = FONT_FAMILY
    font.size = font_size
    font.color.rgb = color
    font.bold = bold

    pf = style.paragraph_format
    pf.alignment = alignment
    pf.space_before = space_before
    pf.space_after = space_after
    pf.left_indent = left_indent
    pf.line_spacing = 1.15


def _add_template_line(doc: "DocxDocumentType") -> None:
    """Add horizontal line to template."""
    para = doc.add_paragraph()
    para.paragraph_format.space_before = SPACING_8
    para.paragraph_format.space_after = SPACING_8

    pPr = para._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn("w:pBdr"), {})
    bottom = pBdr.makeelement(
        qn("w:bottom"),
        {
            qn("w:val"): "single",
            qn("w:sz"): "16",  # 2pt
            qn("w:space"): "1",
            qn("w:color"): f"{BRAND_RED[0]:02X}{BRAND_RED[1]:02X}{BRAND_RED[2]:02X}",
        },
    )
    pBdr.append(bottom)
    pPr.append(pBdr)


# =========================================================================
# Module Exports
# =========================================================================

__all__ = [
    "DocumentGenerator",
    "DocumentOutput",
    "generate_resume",
    "generate_cover_letter",
    "generate_application_package",
    "create_base_templates",
    # Brand constants
    "BRAND_NAVY",
    "BRAND_RED",
    "BRAND_CYAN",
    "BRAND_GREY_LIGHT",
    "BRAND_WHITE",
    "BRAND_GREY_DARK",
    "FONT_FAMILY",
]
