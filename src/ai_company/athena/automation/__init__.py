"""Athena Browser Automation Module.

Provides Playwright-based browser automation for form filling and application
submission across major ATS platforms (Greenhouse, Lever, Workday, iCIMS,
SmartRecruiters, BambooHR).

Exports:
    - browser: Playwright wrapper with stealth mode, session persistence, audit trail
    - form_filler: Smart form field detection and filling for ATS platforms
    - submitter: Application submission workflow with HITL approval gate
"""

from .browser import AthenaBrowser, BrowserConfig, BrowserSession
from .form_filler import ATSPlatform, FieldMapping, FormFiller
from .submitter import ApplicationSubmitter, SubmissionResult, SubmitConfig

__all__ = [
    "AthenaBrowser",
    "BrowserConfig",
    "BrowserSession",
    "FormFiller",
    "ATSPlatform",
    "FieldMapping",
    "ApplicationSubmitter",
    "SubmissionResult",
    "SubmitConfig",
]

__version__ = "1.0.0"
