"""Data Quality Alerting.

Alert generation and notification for data quality issues.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from ai_company.audit.integration import get_writer
from ai_company.audit.events import AuditEvent, AuditEventType

logger = logging.getLogger(__name__)


class QualityAlert:
    """Represents a data quality alert."""

    def __init__(
        self,
        rule_id: str,
        severity: str,
        message: str,
        asset: str,
        details: dict[str, Any] | None = None,
    ):
        self.rule_id = rule_id
        self.severity = severity  # critical, high, medium, low
        self.message = message
        self.asset = asset
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.alert_id = f"{asset}_{rule_id}_{int(datetime.now().timestamp())}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "asset": self.asset,
            "details": self.details,
            "timestamp": self.timestamp,
        }

    def to_audit_event(self) -> AuditEvent:
        """Convert to audit event for logging."""
        return AuditEvent(
            event_type=AuditEventType.DATA_QUALITY_ALERT,
            agent_id="data_quality_monitor",
            tool="quality.check",
            metadata=self.to_dict(),
            severity=self.severity,
        )


class AlertManager:
    """Manages quality alerts: deduplication and audit logging.

    Note: Escalation and notification are not yet implemented.
    """

    def __init__(self, database=None):
        self.database = database
        self._active_alerts: dict[str, QualityAlert] = {}
        self._alert_history: list[QualityAlert] = []
        self._dedup_window_hours = 24

    def raise_alert(self, alert: QualityAlert) -> bool:
        """Raise an alert, handling deduplication.

        Returns True if alert was raised (not deduplicated).
        """
        # Simple deduplication key
        dedup_key = f"{alert.asset}_{alert.rule_id}"

        # Check if similar alert was raised recently
        if dedup_key in self._active_alerts:
            existing = self._active_alerts[dedup_key]
            # Update timestamp but don't re-notify
            existing.timestamp = alert.timestamp
            return False

        # New alert
        self._active_alerts[dedup_key] = alert
        self._alert_history.append(alert)

        # Emit to audit log
        self._emit_audit(alert)

        logger.warning(
            "Quality alert [%s]: %s - %s", alert.severity.upper(), alert.asset, alert.message
        )
        return True

    def raise_from_violations(self, violations: list[dict[str, Any]], asset: str) -> int:
        """Raise alerts from a list of validation violations."""
        raised = 0
        for v in violations:
            alert = QualityAlert(
                rule_id=v.get("rule_id", "unknown"),
                severity=v.get("severity", "medium"),
                message=v.get("message", "Quality violation"),
                asset=asset,
                details=v,
            )
            if self.raise_alert(alert):
                raised += 1
        return raised

    def resolve_alert(self, rule_id: str, asset: str) -> bool:
        """Mark an alert as resolved."""
        dedup_key = f"{asset}_{rule_id}"
        if dedup_key in self._active_alerts:
            del self._active_alerts[dedup_key]
            logger.info("Quality alert resolved: %s", dedup_key)
            return True
        return False

    def get_active_alerts(self, severity: str | None = None) -> list[QualityAlert]:
        """Get currently active alerts."""
        alerts = list(self._active_alerts.values())
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return sorted(alerts, key=lambda a: a.timestamp, reverse=True)

    def get_alert_summary(self) -> dict[str, Any]:
        """Get summary of alert state."""
        active = list(self._active_alerts.values())
        by_severity: dict[str, int] = {}
        for a in active:
            by_severity[a.severity] = by_severity.get(a.severity, 0) + 1

        return {
            "active_count": len(active),
            "by_severity": by_severity,
            "total_raised": len(self._alert_history),
            "assets_affected": len(set(a.asset for a in active)),
        }

    def _emit_audit(self, alert: QualityAlert) -> None:
        """Emit alert to audit log."""
        try:
            writer = get_writer()
            if writer:
                writer.write(alert.to_audit_event())
        except Exception:  # noqa: BLE001
            logger.debug("Audit emission failed for alert", exc_info=True)


# Global alert manager instance
_alert_manager: AlertManager | None = None


def get_alert_manager() -> AlertManager:
    """Get the global alert manager instance."""
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager


def alert_on_quality_failure(asset: str, violations: list[dict[str, Any]]) -> int:
    """Convenience function to raise alerts from validation violations."""
    return get_alert_manager().raise_from_violations(violations, asset)


__all__ = [
    "QualityAlert",
    "AlertManager",
    "get_alert_manager",
    "alert_on_quality_failure",
]
