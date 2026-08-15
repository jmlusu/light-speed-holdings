"""Department service layer.

Base service plumbing plus the client-intake service (Offer B). The
per-department service classes (marketing, sales, customer success, legal,
hr) were removed as unused; department logic now runs through the
MessageBus + workflow engine.
"""

from ai_company.services.base import BaseService, ServiceResult
from ai_company.services.client_intake import ClientIntakeService, GovernanceGateError

__all__ = [
    "BaseService",
    "ServiceResult",
    "ClientIntakeService",
    "GovernanceGateError",
]
