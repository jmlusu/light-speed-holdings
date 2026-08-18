"""Department service layer.

Base service plumbing plus the client-intake service (Offer B) and
the agent onboarding service with HITL gate integration. The
per-department service classes (marketing, sales, customer success, legal)
were removed as unused; department logic now runs through the
MessageBus + workflow engine.
"""

from ai_company.services.base import BaseService, ServiceResult
from ai_company.services.client_intake import ClientIntakeService, GovernanceGateError
from ai_company.services.onboarding import OnboardingService

__all__ = [
    "BaseService",
    "ServiceResult",
    "ClientIntakeService",
    "GovernanceGateError",
    "OnboardingService",
]
