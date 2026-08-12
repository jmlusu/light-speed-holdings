"""Department service layer.

Each department has a service class that provides business logic beyond
simple CRUD, integrates with the MessageBus for task delegation, and
writes outcomes to the memory engine.
"""

from ai_company.services.base import BaseService, ServiceResult
from ai_company.services.client_intake import ClientIntakeService, GovernanceGateError
from ai_company.services.customer_success import CustomerSuccessService
from ai_company.services.hr import HRService
from ai_company.services.legal import LegalService
from ai_company.services.marketing import MarketingService
from ai_company.services.sales import SalesService

__all__ = [
    "BaseService",
    "ServiceResult",
    "ClientIntakeService",
    "GovernanceGateError",
    "MarketingService",
    "SalesService",
    "CustomerSuccessService",
    "LegalService",
    "HRService",
]
