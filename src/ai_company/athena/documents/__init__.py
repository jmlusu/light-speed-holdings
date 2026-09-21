"""Athena document parsing, humanization, and generation module."""

from .generator import (
    BRAND_CYAN,
    BRAND_GREY_DARK,
    BRAND_GREY_LIGHT,
    BRAND_NAVY,
    BRAND_RED,
    BRAND_WHITE,
    FONT_FAMILY,
    DocumentGenerator,
    DocumentOutput,
    create_base_templates,
    generate_application_package,
    generate_cover_letter,
    generate_resume,
)
from .humanizer import (
    HumanizationIntensity,
    HumanizationResult,
    Humanizer,
    create_humanizer,
)
from .parser import (
    DocumentParser,
    DOCXParser,
    ParsedSection,
    ParseResult,
    PDFParser,
    ResumeParser,
    parse_resume,
)

__all__ = [
    "ResumeParser",
    "DocumentParser",
    "PDFParser",
    "DOCXParser",
    "ParseResult",
    "ParsedSection",
    "parse_resume",
    "Humanizer",
    "HumanizationIntensity",
    "HumanizationResult",
    "create_humanizer",
    "DocumentGenerator",
    "DocumentOutput",
    "generate_resume",
    "generate_cover_letter",
    "generate_application_package",
    "create_base_templates",
    "BRAND_NAVY",
    "BRAND_RED",
    "BRAND_CYAN",
    "BRAND_GREY_LIGHT",
    "BRAND_WHITE",
    "BRAND_GREY_DARK",
    "FONT_FAMILY",
]
