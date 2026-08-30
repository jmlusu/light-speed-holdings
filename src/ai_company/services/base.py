"""Base service class for all department services.

Provides common infrastructure:
- ServiceResult return type for consistent API
- FileStore for persistence
- MessageBus integration for task creation
- Memory engine integration for recording outcomes
- Audit trail logging for all actions
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar, cast

from ai_company.audit.events import AuditEvent, AuditEventType
from ai_company.audit.writer import AuditWriter
from ai_company.data.database import Database
from ai_company.memory.integration import get_store, init_memory
from ai_company.models.task import Task, TaskPriority
from ai_company.orchestrator.message_bus import MessageBus
from ai_company.store.file_store import FileStore

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class ServiceResult(Generic[T]):
    """Standard return type for all service operations.

    Provides a consistent envelope for success/failure with typed data payload.

    Attributes:
        success: Whether the operation completed without errors.
        data: The payload returned on success (may be ``None``).
        errors: List of human-readable error messages (empty on success).
        metadata: Arbitrary extra context for tracing and debugging.
    """

    success: bool = True
    data: T | None = None
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: T | None = None, **meta: Any) -> ServiceResult[T]:
        """Create a successful result."""
        return cls(success=True, data=data, metadata=meta)

    @classmethod
    def fail(cls, *errors: str, **meta: Any) -> ServiceResult[Any]:
        """Create a failure result."""
        return cls(success=False, errors=list(errors), metadata=meta)


class BaseService:
    """Base class for all department services.

    Provides shared persistence, messaging, audit trail, and memory integration.

    Args:
        department_id: Unique department identifier (e.g. ``"marketing"``).
        bus: Shared MessageBus instance.  If ``None``, a default is created.
        data_dir: Directory for department-specific data files.
        memory_dir: Directory for the memory store.
        audit_path: Path to the JSONL audit log file.
        database: Optional SQLite database for task persistence.
    """

    def __init__(
        self,
        department_id: str,
        bus: MessageBus | None = None,
        data_dir: str | Path = ".",
        memory_dir: str = "memory",
        audit_path: str | Path | None = None,
        database: Database | None = None,
    ) -> None:
        self.department_id = department_id
        self.bus = bus or MessageBus(database=database)
        self._store = FileStore(Path(data_dir) / department_id, backup=True)
        self._memory = get_store() or init_memory(memory_dir)
        # ``None`` audit_path resolves to the root-aware default
        # (``<data root>/.opencode/audit``) inside AuditWriter, so a
        # service created without an explicit path never writes to the CWD.
        self._audit = AuditWriter(audit_path)

    # ── Audit trail ───────────────────────────────────────────────────

    def _audit_log(
        self,
        action: str,
        event_type: AuditEventType = AuditEventType.DELEGATION,
        entity_id: str = "",
        result: dict[str, Any] | None = None,
        severity: str = "info",
        task_id: str = "",
    ) -> None:
        """Write an audit event for this department action."""
        event = AuditEvent(
            event_type=event_type,
            agent_id=f"{self.department_id}-service",
            tool=action,
            args={"entity_id": entity_id, "department": self.department_id},
            result=result or {},
            severity=severity,
            task_id=task_id,
        )
        self._audit.write(event)

    # ── Task creation via MessageBus ──────────────────────────────────

    def create_task(
        self,
        receiver_id: str,
        instruction: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        sender_id: str = "",
    ) -> Task:
        """Create a task in the inbox via MessageBus.

        Returns the created Task for tracking.

        If a pending task with the same instruction and receiver already
        exists, the existing task is returned instead of creating a
        duplicate (idempotency guard).
        """
        sender = sender_id or f"{self.department_id}-service"

        # Idempotency: check for an existing pending task with the same
        # instruction and receiver to prevent duplicates from concurrent
        # calls or retries.
        for existing in self.bus.get_pending_tasks():
            if (
                existing.receiver_id == receiver_id
                and existing.sender_id == sender
                and existing.instruction == instruction
            ):
                logger.info(
                    "[%s] Idempotent hit — returning existing task %s -> %s",
                    self.department_id,
                    existing.id[:8],
                    receiver_id,
                )
                return existing

        task = Task(
            id=str(uuid.uuid4()),
            sender_id=sender,
            receiver_id=receiver_id,
            instruction=instruction,
            priority=priority,
        )
        # Guard: refuse demo/test tasks matching the refined markers
        # (proj-acme-chatbot, 'Test ' instruction prefix, test-/verify- ids).
        # Routing to an agent whose id merely starts with 'test' is NOT a
        # marker — the real ``test-agent`` can legitimately receive work.
        from ai_company.data.task_store import TaskStore

        if TaskStore.is_test_task(task.model_dump()):
            logger.warning("Refusing to create test/demo task (receiver=%s)", receiver_id)
            raise ValueError(
                "Refusing to create test/demo task: instruction matches demo "
                f"marker (receiver={receiver_id!r})"
            )
        self.bus.send_task(task)
        logger.info(
            "[%s] Created task %s -> %s: %s",
            self.department_id,
            task.id[:8],
            receiver_id,
            instruction[:60],
        )
        # Audit the task creation
        self._audit_log(
            action="create_task",
            event_type=AuditEventType.TASK_CREATED,
            result={"task_id": task.id, "receiver": receiver_id},
            task_id=task.id,
        )
        return task

    # ── Memory recording ─────────────────────────────────────────────

    def record_event(self, content: str, tags: list[str] | None = None, **meta: Any) -> None:
        """Record a department event as episodic memory."""
        self._memory.store(
            "episodic",
            content=content,
            agent_id=f"{self.department_id}-service",
            tags=tags or [self.department_id],
            metadata={"department": self.department_id, **meta},
        )

    def record_knowledge(self, topic: str, content: str, tags: list[str] | None = None) -> None:
        """Record departmental knowledge as semantic memory."""
        self._memory.store(
            "semantic",
            content=content,
            agent_id=f"{self.department_id}-service",
            tags=tags or [self.department_id, topic],
        )

    # ── Generic data helpers ──────────────────────────────────────────

    def _load_data(self, filename: str) -> dict[str, Any]:
        """Load department data from a YAML/JSON file."""
        data = self._store.read_json(filename)
        if data is not None:
            return cast(dict[str, Any], data)
        data = self._store.read_yaml(filename)
        if data is not None:
            return cast(dict[str, Any], data)
        return {}

    def _save_data(self, filename: str, data: dict[str, Any]) -> None:
        """Save department data. Uses YAML for .yaml/.yml, JSON otherwise."""
        if filename.endswith((".yaml", ".yml")):
            self._store.write_yaml(filename, data)
        else:
            self._store.write_json(filename, data)

    def get_summary(self) -> dict[str, Any]:
        """Return a summary of the department's current state."""
        return {
            "department": self.department_id,
            "timestamp": datetime.now().isoformat(),
        }
