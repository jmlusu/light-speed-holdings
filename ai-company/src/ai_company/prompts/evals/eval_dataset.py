"""Test case dataset for prompt evaluation.

Each test case defines:
- A prompt scenario (agent type + task)
- Expected output characteristics (format, structure, key content)
- Scoring criteria

Test cases are organised by agent type and difficulty level.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Difficulty(Enum):
    """Test case difficulty levels."""

    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EDGE_CASE = "edge_case"


class AgentType(Enum):
    """Agent types for which we evaluate prompts."""

    EXECUTIVE = "Executive"
    SPECIALIST = "Specialist"
    BOARD = "Board"
    DEPARTMENT = "Department"


@dataclass
class ExpectedFormat:
    """What the output should look like structurally."""

    must_contain_json: bool = True
    must_have_thought: bool = True
    must_have_plan: bool = True
    must_have_result: bool = True
    must_have_done: bool = True
    plan_must_use_tools: list[str] = field(default_factory=list)
    max_output_tokens: int = 4096
    must_not_contain: list[str] = field(default_factory=list)


@dataclass
class EvalTestCase:
    """A single evaluation test case."""

    id: str
    name: str
    agent_type: AgentType
    difficulty: Difficulty
    task_instruction: str
    system_prompt: str
    expected: ExpectedFormat
    tags: list[str] = field(default_factory=list)
    description: str = ""


# ---------------------------------------------------------------------------
# Executive test cases
# ---------------------------------------------------------------------------

EXECUTIVE_TEST_CASES: list[EvalTestCase] = [
    EvalTestCase(
        id="exec-001",
        name="Simple delegation",
        agent_type=AgentType.EXECUTIVE,
        difficulty=Difficulty.EASY,
        task_instruction="Delegate a code review task to the lead-backend specialist.",
        system_prompt="",  # Filled at runtime from prompts.py
        expected=ExpectedFormat(
            plan_must_use_tools=["delegate"],
            must_contain_json=True,
        ),
        tags=["delegation", "basic"],
    ),
    EvalTestCase(
        id="exec-002",
        name="Multi-step strategy",
        agent_type=AgentType.EXECUTIVE,
        difficulty=Difficulty.MEDIUM,
        task_instruction=(
            "Review the current sprint status, identify blockers, "
            "and create an action plan with delegations."
        ),
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["read", "delegate"],
            must_contain_json=True,
        ),
        tags=["strategy", "multi-step"],
    ),
    EvalTestCase(
        id="exec-003",
        name="Crisis escalation",
        agent_type=AgentType.EXECUTIVE,
        difficulty=Difficulty.HARD,
        task_instruction=(
            "A critical production bug has been reported. The database is returning "
            "incorrect data for all users. What do you do?"
        ),
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["delegate", "read"],
            must_contain_json=True,
        ),
        tags=["crisis", "escalation"],
    ),
    EvalTestCase(
        id="exec-004",
        name="Ambiguous task",
        agent_type=AgentType.EXECUTIVE,
        difficulty=Difficulty.EDGE_CASE,
        task_instruction="Make things better.",
        system_prompt="",
        expected=ExpectedFormat(must_contain_json=True),
        tags=["ambiguous", "edge-case"],
    ),
]

# ---------------------------------------------------------------------------
# Specialist test cases
# ---------------------------------------------------------------------------

SPECIALIST_TEST_CASES: list[EvalTestCase] = [
    EvalTestCase(
        id="spec-001",
        name="Read and modify file",
        agent_type=AgentType.SPECIALIST,
        difficulty=Difficulty.EASY,
        task_instruction="Read src/main.py and add a comment at the top of the file.",
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["read", "write"],
            must_contain_json=True,
        ),
        tags=["file-edit", "basic"],
    ),
    EvalTestCase(
        id="spec-002",
        name="Run tests and fix failures",
        agent_type=AgentType.SPECIALIST,
        difficulty=Difficulty.MEDIUM,
        task_instruction="Run the test suite and fix any failing tests.",
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["execute"],
            must_contain_json=True,
        ),
        tags=["testing", "multi-step"],
    ),
    EvalTestCase(
        id="spec-003",
        name="Search and refactor",
        agent_type=AgentType.SPECIALIST,
        difficulty=Difficulty.HARD,
        task_instruction=(
            "Find all uses of deprecated function 'old_api()' in the codebase "
            "and replace them with 'new_api()'."
        ),
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["grep", "read", "write"],
            must_contain_json=True,
        ),
        tags=["refactor", "search"],
    ),
    EvalTestCase(
        id="spec-004",
        name="File not found recovery",
        agent_type=AgentType.SPECIALIST,
        difficulty=Difficulty.EDGE_CASE,
        task_instruction="Edit the file config/settings.py to add a new setting.",
        system_prompt="",
        expected=ExpectedFormat(must_contain_json=True),
        tags=["error-recovery", "edge-case"],
    ),
]

# ---------------------------------------------------------------------------
# Board test cases
# ---------------------------------------------------------------------------

BOARD_TEST_CASES: list[EvalTestCase] = [
    EvalTestCase(
        id="board-001",
        name="Review strategy document",
        agent_type=AgentType.BOARD,
        difficulty=Difficulty.EASY,
        task_instruction="Review the Q4 strategy document and provide your assessment.",
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["read"],
            must_contain_json=True,
        ),
        tags=["review", "basic"],
    ),
    EvalTestCase(
        id="board-002",
        name="Governance check",
        agent_type=AgentType.BOARD,
        difficulty=Difficulty.MEDIUM,
        task_instruction=(
            "Review the company's AI ethics policy and recommend improvements "
            "based on industry best practices."
        ),
        system_prompt="",
        expected=ExpectedFormat(must_contain_json=True),
        tags=["governance", "ethics"],
    ),
]

# ---------------------------------------------------------------------------
# Department test cases
# ---------------------------------------------------------------------------

DEPARTMENT_TEST_CASES: list[EvalTestCase] = [
    EvalTestCase(
        id="dept-001",
        name="Weekly status report",
        agent_type=AgentType.DEPARTMENT,
        difficulty=Difficulty.EASY,
        task_instruction="Generate a weekly status report for the engineering department.",
        system_prompt="",
        expected=ExpectedFormat(must_contain_json=True),
        tags=["reporting", "basic"],
    ),
    EvalTestCase(
        id="dept-002",
        name="Team coordination",
        agent_type=AgentType.DEPARTMENT,
        difficulty=Difficulty.MEDIUM,
        task_instruction=(
            "Coordinate the team to deliver the new API feature by Friday. "
            "Identify who should work on what."
        ),
        system_prompt="",
        expected=ExpectedFormat(
            plan_must_use_tools=["delegate"],
            must_contain_json=True,
        ),
        tags=["coordination", "planning"],
    ),
]

# ---------------------------------------------------------------------------
# Dataset access
# ---------------------------------------------------------------------------

ALL_TEST_CASES: list[EvalTestCase] = (
    EXECUTIVE_TEST_CASES
    + SPECIALIST_TEST_CASES
    + BOARD_TEST_CASES
    + DEPARTMENT_TEST_CASES
)


def get_test_cases(
    agent_type: AgentType | None = None,
    difficulty: Difficulty | None = None,
    tags: list[str] | None = None,
) -> list[EvalTestCase]:
    """Filter test cases by agent type, difficulty, or tags."""
    result = ALL_TEST_CASES

    if agent_type is not None:
        result = [tc for tc in result if tc.agent_type == agent_type]

    if difficulty is not None:
        result = [tc for tc in result if tc.difficulty == difficulty]

    if tags is not None:
        tag_set = set(tags)
        result = [tc for tc in result if tag_set.intersection(tc.tags)]

    return result
