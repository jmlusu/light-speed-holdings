"""ML capabilities for AI Company Builder.

Provides embedding-based memory, performance modeling, task complexity
scoring, prompt optimization, anomaly detection, and predictive scaling.
"""

from ai_company.ml.embeddings import EmbeddingEngine
from ai_company.ml.performance import AgentPerformanceTracker
from ai_company.ml.complexity import TaskComplexityScorer
from ai_company.ml.prompt_optimizer import PromptOptimizer
from ai_company.ml.anomaly import AnomalyDetector
from ai_company.ml.predictive_scaling import PredictiveScalingEngine

__all__ = [
    "EmbeddingEngine",
    "AgentPerformanceTracker",
    "TaskComplexityScorer",
    "PromptOptimizer",
    "AnomalyDetector",
    "PredictiveScalingEngine",
]
