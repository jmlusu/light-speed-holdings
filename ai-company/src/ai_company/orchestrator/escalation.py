"""
Escalation rules for autonomous coordination.
"""

from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field
from datetime import datetime


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


class EscalationManager:
    def __init__(self, config_path: str = "orchestrator/escalation.yaml"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.rules: List[EscalationRule] = []
        self.events: List[EscalationEvent] = []
        self._load_config()

    def _load_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self.rules = [EscalationRule(**r) for r in data.get("rules", [])]

    def _save_config(self):
        data = {"rules": [r.model_dump() for r in self.rules]}
        with open(self.config_path, "w", encoding="utf-8") as f:
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
        return event

    def get_pending_escalations(self) -> List[EscalationEvent]:
        return [e for e in self.events if not e.resolved]

    def resolve_escalation(self, task_id: str):
        for event in self.events:
            if event.task_id == task_id:
                event.resolved = True

    def list_rules(self) -> List[EscalationRule]:
        return self.rules
