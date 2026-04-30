from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from abc import ABC, abstractmethod

from backend.app.domain.enums import RequestStatus, ExpenseCategory
from backend.app.domain.value_objects import Money, RequestTitle
from backend.app.domain.exceptions import InvalidStateTransition


class RequestState(ABC):
    """Clase abstracta para el patrón State."""

    @abstractmethod
    def transition(self, target_status: RequestStatus) -> "RequestState":
        """Transición a otro estado."""
        pass

    @abstractmethod
    def get_status(self) -> RequestStatus:
        """Retorna el estado actual."""
        pass


class SubmittedState(RequestState):
    """Estado: Solicitud creada/reenviada."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.SUBMITTED

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.MANAGER_REVIEW:
            return ManagerReviewState()
        elif target_status == RequestStatus.CANCELLED:
            return CancelledState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class ManagerReviewState(RequestState):
    """Estado: En revisión del Manager."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.MANAGER_REVIEW

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.APPROVED:
            return ApprovedState()
        elif target_status == RequestStatus.REJECTED:
            return RejectedState()
        elif target_status == RequestStatus.CHANGES_REQUESTED:
            return ChangesRequestedState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class ApprovedState(RequestState):
    """Estado: Aprobado."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.APPROVED

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.FINANCE_REVIEW:
            return FinanceReviewState()
        elif target_status == RequestStatus.READY_FOR_PAYMENT:
            return ReadyForPaymentState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class FinanceReviewState(RequestState):
    """Estado: En revisión de Finanzas."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.FINANCE_REVIEW

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.READY_FOR_PAYMENT:
            return ReadyForPaymentState()
        elif target_status == RequestStatus.REJECTED:
            return RejectedState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class ReadyForPaymentState(RequestState):
    """Estado: Listo para pago."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.READY_FOR_PAYMENT

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.PAID:
            return PaidState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class RejectedState(RequestState):
    """Estado: Rechazado."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.REJECTED

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.SUBMITTED:
            return SubmittedState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class ChangesRequestedState(RequestState):
    """Estado: Cambios solicitados."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.CHANGES_REQUESTED

    def transition(self, target_status: RequestStatus) -> RequestState:
        if target_status == RequestStatus.SUBMITTED:
            return SubmittedState()
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class PaidState(RequestState):
    """Estado: Pagado."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.PAID

    def transition(self, target_status: RequestStatus) -> RequestState:
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


class CancelledState(RequestState):
    """Estado: Cancelado."""

    def get_status(self) -> RequestStatus:
        return RequestStatus.CANCELLED

    def transition(self, target_status: RequestStatus) -> RequestState:
        raise InvalidStateTransition(
            f"No se puede transicionar de {self.get_status()} a {target_status}"
        )


@dataclass
class Request:
    """Entidad Request pura (sin ORM)."""
    id: Optional[int] = None
    employee_id: Optional[int] = None
    title: Optional[RequestTitle] = None
    description: str = ""
    amount: Optional[Money] = None
    category: ExpenseCategory = ExpenseCategory.OTHER
    receipt_url: Optional[str] = None
    state: RequestState = field(default_factory=SubmittedState)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    submitted_by_id: Optional[int] = None
    manager_id: Optional[int] = None
    finance_id: Optional[int] = None

    def __repr__(self) -> str:
        return f"Request(id={self.id}, title={self.title}, status={self.state.get_status()})"

    @property
    def status(self) -> RequestStatus:
        """Retorna el estado actual."""
        return self.state.get_status()

    def transition_to(self, target_status: RequestStatus) -> None:
        """Transiciona a un nuevo estado."""
        self.state = self.state.transition(target_status)
        self.updated_at = datetime.utcnow()


@dataclass
class Approval:
    """Entidad Approval para auditoría de aprobaciones."""
    id: Optional[int] = None
    request_id: Optional[int] = None
    approver_id: Optional[int] = None
    approval_type: str = ""  # MANAGER_REVIEW, FINANCE_REVIEW
    comment: Optional[str] = None
    approved_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AuditLog:
    """Entidad AuditLog para registro de cambios."""
    id: Optional[int] = None
    actor_id: Optional[int] = None
    entity_type: str = ""  # REQUEST, USER, etc
    entity_id: Optional[int] = None
    action: str = ""  # CREATE, UPDATE, APPROVE, REJECT
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    description: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"AuditLog(actor={self.actor_id}, action={self.action}, entity={self.entity_type}:{self.entity_id})"


@dataclass
class Notification:
    """Entidad Notification para notificaciones de usuarios."""
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: str = ""
    message: str = ""
    notification_type: str = ""  # REQUEST_CREATED, APPROVED, REJECTED, etc
    reference_id: Optional[int] = None
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None
