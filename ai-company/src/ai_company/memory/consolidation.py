"""Memory consolidation scheduler — periodically deduplicates and prunes memory.

GAP-005 fix: wires MemoryStore.consolidate_all() and prune() into a
configurable periodic scheduler so memory doesn't grow unbounded.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ConsolidationConfig:
    """Configuration for memory consolidation scheduling."""

    # Run consolidation every N executor ticks (0 = disabled)
    tick_interval: int = 50
    # Trigger when any memory type exceeds this entry count
    entry_threshold: int = 500
    # Max age in days for episodic memories before pruning
    max_episodic_age_days: int = 90
    # Max entries per memory type (most-accessed wins)
    max_entries_per_type: int = 2000
    # Time-based interval in seconds (alternative to tick-based)
    time_interval_seconds: int = 3600


class ConsolidationScheduler:
    """Periodically runs memory consolidation and pruning.

    Can operate in two modes:
    - Tick-based: call ``on_tick()`` from the executor loop; consolidation
      runs every ``config.tick_interval`` ticks.
    - Time-based: runs in a background daemon thread at a fixed interval.

    Example::

        scheduler = ConsolidationScheduler(store, config)
        scheduler.start()  # background thread
        # ... later ...
        scheduler.stop()
    """

    def __init__(
        self,
        store: Any,
        config: ConsolidationConfig | None = None,
    ) -> None:
        self._store = store
        self._config = config or ConsolidationConfig()
        self._tick_count: int = 0
        self._last_consolidated: datetime | None = None
        self._running: bool = False
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    @property
    def last_consolidated(self) -> datetime | None:
        return self._last_consolidated

    @property
    def tick_count(self) -> int:
        return self._tick_count

    def on_tick(self) -> dict[str, int | str] | None:
        """Call from executor tick(). Runs consolidation if interval reached.

        Returns consolidation summary dict if consolidation ran, None otherwise.
        """
        self._tick_count += 1
        if self._should_consolidate():
            return self.run_once()
        return None

    def _should_consolidate(self) -> bool:
        """Check if consolidation should run based on tick count or thresholds."""
        config = self._config

        # Tick-based trigger
        if config.tick_interval > 0 and self._tick_count % config.tick_interval == 0:
            return True

        # Threshold-based trigger
        if self._store is not None:
            try:
                stats = self._store.stats()
                if any(count > config.entry_threshold for count in stats.values()):
                    return True
            except Exception:
                pass

        return False

    def run_once(self) -> dict[str, int | str]:
        """Execute one consolidation + prune cycle. Returns summary."""
        if self._store is None:
            return {"error": "no_store"}

        summary: dict[str, int | str] = {}
        try:
            # Prune first (reduces work for dedup)
            pruned = self._store.prune(
                max_age_days=self._config.max_episodic_age_days,
                max_entries_per_type=self._config.max_entries_per_type,
            )
            summary["entries_pruned"] = pruned

            # Then consolidate (dedup + aggregate)
            result = self._store.consolidate_all()
            summary.update(result)
            summary["consolidation_timestamp"] = 0  # Marker for "ran successfully"

            self._last_consolidated = datetime.now()
            logger.info(
                "Memory consolidation: pruned=%d dedup=%d aggregates=%d",
                pruned,
                result.get("semantic_duplicates_removed", 0),
                result.get("aggregates_created", 0),
            )
        except Exception:
            logger.debug("Memory consolidation failed", exc_info=True)
            summary["error"] = 1

        return summary

    def start(self) -> None:
        """Start time-based consolidation in a background daemon thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._run_loop,
            name="memory-consolidation",
            daemon=True,
        )
        self._thread.start()
        logger.info(
            "Consolidation scheduler started (interval=%ds)",
            self._config.time_interval_seconds,
        )

    def stop(self) -> None:
        """Stop the background consolidation loop."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        logger.info("Consolidation scheduler stopped")

    def _run_loop(self) -> None:
        """Background loop that runs consolidation at fixed intervals."""
        import time

        while self._running:
            time.sleep(self._config.time_interval_seconds)
            if self._running:
                self.run_once()

    def stats(self) -> dict[str, Any]:
        """Return scheduler status for monitoring."""
        return {
            "tick_count": self._tick_count,
            "last_consolidated": (
                self._last_consolidated.isoformat() if self._last_consolidated else None
            ),
            "running": self._running,
            "tick_interval": self._config.tick_interval,
            "time_interval_seconds": self._config.time_interval_seconds,
            "entry_threshold": self._config.entry_threshold,
        }
