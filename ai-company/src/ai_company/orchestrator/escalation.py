"""
Escalation rules for autonomous coordination.

Security hardening:
- File locking for concurrent access to escalation.yaml
- Atomic writes to prevent corruption
"""

from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from ai_company.utils.file_lock import atomic_write, file_lock

logger = logging.getLogger(__name__)


class EscalationRule(BaseModel):
    id: str
    name: str
    trigger: str
    escalate_to: str
    max_retries: int = 3
    timeout_minutes: int = 30
    enabled: bool = True


class EscalationEvent(BaseModel):
    task_id: str
    rule_id: str
    from_agent: str
    to_agent: str
    reason: str
    timestamp: datetime = Field(default_factory=datetime.now)
    resolved: bool = False


class TimelineEntry(BaseModel):
    time: str
    description: str


class ActionItem(BaseModel):
    id: str
    action: str
    owner: str
    due_date: str = ""
    status: str = "open"


class ImpactAssessment(BaseModel):
    tasks_before: int = 0
    tasks_during: int = 0
    tasks_after: int = 0
    agents_before: int = 0
    agents_during: int = 0
    agents_after: int = 0
    downtime_minutes: int = 0


class Postmortem(BaseModel):
    incident_id: str
    title: str
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    severity: str = "medium"
    affected_agent: str = ""
    department: str = ""
    escalation_rule: str = ""
    duration: str = ""
    status: str = "draft"
    root_cause: str = ""
    impact: ImpactAssessment = Field(default_factory=ImpactAssessment)
    timeline: List[TimelineEntry] = Field(default_factory=list)
    resolution_steps: List[str] = Field(default_factory=list)
    action_items: List[ActionItem] = Field(default_factory=list)
    lessons_learned: List[str] = Field(default_factory=list)
    prevention_measures: List[str] = Field(default_factory=list)
    prepared_by: str = ""
    reviewed_by: str = ""
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())


class EscalationManager:
    def __init__(self, config_path: str = "orchestrator/escalation.yaml"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.rules: List[EscalationRule] = []
        self.events: List[EscalationEvent] = []
        self._load_config()
        self._load_events()

    def _load_config(self):
        if self.config_path.exists():
            with file_lock(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    self.rules = [EscalationRule(**r) for r in data.get("rules", [])]

    def _save_config(self):
        with file_lock(self.config_path):
            data = {"rules": [r.model_dump() for r in self.rules]}
            with atomic_write(self.config_path) as f:
                yaml.dump(data, f, default_flow_style=False)

    def _load_events(self) -> None:
        """Load persisted escalation events from the YAML file."""
        if not self.config_path.exists():
            return
        try:
            with file_lock(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                raw_events = data.get("events", [])
                self.events = [EscalationEvent(**e) for e in raw_events]
        except (yaml.YAMLError, KeyError):
            self.events = []

    def _save_events(self) -> None:
        """Persist escalation events back to the YAML file."""
        with file_lock(self.config_path):
            if self.config_path.exists():
                try:
                    with open(self.config_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                except (yaml.YAMLError, OSError):
                    data = {}
            else:
                data = {}

            data["events"] = [
                {
                    **e.model_dump(),
                    "timestamp": e.timestamp.isoformat()
                    if isinstance(e.timestamp, datetime)
                    else str(e.timestamp),
                }
                for e in self.events
            ]

            with atomic_write(self.config_path) as f:
                yaml.dump(data, f, default_flow_style=False)

    def add_rule(
        self,
        rule_id: str,
        name: str,
        trigger: str,
        escalate_to: str,
        max_retries: int = 3,
        timeout_minutes: int = 30,
    ) -> EscalationRule:
        rule = EscalationRule(
            id=rule_id,
            name=name,
            trigger=trigger,
            escalate_to=escalate_to,
            max_retries=max_retries,
            timeout_minutes=timeout_minutes,
        )
        self.rules.append(rule)
        self._save_config()
        return rule

    def remove_rule(self, rule_id: str) -> bool:
        original_len = len(self.rules)
        self.rules = [r for r in self.rules if r.id != rule_id]
        if len(self.rules) < original_len:
            self._save_config()
            return True
        return False

    def trigger_escalation(
        self,
        task_id: str,
        rule_id: str,
        from_agent: str,
        reason: str,
    ) -> Optional[EscalationEvent]:
        rule = next((r for r in self.rules if r.id == rule_id), None)
        if not rule:
            return None

        event = EscalationEvent(
            task_id=task_id,
            rule_id=rule_id,
            from_agent=from_agent,
            to_agent=rule.escalate_to,
            reason=reason,
        )
        self.events.append(event)
        self._save_events()
        return event

    def get_pending_escalations(self) -> List[EscalationEvent]:
        return [e for e in self.events if not e.resolved]

    def resolve_escalation(self, task_id: str):
        for event in self.events:
            if event.task_id == task_id:
                event.resolved = True
        self._save_events()

    def list_rules(self) -> List[EscalationRule]:
        return self.rules

    def get_event(self, task_id: str) -> Optional[EscalationEvent]:
        return next((e for e in self.events if e.task_id == task_id), None)


class PostmortemStore:
    """Stores and retrieves postmortems as JSON files.

    Security hardening:
    - File locking for concurrent access
    - Atomic writes to prevent corruption
    """

    def __init__(self, storage_dir: str = "orchestrator/postmortems"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, postmortem: Postmortem) -> Path:
        path = self.storage_dir / f"{postmortem.incident_id}.json"
        with file_lock(path):
            with atomic_write(path) as f:
                f.write(postmortem.model_dump_json(indent=2))
        return path

    def load(self, incident_id: str) -> Optional[Postmortem]:
        path = self.storage_dir / f"{incident_id}.json"
        if not path.exists():
            return None
        with file_lock(path):
            with open(path, "r", encoding="utf-8") as f:
                return Postmortem.model_validate_json(f.read())

    def list_all(self) -> List[Postmortem]:
        postmortems: List[Postmortem] = []
        for path in sorted(self.storage_dir.glob("*.json")):
            try:
                with file_lock(path):
                    with open(path, "r", encoding="utf-8") as f:
                        postmortems.append(Postmortem.model_validate_json(f.read()))
            except (OSError, ValueError) as exc:
                logger.warning("Failed to load postmortem %s: %s", path, exc)
        return postmortems

    def create_from_escalation(
        self,
        event: EscalationEvent,
        rule: Optional[EscalationRule] = None,
        title: str = "",
    ) -> Postmortem:
        """Create a postmortem skeleton from an escalation event."""
        now = datetime.now()
        postmortem = Postmortem(
            incident_id=f"INC-{event.task_id}",
            title=title or f"Incident: {event.reason}",
            severity="medium",
            affected_agent=event.from_agent,
            escalation_rule=event.rule_id if rule is None else rule.name,
            status="draft",
            root_cause="To be determined during investigation.",
            timeline=[
                TimelineEntry(
                    time=event.timestamp.isoformat() if isinstance(event.timestamp, datetime) else str(event.timestamp),
                    description=f"Escalation triggered: {event.reason}",
                ),
                TimelineEntry(
                    time=now.isoformat(),
                    description="Postmortem initiated.",
                ),
            ],
            resolution_steps=["Investigate root cause", "Implement fix", "Verify resolution"],
            prepared_by=event.to_agent,
        )
        self.save(postmortem)
        return postmortem
