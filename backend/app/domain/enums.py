from enum import Enum


class RequestStatus(str, Enum):
    """Estados posibles de una solicitud de gasto."""
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    MANAGER_REVIEW = "MANAGER_REVIEW"
    FINANCE_REVIEW = "FINANCE_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    READY_FOR_PAYMENT = "READY_FOR_PAYMENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class RoleType(str, Enum):
    """Roles de usuario en el sistema."""
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"
    FINANCE_ANALYST = "FINANCE_ANALYST"
    FINANCE_ADMIN = "FINANCE_ADMIN"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"


class ExpenseCategory(str, Enum):
    """Categorías de gastos."""
    TRANSPORTATION = "TRANSPORTATION"
    TRAVEL = "TRAVEL"
    TOOLS = "TOOLS"
    EVENTS = "EVENTS"
    TRAINING = "TRAINING"
    RELATIONSHIPS = "RELATIONSHIPS"
    OTHER = "OTHER"
