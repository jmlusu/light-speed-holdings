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
        board_ids = {b.id for b in r.board}
        for ex in r.executives:
            if ex.reports_to and ex.reports_to not in exec_ids and ex.reports_to not in board_ids:
                errors.append(
                    f"Executive '{ex.id}' reports_to '{ex.reports_to}' not found in executives or board"
                )
        return errors

    def _check_departments(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.departments:
            errors.append("No departments defined")
        exec_ids = {e.id for e in r.executives}
        for dept in r.departments:
            if dept.executive and dept.executive not in exec_ids:
                errors.append(
                    f"Department '{dept.id}' executive '{dept.executive}' not found in executives"
                )
        return errors

    def _check_specialists(self, r: CompanyRegistry) -> list[str]:
        errors: list[str] = []
        if not r.specialists:
            errors.append("No specialist agents defined")
        exec_ids = {e.id for e in r.executives}
        spec_ids = {s.id for s in r.specialists}
        valid_reports_to = exec_ids | spec_ids
        for spec in r.specialists:
            if spec.reports_to and spec.reports_to not in valid_reports_to:
                errors.append(
                    f"Specialist '{spec.id}' reports_to '{spec.reports_to}' not found in executives or specialists"
                )
            if spec.department:
                dept_ids = {d.id for d in r.departments}
                if spec.department not in dept_ids:
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
