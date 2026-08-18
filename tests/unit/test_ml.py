"""Tests for ML modules — embeddings, performance, complexity, prompt optimizer, anomaly detection, predictive scaling."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

# ── Helpers ───────────────────────────────────────────────────────────


def _make_tmp_dir() -> Path:
    return Path(tempfile.mkdtemp())


# ── EmbeddingEngine Tests ─────────────────────────────────────────────


class TestEmbeddingEngine:
    """Tests for the EmbeddingEngine class."""

    def test_import(self):
        from ai_company.ml.embeddings import EmbeddingEngine

        assert EmbeddingEngine is not None

    def test_encode_requires_sentence_transformers(self, monkeypatch):
        """encode raises a friendly ImportError when sentence-transformers is missing.

        Fully hermetic: the lazy import is forced to fail deterministically
        regardless of whether sentence-transformers is installed, so the test
        never triggers a HuggingFace model download and never depends on run
        order (a previously cached model must not short-circuit the import
        path — see ``embeddings._get_model``).
        """
        import sys
        from types import ModuleType

        from ai_company.ml import embeddings
        from ai_company.ml.embeddings import EmbeddingEngine

        # Order-independence: clear any cached model global first.
        monkeypatch.setattr(embeddings, "_model", None)
        monkeypatch.setattr(embeddings, "_model_name", "")

        # Force `from sentence_transformers import SentenceTransformer` to fail
        # deterministically (module present but attribute missing).
        fake_st = ModuleType("sentence_transformers")
        monkeypatch.setitem(sys.modules, "sentence_transformers", fake_st)

        engine = EmbeddingEngine.__new__(EmbeddingEngine)
        engine.model_name = "all-MiniLM-L6-v2"
        engine.cache_dir = _make_tmp_dir()
        engine._dimension = None
        engine._cache = {}

        with pytest.raises(ImportError, match="sentence-transformers"):
            engine.encode("hello world")

    def test_cache_key_deterministic(self):
        from ai_company.ml.embeddings import EmbeddingEngine

        key1 = EmbeddingEngine._cache_key("hello world")
        key2 = EmbeddingEngine._cache_key("hello world")
        assert key1 == key2
        assert len(key1) == 32  # SHA-256 truncated

    def test_cache_key_unique(self):
        from ai_company.ml.embeddings import EmbeddingEngine

        key1 = EmbeddingEngine._cache_key("hello")
        key2 = EmbeddingEngine._cache_key("world")
        assert key1 != key2

    @patch("ai_company.ml.embeddings._get_model")
    def test_encode_with_mock(self, mock_get_model):
        """Test encode logic with a mocked sentence-transformer model."""
        from ai_company.ml.embeddings import EmbeddingEngine

        mock_model = MagicMock()
        mock_model.get_sentence_embedding_dimension.return_value = 384
        mock_model.encode.return_value = np.random.rand(1, 384).astype(np.float32)
        mock_get_model.return_value = mock_model

        engine = EmbeddingEngine(model_name="test-model")
        result = engine.encode("test text")
        assert result.shape == (384,)
        mock_model.encode.assert_called_once()

    @patch("ai_company.ml.embeddings._get_model")
    def test_encode_batch(self, mock_get_model):
        from ai_company.ml.embeddings import EmbeddingEngine

        mock_model = MagicMock()
        mock_model.get_sentence_embedding_dimension.return_value = 4
        mock_model.encode.return_value = np.random.rand(3, 4).astype(np.float32)
        mock_get_model.return_value = mock_model

        engine = EmbeddingEngine(model_name="test-model")
        result = engine.encode(["a", "b", "c"])
        assert result.shape == (3, 4)

    @patch("ai_company.ml.embeddings._get_model")
    def test_similarity(self, mock_get_model):
        from ai_company.ml.embeddings import EmbeddingEngine

        mock_model = MagicMock()
        mock_model.get_sentence_embedding_dimension.return_value = 4
        # Return identical embeddings for similarity = 1.0
        emb = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        mock_model.encode.return_value = emb.reshape(1, 4)
        mock_get_model.return_value = mock_model

        engine = EmbeddingEngine(model_name="test-model")
        sim = engine.similarity("hello", "world")
        assert abs(sim - 1.0) < 0.01

    def test_init_creates_cache_dir(self):
        tmp = _make_tmp_dir()
        cache_dir = tmp / "embeddings"
        # Patch _get_model to avoid import
        with patch(
            "ai_company.ml.embeddings._get_model",
            return_value=MagicMock(get_sentence_embedding_dimension=MagicMock(return_value=4)),
        ):
            from ai_company.ml.embeddings import EmbeddingEngine

            EmbeddingEngine(cache_dir=cache_dir)
            assert cache_dir.exists()


# ── VectorStore Tests ─────────────────────────────────────────────────


class TestVectorStore:
    """Tests for the VectorStore class."""

    def test_import(self):
        from ai_company.memory.vector_store import VectorStore

        assert VectorStore is not None

    def test_init(self):
        from ai_company.memory.engine import MemoryStore
        from ai_company.memory.vector_store import VectorStore

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        vs = VectorStore(memory_store=ms, index_dir=tmp / "index")
        assert not vs.is_vector_capable  # No engine provided
        assert vs.store is ms

    def test_fallback_search(self):
        from ai_company.memory.engine import MemoryStore
        from ai_company.memory.vector_store import VectorStore

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        ms.store("semantic", content="Python is a programming language", tags=["python"])
        ms.store("semantic", content="Java is also a language", tags=["java"])

        vs = VectorStore(memory_store=ms, index_dir=tmp / "index")
        results = vs.search("Python", memory_type="semantic")
        assert len(results) > 0
        assert "Python" in results[0][0].content

    def test_index_entry(self):
        from ai_company.memory.engine import MemoryEntry, MemoryStore
        from ai_company.memory.vector_store import VectorStore

        mock_engine = MagicMock()
        mock_engine.encode.return_value = np.random.rand(384).astype(np.float32)

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        vs = VectorStore(memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "index")

        entry = MemoryEntry(memory_type="semantic", content="test content")
        vs.index_entry(entry)
        assert entry.id in vs._index

    def test_index_all(self):
        from ai_company.memory.engine import MemoryStore
        from ai_company.memory.vector_store import VectorStore

        mock_engine = MagicMock()
        mock_engine.encode.return_value = np.random.rand(4).astype(np.float32)

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        ms.store("semantic", content="entry 1")
        ms.store("semantic", content="entry 2")

        vs = VectorStore(memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "index")
        count = vs.index_all("semantic")
        assert count >= 1  # At least one entry indexed
        assert len(vs._index) >= 1

    def test_is_vector_capable(self):
        from ai_company.memory.engine import MemoryStore
        from ai_company.memory.vector_store import VectorStore

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")

        vs_no_engine = VectorStore(memory_store=ms, index_dir=tmp / "idx1")
        assert not vs_no_engine.is_vector_capable

        mock_engine = MagicMock()
        vs_with_engine = VectorStore(
            memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "idx2"
        )
        assert vs_with_engine.is_vector_capable


# ── VectorStore Atomic Write Tests (ticket #60) ───────────────────────


class TestVectorStoreAtomicWrite:
    """Regression tests for atomic vector-index writes.

    The vector index must never appear on disk as a partially-written JSON
    file: saves go to a temp file that is fsynced and atomically renamed,
    so a crash or a failed serialization leaves the previous complete
    index intact.
    """

    def test_vector_save_load_roundtrip(self):
        from ai_company.memory.engine import MemoryEntry, MemoryStore
        from ai_company.memory.vector_store import VectorStore

        mock_engine = MagicMock()
        mock_engine.encode.return_value = np.random.rand(4).astype(np.float32)

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        vs = VectorStore(memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "index")

        entry = MemoryEntry(memory_type="semantic", content="round trip")
        vs.index_entry(entry)
        vs.save_index()

        index_file = vs.index_dir / "vector_index.json"
        assert index_file.exists()
        # On-disk content parses as complete JSON.
        data = json.loads(index_file.read_text(encoding="utf-8"))
        assert entry.id in data

        # A fresh store pointed at the same index directory reloads the index.
        vs2 = VectorStore(memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "index")
        assert entry.id in vs2._index

        # No temp-file litter is left behind.
        assert list(vs.index_dir.glob("*.tmp")) == []

    def test_vector_atomic_write_keeps_old_file_on_failure(self):
        from ai_company.memory.engine import MemoryEntry, MemoryStore
        from ai_company.memory.vector_store import VectorStore

        mock_engine = MagicMock()
        mock_engine.encode.return_value = np.random.rand(4).astype(np.float32)

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        vs = VectorStore(memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "index")

        entry = MemoryEntry(memory_type="semantic", content="first")
        vs.index_entry(entry)
        vs.save_index()
        index_file = vs.index_dir / "vector_index.json"
        original_bytes = index_file.read_bytes()
        assert original_bytes  # sanity: the first save produced a real file

        # Make the next serialization fail midway with garbage so the write
        # can never complete. The on-disk file must stay the previous
        # complete JSON rather than a partially-written one.
        entry2 = MemoryEntry(memory_type="semantic", content="second")
        vs.index_entry(entry2)

        def _corrupting_dump(data, f, **kwargs):
            f.write('{"broken": tru')  # partial garbage
            raise RuntimeError("simulated crash during json.dump")

        with (
            patch("ai_company.memory.vector_store.json.dump", side_effect=_corrupting_dump),
            pytest.raises(RuntimeError, match="simulated crash"),
        ):
            vs.save_index()

        # The target file is untouched: still the original complete JSON.
        assert index_file.read_bytes() == original_bytes
        json.loads(index_file.read_text(encoding="utf-8"))  # parses cleanly

        # No temp-file litter is left behind after the failed write.
        assert list(vs.index_dir.glob("*.tmp")) == []

        # A subsequent successful save still works and writes valid JSON.
        vs.save_index()
        data = json.loads(index_file.read_text(encoding="utf-8"))
        assert entry2.id in data


# ── Memory Engine Vector Search Integration Tests ─────────────────────


class TestMemoryEngineVectorIntegration:
    """Tests for memory engine + vector store integration."""

    def test_memory_store_init(self):
        from ai_company.memory.engine import MemoryStore

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        assert not ms.has_vector_search

    def test_memory_store_enable_vector_search(self):
        from ai_company.memory.engine import MemoryStore

        mock_engine = MagicMock()
        mock_engine.encode.return_value = np.random.rand(4).astype(np.float32)

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        ms.enable_vector_search(
            embedding_engine=mock_engine,
            index_dir=tmp / "index",
        )
        assert ms.has_vector_search

    def test_store_indexes_in_vector(self):
        from ai_company.memory.engine import MemoryStore

        mock_engine = MagicMock()
        mock_engine.encode.return_value = np.random.rand(4).astype(np.float32)

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        ms.enable_vector_search(
            embedding_engine=mock_engine,
            index_dir=tmp / "index",
        )

        entry = ms.store("semantic", content="test content")
        # Should have been indexed
        assert ms._vector_store is not None
        assert entry.id in ms._vector_store._index

    def test_recall_without_vector(self):
        from ai_company.memory.engine import MemoryStore

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        ms.store("semantic", content="Python rocks")

        results = ms.recall("semantic", query="Python", use_semantic=False)
        assert len(results) == 1
        assert "Python" in results[0].content

    def test_recall_with_vector_search(self):
        from ai_company.memory.engine import MemoryStore

        mock_engine = MagicMock()
        emb = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        mock_engine.encode.return_value = emb

        tmp = _make_tmp_dir()
        ms = MemoryStore(base_dir=tmp / "memory")
        ms.enable_vector_search(
            embedding_engine=mock_engine,
            index_dir=tmp / "index",
        )

        ms.store("semantic", content="Python is great")
        ms.store("semantic", content="Java is okay")

        results = ms.recall("semantic", query="Python", use_semantic=True, limit=2)
        assert len(results) > 0
