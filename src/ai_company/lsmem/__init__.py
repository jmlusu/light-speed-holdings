"""LS-MEM — LightSpeed Memory Engine Package."""

from .audit import AuditEvent, AuditLogger
from .bridge import TYPE_MAPPING, ImportStats, MemoryStoreBridge, import_memory_store
from .classification import Classification, ClassificationLayer
from .engine import EngineConfig, LSMEMEngine, MemoryRecord
from .gateway import GatewayConfig, GatewayDecision, PermissionGateway
from .injector import InjectionContext, LSMemInjector, create_injector
from .redaction import LEGACY_REDACTION_TOKEN, REDACTION_TOKEN, SecretScanner
from .scoring import MemoryScorer, Tier
from .vector import OllamaVectorStore

__all__ = [
    "LSMEMEngine",
    "EngineConfig",
    "MemoryRecord",
    "SecretScanner",
    "REDACTION_TOKEN",
    "LEGACY_REDACTION_TOKEN",
    "MemoryScorer",
    "Tier",
    "Classification",
    "ClassificationLayer",
    "PermissionGateway",
    "GatewayDecision",
    "GatewayConfig",
    "AuditLogger",
    "AuditEvent",
    "MemoryStoreBridge",
    "import_memory_store",
    "ImportStats",
    "TYPE_MAPPING",
    "LSMemInjector",
    "InjectionContext",
    "create_injector",
    "OllamaVectorStore",
]

__version__ = "0.1.0"
