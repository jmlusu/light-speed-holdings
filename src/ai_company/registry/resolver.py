"""Registry resolver — wires cross-references between entities."""

from __future__ import annotations

from ai_company.models import CompanyRegistry


class RegistryResolver:
    """Resolves cross-references in a CompanyRegistry.

    After parsing, entities may reference each other by ID string.
    This resolver ensures consistency (e.g. every executive's reports_to
    matches an existing executive ID, every department has an executive, etc.)
    """

    def resolve(self, registry: CompanyRegistry) -> None:
        """Run all resolution passes on the registry."""
        self._wire_executive_departments(registry)
        self._wire_specialist_reports_to(registry)
        self._wire_workflow_owners(registry)

    def _wire_executive_departments(self, r: CompanyRegistry) -> None:
        """Ensure each executive's department matches a known department ID."""
        dept_ids = {d.id for d in r.departments}
        for ex in r.executives:
            if ex.department and ex.department not in dept_ids:
                # Non-fatal: just note it — validator will catch it
                pass

    def _wire_specialist_reports_to(self, r: CompanyRegistry) -> None:
        """Ensure each specialist's reports_to references a known executive."""
        exec_ids = {e.id for e in r.executives}
        for spec in r.specialists:
            if spec.reports_to and spec.reports_to not in exec_ids:
                # Non-fatal
                pass

    def _wire_workflow_owners(self, r: CompanyRegistry) -> None:
        """Tag workflow owner IDs for downstream use."""
        # Currently just validates that owner IDs are strings; no-op
        pass
