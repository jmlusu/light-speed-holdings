"""Tests for dummy data detection in the task pipeline.

Verifies that known dummy-data anti-patterns are caught by validation:
  - Short IDs (t1, t2, etc.)
  - Trivial instructions ("do x", "test", etc.)
  - Single-letter agent names ("a", "b")
  - Proper tasks pass validation
"""

from __future__ import annotations

import re

import pytest


# ═══════════════════════════════════════════════════════════════════════
# Detection patterns (mirrors the production regex in api.py)
# ═══════════════════════════════════════════════════════════════════════


TRIVIAL_INSTRUCTION_RE = re.compile(r"^(do [a-z]|test|.{0,5})$", re.IGNORECASE)

SHORT_ID_RE = re.compile(r"^[a-z]\d+$", re.IGNORECASE)  # e.g. "t1", "t2", "a1"

SINGLE_LETTER_NAME_RE = re.compile(r"^[a-z]$", re.IGNORECASE)  # e.g. "a", "b"


# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════


def is_trivial_instruction(instruction: str) -> bool:
    """Return True if the instruction matches a dummy-data pattern."""
    return bool(TRIVIAL_INSTRUCTION_RE.match(instruction.strip()))


def is_short_id(task_id: str) -> bool:
    """Return True if the task ID matches the short dummy pattern (e.g. t1, a2)."""
    return bool(SHORT_ID_RE.match(task_id.strip()))


def is_single_letter_name(name: str) -> bool:
    """Return True if the agent name is a single letter."""
    return bool(SINGLE_LETTER_NAME_RE.match(name.strip()))


# ═══════════════════════════════════════════════════════════════════════
# Short ID Detection Tests
# ═══════════════════════════════════════════════════════════════════════


class TestShortIdDetection:
    """Verify detection of dummy task IDs like t1, t2, a1."""

    @pytest.mark.parametrize("dummy_id", ["t1", "t2", "t3", "a1", "b2", "x9"])
    def test_detects_short_dummy_ids(self, dummy_id: str) -> None:
        assert is_short_id(dummy_id) is True

    @pytest.mark.parametrize(
        "real_id",
        [
            "550e8400-e29b-41d4-a716-446655440000",  # UUID
            "task-abc-123",
            "lead-backend-task-001",
            "review-pr-42",
        ],
    )
    def test_rejects_real_ids(self, real_id: str) -> None:
        assert is_short_id(real_id) is False


# ═══════════════════════════════════════════════════════════════════════
# Trivial Instruction Detection Tests
# ═══════════════════════════════════════════════════════════════════════


class TestTrivialInstructionDetection:
    """Verify detection of placeholder instructions."""

    @pytest.mark.parametrize(
        "trivial",
        [
            "do x",
            "do y",
            "do z",
            "test",
            "hello",
            "a",
            "ok",
        ],
    )
    def test_detects_trivial_instructions(self, trivial: str) -> None:
        assert is_trivial_instruction(trivial) is True

    @pytest.mark.parametrize(
        "meaningful",
        [
            "Build the REST API for task management",
            "Implement WebSocket broadcast layer",
            "Review PR #42 and merge if CI passes",
            "Deploy to staging and run smoke tests",
            "Write comprehensive unit tests",
        ],
    )
    def test_rejects_meaningful_instructions(self, meaningful: str) -> None:
        assert is_trivial_instruction(meaningful) is False


# ═══════════════════════════════════════════════════════════════════════
# Single-Letter Agent Name Detection Tests
# ═══════════════════════════════════════════════════════════════════════


class TestSingleLetterNameDetection:
    """Verify detection of single-letter agent names."""

    @pytest.mark.parametrize("letter", ["a", "b", "c", "x", "z", "A", "Z"])
    def test_detects_single_letter_names(self, letter: str) -> None:
        assert is_single_letter_name(letter) is True

    @pytest.mark.parametrize(
        "real_name",
        [
            "lead-backend",
            "chief-of-staff",
            "test-agent",
            "cto",
            "human-ceo",
        ],
    )
    def test_rejects_real_agent_names(self, real_name: str) -> None:
        assert is_single_letter_name(real_name) is False


# ═══════════════════════════════════════════════════════════════════════
# Real Task Validation Tests
# ═══════════════════════════════════════════════════════════════════════


class TestRealTaskValidation:
    """Verify that properly-formed tasks pass all dummy-data checks."""

    @pytest.mark.parametrize(
        "task",
        [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "sender_id": "human-ceo",
                "receiver_id": "lead-backend",
                "instruction": "Implement the paginated API endpoint",
            },
            {
                "id": "task-2025-07-22-001",
                "sender_id": "chief-of-staff",
                "receiver_id": "lead-engineering",
                "instruction": "Run security audit on authentication module",
            },
            {
                "id": "review-pr-42",
                "sender_id": "lead-engineering",
                "receiver_id": "test-agent",
                "instruction": "Review and approve PR #42",
            },
        ],
    )
    def test_real_tasks_pass_validation(self, task: dict) -> None:
        assert is_short_id(task["id"]) is False
        assert is_trivial_instruction(task["instruction"]) is False
        assert is_single_letter_name(task["sender_id"]) is False
        assert is_single_letter_name(task["receiver_id"]) is False
