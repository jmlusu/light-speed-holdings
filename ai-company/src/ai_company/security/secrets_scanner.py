"""Secrets scanning for CI/CD and pre-commit hooks.

Scans code changes and files for leaked secrets including:
- API keys and tokens
- Passwords and credentials
- Private keys
- Connection strings
- Configuration files with sensitive data

Security features:
- Pattern-based detection with entropy analysis
- Pre-commit hook support
- CI/CD integration
- Configurable allowlist for false positives
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

# Security audit logger
_security_logger = logging.getLogger("ai_company.security.secrets_scanner")


@dataclass
class SecretMatch:
    """A detected secret in the code."""
    file_path: str
    line_number: int
    line_content: str
    secret_type: str
    matched_text: str
    severity: str = "high"


@dataclass
class ScanResult:
    """Result of secrets scanning."""
    files_scanned: int = 0
    secrets_found: list[SecretMatch] = field(default_factory=list)
    clean: bool = True

    @property
    def total_secrets(self) -> int:
        return len(self.secrets_found)

    @property
    def high_severity_count(self) -> int:
        return sum(1 for s in self.secrets_found if s.severity == "high")


class SecretsScanner:
    """Scans files for leaked secrets and credentials.

    Usage:
        scanner = SecretsScanner()
        result = scanner.scan_directory(Path("src"))
        if not result.clean:
            raise SecurityError("Secrets detected!")
    """

    # Secret patterns with severity levels
    SECRET_PATTERNS: dict[str, tuple[re.Pattern, str]] = {
        # API Keys
        "aws_access_key": (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "high"),
        "aws_secret_key": (re.compile(r"(?:aws_secret_access_key|secret_key)[=:]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?", re.IGNORECASE), "high"),
        "github_token": (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "high"),
        "github_fine_grained": (re.compile(r"\bgithub_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59}\b"), "high"),
        "openai_key": (re.compile(r"\bsk-[A-Za-z0-9]{48}\b"), "high"),
        "anthropic_key": (re.compile(r"\bsk-ant-[A-Za-z0-9]{48}\b"), "high"),
        "stripe_key": (re.compile(r"\b(?:sk|pk)_(?:test|live)_[A-Za-z0-9]{24,}\b"), "high"),
        "google_api_key": (re.compile(r"\bAIza[A-Za-z0-9_-]{35}\b"), "high"),

        # Generic API keys (high entropy strings assigned to key-like variables)
        "generic_api_key": (re.compile(r"(?:api[_-]?key|apikey|api[_-]?secret)[=:]\s*['\"]?[A-Za-z0-9]{20,}['\"]?", re.IGNORECASE), "medium"),

        # Passwords
        "password_assignment": (re.compile(r"(?:password|passwd|pwd)[=:]\s*['\"]?[^\s'\"]{8,}['\"]?", re.IGNORECASE), "high"),
        "password_in_url": (re.compile(r"://[^:]+:[^@]+@"), "high"),

        # Private keys
        "private_key": (re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"), "critical"),

        # Connection strings
        "database_url": (re.compile(r"(?:mysql|postgresql|mongodb|redis):\/\/[^\s'\"]+", re.IGNORECASE), "high"),
        "connection_string": (re.compile(r"(?:Server|Data Source)=(?:[^\s;]+;?)+", re.IGNORECASE), "high"),

        # JWT tokens
        "jwt_token": (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\b"), "high"),

        # Slack/Discord tokens
        "slack_token": (re.compile(r"\bxox[bpsar]-[0-9]{10,}-[A-Za-z0-9-]+\b"), "high"),
        "discord_token": (re.compile(r"\b[A-Za-z0-9_-]{24}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}\b"), "high"),
    }

    # Files to always skip
    SKIP_FILES: set[str] = {
        ".env.example",
        "package-lock.json",
        "yarn.lock",
        "poetry.lock",
        "Pipfile.lock",
    }

    # Directories to skip
    SKIP_DIRS: set[str] = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        "env",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        "dist",
        "build",
        "*.egg-info",
    }

    # Allowlist patterns (false positives)
    ALLOWLIST_PATTERNS: list[re.Pattern] = [
        re.compile(r"example\.com"),
        re.compile(r"test[_-]?key"),
        re.compile(r"placeholder"),
        re.compile(r"xxx+"),
        re.compile(r"dummy"),
        re.compile(r"<.*>"),  # Template placeholders
        re.compile(r"your[_-]?api[_-]?key"),
        re.compile(r"REPLACE_ME"),
    ]

    def __init__(
        self,
        scan_secrets: bool = True,
        scan_env_files: bool = True,
        check_entropy: bool = True,
    ) -> None:
        self.scan_secrets = scan_secrets
        self.scan_env_files = scan_env_files
        self.check_entropy = check_entropy

    def scan_file(self, file_path: Path) -> list[SecretMatch]:
        """Scan a single file for secrets.

        Args:
            file_path: Path to the file to scan.

        Returns:
            List of detected secrets.
        """
        matches: list[SecretMatch] = []

        # Skip certain files
        if file_path.name in self.SKIP_FILES:
            return matches

        # Skip binary files
        if self._is_binary(file_path):
            return matches

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeDecodeError) as exc:
            logger.debug("Could not read %s: %s", file_path, exc)
            return matches

        lines = content.splitlines()

        for line_num, line in enumerate(lines, 1):
            # Check against all secret patterns
            for secret_type, (pattern, severity) in self.SECRET_PATTERNS.items():
                for match in pattern.finditer(line):
                    matched_text = match.group()

                    # Check allowlist
                    if self._is_allowlisted(matched_text, line):
                        continue

                    # Optional entropy check for generic patterns
                    if self.check_entropy and secret_type == "generic_api_key":
                        if not self._has_high_entropy(matched_text):
                            continue

                    matches.append(SecretMatch(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line.strip()[:200],
                        secret_type=secret_type,
                        matched_text=matched_text[:50] + "..." if len(matched_text) > 50 else matched_text,
                        severity=severity,
                    ))

        return matches

    def scan_directory(
        self,
        directory: Path,
        include_hidden: bool = False,
    ) -> ScanResult:
        """Scan an entire directory for secrets.

        Args:
            directory: Root directory to scan.
            include_hidden: Whether to include hidden directories.

        Returns:
            ScanResult with all detected secrets.
        """
        result = ScanResult()

        for root, dirs, files in os.walk(directory):
            root_path = Path(root)

            # Skip directories
            dirs[:] = [
                d for d in dirs
                if d not in self.SKIP_DIRS
                and (include_hidden or not d.startswith("."))
            ]

            # Also filter out directories matching glob patterns
            dirs[:] = [
                d for d in dirs
                if not any(
                    Path(d).match(pattern)
                    for pattern in self.SKIP_DIRS
                    if "*" in pattern
                )
            ]

            for file_name in files:
                file_path = root_path / file_name
                result.files_scanned += 1

                file_matches = self.scan_file(file_path)
                result.secrets_found.extend(file_matches)

        result.clean = result.total_secrets == 0
        return result

    def scan_diff(self, diff_content: str) -> list[SecretMatch]:
        """Scan a git diff for secrets in added lines.

        Args:
            diff_content: Git diff output.

        Returns:
            List of secrets found in added lines.
        """
        matches: list[SecretMatch] = []
        current_file = ""
        line_num = 0

        for line in diff_content.splitlines():
            # Track current file
            if line.startswith("+++ b/"):
                current_file = line[6:]
                continue

            # Parse added lines
            if line.startswith("+") and not line.startswith("+++"):
                line_num += 1
                content = line[1:]  # Remove the + prefix

                for secret_type, (pattern, severity) in self.SECRET_PATTERNS.items():
                    for match in pattern.finditer(content):
                        matched_text = match.group()

                        if self._is_allowlisted(matched_text, content):
                            continue

                        matches.append(SecretMatch(
                            file_path=current_file,
                            line_number=line_num,
                            line_content=content.strip()[:200],
                            secret_type=secret_type,
                            matched_text=matched_text[:50] + "..." if len(matched_text) > 50 else matched_text,
                            severity=severity,
                        ))

        return matches

    def _is_binary(self, file_path: Path) -> bool:
        """Check if a file is binary."""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(8192)
            # Check for null bytes
            return b"\x00" in chunk
        except OSError:
            return True

    def _is_allowlisted(self, matched_text: str, line: str) -> bool:
        """Check if a match is in the allowlist (false positive)."""
        for pattern in self.ALLOWLIST_PATTERNS:
            if pattern.search(matched_text) or pattern.search(line):
                return True
        return False

    def _has_high_entropy(self, text: str) -> bool:
        """Check if text has high entropy (likely a real secret)."""
        import math
        from collections import Counter

        # Remove common low-entropy prefixes
        text = re.sub(r"['\"]", "", text)
        text = text.lower()

        if len(text) < 16:
            return False

        # Calculate Shannon entropy
        counter = Counter(text)
        length = len(text)
        entropy = -sum(
            (count / length) * math.log2(count / length)
            for count in counter.values()
        )

        # High entropy threshold (4.0+ indicates randomness)
        return entropy >= 4.0


def scan_for_secrets(
    path: str | Path,
    include_hidden: bool = False,
) -> ScanResult:
    """Convenience function to scan a path for secrets.

    Args:
        path: File or directory path to scan.
        include_hidden: Whether to include hidden directories.

    Returns:
        ScanResult with findings.
    """
    scanner = SecretsScanner()
    target = Path(path)

    if target.is_file():
        result = ScanResult(files_scanned=1)
        result.secrets_found = scanner.scan_file(target)
        result.clean = result.total_secrets == 0
        return result
    elif target.is_dir():
        return scanner.scan_directory(target, include_hidden)
    else:
        logger.error("Path does not exist: %s", target)
        return ScanResult()


def run_pre_commit_scan() -> bool:
    """Run secrets scan as a pre-commit hook.

    Returns:
        True if clean (safe to commit), False if secrets detected.
    """
    scanner = SecretsScanner()

    # Get staged files from git
    try:
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        files = result.stdout.strip().split("\n")
    except (subprocess.SubprocessError, FileNotFoundError) as exc:
        logger.error("Failed to get git staged files: %s", exc)
        return True  # Allow commit if git fails

    total_secrets = 0
    for file_name in files:
        if not file_name:
            continue
        file_path = Path(file_name)
        if file_path.exists():
            matches = scanner.scan_file(file_path)
            total_secrets += len(matches)
            for match in matches:
                print(
                    f"  [SECRETS] {match.file_path}:{match.line_number} "
                    f"- {match.secret_type}: {match.matched_text}"
                )

    if total_secrets > 0:
        print(f"\n[SECRETS SCAN FAILED] Found {total_secrets} potential secrets.")
        print("Please remove secrets before committing.")
        _security_logger.warning(
            "Pre-commit scan detected %d secrets", total_secrets
        )
        return False

    return True


# Hook script for pre-commit
PRE_COMMIT_HOOK = """#!/bin/bash
# AI Company Builder - Pre-commit Secrets Scanner
# Add this to .git/hooks/pre-commit

python -c "from ai_company.security.secrets_scanner import run_pre_commit_scan; import sys; sys.exit(0 if run_pre_commit_scan() else 1)"
"""
