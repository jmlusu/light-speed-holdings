"""Registry resolver — wires and validates cross-references between entities."""

from __future__ import annotations

from ai_company.models import CompanyRegistry


class ResolutionError(Exception):
    """Raised when cross-reference resolution fails."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("\n".join(errors))


class RegistryResolver:
    """Resolves and validates cross-references in a CompanyRegistry.

    After parsing, entities may reference each other by ID string.
    This resolver ensures consistency:
    - Every executive's department matches a known department ID
    - Every specialist's reports_to references a known agent (executive or specialist)
    - Every department's executive references a known agent
    - Every workflow's owner references a known agent
    - No circular references in reports_to chains
    """

    def resolve(self, registry: CompanyRegistry) -> list[str]:
        """Run all resolution passes on the registry.

        Returns a list of error strings. Empty list means all references are valid.
        """
        errors: list[str] = []
        errors.extend(self._wire_executive_departments(registry))
        errors.extend(self._wire_specialist_reports_to(registry))
        errors.extend(self._wire_department_executives(registry))
        errors.extend(self._wire_workflow_owners(registry))
        errors.extend(self._detect_circular_references(registry))
        return errors

    def _wire_executive_departments(self, r: CompanyRegistry) -> list[str]:
        """Ensure each executive's department matches a known department ID."""
        errors: list[str] = []
        dept_ids = {d.id for d in r.departments}
        for ex in r.executives:
            if ex.department and ex.department not in dept_ids:
                errors.append(
                    f"Executive '{ex.id}' references unknown department '{ex.department}'"
                )
        return errors

    def _wire_specialist_reports_to(self, r: CompanyRegistry) -> list[str]:
        """Ensure each specialist's reports_to references a known agent."""
        errors: list[str] = []
        exec_ids = {e.id for e in r.executives}
        spec_ids = {s.id for s in r.specialists}
        valid_targets = exec_ids | spec_ids | {"board", "human_ceo"}
        for spec in r.specialists:
            if spec.reports_to and spec.reports_to not in valid_targets:
                errors.append(
                    f"Specialist '{spec.id}' reports_to '{spec.reports_to}' not found in executives or specialists"
                )
        return errors

    def _wire_department_executives(self, r: CompanyRegistry) -> list[str]:
        """Ensure each department's executive references a known agent."""
        errors: list[str] = []
        exec_ids = {e.id for e in r.executives}
        spec_ids = {s.id for s in r.specialists}
        valid_executives = exec_ids | spec_ids
        for dept in r.departments:
            if dept.executive and dept.executive not in valid_executives:
                errors.append(
                    f"Department '{dept.id}' executive '{dept.executive}' not found in executives or specialists"
                )
        return errors

    def _wire_workflow_owners(self, r: CompanyRegistry) -> list[str]:
        """Ensure each workflow's owner references a known agent."""
        errors: list[str] = []
        exec_ids = {e.id for e in r.executives}
        spec_ids = {s.id for s in r.specialists}
        board_ids = {b.id for b in r.board}
        valid_owners = exec_ids | spec_ids | board_ids
        for wf in r.workflows:
            if wf.owner and wf.owner not in valid_owners:
                errors.append(
                    f"Workflow '{wf.id}' owner '{wf.owner}' not found in executives, specialists, or board"
                )
            for step in wf.steps:
                if step.owner and step.owner not in valid_owners:
                    errors.append(
                        f"Workflow '{wf.id}' step '{step.id}' owner '{step.owner}' not found in executives, specialists, or board"
                    )
        return errors

    def _detect_circular_references(self, r: CompanyRegistry) -> list[str]:
        """Detect circular references in reports_to chains."""
        errors: list[str] = []

        # Build adjacency map: node -> parent (reports_to)
        reports_to: dict[str, str] = {}

        # Executives can report to other executives, board, or human_ceo
        for ex in r.executives:
            if ex.reports_to:
                reports_to[ex.id] = ex.reports_to

        # Specialists can report to executives or other specialists
        for spec in r.specialists:
            if spec.reports_to:
                reports_to[spec.id] = spec.reports_to

        # Check each node for cycles
        for node_id in reports_to:
            cycle = self._find_cycle(node_id, reports_to)
            if cycle:
                errors.append(
                    f"Circular reference detected in reports_to chain: {' -> '.join(cycle)}"
                )

        return errors

    def _find_cycle(self, start: str, reports_to: dict[str, str]) -> list[str] | None:
        """Find a cycle starting from the given node using Floyd's algorithm."""
        visited: set[str] = set()
        path: list[str] = []
        current = start

        while current in reports_to and current not in visited:
            visited.add(current)
            path.append(current)
            current = reports_to[current]
            if current == start:
                path.append(current)
                return path

        return None
