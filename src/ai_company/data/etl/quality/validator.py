"""Data Quality Validator.

Validates records against schemas and quality rules from the data catalog.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from ai_company.paths import get_project_root

logger = logging.getLogger(__name__)

# Cache for loaded schemas and rules
_schema_cache: dict[str, dict[str, Any]] = {}
_rules_cache: dict[str, list[dict[str, Any]]] = {}


def _load_schema(table: str) -> dict[str, Any] | None:
    """Load JSON schema for a table/asset."""
    if table in _schema_cache:
        return _schema_cache[table]

    # Map table names to schema files
    schema_map = {
        "tasks": "tasks.json",
        "audit_events": "audit_events.json",
        "kpi_values": "kpi_values.json",
        "cost_records": "cost_records.json",
        "cost_aggregations": "cost_aggregations.json",
        "escalation_events": "escalation_events.json",
        "memory_entries": "memory_entries.json",
        "company_kpis": "kpi_values.json",  # Reuse KPI schema
        "agent_performance": "agent_performance_metrics.json",
    }

    schema_file = schema_map.get(table)
    if not schema_file:
        logger.debug("No schema mapped for table: %s", table)
        return None

    schema_path = get_project_root() / "data" / "catalog" / "schemas" / schema_file
    if not schema_path.exists():
        logger.warning("Schema file not found: %s", schema_path)
        return None

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        _schema_cache[table] = schema
        return schema if isinstance(schema, dict) else None
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load schema %s: %s", schema_path, exc)
        return None


def _load_quality_rules() -> list[dict[str, Any]]:
    """Load quality rules from catalog."""
    if "all" in _rules_cache:
        return _rules_cache["all"]

    rules_path = get_project_root() / "data" / "catalog" / "quality_rules.yaml"
    if not rules_path.exists():
        logger.warning("Quality rules file not found: %s", rules_path)
        return []

    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        rules = data.get("quality_rules", [])
        _rules_cache["all"] = rules
        return rules if isinstance(rules, list) else []
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to load quality rules: %s", exc)
        return []


def validate_records(records: list[dict[str, Any]], table: str) -> list[dict[str, Any]]:
    """Validate a list of records against schema and quality rules.

    Args:
        records: List of record dicts to validate
        table: Target table/asset name (for schema/rules lookup)

    Returns:
        List of violation dicts with severity, rule_id, message, record info
    """
    violations: list[dict[str, Any]] = []

    if not records:
        return violations

    # Schema validation
    schema = _load_schema(table)
    if schema:
        for i, record in enumerate(records):
            try:
                jsonschema.validate(record, schema)
            except jsonschema.ValidationError as exc:
                violations.append({
                    "severity": "critical",
                    "rule_id": "schema_validation",
                    "message": f"Schema validation failed: {exc.message}",
                    "record_index": i,
                    "record_id": record.get("id") or record.get("event_id") or record.get("kpi_key") or f"index_{i}",
                    "field": ".".join(str(p) for p in exc.path),
                })

    # Quality rules validation
    rules = _load_quality_rules()
    table_rules = [r for r in rules if r.get("asset") == table]

    for rule in table_rules:
        rule_violations = _apply_quality_rule(records, rule)
        violations.extend(rule_violations)

    return violations


def _apply_quality_rule(records: list[dict[str, Any]], rule: dict[str, Any]) -> list[dict[str, Any]]:
    """Apply a single quality rule to records.

    This is a simplified rule engine that handles common rule types.
    For complex SQL-based rules, use the database-level checks instead.
    """
    violations: list[dict[str, Any]] = []
    rule_id = rule.get("rule_id", "unknown")
    severity = rule.get("category", "medium")

    # Rule type: required_fields
    if "required_fields" in rule:
        required = rule["required_fields"]
        for i, record in enumerate(records):
            missing = [f for f in required if f not in record or record[f] in (None, "", [])]
            if missing:
                violations.append({
                    "severity": severity,
                    "rule_id": rule_id,
                    "message": f"Missing required fields: {missing}",
                    "record_index": i,
                    "record_id": record.get("id") or f"index_{i}",
                    "field": missing[0],
                })

    # Rule type: enum validation
    if "valid_values" in rule and "field" in rule:
        valid = set(rule["valid_values"])
        field = rule["field"]
        # Handle nested field paths like "requests[*].status"
        if "[*]" in field:
            # Array field - would need more complex logic
            pass
        else:
            for i, record in enumerate(records):
                value = record.get(field)
                if value is not None and value not in valid:
                    violations.append({
                        "severity": severity,
                        "rule_id": rule_id,
                        "message": f"Invalid value for {field}: {value} (valid: {valid})",
                        "record_index": i,
                        "record_id": record.get("id") or f"index_{i}",
                        "field": field,
                    })

    # Rule type: non_negative
    if rule.get("check") == "non_negative" and "field" in rule:
        field = rule["field"]
        for i, record in enumerate(records):
            value = record.get(field)
            if value is not None:
                try:
                    if float(value) < 0:
                        violations.append({
                            "severity": severity,
                            "rule_id": rule_id,
                            "message": f"Negative value for {field}: {value}",
                            "record_index": i,
                            "record_id": record.get("id") or f"index_{i}",
                            "field": field,
                        })
                except (ValueError, TypeError):
                    pass

    # Rule type: non_empty
    if rule.get("check") == "non_empty" and "field" in rule:
        field = rule["field"]
        for i, record in enumerate(records):
            value = record.get(field)
            if value is None or value == "":
                violations.append({
                    "severity": severity,
                    "rule_id": rule_id,
                    "message": f"Empty value for required field: {field}",
                    "record_index": i,
                    "record_id": record.get("id") or f"index_{i}",
                    "field": field,
                })

    return violations


def validate_company_kpis(kpi_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate company-level KPI records."""
    violations: list[dict[str, Any]] = []

    for i, record in enumerate(kpi_records):
        # Required fields
        required = ["kpi_id", "name", "current", "target", "unit", "frequency", "owner", "formula", "computed_at"]
        missing = [f for f in required if f not in record]
        if missing:
            violations.append({
                "severity": "critical",
                "rule_id": "company_kpi_required_fields",
                "message": f"Missing required fields: {missing}",
                "record_index": i,
                "record_id": record.get("kpi_id", f"index_{i}"),
            })

        # Current should be numeric or null
        current = record.get("current")
        if current is not None:
            try:
                float(current)
            except (ValueError, TypeError):
                violations.append({
                    "severity": "high",
                    "rule_id": "company_kpi_numeric_current",
                    "message": f"Current value must be numeric: {current}",
                    "record_index": i,
                    "record_id": record.get("kpi_id", f"index_{i}"),
                    "field": "current",
                })

        # Target should be numeric
        target = record.get("target")
        if target is not None:
            try:
                float(target)
            except (ValueError, TypeError):
                violations.append({
                    "severity": "high",
                    "rule_id": "company_kpi_numeric_target",
                    "message": f"Target value must be numeric: {target}",
                    "record_index": i,
                    "record_id": record.get("kpi_id", f"index_{i}"),
                    "field": "target",
                })

        # Formula should be descriptive
        formula = record.get("formula", "")
        if len(formula) < 10:
            violations.append({
                "severity": "medium",
                "rule_id": "company_kpi_formula_descriptive",
                "message": f"Formula too short, should describe computation: {formula}",
                "record_index": i,
                "record_id": record.get("kpi_id", f"index_{i}"),
                "field": "formula",
            })

    return violations


def validate_department_kpis(kpi_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Validate department KPI records."""
    violations: list[dict[str, Any]] = []

    valid_frequencies = {"daily", "weekly", "monthly", "quarterly", "per_request", "per_item"}
    valid_units = {"%", "percent", "$", "usd", "count", "score", "minutes", "hours", "days", "campaigns", "count"}

    for i, record in enumerate(kpi_records):
        required = ["kpi_id", "name", "target", "unit", "frequency"]
        missing = [f for f in required if f not in record or record[f] is None]
        if missing:
            violations.append({
                "severity": "high",
                "rule_id": "dept_kpi_required_fields",
                "message": f"Missing required fields: {missing}",
                "record_index": i,
                "record_id": record.get("kpi_id", f"index_{i}"),
            })

        freq = record.get("frequency")
        if freq and freq not in valid_frequencies:
            violations.append({
                "severity": "medium",
                "rule_id": "dept_kpi_valid_frequency",
                "message": f"Invalid frequency: {freq} (valid: {valid_frequencies})",
                "record_index": i,
                "record_id": record.get("kpi_id", f"index_{i}"),
                "field": "frequency",
            })

        unit = record.get("unit")
        if unit and unit not in valid_units:
            violations.append({
                "severity": "low",
                "rule_id": "dept_kpi_valid_unit",
                "message": f"Unusual unit: {unit} (expected one of {valid_units})",
                "record_index": i,
                "record_id": record.get("kpi_id", f"index_{i}"),
                "field": "unit",
            })

    return violations


__all__ = [
    "validate_records",
    "validate_company_kpis",
    "validate_department_kpis",
]