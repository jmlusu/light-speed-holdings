"""Registry validator — checks CompanyRegistry for structural correctness."""

from __future__ import annotations

from ai_company.models import CompanyRegistry


class RegistryValidator:
    """Validates a parsed CompanyRegistry and returns a list of error strings.

    An empty list means the registry is valid.
    """

    def validate(self, r: CompanyRegistry) -> list[str]:
        """Run all validation checks. Returns list of error messages."""
        errors: list[str] = []
        errors.extend(self._check_company(r))
        errors.extend(self._check_executives(r))
        errors.extend(self._check_departments(r))
        errors.extend(self._check_specialists(r))
        errors.extend(self._check_board(r))
        errors.extend(self._check_workflows(r))
        errors.extend(self._check_budget(r))
        errors.extend(self._check_governance_fields(r))
        return errors

    def _check_governance_fields(self, r: CompanyRegistry) -> list[str]:
        """Fail-fast: every agent must carry the 4 MANDATORY governance fields.

        Fields: decision_rights, approval_level, escalation_path, kpis.
        AI_WORKFORCE_90 §5.1. Empty or missing values are errors.
        """
        errors: list[str] = []
        approval_levels = {"self", "lead", "exec", "ceo", "board"}

        def _check(agent_id: str, obj: object) -> None:
            for field in ("decision_rights", "escalation_path", "kpis"):
                val = getattr(obj, field, None)
                if val is None or val == "" or val == []:
                    errors.append(f"Agent '{agent_id}' missing MANDATORY field '{field}'")
            level = getattr(obj, "approval_level", "")
            if not level:
                errors.append(f"Agent '{agent_id}' missing MANDATORY field 'approval_level'")
            elif level not in approval_levels:
                errors.append(
                    f"Agent '{agent_id}' approval_level '{level}' not in {sorted(approval_levels)}"
                )

        for ex in r.executives:
            _check(ex.id, ex)
        for spec in r.specialists:
            _check(spec.id, spec)
        for bm in r.board:
            _check(bm.id, bm)
        return errors

    def _check_company(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.company.name or r.company.name == "AI Company":
            errors.append("Company name is missing or defaulted")
        if not r.company.id:
            errors.append("Company id is required")
        return errors

    def _check_executives(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.executives:
            errors.append("No executives defined")
        exec_ids = {e.id for e in r.executives}
        for ex in r.executives:
            if ex.reports_to and ex.reports_to not in exec_ids and ex.reports_to != "board":
                errors.append(
                    f"Executive '{ex.id}' reports_to '{ex.reports_to}' not found in executives"
                )
        return errors

    def _check_departments(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.departments:
            errors.append("No departments defined")
        exec_ids = {e.id for e in r.executives}
        spec_ids = {s.id for s in r.specialists}
        valid_executives = exec_ids | spec_ids
        for dept in r.departments:
            if dept.executive and dept.executive not in valid_executives:
                errors.append(
                    f"Department '{dept.id}' executive '{dept.executive}' not found in executives or specialists"
                )
        return errors

    def _check_specialists(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.specialists:
            errors.append("No specialist agents defined")
        exec_ids = {e.id for e in r.executives}
        spec_ids = {s.id for s in r.specialists}
        valid_reports_to = exec_ids | spec_ids
        # Build department lookup: accept both id and display name (case-insensitive)
        dept_ids = {d.id for d in r.departments}
        dept_names = {d.name.lower() for d in r.departments if d.name}
        valid_departments = dept_ids | dept_names
        for spec in r.specialists:
            if spec.reports_to and spec.reports_to not in valid_reports_to:
                errors.append(
                    f"Specialist '{spec.id}' reports_to '{spec.reports_to}' not found in executives or specialists"
                )
            if spec.department and spec.department.lower() not in valid_departments:
                errors.append(
                    f"Specialist '{spec.id}' department '{spec.department}' not found in departments"
                )
        return errors

    def _check_board(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.board:
            errors.append("No board members defined")
        return errors

    def _check_workflows(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        for wf in r.workflows:
            if not wf.steps:
                errors.append(f"Workflow '{wf.id}' has no steps")
        return errors

    def _check_budget(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if r.budget.total_budget <= 0:
            errors.append("Budget total_budget must be > 0")
        return errors
