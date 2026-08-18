"""Unified search across agents, tasks, KPIs, and audit events.

Uses SQLite FTS5 for full-text search on tasks and audit events.
Agents are searched via the registry. KPIs are searched via stored metrics.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path

from ai_company.data.database import Database

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Unified search result item."""

    id: str
    title: str
    description: str
    entity_type: str
    url: str
    score: float


class SearchIndex:
    """Unified search index spanning agents, tasks, KPIs, and audit events."""

    def __init__(self, database: Database | None = None) -> None:
        self._db = database

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        """Run a unified search across all indexed entities."""
        results: list[SearchResult] = []
        start = time.time()

        # Search agents via registry
        agent_results = self._search_agents(query)
        results.extend(agent_results)

        # Search tasks via SQLite FTS5
        if self._db:
            task_results = self._search_tasks(query, limit)
            results.extend(task_results)

        # Search audit events via SQLite FTS5
        if self._db:
            audit_results = self._search_audit_events(query, limit)
            results.extend(audit_results)

        # Search KPIs
        kpi_results = self._search_kpis(query)
        results.extend(kpi_results)

        # Sort by score (highest first), limit
        results.sort(key=lambda r: r.score, reverse=True)
        results = results[:limit]

        took_ms = int((time.time() - start) * 1000)
        logger.debug("Search '%s' returned %d results in %dms", query, len(results), took_ms)
        return results

    def _search_agents(self, query: str) -> list[SearchResult]:
        """Search agents via the registry."""
        try:
            from ai_company.registry import load_registry
            registry = load_registry()
            company = registry
        except (ImportError, AttributeError, ValueError):
            return []

        results: list[SearchResult] = []
        query_lower = query.lower()

        # Search specialists
        for agent in company.specialists:
            name = agent.id or ""
            role = agent.seniority or ""
            dept_name = agent.department or ""

            score = 0.0
            if query_lower == name.lower() or query_lower in name.lower():
                score = 1.0
            elif query_lower in role.lower():
                score = 0.8
            elif query_lower in dept_name.lower():
                score = 0.6
            elif query_lower in name.lower() or query_lower in role.lower():
                score = 0.4

            if score > 0:
                results.append(SearchResult(
                    id=name,
                    title=name,
                    description=f"{role} in {dept_name}",
                    entity_type="agent",
                    url=f"/agents?agent={name}",
                    score=score,
                ))

        # Search executives
        for exec_ in company.executives:
            name = exec_.id or ""
            role = exec_.title or ""
            dept_name = exec_.department or ""

            score = 0.0
            if query_lower == name.lower() or query_lower in name.lower():
                score = 1.0
            elif query_lower in role.lower():
                score = 0.8
            elif query_lower in dept_name.lower():
                score = 0.6
            elif query_lower in name.lower() or query_lower in role.lower():
                score = 0.4

            if score > 0:
                results.append(SearchResult(
                    id=name,
                    title=name,
                    description=f"{role} in {dept_name}",
                    entity_type="agent",
                    url=f"/agents?agent={name}",
                    score=score,
                ))

        return results

    def _search_tasks(self, query: str, limit: int) -> list[SearchResult]:
        """Search tasks using SQLite FTS5."""
        if self._db is None:
            return []
        db = self._db
        try:
            import sqlite3
            rows = db.fetchall(
                """SELECT t.id, t.name, t.instruction, t.status, t.agent_id
                   FROM tasks t
                   JOIN tasks_fts f ON f.rowid = t.rowid
                   WHERE tasks_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (query, limit),
            )
        except (sqlite3.OperationalError, AttributeError):
            # FTS5 not available, fallback to LIKE
            rows = db.fetchall(
                """SELECT id, name, instruction, status, agent_id
                   FROM tasks
                   WHERE instruction LIKE ? OR name LIKE ?
                   ORDER BY created_at DESC
                   LIMIT ?""",
                (f"%{query}%", f"%{query}%", limit),
            )

        results: list[SearchResult] = []
        for row in rows:
            results.append(SearchResult(
                id=row["id"],
                title=row["name"] or row["instruction"][:50],
                description=f"Status: {row.get('status', 'unknown')} | Agent: {row.get('agent_id', 'unassigned')}",
                entity_type="task",
                url=f"/tasks?task={row['id']}",
                score=0.5,  # FTS rank not easily convertible
            ))

        return results

    def _search_audit_events(self, query: str, limit: int) -> list[SearchResult]:
        """Search audit events using SQLite FTS5."""
        if self._db is None:
            return []
        db = self._db
        try:
            import sqlite3
            rows = db.fetchall(
                """SELECT e.event_id, e.event_type, e.agent_id, e.task_id, e.timestamp
                   FROM audit_events e
                   JOIN audit_events_fts f ON f.rowid = e.rowid
                   WHERE audit_events_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (query, limit),
            )
        except (sqlite3.OperationalError, AttributeError):
            return []

        results: list[SearchResult] = []
        for row in rows:
            results.append(SearchResult(
                id=row["event_id"],
                title=f"{row['event_type']} by {row.get('agent_id', 'unknown')}",
                description=f"Task: {row.get('task_id', 'none')} | {row.get('timestamp', '')}",
                entity_type="audit",
                url=f"/audit?event={row['event_id']}",
                score=0.3,
            ))

        return results

    def _search_kpis(self, query: str) -> list[SearchResult]:
        """Search KPI definitions by keyword."""
        # Load from KPI config
        try:
            import yaml
            kpi_path = Path("config/company/kpis.yaml")
            if kpi_path.exists():
                with open(kpi_path) as f:
                    kpi_config = yaml.safe_load(f) or {}

                results: list[SearchResult] = []
                query_lower = query.lower()

                for dept_name, dept_kpis in kpi_config.items():
                    for kpi_name, kpi_def in dept_kpis.items():
                        name = kpi_name.lower()
                        desc = str(kpi_def.get("description", "")).lower()
                        unit = str(kpi_def.get("unit", "")).lower()

                        if query_lower in name or query_lower in desc or query_lower in unit:
                            results.append(SearchResult(
                                id=f"{dept_name}.{kpi_name}",
                                title=f"{dept_name} - {kpi_name}",
                                description=str(kpi_def.get("description", ""))[:100],
                                entity_type="kpi",
                                url=f"/kpis?dept={dept_name}",
                                score=0.4,
                            ))

                return results
        except (ImportError, yaml.YAMLError, OSError):
            pass
        return []
