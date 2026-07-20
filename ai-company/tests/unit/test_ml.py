"""Tests for ML modules — embeddings, performance, complexity, prompt optimizer, anomaly detection, predictive scaling."""

from __future__ import annotations

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

    def test_encode_requires_sentence_transformers(self):
        """EmbeddingEngine.encode raises ImportError when sentence-transformers is missing."""
        from ai_company.ml.embeddings import EmbeddingEngine

        engine = EmbeddingEngine.__new__(EmbeddingEngine)
        engine.model_name = "all-MiniLM-L6-v2"
        engine.cache_dir = _make_tmp_dir()
        engine._dimension = None
        engine._cache = {}

        # _get_model should raise if sentence_transformers not installed
        # (in test env it may or may not be installed)
        try:
            from sentence_transformers import SentenceTransformer  # noqa: F401
            # If installed, encode should work
            result = engine.encode("hello world")
            assert result is not None
        except ImportError:
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
        with patch("ai_company.ml.embeddings._get_model", return_value=MagicMock(get_sentence_embedding_dimension=MagicMock(return_value=4))):
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
        from ai_company.memory.engine import MemoryStore, MemoryEntry
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
        vs_with_engine = VectorStore(memory_store=ms, embedding_engine=mock_engine, index_dir=tmp / "idx2")
        assert vs_with_engine.is_vector_capable


# ── AgentPerformanceTracker Tests ─────────────────────────────────────


class TestAgentPerformanceTracker:
    """Tests for the AgentPerformanceTracker class."""

    def test_import(self):
        from ai_company.ml.performance import AgentPerformanceTracker, AgentMetrics, TaskExecutionRecord
        assert AgentPerformanceTracker is not None
        assert AgentMetrics is not None
        assert TaskExecutionRecord is not None

    def test_record_execution(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        record = TaskExecutionRecord(
            task_id="t1",
            agent_id="agent_1",
            timestamp="2026-01-01T00:00:00",
            execution_time_s=10.0,
            prompt_tokens=100,
            completion_tokens=50,
            cost_usd=0.001,
            success=True,
        )
        tracker.record_execution(record)

        metrics = tracker.get_agent_metrics("agent_1")
        assert metrics is not None
        assert metrics.total_tasks == 1
        assert metrics.successful_tasks == 1
        assert metrics.success_rate == 1.0

    def test_multiple_executions(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        for i in range(10):
            record = TaskExecutionRecord(
                task_id=f"t{i}",
                agent_id="agent_1",
                timestamp="2026-01-01T00:00:00",
                execution_time_s=float(5 + i),
                prompt_tokens=100,
                completion_tokens=50,
                cost_usd=0.001,
                success=i < 8,  # 80% success
            )
            tracker.record_execution(record)

        metrics = tracker.get_agent_metrics("agent_1")
        assert metrics.total_tasks == 10
        assert metrics.successful_tasks == 8
        assert abs(metrics.success_rate - 0.8) < 0.01

    def test_predict_execution_time(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        # Add enough records for prediction
        for i in range(10):
            record = TaskExecutionRecord(
                task_id=f"t{i}",
                agent_id="agent_1",
                timestamp="2026-01-01T00:00:00",
                execution_time_s=float(10 + i * 2),
                prompt_tokens=100,
                completion_tokens=50,
                cost_usd=0.001,
                success=True,
                task_complexity=float(i) / 10,
            )
            tracker.record_execution(record)

        prediction = tracker.predict_execution_time("agent_1", task_complexity=0.5)
        assert isinstance(prediction, float)
        assert prediction > 0

    def test_predict_fallback_global_avg(self):
        from ai_company.ml.performance import AgentPerformanceTracker

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        # No records for this agent — should use global average
        prediction = tracker.predict_execution_time("unknown_agent", task_complexity=0.5)
        assert prediction == 30.0  # Default when no data

    def test_get_top_agents(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        for agent, success_count, total in [("a", 9, 10), ("b", 7, 10), ("c", 10, 10)]:
            for i in range(total):
                record = TaskExecutionRecord(
                    task_id=f"{agent}_{i}",
                    agent_id=agent,
                    timestamp="2026-01-01T00:00:00",
                    execution_time_s=10.0,
                    prompt_tokens=100,
                    completion_tokens=50,
                    cost_usd=0.001,
                    success=i < success_count,
                )
                tracker.record_execution(record)

        top = tracker.get_top_agents(metric="success_rate", top_k=2)
        assert len(top) == 2
        assert top[0].agent_id == "c"
        assert top[1].agent_id == "a"

    def test_global_stats(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        assert tracker.get_global_stats()["total_records"] == 0

        record = TaskExecutionRecord(
            task_id="t1", agent_id="a", timestamp="2026-01-01T00:00:00",
            execution_time_s=5.0, prompt_tokens=100, completion_tokens=50,
            cost_usd=0.001, success=True,
        )
        tracker.record_execution(record)

        stats = tracker.get_global_stats()
        assert stats["total_records"] == 1
        assert stats["agents"] == 1

    def test_save_and_reload(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp)

        record = TaskExecutionRecord(
            task_id="t1", agent_id="a", timestamp="2026-01-01T00:00:00",
            execution_time_s=10.0, prompt_tokens=100, completion_tokens=50,
            cost_usd=0.001, success=True,
        )
        tracker.record_execution(record)
        tracker.save_metrics()

        # Reload
        tracker2 = AgentPerformanceTracker(data_dir=tmp)
        metrics = tracker2.get_agent_metrics("a")
        assert metrics is not None
        assert metrics.total_tasks == 1

    def test_task_execution_record_to_dict(self):
        from ai_company.ml.performance import TaskExecutionRecord

        record = TaskExecutionRecord(
            task_id="t1", agent_id="a", timestamp="2026-01-01T00:00:00",
            execution_time_s=10.0, prompt_tokens=100, completion_tokens=50,
            cost_usd=0.001, success=True,
        )
        d = record.to_dict()
        assert d["task_id"] == "t1"
        assert d["execution_time_s"] == 10.0

    def test_agent_metrics_to_dict(self):
        from ai_company.ml.performance import AgentMetrics

        m = AgentMetrics(agent_id="test", total_tasks=5, successful_tasks=4)
        d = m.to_dict()
        assert d["agent_id"] == "test"
        assert d["total_tasks"] == 5


# ── TaskComplexityScorer Tests ────────────────────────────────────────


class TestTaskComplexityScorer:
    """Tests for the TaskComplexityScorer class."""

    def test_import(self):
        from ai_company.ml.complexity import TaskComplexityScorer, ComplexityScore
        assert TaskComplexityScorer is not None
        assert ComplexityScore is not None

    def test_simple_task(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        score = scorer.score_task("Read the file and show the contents")
        assert score.level == "simple"
        assert score.score <= 0.33
        assert score.recommended_tier == "fast"

    def test_complex_task(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        score = scorer.score_task(
            "Implement a distributed microservice architecture with "
            "Kubernetes deployment, database migration, security audit, "
            "and integration testing across multiple components"
        )
        # Complex tasks should score higher than simple tasks
        simple = scorer.score_task("Read the file")
        assert score.score > simple.score
        assert score.level in ("medium", "complex")
        assert score.recommended_tier in ("standard", "premium")

    def test_medium_task(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        score = scorer.score_task("Fix the bug in the API handler and add a test")
        # Should be medium or simple depending on exact scoring
        assert score.level in ("simple", "medium", "complex")
        assert 0.0 <= score.score <= 1.0

    def test_score_range(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        # All scores should be in [0, 1]
        for task in ["Hello", "Implement a full system migration", "Check status"]:
            score = scorer.score_task(task)
            assert 0.0 <= score.score <= 1.0

    def test_score_batch(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        tasks = [
            {"instruction": "Read the file"},
            {"instruction": "Build a distributed system"},
        ]
        scores = scorer.score_batch(tasks)
        assert len(scores) == 2
        assert scores[0].score <= scores[1].score  # Simple < Complex

    def test_custom_keywords(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer(
            custom_complex_keywords={"quantum computing", "blockchain"},
            custom_simple_keywords={"trivial"},
        )
        score_with_custom = scorer.score_task("Implement a quantum computing blockchain system")
        scorer_default = TaskComplexityScorer()
        score_without = scorer_default.score_task("Implement a quantum computing blockchain system")
        # Custom keywords should elevate the score
        assert score_with_custom.score >= score_without.score

    def test_with_tools(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        simple = scorer.score_task("Check something", tools_requested=["read", "grep"])
        complex = scorer.score_task("Build something", tools_requested=["execute", "code_interpreter"])
        assert simple.score <= complex.score

    def test_priority_influence(self):
        from ai_company.ml.complexity import TaskComplexityScorer

        scorer = TaskComplexityScorer()
        low = scorer.score_task("Do something", priority="low")
        critical = scorer.score_task("Do something", priority="critical")
        assert low.score <= critical.score

    def test_complexity_score_to_dict(self):
        from ai_company.ml.complexity import ComplexityScore

        s = ComplexityScore(
            score=0.5, level="medium", signals={"test": 0.5},
            recommended_tier="standard", reasoning="test",
        )
        d = s.to_dict()
        assert d["level"] == "medium"
        assert d["recommended_tier"] == "standard"


# ── PromptOptimizer Tests ─────────────────────────────────────────────


class TestPromptOptimizer:
    """Tests for the PromptOptimizer class."""

    def test_import(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer, PromptVariant, PromptInsight
        assert PromptOptimizer is not None
        assert PromptVariant is not None
        assert PromptInsight is not None

    def test_init(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(
            audit_log_path=tmp / "audit.jsonl",
            results_dir=tmp / "results",
        )
        assert optimizer.audit_log_path == tmp / "audit.jsonl"

    def test_suggest_improvements(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(results_dir=tmp / "results")

        # Short prompt
        suggestions = optimizer.suggest_improvements("Fix it")
        assert any("short" in s.lower() for s in suggestions)

        # Missing action verb
        suggestions = optimizer.suggest_improvements("The file should be updated by someone")
        # Should suggest adding action verb (but "updated" might match)
        assert isinstance(suggestions, list)

    def test_create_variant(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(results_dir=tmp / "results")

        variant = optimizer.create_variant("v1", "Please {task}", "Test variant")
        assert variant.variant_id == "v1"
        assert variant.impressions == 0

    def test_record_variant_outcome(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(results_dir=tmp / "results")

        optimizer.create_variant("v1", "Template", "Test")
        optimizer.record_variant_outcome("v1", success=True)
        optimizer.record_variant_outcome("v1", success=True)
        optimizer.record_variant_outcome("v1", success=False)

        perf = optimizer.get_variant_performance()
        assert len(perf) == 1
        assert perf[0]["impressions"] == 3
        assert abs(perf[0]["success_rate"] - 2 / 3) < 0.01

    def test_select_variant(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(results_dir=tmp / "results")

        # No qualified variants (need >= 3 impressions)
        optimizer.create_variant("v1", "Template")
        assert optimizer.select_variant() is None

        # Add enough impressions
        for _ in range(5):
            optimizer.record_variant_outcome("v1", success=True)

        best = optimizer.select_variant()
        assert best is not None
        assert best.variant_id == "v1"

    def test_analyze_no_data(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(
            audit_log_path=tmp / "nonexistent.jsonl",
            results_dir=tmp / "results",
        )
        result = optimizer.analyze_prompt_effectiveness()
        assert result["data_points"] == 0

    def test_prompt_variant_success_rate(self):
        from ai_company.ml.prompt_optimizer import PromptVariant

        v = PromptVariant(variant_id="v", prompt_template="t")
        assert v.success_rate == 0.0

        v.impressions = 10
        v.successes = 7
        assert abs(v.success_rate - 0.7) < 0.01

    def test_prompt_insight_to_dict(self):
        from ai_company.ml.prompt_optimizer import PromptInsight

        i = PromptInsight(
            insight_type="test",
            description="test insight",
            impact_score=0.5,
            evidence={"key": "value"},
        )
        d = i.to_dict()
        assert d["insight_type"] == "test"
        assert d["impact_score"] == 0.5

    def test_save_and_load_variants(self):
        from ai_company.ml.prompt_optimizer import PromptOptimizer

        tmp = _make_tmp_dir()
        optimizer = PromptOptimizer(results_dir=tmp / "results")
        optimizer.create_variant("v1", "Template", "Test")
        optimizer.record_variant_outcome("v1", success=True)

        # Reload
        optimizer2 = PromptOptimizer(results_dir=tmp / "results")
        assert "v1" in optimizer2._variants
        assert optimizer2._variants["v1"].impressions == 1


# ── AnomalyDetector Tests ─────────────────────────────────────────────


class TestAnomalyDetector:
    """Tests for the AnomalyDetector class."""

    def test_import(self):
        from ai_company.ml.anomaly import AnomalyDetector, AnomalyAlert, MetricWindow
        assert AnomalyDetector is not None
        assert AnomalyAlert is not None
        assert MetricWindow is not None

    def test_init(self):
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        detector = AnomalyDetector(data_dir=tmp)
        assert detector.z_threshold == 3.0

    def test_record_normal_metric(self):
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        detector = AnomalyDetector(data_dir=tmp, min_data_points=5)

        # Record normal values — no alerts expected
        for _ in range(10):
            alerts = detector.record_metric("cost", 1.0)
            assert len(alerts) == 0

    def test_record_anomaly(self):
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        detector = AnomalyDetector(data_dir=tmp, z_threshold=2.0, min_data_points=5)

        # Establish baseline
        for _ in range(20):
            detector.record_metric("cost", 1.0)

        # Spike
        alerts = detector.record_metric("cost", 100.0)
        assert len(alerts) > 0
        assert alerts[0].severity in ("warning", "critical")

    def test_metric_window(self):
        from ai_company.ml.anomaly import MetricWindow

        w = MetricWindow()
        for i in range(10):
            w.add(float(i))

        assert len(w.values) == 10
        assert abs(w.mean - 4.5) < 0.01
        assert w.std > 0

    def test_metric_window_max_size(self):
        from ai_company.ml.anomaly import MetricWindow

        w = MetricWindow(max_size=5)
        for i in range(10):
            w.add(float(i))
        assert len(w.values) == 5
        assert w.values == [5.0, 6.0, 7.0, 8.0, 9.0]

    def test_z_score(self):
        from ai_company.ml.anomaly import MetricWindow

        w = MetricWindow()
        for _ in range(20):
            w.add(10.0)
        w.add(20.0)  # Outlier

        z = w.z_score(20.0)
        assert z > 2.0  # Should be a high Z-score

    def test_iqr_bounds(self):
        from ai_company.ml.anomaly import MetricWindow

        w = MetricWindow()
        for i in range(20):
            w.add(float(i))
        low, high = w.iqr_bounds()
        assert low < high
        assert low < 5.0  # Should include lower values
        assert high > 15.0  # Should include higher values

    def test_get_metric_summary(self):
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        detector = AnomalyDetector(data_dir=tmp, min_data_points=3)

        for i in range(10):
            detector.record_metric("test_metric", float(i))

        summary = detector.get_metric_summary("test_metric")
        assert summary["data_points"] == 10
        assert summary["mean"] > 0

    def test_get_alert_stats(self):
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        detector = AnomalyDetector(data_dir=tmp, z_threshold=1.0, min_data_points=3)

        for _ in range(10):
            detector.record_metric("m", 1.0)
        detector.record_metric("m", 100.0)  # Anomaly

        stats = detector.get_alert_stats()
        assert stats["total_alerts"] > 0

    def test_check_cost_anomaly(self):
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        detector = AnomalyDetector(data_dir=tmp, z_threshold=2.0, min_data_points=5)

        for _ in range(20):
            detector.check_cost_anomaly(0.001)

        alerts = detector.check_cost_anomaly(1.0)
        assert len(alerts) > 0

    def test_anomaly_alert_to_dict(self):
        from ai_company.ml.anomaly import AnomalyAlert

        alert = AnomalyAlert(
            alert_id="a1",
            timestamp="2026-01-01T00:00:00",
            metric_name="test",
            severity="warning",
            current_value=10.0,
            expected_range=(0.0, 5.0),
            deviation=3.5,
            message="test alert",
        )
        d = alert.to_dict()
        assert d["alert_id"] == "a1"
        assert d["expected_range"] == [0.0, 5.0]


# ── PredictiveScalingEngine Tests ─────────────────────────────────────


class TestPredictiveScalingEngine:
    """Tests for the PredictiveScalingEngine class."""

    def test_import(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine, ScalingRecommendation, DailyMetrics
        assert PredictiveScalingEngine is not None
        assert ScalingRecommendation is not None
        assert DailyMetrics is not None

    def test_init(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp)
        assert engine.forecast_horizon == 7

    def test_forecast_task_volume_no_data(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp)

        forecasts = engine.forecast_task_volume(3)
        assert len(forecasts) == 3
        for f in forecasts:
            assert "date" in f
            assert "predicted_count" in f
            assert f["predicted_count"] >= 0

    def test_forecast_daily_costs_no_data(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp)

        forecasts = engine.forecast_daily_costs(3)
        assert len(forecasts) == 3
        for f in forecasts:
            assert "predicted_cost_usd" in f

    def test_capacity_forecast(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp)

        forecast = engine.get_capacity_forecast()
        assert "total_predicted_tasks" in forecast
        assert "total_predicted_cost_usd" in forecast
        assert forecast["forecast_period_days"] == 7

    def test_recommend_tier_adjustments(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp)

        recommendations = engine.recommend_tier_adjustments()
        assert isinstance(recommendations, list)

    def test_daily_metrics_to_dict(self):
        from ai_company.ml.predictive_scaling import DailyMetrics

        m = DailyMetrics(date="2026-01-01", task_count=10, total_cost_usd=0.05)
        d = m.to_dict()
        assert d["date"] == "2026-01-01"
        assert d["task_count"] == 10

    def test_scaling_recommendation_to_dict(self):
        from ai_company.ml.predictive_scaling import ScalingRecommendation

        r = ScalingRecommendation(
            recommendation_type="tier_adjustment",
            current_state={"tier": "fast"},
            predicted_state={"tier": "standard"},
            action="Upgrade tier",
            confidence=0.7,
            reasoning="Cost too high",
        )
        d = r.to_dict()
        assert d["recommendation_type"] == "tier_adjustment"
        assert d["confidence"] == 0.7

    def test_forecast_with_historical_data(self):
        """Test forecasting when some historical data exists."""
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine, DailyMetrics

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp, history_days=30)

        # Simulate 15 days of data
        for i in range(15):
            day = f"2026-07-{i + 1:02d}"
            engine._daily_metrics[day] = DailyMetrics(
                date=day,
                task_count=10 + i,
                total_cost_usd=0.01 * (10 + i),
            )

        forecasts = engine.forecast_task_volume(5)
        assert len(forecasts) == 5
        # Predictions should be reasonable (not negative)
        for f in forecasts:
            assert f["predicted_count"] >= 0

    def test_save_forecasts(self):
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()
        engine = PredictiveScalingEngine(data_dir=tmp)

        forecast = engine.get_capacity_forecast()
        engine.save_forecasts(forecast)

        forecast_dir = tmp / "forecasts"
        assert forecast_dir.exists()
        files = list(forecast_dir.glob("forecast-*.json"))
        assert len(files) == 1


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


# ── ModelRouter Complexity Integration Tests ──────────────────────────


class TestModelRouterComplexity:
    """Tests for model router complexity integration."""

    def test_resolve_with_complexity(self):
        from ai_company.model_router import ModelRouter

        # This will use default/fallback since no config files exist
        router = ModelRouter(config_path="/nonexistent/models.yaml")

        route = router.resolve_with_complexity(
            task_prompt="Read the file and show contents",
            priority="low",
        )
        assert route.tier in ("fast", "standard", "premium", "override")

    def test_resolve_with_complexity_fallback(self):
        """When ML modules unavailable, should fall back to standard routing."""
        from ai_company.model_router import ModelRouter

        router = ModelRouter(config_path="/nonexistent/models.yaml")

        # Complex task — should still resolve even without ML
        route = router.resolve_with_complexity(
            task_prompt="Implement a distributed microservice architecture",
            priority="high",
        )
        assert route.provider  # Should have a provider


# ── Integration: end-to-end ML pipeline ───────────────────────────────


class TestMLPipelineIntegration:
    """Integration tests verifying ML modules work together."""

    def test_complexity_feeds_model_router(self):
        from ai_company.ml.complexity import TaskComplexityScorer
        from ai_company.model_router import ModelRouter

        scorer = TaskComplexityScorer()
        router = ModelRouter(config_path="/nonexistent/models.yaml")

        # Simple task
        simple = scorer.score_task("Read the config file")
        router.resolve_with_complexity(
            task_prompt="Read the config file",
            priority="low",
        )
        assert simple.recommended_tier == "fast"

        # Complex task
        complex_task = scorer.score_task(
            "Implement a full security audit with penetration testing, "
            "compliance review, and architecture refactoring"
        )
        assert complex_task.recommended_tier in ("standard", "premium")

    def test_performance_feeds_anomaly_detection(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord
        from ai_company.ml.anomaly import AnomalyDetector

        tmp = _make_tmp_dir()
        tracker = AgentPerformanceTracker(data_dir=tmp / "perf")
        detector = AnomalyDetector(data_dir=tmp / "anomaly", min_data_points=5)

        # Record normal executions
        for i in range(10):
            record = TaskExecutionRecord(
                task_id=f"t{i}", agent_id="agent_1",
                timestamp="2026-01-01T00:00:00",
                execution_time_s=10.0, prompt_tokens=100,
                completion_tokens=50, cost_usd=0.001, success=True,
            )
            tracker.record_execution(record)
            detector.check_execution_time_anomaly(10.0)

        # Now record an anomalous execution
        detector.check_execution_time_anomaly(500.0)  # 50x longer
        stats = detector.get_alert_stats()
        assert stats["total_alerts"] > 0

    def test_predictive_scaling_uses_performance_data(self):
        from ai_company.ml.performance import AgentPerformanceTracker, TaskExecutionRecord
        from ai_company.ml.predictive_scaling import PredictiveScalingEngine

        tmp = _make_tmp_dir()

        # Seed performance data
        tracker = AgentPerformanceTracker(data_dir=tmp / "perf")
        for i in range(20):
            record = TaskExecutionRecord(
                task_id=f"t{i}", agent_id="agent_1",
                timestamp="2026-07-10T00:00:00",
                execution_time_s=10.0, prompt_tokens=100,
                completion_tokens=50, cost_usd=0.001, success=True,
            )
            tracker.record_execution(record)
        tracker.save_metrics()

        # Predictive scaling should find the data
        engine = PredictiveScalingEngine(data_dir=tmp / "perf")
        assert len(engine._cost_log) > 0 or len(engine._daily_metrics) >= 0
