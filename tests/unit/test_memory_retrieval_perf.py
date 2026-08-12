"""Report-only performance benchmark for the memory retrieval path (ADR-011).

This suite is NOT a CI gate (posture: reported targets, not gates). It measures
the local cosine ``VectorStore`` retrieval path that T3's "sub-50ms retrieval"
touches: a populated ``MemoryStore`` with a stub embedding engine that exercises
the real cosine search + ranking over the in-memory index.

The embedding engine is stubbed (deterministic hash-based vectors) so the
benchmark measures *retrieval* latency — search, filtering, ranking — not model
encoding time. Results appear in the pytest-benchmark summary table in the CI
log; no latency assertion is made, so a slow run never fails the build.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import pytest

from ai_company.memory.engine import MemoryEntry, MemoryStore

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

pytest.importorskip("pytest_benchmark")

MEMORIES = 200
QUERY = "onboarding flow checklist for step three"


class _StubEmbedder:
    """Deterministic normalized embeddings — isolates retrieval, not encoding."""

    def __init__(self, dim: int = 32) -> None:
        self.dim = dim

    def encode(self, text: str) -> np.ndarray:
        digest = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
        rng = np.random.default_rng(digest % (2**31))
        vec = rng.standard_normal(self.dim).astype(np.float32)
        norm = float(np.linalg.norm(vec))
        return vec / norm if norm else vec


@pytest.mark.performance
def test_memory_retrieval_latency_report_only(tmp_path: Path, benchmark: BenchmarkFixture) -> None:
    """Local cosine retrieval latency over a 200-entry index (report-only)."""
    store = MemoryStore(base_dir=str(tmp_path / "memory"))
    for i in range(MEMORIES):
        store.store(
            "episodic",
            f"Interview note {i}: the onboarding flow needs a checklist for step {i % 8}.",
            agent_id="hr",
        )
    # Guarantee one identical-text entry so cosine similarity = 1.0 (deterministic hit).
    store.store("episodic", QUERY, agent_id="hr")

    store.enable_vector_search(
        embedding_engine=_StubEmbedder(),
        index_dir=str(tmp_path / "vector_index"),
    )
    assert store.has_vector_search

    def recall() -> list[MemoryEntry]:
        return store.recall("episodic", query=QUERY, limit=5, use_semantic=True)

    results = recall()
    assert len(results) >= 1

    out = benchmark(recall)
    assert len(out) == len(results)
