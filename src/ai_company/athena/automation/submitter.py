"""Application submission workflow with HITL approval gate.

Provides end-to-end application submission including pre-submit validation,
human-in-the-loop approval, submission execution, confirmation capture,
and audit trail logging.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

from ...executor.hitl_gate import HITLGate
from ...orchestrator.message_bus import MessageBus
from ..models.enums import ApplicationStatus
from ..models.jobs import Application, Document, Job, UserProfile
from ..store import athena_db
from .browser import AthenaBrowser, BrowserConfig
from .form_filler import FormFiller

logger = logging.getLogger(__name__)


class SubmissionStage(str, Enum):
    """Stages of the submission workflow."""

    INITIALIZED = "initialized"
    NAVIGATING = "navigating"
    DETECTING_FIELDS = "detecting_fields"
    FILLING_FORM = "filling_form"
    VALIDATING = "validating"
    AWAITING_APPROVAL = "awaiting_approval"
    SUBMITTING = "submitting"
    CONFIRMING = "confirming"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class SubmitConfig:
    """Configuration for submission behavior."""

    # HITL settings
    require_approval: bool = True
    approval_timeout_minutes: int = 30
    approval_agent_id: str = "athena-automation"

    # Validation
    validate_required_fields: bool = True
    min_required_fields_filled: float = 0.8  # 80% of required fields

    # Retry logic
    max_retries: int = 3
    retry_delay_seconds: int = 5

    # Confirmation
    capture_confirmation_screenshot: bool = True
    capture_receipt_number: bool = True
    confirmation_selectors: list[str] = field(
        default_factory=lambda: [
            "[data-automation-id='confirmationNumber']",
            ".confirmation-number",
            ".receipt-number",
            "#confirmationNumber",
            "text=/confirmation|receipt|reference/i",
        ]
    )

    # Audit
    save_audit_trail: bool = True
    audit_dir: Optional[Path] = None


@dataclass
class SubmissionResult:
    """Result of application submission."""

    success: bool = False
    application_id: Optional[UUID] = None
    job_id: Optional[UUID] = None
    stage: SubmissionStage = SubmissionStage.INITIALIZED
    confirmation_number: Optional[str] = None
    confirmation_url: Optional[str] = None
    screenshot_path: Optional[Path] = None
    error_message: Optional[str] = None
    fields_filled: dict[str, bool] = field(default_factory=dict)
    required_fields_missing: list[str] = field(default_factory=list)
    retry_count: int = 0
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    approval_request_id: Optional[str] = None
    approved: Optional[bool] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "application_id": str(self.application_id) if self.application_id else None,
            "job_id": str(self.job_id) if self.job_id else None,
            "stage": self.stage.value,
            "confirmation_number": self.confirmation_number,
            "confirmation_url": self.confirmation_url,
            "screenshot_path": str(self.screenshot_path) if self.screenshot_path else None,
            "error_message": self.error_message,
            "fields_filled": self.fields_filled,
            "required_fields_missing": self.required_fields_missing,
            "retry_count": self.retry_count,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "approval_request_id": self.approval_request_id,
            "approved": self.approved,
        }


class ApplicationSubmitter:
    """Handles end-to-end application submission workflow."""

    def __init__(
        self,
        browser: Optional[AthenaBrowser] = None,
        config: Optional[SubmitConfig] = None,
        message_bus: Optional[MessageBus] = None,
        hitl_gate: Optional[HITLGate] = None,
    ):
        self.browser = browser
        self.config = config or SubmitConfig()
        self.message_bus = message_bus
        self.hitl_gate = hitl_gate or HITLGate()
        self.form_filler: Optional[FormFiller] = None
        self._current_application: Optional[Application] = None
        self._current_job: Optional[Job] = None
        self._current_profile: Optional[UserProfile] = None
        self._current_resume: Optional[Document] = None
        self._current_cover_letter: Optional[Document] = None
        self._result = SubmissionResult()

    async def __aenter__(self) -> "ApplicationSubmitter":
        if self.browser is None:
            browser_config = BrowserConfig(
                headless=True,
                audit_dir=self.config.audit_dir,
                record_video=True,
                record_har=True,
                screenshot_on_action=True,
            )
            self.browser = AthenaBrowser(browser_config)
            await self.browser.start()

        self.form_filler = FormFiller(self.browser)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        if self.browser:
            await self.browser.stop()

    async def submit_application(
        self,
        job: Job,
        profile: UserProfile,
        resume: Document,
        cover_letter: Optional[Document] = None,
        application: Optional[Application] = None,
    ) -> SubmissionResult:
        """Execute full application submission workflow."""
        self._current_job = job
        self._current_profile = profile
        self._current_resume = resume
        self._current_cover_letter = cover_letter
        self._result = SubmissionResult(job_id=job.id)
        self._result.started_at = datetime.now()

        # Create or use existing application record
        if application is None:
            application = Application(
                job_id=job.id,
                user_profile_id=profile.id,
                resume_id=resume.id,
                cover_letter_id=cover_letter.id if cover_letter else None,
                ats_score=0.0,
                match_score=0.0,
                status=ApplicationStatus.PENDING,
            )
            application = athena_db.add_application(application)

        self._current_application = application
        self._result.application_id = application.id

        logger.info("Starting application submission for job %s", job.id)

        try:
            # Stage 1: Navigate to application URL
            await self._update_stage(SubmissionStage.NAVIGATING)
            await self._navigate_to_application(job)

            # Stage 2: Detect form fields
            await self._update_stage(SubmissionStage.DETECTING_FIELDS)
            if not self.form_filler:
                raise RuntimeError("Form filler not initialized")
            await self.form_filler.detect_fields()

            # Stage 3: Fill form
            await self._update_stage(SubmissionStage.FILLING_FORM)
            fill_results = await self._fill_application_form(profile, resume, cover_letter)
            self._result.fields_filled = fill_results

            # Stage 4: Validate form
            await self._update_stage(SubmissionStage.VALIDATING)
            validation = await self._validate_form()
            self._result.required_fields_missing = validation["missing_required"]

            if not validation["valid"] and self.config.validate_required_fields:
                self._result.success = False
                self._result.stage = SubmissionStage.FAILED
                self._result.error_message = (
                    f"Validation failed: missing required fields: {validation['missing_required']}"
                )
                await self._finalize()
                return self._result

            # Stage 5: HITL Approval
            if self.config.require_approval:
                await self._update_stage(SubmissionStage.AWAITING_APPROVAL)
                approved = await self._request_human_approval()
                self._result.approved = approved
                if not approved:
                    self._result.success = False
                    self._result.stage = SubmissionStage.CANCELLED
                    self._result.error_message = "Human approval denied or timed out"
                    await self._finalize()
                    return self._result

            # Stage 6: Submit
            await self._update_stage(SubmissionStage.SUBMITTING)
            submitted = await self._submit_form()
            if not submitted:
                self._result.success = False
                self._result.stage = SubmissionStage.FAILED
                self._result.error_message = "Form submission failed"
                await self._finalize()
                return self._result

            # Stage 7: Confirm
            await self._update_stage(SubmissionStage.CONFIRMING)
            confirmation = await self._capture_confirmation()
            self._result.confirmation_number = confirmation.get("number")
            self._result.confirmation_url = confirmation.get("url")
            self._result.screenshot_path = confirmation.get("screenshot")

            # Success!
            self._result.success = True
            self._result.stage = SubmissionStage.COMPLETED
            await self._finalize()

        except Exception as e:
            logger.exception("Submission failed with exception")
            self._result.success = False
            self._result.stage = SubmissionStage.FAILED
            self._result.error_message = str(e)
            await self._finalize()

        return self._result

    async def _navigate_to_application(self, job: Job) -> None:
        """Navigate to the job application URL."""
        url = str(job.application_url)
        logger.info("Navigating to application URL: %s", url)

        if not self.browser:
            raise RuntimeError("Browser not initialized")

        await self.browser.navigate(url, wait_until="networkidle")

        # Wait for form to load
        await asyncio.sleep(2)

        # Handle any initial modals/cookies
        await self._handle_initial_modals()

    async def _handle_initial_modals(self) -> None:
        """Handle cookie banners, modals, etc."""
        if not self.browser or not self.browser.page:
            return

        # Common cookie banner selectors
        cookie_selectors = [
            "button:has-text('Accept')",
            "button:has-text('Accept All')",
            "button:has-text('I Agree')",
            "[data-testid='accept-cookies']",
            "#accept-cookies",
            ".cookie-banner button",
        ]

        for selector in cookie_selectors:
            try:
                await self.browser.click(selector, force=True)
                await asyncio.sleep(0.5)
                break
            except (TimeoutError, ValueError):
                continue

    async def _fill_application_form(
        self, profile: UserProfile, resume: Document, cover_letter: Optional[Document]
    ) -> dict[str, bool]:
        """Fill the application form with profile data."""
        resume_path = Path(resume.file_path)
        cover_letter_path = Path(cover_letter.file_path) if cover_letter else None

        if not self.form_filler:
            raise RuntimeError("Form filler not initialized")

        # Try multi-step form handling
        results = await self.form_filler.handle_multi_step_form(
            profile, resume_path, cover_letter_path, max_steps=10
        )

        # Flatten results
        flat_results = {}
        for _step, step_data in results.get("fields_filled", {}).items():
            flat_results.update(step_data)

        return flat_results

    async def _validate_form(self) -> dict[str, Any]:
        """Validate that required fields are filled."""
        if not self.form_filler:
            return {"valid": False, "missing_required": ["form_filler_not_initialized"]}

        missing = []
        filled_count = 0
        required_count = 0

        for form_field in self.form_filler.detected_fields:
            if form_field.required:
                required_count += 1
                # Check if field was filled
                field_key = (
                    f"{getattr(form_field, 'profile_field', 'unknown')} ({form_field.selector})"
                )
                if self._result.fields_filled.get(field_key, False):
                    filled_count += 1
                else:
                    missing.append(field_key)

        # Check threshold
        if required_count > 0:
            fill_ratio = filled_count / required_count
            valid = fill_ratio >= self.config.min_required_fields_filled
        else:
            valid = True

        logger.info(
            "Form validation: %d/%d required fields filled (%.1f%%)",
            filled_count,
            required_count,
            fill_ratio * 100 if required_count else 100,
        )

        return {
            "valid": valid,
            "missing_required": missing,
            "filled": filled_count,
            "total": required_count,
        }

    async def _request_human_approval(self) -> bool:
        """Request human approval via HITL gate."""
        if not self._current_application or not self._current_job:
            return False

        task_id = f"apply-{self._current_application.id}"
        tool = "submit_application"
        args = {
            "job_title": self._current_job.title,
            "company": self._current_job.company,
            "application_id": str(self._current_application.id),
        }

        logger.info("Requesting HITL approval for application %s", self._current_application.id)

        # Use non-blocking request_and_park
        request_id = self.hitl_gate.request_and_park(
            task_id=task_id,
            agent_id=self.config.approval_agent_id,
            tool=tool,
            args=args,
        )

        self._result.approval_request_id = request_id

        # Poll for approval
        timeout = self.config.approval_timeout_minutes * 60
        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() < timeout:
            result = self.hitl_gate.resume_approved(request_id)
            if result is True:
                logger.info("Application approved by human")
                return True
            elif result is False:
                logger.info("Application rejected by human")
                return False
            await asyncio.sleep(2)

        logger.warning(
            "HITL approval timed out after %d minutes", self.config.approval_timeout_minutes
        )
        return False

    async def _submit_form(self) -> bool:
        """Submit the filled form."""
        if not self.browser or not self.browser.page:
            return False

        # Find submit button
        submit_selectors = [
            "button[type='submit']:not([disabled])",
            "input[type='submit']:not([disabled])",
            "button:has-text('Submit Application'):not([disabled])",
            "button:has-text('Apply'):not([disabled])",
            "button:has-text('Submit'):not([disabled])",
            "[data-automation-id='submit']:not([disabled])",
            "button.submit:not([disabled])",
        ]

        for selector in submit_selectors:
            try:
                element = await self.browser.page.query_selector(selector)
                if element:
                    # Check if enabled
                    disabled = await element.get_attribute("disabled")
                    if disabled:
                        continue

                    logger.info("Clicking submit button: %s", selector)
                    await self.browser.click(selector)
                    await asyncio.sleep(3)  # Wait for submission
                    return True
            except (TimeoutError, ValueError) as e:
                logger.debug("Submit selector %s failed: %s", selector, e)
                continue

        logger.error("No submit button found")
        return False

    async def _capture_confirmation(self) -> dict[str, Any]:
        """Capture confirmation number and screenshot after submission."""
        result: dict[str, Any] = {"number": None, "url": None, "screenshot": None}

        if not self.browser or not self.browser.page:
            return result

        # Wait for confirmation page
        await asyncio.sleep(3)

        # Capture URL
        result["url"] = self.browser.page.url

        # Try to find confirmation number
        for selector in self.config.confirmation_selectors:
            try:
                if "text=" in selector:
                    # Text-based selector
                    element = await self.browser.page.query_selector(
                        "xpath=//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'confirmation') "
                        "or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'receipt')]"
                    )
                else:
                    element = await self.browser.page.query_selector(selector)

                if element:
                    text = await element.text_content()
                    if text:
                        # Extract number from text
                        import re

                        numbers = re.findall(r"[\w-]{6,}", text)
                        if numbers:
                            result["number"] = numbers[0]
                            logger.info("Found confirmation number: %s", result["number"])
                            break
            except (TimeoutError, ValueError):
                continue

        # Screenshot
        if self.config.capture_confirmation_screenshot and self.config.audit_dir:
            try:
                screenshot = await self.browser.screenshot("confirmation")
                result["screenshot"] = screenshot
            except (TimeoutError, ValueError, OSError) as e:
                logger.warning("Failed to capture confirmation screenshot: %s", e)

        return result

    async def _update_stage(self, stage: SubmissionStage) -> None:
        """Update current stage and emit event."""
        self._result.stage = stage
        logger.info("Stage: %s", stage.value)

        # Emit event to message bus
        if self.message_bus and self._current_application:
            from ...models.task import Task, TaskStatus

            task = Task(
                id=f"submit-{self._current_application.id}-{stage.value}",
                name="submission_stage_update",
                sender_id="athena-submitter",
                receiver_id="dashboard",
                instruction=(
                    f"Submission {self._current_application.id} reached stage {stage.value} "
                    f"(job_id={self._current_job.id if self._current_job else 'unknown'})"
                ),
                tags=["athena", "submission"],
                status=TaskStatus.COMPLETED,
            )
            self.message_bus.send_task(task)

        # Update application in database
        if self._current_application:
            if stage == SubmissionStage.COMPLETED:
                self._current_application.status = ApplicationStatus.SUBMITTED
                self._current_application.submitted_at = datetime.now()
                if self._result.confirmation_number:
                    self._current_application.receipt_data["confirmation_number"] = (
                        self._result.confirmation_number
                    )
                if self._result.confirmation_url:
                    self._current_application.receipt_data["confirmation_url"] = (
                        self._result.confirmation_url
                    )
            elif stage == SubmissionStage.FAILED:
                self._current_application.status = ApplicationStatus.FAILED
                self._current_application.notes = self._result.error_message or "Submission failed"
            elif stage == SubmissionStage.CANCELLED:
                self._current_application.status = ApplicationStatus.WITHDRAWN
                self._current_application.notes = "Cancelled by user"

            self._current_application.updated_at = datetime.now()
            athena_db.update_application(self._current_application)

    async def _finalize(self) -> None:
        """Finalize submission and save results."""
        self._result.completed_at = datetime.now()

        # Save audit trail
        if self.config.save_audit_trail and self.browser:
            audit_log = self.browser.get_audit_log()
            if self.config.audit_dir:
                self.config.audit_dir.mkdir(parents=True, exist_ok=True)
                audit_file = (
                    self.config.audit_dir
                    / f"submission_{self._result.application_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                import json

                audit_file.write_text(
                    json.dumps(
                        {
                            "result": self._result.to_dict(),
                            "audit_log": audit_log,
                        },
                        indent=2,
                    )
                )
                logger.info("Audit trail saved: %s", audit_file)

        # Emit final event
        if self.message_bus and self._current_application:
            from ...models.task import Task, TaskStatus

            task = Task(
                id=f"submit-{self._current_application.id}-final",
                name="submission_completed",
                sender_id="athena-submitter",
                receiver_id="dashboard",
                instruction=(
                    f"Submission {self._current_application.id} completed successfully"
                    if self._result.success
                    else f"Submission {self._current_application.id} failed: "
                    f"{self._result.error_message or 'unknown error'}"
                ),
                tags=["athena", "submission", "final"],
                status=TaskStatus.COMPLETED if self._result.success else TaskStatus.FAILED,
            )
            self.message_bus.send_task(task)

        logger.info("Submission finalized: success=%s", self._result.success)

    async def retry_submission(self, max_retries: Optional[int] = None) -> SubmissionResult:
        """Retry failed submission."""
        max_retries = max_retries or self.config.max_retries

        for attempt in range(max_retries):
            logger.info("Retry attempt %d/%d", attempt + 1, max_retries)
            self._result.retry_count = attempt + 1

            await asyncio.sleep(self.config.retry_delay_seconds)

            if self._current_job is None or self._current_profile is None:
                raise RuntimeError("No completed submission context to retry")
            if self._current_resume is None:
                raise RuntimeError("Resume is required to retry submission")

            result = await self.submit_application(
                self._current_job,
                self._current_profile,
                self._current_resume,
                self._current_cover_letter,
                application=self._current_application,
            )

            if result.success:
                return result

        return self._result

    def get_result(self) -> SubmissionResult:
        """Get current submission result."""
        return self._result
