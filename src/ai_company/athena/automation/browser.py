"""Playwright browser wrapper for Athena automation.

Provides headless Chromium management with stealth mode, session persistence
(cookies, localStorage), and screenshot/recording for audit trails.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, cast
from urllib.parse import urlparse

try:
    from playwright.async_api import (
        Browser as PlaywrightBrowser,
    )
    from playwright.async_api import (
        BrowserContext,
        Page,
        Playwright,
        async_playwright,
    )

    PLAYWRIGHT_AVAILABLE = True
except ImportError:  # pragma: no cover - playwright is an optional e2e dependency
    PLAYWRIGHT_AVAILABLE = False
    # The names are only referenced in lazy annotations (future annotations) or
    # behind the PLAYWRIGHT_AVAILABLE guard, so Any placeholders keep the module
    # importable and mypy happy when the e2e extra is not installed.
    PlaywrightBrowser = Any  # noqa: F811
    BrowserContext = Any  # noqa: F811
    Page = Any  # noqa: F811
    Playwright = Any  # noqa: F811
    async_playwright = Any  # noqa: F811

logger = logging.getLogger(__name__)


@dataclass
class BrowserConfig:
    """Configuration for browser behavior."""

    headless: bool = True
    slow_mo: int = 0  # milliseconds
    viewport_width: int = 1920
    viewport_height: int = 1080
    user_agent: Optional[str] = None
    locale: str = "en-US"
    timezone_id: str = "America/New_York"
    # Stealth settings
    stealth_enabled: bool = True
    hide_webdriver: bool = True
    mock_chrome_runtime: bool = True
    mock_permissions: bool = True
    # Session persistence
    session_dir: Optional[Path] = None
    persist_cookies: bool = True
    persist_localstorage: bool = True
    # Audit trail
    audit_dir: Optional[Path] = None
    record_video: bool = True
    record_har: bool = True
    screenshot_on_action: bool = True
    # Timeouts
    navigation_timeout: int = 60000  # ms
    action_timeout: int = 30000  # ms
    # Proxy
    proxy_server: Optional[str] = None
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None


@dataclass
class BrowserSession:
    """Represents a persisted browser session."""

    id: str
    created_at: datetime
    updated_at: datetime
    cookies: list[dict[str, Any]] = field(default_factory=list)
    local_storage: dict[str, str] = field(default_factory=dict)
    session_storage: dict[str, str] = field(default_factory=dict)
    origin: str = ""
    user_agent: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "cookies": self.cookies,
            "local_storage": self.local_storage,
            "session_storage": self.session_storage,
            "origin": self.origin,
            "user_agent": self.user_agent,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrowserSession":
        return cls(
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            cookies=data.get("cookies", []),
            local_storage=data.get("local_storage", {}),
            session_storage=data.get("session_storage", {}),
            origin=data.get("origin", ""),
            user_agent=data.get("user_agent", ""),
        )


class AthenaBrowser:
    """Playwright browser wrapper with stealth, persistence, and audit trail."""

    def __init__(self, config: Optional[BrowserConfig] = None):
        self.config = config or BrowserConfig()
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[PlaywrightBrowser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._session: Optional[BrowserSession] = None
        self._audit_log: list[dict[str, Any]] = []
        self._video_path: Optional[Path] = None
        self._har_path: Optional[Path] = None

    async def __aenter__(self) -> "AthenaBrowser":
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        await self.stop()

    async def start(self) -> None:
        """Launch browser with configured stealth and persistence."""
        logger.info("Starting Athena browser (headless=%s)", self.config.headless)

        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError(
                "Athena browser automation requires the optional 'playwright' package. "
                "Install the e2e extras with: uv sync --extra e2e"
            )

        self._playwright = await async_playwright().start()

        # Build launch arguments
        launch_args: dict[str, Any] = {
            "headless": self.config.headless,
            "slow_mo": self.config.slow_mo,
        }

        if self.config.proxy_server:
            launch_args["proxy"] = {
                "server": self.config.proxy_server,
                "username": self.config.proxy_username,
                "password": self.config.proxy_password,
            }

        self._browser = await self._playwright.chromium.launch(**launch_args)

        # Build context options
        context_options = {
            "viewport": {
                "width": self.config.viewport_width,
                "height": self.config.viewport_height,
            },
            "locale": self.config.locale,
            "timezone_id": self.config.timezone_id,
            "record_video_dir": (
                str(self.config.audit_dir / "videos")
                if self.config.audit_dir and self.config.record_video
                else None
            ),
            "record_har_path": (
                str(self.config.audit_dir / "network.har")
                if self.config.audit_dir and self.config.record_har
                else None
            ),
        }

        if self.config.user_agent:
            context_options["user_agent"] = self.config.user_agent

        self._context = await self._browser.new_context(**context_options)

        # Apply stealth modifications
        if self.config.stealth_enabled:
            await self._apply_stealth()

        # Load persisted session if available
        if self.config.session_dir and self.config.persist_cookies:
            await self._load_session()

        self._page = await self._context.new_page()

        # Set default timeouts
        self._page.set_default_navigation_timeout(self.config.navigation_timeout)
        self._page.set_default_timeout(self.config.action_timeout)

        # Enable request/response logging for HAR
        if self.config.record_har:
            self._page.on("request", self._log_request)
            self._page.on("response", self._log_response)

        logger.info("Browser started successfully")

    async def stop(self) -> None:
        """Stop browser and persist session."""
        logger.info("Stopping Athena browser")

        # Persist session before closing
        if self.config.session_dir and self._context:
            await self._save_session()

        # Save audit log
        if self.config.audit_dir:
            await self._save_audit_log()

        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

        logger.info("Browser stopped")

    async def _apply_stealth(self) -> None:
        """Apply stealth modifications to avoid bot detection."""
        if not self._context:
            return

        # Hide webdriver property
        if self.config.hide_webdriver:
            await self._context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

        # Mock Chrome runtime
        if self.config.mock_chrome_runtime:
            await self._context.add_init_script("""
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };
            """)

        # Mock permissions
        if self.config.mock_permissions:
            await self._context.add_init_script("""
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)

        # Additional stealth: mock plugins, languages, etc.
        await self._context.add_init_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32'
            });
        """)

        logger.debug("Stealth modifications applied")

    async def _load_session(self) -> None:
        """Load persisted session (cookies, localStorage)."""
        if not self.config.session_dir or not self._context:
            return

        session_file = self.config.session_dir / "session.json"
        if not session_file.exists():
            logger.debug("No persisted session found")
            return

        try:
            data = json.loads(session_file.read_text())
            self._session = BrowserSession.from_dict(data)

            # Restore cookies
            if self.config.persist_cookies and self._session.cookies:
                await self._context.add_cookies(self._session.cookies)
                logger.debug("Restored %d cookies", len(self._session.cookies))

            # Restore localStorage and sessionStorage via init script
            if self.config.persist_localstorage and (
                self._session.local_storage or self._session.session_storage
            ):
                await self._context.add_init_script(f"""
                    const localData = {json.dumps(self._session.local_storage)};
                    const sessionData = {json.dumps(self._session.session_storage)};
                    for (const [key, value] of Object.entries(localData)) {{
                        localStorage.setItem(key, value);
                    }}
                    for (const [key, value] of Object.entries(sessionData)) {{
                        sessionStorage.setItem(key, value);
                    }}
                """)
                logger.debug(
                    "Restored localStorage (%d items) and sessionStorage (%d items)",
                    len(self._session.local_storage),
                    len(self._session.session_storage),
                )

            logger.info("Session loaded: %s", self._session.id)

        except (json.JSONDecodeError, OSError, ValueError) as e:
            logger.warning("Failed to load session: %s", e)

    async def _save_session(self) -> None:
        """Persist current session (cookies, localStorage)."""
        if not self.config.session_dir or not self._context or not self._page:
            return

        try:
            self.config.session_dir.mkdir(parents=True, exist_ok=True)

            # Get cookies
            cookies = await self._context.cookies()

            # Get localStorage and sessionStorage
            local_storage = await self._page.evaluate("() => JSON.stringify(localStorage)")
            session_storage = await self._page.evaluate("() => JSON.stringify(sessionStorage)")

            # Get origin
            origin = await self._page.evaluate("() => window.location.origin")

            # Get user agent
            user_agent = await self._page.evaluate("() => navigator.userAgent")

            session = BrowserSession(
                id=self._session.id if self._session else str(uuid.uuid4()),
                created_at=self._session.created_at if self._session else datetime.now(),
                updated_at=datetime.now(),
                cookies=cookies,
                local_storage=json.loads(local_storage) if local_storage else {},
                session_storage=json.loads(session_storage) if session_storage else {},
                origin=origin,
                user_agent=user_agent,
            )

            session_file = self.config.session_dir / "session.json"
            session_file.write_text(json.dumps(session.to_dict(), indent=2))

            self._session = session
            logger.info("Session saved: %s", session.id)

        except (OSError, json.JSONDecodeError, ValueError) as e:
            logger.warning("Failed to save session: %s", e)

    def _log_request(self, request: Any) -> None:
        """Log request for audit trail."""
        if not self.config.audit_dir:
            return
        self._audit_log.append(
            {
                "type": "request",
                "timestamp": datetime.now().isoformat(),
                "url": request.url,
                "method": request.method,
                "headers": dict(request.headers),
                "resource_type": request.resource_type,
            }
        )

    def _log_response(self, response: Any) -> None:
        """Log response for audit trail."""
        if not self.config.audit_dir:
            return
        self._audit_log.append(
            {
                "type": "response",
                "timestamp": datetime.now().isoformat(),
                "url": response.url,
                "status": response.status,
                "headers": dict(response.headers),
            }
        )

    async def _save_audit_log(self) -> None:
        """Save audit log to file."""
        if not self.config.audit_dir:
            return

        try:
            self.config.audit_dir.mkdir(parents=True, exist_ok=True)
            audit_file = (
                self.config.audit_dir / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
            )
            lines = [json.dumps(entry) for entry in self._audit_log]
            audit_file.write_text("\n".join(lines))
            logger.info("Audit log saved: %s (%d entries)", audit_file, len(self._audit_log))
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Failed to save audit log: %s", e)

    async def navigate(self, url: str, wait_until: str = "networkidle") -> Page:
        """Navigate to URL and return page."""
        if not self._page:
            raise RuntimeError("Browser not started. Call start() first.")

        logger.info("Navigating to: %s", url)
        await self._page.goto(url, wait_until=wait_until)

        # Screenshot after navigation
        if self.config.screenshot_on_action and self.config.audit_dir:
            await self.screenshot("navigate_" + urlparse(url).netloc.replace(".", "_"))

        return self._page

    async def screenshot(self, name: str = "screenshot") -> Path:
        """Take a screenshot and save to audit directory."""
        if not self._page or not self.config.audit_dir:
            return Path("")

        self.config.audit_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        path = self.config.audit_dir / "screenshots" / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        await self._page.screenshot(path=str(path), full_page=True)
        logger.debug("Screenshot saved: %s", path)
        return path

    async def get_page_content(self) -> str:
        """Get current page HTML content."""
        if not self._page:
            raise RuntimeError("No active page")
        return cast(str, await self._page.content())

    async def wait_for_selector(
        self, selector: str, timeout: Optional[int] = None, state: str = "visible"
    ) -> bool:
        """Wait for selector to appear."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            await self._page.wait_for_selector(selector, timeout=timeout, state=state)
            return True
        except TimeoutError:
            return False

    async def fill_field(self, selector: str, value: str, delay: int = 50) -> bool:
        """Fill a form field with human-like typing."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            await self._page.fill(selector, value, timeout=self.config.action_timeout)
            if delay > 0:
                await asyncio.sleep(delay / 1000)
            if self.config.screenshot_on_action and self.config.audit_dir:
                await self.screenshot(
                    f"fill_{selector.replace('[', '').replace(']', '').replace('=', '_')[:50]}"
                )
            return True
        except (TimeoutError, ValueError) as e:
            logger.warning("Failed to fill field %s: %s", selector, e)
            return False

    async def click(self, selector: str, force: bool = False) -> bool:
        """Click an element."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            await self._page.click(selector, force=force, timeout=self.config.action_timeout)
            if self.config.screenshot_on_action and self.config.audit_dir:
                await self.screenshot(
                    f"click_{selector.replace('[', '').replace(']', '').replace('=', '_')[:50]}"
                )
            return True
        except (TimeoutError, ValueError) as e:
            logger.warning("Failed to click %s: %s", selector, e)
            return False

    async def select_option(self, selector: str, value: str) -> bool:
        """Select option from dropdown."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            await self._page.select_option(
                selector, value=value, timeout=self.config.action_timeout
            )
            if self.config.screenshot_on_action and self.config.audit_dir:
                await self.screenshot(
                    f"select_{selector.replace('[', '').replace(']', '').replace('=', '_')[:50]}"
                )
            return True
        except (TimeoutError, ValueError) as e:
            logger.warning("Failed to select option %s: %s", selector, e)
            return False

    async def upload_file(self, selector: str, file_path: Path) -> bool:
        """Upload a file to file input."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            await self._page.set_input_files(selector, str(file_path))
            if self.config.screenshot_on_action and self.config.audit_dir:
                await self.screenshot(f"upload_{file_path.stem}")
            return True
        except (TimeoutError, ValueError, OSError) as e:
            logger.warning("Failed to upload file %s: %s", file_path, e)
            return False

    async def get_text(self, selector: str) -> Optional[str]:
        """Get text content of an element."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            return cast(Optional[str], await self._page.text_content(selector))
        except (TimeoutError, ValueError):
            return None

    async def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get attribute of an element."""
        if not self._page:
            raise RuntimeError("No active page")
        try:
            return cast(Optional[str], await self._page.get_attribute(selector, attribute))
        except (TimeoutError, ValueError):
            return None

    async def evaluate(self, script: str) -> Any:
        """Evaluate JavaScript in page context."""
        if not self._page:
            raise RuntimeError("No active page")
        return await self._page.evaluate(script)

    @property
    def page(self) -> Optional[Page]:
        """Get current page."""
        return self._page

    @property
    def context(self) -> Optional[BrowserContext]:
        """Get browser context."""
        return self._context

    @property
    def is_running(self) -> bool:
        """Check if browser is running."""
        return self._browser is not None and self._browser.is_connected()

    def get_audit_log(self) -> list[dict[str, Any]]:
        """Get current audit log entries."""
        return self._audit_log.copy()
