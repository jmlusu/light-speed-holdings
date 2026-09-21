"""Smart form field detection and filling for ATS platforms.

Provides heuristic-based field identification using label text, input name,
aria-label, placeholder, and platform-specific selectors for major ATS platforms.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional, cast

try:
    from playwright.async_api import Page
except ImportError:  # pragma: no cover - playwright is an optional e2e dependency
    # Only referenced in lazy annotations (see `from __future__ import annotations`).
    Page = Any  # noqa: F811

from ..models.jobs import UserProfile
from .browser import AthenaBrowser

logger = logging.getLogger(__name__)


class ATSPlatform(str, Enum):
    """Supported ATS platforms."""

    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    WORKDAY = "workday"
    ICIM = "icims"
    SMARTRECRUITERS = "smartrecruiters"
    BAMBOOHR = "bamboohr"
    UNKNOWN = "unknown"


@dataclass
class FieldMapping:
    """Maps a user profile field to a form input."""

    profile_field: str  # e.g., "full_name", "email", "phone"
    selectors: list[str]  # CSS selectors to try in order
    field_type: str  # text, email, tel, textarea, select, radio, checkbox, file
    required: bool = False
    transform: Optional[str] = None  # Optional transform function name
    platform_specific: dict[ATSPlatform, list[str]] = field(default_factory=dict)


@dataclass
class FormField:
    """Represents a detected form field."""

    selector: str
    field_type: str
    label: str = ""
    name: str = ""
    placeholder: str = ""
    aria_label: str = ""
    required: bool = False
    options: list[str] = field(default_factory=list)  # For select/radio
    is_file_input: bool = False
    confidence: float = 0.0  # 0-1 confidence score
    profile_field: Optional[str] = None  # matched user-profile field (e.g. "email")


class FormFiller:
    """Smart form filler for ATS platforms."""

    # Common field patterns for heuristic matching
    FIELD_PATTERNS = {
        "full_name": [
            r"(full\s*name|name)",
            r"(first\s*name|last\s*name)",
            r"(given\s*name|family\s*name)",
        ],
        "first_name": [r"first\s*name", r"given\s*name", r"fname"],
        "last_name": [r"last\s*name", r"family\s*name", r"surname", r"lname"],
        "email": [r"email", r"e-?mail"],
        "phone": [r"phone", r"telephone", r"mobile", r"cell"],
        "location": [r"(address|location|city|state|zip|postal|country)"],
        "linkedin": [r"linkedin", r"linked\s*in"],
        "portfolio": [r"(portfolio|website|personal\s*site)"],
        "github": [r"github", r"git\s*hub"],
        "resume": [r"(resume|cv|curriculum\s*vitae)"],
        "cover_letter": [r"(cover\s*letter|coverletter|motivation)"],
        "summary": [r"(summary|objective|about\s*me|profile)"],
        "experience_years": [r"(years?\s*(of\s*)?experience|experience\s*years?)"],
        "salary_expectation": [r"(salary|compensation|expected|desired)\s*(range|expectation)?"],
        "visa_sponsorship": [r"(visa|sponsor|work\s*authoriz)"],
        "referral": [r"(referral|referred\s*by|how\s*did\s*you\s*hear)"],
    }

    # Platform-specific field mappings
    PLATFORM_MAPPINGS: dict[ATSPlatform, list[FieldMapping]] = {
        ATSPlatform.GREENHOUSE: [
            FieldMapping(
                profile_field="first_name",
                selectors=[
                    "#first_name",
                    "input[name='first_name']",
                    "input[placeholder*='First']",
                ],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="last_name",
                selectors=["#last_name", "input[name='last_name']", "input[placeholder*='Last']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="email",
                selectors=["#email", "input[name='email']", "input[type='email']"],
                field_type="email",
                required=True,
            ),
            FieldMapping(
                profile_field="phone",
                selectors=["#phone", "input[name='phone']", "input[placeholder*='Phone']"],
                field_type="tel",
            ),
            FieldMapping(
                profile_field="linkedin",
                selectors=["#linkedin", "input[name='linkedin']", "input[placeholder*='LinkedIn']"],
                field_type="url",
            ),
            FieldMapping(
                profile_field="github",
                selectors=["#github", "input[name='github']", "input[placeholder*='GitHub']"],
                field_type="url",
            ),
            FieldMapping(
                profile_field="portfolio",
                selectors=[
                    "#portfolio",
                    "input[name='portfolio']",
                    "input[placeholder*='Portfolio']",
                ],
                field_type="url",
            ),
            FieldMapping(
                profile_field="resume",
                selectors=["#resume", "input[name='resume']", "input[type='file'][accept*='pdf']"],
                field_type="file",
                required=True,
            ),
            FieldMapping(
                profile_field="cover_letter",
                selectors=[
                    "#cover_letter",
                    "input[name='cover_letter']",
                    "input[type='file'][accept*='pdf']",
                ],
                field_type="file",
            ),
            FieldMapping(
                profile_field="location",
                selectors=["#location", "input[name='location']", "input[placeholder*='Location']"],
                field_type="text",
            ),
            FieldMapping(
                profile_field="visa_sponsorship",
                selectors=["input[name='sponsorship']", "input[name='visa']"],
                field_type="radio",
                transform="visa_to_yes_no",
            ),
            FieldMapping(
                profile_field="referral",
                selectors=["#referral", "input[name='referral']", "textarea[name='referral']"],
                field_type="textarea",
            ),
        ],
        ATSPlatform.LEVER: [
            FieldMapping(
                profile_field="full_name",
                selectors=["input[name='name']", "input[placeholder*='Name']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="email",
                selectors=["input[name='email']", "input[type='email']"],
                field_type="email",
                required=True,
            ),
            FieldMapping(
                profile_field="phone",
                selectors=["input[name='phone']", "input[placeholder*='Phone']"],
                field_type="tel",
            ),
            FieldMapping(
                profile_field="linkedin",
                selectors=["input[name='linkedin']", "input[placeholder*='LinkedIn']"],
                field_type="url",
            ),
            FieldMapping(
                profile_field="github",
                selectors=["input[name='github']", "input[placeholder*='GitHub']"],
                field_type="url",
            ),
            FieldMapping(
                profile_field="portfolio",
                selectors=["input[name='portfolio']", "input[placeholder*='Portfolio']"],
                field_type="url",
            ),
            FieldMapping(
                profile_field="resume",
                selectors=["input[name='resume']", "input[type='file']"],
                field_type="file",
                required=True,
            ),
            FieldMapping(
                profile_field="cover_letter",
                selectors=[
                    "input[name='coverLetter']",
                    "input[name='cover_letter']",
                    "textarea[name='coverLetter']",
                ],
                field_type="file",
            ),
            FieldMapping(
                profile_field="summary",
                selectors=["textarea[name='additional']", "textarea[placeholder*='Additional']"],
                field_type="textarea",
            ),
        ],
        ATSPlatform.WORKDAY: [
            FieldMapping(
                profile_field="first_name",
                selectors=["input[data-automation-id='firstName']", "input[name*='firstName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="last_name",
                selectors=["input[data-automation-id='lastName']", "input[name*='lastName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="email",
                selectors=["input[data-automation-id='email']", "input[type='email']"],
                field_type="email",
                required=True,
            ),
            FieldMapping(
                profile_field="phone",
                selectors=["input[data-automation-id='phone']", "input[name*='phone']"],
                field_type="tel",
            ),
            FieldMapping(
                profile_field="resume",
                selectors=["input[data-automation-id='resume']", "input[type='file']"],
                field_type="file",
                required=True,
            ),
            FieldMapping(
                profile_field="cover_letter",
                selectors=["input[data-automation-id='coverLetter']", "input[name*='coverLetter']"],
                field_type="file",
            ),
        ],
        ATSPlatform.ICIM: [
            FieldMapping(
                profile_field="first_name",
                selectors=["input[id*='firstName']", "input[name*='firstName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="last_name",
                selectors=["input[id*='lastName']", "input[name*='lastName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="email",
                selectors=["input[id*='email']", "input[type='email']"],
                field_type="email",
                required=True,
            ),
            FieldMapping(
                profile_field="phone",
                selectors=["input[id*='phone']", "input[name*='phone']"],
                field_type="tel",
            ),
            FieldMapping(
                profile_field="resume",
                selectors=["input[id*='resume']", "input[type='file']"],
                field_type="file",
                required=True,
            ),
        ],
        ATSPlatform.SMARTRECRUITERS: [
            FieldMapping(
                profile_field="first_name",
                selectors=["input[name='firstName']", "input[id='firstName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="last_name",
                selectors=["input[name='lastName']", "input[id='lastName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="email",
                selectors=["input[name='email']", "input[type='email']"],
                field_type="email",
                required=True,
            ),
            FieldMapping(
                profile_field="phone",
                selectors=["input[name='phone']", "input[id='phone']"],
                field_type="tel",
            ),
            FieldMapping(
                profile_field="linkedin",
                selectors=["input[name='linkedin']", "input[id='linkedin']"],
                field_type="url",
            ),
            FieldMapping(
                profile_field="resume",
                selectors=["input[name='resume']", "input[type='file']"],
                field_type="file",
                required=True,
            ),
            FieldMapping(
                profile_field="cover_letter",
                selectors=["input[name='coverLetter']", "textarea[name='coverLetter']"],
                field_type="file",
            ),
        ],
        ATSPlatform.BAMBOOHR: [
            FieldMapping(
                profile_field="first_name",
                selectors=["input[name='firstName']", "input[id='firstName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="last_name",
                selectors=["input[name='lastName']", "input[id='lastName']"],
                field_type="text",
                required=True,
            ),
            FieldMapping(
                profile_field="email",
                selectors=["input[name='email']", "input[type='email']"],
                field_type="email",
                required=True,
            ),
            FieldMapping(
                profile_field="phone",
                selectors=["input[name='phone']", "input[id='phone']"],
                field_type="tel",
            ),
            FieldMapping(
                profile_field="resume",
                selectors=["input[name='resume']", "input[type='file']"],
                field_type="file",
                required=True,
            ),
        ],
    }

    def __init__(self, browser: AthenaBrowser):
        self.browser = browser
        self.page: Optional[Page] = browser.page
        self.detected_platform: ATSPlatform = ATSPlatform.UNKNOWN
        self.detected_fields: list[FormField] = []

    @classmethod
    def detect_platform(cls, url: str) -> ATSPlatform:
        """Detect ATS platform from URL."""
        url_lower = url.lower()
        if "greenhouse.io" in url_lower or "boards.greenhouse.io" in url_lower:
            return ATSPlatform.GREENHOUSE
        elif "lever.co" in url_lower or "jobs.lever.co" in url_lower:
            return ATSPlatform.LEVER
        elif "workdayjobs.com" in url_lower or "myworkdayjobs.com" in url_lower:
            return ATSPlatform.WORKDAY
        elif "icims.com" in url_lower:
            return ATSPlatform.ICIM
        elif "smartrecruiters.com" in url_lower:
            return ATSPlatform.SMARTRECRUITERS
        elif "bamboohr.com" in url_lower:
            return ATSPlatform.BAMBOOHR
        return ATSPlatform.UNKNOWN

    async def detect_fields(self) -> list[FormField]:
        """Detect form fields on current page using heuristics."""
        if not self.page:
            raise RuntimeError("No active page")

        self.detected_platform = self.detect_platform(self.page.url)
        logger.info("Detected platform: %s", self.detected_platform.value)

        # Get all form elements
        fields = await self._scan_form_elements()

        # Enhance with platform-specific mappings
        fields = self._enhance_with_platform_mappings(fields)

        self.detected_fields = fields
        logger.info("Detected %d form fields", len(fields))
        return fields

    async def _scan_form_elements(self) -> list[FormField]:
        """Scan page for form elements and extract metadata."""
        if not self.page:
            return []

        # Get all input, select, textarea elements
        elements = await self.page.query_selector_all(
            "input:not([type='hidden']):not([type='submit']):not([type='button']), select, textarea"
        )

        fields = []
        for element in elements:
            field = await self._extract_field_info(element)
            if field:
                fields.append(field)

        return fields

    async def _extract_field_info(self, element: Any) -> Optional[FormField]:
        """Extract metadata from a form element."""
        try:
            tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
            input_type = await element.get_attribute("type") or "text"
            name = await element.get_attribute("name") or ""
            id_attr = await element.get_attribute("id") or ""
            placeholder = await element.get_attribute("placeholder") or ""
            aria_label = await element.get_attribute("aria-label") or ""
            required = await element.get_attribute("required") is not None
            aria_required = await element.get_attribute("aria-required") == "true"

            # Get associated label text
            label = await self._get_label_text(element, id_attr)

            # Get options for select elements
            options = []
            if tag_name == "select":
                options = await element.evaluate("""
                    el => Array.from(el.options).map(o => o.value).filter(v => v)
                """)

            # Build selector
            selector = await self._build_selector(element, tag_name, id_attr, name)

            # Determine field type
            field_type = self._determine_field_type(tag_name, input_type)

            # Check if file input
            is_file = input_type == "file"

            # Calculate confidence based on available identifiers
            confidence = self._calculate_confidence(label, name, id_attr, placeholder, aria_label)

            return FormField(
                selector=selector,
                field_type=field_type,
                label=label,
                name=name,
                placeholder=placeholder,
                aria_label=aria_label,
                required=required or aria_required,
                options=options,
                is_file_input=is_file,
                confidence=confidence,
            )
        except Exception as e:  # noqa: BLE001 - DOM quirks vary across ATS vendors
            logger.debug("Failed to extract field info: %s", e)
            return None

    async def _get_label_text(self, element: Any, id_attr: str) -> str:
        """Get label text associated with an element."""
        if not self.page:
            return ""

        try:
            # Try label[for=id]
            if id_attr:
                label_el = await self.page.query_selector(f"label[for='{id_attr}']")
                if label_el:
                    text = await label_el.text_content()
                    if text:
                        return cast(str, text).strip()

            # Try parent label
            label_el = await element.query_selector("xpath=ancestor::label[1]")
            if label_el:
                text = await label_el.text_content()
                if text:
                    return cast(str, text).strip()

            # Try preceding sibling label
            label_el = await element.query_selector("xpath=preceding-sibling::label[1]")
            if label_el:
                text = await label_el.text_content()
                if text:
                    return cast(str, text).strip()

            # Try aria-labelledby
            aria_labelledby = await element.get_attribute("aria-labelledby")
            if aria_labelledby:
                label_el = await self.page.query_selector(f"#{aria_labelledby}")
                if label_el:
                    text = await label_el.text_content()
                    if text:
                        return cast(str, text).strip()

        except Exception:  # noqa: BLE001 - any label lookup strategy may fail on exotic DOMs
            logger.debug("Failed to resolve label text", exc_info=True)

        return ""

    async def _build_selector(self, element: Any, tag_name: str, id_attr: str, name: str) -> str:
        """Build a robust CSS selector for the element."""
        # Prefer ID
        if id_attr:
            return f"#{id_attr}"

        # Try name attribute
        if name:
            return f"{tag_name}[name='{name}']"

        # Try placeholder
        placeholder = await element.get_attribute("placeholder")
        if placeholder:
            return f"{tag_name}[placeholder='{placeholder}']"

        # Try aria-label
        aria_label = await element.get_attribute("aria-label")
        if aria_label:
            return f"{tag_name}[aria-label='{aria_label}']"

        # Fallback: use nth-of-type (less reliable)
        try:
            index = await element.evaluate("""
                el => Array.from(el.parentNode.querySelectorAll(el.tagName)).indexOf(el) + 1
            """)
            return f"{tag_name}:nth-of-type({index})"
        except Exception:  # noqa: BLE001 - fall back when the DOM probe fails
            return tag_name

    def _determine_field_type(self, tag_name: str, input_type: str) -> str:
        """Determine field type from tag and input type."""
        if tag_name == "select":
            return "select"
        if tag_name == "textarea":
            return "textarea"
        if input_type in ("radio", "checkbox"):
            return input_type
        if input_type == "file":
            return "file"
        return input_type

    def _calculate_confidence(
        self, label: str, name: str, id_attr: str, placeholder: str, aria_label: str
    ) -> float:
        """Calculate confidence score for field identification."""
        score = 0.0
        if id_attr:
            score += 0.3
        if name:
            score += 0.3
        if label:
            score += 0.2
        if placeholder:
            score += 0.1
        if aria_label:
            score += 0.1
        return min(score, 1.0)

    def _enhance_with_platform_mappings(self, fields: list[FormField]) -> list[FormField]:
        """Enhance detected fields with platform-specific mappings."""
        if self.detected_platform not in self.PLATFORM_MAPPINGS:
            return fields

        mappings = self.PLATFORM_MAPPINGS[self.detected_platform]
        enhanced = []

        for field_item in fields:
            # Try to match with platform mappings
            best_match = None
            best_score = 0.0

            for mapping in mappings:
                score = self._match_field_to_mapping(field_item, mapping)
                if score > best_score:
                    best_score = score
                    best_match = mapping

            if best_match and best_score > 0.5:
                # Enhance field with mapping info
                field_item.profile_field = best_match.profile_field
                field_item.required = best_match.required or field_item.required
            enhanced.append(field_item)

        return enhanced

    def _match_field_to_mapping(self, field: FormField, mapping: FieldMapping) -> float:
        """Match a detected field to a platform mapping."""
        score = 0.0
        search_text = " ".join(
            [field.label, field.name, field.placeholder, field.aria_label]
        ).lower()

        for pattern in self.FIELD_PATTERNS.get(mapping.profile_field, []):
            if re.search(pattern, search_text, re.IGNORECASE):
                score += 0.5

        # Exact selector match
        for selector in mapping.selectors:
            if selector in field.selector:
                score += 0.5
                break

        return min(score, 1.0)

    async def fill_form(
        self, profile: UserProfile, resume_path: Path, cover_letter_path: Optional[Path] = None
    ) -> dict[str, bool]:
        """Fill form with user profile data."""
        if not self.detected_fields:
            await self.detect_fields()

        results = {}

        # Build field value map from profile
        field_values = self._build_field_values(profile, resume_path, cover_letter_path)

        # Fill each detected field
        for field_item in self.detected_fields:
            profile_field = getattr(field_item, "profile_field", None)
            if not profile_field:
                # Try heuristic match
                profile_field = self._heuristic_match_field(field_item)

            if profile_field and profile_field in field_values:
                value = field_values[profile_field]
                success = await self._fill_field(field_item, value)
                results[f"{profile_field} ({field_item.selector})"] = success
            else:
                logger.debug("No value for field: %s", field_item.selector)

        return results

    def _build_field_values(
        self, profile: UserProfile, resume_path: Path, cover_letter_path: Optional[Path]
    ) -> dict[str, Any]:
        """Build field values from user profile."""
        values = {
            "full_name": profile.full_name,
            "first_name": profile.full_name.split()[0] if profile.full_name else "",
            "last_name": " ".join(profile.full_name.split()[1:])
            if len(profile.full_name.split()) > 1
            else "",
            "email": profile.email,
            "phone": profile.phone or "",
            "location": profile.location or "",
            "linkedin": str(profile.linkedin_url) if profile.linkedin_url else "",
            "github": str(profile.github_url) if profile.github_url else "",
            "portfolio": str(profile.portfolio_url) if profile.portfolio_url else "",
            "summary": profile.summary or profile.headline or "",
            "headline": profile.headline or "",
            "resume": resume_path,
            "cover_letter": cover_letter_path,
            "visa_sponsorship": profile.preferences.visa_sponsorship_required,
            "salary_expectation": str(profile.preferences.min_salary)
            if profile.preferences.min_salary
            else "",
            "experience_years": self._calculate_total_experience(profile),
            "skills": ", ".join([s.name for s in profile.skills]),
            "education": self._format_education(profile),
            "experience": self._format_experience(profile),
        }
        return values

    def _heuristic_match_field(self, field: FormField) -> Optional[str]:
        """Match field to profile field using heuristics."""
        search_text = " ".join(
            [field.label, field.name, field.placeholder, field.aria_label]
        ).lower()

        for profile_field, patterns in self.FIELD_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, search_text, re.IGNORECASE):
                    return profile_field

        return None

    async def _fill_field(self, field: FormField, value: Any) -> bool:
        """Fill a single field based on its type."""
        if not self.page:
            return False

        try:
            if field.field_type == "file" and isinstance(value, Path):
                return await self.browser.upload_file(field.selector, value)
            elif field.field_type in ("text", "email", "tel", "url", "textarea"):
                return await self.browser.fill_field(field.selector, str(value))
            elif field.field_type == "select":
                return await self.browser.select_option(field.selector, str(value))
            elif field.field_type in ("radio", "checkbox"):
                if value:
                    return await self.browser.click(field.selector)
                return True
            else:
                logger.warning("Unknown field type: %s", field.field_type)
                return False
        except Exception as e:  # noqa: BLE001 - per-field fill errors are handled per-field
            logger.warning("Failed to fill field %s: %s", field.selector, e)
            return False

    def _calculate_total_experience(self, profile: UserProfile) -> str:
        """Calculate total years of experience."""
        total_months = 0
        for exp in profile.experience:
            start = exp.start_date
            end = exp.end_date if not exp.current else datetime.now()
            if start and end:
                months = (end.year - start.year) * 12 + (end.month - start.month)
                total_months += max(0, months)
        years = total_months / 12
        return f"{years:.1f}"

    def _format_education(self, profile: UserProfile) -> str:
        """Format education for text fields."""
        lines = []
        for edu in profile.education:
            line = f"{edu.degree} in {edu.field_of_study} from {edu.institution}"
            if edu.end_date:
                line += f" ({edu.end_date.year})"
            lines.append(line)
        return "\n".join(lines)

    def _format_experience(self, profile: UserProfile) -> str:
        """Format experience for text fields."""
        lines = []
        for exp in profile.experience:
            line = f"{exp.title} at {exp.company}"
            if exp.location:
                line += f" ({exp.location})"
            line += f" - {exp.start_date.strftime('%m/%Y')}"
            if exp.current:
                line += " - Present"
            elif exp.end_date:
                line += f" - {exp.end_date.strftime('%m/%Y')}"
            lines.append(line)
        return "\n".join(lines)

    async def find_next_button(self) -> Optional[str]:
        """Find next/continue button selector."""
        if not self.page:
            return None

        next_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Next')",
            "button:has-text('Continue')",
            "button:has-text('Submit')",
            "button:has-text('Apply')",
            "button:has-text('Save')",
            "[data-automation-id='next']",
            "[data-automation-id='continue']",
            "button.next",
            "button.continue",
            "a.next",
            "a.continue",
        ]

        for selector in next_selectors:
            try:
                if await self.page.query_selector(selector):
                    return selector
            except Exception:  # noqa: BLE001 - missing/transient elements are expected here
                logger.debug("Selector probe failed: %s", selector)
                continue

        return None

    async def click_next(self) -> bool:
        """Click next/continue button."""
        selector = await self.find_next_button()
        if selector:
            return await self.browser.click(selector)
        return False

    async def handle_multi_step_form(
        self,
        profile: UserProfile,
        resume_path: Path,
        cover_letter_path: Optional[Path] = None,
        max_steps: int = 10,
    ) -> dict[str, Any]:
        """Handle multi-step form filling."""
        results: dict[str, Any] = {"steps_completed": 0, "fields_filled": {}, "errors": []}

        for step in range(max_steps):
            logger.info("Processing form step %d", step + 1)

            # Detect fields on current step
            await self.detect_fields()

            # Fill fields
            step_results = await self.fill_form(profile, resume_path, cover_letter_path)
            results["fields_filled"][f"step_{step + 1}"] = step_results

            # Try to find and click next
            next_clicked = await self.click_next()
            if not next_clicked:
                logger.info("No next button found, form may be complete")
                break

            results["steps_completed"] += 1
            await asyncio.sleep(1)  # Wait for next page to load

        return results
